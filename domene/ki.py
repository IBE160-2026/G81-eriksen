"""Dataene som kan sendes til KI, og svaret derfra (NFR-5, AD-10).

Bare søket og de filtrerte turene går til KI. Aldri e-post, bruker-ID, historikk, nivåtak eller
fritekst. Dataklassene har bare feltene under, og en test sjekker at ingen kommer til.
"""

from dataclasses import dataclass
from datetime import date

ARSAK_TIDSAVBRUDD = "tidsavbrudd"
ARSAK_FEIL = "feil"
ARSAK_UGYLDIG = "ugyldig"
KI_FEILARSAKER = (ARSAK_TIDSAVBRUDD, ARSAK_FEIL, ARSAK_UGYLDIG)


@dataclass(frozen=True)
class KiSok:  # NFR-5
    varighet_min: int
    dato: date
    turtype: str | None
    startpunkt_id: str | None


@dataclass(frozen=True)
class KiTur:  # NFR-5
    id: str
    navn: str
    turtyper: tuple[str, ...]
    form: str


@dataclass(frozen=True)
class KiSvar:  # AD-10
    """Svaret fra KI-tjenesten. Ved feil er `arsak` en av `KI_FEILARSAKER`, ellers `None`."""

    tekst: str = ""
    arsak: str | None = None

    @property
    def ok(self) -> bool:
        return self.arsak is None
