from django.db import models
from django.conf import settings
from industries.models import Shop
from products_app.models import Product

User = settings.AUTH_USER_MODEL

class WishlistItem(models.Model):
    WISHLIST_TYPE_CHOICES = [
        ('product', 'Product'),
        ('shop', 'Shop'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist_items')
    wishlist_type = models.CharField(max_length=20, choices=WISHLIST_TYPE_CHOICES)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, related_name='wishlisted_by')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True, blank=True, related_name='wishlisted_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'product'],
                name='unique_user_product_wishlist',
                condition=models.Q(product__isnull=False)
            ),
            models.UniqueConstraint(
                fields=['user', 'shop'],
                name='unique_user_shop_wishlist',
                condition=models.Q(shop__isnull=False)
            ),
        ]

    def __str__(self):
        return f"{self.user} - {self.wishlist_type}"
