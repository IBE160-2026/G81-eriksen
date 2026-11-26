"""Søk: skjemaet, valideringen på serveren og søketilstanden i økten (FR-4, FR-5, AD-5, NFR-2).

Én test per rad i matrisen i spec 1.9 som gjelder Søk. Dagens dato er låst til
torsdag 26. november 2026 med `timezone.localdate`.
"""

import re
from datetime import date
from html.parser import HTMLParser
from unittest import mock

from django.test import TestCase

from tests.web.testturer import lagre_testturer
from turforslag import okt

I_DAG = date(2026, 11, 26)


class Skjema(HTMLParser):
    """Samler `select` med valg, radioknapper, feilmeldinger og alle starttagger."""

    def __init__(self):
        super().__init__()
        self.tagger = []
        self.selects = {}
        self.radio = []
        self._select = None
        self._option = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tagger.append((tag, attrs))
        if tag == "select":
            self._select = attrs["name"]
            self.selects[self._select] = {"attrs": attrs, "valg": []}
        elif tag == "option" and self._select:
            self._option = {"verdi": attrs.get("value"), "valgt": "selected" in attrs, "tekst": ""}
            self.selects[self._select]["valg"].append(self._option)
        elif tag == "input" and attrs.get("type") == "radio":
            self.radio.append(attrs)

    def handle_endtag(self, tag):
        if tag == "select":
            self._select = None
        elif tag == "option":
            self._option = None

    def handle_data(self, data):
        if self._option is not None:
            self._option["tekst"] += data

    def valgt(self, navn):
        return [v["verdi"] for v in self.selects[navn]["valg"] if v["valgt"]]

    def med_autofocus(self):
        return [attrs for _, attrs in self.tagger if "autofocus" in attrs]


def les(svar) -> Skjema:
    skjema = Skjema()
    skjema.feed(svar.content.decode())
    return skjema


def gyldig(**endringer):
    data = {"varighet": "180", "dato": I_DAG.isoformat(), "turtype": "", "startpunkt": ""}
    data.update(endringer)
    return data


@mock.patch("django.utils.timezone.localdate", return_value=I_DAG)
class SokTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        lagre_testturer()

    # --- Første visning ---

    def test_forste_visning(self, _):  # FR-4, UX-DR6
        svar = self.client.get("/")
        self.assertEqual(svar.status_code, 200)
        self.assertContains(
            svar, '<h1 class="display" tabindex="-1">Hvor lang tid har du?</h1>', html=True
        )
        self.assertContains(svar, "Fyll inn varighet og dato, så får du ett turforslag om gangen.")
        skjema = les(svar)

        varighet = skjema.selects["varighet"]["valg"]
        self.assertEqual(varighet[0], {"verdi": "", "valgt": True, "tekst": "Velg"})
        self.assertEqual(len(varighet) - 1, 23)
        self.assertEqual(varighet[1]["tekst"], "1 t")
        self.assertEqual(varighet[2]["tekst"], "1,5 t")
        self.assertEqual(varighet[-1], {"verdi": "720", "valgt": False, "tekst": "12 t"})

        datoer = skjema.selects["dato"]["valg"]
        self.assertEqual(len(datoer), 31)
        self.assertEqual(
            datoer[0], {"verdi": "2026-11-26", "valgt": True, "tekst": "Torsdag 26. november"}
        )
        self.assertEqual(datoer[-1]["verdi"], "2026-12-26")

        self.assertEqual(
            [(r["value"], "checked" in r) for r in skjema.radio],
            [("", True), ("marka", False), ("utsikt", False), ("topptur", False)],
        )
        self.assertEqual({r["name"] for r in skjema.radio}, {"turtype"})

        startpunkter = skjema.selects["startpunkt"]["valg"]
        self.assertEqual(
            [(v["verdi"], v["tekst"]) for v in startpunkter],
            [("", "Alle startpunkt"), ("brate", "Bråten"), ("ovre", "Øvresetra"), ("asen", "Åsen")],
        )
        self.assertContains(svar, "Jeg har foreløpig bare turer i Oslo-området.")
        self.assertEqual(skjema.med_autofocus(), [])

    def test_feltene_star_i_rekkefolgen_fra_design(self, _):  # DESIGN.md › Søk
        innhold = self.client.get("/").content.decode()
        plasser = [
            innhold.index(tekst)
            for tekst in ('name="varighet"', 'name="dato"', 'name="turtype"', 'name="startpunkt"')
        ]
        self.assertEqual(plasser, sorted(plasser))
        self.assertLess(innhold.index("<legend"), innhold.index('name="turtype"'))

    def test_ingen_fritekst_og_ingen_style(self, _):  # FR-4 (Epic 1), AR-17
        svar = self.client.get("/")
        self.assertNotContains(svar, "<textarea")
        self.assertNotContains(svar, "Fritekst")
        self.assertNotContains(svar, "style=")
        self.assertNotContains(svar, "<script>")

    def test_hjelpetekstene_er_koblet_til_feltene(self, _):  # NFR-4
        skjema = les(self.client.get("/"))
        self.assertEqual(skjema.selects["varighet"]["attrs"]["aria-describedby"], "varighet-hint")
        self.assertEqual(skjema.selects["dato"]["attrs"]["aria-describedby"], "dato-hint")
        self.assertEqual(
            skjema.selects["startpunkt"]["attrs"]["aria-describedby"], "startpunkt-hint"
        )

    # --- Mangler varighet ---

    def test_mangler_varighet(self, _):  # FR-4, NFR-2
        svar = self.client.post("/", gyldig(varighet=""))
        self.assertEqual(svar.status_code, 200)
        self.assertContains(svar, "Velg varighet")
        skjema = les(svar)
        varighet = skjema.selects["varighet"]["attrs"]
        self.assertEqual(varighet["aria-invalid"], "true")
        self.assertEqual(varighet["aria-describedby"], "varighet-feil varighet-hint")
        self.assertEqual(skjema.med_autofocus(), [varighet])
        feil = [attrs for tag, attrs in skjema.tagger if attrs.get("id") == "varighet-feil"]
        self.assertEqual(len(feil), 1)
        self.assertIn("feltfeil", feil[0]["class"])
        self.assertEqual(self.client.session.get("sok"), None)

    def test_feilen_star_mellom_feltet_og_hjelpeteksten(self, _):  # UX-DR10
        innhold = self.client.post("/", gyldig(varighet="")).content.decode()
        self.assertLess(innhold.index('name="varighet"'), innhold.index('id="varighet-feil"'))
        self.assertLess(innhold.index('id="varighet-feil"'), innhold.index('id="varighet-hint"'))

    def test_utfylte_felt_beholdes_ved_feil(self, _):  # NFR-2
        skjema = les(
            self.client.post("/", gyldig(varighet="", turtype="utsikt", startpunkt="asen"))
        )
        self.assertEqual(skjema.valgt("startpunkt"), ["asen"])
        self.assertEqual([r["value"] for r in skjema.radio if "checked" in r], ["utsikt"])

    # --- Manipulert POST ---

    def test_manipulert_post_gir_feil_ved_riktig_felt(self, _):  # NFR-2, FR-4
        tilfeller = [
            ("dato", "2026-11-25", "Velg en dato fra i dag til 26. desember"),
            ("dato", "2026-12-27", "Velg en dato fra i dag til 26. desember"),
            ("dato", "i-morgen", "Velg en dato fra i dag til 26. desember"),
            ("turtype", "fjell", "Velg en turtype fra listen"),
            ("startpunkt", "ukjent", "Velg et startpunkt fra listen"),
            ("startpunkt", "uten-turer", "Velg et startpunkt fra listen"),
            ("varighet", "45", "Velg varighet"),
            ("varighet", "750", "Velg varighet"),
            ("varighet", "abc", "Velg varighet"),
        ]
        for felt, verdi, melding in tilfeller:
            with self.subTest(felt=felt, verdi=verdi):
                svar = self.client.post("/", gyldig(**{felt: verdi}))
                self.assertEqual(svar.status_code, 200)
                self.assertContains(svar, f'id="{felt}-feil"')
                self.assertContains(svar, melding)
                self.assertContains(svar, 'class="feltfeil"', count=1)
                self.assertEqual(self.client.session.get("sok"), None)

    def test_manipulert_turtype_gir_fokus_og_aria_pa_radiogruppen(self, _):  # NFR-2, NFR-4
        skjema = les(self.client.post("/", gyldig(turtype="fjell")))
        self.assertTrue(all(r.get("aria-invalid") == "true" for r in skjema.radio))
        self.assertTrue(all(r.get("aria-describedby") == "turtype-feil" for r in skjema.radio))
        fokus = skjema.med_autofocus()
        self.assertEqual(len(fokus), 1)
        self.assertEqual((fokus[0]["name"], fokus[0]["value"]), ("turtype", ""))

    def test_tom_og_rar_post_krasjer_ikke(self, _):  # NFR-2
        for data in ({}, {"varighet": ["60", "90"]}, {"dato": ""}, {"turtype": "x" * 5000}):
            with self.subTest(data=str(data)[:40]):
                self.assertEqual(self.client.post("/", data).status_code, 200)

    def test_forste_ugyldige_felt_far_autofocus(self, _):  # UX-DR10
        skjema = les(self.client.post("/", gyldig(dato="1999-01-01", startpunkt="ukjent")))
        self.assertEqual(skjema.med_autofocus(), [skjema.selects["dato"]["attrs"]])

    # --- Gyldig søk ---

    def test_gyldig_sok_sender_til_forslaget(self, _):  # FR-5, AD-5
        svar = self.client.post("/", gyldig())
        self.assertEqual(svar.status_code, 302)
        sok_id = re.fullmatch(r"/forslag/([\w-]+)/", svar["Location"]).group(1)
        self.assertGreaterEqual(len(sok_id), 16)
        lagret = self.client.session["sok"]
        self.assertEqual(list(lagret), [sok_id])
        self.assertEqual(lagret[sok_id]["sok"]["dato"], "2026-11-26")
        self.assertEqual(lagret[sok_id]["sok"]["varighet_min"], 180)
        self.assertEqual(lagret[sok_id]["rangerte_tur_ider"], ["marka-lang", "utsikt-kort"])
        self.assertEqual(lagret[sok_id]["gjeldende_tur_id"], "marka-lang")
        self.assertEqual(lagret[sok_id]["viste_tur_ider"], ["marka-lang"])
        self.assertNotIn("180", svar["Location"])

    def test_samme_sok_to_ganger_gir_to_ider(self, _):  # AD-5
        forste = self.client.post("/", gyldig())["Location"]
        andre = self.client.post("/", gyldig())["Location"]
        self.assertNotEqual(forste, andre)
        self.assertEqual(len(self.client.session["sok"]), 2)

    # --- Elleve søk ---

    def test_elleve_sok_beholder_de_ti_nyeste(self, _):  # AD-5, AR-7
        adresser = [self.client.post("/", gyldig())["Location"] for _ in range(11)]
        ider = [adresse.split("/")[2] for adresse in adresser]
        self.assertEqual(list(self.client.session["sok"]), ider[1:])
        self.assertRedirects(self.client.get(adresser[0]), "/", fetch_redirect_response=False)
        self.assertEqual(self.client.get(adresser[1]).status_code, 200)

    # --- Endre søk ---

    def test_endre_sok_fyller_ut_skjemaet(self, _):  # FR-4, UX-DR16
        data = gyldig(varighet="150", dato="2026-11-28", turtype="utsikt", startpunkt="asen")
        sok_id = self.client.post("/", data)["Location"].split("/")[2]
        skjema = les(self.client.get(f"/?sok={sok_id}"))
        self.assertEqual(skjema.valgt("varighet"), ["150"])
        self.assertEqual(skjema.valgt("dato"), ["2026-11-28"])
        self.assertEqual(skjema.valgt("startpunkt"), ["asen"])
        self.assertEqual([r["value"] for r in skjema.radio if "checked" in r], ["utsikt"])
        self.assertEqual(skjema.med_autofocus(), [])

    def test_endre_sok_med_ukjent_id_gir_tomt_skjema(self, _):  # FR-4
        svar = self.client.get("/?sok=finnes-ikke")
        self.assertEqual(svar.status_code, 200)
        skjema = les(svar)
        self.assertEqual(skjema.valgt("varighet"), [""])
        self.assertEqual(skjema.valgt("dato"), ["2026-11-26"])
        self.assertNotContains(svar, "feltfeil")
        self.assertNotContains(svar, "ikke lenger tilgjengelig")

    def test_endre_sok_med_dato_som_er_passert_gir_i_dag(self, _):  # FR-4
        sok_id = self.client.post("/", gyldig(dato="2026-11-27"))["Location"].split("/")[2]
        with mock.patch("django.utils.timezone.localdate", return_value=date(2026, 11, 28)):
            skjema = les(self.client.get(f"/?sok={sok_id}"))
        self.assertEqual(skjema.valgt("dato"), ["2026-11-28"])
        self.assertEqual(skjema.valgt("varighet"), ["180"])

    # --- Økten ---

    def test_okten_toemmes_aldri(self, _):  # AD-5
        with (
            mock.patch("django.contrib.sessions.backends.base.SessionBase.flush") as flush,
            mock.patch("django.contrib.sessions.backends.base.SessionBase.cycle_key") as cycle,
            mock.patch("django.contrib.sessions.backends.base.SessionBase.clear") as clear,
        ):
            adresse = self.client.post("/", gyldig())["Location"]
            self.client.get(adresse)
            self.client.get("/forslag/finnes-ikke/")
        flush.assert_not_called()
        cycle.assert_not_called()
        clear.assert_not_called()

    def test_ugyldig_verdi_i_okten_gir_ukjent_id(self, _):  # AD-5
        okt_ = self.client.session
        okt_["sok"] = {"rar": {"sok": {"varighet_min": 7}}, "tekst": "ikke en ordbok"}
        okt_.save()
        with self.assertLogs("turforslag.okt", "WARNING"):
            self.assertRedirects(
                self.client.get("/forslag/rar/"), "/", fetch_redirect_response=False
            )
        self.assertRedirects(self.client.get("/forslag/tekst/"), "/", fetch_redirect_response=False)

    def test_nyeste_10(self, _):  # AR-7
        sokene = {str(n): n for n in range(12)}
        self.assertEqual(list(okt.nyeste_10(sokene)), [str(n) for n in range(2, 12)])
