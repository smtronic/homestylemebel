import pytest
from django.conf import settings


@pytest.mark.django_db
def test_category_str_representation(category):
    assert str(category) == "Столы"


@pytest.mark.django_db
def test_slug_is_generated_if_not_provided(category):
    # Фикстура создаёт категорию с name="Столы"
    assert category.slug == "stolyi"


@pytest.mark.django_db
def test_name_is_capitalized(category):
    assert category.name == "Столы"


@pytest.mark.django_db
def test_get_image_url_returns_default_if_none(category):
    category.image = None
    category.save()
    assert category.get_image_url() == "catalog/default.png"


@pytest.mark.django_db
def test_get_image_url_returns_custom_image_url(category):
    category.image = "catalog/categories/custom.png"
    category.save()
    expected_url = settings.MEDIA_URL + "catalog/categories/custom.png"
    assert category.get_image_url() == expected_url
