"""Systemets sjekk av KI-teksten før den vises (FR-12, FR-13, AD-10, AR-12, AR-16).

KI skriver begrunnelsen med plassholdere (`{tid}`, `{varighet}`, `{lengde}`, `{nivå}`).
`valider_begrunnelse` forkaster teksten med én årsak, eller gir den ferdige teksten der
systemet har satt inn verdiene fra turdata og søk i de samme formatene som reservemalen.
Forkastelsene er et eget begrep og ikke `KiSvar.arsak` (transportfeil, `domene.ki`).
"""

import re
import unicodedata
from collections.abc import Iterable
from dataclasses import dataclass
from enum import StrEnum

from domene.begrunnelse import MAKS_TEGN
from domene.sok import Sok
from domene.tekst import formater_lengde, formater_tid, formater_varighet_timer, nivaord
from domene.tur import Tur, total_lengde_m
from domene.utvalg import ERSTATNING_FOR_TOPPTUR, TOPPTUR, Status


class Forkastelse(StrEnum):  # FR-12, FR-13
    TOM = "tom"
    UGYLDIG = "ugyldig"
    SIFFER = "siffer"
    TALLORD = "tallord"
    NIVAORD = "nivaord"
    TURTYPE = "turtype"
    FOR_LANG = "for_lang"


@dataclass(frozen=True)
class Valideringsresultat:  # FR-12
    """Enten den ferdige `tekst`, eller en `forkastelse` med årsaken."""

    tekst: str | None = None
    forkastelse: Forkastelse | None = None

    @property
    def ok(self) -> bool:
        return self.forkastelse is None


PLASSHOLDERE = ("tid", "varighet", "lengde", "nivå")
PAAKREVD_PLASSHOLDER = "varighet"

# Hele ord, uten hensyn til store/små bokstaver. «toppen» og «tiden» er lov.
TALLORD = frozenset(
    {
        "to", "tre", "fire", "fem", "seks", "sju", "syv", "åtte", "ni", "ti", "elleve", "tolv",
        "tretten", "fjorten", "femten", "seksten", "sytten", "atten", "nitten", "tjue", "tyve",
        "tretti", "tredve", "førti", "femti", "seksti", "sytti", "åtti", "nitti",
        "hundre", "tusen", "halv", "halvannen", "halvtime", "kvarter",
    }
)  # fmt: skip
# «en», «én», «ett», «ei» er tallord bare rett foran en enhet: «en time», men ikke «en fin tur».
TALLORD_FOR_ENHET = frozenset({"en", "én", "ett", "ei"})
ENHETER = frozenset(
    {
        "time", "timer", "minutt", "minutter", "min", "sekund", "sekunder",
        "km", "kilometer", "meter", "mil",
    }
)  # fmt: skip

NIVAORD = frozenset(
    {"grønn", "grønne", "grønt", "blå", "blått", "rød", "røde", "rødt", "svart", "svarte"}
)

# Stammen som må stå i et ord (delstreng) når turtypen er valgt: «Nordmarka», «utsikten».
TURTYPE_STAMME = {"marka": "marka", "utsikt": "utsikt", "topptur": "topptur"}

_PLASSHOLDER = re.compile(r"\{(" + "|".join(PLASSHOLDERE) + r")\}")
_ORD = re.compile(r"[^\W\d_]+")
# En plassholder må ikke henge sammen med bokstaver: «to{tid}» er ett ord i sluttteksten.
_LIMT_I_BOKSTAV = re.compile(r"(?<=[^\W\d_])\{|\}(?=[^\W\d_])")


def _uten_usynlige(tekst: str) -> str:
    """Fjerner tegn i Unicode-kategori Cf (nullbredde, myk bindestrek), som deler ord."""
    return "".join(t for t in tekst if unicodedata.category(t) != "Cf")


def _ord(tekst: str) -> list[str]:
    return [o.casefold() for o in _ORD.findall(tekst)]


def _har_tallord(ord_: list[str]) -> bool:
    for i, o in enumerate(ord_):
        if o in TALLORD:
            return True
        if o in TALLORD_FOR_ENHET and i + 1 < len(ord_) and ord_[i + 1] in ENHETER:
            return True
    return False


def valider_begrunnelse(
    tekst: str, sok: Sok, tur: Tur, status: Status, tillegg: Iterable[str] = ()
) -> Valideringsresultat:  # FR-12, FR-13
    """Sjekker KI-teksten og setter inn verdiene. Ingen database, nett eller klokke.

    Rekkefølge: NFC, tom, plassholdere, siffer, tallord, nivåord, turtype, innsetting,
    tillegg, lengde. `tillegg` er setningene systemet lager (personalisering, preferanse);
    de legges til etter KI-teksten og sjekkes ikke for tall og nivåord, men teller i lengden.
    """
    tekst = _uten_usynlige(unicodedata.normalize("NFC", tekst))
    if not tekst.strip():
        return Valideringsresultat(forkastelse=Forkastelse.TOM)

    brukte = set(_PLASSHOLDER.findall(tekst))
    uten = _PLASSHOLDER.sub(" ", tekst)
    if (
        _LIMT_I_BOKSTAV.search(tekst)
        or "{" in uten
        or "}" in uten
        or PAAKREVD_PLASSHOLDER not in brukte
    ):
        return Valideringsresultat(forkastelse=Forkastelse.UGYLDIG)

    if any(tegn.isnumeric() for tegn in uten):
        return Valideringsresultat(forkastelse=Forkastelse.SIFFER)

    ord_ = _ord(uten)
    if _har_tallord(ord_):
        return Valideringsresultat(forkastelse=Forkastelse.TALLORD)
    if any(o in NIVAORD for o in ord_):
        return Valideringsresultat(forkastelse=Forkastelse.NIVAORD)

    if sok.turtype is not None:
        stamme = (
            ERSTATNING_FOR_TOPPTUR
            if status == Status.TOPPTUR_ERSTATTET and sok.turtype == TOPPTUR
            else TURTYPE_STAMME[sok.turtype]
        )
        if not any(stamme in o for o in ord_):
            return Valideringsresultat(forkastelse=Forkastelse.TURTYPE)

    verdier = {
        "tid": formater_tid(tur.estimert_tid_min),
        "varighet": formater_varighet_timer(sok.varighet_min),
        "lengde": formater_lengde(total_lengde_m(tur.form, tur.lengde_m)),
        "nivå": nivaord(tur.turniva),
    }
    ferdig = _PLASSHOLDER.sub(lambda m: verdier[m.group(1)], tekst)
    deler = [ferdig, *(unicodedata.normalize("NFC", t) for t in tillegg if t.strip())]
    ferdig = " ".join(" ".join(deler).split())
    if len(ferdig) > MAKS_TEGN:
        return Valideringsresultat(forkastelse=Forkastelse.FOR_LANG)
    return Valideringsresultat(tekst=ferdig)
