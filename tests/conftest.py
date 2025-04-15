import pytest
import tempfile
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.catalog.models import Category, Product, ProductExtraImage
from decimal import Decimal


@pytest.fixture
def category():
    return Category.objects.create(name=" Столы ")


@pytest.fixture
def product(category):
    return Product.objects.create(
        name="Стол обеденный",
        sku="SKU001",
        price=Decimal("100.00"),
        discount=10,
        stock=5,
        category=category,
    )


@pytest.fixture
def mock_get_next_image_order(mocker):
    return mocker.patch(
        "apps.catalog.models.product.ProductServices.get_next_image_order",
        return_value=42,
    )


@pytest.fixture
def extra_image(product, django_test_image):
    return ProductExtraImage.objects.create(
        product=product,
        image=django_test_image,
    )


@pytest.fixture
def django_test_image():
    """Возвращает SimpleUploadedFile с изображением PNG."""
    with tempfile.NamedTemporaryFile(suffix=".png") as f:
        image = Image.new("RGB", (100, 100), color="white")
        image.save(f, format="PNG")
        f.seek(0)
        yield SimpleUploadedFile(
            name="test_image.png", content=f.read(), content_type="image/png"
        )
