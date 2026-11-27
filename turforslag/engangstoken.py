"""Engangstoken for «Registrer gjennomført tur» (AD-14, FR-16).

Tokenet lages når skjemaet vises og følger det som skjult felt. Første gyldige POST bruker det
opp, så dobbeltklikk og dobbel POST gir bare én registrering. Tokenene ligger i økten under en
egen nøkkel (ikke `sok`), de 10 nyeste, så flere faner virker. Økten tømmes aldri.
"""

import secrets

NOKKEL = "registrering_token"
MAKS_TOKEN = 10


def _alle(request) -> list[str]:  # AD-14
    verdi = request.session.get(NOKKEL)
    return [t for t in verdi if isinstance(t, str)] if isinstance(verdi, list) else []


def lag(request) -> str:  # AD-14
    """Lager et nytt token og lagrer det i økten."""
    token = secrets.token_urlsafe(24)
    request.session[NOKKEL] = [*_alle(request), token][-MAKS_TOKEN:]
    return token


def _finn(request, token: str) -> str | None:
    funnet = None
    for lagret in _alle(request):  # ingen tidlig exit, så sammenligningen tar like lang tid
        if secrets.compare_digest(lagret.encode(), token.encode()):
            funnet = lagret
    return funnet


def er_gyldig(request, token: str) -> bool:  # AD-14
    """Om tokenet er lagret i økten og ikke brukt."""
    return bool(token) and _finn(request, token) is not None


def bruk(request, token: str) -> bool:  # AD-14
    """Bruker opp tokenet. `True` bare første gang."""
    funnet = _finn(request, token) if token else None
    if funnet is None:
        return False
    request.session[NOKKEL] = [t for t in _alle(request) if t != funnet]
    return True
