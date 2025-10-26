from rest_framework import serializers
from .models import WishlistItem
from industries.serializers import ProductSerializer, ShopSerializer  # import your existing ones


class WishlistItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    shop = ShopSerializer(read_only=True)

    class Meta:
        model = WishlistItem
        fields = ['id', 'wishlist_type', 'product', 'shop', 'added_at']
