"""`domene.tekst`: faste norske formater for tid, lengde og nivå (UX-DR31, AR-16)."""

import unittest

from domene.tekst import formater_lengde_totalt, formater_niva, formater_tid
from domene.tur import Turniva


class FormaterTidTest(unittest.TestCase):
    def test_timer_og_minutter(self):  # FR-3, UX-DR31
        self.assertEqual(formater_tid(95), "ca. 1 t 35 min")

    def test_bare_minutter(self):  # FR-3, UX-DR31
        self.assertEqual(formater_tid(45), "ca. 45 min")

    def test_hele_timer(self):  # FR-3, UX-DR31
        self.assertEqual(formater_tid(120), "ca. 2 t")


class FormaterLengdeTest(unittest.TestCase):
    def test_en_desimal_med_desimalkomma(self):  # UX-DR31, AR-16
        self.assertEqual(formater_lengde_totalt(3500), "3,5 km totalt")

    def test_hele_km_uten_komma_null(self):  # UX-DR31, AR-16
        self.assertEqual(formater_lengde_totalt(6000), "6 km totalt")

    def test_avrunding_til_hel_km_droppes_komma_null(self):  # UX-DR31, AR-16
        self.assertEqual(formater_lengde_totalt(5960), "6 km totalt")

    def test_halv_runder_opp(self):  # UX-DR31, AR-16
        self.assertEqual(formater_lengde_totalt(3450), "3,5 km totalt")
        self.assertEqual(formater_lengde_totalt(3449), "3,4 km totalt")


class FormaterNivaTest(unittest.TestCase):
    def test_alle_nivaer_med_tankestrek(self):  # FR-2, UX-DR31
        self.assertEqual(formater_niva(Turniva.GRONN), "Grønn – lett")
        self.assertEqual(formater_niva(Turniva.BLA), "Blå – moderat")
        self.assertEqual(formater_niva(Turniva.ROD), "Rød – moderat")
        self.assertEqual(formater_niva(Turniva.SVART), "Svart – vanskelig")
