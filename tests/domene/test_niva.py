"""`domene.niva`: nivåtak, grunnnivå og sperre fra vurderingene (FR-18, FR-19, SM-2, NFR-6).

Ingen database. Hvert av de 12 eksemplene i FR-19 er et eget testtilfelle, og «Før» bygges
av registreringer.
"""

import random
import unittest
from dataclasses import FrozenInstanceError, replace
from datetime import date, timedelta

from domene.niva import NivaStatus, Registrering, Sperre, vurder_historikk
from domene.tur import Turniva

GRONN, BLA, ROD, SVART = Turniva.GRONN, Turniva.BLA, Turniva.ROD, Turniva.SVART
START = date(2026, 1, 1)


def historikk(*deler) -> list[Registrering]:
    """Bygger registreringer i rekkefølge, hver del er (turnivå, vanskelighet[, antall])."""
    resultat = []
    for del_ in deler:
        niva, vanskelighet, *antall = del_
        for _ in range(antall[0] if antall else 1):
            n = len(resultat)
            resultat.append(
                Registrering(n + 1, START + timedelta(days=n), f"tur-{niva}", niva, vanskelighet, 4)
            )
    return resultat


def til_blatt(*ekstra):
    """Tre lette grønne turer: grunnnivå blått."""
    return historikk((GRONN, "lett", 3), *ekstra)


class NivaTest(unittest.TestCase):
    def test_tom_historikk_gir_gront_uten_sperre(self):  # FR-18
        self.assertEqual(vurder_historikk([]), NivaStatus(GRONN, GRONN, None, 0, 0))

    def test_eksempel_1_tredje_lette_hever_grunnnivaet(self):  # FR-19 #1
        for_ = historikk((GRONN, "lett", 2))
        self.assertEqual(vurder_historikk(for_), NivaStatus(GRONN, GRONN, None, 0, 2))
        etter = vurder_historikk(historikk((GRONN, "lett", 3)))
        self.assertEqual(etter, NivaStatus(BLA, BLA, None, 1, 0))

    def test_eksempel_2_moderat_teller_ikke(self):  # FR-19 #2
        for_ = historikk((GRONN, "lett"))
        self.assertEqual(vurder_historikk(for_).teller, 1)
        etter = vurder_historikk(historikk((GRONN, "lett"), (GRONN, "moderat")))
        self.assertEqual(etter, NivaStatus(GRONN, GRONN, None, 0, 1))

    def test_eksempel_3_bare_turer_pa_grunnnivaet_teller(self):  # FR-19 #3
        for_ = til_blatt((BLA, "lett", 2))
        self.assertEqual(vurder_historikk(for_), NivaStatus(BLA, BLA, None, 1, 2))
        etter = vurder_historikk(historikk((GRONN, "lett", 3), (BLA, "lett", 2), (GRONN, "lett")))
        self.assertEqual(etter, NivaStatus(BLA, BLA, None, 1, 2))

    def test_eksempel_4_vanskelig_gir_sperre(self):  # FR-19 #4
        for_ = til_blatt((BLA, "lett", 2))
        self.assertEqual(vurder_historikk(for_), NivaStatus(BLA, BLA, None, 1, 2))
        etter = vurder_historikk(til_blatt((BLA, "lett", 2), (BLA, "vanskelig")))
        self.assertEqual(etter, NivaStatus(GRONN, BLA, Sperre(GRONN, BLA), 1, 0))

    def test_eksempel_5_lett_opphever_sperren(self):  # FR-19 #5
        etter = vurder_historikk(til_blatt((BLA, "lett", 2), (BLA, "vanskelig"), (GRONN, "lett")))
        self.assertEqual(etter, NivaStatus(BLA, BLA, None, 1, 0))

    def test_moderat_opphever_ogsa_sperren(self):  # FR-19 oppheving
        etter = vurder_historikk(til_blatt((BLA, "vanskelig"), (ROD, "moderat")))
        self.assertEqual(etter, NivaStatus(BLA, BLA, None, 1, 0))

    def test_eksempel_6_vanskelig_under_sperre_er_uendret(self):  # FR-19 #6
        for_ = til_blatt((BLA, "lett", 2), (BLA, "vanskelig"))
        self.assertEqual(vurder_historikk(for_).sperre, Sperre(GRONN, BLA))
        etter = vurder_historikk(
            til_blatt((BLA, "lett", 2), (BLA, "vanskelig"), (GRONN, "vanskelig"))
        )
        self.assertEqual(etter, NivaStatus(GRONN, BLA, Sperre(GRONN, BLA), 1, 0))

    def test_vanskelig_kan_senke_en_sperre_videre(self):  # FR-19 sperre
        etter = vurder_historikk(
            historikk((GRONN, "lett", 3), (BLA, "lett", 3), (ROD, "vanskelig"), (BLA, "vanskelig"))
        )
        self.assertEqual(etter.sperre, Sperre(GRONN, BLA))
        self.assertEqual(etter.grunnniva, ROD)

    def test_eksempel_7_vanskelig_over_gront_gir_sperre(self):  # FR-19 #7
        for_ = til_blatt((BLA, "lett"))
        self.assertEqual(vurder_historikk(for_), NivaStatus(BLA, BLA, None, 1, 1))
        etter = vurder_historikk(til_blatt((BLA, "lett"), (GRONN, "vanskelig")))
        self.assertEqual(etter, NivaStatus(GRONN, BLA, Sperre(GRONN, GRONN), 1, 0))

    def test_eksempel_8_vanskelig_gronn_tur_ved_gront_gir_ingen_sperre(self):  # FR-19 #8
        for_ = historikk((GRONN, "lett", 2))
        self.assertEqual(vurder_historikk(for_).teller, 2)
        etter = vurder_historikk(historikk((GRONN, "lett", 2), (GRONN, "vanskelig")))
        self.assertEqual(etter, NivaStatus(GRONN, GRONN, None, 0, 0))

    def test_eksempel_9_vanskelig_bla_tur_ved_rodt_gir_sperre_gront(self):  # FR-19 #9
        for_ = historikk((GRONN, "lett", 3), (BLA, "lett", 3))
        self.assertEqual(vurder_historikk(for_), NivaStatus(ROD, ROD, None, 2, 0))
        etter = vurder_historikk(
            historikk((GRONN, "lett", 3), (BLA, "lett", 3), (BLA, "vanskelig"))
        )
        self.assertEqual(etter, NivaStatus(GRONN, ROD, Sperre(GRONN, BLA), 2, 0))

    def test_eksempel_10_turer_over_grunnnivaet_teller_ikke(self):  # FR-19 #10
        for_ = til_blatt()
        self.assertEqual(vurder_historikk(for_), NivaStatus(BLA, BLA, None, 1, 0))
        etter = vurder_historikk(til_blatt((ROD, "lett")))
        self.assertEqual(etter, NivaStatus(BLA, BLA, None, 1, 0))

    def test_eksempel_11_svart_heves_ikke(self):  # FR-19 #11
        for_ = historikk((GRONN, "lett", 3), (BLA, "lett", 3), (ROD, "lett", 3))
        self.assertEqual(vurder_historikk(for_), NivaStatus(SVART, SVART, None, 3, 0))
        etter = vurder_historikk(for_ + historikk((SVART, "lett", 3)))
        self.assertEqual(etter, NivaStatus(SVART, SVART, None, 3, 0))

    def test_eksempel_12_samme_tur_tre_ganger_hever(self):  # FR-19 #12
        gjentatt = [
            Registrering(i, START + timedelta(days=i), "samme-tur", GRONN, "lett", 3)
            for i in range(1, 4)
        ]
        self.assertEqual(vurder_historikk(gjentatt), NivaStatus(BLA, BLA, None, 1, 0))

    def test_moderat_imellom_hindrer_ikke_hevingen(self):  # FR-19 heving
        etter = vurder_historikk(
            historikk((GRONN, "lett"), (GRONN, "moderat"), (GRONN, "lett"), (GRONN, "lett"))
        )
        self.assertEqual(etter, NivaStatus(BLA, BLA, None, 1, 0))

    def test_vanskelig_nullstiller_telleren(self):  # FR-19 sperre
        etter = vurder_historikk(
            historikk((GRONN, "lett", 2), (GRONN, "vanskelig"), (GRONN, "lett", 2))
        )
        self.assertEqual(etter, NivaStatus(GRONN, GRONN, None, 0, 2))

    def test_rekkefolgen_pa_innsending_spiller_ingen_rolle(self):  # FR-19 rekkefølge
        registreringer = til_blatt((BLA, "lett", 2), (BLA, "vanskelig"), (GRONN, "lett"))
        fasit = vurder_historikk(registreringer)
        for frø in range(20):
            blandet = registreringer[:]
            random.Random(frø).shuffle(blandet)
            self.assertEqual(vurder_historikk(blandet), fasit)

    def test_tidlig_dato_registrert_sist_kan_endre_nivataket(self):  # FR-19 rekkefølge
        v = Registrering(1, date(2026, 3, 10), "v", ROD, "vanskelig", 3)
        # Alene: grunnnivået er grønt, så vanskelig på rødt gir ingen sperre.
        self.assertEqual(vurder_historikk([v]), NivaStatus(GRONN, GRONN, None, 0, 0))
        # Seks tidlige lette turer (registrert sist) hever grunnnivået til rødt før v.
        tidlige = [
            Registrering(10 + i, date(2026, 2, 1 + i), f"t{i}", GRONN if i < 3 else BLA, "lett", 3)
            for i in range(6)
        ]
        etter = vurder_historikk([v, *tidlige])
        self.assertEqual(etter, NivaStatus(BLA, ROD, Sperre(BLA, ROD), 2, 0))

    def test_samme_dato_avgjores_av_id(self):  # FR-19 rekkefølge
        lett = Registrering(1, START, "a", GRONN, "lett", 3)
        vanskelig = Registrering(2, START, "b", BLA, "vanskelig", 3)
        # lett (id 1) før vanskelig (id 2): vanskelig nullstiller telleren, så den er 0.
        self.assertEqual(vurder_historikk([vanskelig, lett]), NivaStatus(GRONN, GRONN, None, 0, 0))
        # lett med id 3 kommer etter vanskelig (id 2): telleren er 1.
        lett2 = replace(lett, id=3)
        self.assertEqual(vurder_historikk([lett2, vanskelig]), NivaStatus(GRONN, GRONN, None, 0, 1))

    def test_ugyldig_input_gir_valueerror(self):  # FR-18
        gyldig = Registrering(1, START, "a", GRONN, "lett", 3)
        ugyldige = [
            replace(gyldig, turniva="lilla"),
            replace(gyldig, vanskelighet="umulig"),
            replace(gyldig, fornoydhet=0),
            replace(gyldig, fornoydhet=6),
            replace(gyldig, fornoydhet=True),
            replace(gyldig, fornoydhet=3.5),
        ]
        for ugyldig in ugyldige:
            with self.subTest(ugyldig=ugyldig):
                with self.assertRaises(ValueError):
                    vurder_historikk([gyldig, ugyldig])

    def test_dataklassene_er_frosne(self):
        status = vurder_historikk([])
        with self.assertRaises(FrozenInstanceError):
            status.teller = 1  # type: ignore[misc]


class ForetrukneTurtyperTest(unittest.TestCase):  # FR-20
    def reg(self, id, fornoydhet, turtyper):
        return Registrering(
            id, START + timedelta(days=id), f"t{id}", GRONN, "lett", fornoydhet, turtyper
        )

    def test_fornoydhet_4_og_5_gir_preferanse(self):
        for fornoydhet in (4, 5):
            with self.subTest(fornoydhet=fornoydhet):
                status = vurder_historikk([self.reg(1, fornoydhet, ("utsikt", "topptur"))])
                self.assertEqual(status.foretrukne_turtyper, frozenset({"utsikt", "topptur"}))

    def test_fornoydhet_1_til_3_gir_ingen_preferanse(self):
        for fornoydhet in (1, 2, 3):
            with self.subTest(fornoydhet=fornoydhet):
                status = vurder_historikk([self.reg(1, fornoydhet, ("utsikt",))])
                self.assertEqual(status.foretrukne_turtyper, frozenset())

    def test_senere_lav_fornoydhet_fjerner_ikke_preferansen(self):
        status = vurder_historikk([self.reg(1, 5, ("utsikt",)), self.reg(2, 1, ("utsikt",))])
        self.assertEqual(status.foretrukne_turtyper, frozenset({"utsikt"}))

    def test_ingen_registreringer_gir_tomt_sett(self):
        self.assertEqual(vurder_historikk([]).foretrukne_turtyper, frozenset())

    def test_standardverdier_gir_eksisterende_kall_uendret(self):
        r = Registrering(1, START, "t", GRONN, "lett", 5)
        self.assertEqual(r.turtyper, ())
        self.assertEqual(vurder_historikk([r]).foretrukne_turtyper, frozenset())


if __name__ == "__main__":
    unittest.main()
