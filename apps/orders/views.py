from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.orders.models import Order
from apps.orders.serializers import (
    OrderCreateSerializer,
    OrderSerializer,
    OrderUpdateSerializer,
)
from apps.orders.services.order_services import OrderService


@extend_schema_view(
    create=extend_schema(
        summary="Создать заказ",
        description="Создаёт заказ из текущей корзины. Доступно для всех пользователей. "
        "Для гостей требуется full_name, phone, email (опционально). "
        "Для аутентифицированных пользователей данные берутся из профиля, но могут быть переопределены.",
        request=OrderCreateSerializer,
        responses={
            201: OpenApiResponse(
                description="Заказ создан",
                response={
                    "type": "object",
                    "properties": {"id": {"type": "string", "format": "uuid"}},
                },
            ),
            400: OpenApiResponse(description="Неверные данные или пустая корзина"),
        },
    ),
    list=extend_schema(
        summary="Получить список заказов",
        description="Возвращает список заказов текущего аутентифицированного пользователя.",
        responses={
            200: OrderSerializer(many=True),
            401: OpenApiResponse(description="Пользователь не аутентифицирован"),
        },
    ),
    retrieve=extend_schema(
        summary="Получить детали заказа",
        description="Возвращает детали заказа по ID для аутентифицированного пользователя. "
        "Доступно только для заказов, принадлежащих пользователю.",
        responses={
            200: OrderSerializer,
            401: OpenApiResponse(description="Пользователь не аутентифицирован"),
            403: OpenApiResponse(description="Доступ запрещён"),
            404: OpenApiResponse(description="Заказ не найден"),
        },
    ),
    cancel=extend_schema(
        summary="Отменить заказ",
        description="Позволяет администратору отменить заказ. Статус должен быть 'new' или 'processing'.",
        request=None,
        responses={
            200: OpenApiResponse(description="Заказ успешно отменён"),
            400: OpenApiResponse(description="Нельзя отменить заказ"),
            403: OpenApiResponse(description="Нет прав"),
            404: OpenApiResponse(description="Заказ не найден"),
        },
    ),
    edit=extend_schema(
        summary="Обновить заказ",
        description="Позволяет изменить контактные данные заказа, если он ещё не завершён.",
        request=OrderUpdateSerializer,
        responses={
            200: OrderSerializer,
            400: OpenApiResponse(description="Неверные данные или заказ уже завершён"),
            403: OpenApiResponse(description="Нет доступа"),
            404: OpenApiResponse(description="Заказ не найден"),
        },
    ),
)
class OrderViewSet(viewsets.ViewSet):
    """ViewSet для работы с заказами"""

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        """Разрешения для эндпоинтов"""
        if self.action in ["list", "retrieve", "cancel", "update"]:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от действия"""
        if self.action == "create":
            return OrderCreateSerializer
        return OrderSerializer

    def create(self, request):
        serializer = OrderCreateSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        user = request.user if request.user.is_authenticated else None
        session_key = request.session.session_key
        contact_data = serializer.validated_data

        try:
            order = OrderService.create_order_from_cart(
                user=user, session_key=session_key, contact_data=contact_data
            )
            return Response({"id": str(order.id)}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        orders = Order.objects.filter(user=request.user).select_related("user")
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            order = Order.objects.get(pk=pk, user=request.user)
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response(
                {"detail": "Заказ не найден или не принадлежит пользователю"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @action(
        detail=True,
        methods=["post"],
        url_path="cancel",
        permission_classes=[IsAuthenticated],
    )
    def cancel(self, request, pk=None):
        if not request.user.is_staff:
            return Response(
                {"detail": "Только администратор может отменить заказ"}, status=403
            )

        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"detail": "Заказ не найден"}, status=404)

        try:
            OrderService.cancel_order(order)
            return Response({"detail": "Заказ успешно отменён"}, status=200)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=400)

    @action(
        detail=True,
        methods=["patch"],
        url_path="edit",
        permission_classes=[IsAuthenticated],
    )
    def edit(self, request, pk=None):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"detail": "Заказ не найден"}, status=404)

        user = request.user
        if not (user.is_staff or order.user == user):
            return Response({"detail": "Нет доступа к заказу"}, status=403)

        serializer = OrderUpdateSerializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(OrderSerializer(order).data)
