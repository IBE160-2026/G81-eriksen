"""Ren grenseavgjørelse for KI-kall: time, døgn, tidsskifte (FR-13, NFR-8)."""

import unittest
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from domene.ki_grense import behold_siste_time, kan_sende_ki

OSLO = ZoneInfo("Europe/Oslo")
UTC = ZoneInfo("UTC")
NA = datetime(2026, 12, 1, 12, 0, tzinfo=OSLO)


def nylige(n):
    return [NA - timedelta(minutes=1 + i) for i in range(n)]


def kan(tidspunkter, i_dag=0, na=NA):
    return kan_sende_ki(tidspunkter, i_dag, na, 20, 200)


class KanSendeKiTest(unittest.TestCase):
    def test_19_siste_time(self):
        self.assertTrue(kan(nylige(19)))

    def test_20_siste_time(self):
        self.assertFalse(kan(nylige(20)))

    def test_noyaktig_60_min_teller_ikke(self):
        tider = nylige(19) + [NA - timedelta(minutes=60)]
        self.assertTrue(kan(tider))
        self.assertEqual(len(behold_siste_time(tider, NA)), 19)

    def test_59_min_59_sek_teller(self):
        tider = nylige(19) + [NA - timedelta(minutes=59, seconds=59)]
        self.assertFalse(kan(tider))

    def test_199_i_dag_og_200(self):
        self.assertTrue(kan([], 199))
        self.assertFalse(kan([], 200))
        self.assertFalse(kan([], 201))

    def test_tomt(self):
        self.assertTrue(kan([]))

    def test_tidspunkter_i_annen_sone(self):
        utc = [t.astimezone(UTC) for t in nylige(20)]
        self.assertFalse(kan(utc))

    def test_dato_er_oslo_kalenderdato_rundt_tidsskifte(self):
        # 2026-10-25 (til vintertid) og 2026-03-29 (til sommertid)
        for na_utc, ventet in (
            (datetime(2026, 10, 24, 22, 30, tzinfo=UTC), (10, 25)),  # 00.30 CEST
            (datetime(2026, 10, 25, 22, 30, tzinfo=UTC), (10, 25)),  # 23.30 CET
            (datetime(2026, 10, 25, 23, 30, tzinfo=UTC), (10, 26)),  # 00.30 CET
            (datetime(2026, 3, 28, 22, 30, tzinfo=UTC), (3, 28)),  # 23.30 CET
            (datetime(2026, 3, 28, 23, 30, tzinfo=UTC), (3, 29)),  # 00.30 CET
            (datetime(2026, 3, 29, 21, 30, tzinfo=UTC), (3, 29)),  # 23.30 CEST
            (datetime(2026, 3, 29, 22, 30, tzinfo=UTC), (3, 30)),  # 00.30 CEST
        ):
            with self.subTest(na=na_utc):
                dato = na_utc.astimezone(OSLO).date()
                self.assertEqual((dato.month, dato.day), ventet)
