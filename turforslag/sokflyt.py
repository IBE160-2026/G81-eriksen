"""Kobler views til `domene/` og databasen: søk, turforslag og startpunktvalg (AR-2, FR-5).

Views kaller bare funksjonene her og regner, filtrerer og formaterer ingenting selv. Her
hentes turene fra databasen, og så gjør `domene/` utvalget, begrunnelsen og formateringen.
"""

from collections.abc import Callable
from dataclasses import replace

from domene import tekst
from domene.begrunnelse import reservebegrunnelse
from domene.okt import Soketilstand, alle_vist, neste_forslag, ny_soketilstand, start_pa_nytt
from domene.sok import Sok
from domene.tur import Tur, Turniva
from domene.utvalg import (
    FELT_TURTYPE,
    FELT_VARIGHET,
    NIVATAK_UTEN_HISTORIKK,
    Endringsforslag,
    Status,
    foresla_endringer,
    innenfor_tid_og_nivatak,
    velg_turer,
)
from turforslag import turdata
from turforslag.registrering import avgjor_nivaheving, vurder_bruker


def startpunktvalg() -> tuple[tuple[str, str], ...]:  # FR-4
    """Startpunktene som har turer, som (id, navn) sortert på navn etter norsk alfabet."""
    return tekst.sorter_startpunkter(turdata.startpunkter_med_turer())


def utfor_sok(sok: Sok, bruker=None) -> Soketilstand:  # FR-5, FR-8, FR-18, FR-19
    """Velger og rangerer turene og fryser rangeringen og nivåtaket. Gjester og brukere uten
    historikk har grønt tak. For en innlogget bruker styrer historikken taket og rangeringen,
    og `brukt_heving` lagres (AD-11)."""
    registreringer, status = vurder_bruker(bruker)
    nivatak = status.nivatak if status else NIVATAK_UTEN_HISTORIKK
    heving = avgjor_nivaheving(bruker, status) if status else False
    utvalg = velg_turer(
        sok, turdata.alle_turer(), nivatak, registreringer=registreringer, nivaheving=heving
    )
    return ny_soketilstand(sok, utvalg, heving, nivatak)


def _endringsforslag(tilstand: Soketilstand) -> tuple[Endringsforslag, ...]:  # FR-8, UX-DR17
    """Endringsforslagene for «ingen treff» og «alle vist». Ved «alle vist» er treffene i
    søket `tidligere_treff`, så bare endringer som gir en ny tur tas med."""
    vist = alle_vist(tilstand)
    if tilstand.status != Status.INGEN_TREFF and not vist:
        return ()
    return foresla_endringer(
        tilstand.sok,
        turdata.alle_turer(),
        tilstand.nivatak,
        tilstand.rangerte_tur_ider if vist else (),
    )


def endre_sok(
    tilstand: Soketilstand, felt: str, verdi: str, bruker=None
) -> Soketilstand | None:  # FR-8
    """Kjører søket på nytt med én endring. Feltet og verdien må være et av forslagene som
    gjelder tilstanden akkurat nå, ellers gis `None`. «Velg startpunkt» er en lenke og kan
    ikke kjøres her."""
    for forslag in _endringsforslag(tilstand):
        if forslag.er_lenke or (forslag.felt, forslag.verdi) != (felt, verdi):
            continue
        if felt == FELT_VARIGHET:
            sok = replace(tilstand.sok, varighet_min=int(verdi))
        elif felt == FELT_TURTYPE:
            sok = replace(tilstand.sok, turtype=verdi or None)
        else:  # pragma: no cover - bare startpunkt, som er en lenke
            continue
        return utfor_sok(sok, bruker)
    return None


def _passer(tur: Tur, sok: Sok, nivatak: Turniva) -> bool:  # SM-C1
    # Etter en ny `lastinn` kan turen ha fått høyere nivå eller lengre tid.
    return innenfor_tid_og_nivatak(tur, sok, nivatak)


def _gyldig(sok: Sok, nivatak: Turniva) -> Callable[[str], bool]:  # FR-7, SM-C1
    """Om turen finnes og fortsatt passer søket. Turer som ikke gjør det, hoppes over."""

    def gyldig(tur_id: str) -> bool:
        tur = turdata.hent_tur(tur_id)
        return tur is not None and _passer(tur, sok, nivatak)

    return gyldig


def nytt_forslag(tilstand: Soketilstand, fra_tur_id: str | None) -> Soketilstand:  # FR-7
    """«Nytt forslag»: neste gyldige tur i den frosne rangeringen, uten ny rangering.

    Går bare videre når `fra_tur_id` er gjeldende tur (dobbeltklikk og gamle POST-er).
    """
    return neste_forslag(tilstand, fra_tur_id, _gyldig(tilstand.sok, tilstand.nivatak))


def forfra(tilstand: Soketilstand) -> Soketilstand:  # FR-7
    """«Start fra første forslag igjen»: første gyldige tur, med listen over viste på nytt.

    Gjelder bare ved «alle vist». Ellers gis samme tilstand.
    """
    ny = start_pa_nytt(tilstand)
    gyldig = _gyldig(tilstand.sok, tilstand.nivatak)
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
        return tekst.forslagsvisning(
            tilstand,
            None,
            startpunkt_navn=startpunkt_navn,
            endringsforslag=_endringsforslag(tilstand),
        )
    if tilstand.gjeldende_tur_id is None:
        if not alle_vist(tilstand):
            return None
        # FR-7: ingressen teller bare turene som fortsatt finnes og passer (SM-C1). Er ingen
        # igjen, behandles søke-ID-en som ukjent.
        gyldig = _gyldig(tilstand.sok, tilstand.nivatak)
        antall = sum(1 for tur_id in tilstand.rangerte_tur_ider if gyldig(tur_id))
        if antall == 0:
            return None
        return tekst.forslagsvisning(
            tilstand,
            None,
            startpunkt_navn=startpunkt_navn,
            antall=antall,
            endringsforslag=_endringsforslag(tilstand),
        )
    tur = turdata.hent_tur(tilstand.gjeldende_tur_id)
    if tur is None or not _passer(tur, tilstand.sok, tilstand.nivatak):
        return None
    return tekst.forslagsvisning(
        tilstand, tur, reservebegrunnelse(tilstand.sok, tur), startpunkt_navn
    )
