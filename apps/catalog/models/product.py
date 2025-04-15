from decimal import Decimal
from django.urls import reverse
from apps.catalog.models.base import BaseModel
from apps.catalog.models.category import Category
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.catalog.models.managers import ProductManager
from apps.catalog.services.product_services import ProductServices


class Product(BaseModel):
    """
    Модель товара.
    """

    class Availability(models.TextChoices):
        IN_STOCK = "in_stock", "В наличии"
        BACKORDER = "backorder", "Под заказ"
        UNAVAILABLE = "unavailable", "Недоступен"

    name = models.CharField("Название", max_length=200)
    sku = models.CharField("Артикул", max_length=50, unique=True)
    price = models.DecimalField(
        "Цена", max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    discount = models.PositiveSmallIntegerField(
        "Скидка %", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    stock = models.PositiveIntegerField("Остаток", default=0)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="products"
    )
    main_image = models.ImageField(
        "Основное изображение",
        upload_to="catalog/products/main/",
        default="catalog/default.png",
    )
    _actual_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        editable=False,
        verbose_name="Цена со скидкой",
        default=Decimal("0.00"),
    )
    available_for_order = models.BooleanField(
        "Доступен к заказу", default=True, db_index=True
    )
    availability_status = models.CharField(
        "Статус наличия",
        max_length=20,
        choices=Availability.choices,
        default=Availability.IN_STOCK,
        db_index=True,
        editable=False,
    )

    objects = ProductManager()

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["sku"]
        indexes = [
            models.Index(fields=["slug"], name="product_slug_idx"),
            models.Index(fields=["sku"], name="product_sku_idx"),
            models.Index(fields=["price"], name="product_price_idx"),
            models.Index(
                fields=["availability_status", "stock"], name="availability_idx"
            ),
        ]

    def __str__(self):
        return f"{self.name} ({self.sku})"

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})

    @property
    def actual_price(self):
        return self._actual_price

    def save(self, *args, **kwargs):
        ProductServices.prepare_for_save(self)
        super().save(*args, **kwargs)


class ProductExtraImage(BaseModel):
    """
    Модель дополнительного изображения для товара.
    """

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="catalog/products/extra/")
    ordering = models.PositiveIntegerField(
        "Порядок", default=0, validators=[MinValueValidator(0)]
    )

    class Meta:
        ordering = ["ordering"]

    def __str__(self):
        return f"Доп. изображение {self.id} для {self.product.name}"

    def clean(self):
        if not self.ordering:
            from apps.catalog.services.product_services import ProductServices

            self.ordering = ProductServices.get_next_image_order(self.product)
