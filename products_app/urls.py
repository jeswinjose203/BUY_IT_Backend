from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    ProductViewSet,
)

urlpatterns = [
    # Regular product APIs
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),

    # Custom viewset actions
    path('products/by-shop/', ProductViewSet.as_view({'get': 'by_shop'}), name='product-by-shop'),
    path('products/by-category/', ProductViewSet.as_view({'get': 'by_category'}), name='product-by-category'),
    path('products/search/', ProductViewSet.as_view({'get': 'search'}), name='product-search'),
]

