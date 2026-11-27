"""Begrunnelsen fra reservemalen, brukt når KI ikke skriver den (FR-12, FR-13).

Malen nevner turens tid, varigheten i søket og turtypen når den er valgt. Den nevner aldri
fritekstønsket. Den har ikke med turnavnet eller annen tekst av ukjent lengde, så den holder
seg alltid under `MAKS_TEGN` (testet for alle varigheter og turtyper). Tall og turtype
settes inn av systemet.
"""

from collections.abc import Iterable
from datetime import date

from domene.niva import Sperre
from domene.sok import Sok
from domene.tekst import formater_dato, formater_tid, formater_varighet_timer, nivaord
from domene.tur import NIVAREKKEFOLGE, TURTYPER, Tur, Turniva
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


# Turtypen som «en utsiktstur» og «utsiktsturer» i preferansesetningen (FR-20)
_TURTYPE_ENTALL_OG_FLERTALL = {
    "marka": ("markatur", "markaturer"),
    "utsikt": ("utsiktstur", "utsiktsturer"),
    "topptur": ("topptur", "toppturer"),
}


def preferansesetning(
    tur: Tur, foretrukne_turtyper: Iterable[str], treff: Iterable[Tur]
) -> str:  # FR-20, FR-12
    """«Du får en utsiktstur fordi du har vært fornøyd med utsiktsturer før.»

    Ordet er turens første turtype (marka, utsikt, topptur) som også er foretrukket. Setningen
    kommer bare når turen har en foretrukket turtype og minst ett annet treff i søket ikke
    har det, ellers ville den ikke forklart hvorfor akkurat denne turen vises.

    [ASSUMPTION] Teksten er foreløpig til produkteier har godkjent den (Mikrotekst).
    """
    foretrukne = frozenset(foretrukne_turtyper)
    ord_ = next((t for t in TURTYPER if t in foretrukne and t in tur.turtyper), None)
    if ord_ is None:
        return ""
    if all(not foretrukne.isdisjoint(andre.turtyper) for andre in treff):
        return ""
    en, flere = _TURTYPE_ENTALL_OG_FLERTALL[ord_]
    return f"Du får en {en} fordi du har vært fornøyd med {flere} før."


def historikkbegrunnelse(dato: date, fornoydhet: int) -> str:  # FR-17, FR-12
    """«Du gikk denne turen 12. oktober og ga den 5 av 5.» Fast mal uten KI for turforslag
    fra historikken. Dato og vurdering kommer fra registreringen lenken peker på."""
    return f"Du gikk denne turen {formater_dato(dato)} og ga den {fornoydhet} av 5."
