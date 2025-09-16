from django.urls import path

from apps.shop.views.category import (
    ProductCategoryListAPIView,
    ProductCategoryDetailAPIView,
)
from apps.shop.views.product import (
    ProductAPIView,
    ProductDetailAPIView,
)

urlpatterns = [
    path(
        "product/category/",
        ProductCategoryListAPIView.as_view(),
        name="product_category",
    ),
    path(
        "product/category/<int:pk>/",
        ProductCategoryDetailAPIView.as_view(),
        name="product_category_detail",
    ),
    path("product/", ProductAPIView.as_view(), name="product"),
    path("product/<int:pk>/", ProductDetailAPIView.as_view(), name="product_detail"),
]
