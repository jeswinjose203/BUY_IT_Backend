from django.db import models, transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import Cart, CartItem, ShopProduct, Order, OrderItem
from .serializers import (
    CartSerializer,
    CartItemSerializer,
    OrderSerializer,
    UpdateCartItemSerializer,
    RemoveFromCartSerializer,
    AddToCartSerializer,
)

from drf_spectacular.utils import extend_schema


# -----------------------------
# Helper function
# -----------------------------
def get_user_cart(user):
    """Return or create a cart for the given user."""
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


# -----------------------------
# CART VIEWS
# -----------------------------
class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_user_cart(self.request.user)


class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=AddToCartSerializer,   # 👈 request payload schema
        responses=CartSerializer       # 👈 response payload schema
    )
    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart = get_user_cart(request.user)
        shop_product_id = serializer.validated_data["shop_product_id"]
        quantity = serializer.validated_data.get("quantity", 1)

        shop_product = get_object_or_404(ShopProduct, id=shop_product_id)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            shop_product=shop_product,
            defaults={"quantity": quantity}
        )
        if not created:
            cart_item.quantity = models.F("quantity") + quantity
            cart_item.save(update_fields=["quantity"])
            cart_item.refresh_from_db()

        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)
    
# ---- Update Cart ----
# class UpdateCartView(APIView):
#     permission_classes = [IsAuthenticated]

#     @extend_schema(
#         request=UpdateCartSerializer,
#         responses=CartSerializer
#     )
#     def put(self, request):
#         serializer = UpdateCartSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         cart = get_user_cart(request.user)
#         cart_item = get_object_or_404(CartItem, id=serializer.validated_data["cart_item_id"], cart=cart)

#         cart_item.quantity = serializer.validated_data["quantity"]
#         cart_item.save(update_fields=["quantity"])

#         return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)


# ---- Remove from Cart ----
class RemoveFromCartView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=RemoveFromCartSerializer,
        responses=CartSerializer
    )
    def delete(self, request):
        serializer = RemoveFromCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart = get_user_cart(request.user)
        cart_item = get_object_or_404(CartItem, id=serializer.validated_data["cart_item_id"], cart=cart)

        cart_item.delete()

        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)
    
class ClearCartView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=None,                # no payload
        responses=CartSerializer
    )
    def delete(self, request):
        cart = get_user_cart(request.user)
        cart.clear_cart()  # method already exists in your Cart model
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)
# class AddToCartView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         cart = get_user_cart(request.user)
#         shop_product_id = request.data.get("shop_product_id")
#         quantity = int(request.data.get("quantity", 1))

#         shop_product = get_object_or_404(ShopProduct, id=shop_product_id)

#         cart_item, created = CartItem.objects.get_or_create(
#             cart=cart,
#             shop_product=shop_product,
#             defaults={"quantity": quantity}
#         )
#         if not created:
#             cart_item.quantity = models.F("quantity") + quantity
#             cart_item.save(update_fields=["quantity"])
#             cart_item.refresh_from_db()

#         return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)


class RemoveFromCartView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):  # DELETE method
        cart = get_user_cart(request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, id=item_id)
        cart_item.delete()

        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)



# class UpdateCartItemView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         cart = get_user_cart(request.user)
#         shop_product_id = request.data.get("shop_product_id")
#         quantity = int(request.data.get("quantity", 1))

#         cart_item = get_object_or_404(CartItem, cart=cart, shop_product_id=shop_product_id)

#         if quantity <= 0:
#             cart_item.delete()
#         else:
#             cart_item.quantity = quantity
#             cart_item.save()

#         return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)

# class UpdateCartItemView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, item_id):  # accept item_id
#         cart = get_user_cart(request.user)
#         quantity = int(request.data.get("quantity", 1))

#         cart_item = get_object_or_404(CartItem, cart=cart, id=item_id)

#         if quantity <= 0:
#             cart_item.delete()
#         else:
#             cart_item.quantity = quantity
#             cart_item.save(update_fields=["quantity"])

#         return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)

# class UpdateCartItemView(APIView):
#     permission_classes = [IsAuthenticated]

#     def put(self, request, item_id):  # use PUT for update
#         cart = get_user_cart(request.user)
#         cart_item = get_object_or_404(CartItem, cart=cart, id=item_id)

#         quantity = request.data.get("quantity")

#         if quantity is not None:
#             quantity = int(quantity)
#             if quantity <= 0:
#                 cart_item.delete()
#             else:
#                 cart_item.quantity = quantity
#                 cart_item.save(update_fields=["quantity"])

#         return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)
class UpdateCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=UpdateCartItemSerializer,
        responses=CartSerializer
    )
    def put(self, request, item_id):
        cart = get_user_cart(request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, id=item_id)

        serializer = UpdateCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        quantity = serializer.validated_data["quantity"]

        if quantity <= 0:
            cart_item.delete()
        else:
            cart_item.quantity = quantity
            cart_item.save(update_fields=["quantity"])

        return Response(CartSerializer(cart).data)

class ClearCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = get_user_cart(request.user)
        cart.clear_cart()
        return Response({"message": "Cart cleared successfully"}, status=status.HTTP_200_OK)


class CartCountView(APIView):
    """Get total count of items in cart (for navbar badge)."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = get_user_cart(request.user)
        count = sum(item.quantity for item in cart.items.all())
        return Response({"count": count}, status=status.HTTP_200_OK)


# -----------------------------
# CHECKOUT / ORDER VIEWS
# -----------------------------
class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        cart = get_user_cart(request.user)

        if not cart.items.exists():
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(
            user=request.user,
            total_price=cart.total_price()
        )

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                shop_product=item.shop_product,
                quantity=item.quantity,
                price=item.shop_product.price
            )

        cart.clear_cart()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class OrderListView(generics.ListAPIView):
    """List all orders of the current user."""
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by("-created_at")


class OrderDetailView(generics.RetrieveAPIView):
    """Retrieve details of a specific order."""
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
