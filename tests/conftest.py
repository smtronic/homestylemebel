import tempfile
from decimal import Decimal

import factory
import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from faker import Faker
from PIL import Image

from apps.catalog.models import Category, Product, ProductExtraImage

fake = Faker()

User = get_user_model()


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


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    phone = factory.LazyFunction(lambda: f"+7{fake.msisdn()[3:]}")
    password = factory.PostGenerationMethodCall("set_password", "password")
    is_staff = False
    is_superuser = False
    is_active = True


@pytest.fixture
def user(db):
    return UserFactory.create()
