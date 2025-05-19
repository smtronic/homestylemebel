from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.db import transaction

from apps.cart.models import Cart, CartItem
from apps.catalog.models import Product
from apps.cart.validators import validate_stock


class CartService:
    """
    Сервис для работы с корзиной.
    """

    def __init__(self, cart: Cart):
        self.cart = cart

    @staticmethod
    def get_or_create_cart(request) -> Cart:
        """
        Получает или создаёт корзину пользователя/сеанса.
        """
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
        else:
            if not request.session.session_key:
                request.session.save()
            session_key = request.session.session_key
            cart, _ = Cart.objects.get_or_create(session_key=session_key)
        return cart

    @transaction.atomic
    def add_item(self, product_id: str, quantity: int) -> CartItem:
        """
        Добавляет товар в корзину.
        :param product_id: ID товара
        :param quantity: количество товара
        :return: обновлённый объект CartItem
        """
        product = get_object_or_404(Product, id=product_id)
        if not product.available_for_order:
            raise ValidationError(f"Товар '{product.name}' недоступен для заказа.")

        item, created = CartItem.objects.get_or_create(
            cart=self.cart,
            product=product,
            defaults={"quantity": quantity},
        )

        existing_quantity = 0 if created else item.quantity
        validate_stock(product, quantity, existing_quantity)

        if not created:
            item.quantity += quantity
            item.save()

        return item

    @transaction.atomic
    def update_item(self, item_id: str, new_quantity: int) -> CartItem:
        """
        Обновляет количество товара в корзине.
        :param item_id: ID элемента корзины
        :param new_quantity: новое количество
        :return: обновлённый объект CartItem
        """
        item = get_object_or_404(CartItem, id=item_id, cart=self.cart)
        if not item.product:
            raise ValidationError("Товар удалён и не может быть обновлён.")
        if not item.product.available_for_order:
            raise ValidationError(f"Товар '{item.product.name}' недоступен для заказа.")

        validate_stock(item.product, new_quantity, current_quantity=0)

        item.quantity = new_quantity
        item.save()
        return item

    @transaction.atomic
    def remove_item(self, item_id: str) -> None:
        """
        Удаляет товар из корзины.
        :param item_id: ID элемента корзины
        """
        item = get_object_or_404(CartItem, id=item_id, cart=self.cart)
        item.delete()
