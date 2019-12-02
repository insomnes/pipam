from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from ipam_api.serializers import IPInfoSerializer, NetSerializer, TwoNetsSerializer, TestSerializer


_IPCALC_METHODS = ['GET', 'POST']
_IPCALC_INFO = {"message": "Use POST for action. OPTIONS for info."}

_TEST_MESSAGE = {"message": "TEST MESSAGE"}


def create_ipcalc_operation_response(net1, net2, operation, result):
    response = Response(
        {
            "operation": "{} {} {}".format(net1, operation, net2),
            "result": result
         }
    )
    return response


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
            calculated_data = calc_request_serializer.validated_data['ip']
            ip_info_serializer = IPInfoSerializer(calculated_data)

            return Response(ip_info_serializer.data)

    return Response(_IPCALC_INFO)


@api_view(_IPCALC_METHODS)
def overlaps(request: Request):
    """
    True if this network is partly or wholly contained in other or other is wholly contained in this network.
    """
    if request.method == 'POST':
        serializer = TwoNetsSerializer(data=request.data)
        # Checking data validness
        if serializer.is_valid(raise_exception=True):
            # Turning networks to ipaddress objects
            first_net = serializer.validated_data['first_net']
            second_net = serializer.validated_data['second_net']
            # Check overlaps
            overlaps_comparison_result = first_net.overlaps(second_net)
            response = create_ipcalc_operation_response(first_net, second_net,
                                                        overlaps.__name__, overlaps_comparison_result)

            return response

    return Response(_IPCALC_INFO)

