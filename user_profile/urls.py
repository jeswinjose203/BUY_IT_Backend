from django.urls import path
from .views import *

urlpatterns = [
    path('me/', UserProfileDetail.as_view(), name='user-profile'),
]
