from rest_framework import serializers
from ipaddress import AddressValueError, NetmaskValueError
from ipam_api.ipcalc import ip_validate, calculate


def validate_ip(ip):
    try:
        ip_validate(ip)
    except AddressValueError as exc:
        raise serializers.ValidationError('Address error: {}'.format(exc))
    except NetmaskValueError as exc:
        raise serializers.ValidationError('Netmask error: {}'.format(exc))


class IPInfoSerializer(serializers.Serializer):
    version = serializers.ChoiceField(choices=[4, 6])
    is_multicast = serializers.BooleanField()
    is_private = serializers.BooleanField()
    is_unspecified = serializers.BooleanField()
    is_reserved = serializers.BooleanField()
    is_loopback = serializers.BooleanField()
    is_link_local = serializers.BooleanField()
    is_site_local = serializers.BooleanField(required=False)
    network_address = serializers.CharField()
    broadcast_address = serializers.CharField()
    compressed = serializers.CharField()
    exploded = serializers.CharField()
    wildcard = serializers.CharField()
    netmask = serializers.CharField()
    num_addresses = serializers.IntegerField()
    prefixlen = serializers.IntegerField()
    hostmin = serializers.CharField()
    hostmax = serializers.CharField()


class CalcRequestSerializer(serializers.Serializer):
    ip = serializers.CharField(validators=[validate_ip])

    def save(self, **kwargs):
        ip = self.validated_data['ip']
        return calculate(ip)


