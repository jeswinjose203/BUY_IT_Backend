from django.urls import path
from .views import (
    CartView,
    AddToCartView,
    RemoveFromCartView,
    UpdateCartItemView,
    CartCountView,
    CheckoutView,
    OrderListView,
    OrderDetailView,
    ClearCartView,
)

urlpatterns = [
    # 🛒 Cart APIs
    path("cart/", CartView.as_view(), name="cart-detail"),  
    path("cart/add/", AddToCartView.as_view(), name="cart-add"),  
    path("cart/remove/<uuid:item_id>/", RemoveFromCartView.as_view(), name="cart-remove"),  
    path("cart/update/<uuid:item_id>/", UpdateCartItemView.as_view(), name="cart-update"),  
    path("cart/count/", CartCountView.as_view(), name="cart-count"),  
    path("cart/checkout/", CheckoutView.as_view(), name="cart-checkout"),  
    path("cart/clear/", ClearCartView.as_view(), name="cart-clear"),  
    # 📦 Order APIs
    path("orders/", OrderListView.as_view(), name="order-list"),  
    path("orders/<uuid:pk>/", OrderDetailView.as_view(), name="order-detail"),  
]
