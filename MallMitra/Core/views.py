from django.shortcuts import render

import random
from datetime import timedelta

from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import OTPVerification
from .serializer import SendOTPSerializer


import random


from .service import send_sms_otp

class ConnectionCheckView(APIView):

    def get(self, request):
        return Response({
            "success": True,
            "message": "Connected successfully"
        })


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializer import SendOTPSerializer
from .service import send_sms_otp


class SendOTPView(APIView):

    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"success": False, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        mobile_number = serializer.validated_data["mobile_number"]
        channel = serializer.validated_data["channel"]

        if channel.lower() != "sms":
            return Response(
                {"success": False, "message": "Only SMS channel is supported."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        verification_id = send_sms_otp(mobile_number=mobile_number)

        if not verification_id:
            return Response(
                {"success": False, "message": "SMS could not be sent."},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        return Response(
            {
                "success": True,
                "message": "OTP sent successfully.",
                "mobile_number": mobile_number,
                "channel": channel,
            },
            status=status.HTTP_200_OK,
        )