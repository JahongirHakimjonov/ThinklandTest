from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.shop.models.product import Product


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ["id", "title", "category", "price"]
    search_fields = ["title", "category__title", "description", "category__description"]
    list_filter = [
        "category",
    ]
    autocomplete_fields = ["category"]
