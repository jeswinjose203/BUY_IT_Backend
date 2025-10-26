from django.urls import path
from .views import AddToWishlistView, RemoveFromWishlistView, WishlistListView

urlpatterns = [
    path('all-wishlist/', WishlistListView.as_view(), name='wishlist-list'),
    path('add-to-wishlist/', AddToWishlistView.as_view(), name='wishlist-add'),
    path('remove-from-wishlist/', RemoveFromWishlistView.as_view(), name='wishlist-remove'),
]
