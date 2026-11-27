"""`velg_turer` med nivåtak og historikk (story 3.2, FR-5, FR-19, SM-C1). Ingen database."""

import unittest
from datetime import date

from domene.niva import NivaStatus, Registrering, Sperre, nivaheving, vurder_historikk
from domene.tur import Turniva
from domene.utvalg import Status, er_over_nivatak, foresla_endringer, velg_turer
from tests.domene.test_niva import BLA, GRONN, ROD, SVART, historikk, til_blatt
from tests.domene.test_utvalg import lag_tur, sok

NIVAER = (GRONN, BLA, ROD, SVART)


def turer_pa_alle_nivaer():
    return [lag_tur(id=f"t-{niva}", turniva=niva) for niva in NIVAER]


def gatt(tur_id, fornoydhet, dag=0, id=1):
    return Registrering(id, date(2026, 5, 1 + dag), tur_id, GRONN, "lett", fornoydhet)


def eksempler():
    """Sluttilstanden i hvert av de 12 eksemplene i FR-19."""
    gjentatt = [
        Registrering(i, date(2026, 1, i), "samme-tur", GRONN, "lett", 3) for i in range(1, 4)
    ]
    return {
        1: historikk((GRONN, "lett", 3)),
        2: historikk((GRONN, "lett"), (GRONN, "moderat")),
        3: historikk((GRONN, "lett", 3), (BLA, "lett", 2), (GRONN, "lett")),
        4: til_blatt((BLA, "lett", 2), (BLA, "vanskelig")),
        5: til_blatt((BLA, "lett", 2), (BLA, "vanskelig"), (GRONN, "lett")),
        6: til_blatt((BLA, "lett", 2), (BLA, "vanskelig"), (GRONN, "vanskelig")),
        7: til_blatt((BLA, "lett"), (GRONN, "vanskelig")),
        8: historikk((GRONN, "lett", 2), (GRONN, "vanskelig")),
        9: historikk((GRONN, "lett", 3), (BLA, "lett", 3), (BLA, "vanskelig")),
        10: til_blatt((ROD, "lett")),
        11: historikk((GRONN, "lett", 3), (BLA, "lett", 3), (ROD, "lett", 3), (SVART, "lett", 3)),
        12: gjentatt,
    }


class Fr19SluttilstandTest(unittest.TestCase):
    def test_ingen_tur_over_nivataket_i_noe_av_de_12_eksemplene(self):  # FR-19, SM-C1
        turer = turer_pa_alle_nivaer()
        for nummer, registreringer in eksempler().items():
            with self.subTest(eksempel=nummer):
                status = vurder_historikk(registreringer)
                plass = NIVAER.index(status.nivatak)
                utvalg = velg_turer(sok(180), turer, status.nivatak, registreringer=registreringer)
                self.assertEqual(utvalg.status, Status.TREFF)
                self.assertEqual(len(utvalg.rangerte_tur_ider), plass + 1)
                for tur_id in utvalg.rangerte_tur_ider:
                    self.assertLessEqual(NIVAER.index(Turniva(tur_id[2:])), plass)

    def test_bare_over_nivataket_nar_bare_slike_turer_passer(self):  # FR-19, SM-C1
        turer = [lag_tur(id="r", turniva=ROD), lag_tur(id="s", turniva=SVART)]
        for nummer, registreringer in eksempler().items():
            status = vurder_historikk(registreringer)
            if status.nivatak in (ROD, SVART):
                continue
            with self.subTest(eksempel=nummer):
                utvalg = velg_turer(sok(180), turer, status.nivatak, registreringer=registreringer)
                self.assertEqual(utvalg.status, Status.BARE_OVER_NIVATAK)
                self.assertEqual(utvalg.rangerte_tur_ider, ())


class RangeringTest(unittest.TestCase):
    def test_uten_nye_argumenter_er_utvalget_som_for(self):  # FR-5
        turer = [lag_tur(id="a", estimert_tid_min=60), lag_tur(id="b", estimert_tid_min=120)]
        self.assertEqual(velg_turer(sok(), turer, GRONN).rangerte_tur_ider, ("b", "a"))

    def test_ikke_gatt_foran_gatt(self):  # FR-5 punkt 1
        turer = [lag_tur(id="a", estimert_tid_min=170), lag_tur(id="b", estimert_tid_min=60)]
        utvalg = velg_turer(sok(), turer, GRONN, registreringer=[gatt("a", 5)])
        self.assertEqual(utvalg.rangerte_tur_ider, ("b", "a"))

    def test_gatt_med_hoy_fornoydhet_foran_lav(self):  # FR-5 punkt 1
        turer = [lag_tur(id=i, estimert_tid_min=120) for i in "abc"]
        regs = [gatt("a", 2, id=1), gatt("b", 3, id=2), gatt("c", 5, id=3)]
        utvalg = velg_turer(sok(), turer, GRONN, registreringer=regs)
        self.assertEqual(utvalg.rangerte_tur_ider, ("b", "c", "a"))

    def test_siste_registrering_avgjor_fornoydheten(self):  # FR-5 punkt 1
        turer = [lag_tur(id="a"), lag_tur(id="b")]
        regs = [gatt("a", 5, dag=0, id=2), gatt("a", 1, dag=1, id=1), gatt("b", 3, id=3)]
        utvalg = velg_turer(sok(), turer, GRONN, registreringer=regs)
        self.assertEqual(utvalg.rangerte_tur_ider, ("b", "a"))
        # Samme dato: høyeste id vinner.
        regs = [gatt("a", 5, id=2), gatt("a", 1, id=1), gatt("b", 3, id=3)]
        self.assertEqual(
            velg_turer(sok(), turer, GRONN, registreringer=regs).rangerte_tur_ider, ("a", "b")
        )

    def test_nivaheving_putter_turer_pa_taket_foran(self):  # FR-5 punkt 3
        turer = [lag_tur(id="g", turniva=GRONN, estimert_tid_min=170), lag_tur(id="b", turniva=BLA)]
        uten = velg_turer(sok(), turer, BLA)
        med = velg_turer(sok(), turer, BLA, nivaheving=True)
        self.assertEqual(uten.rangerte_tur_ider, ("g", "b"))
        self.assertEqual(med.rangerte_tur_ider, ("b", "g"))

    def test_ikke_gatt_gar_foran_nivaheving(self):  # FR-5 punkt 1 før 3
        turer = [lag_tur(id="g", turniva=GRONN), lag_tur(id="b", turniva=BLA)]
        utvalg = velg_turer(sok(), turer, BLA, registreringer=[gatt("b", 5)], nivaheving=True)
        self.assertEqual(utvalg.rangerte_tur_ider, ("g", "b"))

    def test_alle_gatt_er_fortsatt_treff(self):  # FR-5
        turer = [lag_tur(id="a"), lag_tur(id="b")]
        regs = [gatt("a", 1, id=1), gatt("b", 4, id=2)]
        utvalg = velg_turer(sok(), turer, GRONN, registreringer=regs)
        self.assertEqual(utvalg.status, Status.TREFF)
        self.assertEqual(set(utvalg.rangerte_tur_ider), {"a", "b"})

    def test_alle_utsiktsturer_gatt_gir_fortsatt_topptur_erstattet(self):  # FR-5, FR-8
        turer = [lag_tur(id="u", turtyper=("utsikt",))]
        utvalg = velg_turer(
            sok(turtype="topptur"), turer, GRONN, registreringer=[gatt("u", 2)], nivaheving=True
        )
        self.assertEqual(utvalg.status, Status.TOPPTUR_ERSTATTET)
        self.assertEqual(utvalg.rangerte_tur_ider, ("u",))

    def test_endringsforslag_bruker_nivataket(self):  # FR-8, FR-19
        turer = [lag_tur(id="b", turniva=BLA, estimert_tid_min=240)]
        self.assertEqual(foresla_endringer(sok(180), turer, GRONN), ())
        forslag = foresla_endringer(sok(180), turer, BLA)
        self.assertEqual([f.felt for f in forslag], ["varighet"])


class NivahevingTest(unittest.TestCase):
    def status(self, hevinger, sperre=None):
        return NivaStatus(GRONN if sperre else BLA, BLA, sperre, hevinger, 0)

    def test_ny_heving_gir_true_og_brukt_gir_false(self):  # FR-19, AD-11
        self.assertTrue(nivaheving(self.status(1), 0))
        self.assertFalse(nivaheving(self.status(1), 1))

    def test_aktiv_sperre_gir_false(self):  # AD-11
        self.assertFalse(nivaheving(self.status(1, Sperre(GRONN, BLA)), 0))

    def test_fjernet_heving_gir_false(self):  # AD-11
        self.assertFalse(nivaheving(self.status(0), 1))

    def test_er_over_nivatak_med_tak(self):  # FR-17
        tur = lag_tur(turniva=BLA)
        self.assertTrue(er_over_nivatak(tur))
        self.assertFalse(er_over_nivatak(tur, BLA))


class ForetrukneTurtyperTest(unittest.TestCase):  # FR-20, FR-5 punkt 4
    def turer(self):
        return [
            lag_tur(id="a-marka", estimert_tid_min=120, turtyper=("marka",)),
            lag_tur(id="b-utsikt", estimert_tid_min=60, turtyper=("utsikt",)),
        ]

    def test_foretrukket_turtype_kommer_foran_lengre_tid(self):
        uten = velg_turer(sok(180), self.turer(), GRONN)
        med = velg_turer(sok(180), self.turer(), GRONN, foretrukne_turtyper=frozenset({"utsikt"}))
        self.assertEqual(uten.rangerte_tur_ider, ("a-marka", "b-utsikt"))
        self.assertEqual(med.rangerte_tur_ider, ("b-utsikt", "a-marka"))

    def test_ikke_gatt_vinner_over_foretrukket_gatt(self):
        utvalg = velg_turer(
            sok(180),
            self.turer(),
            GRONN,
            registreringer=[gatt("b-utsikt", 5)],
            foretrukne_turtyper=frozenset({"utsikt"}),
        )
        self.assertEqual(utvalg.rangerte_tur_ider, ("a-marka", "b-utsikt"))

    def test_gatt_med_lav_fornoydhet_er_sist(self):
        utvalg = velg_turer(
            sok(180),
            self.turer(),
            GRONN,
            registreringer=[gatt("b-utsikt", 2)],
            foretrukne_turtyper=frozenset({"utsikt"}),
        )
        self.assertEqual(utvalg.rangerte_tur_ider[-1], "b-utsikt")

    def test_nivaheving_gar_foran_preferanse(self):
        turer = [
            lag_tur(id="a-gronn", turniva=GRONN, turtyper=("utsikt",), estimert_tid_min=120),
            lag_tur(id="b-bla", turniva=BLA, turtyper=("marka",), estimert_tid_min=60),
        ]
        utvalg = velg_turer(
            sok(180), turer, BLA, nivaheving=True, foretrukne_turtyper=frozenset({"utsikt"})
        )
        self.assertEqual(utvalg.rangerte_tur_ider, ("b-bla", "a-gronn"))

    def test_gjelder_utsiktsturene_ved_topptur_erstattet(self):
        turer = [
            lag_tur(id="a", turtyper=("utsikt",), estimert_tid_min=120),
            lag_tur(id="b", turtyper=("utsikt", "marka"), estimert_tid_min=60),
        ]
        utvalg = velg_turer(
            sok(180, turtype="topptur"), turer, GRONN, foretrukne_turtyper=frozenset({"marka"})
        )
        self.assertEqual(utvalg.status, Status.TOPPTUR_ERSTATTET)
        self.assertEqual(utvalg.rangerte_tur_ider, ("b", "a"))


if __name__ == "__main__":
    unittest.main()
