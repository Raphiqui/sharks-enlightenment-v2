from .base import *
import os

DEBUG = False

SECRET_KEY = os.environ.get("SECRET_KEY")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
    "django": {
        "handlers": ["console"],
        "level": "DEBUG",
        "propagate": False,
    },
}

# Security
SECURE_SSL_REDIRECT = False
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")

# ── Static files ──────────────────────────────────────────────────────────────
# WhiteNoise serves static files directly from Django
# See https://whitenoise.readthedocs.io/en/stable/django.html
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        # CompressedManifestStaticFilesStorage adds cache-busting hashes
        # AND gzip/brotli compression via WhiteNoise
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# ── Django-Vite (production mode) ─────────────────────────────────────────────
# In production, Vite assets are pre-built into back/static/dist/
# The manifest.json tells django-vite which hashed filenames to inject.
DJANGO_VITE = {
    "default": {
        "dev_mode": False,
        "manifest_path": BASE_DIR / "static" / "dist" / "manifest.json",
    }
}

# ── STATICFILES_DIRS override ───────────────────────────────────────────────
# Remove the dist dir from STATICFILES_DIRS in production since collectstatic
# will pick it up, and the dir must exist before collectstatic runs.
# We keep only PROJECT_DIR/static (Django app static files).
STATICFILES_DIRS = [
    BASE_DIR / "static" / "dist",
]

import dj_database_url

if os.environ.get("DATABASE_URL"):
    DATABASES["default"] = dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600,
        conn_health_checks=True,
    )

try:
    from .local import *
except ImportError:
    pass
