from decimal import Decimal

import pytest

from apps.cart.models import Cart, CartItem
from apps.cart.serializers import (
    AddToCartSerializer,
    CartItemSerializer,
    CartItemUpdateSerializer,
    CartSerializer,
)


@pytest.mark.django_db
class TestSerializers:
    def test_cart_model_total_empty(self, user):
        cart = Cart.objects.create(user=user)
        assert cart.total == Decimal("0.00")

    def test_cart_serializer(self, user, product):
        cart = Cart.objects.create(user=user)
        CartItem.objects.create(cart=cart, product=product, quantity=2)
        serializer = CartSerializer(cart)
        assert serializer.data["id"] == str(cart.id)
        assert len(serializer.data["items"]) == 1
        assert serializer.data["total"] == str(product.actual_price * Decimal("2"))

    def test_cart_serializer_empty_cart(self, user):
        cart = Cart.objects.create(user=user)
        serializer = CartSerializer(cart)
        assert serializer.data["id"] == str(cart.id)
        assert len(serializer.data["items"]) == 0
        assert serializer.data["total"] == str(Decimal("0.00"))

    def test_cart_item_serializer(self, product):
        cart = Cart.objects.create(session_key="test_session_key")
        item = CartItem.objects.create(cart=cart, product=product, quantity=2)
        serializer = CartItemSerializer(item)
        assert serializer.data["quantity"] == 2
        assert serializer.data["total_price"] == str(
            product.actual_price * Decimal("2")
        )
        assert serializer.data["is_available"] is True

    def test_cart_item_serializer_product_none(self):
        cart = Cart.objects.create(session_key="test_session_key")
        item = CartItem.objects.create(cart=cart, product=None, quantity=2)
        serializer = CartItemSerializer(item)
        assert serializer.data["product"] is None
        assert serializer.data["total_price"] == "0.00"
        assert serializer.data["is_available"] is False

    def test_cart_item_serializer_unavailable_product(self, product):
        product.available_for_order = False
        product.save()
        cart = Cart.objects.create(session_key="test_session_key")
        item = CartItem.objects.create(cart=cart, product=product, quantity=2)
        serializer = CartItemSerializer(item)
        assert serializer.data["total_price"] == "0.00"
        assert serializer.data["is_available"] is False

    def test_add_to_cart_serializer_valid(self, product):
        data = {"product_id": str(product.id), "quantity": 3}
        serializer = AddToCartSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data["quantity"] == 3
        assert serializer.validated_data["product_id"] == product.id

    def test_add_to_cart_serializer_insufficient_stock(self, product):
        product.stock = 5
        product.save()
        data = {"product_id": str(product.id), "quantity": 6}
        serializer = AddToCartSerializer(data=data)
        assert not serializer.is_valid()
        assert "Недостаточно товара" in str(serializer.errors)
        assert f"В наличии: {product.stock}" in str(serializer.errors)

    def test_add_to_cart_serializer_invalid_product_id(self):
        data = {"product_id": "550e8400-e29b-41d4-a716-446655440000", "quantity": 3}
        serializer = AddToCartSerializer(data=data)
        assert not serializer.is_valid()
        assert "Product does not exist" in str(serializer.errors)

    def test_add_to_cart_serializer_unavailable_product(self, product):
        product.available_for_order = False
        product.save()
        data = {"product_id": str(product.id), "quantity": 3}
        serializer = AddToCartSerializer(data=data)
        assert not serializer.is_valid()
        assert "недоступен для заказа" in str(serializer.errors)

    def test_add_to_cart_serializer_invalid_quantity(self):
        data = {"product_id": "550e8400-e29b-41d4-a716-446655440000", "quantity": 0}
        serializer = AddToCartSerializer(data=data)
        assert not serializer.is_valid()
        assert "Убедитесь, что это значение больше либо равно 1" in str(
            serializer.errors
        )

    def test_cart_item_update_serializer_valid(self):
        data = {"quantity": 3}
        serializer = CartItemUpdateSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data["quantity"] == 3

    def test_cart_item_update_serializer_invalid_quantity(self):
        data = {"quantity": 0}
        serializer = CartItemUpdateSerializer(data=data)
        assert not serializer.is_valid()
        assert "Убедитесь, что это значение больше либо равно 1" in str(
            serializer.errors
        )
