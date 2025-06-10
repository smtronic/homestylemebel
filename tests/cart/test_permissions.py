import pytest
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.sessions.models import Session
from django.test import RequestFactory
from django.utils import timezone
from rest_framework.request import Request
from rest_framework.test import APIClient
from rest_framework.views import APIView

from apps.cart.models import Cart, CartItem
from apps.cart.permissions import IsCartAccessAllowed


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def cart(user):
    return Cart.objects.create(user=user)


@pytest.fixture
def anon_cart(product):
    cart = Cart.objects.create(session_key="test_session_key")
    CartItem.objects.create(cart=cart, product=product, quantity=1)
    return cart


@pytest.fixture
def cart_item(cart, product):
    return CartItem.objects.create(cart=cart, product=product, quantity=1)


@pytest.fixture
def another_user():
    from django.contrib.auth import get_user_model

    User = get_user_model()
    return User.objects.create_user(email="another@example.com", password="test")


@pytest.fixture
def anon_request():
    factory = RequestFactory()
    request = factory.get("/")
    middleware = SessionMiddleware(lambda x: None)
    middleware.process_request(request)
    request.session.save()
    request.user = AnonymousUser()
    return Request(request)


@pytest.mark.django_db
class TestIsCartAccessAllowed:
    def test_has_permission_retrieve_list(self, anon_request):
        permission = IsCartAccessAllowed()
        view = APIView()
        for action in ["retrieve", "list", "add"]:
            view.action = action
            assert permission.has_permission(anon_request, view) is True

    def test_has_permission_update_authenticated(self, user):
        factory = RequestFactory()
        request = factory.patch("/")
        request.user = user
        permission = IsCartAccessAllowed()
        view = APIView()
        view.action = "update_item"
        assert permission.has_permission(request, view) is True

    def test_has_permission_update_anon_with_session(self, anon_request):
        permission = IsCartAccessAllowed()
        view = APIView()
        view.action = "update_item"
        assert permission.has_permission(anon_request, view) is True

    def test_has_permission_update_anon_no_session(self):
        factory = RequestFactory()
        request = factory.patch("/")
        request.user = AnonymousUser()
        permission = IsCartAccessAllowed()
        view = APIView()
        view.action = "update_item"
        assert permission.has_permission(request, view) is False

    def test_has_object_permission_staff(self, admin_user, cart_item):
        factory = RequestFactory()
        request = factory.get("/")
        request.user = admin_user
        permission = IsCartAccessAllowed()
        assert permission.has_object_permission(request, None, cart_item) is True

    def test_has_object_permission_authenticated(self, user, cart_item):
        factory = RequestFactory()
        request = factory.get("/")
        request.user = user
        permission = IsCartAccessAllowed()
        cart_item.cart.user = user
        assert permission.has_object_permission(request, None, cart_item) is True

    def test_has_object_permission_authenticated_non_owner(
        self, user, another_user, cart_item
    ):
        factory = RequestFactory()
        request = factory.get("/")
        request.user = another_user
        permission = IsCartAccessAllowed()
        cart_item.cart.user = user
        assert permission.has_object_permission(request, None, cart_item) is False

    def test_has_object_permission_anon_with_session(self, anon_cart):
        factory = RequestFactory()
        request = factory.get("/")
        middleware = SessionMiddleware(lambda x: None)
        middleware.process_request(request)
        request.session["test"] = "data"  # Добавляем данные в сессию
        request.session.save()
        # Создаём сессию с нужным session_key
        session_data = request.session._session  # Получаем словарь сессии
        session = Session.objects.create(
            session_key=anon_cart.session_key,
            session_data=request.session.encode(session_data),  # Передаём session_data
            expire_date=timezone.now() + timezone.timedelta(days=14),
        )
        request.session = request.session.__class__(session.session_key)
        request.user = AnonymousUser()
        cart_item = anon_cart.items.first()
        permission = IsCartAccessAllowed()
        assert (
            permission.has_object_permission(Request(request), None, cart_item) is True
        )

    def test_has_object_permission_anon_wrong_session(self, anon_cart):
        factory = RequestFactory()
        request = factory.get("/")
        middleware = SessionMiddleware(lambda x: None)
        middleware.process_request(request)
        request.session.save()  # Другой session_key
        request.user = AnonymousUser()
        cart_item = anon_cart.items.first()
        permission = IsCartAccessAllowed()
        assert (
            permission.has_object_permission(Request(request), None, cart_item) is False
        )

    def test_has_object_permission_anon_no_session(self, cart_item):
        factory = RequestFactory()
        request = factory.get("/")
        request.user = AnonymousUser()
        permission = IsCartAccessAllowed()
        assert (
            permission.has_object_permission(Request(request), None, cart_item) is False
        )
