from .base import *  # noqa

SECRET_KEY = "django-insecure-test-key-not-for-production"

DEBUG = False
ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "test_db.sqlite3",  # noqa
    }
}

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.InMemoryStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

WAGTAILADMIN_BASE_URL = "http://testserver"

DJANGO_VITE["default"]["dev_mode"] = True  # noqa

MEDIA_ROOT = BASE_DIR / "test_media"  # noqa

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
