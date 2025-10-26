# from django.db import models
# from categories_app.models import Category

# class Product(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField(blank=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
#     shop_name = models.CharField(max_length=100)  # optional, or link to Shop model

#     def __str__(self):
#         return self.name

from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        "categories_app.Category",  # ✅ use app_label.ModelName (string reference)
        on_delete=models.CASCADE,
        related_name="products"
    )
    image = models.ImageField(upload_to="product_images/", blank=True, null=True)  # 🆕 new field


    def __str__(self):
        return self.name