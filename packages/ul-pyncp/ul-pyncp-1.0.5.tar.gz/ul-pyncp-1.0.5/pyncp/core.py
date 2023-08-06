BROADCAST_ADDRESS = 0
BROADCAST_ADDRESS_SILENT = 0xFFFFFFFF

NCP_PROTOCOL_ID = 6

NCP_CRC_POLYNOM = 0x8005

CMD_DATA = 6
CMD_ERROR = 7

class NcpException(Exception):
    def __init__(self, text):
        self.text = text
    def __str__(self):
        return self.text

class NcpErrorException(NcpException):
    errors = {
        1: ('ERR_GENERAL', 'Общая ошибка'),
        2: ('ERR_PARAMS', 'Ошибка параметров'),
        3: ('ERR_UNSUPPORTED', 'Неизвестный код'),
        4: ('ERR_WRITE', 'Ошибка записи'),
        5: ('ERR_OUTOFMEMORY', 'Недостаточно памяти'),
        6: ('ERR_WRONGADDR', 'Неверный адрес'),
        7: ('ERR_WRONGDATA', 'Некоректные данные в команде'),
        8: ('ERR_BUSY', 'Устройство занято'),
        9: ('ERR_CONNECT', 'Нет связи')         
    }
    def __init__(self, code, data = ''):
        self.code = code
        self.data = data

    def __str__(self):
        descr = NcpErrorException.errors.get(self.code, ('ERR_{}'.format(self.code), 'Ошибка {}'.format(self.code)))
        return  descr[0] + ': ' + descr[1]

def CRC(buf: bytes):
    crc = 0
    for b in buf:
        crc ^= b << 8
        for _ in range(8):
            if crc & 0x8000: 
                crc = (crc << 1) ^ NCP_CRC_POLYNOM
            else:
                crc = crc << 1
            crc &= 0xFFFF
    return crc

class Ncp:
    def __init__(self):
        pass

    def decode(self, buf: bytes):
        if buf[0] != NCP_PROTOCOL_ID:
            raise NcpException('Wrong NCP protocol id')
        if len(buf) < 9:
            raise NcpException('Packet too small')
        if CRC(buf[:-2]) != int.from_bytes(buf[-2:], byteorder = 'big', signed = False):
            raise NcpException('Wrong CRC')
        if buf[5] & 0x7F != 0:
            raise NcpException('Unknown flags')
        self.mac = int.from_bytes(buf[1:5], byteorder = 'little', signed = False)
        self.ans = buf[5] == 0x80
        self.cmd = buf[6]
        self.data = buf[7:-2]

    def encode(self):
        if type(self.mac) is not int or self.mac < 0 or self.mac > 0xFFFFFFFF:
            raise NcpException('Invalid MAC address')
        if type(self.cmd) is not int or self.cmd < 0 or self.cmd > 0xFF: 
            raise NcpException('Invalid command')

        res = bytes([NCP_PROTOCOL_ID]) + \
            self.mac.to_bytes(4, byteorder = 'little', signed = False) + \
            bytes([0, self.cmd]) + \
            self.data
        res += CRC(res).to_bytes(2, byteorder = 'big', signed = False)
        return res



    def check_error(self):
        if self.cmd == CMD_ERROR:
            raise NcpErrorException(self.data[0], self.data[1:])
