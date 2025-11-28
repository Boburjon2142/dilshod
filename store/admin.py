from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "sku",
        "purchase_price",
        "sale_price",
        "quantity",
        "created_at",
    )
    search_fields = ("title", "author", "sku")
