from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from ipam_api.serializers import IPInfoSerializer, CalcRequestSerializer, TwoNetworksRequestSerializer
from ipam_api.ipcalc import calculate


_IPCALC_METHODS = ['GET', 'POST']
_IPCALC_INFO = {"message": "Use POST for action. OPTIONS for info."}


@api_view(_IPCALC_METHODS)
def calculate_ip(request: Request):
    """
    Calculating ip info
    """
    if request.method == 'POST':
        calc_request_serializer = CalcRequestSerializer(data=request.data)
        # Checking data validness
        if calc_request_serializer.is_valid(raise_exception=True):
            # Calculating
            calculated_data = calculate(calc_request_serializer.validated_data['ip'])
            ip_info_serializer = IPInfoSerializer(calculated_data)

            return Response(ip_info_serializer.data)

    return Response(_IPCALC_INFO)


@api_view(_IPCALC_METHODS)
def overlaps(request: Request):
    """
    True if this network is partly or wholly contained in other or other is wholly contained in this network.
    """
    if request.method == 'POST':
        serializer = TwoNetworksRequestSerializer(data=request.data)
        # Checking data validness
        if serializer.is_valid(raise_exception=True):
            # Turning networks to ipaddress objects
            this_net = serializer.validated_data['this_net']
            other_net = serializer.validated_data['other_net']
            # Check overlaps
            overlaps_comparison_result = this_net.overlaps(other_net)

            return Response({"result": overlaps_comparison_result})

    return Response(_IPCALC_INFO)

