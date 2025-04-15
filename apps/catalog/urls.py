from django.urls import path
from .views import CategoryViewSet, ProductViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"products", ProductViewSet)
router.register(r"categories", CategoryViewSet)

urlpatterns = [] + router.urls
