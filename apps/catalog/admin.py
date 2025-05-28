from django.contrib import admin

from apps.catalog.forms import ProductForm
from apps.catalog.models import Category, Product, ProductExtraImage


class ProductImageInline(admin.TabularInline):
    model = ProductExtraImage
    extra = 1
    fields = ("image", "ordering")
    readonly_fields = ("created_at", "updated_at", "slug")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ("name", "description", "image", "created_at", "updated_at", "slug")
    readonly_fields = ("created_at", "updated_at", "slug")
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "sku",
        "price",
        "stock",
        "availability_status",
        "available_for_order",
    )
    form = ProductForm
    fields = (
        "name",
        "sku",
        "price",
        "discount",
        "_actual_price",
        "stock",
        "category",
        "main_image",
        "description",
        "slug",
        "created_at",
        "updated_at",
        "available_for_order",
        "availability_status",
    )
    autocomplete_fields = ["category"]
    list_filter = ("category", "discount", "stock", "availability_status")
    search_fields = ("name", "description")
    readonly_fields = (
        "created_at",
        "updated_at",
        "slug",
        "_actual_price",
        "availability_status",
    )

    inlines = [ProductImageInline]
