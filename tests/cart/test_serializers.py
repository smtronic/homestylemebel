from decimal import Decimal

import pytest

from apps.cart.models import Cart, CartItem
from apps.cart.serializers import (AddToCartSerializer, CartItemSerializer,
                                   CartItemUpdateSerializer, CartSerializer)


@pytest.mark.django_db
class TestSerializers:
    def test_cart_serializer(self, user, product):
        cart = Cart.objects.create(user=user)
        CartItem.objects.create(cart=cart, product=product, quantity=2)
        serializer = CartSerializer(cart)
        assert serializer.data["id"] == str(cart.id)
        assert len(serializer.data["items"]) == 1
        assert serializer.data["total"] == str(product.actual_price * Decimal("2"))

    def test_cart_item_serializer(self, product):
        cart = Cart.objects.create(session_key="test_session_key")
        item = CartItem.objects.create(cart=cart, product=product, quantity=2)
        serializer = CartItemSerializer(item)
        assert serializer.data["quantity"] == 2
        assert serializer.data["total_price"] == str(
            product.actual_price * Decimal("2")
        )
        assert serializer.data["is_available"] is True

    def test_add_to_cart_serializer_valid(self, product):
        data = {"product_id": str(product.id), "quantity": 3}
        serializer = AddToCartSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data["quantity"] == 3

    def test_add_to_cart_serializer_insufficient_stock(self, product):
        data = {"product_id": str(product.id), "quantity": 6}
        serializer = AddToCartSerializer(data=data)
        assert not serializer.is_valid()
        assert "Недостаточно товара" in str(serializer.errors)

    def test_cart_item_update_serializer_valid(self):
        data = {"quantity": 3}
        serializer = CartItemUpdateSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data["quantity"] == 3
