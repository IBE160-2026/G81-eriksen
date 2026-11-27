"""KI-dataklassene har bare de tillatte feltene (NFR-5, FR-13)."""

import unittest
from dataclasses import fields, is_dataclass

from domene.ki import KiSok, KiSvar, KiTur


class KiDataTest(unittest.TestCase):
    def test_felt_er_fast_liste(self):  # NFR-5
        self.assertEqual(
            [f.name for f in fields(KiSok)],
            ["varighet_min", "dato", "turtype", "startpunkt_id"],
        )
        self.assertEqual([f.name for f in fields(KiTur)], ["id", "navn", "turtyper", "form"])

    def test_er_frosne(self):
        for klasse in (KiSok, KiTur, KiSvar):
            self.assertTrue(is_dataclass(klasse))
            self.assertTrue(klasse.__dataclass_params__.frozen)

    def test_svar_ok(self):
        self.assertTrue(KiSvar(tekst="x").ok)
        self.assertFalse(KiSvar(arsak="feil").ok)
