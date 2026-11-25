"""Sammensetningen av turdatabasen i `data/turer.geojson` (FR-1, story 1.7).

Testen leser den committede fila og går uten nett. Den antar ikke nøyaktig 15 turer,
bare minst 15, så den gjelder også når lista utvides (story 6.2).

Reglene (FR-1):

- flertallet er grønne eller blå;
- minst én svart tur, minst tre toppturer og minst fem utsiktsturer;
- hvert startpunkt har minst to turer;
- hver turtype har en grønn tur under 2 t (`estimert_tid_min < 120`), unntatt turtypene i
  `UNNTAK_GRONN_UNDER_2_T`. Hvert unntak er begrunnet i `data/README.md`;
- hver tur har kilde og lisens.
"""

import json
import unittest
from collections import Counter
from dataclasses import replace
from pathlib import Path

from domene.tur import TURTYPER, Tur, Turniva

ROT = Path(__file__).resolve().parents[2]
TURFIL = ROT / "data" / "turer.geojson"
README = ROT / "data" / "README.md"

MIN_TURER = 15
MIN_SVARTE = 1
MIN_TOPPTURER = 3
MIN_UTSIKTSTURER = 5
MIN_TURER_PER_STARTPUNKT = 2
KORT_TUR_MIN = 120  # «under 2 t»
KILDE = "turrutebasen"
LISENS = "CC BY 4.0"

# Turtyper der terrenget ikke gir en grønn tur under 2 t (beslutning 3, 2026-11-25).
# Begrunnelsen står i data/README.md under «Sammensetning og unntak».
UNNTAK_GRONN_UNDER_2_T = frozenset({"topptur", "utsikt"})


def les_turer(sti: Path = TURFIL) -> list[Tur]:
    data = json.loads(sti.read_text(encoding="utf-8"))
    return [Tur.fra_geojson_feature(feature) for feature in data["features"]]


def antall_per_niva_og_turtype(turer: list[Tur]) -> str:
    niva = Counter(tur.turniva.value for tur in turer)
    turtype = Counter(t for tur in turer for t in tur.turtyper)
    return (
        f"{len(turer)} turer; nivå: "
        + ", ".join(f"{n.value} {niva[n.value]}" for n in Turniva)
        + "; turtyper: "
        + ", ".join(f"{t} {turtype[t]}" for t in TURTYPER)
    )


def brudd(turer: list[Tur], unntak: frozenset[str] = UNNTAK_GRONN_UNDER_2_T) -> list[str]:  # FR-1
    """Alle regler som brytes, som norske meldinger. Tom liste betyr at sammensetningen holder."""
    feil = []
    antall = len(turer)
    if antall < MIN_TURER:
        feil.append(f"Turdatabasen har {antall} turer, men skal ha minst {MIN_TURER}.")

    gronn_bla = sum(tur.turniva in (Turniva.GRONN, Turniva.BLA) for tur in turer)
    if gronn_bla * 2 <= antall:
        feil.append(f"Flertallet skal være grønne eller blå, men det er {gronn_bla} av {antall}.")

    minimum = {
        "svarte turer": (sum(t.turniva is Turniva.SVART for t in turer), MIN_SVARTE),
        "toppturer": (sum("topptur" in t.turtyper for t in turer), MIN_TOPPTURER),
        "utsiktsturer": (sum("utsikt" in t.turtyper for t in turer), MIN_UTSIKTSTURER),
    }
    for hva, (funnet, krav) in minimum.items():
        if funnet < krav:
            feil.append(f"Det skal være minst {krav} {hva}, fant {funnet}.")

    per_startpunkt = Counter(tur.startpunkt_id for tur in turer)
    for startpunkt_id, n in sorted(per_startpunkt.items()):
        if n < MIN_TURER_PER_STARTPUNKT:
            feil.append(
                f"Startpunktet «{startpunkt_id}» har {n} tur, men skal ha minst "
                f"{MIN_TURER_PER_STARTPUNKT}."
            )

    for turtype in TURTYPER:
        har_kort_gronn = any(
            turtype in tur.turtyper
            and tur.turniva is Turniva.GRONN
            and tur.estimert_tid_min < KORT_TUR_MIN
            for tur in turer
        )
        if not har_kort_gronn and turtype not in unntak:
            feil.append(
                f"Turtypen «{turtype}» har ingen grønn tur under 2 t og står ikke i unntakslista."
            )
        if har_kort_gronn and turtype in unntak:
            feil.append(
                f"Turtypen «{turtype}» har nå en grønn tur under 2 t. Fjern den fra "
                "unntakslista og fra data/README.md."
            )

    for tur in turer:
        if (tur.kilde, tur.lisens) != (KILDE, LISENS):
            feil.append(
                f"Turen «{tur.id}» har kilde {tur.kilde!r} og lisens {tur.lisens!r} "
                f"(skal være {KILDE!r} og {LISENS!r})."
            )
    return feil


class SammensetningTest(unittest.TestCase):
    def setUp(self):
        self.turer = les_turer()

    def test_turdatabasen_folger_reglene_i_fr_1(self):  # FR-1
        oversikt = antall_per_niva_og_turtype(self.turer)
        print(f"\nSammensetning: {oversikt}")
        self.assertEqual(brudd(self.turer), [], oversikt)

    def test_unntakene_er_begrunnet_i_data_readme(self):  # FR-1
        tekst = README.read_text(encoding="utf-8")
        self.assertTrue(
            "## Sammensetning og unntak" in tekst,
            "data/README.md mangler avsnittet «Sammensetning og unntak».",
        )
        avsnitt = tekst.split("## Sammensetning og unntak", 1)[1].split("\n## ", 1)[0]
        for turtype in sorted(UNNTAK_GRONN_UNDER_2_T):
            with self.subTest(turtype=turtype):
                self.assertTrue(
                    f"`{turtype}`" in avsnitt,
                    f"Unntaket for «{turtype}» er ikke begrunnet i data/README.md.",
                )


class RegelbruddTest(unittest.TestCase):
    """Reglene feiler med en melding som sier hva som brytes (kopier i minnet)."""

    def setUp(self):
        self.turer = les_turer()

    def assert_brudd(self, turer, *deler, unntak=UNNTAK_GRONN_UNDER_2_T):
        meldinger = brudd(turer, unntak)
        self.assertTrue(meldinger, "Forventet minst ett brudd.")
        tekst = "\n".join(meldinger)
        for del_ in deler:
            self.assertIn(del_, tekst)

    def test_uten_svart_tur_feiler(self):  # FR-1
        uten = [t for t in self.turer if t.turniva is not Turniva.SVART]
        self.assert_brudd(uten, "svarte turer", "fant 0")

    def test_startpunkt_med_en_tur_feiler_med_startpunkt_id(self):  # FR-1
        startpunkt_id = self.turer[0].startpunkt_id
        fjern = next(t for t in self.turer[1:] if t.startpunkt_id == startpunkt_id)
        kopi = [t for t in self.turer if t is not fjern]
        # Startpunktet med flest turer kan ha mer enn to; fjern til det har én.
        while sum(t.startpunkt_id == startpunkt_id for t in kopi) > 1:
            kopi.remove(next(t for t in kopi[1:] if t.startpunkt_id == startpunkt_id))
        self.assert_brudd(kopi, f"«{startpunkt_id}»", "minst 2")

    def test_turtype_uten_kort_gronn_tur_godtas_bare_med_unntak(self):  # FR-1
        self.assert_brudd(
            self.turer, *(f"«{t}»" for t in UNNTAK_GRONN_UNDER_2_T), unntak=frozenset()
        )
        # Uten de korte grønne markaturene feiler «marka», som ikke er et unntak.
        kopi = [
            replace(t, turniva=Turniva.BLA)
            if t.turniva is Turniva.GRONN and t.estimert_tid_min < KORT_TUR_MIN
            else t
            for t in self.turer
        ]
        self.assert_brudd(kopi, "«marka»", "unntakslista")

    def test_unodvendig_unntak_feiler(self):  # FR-1
        kort = replace(
            self.turer[0],
            turtyper=("marka", "utsikt", "topptur"),
            turniva=Turniva.GRONN,
            estimert_tid_min=60,
        )
        self.assert_brudd([kort, *self.turer[1:]], "Fjern den fra unntakslista")

    def test_for_fa_turer_feiler(self):  # FR-1
        self.assert_brudd(self.turer[: MIN_TURER - 1], f"minst {MIN_TURER}")

    def test_flertall_rode_og_svarte_feiler(self):  # FR-1
        kopi = [replace(t, turniva=Turniva.ROD) for t in self.turer]
        self.assert_brudd(kopi, "Flertallet")

    def test_for_fa_toppturer_og_utsiktsturer_feiler(self):  # FR-1
        kopi = [replace(t, turtyper=("marka",)) for t in self.turer]
        self.assert_brudd(kopi, "toppturer", "utsiktsturer")

    def test_tur_uten_kilde_og_lisens_feiler(self):  # FR-1
        kopi = [replace(self.turer[0], kilde="", lisens=""), *self.turer[1:]]
        self.assert_brudd(kopi, f"«{self.turer[0].id}»", "kilde")
