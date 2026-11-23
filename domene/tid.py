"""Estimert tid etter sveitsisk regel med påslag for nybegynnere (FR-3).

(15 min/km + 15 min/100 hm opp + 15 min/200 m ned) × 1,15, regnet på totalene for hele
turen og avrundet halv opp til nærmeste 5 minutter. Regningen gjøres med brøker, så
avrundingen ikke påvirkes av flyttallsfeil.
"""

import math
from fractions import Fraction

from domene.tur import Form, total_hoydemeter_m, total_lengde_m, total_nedstigning_m

MIN_PER_KM = 15
MIN_PER_100_HM_OPP = 15
MIN_PER_200_M_NED = 15
PASLAG_NYBEGYNNER = Fraction(115, 100)
AVRUNDING_MIN = 5


def _ra_tid_brok(lengde_m: int, opp_m: int, ned_m: int) -> Fraction:  # FR-3
    return (
        Fraction(lengde_m * MIN_PER_KM, 1000)
        + Fraction(opp_m * MIN_PER_100_HM_OPP, 100)
        + Fraction(ned_m * MIN_PER_200_M_NED, 200)
    ) * PASLAG_NYBEGYNNER


def ra_tid_min(lengde_m: int, opp_m: int, ned_m: int) -> float:  # FR-3
    """Rå tid i minutter for totalene, med påslaget på 15 %, før avrunding."""
    return float(_ra_tid_brok(lengde_m, opp_m, ned_m))


def avrund_til_5(minutter: float | Fraction) -> int:  # FR-3
    """Avrunder halv opp til nærmeste 5 minutter (2,5 går opp). Bruker ikke `round()`,
    som runder halve tall til nærmeste partall."""
    return math.floor(Fraction(minutter) / AVRUNDING_MIN + Fraction(1, 2)) * AVRUNDING_MIN


def estimert_tid_min(  # FR-3
    form: Form, lengde_m: int, hoydemeter_m: int, nedstigning_m: int
) -> int:
    """Estimert tid for hele turen ut fra de lagrede verdiene (én vei ved tur-retur)."""
    ra = _ra_tid_brok(
        total_lengde_m(form, lengde_m),
        total_hoydemeter_m(form, hoydemeter_m, nedstigning_m),
        total_nedstigning_m(form, hoydemeter_m, nedstigning_m),
    )
    return avrund_til_5(ra)
