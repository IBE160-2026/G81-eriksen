"""Konto: Lag konto, Logg inn, Konto og Logg ut (story 2.1, FR-14, AR-9, NFR-5, NFR-8)."""

from datetime import date, timedelta
from unittest import mock

from django.test import Client, TestCase
from django.utils import timezone

from tests.web.test_grunnoppsett import ROT, les_html
from tests.web.testturer import lagre_testturer
from turforslag.models import Bruker, Innloggingsforsok, Registrering, Tur

EPOST = "ola@eksempel.no"
PASSORD = "hemmelig123"
I_DAG = date(2026, 11, 26)


class KontoTest(TestCase):
    def logg_inn(self, epost=EPOST, passord=PASSORD):
        return self.client.post("/logg-inn/", {"epost": epost, "passord": passord})

    def lag_ola(self):
        return Bruker.objects.create_user(EPOST, PASSORD)

    def er_innlogget(self, klient=None):
        return "_auth_user_id" in (klient or self.client).session

    def test_logg_inn_skjema(self):  # UX-DR26
        svar = self.client.get("/logg-inn/")
        self.assertContains(svar, 'type="email"')
        self.assertContains(svar, 'autocomplete="email"')
        self.assertContains(svar, 'autocomplete="current-password"')
        self.assertContains(svar, "novalidate")
        self.assertContains(svar, "Logg inn</button>")
        self.assertContains(svar, "Har du ikke konto?")
        self.assertContains(svar, 'href="/lag-konto/"')

    def test_lag_konto_skjema(self):  # UX-DR26
        svar = self.client.get("/lag-konto/")
        self.assertContains(svar, 'autocomplete="new-password"')
        self.assertContains(svar, "Minst 8 tegn")
        self.assertContains(svar, "Lag konto og fortsett</button>")

    def test_lag_konto_lagrer_epost_med_sma_bokstaver_og_logger_inn(self):  # FR-14, AR-9
        svar = self.client.post("/lag-konto/", {"epost": "  Ola@Eksempel.NO ", "passord": PASSORD})
        self.assertRedirects(svar, "/", fetch_redirect_response=False)
        bruker = Bruker.objects.get()
        self.assertEqual(bruker.email, EPOST)
        self.assertNotEqual(bruker.password, PASSORD)
        self.assertTrue(bruker.check_password(PASSORD))
        self.assertTrue(self.er_innlogget())

    def test_lag_konto_sender_til_next(self):  # NFR-8
        data = {"epost": EPOST, "passord": PASSORD, "next": "/konto/"}
        svar = self.client.post("/lag-konto/", data)
        self.assertRedirects(svar, "/konto/", fetch_redirect_response=False)

    def test_duplikat_lager_ingen_konto(self):  # FR-14
        self.lag_ola()
        data = {"epost": "OLA@eksempel.no", "passord": "annet12345"}
        svar = self.client.post("/lag-konto/", data)
        self.assertEqual(svar.status_code, 200)
        self.assertContains(svar, "Kunne ikke lage konto – prøv å logge inn")
        self.assertEqual(Bruker.objects.count(), 1)
        self.assertTrue(Bruker.objects.get().check_password(PASSORD))
        self.assertFalse(self.er_innlogget())

    def test_ugyldige_felt_gir_feil_ved_feltet(self):  # FR-14
        ugyldig_epost = "E-postadressen må ha med @, for eksempel ola@eksempel.no"
        for epost, passord, feil in (
            ("", PASSORD, "Skriv inn e-postadressen din"),
            ("ola.eksempel.no", PASSORD, ugyldig_epost),
            (EPOST, "kort", "Passordet må ha minst 8 tegn"),
            (EPOST, "", "Passordet må ha minst 8 tegn"),
        ):
            with self.subTest(epost=epost, passord=passord):
                svar = self.client.post("/lag-konto/", {"epost": epost, "passord": passord})
                self.assertEqual(svar.status_code, 200)
                self.assertContains(svar, feil)
                self.assertContains(svar, 'aria-invalid="true"')
                self.assertEqual(Bruker.objects.count(), 0)
        svar = self.client.post("/lag-konto/", {"epost": EPOST, "passord": "kort"})
        self.assertContains(svar, f'value="{EPOST}"')
        self.assertNotContains(svar, 'value="kort"')

    def test_logg_inn_med_annen_case(self):  # FR-14
        self.lag_ola()
        svar = self.logg_inn(epost="OLA@Eksempel.no")
        self.assertRedirects(svar, "/", fetch_redirect_response=False)
        self.assertTrue(self.er_innlogget())

    def test_feil_innlogging_sier_ikke_hvilket_felt(self):  # FR-14
        self.lag_ola()
        for epost, passord in ((EPOST, "feil-passord"), ("annen@eksempel.no", PASSORD), ("", "")):
            with self.subTest(epost=epost):
                svar = self.logg_inn(epost, passord)
                self.assertEqual(svar.status_code, 200)
                self.assertContains(svar, "Feil e-post eller passord")
                self.assertNotContains(svar, "aria-invalid")
                self.assertFalse(self.er_innlogget())
        svar = self.logg_inn(EPOST, "feil-passord")
        self.assertContains(svar, f'value="{EPOST}"')
        self.assertNotContains(svar, "feil-passord")

    def test_next_til_annet_nettsted_gir_sok(self):  # NFR-8, AR-8
        self.lag_ola()
        for neste in ("https://annet.no/", "//annet.no/", "javascript:alert(1)"):
            with self.subTest(neste=neste):
                data = {"epost": EPOST, "passord": PASSORD, "next": neste}
                svar = Client().post("/logg-inn/", data)
                self.assertRedirects(svar, "/", fetch_redirect_response=False)
        data = {"epost": "ny@eksempel.no", "passord": PASSORD, "next": "https://annet.no/"}
        svar = Client().post("/lag-konto/", data)
        self.assertRedirects(svar, "/", fetch_redirect_response=False)

    def test_next_til_egen_side_virker(self):  # NFR-8
        self.lag_ola()
        data = {"epost": EPOST, "passord": PASSORD, "next": "/konto/"}
        svar = self.client.post("/logg-inn/", data)
        self.assertRedirects(svar, "/konto/", fetch_redirect_response=False)

    def test_next_bevares_bare_nar_den_er_trygg(self):  # NFR-8
        svar = self.client.get("/logg-inn/?next=/konto/")
        self.assertContains(svar, '<input type="hidden" name="next" value="/konto/">', html=True)
        self.assertContains(svar, 'href="/lag-konto/?next=/konto/"')
        svar = self.client.get("/logg-inn/?next=https://annet.no/")
        self.assertNotContains(svar, "annet.no")

    def test_innlogget_pa_logg_inn_og_lag_konto_sendes_til_sok(self):  # FR-14
        self.lag_ola()
        self.logg_inn()
        for adresse in ("/logg-inn/", "/lag-konto/"):
            self.assertRedirects(self.client.get(adresse), "/", fetch_redirect_response=False)

    def test_konto_som_gjest_sendes_til_logg_inn(self):  # FR-14
        svar = self.client.get("/konto/")
        self.assertRedirects(svar, "/logg-inn/?next=/konto/", fetch_redirect_response=False)

    def test_konto_viser_epost_personvern_og_logg_ut(self):  # NFR-5, UX-DR30
        self.lag_ola()
        self.logg_inn()
        svar = self.client.get("/konto/")
        self.assertContains(svar, EPOST)
        self.assertContains(svar, '<h2 class="headline-lg">Personvern</h2>', html=True)
        self.assertContains(svar, "Jeg lagrer bare e-postadressen din")
        skjema = [s for s in les_html(svar).finn("form") if s.get("action") == "/logg-ut/"]
        self.assertEqual(len(skjema), 1)
        self.assertEqual(skjema[0]["method"], "post")
        self.assertContains(svar, "Logg ut</button>")

    def test_logg_ut_er_post_og_gir_melding_med_fokus(self):  # AD-6
        self.lag_ola()
        self.logg_inn()
        self.assertEqual(self.client.get("/logg-ut/").status_code, 405)
        self.assertTrue(self.er_innlogget())
        svar = self.client.post("/logg-ut/")
        self.assertRedirects(svar, "/", fetch_redirect_response=False)
        self.assertFalse(self.er_innlogget())
        side = self.client.get("/")
        self.assertContains(side, "Du er logget ut.")
        self.assertContains(side, "data-fokus")
        self.assertNotContains(self.client.get("/"), "Du er logget ut.")

    def test_toppmeny_gjest_og_innlogget(self):  # UX-DR3
        gjest = les_html(self.client.get("/"))
        menypunkt = gjest.finn("a", **{"class": "menypunkt"})
        self.assertEqual([a["href"] for a in menypunkt], ["/logg-inn/"])
        self.lag_ola()
        self.logg_inn()
        svar = self.client.get("/")
        innlogget = les_html(svar)
        menypunkt = innlogget.finn("a", **{"class": "menypunkt"})
        self.assertEqual([a["href"] for a in menypunkt], ["/", "/historikk/", "/konto/"])
        self.assertContains(svar, ">Finn tur</a>")
        self.assertNotContains(svar, ">Logg inn</a>")
        self.assertEqual(svar.content.decode().count('aria-current="page"'), 1)
        self.assertIsNone(innlogget.finn("a", **{"class": "logo"})[0].get("aria-current"))
        self.assertContains(self.client.get("/konto/"), 'href="/konto/" aria-current="page"')

    def test_logg_inn_er_aktivt_menypunkt_for_gjest(self):  # UX-DR3
        self.assertContains(self.client.get("/logg-inn/"), 'href="/logg-inn/" aria-current="page"')

    @mock.patch("django.utils.timezone.localdate", return_value=I_DAG)
    def test_turforslag_beholdes_gjennom_innlogging_og_oppretting(self, _):  # NFR-6, AR-7
        lagre_testturer()
        self.lag_ola()
        soke_data = {
            "varighet": "180",
            "dato": I_DAG.isoformat(),
            "turtype": "",
            "startpunkt": "",
        }
        innlogginger = (
            ("/logg-inn/", {"epost": EPOST, "passord": PASSORD}),
            ("/lag-konto/", {"epost": "ny@eksempel.no", "passord": PASSORD}),
        )
        for adresse, data in innlogginger:
            with self.subTest(adresse=adresse):
                klient = Client()
                forslag = klient.post("/", soke_data)["Location"]
                for_ = klient.get(forslag)
                self.assertEqual(for_.status_code, 200)
                klient.post(adresse, data)
                self.assertTrue(self.er_innlogget(klient))
                etter = klient.get(forslag)
                self.assertEqual(etter.status_code, 200)
                self.assertEqual(
                    [etter.context["visning"].tur.id, etter.context["sok_id"]],
                    [for_.context["visning"].tur.id, for_.context["sok_id"]],
                )

    def test_for_lange_felt_gir_feil_ikke_krasj(self):  # NFR-2
        svar = self.client.post("/lag-konto/", {"epost": EPOST, "passord": "x" * 129})
        self.assertContains(svar, "Passordet kan ha høyst 128 tegn")
        self.assertEqual(Bruker.objects.count(), 0)
        svar = self.logg_inn(EPOST, "x" * 129)
        self.assertContains(svar, "Feil e-post eller passord")

    def test_kontosidene_caches_ikke(self):  # NFR-5
        for adresse in ("/logg-inn/", "/lag-konto/"):
            with self.subTest(adresse=adresse):
                self.assertIn("no-store", self.client.get(adresse)["Cache-Control"])
        self.lag_ola()
        self.logg_inn()
        self.assertIn("no-store", self.client.get("/konto/")["Cache-Control"])

    def test_logg_ut_uten_innlogging_gir_ingen_melding(self):  # AD-6
        svar = self.client.post("/logg-ut/")
        self.assertRedirects(svar, "/", fetch_redirect_response=False)
        self.assertNotContains(self.client.get("/"), "Du er logget ut.")

    def test_logg_inn_er_ikke_aktivt_menypunkt_pa_lag_konto(self):  # UX-DR3
        self.assertNotContains(self.client.get("/lag-konto/"), 'aria-current="page"')

    @mock.patch("django.utils.timezone.localdate", return_value=I_DAG)
    def test_nivatakmeldingen_for_innlogget_har_ingen_kontolofte(self, _):  # 1.12
        lagre_testturer()
        data = {"varighet": "240", "dato": "2026-11-28", "turtype": "", "startpunkt": "ovre"}
        gjest = self.client.get(self.client.post("/", data)["Location"])
        self.assertContains(gjest, "Som ny bruker")
        self.lag_ola()
        self.logg_inn()
        svar = self.client.get(self.client.post("/", data)["Location"])
        self.assertContains(svar, "Ingen grønne turer passer søket")
        self.assertContains(svar, "Jeg foreslår bare grønne turer foreløpig.")
        self.assertNotContains(svar, "Som ny bruker")
        self.assertNotContains(svar, "Lag konto")

    def test_vis_passord_ligger_i_forbedring_js(self):  # AR-18
        js = (ROT / "turforslag" / "static" / "forbedring.js").read_text(encoding="utf-8")
        self.assertIn("Vis passord", js)
        self.assertIn('input[type="password"]', js)

    def test_lenke_til_lag_konto_i_nivatakmeldingen_bare_for_gjester(self):  # 1.12
        mal = (ROT / "turforslag" / "templates" / "turforslag" / "_tilstandspanel.html").read_text(
            encoding="utf-8"
        )
        self.assertIn("user.is_authenticated", mal)
        self.assertIn("Lag konto</a>", mal)


SPERRE = "Det har vært for mange forsøk på å logge inn med denne e-postadressen. Vent 15 minutter"


class InnloggingsgrenseTest(TestCase):  # NFR-8, AR-9
    def logg_inn(self, epost=EPOST, passord=PASSORD):
        return self.client.post("/logg-inn/", {"epost": epost, "passord": passord})

    def feil_forsok(self, antall, epost=EPOST):
        for _ in range(antall):
            self.logg_inn(epost, "feil-passord")

    def antall(self, epost=EPOST):
        return Innloggingsforsok.objects.filter(epost=epost).count()

    def setUp(self):
        Bruker.objects.create_user(EPOST, PASSORD)

    def test_forste_feil_lagres_med_sma_bokstaver(self):
        svar = self.logg_inn("OLA@Eksempel.no", "feil-passord")
        self.assertContains(svar, "Feil e-post eller passord")
        self.assertEqual(self.antall(), 1)

    def test_ukjent_epost_lagres(self):
        svar = self.logg_inn("ukjent@eksempel.no", "x")
        self.assertContains(svar, "Feil e-post eller passord")
        self.assertEqual(self.antall("ukjent@eksempel.no"), 1)

    def test_femte_feil_gir_vanlig_melding_sjette_sperres(self):
        self.feil_forsok(4)
        svar = self.logg_inn(EPOST, "feil-passord")
        self.assertContains(svar, "Feil e-post eller passord")
        self.assertEqual(self.antall(), 5)
        with mock.patch("turforslag.views.authenticate") as auth:
            svar = self.logg_inn(EPOST, "feil-passord")
            auth.assert_not_called()
        self.assertEqual(svar.status_code, 200)
        self.assertContains(svar, SPERRE)
        self.assertContains(svar, f'value="{EPOST}"')
        self.assertNotContains(svar, "feil-passord")
        self.assertEqual(self.antall(), 5)

    def test_riktig_passord_mens_sperret_logger_ikke_inn(self):
        self.feil_forsok(5)
        svar = self.logg_inn(EPOST, PASSORD)
        self.assertContains(svar, SPERRE)
        self.assertNotIn("_auth_user_id", self.client.session)
        self.assertEqual(self.antall(), 5)

    def test_sperre_likt_for_ukjent_epost_og_annen_case(self):
        self.feil_forsok(5, "ukjent@eksempel.no")
        self.assertContains(self.logg_inn("Ukjent@Eksempel.no", "x"), SPERRE)
        self.feil_forsok(5, "OLA@eksempel.no")
        self.assertContains(self.logg_inn(EPOST, "x"), SPERRE)
        self.assertEqual(self.antall("ukjent@eksempel.no"), 5)

    def test_sperren_gjelder_ikke_andre_epost(self):
        self.feil_forsok(5)
        self.assertNotContains(self.logg_inn("annen@eksempel.no", "x"), SPERRE)

    def test_sperren_slutter(self):
        self.feil_forsok(5)
        eldste = Innloggingsforsok.objects.order_by("id").first()
        Innloggingsforsok.objects.filter(pk=eldste.pk).update(
            tidspunkt=timezone.now() - timedelta(minutes=15, seconds=1)
        )
        svar = self.logg_inn(EPOST, PASSORD)
        self.assertRedirects(svar, "/", fetch_redirect_response=False)

    def test_vellykket_innlogging_sletter_forsok(self):
        self.feil_forsok(3)
        Innloggingsforsok.objects.create(epost="annen@eksempel.no")
        self.logg_inn()
        self.assertEqual(self.antall(), 0)
        self.assertEqual(self.antall("annen@eksempel.no"), 1)

    def test_ugyldig_skjema_teller_ikke(self):
        self.logg_inn("", "x")
        self.logg_inn("x" * 255, "x")
        self.assertEqual(Innloggingsforsok.objects.count(), 0)

    def test_opprydding_sletter_gamle_forsok_for_alle(self):
        gammel = timezone.now() - timedelta(minutes=16)
        for epost in ("a@eksempel.no", EPOST):
            Innloggingsforsok.objects.create(epost=epost, tidspunkt=gammel)
        self.logg_inn(EPOST, "feil-passord")
        self.assertEqual(Innloggingsforsok.objects.count(), 1)

    def test_innstillinger_kan_senkes(self):
        with self.settings(INNLOGGING_MAKS_FORSOK=2):
            self.feil_forsok(2)
            self.assertContains(self.logg_inn(EPOST, PASSORD), SPERRE)


class KontoSlettingTest(TestCase):  # FR-15, AR-9, NFR-5, NFR-8, UX-DR30
    def setUp(self):
        lagre_testturer()
        self.ola = Bruker.objects.create_user(EPOST, PASSORD)
        self.annen = Bruker.objects.create_user("kari@eksempel.no", PASSORD)
        self.tur = Tur.objects.first()
        for bruker in (self.ola, self.annen):
            Registrering.objects.create(
                bruker=bruker,
                tur=self.tur,
                dato=I_DAG,
                brukt_tid_min=60,
                vanskelighet="lett",
                fornoydhet=4,
            )
        self.client.post("/logg-inn/", {"epost": EPOST, "passord": PASSORD})
        Innloggingsforsok.objects.create(epost=EPOST, tidspunkt=timezone.now())
        Innloggingsforsok.objects.create(epost="kari@eksempel.no", tidspunkt=timezone.now())

    def test_konto_har_slettelenke_under_logg_ut(self):
        svar = self.client.get("/konto/")
        self.assertContains(svar, 'href="/konto/slett/"')
        self.assertContains(svar, "Slett konto</a>")
        html = svar.content.decode()
        self.assertLess(html.index("Logg ut</button>"), html.index("Slett konto</a>"))

    def test_bekreftelsessiden_og_get_endrer_ingenting(self):
        svar = self.client.get("/konto/slett/")
        self.assertContains(svar, "Vil du slette kontoen?")
        self.assertContains(svar, "All historikken din slettes for godt, og det kan ikke angres.")
        self.assertContains(svar, "Slett kontoen</button>")
        self.assertContains(svar, 'href="/konto/"')
        self.assertContains(svar, "Avbryt</a>")
        self.assertContains(svar, 'aria-current="page"')
        self.assertNotContains(svar, 'type="email"')
        self.assertNotContains(svar, 'type="password"')
        self.assertIn("no-store", svar["Cache-Control"])
        self.assertTrue(Bruker.objects.filter(email=EPOST).exists())
        self.assertEqual(Registrering.objects.count(), 2)

    def test_gjest_sendes_til_logg_inn(self):
        klient = Client()
        svar = klient.get("/konto/slett/")
        self.assertRedirects(svar, "/logg-inn/?next=/konto/slett/", fetch_redirect_response=False)

    def test_sletting_fjerner_egne_data_og_bare_egne(self):
        svar = self.client.post("/konto/slett/")
        self.assertRedirects(svar, "/", fetch_redirect_response=False)
        self.assertFalse(Bruker.objects.filter(email=EPOST).exists())
        self.assertFalse(Registrering.objects.filter(bruker__email=EPOST).exists())
        self.assertEqual(Innloggingsforsok.objects.filter(epost=EPOST).count(), 0)
        self.assertTrue(Bruker.objects.filter(email="kari@eksempel.no").exists())
        self.assertEqual(Registrering.objects.count(), 1)
        self.assertEqual(Innloggingsforsok.objects.count(), 1)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_kvittering_med_fokus_bare_en_gang(self):
        self.client.post("/konto/slett/")
        side = self.client.get("/")
        self.assertContains(side, "Kontoen din er slettet.")
        self.assertContains(side, "data-fokus", count=1)
        self.assertNotContains(self.client.get("/"), "Kontoen din er slettet.")

    def test_dobbel_post_gir_stille_redirect(self):
        self.client.post("/konto/slett/")
        self.client.get("/")
        svar = self.client.post("/konto/slett/")
        self.assertRedirects(svar, "/", fetch_redirect_response=False)
        self.assertNotContains(self.client.get("/"), "Kontoen din er slettet.")

    def test_feil_i_transaksjonen_ruller_tilbake(self):
        with mock.patch.object(Bruker, "delete", side_effect=RuntimeError("feil")):
            svar = self.client.post("/konto/slett/")
        self.assertEqual(svar.status_code, 200)
        self.assertContains(svar, "Kontoen ble ikke slettet. Prøv igjen.")
        self.assertContains(svar, "Slett kontoen</button>")
        self.assertTrue(Bruker.objects.filter(email=EPOST).exists())
        self.assertEqual(Registrering.objects.count(), 2)
        self.assertEqual(Innloggingsforsok.objects.filter(epost=EPOST).count(), 1)
        self.assertIn("_auth_user_id", self.client.session)
