# phone_auth/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import PhoneOTP

User = get_user_model()

class PhoneOTPRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)

class PhoneOTPVerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    otp = serializers.CharField(max_length=6)
    