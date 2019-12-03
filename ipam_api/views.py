from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from ipam_api.serializers import _NET_FIELD_NAME, _FIRST_NET_FIELD_NAME, _SECOND_NET_FIELD_NAME, \
    IPInfoSerializer, NetSerializer, TwoNetsSerializer, TestSerializer

_IPCALC_METHODS = ['GET', 'POST']
_IPCALC_INFO = {"message": "Use POST for action. OPTIONS for info."}

_TEST_MESSAGE = {"message": "TEST MESSAGE"}


def ipcalc_two_networks_operation_api_view(ipcalc_operation_function):
    """
    Decorator which is doing all similar serialization and validation operations
    """
    def ipcalc_operation_function_wrapper(request):
        if request.method == 'POST':
            serializer = TwoNetsSerializer(data=request.data)
            # Checking data validness
            if serializer.is_valid(raise_exception=True):
                # Turning networks to ipaddress objects
                first_net = serializer.validated_data[_FIRST_NET_FIELD_NAME]
                second_net = serializer.validated_data[_SECOND_NET_FIELD_NAME]
                # Decorated function is used here
                operation_result = ipcalc_operation_function(first_net, second_net)
                response = Response(
                    {
                        "operation": "{} {} {}".format(first_net, ipcalc_operation_function.__name__,
                                                       second_net).replace("_", " "),
                        "result": operation_result
                    }
                )

                return response

        # GET behaviour
        return Response(_IPCALC_INFO)

    return ipcalc_operation_function_wrapper


@api_view(_IPCALC_METHODS)
def test(request: Request):
    if request.method == 'POST':
        serializer = TestSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(_TEST_MESSAGE)

    return Response(_IPCALC_INFO)


@api_view(_IPCALC_METHODS)
def calculate_ip(request: Request):
    """
    Calculating ip info
    """
    if request.method == 'POST':
        calc_request_serializer = NetSerializer(data=request.data)
        # Checking data validness
        if calc_request_serializer.is_valid(raise_exception=True):
            # Return network object
            calculated_data = calc_request_serializer.validated_data[_NET_FIELD_NAME]
            ip_info_serializer = IPInfoSerializer(calculated_data)

            return Response(ip_info_serializer.data)

    return Response(_IPCALC_INFO)


@api_view(_IPCALC_METHODS)
@ipcalc_two_networks_operation_api_view
def equal_to(first_net, second_net):
    """
    True if first network is equal to second.
    """
    return first_net == second_net


@api_view(_IPCALC_METHODS)
@ipcalc_two_networks_operation_api_view
def greater_than(first_net, second_net):
    """
    True if first network address is greater than second network address.
    """
    return first_net > second_net


@api_view(_IPCALC_METHODS)
@ipcalc_two_networks_operation_api_view
def less_than(first_net, second_net):
    """
    TTrue if first network address is less than second network address.
    """
    return first_net < second_net


@api_view(_IPCALC_METHODS)
@ipcalc_two_networks_operation_api_view
def subnet_of(first_net, second_net):
    """
    True if first network is a subnet of second.
    """
    return first_net.subnet_of(second_net)


@api_view(_IPCALC_METHODS)
@ipcalc_two_networks_operation_api_view
def supernet_of(first_net, second_net):
    """
    True if first network is a supernet of second.
    """
    return first_net.supernet_of(second_net)


@api_view(_IPCALC_METHODS)
@ipcalc_two_networks_operation_api_view
def overlaps(first_net, second_net):
    """
    True if this network is partly or wholly contained in other or other is wholly contained in this network.
    """
    return first_net.overlaps(second_net)


