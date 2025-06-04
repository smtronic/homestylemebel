import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.cart.models import Cart, CartItem
from apps.orders.models import Order


from tests.conftest import UserFactory


@pytest.mark.django_db
class TestOrderViewSet:
    def test_create_order_auth_user(self, client, user, product):
        client.force_login(user)
        cart = Cart.objects.create(user=user)
        CartItem.objects.create(cart=cart, product=product, quantity=1)

        data = {
            "full_name": "Иван Иванов",
            "phone": "+79990001122",
            "email": "ivan@example.com",
        }
        response = client.post(
            reverse("orders-list"), data, content_type="application/json"
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert "id" in response.data

    def test_create_order_guest_user(self, client, product):
        response = client.post(
            reverse("carts-add"),
            {"product_id": str(product.id), "quantity": 1},
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_201_CREATED

        data = {
            "full_name": "Гость",
            "phone": "+79991112233",
            "email": "guest@example.com",
        }
        response = client.post(
            reverse("orders-list"), data, content_type="application/json"
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_order_empty_cart(self, client, user):
        client.force_login(user)
        data = {
            "full_name": "Иван",
            "phone": "+79990001122",
            "email": "ivan@example.com",
        }
        response = client.post(
            reverse("orders-list"), data, content_type="application/json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_list_orders(self, client, user, product):
        client.force_login(user)
        cart = Cart.objects.create(user=user)
        item = CartItem.objects.create(cart=cart, product=product, quantity=1)

        # Создание заказа через сервис
        from apps.orders.services.order_services import OrderService

        OrderService.create_order_from_cart(
            user=user,
            contact_data={
                "full_name": "User",
                "phone": "+79990000000",
                "email": "user@example.com",
            },
            session_key=None,
        )

        response = client.get(reverse("orders-list"))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_cancel_order_by_admin(self, client, user, product):
        user.is_staff = True
        user.save()
        client.force_login(user)
        cart = Cart.objects.create(user=user)
        item = CartItem.objects.create(cart=cart, product=product, quantity=1)

        from apps.orders.services.order_services import OrderService

        order = OrderService.create_order_from_cart(
            user=user,
            contact_data={
                "full_name": "Admin",
                "phone": "+79990000000",
                "email": "admin@example.com",
            },
            session_key=None,
        )

        response = client.post(reverse("orders-cancel", kwargs={"pk": str(order.id)}))
        assert response.status_code == status.HTTP_200_OK
        order.refresh_from_db()
        assert order.status == Order.Status.CANCELLED

    def test_update_order_by_owner(self, client, user, product):
        client.force_login(user)
        cart = Cart.objects.create(user=user)
        CartItem.objects.create(cart=cart, product=product, quantity=1)

        from apps.orders.services.order_services import OrderService

        order = OrderService.create_order_from_cart(
            user=user,
            contact_data={
                "full_name": "Ivan",
                "phone": "+79990000000",
                "email": "ivan@example.com",
            },
            session_key=None,
        )

        response = client.patch(
            reverse("orders-edit", kwargs={"pk": str(order.id)}),
            data={"full_name": "Иван Обновлённый"},
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_200_OK
        order.refresh_from_db()
        assert order.full_name == "Иван Обновлённый"

    def test_cart_is_cleared_after_order(self, client, user, product):
        client.force_login(user)
        client.post(
            reverse("carts-add"),
            data={"product_id": str(product.id), "quantity": 1},
            format="json",
        )

        assert CartItem.objects.filter(cart__user=user).exists()

        response = client.post(
            reverse("orders-list"),
            data={
                "full_name": "Иван Иванов",
                "phone": "+79000000000",
                "email": "ivan@example.com",
            },
            format="json",
        )

        assert response.status_code == 201
        assert not CartItem.objects.filter(cart__user=user).exists()

    def test_cannot_cancel_completed_order(self, client, user, product):
        # Делаем пользователя администратором
        user.is_staff = True
        user.save()
        client.force_login(user)

        cart = Cart.objects.create(user=user)
        CartItem.objects.create(cart=cart, product=product, quantity=1)

        from apps.orders.services.order_services import OrderService

        order = OrderService.create_order_from_cart(
            user=user,
            contact_data={
                "full_name": "User",
                "phone": "+79991112233",
                "email": "user@example.com",
            },
            session_key=None,
        )

        order.status = Order.Status.COMPLETED
        order.save()

        response = client.post(reverse("orders-cancel", kwargs={"pk": order.id}))
        assert response.status_code == 400
        assert "нельзя" in response.data["detail"].lower()

    def test_cannot_update_order_by_another_user(self, client, user, product):
        another_user = UserFactory()
        cart = Cart.objects.create(user=another_user)
        CartItem.objects.create(cart=cart, product=product, quantity=1)

        from apps.orders.services.order_services import OrderService

        order = OrderService.create_order_from_cart(
            user=another_user,
            contact_data={
                "full_name": "Other",
                "phone": "+79991110000",
                "email": "other@example.com",
            },
            session_key=None,
        )

        client.force_login(user)  # Не владелец заказа
        response = client.patch(
            reverse("orders-edit", kwargs={"pk": order.id}),
            data={"full_name": "Хакер"},
            content_type="application/json",
        )
        assert response.status_code == 403

    def test_create_order_guest_without_session(self, client, product):
        session = client.session
        session.flush()
        session.save()

        data = {
            "full_name": "NoSession",
            "phone": "+79991112233",
            "email": "guest@example.com",
        }
        response = client.post(
            reverse("orders-list"), data, content_type="application/json"
        )
        assert response.status_code == 400

        if hasattr(response.data, "get"):
            # Если response.data - это словарь
            detail = response.data.get("detail", "")
            if not detail and "non_field_errors" in response.data:
                detail = str(response.data["non_field_errors"])
        else:
            detail = str(response.data)

        assert "корзина" in detail.lower()
