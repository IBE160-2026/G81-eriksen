"""Turforslag: første forslag, statusene og ukjent søke-ID (FR-6, FR-7, FR-8, FR-12, FR-13).

Én test per rad i matrisen i spec 1.9 som gjelder Turforslag, og en test som viser at
views ikke importerer formaterings- eller beregningsfunksjoner (AR-2, SM-2).
"""

import ast
import json
import re
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from unittest import mock

from django.test import Client, TestCase

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


def uten_csrf(svar) -> str:
    return re.sub(r'name="csrfmiddlewaretoken" value="[^"]*"', "", svar.content.decode())


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
        self.assertContains(svar, "Nytt forslag", count=1)  # FR-7 (1.11)
        self.assertNotContains(svar, "Registrer gjennomført tur")  # Epic 2

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
        # CSRF-tokenet i «Nytt forslag» maskeres på nytt for hver visning.
        self.assertEqual(uten_csrf(forste), uten_csrf(andre))

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
                "enn beregnet. | Nytt forslag | Kartet i tekst | Rundtur på 3,5 km totalt fra "
                "Bråten. Ruten stiger ca. 130 høydemeter, fra 200 til 260 moh. |"
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


def csrf_token(svar) -> str:
    return re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', svar.content.decode())[1]


@mock.patch("django.utils.timezone.localdate", return_value=I_DAG)
class NyttForslagTest(TestCase):
    """«Nytt forslag» og «alle vist» (story 1.11): én test per rad i matrisen i spec 1.11.

    FR-7, AR-7, NFR-2, UX-DR19, UX-DR22–25. Fragmentbyttet med JS sjekkes manuelt i Chrome.
    Med 3 t og alle turtyper er det tre treff: de to grønne testturene og «marka-tredje».
    """

    @classmethod
    def setUpTestData(cls):
        lagre_testturer()
        turdata.lagre_turer(
            [lag_tur("marka-tredje", "brate", navn="Tredje marka", estimert_tid_min=100)]
        )

    def sok(self, varighet="180", turtype="", klient=None, **ekstra):
        data = {"varighet": varighet, "dato": "2026-11-28", "turtype": turtype, "startpunkt": ""}
        svar = (klient or self.client).post("/", {**data, **ekstra})
        self.assertEqual(svar.status_code, 302)
        adresse = svar["Location"]
        return adresse, adresse.split("/")[2]

    def tilstand(self, sok_id):
        return self.client.session["sok"][sok_id]

    def nytt(self, adresse, tur, **headers):
        data = {} if tur is None else {"tur": tur}
        return self.client.post(adresse + "nytt/", data, headers=headers)

    def gjennom_alle(self, adresse, sok_id):
        while (gjeldende := self.tilstand(sok_id)["gjeldende_tur_id"]) is not None:
            self.assertRedirects(
                self.nytt(adresse, gjeldende), adresse, fetch_redirect_response=False
            )

    def navn(self, tur_id):
        return turdata.hent_tur(tur_id).navn

    # --- Knappen ---

    def test_knappen_paa_turforslaget(self, _):  # FR-7, UX-DR22, AR-17
        adresse, sok_id = self.sok()
        svar = self.client.get(adresse)
        gjeldende = self.tilstand(sok_id)["gjeldende_tur_id"]
        innhold = svar.content.decode()
        skjema = re.search(r"<form [^>]*data-nytt-forslag[^>]*>(.*?)</form>", innhold, re.S)
        self.assertIsNotNone(skjema)
        self.assertIn('method="post"', skjema[0])
        self.assertIn(f'action="{adresse}nytt/"', skjema[0])
        self.assertIn('data-lastetekst="Finner et nytt forslag …"', skjema[0])
        self.assertIn('name="csrfmiddlewaretoken"', skjema[1])
        self.assertIn(f'<input type="hidden" name="tur" value="{gjeldende}">', skjema[1])
        self.assertIn(
            '<button class="knapp-primaer" type="submit">Nytt forslag</button>', skjema[1]
        )
        # Live-regionen står i <main>, utenfor beholderen som byttes og dempes.
        self.assertContains(
            svar, '<p class="skjult-tekst" aria-live="polite" data-lastestatus></p>', html=True
        )
        self.assertLess(innhold.index("data-lastestatus"), innhold.index('class="forslag"'))
        self.assertIn(
            'class="forslag" data-tittel="Rundt Bråtenvann – Turforslag – Your Next Adventure"',
            innhold,
        )
        # «Kart lastes …» står på kartflaten og er skjult til kart.js viser den (1A).
        self.assertContains(svar, '<p class="kart-lastes" hidden>Kart lastes …</p>', html=True)
        self.assertNotContains(svar, "Finner en tur med")
        self.assertNotContains(svar, "style=")

    # --- Matrisen ---

    def test_neste(self, _):  # FR-7
        adresse, sok_id = self.sok()
        a, b, _c = self.tilstand(sok_id)["rangerte_tur_ider"]
        svar = self.nytt(adresse, a)
        self.assertRedirects(svar, adresse, fetch_redirect_response=False)
        tilstand = self.tilstand(sok_id)
        self.assertEqual(tilstand["gjeldende_tur_id"], b)
        self.assertEqual(tilstand["viste_tur_ider"], [a, b])
        side = self.client.get(adresse)
        self.assertContains(
            side, f"<title>{self.navn(b)} – Turforslag – Your Next Adventure</title>", html=True
        )
        self.assertContains(side, f'<input type="hidden" name="tur" value="{b}">', html=True)

    def test_rekkefolge_uten_gjentakelse(self, _):  # FR-7
        adresse, sok_id = self.sok()
        rangert = self.tilstand(sok_id)["rangerte_tur_ider"]
        viste = []
        with mock.patch("turforslag.sokflyt.velg_turer", side_effect=AssertionError("rangert")):
            while (gjeldende := self.tilstand(sok_id)["gjeldende_tur_id"]) is not None:
                overskrift = f'<h1 class="headline-md" tabindex="-1">{self.navn(gjeldende)}</h1>'
                self.assertContains(self.client.get(adresse), overskrift, html=True)
                viste.append(gjeldende)
                self.nytt(adresse, gjeldende)
        self.assertEqual(viste, rangert)
        self.assertEqual(len(set(viste)), 3)

    def test_siste_gir_alle_vist(self, _):  # FR-7, UX-DR19, NFR-2
        adresse, sok_id = self.sok()
        self.gjennom_alle(adresse, sok_id)
        tilstand = self.tilstand(sok_id)
        self.assertIsNone(tilstand["gjeldende_tur_id"])
        self.assertEqual(sorted(tilstand["viste_tur_ider"]), sorted(tilstand["rangerte_tur_ider"]))
        svar = self.client.get(adresse)
        self.assertEqual(svar.status_code, 200)
        self.assertContains(
            svar,
            "<title>Du har sett alle turene som passer søket – Your Next Adventure</title>",
            html=True,
        )
        self.assertContains(
            svar,
            '<h1 class="headline-lg" tabindex="-1">Du har sett alle turene som passer søket</h1>',
            html=True,
        )
        self.assertContains(svar, "<h1", count=1)
        self.assertContains(
            svar, "<p>Det var tre turer som passer 3 timer. Vil du prøve noe annet?</p>", html=True
        )
        self.assertContains(svar, f'<form method="post" action="{adresse}forfra/">')
        self.assertContains(
            svar,
            '<button class="handlingslenke" type="submit">Start fra første forslag igjen</button>',
            html=True,
        )
        self.assertContains(
            svar, f'<a class="handlingslenke" href="/?sok={sok_id}">Endre søk</a>', html=True
        )
        self.assertContains(svar, "Endre søk", count=1)
        self.assertContains(svar, 'data-tittel="Du har sett alle turene som passer søket – ')
        self.assertNotContains(svar, "Nytt forslag")
        self.assertNotContains(svar, "Turforslaget er ikke lenger tilgjengelig")
        # Panelet har ikke kart.js eller Leaflet.
        for tekst in ("leaflet", "kart.js", 'class="kart', "kart-geojson"):
            self.assertNotContains(svar, tekst)
        self.assertNotContains(svar, "style=")

    def test_dobbeltklikk_gaar_bare_ett_steg(self, _):  # FR-7, NFR-2
        adresse, sok_id = self.sok()
        a, b, _c = self.tilstand(sok_id)["rangerte_tur_ider"]
        self.nytt(adresse, a)
        for _gang in range(2):
            svar = self.nytt(adresse, a)
            self.assertRedirects(svar, adresse, fetch_redirect_response=False)
        tilstand = self.tilstand(sok_id)
        self.assertEqual(tilstand["gjeldende_tur_id"], b)
        self.assertEqual(tilstand["viste_tur_ider"], [a, b])
        self.assertContains(self.client.get(adresse), self.navn(b))

    def test_start_paa_nytt(self, _):  # FR-7
        adresse, sok_id = self.sok()
        a = self.tilstand(sok_id)["rangerte_tur_ider"][0]
        self.gjennom_alle(adresse, sok_id)
        for _gang in range(2):  # dobbeltklikk: andre POST endrer ingenting
            svar = self.client.post(adresse + "forfra/")
            self.assertRedirects(svar, adresse, fetch_redirect_response=False)
            tilstand = self.tilstand(sok_id)
            self.assertEqual(tilstand["gjeldende_tur_id"], a)
            self.assertEqual(tilstand["viste_tur_ider"], [a])
        self.assertContains(
            self.client.get(adresse),
            f"<title>{self.navn(a)} – Turforslag – Your Next Adventure</title>",
            html=True,
        )

    def test_start_paa_nytt_hopper_over_borte_forste_tur(self, _):  # FR-7, SM-C1
        adresse, sok_id = self.sok()
        a, b, _c = self.tilstand(sok_id)["rangerte_tur_ider"]
        self.gjennom_alle(adresse, sok_id)
        Tur.objects.filter(id=a).delete()
        self.client.post(adresse + "forfra/")
        self.assertEqual(self.tilstand(sok_id)["gjeldende_tur_id"], b)
        self.assertEqual(self.tilstand(sok_id)["viste_tur_ider"], [a, b])

    def test_forfra_uten_alle_vist_endrer_ingenting(self, _):  # NFR-2
        adresse, sok_id = self.sok()
        for_ = self.tilstand(sok_id)
        self.assertRedirects(
            self.client.post(adresse + "forfra/"), adresse, fetch_redirect_response=False
        )
        self.assertEqual(self.tilstand(sok_id), for_)

    def test_ny_innlasting_etter_neste(self, _):  # FR-7, AD-5
        adresse, sok_id = self.sok()
        a, b, _c = self.tilstand(sok_id)["rangerte_tur_ider"]
        self.nytt(adresse, a)
        with mock.patch("turforslag.sokflyt.velg_turer", side_effect=AssertionError("rangert")):
            forste = self.client.get(adresse)
            andre = self.client.get(adresse)
        self.assertContains(forste, self.navn(b))
        self.assertEqual(uten_csrf(forste), uten_csrf(andre))
        self.assertEqual(self.tilstand(sok_id)["viste_tur_ider"], [a, b])

    def test_ukjent_sok(self, _):  # FR-7, NFR-2
        for handling in ("nytt/", "forfra/"):
            with self.subTest(handling=handling):
                svar = self.client.post(f"/forslag/finnes-ikke/{handling}", {"tur": "marka-lang"})
                self.assertRedirects(svar, "/", fetch_redirect_response=False)
                self.assertContains(
                    self.client.get("/"), "Turforslaget er ikke lenger tilgjengelig."
                )

    def test_manipulerte_post(self, _):  # NFR-2
        adresse, sok_id = self.sok()
        for_ = self.tilstand(sok_id)
        for tur in (None, "", "finnes-ikke", for_["rangerte_tur_ider"][1], "x" * 5000):
            with self.subTest(tur=tur and tur[:20]):
                svar = self.nytt(adresse, tur)
                self.assertRedirects(svar, adresse, fetch_redirect_response=False)
                self.assertEqual(self.tilstand(sok_id), for_)
        svar = self.client.post(adresse + "nytt/", {"tur": ["a", "b"]})
        self.assertEqual(svar.status_code, 302)
        self.assertEqual(self.tilstand(sok_id), for_)

    def test_get_til_post_adressene_gir_405(self, _):  # PRG, NFR-2
        adresse, _sok_id = self.sok()
        for handling in ("nytt/", "forfra/"):
            with self.subTest(handling=handling):
                self.assertEqual(self.client.get(adresse + handling).status_code, 405)

    def test_borte_tur_hoppes_over(self, _):  # FR-7, SM-C1
        adresse, sok_id = self.sok()
        a, b, c = self.tilstand(sok_id)["rangerte_tur_ider"]
        Tur.objects.filter(id=b).delete()
        self.nytt(adresse, a)
        tilstand = self.tilstand(sok_id)
        self.assertEqual(tilstand["gjeldende_tur_id"], c)
        self.assertEqual(tilstand["viste_tur_ider"], [a, b, c])
        self.assertContains(self.client.get(adresse), self.navn(c))

    def test_tur_som_ikke_lenger_passer_hoppes_over(self, _):  # FR-7, SM-C1
        adresse, sok_id = self.sok()
        a, b, c = self.tilstand(sok_id)["rangerte_tur_ider"]
        Tur.objects.filter(id=b).update(turniva="bla")
        Tur.objects.filter(id=c).update(estimert_tid_min=200)
        self.nytt(adresse, a)
        self.assertIsNone(self.tilstand(sok_id)["gjeldende_tur_id"])
        svar = self.client.get(adresse)
        self.assertContains(svar, "Du har sett alle turene som passer søket")
        # Ingressen teller bare turene som fortsatt passer (bare a).
        self.assertContains(svar, "Det var én tur som passer 3 timer.")

    def test_forfra_naar_alle_turene_er_borte(self, _):  # FR-7, NFR-2
        adresse, sok_id = self.sok()
        rangert = self.tilstand(sok_id)["rangerte_tur_ider"]
        self.gjennom_alle(adresse, sok_id)
        Tur.objects.filter(id__in=rangert).delete()
        svar = self.client.post(adresse + "forfra/")
        self.assertRedirects(svar, adresse, fetch_redirect_response=False)
        tilstand = self.tilstand(sok_id)
        self.assertIsNone(tilstand["gjeldende_tur_id"])
        self.assertEqual(sorted(tilstand["viste_tur_ider"]), sorted(rangert))
        # Ingen turer igjen: ingen panel med «Det var 0 turer», men Søk med meldingen.
        self.assertRedirects(self.client.get(adresse), "/", fetch_redirect_response=False)
        self.assertContains(self.client.get("/"), "Turforslaget er ikke lenger tilgjengelig.")

    def test_forfra_naar_noen_turer_er_borte(self, _):  # FR-7, SM-C1
        adresse, sok_id = self.sok()
        a, b, c = self.tilstand(sok_id)["rangerte_tur_ider"]
        self.gjennom_alle(adresse, sok_id)
        Tur.objects.filter(id__in=[a, b]).delete()
        self.client.post(adresse + "forfra/")
        self.assertEqual(self.tilstand(sok_id)["gjeldende_tur_id"], c)
        self.nytt(adresse, c)
        self.assertContains(self.client.get(adresse), "Det var én tur som passer 3 timer.")

    def test_en_tur(self, _):  # FR-7
        adresse, sok_id = self.sok(varighet="150", turtype="utsikt")
        self.assertEqual(self.tilstand(sok_id)["rangerte_tur_ider"], ["utsikt-kort"])
        self.nytt(adresse, "utsikt-kort")
        self.assertContains(
            self.client.get(adresse), "Det var én tur med utsikt som passer 2,5 timer."
        )

    def test_alle_vist_etter_topptur_erstattet(self, _):  # FR-7, FR-8
        adresse, sok_id = self.sok(varighet="150", turtype="topptur")
        self.assertEqual(self.tilstand(sok_id)["status"], "topptur_erstattet")
        self.nytt(adresse, "utsikt-kort")
        svar = self.client.get(adresse)
        self.assertContains(svar, "Du har sett alle turene som passer søket")
        self.assertContains(svar, "Det var én tur med utsikt som passer 2,5 timer.")

    # --- Fragment ---

    def test_fragment(self, _):  # FR-7, AR-7, UX-DR22–25
        adresse, sok_id = self.sok()
        a, b, _c = self.tilstand(sok_id)["rangerte_tur_ider"]
        svar = self.nytt(adresse, a, x_fragment="1")
        self.assertRedirects(svar, adresse, fetch_redirect_response=False)
        fragment = self.client.get(adresse, headers={"x-fragment": "1"})
        self.assertEqual(fragment.status_code, 200)
        innhold = fragment.content.decode()
        self.assertTrue(
            innhold.lstrip().startswith('<div class="forslag" data-tittel='), innhold[:200]
        )
        for tekst in ("<html", "<head", "<main", "<header", "<title", "data-lastestatus"):
            self.assertNotIn(tekst, innhold)
        self.assertIn(f'data-tittel="{self.navn(b)} – Turforslag – Your Next Adventure"', innhold)
        self.assertIn('<script id="kart-geojson" type="application/json">', innhold)
        self.assertIn("data-nytt-forslag", innhold)
        self.assertIn("X-Fragment", fragment["Vary"])
        # GET uten headeren er uendret: hele siden.
        hel = self.client.get(adresse)
        self.assertContains(hel, "<main>")
        self.assertIn("X-Fragment", hel["Vary"])

    def test_fragment_alle_vist(self, _):  # FR-7, UX-DR19
        adresse, sok_id = self.sok()
        self.gjennom_alle(adresse, sok_id)
        innhold = self.client.get(adresse, headers={"x-fragment": "1"}).content.decode()
        self.assertTrue(
            innhold.lstrip().startswith(
                '<div class="tilstand" data-tittel="Du har sett alle turene som passer søket – '
                'Your Next Adventure">'
            ),
            innhold[:200],
        )
        self.assertNotIn("<main", innhold)

    def test_fragment_ukjent_sok_sender_til_sok(self, _):  # FR-7: forbedring.js sender vanlig
        svar = self.client.get("/forslag/finnes-ikke/", headers={"x-fragment": "1"})
        self.assertRedirects(svar, "/", fetch_redirect_response=False)

    # --- Økten og CSRF ---

    def test_oppdatert_sok_blir_nyeste_av_10(self, _):  # AD-5, AR-7
        adresse, forste = self.sok()
        andre = self.sok(turtype="utsikt")[1]
        self.nytt(adresse, self.tilstand(forste)["gjeldende_tur_id"])
        self.assertEqual(list(self.client.session["sok"])[-1], forste)
        for _gang in range(8):
            self.sok()
        self.nytt(adresse, self.tilstand(forste)["gjeldende_tur_id"])
        self.sok()  # 11. søk: det eldste (andre) faller ut, ikke det oppdaterte
        sokene = self.client.session["sok"]
        self.assertEqual(len(sokene), 10)
        self.assertIn(forste, sokene)
        self.assertNotIn(andre, sokene)

    def test_andre_sok_paavirkes_ikke(self, _):  # FR-7, AD-5
        adresse, forste = self.sok()
        andre = self.sok()[1]
        for_ = self.tilstand(andre)
        self.nytt(adresse, self.tilstand(forste)["gjeldende_tur_id"])
        self.assertEqual(self.tilstand(andre), for_)

    def test_csrf_haandheves(self, _):  # AR-7, PRG
        klient = Client(enforce_csrf_checks=True)
        token = csrf_token(klient.get("/"))
        adresse = self.sok(klient=klient, csrfmiddlewaretoken=token)[0]
        side = klient.get(adresse)
        tur = re.search(r'name="tur" value="([^"]+)"', side.content.decode())[1]
        self.assertEqual(klient.post(adresse + "nytt/", {"tur": tur}).status_code, 403)
        svar = klient.post(adresse + "nytt/", {"tur": tur, "csrfmiddlewaretoken": csrf_token(side)})
        self.assertRedirects(svar, adresse, fetch_redirect_response=False)
        self.assertEqual(klient.post(adresse + "forfra/").status_code, 403)


@mock.patch("django.utils.timezone.localdate", return_value=I_DAG)
class EndringsforslagTest(TestCase):
    """Endringsforslag i Tilstandspanelet (story 1.12): FR-8, UX-DR17, UX-DR22, UX-DR25, SM-C1."""

    @classmethod
    def setUpTestData(cls):
        lagre_testturer()

    def sok(self, varighet, turtype="", startpunkt=""):
        data = {"varighet": varighet, "dato": "2026-11-28", "turtype": turtype}
        data["startpunkt"] = startpunkt
        svar = self.client.post("/", data)
        self.assertEqual(svar.status_code, 302)
        return svar["Location"]

    def tilstand(self, adresse):
        return self.client.session["sok"][adresse.split("/")[2]]

    def endre(self, adresse, felt, verdi):
        return self.client.post(adresse + "endre/", {"felt": felt, "verdi": verdi})

    def vis_alle(self, adresse):
        while (gjeldende := self.tilstand(adresse)["gjeldende_tur_id"]) is not None:
            self.client.post(adresse + "nytt/", {"tur": gjeldende})

    def test_ingen_treff_viser_forslag(self, _):  # FR-8, UX-DR17
        svar = self.client.get(self.sok("120", turtype="topptur"))
        self.assertContains(svar, "Prøv å endre søket:")
        self.assertContains(
            svar, '<button class="handlingslenke" type="submit">Prøv 5 timer</button>', html=True
        )
        self.assertContains(svar, 'name="felt" value="varighet"')
        self.assertContains(svar, 'name="verdi" value="300"')
        self.assertContains(svar, "csrfmiddlewaretoken")
        self.assertContains(svar, "Endre søk", count=1)
        self.assertNotContains(svar, "data-nytt-forslag")

    def test_startpunkt_og_turtype_i_fast_rekkefolge(self, _):  # FR-8
        adresse = self.sok("180", turtype="utsikt", startpunkt="brate")
        svar = self.client.get(adresse)
        sok_id = adresse.split("/")[2]
        self.assertNotContains(svar, "Prøv 3,5 timer")
        self.assertContains(svar, "Velg startpunkt")
        self.assertContains(svar, "Prøv marka")
        tekst = tekster(svar)
        self.assertLess(tekst.index("| Velg startpunkt |"), tekst.index("| Prøv marka |"))
        lenke = f"/?sok={sok_id}&amp;fokus=startpunkt"
        self.assertContains(
            svar, f'<a class="handlingslenke" href="{lenke}">Velg startpunkt</a>', html=True
        )

    def test_uten_forslag_bare_endre_sok(self, _):  # FR-8
        Tur.objects.all().delete()
        svar = self.client.get(self.sok("720"))
        self.assertContains(svar, "Jeg fant ingen tur som passer søket ditt")
        self.assertNotContains(svar, "Prøv å endre søket:")
        self.assertNotContains(svar, 'name="felt"')
        self.assertContains(svar, "Endre søk", count=1)

    def test_trykk_alle_turtyper(self, _):  # FR-8
        Tur.objects.all().delete()
        turdata.lagre_turer([lag_tur("uten-type", "brate", turtyper=())])
        adresse = self.sok("720", turtype="marka", startpunkt="brate")
        self.assertContains(self.client.get(adresse), "Prøv alle turtyper")
        svar = self.endre(adresse, "turtype", "")
        self.assertEqual(svar.status_code, 302)
        ny = svar["Location"]
        self.assertNotEqual(ny, adresse)
        sok = self.tilstand(ny)["sok"]
        self.assertIsNone(sok["turtype"])
        self.assertEqual(sok["varighet_min"], 720)
        self.assertEqual(sok["startpunkt_id"], "brate")

    def test_halvtime(self, _):  # FR-8
        turdata.lagre_turer([lag_tur("marka-halv", "brate", estimert_tid_min=90)])
        svar = self.client.get(self.sok("60", turtype="marka"))
        self.assertContains(svar, "Prøv 1,5 timer")
        self.assertContains(svar, 'name="verdi" value="90"')

    def test_trykk_forslag(self, _):  # FR-8, UX-DR22
        adresse = self.sok("120", turtype="topptur")
        svar = self.endre(adresse, "varighet", "300")
        self.assertEqual(svar.status_code, 302)
        ny = svar["Location"]
        self.assertNotEqual(ny, adresse)
        self.assertTrue(ny.startswith("/forslag/"))
        tilstand = self.tilstand(ny)
        self.assertEqual(tilstand["sok"]["varighet_min"], 300)
        self.assertEqual(tilstand["sok"]["turtype"], "topptur")
        self.assertEqual(tilstand["status"], "treff")
        self.assertContains(self.client.get(ny), "Åstoppen")
        self.assertIn(adresse.split("/")[2], self.client.session["sok"])

    def test_trykk_turtype_beholder_de_andre_valgene(self, _):  # FR-8
        adresse = self.sok("180", turtype="topptur", startpunkt="brate")
        tilstand = self.tilstand(self.endre(adresse, "turtype", "marka")["Location"])
        self.assertEqual(tilstand["sok"]["turtype"], "marka")
        self.assertEqual(tilstand["sok"]["startpunkt_id"], "brate")
        self.assertEqual(tilstand["sok"]["varighet_min"], 180)

    def test_ugyldig_input_gir_sok(self, _):  # FR-8, NFR-2
        adresse = self.sok("120", turtype="topptur")
        for_ = dict(self.client.session["sok"])
        for felt, verdi in (
            ("varighet", "301"),
            ("varighet", "150"),
            ("varighet", "abc"),
            ("varighet", ""),
            ("turtype", "marka"),
            ("startpunkt", ""),
            ("dato", "2026-11-29"),
            ("finnes-ikke", "x"),
            ("", ""),
        ):
            with self.subTest(felt=felt, verdi=verdi):
                svar = self.endre(adresse, felt, verdi)
                self.assertRedirects(svar, "/", fetch_redirect_response=False)
        for data in (
            {},
            {"felt": "varighet"},
            {"verdi": "300"},
            {"felt": ["a", "b"], "verdi": "x" * 5000},
        ):
            with self.subTest(data=data):
                svar = self.client.post(adresse + "endre/", data)
                self.assertRedirects(svar, "/", fetch_redirect_response=False)
        self.assertEqual(self.client.session["sok"], for_)

    def test_ukjent_sok_id(self, _):  # FR-8, NFR-2
        data = {"felt": "varighet", "verdi": "300"}
        svar = self.client.post("/forslag/finnes-ikke/endre/", data)
        self.assertRedirects(svar, "/", fetch_redirect_response=False)
        self.assertContains(self.client.get("/"), "Turforslaget er ikke lenger tilgjengelig.")

    def test_get_gir_405(self, _):  # PRG
        adresse = self.sok("120", turtype="topptur")
        self.assertEqual(self.client.get(adresse + "endre/").status_code, 405)

    def test_csrf(self, _):  # AR-7, PRG
        klient = Client(enforce_csrf_checks=True)
        token = csrf_token(klient.get("/"))
        data = {"varighet": "120", "dato": "2026-11-28", "turtype": "topptur", "startpunkt": ""}
        adresse = klient.post("/", {**data, "csrfmiddlewaretoken": token})["Location"]
        side = klient.get(adresse)
        skjema = {"felt": "varighet", "verdi": "300"}
        self.assertEqual(klient.post(adresse + "endre/", skjema).status_code, 403)
        svar = klient.post(adresse + "endre/", {**skjema, "csrfmiddlewaretoken": csrf_token(side)})
        self.assertEqual(svar.status_code, 302)
        self.assertTrue(svar["Location"].startswith("/forslag/"))

    def test_fokus_paa_startpunkt(self, _):  # FR-8, UX-DR22
        sok_id = self.sok("300", turtype="topptur", startpunkt="brate").split("/")[2]
        svar = self.client.get(f"/?sok={sok_id}&fokus=startpunkt")
        html = svar.content.decode()
        self.assertEqual(html.count("autofocus"), 1)
        self.assertRegex(html, r'<select id="startpunkt"[^>]*autofocus')
        self.assertContains(svar, '<option value="brate" selected>Bråten</option>', html=True)
        for fokus in ("varighet", "x", "", "startpunkt&fokus=dato"):
            with self.subTest(fokus=fokus):
                svar = self.client.get("/", {"sok": sok_id, "fokus": fokus})
                self.assertNotContains(svar, "autofocus")

    def test_alle_vist_bare_forslag_med_ny_tur(self, _):  # FR-8, FR-7
        adresse = self.sok("180")
        self.vis_alle(adresse)
        svar = self.client.get(adresse)
        self.assertContains(svar, "Du har sett alle turene som passer søket")
        self.assertContains(svar, "Start fra første forslag igjen")
        self.assertContains(svar, "Prøv 5 timer")  # topptur-lang er en ny tur
        self.assertContains(svar, "Endre søk", count=1)
        ny = self.endre(adresse, "varighet", "300")["Location"]
        self.assertNotEqual(ny, adresse)
        self.assertContains(self.client.get(ny), "Åstoppen")

    def test_alle_vist_uten_forslag(self, _):  # FR-8
        adresse = self.sok("720")
        self.vis_alle(adresse)
        svar = self.client.get(adresse)
        self.assertContains(svar, "Du har sett alle turene som passer søket")
        self.assertNotContains(svar, 'name="felt"')
        self.assertContains(svar, "Start fra første forslag igjen")
        self.assertContains(svar, "Endre søk", count=1)

    def test_topptur_erstattet_rekkefolge(self, _):  # FR-8, UX-DR22
        tekst = tekster(self.client.get(self.sok("150", turtype="topptur")))
        for foer, etter in (
            ("Åsen utsikt", "Utsikt i stedet for topptur"),
            ("Utsikt i stedet for topptur", "Ingen topptur passer søket ditt"),
            ("Ingen topptur passer søket ditt", "Tur-retur"),
        ):
            self.assertLess(tekst.index(f"| {foer} |"), tekst.index(f"| {etter} |"))

    def test_bare_over_nivataket_gjest(self, _):  # FR-8, SM-C1
        svar = self.client.get(self.sok("240", startpunkt="ovre"))
        self.assertContains(svar, "Ingen grønne turer passer søket")
        self.assertNotContains(svar, "Prøv å endre søket:")
        self.assertNotContains(svar, "lengre")
        self.assertNotContains(svar, "vanskeligere")
        self.assertNotContains(svar, "Blå – moderat")
        self.assertContains(svar, "Endre søk", count=1)

    def test_forslag_gir_aldri_tur_over_nivataket(self, _):  # SM-C1
        svar = self.client.get(self.sok("60", startpunkt="ovre"))
        self.assertNotContains(svar, "Øvresetra blå")
        self.assertNotContains(svar, 'name="felt"')


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
