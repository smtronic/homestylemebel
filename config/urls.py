from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from django.views.generic import TemplateView

urlpatterns = [
    # Админка
    path("admin/", admin.site.urls),
    # API v1
    path("api/v1/catalog/", include("apps.catalog.urls")),
    path("api/v1/carts/", include("apps.cart.urls")),
    path("api/v1/orders/", include("apps.orders.urls")),
    # Swagger и Redoc
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/v1/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/v1/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
        path(
            "api/v1/",
            TemplateView.as_view(template_name="api_index.html"),
            name="api-index",
        ),
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
