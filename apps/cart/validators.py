from django.core.exceptions import ValidationError
from apps.catalog.models import Product


def validate_stock(
    product: Product, requested_quantity: int, current_quantity: int = 0
) -> None:
    if product is None:
        raise ValidationError("Товар не существует или был удалён.")
    if not product.available_for_order:
        raise ValidationError(f"Товар '{product.name}' недоступен для заказа.")
    if requested_quantity < 0:
        raise ValidationError("Количество должно быть положительным.")
    if product.stock is None or product.stock < 0:
        raise ValidationError("Некорректное значение запасов.")
    if requested_quantity + current_quantity > product.stock:
        raise ValidationError(
            f"Недостаточно товара '{product.name}'. В наличии: {product.stock}."
        )
