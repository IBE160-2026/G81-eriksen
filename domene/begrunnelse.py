"""Begrunnelsen fra reservemalen, brukt når KI ikke skriver den (FR-12, FR-13).

Malen nevner turens tid, varigheten i søket og turtypen når den er valgt. Den nevner aldri
fritekstønsket. Den har ikke med turnavnet eller annen tekst av ukjent lengde, så den holder
seg alltid under `MAKS_TEGN` (testet for alle varigheter og turtyper). Tall og turtype
settes inn av systemet.
"""

from datetime import date

from domene.niva import Sperre
from domene.sok import Sok
from domene.tekst import formater_dato, formater_tid, formater_varighet_timer, nivaord
from domene.tur import NIVAREKKEFOLGE, Tur, Turniva
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


def personaliseringssetning(
    turniva: Turniva, nivatak: Turniva, nivaheving: bool, sperre: Sperre | None
) -> str:  # FR-12, FR-19
    """Setningen som forklarer nivået, lagt til etter malteksten. Høyst én: sperre, ellers
    heving, ellers nådd nivå. Grønn tur uten sperre gir ingen setning.

    [ASSUMPTION] Sperresetningen og nådd-nivå-setningen er foreløpige til produkteier har
    godkjent dem (Mikrotekst). Ingen tall i setningene.
    """
    if sperre is not None:
        return (
            f"Du får en {nivaord(turniva)} tur igjen fordi den siste "
            f"{nivaord(sperre.turniva, 'bestemt')} turen føltes vanskelig."
        )
    if turniva == NIVAREKKEFOLGE[0]:
        return ""
    if nivaheving and turniva == nivatak:
        under = NIVAREKKEFOLGE[NIVAREKKEFOLGE.index(turniva) - 1]
        return (
            f"Du får en {nivaord(turniva)} tur fordi de tre siste "
            f"{nivaord(under, 'bestemt')} turene var lette for deg."
        )
    return (
        f"Du får en {nivaord(turniva)} tur fordi du har nådd {nivaord(turniva, 'intetkjonn')} nivå."
    )


def historikkbegrunnelse(dato: date, fornoydhet: int) -> str:  # FR-17, FR-12
    """«Du gikk denne turen 12. oktober og ga den 5 av 5.» Fast mal uten KI for turforslag
    fra historikken. Dato og vurdering kommer fra registreringen lenken peker på."""
    return f"Du gikk denne turen {formater_dato(dato)} og ga den {fornoydhet} av 5."
