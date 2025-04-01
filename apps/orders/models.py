from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from apps.catalog.models import Product
from uuid import uuid4
from apps.cart.models import Cart
from phonenumber_field.modelfields import PhoneNumberField


User = get_user_model()


class Order(models.Model):
    """Заказ"""

    class Status(models.TextChoices):
        NEW = "new", "Новый"
        PROCESSING = "processing", "В обработке"
        COMPLETED = "completed", "Завершён"
        CANCELLED = "cancelled", "Отменён"

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, verbose_name="Корзина")
    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    phone = PhoneNumberField(region="RU", unique=False, verbose_name="Контактный номер")
    email = models.EmailField(null=True, blank=True, verbose_name="Email")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
        verbose_name="Статус заказа",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлен")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ #{self.id} - {self.get_status_display()}"

    @property
    def total(self):
        """Общая стоимость заказа"""
        return sum(item.total_price for item in self.items.all())


class OrderItem(models.Model):
    """Товар в заказе"""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="Товар")
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name="Количество",
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена на момент заказа"
    )

    class Meta:
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Товары в заказе"
        constraints = [
            models.UniqueConstraint(
                fields=["order", "product"], name="unique_product_in_order"
            )
        ]

    def clean(self):
        """Проверки для товара в заказе"""
        if self.quantity > self.product.stock:
            raise ValidationError(
                f"Недостаточно товара '{self.product.name}' на складе. Остаток: {self.product.stock}."
            )
        if not self.price:
            self.price = self.product.actual_price

    @property
    def total_price(self):
        """Сумма по позиции с округлением"""
        return round(self.price * self.quantity, 2)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} × {self.quantity}"
