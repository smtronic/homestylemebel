import pytest
from decimal import Decimal


@pytest.mark.django_db
def test_actual_price_calculation(product):
    assert product.actual_price == product.price * Decimal("0.9")


@pytest.mark.django_db
def test_product_str(product):
    assert str(product) == f"{product.name} ({product.sku})"


@pytest.mark.django_db
def test_actual_price_calculation_with_discount_zero(product):
    product.discount = 0
    product.save()
    assert product.actual_price == product.price


@pytest.mark.django_db
def test_actual_price_calculation_with_discount_full(product):
    product.discount = 100
    product.save()
    assert product.actual_price == Decimal("0.00")


@pytest.mark.django_db
def test_product_availability_status(product):
    product.stock = 0
    product.save()
    assert product.availability_status == "backorder"
