from categories_app.models import Category
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Prefetch
from drf_spectacular.utils import extend_schema,OpenApiParameter

from .models import Product
from .serializers import (
    ProductSerializer,
    ProductWithShopPriceSerializer,
    ProductWithShopsSerializer,
)
from industries.models import ShopProduct


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @extend_schema(
        description="List all products",
        responses={200: ProductSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @extend_schema(
        description="Get details of a single product",
        responses={200: ProductSerializer},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=False, methods=["get"])
    def by_category(self, request):
        """
        Get products filtered by category.
        If category name is passed → return products in that category.
        If not passed → return all products grouped by category.
        """
        category_name = request.query_params.get("category")

        if category_name:
            products = Product.objects.filter(category__name=category_name)
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)

        # If no category name → return all products grouped by category
        categories = Category.objects.prefetch_related("products")
        data = []
        for category in categories:
            data.append({
                "category": category.name,
                "products": ProductSerializer(category.products.all(), many=True).data
            })
        return Response(data)
    
    @action(detail=False, methods=["get"])
    def by_shop(self, request):
        """
        Get products filtered by shop_name.
        If shop_name is passed → return products with price & availability.
        If not passed → return all products with all shops.
        """
        shop_name = request.query_params.get("shop_name")

        if shop_name:
            # Optimized fetch for one shop
            shop_products = ShopProduct.objects.select_related("product").filter(
                shop__name=shop_name, is_available=True
            )
            shop_product_map = {sp.product_id: sp for sp in shop_products}

            products = Product.objects.filter(id__in=shop_product_map.keys())
            serializer = ProductWithShopPriceSerializer(
                products, many=True, context={"shop_product_map": shop_product_map}
            )
            return Response(serializer.data)

        # If no shop_name → return all products with shop details
        products = Product.objects.prefetch_related(
            Prefetch(
                "shop_offerings",
                queryset=ShopProduct.objects.select_related("shop").filter(
                    is_available=True
                ),
            )
        )
        serializer = ProductWithShopsSerializer(products, many=True)
        return Response(serializer.data)


    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="q",
                description="Search products by name",
                required=True,
                type=str
            ),
        ],
        responses=ProductSerializer(many=True)
    )
    @action(detail=False, methods=["get"])
    def search(self, request):
        query = request.query_params.get("q")
        if not query:
            return Response({"detail": "Query parameter 'q' is required"}, status=400)

        products = Product.objects.filter(name__icontains=query)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
