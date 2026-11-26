"""Søketilstanden i økten (AD-5, AR-7, FR-7).

Bare denne modulen leser og skriver `request.session["sok"]`, og alltid hele verdien, så
Django merker endringen. Verdien er en ordbok fra søke-ID til `Soketilstand.til_dict()`,
eldst først, med de 10 nyeste søkene. Hver gyldig POST gir en ny søke-ID, så to faner har
hvert sitt forslag. Økten tømmes aldri (`flush`, `cycle_key` og `clear` brukes ikke).
"""

import logging
import secrets
from typing import Any

from domene.okt import Soketilstand

logger = logging.getLogger(__name__)

OKTNOKKEL = "sok"
MAKS_SOK = 10


def _alle(request) -> dict[str, Any]:  # AD-5
    verdi = request.session.get(OKTNOKKEL)
    return dict(verdi) if isinstance(verdi, dict) else {}


def nyeste_10(sokene: dict[str, Any]) -> dict[str, Any]:  # AD-5, AR-7
    """De `MAKS_SOK` siste søkene i ordboka (innsettingsrekkefølgen er eldst først)."""
    return dict(list(sokene.items())[-MAKS_SOK:])


def lagre_sok(request, tilstand: Soketilstand) -> str:  # AD-5, FR-7
    """Lagrer tilstanden under en ny, tilfeldig søke-ID og gir ID-en tilbake."""
    sokene = _alle(request)
    sok_id = secrets.token_urlsafe(16)
    while sok_id in sokene:  # pragma: no cover - praktisk talt umulig
        sok_id = secrets.token_urlsafe(16)
    sokene[sok_id] = tilstand.til_dict()
    request.session[OKTNOKKEL] = nyeste_10(sokene)
    return sok_id


def hent_sok(request, sok_id: str) -> Soketilstand | None:  # AD-5, FR-7
    """Tilstanden for søke-ID-en, eller `None` når ID-en er ukjent eller verdien er ugyldig."""
    data = _alle(request).get(sok_id)
    if not isinstance(data, dict):
        return None
    try:
        return Soketilstand.fra_dict(data)
    except ValueError:
        logger.warning("Ugyldig søketilstand i økten. Søke-ID-en behandles som ukjent.")
        return None
