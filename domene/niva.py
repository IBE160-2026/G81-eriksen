"""Nivåtak, grunnnivå og sperre utledet fra vurderingene til brukeren (FR-18, FR-19, AD-11, AR-13).

Statusen lagres aldri. Den regnes alltid ut fra hele historikken, så en registrering med
tidligere dato kan endre nivåtaket. Nivåer sammenlignes med posisjonen i `NIVAREKKEFOLGE`.
"""

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date

from domene.tur import NIVAREKKEFOLGE, Turniva

VANSKELIGHETER = ("lett", "moderat", "vanskelig")
MIN_FORNOYDHET = 1
MAKS_FORNOYDHET = 5
TURER_PER_HEVING = 3


@dataclass(frozen=True)
class Registrering:  # FR-16
    id: int
    dato: date
    tur_id: str
    turniva: Turniva
    vanskelighet: str
    fornoydhet: int


@dataclass(frozen=True)
class Sperre:  # FR-19
    niva: Turniva  # sperrenivået
    turniva: Turniva  # turnivået som ga sperren


@dataclass(frozen=True)
class NivaStatus:  # FR-18, FR-19
    nivatak: Turniva
    grunnniva: Turniva
    sperre: Sperre | None
    antall_hevinger: int
    teller: int


def _pos(niva: Turniva) -> int:
    return NIVAREKKEFOLGE.index(niva)


def _valider(registrering: Registrering) -> None:
    if registrering.turniva not in NIVAREKKEFOLGE:
        raise ValueError(f"Ukjent turnivå: {registrering.turniva!r}.")
    if registrering.vanskelighet not in VANSKELIGHETER:
        raise ValueError(f"Ukjent vanskelighet: {registrering.vanskelighet!r}.")
    f = registrering.fornoydhet
    if isinstance(f, bool) or not isinstance(f, int) or not MIN_FORNOYDHET <= f <= MAKS_FORNOYDHET:
        raise ValueError(
            f"Fornøydhet må være et helt tall fra {MIN_FORNOYDHET} til {MAKS_FORNOYDHET}: {f!r}."
        )


def vurder_historikk(registreringer: Iterable[Registrering]) -> NivaStatus:
    """Regner ut nivåstatus fra registreringene, sortert på (dato, id) (FR-19)."""
    alle = list(registreringer)
    for registrering in alle:
        _valider(registrering)

    grunnniva = NIVAREKKEFOLGE[0]
    sperre: Sperre | None = None
    hevinger = 0
    teller = 0

    for r in sorted(alle, key=lambda r: (r.dato, r.id)):
        if r.vanskelighet == "vanskelig":
            teller = 0
            kandidat = NIVAREKKEFOLGE[max(_pos(r.turniva) - 1, 0)]
            nivatak = sperre.niva if sperre else grunnniva
            if _pos(kandidat) < _pos(nivatak):
                sperre = Sperre(kandidat, r.turniva)
        elif sperre is not None:
            sperre = None
        elif (
            r.vanskelighet == "lett" and r.turniva == grunnniva and grunnniva != NIVAREKKEFOLGE[-1]
        ):
            teller += 1
            if teller == TURER_PER_HEVING:
                grunnniva = NIVAREKKEFOLGE[_pos(grunnniva) + 1]
                hevinger += 1
                teller = 0

    return NivaStatus(
        nivatak=sperre.niva if sperre else grunnniva,
        grunnniva=grunnniva,
        sperre=sperre,
        antall_hevinger=hevinger,
        teller=teller,
    )


def nivaheving(status: NivaStatus, brukt_heving: int) -> bool:  # FR-19, AD-11
    """Om dette søket er det første etter en ny heving: flere hevinger enn de som er brukt,
    og ingen aktiv sperre. Med sperre regnes hevingen som brukt, uten å gi `True`."""
    return status.sperre is None and status.antall_hevinger > brukt_heving
