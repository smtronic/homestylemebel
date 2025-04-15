from rest_framework import serializers
from apps.catalog.models import Category, Product, ProductExtraImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "slug", "description", "image")


class ProductExtraImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductExtraImage
        fields = ("image",)


class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field="slug", read_only=True)
    actual_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = Product
        fields = (
            "sku",
            "name",
            "price",
            "discount",
            "actual_price",
            "main_image",
            "stock",
            "category",
        )


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    extra_images = ProductExtraImageSerializer(many=True, read_only=True)
    actual_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = Product
        fields = (
            "sku",
            "name",
            "description",
            "price",
            "discount",
            "actual_price",
            "stock",
            "main_image",
            "extra_images",
            "category",
            "slug",
        )

        read_only_fields = ("slug", "actual_price")


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "sku",
            "name",
            "description",
            "price",
            "discount",
            "stock",
            "main_image",
            "category",
        )
