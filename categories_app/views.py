from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Category
from .serializers import CategorySerializer
from drf_spectacular.utils import extend_schema

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @extend_schema(
        description="List all categories",
        responses={200: CategorySerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @extend_schema(
        description="Get details of a single category",
        responses={200: CategorySerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
