"""`domene.sok`: søket og valideringen av det (FR-5)."""

import unittest
from dataclasses import FrozenInstanceError, replace
from datetime import date, datetime

from domene.sok import MAKS_VARIGHET_MIN, MIN_VARIGHET_MIN, VARIGHET_STEG_MIN, Sok
from domene.tur import TURTYPER

DATO = date(2026, 11, 26)


class SokTest(unittest.TestCase):
    def test_grensene_er_1_til_12_timer_i_halvtimessteg(self):  # FR-5, beslutning 4 og 5
        self.assertEqual(MIN_VARIGHET_MIN, 60)
        self.assertEqual(MAKS_VARIGHET_MIN, 720)
        self.assertEqual(VARIGHET_STEG_MIN, 30)

    def test_standardverdiene_er_ingen_turtype_og_intet_startpunkt(self):  # FR-5
        sok = Sok(varighet_min=180, dato=DATO)
        self.assertIsNone(sok.turtype)
        self.assertIsNone(sok.startpunkt_id)

    def test_alle_varigheter_fra_60_til_720_i_steg_pa_30_godtas(self):  # FR-5
        varigheter = range(MIN_VARIGHET_MIN, MAKS_VARIGHET_MIN + 1, VARIGHET_STEG_MIN)
        self.assertEqual(len(varigheter), 23)
        for varighet in varigheter:
            with self.subTest(varighet=varighet):
                self.assertEqual(Sok(varighet_min=varighet, dato=DATO).varighet_min, varighet)

    def test_alle_turtyper_og_et_startpunkt_godtas(self):  # FR-5
        for turtype in TURTYPER:
            with self.subTest(turtype=turtype):
                sok = Sok(180, DATO, turtype=turtype, startpunkt_id="sorkedalen")
                self.assertEqual(sok.turtype, turtype)
                self.assertEqual(sok.startpunkt_id, "sorkedalen")

    def test_sok_er_frosset_og_kan_endres_med_replace(self):  # FR-5
        sok = Sok(180, DATO)
        with self.assertRaises(FrozenInstanceError):
            sok.varighet_min = 210
        self.assertEqual(replace(sok, varighet_min=210), Sok(210, DATO))

    def test_replace_valideres_ogsa(self):  # FR-5
        with self.assertRaises(ValueError):
            replace(Sok(180, DATO), varighet_min=45)

    def test_ugyldig_varighet_gir_valueerror(self):  # FR-5, matrisen: ugyldig søk
        for varighet in (45, 75, 750, 0, 30, 705, -60, 180.0, "180", True, None):
            with self.subTest(varighet=varighet):
                with self.assertRaisesRegex(ValueError, "Varigheten"):
                    Sok(varighet_min=varighet, dato=DATO)

    def test_ukjent_turtype_gir_valueerror(self):  # FR-5, matrisen: ugyldig søk
        for turtype in ("fjell", "", "Topptur"):
            with self.subTest(turtype=turtype):
                with self.assertRaisesRegex(ValueError, "Ukjent turtype"):
                    Sok(180, DATO, turtype=turtype)

    def test_tomt_startpunkt_gir_valueerror(self):  # FR-5, matrisen: ugyldig søk
        for startpunkt_id in ("", "   ", " sorkedalen ", "sorkedalen ", 7):
            with self.subTest(startpunkt_id=startpunkt_id):
                with self.assertRaisesRegex(ValueError, "tekst som ikke er tom"):
                    Sok(180, DATO, startpunkt_id=startpunkt_id)

    def test_dato_ma_vaere_en_date(self):  # FR-5
        for dato in ("2026-11-26", None, datetime(2026, 11, 26, 12, 0)):
            with self.subTest(dato=dato):
                with self.assertRaisesRegex(ValueError, "Datoen"):
                    Sok(180, dato)
