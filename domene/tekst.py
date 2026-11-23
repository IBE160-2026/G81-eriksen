"""Norsk formatering av tid, lengde og nivå (UX-DR31, AR-16).

Faste formater: «ca. 1 t 35 min», «3,5 km totalt» og «Grønn – lett».
"""

from decimal import ROUND_HALF_UP, Decimal

from domene.tur import Turniva

_NIVATEKST = {
    Turniva.GRONN: "Grønn – lett",
    Turniva.BLA: "Blå – moderat",
    Turniva.ROD: "Rød – moderat",
    Turniva.SVART: "Svart – vanskelig",
}


def formater_tid(minutter: int) -> str:  # FR-3, UX-DR31
    """«ca. 45 min», «ca. 2 t» eller «ca. 1 t 35 min»."""
    timer, rest = divmod(minutter, 60)
    if timer == 0:
        return f"ca. {rest} min"
    if rest == 0:
        return f"ca. {timer} t"
    return f"ca. {timer} t {rest} min"


def formater_lengde_totalt(lengde_m: int) -> str:  # UX-DR31, AR-16
    """«3,5 km totalt»: én desimal med desimalkomma, avrundet halv opp, uten «,0».

    `lengde_m` er lengden for hele turen, ikke den lagrede lengden for én vei ved
    tur-retur. Den som kaller, regner den ut med `domene.tur.total_lengde_m` først.
    """
    km = (Decimal(lengde_m) / 1000).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
    if km == km.to_integral_value():
        return f"{int(km)} km totalt"
    return f"{km:f}".replace(".", ",") + " km totalt"


def formater_niva(niva: Turniva) -> str:  # FR-2, UX-DR31
    """«Grønn – lett», «Blå – moderat», «Rød – moderat» eller «Svart – vanskelig»."""
    return _NIVATEKST[niva]
