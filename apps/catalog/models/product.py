from django.urls import reverse
from apps.catalog.models.base import BaseModel
from apps.catalog.models.category import Category
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.catalog.services.product_services import ProductServices
from apps.catalog.models.managers import ProductManager


class Product(BaseModel):
    """
    Модель товара.
    """

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

    objects = ProductManager()

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["sku"]
        indexes = [
            models.Index(fields=["slug"], name="product_slug_idx"),
            models.Index(fields=["sku"], name="product_sku_idx"),
            models.Index(fields=["price"], name="product_price_idx"),
        ]

    def __str__(self):
        return f"{self.name} ({self.sku})"

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})

    @property
    def actual_price(self):
        return round(self.price * (100 - self.discount) / 100, 2)

    def clean(self, *args, **kwargs):
        self.name = self.name.strip().capitalize()
        self.sku = self.sku.strip()
        ProductServices.update_product_slug(self)

    def save(self, *args, **kwargs):
        self.clean()
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
        """
        Устанавливает `ordering`, если он не задан, и предотвращает конфликты.
        """
        if not self.ordering:  # Если ordering = 0 или None
            self.ordering = ProductServices.get_next_image_order(self.product)
