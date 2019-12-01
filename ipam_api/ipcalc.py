"""
IP calculator
"""
from ipaddress import IPv4Network, IPv6Network


class CustomIPv4Network(IPv4Network):
    """
    Class with custom IP info not provided explicitly by IPv4Network
    """
    def __init__(self, address, strict=False):
        super().__init__(address, strict)
        self.hostmin = self.network_address + 1 if self.prefixlen < 30 else self.network_address
        self.hostmax = self.broadcast_address - 1 if self.prefixlen < 30 else self.broadcast_address
        self.wildcard = self.hostmask


class CustomIPv6Network(IPv6Network):
    """
    Class with custom IP info not provided explicitly by IPv6Network
    """
    def __init__(self, address, strict=False):
        super().__init__(address, strict)
        self.hostmin = self.network_address + 1 if self.prefixlen < 126 else self.network_address
        self.hostmax = self.broadcast_address - 1 if self.prefixlen < 126 else self.broadcast_address
        self.wildcard = self.hostmask


def calculate(ip):
    """
    Calculating ip. This function depends on previous ip validation.
    """
    if is_ipv6(ip):
        return CustomIPv6Network(ip)
    else:
        return CustomIPv4Network(ip)


def ip_validate(ip):
    """
    Simple function. Use with except
    """
    if is_ipv6(ip):
        IPv6Network(ip, strict=False)
    else:
        IPv4Network(ip, strict=False)

    return None


def is_ipv6(ip):
    if ':' in ip:
        return True
    else:
        return False
