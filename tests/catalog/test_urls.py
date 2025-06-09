from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.catalog.models import Category, Product
from apps.users.models import User


class CategoryURLTest(APITestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Столы", slug="stolyi")
        self.url_list = reverse("category-list")  # Используем имя маршрута
        self.url_detail = reverse("category-detail", args=[self.category.slug])

    def test_get_category_list(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # DRF pagination: response.data может быть словарём с ключом 'results'
        data = response.data
        if isinstance(data, dict) and "results" in data:
            data = data["results"]
        names = [cat["name"] for cat in data]
        self.assertIn(self.category.name, names)

    def test_get_category_detail(self):
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.category.name)


class ProductURLTest(APITestCase):

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
        self.url_list = reverse("product-list")  # Используем имя маршрута
        self.url_detail = reverse("product-detail", args=[self.product.slug])

    def test_get_product_list(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # DRF pagination: response.data может быть словарём с ключом 'results'
        data = response.data
        if isinstance(data, dict) and "results" in data:
            data = data["results"]
        skus = [prod["sku"] for prod in data]
        self.assertIn(self.product.sku, skus)

    def test_get_product_detail(self):
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["sku"], self.product.sku)

    def test_create_product_as_admin(self):
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
        response = self.client.post(self.url_list, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_product_as_user(self):
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
        response = self.client.post(self.url_list, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
