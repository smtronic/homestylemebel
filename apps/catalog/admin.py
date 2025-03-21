from django.contrib import admin
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
    fields = (
        "name",
        "sku",
        "price",
        "discount",
        "stock",
        "category",
        "main_image",
        "description",
        "slug",
        "created_at",
        "updated_at",
    )
    autocomplete_fields = ["category"]
    list_filter = ("category", "discount", "stock")
    search_fields = ("name", "description")
    # prepopulated_fields = {"slug": ("name", "sku")}
    readonly_fields = ("created_at", "updated_at", "slug")

    inlines = [ProductImageInline]
