"""Kobler views til `domene/` og databasen: søk, turforslag og startpunktvalg (AR-2, FR-5).

Views kaller bare funksjonene her og regner, filtrerer og formaterer ingenting selv. Her
hentes turene fra databasen, og så gjør `domene/` utvalget, begrunnelsen og formateringen.
"""

from collections.abc import Callable

from domene import tekst
from domene.begrunnelse import reservebegrunnelse
from domene.okt import Soketilstand, alle_vist, neste_forslag, ny_soketilstand, start_pa_nytt
from domene.sok import Sok
from domene.tur import Tur
from domene.utvalg import NIVATAK_UTEN_HISTORIKK, Status, innenfor_tid_og_nivatak, velg_turer
from turforslag import turdata


def startpunktvalg() -> tuple[tuple[str, str], ...]:  # FR-4
    """Startpunktene som har turer, som (id, navn) sortert på navn etter norsk alfabet."""
    return tekst.sorter_startpunkter(turdata.startpunkter_med_turer())


def utfor_sok(sok: Sok) -> Soketilstand:  # FR-5, FR-8, FR-18
    """Velger og rangerer turene for en gjest (grønt nivåtak) og fryser rangeringen."""
    utvalg = velg_turer(sok, turdata.alle_turer(), NIVATAK_UTEN_HISTORIKK)
    return ny_soketilstand(sok, utvalg)


def _passer(tur: Tur, sok: Sok) -> bool:  # SM-C1
    # Etter en ny `lastinn` kan turen ha fått høyere nivå eller lengre tid.
    return innenfor_tid_og_nivatak(tur, sok, NIVATAK_UTEN_HISTORIKK)


def _gyldig(sok: Sok) -> Callable[[str], bool]:  # FR-7, SM-C1
    """Om turen finnes og fortsatt passer søket. Turer som ikke gjør det, hoppes over."""

    def gyldig(tur_id: str) -> bool:
        tur = turdata.hent_tur(tur_id)
        return tur is not None and _passer(tur, sok)

    return gyldig


def nytt_forslag(tilstand: Soketilstand, fra_tur_id: str | None) -> Soketilstand:  # FR-7
    """«Nytt forslag»: neste gyldige tur i den frosne rangeringen, uten ny rangering.

    Går bare videre når `fra_tur_id` er gjeldende tur (dobbeltklikk og gamle POST-er).
    """
    return neste_forslag(tilstand, fra_tur_id, _gyldig(tilstand.sok))


def forfra(tilstand: Soketilstand) -> Soketilstand:  # FR-7
    """«Start fra første forslag igjen»: første gyldige tur, med listen over viste på nytt.

    Gjelder bare ved «alle vist». Ellers gis samme tilstand.
    """
    ny = start_pa_nytt(tilstand)
    gyldig = _gyldig(tilstand.sok)
    if ny != tilstand and ny.gjeldende_tur_id is not None and not gyldig(ny.gjeldende_tur_id):
        ny = neste_forslag(ny, ny.gjeldende_tur_id, gyldig)
    return ny


def forslagsvisning(tilstand: Soketilstand) -> tekst.Forslagsvisning | None:  # FR-6, FR-7
    """Visningen av gjeldende tur uten ny rangering, eller Tilstandspanelet.

    Ved «alle vist» gis Tilstandspanelet med antallet turer som fortsatt passer (er det
    ingen, gis `None`). Ellers gis `None` når
    tilstanden ikke peker på en tur som finnes, eller når turen ikke lenger passer varigheten
    eller nivåtaket (SM-C1). Da behandles søke-ID-en som ukjent.
    """
    startpunkt_navn = None
    if tilstand.sok.startpunkt_id is not None:
        startpunkt_navn = dict(turdata.startpunkter_med_turer()).get(tilstand.sok.startpunkt_id)
    if tilstand.status in (Status.INGEN_TREFF, Status.BARE_OVER_NIVATAK):  # FR-8
        return tekst.forslagsvisning(tilstand, None, startpunkt_navn=startpunkt_navn)
    if tilstand.gjeldende_tur_id is None:
        if not alle_vist(tilstand):
            return None
        # FR-7: ingressen teller bare turene som fortsatt finnes og passer (SM-C1). Er ingen
        # igjen, behandles søke-ID-en som ukjent.
        gyldig = _gyldig(tilstand.sok)
        antall = sum(1 for tur_id in tilstand.rangerte_tur_ider if gyldig(tur_id))
        if antall == 0:
            return None
        return tekst.forslagsvisning(tilstand, None, startpunkt_navn=startpunkt_navn, antall=antall)
    tur = turdata.hent_tur(tilstand.gjeldende_tur_id)
    if tur is None or not _passer(tur, tilstand.sok):
        return None
    return tekst.forslagsvisning(
        tilstand, tur, reservebegrunnelse(tilstand.sok, tur), startpunkt_navn
    )
