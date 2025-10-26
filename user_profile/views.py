from drf_spectacular.utils import extend_schema, OpenApiExample
from drf_spectacular.openapi import OpenApiTypes
from rest_framework import generics, permissions, parsers
from .models import UserProfile
from .serializers import UserProfileSerializer

class UserProfileDetail(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]

    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile

    @extend_schema(
        operation_id='user_profile_partial_update',
        request={
            'multipart/form-data': UserProfileSerializer,
            'application/json': UserProfileSerializer,
        },
        responses={200: UserProfileSerializer},
        description='Update user profile. Use multipart/form-data for file uploads.',
        examples=[
            OpenApiExample(
                'Multipart form data example',
                value={
                    'name': 'John Doe',
                    'phone_number': '+1234567890',
                    'profile_picture': 'binary file data'
                },
                request_only=True,
                media_type='multipart/form-data'
            )
        ]
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        operation_id='user_profile_update',
        request={
            'multipart/form-data': UserProfileSerializer,
            'application/json': UserProfileSerializer,
        },
        responses={200: UserProfileSerializer},
        description='Update user profile. Use multipart/form-data for file uploads.',
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)