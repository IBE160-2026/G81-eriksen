"""Søket bruker nivåtaket og historikken (story 3.2, FR-5, FR-19, FR-17, NFR-8, SM-C1)."""

from datetime import date
from unittest import mock

from django.test import Client, TestCase

from tests.web.test_registrering import PASSORD
from tests.web.testturer import lagre_testturer
from turforslag.models import Bruker, Registrering

I_DAG = date(2026, 11, 27)
SOK = {"varighet": "300", "dato": I_DAG.isoformat(), "turtype": "", "startpunkt": ""}


class NivaSokBase(TestCase):
    def setUp(self):
        lagre_testturer()
        self.ola = Bruker.objects.create_user("ola@eksempel.no", PASSORD)
        self.client.force_login(self.ola)
        patcher = mock.patch("django.utils.timezone.localdate", return_value=I_DAG)
        patcher.start()
        self.addCleanup(patcher.stop)

    def lag(self, bruker, tur_id, vanskelighet="lett", dag=1, fornoydhet=4):
        return Registrering.objects.create(
            bruker=bruker,
            tur_id=tur_id,
            dato=date(2026, 10, dag),
            brukt_tid_min=110,
            vanskelighet=vanskelighet,
            fornoydhet=fornoydhet,
        )

    def blatt_grunnniva(self, bruker=None):
        """Tre lette grønne turer: grunnnivå blått, én heving."""
        for dag in (1, 2, 3):
            self.lag(bruker or self.ola, "marka-lang", dag=dag)

    def sok(self, klient=None, **endringer):
        klient = klient or self.client
        svar = klient.post("/", {**SOK, **endringer})
        sok_id = svar["Location"].rstrip("/").split("/")[-1] if svar.status_code == 302 else None
        tilstand = klient.session.get("sok", {}).get(sok_id)
        return svar, sok_id, tilstand

    def brukt(self, bruker=None):
        return Bruker.objects.get(pk=(bruker or self.ola).pk).brukt_heving


class GjestTest(NivaSokBase):
    def test_gjest_har_gront_tak_uten_lagring(self):  # FR-19, FR-18
        gjest = Client()
        _, _, tilstand = self.sok(gjest)
        self.assertEqual(tilstand["nivatak"], "gronn")
        self.assertIs(tilstand["nivaheving"], False)
        self.assertNotIn("bla-marka", tilstand["rangerte_tur_ider"])
        self.assertEqual(self.brukt(), 0)


class InnloggetTest(NivaSokBase):
    def test_uten_historikk_gront_tak(self):  # FR-18
        _, _, tilstand = self.sok()
        self.assertEqual(tilstand["nivatak"], "gronn")
        self.assertIs(tilstand["nivaheving"], False)
        self.assertEqual(self.brukt(), 0)

    def test_blatt_grunnniva_gir_bla_turer_og_heving_en_gang(self):  # FR-19, AD-11
        self.blatt_grunnniva()
        _, _, forste = self.sok()
        self.assertEqual(forste["nivatak"], "bla")
        self.assertIs(forste["nivaheving"], True)
        self.assertEqual(forste["rangerte_tur_ider"][0], "bla-marka")
        self.assertEqual(self.brukt(), 1)
        _, _, andre = self.sok()
        self.assertIs(andre["nivaheving"], False)
        self.assertEqual(self.brukt(), 1)
        # Uten heving rangeres lengst tid først, men gåtte turer sist.
        self.assertEqual(andre["rangerte_tur_ider"][-1], "marka-lang")

    def test_ikke_gatt_foran_gatt(self):  # FR-5 punkt 1
        self.blatt_grunnniva()
        _, _, tilstand = self.sok()
        self.assertEqual(tilstand["rangerte_tur_ider"][-1], "marka-lang")
        self.assertEqual(len(tilstand["rangerte_tur_ider"]), 4)

    def test_aktiv_sperre_gir_sperrenivaet_og_brukt_heving(self):  # FR-19, AD-11
        self.blatt_grunnniva()
        self.lag(self.ola, "bla-marka", "vanskelig", dag=10)
        _, _, tilstand = self.sok()
        self.assertEqual(tilstand["nivatak"], "gronn")
        self.assertIs(tilstand["nivaheving"], False)
        self.assertNotIn("bla-marka", tilstand["rangerte_tur_ider"])
        self.assertEqual(self.brukt(), 1)

    def test_ingen_treff_og_bare_over_nivataket_lagrer_brukt_heving(self):  # FR-19, AD-11
        self.blatt_grunnniva()
        _, _, tilstand = self.sok(varighet="60")
        self.assertEqual(tilstand["status"], "ingen_treff")
        self.assertEqual(self.brukt(), 1)
        Bruker.objects.filter(pk=self.ola.pk).update(brukt_heving=0)
        self.lag(self.ola, "bla-marka", "vanskelig", dag=10)
        _, _, tilstand = self.sok(varighet="210", startpunkt="ovre")
        self.assertEqual(tilstand["status"], "bare_over_nivatak")
        self.assertEqual(self.brukt(), 1)

    def test_fjernet_heving_setter_brukt_heving_ned(self):  # AD-11
        Bruker.objects.filter(pk=self.ola.pk).update(brukt_heving=2)
        _, _, tilstand = self.sok()
        self.assertIs(tilstand["nivaheving"], False)
        self.assertEqual(self.brukt(), 0)

    def test_annen_bruker_er_upavirket(self):  # NFR-8
        kari = Bruker.objects.create_user("kari@eksempel.no", PASSORD)
        self.blatt_grunnniva(kari)
        _, _, tilstand = self.sok()
        self.assertEqual(tilstand["nivatak"], "gronn")
        self.assertEqual(self.brukt(), 0)
        self.assertEqual(self.brukt(kari), 0)

    def test_ugyldig_sok_endrer_ikke_brukt_heving(self):  # AD-11
        self.blatt_grunnniva()
        svar = self.client.post("/", {**SOK, "varighet": ""})
        self.assertEqual(svar.status_code, 200)
        self.assertEqual(self.brukt(), 0)

    def test_innlasting_nytt_forslag_og_annen_fane_endrer_ingenting(self):  # FR-7, AD-11
        self.blatt_grunnniva()
        _, sok_id, forste = self.sok()
        self.assertEqual(self.brukt(), 1)
        self.lag(self.ola, "bla-marka", "vanskelig", dag=20)  # ny registrering i annen fane
        self.client.get(f"/forslag/{sok_id}/")
        tur = self.client.session["sok"][sok_id]["gjeldende_tur_id"]
        self.client.post(f"/forslag/{sok_id}/nytt/", {"tur": tur})
        etter = self.client.session["sok"][sok_id]
        self.assertEqual(etter["nivatak"], "bla")
        self.assertEqual(etter["rangerte_tur_ider"], forste["rangerte_tur_ider"])
        self.assertIs(etter["nivaheving"], True)
        self.assertEqual(self.brukt(), 1)

    def test_eldre_okt_uten_nivatak_leses(self):  # AD-5
        _, sok_id, _ = self.sok()
        okt = self.client.session
        del okt["sok"][sok_id]["nivatak"]
        okt["sok"] = okt["sok"]
        okt.save()
        self.assertEqual(self.client.get(f"/forslag/{sok_id}/").status_code, 200)

    def test_endringsforslag_regner_ut_pa_nytt_fra_historikken(self):  # FR-8, FR-19
        self.blatt_grunnniva()
        _, sok_id, tilstand = self.sok(varighet="60")
        self.assertEqual(tilstand["status"], "ingen_treff")
        svar = self.client.post(f"/forslag/{sok_id}/endre/", {"felt": "varighet", "verdi": "150"})
        self.assertEqual(svar.status_code, 302)
        ny_id = svar["Location"].rstrip("/").split("/")[-1]
        ny = self.client.session["sok"][ny_id]
        self.assertEqual(ny["nivatak"], "bla")
        self.assertEqual(ny["status"], "treff")


class HistorikkMerknadTest(NivaSokBase):
    def test_merknaden_bruker_nivataket_fra_historikken(self):  # FR-17
        self.blatt_grunnniva()
        r = self.lag(self.ola, "bla-marka", dag=5)
        svar = self.client.get(f"/historikk/{r.id}/")
        self.assertNotContains(svar, "Denne turen er over nivået")

    def test_merknaden_med_aktiv_sperre(self):  # FR-17
        self.blatt_grunnniva()
        r = self.lag(self.ola, "bla-marka", "vanskelig", dag=5)
        svar = self.client.get(f"/historikk/{r.id}/")
        self.assertContains(svar, "Denne turen er over nivået jeg foreslår for deg nå.")
