"""Registrer gjennomført tur og Historikk (story 2.3, FR-16, FR-17, AD-14, NFR-8)."""

from datetime import date
from unittest import mock

from django.db.models import ProtectedError
from django.test import Client, TestCase

from tests.web.test_grunnoppsett import les_html
from tests.web.testturer import lagre_testturer
from turforslag import engangstoken
from turforslag.models import Bruker, Registrering, Tur

I_DAG = date(2026, 11, 27)
PASSORD = "hemmelig123"
TUR = "marka-lang"
FEIL_TID = "Brukt tid må være mellom 10 minutter og 24 timer"


class RegistreringTestBase(TestCase):
    def setUp(self):
        lagre_testturer()
        self.ola = Bruker.objects.create_user("ola@eksempel.no", PASSORD)
        self.client.force_login(self.ola)
        patcher = mock.patch("django.utils.timezone.localdate", return_value=I_DAG)
        patcher.start()
        self.addCleanup(patcher.stop)

    def adresse(self, tur_id=TUR):
        return f"/registrer/{tur_id}/"

    def token(self, tur_id=TUR):
        svar = self.client.get(self.adresse(tur_id))
        self.assertEqual(svar.status_code, 200)
        return les_html(svar).finn("input", name="token")[0]["value"]

    def data(self, token, **endringer):
        data = {
            "token": token,
            "dato": "2026-11-07",
            "timer": "1",
            "minutter": "50",
            "vanskelighet": "lett",
            "fornoydhet": "5",
        }
        data.update(endringer)
        return data

    def registrer(self, **endringer):
        return self.client.post(self.adresse(), self.data(self.token(), **endringer))


class SkjemaTest(RegistreringTestBase):
    def test_skjema_har_turoppsummering_og_fire_felt(self):  # FR-16, UX-DR27
        svar = self.client.get(self.adresse())
        self.assertContains(svar, "<title>Registrer gjennomført tur: Rundt Bråtenvann")
        self.assertContains(svar, "Rundtur")
        self.assertContains(svar, "3,5 km")
        self.assertContains(svar, "estimert ca. 2 t 50 min")
        self.assertContains(svar, "Alle fire felt er påkrevd.")
        self.assertContains(svar, 'type="date"')
        self.assertContains(svar, 'value="2026-11-27"')
        self.assertContains(svar, 'max="2026-11-27"')
        self.assertContains(svar, "I dag eller tidligere")
        self.assertContains(svar, "<legend", count=3)
        self.assertContains(svar, 'inputmode="numeric"', count=2)
        self.assertContains(svar, "10 min–24 t")
        self.assertContains(svar, "1 = ikke fornøyd, 5 = svært fornøyd")
        self.assertContains(svar, 'type="radio"', count=8)
        self.assertContains(svar, "Registrer gjennomført tur</button>")
        self.assertContains(svar, 'href="/historikk/">Avbryt</a>')
        self.assertNotContains(svar, "autofocus")

    def test_ukjent_tur_gir_404(self):  # FR-16
        self.assertEqual(self.client.get("/registrer/finnes-ikke/").status_code, 404)
        self.assertEqual(self.client.post("/registrer/finnes-ikke/", {}).status_code, 404)

    def test_gjest_sendes_til_logg_inn(self):  # FR-16
        for adresse in (self.adresse(), "/historikk/"):
            with self.subTest(adresse=adresse):
                svar = Client().get(adresse)
                self.assertRedirects(
                    svar, f"/logg-inn/?next={adresse}", fetch_redirect_response=False
                )
        self.assertEqual(Client().post(self.adresse(), self.data("x")).status_code, 302)
        self.assertEqual(Registrering.objects.count(), 0)

    def test_knapp_pa_turforslaget_for_gjest_og_innlogget(self):  # FR-16, FR-14
        soke_data = {"varighet": "180", "dato": I_DAG.isoformat(), "turtype": "", "startpunkt": ""}
        gjest = Client()
        forslag = gjest.post("/", soke_data)["Location"]
        svar = gjest.get(forslag)
        self.assertContains(svar, 'class="knapp-sekundaer" href="/logg-inn/?next=/registrer/')
        self.assertContains(svar, f"&amp;sok={forslag.split('/')[2]}")
        self.assertContains(svar, "Registrer gjennomført tur</a>")
        forslag = self.client.post("/", soke_data)["Location"]
        svar = self.client.get(forslag)
        self.assertContains(svar, 'class="knapp-sekundaer" href="/registrer/')
        self.assertContains(svar, 'class="knapp-primaer" type="submit">Nytt forslag')
        fragment = self.client.get(forslag, headers={"X-Fragment": "1"})
        self.assertContains(fragment, 'href="/registrer/')


class LagringTest(RegistreringTestBase):
    def test_gyldig_registrering_lagres_og_gir_historikk_med_melding(self):  # FR-16
        svar = self.registrer()
        self.assertRedirects(svar, "/historikk/", fetch_redirect_response=False)
        registrering = Registrering.objects.get()
        self.assertEqual(registrering.bruker, self.ola)
        self.assertEqual(registrering.tur_id, TUR)
        self.assertEqual(registrering.dato, date(2026, 11, 7))
        self.assertEqual(registrering.brukt_tid_min, 110)
        self.assertEqual(registrering.vanskelighet, "lett")
        self.assertEqual(registrering.fornoydhet, 5)
        side = self.client.get("/historikk/")
        self.assertContains(side, "Turen er registrert i historikken din.")
        self.assertContains(side, "data-fokus")
        self.assertNotContains(self.client.get("/historikk/"), "Turen er registrert")

    def test_tid_med_bare_timer_eller_bare_minutter(self):  # FR-16
        for timer, minutter, forventet in (
            ("2", "", 120),
            ("", "45", 45),
            ("0", "10", 10),
            ("24", "0", 1440),
            ("", "90", 90),
        ):
            with self.subTest(timer=timer, minutter=minutter):
                self.registrer(timer=timer, minutter=minutter)
                self.assertEqual(Registrering.objects.latest("id").brukt_tid_min, forventet)

    def test_i_dag_og_gammel_dato_er_gyldig(self):  # FR-16
        self.registrer(dato="2026-11-27")
        self.registrer(dato="2019-01-01")
        self.assertEqual(Registrering.objects.count(), 2)

    def assert_feil(self, melding, felt, **endringer):
        token = self.token()
        svar = self.client.post(self.adresse(), self.data(token, **endringer))
        self.assertEqual(svar.status_code, 200)
        self.assertContains(svar, melding)
        self.assertContains(svar, "autofocus", count=1)
        self.assertEqual(Registrering.objects.count(), 0)
        autofokus = [a for a in les_html(svar).finn("input") if "autofocus" in a]
        self.assertEqual(autofokus[0]["name"], felt)
        # Ugyldig skjema beholder tokenet, så det kan rettes og sendes igjen.
        self.assertContains(svar, f'value="{token}"')
        return token

    def test_mangler_felt(self):  # FR-16
        self.assert_feil("Velg datoen du gikk turen", "dato", dato="")
        self.assert_feil(FEIL_TID, "timer", timer="", minutter="")
        self.assert_feil("Velg hvor vanskelig turen føltes", "vanskelighet", vanskelighet="")
        self.assert_feil("Velg hvor fornøyd du var", "fornoydhet", fornoydhet="")

    def test_ugyldige_verdier(self):  # FR-16
        self.assert_feil("Velg datoen du gikk turen", "dato", dato="i går")
        self.assert_feil("Datoen kan ikke være frem i tid", "dato", dato="2026-11-28")
        for dato in ("20261107", "2026-W45-5", "0001-01-01", "1899-12-31", "2026-1-7"):
            with self.subTest(dato=dato):
                self.assert_feil("Velg datoen du gikk turen", "dato", dato=dato)
        for timer, minutter in (("0", "5"), ("24", "1"), ("25", ""), ("", "1441")):
            with self.subTest(timer=timer, minutter=minutter):
                self.assert_feil(FEIL_TID, "timer", timer=timer, minutter=minutter)
        self.assert_feil(FEIL_TID, "timer", timer="abc")
        self.assert_feil(FEIL_TID, "timer", timer="-1", minutter="30")
        self.assert_feil(FEIL_TID, "minutter", timer="1", minutter="x")
        self.assert_feil(FEIL_TID, "timer", timer="9" * 5000)
        self.assert_feil("Velg hvor vanskelig turen føltes", "vanskelighet", vanskelighet="umulig")
        self.assert_feil("Velg hvor fornøyd du var", "fornoydhet", fornoydhet="6")
        self.assert_feil("Velg hvor fornøyd du var", "fornoydhet", fornoydhet="0")

    def test_feilen_star_ved_feltet_og_fokus_gar_til_forste_felt_med_feil(self):  # FR-16
        token = self.token()
        svar = self.client.post(
            self.adresse(), self.data(token, timer="", minutter="", vanskelighet="", fornoydhet="")
        )
        self.assertContains(svar, "autofocus", count=1)
        felt = [a for a in les_html(svar).finn("input") if "autofocus" in a]
        self.assertEqual(felt[0]["name"], "timer")
        self.assertContains(svar, 'class="feltfeil"', count=3)
        self.assertContains(svar, 'aria-invalid="true"')

    def test_rettet_skjema_lagres_med_samme_token(self):  # AD-14
        token = self.assert_feil("Velg hvor fornøyd du var", "fornoydhet", fornoydhet="")
        self.client.post(self.adresse(), self.data(token))
        self.assertEqual(Registrering.objects.count(), 1)

    def test_innsendte_verdier_beholdes_ved_feil(self):  # FR-16
        token = self.token()
        svar = self.client.post(
            self.adresse(), self.data(token, dato="2026-11-01", timer="1", minutter="x")
        )
        self.assertContains(svar, 'value="2026-11-01"')
        self.assertContains(svar, 'name="vanskelighet" value="lett" checked')
        self.assertContains(svar, 'name="fornoydhet" value="5" checked')

    def test_dobbel_innsending_gir_en_registrering(self):  # AD-14, FR-16
        data = self.data(self.token())
        forste = self.client.post(self.adresse(), data)
        andre = self.client.post(self.adresse(), data)
        self.assertRedirects(forste, "/historikk/", fetch_redirect_response=False)
        self.assertRedirects(andre, "/historikk/", fetch_redirect_response=False)
        self.assertEqual(Registrering.objects.count(), 1)

    def test_ukjent_eller_manglende_token_lagrer_ingenting(self):  # AD-14
        self.token()
        for token in ("feil", "", None):
            with self.subTest(token=token):
                data = self.data(token or "")
                if token is None:
                    del data["token"]
                svar = self.client.post(self.adresse(), data)
                self.assertRedirects(svar, "/historikk/", fetch_redirect_response=False)
        self.assertEqual(Registrering.objects.count(), 0)

    def test_token_fra_annen_okt_virker_ikke(self):  # AD-14
        token = self.token()
        annen = Client()
        annen.force_login(self.ola)
        annen.post(self.adresse(), self.data(token))
        self.assertEqual(Registrering.objects.count(), 0)

    def test_to_faner_har_hvert_sitt_token(self):  # AD-14
        forste = self.token()
        andre = self.token(tur_id="utsikt-kort")
        self.assertNotEqual(forste, andre)
        self.client.post(self.adresse(), self.data(forste))
        self.client.post(self.adresse("utsikt-kort"), self.data(andre))
        self.assertEqual(Registrering.objects.count(), 2)

    def test_tur_id_kommer_fra_url(self):  # AR-7
        data = self.data(self.token(tur_id="utsikt-kort"), tur="marka-lang")
        self.client.post(self.adresse("utsikt-kort"), data)
        self.assertEqual(Registrering.objects.get().tur_id, "utsikt-kort")

    def test_tokenet_ligger_utenfor_sok_og_okten_tommes_ikke(self):  # AD-14, AR-7
        soke_data = {"varighet": "180", "dato": I_DAG.isoformat(), "turtype": "", "startpunkt": ""}
        self.client.post("/", soke_data)
        self.token()
        okt = self.client.session
        self.assertIn("sok", okt)
        self.assertEqual(len(okt[engangstoken.NOKKEL]), 1)
        self.assertNotIn(engangstoken.NOKKEL, okt["sok"])

    def test_tokenet_sammenlignes_med_compare_digest(self):  # AD-14
        token = self.token()
        with mock.patch("turforslag.engangstoken.secrets.compare_digest", return_value=False) as m:
            self.client.post(self.adresse(), self.data(token))
        self.assertTrue(m.called)
        self.assertEqual(Registrering.objects.count(), 0)


class HistorikkTest(RegistreringTestBase):
    def lag(self, bruker, tur_id=TUR, dato=date(2026, 11, 7), **endringer):
        data = {"brukt_tid_min": 110, "vanskelighet": "lett", "fornoydhet": 5}
        data.update(endringer)
        return Registrering.objects.create(bruker=bruker, tur_id=tur_id, dato=dato, **data)

    def test_tom_historikk(self):  # FR-17
        svar = self.client.get("/historikk/")
        self.assertContains(svar, "Du har ikke registrert noen turer ennå.")
        self.assertContains(svar, 'href="/">Finn tur</a>')
        self.assertNotContains(svar, "<table")
        self.assertNotContains(svar, "Nye søk prioriterer")

    def test_tabell_med_en_rad(self):  # FR-17, UX-DR28
        self.lag(self.ola)
        svar = self.client.get("/historikk/")
        self.assertContains(svar, '<h1 class="headline-lg" tabindex="-1">Historikk</h1>')
        self.assertContains(svar, 'role="region" aria-label="Historikk" tabindex="0"')
        self.assertContains(svar, "<table")
        for kolonne in ("Tur", "Dato", "Brukt tid", "Opplevd vanskelighet", "Fornøydhet"):
            self.assertContains(svar, f'<th scope="col">{kolonne}</th>')
        self.assertContains(svar, '<span class="skjult-tekst">Handlinger</span>')
        self.assertContains(svar, '<th scope="row">')
        self.assertContains(svar, "Rundt Bråtenvann")
        self.assertContains(svar, "Grønn – lett")
        self.assertContains(svar, "<td>7. nov.</td>")
        self.assertContains(svar, "1 t 50 min")
        self.assertContains(svar, "estimert ca. 2 t 50 min")
        self.assertContains(svar, "<td>Lett</td>")
        self.assertContains(svar, "<td>5 av 5</td>")
        self.assertContains(svar, "Nye søk prioriterer turer du ikke har gått.")
        self.assertNotContains(svar, "Du har ikke registrert")
        self.assertNotContains(svar, "data-fokus")

    def test_bare_egne_rader(self):  # NFR-8
        kari = Bruker.objects.create_user("kari@eksempel.no", PASSORD)
        self.lag(kari, tur_id="utsikt-kort")
        self.lag(self.ola, tur_id="topptur-lang")
        svar = self.client.get("/historikk/")
        self.assertContains(svar, "Åstoppen")
        self.assertNotContains(svar, "Åsen utsikt")
        andre = Client()
        andre.force_login(kari)
        svar = andre.get("/historikk/")
        self.assertContains(svar, "Åsen utsikt")
        self.assertNotContains(svar, "Åstoppen")

    def test_nyeste_forst_og_samme_tur_flere_ganger(self):  # FR-17
        self.lag(self.ola, dato=date(2026, 11, 7), fornoydhet=1)
        self.lag(self.ola, dato=date(2026, 11, 20), fornoydhet=2)
        self.lag(self.ola, dato=date(2026, 11, 7), fornoydhet=3)
        svar = self.client.get("/historikk/")
        self.assertContains(svar, "Rundt Bråtenvann", count=9)  # navn, to lenketillegg per rad
        innhold = svar.content.decode()
        plassering = [innhold.index(f"<td>{n} av 5</td>") for n in (2, 3, 1)]
        self.assertEqual(plassering, sorted(plassering))

    def test_registrering_og_historikk_i_ett_gjennomlop(self):  # FR-16, FR-17
        self.registrer(timer="1", minutter="50")
        side = self.client.get("/historikk/")
        self.assertContains(side, "<td>5 av 5</td>")
        self.assertContains(side, "1 t 50 min")

    def test_menyen_har_historikk_mellom_finn_tur_og_konto(self):  # UX-DR3
        svar = self.client.get("/historikk/")
        menypunkt = les_html(svar).finn("a", **{"class": "menypunkt"})
        self.assertEqual([a["href"] for a in menypunkt], ["/", "/historikk/", "/konto/"])
        self.assertContains(svar, 'href="/historikk/" aria-current="page"')
        self.assertContains(svar, 'aria-current="page"', count=1)
        self.assertNotContains(self.client.get("/konto/"), 'href="/historikk/" aria-current')

    def test_sidene_er_ikke_cachet(self):  # NFR-8
        self.assertIn("no-store", self.client.get("/historikk/")["Cache-Control"])
        self.assertIn("no-store", self.client.get(self.adresse())["Cache-Control"])

    def test_tur_med_registrering_kan_ikke_slettes(self):  # AR-5
        self.lag(self.ola)
        with self.assertRaises(ProtectedError):
            Tur.objects.get(id=TUR).delete()

    def test_bruker_slettes_sammen_med_registreringene(self):  # AD-15
        self.lag(self.ola)
        self.ola.delete()
        self.assertEqual(Registrering.objects.count(), 0)


class HistorikkTurTest(RegistreringTestBase):
    def lag(self, bruker, tur_id=TUR, dato=date(2026, 11, 7), **endringer):
        data = {"brukt_tid_min": 110, "vanskelighet": "lett", "fornoydhet": 5}
        data.update(endringer)
        return Registrering.objects.create(bruker=bruker, tur_id=tur_id, dato=dato, **data)

    def adresse_til(self, registrering):
        return f"/historikk/{registrering.id}/"

    def test_apne_fra_historikk(self):  # FR-17, UX-DR29
        r = self.lag(self.ola, dato=date(2026, 10, 12), fornoydhet=4)
        svar = self.client.get(self.adresse_til(r))
        self.assertEqual(svar.status_code, 200)
        self.assertContains(svar, "<title>Rundt Bråtenvann – Turforslag")
        self.assertContains(svar, "Fra historikken din")
        self.assertContains(svar, "Du gikk denne turen 12. oktober og ga den 4 av 5.")
        self.assertContains(svar, "Begrunnelse fra mal")
        self.assertContains(svar, "Finn en ny tur")
        self.assertContains(svar, 'href="/registrer/marka-lang/">Registrer gjennomført tur</a>')
        self.assertContains(svar, "data-kart")
        self.assertNotContains(svar, "Endre søk")
        self.assertNotContains(svar, "Nytt forslag")
        self.assertNotContains(svar, "som du ba om")
        self.assertNotContains(svar, "Denne turen er over nivået")

    def test_samme_tur_flere_ganger(self):  # FR-17
        a = self.lag(self.ola, dato=date(2026, 10, 12), fornoydhet=4)
        b = self.lag(self.ola, dato=date(2026, 9, 1), fornoydhet=2)
        self.assertContains(self.client.get(self.adresse_til(a)), "12. oktober og ga den 4 av 5")
        self.assertContains(self.client.get(self.adresse_til(b)), "1. september og ga den 2 av 5")

    def test_over_gront_gir_melding_rett_etter_turnavnet(self):  # FR-17
        r = self.lag(self.ola, tur_id="bla-marka")
        svar = self.client.get(self.adresse_til(r))
        self.assertContains(svar, "Denne turen er over nivået jeg foreslår for deg nå.")
        innhold = svar.content.decode()
        self.assertLess(innhold.index("</h1>"), innhold.index("Denne turen er over nivået"))
        self.assertLess(innhold.index("Denne turen er over nivået"), innhold.index('class="niva"'))
        self.assertContains(svar, "Øvresetra blå")

    def test_andres_ukjent_og_gjest(self):  # NFR-8
        kari = Bruker.objects.create_user("kari@eksempel.no", PASSORD)
        andres = self.lag(kari)
        self.assertEqual(self.client.get(self.adresse_til(andres)).status_code, 404)
        self.assertEqual(self.client.get("/historikk/99999/").status_code, 404)
        egen = self.lag(self.ola)
        gjest = Client()
        svar = gjest.get(self.adresse_til(egen))
        self.assertEqual(svar.status_code, 302)
        self.assertIn("/logg-inn/?next=", svar["Location"])

    def test_soketilstand_er_uendret(self):  # FR-7
        self.client.post("/", {"dato": "2026-11-27", "varighet": "300"})
        for_okt = dict(self.client.session).get("sok")
        r = self.lag(self.ola)
        self.client.get(self.adresse_til(r))
        self.assertEqual(dict(self.client.session).get("sok"), for_okt)

    def test_handlinger_i_tabellen(self):  # FR-17, UX-DR28
        r = self.lag(self.ola, dato=date(2026, 11, 7))
        svar = self.client.get("/historikk/")
        self.assertContains(svar, f'href="/historikk/{r.id}/">Åpne som turforslag')
        self.assertContains(svar, 'href="/registrer/marka-lang/">Registrer gjennomført tur')
        self.assertContains(
            svar, '<span class="skjult-tekst"> – Rundt Bråtenvann, 7. nov.</span>', count=2
        )


class KravOmKontoTest(TestCase):  # FR-14, AD-6, AR-8, NFR-8, UX-DR26
    def setUp(self):
        lagre_testturer()
        self.ola = Bruker.objects.create_user("ola@eksempel.no", PASSORD)
        self.gjest = Client()
        self.sok_id = self.gjest.post(
            "/", {"varighet": "180", "dato": "2026-11-27", "turtype": "", "startpunkt": ""}
        )["Location"].split("/")[2]
        self.adresse = f"/logg-inn/?next=/registrer/{TUR}/&sok={self.sok_id}"

    def test_knappen_peker_til_logg_inn_med_next_og_sok(self):
        svar = self.gjest.get(f"/forslag/{self.sok_id}/")
        tur = svar.context["visning"].tur.id
        self.assertContains(svar, f'href="/logg-inn/?next=/registrer/{tur}/&amp;sok={self.sok_id}"')

    def test_logg_inn_viser_oppsummering_og_tilbake(self):
        for side in ("/logg-inn/", "/lag-konto/"):
            with self.subTest(side=side):
                svar = self.gjest.get(self.adresse.replace("/logg-inn/", side))
                self.assertContains(svar, "Logg inn for å registrere")
                self.assertContains(svar, "Rundt Bråtenvann")
                self.assertContains(svar, "Turforslaget er tatt vare på.")
                self.assertContains(
                    svar, f'href="/forslag/{self.sok_id}/">Tilbake til turforslaget'
                )
                self.assertContains(svar, f'name="sok" value="{self.sok_id}"')
                self.assertContains(svar, "next=/registrer/marka-lang/&amp;sok=" + self.sok_id)

    def test_ukjent_sok_gir_ingen_tatt_vare_pa(self):
        for sok in ("finnes-ikke", ""):
            svar = self.gjest.get(f"/logg-inn/?next=/registrer/{TUR}/&sok={sok}")
            self.assertContains(svar, "Logg inn for å registrere")
            self.assertNotContains(svar, "tatt vare på")
            self.assertNotContains(svar, "Tilbake til turforslaget")
            self.assertNotContains(svar, 'name="sok"')

    def test_ukjent_tur_og_vanlig_logg_inn_uten_oppsummering(self):
        for adresse in ("/logg-inn/?next=/registrer/finnes-ikke/", "/logg-inn/?next=/historikk/"):
            svar = self.gjest.get(adresse)
            self.assertNotContains(svar, "Logg inn for å registrere")
            self.assertNotContains(svar, "turoppsummering")

    def test_logg_inn_herfra_gar_til_registreringen_med_samme_forslag(self):
        for_okt = dict(self.gjest.session).get("sok")
        svar = self.gjest.post(
            "/logg-inn/",
            {
                "epost": "ola@eksempel.no",
                "passord": PASSORD,
                "next": f"/registrer/{TUR}/",
                "sok": self.sok_id,
            },
        )
        self.assertRedirects(svar, f"/registrer/{TUR}/", fetch_redirect_response=False)
        self.assertEqual(dict(self.gjest.session).get("sok"), for_okt)

    def test_feil_innlogging_bevarer_next_og_sok(self):
        svar = self.gjest.post(
            "/logg-inn/",
            {
                "epost": "ola@eksempel.no",
                "passord": "feil",
                "next": f"/registrer/{TUR}/",
                "sok": self.sok_id,
            },
        )
        self.assertContains(svar, "Turforslaget er tatt vare på.")
        self.assertContains(svar, f'name="sok" value="{self.sok_id}"')

    def test_lag_konto_herfra_gar_til_registreringen(self):
        svar = self.gjest.post(
            "/lag-konto/",
            {
                "epost": "ny@eksempel.no",
                "passord": PASSORD,
                "next": f"/registrer/{TUR}/",
                "sok": self.sok_id,
            },
        )
        self.assertRedirects(svar, f"/registrer/{TUR}/", fetch_redirect_response=False)
        self.assertTrue(Bruker.objects.filter(email="ny@eksempel.no").exists())

    def test_direkte_til_registrering_og_historikk(self):
        svar = self.gjest.get(f"/registrer/{TUR}/", follow=True)
        self.assertContains(svar, "Logg inn for å registrere")
        self.assertNotContains(svar, "tatt vare på")
        svar = self.gjest.post(
            "/logg-inn/",
            {"epost": "ola@eksempel.no", "passord": PASSORD, "next": "/historikk/"},
        )
        self.assertRedirects(svar, "/historikk/", fetch_redirect_response=False)

    def test_ekstern_next_gir_sok(self):
        svar = Client().post(
            "/logg-inn/",
            {"epost": "ola@eksempel.no", "passord": PASSORD, "next": "https://annet.no/"},
        )
        self.assertRedirects(svar, "/", fetch_redirect_response=False)

    def test_utlopt_innlogging_sendes_til_logg_inn_med_next(self):
        self.client.force_login(self.ola)
        self.client.logout()
        svar = self.client.get("/konto/")
        self.assertRedirects(svar, "/logg-inn/?next=/konto/", fetch_redirect_response=False)
