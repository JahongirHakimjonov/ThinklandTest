from django.db import models

from apps.shared.models.base import AbstractBaseModel


class ProductCategory(AbstractBaseModel):
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="categories/", blank=True, null=True)

    class Meta:
        verbose_name = "Product Category"
        verbose_name_plural = "Product Categories"
        ordering = ["-created_at"]
        db_table = "product_category"

    def __str__(self) -> str:
        return self.title
