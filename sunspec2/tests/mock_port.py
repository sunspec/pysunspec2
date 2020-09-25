class MockPort(object):
    PARITY_NONE = 'N'
    PARITY_EVEN = 'E'

    def __init__(self, port, baudrate, bytesize, parity, stopbits, xonxoff, timeout, writeTimeout):
        self.connected = True
        self.port = port
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.xonxoff = xonxoff
        self.timeout = timeout
        self.writeTimeout = writeTimeout

        self.buffer = []
        self.request = []

    def open(self):
        pass

    def close(self):
        self.connected = False

    def read(self, count):
        return self.buffer.pop(0)

    def write(self, data):
        self.request.append(data)

    def flushInput(self):
        pass

    def _set_buffer(self, resp_list):
        for bs in resp_list:
            self.buffer.append(bs)

    def clear_buffer(self):
        self.buffer = []


def mock_port(port, baudrate, bytesize, parity, stopbits, xonxoff, timeout, writeTimeout):
    return MockPort(port, baudrate, bytesize, parity, stopbits, xonxoff, timeout, writeTimeout)
