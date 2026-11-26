"""Måleskriptet for kartfargene, uten nett (story 6.5, UX-DR35, NFR-4, UX-DR1).

PNG-ene lages i minnet med `zlib` og `struct`, og `hent` byttes ut med en funksjon som
svarer med dem. Ingen test henter fliser fra Kartverket.
"""

import contextlib
import io
import struct
import tempfile
import unittest
import zlib
from pathlib import Path
from unittest import mock

from skript import mal_kartfarger as mal
from tests.domene.test_bare_standardbibliotek import ikke_standard_importer

ROT = Path(__file__).resolve().parents[2]
HVIT = (255, 255, 255)
SVART = (0, 0, 0)
PLOMME = (0x6A, 0x3D, 0x9A)
SKOG = (0xDF, 0xED, 0xA3)


def _paeth(a, b, c):
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    return b if pb <= pc else c


def _filtrer(rad, forrige, kanaler, filter_):
    """Det motsatte av dekodingen i skriptet: lager de filtrerte bytene for én rad."""
    ut = bytearray()
    for x, verdi in enumerate(rad):
        a = rad[x - kanaler] if x >= kanaler else 0
        b = forrige[x]
        c = forrige[x - kanaler] if x >= kanaler else 0
        prediksjon = (0, a, b, (a + b) // 2, _paeth(a, b, c))[filter_]
        ut.append((verdi - prediksjon) & 255)
    return bytes(ut)


def _bit(typ, innhold):
    crc = zlib.crc32(typ + innhold) & 0xFFFFFFFF
    return struct.pack(">I", len(innhold)) + typ + innhold + struct.pack(">I", crc)


def lag_png(rader, fargetype=6, palett=b"", gjennomsiktig=b""):
    """PNG med 8 bit per kanal. `rader` er lister med kanalverdier per piksel.

    Rad nr. i bruker filter i % 5, så alle fem filtrene (0–4) blir dekodet.
    """
    kanaler = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[fargetype]
    hoyde, bredde = len(rader), len(rader[0])
    forrige = bytes(bredde * kanaler)
    raa = bytearray()
    for i, rad in enumerate(rader):
        flat = bytes(v for piksel in rad for v in piksel)
        filter_ = i % 5
        raa += bytes([filter_]) + _filtrer(flat, forrige, kanaler, filter_)
        forrige = flat
    data = mal.PNG_SIGNATUR + _bit(
        b"IHDR", struct.pack(">IIBBBBB", bredde, hoyde, 8, fargetype, 0, 0, 0)
    )
    if palett:
        data += _bit(b"PLTE", palett)
    if gjennomsiktig:
        data += _bit(b"tRNS", gjennomsiktig)
    return data + _bit(b"IDAT", zlib.compress(bytes(raa))) + _bit(b"IEND", b"")


class LuminansOgKontrastTest(unittest.TestCase):  # NFR-4, WCAG 2.1
    def test_luminans_for_hvit_og_svart(self):
        self.assertAlmostEqual(mal.luminans(HVIT), 1.0)
        self.assertAlmostEqual(mal.luminans(SVART), 0.0)

    def test_hvit_mot_svart_er_21(self):
        self.assertAlmostEqual(mal.kontrast(HVIT, SVART), 21.0)

    def test_kontrasten_er_lik_begge_veier(self):
        self.assertEqual(mal.kontrast(PLOMME, HVIT), mal.kontrast(HVIT, PLOMME))

    def test_plommelilla_mot_hvit_er_omtrent_7_6(self):  # DESIGN.md › Kontrastmål
        self.assertAlmostEqual(mal.kontrast(PLOMME, HVIT), 7.6, delta=0.05)

    def test_lik_farge_gir_1(self):
        self.assertAlmostEqual(mal.kontrast(SKOG, SKOG), 1.0)

    def test_hex_begge_veier(self):
        self.assertEqual(mal.hex_til_rgb("#6a3d9a"), PLOMME)
        self.assertEqual(mal.rgb_til_hex(PLOMME), "#6A3D9A")
        with self.assertRaises(ValueError):
            mal.hex_til_rgb("#fff")

    def test_fargetone(self):
        self.assertEqual(mal.fargetone((255, 0, 0)), 0)
        self.assertEqual(mal.fargetone((0, 0, 255)), 240)
        self.assertEqual(mal.fargetone(PLOMME), 269)


class PngTest(unittest.TestCase):
    def test_rgba_med_alle_filtrene(self):
        rader = [
            [
                ((x * 37 + y * 11) % 256, (x * 5 + y * 90) % 256, (x * y * 7) % 256, 255 - y)
                for x in range(4)
            ]
            for y in range(6)
        ]
        bilde = mal.les_png(lag_png(rader))
        self.assertEqual((bilde.bredde, bilde.hoyde), (4, 6))
        self.assertEqual(bilde.piksler, [tuple(p) for rad in rader for p in rad])
        self.assertEqual(bilde.piksel(3, 5), tuple(rader[5][3]))

    def test_rgb_uten_alfa(self):
        rader = [[(10, 20, 30), (200, 100, 0)], [(1, 2, 3), (250, 251, 252)]]
        bilde = mal.les_png(lag_png(rader, fargetype=2))
        self.assertEqual(
            bilde.piksler,
            [(10, 20, 30, 255), (200, 100, 0, 255), (1, 2, 3, 255), (250, 251, 252, 255)],
        )

    def test_palett_med_gjennomsiktighet(self):
        palett = bytes([255, 0, 0, 0, 255, 0])
        rader = [[(0,), (1,)], [(1,), (0,)]]
        bilde = mal.les_png(lag_png(rader, fargetype=3, palett=palett, gjennomsiktig=b"\x00"))
        self.assertEqual(
            bilde.piksler, [(255, 0, 0, 0), (0, 255, 0, 255), (0, 255, 0, 255), (255, 0, 0, 0)]
        )

    def test_gratone_med_og_uten_alfa(self):
        self.assertEqual(
            mal.les_png(lag_png([[(7,), (9,)]], fargetype=0)).piksler,
            [(7, 7, 7, 255), (9, 9, 9, 255)],
        )
        self.assertEqual(
            mal.les_png(lag_png([[(7, 0), (9, 128)]], fargetype=4)).piksler,
            [(7, 7, 7, 0), (9, 9, 9, 128)],
        )

    def test_avviser_annet_enn_png(self):
        with self.assertRaises(ValueError):
            mal.les_png(b"GIF89a")

    def test_avviser_16_bit(self):
        data = mal.PNG_SIGNATUR + _bit(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 16, 2, 0, 0, 0))
        with self.assertRaises(ValueError):
            mal.les_png(data)


class FlisTest(unittest.TestCase):  # AR-10
    def test_flisen_for_nordmarka(self):
        self.assertEqual(mal.flis_for(60.010, 10.690, 13), (4339, 2378))
        self.assertEqual(mal.flis_for(60.010, 10.690, 15), (17357, 9513))

    def test_adressen_har_raden_for_kolonnen(self):
        self.assertTrue(mal.flis_url(13, 4339, 2378).endswith("/webmercator/13/2378/4339.png"))

    def test_minst_to_steder_og_to_zoomnivaer_per_flate(self):  # UX-DR35
        self.assertGreaterEqual(len(mal.ZOOMNIVAER), 2)
        for flatetype in ("skog", "myr", "vann", "bebyggelse"):
            with self.subTest(flatetype=flatetype):
                steder = [s for s in mal.MALESTEDER if s.flatetype == flatetype]
                self.assertGreaterEqual(len(steder), 2)


class FlateTest(unittest.TestCase):
    def test_skyggelagt_skog_er_skog(self):
        self.assertTrue(mal.i_flaten((0x92, 0xA0, 0x56), SKOG))
        self.assertTrue(mal.i_flaten(SKOG, SKOG))

    def test_annen_tone_eller_for_mork_er_ikke_skog(self):
        self.assertFalse(mal.i_flaten((0xD8, 0xA9, 0x7D), SKOG))  # kote
        self.assertFalse(mal.i_flaten((0xDF - 100, 0xED - 100, 0xA3 - 100), SKOG))
        self.assertFalse(mal.i_flaten(HVIT, SKOG))

    def test_glatt_flate_tar_bort_kanter_rundt_tekst(self):
        hvit = (254, 254, 254, 255)
        rader = [[hvit] * 5 for _ in range(5)]
        rader[2][3] = (20, 20, 20, 255)  # en svart prikk, som tekst
        bilde = mal.les_png(lag_png(rader))
        myr = mal.Flate("myr", "#FEFEFE", glatt=True)
        # Bare de indre 3 × 3 har fire naboer; prikken og naboene til prikken faller bort.
        self.assertEqual(len(mal.piksler_i_flaten(bilde, myr)), 9 - 1 - 3)
        self.assertEqual(len(mal.piksler_i_flaten(bilde, mal.Flate("hvit", "#FEFEFE"))), 24)

    def test_persentil_fra_den_morkeste(self):
        farger = [(v, v, v) for v in range(100, 200)]
        self.assertEqual(mal.mork_persentil(farger, 0.01), (101, 101, 101))
        self.assertEqual(mal.mork_persentil(farger, 0.0), (100, 100, 100))
        with self.assertRaises(ValueError):
            mal.mork_persentil([])


class MalingTest(unittest.TestCase):
    def test_maler_alle_stedene_uten_nett(self):  # UX-DR35, ingen nettverkskall i tester
        rader = [[(0xD2, 0xE0, 0x96, 255)] * 4 for _ in range(4)]
        rader[0][0] = (0xB0, 0xBE, 0x74, 255)
        png = lag_png(rader)
        adresser = []

        def falsk_hent(url):
            adresser.append(url)
            return png

        with tempfile.TemporaryDirectory() as mappe, self.assertLogs(mal.logger, "WARNING"):
            malinger = mal.mal_alle(falsk_hent, Path(mappe))
            self.assertEqual(len(list(Path(mappe).iterdir())), 16)
        self.assertEqual(len(adresser), len(mal.MALESTEDER) * len(mal.ZOOMNIVAER))
        skog = [m for m in malinger if m.flate == "skog"]
        self.assertEqual(len(skog), 4)
        self.assertEqual(skog[0].flis, "13/4339/2378")
        self.assertIn("/13/2378/4339.png", adresser[4])
        self.assertEqual(skog[0].typisk, (0xD2, 0xE0, 0x96))
        self.assertEqual(skog[0].morkest, (0xB0, 0xBE, 0x74))  # 1. persentil av 16 = mørkeste
        self.assertEqual(skog[0].antall, 16)

    def test_tokenene_leses_fra_tokens_css(self):  # UX-DR1
        css = (ROT / "turforslag" / "static" / "css" / "tokens.css").read_text(encoding="utf-8")
        tokener = mal.les_tokens(css)
        self.assertEqual(set(tokener), set(mal.KARTLAG_TOKENER))
        with self.assertRaises(ValueError):
            mal.les_tokens(":root { --map-route: #6a3d9a; }")

    def test_kravene_og_tabellene(self):  # DESIGN.md › Kontrastmål
        tokener = {
            "map-route": PLOMME,
            "map-marker-start": (0x35, 0x51, 0x46),
            "map-focus-ring": (0xB0, 0x62, 0x4A),
            "map-overlay-surface": HVIT,
        }
        alle = {f.navn: (HVIT, HVIT) for flater in mal.FLATER.values() for f in flater}
        lys = alle | {"skog": (SKOG, SKOG)}
        self.assertEqual(mal.krav_oppfylt(lys, tokener), [])
        mork = alle | {"skog": (SKOG, (0x92, 0xA0, 0x56))}
        self.assertEqual(
            [b.split(":")[0] for b in mal.krav_oppfylt(mork, tokener)], ["map-route mot skog"]
        )
        tabell = mal.kontrasttabell(lys, tokener)
        self.assertIn("| **7,64** |", tabell)
        self.assertEqual(mal._tall(2.998), "2,99")  # rundes ned, aldri opp til kravet
        self.assertIn("| skog | `#DFEDA3` / `#DFEDA3` |", tabell)

    def test_skriptet_bruker_bare_standardbiblioteket(self):  # AR-2, ingen ny pakke
        kilde = (ROT / "skript" / "mal_kartfarger.py").read_text(encoding="utf-8")
        self.assertEqual(ikke_standard_importer(kilde), [])


DOKUMENTERTE_FLATER = {  # docs/kartfarger.md › Kontrast: (typisk, mørkest)
    "skog": ((0xD8, 0xE6, 0x9C), (0x9B, 0xA9, 0x5F)),
    "myr (hvit flate)": ((0xF2, 0xF2, 0xF2), (0xEA, 0xEA, 0xEA)),
    "vann": ((0xE0, 0xFE, 0xFE), (0xE0, 0xFE, 0xFE)),
    "boligfelt": ((0xEA, 0xD3, 0xBF), (0xC9, 0xB2, 0x9E)),
    "bebygd (grå)": ((0xEE, 0xEE, 0xDD), (0xA9, 0xA9, 0x99)),
}


def _maling(flate, typisk, morkest, antall):
    return mal.Maling("13/1/1", "Sted", flate, typisk, morkest, antall)


class KravTest(unittest.TestCase):  # UX-DR35, NFR-4, DESIGN.md › Kontrastmål
    def test_de_ekte_tokenene_holder_mot_de_dokumenterte_flatene(self):
        tokener = mal.les_tokens(mal.TOKENS_CSS.read_text(encoding="utf-8"))
        self.assertEqual(mal.krav_oppfylt(DOKUMENTERTE_FLATER, tokener), [])

    def test_en_flate_som_mangler_er_et_brudd(self):
        tokener = mal.les_tokens(mal.TOKENS_CSS.read_text(encoding="utf-8"))
        uten_myr = {n: v for n, v in DOKUMENTERTE_FLATER.items() if n != "myr (hvit flate)"}
        self.assertEqual(
            mal.krav_oppfylt(uten_myr, tokener), ["myr (hvit flate) ble ikke funnet på noen flis."]
        )

    def test_hvert_token_under_kravet_gir_riktig_brudd(self):
        tokener = mal.les_tokens(mal.TOKENS_CSS.read_text(encoding="utf-8"))
        lys_gra = (0xCC, 0xCC, 0xCC)
        for token, farge, ventet in (
            ("map-marker-start", (0x90, 0x90, 0x90), "map-marker-start mot skog"),
            ("map-marker-start", (0x80, 0x80, 0x80), "map-marker-start mot «S» er under 4,5."),
            ("map-focus-ring", lys_gra, "map-focus-ring mot den hvite ytre kanten er under 3."),
        ):
            with self.subTest(token=token, farge=farge):
                brudd = mal.krav_oppfylt(DOKUMENTERTE_FLATER, tokener | {token: farge})
                self.assertTrue(any(b.startswith(ventet) for b in brudd), brudd)

    def test_oppsummer_tar_den_morkeste_persentilen_og_typisk_fra_storste_flis(self):
        malinger = [
            _maling("boligfelt", (0xFB, 0xE4, 0xD0), (0xD0, 0xB9, 0xA4), 100),
            _maling("boligfelt", (0xEA, 0xD3, 0xBF), (0xDF, 0xC8, 0xB3), 300),
            _maling("boligfelt", (0xED, 0xD6, 0xC2), (0xC9, 0xB2, 0x9E), 200),
            _maling("vann", (0xE0, 0xFE, 0xFE), (0xE0, 0xFE, 0xFE), 5),
        ]
        self.assertEqual(
            mal.oppsummer(malinger),
            {
                "boligfelt": ((0xEA, 0xD3, 0xBF), (0xC9, 0xB2, 0x9E)),
                "vann": ((0xE0, 0xFE, 0xFE), (0xE0, 0xFE, 0xFE)),
            },
        )


class MainTest(unittest.TestCase):  # exit-kode, uten nett
    def _kjor(self, hent):
        with (
            mock.patch.object(mal, "hent", hent),
            contextlib.redirect_stdout(io.StringIO()),
            self.assertLogs(mal.logger, "WARNING") as logg,
        ):
            kode = mal.main()
        return kode, logg.output

    def test_alle_flater_og_krav_holder_gir_0(self):
        # Én 3 × 3-blokk i grunnfargen til hver flate, så også myr har en indre hvit piksel.
        blokker = [mal.hex_til_rgb(f.grunnfarge) for fl in mal.FLATER.values() for f in fl]
        rader = [[(*farge, 255) for farge in blokker for _ in range(3)] for _ in range(3)]
        png = lag_png(rader)
        with (
            mock.patch.object(mal, "hent", lambda url: png),
            contextlib.redirect_stdout(io.StringIO()) as ut,
            self.assertNoLogs(mal.logger, "WARNING"),
        ):
            self.assertEqual(mal.main(), 0)
        self.assertIn("## Kontrast", ut.getvalue())

    def test_brudd_gir_1(self):
        # Bare mørk skog på alle flisene: ruten er under 3:1, og de andre flatene mangler.
        png = lag_png([[(0x92, 0xA0, 0x56, 255)] * 4 for _ in range(4)])
        kode, logg = self._kjor(lambda url: png)
        self.assertEqual(kode, 1)
        self.assertTrue(any("map-route mot skog" in linje for linje in logg))
        self.assertTrue(any("vann ble ikke funnet" in linje for linje in logg))

    def test_feil_ved_henting_gir_1(self):
        def feiler(url):
            raise OSError("ingen nett")

        kode, logg = self._kjor(feiler)
        self.assertEqual(kode, 1)
        self.assertTrue(any("Målingen stoppet" in linje for linje in logg))
