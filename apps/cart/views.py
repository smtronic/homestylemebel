from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction

from apps.cart.models import CartItem
from apps.cart.serializers import (
    CartSerializer,
    CartItemSerializer,
    AddToCartSerializer,
    CartItemUpdateSerializer,
)
from apps.cart.permissions import IsCartAccessAllowed
from apps.cart.services.cart_services import CartService
from drf_spectacular.utils import OpenApiParameter, extend_schema


class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsCartAccessAllowed]

    def _get_or_create_cart(self, request):
        """Вспомогательный метод для получения или создания корзины."""
        return CartService.get_or_create_cart(request)

    def retrieve(self, request):
        """
        Возвращает информацию о корзине пользователя (ID, товары, общая сумма).
        """
        cart = self._get_or_create_cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def list(self, request):
        """
        Возвращает список товаров в корзине пользователя.
        """
        cart = self._get_or_create_cart(request)
        items = cart.items.select_related("product")
        serializer = CartItemSerializer(items, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["post"], url_path="add", url_name="add")
    @transaction.atomic
    def add(self, request):
        """
        Добавляет товар в корзину.
        """
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart = self._get_or_create_cart(request)
        service = CartService(cart)
        item = service.add_item(
            product_id=serializer.validated_data["product_id"],
            quantity=serializer.validated_data["quantity"],
        )

        return Response(CartItemSerializer(item).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["patch"], url_path="update", url_name="update")
    @extend_schema(parameters=[OpenApiParameter("id", str, OpenApiParameter.PATH)])
    @transaction.atomic
    def update_item(self, request, pk=None):
        """
        Обновляет количество товара в корзине.
        """
        serializer = CartItemUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart = self._get_or_create_cart(request)
        service = CartService(cart)
        item = service.update_item(
            item_id=pk,
            new_quantity=serializer.validated_data["quantity"],
        )

        return Response(CartItemSerializer(item).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["delete"], url_path="remove", url_name="remove")
    @extend_schema(parameters=[OpenApiParameter("id", str, OpenApiParameter.PATH)])
    @transaction.atomic
    def remove(self, request, pk=None):
        """
        Удаляет товар из корзины.
        """
        cart = self._get_or_create_cart(request)
        service = CartService(cart)
        service.remove_item(item_id=pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
