import pytest
from apps.catalog.serializers import ProductListSerializer


@pytest.mark.django_db
def test_product_list_serializer_output(product):
    serializer = ProductListSerializer(product)
    expected_data = {
        "sku": product.sku,
        "name": product.name,
        "price": str(product.price),
        "discount": product.discount,
        "actual_price": str(product.actual_price),
        "main_image": product.main_image.url if product.main_image else None,
        "stock": product.stock,
        "category": product.category.slug,
    }
    assert serializer.data == expected_data
