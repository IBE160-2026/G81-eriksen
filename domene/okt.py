"""Søketilstanden som lagres i økten (AD-5, FR-7).

Tilstanden har søket, statusen og den frosne rangeringen fra `velg_turer`, så en ny
innlasting gir samme tur uten å rangere på nytt. `til_dict` og `fra_dict` gir en verdi som
kan lagres som JSON, med datoen som ISO-streng. `fra_dict` tåler at felt som kommer
senere (KI-begrunnelsen i Epic 4), mangler, og at ukjente felt finnes.
"""

from dataclasses import dataclass
from datetime import date
from typing import Any

from domene.sok import Sok
from domene.utvalg import Status, Utvalg


@dataclass(frozen=True)
class Soketilstand:  # AD-5, FR-7
    """Ett søk i økten. `gjeldende_tur_id` er `None` når ingen tur vises."""

    sok: Sok
    status: Status
    rangerte_tur_ider: tuple[str, ...]
    viste_tur_ider: tuple[str, ...] = ()
    gjeldende_tur_id: str | None = None
    nivaheving: bool = False

    def til_dict(self) -> dict[str, Any]:  # AD-5
        return {
            "sok": {
                "varighet_min": self.sok.varighet_min,
                "dato": self.sok.dato.isoformat(),
                "turtype": self.sok.turtype,
                "startpunkt_id": self.sok.startpunkt_id,
            },
            "status": self.status.value,
            "rangerte_tur_ider": list(self.rangerte_tur_ider),
            "viste_tur_ider": list(self.viste_tur_ider),
            "gjeldende_tur_id": self.gjeldende_tur_id,
            "nivaheving": self.nivaheving,
        }

    @classmethod
    def fra_dict(cls, data: dict[str, Any]) -> "Soketilstand":  # AD-5
        """Gjør en lagret verdi om til tilstanden. Ugyldige verdier gir `ValueError`."""
        try:
            sok_data = data["sok"]
            sok = Sok(
                varighet_min=sok_data["varighet_min"],
                dato=date.fromisoformat(sok_data["dato"]),
                turtype=sok_data.get("turtype"),
                startpunkt_id=sok_data.get("startpunkt_id"),
            )
            gjeldende = data.get("gjeldende_tur_id")
            if gjeldende is not None and not isinstance(gjeldende, str):
                raise ValueError(f"Ugyldig gjeldende tur-ID {gjeldende!r}.")
            return cls(
                sok=sok,
                status=Status(data["status"]),
                rangerte_tur_ider=_ider(data["rangerte_tur_ider"]),
                viste_tur_ider=_ider(data.get("viste_tur_ider", [])),
                gjeldende_tur_id=gjeldende,
                nivaheving=bool(data.get("nivaheving", False)),
            )
        except (KeyError, TypeError, AttributeError) as feil:
            raise ValueError(f"Søketilstanden kan ikke leses: {feil!r}.") from feil


def _ider(verdi: Any) -> tuple[str, ...]:  # AD-5
    if not isinstance(verdi, list | tuple) or not all(isinstance(i, str) for i in verdi):
        raise ValueError(f"Forventet en liste med tur-ID-er, fikk {verdi!r}.")
    return tuple(verdi)


def ny_soketilstand(sok: Sok, utvalg: Utvalg) -> Soketilstand:  # AD-5, FR-7
    """Tilstanden rett etter et søk: første tur i rangeringen vises, om det finnes en."""
    forste = utvalg.rangerte_tur_ider[0] if utvalg.rangerte_tur_ider else None
    return Soketilstand(
        sok=sok,
        status=utvalg.status,
        rangerte_tur_ider=utvalg.rangerte_tur_ider,
        viste_tur_ider=(forste,) if forste else (),
        gjeldende_tur_id=forste,
    )
