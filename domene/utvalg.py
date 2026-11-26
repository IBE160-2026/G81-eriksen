"""Utvalget: hvilke turer som passer et søk, i hvilken rekkefølge, og med hvilken status.

`velg_turer` filtrerer på tid, nivåtak, turtype og startpunkt (FR-5) og rangerer med én
sorteringsnøkkel (FR-5 punkt 5 og 6), så senere ledd (gåtte turer, nivåheving, foretrukne
turtyper) kan legges foran uten omskriving. Er topptur valgt og ingen topptur passer,
erstattes den med utsiktsturer (FR-8). Gjester og brukere uten historikk har grønt
nivåtak (FR-18). Ingen tur over nivåtaket er noen gang med (SM-C1).
Når ingen tur passer (eller alle er vist), gir `foresla_endringer` høyst tre endringsforslag
som hver gir treff (FR-8, UX-DR17).
"""

from collections.abc import Iterable
from dataclasses import dataclass, replace
from enum import StrEnum

from domene.sok import MAKS_VARIGHET_MIN, VARIGHET_STEG_MIN, Sok
from domene.tur import NIVAREKKEFOLGE, TURTYPER, Tur, Turniva

# Nivåtaket for gjester og brukere uten historikk (FR-18).
NIVATAK_UTEN_HISTORIKK = Turniva.GRONN

TOPPTUR = "topptur"
ERSTATNING_FOR_TOPPTUR = "utsikt"  # FR-8


class Status(StrEnum):  # FR-5, FR-8
    TREFF = "treff"
    TOPPTUR_ERSTATTET = "topptur_erstattet"
    BARE_OVER_NIVATAK = "bare_over_nivatak"
    INGEN_TREFF = "ingen_treff"


@dataclass(frozen=True)
class Utvalg:  # FR-5
    """Resultatet av et søk. `rangerte_tur_ider` er tom ved `BARE_OVER_NIVATAK` og
    `INGEN_TREFF`, og har utsiktsturene ved `TOPPTUR_ERSTATTET`."""

    status: Status
    rangerte_tur_ider: tuple[str, ...]


def _nivaplass(niva: Turniva) -> int:  # FR-5
    """Plassen i `NIVAREKKEFOLGE`. `Turniva` sammenlignes aldri med `<` (alfabetisk)."""
    return NIVAREKKEFOLGE.index(niva)


def _passer(tur: Tur, sok: Sok, nivatak: Turniva | None) -> bool:  # FR-5
    """Om turen passer søket. Med `nivatak=None` sjekkes ikke nivået."""
    if tur.estimert_tid_min > sok.varighet_min:
        return False
    if nivatak is not None and _nivaplass(tur.turniva) > _nivaplass(nivatak):
        return False
    if sok.turtype is not None and sok.turtype not in tur.turtyper:
        return False
    return sok.startpunkt_id is None or tur.startpunkt_id == sok.startpunkt_id


def innenfor_tid_og_nivatak(tur: Tur, sok: Sok, nivatak: Turniva) -> bool:  # FR-5, SM-C1
    """Om turen fortsatt passer varigheten og nivåtaket. Brukes før en lagret tur vises,
    fordi turdatabasen kan ha endret seg etter søket. Turtype og startpunkt sjekkes ikke,
    fordi en utsiktstur kan ha erstattet en topptur (FR-8)."""
    return tur.estimert_tid_min <= sok.varighet_min and _nivaplass(tur.turniva) <= _nivaplass(
        Turniva(nivatak)
    )


def _rangeringsnokkel(tur: Tur) -> tuple[int, str]:  # FR-5 punkt 5 og 6
    """Lengst tid først (nærmest varigheten, siden alle er ≤), så tur-ID stigende."""
    return (-tur.estimert_tid_min, str(tur.id))


def _rangerte_ider(turer: Iterable[Tur], sok: Sok, nivatak: Turniva) -> tuple[str, ...]:  # FR-5
    passende = [tur for tur in turer if _passer(tur, sok, nivatak)]
    return tuple(tur.id for tur in sorted(passende, key=_rangeringsnokkel))


def velg_turer(sok: Sok, turer: Iterable[Tur], nivatak: Turniva) -> Utvalg:  # FR-5, FR-8, FR-18
    """Velger og rangerer turene som passer søket innenfor nivåtaket.

    1. Passer noen tur innenfor taket: `TREFF`.
    2. Er topptur valgt: utsiktsturer som passer de samme filtrene innenfor taket gir
       `TOPPTUR_ERSTATTET`, også når en topptur over taket passer (beslutning 1 og 2).
    3. Passer turer alle de andre filtrene i søket, men bare over taket:
       `BARE_OVER_NIVATAK`, uten turer. Utsiktsturer over taket teller ikke ved topptur
       (beslutning 3).
    4. Ellers `INGEN_TREFF`.
    """
    turer = tuple(turer)
    nivatak = Turniva(nivatak)

    treff = _rangerte_ider(turer, sok, nivatak)
    if treff:
        return Utvalg(Status.TREFF, treff)

    if sok.turtype == TOPPTUR:  # FR-8
        utsikt = _rangerte_ider(turer, replace(sok, turtype=ERSTATNING_FOR_TOPPTUR), nivatak)
        if utsikt:
            return Utvalg(Status.TOPPTUR_ERSTATTET, utsikt)

    if any(_passer(tur, sok, None) for tur in turer):
        return Utvalg(Status.BARE_OVER_NIVATAK, ())
    return Utvalg(Status.INGEN_TREFF, ())


# Feltene et endringsforslag kan gjelde, i fast rekkefølge (FR-8).
FELT_VARIGHET = "varighet"
FELT_STARTPUNKT = "startpunkt"
FELT_TURTYPE = "turtype"


@dataclass(frozen=True)
class Endringsforslag:  # FR-8, UX-DR17
    """Ett forslag til endring av søket. `verdi` er den nye verdien som tekst: minutter for
    varighet, turtypen for turtype (tom betyr «alle turtyper»). «Velg startpunkt» har tom
    verdi og er en lenke til skjemaet, ikke en endring som kjøres direkte."""

    felt: str
    verdi: str
    etikett: str

    @property
    def er_lenke(self) -> bool:
        return self.felt == FELT_STARTPUNKT


def _gir_treff(
    sok: Sok, turer: tuple[Tur, ...], nivatak: Turniva, tidligere_treff: frozenset[str]
) -> bool:  # FR-8
    """Om søket gir `TREFF`, og (ved «alle vist») minst én tur utenom `tidligere_treff`."""
    utvalg = velg_turer(sok, turer, nivatak)
    if utvalg.status != Status.TREFF:
        return False
    return any(tur_id not in tidligere_treff for tur_id in utvalg.rangerte_tur_ider)


def foresla_endringer(
    sok: Sok,
    turer: Iterable[Tur],
    nivatak: Turniva,
    tidligere_treff: Iterable[str] = (),
) -> tuple[Endringsforslag, ...]:  # FR-8, UX-DR17, UX-DR22
    """Høyst tre endringer av søket i fast rekkefølge, med de andre valgene uendret.

    1. Varighet: korteste lengre varighet i halvtimessteg som gir treff (ikke ved 12 t).
    2. Startpunkt: bare når et startpunkt er valgt og et annet (eller «alle») gir treff.
    3. Turtype: bare når en turtype er valgt: første av marka, utsikt, topptur som gir treff,
       ellers «alle turtyper».

    Et forslag tas bare med når det endrede søket gir `TREFF`, og ved «alle vist» også minst
    én tur som ikke står i `tidligere_treff`. `velg_turer` er uendret.
    """
    from domene.tekst import formater_turtype, formater_varighet_timer

    turer = tuple(turer)
    nivatak = Turniva(nivatak)
    tidligere = frozenset(tidligere_treff)

    def gir_treff(endret: Sok) -> bool:
        return _gir_treff(endret, turer, nivatak, tidligere)

    forslag: list[Endringsforslag] = []

    for minutter in range(
        sok.varighet_min + VARIGHET_STEG_MIN, MAKS_VARIGHET_MIN + 1, VARIGHET_STEG_MIN
    ):
        if gir_treff(replace(sok, varighet_min=minutter)):
            etikett = f"Prøv {formater_varighet_timer(minutter)}"
            forslag.append(Endringsforslag(FELT_VARIGHET, str(minutter), etikett))
            break

    if sok.startpunkt_id is not None:
        startpunkter = {tur.startpunkt_id for tur in turer} - {sok.startpunkt_id}
        kandidater = [None, *sorted(startpunkter)]
        if any(gir_treff(replace(sok, startpunkt_id=kandidat)) for kandidat in kandidater):
            forslag.append(Endringsforslag(FELT_STARTPUNKT, "", "Velg startpunkt"))

    if sok.turtype is not None:
        for turtype in (t for t in TURTYPER if t != sok.turtype):
            if gir_treff(replace(sok, turtype=turtype)):
                etikett = f"Prøv {formater_turtype(turtype).lower()}"
                forslag.append(Endringsforslag(FELT_TURTYPE, turtype, etikett))
                break
        else:
            if gir_treff(replace(sok, turtype=None)):
                forslag.append(Endringsforslag(FELT_TURTYPE, "", "Prøv alle turtyper"))

    return tuple(forslag)
