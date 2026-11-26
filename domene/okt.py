"""Søketilstanden som lagres i økten (AD-5, FR-7).

Tilstanden har søket, statusen og den frosne rangeringen fra `velg_turer`, så en ny
innlasting gir samme tur uten å rangere på nytt. `til_dict` og `fra_dict` gir en verdi som
kan lagres som JSON, med datoen som ISO-streng. `fra_dict` tåler at felt som kommer senere
(KI-begrunnelsen i Epic 4), mangler, og at ukjente felt finnes. «Nytt forslag» og «Start fra
første forslag igjen» (1.11) er rene funksjoner som gir en ny tilstand uten ny rangering.
"""

from collections.abc import Callable
from dataclasses import dataclass, replace
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


def alle_vist(tilstand: Soketilstand) -> bool:  # FR-7
    """«Alle vist»: søket hadde treff, ingen tur vises, og alle turene i rangeringen er vist.

    Det er ikke det samme som en ukjent søke-ID eller en tilstand uten treff.
    """
    return (
        tilstand.gjeldende_tur_id is None
        and tilstand.status in (Status.TREFF, Status.TOPPTUR_ERSTATTET)
        and bool(tilstand.rangerte_tur_ider)
        and set(tilstand.rangerte_tur_ider) <= set(tilstand.viste_tur_ider)
    )


def neste_forslag(
    tilstand: Soketilstand, fra_tur_id: str | None, gyldig: Callable[[str], bool]
) -> Soketilstand:  # FR-7, NFR-2
    """«Nytt forslag»: neste tur i den frosne rangeringen som ikke er vist.

    Går bare videre når `fra_tur_id` er gjeldende tur, så et dobbeltklikk eller en gammel
    POST gir samme tilstand tilbake. En tur der `gyldig` gir `False` (slettet, eller ikke
    lenger innenfor tid og nivåtak), hoppes over og markeres som vist. Er det ingen igjen,
    blir `gjeldende_tur_id` `None` («alle vist»).
    """
    if tilstand.gjeldende_tur_id is None or fra_tur_id != tilstand.gjeldende_tur_id:
        return tilstand
    viste = list(tilstand.viste_tur_ider)
    if tilstand.gjeldende_tur_id not in viste:
        viste.append(tilstand.gjeldende_tur_id)
    for tur_id in tilstand.rangerte_tur_ider:
        if tur_id in viste:
            continue
        viste.append(tur_id)
        if gyldig(tur_id):
            return replace(tilstand, viste_tur_ider=tuple(viste), gjeldende_tur_id=tur_id)
    return replace(tilstand, viste_tur_ider=tuple(viste), gjeldende_tur_id=None)


def start_pa_nytt(tilstand: Soketilstand) -> Soketilstand:  # FR-7
    """«Start fra første forslag igjen»: første tur vises, og listen over viste starter på nytt.

    Gjelder bare ved «alle vist». Ellers (for eksempel et dobbeltklikk) gis samme tilstand.
    """
    if not alle_vist(tilstand):
        return tilstand
    forste = tilstand.rangerte_tur_ider[0]
    return replace(tilstand, viste_tur_ider=(forste,), gjeldende_tur_id=forste)
