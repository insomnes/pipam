from rest_framework import serializers
from rest_framework.settings import DEFAULTS
from ipaddress import AddressValueError, NetmaskValueError
from ipam_api.ipcalc import calculate_net


_DIFFERENT_VERSIONS_ERROR = "Networks must be the same IP version"
_REQUIRED_ERROR = "This field is required."
_IP_FIELD_NAME = 'ip'
_FIRST_NET_FIELD_NAME = 'first_net'
_SECOND_NET_FIELD_NAME = 'second_net'


def check_fields_presence_for_serializer(data, *args):
    """
    Checking presence of field names (*args) in data
    """
    errors = dict()
    for field_name in args:
        if field_name not in data:
            errors[field_name] = [_REQUIRED_ERROR]
    if errors:
        raise serializers.ValidationError(errors)
    return None


def validate_and_return_networks_for_serializer(data, *args):
    errors = dict()
    validated_data = dict()

    for net in args:
        try:
            validated_net = calculate_net(data[net])
        except AddressValueError as exc:
            errors[net] = ['Address error: {}'.format(exc)]
        except NetmaskValueError as exc:
            errors[net] = ['Netmask error: {}'.format(exc)]
        else:
            validated_data[net] = validated_net

    if errors:
        raise serializers.ValidationError(errors)

    return validated_data


class TestSerializer(serializers.Serializer):
    ip = serializers.IPAddressField()


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


class NetSerializer(serializers.Serializer):
    def to_internal_value(self, data):
        """
        Converts network to ipaddress ip_network object
        """
        # Checking that IP field is in request data
        check_fields_presence_for_serializer(data, _IP_FIELD_NAME)

        validated_data = validate_and_return_networks_for_serializer(data, _IP_FIELD_NAME)

        return validated_data


class TwoNetsSerializer(serializers.Serializer):
    def to_internal_value(self, data):
        """
        Converts networks to ipaddress ip_network objects
        """
        fields = [_FIRST_NET_FIELD_NAME, _SECOND_NET_FIELD_NAME]
        errors = dict()

        # Checking that network fields are in request data
        check_fields_presence_for_serializer(data, *fields)

        # Checking first network
        validated_data = validate_and_return_networks_for_serializer(data, *fields)

        # Checking version equivalence
        if validated_data[_FIRST_NET_FIELD_NAME].version != validated_data[_SECOND_NET_FIELD_NAME].version:
            errors[DEFAULTS['NON_FIELD_ERRORS_KEY']] = [_DIFFERENT_VERSIONS_ERROR]
        if errors:
            raise serializers.ValidationError(errors)

        return validated_data
