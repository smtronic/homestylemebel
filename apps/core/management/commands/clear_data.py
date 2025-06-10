from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.cart.models import Cart, CartItem
from apps.catalog.models import Category, Product
from apps.orders.models import Order, OrderItem

User = get_user_model()


class Command(BaseCommand):
    help = "Очистить все тестовые данные из базы (кроме суперпользователя)"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Deleting all test data..."))
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        CartItem.objects.all().delete()
        Cart.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        self.stdout.write(self.style.SUCCESS("All test data deleted!"))
