"""
    Copyright (C) 2020 SunSpec Alliance

    Permission is hereby granted, free of charge, to any person obtaining a
    copy of this software and associated documentation files (the "Software"),
    to deal in the Software without restriction, including without limitation
    the rights to use, copy, modify, merge, publish, distribute, sublicense,
    and/or sell copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included
    in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
    THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
    IN THE SOFTWARE.
"""

import time
import uuid
import warnings
from collections import UserDict
from sunspec2 import mdef, device, mb
import sunspec2.modbus.modbus as modbus_client

TEST_NAME = 'test_name'

modbus_rtu_clients = {}


class SunSpecModbusClientError(Exception):
    pass


class SunSpecModbusValueError(Exception):
    pass


class SunSpecModbusClientTimeout(SunSpecModbusClientError):
    pass


class SunSpecModbusClientException(SunSpecModbusClientError):
    pass


class SunSpecModbusClientPoint(device.Point):

    def read(self):
        data = self.model.device.read(self.model.model_addr + self.offset, self.len)
        self.set_mb(data=data, dirty=False)

    def write(self):
        """Write the point to the physical device"""
        try:
            data = self.info.to_data(self.value, int(self.len) * 2)
        except Exception as e:
            raise SunSpecModbusValueError('Point value error for %s %s: %s' % (self.pdef.get(mdef.NAME), self.value,
                                                                               str(e)))
        model_addr = self.model.model_addr
        point_offset = self.offset
        addr = model_addr + point_offset
        self.model.device.write(addr, data)
        self.dirty = False


class SunSpecModbusClientGroup(device.Group):

    def __init__(self, gdef=None, model=None, model_offset=0, group_len=0, data=None, data_offset=0, group_class=None,
                 point_class=None, index=None):

        device.Group.__init__(self, gdef=gdef, model=model, model_offset=model_offset, group_len=group_len,
                              data=data, data_offset=data_offset, group_class=group_class, point_class=point_class,
                              index=index)

    def read(self, len=None):
        if len is None:
            len = self.len
        # check if currently connected
        connected = self.model.device.is_connected()
        if not connected:
            self.model.device.connect()

        if self.access_regions:
            data = bytearray()
            for region in self.access_regions:
                data += self.model.device.read(self.model.model_addr + self.offset + region[0], region[1])
            data = bytes(data)
        else:
            data = self.model.device.read(self.model.model_addr + self.offset, len)
        self.set_mb(data=data, dirty=False)

        # disconnect if was not connected
        if not connected:
            self.model.device.disconnect()

    def write(self):
        start_addr = next_addr = self.model.model_addr + self.offset
        data = b''
        start_addr, next_addr, data = self.write_points(start_addr, next_addr, data)
        if data:
            self.model.device.write(start_addr, data)

    def write_points(self, start_addr=None, next_addr=None, data=None):
        """
        Write all points that have been modified since the last write operation to the physical device
        """

        for name, point in self.points.items():
            model_addr = self.model.model_addr
            point_offset = point.offset
            point_addr = model_addr + point_offset
            if data and (not point.dirty or point_addr != next_addr):
                self.model.device.write(start_addr, data)
                data = b''
            if point.dirty:
                point_len = point.len
                try:
                    point_data = point.info.to_data(point.value, int(point_len) * 2)
                except Exception as e:
                    raise SunSpecModbusValueError('Point value error for %s %s: %s' % (name, point.value, str(e)))
                if not data:
                    start_addr = point_addr
                next_addr = point_addr + point_len
                data += point_data
                point.dirty = False

        for name, group in self.groups.items():
            if isinstance(group, list):
                for g in group:
                    start_addr, next_addr, data = g.write_points(start_addr, next_addr, data)
            else:
                start_addr, next_addr, data = group.write_points(start_addr, next_addr, data)

        return start_addr, next_addr, data


class SunSpecModbusClientModel(SunSpecModbusClientGroup):
    def __init__(self, model_id=None, model_addr=0, model_len=0, model_def=None, data=None, mb_device=None,
                 group_class=SunSpecModbusClientGroup, point_class=SunSpecModbusClientPoint):
        self.model_id = model_id
        self.model_addr = model_addr
        self.model_len = model_len
        self.model_def = model_def
        self.error_info = ''
        self.mid = None
        self.device = mb_device
        self.model = self

        gdef = None
        try:
            if self.model_def is None:
                self.model_def = device.get_model_def(model_id)
            if self.model_def is not None:
                gdef = self.model_def.get(mdef.GROUP)
        except Exception as e:
            self.add_error(str(e))

        # determine largest point index that contains a group len
        group_len_points_index = mdef.get_group_len_points_index(gdef)
        # if data len < largest point index that contains a group len, read the rest of the point data
        data_regs = len(data)/2
        remaining = group_len_points_index - data_regs
        if remaining > 0:
            points_data = self.device.read(self.model_addr + data_regs, remaining)
            data += points_data

        SunSpecModbusClientGroup.__init__(self, gdef=gdef, model=self.model, model_offset=0, group_len=self.model_len,
                                          data=data, data_offset=0, group_class=group_class, point_class=point_class)

        if self.model_len is not None:
            self.len = self.model_len

        if self.model_len and self.len:
            if self.model_len != self.len:
                self.add_error('Model error: Discovered length %s does not match computed length %s' %
                               (self.model_len, self.len))

    def add_error(self, error_info):
        self.error_info = '%s%s\n' % (self.error_info, error_info)

    def read(self, len=None):
        SunSpecModbusClientGroup.read(self, len=self.len + 2)


class SunSpecModbusClientUnit(device.Device):
    """A device proxy that represents a specific unit ID on a parent device.

    This class acts like a regular Device but delegates all Modbus communication
    to the parent device using the specified unit ID. The parent device handles
    all connection management.
    """

    def __init__(self, parent_device, unit_id, model_class=SunSpecModbusClientModel):
        device.Device.__init__(self, model_class=model_class)
        self.parent_device = parent_device
        self.unit_id = unit_id
        self.did = f"{parent_device.did}_unit_{unit_id}"

    def is_connected(self):
        """Check if the parent device is connected."""
        return self.parent_device.is_connected()

    def read(self, addr, count):
        """Read from this unit using the parent device's read_unit method."""
        return self.parent_device.read_unit(self.unit_id, addr, count)

    def write(self, addr, data):
        """Write to this unit using the parent device's write_unit method."""
        return self.parent_device.write_unit(self.unit_id, addr, data)


class SunSpecModbusClientUnitCollection(UserDict):
    """A collection that provides access to different unit IDs as device-like objects.

    Units are only available after being scanned with scan_units().

    Usage:
        # Scan units to discover their models
        d.scan_units([1, 2, 3])

        # Access unit models through the Units collection
        d.Units[1].common[0].Mn.value       # Access unit 1's common model
        d.Units[2].DERVoltVar[0].Ena.value  # Access unit 2's DERVoltVar model

        # Read/write directly to a unit
        data = d.Units[3].read(40000, 10)
        d.Units[3].write(40100, data)

        # Accessing unscanned units raises KeyError
        d.Units[99]  # Raises: KeyError: "Unit 99 has not been scanned. Use scan_units([99]) first."
    """

    def __init__(self, parent_device):
        super().__init__()
        self.parent_device = parent_device

    def __getitem__(self, unit_id):
        """Get a SunSpecModbusClientUnit for the specified unit ID.

        Raises KeyError if the unit has not been scanned yet.
        """
        if unit_id not in self.data:
            raise KeyError(f"Unit {unit_id} has not been scanned. Use scan_units([{unit_id}]) first.")
        return self.data[unit_id]

    def _create_unit(self, unit_id):
        """Internal method to create a unit device during scanning."""
        if unit_id not in self.data:
            self.data[unit_id] = SunSpecModbusClientUnit(
                self.parent_device,
                unit_id,
                model_class=self.parent_device.model_class
            )
        return self.data[unit_id]


class SunSpecModbusClientDevice(device.Device):
    def __init__(self, model_class=SunSpecModbusClientModel):
        device.Device.__init__(self, model_class=model_class)
        self.did = str(uuid.uuid4())
        self.retry_count = 2
        self.base_addr_list = [40000, 0, 50000]
        self.base_addr = None
        self.Units = SunSpecModbusClientUnitCollection(self)

    def connect(self):
        pass

    def disconnect(self):
        pass

    def is_connected(self):
        return True

    def close(self):
        pass

    # must be overridden by Modbus protocol implementation
    def read(self, addr, count):
        return ''

    # must be overridden by Modbus protocol implementation
    def write(self, addr, data):
        return

    # must be overridden by Modbus protocol implementation
    def read_unit(self, unit_id, addr, count):
        """Read Modbus device registers using a specific unit ID.

        Parameters:
            unit_id :
                Modbus Unit Identifier to use for this request.
            addr :
                Starting Modbus address.
            count :
                Read length in Modbus registers.
        Returns:
            Byte string containing register contents.
        """
        return ''

    # must be overridden by Modbus protocol implementation
    def write_unit(self, unit_id, addr, data):
        """Write Modbus device registers using a specific unit ID.

        Parameters:
            unit_id :
                Modbus Unit Identifier to use for this request.
            addr :
                Starting Modbus address.
            data :
                Byte string containing register contents.
        """
        return

    def scan(self, progress=None, delay=None, connect=True, full_model_read=True):
        """Scan all the models of the physical device and create the
        corresponding model objects within the device object based on the
        SunSpec model definitions.

        This method scans the default unit ID and adds models directly to the device.
        """
        self.base_addr = None
        self.delete_models()

        # Use scan_units to scan the default unit ID
        # This will populate both the Units collection and the main device
        self.scan_units([self.unit_id], progress=progress, delay=delay,
                       connect=connect, full_model_read=full_model_read)

    def scan_units(self, unit_ids, progress=None, delay=None, connect=True, full_model_read=True):
        """Scan multiple unit IDs and create corresponding unit objects with their models.

        This method scans each specified unit ID for SunSpec models and creates
        SunSpecModbusClientUnit objects that can be accessed via the Units collection.

        Parameters:
            unit_ids :
                List of Modbus Unit Identifiers to scan.
            progress :
                Progress callback function.
            delay :
                Delay between operations in seconds.
            connect :
                Whether to connect/disconnect automatically.
            full_model_read :
                Whether to perform full model reads during scan.

        Example:
            # Scan units 1, 2, and 3
            d.scan_units([1, 2, 3])

            # Access models from different units
            unit1_common = d.Units[1].common[0]
            unit2_inverter = d.Units[2].inverter[0]
        """
        if not isinstance(unit_ids, (list, tuple)):
            unit_ids = [unit_ids]

        connected = False
        if connect:
            self.connect()
            connected = True

        try:
            for unit_id in unit_ids:
                if progress is not None:
                    cont = progress(f'Scanning unit {unit_id}')
                    if not cont:
                        break

                self._scan_single_unit(unit_id, progress, delay, full_model_read)

        finally:
            if connected:
                self.disconnect()

    def _scan_single_unit(self, unit_id, progress=None, delay=None, full_model_read=True):
        """Scan a single unit ID and populate its models."""
        base_addr = None
        data = ''
        error = ''

        # Get or create the unit device for this unit ID
        unit_device = self.Units._create_unit(unit_id)

        # Clean up any existing models in the unit device before scanning
        unit_device.delete_models()

        if delay is not None:
            time.sleep(delay)

        error_dict = {}
        if base_addr is None:
            for addr in self.base_addr_list:
                error_dict[addr] = ''
                try:
                    data = self.read_unit(unit_id, addr, 3)
                    if data:
                        if data[:4] == b'SunS':
                            base_addr = addr
                            break
                        else:
                            error_dict[addr] = 'Device responded - not SunSpec register map'
                    else:
                        error_dict[addr] = 'Data time out'
                except SunSpecModbusClientError as e:
                    error_dict[addr] = str(e)
                except modbus_client.ModbusClientTimeout as e:
                    error_dict[addr] = str(e)
                except modbus_client.ModbusClientException as e:
                    error_dict[addr] = str(e)
                except Exception as e:
                    error_dict[addr] = str(e)

                if delay is not None:
                    time.sleep(delay)

        error = f'Error scanning SunSpec base addresses for unit {unit_id}. \n'
        for k, v in error_dict.items():
            error += 'Base address %s error = %s. \n' % (k, v)

        if base_addr is not None:
            model_id_data = data[4:6]
            model_id = mb.data_to_u16(model_id_data)
            addr = base_addr + 2

            mid = 0
            while model_id != mb.SUNS_END_MODEL_ID:
                # read model and model len separately due to some devices not supplying
                # count for the end model id
                model_len_data = self.read_unit(unit_id, addr + 1, 1)
                if model_len_data and len(model_len_data) == 2:
                    if progress is not None:
                        cont = progress(f'Scanning unit {unit_id} model {model_id}')
                        if not cont:
                            raise SunSpecModbusClientError('Device scan terminated')
                    model_len = mb.data_to_u16(model_len_data)

                    # read model data and add to the unit device
                    model_data = model_id_data + model_len_data
                    model = self.model_class(model_id=model_id, model_addr=addr, model_len=model_len, data=model_data,
                                             mb_device=unit_device)
                    if full_model_read and model.model_def:
                        model.read()
                    model.mid = f'{unit_device.did}_{mid}'
                    mid += 1
                    unit_device.add_model(model)

                    # If this is the default unit, also add the same model to the main device
                    if unit_id == self.unit_id:
                        # Add the same model instance to the main device
                        # This ensures both the unit and main device share the exact same data
                        self.add_model(model)

                    addr += model_len + 2
                    model_id_data = self.read_unit(unit_id, addr, 1)
                    if model_id_data and len(model_id_data) == 2:
                        model_id = mb.data_to_u16(model_id_data)
                    else:
                        break
                else:
                    break

                if delay is not None:
                    time.sleep(delay)

        else:
            raise SunSpecModbusClientError(error)

class SunSpecModbusClientDeviceTCP(SunSpecModbusClientDevice):
    """Provides access to a Modbus RTU device.
    Parameters:
        unit_id :
            Modbus Unit Identifier.
        ipaddr :
            IP address of the Modbus TCP device.
        ipport :
            Port number for Modbus TCP. Default is 502 if not specified.
        timeout :
            Modbus request timeout in seconds. Fractional seconds are permitted
            such as .5.
        ctx :
            Context variable to be used by the object creator. Not used by the
            modbus module.
        trace_func :
            Trace function to use for detailed logging. No detailed logging is
            perform is a trace function is not supplied.
        max_count :
            Maximum register count for a single Modbus request.
        max_write_count :
            Maximum register count for a single Modbus write request.
        model_class :
            Model class to use for creating models in the device. Default is
            :class:`sunspec2.modbus.client.SunSpecModbusClientModel`.
        slave_id : [DEPRECATED] Use unit_id instead.
    Raises:
        SunSpecModbusClientError: Raised for any general modbus client error.
        SunSpecModbusClientTimeoutError: Raised for a modbus client request timeout.
        SunSpecModbusClientException: Raised for an exception response to a modbus
            client request.
    """

    def __init__(self, unit_id=1, ipaddr='127.0.0.1', ipport=502, timeout=None, ctx=None, trace_func=None,
                 max_count=modbus_client.REQ_COUNT_MAX, max_write_count=modbus_client.REQ_WRITE_COUNT_MAX,
                 model_class=SunSpecModbusClientModel, slave_id=None):
        SunSpecModbusClientDevice.__init__(self, model_class=model_class)
        if unit_id == 1 and slave_id is not None:
            unit_id = slave_id
        if slave_id is not None:
            warnings.warn(
                "The 'slave_id' parameter is deprecated and will be removed in a future version. Use 'unit_id' instead.",
                DeprecationWarning,
                stacklevel=2
            )
        self.unit_id = unit_id
        self.ipaddr = ipaddr
        self.ipport = ipport
        self.timeout = timeout
        self.ctx = ctx
        self.socket = None
        self.trace_func = trace_func
        self.max_count = max_count
        self.max_write_count = max_write_count

        self.client = modbus_client.ModbusClientTCP(unit_id=unit_id, ipaddr=ipaddr, ipport=ipport, timeout=timeout,
                                                    ctx=ctx, trace_func=trace_func,
                                                    max_count=modbus_client.REQ_COUNT_MAX,
                                                    max_write_count=modbus_client.REQ_WRITE_COUNT_MAX)

        if self.client is None:
            raise SunSpecModbusClientError('No modbus tcp client set for device')

    def connect(self, timeout=None):
        self.client.connect(timeout)

    def disconnect(self):
        self.client.disconnect()

    def is_connected(self):
        return self.client.is_connected()

    def read(self, addr, count, op=modbus_client.FUNC_READ_HOLDING):
        """Read Modbus device registers using the default unit ID."""
        return self.read_unit(self.unit_id, addr, count, op)

    def write(self, addr, data):
        """Write Modbus device registers using the default unit ID."""
        return self.write_unit(self.unit_id, addr, data)

    def read_unit(self, unit_id, addr, count, op=modbus_client.FUNC_READ_HOLDING):
        """Read Modbus device registers using a specific unit ID.

        Parameters:
            unit_id :
                Modbus Unit Identifier to use for this request.
            addr :
                Starting Modbus address.
            count :
                Read length in Modbus registers.
            op :
                Modbus function code for request.
        Returns:
            Byte string containing register contents.
        """
        return self.client.read(addr, count, op, unit_id=unit_id)

    def write_unit(self, unit_id, addr, data):
        """Write Modbus device registers using a specific unit ID.

        Parameters:
            unit_id :
                Modbus Unit Identifier to use for this request.
            addr :
                Starting Modbus address.
            data :
                Byte string containing register contents.
        """
        return self.client.write(addr, data, unit_id=unit_id)


class SunSpecModbusClientDeviceRTU(SunSpecModbusClientDevice):
    """Provides access to a Modbus RTU device.
    Parameters:
        unit_id :
            Modbus Unit Identifier.
        name :
            Name of the serial port such as 'com4' or '/dev/ttyUSB0'.
        baudrate :
            Baud rate such as 9600 or 19200. Default is 9600 if not specified.
        parity :
            Parity. Possible values:
                :const:`sunspec.core.modbus.client.PARITY_NONE`,
                :const:`sunspec.core.modbus.client.PARITY_EVEN` Defaulted to
                :const:`PARITY_NONE`.
        timeout :
            Modbus request timeout in seconds. Fractional seconds are permitted
            such as .5.
        ctx :
            Context variable to be used by the object creator. Not used by the
            modbus module.
        trace_func :
            Trace function to use for detailed logging. No detailed logging is
            perform is a trace function is not supplied.
        max_count :
            Maximum register count for a single Modbus request.
        slave_id : [DEPRECATED] Use unit_id instead.
    Raises:
        SunSpecModbusClientError: Raised for any general modbus client error.
        SunSpecModbusClientTimeoutError: Raised for a modbus client request timeout.
        SunSpecModbusClientException: Raised for an exception response to a modbus
            client request.
    """

    def __init__(self, unit_id=None, name=None, baudrate=None, parity=None, timeout=None, ctx=None, trace_func=None,
                 max_count=modbus_client.REQ_COUNT_MAX, max_write_count=modbus_client.REQ_WRITE_COUNT_MAX,
                 model_class=SunSpecModbusClientModel, slave_id=None):
        # test if this super class init is needed
        SunSpecModbusClientDevice.__init__(self, model_class=model_class)
        # Backward compatibility for slave_id
        if unit_id is not None:
            self.unit_id = unit_id
        elif slave_id is not None:
            self.unit_id = slave_id
        else:
            raise ValueError("unit_id must be provided")
        if name is None:
            raise ValueError("name must be provided")
        if slave_id is not None:
            warnings.warn(
                "The 'slave_id' parameter is deprecated and will be removed in a future version. Use 'unit_id' instead.",
                DeprecationWarning,
                stacklevel=2
            )
        self.name = name
        self.client = None
        self.ctx = ctx
        self.trace_func = trace_func
        self.max_count = max_count
        self.max_write_count = max_write_count

        self.client = modbus_client.modbus_rtu_client(name, baudrate, parity, timeout)
        if self.client is None:
            raise SunSpecModbusClientError('No modbus rtu client set for device')
        self.client.add_device(self.unit_id, self)

    def open(self):
        self.client.open()

    def close(self):
        """Close the device. Called when device is no longer in use.
        """

        if self.client:
            self.client.remove_device(self.unit_id)

    def read(self, addr, count, op=modbus_client.FUNC_READ_HOLDING):
        """Read Modbus device registers using the default unit ID."""
        return self.read_unit(self.unit_id, addr, count, op)

    def write(self, addr, data):
        """Write Modbus device registers using the default unit ID."""
        return self.write_unit(self.unit_id, addr, data)

    def read_unit(self, unit_id, addr, count, op=modbus_client.FUNC_READ_HOLDING):
        """Read Modbus device registers using a specific unit ID.

        Parameters:
            unit_id :
                Modbus Unit Identifier to use for this request.
            addr :
                Starting Modbus address.
            count :
                Read length in Modbus registers.
            op :
                Modbus function code for request.
        Returns:
            Byte string containing register contents.
        """
        return self.client.read(unit_id, addr, count, op=op, max_count=self.max_count)

    def write_unit(self, unit_id, addr, data):
        """Write Modbus device registers using a specific unit ID.

        Parameters:
            unit_id :
                Modbus Unit Identifier to use for this request.
            addr :
                Starting Modbus address.
            data :
                Byte string containing register contents.
        """
        return self.client.write(unit_id, addr, data, max_write_count=self.max_write_count)
