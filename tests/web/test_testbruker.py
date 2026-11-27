"""Testbrukeren viser personaliseringen (story 3.4, FR-21, SM-4, AR-5, AD-11, NFR-2)."""

import json
import tempfile
from datetime import date
from io import StringIO
from pathlib import Path
from unittest import mock

from django.conf import settings
from django.contrib.auth import authenticate
from django.core.management import call_command
from django.core.management.base import CommandError
from django.db import DatabaseError
from django.test import Client, SimpleTestCase, TestCase

from domene import tur as domenetur
from domene.tur import Turniva
from tests.web.test_registrering import PASSORD
from turforslag import testbruker
from turforslag.models import Bruker, Registrering, Tur

ROT = Path(settings.BASE_DIR)
FIL = ROT / "data" / "testbruker.toml"
TURFIL = ROT / "data" / "turer.geojson"
I_DAG = date(2026, 11, 27)
EPOST = "testbruker@example.com"
PASSORD_TEST = "Testbruker2026"
SOK = {"varighet": "240", "dato": I_DAG.isoformat(), "turtype": "", "startpunkt": "ostmarksetra"}


def turer() -> list[domenetur.Tur]:
    data = json.loads(TURFIL.read_text(encoding="utf-8"))
    return [domenetur.Tur.fra_geojson_feature(f) for f in data["features"]]


class FilhistorikkTest(SimpleTestCase):  # Uten database
    def test_fila_gir_bla_grunnniva_ingen_sperre_og_en_heving(self):  # FR-19, FR-21
        alle = turer()
        bruker = testbruker.les_og_valider(FIL, {t.id for t in alle}, I_DAG)
        status = testbruker.historikk(bruker, alle)
        self.assertEqual(status.grunnniva, Turniva.BLA)
        self.assertEqual(status.nivatak, Turniva.BLA)
        self.assertIsNone(status.sperre)
        self.assertEqual(status.antall_hevinger, 1)

    def test_innholdet_i_fila(self):  # AR-5, FR-21
        alle = turer()
        bruker = testbruker.les_og_valider(FIL, {t.id for t in alle}, I_DAG)
        self.assertGreaterEqual(len(bruker.registreringer), 5)
        lette = [r for r in bruker.registreringer if r.vanskelighet == "lett"]
        self.assertEqual(len(lette), 3)
        self.assertEqual(len({r.tur_id for r in lette}), 2)
        self.assertTrue(any(r.fornoydhet <= 2 for r in bruker.registreringer))
        self.assertTrue(all(r.dato < I_DAG for r in bruker.registreringer))
        self.assertEqual(bruker.epost, EPOST)

    def test_hver_registrering_har_kommentar(self):  # AR-5
        blokker = FIL.read_text(encoding="utf-8").split("[[registrering]]")
        for blokk in blokker[:-1]:
            self.assertTrue(blokk.rstrip().splitlines()[-1].startswith("#"))


class LastinnTestbrukerTest(TestCase):
    def setUp(self):
        mappe = tempfile.TemporaryDirectory()
        self.addCleanup(mappe.cleanup)
        self.mappe = Path(mappe.name)
        patcher = mock.patch("django.utils.timezone.localdate", return_value=I_DAG)
        patcher.start()
        self.addCleanup(patcher.stop)

    def lastinn(self, *argumenter):
        ut = StringIO()
        call_command("lastinn", *argumenter, stdout=ut, stderr=StringIO())
        return ut.getvalue()

    def fil_med(self, tekst: str) -> Path:
        sti = self.mappe / "testbruker.toml"
        sti.write_text(tekst, encoding="utf-8")
        return sti

    def registreringer(self):
        return list(
            Registrering.objects.filter(bruker__email=EPOST)
            .order_by("dato", "id")
            .values_list("tur_id", "dato", "brukt_tid_min", "vanskelighet", "fornoydhet")
        )

    def test_forste_kjoring(self):  # FR-21
        ut = self.lastinn()
        bruker = Bruker.objects.get(email=EPOST)
        self.assertEqual(len(self.registreringer()), 5)
        self.assertEqual(bruker.brukt_heving, 0)
        self.assertIn("Gjenskapte testbrukeren", ut)

    def test_passord_er_bare_hash(self):  # NFR-1
        self.lastinn()
        bruker = Bruker.objects.get(email=EPOST)
        self.assertNotIn(PASSORD_TEST, bruker.password)
        self.assertIsNotNone(authenticate(email=EPOST, password=PASSORD_TEST))

    def test_to_kjoringer_gir_en_bruker_med_samme_registreringer(self):  # AC 2
        self.lastinn()
        for_ = self.registreringer()
        self.lastinn()
        self.assertEqual(Bruker.objects.filter(email=EPOST).count(), 1)
        self.assertEqual(self.registreringer(), for_)
        self.assertEqual(Registrering.objects.count(), 5)

    def test_endret_eller_slettet_testbruker_gjenskapes(self):  # AD-11
        self.lastinn()
        bruker = Bruker.objects.get(email=EPOST)
        bruker.brukt_heving = 5
        bruker.save()
        Registrering.objects.filter(bruker=bruker).first().delete()
        self.lastinn()
        self.assertEqual(len(self.registreringer()), 5)
        self.assertEqual(Bruker.objects.get(email=EPOST).brukt_heving, 0)
        Bruker.objects.filter(email=EPOST).delete()
        self.lastinn()
        self.assertEqual(len(self.registreringer()), 5)

    def test_andre_brukere_er_urorte(self):  # AD-11
        self.lastinn()
        ola = Bruker.objects.create_user("ola@eksempel.no", PASSORD)
        Registrering.objects.create(
            bruker=ola,
            tur_id="sognsvann-brekke",
            dato=date(2026, 10, 1),
            brukt_tid_min=50,
            vanskelighet="lett",
            fornoydhet=3,
        )
        self.lastinn()
        self.assertEqual(Registrering.objects.filter(bruker=ola).count(), 1)
        self.assertTrue(Bruker.objects.filter(pk=ola.pk).exists())

    def test_med_fil_uten_testbruker_hoppes_det_over(self):
        self.lastinn("--fil", str(TURFIL))
        self.assertFalse(Bruker.objects.filter(email=EPOST).exists())

    def test_med_fil_og_testbruker_laster_oppgitt_fil(self):
        sti = self.fil_med(FIL.read_text(encoding="utf-8").replace(EPOST, "annen@example.com"))
        self.lastinn("--fil", str(TURFIL), "--testbruker", str(sti))
        self.assertTrue(Bruker.objects.filter(email="annen@example.com").exists())

    def test_ugyldige_filer_endrer_ingenting_heller_ikke_turene(self):  # NFR-2
        ok = FIL.read_text(encoding="utf-8")
        tilfeller = {
            "mangler": None,
            "toml": "dette er ikke = = toml [",
            "epost": ok.replace(EPOST, "ikke-en-epost"),
            "kort passord": ok.replace(PASSORD_TEST, "abc1"),
            "tur-id": ok.replace("sognsvann-brekke", "finnes-ikke", 1),
            "frem i tid": ok.replace("2026-08-02", "2026-12-01"),
            "dato": ok.replace("2026-08-02", "2026-13-45"),
            "tid": ok.replace("brukt_tid_min = 45", "brukt_tid_min = 5"),
            "vanskelighet": ok.replace('vanskelighet = "lett"', 'vanskelighet = "svaer"', 1),
            "fornoydhet": ok.replace("fornoydhet = 4", "fornoydhet = 6", 1),
            "felt": ok.replace("fornoydhet = 4\n", "", 1),
        }
        for navn, innhold in tilfeller.items():
            with self.subTest(navn):
                sti = self.mappe / "mangler.toml" if innhold is None else self.fil_med(innhold)
                with self.assertRaises(CommandError) as feil:
                    self.lastinn("--testbruker", str(sti))
                self.assertIn("Ingenting er endret", str(feil.exception))
                self.assertEqual(Tur.objects.count(), 0)
                self.assertEqual(Bruker.objects.count(), 0)

    def test_feil_i_fila_stopper_for_turene_lagres_og_beholder_testbruker(self):
        self.lastinn()
        sti = self.fil_med(FIL.read_text(encoding="utf-8").replace("2026-08-16", "2026-12-16"))
        with self.assertRaises(CommandError) as feil:
            self.lastinn("--testbruker", str(sti))
        self.assertIn("registrering nr. 2", str(feil.exception))
        self.assertIn("dato", str(feil.exception))
        self.assertEqual(len(self.registreringer()), 5)

    def test_feil_etter_sletting_ruller_alt_tilbake_manglende_tur(self):  # NFR-2
        self.lastinn()
        ola = Bruker.objects.create_user("ola@eksempel.no", PASSORD)
        Registrering.objects.create(
            bruker=ola,
            tur_id="grorud-badedammen",
            dato=date(2026, 10, 1),
            brukt_tid_min=50,
            vanskelighet="lett",
            fornoydhet=3,
        )
        data = json.loads(TURFIL.read_text(encoding="utf-8"))
        data["features"] = [f for f in data["features"] if f["id"] != "grorud-badedammen"]
        turfil = self.mappe / "turer.geojson"
        turfil.write_text(json.dumps(data), encoding="utf-8")
        antall_turer = Tur.objects.count()
        gammel = Bruker.objects.get(email=EPOST).pk
        for_ = self.registreringer()
        with self.assertRaises(CommandError) as feil:
            self.lastinn("--fil", str(turfil), "--testbruker", str(FIL))
        self.assertIn("Ingenting er endret", str(feil.exception))
        self.assertEqual(Bruker.objects.get(email=EPOST).pk, gammel)
        self.assertEqual(self.registreringer(), for_)
        self.assertEqual(Tur.objects.count(), antall_turer)

    def test_databasefeil_etter_sletting_ruller_alt_tilbake(self):  # NFR-2
        self.lastinn()
        gammel = Bruker.objects.get(email=EPOST).pk
        for_ = self.registreringer()
        antall_turer = Tur.objects.count()
        with mock.patch("turforslag.testbruker.opprett", side_effect=DatabaseError("feil")):
            with self.assertRaises(CommandError) as feil:
                self.lastinn()
        self.assertIn("Ingenting er endret", str(feil.exception))
        self.assertEqual(Bruker.objects.get(email=EPOST).pk, gammel)
        self.assertEqual(self.registreringer(), for_)
        self.assertEqual(Tur.objects.count(), antall_turer)


class ReadmeSokTest(TestCase):
    def setUp(self):
        patcher = mock.patch("django.utils.timezone.localdate", return_value=I_DAG)
        patcher.start()
        self.addCleanup(patcher.stop)
        call_command("lastinn", stdout=StringIO(), stderr=StringIO())
        self.klient = Client()
        self.assertTrue(self.klient.login(username=EPOST, password=PASSORD_TEST))

    def sok(self):
        svar = self.klient.post("/", SOK)
        sok_id = svar["Location"].rstrip("/").split("/")[-1]
        return self.klient.session["sok"][sok_id], sok_id

    def test_readme_soket_gir_bla_tur_forst_med_hevingen_en_gang(self):  # FR-21, SM-4
        forste, sok_id = self.sok()
        self.assertEqual(forste["rangerte_tur_ider"][0], "noklevann-rundt")
        self.assertIs(forste["nivaheving"], True)
        self.assertContains(
            self.klient.get(f"/forslag/{sok_id}/"),
            "fordi de tre siste grønne turene var lette for deg",
        )
        self.assertEqual(Bruker.objects.get(email=EPOST).brukt_heving, 1)
        andre, sok_id = self.sok()
        self.assertIs(andre["nivaheving"], False)
        self.assertNotContains(
            self.klient.get(f"/forslag/{sok_id}/"), "de tre siste grønne turene var lette"
        )

    def test_historikk_viser_alle_registreringene(self):  # FR-17
        svar = self.klient.get("/historikk/")
        self.assertEqual(svar.status_code, 200)
        for tur in Tur.objects.filter(registreringer__bruker__email=EPOST).distinct():
            self.assertContains(svar, tur.navn)

    def test_ny_vanskelig_bla_tur_gir_sperresetning(self):  # FR-19, FR-21
        self.sok()
        Registrering.objects.create(
            bruker=Bruker.objects.get(email=EPOST),
            tur_id="noklevann-rundt",
            dato=date(2026, 11, 20),
            brukt_tid_min=200,
            vanskelighet="vanskelig",
            fornoydhet=3,
        )
        tilstand, sok_id = self.sok()
        self.assertEqual(tilstand["nivatak"], "gronn")
        self.assertContains(
            self.klient.get(f"/forslag/{sok_id}/"), "fordi den siste blå turen føltes vanskelig"
        )

    def test_readme_har_innlogging_og_sperre(self):  # AR-20
        readme = (ROT / "README.md").read_text(encoding="utf-8")
        self.assertIn(EPOST, readme)
        self.assertIn(PASSORD_TEST, readme)
        self.assertIn("vanskelig", readme)
