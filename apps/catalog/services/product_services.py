import logging
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from pytils.translit import slugify

logger = logging.getLogger(__name__)


class ProductServices:
    @staticmethod
    def prepare_for_save(product):
        try:
            ProductServices.normalize_fields(product)
            ProductServices.update_slug(product)

            if product.price is not None and product.discount is not None:
                ProductServices.calculate_actual_price(product)

            if product.stock is not None:
                ProductServices.determine_availability_status(product)
        except Exception as e:
            logger.error(f"Ошибка при подготовке товара к сохранению: {e}")
            raise

    @staticmethod
    def normalize_fields(product):
        product.name = product.name.strip().capitalize()
        product.sku = product.sku.strip()

    @staticmethod
    def update_slug(product):
        expected_slug = slugify(f"{product.name}-{product.sku}")

        if not product.slug or product.slug != expected_slug:
            product.slug = expected_slug

    @staticmethod
    def calculate_actual_price(product):
        product._actual_price = (
            product.price * (100 - product.discount) / 100
        ).quantize(Decimal("0.01"))

    @staticmethod
    def determine_availability_status(product):
        if product.stock > 0:
            product.availability_status = "in_stock"
        else:
            product.availability_status = (
                "backorder" if product.available_for_order else "unavailable"
            )

    @staticmethod
    def get_next_image_order(product):
        return (
            product.images.aggregate(models.Max("ordering"))["ordering__max"] or 0 + 1
        )
