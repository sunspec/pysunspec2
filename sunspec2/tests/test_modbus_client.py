import sunspec2.modbus.client as client
import pytest
import socket
import sunspec2.tests.mock_socket as MockSocket
import serial
import sunspec2.tests.mock_port as MockPort
import sunspec2.file.client as file_client
import sunspec2.modbus.modbus as suns_modbus
import struct

class TestSunSpecModbusClientPoint:
    def test_read(self, monkeypatch):
        monkeypatch.setattr(socket, 'socket', MockSocket.mock_socket)
        monkeypatch.setattr(serial, 'Serial', MockPort.mock_port)

        monkeypatch.setattr(client.SunSpecModbusClientDeviceTCP, 'connect', MockSocket.mock_tcp_connect)
        monkeypatch.setattr(client.SunSpecModbusClientDeviceTCP, 'disconnect', MockSocket.mock_tcp_connect)

        # tcp
        d_tcp = client.SunSpecModbusClientDeviceTCP(slave_id=1, ipaddr='127.0.0.1', ipport=8502)
        tcp_buffer = [b'\x00\x00\x00\x00\x00\t\x01\x03\x06',
                      b'SunS\x00\x01',
                      b'\x00\x00\x00\x00\x00\x05\x01\x03\x02',
                      b'\x00B',
                      b'\x00\x00\x00\x00\x00\x8b\x01\x03\x88',
                      b'\x00\x01\x00BSunSpecTest\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00TestDevice-1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00opt_a_b_c\x00\x00\x00\x00\x00\x00\x001.2.3\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00sn-123456789\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00',
                      b'\x00\x00\x00\x00\x00\x05\x01\x03\x02',
                      b'\x00~',
                      b'\x00\x00\x00\x00\x00\x05\x01\x03\x02',
                      b'\x00@',
                      b'\x00\x00\x00\x00\x00\x87\x01\x03\x84',
                      b'\x00~\x00@\x00\x03\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x80\x00\x80\x00\x80\x00\xff'
                      b'\xff\xff\xff\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00'
                      b'\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80'
                      b'\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff'
                      b'\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff',
                      b'\x00\x00\x00\x00\x00\x05\x01\x03\x02',
                      b'\xff\xff']
        d_tcp.connect()
        d_tcp.client.socket._set_buffer(tcp_buffer)
        d_tcp.scan()

        assert d_tcp.common[0].SN.value == 'sn-123456789'
        assert not d_tcp.common[0].SN.dirty

        d_tcp.common[0].SN.value = 'will be overwritten by read'
        assert d_tcp.common[0].SN.value == 'will be overwritten by read'
        assert d_tcp.common[0].SN.dirty
        d_tcp.client.socket.clear_buffer()
        tcp_p_buffer = [b'\x00\x00\x00\x00\x00#\x01\x03 ',
                        b'sn-123456789\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00']
        d_tcp.client.socket._set_buffer(tcp_p_buffer)
        d_tcp.common[0].SN.read()
        assert d_tcp.common[0].SN.value == 'sn-123456789'
        assert not d_tcp.common[0].SN.dirty

        # rtu
        d_rtu = client.SunSpecModbusClientDeviceRTU(slave_id=1, name="COM2")
        rtu_buffer = [b'\x01\x03\x06Su',
                      b'nS\x00\x01\x8d\xe4',
                      b'\x01\x03\x02\x00B',
                      b'8u',
                      b'\x01\x03\x88\x00\x01',
                      b'\x00BSunSpecTest\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00TestDevice-1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00opt_a_b_c\x00\x00\x00\x00\x00\x00\x001.2.3\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00sn-123456789\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x01\x00\x00M\xf9',
                      b'\x01\x03\x02\x00~',
                      b'8d',
                      b'\x01\x03\x02\x00@',
                      b'\xb9\xb4',
                      b'\x01\x03\x84\x00~',
                      b'\x00@\x00\x03\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x80\x00\x80\x00\x80\x00'
                      b'\xff\xff\xff\xff\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff'
                      b'\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00'
                      b'\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff'
                      b'\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xffI',
                      b'\x01\x03\x02\xff\xff',
                      b'\xb9\xf4']
        d_rtu.open()
        d_rtu.client.serial._set_buffer(rtu_buffer)
        d_rtu.scan()
        assert d_rtu.common[0].SN.value == 'sn-123456789'
        assert not d_rtu.common[0].SN.dirty

        d_rtu.common[0].SN.value = 'will be overwritten by read'
        assert d_rtu.common[0].SN.value == 'will be overwritten by read'
        assert d_rtu.common[0].SN.dirty

        d_rtu.client.serial.clear_buffer()
        tcp_p_buffer = [b'\x01\x03 sn',
                        b'-123456789\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xd5\xb8']
        d_rtu.client.serial._set_buffer(tcp_p_buffer)
        d_rtu.common[0].SN.read()
        assert d_rtu.common[0].SN.value == 'sn-123456789'
        assert not d_rtu.common[0].SN.dirty

    def test_write(self, monkeypatch):
        monkeypatch.setattr(socket, 'socket', MockSocket.mock_socket)
        monkeypatch.setattr(serial, 'Serial', MockPort.mock_port)

        monkeypatch.setattr(client.SunSpecModbusClientDeviceTCP, 'connect', MockSocket.mock_tcp_connect)
        monkeypatch.setattr(client.SunSpecModbusClientDeviceTCP, 'disconnect', MockSocket.mock_tcp_connect)

        # tcp
        d_tcp = client.SunSpecModbusClientDeviceTCP(slave_id=1, ipaddr='127.0.0.1', ipport=8502)
        # simulate a sequence of exchanges with the device
        tcp_buffer = [b'\x00\x00\x00\x00\x00\t\x01\x03\x06',  # Readback first 6 registers
                      b'SunS\x00\x01',  # SunSpec ID + common model header (ID = 1)
                      b'\x00\x00\x00\x00\x00\x05\x01\x03\x02',  # Read back L register to get common model length
                      b'\x00B',  # common model length = 0x42 = 66 = 'B'
                      b'\x00\x00\x00\x00\x00\x8b\x01\x03\x88',  # Readback 0x88 bytes in common model (0x44 = 68 regs)
                      b'\x00\x01\x00BSunSpecTest\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00TestDevice-1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00opt_a_b_c\x00\x00\x00\x00\x00\x00\x001.2.3\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00sn-123456789\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00',
                      b'\x00\x00\x00\x00\x00\x05\x01\x03\x02',  # Readback/response to query next model
                      b'\x00~',  # 126 = '~' = 0x7e
                      b'\x00\x00\x00\x00\x00\x05\x01\x03\x02',  # readback next model len
                      b'\x00@',  # 64 = '@' = 0x40
                      b'\x00\x00\x00\x00\x00\x87\x01\x03\x84',  # readback next model data (0x84 bytes = 66 regs)
                      b'\x00~\x00@\x00\x03\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x80\x00\x80\x00\x80\x00\xff'
                      b'\xff\xff\xff\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00'
                      b'\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80'
                      b'\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff'
                      b'\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff',
                      b'\x00\x00\x00\x00\x00\x05\x01\x03\x02',  # readback next model
                      b'\xff\xff']  # terminator
        d_tcp.client.connect()
        d_tcp.client.socket._set_buffer(tcp_buffer)
        d_tcp.scan()

        assert d_tcp.common[0].SN.value == 'sn-123456789'
        assert not d_tcp.common[0].SN.dirty

        d_tcp.common[0].SN.value = 'sn-000'
        assert d_tcp.common[0].SN.value == 'sn-000'
        assert d_tcp.common[0].SN.dirty

        tcp_write_buffer = [b'\x00\x00\x00\x00\x00\x06\x01\x10\x9c',
                            b't\x00\x10']
        d_tcp.client.socket.clear_buffer()
        d_tcp.client.socket._set_buffer(tcp_write_buffer)
        d_tcp.common[0].write()

        d_tcp.common[0].SN.value = 'will be overwritten by read'
        assert d_tcp.common[0].SN.value == 'will be overwritten by read'
        assert d_tcp.common[0].SN.dirty

        tcp_read_buffer = [b'\x00\x00\x00\x00\x00#\x01\x03 ',  # Read back data to verify write
                           b'sn-000\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                           b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00']
        d_tcp.client.socket.clear_buffer()
        d_tcp.client.socket._set_buffer(tcp_read_buffer)
        d_tcp.common[0].SN.read()
        assert d_tcp.common[0].SN.value == 'sn-000'
        assert not d_tcp.common[0].SN.dirty

        # rtu
        d_rtu = client.SunSpecModbusClientDeviceRTU(slave_id=1, name="COM2")
        rtu_buffer = [  # simulate a sequence of responses from the device scan
            b'\x01\x03\x06Su',
            b'nS\x00\x01\x8d\xe4',  # Response: SunSpec ID + common model header (ID = 1) + CRC
            b'\x01\x03\x02\x00B',
            b'8u',  # Response: common model length = 0x42 = 66 = 'B' + CRC
            b'\x01\x03\x88\x00\x01',  # Readback registers in common model (0x44 = 68 regs)
            b'\x00BSunSpecTest\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            b'\x00\x00TestDevice-2\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            b'\x00\x00opt_a_b_c\x00\x00\x00\x00\x00\x00\x001.2.3\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            b'\x00sn-123456789\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x01\x00\x00\xb9\xfb',  # Common model data
            b'\x01\x03\x02\xff\xff',  # Terminator data
            b'\xb9\xf4'  # CRC
        ]
        d_rtu.open()
        d_rtu.client.serial._set_buffer(rtu_buffer)
        d_rtu.scan()
        assert d_rtu.common[0].SN.value == 'sn-123456789'
        assert not d_rtu.common[0].SN.dirty

        assert d_rtu.common[0].DA.value == 1
        d_rtu.common[0].DA.value = 2
        assert d_rtu.common[0].DA.value == 2
        assert d_rtu.common[0].DA.dirty

        # 0x01: This is the device address, 1.
        # 0x06: This is the function code for "Write Single Register"/0x10 (16) = "Write Multiple Registers".
        # 0x9c84: This is the register address, 0x9c84 is 40068. (DA)
        # 0x0002: This is the data value to be written to the register, 2.
        # Cyclic Redundancy Check (CRC) - struct.pack('>H', suns_modbus.computeCRC(b'\x01\x06\x9c\x84\x00\x02'))
        rtu_read_buffer = [
            b'\x01\x06\x9c\x84\x00\x02',
            suns_modbus.computeCRC(b'\x01\x06\x9c\x84\x00\x02').to_bytes(2, 'big')
        ]
        d_rtu.client.serial.clear_buffer()
        d_rtu.client.serial._set_buffer(rtu_read_buffer)
        d_rtu.common[0].write()

        # 0x01: Slave Address (1).
        # 0x03: Function Code (Read Holding Registers). T
        # 0x02: Byte Count (2). This tells you that the response contains 2 bytes of data.
        # 0x0002: Data (2 in decimal). This is the actual data read from the holding registers. DA = 2
        rtu_read_buffer = [
            b'\x01\x03\x02\x00\x02',  # Read back data to verify write
            struct.pack('>H', suns_modbus.computeCRC(b'\x01\x03\x02\x00\x02'))
        ]
        d_rtu.client.serial.clear_buffer()
        d_rtu.client.serial._set_buffer(rtu_read_buffer)
        d_rtu.common[0].DA.read()
        assert d_rtu.common[0].DA.value == 2
        assert not d_rtu.common[0].SN.dirty

    def test_get_text(self, monkeypatch):
        monkeypatch.setattr(socket, 'socket', MockSocket.mock_socket)
        monkeypatch.setattr(serial, 'Serial', MockPort.mock_port)

        monkeypatch.setattr(client.SunSpecModbusClientDeviceTCP, 'connect', MockSocket.mock_tcp_connect)
        monkeypatch.setattr(client.SunSpecModbusClientDeviceTCP, 'disconnect', MockSocket.mock_tcp_connect)

        # tcp
        d_tcp = client.SunSpecModbusClientDeviceTCP(slave_id=1, ipaddr='127.0.0.1', ipport=8502)
        tcp_buffer = [b'\x00\x00\x00\x00\x00\t\x01\x03\x06',
                      b'SunS\x00\x01',
                      b'\x00\x00\x00\x00\x00\x05\x01\x03\x02',
                      b'\x00B',
                      b'\x00\x00\x00\x00\x00\x8b\x01\x03\x88',
                      b'\x00\x01\x00BSunSpecTest\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00TestDevice-1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00opt_a_b_c\x00\x00\x00\x00\x00\x00\x001.2.3\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00sn-123456789\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00',
                      b'\x00\x00\x00\x00\x00\x05\x01\x03\x02',
                      b'\x00~',
                      b'\x00\x00\x00\x00\x00\x05\x01\x03\x02',
                      b'\x00@',
                      b'\x00\x00\x00\x00\x00\x87\x01\x03\x84',
                      b'\x00~\x00@\x00\x03\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x80\x00\x80\x00\x80\x00\xff'
                      b'\xff\xff\xff\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00'
                      b'\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80'
                      b'\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff'
                      b'\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff',
                      b'\x00\x00\x00\x00\x00\x05\x01\x03\x02',
                      b'\xff\xff']
        d_tcp.connect()
        d_tcp.client.socket._set_buffer(tcp_buffer)
        d_tcp.scan()
        expected_output = '      SN                                         sn-123456789\n'
        assert d_tcp.common[0].SN.get_text() == expected_output

        d_rtu = client.SunSpecModbusClientDeviceRTU(slave_id=1, name="COM2")
        rtu_buffer = [b'\x01\x03\x06Su',
                      b'nS\x00\x01\x8d\xe4',
                      b'\x01\x03\x02\x00B',
                      b'8u',
                      b'\x01\x03\x88\x00\x01',
                      b'\x00BSunSpecTest\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00TestDevice-1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00opt_a_b_c\x00\x00\x00\x00\x00\x00\x001.2.3\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00sn-123456789\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x01\x00\x00M\xf9',
                      b'\x01\x03\x02\x00~',
                      b'8d',
                      b'\x01\x03\x02\x00@',
                      b'\xb9\xb4',
                      b'\x01\x03\x84\x00~',
                      b'\x00@\x00\x03\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x80\x00\x80\x00\x80\x00'
                      b'\xff\xff\xff\xff\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff'
                      b'\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00'
                      b'\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff'
                      b'\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xffI',
                      b'\x01\x03\x02\xff\xff',
                      b'\xb9\xf4']
        d_rtu.open()
        d_rtu.client.serial._set_buffer(rtu_buffer)
        d_rtu.scan()
        assert d_rtu.common[0].SN.get_text() == expected_output


class TestSunSpecModbusClientGroup:
    def test_read(self, monkeypatch):
        monkeypatch.setattr(socket, 'socket', MockSocket.mock_socket)
        monkeypatch.setattr(serial, 'Serial', MockPort.mock_port)

        monkeypatch.setattr(client.SunSpecModbusClientDeviceTCP, 'connect', MockSocket.mock_tcp_connect)
        monkeypatch.setattr(client.SunSpecModbusClientDeviceTCP, 'disconnect', MockSocket.mock_tcp_connect)

        # tcp
        d_tcp = client.SunSpecModbusClientDeviceTCP(slave_id=1, ipaddr='127.0.0.1', ipport=8502)
        tcp_buffer = [b'\x00\x00\x00\x00\x00\t\x01\x03\x06',
                      b'SunS\x00\x01',
                      b'\x00\x00\x00\x00\x00\x05\x01\x03\x02',
                      b'\x00B',
                      b'\x00\x00\x00\x00\x00\x8b\x01\x03\x88',
                      b'\x00\x01\x00BSunSpecTest\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00TestDevice-1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00opt_a_b_c\x00\x00\x00\x00\x00\x00\x001.2.3\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00sn-123456789\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00',
                      b'\x00\x00\x00\x00\x00\x05\x01\x03\x02',
                      b'\x00~',
                      b'\x00\x00\x00\x00\x00\x05\x01\x03\x02',
                      b'\x00@',
                      b'\x00\x00\x00\x00\x00\x87\x01\x03\x84',
                      b'\x00~\x00@\x00\x03\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x80\x00\x80\x00\x80\x00\xff'
                      b'\xff\xff\xff\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00'
                      b'\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80'
                      b'\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff'
                      b'\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff',
                      b'\x00\x00\x00\x00\x00\x05\x01\x03\x02',
                      b'\xff\xff']
        d_tcp.client.connect()
        d_tcp.client.socket._set_buffer(tcp_buffer)
        d_tcp.scan()
        assert d_tcp.common[0].SN.value == "sn-123456789"
        assert d_tcp.common[0].Vr.value == "1.2.3"
        assert not d_tcp.common[0].SN.dirty
        assert not d_tcp.common[0].Vr.dirty

        d_tcp.common[0].SN.value = 'this will overwrite from read'
        d_tcp.common[0].Vr.value = 'this will overwrite from read'
        assert d_tcp.common[0].SN.value == 'this will overwrite from read'
        assert d_tcp.common[0].Vr.value == 'this will overwrite from read'
        assert d_tcp.common[0].SN.dirty
        assert d_tcp.common[0].Vr.dirty

        tcp_read_buffer = [b'\x00\x00\x00\x00\x00\x87\x01\x03\x84',
                           b'\x00\x01\x00BSunSpecTest\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                           b'\x00\x00\x00\x00\x00\x00TestDevice-1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                           b'\x00\x00\x00\x00\x00\x00\x00\x00opt_a_b_c\x00\x00\x00\x00\x00\x00\x001.2.3\x00\x00\x00'
                           b'\x00\x00\x00\x00\x00\x00\x00\x00sn-123456789\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                           b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00']
        d_tcp.client.socket.clear_buffer()
        d_tcp.client.socket._set_buffer(tcp_read_buffer)
        d_tcp.common[0].read()

        assert d_tcp.common[0].SN.value == "sn-123456789"
        assert d_tcp.common[0].Vr.value == "1.2.3"
        assert not d_tcp.common[0].SN.dirty
        assert not d_tcp.common[0].Vr.dirty

        # rtu
        d_rtu = client.SunSpecModbusClientDeviceRTU(slave_id=1, name="COM2")
        rtu_buffer = [b'\x01\x03\x06Su',
                      b'nS\x00\x01\x8d\xe4',
                      b'\x01\x03\x02\x00B',
                      b'8u',
                      b'\x01\x03\x88\x00\x01',
                      b'\x00BSunSpecTest\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00TestDevice-1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00opt_a_b_c\x00\x00\x00\x00\x00\x00\x001.2.3\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00sn-123456789\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x01\x00\x00M\xf9',
                      b'\x01\x03\x02\x00~',
                      b'8d',
                      b'\x01\x03\x02\x00@',
                      b'\xb9\xb4',
                      b'\x01\x03\x84\x00~',
                      b'\x00@\x00\x03\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x80\x00\x80\x00\x80\x00'
                      b'\xff\xff\xff\xff\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff'
                      b'\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00'
                      b'\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff'
                      b'\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xffI',
                      b'\x01\x03\x02\xff\xff',
                      b'\xb9\xf4']
        d_rtu.open()
        d_rtu.client.serial._set_buffer(rtu_buffer)
        d_rtu.scan()
        assert d_rtu.common[0].SN.value == "sn-123456789"
        assert d_rtu.common[0].Vr.value == "1.2.3"
        assert not d_rtu.common[0].SN.dirty
        assert not d_rtu.common[0].Vr.dirty

        d_rtu.common[0].SN.value = 'this will overwrite from read'
        d_rtu.common[0].Vr.value = 'this will overwrite from read'
        assert d_rtu.common[0].SN.value == 'this will overwrite from read'
        assert d_rtu.common[0].Vr.value == 'this will overwrite from read'
        assert d_rtu.common[0].SN.dirty
        assert d_rtu.common[0].Vr.dirty

        rtu_read_buffer = [b'\x01\x03\x84\x00\x01',
                           b'\x00BSunSpecTest\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                           b'\x00\x00\x00\x00TestDevice-1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                           b'\x00\x00\x00\x00\x00\x00opt_a_b_c\x00\x00\x00\x00\x00\x00\x001.2.3\x00\x00\x00\x00'
                           b'\x00\x00\x00\x00\x00\x00\x00sn-123456789\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                           b'\x00\x00\x00\x00\x00\x00\x00\x00\x00H\xef']
        d_rtu.client.serial.clear_buffer()
        d_rtu.client.serial._set_buffer(rtu_read_buffer)
        d_rtu.common[0].read()
        assert d_rtu.common[0].SN.value == "sn-123456789"
        assert d_rtu.common[0].Vr.value == "1.2.3"
        assert not d_rtu.common[0].SN.dirty
        assert not d_rtu.common[0].Vr.dirty

    def test_write(self, monkeypatch):
        monkeypatch.setattr(socket, 'socket', MockSocket.mock_socket)
        monkeypatch.setattr(serial, 'Serial', MockPort.mock_port)

        monkeypatch.setattr(client.SunSpecModbusClientDeviceTCP, 'connect', MockSocket.mock_tcp_connect)
        monkeypatch.setattr(client.SunSpecModbusClientDeviceTCP, 'disconnect', MockSocket.mock_tcp_connect)

        # tcp
        d_tcp = client.SunSpecModbusClientDeviceTCP(slave_id=1, ipaddr='127.0.0.1', ipport=8502)
        tcp_buffer = [b'\x00\x00\x00\x00\x00\t\x01\x03\x06',
                      b'SunS\x00\x01',
                      b'\x00\x00\x00\x00\x00\x05\x01\x03\x02',
                      b'\x00B',
                      b'\x00\x00\x00\x00\x00\x8b\x01\x03\x88',
                      b'\x00\x01\x00BSunSpecTest\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00TestDevice-1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00opt_a_b_c\x00\x00\x00\x00\x00\x00\x001.2.3\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00sn-123456789\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00',
                      b'\x00\x00\x00\x00\x00\x05\x01\x03\x02',
                      b'\x00~',
                      b'\x00\x00\x00\x00\x00\x05\x01\x03\x02',
                      b'\x00@',
                      b'\x00\x00\x00\x00\x00\x87\x01\x03\x84',
                      b'\x00~\x00@\x00\x03\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x80\x00\x80\x00\x80\x00\xff'
                      b'\xff\xff\xff\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00'
                      b'\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80'
                      b'\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff'
                      b'\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff',
                      b'\x00\x00\x00\x00\x00\x05\x01\x03\x02',
                      b'\xff\xff']
        d_tcp.client.connect()
        d_tcp.client.socket._set_buffer(tcp_buffer)
        d_tcp.scan()
        assert d_tcp.common[0].SN.value == "sn-123456789"
        assert d_tcp.common[0].Vr.value == "1.2.3"
        assert not d_tcp.common[0].SN.dirty
        assert not d_tcp.common[0].Vr.dirty

        d_tcp.common[0].SN.value = 'sn-000'
        d_tcp.common[0].Vr.value = 'v0.0.0'
        assert d_tcp.common[0].SN.value == "sn-000"
        assert d_tcp.common[0].Vr.value == "v0.0.0"
        assert d_tcp.common[0].SN.dirty
        assert d_tcp.common[0].Vr.dirty

        tcp_write_buffer = [b'\x00\x00\x00\x00\x00\x06\x01\x10\x9c',
                            b'l\x00\x18']
        d_tcp.client.socket.clear_buffer()
        d_tcp.client.socket._set_buffer(tcp_write_buffer)
        d_tcp.common[0].write()

        d_tcp.common[0].SN.value = 'this will overwrite from read'
        d_tcp.common[0].Vr.value = 'this will overwrite from read'
        assert d_tcp.common[0].SN.value == 'this will overwrite from read'
        assert d_tcp.common[0].Vr.value == 'this will overwrite from read'
        assert d_tcp.common[0].SN.dirty
        assert d_tcp.common[0].Vr.dirty

        tcp_read_buffer = [b'\x00\x00\x00\x00\x00\x87\x01\x03\x84',
                           b'\x00\x01\x00BSunSpecTest\x00\x00\x00\x00\x00\x00\x00'
                           b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                           b'\x00TestDevice-1\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                           b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00opt_a_b_c'
                           b'\x00\x00\x00\x00\x00\x00\x00v0.0.0\x00\x00\x00\x00\x00'
                           b'\x00\x00\x00\x00\x00sn-000\x00\x00\x00\x00\x00\x00\x00'
                           b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00']
        d_tcp.client.socket.clear_buffer()
        d_tcp.client.socket._set_buffer(tcp_read_buffer)
        d_tcp.common[0].read()

        assert d_tcp.common[0].SN.value == "sn-000"
        assert d_tcp.common[0].Vr.value == "v0.0.0"
        assert not d_tcp.common[0].SN.dirty
        assert not d_tcp.common[0].Vr.dirty

        # rtu
        d_rtu = client.SunSpecModbusClientDeviceRTU(slave_id=1, name="COM2")
        rtu_buffer = [
            b'\x01\x03\x06Su',
            b'nS\x00\x01\x8d\xe4',
            b'\x01\x03\x02\x00B',
            b'8u',
            b'\x01\x03\x88\x00\x01',
            b'\x00BSunSpecTest\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            b'\x00TestDevice-2\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            b'opt_a_b_c\x00\x00\x00\x00\x00\x00\x001.2.3\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00sn-123456789'
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00I\xfb',
            b'\x01\x03\x02\xff\xff',
            b'\xb9\xf4'
        ]
        d_rtu.open()
        d_rtu.client.serial._set_buffer(rtu_buffer)
        d_rtu.scan()
        assert d_rtu.common[0].SN.value == "sn-123456789"
        assert d_rtu.common[0].Vr.value == "1.2.3"
        assert not d_rtu.common[0].SN.dirty
        assert not d_rtu.common[0].Vr.dirty

        d_rtu.common[0].DA.value = 2
        assert d_rtu.common[0].DA.value == 2
        assert d_rtu.common[0].DA.dirty

        rtu_read_buffer = [
            b'\x01\x06\x9c\x84\x00\x02',
            struct.pack('>H', suns_modbus.computeCRC(b'\x01\x06\x9c\x84\x00\x02'))
        ]
        d_rtu.client.serial.clear_buffer()
        d_rtu.client.serial._set_buffer(rtu_read_buffer)
        d_rtu.common[0].write()

        d_rtu.common[0].SN.value = 'this will overwrite from read'
        d_rtu.common[0].Vr.value = 'this will overwrite from read'
        assert d_rtu.common[0].SN.value == 'this will overwrite from read'
        assert d_rtu.common[0].Vr.value == 'this will overwrite from read'
        assert d_rtu.common[0].SN.dirty
        assert d_rtu.common[0].Vr.dirty

        rtu_read_buffer = [b'\x01\x03\x84\x00\x01',
                           b'\x00BSunSpecTest\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                           b'\x00\x00\x00\x00\x00\x00\x00\x00TestDevice-1\x00\x00\x00\x00\x00\x00'
                           b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00opt_a_b_c\x00'
                           b'\x00\x00\x00\x00\x00\x00v0.0.0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                           b'sn-000\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                           b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xd4h']
        d_rtu.client.serial.clear_buffer()
        d_rtu.client.serial._set_buffer(rtu_read_buffer)
        d_rtu.common[0].read()
        assert d_rtu.common[0].SN.value == "sn-000"
        assert d_rtu.common[0].Vr.value == "v0.0.0"
        assert not d_rtu.common[0].SN.dirty
        assert not d_rtu.common[0].Vr.dirty

    def test_write_points(self):
        pass

    def test_get_text(self, monkeypatch):
        monkeypatch.setattr(socket, 'socket', MockSocket.mock_socket)
        monkeypatch.setattr(serial, 'Serial', MockPort.mock_port)

        monkeypatch.setattr(client.SunSpecModbusClientDeviceTCP, 'connect', MockSocket.mock_tcp_connect)
        monkeypatch.setattr(client.SunSpecModbusClientDeviceTCP, 'disconnect', MockSocket.mock_tcp_connect)

        # tcp
        d_tcp = client.SunSpecModbusClientDeviceTCP(slave_id=1, ipaddr='127.0.0.1', ipport=8502)
        tcp_buffer = [b'\x00\x00\x00\x00\x00\t\x01\x03\x06',
                      b'SunS\x00\x01',
                      b'\x00\x00\x00\x00\x00\x05\x01\x03\x02',
                      b'\x00B',
                      b'\x00\x00\x00\x00\x00\x8b\x01\x03\x88',
                      b'\x00\x01\x00BSunSpecTest\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00TestDevice-1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00opt_a_b_c\x00\x00\x00\x00\x00\x00\x001.2.3\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00sn-123456789\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00',
                      b'\x00\x00\x00\x00\x00\x05\x01\x03\x02',
                      b'\x00~',
                      b'\x00\x00\x00\x00\x00\x05\x01\x03\x02',
                      b'\x00@',
                      b'\x00\x00\x00\x00\x00\x87\x01\x03\x84',
                      b'\x00~\x00@\x00\x03\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x80\x00\x80\x00\x80\x00\xff'
                      b'\xff\xff\xff\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00'
                      b'\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80'
                      b'\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff'
                      b'\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff',
                      b'\x00\x00\x00\x00\x00\x05\x01\x03\x02',
                      b'\xff\xff']
        d_tcp.client.connect()
        d_tcp.client.socket._set_buffer(tcp_buffer)
        d_tcp.scan()
        expected_output = '''      ID                                                    1\n      L        ''' + \
                          '''                                            66\n      Mn                      ''' + \
                          '''                    SunSpecTest\n      Md                                     ''' + \
                          '''    TestDevice-1\n      Opt                                           opt_a_b_''' + \
                          '''c\n      Vr                                                1.2.3\n      SN    ''' + \
                          '''                                     sn-123456789\n      DA                   ''' + \
                          '''                                 1\n      Pad                                 ''' + \
                          '''                  0\n'''
        assert d_tcp.common[0].get_text() == expected_output

        # rtu
        d_rtu = client.SunSpecModbusClientDeviceRTU(slave_id=1, name="COM2")
        rtu_buffer = [b'\x01\x03\x06Su',
                      b'nS\x00\x01\x8d\xe4',
                      b'\x01\x03\x02\x00B',
                      b'8u',
                      b'\x01\x03\x88\x00\x01',
                      b'\x00BSunSpecTest\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00TestDevice-1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00opt_a_b_c\x00\x00\x00\x00\x00\x00\x001.2.3\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00sn-123456789\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x01\x00\x00M\xf9',
                      b'\x01\x03\x02\x00~',
                      b'8d',
                      b'\x01\x03\x02\x00@',
                      b'\xb9\xb4',
                      b'\x01\x03\x84\x00~',
                      b'\x00@\x00\x03\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x80\x00\x80\x00\x80\x00'
                      b'\xff\xff\xff\xff\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff'
                      b'\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00'
                      b'\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff'
                      b'\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xffI',
                      b'\x01\x03\x02\xff\xff',
                      b'\xb9\xf4']
        d_rtu.open()
        d_rtu.client.serial._set_buffer(rtu_buffer)
        d_rtu.scan()
        assert d_rtu.common[0].get_text() == expected_output


class TestSunSpecModbusClientModel:
    def test___init__(self, monkeypatch):
        d_rtu = client.SunSpecModbusClientDeviceRTU(slave_id=1, name="COM2")
        monkeypatch.setattr(serial, 'Serial', MockPort.mock_port)

        rtu_buffer = [
            b'\x01\x03\x06Su',
            b'nS\x00\x01\x8d\xe4',
            b'\x01\x03\x02\x00B',
            b'8u',
            b'\x01\x03\x88\x00\x01',
            b'\x00BSunSpecTest\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00TestDevice-2\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00opt_a_b_c\x00\x00\x00\x00\x00\x00\x001.2.3\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00sn-123456789\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\xb9\xfb',
            b'\x01\x03\x02\xff\xff',
            b'\xb9\xf4'
        ]
        d_rtu.open()
        d_rtu.client.serial._set_buffer(rtu_buffer)
        d_rtu.scan()
        client_model = d_rtu.models['common'][0]
        assert client_model.model_id == 1
        assert client_model.model_addr == 40002
        assert client_model.model_len == 66
        assert client_model.model_def['id'] == 1
        assert client_model.error_info == ''
        assert client_model.gdef['name'] == 'common'
        assert client_model.mid is not None
        assert client_model.__class__.__name__ == 'SunSpecModbusClientModel'

        monkeypatch.setattr(socket, 'socket', MockSocket.mock_socket)
        monkeypatch.setattr(client.SunSpecModbusClientDeviceTCP, 'connect', MockSocket.mock_tcp_connect)
        monkeypatch.setattr(client.SunSpecModbusClientDeviceTCP, 'disconnect', MockSocket.mock_tcp_connect)

        c_tcp = client.SunSpecModbusClientDeviceTCP()
        tcp_req_check = [b'\x00\x00\x00\x00\x00\x06\x01\x03\x00\x00\x00\x03',
                         b'\x00\x00\x00\x00\x00\x06\x01\x03\x00\x03\x00\x01',
                         b'\x00\x00\x00\x00\x00\x06\x01\x03\x00\x02\x00B',
                         b'\x00\x00\x00\x00\x00\x06\x01\x03\x00F\x00\x01',
                         b'\x00\x00\x00\x00\x00\x06\x01\x03\x00G\x00\x01',
                         b'\x00\x00\x00\x00\x00\x06\x01\x03\x00F\x00@',
                         b'\x00\x00\x00\x00\x00\x06\x01\x03\x00\x88\x00\x01']
        tcp_buffer = [b'\x00\x00\x00\x00\x00\t\x01\x03\x06',
                      b'SunS\x00\x01',
                      b'\x00\x00\x00\x00\x00\x05\x01\x03\x02',
                      b'\x00B',
                      b'\x00\x00\x00\x00\x00\x8b\x01\x03\x88',
                      b'\x00\x01\x00BSunSpecTest\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00TestDevice-1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00opt_a_b_c\x00\x00\x00\x00\x00\x00\x001.2.3\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00sn-123456789\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00',
                      b'\x00\x00\x00\x00\x00\x05\x01\x03\x02',
                      b'\x00~',
                      b'\x00\x00\x00\x00\x00\x05\x01\x03\x02',
                      b'\x00@',
                      b'\x00\x00\x00\x00\x00\x87\x01\x03\x84',
                      b'\x00~\x00@\x00\x03\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x80\x00\x80\x00\x80\x00\xff'
                      b'\xff\xff\xff\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00'
                      b'\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80'
                      b'\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff'
                      b'\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff',
                      b'\x00\x00\x00\x00\x00\x05\x01\x03\x02',
                      b'\xff\xff']
        c_tcp.client.connect()
        c_tcp.client.socket._set_buffer(tcp_buffer)
        c_tcp.scan()
        c_tcp_model = c_tcp.models['common'][0]
        assert c_tcp_model.model_id == 1
        assert c_tcp_model.model_addr == 40002
        assert c_tcp_model.model_len == 66
        assert c_tcp_model.model_def['id'] == 1
        assert c_tcp_model.error_info == ''
        assert c_tcp_model.gdef['name'] == 'common'
        assert c_tcp_model.mid is not None
        assert c_tcp_model.__class__.__name__ == 'SunSpecModbusClientModel'

    def test_error(self, monkeypatch):
        d_rtu = client.SunSpecModbusClientDeviceRTU(slave_id=1, name="COM2")
        monkeypatch.setattr(serial, 'Serial', MockPort.mock_port)

        rtu_buffer = [
            b'\x01\x83\x02\xc0\xf1',
            b'\x01\x03\x06Su',
            b'nS\x00\x01\x8d\xe4',
            b'\x01\x03\x02\x00B',
            b'8u',
            b'\x01\x03\x88\x00\x01',
            b'\x00BSunSpecTest\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00TestDevice-1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00opt_a_b_c\x00\x00\x00\x00\x00\x00\x001.2.3\x00\x00\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00sn-123456789\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x01\x00\x00M\xf9',
            b'\x01\x03\x02\x00~',
            b'8d',
            b'\x01\x03\x02\x00@',
            b'\xb9\xb4',
            b'\x01\x03\x84\x00~',
            b'\x00@\x00\x03\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x80\x00\x80\x00\x80\x00'
            b'\xff\xff\xff\xff\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff'
            b'\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00'
            b'\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff'
            b'\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xffI',
            b'\x01\x03\x02\xff\xff',
            b'\xb9\xf4']
        d_rtu.open()
        d_rtu.client.serial._set_buffer(rtu_buffer)
        d_rtu.scan()
        client_model = d_rtu.models['common'][0]
        client_model.add_error('test error')
        assert client_model.error_info == 'test error\n'

    def test_get_text(self, monkeypatch):
        monkeypatch.setattr(socket, 'socket', MockSocket.mock_socket)
        monkeypatch.setattr(serial, 'Serial', MockPort.mock_port)

        monkeypatch.setattr(client.SunSpecModbusClientDeviceTCP, 'connect', MockSocket.mock_tcp_connect)
        monkeypatch.setattr(client.SunSpecModbusClientDeviceTCP, 'disconnect', MockSocket.mock_tcp_connect)

        # tcp
        d_tcp = client.SunSpecModbusClientDeviceTCP(slave_id=1, ipaddr='127.0.0.1', ipport=8502)
        tcp_buffer = [b'\x00\x00\x00\x00\x00\t\x01\x03\x06',
                      b'SunS\x00\x01',
                      b'\x00\x00\x00\x00\x00\x05\x01\x03\x02',
                      b'\x00B',
                      b'\x00\x00\x00\x00\x00\x8b\x01\x03\x88',
                      b'\x00\x01\x00BSunSpecTest\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00TestDevice-1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00opt_a_b_c\x00\x00\x00\x00\x00\x00\x001.2.3\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00sn-123456789\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00',
                      b'\x00\x00\x00\x00\x00\x05\x01\x03\x02',
                      b'\x00~',
                      b'\x00\x00\x00\x00\x00\x05\x01\x03\x02',
                      b'\x00@',
                      b'\x00\x00\x00\x00\x00\x87\x01\x03\x84',
                      b'\x00~\x00@\x00\x03\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x80\x00\x80\x00\x80\x00\xff'
                      b'\xff\xff\xff\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00'
                      b'\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80'
                      b'\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff'
                      b'\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff',
                      b'\x00\x00\x00\x00\x00\x05\x01\x03\x02',
                      b'\xff\xff']
        d_tcp.client.connect()
        d_tcp.client.socket._set_buffer(tcp_buffer)
        d_tcp.scan()
        expected_output = '''      ID                                                    1\n      L        ''' + \
                          '''                                            66\n      Mn                      ''' + \
                          '''                    SunSpecTest\n      Md                                     ''' + \
                          '''    TestDevice-1\n      Opt                                           opt_a_b_''' + \
                          '''c\n      Vr                                                1.2.3\n      SN    ''' + \
                          '''                                     sn-123456789\n      DA                   ''' + \
                          '''                                 1\n      Pad                                 ''' + \
                          '''                  0\n'''
        assert d_tcp.common[0].get_text() == expected_output

        # rtu
        d_rtu = client.SunSpecModbusClientDeviceRTU(slave_id=1, name="COM2")
        rtu_buffer = [b'\x01\x03\x06Su',
                      b'nS\x00\x01\x8d\xe4',
                      b'\x01\x03\x02\x00B',
                      b'8u',
                      b'\x01\x03\x88\x00\x01',
                      b'\x00BSunSpecTest\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00TestDevice-1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00opt_a_b_c\x00\x00\x00\x00\x00\x00\x001.2.3\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00sn-123456789\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x01\x00\x00M\xf9',
                      b'\x01\x03\x02\x00~',
                      b'8d',
                      b'\x01\x03\x02\x00@',
                      b'\xb9\xb4',
                      b'\x01\x03\x84\x00~',
                      b'\x00@\x00\x03\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x80\x00\x80\x00\x80\x00'
                      b'\xff\xff\xff\xff\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff'
                      b'\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00'
                      b'\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff'
                      b'\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xffI',
                      b'\x01\x03\x02\xff\xff',
                      b'\xb9\xf4']
        d_rtu.open()
        d_rtu.client.serial._set_buffer(rtu_buffer)
        d_rtu.scan()
        assert d_rtu.common[0].get_text() == expected_output

    def test_read(self, monkeypatch):
        d_rtu = client.SunSpecModbusClientDeviceRTU(slave_id=1, name="COM2")
        monkeypatch.setattr(serial, 'Serial', MockPort.mock_port)

        rtu_buffer = [b'\x01\x83\x02\xc0\xf1',
                      b'\x01\x03\x06Su',
                      b'nS\x00\x01\x8d\xe4',
                      b'\x01\x03\x02\x00B',
                      b'8u',
                      b'\x01\x03\x02\xff\xff',
                      b'\xb9\xf4',
                      b'\x01\x03\x88\x00\x01',
                      b'\x00BSunSpecTest\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00TestDevice-2\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00opt_a_b_c\x00\x00\x00\x00\x00\x00\x001.2.3\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00sn-123456789\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x01\x00\x00\xb9\xfb']
        d_rtu.open()
        d_rtu.client.serial._set_buffer(rtu_buffer)
        d_rtu.scan(full_model_read=False)
        d_rtu.models['common'][0].read()
        assert d_rtu.models['common'][0].__class__.__name__ == "SunSpecModbusClientModel"
        assert d_rtu.common[0].ID.value == 1
        assert d_rtu.common[0].L.value == 66
        assert d_rtu.common[0].Mn.value == "SunSpecTest"
        assert d_rtu.common[0].Md.value == "TestDevice-2"
        assert d_rtu.common[0].Opt.value == "opt_a_b_c"
        assert d_rtu.common[0].Vr.value == "1.2.3"
        assert d_rtu.common[0].SN.value == "sn-123456789"
        assert d_rtu.common[0].DA.value == 1
        assert d_rtu.common[0].Pad.value == 0

        monkeypatch.setattr(socket, 'socket', MockSocket.mock_socket)
        monkeypatch.setattr(client.SunSpecModbusClientDeviceTCP, 'connect', MockSocket.mock_tcp_connect)
        monkeypatch.setattr(client.SunSpecModbusClientDeviceTCP, 'disconnect', MockSocket.mock_tcp_connect)

        c_tcp = client.SunSpecModbusClientDeviceTCP()
        tcp_buffer = [b'\x00\x00\x00\x00\x00\x03\x01\x83\x02',
                      b'\x00\x00\x00\x00\x00\t\x01\x03\x06',
                      b'SunS\x00\x01',
                      b'\x00\x00\x00\x00\x00\x05\x01\x03\x02',
                      b'\x00B',
                      b'\x00\x00\x00\x00\x00\x05\x01\x03\x02',
                      b'\xff\xff',
                      b'\x00\x00\x00\x00\x00\x8b\x01\x03\x88',
                      b'\x00\x01\x00BSunSpecTest\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00Test-1547-1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00opt_a_b_c\x00\x00\x00\x00\x00\x00\x001.2.3\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00sn-123456789\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x01\x00\x00']
        c_tcp.client.connect()
        c_tcp.client.socket._set_buffer(tcp_buffer)
        c_tcp.scan(full_model_read=False)
        c_tcp.models['common'][0].read()
        assert c_tcp.models['common'][0].__class__.__name__ == "SunSpecModbusClientModel"
        assert c_tcp.common[0].ID.value == 1
        assert c_tcp.common[0].L.value == 66
        assert c_tcp.common[0].Mn.value == "SunSpecTest"
        assert c_tcp.common[0].Md.value == "Test-1547-1"
        assert c_tcp.common[0].Opt.value == "opt_a_b_c"
        assert c_tcp.common[0].Vr.value == "1.2.3"
        assert c_tcp.common[0].SN.value == "sn-123456789"
        assert c_tcp.common[0].DA.value == 1
        assert c_tcp.common[0].Pad.value == 0


class TestSunSpecModbusClientDevice:
    def test___init__(self):
        d = client.SunSpecModbusClientDevice()
        assert d.did
        assert d.retry_count == 2
        assert d.base_addr_list == [40000, 0, 50000]
        assert d.base_addr is None

    def test_connect(self):
        pass

    def test_disconnect(self):
        pass

    def test_close(self):
        pass

    def test_read(self):
        pass

    def test_write(self):
        pass

    def test_scan(self, monkeypatch):
        # tcp scan
        monkeypatch.setattr(socket, 'socket', MockSocket.mock_socket)
        monkeypatch.setattr(client.SunSpecModbusClientDeviceTCP, 'connect', MockSocket.mock_tcp_connect)
        monkeypatch.setattr(client.SunSpecModbusClientDeviceTCP, 'disconnect', MockSocket.mock_tcp_connect)

        c_tcp = client.SunSpecModbusClientDeviceTCP()
        tcp_req_check = [b'\x00\x00\x00\x00\x00\x06\x01\x03\x9c@\x00\x03',
                         b'\x00\x00\x00\x00\x00\x06\x01\x03\x9cC\x00\x01',
                         b'\x00\x00\x00\x00\x00\x06\x01\x03\x9cB\x00D',
                         b'\x00\x00\x00\x00\x00\x06\x01\x03\x9c\x86\x00\x01']
        tcp_buffer = [b'\x00\x00\x00\x00\x00\t\x01\x03\x06',
                      b'SunS\x00\x01',
                      b'\x00\x00\x00\x00\x00\x05\x01\x03\x02',
                      b'\x00B',
                      b'\x00\x00\x00\x00\x00\x8b\x01\x03\x88',
                      b'\x00\x01\x00BSunSpecTest\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00TestDevice-1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00opt_a_b_c\x00\x00\x00\x00\x00\x00\x001.2.3\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00sn-123456789\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00',
                      b'\x00\x00\x00\x00\x00\x05\x01\x03\x02',
                      b'\x00~',
                      b'\x00\x00\x00\x00\x00\x05\x01\x03\x02',
                      b'\x00@',
                      b'\x00\x00\x00\x00\x00\x87\x01\x03\x84',
                      b'\x00~\x00@\x00\x03\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x80\x00\x80\x00\x80\x00\xff'
                      b'\xff\xff\xff\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00'
                      b'\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80'
                      b'\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff'
                      b'\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff',
                      b'\x00\x00\x00\x00\x00\x05\x01\x03\x02',
                      b'\xff\xff']
        c_tcp.client.connect()
        c_tcp.client.socket._set_buffer(tcp_buffer)
        c_tcp.scan()
        assert c_tcp.common
        assert c_tcp.volt_var
        for req in range(len(tcp_req_check)):
            assert tcp_req_check[req] == c_tcp.client.socket.request[req]

        # test full model read = false on scan
        # also tests successive scans
        c_tcp.client.socket.clear_buffer()
        c_tcp.client.socket.request = []
        tcp_buffer2 = [
            b'\x00\x00\x00\x00\x00\t\x01\x03\x06',
            b'SunS\x00\x01',
            b'\x00\x00\x00\x00\x00\x05\x01\x03\x02',
            b'\x00B',
            b'\x00\x00\x00\x00\x00\x05\x01\x03\x02',
            b'\xff\xff'
        ]
        tcp_req_check2 = [
            b'\x00\x00\x00\x00\x00\x06\x01\x03\x9c@\x00\x03',
            b'\x00\x00\x00\x00\x00\x06\x01\x03\x9cC\x00\x01',
            b'\x00\x00\x00\x00\x00\x06\x01\x03\x9c\x86\x00\x01'
        ]
        c_tcp.client.socket._set_buffer(tcp_buffer2)
        c_tcp.scan(full_model_read=False)
        assert c_tcp.common
        assert c_tcp.common[0].ID.value == 1
        assert c_tcp.common[0].L.value == 66
        assert c_tcp.common[0].Mn.value is None
        assert c_tcp.common[0].Md.value is None
        for req in range(len(tcp_req_check2)):
            assert tcp_req_check2[req] == c_tcp.client.socket.request[req]

        # rtu scan
        monkeypatch.setattr(serial, 'Serial', MockPort.mock_port)
        c_rtu = client.SunSpecModbusClientDeviceRTU(1, "COMM2")

        rtu_req_check = [
            b'\x01\x03\x9c@\x00\x03*O',
            b'\x01\x03\x9cC\x00\x01[\x8e',
            b'\x01\x03\x9cB\x00D\xcb\xbd',
            b'\x01\x03\x9c\x86\x00\x01K\xb3',
        ]
        rtu_buffer = [
            b'\x01\x03\x06Su',
            b'nS\x00\x01\x8d\xe4',
            b'\x01\x03\x02\x00B',
            b'8u',
            b'\x01\x03\x88\x00\x01',
            b'\x00BSunSpecTest\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            b'TestDevice-2\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00opt_a_b_c'
            b'\x00\x00\x00\x00\x00\x00\x001.2.3\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00sn-123456789\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\xb9\xfb',
            b'\x01\x03\x02\xff\xff',
            b'\xb9\xf4'
        ]
        c_rtu.open()
        c_rtu.client.serial._set_buffer(rtu_buffer)
        c_rtu.scan()
        assert c_rtu.common
        for req in range(len(rtu_req_check)):
            assert rtu_req_check[req] == c_rtu.client.serial.request[req]

        # test full model read = false on scan
        # also tests successive scans
        c_rtu.client.serial.clear_buffer()
        c_rtu.client.serial.request = []
        rtu_req_check2 = [
            b'\x01\x03\x9c@\x00\x03*O',
            b'\x01\x03\x9cC\x00\x01[\x8e',
            b'\x01\x03\x9c\x86\x00\x01K\xb3'
        ]
        rtu_buffer2 = [
            b'\x01\x03\x06Su',
            b'nS\x00\x01\x8d\xe4',
            b'\x01\x03\x02\x00B',
            b'8u',
            b'\x01\x03\x02\xff\xff',
            b'\xb9\xf4'
        ]
        c_rtu.client.serial._set_buffer(rtu_buffer2)
        c_rtu.scan(full_model_read=False)
        assert c_rtu.common
        assert c_rtu.common[0].ID.value == 1
        assert c_rtu.common[0].L.value == 66
        assert c_rtu.common[0].Mn.value is None
        assert c_rtu.common[0].Md.value is None
        for req in range(len(rtu_req_check2)):
            assert rtu_req_check2[req] == c_rtu.client.serial.request[req]

    def test_get_text(self, monkeypatch):
        # tcp scan
        monkeypatch.setattr(socket, 'socket', MockSocket.mock_socket)
        monkeypatch.setattr(client.SunSpecModbusClientDeviceTCP, 'connect', MockSocket.mock_tcp_connect)
        monkeypatch.setattr(client.SunSpecModbusClientDeviceTCP, 'disconnect', MockSocket.mock_tcp_connect)

        c_tcp = client.SunSpecModbusClientDeviceTCP()
        tcp_req_check = [b'\x00\x00\x00\x00\x00\x06\x01\x03\x00\x00\x00\x03',
                         b'\x00\x00\x00\x00\x00\x06\x01\x03\x00\x03\x00\x01',
                         b'\x00\x00\x00\x00\x00\x06\x01\x03\x00\x02\x00B',
                         b'\x00\x00\x00\x00\x00\x06\x01\x03\x00F\x00\x01',
                         b'\x00\x00\x00\x00\x00\x06\x01\x03\x00G\x00\x01',
                         b'\x00\x00\x00\x00\x00\x06\x01\x03\x00F\x00@',
                         b'\x00\x00\x00\x00\x00\x06\x01\x03\x00\x88\x00\x01']
        tcp_buffer = [b'\x00\x00\x00\x00\x00\t\x01\x03\x06',
                      b'SunS\x00\x01',
                      b'\x00\x00\x00\x00\x00\x05\x01\x03\x02',
                      b'\x00B',
                      b'\x00\x00\x00\x00\x00\x8b\x01\x03\x88',
                      b'\x00\x01\x00BSunSpecTest\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00TestDevice-1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00opt_a_b_c\x00\x00\x00\x00\x00\x00\x001.2.3\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00sn-123456789\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00',
                      b'\x00\x00\x00\x00\x00\x05\x01\x03\x02',
                      b'\x00~',
                      b'\x00\x00\x00\x00\x00\x05\x01\x03\x02',
                      b'\x00@',
                      b'\x00\x00\x00\x00\x00\x87\x01\x03\x84',
                      b'\x00~\x00@\x00\x03\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x80\x00\x80\x00\x80\x00\xff'
                      b'\xff\xff\xff\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00'
                      b'\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80'
                      b'\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff'
                      b'\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff',
                      b'\x00\x00\x00\x00\x00\x05\x01\x03\x02',
                      b'\xff\xff']
        c_tcp.client.connect()
        c_tcp.client.socket._set_buffer(tcp_buffer)
        c_tcp.scan()
        expected_output = \
            '''Model: common (1)\n\n      ID                                                    1\n      L       ''' + \
            '''                                             66\n      Mn                                         ''' + \
            ''' SunSpecTest\n      Md                                         TestDevice-1\n      Opt            ''' + \
            '''                               opt_a_b_c\n      Vr                                                ''' + \
            '''1.2.3\n      SN                                         sn-123456789\n      DA                    ''' + \
            '''                                1\n      Pad                                                   0\n''' + \
            '''\nModel: volt_var (126)\n\n      ID                                                  126\n      L ''' + \
            '''                                                   64\n      ActCrv                               ''' + \
            '''                 3\n      ModEna                                             None\n      WinTms   ''' + \
            '''                                          None Secs\n      RvrtTms                                ''' + \
            '''            None Secs\n      RmpTms                                             None Secs\n      N''' + \
            '''Crv                                               None\n      NPt                                 ''' + \
            '''               None\n      V_SF                                               None\n      DeptRef_''' + \
            '''SF                                         None\n      RmpIncDec_SF                               ''' + \
            '''        None\n   01:ActPt                                              None\n   01:DeptRef        ''' + \
            '''                                    None\n   01:V1                                                ''' + \
            ''' None % VRef\n   01:VAr1                                               None\n   01:V2             ''' + \
            '''                                    None % VRef\n   01:VAr2                                       ''' + \
            '''        None\n   01:V3                                                 None % VRef\n   01:VAr3    ''' + \
            '''                                           None\n   01:V4                                         ''' + \
            '''        None % VRef\n   01:VAr4                                               None\n   01:V5      ''' + \
            '''                                           None % VRef\n   01:VAr5                                ''' + \
            '''               None\n   01:V6                                                 None % VRef\n   01:V''' + \
            '''Ar6                                               None\n   01:V7                                  ''' + \
            '''               None % VRef\n   01:VAr7                                               None\n   01:V''' + \
            '''8                                                 None % VRef\n   01:VAr8                         ''' + \
            '''                      None\n   01:V9                                                 None % VRef\n''' + \
            '''   01:VAr9                                               None\n   01:V10                          ''' + \
            '''                      None % VRef\n   01:VAr10                                              None\n''' + \
            '''   01:V11                                                None % VRef\n   01:VAr11                 ''' + \
            '''                             None\n   01:V12                                                None %''' + \
        ''' VRef\n   01:VAr12                                              None\n   01:V13                       ''' + \
            '''                         None % VRef\n   01:VAr13                                              Non''' + \
            '''e\n   01:V14                                                None % VRef\n   01:VAr14              ''' + \
            '''                                None\n   01:V15                                                Non''' + \
            '''e % VRef\n   01:VAr15                                              None\n   01:V16                ''' + \
            '''                                None % VRef\n   01:VAr16                                          ''' + \
            '''    None\n   01:V17                                                None % VRef\n   01:VAr17       ''' + \
            '''                                       None\n   01:V18                                            ''' + \
            '''    None % VRef\n   01:VAr18                                              None\n   01:V19         ''' + \
            '''                                       None % VRef\n   01:VAr19                                   ''' + \
            '''           None\n   01:V20                                                None % VRef\n   01:VAr20''' + \
            '''                                              None\n   01:CrvNam                                  ''' + \
            '''           None\n   01:RmpTms                                             None Secs\n   01:RmpDecT''' + \
            '''mm                                          None % ref_value/min\n   01:RmpIncTmm                 ''' + \
            '''                         None % ref_value/min\n   01:ReadOnly                                     ''' + \
            '''      None\n'''
        get_text_output = c_tcp.get_text()
        assert get_text_output[get_text_output.index('Model'):] == expected_output

        # rtu scan
        monkeypatch.setattr(serial, 'Serial', MockPort.mock_port)
        c_rtu = client.SunSpecModbusClientDeviceRTU(1, "COMM2")

        rtu_req_check = [b'\x01\x03\x00\x00\x00\x03\x05\xcb', b'\x01\x03\x00\x03\x00\x01t\n',
                         b'\x01\x03\x00\x02\x00Bd;', b'\x01\x03\x00F\x00\x01e\xdf', b'\x01\x03\x00G\x00\x014\x1f',
                         b'\x01\x03\x00F\x00@\xa5\xef', b'\x01\x03\x00\x88\x00\x01\x04 ']
        rtu_buffer = [b'\x01\x03\x06Su',
                      b'nS\x00\x01\x8d\xe4',
                      b'\x01\x03\x02\x00B',
                      b'8u',
                      b'\x01\x03\x88\x00\x01',
                      b'\x00BSunSpecTest\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00TestDevice-1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00opt_a_b_c\x00\x00\x00\x00\x00\x00\x001.2.3\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00sn-123456789\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x01\x00\x00M\xf9',
                      b'\x01\x03\x02\x00~',
                      b'8d',
                      b'\x01\x03\x02\x00@',
                      b'\xb9\xb4',
                      b'\x01\x03\x84\x00~',
                      b'\x00@\x00\x03\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x80\x00\x80\x00\x80\x00'
                      b'\xff\xff\xff\xff\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff'
                      b'\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00'
                      b'\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff'
                      b'\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xffI',
                      b'\x01\x03\x02\xff\xff',
                      b'\xb9\xf4']
        c_rtu.open()
        c_rtu.client.serial._set_buffer(rtu_buffer)
        c_rtu.scan()
        get_text_output = c_rtu.get_text()
        assert get_text_output[get_text_output.index('Model'):] == expected_output


class TestSunSpecModbusClientDeviceTCP:
    def test___init__(self):
        d = client.SunSpecModbusClientDeviceTCP()
        assert d.slave_id == 1
        assert d.ipaddr == '127.0.0.1'
        assert d.ipport == 502
        assert d.timeout is None
        assert d.ctx is None
        assert d.trace_func is None
        assert d.max_count == 125
        assert d.client.__class__.__name__ == 'ModbusClientTCP'

    def test_connect(self, monkeypatch):
        d = client.SunSpecModbusClientDeviceTCP()
        with pytest.raises(Exception) as exc:
            d.connect()

        assert 'Connection error' in str(exc.value)
        monkeypatch.setattr(socket, 'socket', MockSocket.mock_socket)

        d.connect()
        assert d.client.socket is not None
        assert d.client.socket.connected is True
        assert d.client.socket.ipaddr == '127.0.0.1'
        assert d.client.socket.ipport == 502
        assert d.client.socket.timeout == 2

    def test_disconnect(self, monkeypatch):
        monkeypatch.setattr(socket, 'socket', MockSocket.mock_socket)

        d = client.SunSpecModbusClientDeviceTCP()
        d.client.connect()
        assert d.client.socket
        d.client.disconnect()
        assert d.client.socket is None

    def test_read(self, monkeypatch):
        monkeypatch.setattr(socket, 'socket', MockSocket.mock_socket)
        d = client.SunSpecModbusClientDeviceTCP()
        buffer = [b'\x00\x00\x00\x00\x00\x8f\x01\x03\x8c', b'SunS\x00\x01\x00BSunSpecTest\x00\x00\x00\x00\x00\x00'
                                                           b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                                           b'\x00\x00TestDevice-1\x00\x00\x00\x00\x00\x00\x00\x00'
                                                           b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00opt_a_b_c'
                                                           b'\x00\x00\x00\x00\x00\x00\x001.2.3\x00\x00\x00\x00\x00'
                                                           b'\x00\x00\x00\x00\x00\x00sn-123456789\x00\x00\x00\x00'
                                                           b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                                           b'\x00\x00\x00\x00\x01\x00\x00']
        check_req = b'\x00\x00\x00\x00\x00\x06\x01\x03\x9c@\x00F'
        d.client.connect()
        d.client.socket._set_buffer(buffer)
        assert d.read(40000, 70) == buffer[1]
        assert d.client.socket.request[0] == check_req

    def test_write(self, monkeypatch):
        monkeypatch.setattr(socket, 'socket', MockSocket.mock_socket)
        d = client.SunSpecModbusClientDeviceTCP()
        d.client.connect()

        data_to_write = b'sn-000\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

        buffer = [b'\x00\x00\x00\x00\x00\x06\x01\x10\x9c', b't\x00\x10']
        d.client.socket._set_buffer(buffer)
        d.client.write(40052, data_to_write)

        check_req = b"\x00\x00\x00\x00\x00'\x01\x10\x9ct\x00\x10 sn-000\x00\x00\x00\x00\x00\x00\x00" \
                    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        assert d.client.socket.request[0] == check_req

    def test_get_text(self, monkeypatch):
        # tcp scan
        monkeypatch.setattr(socket, 'socket', MockSocket.mock_socket)
        monkeypatch.setattr(client.SunSpecModbusClientDeviceTCP, 'connect', MockSocket.mock_tcp_connect)
        monkeypatch.setattr(client.SunSpecModbusClientDeviceTCP, 'disconnect', MockSocket.mock_tcp_connect)

        c_tcp = client.SunSpecModbusClientDeviceTCP()
        tcp_req_check = [b'\x00\x00\x00\x00\x00\x06\x01\x03\x00\x00\x00\x03',
                         b'\x00\x00\x00\x00\x00\x06\x01\x03\x00\x03\x00\x01',
                         b'\x00\x00\x00\x00\x00\x06\x01\x03\x00\x02\x00B',
                         b'\x00\x00\x00\x00\x00\x06\x01\x03\x00F\x00\x01',
                         b'\x00\x00\x00\x00\x00\x06\x01\x03\x00G\x00\x01',
                         b'\x00\x00\x00\x00\x00\x06\x01\x03\x00F\x00@',
                         b'\x00\x00\x00\x00\x00\x06\x01\x03\x00\x88\x00\x01']
        tcp_buffer = [b'\x00\x00\x00\x00\x00\t\x01\x03\x06',
                      b'SunS\x00\x01',
                      b'\x00\x00\x00\x00\x00\x05\x01\x03\x02',
                      b'\x00B',
                      b'\x00\x00\x00\x00\x00\x8b\x01\x03\x88',
                      b'\x00\x01\x00BSunSpecTest\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00TestDevice-1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00opt_a_b_c\x00\x00\x00\x00\x00\x00\x001.2.3\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00sn-123456789\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00',
                      b'\x00\x00\x00\x00\x00\x05\x01\x03\x02',
                      b'\x00~',
                      b'\x00\x00\x00\x00\x00\x05\x01\x03\x02',
                      b'\x00@',
                      b'\x00\x00\x00\x00\x00\x87\x01\x03\x84',
                      b'\x00~\x00@\x00\x03\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x80\x00\x80\x00\x80\x00\xff'
                      b'\xff\xff\xff\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00'
                      b'\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80'
                      b'\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff'
                      b'\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff',
                      b'\x00\x00\x00\x00\x00\x05\x01\x03\x02',
                      b'\xff\xff']
        c_tcp.client.connect()
        c_tcp.client.socket._set_buffer(tcp_buffer)
        c_tcp.scan()
        expected_output = \
            '''Model: common (1)\n\n      ID                                                    1\n      L       ''' + \
            '''                                             66\n      Mn                                         ''' + \
            ''' SunSpecTest\n      Md                                         TestDevice-1\n      Opt            ''' + \
            '''                               opt_a_b_c\n      Vr                                                ''' + \
            '''1.2.3\n      SN                                         sn-123456789\n      DA                    ''' + \
            '''                                1\n      Pad                                                   0\n''' + \
            '''\nModel: volt_var (126)\n\n      ID                                                  126\n      L ''' + \
            '''                                                   64\n      ActCrv                               ''' + \
            '''                 3\n      ModEna                                             None\n      WinTms   ''' + \
            '''                                          None Secs\n      RvrtTms                                ''' + \
            '''            None Secs\n      RmpTms                                             None Secs\n      N''' + \
            '''Crv                                               None\n      NPt                                 ''' + \
            '''               None\n      V_SF                                               None\n      DeptRef_''' + \
            '''SF                                         None\n      RmpIncDec_SF                               ''' + \
            '''        None\n   01:ActPt                                              None\n   01:DeptRef        ''' + \
            '''                                    None\n   01:V1                                                ''' + \
            ''' None % VRef\n   01:VAr1                                               None\n   01:V2             ''' + \
            '''                                    None % VRef\n   01:VAr2                                       ''' + \
            '''        None\n   01:V3                                                 None % VRef\n   01:VAr3    ''' + \
            '''                                           None\n   01:V4                                         ''' + \
            '''        None % VRef\n   01:VAr4                                               None\n   01:V5      ''' + \
            '''                                           None % VRef\n   01:VAr5                                ''' + \
            '''               None\n   01:V6                                                 None % VRef\n   01:V''' + \
            '''Ar6                                               None\n   01:V7                                  ''' + \
            '''               None % VRef\n   01:VAr7                                               None\n   01:V''' + \
            '''8                                                 None % VRef\n   01:VAr8                         ''' + \
            '''                      None\n   01:V9                                                 None % VRef\n''' + \
            '''   01:VAr9                                               None\n   01:V10                          ''' + \
            '''                      None % VRef\n   01:VAr10                                              None\n''' + \
            '''   01:V11                                                None % VRef\n   01:VAr11                 ''' + \
            '''                             None\n   01:V12                                                None %''' + \
            ''' VRef\n   01:VAr12                                              None\n   01:V13                       ''' + \
            '''                         None % VRef\n   01:VAr13                                              Non''' + \
            '''e\n   01:V14                                                None % VRef\n   01:VAr14              ''' + \
            '''                                None\n   01:V15                                                Non''' + \
            '''e % VRef\n   01:VAr15                                              None\n   01:V16                ''' + \
            '''                                None % VRef\n   01:VAr16                                          ''' + \
            '''    None\n   01:V17                                                None % VRef\n   01:VAr17       ''' + \
            '''                                       None\n   01:V18                                            ''' + \
            '''    None % VRef\n   01:VAr18                                              None\n   01:V19         ''' + \
            '''                                       None % VRef\n   01:VAr19                                   ''' + \
            '''           None\n   01:V20                                                None % VRef\n   01:VAr20''' + \
            '''                                              None\n   01:CrvNam                                  ''' + \
            '''           None\n   01:RmpTms                                             None Secs\n   01:RmpDecT''' + \
            '''mm                                          None % ref_value/min\n   01:RmpIncTmm                 ''' + \
            '''                         None % ref_value/min\n   01:ReadOnly                                     ''' + \
            '''      None\n'''
        get_text_output = c_tcp.get_text()
        assert get_text_output[get_text_output.index('Model'):] == expected_output


class TestSunSpecModbusClientDeviceRTU:
    def test___init__(self, monkeypatch):
        monkeypatch.setattr(serial, 'Serial', MockPort.mock_port)
        d = client.SunSpecModbusClientDeviceRTU(1, "COMM2")
        assert d.slave_id == 1
        assert d.name == "COMM2"
        assert d.client.__class__.__name__ == "ModbusClientRTU"
        assert d.ctx is None
        assert d.trace_func is None
        assert d.max_count == 125

    def test_open(self, monkeypatch):
        monkeypatch.setattr(serial, 'Serial', MockPort.mock_port)
        d = client.SunSpecModbusClientDeviceRTU(1, "COMM2")
        d.open()
        assert d.client.serial.connected

    def test_close(self, monkeypatch):
        monkeypatch.setattr(serial, 'Serial', MockPort.mock_port)
        d = client.SunSpecModbusClientDeviceRTU(1, "COMM2")
        d.open()
        d.close()
        assert not d.client.serial.connected

    def test_read(self, monkeypatch):
        monkeypatch.setattr(serial, 'Serial', MockPort.mock_port)
        d = client.SunSpecModbusClientDeviceRTU(1, "COMM2")
        d.open()
        in_buff = [b'\x01\x03\x8cSu', b'nS\x00\x01\x00BSunSpecTest\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                      b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00TestDevice-1\x00\x00\x00\x00\x00'
                                      b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00opt_a_b_c\x00'
                                      b'\x00\x00\x00\x00\x00\x001.2.3\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                      b'sn-123456789\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                      b'\x00\x00\x00\x00\x00\x00\x01\x00\x00\xb7d']
        check_req = b'\x01\x03\x9c@\x00F\xeb\xbc'
        d.client.serial._set_buffer(in_buff)
        check_read = in_buff[0] + in_buff[1]
        assert d.read(40000, 70) == check_read[3:-2]
        assert d.client.serial.request[0] == check_req

    def test_write(self, monkeypatch):
        monkeypatch.setattr(serial, 'Serial', MockPort.mock_port)
        d = client.SunSpecModbusClientDeviceRTU(1, "COMM2")
        d.open()
        data_to_write = b'v0.0.0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00sn-000\x00\x00\x00\x00\x00\x00\x00' \
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

        buffer = [b'\x01\x10\x9cl\x00', b'\x18.N']
        d.client.serial._set_buffer(buffer)
        d.write(40044, data_to_write)

        check_req = b'\x01\x10\x9cl\x00\x180v0.0.0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00sn-000\x00' \
                    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                    b'\x00\x00\x00\x00\x00\xad\xff'
        assert d.client.serial.request[0] == check_req

    def test_get_text(self, monkeypatch):
        # rtu scan
        monkeypatch.setattr(serial, 'Serial', MockPort.mock_port)
        c_rtu = client.SunSpecModbusClientDeviceRTU(1, "COMM2")

        rtu_req_check = [b'\x01\x03\x00\x00\x00\x03\x05\xcb', b'\x01\x03\x00\x03\x00\x01t\n',
                         b'\x01\x03\x00\x02\x00Bd;', b'\x01\x03\x00F\x00\x01e\xdf', b'\x01\x03\x00G\x00\x014\x1f',
                         b'\x01\x03\x00F\x00@\xa5\xef', b'\x01\x03\x00\x88\x00\x01\x04 ']
        rtu_buffer = [b'\x01\x03\x06Su',
                      b'nS\x00\x01\x8d\xe4',
                      b'\x01\x03\x02\x00B',
                      b'8u',
                      b'\x01\x03\x88\x00\x01',
                      b'\x00BSunSpecTest\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00TestDevice-1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00opt_a_b_c\x00\x00\x00\x00\x00\x00\x001.2.3\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00sn-123456789\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x01\x00\x00M\xf9',
                      b'\x01\x03\x02\x00~',
                      b'8d',
                      b'\x01\x03\x02\x00@',
                      b'\xb9\xb4',
                      b'\x01\x03\x84\x00~',
                      b'\x00@\x00\x03\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x80\x00\x80\x00\x80\x00'
                      b'\xff\xff\xff\xff\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff'
                      b'\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00'
                      b'\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff'
                      b'\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\xff\xff\x80\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xffI',
                      b'\x01\x03\x02\xff\xff',
                      b'\xb9\xf4']
        expected_output = \
            '''Model: common (1)\n\n      ID                                                    1\n      L       ''' + \
            '''                                             66\n      Mn                                         ''' + \
            ''' SunSpecTest\n      Md                                         TestDevice-1\n      Opt            ''' + \
            '''                               opt_a_b_c\n      Vr                                                ''' + \
            '''1.2.3\n      SN                                         sn-123456789\n      DA                    ''' + \
            '''                                1\n      Pad                                                   0\n''' + \
            '''\nModel: volt_var (126)\n\n      ID                                                  126\n      L ''' + \
            '''                                                   64\n      ActCrv                               ''' + \
            '''                 3\n      ModEna                                             None\n      WinTms   ''' + \
            '''                                          None Secs\n      RvrtTms                                ''' + \
            '''            None Secs\n      RmpTms                                             None Secs\n      N''' + \
            '''Crv                                               None\n      NPt                                 ''' + \
            '''               None\n      V_SF                                               None\n      DeptRef_''' + \
            '''SF                                         None\n      RmpIncDec_SF                               ''' + \
            '''        None\n   01:ActPt                                              None\n   01:DeptRef        ''' + \
            '''                                    None\n   01:V1                                                ''' + \
            ''' None % VRef\n   01:VAr1                                               None\n   01:V2             ''' + \
            '''                                    None % VRef\n   01:VAr2                                       ''' + \
            '''        None\n   01:V3                                                 None % VRef\n   01:VAr3    ''' + \
            '''                                           None\n   01:V4                                         ''' + \
            '''        None % VRef\n   01:VAr4                                               None\n   01:V5      ''' + \
            '''                                           None % VRef\n   01:VAr5                                ''' + \
            '''               None\n   01:V6                                                 None % VRef\n   01:V''' + \
            '''Ar6                                               None\n   01:V7                                  ''' + \
            '''               None % VRef\n   01:VAr7                                               None\n   01:V''' + \
            '''8                                                 None % VRef\n   01:VAr8                         ''' + \
            '''                      None\n   01:V9                                                 None % VRef\n''' + \
            '''   01:VAr9                                               None\n   01:V10                          ''' + \
            '''                      None % VRef\n   01:VAr10                                              None\n''' + \
            '''   01:V11                                                None % VRef\n   01:VAr11                 ''' + \
            '''                             None\n   01:V12                                                None %''' + \
            ''' VRef\n   01:VAr12                                              None\n   01:V13                       ''' + \
            '''                         None % VRef\n   01:VAr13                                              Non''' + \
            '''e\n   01:V14                                                None % VRef\n   01:VAr14              ''' + \
            '''                                None\n   01:V15                                                Non''' + \
            '''e % VRef\n   01:VAr15                                              None\n   01:V16                ''' + \
            '''                                None % VRef\n   01:VAr16                                          ''' + \
            '''    None\n   01:V17                                                None % VRef\n   01:VAr17       ''' + \
            '''                                       None\n   01:V18                                            ''' + \
            '''    None % VRef\n   01:VAr18                                              None\n   01:V19         ''' + \
            '''                                       None % VRef\n   01:VAr19                                   ''' + \
            '''           None\n   01:V20                                                None % VRef\n   01:VAr20''' + \
            '''                                              None\n   01:CrvNam                                  ''' + \
            '''           None\n   01:RmpTms                                             None Secs\n   01:RmpDecT''' + \
            '''mm                                          None % ref_value/min\n   01:RmpIncTmm                 ''' + \
            '''                         None % ref_value/min\n   01:ReadOnly                                     ''' + \
            '''      None\n'''
        c_rtu.open()
        c_rtu.client.serial._set_buffer(rtu_buffer)
        c_rtu.scan()
        get_text_output = c_rtu.get_text()
        assert get_text_output[get_text_output.index('Model'):] == expected_output


class TestSunSpecFileClientDevice(object):
    def test___init__(self):
        d = file_client.FileClientDevice(filename=None, addr=40002)
        assert d.filename is None
        assert d.addr == 40002

    def test_scan(self):
        d = file_client.FileClientDevice(filename='./sunspec2/tests/test_data/device_1547.json', addr=40002)
        d.scan()
        assert d.models['common'][0] is not None
        assert d.models['common'][0].Mn.cvalue == 'SunSpecTest'
        assert d.models['common'][0].Md.cvalue == 'Test-1547-1'
        assert d.models['common'][0].Opt.cvalue == 'opt_a_b_c'
        assert d.models['common'][0].Vr.cvalue == '1.2.3'
        assert d.models['common'][0].SN.cvalue == 'sn-123456789'
        assert d.models['common'][0].DA.cvalue == 1
        assert d.models['common'][0].Pad.cvalue == 0

    def test_close(self):
        pass

    def test_read(self):
        d = file_client.FileClientDevice(filename='./sunspec2/tests/test_data/device_1547.json', addr=40002)
        d.scan()
        assert d.models['common'][0].model_addr == 40002
        assert d.models['common'][0].points_len == 68
        assert d.models['common'][0].len == 68
        assert d.models['DERMeasureAC'][0].model_addr == 40070
        assert d.models['DERMeasureAC'][0].points_len == 155
        assert d.models['DERMeasureAC'][0].len == 155
        assert d.models['DERMeasureAC'][0].ID.cvalue == 701
        assert d.models['DERMeasureAC'][0].L.cvalue == 153
        assert d.models['DERCapacity'][0].L.cvalue == 50
        assert d.models['DERCapacity'][0].len == 52
        assert d.models['DERCtlAC'][0].len == 67
        assert d.models['DERCtlAC'][0].points_len == 59

    def test_write(self):
        d = file_client.FileClientDevice(filename='./sunspec2/tests/test_data/device_1547.json', addr=40002)
        d.scan()
        d.models['common'][0].SN.cvalue = 'sn-000'
        d.write()
        d.read()
        assert d.models['common'][0].SN.cvalue == 'sn-000'



if __name__ == "__main__":
    pass

