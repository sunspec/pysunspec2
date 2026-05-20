import pytest
import ssl
import time
import threading
from pymodbus.server import StartTlsServer
from pymodbus.datastore import (
    ModbusSlaveContext,
    ModbusServerContext,
    ModbusSequentialDataBlock,
)
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

    block = ModbusSequentialDataBlock(0, [0] * 100)
    store = ModbusSlaveContext(di=block, co=block, hr=block, ir=block)
    context = ModbusServerContext(slaves=store, single=True)

    StartTlsServer(context, address=(IPADDR, IPPORT), sslctx=sslctx)


@pytest.fixture(scope="module", autouse=True)
def tls_modbus_server():
    server_thread = threading.Thread(target=run_tls_modbus_server, daemon=True)
    server_thread.start()
    time.sleep(2)  # Give the server time to start
    yield


@pytest.mark.parametrize(
    "cafile, certfile, keyfile, ipaddr, ipport", [(CAFILE_CLIENT, CLIENT_CERTFILE, CLIENT_KEYFILE, IPADDR, IPPORT)]
)
def test_tls_connection(cafile, certfile, keyfile, ipaddr, ipport):
    """
    Test TLS connection for SunSpecModbusClientDeviceTCP.
    The TLS-enabled Modbus TCP server is started automatically.
    """
    device = SunSpecModbusClientDeviceTCP(
        slave_id=1,
        ipaddr=ipaddr,
        ipport=ipport,
        tls=True,
        cafile=CAFILE_SERVER,
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
