class MockSocket(object):
    def __init__(self):
        self.connected = False
        self.timeout = 0
        self.ipaddr = None
        self.ipport = None
        self.buffer = []

        self.request = []

    def settimeout(self, timeout):
        self.timeout = timeout

    def connect(self, ipaddrAndipportTup):
        self.connected = True
        self.ipaddr = ipaddrAndipportTup[0]
        self.ipport = ipaddrAndipportTup[1]

    def close(self):
        self.connected = False

    def recv(self, size):
        return self.buffer.pop(0)

    def sendall(self, data):
        self.request.append(data)

    def _set_buffer(self, resp_list):
        for bs in resp_list:
            self.buffer.append(bs)

    def clear_buffer(self):
        self.buffer = []


def mock_socket(AF_INET, SOCK_STREAM):
    return MockSocket()
