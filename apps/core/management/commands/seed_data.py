import random
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Faker
from pytils.translit import slugify

from apps.cart.models import Cart, CartItem
from apps.catalog.models import Category, Product
from apps.orders.models import Order, OrderItem

User = get_user_model()
fake = Faker("ru_RU")


class Command(BaseCommand):
    help = "Seed database with fake data for dev/demo purposes."

    def handle(self, *args, **options):
        # Users (реалистичные имена через Faker)
        users = [
            User.objects.create_user(
                email=fake.unique.email(),
                password="password",
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone=fake.phone_number(),
            )
            for _ in range(8)
        ]
        self.stdout.write(self.style.SUCCESS(f"Created {len(users)} users."))

        # Categories (мебельная тематика)
        category_names = ["Столы", "Мягкая мебель", "Стулья", "Шкафы", "Кровати"]
        categories = [
            Category.objects.create(name=name, slug=slugify(name))
            for name in category_names
        ]
        self.stdout.write(self.style.SUCCESS(f"Created {len(categories)} categories."))

        # Products (по 5 в каждой категории)
        products = []
        products_data = {
            "Столы": [
                ("Стол письменный", "SKU-0001", 6000, 3),
                ("Стол обеденный", "SKU-0002", 10000, 0),
                ("Стол журнальный", "SKU-0003", 3500, 7),
                ("Стол компьютерный", "SKU-0004", 8500, 2),
                ("Стол кухонный", "SKU-0005", 7200, 5),
            ],
            "Мягкая мебель": [
                ("Диван угловой", "SKU-0101", 45000, 5),
                ("Кресло мягкое", "SKU-0102", 12680, 9),
                ("Диван-кровать", "SKU-0103", 32000, 3),
                ("Пуф", "SKU-0104", 4100, 8),
                ("Кушетка", "SKU-0105", 21000, 1),
            ],
            "Стулья": [
                ("Стул офисный", "SKU-0201", 1730, 17),
                ("Табурет", "SKU-0202", 1410, 15),
                ("Стул деревянный", "SKU-0203", 2100, 10),
                ("Стул барный", "SKU-0204", 3200, 4),
                ("Стул складной", "SKU-0205", 1100, 12),
            ],
            "Шкафы": [
                ("Шкаф-купе", "SKU-0301", 41400, 12),
                ("Шкаф книжный", "SKU-0302", 13600, 10),
                ("Шкаф для одежды", "SKU-0303", 22000, 6),
                ("Шкаф угловой", "SKU-0304", 18500, 2),
                ("Шкаф для обуви", "SKU-0305", 9500, 8),
            ],
            "Кровати": [
                ("Кровать двуспальная", "SKU-0401", 59999, 0),
                ("Кровать детская", "SKU-0402", 9999, 1),
                ("Кровать односпальная", "SKU-0403", 15500, 3),
                ("Кровать с ящиками", "SKU-0404", 18500, 2),
                ("Кровать-чердак", "SKU-0405", 21000, 1),
            ],
        }
        for cat in categories:
            for name, sku, price, stock in products_data[cat.name]:
                product = Product.objects.create(
                    name=name,
                    sku=sku,
                    price=Decimal(price),
                    stock=stock,
                    category=cat,
                    slug=slugify(f"{name}-{sku}"),
                )
                products.append(product)
        self.stdout.write(self.style.SUCCESS(f"Created {len(products)} products."))

        # Carts & CartItems
        for user in users:
            cart = Cart.objects.create(user=user)
            for product in random.sample(products, 2):
                CartItem.objects.create(
                    cart=cart, product=product, quantity=random.randint(1, 3)
                )
        self.stdout.write(self.style.SUCCESS("Created carts and cart items for users."))

        # Orders & OrderItems
        for user in users:
            cart = Cart.objects.filter(user=user).first()
            if cart and cart.items.exists():
                order = Order.objects.create(
                    user=user,
                    cart=cart,
                    full_name=f"{user.first_name} {user.last_name}",
                    phone=user.phone,
                    email=user.email,
                    status=Order.Status.NEW,
                )
                for item in cart.items.all():
                    if item.product.stock > 0:
                        OrderItem.objects.create(
                            order=order,
                            product=item.product,
                            quantity=min(item.quantity, item.product.stock),
                            price=item.product.price,
                        )
        self.stdout.write(self.style.SUCCESS("Created orders and order items."))
        self.stdout.write(self.style.SUCCESS("Seeding complete!"))
