import pytest
from apps.catalog.serializers import CategorySerializer


@pytest.mark.django_db
def test_category_serializer_output(category):
    serializer = CategorySerializer(category)
    expected_data = {
        "id": str(category.id),
        "name": "Столы",
        "slug": category.slug,
        "description": category.description,
        "image": category.image.url if category.image else None,
    }

    assert serializer.data == expected_data


@pytest.mark.django_db
def test_category_serializer_create():
    data = {
        "name": "Шкафы",
        "slug": "shkafy",
        "description": "Для хранения одежды",
    }
    serializer = CategorySerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    category = serializer.save()

    assert category.name == "Шкафы"
    assert category.slug == "shkafy"
    assert category.description == "Для хранения одежды"
