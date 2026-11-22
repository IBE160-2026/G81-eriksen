"""Kildetreet følger spinen › Structural Seed (AR-1, NFR-1)."""

import unittest
from pathlib import Path

from dotenv import dotenv_values

ROT = Path(__file__).resolve().parents[1]


class KildetreTest(unittest.TestCase):
    def test_mappene_finnes(self):  # AR-1
        for mappe in [
            "config",
            "turforslag",
            "domene",
            "tjenester",
            "data",
            "skript",
            "tests",
            "tests/domene",
            "tests/tjenester",
            "tests/web",
            "tests/fixtures",
            "docs",
        ]:
            with self.subTest(mappe=mappe):
                self.assertTrue((ROT / mappe).is_dir())

    def test_filene_for_installasjon_finnes(self):  # NFR-1
        for fil in [
            "manage.py",
            "requirements.txt",
            "requirements-dev.txt",
            "pyproject.toml",
            ".env.example",
        ]:
            with self.subTest(fil=fil):
                self.assertTrue((ROT / fil).is_file())

    def test_pakkene_er_last(self):  # AR-1
        krav = (ROT / "requirements.txt").read_text(encoding="utf-8").split()
        for linje in ["Django==6.1.3", "anthropic==2.6.0", "python-dotenv==1.2.4"]:
            self.assertIn(linje, krav)
        dev = (ROT / "requirements-dev.txt").read_text(encoding="utf-8").split()
        self.assertIn("-r", dev)
        self.assertIn("requirements.txt", dev)
        self.assertIn("ruff==0.17.4", dev)

    def test_alle_pakker_har_last_versjon(self):  # AR-1
        for fil in ["requirements.txt", "requirements-dev.txt"]:
            linjer = (ROT / fil).read_text(encoding="utf-8").splitlines()
            for linje in linjer:
                linje = linje.strip()
                if not linje or linje.startswith("#") or linje == "-r requirements.txt":
                    continue
                with self.subTest(fil=fil, linje=linje):
                    self.assertIn("==", linje)

    def test_env_example_virker_uten_endring(self):  # AD-12 punkt 3
        verdier = dotenv_values(ROT / ".env.example")
        self.assertTrue(verdier["DJANGO_SECRET_KEY"])
        self.assertEqual(verdier["DEBUG"], "True")
        self.assertEqual(verdier["ANTHROPIC_API_KEY"], "")
        self.assertEqual(
            verdier["MET_USER_AGENT"],
            "YourNextAdventure/0.1 https://github.com/IBE160-2026/G81-eriksen",
        )
        self.assertNotIn("@", verdier["MET_USER_AGENT"])
        self.assertNotIn("DATABASE_URL", verdier)
