from rest_framework.views import APIView
from rest_framework.response import Response
from ipam_api.serializers import IPInfoSerializer, CalcRequestSerializer

IPCALC_INFO = {"message": "Use POST for calculation. OPTIONS for info."}


class IPCalc(APIView):
    """
    Ye olde good IP calculator.
    Send POST with json { "ip": "%IPADDRESS%"}. Default prefix is 32.
    """
    def get(self, request, format=None):
        """
        Return info message.
        """
        return Response(IPCALC_INFO)

    def post(self, request, format=None):
        """
        Return calculated IP.
        """
        calc_request_serializer = CalcRequestSerializer(data=request.data)
        # Checking data validness
        if calc_request_serializer.is_valid(raise_exception=True):
            # Calculating
            calculated_data = calc_request_serializer.save()
            ip_info_serializer = IPInfoSerializer(calculated_data)

            return Response(ip_info_serializer.data)

