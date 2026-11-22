"""Django-innstillinger for Your Next Adventure.

Miljøverdier leses bare her, via `config.miljo` (AD-12 punkt 3). Ingen verdi står
som reserve i koden: de ligger i `.env.example`.
"""

import os
from pathlib import Path

from django.utils.csp import CSP

from config import miljo

BASE_DIR = Path(__file__).resolve().parent.parent

MILJO = miljo.last_inn(BASE_DIR, os.environ)  # NFR-1, AD-12 punkt 3

SECRET_KEY = MILJO.secret_key
DEBUG = MILJO.debug
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]"]

ANTHROPIC_API_KEY = MILJO.anthropic_api_key
MET_USER_AGENT = MILJO.met_user_agent

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "turforslag",
    "tjenester",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.csp.ContentSecurityPolicyMiddleware",  # AR-17
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# SQLite lokalt og i tester (AD-4). Postgres på Vercel kommer i story 1.2.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Egen brukermodell fra første migrering (AR-9, AD-7)
AUTH_USER_MODEL = "turforslag.Bruker"

# Bare minimumslengde 8 (AD-7)
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 8},
    },
]

# Norsk og Oslo-tid (AD-12 punkt 5)
LANGUAGE_CODE = "nb"
TIME_ZONE = "Europe/Oslo"
USE_I18N = True
USE_TZ = True

# Content-Security-Policy (AR-17). Ingen inline-skript og ingen style-attributter i malene.
SECURE_CSP = {
    "default-src": [CSP.SELF],
    "img-src": [CSP.SELF, "https://cache.kartverket.no"],
    "object-src": [CSP.NONE],
    "base-uri": [CSP.SELF],
    "form-action": [CSP.SELF],
    "frame-ancestors": [CSP.NONE],
}

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
