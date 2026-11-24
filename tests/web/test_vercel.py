"""Publisering på Vercel (AD-15, NFR-10, AR-24)."""

import json
import os
import secrets
import subprocess
import sys
import tomllib
import unittest
from pathlib import Path

from dotenv import dotenv_values

ROT = Path(__file__).resolve().parents[2]

LES_INNSTILLINGENE = """
import json
import django
from django.conf import settings

django.setup()
db = settings.DATABASES["default"]
print(json.dumps({
    "debug": settings.DEBUG,
    "hosts": settings.ALLOWED_HOSTS,
    "csrf": settings.CSRF_TRUSTED_ORIGINS,
    "proxy": list(settings.SECURE_PROXY_SSL_HEADER),
    "okt": settings.SESSION_COOKIE_SECURE,
    "csrf_cookie": settings.CSRF_COOKIE_SECURE,
    "motor": db["ENGINE"],
    "vert": db["HOST"],
    "uten_markor": db["DISABLE_SERVER_SIDE_CURSORS"],
    "logg": settings.LOGGING["handlers"]["standard_ut"]["stream"],
    "static_root": settings.STATIC_ROOT.name,
}))
"""


def vercel_miljo(**ekstra):
    """Et miljø som på Vercel, med en tilfeldig nøkkel og uten ekte databaseadresser."""
    miljo = {
        k: v
        for k, v in os.environ.items()
        if k not in {"DATABASE_URL", "DATABASE_URL_UNPOOLED", "CI", "DEBUG"}
    }
    miljo.update(
        VERCEL="1",
        DJANGO_SECRET_KEY=secrets.token_urlsafe(50),
        DATABASE_URL="postgresql://u:p@db.example.invalid/db",
        PYTHONIOENCODING="utf-8",
    )
    miljo.update(ekstra)
    return miljo


def kjor(argumenter, miljo):
    return subprocess.run(
        [sys.executable, *argumenter],
        cwd=ROT,
        env=miljo,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=120,
    )


class FilerForVercelTest(unittest.TestCase):
    def test_pyproject_har_de_samme_pakkene_som_requirements(self):  # AD-15 punkt 1
        pyproject = tomllib.loads((ROT / "pyproject.toml").read_text(encoding="utf-8"))
        linjer = (ROT / "requirements.txt").read_text(encoding="utf-8").splitlines()
        krav = [linje.split("#")[0].strip() for linje in linjer]
        krav = [linje for linje in krav if linje and not linje.startswith("-")]
        self.assertEqual(sorted(pyproject["project"]["dependencies"]), sorted(krav))
        self.assertIn("psycopg[binary]==3.3.9", krav)

    def test_byggesteget_migrerer_og_laster_inn_turene(self):  # AD-15 punkt 4, AR-5
        pyproject = tomllib.loads((ROT / "pyproject.toml").read_text(encoding="utf-8"))
        self.assertEqual(
            pyproject["tool"]["vercel"]["scripts"]["build"],
            "python manage.py migrate --noinput && python manage.py lastinn",
        )

    def test_python_versjon_og_region(self):  # AD-15 punkt 1 og 2
        self.assertEqual((ROT / ".python-version").read_text(encoding="utf-8").strip(), "3.14")
        vercel = json.loads((ROT / "vercel.json").read_text(encoding="utf-8"))
        self.assertEqual(vercel["regions"], ["fra1"])


class InnstillingerPaVercelTest(unittest.TestCase):
    def test_check_deploy_er_ren(self):  # AD-15 punkt 5, AR-24
        svar = kjor(["manage.py", "check", "--deploy", "--fail-level", "WARNING"], vercel_miljo())
        self.assertEqual(svar.returncode, 0, svar.stdout + svar.stderr)

    def test_innstillingene_pa_vercel(self):  # AD-15 punkt 3, 4, 5 og 7
        miljo = vercel_miljo(
            DJANGO_SETTINGS_MODULE="config.settings",
            DEBUG="True",
            DATABASE_URL="postgresql://u:p@pool.example.invalid/db?sslmode=require",
        )
        svar = kjor(["-c", LES_INNSTILLINGENE], miljo)
        self.assertEqual(svar.returncode, 0, svar.stderr)
        self.assertEqual(
            json.loads(svar.stdout),
            {
                "debug": False,
                "hosts": [".vercel.app"],
                "csrf": ["https://*.vercel.app"],
                "proxy": ["HTTP_X_FORWARDED_PROTO", "https"],
                "okt": True,
                "csrf_cookie": True,
                "motor": "django.db.backends.postgresql",
                "vert": "pool.example.invalid",
                "uten_markor": True,
                "logg": "ext://sys.stdout",
                "static_root": "staticfiles",
            },
        )

    def test_utviklingsnokkelen_stopper_appen(self):  # AD-15 punkt 5
        nokkel = dotenv_values(ROT / ".env.example")["DJANGO_SECRET_KEY"]
        svar = kjor(["manage.py", "check"], vercel_miljo(DJANGO_SECRET_KEY=nokkel))
        self.assertNotEqual(svar.returncode, 0)
        self.assertIn("ImproperlyConfigured", svar.stderr)
        self.assertIn("utviklingsnøkkelen i .env.example", svar.stderr)
