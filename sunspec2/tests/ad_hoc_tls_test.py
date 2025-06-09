import os
from sunspec2.modbus.client import SunSpecModbusClientDeviceTCP

BASE_DIR = os.path.dirname(__file__)
CAFILE = os.path.join(BASE_DIR, "tls_data", "ca.crt")
CLIENT_CERTFILE = os.path.join(BASE_DIR, "tls_data", "client.crt")
CLIENT_KEYFILE = os.path.join(BASE_DIR, "tls_data", "client.key")
IPADDR = "localhost"
IPPORT = 8502

def test_tls_connection(
    ipaddr,
    ipport,
    cafile,
    certfile=None,
    keyfile=None,
    insecure_skip_tls_verify=False,
):
    """
    Ad-hoc TLS tester for an already running SunSpec Modbus TCP server.
    """
    device = SunSpecModbusClientDeviceTCP(
        slave_id=1,
        ipaddr=ipaddr,
        ipport=ipport,
        tls=True,
        cafile=cafile,
        certfile=certfile,
        keyfile=keyfile,
        insecure_skip_tls_verify=insecure_skip_tls_verify,
    )
    try:
        device.connect()
        print("TLS connection successful!")
    except Exception as e:
        print(f"TLS connection failed: {e}")

    device.scan()
    print("Device scan completed successfully.")

    if device.is_connected():
        device.disconnect()
        print("Device disconnected.")

if __name__ == "__main__":
    test_tls_connection(
        ipaddr=IPADDR,
        ipport=IPPORT,
        cafile=CAFILE,
        certfile=CLIENT_CERTFILE,
        keyfile=CLIENT_KEYFILE,
        insecure_skip_tls_verify=False,
    )