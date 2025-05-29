from decimal import Decimal, ROUND_HALF_UP
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from apps.catalog.models import Product

User = get_user_model()


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        validators=[RegexValidator(r"^[a-zA-Z0-9]{20,40}$")],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(user__isnull=False)
                | models.Q(session_key__isnull=False),
                name="cart_has_user_or_session",
            )
        ]
        indexes = [models.Index(fields=["user"]), models.Index(fields=["session_key"])]

    @property
    def total(self) -> Decimal:
        total = sum(item.total_price for item in self.items.all())
        return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def __str__(self):
        return f"Cart #{self.id}"


class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True
    )
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "product"],
                name="unique_product_in_cart",
                condition=models.Q(product__isnull=False),
            )
        ]
        indexes = [models.Index(fields=["cart"]), models.Index(fields=["product"])]

    @property
    def price(self) -> Decimal:
        return (
            self.product.actual_price
            if self.product and self.product.available_for_order
            else Decimal("0.00")
        )

    @property
    def total_price(self) -> Decimal:
        return (self.price * Decimal(self.quantity)).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

    def __str__(self):
        return f"{self.product.name if self.product else 'Удалённый товар'} × {self.quantity}"
