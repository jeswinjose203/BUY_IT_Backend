from rest_framework import serializers
from .models import Product
from categories_app.serializers import CategorySerializer
from industries.models import ShopProduct


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "description", "category","image"]


class ShopProductInfoSerializer(serializers.ModelSerializer):
    shop_name = serializers.CharField(source="shop.name", read_only=True)
    shop_location = serializers.CharField(source="shop.location", read_only=True)

    class Meta:
        model = ShopProduct
        fields = ["shop_name", "shop_location", "price", "is_available"]


class ProductWithShopsSerializer(serializers.ModelSerializer):
    available_at_shops = ShopProductInfoSerializer(
        source="shop_offerings", many=True, read_only=True
    )

    class Meta:
        model = Product
        fields = ["id", "name", "description", "category", "available_at_shops","image"]


class ProductWithShopPriceSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    price = serializers.SerializerMethodField()
    is_available = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "name", "description", "category", "price", "is_available","image"]

    def get_price(self, obj):
        shop_product_map = self.context.get("shop_product_map", {})
        sp = shop_product_map.get(obj.id)
        return sp.price if sp else None

    def get_is_available(self, obj):
        shop_product_map = self.context.get("shop_product_map", {})
        sp = shop_product_map.get(obj.id)
        return sp.is_available if sp else False
