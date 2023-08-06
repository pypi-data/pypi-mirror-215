from numpy import uintc

def uint32_to_ipv4(num: uintc) -> str:
    """
    convert unsigned 32-bit int number to IPv4 format
    :param num: number to convert
    :return: IPv4 address
    """
    return '{}.{}.{}.{}'.format(
        (num & 0xff000000) >> 24,
        (num & 0x00ff0000) >> 16,
        (num & 0x0000ff00) >> 8,
        (num & 0x000000ff) >> 0
    )
