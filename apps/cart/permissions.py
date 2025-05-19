from rest_framework.permissions import BasePermission
from django.contrib.auth.models import AnonymousUser


class IsCartAccessAllowed(BasePermission):
    """
    Пользователь имеет доступ к корзине, если:
    - Это GET/POST-запросы (list, add) без учёта владельца корзины.
    - Для остальных действий — требуется быть владельцем корзины (по user или session_key).
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет, может ли пользователь выполнить действие на уровне запроса.
        """
        if view.action in ("list", "add"):
            return True

        # Для остальных действий требуется авторизация или сессия
        return request.user.is_authenticated or (
            hasattr(request, "session") and request.session.session_key
        )

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет, может ли пользователь выполнить действие над конкретным объектом.
        """
        if request.user.is_staff:
            return True

        if request.user.is_authenticated:
            return obj.cart.user == request.user if obj.cart.user else False

        if hasattr(request, "session") and request.session.session_key:
            return obj.cart.session_key == request.session.session_key

        return False
