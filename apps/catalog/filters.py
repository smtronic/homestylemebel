from django_filters import rest_framework as django_filters

from apps.catalog.models import Category, Product


class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(
        field_name="price", lookup_expr="gte", label="Цена от"
    )
    max_price = django_filters.NumberFilter(
        field_name="price", lookup_expr="lte", label="Цена до"
    )
    in_stock = django_filters.BooleanFilter(
        field_name="stock", lookup_expr="gt", label="В наличии"
    )
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        field_name="category__slug",
        to_field_name="slug",
        label="Категория",
    )

    class Meta:
        model = Product
        fields = ["category", "min_price", "max_price", "in_stock"]
