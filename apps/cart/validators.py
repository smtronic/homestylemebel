from django.core.exceptions import ValidationError
from apps.catalog.models import Product


def validate_stock(
    product: Product, requested_quantity: int, current_quantity: int = 0
) -> None:
    """
    Проверяет, достаточно ли товара на складе и доступен ли он для заказа.

    Args:
        product: Объект модели Product.
        requested_quantity: Количество товара, которое хочет добавить пользователь.
        current_quantity: Текущее количество этого товара уже в корзине.

    Raises:
        ValidationError: Если товар недоступен, количество некорректно или больше доступного на складе.
    """
    if not product.available_for_order:
        raise ValidationError(f"Товар '{product.name}' недоступен для заказа.")

    if requested_quantity < 0 or current_quantity < 0:
        raise ValidationError("Количество не может быть отрицательным.")

    if product.stock is None or product.stock < 0:
        raise ValidationError(
            f"Некорректное значение stock для товара '{product.name}'."
        )

    total_requested = requested_quantity + current_quantity

    if total_requested > product.stock:
        raise ValidationError(
            {
                "error": "insufficient_stock",
                "message": (
                    f"Недостаточно товара '{product.name}' на складе. "
                    f"Доступно: {product.stock}, требуется: {total_requested}."
                ),
            }
        )
