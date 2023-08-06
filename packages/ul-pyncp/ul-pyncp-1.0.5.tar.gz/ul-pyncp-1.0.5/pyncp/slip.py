import re
class SlipException(Exception):
    def __str__(self):
        return 'SLIP decode error'

def encode(buf: bytes) -> bytes:
    """Кодирует данные в SLIP

    Args:
        buf (bytes): данные

    Returns:
        bytes: закодированный SLIP пакет
    """
    return b'\xC0' + buf.replace(b'\xDB',b'\xDB\xDD').replace(b'\xC0', b'\xDB\xDC') + b'\xC0'

def decode(buf: bytes) -> bytes:
    """Декодирует данные из SLIP

    Args:
        buf (bytes): SLIP пакет

    Raises:
        SlipException: при неверном формате пакета

    Returns:
        bytes: декодированные данные
    """
    if buf[0] != 0xC0 or buf[-1] != 0xC0: raise SlipException()
    if re.search(b'\xDB[^\xDC\xDD]', buf) is not None: raise SlipException()
    return buf[1:-1].replace(b'\xDB\xDC', b'\xC0').replace(b'\xDB\xDD', b'\xDB')