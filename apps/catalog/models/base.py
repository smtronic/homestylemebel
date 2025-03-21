from django.db import models
from uuid import uuid4


class BaseModel(models.Model):
    """
    Базовая модель с общими полями для всех моделей.
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)
    slug = models.SlugField("Slug", max_length=150, unique=True, blank=True)
    description = models.TextField("Описание", blank=True, null=True)

    class Meta:
        abstract = True
