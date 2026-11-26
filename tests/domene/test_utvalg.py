"""`domene.utvalg`: filtrering, rangering og status for et søk (FR-5, FR-8, FR-18, SM-2).

Testene bruker egne turer laget med `lag_tur` og leser ikke `data/turer.geojson`.
"""

import random
import unittest
from dataclasses import FrozenInstanceError, replace
from datetime import date

from domene.sok import MAKS_VARIGHET_MIN, MIN_VARIGHET_MIN, VARIGHET_STEG_MIN, Sok
from domene.tur import NIVAREKKEFOLGE, TURTYPER, Form, Tur, Turniva
from domene.utvalg import (
    NIVATAK_UTEN_HISTORIKK,
    Endringsforslag,
    Status,
    Utvalg,
    foresla_endringer,
    innenfor_tid_og_nivatak,
    velg_turer,
)

DATO = date(2026, 11, 26)
GRONN, BLA, ROD, SVART = Turniva.GRONN, Turniva.BLA, Turniva.ROD, Turniva.SVART


def lag_tur(**endringer) -> Tur:
    tur = Tur(
        id="tur",
        navn="Tur",
        startpunkt_id="sorkedalen",
        startpunkt_navn="Sørkedalen",
        startpunkt_lat=59.9876,
        startpunkt_lon=10.6543,
        startpunkt_hoyde_m=180,
        form=Form.TUR_RETUR,
        turtyper=("marka",),
        lengde_m=3000,
        hoydemeter_m=150,
        nedstigning_m=0,
        hoydeprofil=((0, 180), (3000, 330)),
        turniva=GRONN,
        estimert_tid_min=120,
        ut_no_url="",
        kilde="turrutebasen",
        lisens="CC BY 4.0",
        geometry=((10.6543, 59.9876), (10.67, 60.0)),
    )
    return replace(tur, **endringer)


def sok(varighet_min=180, turtype=None, startpunkt_id=None) -> Sok:
    return Sok(varighet_min, DATO, turtype=turtype, startpunkt_id=startpunkt_id)


class NivarekkefolgeTest(unittest.TestCase):
    def test_rekkefolgen_er_gronn_bla_rod_svart(self):  # FR-5
        self.assertEqual(NIVAREKKEFOLGE, (GRONN, BLA, ROD, SVART))
        # StrEnum sammenligner alfabetisk, så «bla» < «gronn». Derfor rekkefølgen.
        self.assertLess(BLA, GRONN)

    def test_gjest_og_bruker_uten_historikk_har_gront_nivatak(self):  # FR-18
        self.assertIs(NIVATAK_UTEN_HISTORIKK, GRONN)


class UtvalgDataklasseTest(unittest.TestCase):
    def test_utvalget_er_frosset_med_tuple(self):  # FR-5
        utvalg = velg_turer(sok(), [lag_tur()], GRONN)
        self.assertIsInstance(utvalg.rangerte_tur_ider, tuple)
        with self.assertRaises(FrozenInstanceError):
            utvalg.status = Status.INGEN_TREFF

    def test_statusene(self):  # FR-5, FR-8
        self.assertEqual(
            [s.name for s in Status],
            ["TREFF", "TOPPTUR_ERSTATTET", "BARE_OVER_NIVATAK", "INGEN_TREFF"],
        )


class MatriseTest(unittest.TestCase):
    """Én test per rad i I/O-matrisen i spec 1.8."""

    def test_treff(self):  # FR-5, FR-18: 3 t, alle turtyper, grønt tak
        turer = [
            lag_tur(id="kort", estimert_tid_min=90),
            lag_tur(id="lang", estimert_tid_min=180, turtyper=("utsikt",)),
            lag_tur(id="for-lang", estimert_tid_min=185),
            lag_tur(id="bla", estimert_tid_min=150, turniva=BLA),
            lag_tur(id="midt", estimert_tid_min=120, turtyper=("topptur",)),
        ]
        self.assertEqual(
            velg_turer(sok(180), turer, NIVATAK_UTEN_HISTORIKK),
            Utvalg(Status.TREFF, ("lang", "midt", "kort")),
        )

    def test_lang_tur(self):  # FR-5, beslutning 4: 580 og 575 min med 12 t og svart tak
        turer = [
            lag_tur(id="svart", estimert_tid_min=580, turniva=SVART),
            lag_tur(id="rod", estimert_tid_min=575, turniva=ROD),
        ]
        self.assertEqual(
            velg_turer(sok(MAKS_VARIGHET_MIN), turer, SVART),
            Utvalg(Status.TREFF, ("svart", "rod")),
        )

    def test_lik_tid_er_med(self):  # FR-5
        utvalg = velg_turer(sok(150), [lag_tur(id="a", estimert_tid_min=150)], GRONN)
        self.assertEqual(utvalg, Utvalg(Status.TREFF, ("a",)))

    def test_ingen_minstetid(self):  # FR-5
        utvalg = velg_turer(sok(720), [lag_tur(id="a", estimert_tid_min=30)], GRONN)
        self.assertEqual(utvalg, Utvalg(Status.TREFF, ("a",)))

    def test_lik_tid_ulik_id_gir_id_stigende(self):  # FR-5 punkt 6
        turer = [lag_tur(id="b", estimert_tid_min=120), lag_tur(id="a", estimert_tid_min=120)]
        self.assertEqual(velg_turer(sok(), turer, GRONN).rangerte_tur_ider, ("a", "b"))

    def test_id_sorteres_som_tekst(self):  # FR-5 punkt 6
        turer = [lag_tur(id="tur-10"), lag_tur(id="tur-9"), lag_tur(id="tur-2")]
        self.assertEqual(
            velg_turer(sok(), turer, GRONN).rangerte_tur_ider, ("tur-10", "tur-2", "tur-9")
        )

    def test_over_nivataket_er_aldri_med(self):  # FR-5, FR-18, SM-C1
        turer = [lag_tur(id="bla", turniva=BLA), lag_tur(id="gronn", estimert_tid_min=60)]
        self.assertEqual(velg_turer(sok(), turer, GRONN), Utvalg(Status.TREFF, ("gronn",)))

    def test_nivataket_tar_med_alle_lavere_nivaer(self):  # FR-5
        turer = [lag_tur(id=n.value, turniva=n) for n in NIVAREKKEFOLGE]
        for plass, tak in enumerate(NIVAREKKEFOLGE):
            with self.subTest(tak=tak):
                forventet = tuple(sorted(n.value for n in NIVAREKKEFOLGE[: plass + 1]))
                self.assertEqual(velg_turer(sok(), turer, tak).rangerte_tur_ider, forventet)

    def test_turtype_og_startpunkt(self):  # FR-5
        turer = [
            lag_tur(id="begge", turtyper=("marka", "utsikt")),
            lag_tur(id="feil-type", turtyper=("utsikt",)),
            lag_tur(id="feil-start", startpunkt_id="frognerseteren"),
            lag_tur(id="ingen-type", turtyper=()),
        ]
        utvalg = velg_turer(sok(turtype="marka", startpunkt_id="sorkedalen"), turer, GRONN)
        self.assertEqual(utvalg, Utvalg(Status.TREFF, ("begge",)))

    def test_topptur_som_passer_gir_treff_ikke_erstatning(self):  # FR-5, FR-8
        turer = [
            lag_tur(id="gronn-topptur", turtyper=("topptur",), estimert_tid_min=150),
            lag_tur(id="gronn-utsikt", turtyper=("utsikt",), estimert_tid_min=170),
        ]
        self.assertEqual(
            velg_turer(sok(180, turtype="topptur"), turer, GRONN),
            Utvalg(Status.TREFF, ("gronn-topptur",)),
        )

    def test_topptur_erstattet(self):  # FR-8
        turer = [
            lag_tur(id="topptur-lang", turtyper=("topptur",), estimert_tid_min=240),
            lag_tur(id="utsikt-a", turtyper=("utsikt",), estimert_tid_min=100),
            lag_tur(id="utsikt-b", turtyper=("utsikt", "marka"), estimert_tid_min=170),
            lag_tur(id="marka", estimert_tid_min=60),
        ]
        self.assertEqual(
            velg_turer(sok(180, turtype="topptur"), turer, GRONN),
            Utvalg(Status.TOPPTUR_ERSTATTET, ("utsikt-b", "utsikt-a")),
        )

    def test_topptur_over_taket_og_utsikt_innenfor_gir_erstattet(self):  # FR-8, beslutning 1
        turer = [
            lag_tur(id="bla-topptur", turtyper=("topptur",), turniva=BLA),
            lag_tur(id="gronn-utsikt", turtyper=("utsikt",)),
        ]
        self.assertEqual(
            velg_turer(sok(turtype="topptur"), turer, GRONN),
            Utvalg(Status.TOPPTUR_ERSTATTET, ("gronn-utsikt",)),
        )

    def test_topptur_feil_startpunkt_gir_utsikt_fra_samme_startpunkt(self):  # FR-8, beslutning 2
        turer = [
            lag_tur(id="topptur-y", turtyper=("topptur",), startpunkt_id="y"),
            lag_tur(id="utsikt-x", turtyper=("utsikt",), startpunkt_id="x"),
            lag_tur(id="utsikt-y", turtyper=("utsikt",), startpunkt_id="y"),
        ]
        self.assertEqual(
            velg_turer(sok(turtype="topptur", startpunkt_id="x"), turer, GRONN),
            Utvalg(Status.TOPPTUR_ERSTATTET, ("utsikt-x",)),
        )

    def test_utsiktsturene_far_ogsa_tid_og_nivatak(self):  # FR-8, beslutning 2
        turer = [
            lag_tur(id="topptur", turtyper=("topptur",), estimert_tid_min=300),
            lag_tur(id="utsikt-lang", turtyper=("utsikt",), estimert_tid_min=200),
            lag_tur(id="utsikt-bla", turtyper=("utsikt",), turniva=BLA),
            lag_tur(id="utsikt-ok", turtyper=("utsikt",), estimert_tid_min=90),
        ]
        self.assertEqual(
            velg_turer(sok(180, turtype="topptur"), turer, GRONN),
            Utvalg(Status.TOPPTUR_ERSTATTET, ("utsikt-ok",)),
        )

    def test_topptur_bare_utsikt_over_taket_gir_ingen_treff(self):  # FR-8, beslutning 3
        turer = [
            lag_tur(id="bla-utsikt", turtyper=("utsikt",), turniva=BLA),
            lag_tur(id="topptur-lang", turtyper=("topptur",), estimert_tid_min=300),
        ]
        self.assertEqual(
            velg_turer(sok(turtype="topptur"), turer, GRONN), Utvalg(Status.INGEN_TREFF, ())
        )

    def test_topptur_bare_topptur_over_taket_gir_bare_over_nivatak(self):  # FR-8, beslutning 3
        turer = [
            lag_tur(id="bla-topptur", turtyper=("topptur",), turniva=BLA),
            lag_tur(id="bla-utsikt", turtyper=("utsikt",), turniva=BLA),
        ]
        self.assertEqual(
            velg_turer(sok(turtype="topptur"), turer, GRONN),
            Utvalg(Status.BARE_OVER_NIVATAK, ()),
        )

    def test_bare_over_nivataket(self):  # FR-5, FR-18, SM-C1
        turer = [lag_tur(id="bla", turniva=BLA), lag_tur(id="svart", turniva=SVART)]
        self.assertEqual(velg_turer(sok(), turer, GRONN), Utvalg(Status.BARE_OVER_NIVATAK, ()))

    def test_bare_over_nivataket_krever_at_resten_av_soket_passer(self):  # FR-5
        turer = [lag_tur(id="bla", turniva=BLA, startpunkt_id="y")]
        self.assertEqual(
            velg_turer(sok(startpunkt_id="x"), turer, GRONN), Utvalg(Status.INGEN_TREFF, ())
        )

    def test_ingen_treff(self):  # FR-5
        turer = [
            lag_tur(id="lang", estimert_tid_min=200),
            lag_tur(id="bla-lang", turniva=BLA, estimert_tid_min=300),
        ]
        self.assertEqual(velg_turer(sok(180), turer, SVART), Utvalg(Status.INGEN_TREFF, ()))

    def test_tom_turliste_gir_ingen_treff(self):  # FR-5
        self.assertEqual(velg_turer(sok(), [], GRONN), Utvalg(Status.INGEN_TREFF, ()))


# Et lite, variert sett: alle nivåer, turtyper, tre startpunkter og tider fra 45 til 580 min.
VARIERTE_TURER = (
    lag_tur(
        id="g-marka-a-90",
        turniva=GRONN,
        turtyper=("marka",),
        startpunkt_id="a",
        estimert_tid_min=90,
    ),
    lag_tur(
        id="g-utsikt-a-150",
        turniva=GRONN,
        turtyper=("utsikt",),
        startpunkt_id="a",
        estimert_tid_min=150,
    ),
    lag_tur(
        id="g-topptur-a-240",
        turniva=GRONN,
        turtyper=("topptur",),
        startpunkt_id="a",
        estimert_tid_min=240,
    ),
    lag_tur(
        id="b-topptur-b-120",
        turniva=BLA,
        turtyper=("topptur",),
        startpunkt_id="b",
        estimert_tid_min=120,
    ),
    lag_tur(
        id="b-marka-c-45", turniva=BLA, turtyper=("marka",), startpunkt_id="c", estimert_tid_min=45
    ),
    lag_tur(
        id="r-topptur-b-300",
        turniva=ROD,
        turtyper=("topptur", "utsikt"),
        startpunkt_id="b",
        estimert_tid_min=300,
    ),
    lag_tur(
        id="r-utsikt-c-200",
        turniva=ROD,
        turtyper=("utsikt",),
        startpunkt_id="c",
        estimert_tid_min=200,
    ),
    lag_tur(
        id="s-marka-c-580",
        turniva=SVART,
        turtyper=("marka", "utsikt"),
        startpunkt_id="c",
        estimert_tid_min=580,
    ),
    lag_tur(
        id="s-topptur-a-150",
        turniva=SVART,
        turtyper=("topptur",),
        startpunkt_id="a",
        estimert_tid_min=150,
    ),
)


def alle_sok():
    for varighet in range(MIN_VARIGHET_MIN, MAKS_VARIGHET_MIN + 1, VARIGHET_STEG_MIN):
        for turtype in (None, *TURTYPER):
            for startpunkt_id in (None, "a", "b", "c", "ukjent"):
                yield sok(varighet, turtype, startpunkt_id)


class EgenskaperTest(unittest.TestCase):
    def test_ingen_tur_over_nivataket_for_hvert_tak_og_hver_status(self):  # SM-C1, SM-2, FR-5
        turer_etter_id = {tur.id: tur for tur in VARIERTE_TURER}
        sett: set[tuple[Turniva, Status]] = set()
        for tak in NIVAREKKEFOLGE:
            tillatte = set(NIVAREKKEFOLGE[: NIVAREKKEFOLGE.index(tak) + 1])
            for s in alle_sok():
                utvalg = velg_turer(s, VARIERTE_TURER, tak)
                sett.add((tak, utvalg.status))
                with self.subTest(tak=tak, sok=s, status=utvalg.status):
                    for tur_id in utvalg.rangerte_tur_ider:
                        tur = turer_etter_id[tur_id]
                        self.assertIn(tur.turniva, tillatte)
                        self.assertLessEqual(tur.estimert_tid_min, s.varighet_min)
                        if s.startpunkt_id is not None:
                            self.assertEqual(tur.startpunkt_id, s.startpunkt_id)
                        if utvalg.status == Status.TREFF and s.turtype is not None:
                            self.assertIn(s.turtype, tur.turtyper)
                    rangerte = [turer_etter_id[tur_id] for tur_id in utvalg.rangerte_tur_ider]
                    self.assertEqual(len(set(utvalg.rangerte_tur_ider)), len(rangerte))
                    self.assertEqual(
                        rangerte, sorted(rangerte, key=lambda t: (-t.estimert_tid_min, t.id))
                    )
                    if utvalg.status in (Status.BARE_OVER_NIVATAK, Status.INGEN_TREFF):
                        self.assertEqual(utvalg.rangerte_tur_ider, ())
                    else:
                        self.assertTrue(utvalg.rangerte_tur_ider)
                    if utvalg.status == Status.TOPPTUR_ERSTATTET:
                        self.assertEqual(s.turtype, "topptur")
                        for tur_id in utvalg.rangerte_tur_ider:
                            self.assertIn("utsikt", turer_etter_id[tur_id].turtyper)
        # Alle fire statusene forekommer, og hvert tak gir treff og ingen treff.
        self.assertEqual({status for _, status in sett}, set(Status))
        for tak in NIVAREKKEFOLGE:
            self.assertIn((tak, Status.TREFF), sett)
            self.assertIn((tak, Status.INGEN_TREFF), sett)
        self.assertIn((GRONN, Status.TOPPTUR_ERSTATTET), sett)
        self.assertIn((GRONN, Status.BARE_OVER_NIVATAK), sett)

    def test_rekkefolgen_pa_turlista_endrer_ikke_resultatet(self):  # FR-5
        stokket = list(VARIERTE_TURER)
        random.Random(18).shuffle(stokket)
        for tak in NIVAREKKEFOLGE:
            for s in alle_sok():
                with self.subTest(tak=tak, sok=s):
                    forventet = velg_turer(s, VARIERTE_TURER, tak)
                    self.assertEqual(velg_turer(s, tuple(reversed(VARIERTE_TURER)), tak), forventet)
                    self.assertEqual(velg_turer(s, stokket, tak), forventet)

    def test_turene_kan_komme_fra_en_generator(self):  # FR-5
        s = sok(720, turtype="topptur")
        forventet = velg_turer(s, VARIERTE_TURER, GRONN)
        self.assertEqual(velg_turer(s, (tur for tur in VARIERTE_TURER), GRONN), forventet)

    def test_samme_sok_gir_samme_liste(self):  # FR-5 punkt 6
        s = sok(720)
        self.assertEqual(velg_turer(s, VARIERTE_TURER, SVART), velg_turer(s, VARIERTE_TURER, SVART))
        self.assertEqual(
            velg_turer(s, VARIERTE_TURER, SVART).rangerte_tur_ider,
            (
                "s-marka-c-580",
                "r-topptur-b-300",
                "g-topptur-a-240",
                "r-utsikt-c-200",
                "g-utsikt-a-150",
                "s-topptur-a-150",
                "b-topptur-b-120",
                "g-marka-a-90",
                "b-marka-c-45",
            ),
        )

    def test_datoen_pavirker_ikke_utvalget(self):  # FR-5, AD-2
        a = Sok(180, date(2026, 1, 1))
        b = Sok(180, date(2026, 7, 1))
        self.assertEqual(velg_turer(a, VARIERTE_TURER, ROD), velg_turer(b, VARIERTE_TURER, ROD))


class InnenforTidOgNivatakTest(unittest.TestCase):
    def test_tid_og_niva(self):  # FR-5, SM-C1
        self.assertTrue(innenfor_tid_og_nivatak(lag_tur(estimert_tid_min=180), sok(180), GRONN))
        self.assertFalse(innenfor_tid_og_nivatak(lag_tur(estimert_tid_min=185), sok(180), GRONN))
        self.assertFalse(innenfor_tid_og_nivatak(lag_tur(turniva=BLA), sok(180), GRONN))
        # «bla» < «gronn» alfabetisk, men blått er over grønt nivåtak.
        self.assertTrue(innenfor_tid_og_nivatak(lag_tur(turniva=GRONN), sok(180), BLA))

    def test_turtype_og_startpunkt_sjekkes_ikke(self):  # FR-8
        tur = lag_tur(turtyper=("utsikt",))
        self.assertTrue(innenfor_tid_og_nivatak(tur, sok(180, turtype="topptur"), GRONN))


class ForeslaEndringerTest(unittest.TestCase):
    """`foresla_endringer` (FR-8, UX-DR17, UX-DR22): høyst tre forslag i fast rekkefølge."""

    def forslag(self, turer, sok_, tidligere=()):
        return foresla_endringer(sok_, turer, NIVATAK_UTEN_HISTORIKK, tidligere)

    def test_lengre_varighet(self):
        turer = [lag_tur(id="a", estimert_tid_min=170)]
        self.assertEqual(
            self.forslag(turer, sok(120)), (Endringsforslag("varighet", "180", "Prøv 3 timer"),)
        )

    def test_halvtime(self):
        turer = [lag_tur(id="a", estimert_tid_min=150)]
        self.assertEqual(
            self.forslag(turer, sok(120)), (Endringsforslag("varighet", "150", "Prøv 2,5 timer"),)
        )

    def test_ingen_varighetsforslag_ved_12_timer(self):
        turer = [lag_tur(id="a", turtyper=("utsikt",))]
        self.assertEqual(
            self.forslag(turer, sok(MAKS_VARIGHET_MIN, turtype="marka"))[0].felt, "turtype"
        )
        self.assertNotIn(
            "varighet",
            [f.felt for f in self.forslag(turer, sok(MAKS_VARIGHET_MIN, turtype="marka"))],
        )

    def test_ingen_varighetsforslag_naar_ingen_lengre_varighet_gir_treff(self):
        turer = [lag_tur(id="a", turtyper=("utsikt",), estimert_tid_min=60)]
        forslag = self.forslag(turer, sok(60, turtype="marka"))
        self.assertEqual([f.felt for f in forslag], ["turtype"])

    def test_startpunkt_bare_naar_valgt_og_annet_gir_treff(self):
        turer = [lag_tur(id="a", startpunkt_id="x")]
        forslag = self.forslag(turer, sok(180, startpunkt_id="z"))
        self.assertEqual([f.etikett for f in forslag], ["Velg startpunkt"])
        self.assertNotIn("startpunkt", [f.felt for f in self.forslag(turer, sok(180))])
        self.assertEqual(self.forslag([], sok(180, startpunkt_id="z")), ())

    def test_turtype_foerste_i_rekkefolgen(self):
        turer = [lag_tur(id="a", turtyper=("topptur",)), lag_tur(id="b", turtyper=("utsikt",))]
        forslag = self.forslag(turer, sok(180, turtype="marka"))
        self.assertEqual(forslag, (Endringsforslag("turtype", "utsikt", "Prøv utsikt"),))
        turer = [lag_tur(id="a", turtyper=("marka",))]
        forslag = self.forslag(turer, sok(180, turtype="topptur"))
        self.assertEqual(forslag, (Endringsforslag("turtype", "marka", "Prøv marka"),))

    def test_alle_turtyper_som_reserve(self):  # FR-8
        # Turen har ingen turtype, så bare søk uten turtype gir treff.
        turer = [lag_tur(id="a", turtyper=())]
        self.assertEqual(
            self.forslag(turer, sok(180, turtype="marka")),
            (Endringsforslag("turtype", "", "Prøv alle turtyper"),),
        )

    def test_ingen_forslag_naar_alle_turtyper_heller_ikke_gir_treff(self):
        turer = [lag_tur(id="a", turniva=BLA)]
        self.assertEqual(self.forslag(turer, sok(180, turtype="marka")), ())

    def test_nivaet_over_taket_gir_ikke_forslag(self):
        turer = [lag_tur(id="a", turniva=BLA)]
        self.assertEqual(self.forslag(turer, sok(180, turtype="marka", startpunkt_id="x")), ())

    def test_tre_forslag_i_fast_rekkefolge(self):
        turer = [
            lag_tur(id="a", startpunkt_id="x", turtyper=("utsikt",), estimert_tid_min=90),
            lag_tur(id="b", startpunkt_id="y", turtyper=("utsikt",), estimert_tid_min=60),
            lag_tur(id="c", startpunkt_id="x", turtyper=("marka",), estimert_tid_min=60),
        ]
        forslag = self.forslag(turer, sok(60, turtype="utsikt", startpunkt_id="x"))
        self.assertEqual(
            [(f.felt, f.verdi, f.etikett) for f in forslag],
            [
                ("varighet", "90", "Prøv 1,5 timer"),
                ("startpunkt", "", "Velg startpunkt"),
                ("turtype", "marka", "Prøv marka"),
            ],
        )

    def test_alle_vist_krever_ny_tur(self):
        turer = [lag_tur(id="a", estimert_tid_min=120), lag_tur(id="b", estimert_tid_min=150)]
        sokt = sok(120)
        self.assertEqual(
            self.forslag(turer, sokt, ("a",)),
            (Endringsforslag("varighet", "150", "Prøv 2,5 timer"),),
        )
        self.assertEqual(self.forslag(turer, sokt, ("a", "b")), ())

    def test_velg_turer_er_uendret(self):
        turer = [lag_tur(id="a")]
        for_ = velg_turer(sok(180), turer, NIVATAK_UTEN_HISTORIKK)
        self.forslag(turer, sok(60))
        self.assertEqual(for_, velg_turer(sok(180), turer, NIVATAK_UTEN_HISTORIKK))
