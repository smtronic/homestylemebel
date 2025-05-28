from rest_framework.permissions import BasePermission


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
        if view.action in ("retrieve", "list", "add"):
            return True
        return request.user.is_authenticated or bool(
            hasattr(request, "session") and request.session.session_key
        )

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет, может ли пользователь выполнить действие над конкретным объектом.
        """
        if request.user.is_staff:
            return True
        if request.user.is_authenticated:
            return obj.cart.user == request.user
        if hasattr(request, "session") and request.session.session_key:
            return obj.cart.session_key == request.session.session_key
        return False
