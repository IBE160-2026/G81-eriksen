"""`domene.okt`: søketilstanden i økten og «Nytt forslag» (AD-5, FR-7). Ingen database."""

import json
import unittest
from dataclasses import FrozenInstanceError
from datetime import date

from domene.niva import Sperre
from domene.okt import (
    Soketilstand,
    alle_vist,
    neste_forslag,
    ny_soketilstand,
    start_pa_nytt,
)
from domene.sok import Sok
from domene.tur import Turniva
from domene.utvalg import Status, Utvalg

SOK = Sok(150, date(2026, 11, 28), turtype="utsikt", startpunkt_id="asen")


def tilstand(**endringer) -> Soketilstand:
    verdier = {
        "sok": SOK,
        "status": Status.TREFF,
        "rangerte_tur_ider": ("a", "b", "c"),
        "viste_tur_ider": ("a",),
        "gjeldende_tur_id": "a",
    }
    verdier.update(endringer)
    return Soketilstand(**verdier)


class SoketilstandTest(unittest.TestCase):
    def test_standardverdier(self):  # AD-5
        ny = Soketilstand(SOK, Status.INGEN_TREFF, ())
        self.assertEqual(ny.viste_tur_ider, ())
        self.assertIsNone(ny.gjeldende_tur_id)
        self.assertIs(ny.nivaheving, False)

    def test_er_frosset(self):  # AD-5
        with self.assertRaises(FrozenInstanceError):
            tilstand().gjeldende_tur_id = "b"

    def test_til_dict_har_dato_som_iso_og_kan_bli_json(self):  # AD-5
        data = tilstand().til_dict()
        self.assertEqual(
            data,
            {
                "sok": {
                    "varighet_min": 150,
                    "dato": "2026-11-28",
                    "turtype": "utsikt",
                    "startpunkt_id": "asen",
                },
                "status": "treff",
                "rangerte_tur_ider": ["a", "b", "c"],
                "viste_tur_ider": ["a"],
                "gjeldende_tur_id": "a",
                "nivaheving": False,
                "nivatak": "gronn",
                "grunnniva": "gronn",
                "sperre": None,
                "har_historikk": False,
            },
        )
        self.assertEqual(json.loads(json.dumps(data)), data)

    def test_grunnlaget_for_begrunnelsen_gar_gjennom_json(self):  # FR-12, AD-5
        original = tilstand(
            nivatak=Turniva.GRONN,
            grunnniva=Turniva.BLA,
            sperre=Sperre(Turniva.GRONN, Turniva.BLA),
            har_historikk=True,
        )
        data = json.loads(json.dumps(original.til_dict()))
        self.assertEqual(data["sperre"], {"niva": "gronn", "turniva": "bla"})
        self.assertEqual(Soketilstand.fra_dict(data), original)

    def test_eldre_okt_uten_grunnlaget_leses_med_standard(self):  # NFR-2
        data = tilstand().til_dict()
        for felt in ("grunnniva", "sperre", "har_historikk"):
            del data[felt]
        lest = Soketilstand.fra_dict(data)
        self.assertEqual(
            (lest.grunnniva, lest.sperre, lest.har_historikk), (Turniva.GRONN, None, False)
        )

    def test_ugyldig_sperre_gir_value_error(self):  # NFR-2
        data = tilstand().til_dict()
        data["sperre"] = {"niva": "lilla", "turniva": "bla"}
        with self.assertRaises(ValueError):
            Soketilstand.fra_dict(data)
        data["sperre"] = {"niva": "gronn"}
        with self.assertRaises(ValueError):
            Soketilstand.fra_dict(data)

    def test_nivatak_gar_gjennom_json(self):  # FR-19
        original = tilstand(nivatak=Turniva.BLA, nivaheving=True)
        tilbake = Soketilstand.fra_dict(json.loads(json.dumps(original.til_dict())))
        self.assertEqual(tilbake.nivatak, Turniva.BLA)
        self.assertIs(type(tilbake.nivatak), Turniva)

    def test_rundtur_gjennom_json(self):  # AD-5
        for original in (
            tilstand(),
            tilstand(nivaheving=True, status=Status.TOPPTUR_ERSTATTET),
            Soketilstand(Sok(60, date(2026, 12, 1)), Status.INGEN_TREFF, ()),
        ):
            with self.subTest(original=original):
                tilbake = Soketilstand.fra_dict(json.loads(json.dumps(original.til_dict())))
                self.assertEqual(tilbake, original)
                self.assertIs(type(tilbake.status), Status)
                self.assertIsInstance(tilbake.rangerte_tur_ider, tuple)

    def test_fra_dict_taaler_manglende_og_ukjente_felt(self):  # AD-5 (KI-felt kommer i 4.5)
        data = tilstand().til_dict()
        for felt in ("viste_tur_ider", "gjeldende_tur_id", "nivaheving", "nivatak"):
            del data[felt]
        data["ki_begrunnelse"] = "Kommer i Epic 4"
        data["sok"]["fritekst"] = "forbi et vann"
        del data["sok"]["turtype"]
        tilbake = Soketilstand.fra_dict(data)
        self.assertEqual(tilbake.viste_tur_ider, ())
        self.assertIsNone(tilbake.gjeldende_tur_id)
        self.assertIs(tilbake.nivaheving, False)
        self.assertEqual(tilbake.nivatak, Turniva.GRONN)  # FR-19: eldre økt leses med grønt tak
        self.assertIsNone(tilbake.sok.turtype)

    def test_ugyldige_verdier_gir_value_error(self):  # AD-5, NFR-2
        gyldig = tilstand().til_dict()
        ugyldige = [
            {},
            {"sok": "tekst"},
            {**gyldig, "status": "ukjent"},
            {**gyldig, "sok": {**gyldig["sok"], "dato": "i går"}},
            {**gyldig, "sok": {**gyldig["sok"], "dato": 20261128}},
            {**gyldig, "sok": {**gyldig["sok"], "varighet_min": 45}},
            {**gyldig, "sok": {**gyldig["sok"], "turtype": "fjell"}},
            {**gyldig, "rangerte_tur_ider": "abc"},
            {**gyldig, "rangerte_tur_ider": [1, 2]},
            {**gyldig, "gjeldende_tur_id": 7},
        ]
        for data in ugyldige:
            with self.subTest(data=data), self.assertRaises(ValueError):
                Soketilstand.fra_dict(data)


class NySoketilstandTest(unittest.TestCase):
    def test_forste_tur_er_gjeldende_og_vist(self):  # FR-7
        ny = ny_soketilstand(SOK, Utvalg(Status.TREFF, ("x", "y")))
        self.assertEqual(ny.rangerte_tur_ider, ("x", "y"))
        self.assertEqual(ny.gjeldende_tur_id, "x")
        self.assertEqual(ny.viste_tur_ider, ("x",))
        self.assertEqual(ny.status, Status.TREFF)

    def test_uten_turer(self):  # FR-8
        ny = ny_soketilstand(SOK, Utvalg(Status.BARE_OVER_NIVATAK, ()))
        self.assertIsNone(ny.gjeldende_tur_id)
        self.assertEqual(ny.viste_tur_ider, ())


def alle_gyldige(_tur_id: str) -> bool:
    return True


class NesteForslagTest(unittest.TestCase):
    """Matrisen i spec 1.11 (FR-7, NFR-2): rene funksjoner, aldri ny rangering."""

    def test_neste(self):  # FR-7
        ny = neste_forslag(tilstand(), "a", alle_gyldige)
        self.assertEqual(ny.gjeldende_tur_id, "b")
        self.assertEqual(ny.viste_tur_ider, ("a", "b"))
        self.assertEqual(ny.rangerte_tur_ider, ("a", "b", "c"))
        self.assertFalse(alle_vist(ny))

    def test_rekkefolge_uten_gjentakelse(self):  # FR-7
        naa = tilstand()
        viste = [naa.gjeldende_tur_id]
        while naa.gjeldende_tur_id is not None:
            naa = neste_forslag(naa, naa.gjeldende_tur_id, alle_gyldige)
            viste.append(naa.gjeldende_tur_id)
        self.assertEqual(viste, ["a", "b", "c", None])

    def test_siste_gir_alle_vist(self):  # FR-7
        siste = tilstand(viste_tur_ider=("a", "b", "c"), gjeldende_tur_id="c")
        ny = neste_forslag(siste, "c", alle_gyldige)
        self.assertIsNone(ny.gjeldende_tur_id)
        self.assertEqual(ny.viste_tur_ider, ("a", "b", "c"))
        self.assertTrue(alle_vist(ny))
        self.assertEqual(ny.status, Status.TREFF)

    def test_dobbeltklikk_gaar_bare_ett_steg(self):  # FR-7, NFR-2
        naa = tilstand(viste_tur_ider=("a", "b"), gjeldende_tur_id="b")
        self.assertEqual(neste_forslag(naa, "a", alle_gyldige), naa)

    def test_manipulert_tur_gir_ingen_endring(self):  # NFR-2
        for fra in (None, "", "x", "c"):
            with self.subTest(fra=fra):
                self.assertEqual(neste_forslag(tilstand(), fra, alle_gyldige), tilstand())

    def test_uten_gjeldende_tur_gir_ingen_endring(self):  # FR-7, FR-8
        for naa in (
            tilstand(viste_tur_ider=("a", "b", "c"), gjeldende_tur_id=None),
            Soketilstand(SOK, Status.INGEN_TREFF, ()),
        ):
            with self.subTest(naa=naa):
                self.assertEqual(neste_forslag(naa, None, alle_gyldige), naa)

    def test_en_tur(self):  # FR-7
        en = tilstand(rangerte_tur_ider=("a",))
        ny = neste_forslag(en, "a", alle_gyldige)
        self.assertIsNone(ny.gjeldende_tur_id)
        self.assertTrue(alle_vist(ny))

    def test_borte_tur_hoppes_over_og_markeres_som_vist(self):  # FR-7, SM-C1
        ny = neste_forslag(tilstand(), "a", lambda tur_id: tur_id != "b")
        self.assertEqual(ny.gjeldende_tur_id, "c")
        self.assertEqual(ny.viste_tur_ider, ("a", "b", "c"))

    def test_alle_resterende_borte_gir_alle_vist(self):  # FR-7, SM-C1
        ny = neste_forslag(tilstand(), "a", lambda tur_id: tur_id == "a")
        self.assertIsNone(ny.gjeldende_tur_id)
        self.assertEqual(ny.viste_tur_ider, ("a", "b", "c"))
        self.assertTrue(alle_vist(ny))

    def test_gyldig_kalles_bare_for_turer_som_ikke_er_vist(self):  # FR-7
        kalt = []
        neste_forslag(tilstand(), "a", lambda tur_id: kalt.append(tur_id) or True)
        self.assertEqual(kalt, ["b"])


class AlleVistTest(unittest.TestCase):
    def test_bare_ved_treff_uten_gjeldende_og_alle_vist(self):  # FR-7
        ferdig = {"viste_tur_ider": ("a", "b", "c"), "gjeldende_tur_id": None}
        self.assertTrue(alle_vist(tilstand(**ferdig)))
        self.assertTrue(alle_vist(tilstand(**ferdig, status=Status.TOPPTUR_ERSTATTET)))
        self.assertFalse(alle_vist(tilstand()))
        self.assertFalse(alle_vist(tilstand(viste_tur_ider=("a", "b"), gjeldende_tur_id=None)))
        self.assertFalse(alle_vist(Soketilstand(SOK, Status.INGEN_TREFF, ())))
        self.assertFalse(alle_vist(Soketilstand(SOK, Status.BARE_OVER_NIVATAK, ())))


class StartPaNyttTest(unittest.TestCase):
    def test_start_paa_nytt_fra_alle_vist(self):  # FR-7
        ferdig = tilstand(viste_tur_ider=("a", "b", "c"), gjeldende_tur_id=None)
        ny = start_pa_nytt(ferdig)
        self.assertEqual(ny.gjeldende_tur_id, "a")
        self.assertEqual(ny.viste_tur_ider, ("a",))
        self.assertEqual(ny.rangerte_tur_ider, ("a", "b", "c"))

    def test_ellers_ingen_endring(self):  # FR-7, NFR-2: dobbeltklikk og manipulerte POST-er
        for naa in (
            tilstand(),
            tilstand(viste_tur_ider=("a", "b"), gjeldende_tur_id="b"),
            Soketilstand(SOK, Status.INGEN_TREFF, ()),
        ):
            with self.subTest(naa=naa):
                self.assertEqual(start_pa_nytt(naa), naa)
