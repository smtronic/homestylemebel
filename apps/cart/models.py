from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from apps.catalog.models import Product
from uuid import uuid4

User = get_user_model()


class Cart(models.Model):
    """
    Модель корзины покупателя (для авторизованных и анонимных пользователей).
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Пользователь",
    )
    session_key = models.CharField(
        max_length=40, null=True, blank=True, verbose_name="Ключ сессии"
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

    @property
    def total(self):
        """Итоговая сумма корзины"""
        return round(sum(item.total_price for item in self.items.all()), 2)

    def __str__(self):
        return f"Корзина #{self.id}"


class CartItem(models.Model):
    """Товар в корзине"""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],  # Минимальное количество 1
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена на момент добавления"
    )

    class Meta:
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Товары в корзине"
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "product"], name="unique_product_in_cart"
            )
        ]

    @property
    def total_price(self):
        """Сумма по позиции с округлением"""
        return round(self.price * self.quantity, 2)

    def __str__(self):
        return f"{self.product.name} × {self.quantity}"
