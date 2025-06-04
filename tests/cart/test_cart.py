import pytest
from django.test import Client
from django.urls import reverse
from rest_framework import status

from apps.cart.models import Cart, CartItem


@pytest.fixture
def client():
    return Client()


@pytest.mark.django_db
class TestCartViewSet:
    def test_retrieve_empty_cart(self, client, user):
        client.force_login(user)
        response = client.get(reverse("carts-list"))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0

    def test_retrieve_full_cart(self, client, user, product):
        client.force_login(user)
        cart = Cart.objects.create(user=user)
        CartItem.objects.create(cart=cart, product=product, quantity=2)
        response = client.get(reverse("carts-list"))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["quantity"] == 2

    def test_add_item(self, client, user, product):
        client.force_login(user)
        data = {"product_id": str(product.id), "quantity": 3}
        response = client.post(
            reverse("carts-add"), data, content_type="application/json"
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["quantity"] == 3

    def test_add_item_insufficient_stock(self, client, user, product):
        client.force_login(user)
        data = {"product_id": str(product.id), "quantity": 6}
        response = client.post(
            reverse("carts-add"), data, content_type="application/json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_item(self, client, user, product):
        client.force_login(user)
        cart = Cart.objects.create(user=user)
        item = CartItem.objects.create(cart=cart, product=product, quantity=2)
        data = {"quantity": 5}
        response = client.patch(
            reverse("carts-update-item", kwargs={"pk": str(item.id)}),
            data,
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["quantity"] == 5

    def test_remove_item(self, client, user, product):
        client.force_login(user)
        cart = Cart.objects.create(user=user)
        item = CartItem.objects.create(cart=cart, product=product)
        response = client.delete(reverse("carts-remove", kwargs={"pk": str(item.id)}))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert cart.items.count() == 0

    def test_anon_user_cart(self, client, product):
        data = {"product_id": str(product.id), "quantity": 3}
        response = client.post(
            reverse("carts-add"), data, content_type="application/json"
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["quantity"] == 3
