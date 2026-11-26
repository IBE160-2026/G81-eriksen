"""Begrunnelsen fra reservemalen, brukt når KI ikke skriver den (FR-12, FR-13).

Malen nevner turens tid, varigheten i søket og turtypen når den er valgt. Den nevner aldri
fritekstønsket. Den har ikke med turnavnet eller annen tekst av ukjent lengde, så den holder
seg alltid under `MAKS_TEGN` (testet for alle varigheter og turtyper). Tall og turtype
settes inn av systemet.
"""

from domene.sok import Sok
from domene.tekst import formater_tid, formater_varighet_timer
from domene.tur import Tur
from domene.utvalg import ERSTATNING_FOR_TOPPTUR, TOPPTUR

MAKS_TEGN = 300  # FR-12

# Hvordan turtypen nevnes i en setning: «Den har utsikt, som du ba om.»
_TURTYPE_I_SETNING = {
    "marka": "går i marka",
    "utsikt": "har utsikt",
    "topptur": "går til en topp",
}


def reservebegrunnelse(sok: Sok, tur: Tur) -> str:  # FR-12, FR-13
    """«Turen tar ca. 2 t og passer innenfor 2,5 timer. Den har utsikt, som du ba om.»

    Er topptur erstattet med en utsiktstur (FR-8), sier malen at turen har utsikt i stedet.
    """
    tekst = (
        f"Turen tar {formater_tid(tur.estimert_tid_min)} og passer innenfor "
        f"{formater_varighet_timer(sok.varighet_min)}."
    )
    if sok.turtype is not None and sok.turtype in tur.turtyper:
        tekst += f" Den {_TURTYPE_I_SETNING[sok.turtype]}, som du ba om."
    elif sok.turtype == TOPPTUR and ERSTATNING_FOR_TOPPTUR in tur.turtyper:
        tekst += " Ingen topptur passet, så den har utsikt i stedet."
    return tekst
