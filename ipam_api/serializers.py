from rest_framework import serializers
from ipam_api.ipcalc import IPString


class IPInfoSeializer(serializers.Serializer):
    version = serializers.ChoiceField(choices=[4, 6])
    is_multicast = serializers.BooleanField()
    is_private = serializers.BooleanField()
    is_unspecified = serializers.BooleanField()
    is_reserved = serializers.BooleanField()
    is_loopback = serializers.BooleanField()
    is_link_local = serializers.BooleanField()
    network_address = serializers.CharField()
    broadcast_address = serializers.CharField()
    hostmask = serializers.CharField()
    netmask = serializers.CharField()
    num_addresses = serializers.IntegerField()
    prefixlen = serializers.IntegerField()
    hostmin = serializers.CharField()
    hostmax = serializers.CharField()


class IPStringSerializer(serializers.Serializer):
    ip_str = serializers.IPAddressField(protocol='IPv4')
    prefix = serializers.IntegerField(min_value=0, max_value=32, default=32)
    verbose = serializers.BooleanField(default=False)

    def create(self, validated_data):
        return IPString(**validated_data)

