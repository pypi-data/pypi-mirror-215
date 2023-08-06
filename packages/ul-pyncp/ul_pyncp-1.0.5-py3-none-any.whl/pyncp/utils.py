from .core import NcpErrorException, BROADCAST_ADDRESS, BROADCAST_ADDRESS_SILENT, CMD_DATA
from .answer import NcpAnswer
from .request import NcpRequest

from . import slip as SLIP

def decode_data(data: bytes, slip: bool = None) -> (int, bytes):
    """Кодирует данные в NCP data

    Args:
        data (bytes): данные

    Returns:
        int, bytes: адрес, закодированный пакет
    """
    if slip is None:
        slip = data[0] == 0xC0
        
    if slip: data = SLIP.decode(data)
    ncp = NcpAnswer(data, command = CMD_DATA)
    return ncp.mac, ncp.data()

def encode_data(data, mac: int = BROADCAST_ADDRESS, slip: bool = False):
    ncp = NcpRequest(mac)
    packet = ncp.data(data)
    if slip: 
        packet = SLIP.encode(packet)
    return packet