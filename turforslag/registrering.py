"""Kobler views til `domene/` og databasen: registrering og Historikk (AR-2, FR-16, FR-17).

Alt hentes filtrert på brukeren (NFR-8). Formateringen gjøres i `domene/tekst.py`.
"""

from datetime import date

from domene import tekst
from domene.begrunnelse import historikkbegrunnelse
from domene.niva import NivaStatus, nivaheving, vurder_historikk
from domene.niva import Registrering as DomeneRegistrering
from domene.tur import Turniva
from domene.utvalg import NIVATAK_UTEN_HISTORIKK, er_over_nivatak
from turforslag import turdata
from turforslag.models import Registrering, Tur


def oppsummering(tur_id: str) -> tekst.Turoppsummering | None:  # FR-16
    """Turoppsummeringen for turen, eller `None` når turen ikke finnes."""
    tur = turdata.hent_tur(tur_id)
    return tekst.turoppsummering(tur) if tur else None


def lagre(bruker, tur_id: str, dato: date, brukt_tid_min: int, vanskelighet: str, fornoydhet: str):
    """Lagrer registreringen for brukeren og turen. Turen må finnes."""
    return Registrering.objects.create(
        bruker=bruker,
        tur=Tur.objects.get(id=tur_id),
        dato=dato,
        brukt_tid_min=brukt_tid_min,
        vanskelighet=vanskelighet,
        fornoydhet=int(fornoydhet),
    )


def domeneregistreringer(bruker) -> tuple[DomeneRegistrering, ...]:  # FR-19, NFR-8
    """Brukerens egne registreringer som domeneobjekter. Gjester har ingen."""
    if not getattr(bruker, "is_authenticated", False):
        return ()
    return tuple(
        DomeneRegistrering(
            id=r.id,
            dato=r.dato,
            tur_id=r.tur_id,
            turniva=Turniva(r.tur.turniva),
            vanskelighet=r.vanskelighet,
            fornoydhet=r.fornoydhet,
            turtyper=tuple(r.tur.turtyper),
        )
        for r in Registrering.objects.filter(bruker=bruker).select_related("tur")
    )


def vurder_bruker(bruker) -> tuple[tuple[DomeneRegistrering, ...], NivaStatus | None]:  # FR-19
    """Registreringene og nivåstatusen til en innlogget bruker. Gjester gir `((), None)`."""
    if not getattr(bruker, "is_authenticated", False):
        return (), None
    registreringer = domeneregistreringer(bruker)
    return registreringer, vurder_historikk(registreringer)


def avgjor_nivaheving(bruker, status: NivaStatus) -> bool:  # FR-19, AD-11
    """Om søket er første etter en heving. Lagrer `brukt_heving` som `antall_hevinger`."""
    heving = nivaheving(status, bruker.brukt_heving)
    if bruker.brukt_heving != status.antall_hevinger:
        bruker.brukt_heving = status.antall_hevinger
        bruker.save(update_fields=["brukt_heving"])
    return heving


def historikk(bruker) -> tuple[tekst.Historikkrad, ...]:  # FR-17, NFR-8
    """Brukerens egne registreringer, nyeste først, én rad per registrering."""
    registreringer = (
        Registrering.objects.filter(bruker=bruker)
        .select_related("tur__startpunkt")
        .order_by("-dato", "-id")
    )
    return tuple(
        tekst.historikkrad(
            r.id,
            turdata.tur_fra_modell(r.tur),
            r.dato,
            r.brukt_tid_min,
            r.vanskelighet,
            r.fornoydhet,
        )
        for r in registreringer
    )


def historikkvisning(bruker, registrering_id: int) -> tekst.Forslagsvisning | None:  # FR-17
    """Turforslaget fra brukerens egen registrering. `None` når registreringen ikke er
    brukerens eller ikke finnes, eller når turen ikke finnes i turdatabasen. Rører ikke
    søketilstanden."""
    r = (
        Registrering.objects.filter(bruker=bruker, id=registrering_id)
        .select_related("tur__startpunkt")
        .first()
    )
    tur = turdata.hent_tur(r.tur_id) if r else None
    if r is None or tur is None:
        return None
    _, status = vurder_bruker(bruker)
    nivatak = status.nivatak if status else NIVATAK_UTEN_HISTORIKK
    return tekst.historikkvisning(
        tur, historikkbegrunnelse(r.dato, r.fornoydhet), er_over_nivatak(tur, nivatak)
    )
