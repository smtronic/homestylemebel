from decimal import Decimal
from rest_framework.test import APITestCase
from rest_framework import status
from apps.catalog.models import Category, Product
from apps.users.models import User
from rest_framework.authtoken.models import Token


class CategoryViewSetTest(APITestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Столы", slug="stolyi")
        self.url = "/api/v1/categories/"

    def test_get_category_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_category_detail(self):
        response = self.client.get(f"{self.url}{self.category.slug}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.category.name)


class ProductViewSetTest(APITestCase):

    def setUp(self):
        # Создаем пользователей
        self.user = User.objects.create_user(
            email="testuser@example.com", password="password"
        )
        self.admin_user = User.objects.create_superuser(
            email="admin@example.com", password="password"
        )

        # Создаем категорию и продукт
        self.category = Category.objects.create(name="Столы", slug="stolyi")
        self.product = Product.objects.create(
            sku="SKU001",
            name="Стол обеденный",
            price=Decimal("100.00"),
            discount=10,
            stock=5,
            category=self.category,
            slug="stol-obedennyj-sku001",
        )
        self.product_url = f"/api/v1/products/{self.product.slug}/"
        self.products_url = "/api/v1/products/"

    def test_get_product_list(self):
        response = self.client.get(self.products_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_product_detail(self):
        response = self.client.get(self.product_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["sku"], self.product.sku)

    def test_create_product_as_admin(self):
        # В данном случае авторизация не требуется, так как мы не используем токены
        self.client.force_authenticate(user=self.admin_user)
        data = {
            "sku": "SKU002",
            "name": "Стол письменный",
            "price": 150.00,
            "discount": 15,
            "stock": 10,
            "category": self.category.id,
            "slug": "stol-pismennyj-sku002",
        }
        response = self.client.post(self.products_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_product_as_user(self):
        # Обычный пользователь не имеет прав на создание
        self.client.force_authenticate(user=self.user)
        data = {
            "sku": "SKU002",
            "name": "Стол письменный",
            "price": 150.00,
            "discount": 15,
            "stock": 10,
            "category": self.category.id,
            "slug": "stol-pismennyj-sku002",
        }
        response = self.client.post(self.products_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
