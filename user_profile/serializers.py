from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.openapi import OpenApiTypes
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    
    @extend_schema_field({
        'type': 'string',
        'format': 'binary',
        'description': 'Profile picture image file'
    })
    class CustomImageField(serializers.ImageField):
        pass
    
    profile_picture = CustomImageField(required=False, allow_null=True)

    class Meta:
        model = UserProfile
        fields = [
            'name', 
            'phone_number', 
            'address', 
            'default_delivery_address', 
            'preferred_payment_method', 
            'profile_picture'
        ]