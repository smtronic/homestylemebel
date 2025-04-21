from django.db import transaction
from django.core.exceptions import ValidationError
from apps.cart.models import Cart, CartItem
from apps.catalog.models import Product


class CartService:
    @staticmethod
    def get_or_create_cart(request):
        """
        Get or create a cart for the user, if authenticated, or for the session if anonymous.
        """
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
        """
        Add product to cart with stock validation and handling of duplicates (if product already exists).
        """
        # Ensure enough stock is available
        if quantity > product.stock:
            raise ValidationError(
                f"Not enough stock for product '{product.name}'. Available: {product.stock}."
            )

        # Add or update item in the cart
        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"quantity": quantity, "price": product.actual_price},
        )

        # If the item already exists, just update the quantity
        if not created:
            item.quantity += quantity
            item.save()

        return item

    @staticmethod
    @transaction.atomic
    def remove_from_cart(cart, product):
        """
        Remove an item from the cart.
        """
        CartItem.objects.filter(cart=cart, product=product).delete()

    @staticmethod
    def get_cart_total(cart):
        """
        Get the total sum of the cart.
        """
        return round(sum(item.total_price for item in cart.items.all()), 2)
