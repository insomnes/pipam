from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ipam_api.serializers import IPInfoSeializer, IPStringSerializer
from ipam_api.ipcalc import IPString, calculate

IPCALC_INFO = {"message": "Use POST for calculation. OPTIONS for info."}


class IPCalc(APIView):
    """
    Ye olde good IP calculator.
    Send POST with json { "ip_str": "%IP_STRING%", "prefix": %PREFIX% }
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
        ip_str_serializer = IPStringSerializer(data=request.data)
        # Checking data validness
        if ip_str_serializer.is_valid():
            # Creating ip string object
            ip_str = ip_str_serializer.save()
            # Calculating
            calculated_data = calculate(ip_str)
            # Serializing calculated data
            ip_info_serializer = IPInfoSeializer(calculated_data)
            return Response(ip_info_serializer.data)

        # Return error if request is bad
        return Response(ip_str_serializer.errors, status.HTTP_400_BAD_REQUEST)
