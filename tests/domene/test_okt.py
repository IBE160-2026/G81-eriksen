"""`domene.okt.Soketilstand`: søketilstanden i økten (AD-5, FR-7). Ingen database."""

import json
import unittest
from dataclasses import FrozenInstanceError
from datetime import date

from domene.okt import Soketilstand, ny_soketilstand
from domene.sok import Sok
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
            },
        )
        self.assertEqual(json.loads(json.dumps(data)), data)

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
        for felt in ("viste_tur_ider", "gjeldende_tur_id", "nivaheving"):
            del data[felt]
        data["ki_begrunnelse"] = "Kommer i Epic 4"
        data["sok"]["fritekst"] = "forbi et vann"
        del data["sok"]["turtype"]
        tilbake = Soketilstand.fra_dict(data)
        self.assertEqual(tilbake.viste_tur_ider, ())
        self.assertIsNone(tilbake.gjeldende_tur_id)
        self.assertIs(tilbake.nivaheving, False)
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
