from .core import Ncp, NcpException

class NcpAnswer:
    def __init__(self, data: bytes, mac: int = None, command: int = None):
        self.mac = mac
        self.command = command
        self.ncp = Ncp()

        if data is not None:            
            self.decode(data)

    def decode(self, data):
        self.ncp.decode(data)
        if self.mac is not None and self.mac != self.ncp.mac:
            raise NcpException('Wrong answer MAC address')
        self.mac = self.ncp.mac

        self.ncp.check_error()

        if self.command is not None and self.command != self.ncp.cmd:
            raise NcpException('Wrong answer command')


    def data(self):
        return self.ncp.data