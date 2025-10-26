from django.contrib import admin
from .models import Shop, ShopProduct
from products_app.models import Product

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ("name", "location")

@admin.register(ShopProduct)
class ShopProductAdmin(admin.ModelAdmin):
    list_display = ("shop", "product", "price", "is_available")
