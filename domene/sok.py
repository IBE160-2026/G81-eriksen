"""Søket som utvalget får inn: varighet, dato, turtype og startpunkt (FR-5).

Søket er frosset, så `dataclasses.replace` kan lage endrede søk (1.12). Ugyldige verdier
stoppes i `__post_init__` med `ValueError` på norsk. Fritekst kommer i Epic 4.
"""

from dataclasses import dataclass
from datetime import date, datetime

from domene.tur import TURTYPER

# Grensene for varigheten i minutter (FR-5, beslutning 5 i spec 1.8): 1–12 t i halvtimessteg.
MIN_VARIGHET_MIN = 60
MAKS_VARIGHET_MIN = 720
VARIGHET_STEG_MIN = 30

# Søket kan gjelde fra i dag til og med så mange dager frem (FR-4): 31 datoer.
DATO_DAGER_FREM = 30


@dataclass(frozen=True)
class Sok:  # FR-5
    """Ett søk. `turtype` og `startpunkt_id` er `None` når de ikke er valgt."""

    varighet_min: int
    dato: date
    turtype: str | None = None
    startpunkt_id: str | None = None

    def __post_init__(self) -> None:  # FR-5
        varighet = self.varighet_min
        if not isinstance(varighet, int) or isinstance(varighet, bool):
            raise ValueError(f"Varigheten må være et heltall i minutter, fikk {varighet!r}.")
        if not MIN_VARIGHET_MIN <= varighet <= MAKS_VARIGHET_MIN:
            raise ValueError(
                f"Varigheten må være mellom {MIN_VARIGHET_MIN} og {MAKS_VARIGHET_MIN} "
                f"minutter, fikk {varighet}."
            )
        if (varighet - MIN_VARIGHET_MIN) % VARIGHET_STEG_MIN != 0:
            raise ValueError(
                f"Varigheten må gå i steg på {VARIGHET_STEG_MIN} minutter, fikk {varighet}."
            )
        if not isinstance(self.dato, date) or isinstance(self.dato, datetime):
            raise ValueError(f"Datoen må være en dato uten klokkeslett, fikk {self.dato!r}.")
        if self.turtype is not None and self.turtype not in TURTYPER:
            raise ValueError(
                f"Ukjent turtype {self.turtype!r}. Lovlige turtyper er {', '.join(TURTYPER)}."
            )
        if self.startpunkt_id is not None and (
            not isinstance(self.startpunkt_id, str)
            or not self.startpunkt_id.strip()
            or self.startpunkt_id != self.startpunkt_id.strip()
        ):
            raise ValueError(
                f"Startpunkt-ID-en {self.startpunkt_id!r} må være en tekst som ikke er tom."
            )
