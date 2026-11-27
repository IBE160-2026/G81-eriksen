import unittest
from datetime import UTC, datetime, timedelta

from domene.innlogging import er_sperret

NA = datetime(2026, 11, 27, 12, 0, tzinfo=UTC)


def for_siden(minutter):
    return NA - timedelta(minutes=minutter)


class ErSperretTest(unittest.TestCase):  # AR-2, NFR-8
    def test_tom_liste_er_ikke_sperret(self):
        self.assertFalse(er_sperret([], NA, 5, 15))

    def test_fire_forsok_er_ikke_sperret_fem_er(self):
        self.assertFalse(er_sperret([for_siden(1)] * 4, NA, 5, 15))
        self.assertTrue(er_sperret([for_siden(1)] * 5, NA, 5, 15))

    def test_forsok_pa_akkurat_sperretiden_teller_ikke(self):
        self.assertFalse(er_sperret([for_siden(15)] + [for_siden(1)] * 4, NA, 5, 15))
        self.assertTrue(er_sperret([for_siden(14.9)] + [for_siden(1)] * 4, NA, 5, 15))

    def test_gamle_forsok_teller_ikke(self):
        self.assertFalse(er_sperret([for_siden(60)] * 10, NA, 5, 15))

    def test_lav_grense(self):
        self.assertTrue(er_sperret([for_siden(1)], NA, 1, 15))
        self.assertFalse(er_sperret([for_siden(1)] * 2, NA, 3, 2))
