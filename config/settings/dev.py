from .base import *

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

INSTALLED_APPS += [
    "debug_toolbar",
    "django_extensions",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
] + MIDDLEWARE

INTERNAL_IPS = [
    "127.0.0.1",
]
