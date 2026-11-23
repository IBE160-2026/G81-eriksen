"""Byggeskriptet for turdatabasen, med lagrede svar i stedet for nett (AD-3 punkt 2, AR-2, AR-15).

`hent` byttes ut med `FalskHent`, som svarer fra `tests/fixtures/`. Hver test bruker en
midlertidig `data/`-mappe.
"""

import http.client
import io
import json
import re
import shutil
import tempfile
import unittest
import urllib.error
import urllib.parse
from pathlib import Path
from unittest import mock

from domene import gradering, rute, tid
from domene.tur import Form, Tur
from skript import bygg_turdatabase as bygg
from tests.domene.test_bare_standardbibliotek import ikke_standard_importer

ROT = Path(__file__).resolve().parents[2]
FIXTURES = ROT / "tests" / "fixtures"
GAMMEL = '{"type": "FeatureCollection", "features": []}\n'

STARTPUNKT = 'startpunkt = { id = "sognsvann", navn = "Sognsvann", lat = 59.96711, lon = 10.73382 }'


def tur_toml(
    tur_id="brekke",
    form="tur-retur",
    rutenummer='["F_20220203_01"]',
    rutepunkter="fra = [59.971026, 10.733128]\ntil = [59.971357, 10.747841]",
    startpunkt=STARTPUNKT,
    ekstra='ut_no_url = ""',
):
    return (
        f'[[tur]]\nid = "{tur_id}"\nnavn = "Testtur"\nform = "{form}"\n'
        f'turtyper = ["marka"]\nrutenummer = {rutenummer}\n{ekstra}\n{startpunkt}\n\n'
        f"[tur.rutepunkter]\n{rutepunkter}\n\n"
    )


class FalskHent:
    """Svarer på WFS- og høydekall fra lagrede svar. Kan feile på ønsket kall."""

    def __init__(self, feil_pa=None, alias=None, wfs_svar=None, hoyde_svar=None):
        self.hoyder = json.loads((FIXTURES / "hoyder_testturer.json").read_text(encoding="utf-8"))
        self.kall: list[str] = []
        self.feil_pa = feil_pa  # (prefiks for URL, unntak)
        self.alias = alias or {}  # rutenummer -> rutenummer med fixture
        self.wfs_svar = wfs_svar  # bytes som erstatter alle WFS-svar
        self.hoyde_svar = hoyde_svar  # funksjon: antall punkter -> bytes som erstatter svaret

    def __call__(self, url: str) -> bytes:
        self.kall.append(url)
        if self.feil_pa and url.startswith(self.feil_pa[0]):
            raise self.feil_pa[1]
        sporring = urllib.parse.parse_qs(urllib.parse.urlsplit(url).query)
        if url.startswith(bygg.WFS_URL):
            if self.wfs_svar is not None:
                return self.wfs_svar
            nummer = re.search(r"<fes:Literal>(.*?)</fes:Literal>", sporring["filter"][0])[1]
            nummer = self.alias.get(nummer, nummer)
            fil = FIXTURES / f"wfs_{nummer}.xml"
            return (fil if fil.exists() else FIXTURES / "wfs_tom.xml").read_bytes()
        punkter = json.loads(sporring["punkter"][0])
        if self.hoyde_svar is not None:
            return self.hoyde_svar(len(punkter))
        if len(punkter) > bygg.MAKS_PUNKTER_PER_KALL:
            raise AssertionError(f"{len(punkter)} punkter i ett høydekall")
        svar = [
            {"datakilde": "dtm1", "terreng": None, "x": x, "y": y, "z": self.hoyder[f"{x},{y}"]}
            for x, y in punkter
        ]
        return json.dumps({"koordsys": 4258, "punkter": svar}).encode()


class MidlertidigDataTest(unittest.TestCase):
    """Gir en midlertidig `data/`-mappe med en gammel `turer.geojson`."""

    def setUp(self):
        self.mappe = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.mappe, ignore_errors=True)
        self.turer = self.mappe / bygg.TURER
        self.turer.write_text(GAMMEL, encoding="utf-8")

    def skriv_liste(self, tekst: str) -> None:
        (self.mappe / bygg.KURATERINGSLISTE).write_text(tekst, encoding="utf-8")

    def bruk_ekte_liste(self) -> None:
        shutil.copy(ROT / "data" / bygg.KURATERINGSLISTE, self.mappe / bygg.KURATERINGSLISTE)

    def assert_stopper_og_gammel_fil_star(self, hent, *deler: str) -> str:
        """Kjører byggingen, sjekker at den stopper med alle `deler` i meldingen, at den gamle
        fila er uendret og at ingen midlertidig fil ligger igjen."""
        with self.assertRaises(bygg.ByggFeil) as feil:
            bygg.bygg(self.mappe, hent)
        melding = str(feil.exception)
        for del_ in deler:
            self.assertIn(del_, melding)
        self.assertEqual(self.turer.read_text(encoding="utf-8"), GAMMEL)
        self.assertFalse(list(self.mappe.glob("*.tmp")))
        return melding


class GyldigListeTest(MidlertidigDataTest):
    def setUp(self):
        super().setUp()
        self.bruk_ekte_liste()

    def test_bygger_alle_testturene_med_feltene_i_ad_3(self):  # AD-3 punkt 1 og 2
        bygg.bygg(self.mappe, FalskHent())
        samling = json.loads(self.turer.read_text(encoding="utf-8"))
        self.assertEqual(samling["type"], "FeatureCollection")
        ider = [f["id"] for f in samling["features"]]
        self.assertEqual(ider, ["frognervassdraget", "sognsvann-brekke", "rundtur-ulsrudvann"])
        for feature in samling["features"]:
            with self.subTest(tur=feature["id"]):
                tur = Tur.fra_geojson_feature(feature)
                self.assertEqual(tur.kilde, "turrutebasen")
                self.assertEqual(tur.lisens, "CC BY 4.0")
                self.assertEqual(tur.ut_no_url, "")
                # Lengden er stiens lengde, og profilen slutter der.
                self.assertEqual(tur.lengde_m, rute.hele_meter(rute.linjelengde_m(tur.geometry)))
                self.assertEqual(tur.hoydeprofil[0][0], 0)
                self.assertEqual(tur.hoydeprofil[-1][0], tur.lengde_m)
                # Høydemeterne regnes fra de samme punktene som profilen.
                self.assertEqual(
                    rute.hoydemeter_og_nedstigning([h for _, h in tur.hoydeprofil]),
                    (tur.hoydemeter_m, tur.nedstigning_m),
                )

    def test_niva_og_tid_er_lik_det_domene_gir(self):  # AD-3, FR-2, FR-3, AR-2
        bygg.bygg(self.mappe, FalskHent())
        for feature in json.loads(self.turer.read_text(encoding="utf-8"))["features"]:
            tur = Tur.fra_geojson_feature(feature)
            with self.subTest(tur=tur.id):
                self.assertEqual(tur.turniva, gradering.turniva(tur.lengde_m, tur.hoydemeter_m))
                self.assertEqual(
                    tur.estimert_tid_min,
                    tid.estimert_tid_min(
                        tur.form, tur.lengde_m, tur.hoydemeter_m, tur.nedstigning_m
                    ),
                )

    def test_tur_retur_lagrer_en_vei_og_rundtur_hele_runden(self):  # AD-3, FR-2
        turer = {t.id: t for t in bygg.bygg(self.mappe, FalskHent())}
        frogner = turer["frognervassdraget"]
        self.assertIs(frogner.form, Form.TUR_RETUR)
        self.assertEqual(frogner.geometry[0], (10.72659, 59.969076))
        self.assertEqual(frogner.geometry[-1], (10.716583, 59.952655))
        rundtur = turer["rundtur-ulsrudvann"]
        self.assertIs(rundtur.form, Form.RUNDTUR)
        self.assertEqual(rundtur.geometry[0], rundtur.geometry[-1])

    def test_startpunktet_far_hoyde_fra_api_et(self):  # AD-3
        turer = bygg.bygg(self.mappe, FalskHent())
        self.assertEqual(
            {t.startpunkt_hoyde_m for t in turer if t.startpunkt_id == "sognsvann"}, {200}
        )

    def test_to_kjoringer_gir_lik_fil_byte_for_byte(self):  # AD-3, AR-15
        bygg.bygg(self.mappe, FalskHent())
        forste = self.turer.read_bytes()
        bygg.bygg(self.mappe, FalskHent())
        self.assertEqual(self.turer.read_bytes(), forste)
        self.assertFalse(list(self.mappe.glob("*.tmp")))

    def test_committet_turer_geojson_er_bygget_fra_lista(self):  # AD-3 punkt 2
        bygg.bygg(self.mappe, FalskHent())
        self.assertEqual(
            self.turer.read_text(encoding="utf-8"),
            (ROT / "data" / bygg.TURER).read_text(encoding="utf-8"),
        )

    def test_hoydene_hentes_i_bolker_pa_hoyst_50(self):  # AD-3 punkt 2
        hent = FalskHent()
        bygg.bygg(self.mappe, hent)
        hoydekall = [k for k in hent.kall if k.startswith(bygg.HOYDE_URL)]
        self.assertGreater(len(hoydekall), 3)
        for kall in hoydekall:
            sporring = urllib.parse.parse_qs(urllib.parse.urlsplit(kall).query)
            self.assertEqual(sporring["koordsys"], ["4258"])
            self.assertLessEqual(len(json.loads(sporring["punkter"][0])), 50)

    def test_wfs_filteret_bruker_stien_til_rutenummer(self):  # AD-3 punkt 2
        sporring = urllib.parse.parse_qs(urllib.parse.urlsplit(bygg.wfs_url("F_01812_03")).query)
        self.assertEqual(sporring["typeNames"], ["app:Fotrute"])
        self.assertEqual(sporring["srsName"], ["EPSG:4326"])
        self.assertIn("app:fotruteInfo/app:FotruteInfo/app:rutenummer", sporring["filter"][0])
        self.assertIn("<fes:Literal>F_01812_03</fes:Literal>", sporring["filter"][0])


class FeilIMatrisenTest(MidlertidigDataTest):
    def test_ingen_sti_mellom_komponenter(self):  # AD-3
        # F_20220203_01 har to komponenter; «til» ligger på den andre.
        self.skriv_liste(
            tur_toml(rutepunkter="fra = [59.971026, 10.733128]\ntil = [59.969127, 10.761513]")
        )
        melding = self.assert_stopper_og_gammel_fil_star(FalskHent(), "«brekke»", "F_20220203_01")
        self.assertIn("ingen sti", melding)

    def test_punkt_for_langt_unna(self):  # AD-3
        # Via-punktet ligger ca. 100 m nord for nærmeste node (59.968754, 10.739337).
        self.skriv_liste(
            tur_toml(
                rutepunkter="fra = [59.971026, 10.733128]\nvia = [[59.969654, 10.739337]]\n"
                "til = [59.971357, 10.747841]"
            )
        )
        melding = self.assert_stopper_og_gammel_fil_star(FalskHent(), "«brekke»", "maks 50 m")
        self.assertRegex(melding, r"ligger \d+ m fra nærmeste node")

    def test_ukjent_rutenummer_gir_0_segmenter(self):  # AD-3
        self.skriv_liste(tur_toml(rutenummer='["F_FINNES_IKKE"]'))
        self.assert_stopper_og_gammel_fil_star(
            FalskHent(), "«brekke»", "F_FINNES_IKKE", "0 segmenter"
        )

    def test_http_500_fra_hoyde_api_et(self):  # AD-3
        self.skriv_liste(tur_toml())
        hent = FalskHent(
            feil_pa=(bygg.HOYDE_URL, bygg.HentFeil("ws.geonorge.no svarte med HTTP 500."))
        )
        self.assert_stopper_og_gammel_fil_star(hent, "«brekke»", "HTTP 500")

    def test_tidsavbrudd_fra_wfs(self):  # AD-3
        self.skriv_liste(tur_toml())
        hent = FalskHent(feil_pa=(bygg.WFS_URL, bygg.HentFeil("svarte ikke innen 60 s.")))
        self.assert_stopper_og_gammel_fil_star(hent, "«brekke»", "F_20220203_01", "60 s")

    def test_feil_i_siste_tur_skriver_ingenting(self):  # AD-3
        self.bruk_ekte_liste()
        liste = self.mappe / bygg.KURATERINGSLISTE
        tekst = liste.read_text(encoding="utf-8").replace('["F_20200422_1"]', '["F_FINNES_IKKE"]')
        liste.write_text(tekst, encoding="utf-8")
        self.assert_stopper_og_gammel_fil_star(FalskHent(), "«rundtur-ulsrudvann»")

    def test_ulikt_startpunkt_stopper_for_noe_hentes(self):  # AD-3 punkt 2
        annet = STARTPUNKT.replace('navn = "Sognsvann"', 'navn = "Sognsvann stasjon"')
        self.skriv_liste(tur_toml() + tur_toml(tur_id="brekke-2", startpunkt=annet))
        hent = FalskHent()
        self.assert_stopper_og_gammel_fil_star(hent, "«sognsvann»")
        self.assertEqual(hent.kall, [])

    def test_ulik_koordinat_for_samme_startpunkt_stopper(self):  # AD-3 punkt 2
        annet = STARTPUNKT.replace("lat = 59.96711", "lat = 59.9672")
        self.skriv_liste(tur_toml() + tur_toml(tur_id="brekke-2", startpunkt=annet))
        self.assert_stopper_og_gammel_fil_star(FalskHent(), "«sognsvann»")

    def test_osm_uttrekk_med_100_objekter_stopper(self):  # AD-3 punkt 3
        self.skriv_liste(tur_toml())
        features = [{"type": "Feature", "geometry": None, "properties": {}}] * 100
        (self.mappe / bygg.OSM_UTTREKK).write_text(
            json.dumps({"type": "FeatureCollection", "features": features}), encoding="utf-8"
        )
        hent = FalskHent()
        self.assert_stopper_og_gammel_fil_star(hent, "100 objekter")
        self.assertEqual(hent.kall, [])

    def test_osm_uttrekk_med_99_objekter_godtas(self):  # AD-3 punkt 3
        features = [{"type": "Feature", "geometry": None, "properties": {}}] * 99
        (self.mappe / bygg.OSM_UTTREKK).write_text(
            json.dumps({"type": "FeatureCollection", "features": features}), encoding="utf-8"
        )
        bygg.sjekk_osm_uttrekk(self.mappe)

    def test_rundtur_uten_via_stopper(self):  # AD-3 punkt 2
        self.skriv_liste(tur_toml(form="rundtur", rutepunkter="fra = [59.971026, 10.733128]"))
        hent = FalskHent()
        self.assert_stopper_og_gammel_fil_star(hent, "«brekke»", "via")
        self.assertEqual(hent.kall, [])

    def test_rundtur_med_til_stopper(self):  # AD-3 punkt 2
        self.skriv_liste(tur_toml(form="rundtur"))
        self.assert_stopper_og_gammel_fil_star(FalskHent(), "«brekke»", "til")

    def test_tur_retur_uten_til_stopper(self):  # AD-3 punkt 2
        self.skriv_liste(tur_toml(rutepunkter="fra = [59.971026, 10.733128]"))
        hent = FalskHent()
        self.assert_stopper_og_gammel_fil_star(hent, "«brekke»", "til")
        self.assertEqual(hent.kall, [])

    def test_lon_lat_skrevet_feil_vei_stopper(self):  # AD-3 punkt 2
        self.skriv_liste(
            tur_toml(rutepunkter="fra = [10.733128, 59.971026]\ntil = [59.971357, 10.747841]")
        )
        self.assert_stopper_og_gammel_fil_star(FalskHent(), "«brekke»", "[lat, lon]")

    def test_ukjent_turtype_og_dobbel_id_stopper(self):  # AD-3 punkt 2
        self.skriv_liste(tur_toml().replace('["marka"]', '["fjell"]'))
        self.assert_stopper_og_gammel_fil_star(FalskHent(), "fjell")
        self.skriv_liste(tur_toml() + tur_toml())
        self.assert_stopper_og_gammel_fil_star(FalskHent(), "«brekke»", "flere ganger")

    def test_ugyldig_toml_stopper(self):  # AD-3 punkt 2
        self.skriv_liste("[[tur]\n")
        self.assert_stopper_og_gammel_fil_star(FalskHent(), "TOML")

    def test_feil_ved_bytte_av_fil_gir_melding_og_ingen_midlertidig_fil(self):  # AD-3
        # For eksempel en låst fil på Windows.
        self.skriv_liste(tur_toml())
        with mock.patch.object(bygg.os, "replace", side_effect=PermissionError("låst")):
            self.assert_stopper_og_gammel_fil_star(FalskHent(), "Kunne ikke skrive", "låst")
        self.assertFalse(list(self.mappe.glob(".*")))

    def test_ugyldige_hoydesvar(self):  # AD-3
        tilfeller = {
            "z er null": ("null", "ingen gyldig høyde"),
            "z er NaN": ("NaN", "ingen gyldig høyde"),
            "z er tekst": ('"abc"', "ingen gyldig høyde"),
            "for få punkter": (None, "0 høyder"),
            "ikke JSON": ("<html>", "ikke kunne leses"),
        }
        self.skriv_liste(tur_toml())
        for navn, (z, tekst) in tilfeller.items():

            def svar(antall, z=z):
                punkter = [] if z is None else [f'{{"z": {z}}}'] * antall
                return f'{{"punkter": [{", ".join(punkter)}]}}'.encode()

            with self.subTest(navn):
                self.assert_stopper_og_gammel_fil_star(
                    FalskHent(hoyde_svar=svar), "«brekke»", tekst
                )

    def test_ugyldige_wfs_svar(self):  # AD-3
        rapport = (
            b'<?xml version="1.0"?><ows:ExceptionReport xmlns:ows="http://www.opengis.net/ows/1.1">'
            b'<ows:Exception exceptionCode="InvalidParameterValue"/></ows:ExceptionReport>'
        )
        self.skriv_liste(tur_toml())
        for navn, svar in {"ExceptionReport": rapport, "ikke XML": b"\xff\x00 ikke xml"}.items():
            with self.subTest(navn):
                self.assert_stopper_og_gammel_fil_star(
                    FalskHent(wfs_svar=svar), "«brekke»", "F_20220203_01"
                )

    def test_ukjente_felt_stopper_for_noe_hentes(self):  # AD-3 punkt 2
        tilfeller = {
            "rutenumer": tur_toml(ekstra='ut_no_url = ""\nrutenumer = ["F_1"]'),
            "vai": tur_toml(
                rutepunkter="fra = [59.971026, 10.733128]\nvai = [[59.97, 10.74]]\n"
                "til = [59.971357, 10.747841]"
            ),
            "hoyde": tur_toml(startpunkt=STARTPUNKT.replace(" }", ", hoyde = 200 }")),
        }
        for felt, tekst in tilfeller.items():
            with self.subTest(felt):
                self.skriv_liste(tekst)
                hent = FalskHent()
                self.assert_stopper_og_gammel_fil_star(hent, "«brekke»", felt, "ukjente felt")
                self.assertEqual(hent.kall, [])

    def test_via_pa_samme_node_som_fra_stopper(self):  # AD-3
        # Via-punktet ligger ca. 10 m fra «fra» og ville ellers forsvunnet.
        self.skriv_liste(
            tur_toml(
                rutepunkter="fra = [59.971026, 10.733128]\nvia = [[59.971116, 10.733128]]\n"
                "til = [59.971357, 10.747841]"
            )
        )
        self.assert_stopper_og_gammel_fil_star(
            FalskHent(), "«brekke»", "samme node", "F_20220203_01"
        )

    def test_kurateringslista_kan_ikke_leses(self):  # AD-3 punkt 2
        liste = self.mappe / bygg.KURATERINGSLISTE
        liste.write_bytes(b'[[tur]]\nid = "\xff\xfe"\n')
        self.assert_stopper_og_gammel_fil_star(FalskHent(), "UTF-8")
        liste.unlink()
        liste.mkdir()  # OSError ved lesing
        self.assert_stopper_og_gammel_fil_star(FalskHent(), "kurateringslista")

    def test_osm_uttrekk_som_ikke_kan_leses_stopper(self):  # AD-3 punkt 3
        self.skriv_liste(tur_toml())
        osm = self.mappe / bygg.OSM_UTTREKK
        osm.write_text('{"features": 5}', encoding="utf-8")
        self.assert_stopper_og_gammel_fil_star(FalskHent(), bygg.OSM_UTTREKK, "features")
        osm.unlink()
        osm.mkdir()  # OSError ved lesing
        self.assert_stopper_og_gammel_fil_star(FalskHent(), bygg.OSM_UTTREKK)


class ValgfrieFeltTest(MidlertidigDataTest):
    def test_manglende_ut_no_url_blir_tom(self):  # AD-3
        self.skriv_liste(tur_toml(ekstra=""))
        (tur,) = bygg.bygg(self.mappe, FalskHent())
        self.assertEqual(tur.ut_no_url, "")
        self.assertEqual(tur.navn, "Testtur")
        self.assertIsInstance(tur.turtyper, tuple)
        self.assertIsInstance(tur.geometry, tuple)


class DelteSegmenterTest(MidlertidigDataTest):
    def test_segmenter_som_deles_mellom_rutenummer_tas_med_en_gang(self):  # AD-3 punkt 2
        self.skriv_liste(tur_toml())
        (en,) = bygg.bygg(self.mappe, FalskHent())
        self.skriv_liste(tur_toml(rutenummer='["F_20220203_01", "F_KOPI"]'))
        hent = FalskHent(alias={"F_KOPI": "F_20220203_01"})
        (to,) = bygg.bygg(self.mappe, hent)
        self.assertEqual(sum(k.startswith(bygg.WFS_URL) for k in hent.kall), 2)
        self.assertEqual((to.lengde_m, to.geometry), (en.lengde_m, en.geometry))
        segmenter = bygg.les_segmenter((FIXTURES / "wfs_F_20220203_01.xml").read_bytes())
        self.assertEqual(rute.lag_nettverk(segmenter + segmenter), rute.lag_nettverk(segmenter))


class HentTest(unittest.TestCase):
    """Den ekte `hent` med `urllib.request.urlopen` byttet ut (ingen nettverk)."""

    def test_sender_user_agent_og_tidsavbrudd_60_s(self):  # AD-3
        svar = mock.MagicMock()
        svar.__enter__.return_value.read.return_value = b"ok"
        with mock.patch.object(bygg.urllib.request, "urlopen", return_value=svar) as urlopen:
            self.assertEqual(bygg.hent("https://ws.geonorge.no/x"), b"ok")
        foresporsel = urlopen.call_args.args[0]
        self.assertEqual(foresporsel.get_header("User-agent"), bygg.USER_AGENT)
        self.assertEqual(urlopen.call_args.kwargs["timeout"], 60)
        self.assertNotIn("@", bygg.USER_AGENT)

    def test_http_500_blir_hentfeil(self):  # AD-3
        feil = urllib.error.HTTPError("https://ws.geonorge.no/x", 500, "feil", {}, io.BytesIO())
        with mock.patch.object(bygg.urllib.request, "urlopen", side_effect=feil):
            with self.assertRaisesRegex(bygg.HentFeil, "HTTP 500"):
                bygg.hent("https://ws.geonorge.no/x")

    def test_nettverksfeil_blir_hentfeil(self):  # AD-3
        tilfeller = {
            "ukjent vert": (
                urllib.error.URLError("Name or service not known"),
                "Fikk ikke kontakt",
            ),
            "tilkobling brutt": (ConnectionResetError(), "Nettverksfeil"),
        }
        for navn, (feil, tekst) in tilfeller.items():
            with self.subTest(navn):
                with mock.patch.object(bygg.urllib.request, "urlopen", side_effect=feil):
                    with self.assertRaisesRegex(bygg.HentFeil, tekst):
                        bygg.hent("https://ws.geonorge.no/x")

    def test_brutt_svar_under_lesing_blir_hentfeil(self):  # AD-3
        for feil in (http.client.IncompleteRead(b"del"), http.client.RemoteDisconnected("borte")):
            with self.subTest(type(feil).__name__):
                svar = mock.MagicMock()
                svar.__enter__.return_value.read.side_effect = feil
                with mock.patch.object(bygg.urllib.request, "urlopen", return_value=svar):
                    with self.assertRaisesRegex(bygg.HentFeil, "ble brutt"):
                        bygg.hent("https://ws.geonorge.no/x")

    def test_tidsavbrudd_blir_hentfeil(self):  # AD-3
        for feil in (TimeoutError("timed out"), urllib.error.URLError(TimeoutError())):
            with self.subTest(feil=type(feil).__name__):
                with mock.patch.object(bygg.urllib.request, "urlopen", side_effect=feil):
                    with self.assertRaisesRegex(bygg.HentFeil, "60 s"):
                        bygg.hent("https://ws.geonorge.no/x")


class MainTest(MidlertidigDataTest):
    def test_feil_gir_norsk_melding_og_exit_kode_1(self):  # AD-3
        self.skriv_liste(tur_toml(rutenummer='["F_FINNES_IKKE"]'))
        with (
            mock.patch.object(bygg, "DATA", self.mappe),
            mock.patch.object(bygg, "hent", FalskHent()),
            self.assertLogs("skript.bygg_turdatabase", level="ERROR") as logg,
        ):
            self.assertEqual(bygg.main(), 1)
        self.assertIn("«brekke»", logg.output[0])
        self.assertIn("F_FINNES_IKKE", logg.output[0])
        self.assertEqual(self.turer.read_text(encoding="utf-8"), GAMMEL)

    def test_vellykket_kjoring_gir_exit_kode_0(self):  # AD-3
        self.skriv_liste(tur_toml())
        with (
            mock.patch.object(bygg, "DATA", self.mappe),
            mock.patch.object(bygg, "hent", FalskHent()),
            self.assertLogs("skript.bygg_turdatabase", level="INFO"),
        ):
            self.assertEqual(bygg.main(), 0)
        self.assertNotEqual(self.turer.read_text(encoding="utf-8"), GAMMEL)


class BareStandardbibliotekTest(unittest.TestCase):
    def test_skript_importerer_bare_standardbiblioteket_og_domene(self):  # AR-2
        filer = sorted((ROT / "skript").rglob("*.py"))
        self.assertIn("bygg_turdatabase.py", [f.name for f in filer])
        for fil in filer:
            with self.subTest(fil=fil.name):
                self.assertEqual(ikke_standard_importer(fil.read_text(encoding="utf-8")), [])
