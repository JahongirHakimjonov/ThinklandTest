from rest_framework import serializers

from apps.shop.models.category import ProductCategory


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ["id", "title", "description", "image", "created_at"]
        read_only_fields = ["id", "created_at"]
