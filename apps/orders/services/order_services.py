from django.db import models, transaction
from rest_framework.exceptions import ValidationError

from apps.cart.models import Cart
from apps.catalog.models import Product
from apps.orders.models import Order, OrderItem


class OrderService:
    @staticmethod
    @transaction.atomic
    def create_order_from_cart(user=None, session_key=None, contact_data=None):
        """
        Создает заказ из корзины с валидацией и обработкой транзакции
        """
        cart = OrderService._get_valid_cart(user, session_key)
        order = Order.objects.create(
            user=user,
            cart=cart,
            full_name=contact_data["full_name"],
            phone=contact_data["phone"],
            email=contact_data.get("email"),
            status=Order.Status.NEW,
        )
        OrderItem.objects.bulk_create_from_cart(
            order, cart.items.select_related("product")
        )

        # Обновление склада
        for cart_item in cart.items.select_related("product"):
            Product.objects.filter(pk=cart_item.product.pk).update(
                stock=models.F("stock") - cart_item.quantity
            )
        cart.items.all().delete()

        return order

    @staticmethod
    def _get_valid_cart(user, session_key):
        """Валидация корзины перед созданием заказа"""
        if user:
            cart = Cart.objects.filter(user=user).first()
        else:
            cart = Cart.objects.filter(session_key=session_key).first()

        if not cart:
            raise ValidationError("Корзина не найдена")

        if not cart.items.exists():
            raise ValidationError("Нельзя оформить заказ с пустой корзиной")

        for item in cart.items.select_related("product"):
            if item.quantity > item.product.stock:
                raise ValidationError(
                    f"Недостаточно товара '{item.product.name}' на складе. "
                    f"Доступно: {item.product.stock}, запрошено: {item.quantity}"
                )

        return cart

    @staticmethod
    def cancel_order(order, reason=None):
        """Отмена заказа с возвратом товаров на склад"""
        if order.status == Order.Status.CANCELLED:
            raise ValidationError("Заказ уже отменен")

        if order.status == Order.Status.COMPLETED:
            raise ValidationError("Нельзя отменить завершенный заказ")

        with transaction.atomic():
            for item in order.items.select_related("product"):
                Product.objects.filter(pk=item.product.pk).update(
                    stock=models.F("stock") + item.quantity
                )
            order.status = Order.Status.CANCELLED
            if reason:
                order.notes = f"Причина отмены: {reason}"
            order.save()

        return order
