from django.db import models

from apps.shared.models.base import AbstractBaseModel
from apps.shop.models.category import ProductCategory


class Product(AbstractBaseModel):
    title = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        ProductCategory, on_delete=models.CASCADE, related_name="products"
    )

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["-created_at"]
        db_table = "product"

    def __str__(self) -> str:
        return self.title
