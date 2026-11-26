"""Kobler views til `domene/` og databasen: søk, turforslag og startpunktvalg (AR-2, FR-5).

Views kaller bare funksjonene her og regner, filtrerer og formaterer ingenting selv. Her
hentes turene fra databasen, og så gjør `domene/` utvalget, begrunnelsen og formateringen.
"""

from domene import tekst
from domene.begrunnelse import reservebegrunnelse
from domene.okt import Soketilstand, ny_soketilstand
from domene.sok import Sok
from domene.utvalg import NIVATAK_UTEN_HISTORIKK, Status, innenfor_tid_og_nivatak, velg_turer
from turforslag import turdata


def startpunktvalg() -> tuple[tuple[str, str], ...]:  # FR-4
    """Startpunktene som har turer, som (id, navn) sortert på navn etter norsk alfabet."""
    return tekst.sorter_startpunkter(turdata.startpunkter_med_turer())


def utfor_sok(sok: Sok) -> Soketilstand:  # FR-5, FR-8, FR-18
    """Velger og rangerer turene for en gjest (grønt nivåtak) og fryser rangeringen."""
    utvalg = velg_turer(sok, turdata.alle_turer(), NIVATAK_UTEN_HISTORIKK)
    return ny_soketilstand(sok, utvalg)


def forslagsvisning(tilstand: Soketilstand) -> tekst.Forslagsvisning | None:  # FR-6, FR-7
    """Visningen av gjeldende tur uten ny rangering, eller Tilstandspanelet.

    Gir `None` når tilstanden ikke peker på en tur som finnes, eller når turen ikke lenger
    passer varigheten eller nivåtaket (SM-C1). Da behandles søke-ID-en som ukjent.
    """
    startpunkt_navn = None
    if tilstand.sok.startpunkt_id is not None:
        startpunkt_navn = dict(turdata.startpunkter_med_turer()).get(tilstand.sok.startpunkt_id)
    if tilstand.status in (Status.INGEN_TREFF, Status.BARE_OVER_NIVATAK):  # FR-8
        return tekst.forslagsvisning(tilstand, None, startpunkt_navn=startpunkt_navn)
    if tilstand.gjeldende_tur_id is None:
        return None
    tur = turdata.hent_tur(tilstand.gjeldende_tur_id)
    # SM-C1: etter en ny `lastinn` kan turen ha fått høyere nivå eller lengre tid.
    if tur is None or not innenfor_tid_og_nivatak(tur, tilstand.sok, NIVATAK_UTEN_HISTORIKK):
        return None
    return tekst.forslagsvisning(
        tilstand, tur, reservebegrunnelse(tilstand.sok, tur), startpunkt_navn
    )
