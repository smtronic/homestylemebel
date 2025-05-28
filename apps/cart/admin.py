from django.contrib import admin

from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "session_key", "created_at", "updated_at", "total")
    search_fields = ("user__email", "session_key")
    list_filter = ("created_at", "updated_at")
    inlines = [CartItemInline]

    def total(self, obj):
        return obj.total

    total.short_description = "Итоговая сумма"


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("cart", "product", "quantity", "total_price")
    list_display_links = ("cart", "product")
    readonly_fields = ("total_price",)
    search_fields = ("cart__id", "product__name")
    list_filter = ("cart__created_at",)
