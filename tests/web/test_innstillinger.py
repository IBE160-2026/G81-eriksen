"""Innstillinger og CSP (AD-12 punkt 5, AR-17)."""

import re
from pathlib import Path

from django.conf import settings
from django.test import Client, SimpleTestCase, override_settings

MALER = Path(__file__).resolve().parents[2] / "turforslag" / "templates"

FORVENTET_CSP = {
    "default-src": "'self'",
    "img-src": "'self' https://cache.kartverket.no",
    "object-src": "'none'",
    "base-uri": "'self'",
    "form-action": "'self'",
    "frame-ancestors": "'none'",
}


def csp_direktiver(svar):
    direktiver = {}
    for del_ in svar["Content-Security-Policy"].split(";"):
        navn, _, verdi = del_.strip().partition(" ")
        direktiver[navn] = verdi
    return direktiver


class InnstillingerTest(SimpleTestCase):
    def test_norsk_og_oslo(self):  # AD-12 punkt 5
        self.assertEqual(settings.LANGUAGE_CODE, "nb")
        self.assertEqual(settings.TIME_ZONE, "Europe/Oslo")
        self.assertTrue(settings.USE_TZ)

    def test_egen_brukermodell(self):  # AR-9
        self.assertEqual(settings.AUTH_USER_MODEL, "turforslag.Bruker")

    def test_bare_minimumslengde_8(self):  # AD-7
        self.assertEqual(
            settings.AUTH_PASSWORD_VALIDATORS,
            [
                {
                    "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
                    "OPTIONS": {"min_length": 8},
                }
            ],
        )


class CspTest(SimpleTestCase):
    def test_csp_hodet(self):  # AR-17
        self.assertEqual(csp_direktiver(self.client.get("/")), FORVENTET_CSP)

    def test_csp_hodet_pa_404(self):  # AR-17
        svar = self.client.get("/finnes-ikke/")
        self.assertEqual(svar.status_code, 404)
        self.assertEqual(csp_direktiver(svar), FORVENTET_CSP)

    def test_csp_hodet_pa_csrf_feil(self):  # AR-17
        svar = Client(enforce_csrf_checks=True).post("/")
        self.assertEqual(svar.status_code, 403)
        self.assertEqual(csp_direktiver(svar), FORVENTET_CSP)

    @override_settings(ROOT_URLCONF="tests.web.urls_feil")
    def test_csp_hodet_pa_500(self):  # AR-17
        with self.assertLogs("django.request", "ERROR"):
            svar = Client(raise_request_exception=False).get("/feil/")
        self.assertEqual(svar.status_code, 500)
        self.assertEqual(csp_direktiver(svar), FORVENTET_CSP)

    def test_malene_har_ingen_inline_stil_eller_skript(self):  # AR-17
        maler = sorted(MALER.rglob("*.html"))
        self.assertTrue(maler)
        for mal in maler:
            tekst = mal.read_text(encoding="utf-8")
            with self.subTest(mal=mal.name):
                self.assertIsNone(re.search(r"\sstyle\s*=", tekst, re.IGNORECASE))
                self.assertIsNone(re.search(r"<style", tekst, re.IGNORECASE))
                self.assertIsNone(re.search(r"\son[a-z]+\s*=", tekst, re.IGNORECASE))
                self.assertNotIn("javascript:", tekst.lower())
                for skript in re.findall(r"<script[^>]*>", tekst, re.IGNORECASE):
                    self.assertIsNotNone(re.search(r"\ssrc\s*=", skript, re.IGNORECASE))
