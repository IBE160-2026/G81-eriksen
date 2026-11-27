"""`domene.begrunnelse.reservebegrunnelse` (FR-12, FR-13). Ingen database."""

import inspect
import unittest
from datetime import date

from domene.begrunnelse import (
    MAKS_TEGN,
    historikkbegrunnelse,
    personaliseringssetning,
    reservebegrunnelse,
)
from domene.niva import Sperre
from domene.sok import Sok
from domene.tekst import nivaord, varighetsvalg
from domene.tur import NIVAREKKEFOLGE, TURTYPER, Turniva
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


class HistorikkbegrunnelseTest(unittest.TestCase):
    def test_mal(self):  # FR-17
        self.assertEqual(
            historikkbegrunnelse(date(2026, 10, 12), 5),
            "Du gikk denne turen 12. oktober og ga den 5 av 5.",
        )

    def test_alle_datoer_og_vurderinger_under_grensen(self):  # FR-12
        for maned in range(1, 13):
            for n in range(1, 6):
                self.assertLessEqual(len(historikkbegrunnelse(date(2026, maned, 28), n)), MAKS_TEGN)


G, B, R, S = Turniva.GRONN, Turniva.BLA, Turniva.ROD, Turniva.SVART


class PersonaliseringssetningTest(unittest.TestCase):
    def test_heving(self):  # FR-12, FR-19
        self.assertEqual(
            personaliseringssetning(B, B, True, None),
            "Du får en blå tur fordi de tre siste grønne turene var lette for deg.",
        )
        self.assertEqual(
            personaliseringssetning(R, R, True, None),
            "Du får en rød tur fordi de tre siste blå turene var lette for deg.",
        )
        self.assertEqual(
            personaliseringssetning(S, S, True, None),
            "Du får en svart tur fordi de tre siste røde turene var lette for deg.",
        )

    def test_nadd_niva(self):  # FR-12
        self.assertEqual(
            personaliseringssetning(B, B, False, None),
            "Du får en blå tur fordi du har nådd blått nivå.",
        )
        # Heving, men turen er under taket: «de tre siste» ville vært feil.
        self.assertEqual(
            personaliseringssetning(B, R, True, None),
            "Du får en blå tur fordi du har nådd blått nivå.",
        )

    def test_sperre(self):  # FR-12, FR-19
        self.assertEqual(
            personaliseringssetning(G, G, False, Sperre(G, B)),
            "Du får en grønn tur igjen fordi den siste blå turen føltes vanskelig.",
        )
        self.assertEqual(
            personaliseringssetning(B, B, True, Sperre(B, S)),
            "Du får en blå tur igjen fordi den siste svarte turen føltes vanskelig.",
        )

    def test_ingen_setning_for_gronn_tur_uten_sperre(self):  # FR-12
        self.assertEqual(personaliseringssetning(G, G, False, None), "")
        self.assertEqual(personaliseringssetning(G, B, True, None), "")

    def test_nivaord_boyning(self):  # AR-16
        forventet = {
            G: ("grønn", "grønne", "grønt"),
            B: ("blå", "blå", "blått"),
            R: ("rød", "røde", "rødt"),
            S: ("svart", "svarte", "svart"),
        }
        for niva, (m, bestemt, n) in forventet.items():
            self.assertEqual(
                (nivaord(niva), nivaord(niva, "bestemt"), nivaord(niva, "intetkjonn")),
                (m, bestemt, n),
            )

    def test_ingen_tall_i_setningene(self):  # FR-12
        for tur in NIVAREKKEFOLGE:
            for tak in NIVAREKKEFOLGE:
                for sperre in (None, Sperre(G, B)):
                    setning = personaliseringssetning(tur, tak, True, sperre)
                    self.assertFalse(any(t.isdigit() for t in setning))

    def test_hele_begrunnelsen_hoyst_300_tegn(self):  # FR-12
        tur_typer = TURTYPER
        for tur_niva in NIVAREKKEFOLGE:
            for tak in NIVAREKKEFOLGE:
                for heving in (False, True):
                    for sperre in (
                        None,
                        *(Sperre(n, s) for n in NIVAREKKEFOLGE for s in NIVAREKKEFOLGE),
                    ):
                        setning = personaliseringssetning(tur_niva, tak, heving, sperre)
                        for minutter, _ in varighetsvalg():
                            for turtype in (None, *TURTYPER):
                                tur = lag_tur(estimert_tid_min=715, turtyper=tur_typer)
                                mal = reservebegrunnelse(Sok(minutter, DATO, turtype=turtype), tur)
                                self.assertLessEqual(len(f"{mal} {setning}"), MAKS_TEGN)
