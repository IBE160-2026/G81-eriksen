"""`domene.gradering`: turnivå etter Merkehåndboka (FR-2, AR-19)."""

import unittest

from domene.gradering import turniva
from domene.tur import Turniva


class GraderingTest(unittest.TestCase):
    def test_under_alle_gronne_grenser_er_gronn(self):  # FR-2
        self.assertIs(turniva(4900, 299), Turniva.GRONN)

    def test_verdi_pa_gronn_grense_graderes_opp_til_bla(self):  # FR-2, AR-19
        self.assertIs(turniva(5000, 0), Turniva.BLA)
        self.assertIs(turniva(0, 300), Turniva.BLA)

    def test_verdi_pa_bla_grense_gir_rod(self):  # FR-2, AR-19
        self.assertIs(turniva(10_000, 0), Turniva.ROD)
        self.assertIs(turniva(0, 600), Turniva.ROD)

    def test_verdi_pa_rod_grense_gir_svart(self):  # FR-2, AR-19
        self.assertIs(turniva(20_000, 0), Turniva.SVART)
        self.assertIs(turniva(0, 1000), Turniva.SVART)

    def test_strengeste_av_lengde_og_hoydemeter_vinner(self):  # FR-2
        self.assertIs(turniva(3000, 650), Turniva.ROD)
        self.assertIs(turniva(12_000, 100), Turniva.ROD)

    def test_graderer_lagrede_verdier_for_en_vei_ved_tur_retur(self):  # FR-2
        # turniva() tar ingen form; den graderer de lagrede verdiene, som er én vei ved tur-retur.
        # Tur-retur med 3 km én vei (6 km totalt) og 150 hm er grønn, ikke blå.
        self.assertIs(turniva(3000, 150), Turniva.GRONN)

    def test_graderer_lagrede_verdier_for_hele_runden_ved_rundtur(self):  # FR-2
        # turniva() tar ingen form; ved rundtur er de lagrede verdiene hele runden.
        # Rundtur på 6 km lagres som hele runden og blir blå.
        self.assertIs(turniva(6000, 150), Turniva.BLA)
