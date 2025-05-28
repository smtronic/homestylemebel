from uuid import UUID

from drf_spectacular.utils import (OpenApiParameter, extend_schema,
                                   extend_schema_view)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.cart.cart_services import CartService
from apps.cart.permissions import IsCartAccessAllowed
from apps.cart.serializers import (AddToCartSerializer, CartItemSerializer,
                                   CartItemUpdateSerializer, CartSerializer)


@extend_schema_view(
    add=extend_schema(
        request=AddToCartSerializer,
        responses={201: CartItemSerializer},
    ),
)
class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsCartAccessAllowed]
    serializer_class = None

    @action(detail=False, methods=["get"], url_path="detail", name="cart-detail")
    @extend_schema(
        responses=CartSerializer,
        summary="Получить корзину",
        description="Возвращает информацию о корзине: товары, сумма, ID и т.п.",
    )
    def get_current_cart(self, request):
        cart = CartService.get_or_create_cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @extend_schema(
        responses=CartItemSerializer(many=True),
        summary="Список товаров в корзине",
    )
    def list(self, request):
        cart = CartService.get_or_create_cart(request)
        service = CartService(cart)
        items = service.get_items()
        serializer = CartItemSerializer(items, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["post"], url_path="add", name="cart-add")
    @extend_schema(
        request=AddToCartSerializer,
        responses={201: CartItemSerializer},
        summary="Добавить товар в корзину",
    )
    def add(self, request):
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart = CartService.get_or_create_cart(request)
        service = CartService(cart)
        item = service.add_item(
            product_id=serializer.validated_data["product_id"],
            quantity=serializer.validated_data["quantity"],
        )
        return Response(CartItemSerializer(item).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["patch"], url_path="update", name="cart-update")
    @extend_schema(
        request=CartItemUpdateSerializer,
        parameters=[
            OpenApiParameter(
                "pk",
                UUID,
                OpenApiParameter.PATH,
                description="UUID позиции товара в корзине",
            )
        ],
        responses={200: CartItemSerializer},
        summary="Обновить количество товара",
    )
    def update_item(self, request, pk=None):
        cart = CartService.get_or_create_cart(request)
        service = CartService(cart)
        serializer = CartItemUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        item = service.update_item(pk, serializer.validated_data["quantity"])
        return Response(CartItemSerializer(item).data)

    @action(detail=True, methods=["delete"], url_path="remove", name="cart-remove")
    @extend_schema(
        parameters=[
            OpenApiParameter(
                "pk",
                UUID,
                OpenApiParameter.PATH,
                description="UUID позиции товара в корзине",
            )
        ],
        responses={204: None},
        summary="Удалить товар из корзины",
    )
    def remove(self, request, pk=None):
        cart = CartService.get_or_create_cart(request)
        service = CartService(cart)
        service.remove_item(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
