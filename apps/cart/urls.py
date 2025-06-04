from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.cart.views import CartViewSet

router = DefaultRouter()
router.register(r"", CartViewSet, basename="carts")

urlpatterns = [
    path("", include(router.urls)),
]
