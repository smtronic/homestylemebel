import pytest
from apps.catalog.serializers import ProductDetailSerializer


@pytest.mark.django_db
def test_product_detail_serializer_output(product):
    serializer = ProductDetailSerializer(product)
    expected_data = {
        "sku": product.sku,
        "name": product.name,
        "description": product.description,
        "price": str(product.price),
        "discount": product.discount,
        "actual_price": str(product.actual_price),
        "stock": product.stock,
        "main_image": product.main_image.url if product.main_image else None,
        "extra_images": [
            {"image": extra_image.image.url}
            for extra_image in product.extra_images.all()
        ],
        "category": {
            "id": str(product.category.id),
            "name": product.category.name,
            "slug": product.category.slug,
            "description": product.category.description,
            "image": product.category.image.url if product.category.image else None,
        },
        "slug": product.slug,
    }
    assert serializer.data == expected_data
