"""`config.miljo.last_inn` (AD-12 punkt 3, NFR-1). Testene rører ikke den ekte `.env`."""

import tempfile
import unittest
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured
from dotenv import dotenv_values

from config import miljo

ROT = Path(__file__).resolve().parents[2]

# Falsk adresse: `last_inn` kobler aldri til databasen.
DB_URL = "postgresql://u:p@db.example.invalid/db"

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

    def test_vercel_hopper_over_sjekken_av_env(self):  # AD-15 punkt 5
        verdier = miljo.last_inn(
            self.mappe, {"VERCEL": "1", "DJANGO_SECRET_KEY": "fra-vercel", "DATABASE_URL": DB_URL}
        )
        self.assertEqual(verdier.secret_key, "fra-vercel")
        self.assertTrue(verdier.vercel)

    def test_vercel_leser_ikke_env_fila(self):  # AD-12 punkt 3
        # Nøkkelen i .env brukes ikke på Vercel, så vakten stopper appen.
        self.skriv_env(GYLDIG_ENV)
        with self.assertRaises(ImproperlyConfigured) as feil:
            miljo.last_inn(self.mappe, {"VERCEL": "1", "DATABASE_URL": DB_URL})
        self.assertIn("mangler eller er tom på Vercel", str(feil.exception))


class VercelTest(unittest.TestCase):
    """Matrisen i story 1.2 (AD-15 punkt 3 og 5, NFR-10)."""

    def setUp(self):
        self._mappe = tempfile.TemporaryDirectory()
        self.mappe = Path(self._mappe.name)

    def tearDown(self):
        self._mappe.cleanup()

    def test_lokalt_som_for(self):  # AD-4, AD-12 punkt 3
        (self.mappe / ".env").write_text(GYLDIG_ENV, encoding="utf-8")
        verdier = miljo.last_inn(self.mappe, {})
        self.assertFalse(verdier.vercel)
        self.assertTrue(verdier.debug)
        self.assertEqual(verdier.database_url, "")

    def test_vercel_gyldig_bruker_poolen(self):  # AD-15 punkt 3
        verdier = miljo.last_inn(
            self.mappe,
            {
                "VERCEL": "1",
                "DJANGO_SECRET_KEY": "egen-nokkel",
                "DATABASE_URL": "postgresql://u:p@pool/db",
                "DATABASE_URL_UNPOOLED": "postgresql://u:p@direkte/db",
            },
        )
        self.assertEqual(verdier.database_url, "postgresql://u:p@pool/db")
        self.assertFalse(verdier.debug)

    def test_bygging_bruker_den_direkte_adressen(self):  # AD-15 punkt 3
        verdier = miljo.last_inn(
            self.mappe,
            {
                "VERCEL": "1",
                "CI": "1",
                "DJANGO_SECRET_KEY": "egen-nokkel",
                "DATABASE_URL": "postgresql://u:p@pool/db",
                "DATABASE_URL_UNPOOLED": "postgresql://u:p@direkte/db",
            },
        )
        self.assertEqual(verdier.database_url, "postgresql://u:p@direkte/db")

    def test_bygging_uten_direkte_adresse_bruker_poolen(self):  # AD-15 punkt 3
        verdier = miljo.last_inn(
            self.mappe,
            {
                "VERCEL": "1",
                "CI": "1",
                "DJANGO_SECRET_KEY": "egen-nokkel",
                "DATABASE_URL": "postgresql://u:p@pool/db",
            },
        )
        self.assertEqual(verdier.database_url, "postgresql://u:p@pool/db")

    def test_mangler_eller_tom_nokkel_stopper(self):  # AD-15 punkt 5
        for environ in [
            {"VERCEL": "1", "DATABASE_URL": DB_URL},
            {"VERCEL": "1", "DJANGO_SECRET_KEY": "", "DATABASE_URL": DB_URL},
            {"VERCEL": "1", "DJANGO_SECRET_KEY": "  ", "DATABASE_URL": DB_URL},
        ]:
            with self.subTest(environ=environ):
                with self.assertRaises(ImproperlyConfigured) as feil:
                    miljo.last_inn(self.mappe, environ)
                self.assertIn("mangler eller er tom på Vercel", str(feil.exception))

    def test_utviklingsnokkelen_stopper(self):  # AD-15 punkt 5
        nokkel = dotenv_values(ROT / ".env.example")["DJANGO_SECRET_KEY"]
        with self.assertRaises(ImproperlyConfigured) as feil:
            miljo.last_inn(
                ROT, {"VERCEL": "1", "DJANGO_SECRET_KEY": nokkel, "DATABASE_URL": DB_URL}
            )
        self.assertIn("lik utviklingsnøkkelen i .env.example", str(feil.exception))
        self.assertNotIn(nokkel, str(feil.exception))

    def test_utviklingsnokkelen_leses_fra_fila(self):  # AD-15 punkt 5, ikke hardkodet
        (self.mappe / ".env.example").write_text(
            "DJANGO_SECRET_KEY=annen-eksempelverdi\n", encoding="utf-8"
        )
        with self.assertRaises(ImproperlyConfigured):
            miljo.last_inn(
                self.mappe,
                {"VERCEL": "1", "DJANGO_SECRET_KEY": "annen-eksempelverdi", "DATABASE_URL": DB_URL},
            )

    def test_debug_er_av_pa_vercel(self):  # AD-15 punkt 5
        verdier = miljo.last_inn(
            self.mappe,
            {
                "VERCEL": "1",
                "DJANGO_SECRET_KEY": "egen-nokkel",
                "DEBUG": "True",
                "DATABASE_URL": DB_URL,
            },
        )
        self.assertIs(verdier.debug, False)

    def test_mangler_database_stopper(self):  # AD-15 punkt 3
        for environ in [
            {"VERCEL": "1", "DJANGO_SECRET_KEY": "egen-nokkel"},
            {"VERCEL": "1", "DJANGO_SECRET_KEY": "egen-nokkel", "DATABASE_URL": "  "},
        ]:
            with self.subTest(environ=environ):
                with self.assertRaises(ImproperlyConfigured) as feil:
                    miljo.last_inn(self.mappe, environ)
                self.assertIn("DATABASE_URL mangler på Vercel", str(feil.exception))

    def test_ci_tolkes_som_sann_eller_usann(self):  # AD-15 punkt 3
        environ = {
            "VERCEL": "1",
            "DJANGO_SECRET_KEY": "egen-nokkel",
            "DATABASE_URL": "postgresql://u:p@pool/db",
            "DATABASE_URL_UNPOOLED": " postgresql://u:p@direkte/db ",
        }
        for ci, forventet in [("true", "direkte"), ("0", "pool"), ("false", "pool")]:
            with self.subTest(ci=ci):
                verdier = miljo.last_inn(self.mappe, {**environ, "CI": ci})
                self.assertEqual(verdier.database_url, f"postgresql://u:p@{forventet}/db")

    def test_tom_database_url_lokalt_gir_sqlite(self):  # AD-4
        (self.mappe / ".env").write_text(GYLDIG_ENV, encoding="utf-8")
        self.assertEqual(miljo.last_inn(self.mappe, {"DATABASE_URL": "   "}).database_url, "")


class DatabaseFraUrlTest(unittest.TestCase):  # AD-4, AD-15 punkt 3
    def test_postgres_url(self):
        url = "postgresql://u:p%40ss@host:5432/db?sslmode=require&channel_binding=require"
        self.assertEqual(
            miljo.database_fra_url(url),
            {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": "db",
                "USER": "u",
                "PASSWORD": "p@ss",
                "HOST": "host",
                "PORT": "5432",
                "DISABLE_SERVER_SIDE_CURSORS": True,
                "OPTIONS": {"sslmode": "require", "channel_binding": "require"},
            },
        )

    def test_postgres_skjemaet_og_uten_port(self):
        oppsett = miljo.database_fra_url("postgres://u:p@host/db")
        self.assertEqual(oppsett["ENGINE"], "django.db.backends.postgresql")
        self.assertEqual(oppsett["PORT"], "")
        self.assertEqual(oppsett["OPTIONS"], {})

    def test_ugyldig_url_stopper_med_norsk_melding(self):
        for url in [
            "mysql://u:p@host/db",
            "sqlite:///db.sqlite3",
            "postgresql://u:p@host:abc/db",
            "postgresql://u:p@host",
            "ikke en url",
        ]:
            with self.subTest(url=url):
                with self.assertRaises(ImproperlyConfigured) as feil:
                    miljo.database_fra_url(url)
                self.assertIn("DATABASE_URL må være en Postgres-adresse", str(feil.exception))
