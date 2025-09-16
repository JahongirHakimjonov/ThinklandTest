from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.shop.models.category import ProductCategory


@admin.register(ProductCategory)
class ProductCategoryAdmin(ModelAdmin):
    list_display = ["id", "title"]
    search_fields = ["title"]
