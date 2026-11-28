"""BegrensetKi: telling i økt og database, reserve ved nådd grense, logg (FR-13, NFR-8)."""

import tempfile
from datetime import date, datetime, timedelta
from pathlib import Path
from unittest import mock
from zoneinfo import ZoneInfo

from django.core.management import call_command
from django.db import OperationalError
from django.test import SimpleTestCase, TestCase, override_settings

from domene.ki import KiSok, KiTur
from tjenester.ki import hent_ki, logg
from tjenester.ki.falsk import FalskKi
from tjenester.ki.grense import NOKKEL, BegrensetKi
from tjenester.ki.reserve import ReserveKi
from tjenester.models import KiForbruk

OSLO = ZoneInfo("Europe/Oslo")
SOK = KiSok(120, date(2026, 12, 1), "utsikt", None)
TUR = KiTur("t1", "Tur", ("utsikt",), "rundtur")
LOGG = "tjenester.ki.grense.logg_totalgrense_nadd"


def idag():
    return datetime.now(OSLO).date()


def fjern_handlere():
    for h in list(logg.logger.handlers):
        h.close()
        logg.logger.removeHandler(h)


class BegrensetKiTest(TestCase):
    def setUp(self):
        patch = mock.patch(LOGG)
        self.logg = patch.start()
        self.addCleanup(patch.stop)
        self.okt = {}
        self.indre = FalskKi("ki-tekst")
        self.ki = BegrensetKi(self.indre, self.okt)

    def kall(self):
        return self.ki.begrunnelse(SOK, TUR, "reserve")

    def test_to_kall_gir_en_rad_med_antall_2(self):
        self.assertEqual(self.kall().tekst, "ki-tekst")
        self.assertEqual(self.kall().tekst, "ki-tekst")
        self.assertEqual(self.indre.antall_kall, 2)
        rader = KiForbruk.objects.all()
        self.assertEqual(rader.count(), 1)
        self.assertEqual((rader[0].dato, rader[0].antall), (idag(), 2))
        self.assertEqual(len(self.okt[NOKKEL]), 2)

    @override_settings(KI_MAKS_PER_NETTLESER_TIME=2)
    def test_nettlesergrense_gir_reserve_uten_kall(self):
        self.kall()
        self.kall()
        svar = self.kall()
        self.assertEqual((svar.tekst, svar.ok), ("reserve", True))
        self.assertEqual(self.indre.antall_kall, 2)
        self.assertEqual(KiForbruk.objects.get().antall, 2)

    @override_settings(KI_MAKS_PER_DOGN=1)
    def test_dognsgrense_gjelder_ogsa_for_ny_okt(self):
        self.kall()
        ny = BegrensetKi(self.indre, {})
        self.assertEqual(ny.begrunnelse(SOK, TUR, "reserve").tekst, "reserve")
        self.assertEqual(self.indre.antall_kall, 1)
        self.assertEqual(KiForbruk.objects.get().antall, 1)

    @override_settings(KI_MAKS_PER_DOGN=0)
    def test_nadd_grense_gir_reserve_uten_rad(self):
        self.assertEqual(self.kall().tekst, "reserve")
        self.assertEqual(self.indre.antall_kall, 0)
        self.assertFalse(KiForbruk.objects.exists())

    @override_settings(KI_MAKS_PER_DOGN=2)
    def test_siste_kall_logger_en_gang(self):
        self.kall()
        self.logg.assert_not_called()
        self.kall()
        self.assertEqual(self.logg.call_count, 1)
        self.kall()  # over grensen: ingen sending, ingen ny linje
        self.assertEqual(self.logg.call_count, 1)
        self.assertEqual(self.indre.antall_kall, 2)

    @override_settings(KI_MAKS_PER_DOGN=1)
    def test_neste_dogn_kan_gi_ny_logglinje(self):
        self.kall()
        KiForbruk.objects.update(dato=idag() - timedelta(days=1))
        self.kall()
        self.assertEqual(self.logg.call_count, 2)
        self.assertEqual(KiForbruk.objects.count(), 2)

    def test_skadet_okt_behandles_som_tom(self):
        for skadet in ("søppel", 5, None, {"a": 1}, ["ikke-dato", 3, None, "2026-12-01T10:00:00"]):
            with self.subTest(skadet=skadet):
                okt = {NOKKEL: skadet}
                svar = BegrensetKi(self.indre, okt).begrunnelse(SOK, TUR, "reserve")
                self.assertEqual(svar.tekst, "ki-tekst")
                self.assertEqual(len(okt[NOKKEL]), 1)

    def test_okt_som_kaster_behandles_som_tom(self):
        class Skadet(dict):
            def get(self, *args, **kwargs):
                raise RuntimeError("skadet")

        svar = BegrensetKi(self.indre, Skadet()).begrunnelse(SOK, TUR, "r")
        self.assertEqual(svar.tekst, "ki-tekst")

    @override_settings(KI_MAKS_PER_NETTLESER_TIME=1)
    def test_gamle_tidspunkter_fjernes(self):
        gammel = (datetime.now(OSLO) - timedelta(minutes=61)).isoformat()
        self.okt[NOKKEL] = [gammel]
        self.assertEqual(self.kall().tekst, "ki-tekst")
        self.assertEqual(len(self.okt[NOKKEL]), 1)

    @override_settings(KI_MAKS_PER_NETTLESER_TIME=1)
    def test_feilet_kall_teller_likevel(self):
        indre = FalskKi.feil()
        ki = BegrensetKi(indre, self.okt)
        ki.begrunnelse(SOK, TUR, "reserve")
        ki.begrunnelse(SOK, TUR, "reserve")
        self.assertEqual(indre.antall_kall, 1)
        self.assertEqual(KiForbruk.objects.get().antall, 1)


class AtomiskOgRobustTest(TestCase):
    def setUp(self):
        patch = mock.patch(LOGG)
        self.logg = patch.start()
        self.addCleanup(patch.stop)
        self.indre = FalskKi("ki-tekst")

    @override_settings(KI_MAKS_PER_DOGN=3)
    def test_oppdatering_over_grensen_treffer_ikke(self):
        KiForbruk.objects.create(dato=idag(), antall=3)
        okt = {}
        svar = BegrensetKi(self.indre, okt).begrunnelse(SOK, TUR, "reserve")
        self.assertEqual(svar.tekst, "reserve")
        self.assertEqual(self.indre.antall_kall, 0)
        self.assertEqual(KiForbruk.objects.get().antall, 3)
        self.assertEqual(okt[NOKKEL], [])
        self.logg.assert_not_called()

    def test_db_feil_gir_reserve_uten_unntak(self):
        okt = {}
        with mock.patch.object(KiForbruk.objects, "get_or_create", side_effect=OperationalError):
            svar = BegrensetKi(self.indre, okt).begrunnelse(SOK, TUR, "reserve")
        self.assertEqual(svar.tekst, "reserve")
        self.assertEqual(self.indre.antall_kall, 0)
        self.assertEqual(okt[NOKKEL], [])

    @override_settings(KI_MAKS_PER_NETTLESER_TIME=1)
    def test_fremtidige_tidspunkter_teller_ikke(self):
        frem = (datetime.now(OSLO) + timedelta(days=3)).isoformat()
        okt = {NOKKEL: [frem]}
        svar = BegrensetKi(self.indre, okt).begrunnelse(SOK, TUR, "reserve")
        self.assertEqual(svar.tekst, "ki-tekst")
        self.assertEqual(len(okt[NOKKEL]), 1)
        self.assertNotEqual(okt[NOKKEL][0], frem)

    def test_bruker_oslo_dato_rundt_midnatt(self):
        # 23.30 UTC 1. des. er 00.30 Oslo 2. des.
        fast = datetime(2026, 12, 1, 23, 30, tzinfo=ZoneInfo("UTC"))
        with mock.patch("tjenester.ki.grense.datetime") as dt:
            dt.now.side_effect = lambda tz=None: fast.astimezone(tz)
            dt.fromisoformat = datetime.fromisoformat
            BegrensetKi(self.indre, {}).begrunnelse(SOK, TUR, "reserve")
        self.assertEqual(KiForbruk.objects.get().dato, date(2026, 12, 2))


class HentKiTest(TestCase):
    @override_settings(ANTHROPIC_API_KEY="sk-test")
    def test_nokkel_og_okt_gir_begrenset(self):
        self.assertIsInstance(hent_ki(okt={}), BegrensetKi)

    @override_settings(ANTHROPIC_API_KEY="sk-test")
    def test_tving_reserve_med_okt(self):
        self.assertIsInstance(hent_ki(tving_reserve=True, okt={}), ReserveKi)

    def test_uten_nokkel_teller_ikke(self):
        for nokkel in (None, "", "  "):
            with self.subTest(nokkel=nokkel), override_settings(ANTHROPIC_API_KEY=nokkel):
                okt = {}
                ki = hent_ki(okt=okt)
                self.assertIsInstance(ki, ReserveKi)
                self.assertEqual(ki.begrunnelse(SOK, TUR, "r").tekst, "r")
                self.assertEqual(okt, {})
                self.assertFalse(KiForbruk.objects.exists())


class TotalgrenseLoggTest(TestCase):
    def setUp(self):
        fjern_handlere()
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.addCleanup(fjern_handlere)

    @override_settings(KI_MAKS_PER_DOGN=1)
    def test_logglinje_format_uten_personopplysninger(self):
        with override_settings(BASE_DIR=Path(self.tmp.name), VERCEL=False):
            BegrensetKi(FalskKi("x"), {}).begrunnelse(SOK, TUR, "r")
            for h in logg.logger.handlers:
                h.flush()
            fil = Path(self.tmp.name) / "logs" / "ki.log"
            linjer = fil.read_text(encoding="utf-8").split("\n")[:-1]
        self.assertEqual(len(linjer), 1)
        tid, kalltype, arsak, svar = linjer[0].split("\t")
        self.assertIsNotNone(datetime.fromisoformat(tid).utcoffset())
        self.assertEqual((kalltype, arsak, svar), ("", "totalgrense", ""))


class MigrasjonTest(SimpleTestCase):
    databases = {"default"}

    def test_ingen_manglende_migrasjoner(self):
        call_command("makemigrations", "--check", "--dry-run", verbosity=0)
