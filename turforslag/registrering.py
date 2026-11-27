"""Kobler views til `domene/` og databasen: registrering og Historikk (AR-2, FR-16, FR-17).

Alt hentes filtrert på brukeren (NFR-8). Formateringen gjøres i `domene/tekst.py`.
"""

from datetime import date

from domene import tekst
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


def historikk(bruker) -> tuple[tekst.Historikkrad, ...]:  # FR-17, NFR-8
    """Brukerens egne registreringer, nyeste først, én rad per registrering."""
    registreringer = (
        Registrering.objects.filter(bruker=bruker)
        .select_related("tur__startpunkt")
        .order_by("-dato", "-id")
    )
    return tuple(
        tekst.historikkrad(
            turdata.tur_fra_modell(r.tur),
            r.dato,
            r.brukt_tid_min,
            r.vanskelighet,
            r.fornoydhet,
        )
        for r in registreringer
    )
