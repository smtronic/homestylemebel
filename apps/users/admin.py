from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "phone",
        "is_active",
        "is_staff",
        "is_superuser",
        "date_joined",
    )
    search_fields = ("email", "first_name", "last_name", "phone_number")
    list_filter = ("is_active", "is_staff", "is_superuser")
    ordering = ("email",)


admin.site.register(User, UserAdmin)
