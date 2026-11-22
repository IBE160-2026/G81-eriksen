"""`config.miljo.last_inn` (AD-12 punkt 3, NFR-1). Testene rører ikke den ekte `.env`."""

import tempfile
import unittest
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

from config import miljo

GYLDIG_ENV = (
    "DJANGO_SECRET_KEY=test-nokkel\n"
    "DEBUG=True\n"
    "ANTHROPIC_API_KEY=\n"
    "MET_USER_AGENT=YourNextAdventure/0.1 https://example.invalid\n"
)


class LastInnTest(unittest.TestCase):
    def setUp(self):
        self._mappe = tempfile.TemporaryDirectory()
        self.mappe = Path(self._mappe.name)

    def tearDown(self):
        self._mappe.cleanup()

    def skriv_env(self, innhold):
        (self.mappe / ".env").write_text(innhold, encoding="utf-8")

    def test_leser_verdiene_fra_env(self):  # NFR-1
        self.skriv_env(GYLDIG_ENV)
        verdier = miljo.last_inn(self.mappe, {})
        self.assertEqual(verdier.secret_key, "test-nokkel")
        self.assertTrue(verdier.debug)
        self.assertEqual(verdier.anthropic_api_key, "")
        self.assertEqual(verdier.met_user_agent, "YourNextAdventure/0.1 https://example.invalid")

    def test_miljoet_gaar_foran_env(self):
        self.skriv_env(GYLDIG_ENV)
        verdier = miljo.last_inn(self.mappe, {"DEBUG": "False"})
        self.assertFalse(verdier.debug)

    def test_debug_tolkes_som_sann_eller_usann(self):
        tabell = {
            "1": True,
            "yes": True,
            "on": True,
            "ja": True,
            " TRUE ": True,
            "nei": False,
            "0": False,
        }
        for verdi, forventet in tabell.items():
            with self.subTest(verdi=verdi):
                self.skriv_env(f"DJANGO_SECRET_KEY=test-nokkel\nDEBUG='{verdi}'\n")
                self.assertIs(miljo.last_inn(self.mappe, {}).debug, forventet)

    def test_mangler_env_stopper_med_norsk_melding(self):  # AD-12 punkt 3
        with self.assertRaises(ImproperlyConfigured) as feil:
            miljo.last_inn(self.mappe, {})
        self.assertIn("Kopier .env.example til .env", str(feil.exception))

    def test_tom_nokkel_stopper_med_norsk_melding(self):  # AD-12 punkt 3
        self.skriv_env("DJANGO_SECRET_KEY=\nDEBUG=True\n")
        with self.assertRaises(ImproperlyConfigured) as feil:
            miljo.last_inn(self.mappe, {})
        self.assertIn("Kopier .env.example til .env", str(feil.exception))

    def test_manglende_nokkel_stopper(self):  # AD-12 punkt 3
        self.skriv_env("DEBUG=True\n")
        with self.assertRaises(ImproperlyConfigured):
            miljo.last_inn(self.mappe, {})

    def test_vercel_hopper_over_sjekken_av_env(self):  # AD-15 punkt 5, egen sjekk i story 1.2
        verdier = miljo.last_inn(self.mappe, {"VERCEL": "1", "DJANGO_SECRET_KEY": "fra-vercel"})
        self.assertEqual(verdier.secret_key, "fra-vercel")

    def test_vercel_leser_ikke_env_fila(self):  # AD-12 punkt 3
        self.skriv_env(GYLDIG_ENV)
        verdier = miljo.last_inn(self.mappe, {"VERCEL": "1"})
        self.assertEqual(verdier.secret_key, "")
        self.assertFalse(verdier.debug)
