from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.shared.exceptions.http404 import get_object_or_404
from apps.shared.pagination.custom import CustomPagination
from apps.shared.permissions.role import HasRole
from apps.shop.models.product import ProductCategory
from apps.shop.serializers.product import ProductCategorySerializer
from apps.users.models.users import RoleChoices


class ProductCategoryListAPIView(APIView):
    serializer_class = ProductCategorySerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.IsAuthenticated()]
        return [HasRole([RoleChoices.ADMIN, RoleChoices.MODERATOR])]

    @extend_schema(
        summary="List Product Categories",
        description="Retrieve a list of all product categories.",
        responses={200: ProductCategorySerializer(many=True)},
    )
    @extend_schema(operation_id="product_category_list")
    def get(self, request):
        queryset = ProductCategory.objects.all()
        paginator = self.pagination_class()
        paginated_data = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(
            paginated_data, many=True, context={"request": request}
        )
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Product category created successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "success": False,
                "message": "Product category creation failed",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class ProductCategoryDetailAPIView(APIView):
    serializer_class = ProductCategorySerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.IsAuthenticated()]
        return [HasRole([RoleChoices.ADMIN, RoleChoices.MODERATOR])]

    @extend_schema(operation_id="product_category_detail")
    def get(self, request, pk):
        product_category = get_object_or_404(ProductCategory, pk=pk)
        serializer = self.serializer_class(
            product_category, context={"request": request}
        )
        return Response(
            {
                "success": True,
                "message": "Product category data",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def patch(self, request, pk):
        product_category = get_object_or_404(ProductCategory, pk=pk)
        serializer = self.serializer_class(
            product_category,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Product category updated successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "success": False,
                "message": "Product category update failed",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, pk):
        product_category = get_object_or_404(ProductCategory, pk=pk)
        product_category.delete()
        return Response(
            {
                "success": True,
                "message": "Product category deleted successfully",
            },
            status=status.HTTP_200_OK,
        )
