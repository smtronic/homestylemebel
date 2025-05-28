from decimal import ROUND_HALF_UP, Decimal
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

from apps.cart.validators import validate_stock
from apps.catalog.models import Product

User = get_user_model()


class Cart(models.Model):
    """
    Модель корзины покупателя (для авторизованных и анонимных пользователей).
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  # Корзина удаляется при удалении пользователя
        null=True,
        blank=True,
        verbose_name="Пользователь",
    )
    session_key = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        verbose_name="Ключ сессии",
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z0-9]{20,40}$",
                message="Некорректный ключ сессии.",
                code="invalid_session_key",
            )
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"
        constraints = [
            models.CheckConstraint(
                check=models.Q(user__isnull=False)
                | models.Q(session_key__isnull=False),
                name="cart_has_user_or_session",
            )
        ]
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["session_key"]),
        ]

    @property
    def total(self):
        """Итоговая сумма корзины"""
        total = sum(item.total_price for item in self.items.all())
        return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def __str__(self):
        return f"Корзина #{self.id}"


class CartItem(models.Model):
    """Товар в корзине"""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,  # При удалении товара поле становится NULL
        null=True,
        blank=True,
        verbose_name="Товар",
    )
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
    )

    class Meta:
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Товары в корзине"
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "product"],
                name="unique_product_in_cart",
                condition=models.Q(
                    product__isnull=False
                ),  # Уникальность только для product != NULL
            )
        ]
        indexes = [
            models.Index(fields=["cart"]),
            models.Index(fields=["product"]),
        ]

    @property
    def price(self):
        """Цена товара или 0.00, если товар удалён"""
        return (
            self.product.actual_price
            if self.product and self.product.available_for_order
            else Decimal("0.00")
        )

    @property
    def total_price(self):
        """Сумма по позиции с округлением"""
        total = self.price * Decimal(self.quantity)
        return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def clean(self):
        """Проверка quantity на соответствие product.stock и available_for_order"""
        if not self.product:
            raise ValidationError("Товар не существует.")
        if self.product.available_for_order:
            validate_stock(self.product, self.quantity, current_quantity=0)
        else:
            raise ValidationError(f"Товар '{self.product.name}' недоступен для заказа.")

    def __str__(self):
        return f"{self.product.name if self.product else 'Удалённый товар'} × {self.quantity}"
