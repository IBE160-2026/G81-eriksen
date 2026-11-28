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
VERCEL = MILJO.vercel
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

# SQLite lokalt og i tester. Postgres når `DATABASE_URL` finnes (AD-4, AD-15 punkt 3).
if MILJO.database_url:
    DATABASES = {"default": miljo.database_fra_url(MILJO.database_url)}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Egen brukermodell fra første migrering (AR-9, AD-7)
AUTH_USER_MODEL = "turforslag.Bruker"

# Innlogging (FR-14): gjester som åpner Konto sendes til Logg inn med `next`.
LOGIN_URL = "turforslag:logg_inn"

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
# Vercel kjører `collectstatic` og serverer filene fra CDN-et. Ingen WhiteNoise (AD-15 punkt 4).
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Publisering på Vercel (`VERCEL` er satt), AD-15 punkt 5 og 7. DEBUG er alltid av der,
# og nøkkelen er sjekket i `config.miljo`.
if MILJO.vercel:
    ALLOWED_HOSTS = [".vercel.app"]
    CSRF_TRUSTED_ORIGINS = ["https://*.vercel.app"]
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    # Advarsler fra `check --deploy` som ikke rettes i appen (AD-15 punkt 5):
    # - security.W004 (SECURE_HSTS_SECONDS): hele toppdomenet `.app` står på HSTS-preload-
    #   listen i nettleserne, og Vercel sender selv `Strict-Transport-Security` for
    #   `*.vercel.app`.
    # - security.W008 (SECURE_SSL_REDIRECT): Vercel sender alltid HTTP videre til HTTPS
    #   med 308 før forespørselen når appen.
    SILENCED_SYSTEM_CHECKS = ["security.W004", "security.W008"]

    # Logging til standard ut, der Vercel samler kjøreloggen (AD-10 punkt 8, AD-15 punkt 7).
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "standard_ut": {"class": "logging.StreamHandler", "stream": "ext://sys.stdout"},
        },
        "root": {"handlers": ["standard_ut"], "level": "INFO"},
    }

# Innloggingsgrense (NFR-8, AR-9): så mange mislykkede forsøk med samme e-post på så mange
# minutter sperrer nye forsøk. Testene bruker `override_settings`.
INNLOGGING_MAKS_FORSOK = 5
INNLOGGING_SPERRETID_MIN = 15

# Grenser for KI-kall (FR-13, NFR-8, AD-10 punkt 9)
KI_MAKS_PER_NETTLESER_TIME = 20
KI_MAKS_PER_DOGN = 200
