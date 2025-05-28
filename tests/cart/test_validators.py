import pytest
from django.core.exceptions import ValidationError

from apps.cart.validators import validate_stock


@pytest.mark.django_db
class TestValidators:
    def test_validate_stock_sufficient(self, product):
        validate_stock(product, 3)

    def test_validate_stock_insufficient(self, product):
        with pytest.raises(ValidationError, match="Недостаточно товара"):
            validate_stock(product, 6)

    def test_validate_stock_not_available(self, product):
        product.available_for_order = False
        product.save()
        with pytest.raises(ValidationError, match="недоступен для заказа"):
            validate_stock(product, 1)

    def test_validate_stock_product_none(self):
        with pytest.raises(ValidationError, match="Товар не существует"):
            validate_stock(None, 1)
