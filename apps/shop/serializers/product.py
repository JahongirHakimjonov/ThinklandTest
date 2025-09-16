from rest_framework import serializers

from apps.shop.models.category import ProductCategory
from apps.shop.models.product import Product
from apps.shop.serializers.category import ProductCategorySerializer


class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductCategory.objects.all(), source="category", write_only=True
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "price",
            "image",
            "description",
            "category",
            "category_id",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]
