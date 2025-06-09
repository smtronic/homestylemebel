from drf_spectacular.utils import extend_schema_field
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from apps.cart.models import Cart
from apps.catalog.models import Product
from apps.orders.models import Order, OrderItem


class ProductInOrderSerializer(serializers.ModelSerializer):
    """Краткая информация о товаре в заказе"""

    class Meta:
        model = Product
        fields = ("id", "name", "sku", "price", "main_image", "slug")


class OrderItemSerializer(serializers.ModelSerializer):
    """Сериализатор позиции в заказе"""

    product = ProductInOrderSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ("product", "quantity", "price", "total_price")

    @extend_schema_field({"type": "number", "format": "decimal"})
    def get_total_price(self, obj):
        return round(obj.quantity * obj.price, 2)


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор для получения заказа"""

    items = OrderItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            "id",
            "full_name",
            "email",
            "phone",
            "status",
            "created_at",
            "updated_at",
            "total",
            "items",
        )
        read_only_fields = (
            "status",
            "created_at",
            "updated_at",
            "total",
            "items",
        )

    @extend_schema_field({"type": "number", "format": "decimal"})
    def get_total(self, obj):
        return round(obj.total, 2)


class OrderCreateSerializer(serializers.Serializer):
    """Сериализатор для создания заказа"""

    full_name = serializers.CharField(max_length=255)
    phone = PhoneNumberField(region="RU")
    email = serializers.EmailField(required=False)

    def validate(self, data):
        """
        Проверка наличия корзины и её содержимого
        """
        request = self.context["request"]
        user = request.user if request.user.is_authenticated else None
        session_key = request.session.session_key

        cart = Cart.objects.filter(
            user=user if user else None, session_key=session_key if not user else None
        ).first()

        if not cart:
            raise serializers.ValidationError("Корзина не найдена.")

        if not cart.items.exists():
            raise serializers.ValidationError(
                "Нельзя оформить заказ с пустой корзиной."
            )

        return data


class OrderUpdateSerializer(serializers.ModelSerializer):
    phone = PhoneNumberField(region="RU")

    class Meta:
        model = Order
        fields = ["full_name", "phone", "email"]

    def validate(self, data):
        if self.instance.status in [Order.Status.COMPLETED, Order.Status.CANCELLED]:
            raise serializers.ValidationError(
                "Нельзя изменить завершённый или отменённый заказ."
            )
        return data
