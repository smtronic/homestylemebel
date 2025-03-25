from django.db import transaction
from apps.cart.models import Cart, CartItem
from django.core.exceptions import ValidationError


class CartService:
    @staticmethod
    def get_or_create_cart(request):
        """Получение или создание корзины с автоматической привязкой"""
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
        else:
            if not request.session.session_key:
                request.session.create()
            cart, _ = Cart.objects.get_or_create(
                session_key=request.session.session_key
            )
        return cart

    @staticmethod
    @transaction.atomic
    def add_to_cart(cart, product, quantity=1):
        """Добавление товара в корзину с обработкой дублей"""
        if quantity > product.stock:
            raise ValidationError(
                f"На складе недостаточно товара '{product.name}'. Остаток: {product.stock}."
            )

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"quantity": quantity, "price": product.actual_price},
        )

        if not created:
            item.quantity += quantity
            item.save()
        return item
