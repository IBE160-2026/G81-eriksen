"""Logg over forkastede KI-svar: format, escape, avvisning, rotasjon, opprydding (FR-13, NFR-5)."""

import inspect
import logging
import tempfile
from datetime import date, datetime
from pathlib import Path
from unittest import mock

from django.test import SimpleTestCase, override_settings

from tjenester.ki import logg
from tjenester.ki.logg import OpprydningsHandler, filer_a_slette, logg_forkastet


def fjern_handlere():
    for h in list(logg.logger.handlers):
        h.close()
        logg.logger.removeHandler(h)


class LoggTest(SimpleTestCase):
    def setUp(self):
        fjern_handlere()
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.addCleanup(fjern_handlere)  # kjøres først, så filen er lukket før mappen slettes
        self.rot = Path(self.tmp.name)

    def linjer(self):
        for h in logg.logger.handlers:
            h.flush()
        fil = self.rot / "logs" / "ki.log"
        return fil.read_text(encoding="utf-8").split("\n")[:-1]

    def test_signatur_uten_personfelt(self):  # NFR-5
        params = list(inspect.signature(logg_forkastet).parameters)
        self.assertEqual(params, ["kalltype", "arsak", "svar"])

    def test_lokal_linje_og_ingen_mappe_for_forste_skriving(self):  # FR-13
        with override_settings(BASE_DIR=self.rot, VERCEL=False):
            self.assertFalse((self.rot / "logs").exists())
            logg_forkastet("begrunnelse", "siffer", "Turen er 5 km.")
            linjer = self.linjer()
        self.assertEqual(len(linjer), 1)
        tid, kalltype, arsak, svar = linjer[0].split("\t")
        self.assertEqual((kalltype, arsak, svar), ("begrunnelse", "siffer", "Turen er 5 km."))
        self.assertIsNotNone(datetime.fromisoformat(tid).utcoffset())

    def test_handler_legges_bare_til_en_gang(self):
        with override_settings(BASE_DIR=self.rot, VERCEL=False):
            logg_forkastet("tolking", "tidsavbrudd", None)
            logg_forkastet("tolking", "feil", None)
            linjer = self.linjer()
        self.assertEqual(len(logg.logger.handlers), 1)
        self.assertEqual(len(linjer), 2)

    def test_tomt_svar(self):
        linje = logg.lag_linje("tolking", "tidsavbrudd", None)
        self.assertTrue(linje.endswith("\ttolking\ttidsavbrudd\t"))

    def test_escape_gir_en_linje(self):
        linje = logg.lag_linje("begrunnelse", "tom", "a\nb\tc\\d\r e\x85")
        self.assertEqual(len(linje.splitlines()), 1)
        felt = linje.split("\t")
        self.assertEqual(len(felt), 4)
        self.assertEqual(felt[3], "a\\nb\\tc\\\\d\\r\\ne\\n")

    def test_avviser_ukjent_kalltype_og_arsak(self):  # NFR-5
        with override_settings(BASE_DIR=self.rot, VERCEL=False):
            for kt, ar in [("fritekst", "Ola@x.no"), ("tolking", "Ola@x.no"), ("x", "siffer")]:
                with self.subTest(kt=kt, ar=ar), self.assertRaises(ValueError):
                    logg_forkastet(kt, ar, "svar")
        self.assertFalse((self.rot / "logs").exists())

    def test_vercel_til_logger_uten_fil(self):
        with override_settings(BASE_DIR=self.rot, VERCEL=True):
            with self.assertLogs(logg.logger, logging.INFO) as cm:
                logg_forkastet("begrunnelse", "ugyldig", "x")
        self.assertEqual(len(cm.output), 1)
        self.assertFalse((self.rot / "logs").exists())
        self.assertEqual(logg.logger.handlers, [])
        self.assertTrue(logg.logger.propagate)

    def test_oserror_kastes_ikke(self):
        with override_settings(BASE_DIR=self.rot, VERCEL=False):
            with mock.patch.object(Path, "mkdir", side_effect=OSError("nei")):
                logg_forkastet("begrunnelse", "siffer", "x")
            with self.assertRaises(ValueError):
                logg_forkastet("fritekst", "siffer", "x")

    def test_rydd_tåler_oserror(self):
        mappe = self.rot / "logs"
        mappe.mkdir()
        h = OpprydningsHandler(mappe / "ki.log")
        self.addCleanup(h.close)
        with mock.patch.object(Path, "iterdir", side_effect=OSError("nei")):
            h.rydd()

    def test_doRollover_rydder(self):
        mappe = self.rot / "logs"
        mappe.mkdir()
        for n in ["ki.log.2026-09-01", "ki.log.2026-11-20"]:
            (mappe / n).write_text("x")
        h = OpprydningsHandler(mappe / "ki.log")
        self.addCleanup(h.close)
        with mock.patch.object(logg, "_i_dag", return_value=date(2026, 11, 27)):
            h.doRollover()
        navn = sorted(p.name for p in mappe.iterdir())
        self.assertNotIn("ki.log.2026-09-01", navn)
        self.assertIn("ki.log.2026-11-20", navn)

    def test_rotasjon_uten_backupcount_og_navn(self):
        mappe = self.rot / "logs"
        mappe.mkdir()
        h = OpprydningsHandler(mappe / "ki.log")
        self.addCleanup(h.close)
        self.assertEqual(h.backupCount, 0)
        self.assertEqual(h.when, "MIDNIGHT")
        self.assertEqual(h.encoding, "utf-8")
        self.assertEqual(h.suffix, "%Y-%m-%d")

    def test_opprydding_grenser(self):
        navn = [
            "ki.log.2026-10-28",
            "ki.log.2026-10-27",
            "notater.txt",
            "ki.log",
            "ki.log.2026-13-45",
            "ki.log.ugyldig",
        ]
        self.assertEqual(filer_a_slette(navn, date(2026, 11, 27)), ["ki.log.2026-10-27"])

    def test_opprydding_ved_oppstart_etter_pause(self):
        mappe = self.rot / "logs"
        mappe.mkdir()
        for n in ["ki.log.2026-09-01", "ki.log.2026-11-20", "notater.txt", "ki.log"]:
            (mappe / n).write_text("x")
        with mock.patch.object(logg, "_i_dag", return_value=date(2026, 11, 27)):
            h = OpprydningsHandler(mappe / "ki.log")
            self.addCleanup(h.close)
        self.assertEqual(
            sorted(p.name for p in mappe.iterdir()),
            ["ki.log", "ki.log.2026-11-20", "notater.txt"],
        )
