from .views import PhoneOTPRequestView, PhoneOTPVerifyView
from django.urls import path
urlpatterns = [
    path('request-otp/', PhoneOTPRequestView.as_view(), name='request_otp'),
    path('verify-otp/', PhoneOTPVerifyView.as_view(), name='verify_otp'),
]