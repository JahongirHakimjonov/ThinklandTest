from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.shared.exceptions.http404 import get_object_or_404
from apps.shared.pagination.custom import CustomPagination
from apps.shared.permissions.role import HasRole
from apps.shop.documents.product import ProductDocument
from apps.shop.models.product import Product
from apps.shop.serializers.product import ProductSerializer
from apps.users.models.users import RoleChoices


class ProductAPIView(APIView):
    serializer_class = ProductSerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.IsAuthenticated()]
        return [HasRole([RoleChoices.ADMIN, RoleChoices.MODERATOR])]

    @extend_schema(
        summary="List Products (Elasticsearch)",
        description="Retrieve a list of products, optionally filtered by category (Elasticsearch).",
        parameters=[
            OpenApiParameter(
                name="category",
                location="query",
                required=False,
                type=OpenApiTypes.INT,
                description="ID of the product category to filter by.",
            ),
            OpenApiParameter(
                name="q",
                location="query",
                required=False,
                type=OpenApiTypes.STR,
                description="Search query to filter products by title, description, or category title.",
            ),
        ],
        responses={200: ProductSerializer(many=True)},
    )
    @extend_schema(operation_id="product_list")
    def get(self, request):
        q = request.query_params.get("q", "").strip()
        category = request.query_params.get("category")

        # Start search (match_all by default)
        search = ProductDocument.search()

        # Text search: multi_match across important fields
        if q:
            # boost title higher, include category.title for better matching
            search = search.query(
                "multi_match",
                query=q,
                fields=["title^3", "description", "category.title"],
                type="best_fields",  # good default for simple text search
                operator="and",  # require all query terms (change to "or" if you want broader matches)
                fuzziness="AUTO",  # sensible default; remove or override via query param if you don't want fuzziness
            )

        # Category filter (keeps previous logic)
        if category and category.isdigit():
            search = search.filter("term", **{"category.id": int(category)})

        # Execute
        results = search.execute()

        # Build hit list and paginate with your DRF paginator API shape
        hits = [hit.to_dict() for hit in results.hits]

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(hits, request)
        serializer = self.serializer_class(
            page, many=True, context={"request": request}
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
                    "message": "Product created successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "success": False,
                "message": "Product creation failed",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class ProductDetailAPIView(APIView):
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.IsAuthenticated()]
        return [HasRole([RoleChoices.ADMIN, RoleChoices.MODERATOR])]

    @extend_schema(operation_id="product_detail")
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = self.serializer_class(product, context={"request": request})
        return Response(
            {
                "success": True,
                "message": "Product data",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def patch(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = self.serializer_class(
            product, data=request.data, partial=True, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Product updated successfully",
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "success": False,
                "message": "Product update failed",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response(
            {
                "success": True,
                "message": "Product deleted successfully",
            },
            status=status.HTTP_200_OK,
        )
