"""`domene.tid`: estimert tid etter sveitsisk regel + 15 % (FR-3)."""

import unittest

from domene.tekst import formater_tid
from domene.tid import avrund_til_5, estimert_tid_min, ra_tid_min
from domene.tur import Form


class RaTidTest(unittest.TestCase):
    def test_leddene_summeres_og_far_15_prosent_paslag(self):  # FR-3
        self.assertAlmostEqual(ra_tid_min(1000, 0, 0), 15 * 1.15)
        self.assertAlmostEqual(ra_tid_min(0, 100, 0), 15 * 1.15)
        self.assertAlmostEqual(ra_tid_min(0, 0, 200), 15 * 1.15)

    def test_regneeksempelet_gir_142_3_min_ra_tid(self):  # FR-3
        # Hele turen: 6 km, 150 hm opp og 150 m ned.
        self.assertAlmostEqual(ra_tid_min(6000, 150, 150), 142.3125)
        self.assertEqual(f"{ra_tid_min(6000, 150, 150):.1f}", "142.3")


class AvrundingTest(unittest.TestCase):
    def test_avrunder_til_naermeste_5_minutter(self):  # FR-3
        self.assertEqual(avrund_til_5(142.3125), 140)
        self.assertEqual(avrund_til_5(143), 145)
        self.assertEqual(avrund_til_5(0), 0)

    def test_halv_runder_opp(self):  # FR-3
        self.assertEqual(avrund_til_5(137.5), 140)
        # round() ville gitt 140 her (28,5 → 28), men halv opp gir 145.
        self.assertEqual(avrund_til_5(142.5), 145)


class EstimertTidTest(unittest.TestCase):
    def test_regneeksempelet_gir_140_og_ca_2_t_20_min(self):  # FR-3
        tid = estimert_tid_min(Form.TUR_RETUR, 3000, 150, 0)
        self.assertEqual(tid, 140)
        self.assertEqual(formater_tid(tid), "ca. 2 t 20 min")

    def test_tur_retur_bytter_opp_og_ned_tilbake(self):  # FR-3
        # Én vei 2 km, 100 hm opp, 40 m ned → totalt 4 km, 140 opp, 140 ned.
        self.assertEqual(
            estimert_tid_min(Form.TUR_RETUR, 2000, 100, 40),
            avrund_til_5(ra_tid_min(4000, 140, 140)),
        )

    def test_rundtur_regnes_pa_de_lagrede_verdiene(self):  # FR-3
        self.assertEqual(
            estimert_tid_min(Form.RUNDTUR, 6000, 150, 150),
            avrund_til_5(ra_tid_min(6000, 150, 150)),
        )

    def test_rundtur_med_ulik_opp_og_ned(self):  # FR-3
        # (90 + 45 + 7,5) × 1,15 = 142,5 × 1,15 = 163,875 → 165.
        self.assertEqual(estimert_tid_min(Form.RUNDTUR, 6000, 300, 100), 165)

    def test_eksakt_halv_fra_heltallsverdier_runder_opp(self):  # FR-3
        # 10 km rundtur gir 150 × 1,15 = 172,5 min, som skal bli 175. round(172.5 / 5) * 5
        # ville gitt 170, fordi round() runder 34,5 til nærmeste partall.
        self.assertEqual(estimert_tid_min(Form.RUNDTUR, 10_000, 0, 0), 175)
