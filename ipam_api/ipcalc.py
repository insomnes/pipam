"""
IP calculator
"""
from ipaddress import IPv4Network


class IPString:
    def __init__(self, ip_str, prefix=32, verbose=False):
        self.ip_str = ip_str
        self.prefix = prefix
        self.verbose = verbose


class CustomIPv4Network(IPv4Network):
    """
    Class with custom IP info not provided explicitly by IPv4Network
    """

    def __init__(self, *args, **kwargs):
        super(CustomIPv4Network, self).__init__(*args, **kwargs)
        hosts = tuple(self.hosts())
        self.hostmin = hosts[0]
        self.hostmax = hosts[-1]


def calculate(ip: IPString) -> IPv4Network:
    address = ip.ip_str + '/' + str(ip.prefix)
    return CustomIPv4Network(address, strict=False)


