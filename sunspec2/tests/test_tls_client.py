import pytest
import ssl
import time
import threading
from pymodbus.server import StartTlsServer
from pymodbus.datastore import (
    ModbusServerContext,
    ModbusSequentialDataBlock,
)

# pymodbus renamed the per-device context (ModbusSlaveContext ->
# ModbusDeviceContext) during the 3.x series; accept either name.
try:
    from pymodbus.datastore import ModbusDeviceContext
except ImportError:  # older pymodbus 3.x
    from pymodbus.datastore import ModbusSlaveContext as ModbusDeviceContext
from sunspec2.modbus.client import SunSpecModbusClientDeviceTCP
import os

BASE_DIR = os.path.dirname(__file__)
TLS_DATA = os.path.join(BASE_DIR, "tls_data")
# Trust anchors: a server validates client certificates against the
# client CA chain, and a client validates the server against the
# server CA chain. See tls_data/README.md for the directory layout.
CAFILE_SERVER = os.path.join(TLS_DATA, "ca", "server_ca_chain.crt")
CAFILE_CLIENT = os.path.join(TLS_DATA, "ca", "client_ca_chain.crt")
CERTFILE = os.path.join(TLS_DATA, "server", "tls1_2", "server_valid.crt")
KEYFILE = os.path.join(TLS_DATA, "server", "tls1_2", "server_valid.key")
CLIENT_CERTFILE = os.path.join(TLS_DATA, "client", "tls1_2", "client_readonly.crt")
CLIENT_KEYFILE = os.path.join(TLS_DATA, "client", "tls1_2", "client_readonly.key")
IPADDR = "localhost"
IPPORT = 8502


def run_tls_modbus_server():
    # The server presents the server certificate and verifies connecting
    # clients against the client CA chain (mutual TLS).
    sslctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    sslctx.load_cert_chain(certfile=CERTFILE, keyfile=KEYFILE)
    sslctx.load_verify_locations(cafile=CAFILE_CLIENT)
    sslctx.verify_mode = ssl.CERT_REQUIRED

    # Data block starts at address 1 (pymodbus 3.13 rejects a 0 start).
    block = ModbusSequentialDataBlock(1, [0] * 100)
    store = ModbusDeviceContext(di=block, co=block, hr=block, ir=block)
    # ModbusServerContext gained the 'devices' keyword (replacing
    # 'slaves') during the pymodbus 3.x series.
    try:
        context = ModbusServerContext(devices=store, single=True)
    except TypeError:  # older pymodbus 3.x
        context = ModbusServerContext(slaves=store, single=True)

    StartTlsServer(context, address=(IPADDR, IPPORT), sslctx=sslctx)


@pytest.fixture(scope="module", autouse=True)
def tls_modbus_server():
    server_thread = threading.Thread(target=run_tls_modbus_server, daemon=True)
    server_thread.start()
    time.sleep(2)  # Give the server time to start
    yield


@pytest.mark.parametrize(
    "cafile, certfile, keyfile, ipaddr, ipport",
    [(CAFILE_SERVER, CLIENT_CERTFILE, CLIENT_KEYFILE, IPADDR, IPPORT)],
)
def test_tls_connection(cafile, certfile, keyfile, ipaddr, ipport):
    """
    Test TLS connection for SunSpecModbusClientDeviceTCP.
    The TLS-enabled Modbus TCP server is started automatically.

    The client validates the server against the server CA chain
    (``cafile``) and presents its own client certificate for mutual TLS.
    """
    device = SunSpecModbusClientDeviceTCP(
        slave_id=1,
        ipaddr=ipaddr,
        ipport=ipport,
        tls=True,
        cafile=cafile,
        certfile=certfile,
        keyfile=keyfile,
        insecure_skip_tls_verify=False,
    )
    try:
        device.connect()
        assert device.is_connected()
    except Exception as e:
        pytest.fail(f"TLS connection failed: {e}")
    finally:
        device.disconnect()
