from rest_framework import serializers
from ipaddress import AddressValueError, NetmaskValueError
from ipam_api.ipcalc import check_network_versions_equivalence, ip_validate, ip_validate_and_return


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


class TwoNetworksRequestSerializer(serializers.Serializer):
    this_net = serializers.CharField()
    other_net = serializers.CharField()

    def to_internal_value(self, data):
        """
        Converts networks to ipaddress ip_network objects
        """
        errors = dict()
        validated_data = dict()

        # Checking first network
        try:
            validated_this_net = validate_and_return_network(data['this_net'])
        except serializers.ValidationError as exc:
            errors['this_net'] = exc
        else:
            validated_data['this_net'] = validated_this_net
        # Checking second net
        try:
            validated_other_net = validate_and_return_network(data['other_net'])
        except serializers.ValidationError as exc:
            errors['other_net'] = exc
        else:
            validated_data['other_net'] = validated_other_net

        # Checking version equivalence
        if not errors:
            if validated_this_net.version != validated_other_net.version:
                errors['non_field_errors'] = 'Networks must be the same IP version'
        if errors:
            raise serializers.ValidationError(errors)
        else:
            return validated_data


