import unicodedata
import unittest

from domene.begrunnelse import MAKS_TEGN
from domene.ki_validering import Forkastelse, valider_begrunnelse
from domene.tur import Form, Turniva
from domene.utvalg import Status
from tests.domene.test_utvalg import lag_tur, sok

GYLDIG = "Turen tar {tid}, så den passer innenfor {varighet}."


def valider(tekst, turtype=None, status=Status.TREFF, tillegg=(), **tur):
    return valider_begrunnelse(tekst, sok(120, turtype=turtype), lag_tur(**tur), status, tillegg)


class KiValideringTest(unittest.TestCase):
    def assert_forkastet(self, resultat, arsak):
        self.assertFalse(resultat.ok)
        self.assertIsNone(resultat.tekst)
        self.assertEqual(resultat.forkastelse, arsak)

    def test_mikrotekst_eksempelet(self):  # FR-12, FR-13
        tekst = (
            "Turen tar {tid}, så den passer innenfor {varighet}. Den har utsikt, som du ba om, "
            "og er {nivå}, som passer når du er ny."
        )
        r = valider(
            tekst, "utsikt", estimert_tid_min=95, turtyper=("utsikt",), turniva=Turniva.GRONN
        )
        self.assertTrue(r.ok)
        self.assertEqual(
            r.tekst,
            "Turen tar ca. 1 t 35 min, så den passer innenfor 2 timer. "
            "Den har utsikt, som du ba om, og er grønn, som passer når du er ny.",
        )

    def test_tom(self):  # FR-13
        for tekst in ("", "   ", "\n\t"):
            with self.subTest(tekst=tekst):
                self.assert_forkastet(valider(tekst), Forkastelse.TOM)

    def test_ugyldige_plassholdere(self):  # FR-13
        for tekst in (
            "Turen er {Tid} og {varighet}.",
            "Turen er {niva} og {varighet}.",
            "Turen koster {pris} og {varighet}.",
            "Turen {varighet} {",
            "Turen {varighet} }",
            "Turen tar {tid}.",
            "Turen {varighet} {{tid}}",
        ):
            with self.subTest(tekst=tekst):
                self.assert_forkastet(valider(tekst), Forkastelse.UGYLDIG)

    def test_samme_plassholder_flere_ganger(self):  # FR-12
        self.assertEqual(valider("{varighet} og {varighet}").tekst, "2 timer og 2 timer")

    def test_siffer(self):  # FR-12
        for tekst in ("2 timer", "5 km", "1,5", "tur ٣", "tur ²"):
            with self.subTest(tekst=tekst):
                self.assert_forkastet(valider(f"{{varighet}} {tekst}"), Forkastelse.SIFFER)

    def test_tallord(self):  # FR-12
        for ord_ in ("to", "Tolv", "halvtime", "en time", "ett minutt", "ei mil", "Hundre"):
            with self.subTest(ord=ord_):
                self.assert_forkastet(valider(f"{{varighet}} {ord_}."), Forkastelse.TALLORD)

    def test_lovlige_ord_med_tallord_inni(self):  # FR-12
        for ord_ in ("en fin tur", "toppen", "tiden", "en tur"):
            with self.subTest(ord=ord_):
                self.assertTrue(valider(f"{{varighet}} {ord_}.").ok)

    def test_nivaord(self):  # FR-12
        for ord_ in ("grønn", "Blått", "svarte", "RØDE"):
            with self.subTest(ord=ord_):
                self.assert_forkastet(valider(f"{{varighet}} {ord_}."), Forkastelse.NIVAORD)

    def test_delord_av_nivaord_er_lov(self):  # FR-12
        self.assertTrue(valider("{varighet} Svartkulp og blåbær.").ok)

    def test_innsatte_verdier_gir_ikke_forkasting(self):  # FR-12
        r = valider("{tid} {varighet} {lengde} {nivå}", turniva=Turniva.GRONN, form=Form.RUNDTUR)
        self.assertTrue(r.ok)
        self.assertEqual(r.tekst, "ca. 2 t 2 timer 3 km grønn")

    def test_turtype_mangler(self):  # FR-13
        for turtype in ("marka", "utsikt", "topptur"):
            with self.subTest(turtype=turtype):
                self.assert_forkastet(valider(GYLDIG, turtype), Forkastelse.TURTYPE)

    def test_turtype_som_delstreng(self):  # FR-13
        for turtype, ord_ in (
            ("marka", "Nordmarka"),
            ("utsikt", "utsikten"),
            ("topptur", "toppturer"),
        ):
            with self.subTest(turtype=turtype):
                self.assertTrue(valider(f"{{varighet}} {ord_}.", turtype).ok)

    def test_alle_turtyper_sjekkes_ikke(self):  # FR-13
        self.assertTrue(valider(GYLDIG).ok)

    def test_topptur_erstattet_krever_utsikt(self):  # FR-8, FR-13
        s = Status.TOPPTUR_ERSTATTET
        self.assert_forkastet(valider("{varighet} topptur.", "topptur", s), Forkastelse.TURTYPE)
        self.assertTrue(valider("{varighet} utsikt.", "topptur", s).ok)

    def test_lengde_300_og_301(self):  # FR-12
        for antall, ok in ((MAKS_TEGN, True), (MAKS_TEGN + 1, False)):
            with self.subTest(antall=antall):
                r = valider("{varighet} " + "a" * (antall - len("2 timer ")))
                self.assertEqual(r.ok, ok)
                if ok:
                    self.assertEqual(len(r.tekst), MAKS_TEGN)
                else:
                    self.assertEqual(r.forkastelse, Forkastelse.FOR_LANG)

    def test_tillegg_legges_til_og_teller(self):  # FR-12
        r = valider("{varighet}.", tillegg=("Første.", "", "Andre."))
        self.assertEqual(r.tekst, "2 timer. Første. Andre.")
        r = valider("{varighet} " + "a" * 270, tillegg=("b" * 30,))
        self.assertEqual(r.forkastelse, Forkastelse.FOR_LANG)

    def test_tillegg_sjekkes_ikke_for_tall_og_nivaord(self):  # FR-12
        self.assertTrue(valider("{varighet}.", tillegg=("Du får en grønn tur 3 ganger.",)).ok)

    def test_mellomrom_og_linjeskift_normaliseres(self):  # FR-12
        self.assertEqual(valider("  {varighet}\n\ner   fint.  ").tekst, "2 timer er fint.")

    def test_unicode_normalisering(self):  # FR-13
        dekomponert = unicodedata.normalize("NFD", "{varighet} og {nivå}.")
        self.assertNotEqual(dekomponert, "{varighet} og {nivå}.")
        self.assertEqual(valider(dekomponert).tekst, "2 timer og grønn.")

    def test_andre_tall_enn_siffer(self):  # FR-12
        for tegn in ("½", "Ⅻ"):
            with self.subTest(tegn=tegn):
                self.assert_forkastet(valider(f"{{varighet}} {tegn}."), Forkastelse.SIFFER)

    def test_usynlige_tegn_skjuler_ikke_ord(self):  # FR-12
        self.assert_forkastet(valider("{varighet} grøn​n."), Forkastelse.NIVAORD)
        self.assert_forkastet(valider("{varighet} t­o."), Forkastelse.TALLORD)

    def test_plassholder_limt_til_bokstaver(self):  # FR-13
        for tekst in ("{varighet} to{tid}", "{varighet} Sv{varighet}artkulp", "{varighet}a"):
            with self.subTest(tekst=tekst):
                self.assert_forkastet(valider(tekst), Forkastelse.UGYLDIG)
        self.assertTrue(valider("{varighet}, ({nivå}) {tid}.").ok)


if __name__ == "__main__":
    unittest.main()
