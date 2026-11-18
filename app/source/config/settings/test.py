"""
Settings for `manage.py test` (local and Jenkins).

Supplies dummy values for the mandatory env vars, so the test run needs
no credentials at all.
"""

import os

os.environ.setdefault("SECRET_KEY", "test-only-not-a-secret")
os.environ.setdefault("EMAIL_HOST", "localhost")
os.environ.setdefault("EMAIL_HOST_USER", "test@example.com")
os.environ.setdefault("EMAIL_HOST_PASSWORD", "test-only")

from .base import *

DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
