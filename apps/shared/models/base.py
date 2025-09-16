from django.db import models


class AbstractBaseModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name="Created At"
    )
    updated_at = models.DateTimeField(
        auto_now=True, db_index=True, verbose_name="Updated At"
    )

    class Meta:
        abstract = True
