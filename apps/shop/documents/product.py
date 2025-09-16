from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl.registries import registry

from apps.shop.models.product import Product, ProductCategory

product_index = Index("products")


@registry.register_document
class ProductDocument(Document):
    category = fields.ObjectField(
        properties={
            "id": fields.IntegerField(),
            "title": fields.TextField(),
        }
    )

    class Index:
        name = "products"
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }

    class Django:
        model = Product
        fields = [
            "id",
            "title",
            "price",
            "image",
            "description",
            "created_at",
        ]
        related_models = [
            ProductCategory,
        ]

    def get_queryset(self):
        return super().get_queryset().select_related("category")

    def get_instances_from_related(self, related_instance):
        """
        Return a queryset (or iterable) of Product instances that should
        be updated when `related_instance` (e.g. a ProductCategory) changes.
        """
        if isinstance(related_instance, ProductCategory):
            return Product.objects.filter(category=related_instance)

        return Product.objects.none()
