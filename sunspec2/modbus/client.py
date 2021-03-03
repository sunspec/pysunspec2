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
import sunspec2.mdef as mdef
import sunspec2.device as device
import sunspec2.mb as mb
import sunspec2.modbus.modbus as modbus_client

TEST_NAME = 'test_name'

modbus_rtu_clients = {}


class SunSpecModbusClientError(Exception):
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

        data = self.info.to_data(self.value, int(self.len) * 2)
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

    def read(self):
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
            data = self.model.device.read(self.model.model_addr + self.offset, self.len)
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
                point_data = point.info.to_data(point.value, int(point_len) * 2)
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


class SunSpecModbusClientDevice(device.Device):
    def __init__(self, model_class=SunSpecModbusClientModel):
        device.Device.__init__(self, model_class=model_class)
        self.did = str(uuid.uuid4())
        self.retry_count = 2
        self.base_addr_list = [0, 40000, 50000]
        self.base_addr = None

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

    def scan(self, progress=None, delay=None, connect=True):
        """Scan all the models of the physical device and create the
        corresponding model objects within the device object based on the
        SunSpec model definitions.
        """

        data = error = ''
        connected = False

        if connect:
            self.connect()
            connected = True

            if delay is not None:
                time.sleep(delay)

        if self.base_addr is None:
            for addr in self.base_addr_list:
                try:
                    data = self.read(addr, 3)
                    if data[:4] == b'SunS':
                        self.base_addr = addr
                        break
                    else:
                        error = 'Device responded - not SunSpec register map'
                except SunSpecModbusClientError as e:
                    if not error:
                        error = str(e)
                except modbus_client.ModbusClientException:
                    pass

                if delay is not None:
                    time.sleep(delay)

        if self.base_addr is not None:
            model_id_data = data[4:6]
            model_id = mb.data_to_u16(model_id_data)
            addr = self.base_addr + 2

            mid = 0
            while model_id != mb.SUNS_END_MODEL_ID:
                # read model and model len separately due to some devices not supplying
                # count for the end model id
                model_len_data = self.read(addr + 1, 1)
                if model_len_data and len(model_len_data) == 2:
                    if progress is not None:
                        cont = progress('Scanning model %s' % (model_id))
                        if not cont:
                            raise SunSpecModbusClientError('Device scan terminated')
                    model_len = mb.data_to_u16(model_len_data)

                    # read model data
                    ### model_data = self.read(addr, model_len + 2)
                    model_data = model_id_data + model_len_data
                    model = self.model_class(model_id=model_id, model_addr=addr, model_len=model_len, data=model_data,
                                             mb_device=self)
                    model.read()
                    model.mid = '%s_%s' % (self.did, mid)
                    mid += 1
                    self.add_model(model)

                    addr += model_len + 2
                    model_id_data = self.read(addr, 1)
                    if model_id_data and len(model_id_data) == 2:
                        model_id = mb.data_to_u16(model_id_data)
                    else:
                        break
                else:
                    break

                if delay is not None:
                    time.sleep(delay)

        else:
            if not error:
                error = 'Unknown error'
            raise SunSpecModbusClientError(error)

        if connected:
            self.disconnect()


class SunSpecModbusClientDeviceTCP(SunSpecModbusClientDevice):
    def __init__(self, slave_id=1, ipaddr='127.0.0.1', ipport=502, timeout=None, ctx=None, trace_func=None,
                 max_count=modbus_client.REQ_COUNT_MAX, test=False, model_class=SunSpecModbusClientModel):
        SunSpecModbusClientDevice.__init__(self, model_class=model_class)
        self.slave_id = slave_id
        self.ipaddr = ipaddr
        self.ipport = ipport
        self.timeout = timeout
        self.ctx = ctx
        self.socket = None
        self.trace_func = trace_func
        self.max_count = max_count

        self.client = modbus_client.ModbusClientTCP(slave_id=slave_id, ipaddr=ipaddr, ipport=ipport, timeout=timeout,
                                                    ctx=ctx, trace_func=trace_func,
                                                    max_count=modbus_client.REQ_COUNT_MAX, test=test)
        if self.client is None:
            raise SunSpecModbusClientError('No modbus tcp client set for device')

    def connect(self):
        self.client.connect()

    def disconnect(self):
        self.client.disconnect()

    def is_connected(self):
        return self.client.is_connected()

    def read(self, addr, count, op=modbus_client.FUNC_READ_HOLDING):
        return self.client.read(addr, count, op)

    def write(self, addr, data):
        return self.client.write(addr, data)


class SunSpecModbusClientDeviceRTU(SunSpecModbusClientDevice):
    """Provides access to a Modbus RTU device.
    Parameters:
        slave_id :
            Modbus slave id.
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
    Raises:
        SunSpecModbusClientError: Raised for any general modbus client error.
        SunSpecModbusClientTimeoutError: Raised for a modbus client request timeout.
        SunSpecModbusClientException: Raised for an exception response to a modbus
            client request.
    """

    def __init__(self, slave_id, name, baudrate=None, parity=None, timeout=None, ctx=None, trace_func=None,
                 max_count=modbus_client.REQ_COUNT_MAX, model_class=SunSpecModbusClientModel):
        # test if this super class init is needed
        SunSpecModbusClientDevice.__init__(self, model_class=model_class)
        self.slave_id = slave_id
        self.name = name
        self.client = None
        self.ctx = ctx
        self.trace_func = trace_func
        self.max_count = max_count

        self.client = modbus_client.modbus_rtu_client(name, baudrate, parity)
        if self.client is None:
            raise SunSpecModbusClientError('No modbus rtu client set for device')
        self.client.add_device(self.slave_id, self)

        if timeout is not None and self.client.serial is not None:
            self.client.serial.timeout = timeout
            self.client.serial.writeTimeout = timeout

    def open(self):
        self.client.open()

    def close(self):
        """Close the device. Called when device is not longer in use.
        """

        if self.client:
            self.client.remove_device(self.slave_id)

    def read(self, addr, count, op=modbus_client.FUNC_READ_HOLDING):
        """Read Modbus device registers.
        Parameters:
            addr :
                Starting Modbus address.
            count :
                Read length in Modbus registers.
            op :
                Modbus function code for request.
        Returns:
            Byte string containing register contents.
        """

        return self.client.read(self.slave_id, addr, count, op=op, trace_func=self.trace_func, max_count=self.max_count)

    def write(self, addr, data):
        """Write Modbus device registers.
        Parameters:
            addr :
                Starting Modbus address.
            count :
                Byte string containing register contents.
        """

        return self.client.write(self.slave_id, addr, data, trace_func=self.trace_func, max_count=self.max_count)
