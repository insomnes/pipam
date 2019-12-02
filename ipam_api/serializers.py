from rest_framework import serializers
from rest_framework.settings import DEFAULTS
from ipaddress import AddressValueError, NetmaskValueError
from ipam_api.ipcalc import check_network_versions_equivalence, ip_validate, ip_validate_and_return


_DIFFERENT_VERSIONS_ERROR = "Networks must be the same IP version"
_REQUIRED_ERROR = "This field is required."


def validate_ip(ip):
    try:
        ip_validate(ip)
    except AddressValueError as exc:
        raise serializers.ValidationError('Address error: {}'.format(exc))
    except NetmaskValueError as exc:
        raise serializers.ValidationError('Netmask error: {}'.format(exc))


def validate_and_return_network(net):
    try:
        return ip_validate_and_return(net)
    except AddressValueError as exc:
        raise serializers.ValidationError('Address error: {}'.format(exc))
    except NetmaskValueError as exc:
        raise serializers.ValidationError('Netmask error: {}'.format(exc))


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
        errors = dict()
        validated_data = dict()

        # Checking that IP field is in request data
        if 'ip' not in data:
            errors['ip'] = [_REQUIRED_ERROR]
            raise serializers.ValidationError(errors)

        # Checking ip
        try:
            validated_ip = validate_and_return_network(data['ip'])
        except serializers.ValidationError as exc:
            errors['ip'] = exc.detail
        else:
            validated_data['ip'] = validated_ip

        if errors:
            raise serializers.ValidationError(errors)
        else:
            return validated_data


class TwoNetsSerializer(serializers.Serializer):
    def to_internal_value(self, data):
        """
        Converts networks to ipaddress ip_network objects
        """
        errors = dict()
        validated_data = dict()

        # Checking that network fields are in request data
        if 'first_net' not in data:
            errors['first_net'] = [_REQUIRED_ERROR]
        if 'second_net' not in data:
            errors['second_net'] = [_REQUIRED_ERROR]
        if errors:
            raise serializers.ValidationError(errors)

        # Checking first network
        try:
            validated_firs_net = validate_and_return_network(data['first_net'])
        except serializers.ValidationError as exc:
            errors['first_net'] = exc.detail
        else:
            validated_data['first_net'] = validated_firs_net
        # Checking second net
        try:
            validated_second_net = validate_and_return_network(data['second_net'])
        except serializers.ValidationError as exc:
            errors['second_net'] = exc.detail
        else:
            validated_data['second_net'] = validated_second_net

        # Checking version equivalence
        if not errors:
            if validated_firs_net.version != validated_second_net.version:
                errors[DEFAULTS['NON_FIELD_ERRORS_KEY']] = _DIFFERENT_VERSIONS_ERROR
        if errors:
            raise serializers.ValidationError(errors)
        else:
            return validated_data


