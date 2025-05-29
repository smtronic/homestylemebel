from uuid import UUID

from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.cart.cart_services import CartService
from apps.cart.permissions import IsCartAccessAllowed
from apps.cart.serializers import (
    AddToCartSerializer,
    CartItemSerializer,
    CartItemUpdateSerializer,
    CartSerializer,
)


@extend_schema_view(
    get_current_cart=extend_schema(responses=CartSerializer),
    list=extend_schema(responses=CartItemSerializer(many=True)),
    add=extend_schema(
        request=AddToCartSerializer,
        responses={201: CartItemSerializer},
        summary="Добавить товар в корзину",
    ),
    update_item=extend_schema(
        request=CartItemUpdateSerializer,
        parameters=[
            OpenApiParameter(
                name="pk",
                type=UUID,
                location=OpenApiParameter.PATH,
                description="UUID позиции товара в корзине",
                required=True,
            )
        ],
        responses={200: CartItemSerializer},
        summary="Обновить количество товара",
        description="Изменяет количество конкретной позиции в корзине.",
    ),
    remove=extend_schema(
        parameters=[
            OpenApiParameter(
                name="pk",
                type=UUID,
                location=OpenApiParameter.PATH,
                description="UUID позиции товара в корзине",
                required=True,
            )
        ],
        responses={204: None},
        summary="Удалить товар из корзины",
    ),
)
class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsCartAccessAllowed]

    def get_serializer_class(self):
        if self.action == "get_current_cart":
            return CartSerializer
        if self.action == "list":
            return CartItemSerializer
        if self.action == "add":
            return AddToCartSerializer
        if self.action == "update_item":
            return CartItemUpdateSerializer
        return None  # для remove — нет тела запроса

    @action(detail=False, methods=["get"], url_path="detail", name="cart-detail")
    def get_current_cart(self, request):
        cart = CartService.get_or_create_cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def list(self, request):
        cart = CartService.get_or_create_cart(request)
        service = CartService(cart)
        items = service.get_items()
        serializer = CartItemSerializer(items, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["post"], url_path="add", name="cart-add")
    def add(self, request):
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart = CartService.get_or_create_cart(request)
        service = CartService(cart)
        try:
            item = service.add_item(
                product_id=serializer.validated_data["product_id"],
                quantity=serializer.validated_data["quantity"],
            )
            return Response(
                CartItemSerializer(item).data,
                status=status.HTTP_201_CREATED,
            )
        except DjangoValidationError as e:
            raise DRFValidationError(
                e.message_dict if hasattr(e, "message_dict") else e.messages
            )

    @action(detail=True, methods=["patch"], url_path="update", name="cart-update")
    def update_item(self, request, pk=None):
        cart = CartService.get_or_create_cart(request)
        service = CartService(cart)

        serializer = CartItemUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        item = service.update_item(pk, serializer.validated_data["quantity"])
        return Response(CartItemSerializer(item).data)

    @action(detail=True, methods=["delete"], url_path="remove", name="cart-remove")
    def remove(self, request, pk=None):
        cart = CartService.get_or_create_cart(request)
        service = CartService(cart)
        service.remove_item(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
