"""KI skriver begrunnelsen: flyten fra første visning til lagring (story 4.5).

Gjelder FR-12 (begrunnelsen lages og lagres), FR-13 (reserve ved feil), NFR-5 (ingen
personopplysninger til KI) og NFR-8 (KI-tekst escapes). Bare `FalskKi`, `mock` og falsk
transport brukes, aldri nøkkel eller nettverk.
"""

import json
import tempfile
from dataclasses import replace
from datetime import date
from pathlib import Path
from unittest import mock

import httpx2
from django.test import TestCase, override_settings

from domene.begrunnelse import reservebegrunnelse
from domene.ki import KiSok, KiSvar, KiTur
from domene.okt import lagret_begrunnelse
from domene.sok import Sok
from domene.utvalg import Status
from tests.tjenester.test_ki_logg import fjern_handlere
from tests.web.testturer import lagre_testturer
from tjenester.ki import logg
from tjenester.ki.ekte import EkteKi
from tjenester.ki.falsk import FalskKi
from turforslag import okt, sokflyt, turdata
from turforslag.models import Bruker, Registrering

I_DAG = date(2026, 11, 26)
GYLDIG = "Fin tur for {varighet}."
FERDIG = "Fin tur for 3 timer."
MERKE_KI = "Skrevet med KI"
MERKE_MAL = "Begrunnelse fra mal"


class FlytBase(TestCase):
    @classmethod
    def setUpTestData(cls):
        lagre_testturer()

    def setUp(self):
        p = mock.patch("django.utils.timezone.localdate", return_value=I_DAG)
        p.start()
        self.addCleanup(p.stop)
        p = mock.patch("turforslag.sokflyt.logg_forkastet")
        self.logg = p.start()
        self.addCleanup(p.stop)

    def sok(self, varighet="180", turtype="", startpunkt=""):
        data = {
            "varighet": varighet,
            "dato": "2026-11-28",
            "turtype": turtype,
            "startpunkt": startpunkt,
        }
        svar = self.client.post("/", data)
        self.assertEqual(svar.status_code, 302)
        return svar["Location"]

    def hent(self, adresse, falsk, **extra):
        with mock.patch("turforslag.sokflyt.hent_ki", return_value=falsk):
            return self.client.get(adresse, **extra)

    def sok_id(self, adresse):
        return adresse.rstrip("/").split("/")[-1]

    def lagret(self, adresse):
        class Foresporsel:
            session = self.client.session

        return okt.hent_sok(Foresporsel, self.sok_id(adresse))

    def nytt(self, adresse):
        t = self.lagret(adresse)
        return self.client.post(adresse + "nytt/", {"tur": t.gjeldende_tur_id})


class GodkjentSvarTest(FlytBase):
    def test_godkjent_svar_vises_med_ki_merke_og_lagres(self):  # FR-12, FR-13
        adresse = self.sok()
        falsk = FalskKi(GYLDIG)
        svar = self.hent(adresse, falsk)
        self.assertContains(svar, FERDIG)
        self.assertContains(svar, '<span aria-hidden="true">✦ </span>Skrevet med KI')
        self.assertNotContains(svar, MERKE_MAL)
        self.assertEqual(falsk.antall_kall, 1)
        self.assertFalse(self.logg.called)
        t = self.lagret(adresse)
        b = lagret_begrunnelse(t, t.gjeldende_tur_id)
        self.assertEqual((b.tekst, b.ki), (FERDIG, True))

    def test_merket_star_rett_over_begrunnelse(self):  # FR-12
        svar = self.hent(self.sok(), FalskKi(GYLDIG))
        html = svar.content.decode()
        self.assertLess(html.index(MERKE_KI), html.index('id="begrunnelse-tittel"'))

    def test_ny_innlasting_og_fragment_kaller_ikke_igjen(self):  # FR-12, AD-10
        adresse = self.sok()
        falsk = FalskKi(GYLDIG)
        self.hent(adresse, falsk)
        svar = self.hent(adresse, falsk)
        fragment = self.hent(adresse, falsk, headers={"X-Fragment": "1"})
        self.assertEqual(falsk.antall_kall, 1)
        for s in (svar, fragment):
            self.assertContains(s, FERDIG)
            self.assertContains(s, MERKE_KI)

    def test_fragmentet_kan_gjore_forste_kallet(self):  # FR-12
        falsk = FalskKi(GYLDIG)
        svar = self.hent(self.sok(), falsk, headers={"X-Fragment": "1"})
        self.assertContains(svar, MERKE_KI)
        self.assertEqual(falsk.antall_kall, 1)

    def test_nytt_forslag_og_forfra_bruker_lagret_tekst(self):  # FR-12, AD-10
        adresse = self.sok(varighet="180")
        falsk = FalskKi(GYLDIG)
        self.hent(adresse, falsk)
        while self.lagret(adresse).gjeldende_tur_id is not None:
            self.nytt(adresse)
            self.hent(adresse, falsk)
        antall = len(self.lagret(adresse).rangerte_tur_ider)
        self.assertEqual(falsk.antall_kall, antall)
        self.assertGreater(antall, 1)
        self.client.post(adresse + "forfra/")
        svar = self.hent(adresse, falsk)
        self.assertEqual(falsk.antall_kall, antall)
        self.assertContains(svar, FERDIG)
        self.assertContains(svar, MERKE_KI)

    def test_html_i_svaret_escapes(self):  # NFR-8
        svar = self.hent(self.sok(), FalskKi("<script>alert</script> {varighet}"))
        self.assertNotContains(svar, "<script>alert")
        self.assertContains(svar, "&lt;script&gt;alert&lt;/script&gt;")


class ReserveTest(FlytBase):
    def assert_reserve(self, adresse, svar):
        self.assertContains(svar, MERKE_MAL)
        self.assertNotContains(svar, MERKE_KI)
        t = self.lagret(adresse)
        b = lagret_begrunnelse(t, t.gjeldende_tur_id)
        self.assertFalse(b.ki)
        tur = turdata.hent_tur(t.gjeldende_tur_id)
        self.assertTrue(b.tekst.startswith(reservebegrunnelse(t.sok, tur)))

    def test_forkastede_svar_gir_reserve_og_logg(self):  # FR-12, FR-13
        eksempler = {
            "2 timer {varighet}": "siffer",
            "to {varighet}": "tallord",
            "{varighet} er en grønn tur": "nivaord",
            "Fin tur": "ugyldig",
            "{varighet} " + "fin " * 100: "for_lang",
            "": "tom",
        }
        for tekst, arsak in eksempler.items():
            with self.subTest(arsak=arsak):
                self.logg.reset_mock()
                self.client = self.client_class()
                adresse = self.sok()
                svar = self.hent(adresse, FalskKi(tekst))
                self.assert_reserve(adresse, svar)
                self.logg.assert_called_once_with("begrunnelse", arsak, tekst)

    def test_feilresultater_gir_reserve_og_logg_uten_svar(self):  # FR-13
        for falsk, arsak in (
            (FalskKi.tidsavbrudd(), "tidsavbrudd"),
            (FalskKi.feil(), "feil"),
            (FalskKi(KiSvar(arsak="ugyldig")), "ugyldig"),
        ):
            with self.subTest(arsak=arsak):
                self.logg.reset_mock()
                self.client = self.client_class()
                adresse = self.sok()
                svar = self.hent(adresse, falsk)
                self.assert_reserve(adresse, svar)
                self.logg.assert_called_once_with("begrunnelse", arsak, None)

    def test_forkastet_svar_kalles_ikke_igjen(self):  # FR-12
        adresse = self.sok()
        falsk = FalskKi.feil()
        self.hent(adresse, falsk)
        svar = self.hent(adresse, falsk)
        self.assertEqual(falsk.antall_kall, 1)
        self.assertContains(svar, MERKE_MAL)

    def test_unntak_fra_ki_og_logg_nar_ikke_viewet(self):  # FR-13
        adresse = self.sok()
        kaster = mock.Mock()
        kaster.begrunnelse.side_effect = RuntimeError("feil")
        self.assertContains(self.hent(adresse, kaster), MERKE_MAL)
        self.client = self.client_class()
        adresse = self.sok()
        self.logg.side_effect = OSError("disk")
        svar = self.hent(adresse, FalskKi("Fin tur"))
        self.assertContains(svar, MERKE_MAL)

    @override_settings(ANTHROPIC_API_KEY="")
    def test_uten_nokkel_reserve_lagres_uten_logg_og_telling(self):  # FR-13
        adresse = self.sok()
        svar = self.client.get(adresse)
        self.assertContains(svar, MERKE_MAL)
        self.assertFalse(self.logg.called)
        self.assertNotIn("ki_kall", self.client.session)
        t = self.lagret(adresse)
        self.assertFalse(lagret_begrunnelse(t, t.gjeldende_tur_id).ki)

    @override_settings(ANTHROPIC_API_KEY="sk-test", KI_MAKS_PER_NETTLESER_TIME=1)
    def test_nadd_grense_gir_reserve_uten_logg(self):  # FR-13, AD-10
        adresse = self.sok(varighet="180")
        with mock.patch.object(EkteKi, "begrunnelse", return_value=KiSvar(tekst=GYLDIG)) as ekte:
            forste = self.client.get(adresse)
            self.nytt(adresse)
            andre = self.client.get(adresse)
        self.assertContains(forste, MERKE_KI)
        self.assertContains(andre, MERKE_MAL)
        self.assertEqual(ekte.call_count, 1)
        self.assertFalse(self.logg.called)


class SendesIkkeTest(FlytBase):
    def test_head_og_post_sender_ikke_kall(self):  # FR-12
        adresse = self.sok()
        falsk = FalskKi(GYLDIG)
        with mock.patch("turforslag.sokflyt.hent_ki", return_value=falsk):
            self.client.head(adresse)
        self.assertEqual(falsk.antall_kall, 0)

    def test_sok_og_nytt_forslag_sender_ikke_kall(self):  # FR-12
        falsk = FalskKi(GYLDIG)
        with mock.patch("turforslag.sokflyt.hent_ki", return_value=falsk):
            adresse = self.sok()
            self.nytt(adresse)
            self.sok(varighet="60")
        self.assertEqual(falsk.antall_kall, 0)

    def test_tilstander_uten_tur_kaller_aldri(self):  # FR-12, AD-10
        falsk = FalskKi(GYLDIG)
        ingen = self.sok(varighet="60")
        self.hent(ingen, falsk)
        self.assertEqual(self.lagret(ingen).status, Status.INGEN_TREFF)
        alle = self.sok(varighet="180")
        while self.lagret(alle).gjeldende_tur_id is not None:
            self.nytt(alle)
        self.hent(alle, falsk)
        self.assertEqual(falsk.antall_kall, 0)

    def test_over_nivatak_kaller_aldri(self):  # FR-8, AD-10
        t = sokflyt.utfor_sok(Sok(varighet_min=180, dato=date(2026, 11, 28)))
        t = replace(t, status=Status.BARE_OVER_NIVATAK, gjeldende_tur_id=None)
        falsk = FalskKi(GYLDIG)
        with mock.patch("turforslag.sokflyt.hent_ki", return_value=falsk):
            self.assertIs(sokflyt.sikre_begrunnelse(t, {}), t)
            sokflyt.forslagsvisning(t)
        self.assertEqual(falsk.antall_kall, 0)

    def test_ukjent_tur_og_tur_som_ikke_passer(self):  # SM-C1
        t = sokflyt.utfor_sok(Sok(varighet_min=180, dato=date(2026, 11, 28)))
        falsk = FalskKi(GYLDIG)
        with mock.patch("turforslag.sokflyt.hent_ki", return_value=falsk):
            borte = replace(t, gjeldende_tur_id="finnes-ikke")
            self.assertIs(sokflyt.sikre_begrunnelse(borte, {}), borte)
            kort = replace(t, sok=replace(t.sok, varighet_min=60))
            self.assertIs(sokflyt.sikre_begrunnelse(kort, {}), kort)
        self.assertEqual(falsk.antall_kall, 0)

    def test_historikk_kaller_aldri(self):  # FR-17, AD-10
        ola = Bruker.objects.create_user("ola@eksempel.no", "hemmelig123")
        r = Registrering.objects.create(
            bruker=ola,
            tur_id="marka-lang",
            dato=date(2026, 11, 7),
            brukt_tid_min=110,
            vanskelighet="lett",
            fornoydhet=5,
        )
        self.client.force_login(ola)
        falsk = FalskKi(GYLDIG)
        with mock.patch("turforslag.sokflyt.hent_ki", return_value=falsk):
            svar = self.client.get(f"/historikk/{r.id}/")
        self.assertContains(svar, MERKE_MAL)
        self.assertNotContains(svar, MERKE_KI)
        self.assertEqual(falsk.antall_kall, 0)

    def test_forslagsvisning_er_ren(self):  # FR-12
        t = sokflyt.utfor_sok(Sok(varighet_min=180, dato=date(2026, 11, 28)))
        falsk = FalskKi(GYLDIG)
        with mock.patch("turforslag.sokflyt.hent_ki", return_value=falsk):
            visning = sokflyt.forslagsvisning(t)
        self.assertEqual(falsk.antall_kall, 0)
        self.assertFalse(visning.tur.skrevet_med_ki)


class GammelOgSkadetTilstandTest(FlytBase):
    def endre_okt(self, adresse, endre):
        sesjon = self.client.session
        endre(sesjon[okt.OKTNOKKEL][self.sok_id(adresse)])
        sesjon.save()

    def test_tilstand_for_4_5_leses_og_far_ett_kall(self):  # NFR-2, AD-5
        adresse = self.sok()
        self.endre_okt(adresse, lambda d: d.pop("begrunnelser", None))
        falsk = FalskKi(GYLDIG)
        svar = self.hent(adresse, falsk)
        self.assertContains(svar, MERKE_KI)
        self.assertEqual(falsk.antall_kall, 1)

    def test_skadet_felt_gir_ikke_ukjent_sok(self):  # NFR-2
        for skadet in ("tekst", [{"tur_id": "x"}, 5, {"tur_id": "x", "tekst": "t", "ki": 1}]):
            with self.subTest(skadet=skadet):
                self.client = self.client_class()
                adresse = self.sok()
                self.endre_okt(adresse, lambda d, s=skadet: d.update(begrunnelser=s))
                falsk = FalskKi(GYLDIG)
                svar = self.hent(adresse, falsk)
                self.assertEqual(svar.status_code, 200)
                self.assertContains(svar, MERKE_KI)
                self.assertEqual(falsk.antall_kall, 1)


class ToppturErstattetTest(FlytBase):
    def test_flagget_sendes_og_utsikt_kreves(self):  # FR-8, FR-12
        adresse = self.sok(varighet="180", turtype="topptur")
        self.assertEqual(self.lagret(adresse).status, Status.TOPPTUR_ERSTATTET)
        falsk = FalskKi("Fin tur for {varighet}")
        svar = self.hent(adresse, falsk)
        self.assertEqual(falsk.kall_topptur_erstattet, [True])
        self.assertContains(svar, MERKE_MAL)
        self.logg.assert_called_once_with("begrunnelse", "turtype", "Fin tur for {varighet}")

    def test_utsikt_i_svaret_godkjennes(self):  # FR-8
        adresse = self.sok(varighet="180", turtype="topptur")
        svar = self.hent(adresse, FalskKi("Utsikt på {varighet}."))
        self.assertContains(svar, MERKE_KI)

    def test_vanlig_sok_sender_false(self):  # FR-12
        falsk = FalskKi(GYLDIG)
        self.hent(self.sok(), falsk)
        self.assertEqual(falsk.kall_topptur_erstattet, [False])


class LostUpdateTest(FlytBase):
    def test_tilstand_endret_under_kallet_rulles_ikke_tilbake(self):  # FR-12, NFR-2
        adresse = self.sok(varighet="180")
        sok_id = self.sok_id(adresse)
        forste = self.lagret(adresse).gjeldende_tur_id
        andre = self.lagret(adresse).rangerte_tur_ider[1]

        class Endrer:
            def begrunnelse(self, sok, tur, reserve, *, topptur_erstattet=False):
                data = dict(self.okt[okt.OKTNOKKEL])
                d = dict(data[sok_id])
                d["gjeldende_tur_id"] = andre
                d["viste_tur_ider"] = [forste, andre]
                data[sok_id] = d
                self.okt[okt.OKTNOKKEL] = data
                return KiSvar(tekst=GYLDIG)

        def hent_ki(tving_reserve=False, okt=None):
            ki = Endrer()
            ki.okt = okt
            return ki

        with mock.patch("turforslag.sokflyt.hent_ki", side_effect=hent_ki):
            svar = self.client.get(adresse)
        self.assertEqual(svar.status_code, 200)
        t = self.lagret(adresse)
        self.assertEqual(t.gjeldende_tur_id, andre)
        self.assertEqual(t.viste_tur_ider, (forste, andre))
        b = lagret_begrunnelse(t, forste)
        self.assertEqual((b.tekst, b.ki), (FERDIG, True))


class PersonvernTest(FlytBase):
    def test_sendt_melding_til_ekte_ki_har_ingen_personopplysninger(self):  # NFR-5
        ola = Bruker.objects.create_user("ola.melding@eksempel.no", "hemmelig123")
        self.client.force_login(ola)
        adresse = self.sok(turtype="marka", startpunkt="brate")
        sendt = []

        def handler(request):
            sendt.append(json.loads(request.content))
            return httpx2.Response(
                200,
                json={
                    "id": "msg_1",
                    "type": "message",
                    "role": "assistant",
                    "model": "claude-haiku-5-5",
                    "content": [{"type": "text", "text": "Marka passer {varighet}."}],
                    "stop_reason": "end_turn",
                    "stop_sequence": None,
                    "usage": {"input_tokens": 1, "output_tokens": 1},
                },
            )

        ki = EkteKi("sk-test", http_client=httpx2.Client(transport=httpx2.MockTransport(handler)))
        svar = self.hent(adresse, ki)
        self.assertContains(svar, MERKE_KI)
        self.assertEqual(len(sendt), 1)
        melding = json.dumps(sendt[0]["messages"], ensure_ascii=False).lower()
        for forbudt in ("@", "ola.melding", "eksempel", self.sok_id(adresse).lower(), "bruker"):
            self.assertNotIn(forbudt, melding)
        self.assertIn("brate", melding)

    def test_bare_sok_og_tur_til_ki(self):  # NFR-5
        ola = Bruker.objects.create_user("ola.personvern@eksempel.no", "hemmelig123")
        Registrering.objects.create(
            bruker=ola,
            tur_id="marka-lang",
            dato=date(2026, 11, 7),
            brukt_tid_min=110,
            vanskelighet="lett",
            fornoydhet=5,
        )
        self.client.force_login(ola)
        adresse = self.sok(turtype="marka", startpunkt="brate")
        falsk = FalskKi(GYLDIG)
        self.hent(adresse, falsk)
        sok, tur, _ = falsk.kall[0]
        self.assertIsInstance(sok, KiSok)
        self.assertIsInstance(tur, KiTur)
        self.assertEqual(sok.startpunkt_id, "brate")
        alt = repr(falsk.kall).lower()
        for forbudt in ("ola.personvern", "@", self.sok_id(adresse).lower(), "nivåtak"):
            self.assertNotIn(forbudt, alt)

    def test_loggfilen_har_ikke_sok_id_eller_epost(self):  # NFR-5, FR-13
        fjern_handlere()
        self.addCleanup(fjern_handlere)
        ola = Bruker.objects.create_user("ola.logg@eksempel.no", "hemmelig123")
        self.client.force_login(ola)
        adresse = self.sok()
        with tempfile.TemporaryDirectory() as mappe:
            with (
                override_settings(BASE_DIR=Path(mappe), VERCEL=False),
                mock.patch.object(sokflyt, "logg_forkastet", logg.logg_forkastet),
            ):
                self.hent(adresse, FalskKi("2 timer {varighet}"))
                for h in logg.logger.handlers:
                    h.flush()
                innhold = (Path(mappe) / "logs" / "ki.log").read_text(encoding="utf-8")
            fjern_handlere()
        self.assertIn("\tbegrunnelse\tsiffer\t", innhold)
        for forbudt in (self.sok_id(adresse), "ola.logg", "@"):
            self.assertNotIn(forbudt, innhold)
