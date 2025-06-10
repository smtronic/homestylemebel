import pytest

from apps.catalog.serializers import ProductExtraImageSerializer


@pytest.mark.django_db
def test_extra_image_serializer_output(extra_image):
    serializer = ProductExtraImageSerializer(extra_image)
    expected_data = {
        "image": extra_image.image.url if extra_image.image else None,
    }
    assert serializer.data == expected_data
