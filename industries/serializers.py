from rest_framework import serializers
from .models import Shop, ShopProduct, ShopReview
from products_app.serializers import ProductSerializer
from django.db.models import Avg


class ShopProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  # Include product details

    class Meta:
        model = ShopProduct
        fields = ['id', 'product', 'price', 'is_available']


class ShopSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Shop
        fields = ['id', 'name', 'description', 'location', 'average_rating', 'review_count','image']

    def get_average_rating(self, obj):
        avg = obj.reviews.aggregate(avg=Avg("rating"))["avg"]
        return round(avg, 1) if avg else 0

    def get_review_count(self, obj):
        return obj.reviews.count()


class ShopWithProductsSerializer(serializers.ModelSerializer):
    shop_products = ShopProductSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Shop
        fields = [
            'id', 'name', 'description', 'location',
            'average_rating', 'review_count', 'shop_products','image'
        ]

    def get_average_rating(self, obj):
        avg = obj.reviews.aggregate(avg=Avg("rating"))["avg"]
        return round(avg, 1) if avg else 0

    def get_review_count(self, obj):
        return obj.reviews.count()


class ShopReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = ShopReview
        fields = ['id', 'shop', 'user_name', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'shop', 'user_name', 'created_at']


