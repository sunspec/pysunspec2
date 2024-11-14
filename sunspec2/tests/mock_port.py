class MockPort(object):
    PARITY_NONE = 'N'
    PARITY_EVEN = 'E'

    def __init__(self, port, baudrate, bytesize, parity, stopbits, xonxoff, timeout):
        self.connected = True
        self.port = port
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.xonxoff = xonxoff
        self.timeout = timeout

        self.buffer = []
        self.request = []

    def open(self):
        pass

    def close(self):
        self.connected = False

    def read(self, count):
        if len(self.buffer) == 0:
            return b''
        print(f"MockPort.read: count={count}. Message: {self.buffer[0]}")
        return self.buffer.pop(0)  # get the first element

    def write(self, data):
        self.request.append(data)

    def flushInput(self):
        pass

    def _set_buffer(self, resp_list):
        for bs in resp_list:
            self.buffer.append(bs)

    def clear_buffer(self):
        self.buffer = []


def mock_port(port, baudrate, bytesize, parity, stopbits, xonxoff, timeout):
    return MockPort(port, baudrate, bytesize, parity, stopbits, xonxoff, timeout)
