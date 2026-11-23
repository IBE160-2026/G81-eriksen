"""Turnivå etter Merkehåndboka (2019, s. 100–101) (FR-2, AR-19).

Grensene skrives med «<»: en verdi akkurat på grensen graderes opp, og svart betyr
≥ 20 km eller ≥ 1000 hm. Den strengeste av lengde og høydemeter vinner.

Tur-retur graderes etter verdiene for én vei og rundtur etter hele runden. Det er i
begge tilfeller de lagrede feltene `lengde_m` og `hoydemeter_m` i `Tur`.
"""

from domene.tur import Turniva

# Øvre grense (ikke med) for hvert nivå, i meter (FR-2, AR-19).
GRONN_LENGDE_UNDER_M = 5_000
GRONN_HOYDEMETER_UNDER_M = 300
BLA_LENGDE_UNDER_M = 10_000
BLA_HOYDEMETER_UNDER_M = 600
ROD_LENGDE_UNDER_M = 20_000
ROD_HOYDEMETER_UNDER_M = 1_000

_GRENSER = (
    (Turniva.GRONN, GRONN_LENGDE_UNDER_M, GRONN_HOYDEMETER_UNDER_M),
    (Turniva.BLA, BLA_LENGDE_UNDER_M, BLA_HOYDEMETER_UNDER_M),
    (Turniva.ROD, ROD_LENGDE_UNDER_M, ROD_HOYDEMETER_UNDER_M),
)


def turniva(lengde_m: int, hoydemeter_m: int) -> Turniva:  # FR-2, AR-19
    """Gir det letteste nivået der både lengden og høydemeterne er under grensene."""
    for niva, lengde_under_m, hoydemeter_under_m in _GRENSER:
        if lengde_m < lengde_under_m and hoydemeter_m < hoydemeter_under_m:
            return niva
    return Turniva.SVART
