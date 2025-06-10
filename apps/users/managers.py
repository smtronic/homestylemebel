from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """
    Менеджер для кастомной модели пользователя
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Создание и сохранение пользователя с email и паролем
        """
        if not email:
            raise ValueError("Пользователь должен иметь email")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Создание суперпользователя
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)
