import pytest
from apps.catalog.models import ProductExtraImage
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.mark.django_db
def test_extra_image_str(product):
    image = ProductExtraImage.objects.create(
        product=product,
        image=SimpleUploadedFile("test.jpg", b"file_content"),
        ordering=1,
    )
    assert str(image) == f"Доп. изображение {image.id} для {product.name}"


@pytest.mark.django_db
def test_extra_image_ordering_default(product):
    image = ProductExtraImage.objects.create(
        product=product,
        image=SimpleUploadedFile("test.jpg", b"file_content"),
        ordering=0,
    )
    assert image.ordering == 0  # Явно заданное значение сохраняется


@pytest.mark.django_db
def test_clean_sets_ordering_if_missing(product, mock_get_next_image_order):
    image = ProductExtraImage(
        product=product,
        image=SimpleUploadedFile("test.jpg", b"file_content"),
    )
    image.clean()
    assert image.ordering == 42
