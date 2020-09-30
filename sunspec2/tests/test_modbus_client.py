import sunspec2.modbus.client as client
import pytest
import socket
import sunspec2.tests.mock_socket as MockSocket
import serial
import sunspec2.tests.mock_port as MockPort


class TestSunSpecModbusClientPoint:
    def test_read(self, monkeypatch):
        monkeypatch.setattr(socket, 'socket', MockSocket.mock_socket)
        monkeypatch.setattr(serial, 'Serial', MockPort.mock_port)

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

        tcp_read_buffer = [b'\x00\x00\x00\x00\x00#\x01\x03 ',
                           b'sn-000\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                           b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00']
        d_tcp.client.socket.clear_buffer()
        d_tcp.client.socket._set_buffer(tcp_read_buffer)
        d_tcp.common[0].SN.read()
        assert d_tcp.common[0].SN.value == 'sn-000'
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

        d_rtu.common[0].SN.value = 'sn-000'
        assert d_rtu.common[0].SN.value == 'sn-000'
        assert d_rtu.common[0].SN.dirty

        rtu_write_buffer = [b'\x01\x10\x9ct\x00',
                            b'\x10\xaf\x8f']
        d_rtu.client.serial.clear_buffer()
        d_rtu.client.serial._set_buffer(rtu_write_buffer)
        d_rtu.common[0].write()

        d_rtu.common[0].SN.value = 'will be overwritten by read'
        assert d_rtu.common[0].SN.value == 'will be overwritten by read'
        assert d_rtu.common[0].SN.dirty

        rtu_read_buffer = [b'\x01\x03 sn',
                           b'-000\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                           b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\r\xfb']
        d_rtu.client.serial.clear_buffer()
        d_rtu.client.serial._set_buffer(rtu_read_buffer)
        d_rtu.common[0].SN.read()
        assert d_rtu.common[0].SN.value == 'sn-000'
        assert not d_rtu.common[0].SN.dirty


class TestSunSpecModbusClientGroup:
    def test_read(self, monkeypatch):
        monkeypatch.setattr(socket, 'socket', MockSocket.mock_socket)
        monkeypatch.setattr(serial, 'Serial', MockPort.mock_port)

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

        d_rtu.common[0].SN.value = 'sn-000'
        d_rtu.common[0].Vr.value = 'v0.0.0'
        assert d_rtu.common[0].SN.value == "sn-000"
        assert d_rtu.common[0].Vr.value == "v0.0.0"
        assert d_rtu.common[0].SN.dirty
        assert d_rtu.common[0].Vr.dirty

        rtu_write_buffer = [b'\x01\x10\x9cl\x00',
                            b'\x18.N']
        d_rtu.client.serial.clear_buffer()
        d_rtu.client.serial._set_buffer(rtu_write_buffer)
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


class TestSunSpecModbusClientModel:
    def test___init__(self):
        c = client.SunSpecModbusClientModel(704)
        assert c.model_id == 704
        assert c.model_addr == 0
        assert c.model_len == 0
        assert c.model_def['id'] == 704
        assert c.error_info == ''
        assert c.gdef['name'] == 'DERCtlAC'
        assert c.mid is None
        assert c.device is None
        assert c.model == c

    def test_error(self):
        c = client.SunSpecModbusClientModel(704)
        c.add_error('test error')
        assert c.error_info == 'test error\n'


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
        c_tcp = client.SunSpecModbusClientDeviceTCP()
        tcp_req_check = [b'\x00\x00\x00\x00\x00\x06\x01\x03\x9c@\x00\x03',
                         b'\x00\x00\x00\x00\x00\x06\x01\x03\x9cC\x00\x01',
                         b'\x00\x00\x00\x00\x00\x06\x01\x03\x9cB\x00D',
                         b'\x00\x00\x00\x00\x00\x06\x01\x03\x9c\x86\x00\x01',
                         b'\x00\x00\x00\x00\x00\x06\x01\x03\x9c\x87\x00\x01',
                         b'\x00\x00\x00\x00\x00\x06\x01\x03\x9c\x86\x00B',
                         b'\x00\x00\x00\x00\x00\x06\x01\x03\x9c\xc8\x00\x01']
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

        # rtu scan
        monkeypatch.setattr(serial, 'Serial', MockPort.mock_port)
        c_rtu = client.SunSpecModbusClientDeviceRTU(1, "COMM2")

        rtu_req_check = [b'\x01\x03\x9c@\x00\x03*O',
                         b'\x01\x03\x9cC\x00\x01[\x8e',
                         b'\x01\x03\x9cB\x00D\xcb\xbd',
                         b'\x01\x03\x9c\x86\x00\x01K\xb3',
                         b'\x01\x03\x9c\x87\x00\x01\x1as',
                         b'\x01\x03\x9c\x86\x00B\nB',
                         b'\x01\x03\x9c\xc8\x00\x01+\xa4']
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
        assert c_rtu.common
        assert c_rtu.volt_var
        for req in range(len(rtu_req_check)):
            assert rtu_req_check[req] == c_rtu.client.serial.request[req]


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


if __name__ == "__main__":
    pass

