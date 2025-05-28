from django.urls import path
from rest_framework import routers

from .views import CategoryViewSet, ProductViewSet

router = routers.DefaultRouter()
router.register(r"products", ProductViewSet)
router.register(r"categories", CategoryViewSet)

urlpatterns = [] + router.urls
