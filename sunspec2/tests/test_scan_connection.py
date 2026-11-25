"""Exercise scan connection ownership against a loopback Modbus TCP peer."""
import socketserver
import struct
import threading

import pytest

from sunspec2.modbus.client import SunSpecModbusClientDeviceTCP


@pytest.fixture
def modbus_peer():
    # SunSpec identifier, common model, and end marker.
    registers = b'SunS' + struct.pack('>HH', 1, 66) + bytes(132) + b'\xff\xff\x00\x00'
    connections = []

    class Handler(socketserver.StreamRequestHandler):
        def handle(self):
            connections.append(self.request)
            while True:
                header = self.rfile.read(6)
                if not header:
                    return
                transaction, protocol, length = struct.unpack('>HHH', header)
                request = self.rfile.read(length)
                unit, function, address, count = struct.unpack('>BBHH', request)
                assert function == 3
                start = (address - 40000) * 2
                payload = registers[start:start + count * 2]
                response = bytes([unit, function, len(payload)]) + payload
                self.wfile.write(struct.pack('>HHH', transaction, protocol, len(response)) + response)

    with socketserver.ThreadingTCPServer(('127.0.0.1', 0), Handler) as server:
        thread = threading.Thread(target=server.serve_forever)
        thread.start()
        try:
            yield server.server_address, connections
        finally:
            server.shutdown()
            thread.join(timeout=2)


@pytest.mark.parametrize('preconnected,scan_connect', [(True, True), (True, False), (False, True)])
def test_scan_preserves_caller_connection(modbus_peer, preconnected, scan_connect):
    address, connections = modbus_peer
    device = SunSpecModbusClientDeviceTCP(ipaddr=address[0], ipport=address[1], timeout=1)
    try:
        if preconnected:
            device.connect()
        original_socket = device.client.socket
        device.scan(connect=scan_connect)
        assert device.base_addr == 40000
        assert device.models[1][0].ID.value == 1
        assert bool(device.is_connected()) == preconnected
        assert device.client.socket is original_socket
        if preconnected:
            # A later operation must reuse the same connection as the scan.
            assert device.read(40000, 2) == b'SunS'
        assert len(connections) == 1
    finally:
        device.disconnect()
