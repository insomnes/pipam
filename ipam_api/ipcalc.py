"""
IP calculator
"""
from ipaddress import IPv4Network, IPv6Network, ip_network


_MAX_IPV4_PREFIX_LEN = 32
_MAX_IPV6_PREFIX_LEN = 128


class CustomIPv4Network(IPv4Network):
    """
    Class with custom IP info not provided explicitly by IPv4Network
    """
    def __init__(self, address, strict=False):
        super().__init__(address, strict)
        if self.prefixlen < _MAX_IPV4_PREFIX_LEN - 1:
            self.hostmin = self.network_address + 1
            self.hostmax = self.broadcast_address - 1
        else:
            self.hostmin = self.network_address
            self.hostmax = self.broadcast_address

        self.wildcard = self.hostmask


class CustomIPv6Network(IPv6Network):
    """
    Class with custom IP info not provided explicitly by IPv6Network
    """
    def __init__(self, address, strict=False):
        super().__init__(address, strict)
        if self.prefixlen < _MAX_IPV6_PREFIX_LEN - 1:
            self.hostmin = self.network_address + 1
            self.hostmax = self.broadcast_address - 1
        else:
            self.hostmin = self.network_address
            self.hostmax = self.broadcast_address

        self.wildcard = self.hostmask


def calculate_net(ip):
    if is_ipv6(ip):
        return CustomIPv6Network(ip, strict=False)
    else:
        return CustomIPv4Network(ip, strict=False)


def is_ipv6(ip):
    """
    Monkey IPv6 check.
    """
    if ':' in ip:
        return True
    else:
        return False
