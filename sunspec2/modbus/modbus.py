"""
    Copyright (C) 2018 SunSpec Alliance
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

import socket
import struct
import serial
import time

PARITY_NONE = 'N'
PARITY_EVEN = 'E'

REQ_COUNT_MAX = 125
REQ_WRITE_COUNT_MAX = 123

FUNC_READ_HOLDING = 3
FUNC_READ_INPUT = 4
FUNC_WRITE_MULTIPLE = 16
FUNC_WRITE_SINGLE = 6

TEST_NAME = 'test_name'

modbus_rtu_clients = {}

TCP_HDR_LEN = 6
TCP_RESP_MIN_LEN = 3
TCP_HDR_O_LEN = 4
TCP_READ_REQ_LEN = 6
TCP_WRITE_MULT_REQ_LEN = 7
TCP_WRITE_SINGLE_REQ_LEN = 4

TCP_DEFAULT_PORT = 502
TCP_DEFAULT_TIMEOUT = 2


class ModbusClientError(Exception):
    pass


class ModbusClientTimeout(ModbusClientError):
    pass


class ModbusClientException(ModbusClientError):
    pass


def modbus_rtu_client(name=None, baudrate=None, parity=None, timeout=0.5):
    global modbus_rtu_clients

    client = modbus_rtu_clients.get(name)
    if client is not None:
        if baudrate is not None and client.baudrate != baudrate:
            raise ModbusClientError('Modbus client baudrate mismatch')
        if parity is not None and client.parity != parity:
            raise ModbusClientError('Modbus client parity mismatch')
    else:
        if baudrate is None:
            baudrate = 9600
        if parity is None:
            parity = PARITY_NONE
        client = ModbusClientRTU(name, baudrate, parity, timeout)
        modbus_rtu_clients[name] = client
    return client


def modbus_rtu_client_remove(name=None):

    global modbus_rtu_clients

    if modbus_rtu_clients.get(name):
        del modbus_rtu_clients[name]


def __generate_crc16_table():
    ''' Generates a crc16 lookup table
    .. note:: This will only be generated once
    '''
    result = []
    for byte in range(256):
        crc = 0x0000
        for bit in range(8):
            if (byte ^ crc) & 0x0001:
                crc = (crc >> 1) ^ 0xa001
            else: crc >>= 1
            byte >>= 1
        result.append(crc)
    return result


__crc16_table = __generate_crc16_table()


def computeCRC(data):
    ''' Computes a crc16 on the passed in string. For modbus,
    this is only used on the binary serial protocols (in this
    case RTU).
    The difference between modbus's crc16 and a normal crc16
    is that modbus starts the crc value out at 0xffff.
    :param data: The data to create a crc16 of
    :returns: The calculated CRC
    '''
    crc = 0xffff

    for a in data:
        idx = __crc16_table[(crc ^ a) & 0xff];
        crc = ((crc >> 8) & 0xff) ^ idx
    swapped = ((crc << 8) & 0xff00) | ((crc >> 8) & 0x00ff)
    return swapped


def checkCRC(data, check):
    ''' Checks if the data matches the passed in CRC
    :param data: The data to create a crc16 of
    :param check: The CRC to validate
    :returns: True if matched, False otherwise
    '''
    return computeCRC(data) == check


class ModbusClientRTU:
    """A Modbus RTU client that multiple devices can use to access devices over
    the same serial interface. Currently, the implementation does not support
    concurent device requests so the support of multiple devices must be single
    threaded.
    Parameters:
        name :
            Name of the serial port such as 'com4' or '/dev/ttyUSB0'.
        baudrate :
            Baud rate such as 9600 or 19200. Default is 9600 if not specified.
        parity :
            Parity. Possible values:
                :const:`sunspec.core.modbus.client.PARITY_NONE`,
                :const:`sunspec.core.modbus.client.PARITY_EVEN`.  Defaults to
                :const:`PARITY_NONE`.
    Raises:
        ModbusClientError: Raised for any general modbus client error.
        ModbusClientTimeoutError: Raised for a modbus client request timeout.
        ModbusClientException: Raised for an exception response to a modbus
            client request.
    Attributes:
        name
            Name of the serial port such as 'com4' or '/dev/ttyUSB0'.
        baudrate
            Baud rate.
        parity
            Parity. Possible values:
                :const:`sunspec.core.modbus.client.PARITY_NONE`,
                :const:`sunspec.core.modbus.client.PARITY_EVEN`
        serial
            The pyserial.Serial object used for serial communications.
        timeout
            Read timeout in seconds. Fractional values are permitted.
        write_timeout
            Write timeout in seconds. Fractional values are permitted.
        devices
            List of :const:`sunspec.core.modbus.client.ModbusClientDeviceRTU`
            devices currently using the client.
    """

    def __init__(self, name='/dev/ttyUSB0', baudrate=9600, parity=None, timeout=0.5):
        self.name = name
        self.baudrate = baudrate
        self.parity = parity
        self.serial = None
        self.timeout = timeout
        self.write_timeout = timeout
        self.devices = {}
        self.trace_func = None
        self.inter_frame_gap = 0.00175

        baudrate = int(baudrate)
        if baudrate <= 19200:
            self.inter_frame_gap = (1/(baudrate/10)) * 3.5

        self.open()

    def open(self):
        """Open the RTU client serial interface.
        """

        try:
            if self.parity == PARITY_EVEN:
                parity = serial.PARITY_EVEN
            else:
                parity = serial.PARITY_NONE

            self.serial = serial.Serial(port=self.name, baudrate=self.baudrate,
                                        bytesize=8, parity=parity,
                                        stopbits=1,
                                        timeout=self.timeout,
                                        xonxoff=False,
                                        )

        except Exception as e:
            if self.serial is not None:
                self.serial.close()
                self.serial = None
            raise ModbusClientError('Serial init error: %s' % str(e))

    def close(self):
        """Close the RTU client serial interface.
        """

        try:
            if self.serial is not None:
                self.serial.close()
        except Exception as e:
            raise ModbusClientError('Serial close error: %s' % str(e))

    def add_device(self, unit_id, device):
        """Add a device to the RTU client.
        Parameters:
            unit_id :
                Modbus Unit Identifier.
            device :
                Device to add to the client.
        """

        self.devices[unit_id] = device

    def remove_device(self, unit_id):
        """Remove a device from the RTU client.
        Parameters:
            unit_id :
                Modbus Unit Identifier.
        """

        if self.devices.get(unit_id):
            del self.devices[unit_id]

        # if no more devices using the client interface, close and remove the client
        if len(self.devices) == 0:
            self.close()
            modbus_rtu_client_remove(self.name)

    def _read(self, unit_id, addr, count, op=FUNC_READ_HOLDING):
        resp = bytearray()
        len_remaining = 5
        len_found = False
        except_code = None

        req = struct.pack('>BBHH', int(unit_id), op, int(addr), int(count))
        req += struct.pack('>H', computeCRC(req))

        if self.trace_func:
            # s = '{}:{}[addr={}] ->'.format(self.name, str(unit_id), addr)
            s = '> '
            for c in req:
                s += '%02X' % c
            self.trace_func(s)

        self.serial.flushInput()
        try:
            time.sleep(self.inter_frame_gap)
            self.serial.write(req)
        except Exception as e:
            raise ModbusClientError('Serial write error: %s' % str(e))

        while len_remaining > 0:
            c = self.serial.read(len_remaining)

            len_read = len(c)
            if len_read > 0:
                resp += c
                len_remaining -= len_read
                if len_found is False and len(resp) >= 5:
                    if not resp[1] & 0x80:
                        len_remaining = (resp[2] + 5) - len(resp)
                        len_found = True
                    else:
                        except_code = resp[2]
            else:
                raise ModbusClientTimeout('Response timeout')

        if self.trace_func:
            # s = '{}:{}[addr={}] <--'.format(self.name, str(unit_id), addr)
            s = '< '
            for c in resp:
                s += '%02X' % c
            self.trace_func(s)

        crc = (resp[-2] << 8) | resp[-1]
        if not checkCRC(resp[:-2], crc):
            raise ModbusClientError('CRC error')

        if except_code:
            raise ModbusClientException('Modbus exception %d' % (except_code))

        return resp[3:-2]

    def read(self, unit_id, addr, count, op=FUNC_READ_HOLDING, max_count=REQ_COUNT_MAX):
        """
        Parameters:
            unit_id :
                Modbus Unit Identifier.
            addr :
                Starting Modbus address.
            count :
                Read length in Modbus registers.
            op :
                Modbus function code for request. Possible values:
                    :const:`FUNC_READ_HOLDING`, :const:`FUNC_READ_INPUT`.
            max_count :
                Maximum register count for a single Modbus request.
        Returns:
            Byte string containing register contents.
        """
        resp = bytearray()
        read_offset = 0

        if self.serial is not None:
            while count > 0:
                if count > max_count:
                    read_count = max_count
                else:
                    read_count = count
                data = self._read(unit_id, addr + read_offset, read_count, op=op)
                if data:
                    resp += data
                    count -= read_count
                    read_offset += read_count
                else:
                    return
        else:
            raise ModbusClientError('Client serial port not open: %s' % self.name)

        return bytes(resp)

    def _write(self, unit_id, addr, data):
        resp = bytearray()
        len_remaining = 5
        len_found = False
        except_code = None
        func = FUNC_WRITE_MULTIPLE
        len_data = len(data)
        count = int(len_data/2)

        req = struct.pack('>BBHHB', int(unit_id), func, int(addr), count, len_data)

        req += data
        req += struct.pack('>H', computeCRC(req))

        if self.trace_func:
            # s = '{}:{}[addr={}] ->'.format(self.name, str(unit_id), addr)
            s = '> '
            for c in req:
                s += '%02X' % c
            self.trace_func(s)

        self.serial.flushInput()

        try:
            time.sleep(self.inter_frame_gap)
            self.serial.write(bytes(req))
        except Exception as e:
            raise ModbusClientError('Serial write error: %s' % str(e))

        while len_remaining > 0:
            c = self.serial.read(len_remaining)

            len_read = len(c)
            if len_read > 0:
                resp += c
                len_remaining -= len_read
                if len_found is False and len(resp) >= 5:
                    if not (resp[1] & 0x80):
                        len_remaining = 8 - len(resp)
                        len_found = True
                    else:
                        except_code = resp[2]
            else:
                raise ModbusClientTimeout('Response timeout')

        if self.trace_func:
            # s = '{}:{}[addr={}] <--'.format(self.name, str(unit_id), addr)
            s = '< '
            for c in resp:
                s += '%02X' % c
            self.trace_func(s)

        crc = (resp[-2] << 8) | resp[-1]
        if not checkCRC(resp[:-2], crc):
            raise ModbusClientError('CRC error')

        if except_code:
            raise ModbusClientException('Modbus exception: %d' % except_code)
        else:
            resp_unit_id, resp_func, resp_addr, resp_count, resp_crc = struct.unpack('>BBHHH', bytes(resp))
            if resp_unit_id != unit_id or resp_func != func or resp_addr != addr or resp_count != count:
                raise ModbusClientError('Modbus response format error')

    def _write_single(self, unit_id, addr, data):
        resp = bytearray()
        len_remaining = 5
        len_found = False
        except_code = None
        func = FUNC_WRITE_SINGLE

        req = struct.pack('>BBH', int(unit_id), func, int(addr))
        req += data
        req += struct.pack('>H', computeCRC(req))

        if self.trace_func:
            # s = '{}:{}[addr={}] ->'.format(self.name, str(unit_id), addr)
            s = '> '
            for c in req:
                s += '%02X' % c
            self.trace_func(s)

        self.serial.flushInput()

        try:
            time.sleep(self.inter_frame_gap)
            self.serial.write(bytes(req))
        except Exception as e:
            raise ModbusClientError('Serial write error: %s' % str(e))

        while len_remaining > 0:
            c = self.serial.read(len_remaining)

            len_read = len(c)
            if len_read > 0:
                resp += c
                len_remaining -= len_read
                if len_found is False and len(resp) >= 5:
                    if not resp[1] & 0x80:
                        len_remaining = 8 - len(resp)
                        len_found = True
                    else:
                        except_code = resp[2]
            else:
                raise ModbusClientTimeout('Response timeout')

        if self.trace_func:
            # s = '{}:{}[addr={}] <--'.format(self.name, str(unit_id), addr)
            s = '< '
            for c in resp:
                s += '%02X' % c
            self.trace_func(s)

        crc = (resp[-2] << 8) | resp[-1]
        if not checkCRC(resp[:-2], crc):
            raise ModbusClientError('CRC error')

        if except_code:
            raise ModbusClientException('Modbus exception: %d' % except_code)
        else:
            resp_unit_id, resp_func, resp_addr, resp_data, _ = struct.unpack('>BBHHH', bytes(resp))
            if (resp_unit_id != unit_id or resp_func != func or resp_addr != addr or
                    resp_data != int.from_bytes(data, 'big')):
                raise ModbusClientError('Modbus response error')

    def write(self, unit_id, addr, data, max_write_count=REQ_WRITE_COUNT_MAX):
        """
        Parameters:
            unit_id :
                Modbus Unit Identifier.
            addr :
                Starting Modbus address.
            data :
                Byte string containing register contents.
            max_write_count :
                Maximum register count for a single Modbus write.
        """

        write_offset = 0
        count = len(data)/2

        if self.serial is not None:
            if count == 1:  # If only one register, use Func Code 0x06
                self._write_single(unit_id, addr, data)
            else:
                while count > 0:
                    if count > max_write_count:
                        write_count = max_write_count
                    else:
                        write_count = count
                    start = int(write_offset * 2)
                    end = int((write_offset + write_count) * 2)
                    self._write(unit_id, addr + write_offset, data[start:end])
                    count -= write_count
                    write_offset += write_count
        else:
            raise ModbusClientError('Client serial port not open: %s' % self.name)


class ModbusClientTCP:
    def __init__(self, unit_id=1, ipaddr='127.0.0.1', ipport=502, timeout=None, ctx=None, trace_func=None,
                 max_count=REQ_COUNT_MAX, max_write_count=REQ_WRITE_COUNT_MAX):
        self.unit_id = unit_id
        self.ipaddr = ipaddr
        self.ipport = ipport
        self.timeout = timeout
        self.ctx = ctx
        self.socket = None
        self.trace_func = trace_func
        self.max_count = max_count
        self.max_write_count = max_write_count

        if ipport is None:
            self.ipport = TCP_DEFAULT_PORT
        if timeout is None:
            self.timeout = TCP_DEFAULT_TIMEOUT

    def close(self):

        self.disconnect()

    def connect(self, timeout=None):
        """Connect to TCP destination.

        Parameters:

            timeout :
                Connection timeout in seconds.
        """
        if self.socket:
            self.disconnect()

        if timeout is None:
            timeout = self.timeout

        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(timeout)
            self.socket.connect((self.ipaddr, self.ipport))
        except Exception as e:
            raise ModbusClientError('Connection error: %s' % str(e))

    def disconnect(self):
        """Disconnect from TCP destination.
        """

        try:
            if self.socket:
                self.socket.close()
            self.socket = None
        except Exception:
            pass

    def is_connected(self):
        return self.socket

    def _read(self, addr, count, op=FUNC_READ_HOLDING):
        resp = bytearray()
        len_remaining = TCP_HDR_LEN + TCP_RESP_MIN_LEN
        len_found = False
        except_code = None

        req = struct.pack('>HHHBBHH', 0, 0, TCP_READ_REQ_LEN, int(self.unit_id), op, int(addr), int(count))

        if self.trace_func:
            # s = '%s:%s:%s[addr=%s] ->' % (self.ipaddr, str(self.ipport), str(self.unit_id), addr)
            s = '> '
            for c in req:
                s += '%02X' % c
            self.trace_func(s)

        try:
            self.socket.sendall(req)
        except Exception as e:
            raise ModbusClientError('Socket write error: %s' % str(e))

        while len_remaining > 0:
            c = self.socket.recv(len_remaining)
            len_read = len(c)
            if len_read > 0:
                resp += c
                len_remaining -= len_read
                if len_found is False and len(resp) >= TCP_HDR_LEN + TCP_RESP_MIN_LEN:
                    data_len = struct.unpack('>H', resp[TCP_HDR_O_LEN:TCP_HDR_O_LEN + 2])
                    len_remaining = data_len[0] - (len(resp) - TCP_HDR_LEN)
            else:
                raise ModbusClientTimeout('Response timeout')

        if resp[TCP_HDR_LEN + 1] & 0x80:
            except_code = resp[TCP_HDR_LEN + 2]

        if self.trace_func:
            # s = '%s:%s:%s[addr=%s] <--' % (self.ipaddr, str(self.ipport), str(self.unit_id), addr)
            s ='< '
            for c in resp:
                s += '%02X' % c
            self.trace_func(s)

        if except_code:
            raise ModbusClientException('Modbus exception %d: addr: %s count: %s' % (except_code, addr, count))

        return resp[(TCP_HDR_LEN + 3):]

    def read(self, addr, count, op=FUNC_READ_HOLDING):
        """ Read Modbus device registers. If no connection exists to the
        destination, one is created and disconnected at the end of the request.

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

        resp = bytearray()
        read_offset = 0
        local_connect = False

        if self.socket is None:
            local_connect = True
            self.connect(self.timeout)

        try:
            while count > 0:
                if count > self.max_count:
                    read_count = self.max_count
                else:
                    read_count = count
                data = self._read(addr + read_offset, read_count, op=op)

                if data:
                    resp += data
                    count -= read_count
                    read_offset += read_count
                else:
                    break
        except socket.timeout as e:
            raise ModbusClientTimeout(str(e))
        finally:
            if local_connect:
                self.disconnect()

        return bytes(resp)

    def _write(self, addr, data):
        resp = bytearray()
        len_remaining = TCP_HDR_LEN + TCP_RESP_MIN_LEN
        len_found = False
        except_code = None
        func = FUNC_WRITE_MULTIPLE

        write_len = len(data)
        write_count = int(write_len/2)
        req = struct.pack('>HHHBBHHB', 0, 0, TCP_WRITE_MULT_REQ_LEN + write_len, int(self.unit_id),
                          func, int(addr), write_count, write_len)
        req += data

        if self.trace_func:
            # s = '%s:%s:%s[addr=%s] ->' % (self.ipaddr, str(self.ipport), str(self.unit_id), addr)
            s = '> '
            for c in req:
                s += '%02X' % c
            self.trace_func(s)

        try:
            self.socket.sendall(req)
        except Exception as e:
            raise ModbusClientError('Socket write error: %s' % str(e))

        while len_remaining > 0:
            c = self.socket.recv(len_remaining)
            len_read = len(c)
            if len_read > 0:
                resp += c
                len_remaining -= len_read
                if len_found is False and len(resp) >= TCP_HDR_LEN + TCP_RESP_MIN_LEN:
                    data_len = struct.unpack('>H', resp[TCP_HDR_O_LEN:TCP_HDR_O_LEN + 2])
                    len_remaining = data_len[0] - (len(resp) - TCP_HDR_LEN)
            else:
                raise ModbusClientTimeout('Response timeout')

        if (resp[TCP_HDR_LEN + 1]) & 0x80:
            except_code = resp[TCP_HDR_LEN + 2]

        if self.trace_func:
            # s = '%s:%s:%s[addr=%s] <--' % (self.ipaddr, str(self.ipport), str(self.unit_id), addr)
            s = '< '
            for c in resp:
                s += '%02X' % c
            self.trace_func(s)

        if except_code:
            raise ModbusClientException('Modbus exception: %d' % except_code)

    def _write_single(self, addr, data):
        """
        Write Single Modbus device register
        """

        resp = bytearray()
        len_remaining = TCP_HDR_LEN + TCP_RESP_MIN_LEN
        len_found = False
        except_code = None
        func = FUNC_WRITE_SINGLE

        write_len = len(data)
        req = struct.pack('>HHHBBH', 0, 0, TCP_WRITE_SINGLE_REQ_LEN + write_len, int(self.unit_id),
                          func, int(addr))
        req += data

        if self.trace_func:
            # s = '%s:%s:%s[addr=%s] ->' % (self.ipaddr, str(self.ipport), str(self.unit_id), addr)
            s = '> '
            for c in req:
                s += '%02X' % c
            self.trace_func(s)

        try:
            self.socket.sendall(req)
        except Exception as e:
            raise ModbusClientError('Socket write error: %s' % str(e))

        while len_remaining > 0:
            c = self.socket.recv(len_remaining)
            len_read = len(c)
            if len_read > 0:
                resp += c
                len_remaining -= len_read
                if len_found is False and len(resp) >= TCP_HDR_LEN + TCP_RESP_MIN_LEN:
                    data_len = struct.unpack('>H', resp[TCP_HDR_O_LEN:TCP_HDR_O_LEN + 2])
                    len_remaining = data_len[0] - (len(resp) - TCP_HDR_LEN)
            else:
                raise ModbusClientTimeout('Response timeout')

        if (resp[TCP_HDR_LEN + 1]) & 0x80:
            except_code = resp[TCP_HDR_LEN + 2]

        if self.trace_func:
            # s = '%s:%s:%s[addr=%s] <--' % (self.ipaddr, str(self.ipport), str(self.unit_id), addr)
            s = '< '
            for c in resp:
                s += '%02X' % c
            self.trace_func(s)

        if except_code:
            raise ModbusClientException('Modbus exception: %d' % except_code)

    def write(self, addr, data):
        """ Write Modbus device registers. If no connection exists to the
        destination, one is created and disconnected at the end of the request.

        Parameters:

            addr :
                Starting Modbus address.

            data :
                Byte string containing register contents.
        """
        write_offset = 0
        local_connect = False
        count = len(data)/2

        if self.socket is None:
            local_connect = True
            self.connect(self.timeout)

        try:
            if count == 1:
                self._write_single(addr, data)  # If only one register, use Func Code 0x06
            else:
                while count > 0:
                    if count > self.max_write_count:
                        write_count = self.max_write_count
                    else:
                        write_count = count
                    start = write_offset * 2
                    end = int((write_offset + write_count) * 2)
                    self._write(addr + write_offset, data[start:end])
                    count -= write_count
                    write_offset += write_count
        finally:
            if local_connect:
                self.disconnect()
