"""Turforslag: første forslag, statusene og ukjent søke-ID (FR-6, FR-7, FR-8, FR-12, FR-13).

Én test per rad i matrisen i spec 1.9 som gjelder Turforslag, og en test som viser at
views ikke importerer formaterings- eller beregningsfunksjoner (AR-2, SM-2).
"""

import ast
import json
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from unittest import mock

from django.test import TestCase

from tests.web.testturer import TURER, lag_tur, lagre_testturer
from turforslag import turdata
from turforslag.models import Tur

I_DAG = date(2026, 11, 26)  # torsdag
VIEWS = Path(__file__).resolve().parents[2] / "turforslag" / "views.py"


class Rekkefolge(HTMLParser):
    """Starttagger med attributter og all tekst, i DOM-rekkefølgen."""

    def __init__(self):
        super().__init__()
        self.hendelser = []

    def handle_starttag(self, tag, attrs):
        self.hendelser.append(("tag", tag, dict(attrs)))

    def handle_data(self, data):
        if data.strip():
            self.hendelser.append(("tekst", " ".join(data.split()), {}))


def tekster(svar) -> str:
    parser = Rekkefolge()
    parser.feed(svar.content.decode())
    deler = [verdi for slag, verdi, _ in parser.hendelser if slag == "tekst"]
    return "| " + " | ".join(deler) + " |"


@mock.patch("django.utils.timezone.localdate", return_value=I_DAG)
class ForslagTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        lagre_testturer()

    def sok(self, varighet="180", dato="2026-11-28", turtype="", startpunkt=""):
        data = {"varighet": varighet, "dato": dato, "turtype": turtype, "startpunkt": startpunkt}
        svar = self.client.post("/", data)
        self.assertEqual(svar.status_code, 302)
        return svar["Location"]

    # --- Gyldig søk og innholdet i forslaget ---

    def test_forslaget_viser_forste_tur(self, _):  # FR-6, FR-7
        svar = self.client.get(self.sok())
        self.assertEqual(svar.status_code, 200)
        self.assertContains(
            svar, "<title>Rundt Bråtenvann – Turforslag – Your Next Adventure</title>", html=True
        )
        self.assertContains(svar, "<h1", count=1)
        self.assertContains(svar, "Lørdag 28. nov. · 3 t")
        self.assertContains(svar, 'class="nivamerke nivamerke-gronn"')
        self.assertContains(svar, "Grønn – lett")
        self.assertContains(svar, "Rundtur")
        self.assertContains(svar, "Start: Bråten")
        self.assertContains(svar, "3,5 km")
        self.assertContains(svar, "ca. 130")
        self.assertContains(svar, "ca. 2 t 50 min")
        self.assertContains(svar, "(pauser ikke inkludert)")
        self.assertContains(svar, "Begrunnelse fra mal")
        self.assertContains(svar, "Turen tar ca. 2 t 50 min og passer innenfor 3 timer.")
        self.assertNotContains(svar, "som du ba om")  # Alle turtyper: ingen Turtype-treff
        self.assertNotContains(svar, "style=")
        self.assertNotContains(svar, "Nytt forslag")
        self.assertNotContains(svar, "Registrer gjennomført tur")

    def test_dom_rekkefolgen(self, _):  # UX-DR12, EXPERIENCE.md › Turforslag – rekkefølge
        tekst = tekster(self.client.get(self.sok(turtype="utsikt", varighet="150")))
        rekkefolge = [
            "Lørdag 28. nov. · 2,5 t · Utsikt",
            "Endre søk",
            "Åsen utsikt",
            "Grønn – lett",
            "Jeg har beregnet nivået etter Merkehåndbokas mal ut fra lengde og høydemeter. "
            "Terreng og føre er ikke vurdert.",
            "Utsikt – som du ba om",
            "Tur-retur",
            "Start: Åsen",
            "totalt",
            "høydemeter",
            "(pauser ikke inkludert)",
            "Begrunnelse fra mal",
            "Begrunnelse",
            "Turen tar ca. 2 t 20 min og passer innenfor 2,5 timer. Den har utsikt, som du ba om.",
            "Slik lager jeg forslaget",
            "Ruten, tiden og nivået kommer fra Kartverkets turdata og faste formler, ikke fra KI.",
            "Tiden kan bomme med rundt 15 prosent, og nybegynnere bruker ofte lenger tid enn "
            "beregnet.",
        ]
        plasser = [tekst.index(f"| {del_} |") for del_ in rekkefolge]
        self.assertEqual(plasser, sorted(plasser))

    def test_overskrifter_og_forklaringspanel(self, _):  # UX-DR12, UX-DR17
        svar = self.client.get(self.sok())
        self.assertContains(
            svar, '<h1 class="headline-md" tabindex="-1">Rundt Bråtenvann</h1>', html=True
        )
        self.assertContains(
            svar, '<h2 class="eyebrow" id="begrunnelse-tittel">Begrunnelse</h2>', html=True
        )
        self.assertContains(svar, '<details class="forklaringspanel">')
        self.assertNotContains(svar, "<details open")
        self.assertNotContains(svar, "KI tolker ønsket ditt")

    def test_endre_sok_lenker_til_sok_med_id(self, _):  # UX-DR16
        adresse = self.sok()
        sok_id = adresse.split("/")[2]
        self.assertContains(
            self.client.get(adresse), f'<a href="/?sok={sok_id}">Endre søk</a>', html=True
        )

    def test_ut_no_lenke_i_samme_fane(self, _):  # FR-6
        svar = self.client.get(self.sok())
        self.assertContains(
            svar,
            '<a class="ut-no" href="https://ut.no/turforslag/123">Se turen på ut.no'
            '<span aria-hidden="true">&nbsp;↗</span>'
            '<span class="skjult-tekst"> (åpnes på ut.no)</span></a>',
            html=True,
        )
        self.assertNotContains(svar, "target=")

    def test_startpunkt_i_sokeoppsummeringen(self, _):  # UX-DR16
        svar = self.client.get(self.sok(startpunkt="brate"))
        self.assertContains(svar, "Lørdag 28. nov. · 3 t · Bråten")

    # --- Uten URL ---

    def test_uten_url_ingen_ut_no_lenke(self, _):  # FR-6
        svar = self.client.get(self.sok(turtype="utsikt"))
        self.assertContains(svar, "Åsen utsikt")
        self.assertNotContains(svar, "ut.no")

    # --- Ny innlasting og to faner ---

    def test_ny_innlasting_gir_samme_tur(self, _):  # FR-7, AD-5
        adresse = self.sok()
        forste = self.client.get(adresse)
        with mock.patch("turforslag.sokflyt.velg_turer", side_effect=AssertionError("rangert")):
            andre = self.client.get(adresse)
        self.assertEqual(forste.content, andre.content)

    def test_frosset_rangering_tross_ny_tur_som_ville_rangert_forst(self, _):  # FR-7, AD-5
        adresse = self.sok()
        turdata.lagre_turer(
            [lag_tur("ny-forst", "asen", navn="Ny førstetur", estimert_tid_min=180)]
        )
        svar = self.client.get(adresse)
        self.assertContains(svar, "Rundt Bråtenvann")
        self.assertNotContains(svar, "Ny førstetur")

    def test_tur_over_nivataket_etter_ny_lastinn_vises_ikke(self, _):  # SM-C1, FR-7
        adresse = self.sok()
        Tur.objects.filter(id="marka-lang").update(turniva="bla")
        self.assertRedirects(self.client.get(adresse), "/", fetch_redirect_response=False)
        self.assertContains(self.client.get("/"), "Turforslaget er ikke lenger tilgjengelig.")

    def test_tur_over_varigheten_etter_ny_lastinn_vises_ikke(self, _):  # FR-5, FR-7
        adresse = self.sok()
        Tur.objects.filter(id="marka-lang").update(estimert_tid_min=185)
        self.assertRedirects(self.client.get(adresse), "/", fetch_redirect_response=False)
        self.assertContains(self.client.get("/"), "Turforslaget er ikke lenger tilgjengelig.")

    def test_to_faner_har_hvert_sitt_forslag(self, _):  # FR-7, AD-5
        fane_1 = self.sok()
        fane_2 = self.sok(turtype="utsikt")
        self.assertNotEqual(fane_1, fane_2)
        self.assertContains(self.client.get(fane_1), "Rundt Bråtenvann")
        self.assertContains(self.client.get(fane_2), "Åsen utsikt")
        self.assertContains(self.client.get(fane_1), "Rundt Bråtenvann")

    # --- Ukjent ID og slettet tur ---

    def test_ukjent_id_sender_til_sok_med_melding(self, _):  # FR-7, UX-DR21
        svar = self.client.get("/forslag/finnes-ikke/")
        self.assertRedirects(svar, "/", fetch_redirect_response=False)
        sok = self.client.get("/")
        self.assertContains(sok, "Turforslaget er ikke lenger tilgjengelig.")
        self.assertContains(sok, "Søk på nytt for å få et forslag.")
        innhold = sok.content.decode()
        self.assertLess(innhold.index("</h1>"), innhold.index("data-fokus"))
        self.assertLess(innhold.index("data-fokus"), innhold.index("ikke lenger tilgjengelig"))
        self.assertContains(sok, "data-fokus", count=1)
        # Meldingen vises bare én gang.
        self.assertNotContains(self.client.get("/"), "ikke lenger tilgjengelig")

    def test_slettet_tur_gir_som_ukjent_id(self, _):  # FR-7
        adresse = self.sok()
        Tur.objects.filter(id="marka-lang").delete()
        self.assertRedirects(self.client.get(adresse), "/", fetch_redirect_response=False)
        self.assertContains(self.client.get("/"), "Turforslaget er ikke lenger tilgjengelig.")

    def test_post_til_forslaget_er_ikke_lov(self, _):  # PRG: forslaget er bare GET
        self.assertEqual(self.client.post(self.sok()).status_code, 405)

    # --- Statusene (beslutning 2026-11-26, 1A) ---

    def test_topptur_erstattet(self, _):  # FR-8
        svar = self.client.get(self.sok(turtype="topptur", varighet="150"))
        self.assertContains(
            svar, "<title>Åsen utsikt – Turforslag – Your Next Adventure</title>", html=True
        )
        self.assertContains(svar, "Utsikt i stedet for topptur")
        self.assertContains(svar, "Ingen topptur passer søket ditt")
        self.assertContains(svar, 'class="melding melding-advarsel" role="alert"')
        self.assertNotContains(svar, "som du ba om")
        self.assertContains(svar, "Ingen topptur passet, så den har utsikt i stedet.")
        tekst = tekster(svar)
        self.assertLess(
            tekst.index("| Åsen utsikt |"), tekst.index("| Utsikt i stedet for topptur |")
        )
        self.assertLess(
            tekst.index("| Utsikt i stedet for topptur |"),
            tekst.index("| Ingen topptur passer søket ditt |"),
        )
        self.assertLess(
            tekst.index("| Ingen topptur passer søket ditt |"), tekst.index("| Tur-retur |")
        )

    def test_ingen_treff(self, _):  # FR-8
        adresse = self.sok(turtype="topptur", varighet="120")
        svar = self.client.get(adresse)
        self.assertEqual(svar.status_code, 200)
        self.assertContains(
            svar,
            "<title>Jeg fant ingen tur som passer søket ditt – Your Next Adventure</title>",
            html=True,
        )
        self.assertContains(
            svar,
            '<h1 class="headline-lg" tabindex="-1">Jeg fant ingen tur som passer søket ditt</h1>',
            html=True,
        )
        sok_id = adresse.split("/")[2]
        self.assertContains(svar, f'href="/?sok={sok_id}"', count=1)
        self.assertContains(svar, "Endre søk", count=1)
        self.assertContains(svar, "Lørdag 28. nov. · 2 t · Topptur")
        self.assertNotContains(svar, "nivamerke")
        self.assertNotContains(svar, "Begrunnelse")

    def test_bare_over_nivataket(self, _):  # FR-8, SM-C1
        svar = self.client.get(self.sok(varighet="240", startpunkt="ovre"))
        self.assertContains(
            svar, "<title>Ingen grønne turer passer søket – Your Next Adventure</title>", html=True
        )
        self.assertContains(
            svar,
            '<h1 class="headline-lg" tabindex="-1">Ingen grønne turer passer søket</h1>',
            html=True,
        )
        self.assertContains(
            svar,
            "Som ny bruker får du grønne turer. Lag konto og vurder turene dine, så tilpasser jeg "
            "forslagene etter hvordan turene kjentes for deg.",
        )
        self.assertContains(svar, "Lørdag 28. nov. · 4 t · Øvresetra")
        self.assertContains(svar, "Endre søk", count=1)
        self.assertNotContains(svar, "Øvresetra blå")
        self.assertNotContains(svar, "Blå – moderat")

    def test_ingen_tur_over_nivataket_vises_noen_gang(self, _):  # SM-C1
        for varighet in ("60", "210", "300", "720"):
            for startpunkt in ("", "ovre"):
                with self.subTest(varighet=varighet, startpunkt=startpunkt):
                    svar = self.client.get(self.sok(varighet=varighet, startpunkt=startpunkt))
                    self.assertNotContains(svar, "Øvresetra blå")


@mock.patch("django.utils.timezone.localdate", return_value=I_DAG)
class KartTest(TestCase):
    """Kart og «Kartet i tekst» (story 1.10): én test per rad i matrisen i spec 1.10.

    FR-6, AR-10, UX-DR12, UX-DR13, UX-DR15. Berøring, tastatur og fliser sjekkes manuelt.
    """

    @classmethod
    def setUpTestData(cls):
        lagre_testturer()

    def forslag(self, varighet="180", turtype=""):
        data = {"varighet": varighet, "dato": "2026-11-28", "turtype": turtype, "startpunkt": ""}
        adresse = self.client.post("/", data)["Location"]
        return adresse, self.client.get(adresse)

    def tagger(self, svar):
        parser = Rekkefolge()
        parser.feed(svar.content.decode())
        return [(tag, attrs) for slag, tag, attrs in parser.hendelser if slag == "tag"]

    def assert_uten_kart(self, svar, status_code=200):
        for tekst in ("leaflet", "kart.js", 'class="kart', "kart-geojson", "Kartet i tekst"):
            self.assertNotContains(svar, tekst, status_code=status_code)
        skript = [attrs for tag, attrs in self.tagger(svar) if tag == "script"]
        self.assertEqual(len(skript), 1)
        self.assertTrue(skript[0]["src"].endswith("forbedring.js"))

    def test_forslag_med_tur(self, _):  # FR-6, AR-10, UX-DR13
        _, svar = self.forslag()
        tagger = self.tagger(svar)
        flater = [attrs for tag, attrs in tagger if "kart-flate" in attrs.get("class", "")]
        self.assertEqual(len(flater), 1)
        self.assertEqual(flater[0]["tabindex"], "0")
        self.assertEqual(flater[0]["role"], "region")
        self.assertEqual(flater[0]["aria-label"], "Kart over Rundt Bråtenvann")
        # Leaflet og kart.js bare på denne siden, alle med defer, Leaflet før kart.js.
        skript = [attrs["src"] for tag, attrs in tagger if tag == "script" and "src" in attrs]
        self.assertEqual(len(skript), 3)
        self.assertTrue(skript[0].endswith("vendor/leaflet/leaflet.js"))
        self.assertTrue(skript[1].endswith("kart.js"))
        self.assertTrue(skript[2].endswith("forbedring.js"))
        stilark = [attrs["href"] for tag, attrs in tagger if attrs.get("rel") == "stylesheet"]
        self.assertTrue(stilark[1].endswith("vendor/leaflet/leaflet.css"))
        self.assertTrue(stilark[2].endswith("css/side.css"))
        # GeoJSON med json_script: ingen inline-skript som kjøres.
        innhold = svar.content.decode()
        start = innhold.index('<script id="kart-geojson" type="application/json">')
        data = innhold[start:].split(">", 1)[1].split("</script>", 1)[0]
        geojson = json.loads(data)
        self.assertEqual(geojson["geometry"]["type"], "LineString")
        linje = [list(punkt) for punkt in TURER[0].geometry]  # Rundt Bråtenvann
        self.assertEqual(geojson["geometry"]["coordinates"], linje)
        self.assertEqual(geojson["properties"]["start"], linje[0])
        # Kreditering renderes på serveren med understrekede lenker (side.css).
        self.assertContains(
            svar,
            '<p class="kreditering caption">© <a href="https://www.kartverket.no/api-og-data/'
            'vilkar-for-bruk">Kartverket</a> · © <a href="https://www.openstreetmap.org/'
            'copyright" lang="en">OpenStreetMap contributors</a></p>',
            html=True,
        )
        self.assertContains(svar, 'aria-label="Zoom inn"')
        self.assertContains(svar, 'aria-label="Zoom ut"')
        self.assertNotContains(svar, "style=")

    def test_tastaturrekkefolgen(self, _):  # UX-DR13, EXPERIENCE.md › Kart – oppførsel
        _, svar = self.forslag()
        fokuserbare = []
        for tag, attrs in self.tagger(svar):
            klasse = attrs.get("class", "")
            if tag in ("a", "button") and "kart-prov-igjen" not in klasse:
                fokuserbare.append(attrs.get("aria-label") or attrs.get("href") or klasse)
            elif attrs.get("tabindex") == "0":
                fokuserbare.append("kartflaten")
        start = fokuserbare.index("#kartet-i-tekst")
        self.assertEqual(
            fokuserbare[start : start + 8],
            [
                "#kartet-i-tekst",
                "kartflaten",
                "#kartet-i-tekst",  # lenken i meldingen, synlig bare uten JS og ved feil
                "kartlag kart-knapp kart-vis-hele",
                "Zoom inn",
                "Zoom ut",
                "https://www.kartverket.no/api-og-data/vilkar-for-bruk",
                "https://www.openstreetmap.org/copyright",
            ],
        )

    def test_uten_js(self, _):  # UX-DR13, AR-18
        adresse, svar = self.forslag()
        self.assertContains(svar, '<div class="kart no-js" data-kart data-kart-geojson=')
        self.assertContains(
            svar,
            '<p class="melding-tittel">Kartet kunne ikke lastes. Ruten er beskrevet i '
            '"<a href="#kartet-i-tekst">Kartet i tekst</a>".</p>',
            html=True,
        )
        self.assertContains(
            svar,
            f'<a class="knapp-sekundaer kart-prov-igjen-lenke" href="{adresse}">Prøv igjen</a>',
            html=True,
        )
        self.assertContains(svar, 'class="melding melding-info kart-melding" role="status"')
        self.assertContains(svar, "Bruk to fingre for å flytte kartet")

    def test_kartet_i_tekst_rundtur(self, _):  # FR-6, UX-DR15
        _, svar = self.forslag()
        self.assertContains(svar, '<h2 id="kartet-i-tekst">Kartet i tekst</h2>', html=True)
        self.assertContains(
            svar,
            "Rundtur på 3,5 km totalt fra Bråten. Ruten stiger ca. 130 høydemeter, "
            "fra 200 til 260 moh.",
        )

    def test_kartet_i_tekst_tur_retur(self, _):  # FR-3, FR-6, UX-DR15
        _, svar = self.forslag(varighet="150", turtype="utsikt")
        self.assertContains(
            svar,
            "Tur-retur på 3,5 km totalt fra Åsen. Ruten stiger ca. 70 høydemeter, "
            "fra 210 til 270 moh.",
        )

    def test_kartet_i_tekst_sist_og_kartet_etter_nokkeltall(self, _):  # UX-DR12
        tekst = tekster(self.forslag()[1])
        rekkefolge = [
            "(pauser ikke inkludert)",
            "Kartet i tekst",
            "Vis hele ruten",
            "Kartverket",
            "OpenStreetMap contributors",
            "Begrunnelse fra mal",
            "Slik lager jeg forslaget",
        ]
        plasser = [tekst.index(f"| {del_} |") for del_ in rekkefolge]
        self.assertEqual(plasser, sorted(plasser))
        # Kartbeskrivelse står sist i DOM-en (EXPERIENCE.md › Turforslag – rekkefølge, punkt 10).
        self.assertTrue(
            tekst.endswith(
                "| Tiden kan bomme med rundt 15 prosent, og nybegynnere bruker ofte lenger tid "
                "enn beregnet. | Kartet i tekst | Rundtur på 3,5 km totalt fra Bråten. Ruten "
                "stiger ca. 130 høydemeter, fra 200 til 260 moh. |"
            ),
            tekst[-300:],
        )

    def test_tilstandspanel_uten_kart(self, _):  # FR-8, AR-10
        _, svar = self.forslag(varighet="120", turtype="topptur")
        self.assertContains(svar, "Jeg fant ingen tur som passer søket ditt")
        self.assert_uten_kart(svar)

    def test_sok_og_feilsider_uten_leaflet(self, _):  # AR-10, AD-1
        self.assert_uten_kart(self.client.get("/"))
        self.assert_uten_kart(self.client.get("/finnes-ikke/"), status_code=404)


class ViewsLagdelingTest(TestCase):
    def test_views_importerer_ikke_fra_domene(self):  # AR-2, SM-2
        """Views regner, filtrerer og formaterer ingenting selv: ingen import fra `domene`
        og ingen direkte bruk av formatering, utvalg eller turdata."""
        tre = ast.parse(VIEWS.read_text(encoding="utf-8"))
        moduler = []
        navn = []
        for node in ast.walk(tre):
            if isinstance(node, ast.Import):
                moduler += [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                moduler.append(node.module or "")
                navn += [alias.name for alias in node.names]
        for modul in moduler:
            with self.subTest(modul=modul):
                self.assertFalse(modul.split(".")[0] == "domene", modul)
                self.assertNotIn(modul, ("turforslag.turdata", "turforslag.models"))
        for forbudt in ("tekst", "utvalg", "begrunnelse", "turdata", "velg_turer"):
            self.assertNotIn(forbudt, navn)
        self.assertNotRegex(
            VIEWS.read_text(encoding="utf-8"), r"formater_|velg_turer|estimert_tid|objects\."
        )
