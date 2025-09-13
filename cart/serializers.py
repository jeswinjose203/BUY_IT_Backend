from rest_framework import serializers
from .models import Cart, CartItem, ShopProduct, Order, OrderItem


class ShopProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopProduct
        fields = ["id", "price"]

class AddToCartSerializer(serializers.Serializer):
    shop_product_id = serializers.CharField(required=True)  # accepts both int and uuid
    quantity = serializers.IntegerField(min_value=1, default=1)

    def validate_shop_product_id(self, value):
        # Try UUID first
        from uuid import UUID
        try:
            value = UUID(value)
        except (ValueError, TypeError):
            # fallback to integer
            try:
                value = int(value)
            except ValueError:
                raise serializers.ValidationError("shop_product_id must be int or UUID")

        if not ShopProduct.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid shop_product_id")

        return value

class UpdateCartItemSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=0, required=True)

class RemoveFromCartSerializer(serializers.Serializer):
    cart_item_id = serializers.UUIDField()


class CartItemSerializer(serializers.ModelSerializer):
    shop_product = ShopProductSerializer()
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["id", "shop_product", "quantity", "subtotal"]

    def get_subtotal(self, obj):
        return obj.subtotal()


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "items", "total_price"]

    def get_total_price(self, obj):
        return obj.total_price()


class OrderItemSerializer(serializers.ModelSerializer):
    shop_product = ShopProductSerializer()
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ["id", "shop_product", "quantity", "price", "subtotal"]

    def get_subtotal(self, obj):
        return obj.subtotal()


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "total_price", "status", "created_at", "items"]
