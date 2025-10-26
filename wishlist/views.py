from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import WishlistItem
from .serializers import WishlistItemSerializer
from industries.models import Shop
from products_app.models import Product


class WishlistListView(generics.ListAPIView):
    serializer_class = WishlistItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WishlistItem.objects.filter(user=self.request.user).order_by('-added_at')


class AddToWishlistView(generics.CreateAPIView):
    serializer_class = WishlistItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        wishlist_type = request.data.get("wishlist_type")
        product_id = request.data.get("product_id")
        shop_id = request.data.get("shop_id")

        # Validate wishlist_type
        if wishlist_type not in ["product", "shop"]:
            return Response(
                {"error": 'Invalid wishlist_type. Must be "product" or "shop".'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Product wishlist
        if wishlist_type == "product":
            if not product_id:
                return Response(
                    {"error": "product_id is required when wishlist_type='product'"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                product = Product.objects.get(id=product_id)
                wishlist_item, created = WishlistItem.objects.get_or_create(
                    user=request.user,
                    product=product,
                    wishlist_type="product"
                )
                if not created:
                    return Response({"message": "Product already in wishlist."})
                return Response({"message": "Product added to wishlist successfully."})
            except Product.DoesNotExist:
                return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        # Shop wishlist
        elif wishlist_type == "shop":
            if not shop_id:
                return Response(
                    {"error": "shop_id is required when wishlist_type='shop'"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                shop = Shop.objects.get(id=shop_id)
                wishlist_item, created = WishlistItem.objects.get_or_create(
                    user=request.user,
                    shop=shop,
                    wishlist_type="shop"
                )
                if not created:
                    return Response({"message": "Shop already in wishlist."})
                return Response({"message": "Shop added to wishlist successfully."})
            except Shop.DoesNotExist:
                return Response({"error": "Shop not found."}, status=status.HTTP_404_NOT_FOUND)

class RemoveFromWishlistView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        wishlist_type = request.query_params.get("wishlist_type")
        product_id = request.query_params.get("product_id")
        shop_id = request.query_params.get("shop_id")
        # wishlist_type = request.data.get("wishlist_type") or request.query_params.get("wishlist_type")
        # product_id = request.data.get("product_id") or request.query_params.get("product_id")
        # shop_id = request.data.get("shop_id") or request.query_params.get("shop_id")

        if not wishlist_type:
            return Response({"error": "wishlist_type is required."}, status=400)

        if wishlist_type == "product":
            if not product_id:
                return Response({"error": "product_id is required."}, status=400)
            deleted, _ = WishlistItem.objects.filter(
                user=request.user, product_id=product_id, wishlist_type="product"
            ).delete()

        elif wishlist_type == "shop":
            if not shop_id:
                return Response({"error": "shop_id is required."}, status=400)
            deleted, _ = WishlistItem.objects.filter(
                user=request.user, shop_id=shop_id, wishlist_type="shop"
            ).delete()
        else:
            return Response({"error": 'Invalid wishlist_type.'}, status=400)

        if deleted:
            return Response({"message": "Removed from wishlist successfully."})
        else:
            return Response({"message": "Item not found in wishlist."}, status=404)


# class RemoveFromWishlistView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        wishlist_type = request.data.get("wishlist_type")
        product_id = request.data.get("product_id")
        shop_id = request.data.get("shop_id")

        if not wishlist_type:
            return Response(
                {"error": "wishlist_type is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if wishlist_type == "product":
            if not product_id:
                return Response(
                    {"error": "product_id is required when wishlist_type='product'"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            deleted, _ = WishlistItem.objects.filter(
                user=request.user,
                product_id=product_id,
                wishlist_type="product"
            ).delete()

        elif wishlist_type == "shop":
            if not shop_id:
                return Response(
                    {"error": "shop_id is required when wishlist_type='shop'"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            deleted, _ = WishlistItem.objects.filter(
                user=request.user,
                shop_id=shop_id,
                wishlist_type="shop"
            ).delete()

        else:
            return Response(
                {"error": 'Invalid wishlist_type. Must be "product" or "shop".'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if deleted:
            return Response({"message": "Removed from wishlist successfully."})
        else:
            return Response(
                {"message": "Item not found in wishlist."},
                status=status.HTTP_404_NOT_FOUND
            )