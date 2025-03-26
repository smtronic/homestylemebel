from django.db import models


class OrderItemManager(models.Manager):
    def bulk_create_from_cart(self, order, cart_items):
        """Создание товаров заказа из корзины"""
        order_items = [
            self.model(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.price,
            )
            for cart_item in cart_items
        ]
        self.bulk_create(order_items)
        return order_items
