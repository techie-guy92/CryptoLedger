"""
Base settings shared by dev, prod and test.

Everything comes from environment variables. Only the keys read with
env("KEY") and no default are mandatory; everything else has a safe default.
"""

import os
from datetime import timedelta
from pathlib import Path

# ------------------------------------------------------------------
# Paths & env
# ------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent.parent


def env(key: str, default: str | None = None) -> str:
    value = os.getenv(key, default)
    if value is None:
        raise RuntimeError(f"Missing required env var: {key}")
    return value


def env_bool(key: str, default: bool = False) -> bool:
    return os.getenv(key, str(default)).lower() in ("1", "true", "yes", "on")


def env_list(key: str, default: str = "") -> list[str]:
    raw = os.getenv(key, default)
    return [item.strip() for item in raw.split(",") if item.strip()]


# ------------------------------------------------------------------
# Core
# ------------------------------------------------------------------
SECRET_KEY = env("SECRET_KEY")
DEBUG = env_bool("DEBUG", False)
ALLOWED_HOSTS = env_list("ALLOWED_HOSTS", "127.0.0.1,localhost")
FRONTEND_DOMAIN = env("FRONTEND_DOMAIN", "")
CSRF_TRUSTED_ORIGINS = env_list("CSRF_TRUSTED_ORIGINS")

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

# ------------------------------------------------------------------
# Applications
# ------------------------------------------------------------------
INSTALLED_APPS = [
    "django_prometheus",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third parties
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
    "drf_spectacular",
    "django_filters",
    # created apps
    "main",
    "users",
]

MIDDLEWARE = [
    "config.metrics_middleware.MetricsHostBypassMiddleware",
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_prometheus.middleware.PrometheusAfterMiddleware",
]

PROMETHEUS_EXPORT_MIGRATIONS = True

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# ------------------------------------------------------------------
# Database (SQLite; SQLITE_PATH lets compose/k8s point it at a volume)
# ------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": env("SQLITE_PATH", str(BASE_DIR / "db.sqlite3")),
        "OPTIONS": {
            "timeout": 20,
        },
    }
}

# ------------------------------------------------------------------
# Auth
# ------------------------------------------------------------------
AUTH_USER_MODEL = "users.CustomUser"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LOGIN_REDIRECT_URL = "/admin/"
LOGOUT_REDIRECT_URL = "/admin/login/"

# ------------------------------------------------------------------
# i18n / TZ
# ------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Tehran"
USE_I18N = True
USE_TZ = True

# ------------------------------------------------------------------
# Static & media (STORAGES lives in prod.py / collectstatic.py)
# ------------------------------------------------------------------
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ------------------------------------------------------------------
# Logging (stdout only: containers/k8s collect it from there)
# ------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "{levelname} {name} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}

# ------------------------------------------------------------------
# Email
# ------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = int(env("EMAIL_PORT", "587"))
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = env_bool("EMAIL_USE_TLS", True)
EMAIL_FROM_EMAIL = EMAIL_HOST_USER

# ------------------------------------------------------------------
# DRF / JWT / API docs
# ------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 5,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_FILTER_BACKENDS": [
        "rest_framework.filters.SearchFilter",
    ],
}

# ACCESS_TOKEN / REFRESH_TOKEN are lifetimes in DAYS (same names as before)
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=int(env("ACCESS_TOKEN", "1"))),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=int(env("REFRESH_TOKEN", "7"))),
    "ROTATE_REFRESH_TOKENS": env_bool("ROTATE_REFRESH_TOKENS", False),
    "BLACKLIST_AFTER_ROTATION": env_bool("BLACKLIST_AFTER_ROTATION", False),
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "CryptoLedger",
    "DESCRIPTION": "Here you can make a plan for buying and selling your coins",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

# ------------------------------------------------------------------
# Celery / cache (not used yet; kept from the old settings.py)
# ------------------------------------------------------------------
# CELERY_BROKER_URL = env("URL_BROKER")
# CELERY_RESULT_BACKEND = env("REDIS_CELERY_RESULTS")
# CELERY_RESULT_EXPIRES = 3600
# CELERY_TASK_SERIALIZER = "json"
# CELERY_RESULT_SERIALIZER = "json"
# CELERY_ACCEPT_CONTENT = ["json"]
# CELERY_TIMEZONE = "Asia/Tehran"
# CELERY_ENABLE_UTC = True
# CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
# CELERY_BROKER_HEARTBEAT = 0
# CELERY_TASK_ACKS_LATE = True
# CELERY_TASK_REJECT_ON_WORKER_LOST = True
# CELERY_TASK_TIME_LIMIT = 300
#
# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": env("REDIS_DJANGO_CACHE"),
#         "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
#     }
# }
# SESSION_ENGINE = "django.contrib.sessions.backends.cache"
# SESSION_CACHE_ALIAS = "default"
# CACHE_TTL = 60 * 15
