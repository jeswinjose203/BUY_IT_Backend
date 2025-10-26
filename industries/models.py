from django.db import models

from login.models import User

class Shop(models.Model):  # Industry -> renamed as Shop
    name = models.CharField(max_length=255)  # MILMA, PDDP, etc.
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    
    is_open = models.BooleanField(default=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)


    image = models.ImageField(upload_to="shops/", null=True, blank=True)    
    
    def __str__(self):
        return self.name


class ShopProduct(models.Model):  # Links Shop and Product
    shop = models.ForeignKey(
        "industries.Shop", 
        on_delete=models.CASCADE, 
        related_name="shop_products"
    )
    product = models.ForeignKey(
        "products_app.Product",  # ✅ keep as string reference
        on_delete=models.CASCADE, 
        related_name="shop_offerings"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ("shop", "product")

    def __str__(self):
        return f"{self.product.name} at {self.shop.name} - ₹{self.price}"


class ShopReview(models.Model):
    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="shop_reviews"
    )
    rating = models.PositiveIntegerField()  # 1–5
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("shop", "user")  # one review per user per shop
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.shop.name} - {self.user.username} ({self.rating}/5)"


