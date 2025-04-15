from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from apps.catalog.models import Category, Product
from apps.catalog.serializers import (
    CategorySerializer,
    ProductListSerializer,
    ProductDetailSerializer,
    ProductCreateUpdateSerializer,
)
from apps.catalog.permissions import IsAdminOrReadOnly
from apps.catalog.filters import ProductFilter


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"
    permission_classes = (IsAdminOrReadOnly,)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("category").prefetch_related(
        "extra_images"
    )
    lookup_field = "slug"
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = ProductFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["name", "description", "sku"]
    ordering_fields = ["price", "sku", "discount", "stock"]
    ordering = ["price"]

    def get_serializer_class(self):
        if self.action == "list":
            return ProductListSerializer
        elif self.action == "retrieve":
            return ProductDetailSerializer
        return ProductCreateUpdateSerializer
