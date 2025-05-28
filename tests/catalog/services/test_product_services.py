from decimal import Decimal
from unittest.mock import patch

import pytest

from apps.catalog.services.product_services import ProductServices


@pytest.mark.django_db
def test_prepare_for_save_normalizes_fields(product):
    product.name = "  стол кухонный "
    product.sku = " SKU001 "
    product.slug = ""

    ProductServices.prepare_for_save(product)

    assert product.name == "Стол кухонный"
    assert product.sku == "SKU001"
    assert product.slug == "stol-kuhonnyij-sku001"


@pytest.mark.django_db
def test_calculate_actual_price_sets_correct_value(product):
    product.price = Decimal("200.00")
    product.discount = 25

    ProductServices.calculate_actual_price(product)

    assert product._actual_price == Decimal("150.00")


@pytest.mark.django_db
def test_determine_availability_status_in_stock(product):
    product.stock = 3
    ProductServices.determine_availability_status(product)
    assert product.availability_status == "in_stock"


@pytest.mark.django_db
def test_determine_availability_status_backorder(product):
    product.stock = 0
    product.available_for_order = True
    ProductServices.determine_availability_status(product)
    assert product.availability_status == "backorder"


@pytest.mark.django_db
def test_determine_availability_status_unavailable(product):
    product.stock = 0
    product.available_for_order = False
    ProductServices.determine_availability_status(product)
    assert product.availability_status == "unavailable"


@pytest.mark.django_db
def test_prepare_for_save_logs_and_raises_error(product, caplog):
    with patch(
        "apps.catalog.services.product_services.ProductServices.normalize_fields"
    ) as mock_normalize:
        mock_normalize.side_effect = ValueError("ошибка при нормализации")

        with caplog.at_level("ERROR"):
            with pytest.raises(ValueError, match="ошибка при нормализации"):
                ProductServices.prepare_for_save(product)

        assert "Ошибка при подготовке товара к сохранению" in caplog.text
        assert "ошибка при нормализации" in caplog.text
