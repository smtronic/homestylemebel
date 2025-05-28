from django.db import models
from django.urls import reverse
from pytils.translit import slugify

from apps.catalog.models.base import BaseModel


class Category(BaseModel):
    """
    Модель категории товаров.
    """

    name = models.CharField("Название", max_length=100, unique=True)
    image = models.ImageField(
        "Изображение", upload_to="catalog/categories/", default="catalog/default.png"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_image_url(self):
        return self.image.url if self.image else "catalog/default.png"

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})

    def clean(self):
        self.name = self.name.strip().capitalize()
        if not self.slug:
            self.slug = slugify(self.name.lower())

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
