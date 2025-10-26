from django.shortcuts import render

# Create your views here.
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PhoneOTPRequestSerializer, PhoneOTPVerifySerializer
from .models import PhoneOTP
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()


def send_otp(phone, otp):
    print(f"OTP for {phone}: {otp}")  # replace with SMS API in production

from drf_spectacular.utils import extend_schema,OpenApiResponse

class PhoneOTPRequestView(APIView):
    @extend_schema(
        request=PhoneOTPRequestSerializer,
        responses={200: OpenApiResponse(description="OTP sent")}
    )
    def post(self, request):
        serializer = PhoneOTPRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone_number']

        otp_obj, _ = PhoneOTP.objects.get_or_create(phone_number=phone)
        otp_obj.generate_otp()
        send_otp(phone, otp_obj.otp)
        return Response({"detail": "OTP sent"}, status=status.HTTP_200_OK)


class PhoneOTPVerifyView(APIView):
    @extend_schema(
        request=PhoneOTPVerifySerializer,
        responses={200: OpenApiResponse(description="Token returned")}
    )
    def post(self, request):
        serializer = PhoneOTPVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone_number']
        otp = serializer.validated_data['otp']

        try:
            otp_obj = PhoneOTP.objects.get(phone_number=phone)
            if otp_obj.otp != otp:
                return Response({"detail": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
        except PhoneOTP.DoesNotExist:
            return Response({"detail": "OTP not requested"}, status=status.HTTP_400_BAD_REQUEST)

        # Login or create user
        user, _ = User.objects.get_or_create(username=phone)
        token, _ = Token.objects.get_or_create(user=user)

        return Response({"token": token.key}, status=status.HTTP_200_OK)