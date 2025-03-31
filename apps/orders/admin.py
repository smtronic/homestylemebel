from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "phone", "status", "created_at", "updated_at")
    search_fields = ("full_name", "phone", "email")
    list_filter = (("status", admin.ChoicesFieldListFilter), "created_at")
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "price", "total_price")
    search_fields = ("order__id", "product__name")
    list_filter = ("order__created_at",)

    def total_price(self, obj):
        return obj.total_price

    total_price.short_description = "Сумма по позиции"
