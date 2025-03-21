from pytils.translit import slugify
from django.core.exceptions import ValidationError
from django.apps import apps


class ProductServices:

    @staticmethod
    def update_product_slug(product):
        if not product.slug:
            product.slug = slugify(f"{product.name}-{product.sku}")
        else:
            expected_slug = slugify(f"{product.name}-{product.sku}")
            if expected_slug not in product.slug:
                raise ValidationError(
                    "Slug не соответствует name/sku. Проверьте корректность."
                )

    @staticmethod
    def get_next_image_order(product):
        """
        Возвращает следующий доступный `ordering` для изображений продукта.
        """
        ProductExtraImage = apps.get_model(
            "catalog", "ProductExtraImage"
        )  # ← Django-way

        last_order = (
            ProductExtraImage.objects.filter(product=product)
            .order_by("-ordering")
            .first()
        )
        return (last_order.ordering + 1) if last_order else 1
