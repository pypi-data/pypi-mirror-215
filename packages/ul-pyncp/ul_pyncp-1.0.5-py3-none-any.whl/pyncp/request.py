from .core import Ncp, NcpException, CMD_DATA

class NcpRequest:
    def __init__(self, mac):
        self.ncp = Ncp()
        self.ncp.mac = mac

    def data(self, data):
        self.ncp.cmd = CMD_DATA
        self.ncp.data = data
        return self.ncp.encode()