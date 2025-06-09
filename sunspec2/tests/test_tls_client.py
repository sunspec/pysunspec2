import pytest
import ssl
import time
import threading
from pymodbus.server.sync import StartTlsServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from sunspec2.modbus.client import SunSpecModbusClientDeviceTCP
import os

BASE_DIR = os.path.dirname(__file__)
CAFILE = os.path.join(BASE_DIR, "tls_data", "ca.crt")
CERTFILE = os.path.join(BASE_DIR, "tls_data", "server.crt")
KEYFILE = os.path.join(BASE_DIR, "tls_data", "server.key")
CLIENT_CERTFILE = os.path.join(BASE_DIR, "tls_data", "client.crt")
CLIENT_KEYFILE = os.path.join(BASE_DIR, "tls_data", "client.key")
IPADDR = "localhost"
IPPORT = 8502

def run_tls_modbus_server():
    sslctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    sslctx.load_cert_chain(certfile=CERTFILE, keyfile=KEYFILE)
    sslctx.load_verify_locations(cafile=CAFILE)
    sslctx.verify_mode = ssl.CERT_REQUIRED

    store = ModbusSlaveContext()
    context = ModbusServerContext(slaves=store, single=True)

    StartTlsServer(
        context,
        address=(IPADDR, IPPORT),
        sslctx=sslctx,
    )

@pytest.fixture(scope="module", autouse=True)
def tls_modbus_server():
    server_thread = threading.Thread(target=run_tls_modbus_server, daemon=True)
    server_thread.start()
    time.sleep(2)  # Give the server time to start
    yield

@pytest.mark.parametrize(
    "cafile, certfile, keyfile, ipaddr, ipport", [(CAFILE, CLIENT_CERTFILE, CLIENT_KEYFILE, IPADDR, IPPORT)]
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