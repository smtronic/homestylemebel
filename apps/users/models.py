from uuid import uuid4

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

from apps.users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Кастомная модель пользователя
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(unique=True, max_length=255, verbose_name="Email")
    phone = PhoneNumberField(region="RU", unique=False, verbose_name="Контактный номер")
    first_name = models.CharField(max_length=255, verbose_name="Имя", blank=True)
    last_name = models.CharField(max_length=255, verbose_name="Фамилия", blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    is_staff = models.BooleanField(
        default=False, verbose_name="Является ли администратором"
    )
    is_superuser = models.BooleanField(
        default=False, verbose_name="Является ли суперпользователем"
    )
    date_joined = models.DateTimeField(
        default=timezone.now, verbose_name="Дата регистрации"
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name
