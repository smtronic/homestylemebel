from decimal import Decimal

from django.db import transaction
from django.shortcuts import get_object_or_404

from apps.cart.models import Cart, CartItem
from apps.cart.validators import validate_stock
from apps.catalog.models import Product


class CartService:
    def __init__(self, cart: Cart):
        self.cart = cart

    @staticmethod
    def get_or_create_cart(request) -> Cart:
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
        else:
            if not request.session.session_key:
                request.session.save()
            cart, _ = Cart.objects.get_or_create(
                session_key=request.session.session_key
            )
        return cart

    @transaction.atomic
    def add_item(self, product_id: str, quantity: int) -> CartItem:
        product = get_object_or_404(Product, id=product_id)
        item, created = CartItem.objects.get_or_create(
            cart=self.cart,
            product=product,
            defaults={"quantity": quantity},
        )
        new_quantity = quantity if created else item.quantity + quantity
        validate_stock(product, new_quantity, current_quantity=0)
        item.quantity = new_quantity
        item.save()
        return item

    @transaction.atomic
    def update_item(self, item_id: str, new_quantity: int) -> CartItem:
        item = get_object_or_404(CartItem, id=item_id, cart=self.cart)
        validate_stock(item.product, new_quantity, current_quantity=0)
        item.quantity = new_quantity
        item.save()
        return item

    @transaction.atomic
    def remove_item(self, item_id: str):
        item = get_object_or_404(CartItem, id=item_id, cart=self.cart)
        item.delete()

    def get_items(self):
        return self.cart.items.select_related("product")

    def total(self) -> Decimal:
        return self.cart.total
