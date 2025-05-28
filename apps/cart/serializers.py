from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.cart.models import Cart, CartItem
from apps.cart.validators import validate_stock
from apps.catalog.models import Product


class ProductInCartSerializer(serializers.ModelSerializer):

    actual_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id",
            "sku",
            "name",
            "main_image",
            "slug",
            "price",
            "discount",
            "actual_price",
        )

    @extend_schema_field(serializers.DecimalField(max_digits=10, decimal_places=2))
    def get_actual_price(self, obj):
        return obj.actual_price


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductInCartSerializer(read_only=True, allow_null=True)
    total_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    is_available = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ("id", "product", "quantity", "total_price", "is_available")

    @extend_schema_field(serializers.BooleanField())
    def get_is_available(self, obj):
        return obj.product is not None and obj.product.available_for_order


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ("id", "items", "total")


class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1)

    def validate(self, data):
        product = Product.objects.filter(id=data["product_id"]).first()
        if not product:
            raise serializers.ValidationError("Товар не существует.")
        if not product.available_for_order:
            raise serializers.ValidationError(
                f"Товар '{product.name}' недоступен для заказа."
            )
        validate_stock(product, data["quantity"], current_quantity=0)
        return data


class CartItemUpdateSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)
