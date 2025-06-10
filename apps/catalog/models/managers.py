from django.db import models


class ProductManager(models.Manager):
    """
    Менеджер для модели Product.
    """

    def available(self):
        return self.filter(stock__gt=0)

    def with_extra_images(self):
        return self.prefetch_related("images")
