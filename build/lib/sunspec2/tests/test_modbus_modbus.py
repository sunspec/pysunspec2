import sunspec2.modbus.modbus as modbus_client
import pytest
import socket
import serial
import sunspec2.tests.mock_socket as MockSocket
import sunspec2.tests.mock_port as MockPort


def test_modbus_rtu_client(monkeypatch):
    monkeypatch.setattr(serial, 'Serial', MockPort.mock_port)
    c = modbus_client.modbus_rtu_client('COMM2')
    assert c.baudrate == 9600
    assert c.parity == "N"
    assert modbus_client.modbus_rtu_clients['COMM2']

    with pytest.raises(modbus_client.ModbusClientError) as exc1:
        c2 = modbus_client.modbus_rtu_client('COMM2', baudrate=99)
    assert 'Modbus client baudrate mismatch' in str(exc1.value)

    with pytest.raises(modbus_client.ModbusClientError) as exc2:
        c2 = modbus_client.modbus_rtu_client('COMM2', parity='E')
    assert 'Modbus client parity mismatch' in str(exc2.value)


def test_modbus_rtu_client_remove(monkeypatch):
    monkeypatch.setattr(serial, 'Serial', MockPort.mock_port)
    c = modbus_client.modbus_rtu_client('COMM2')
    assert modbus_client.modbus_rtu_clients['COMM2']
    modbus_client.modbus_rtu_client_remove('COMM2')
    assert modbus_client.modbus_rtu_clients.get('COMM2') is None


def test___generate_crc16_table():
    pass


def test_computeCRC():
    pass


def test_checkCRC():
    pass


class TestModbusClientRTU:
    def test___init__(self, monkeypatch):
        monkeypatch.setattr(serial, 'Serial', MockPort.mock_port)
        c = modbus_client.ModbusClientRTU(name="COM2")
        assert c.name == "COM2"
        assert c.baudrate == 9600
        assert c.parity is None
        assert c.serial is not None
        assert c.timeout == .5
        assert c.write_timeout == .5
        assert not c.devices

    def test_open(self, monkeypatch):
        monkeypatch.setattr(serial, 'Serial', MockPort.mock_port)
        c = modbus_client.ModbusClientRTU(name="COM2")
        c.open()
        assert c.serial.connected

    def test_close(self, monkeypatch):
        monkeypatch.setattr(serial, 'Serial', MockPort.mock_port)
        c = modbus_client.ModbusClientRTU(name="COM2")
        c.open()
        c.close()
        assert not c.serial.connected

    def test_add_device(self, monkeypatch):
        monkeypatch.setattr(serial, 'Serial', MockPort.mock_port)
        c = modbus_client.ModbusClientRTU(name="COM2")
        c.add_device(1, "1")
        assert c.devices.get(1) is not None
        assert c.devices[1] == "1"

    def test_remove_device(self, monkeypatch):
        monkeypatch.setattr(serial, 'Serial', MockPort.mock_port)
        c = modbus_client.ModbusClientRTU(name="COM2")
        c.add_device(1, "1")
        assert c.devices.get(1) is not None
        assert c.devices[1] == "1"
        c.remove_device(1)
        assert c.devices.get(1) is None

    def test__read(self):
        pass

    def test_read(self, monkeypatch):
        monkeypatch.setattr(serial, 'Serial', MockPort.mock_port)
        c = modbus_client.ModbusClientRTU(name="COM2")
        in_buff = [b'\x01\x03\x8cSu', b'nS\x00\x01\x00BSunSpecTest\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                      b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00TestDevice-1\x00\x00\x00\x00\x00'
                                      b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00opt_a_b_c\x00'
                                      b'\x00\x00\x00\x00\x00\x001.2.3\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                      b'sn-123456789\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                      b'\x00\x00\x00\x00\x00\x00\x01\x00\x00\xb7d']
        check_req = b'\x01\x03\x9c@\x00F\xeb\xbc'
        c.open()
        c.serial._set_buffer(in_buff)

        check_read = in_buff[0] + in_buff[1]
        assert c.read(1, 40000, 70) == check_read[3:-2]
        assert c.serial.request[0] == check_req

    def test__write(self):
        pass

    def test_write(self, monkeypatch):
        monkeypatch.setattr(serial, 'Serial', MockPort.mock_port)
        c = modbus_client.ModbusClientRTU(name="COM2")
        c.open()
        data_to_write = b'v0.0.0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00sn-000\x00\x00\x00\x00\x00\x00\x00' \
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

        buffer = [b'\x01\x10\x9cl\x00', b'\x18.N']
        c.serial._set_buffer(buffer)
        c.write(1, 40044, data_to_write)

        check_req = b'\x01\x10\x9cl\x00\x180v0.0.0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00sn-000\x00' \
                    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                    b'\x00\x00\x00\x00\x00\xad\xff'
        assert c.serial.request[0] == check_req


class TestModbusClientTCP:
    def test___init__(self):
        c = modbus_client.ModbusClientTCP()
        assert c.slave_id == 1
        assert c.ipaddr == '127.0.0.1'
        assert c.ipport == 502
        assert c.timeout == 2
        assert c.ctx is None
        assert c.trace_func is None
        assert c.max_count == 125

    def test_close(self, monkeypatch):
        monkeypatch.setattr(socket, 'socket', MockSocket.mock_socket)

        c = modbus_client.ModbusClientTCP()
        c.connect()
        assert c.socket
        c.disconnect()
        assert c.socket is None

    def test_connect(self, monkeypatch):
        c = modbus_client.ModbusClientTCP()

        with pytest.raises(Exception) as exc:
            c.connect()
        assert 'Connection error' in str(exc.value)

        monkeypatch.setattr(socket, 'socket', MockSocket.mock_socket)
        c.connect()
        assert c.socket is not None
        assert c.socket.connected is True
        assert c.socket.ipaddr == '127.0.0.1'
        assert c.socket.ipport == 502
        assert c.socket.timeout == 2

    def test_disconnect(self, monkeypatch):
        monkeypatch.setattr(socket, 'socket', MockSocket.mock_socket)

        c = modbus_client.ModbusClientTCP()
        c.connect()
        assert c.socket
        c.disconnect()
        assert c.socket is None

    def test__read(self, monkeypatch):
        pass

    def test_read(self, monkeypatch):
        c = modbus_client.ModbusClientTCP()
        monkeypatch.setattr(socket, 'socket', MockSocket.mock_socket)
        in_buff = [b'\x00\x00\x00\x00\x00\x8f\x01\x03\x8c', b'SunS\x00\x01\x00BSunSpecTest\x00\x00\x00\x00\x00\x00'
                                                            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                                            b'\x00\x00TestDevice-1\x00\x00\x00\x00\x00\x00\x00\x00'
                                                            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00opt_a_b_c'
                                                            b'\x00\x00\x00\x00\x00\x00\x001.2.3\x00\x00\x00\x00\x00'
                                                            b'\x00\x00\x00\x00\x00\x00sn-123456789\x00\x00\x00\x00'
                                                            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                                            b'\x00\x00\x00\x00\x01\x00\x00']
        check_req = b'\x00\x00\x00\x00\x00\x06\x01\x03\x9c@\x00F'
        c.connect()
        c.socket._set_buffer(in_buff)
        assert c.read(40000, 70) == in_buff[1]
        assert c.socket.request[0] == check_req

    def test__write(self, monkeypatch):
        pass

    def test_write(self, monkeypatch):
        c = modbus_client.ModbusClientTCP()
        monkeypatch.setattr(socket, 'socket', MockSocket.mock_socket)
        c.connect()
        data_to_write = b'sn-000\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

        buffer = [b'\x00\x00\x00\x00\x00\x06\x01\x10\x9c', b't\x00\x10']
        c.socket._set_buffer(buffer)
        c.write(40052, data_to_write)

        check_req = b"\x00\x00\x00\x00\x00'\x01\x10\x9ct\x00\x10 sn-000\x00\x00\x00\x00\x00\x00\x00" \
                    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        assert c.socket.request[0] == check_req
