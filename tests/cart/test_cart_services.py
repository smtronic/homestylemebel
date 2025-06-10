import pytest
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.exceptions import ValidationError
from django.test import RequestFactory

from apps.cart.cart_services import CartService
from apps.cart.models import Cart, CartItem


@pytest.fixture
def anon_request():
    request = RequestFactory().get("/")
    middleware = SessionMiddleware(lambda x: None)
    middleware.process_request(request)
    request.session.save()

    # Добавляем AuthenticationMiddleware для избежания ошибок с request.user
    auth_middleware = AuthenticationMiddleware(lambda x: None)
    auth_middleware.process_request(request)

    return request


@pytest.fixture
def auth_request(user):
    request = RequestFactory().get("/")
    middleware = SessionMiddleware(lambda x: None)
    middleware.process_request(request)
    request.session.save()

    # Устанавливаем аутентифицированного пользователя
    request.user = user
    return request


@pytest.mark.django_db
class TestCartService:
    def test_get_or_create_cart_auth(self, auth_request, user):
        cart = CartService.get_or_create_cart(auth_request)
        assert cart.user == user
        assert cart.session_key is None

    def test_get_or_create_cart_anon(self, anon_request):
        cart = CartService.get_or_create_cart(anon_request)
        assert cart.user is None
        assert cart.session_key == anon_request.session.session_key

    def test_add_item_new(self, user, product):
        cart = Cart.objects.create(user=user)
        service = CartService(cart)
        item = service.add_item(str(product.id), 3)
        assert item.quantity == 3
        assert item.product == product
        assert cart.items.count() == 1

    def test_add_item_existing(self, user, product):
        cart = Cart.objects.create(user=user)
        CartItem.objects.create(cart=cart, product=product, quantity=2)
        service = CartService(cart)
        item = service.add_item(str(product.id), 3)
        assert item.quantity == 5
        assert cart.items.count() == 1

    def test_add_item_insufficient_stock(self, user, product):
        cart = Cart.objects.create(user=user)
        service = CartService(cart)
        with pytest.raises(ValidationError, match="Недостаточно товара"):
            service.add_item(str(product.id), 6)

    def test_update_item(self, user, product):
        cart = Cart.objects.create(user=user)
        item = CartItem.objects.create(cart=cart, product=product, quantity=2)
        service = CartService(cart)
        updated_item = service.update_item(str(item.id), 5)
        assert updated_item.quantity == 5

    def test_update_item_product_none(self, user):
        cart = Cart.objects.create(user=user)
        item = CartItem.objects.create(cart=cart, product=None)
        service = CartService(cart)
        with pytest.raises(ValidationError, match="Товар не существует"):
            service.update_item(str(item.id), 5)

    def test_remove_item(self, user, product):
        cart = Cart.objects.create(user=user)
        item = CartItem.objects.create(cart=cart, product=product)
        service = CartService(cart)
        service.remove_item(str(item.id))
        assert cart.items.count() == 0
