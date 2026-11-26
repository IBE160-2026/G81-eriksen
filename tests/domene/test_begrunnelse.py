"""`domene.begrunnelse.reservebegrunnelse` (FR-12, FR-13). Ingen database."""

import inspect
import unittest
from datetime import date

from domene.begrunnelse import MAKS_TEGN, reservebegrunnelse
from domene.sok import Sok
from domene.tekst import varighetsvalg
from domene.tur import TURTYPER
from tests.domene.test_utvalg import lag_tur

DATO = date(2026, 11, 28)


class ReservebegrunnelseTest(unittest.TestCase):
    def test_med_turtype(self):  # FR-12, FR-13
        tur = lag_tur(estimert_tid_min=120, turtyper=("utsikt",))
        self.assertEqual(
            reservebegrunnelse(Sok(150, DATO, turtype="utsikt"), tur),
            "Turen tar ca. 2 t og passer innenfor 2,5 timer. Den har utsikt, som du ba om.",
        )

    def test_uten_turtype_nevner_varigheten(self):  # FR-12
        tur = lag_tur(estimert_tid_min=95, turtyper=("utsikt",))
        self.assertEqual(
            reservebegrunnelse(Sok(120, DATO), tur),
            "Turen tar ca. 1 t 35 min og passer innenfor 2 timer.",
        )

    def test_en_time_i_entall(self):  # UX-DR31
        self.assertIn(
            "innenfor 1 time.", reservebegrunnelse(Sok(60, DATO), lag_tur(estimert_tid_min=45))
        )

    def test_alle_turtyper(self):  # FR-12
        tur = lag_tur(turtyper=TURTYPER)
        forventet = {
            "marka": "Den går i marka, som du ba om.",
            "utsikt": "Den har utsikt, som du ba om.",
            "topptur": "Den går til en topp, som du ba om.",
        }
        for turtype, setning in forventet.items():
            with self.subTest(turtype=turtype):
                self.assertTrue(
                    reservebegrunnelse(Sok(180, DATO, turtype=turtype), tur).endswith(setning)
                )

    def test_topptur_erstattet_lover_ikke_topptur(self):  # FR-8, FR-13
        tekst = reservebegrunnelse(Sok(150, DATO, turtype="topptur"), lag_tur(turtyper=("utsikt",)))
        self.assertNotIn("som du ba om", tekst)
        self.assertTrue(tekst.endswith("Ingen topptur passet, så den har utsikt i stedet."))

    def test_hoyst_300_tegn_for_alle_sok(self):  # FR-12
        tur = lag_tur(estimert_tid_min=715, turtyper=TURTYPER)
        for minutter, _ in varighetsvalg():
            for turtype in (None, *TURTYPER):
                with self.subTest(minutter=minutter, turtype=turtype):
                    self.assertLessEqual(
                        len(reservebegrunnelse(Sok(minutter, DATO, turtype=turtype), tur)),
                        MAKS_TEGN,
                    )
        self.assertEqual(MAKS_TEGN, 300)

    def test_nevner_aldri_fritekst(self):  # FR-13
        self.assertEqual(list(inspect.signature(reservebegrunnelse).parameters), ["sok", "tur"])
