from rest_framework import generics, permissions,serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from geopy.distance import geodesic

from .models import Shop, ShopProduct, ShopReview
from categories_app.models import Category
from .serializers import (
    ShopSerializer,
    ShopWithProductsSerializer,
    ShopProductSerializer,
    ShopReviewSerializer,
)

from drf_spectacular.utils import extend_schema, OpenApiParameter

# -------------------------
# Shops
# -------------------------
class ShopListView(generics.ListAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopWithProductsSerializer


class ShopDetailView(generics.RetrieveAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopWithProductsSerializer


class ShopProductsView(generics.ListAPIView):
    serializer_class = ShopProductSerializer

    def get_queryset(self):
        return ShopProduct.objects.filter(shop_id=self.kwargs["pk"])


# -------------------------
# Shop Reviews (CRUD)
# -------------------------
from django.db import IntegrityError
from rest_framework import status

class ShopReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ShopReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return ShopReview.objects.filter(shop_id=self.kwargs["shop_id"])

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user, shop_id=self.kwargs["shop_id"])
        except IntegrityError:
            # If duplicate, return proper error
            raise serializers.ValidationError(
                {"detail": "You have already reviewed this shop."}
            )



class ShopReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShopReview.objects.all()
    serializer_class = ShopReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        review = self.get_object()
        if review.user != self.request.user:
            raise PermissionDenied("You can only edit your own review.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You can only delete your own review.")
        instance.delete()


# -------------------------
# Categories & Filtering
# -------------------------
class ShopCategoriesView(APIView):
    def get(self, request, pk):
        categories = Category.objects.filter(
            products__shop_offerings__shop_id=pk,
            products__shop_offerings__is_available=True
        ).distinct()

        return Response([{"id": c.id, "name": c.name} for c in categories])

class ShopsByCategoryView(APIView):

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="category_id",
                description="ID of the category to filter shops",
                required=True,
                type=int
            )
        ],
        responses=ShopWithProductsSerializer(many=True)
    )
    def get(self, request):
        category_id = request.query_params.get("category_id")
        if not category_id:
            return Response({"detail": "category_id is required"}, status=400)

        shops = Shop.objects.filter(
            shop_products__product__category_id=category_id,
            shop_products__is_available=True
        ).distinct()

        serializer = ShopWithProductsSerializer(shops, many=True)
        return Response(serializer.data)

# -------------------------
# Shop Availability
# -------------------------
class ShopAvailabilityView(APIView):
    def get(self, request, pk):
        try:
            shop = Shop.objects.get(pk=pk)
            return Response({
                "shop_id": shop.id,
                "shop_name": shop.name,
                "is_available": shop.is_open
            })
        except Shop.DoesNotExist:
            return Response({"detail": "Shop not found"}, status=404)


# -------------------------
# Nearby Shops
# -------------------------

class NearbyShopsView(APIView):

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="lat",
                description="Latitude of the user's location",
                required=True,
                type=float
            ),
            OpenApiParameter(
                name="lng",
                description="Longitude of the user's location",
                required=True,
                type=float
            ),
            OpenApiParameter(
                name="radius",
                description="Distance radius in km to search nearby shops (default 5 km)",
                required=False,
                type=float
            )
        ],
        responses={
            200: dict  # or you can define a serializer for id, name, distance_km
        }
    )
    def get(self, request):
        try:
            lat = float(request.query_params.get("lat"))
            lng = float(request.query_params.get("lng"))
            radius = float(request.query_params.get("radius", 5))
        except (TypeError, ValueError):
            return Response({"detail": "lat, lng, and radius are required"}, status=400)

        user_location = (lat, lng)
        nearby_shops = []

        for shop in Shop.objects.all():
            if shop.latitude and shop.longitude:
                distance = geodesic(user_location, (shop.latitude, shop.longitude)).km
                if distance <= radius:
                    nearby_shops.append((shop, round(distance, 2)))

        data = [{"id": s.id, "name": s.name, "distance_km": d} for s, d in nearby_shops]
        return Response(data)





from rest_framework import generics
from drf_spectacular.utils import extend_schema, OpenApiParameter

class ShopSearchView(generics.ListAPIView):
    """
    Search shops by name (partial match).
    Example: /api/shops/search/?q=milk
    """
    serializer_class = ShopWithProductsSerializer

    def get_queryset(self):
        query = self.request.query_params.get("q", "")
        if query:
            return Shop.objects.filter(name__icontains=query)
        return Shop.objects.none()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="q",
                description="Search query for shop name",
                required=True,
                type=str
            )
        ],
        responses=ShopWithProductsSerializer(many=True)
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
