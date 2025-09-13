import uuid
from django.db import models
from django.contrib.auth.models import User

from industries.models import ShopProduct





class Cart(models.Model):
    """Shopping cart linked to a user."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return sum(item.subtotal() for item in self.items.all())

    def clear_cart(self):
        self.items.all().delete()

    def __str__(self):
        return f"Cart of {self.user.username}"


class CartItem(models.Model):
    """Items inside a cart."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    shop_product = models.ForeignKey("industries.ShopProduct", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("cart", "shop_product")

    def subtotal(self):
        return self.quantity * self.shop_product.price

    def __str__(self):
        return f"{self.quantity} x {self.shop_product.product.name}"


class Order(models.Model):
    """User order created from checkout."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[("PENDING", "Pending"), ("PAID", "Paid"), ("SHIPPED", "Shipped"), ("DELIVERED", "Delivered")],
        default="PENDING",
    )

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class OrderItem(models.Model):
    """Individual items in an order."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    shop_product = models.ForeignKey("industries.ShopProduct", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # snapshot of product price at purchase time

    def subtotal(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.quantity} x {self.shop_product.product.name} at {self.shop_product.shop.name}"
