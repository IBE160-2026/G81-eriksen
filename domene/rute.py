"""Rutenettverk, korteste sti, omsampling og høydemeter for byggeskriptet (AD-3 punkt 2, AR-2).

Ett rutenummer i Turrutebasen er et nettverk av delte, usorterte segmenter med
forgreininger. Segmentene blir kanter i en graf der endepunktene innenfor 1 m er samme
node. Rutepunktene i kurateringslista festes til nærmeste node (høyst 50 m unna), og
stien er den korteste veien gjennom nettverket mellom hvert par av punkter.

Høydene hentes langs stien hvert 25 m. Støyfilteret teller bare endringer på minst 5 m
(hysterese), og resten på slutten telles med. Tallene og begrunnelsen står i
`data/README.md` og i spiken før story 1.5.

Alle punkter er (lon, lat) i WGS84, som i GeoJSON.
"""

import heapq
import math
from collections.abc import Sequence
from dataclasses import dataclass

from domene.tur import avstand_m

Punkt = tuple[float, float]

NODETOLERANSE_M = 1.0
MAKS_FESTEAVSTAND_M = 50.0
PUNKTAVSTAND_M = 25.0
STOYTERSKEL_M = 5.0
# Interpolerte punkter rundes til 6 desimaler (ca. 0,1 m), som koordinatene i Turrutebasen.
KOORDINATDESIMALER = 6
# Ligger siste omsamplede punkt nærmere slutten enn dette, brukes slutten i stedet.
MIN_REST_M = 0.5


class RuteFeil(Exception):  # AD-3
    """Felles grunnklasse for feil når stien bygges."""


class TomtNettverk(RuteFeil):  # AD-3
    """Ingen segmenter å bygge nettverket av."""


class PunktForLangtUnna(RuteFeil):  # AD-3
    """Et rutepunkt ligger lenger unna nærmeste node enn tillatt."""

    def __init__(self, punkt: Punkt, avstand_m: float, maks_m: float):
        self.punkt = punkt
        self.avstand_m = avstand_m
        self.maks_m = maks_m
        super().__init__(
            f"Punktet {punkt} ligger {avstand_m:.0f} m fra nærmeste node (maks {maks_m:.0f} m)."
        )


class IngenSti(RuteFeil):  # AD-3
    """Det finnes ingen sti gjennom nettverket mellom to rutepunkter."""

    def __init__(self, fra: Punkt, til: Punkt):
        self.fra = fra
        self.til = til
        super().__init__(f"Ingen sti mellom {fra} og {til}.")


class PunkterPaSammeNode(RuteFeil):  # AD-3
    """To rutepunkter etter hverandre festes til samme node, så det ene ville forsvunnet."""

    def __init__(self, fra: Punkt, til: Punkt):
        self.fra = fra
        self.til = til
        super().__init__(f"Rutepunktene {fra} og {til} festes til samme node.")


@dataclass(frozen=True)
class Kant:  # AD-3
    """Ett segment mellom to noder, med punktene i retning `fra` → `til`."""

    fra: int
    til: int
    punkter: tuple[Punkt, ...]
    lengde_m: float


@dataclass(frozen=True)
class Nettverk:  # AD-3
    noder: tuple[Punkt, ...]
    kanter: tuple[Kant, ...]


def linjelengde_m(punkter: Sequence[Punkt]) -> float:  # AD-3, AR-3
    """Summen av haversine-avstandene langs linja."""
    return sum(avstand_m(a, b) for a, b in zip(punkter, punkter[1:], strict=False))


def hele_meter(verdi: float) -> int:  # AD-3
    """Avrunder halv opp til hele meter (ikke `round()`, som runder til partall)."""
    return math.floor(verdi + 0.5)


def _desimeter(hoyde_m: float) -> int:
    return math.floor(hoyde_m * 10 + 0.5)


def lag_nettverk(  # AD-3
    segmenter: Sequence[Sequence[Punkt]], toleranse_m: float = NODETOLERANSE_M
) -> Nettverk:
    """Lager nettverket. Endepunkter innenfor `toleranse_m` blir samme node.

    Like segmenter (også snudde) tas med én gang, og segmentene sorteres, så nodene og
    kantene får samme rekkefølge uansett hvilken rekkefølge kilden gir dem i.
    """
    unike: set[tuple[Punkt, ...]] = set()
    for segment in segmenter:
        punkter = tuple((float(p[0]), float(p[1])) for p in segment)
        if len(punkter) < 2:
            continue
        unike.add(min(punkter, punkter[::-1]))
    if not unike:
        raise TomtNettverk("Ingen segmenter å bygge nettverket av.")

    noder: list[Punkt] = []

    def node_for(punkt: Punkt) -> int:
        for indeks, node in enumerate(noder):
            if avstand_m(node, punkt) <= toleranse_m:
                return indeks
        noder.append(punkt)
        return len(noder) - 1

    kanter = []
    for punkter in sorted(unike):
        fra, til = node_for(punkter[0]), node_for(punkter[-1])
        kanter.append(Kant(fra, til, punkter, linjelengde_m(punkter)))
    return Nettverk(tuple(noder), tuple(kanter))


def fest_punkt(  # AD-3
    nettverk: Nettverk, punkt: Punkt, maks_m: float = MAKS_FESTEAVSTAND_M
) -> int:
    """Gir indeksen til nærmeste node. Ligger den lenger unna enn `maks_m`, kommer
    `PunktForLangtUnna`."""
    beste, beste_avstand = min(
        ((indeks, avstand_m(node, punkt)) for indeks, node in enumerate(nettverk.noder)),
        key=lambda par: (par[1], par[0]),
    )
    if beste_avstand > maks_m:
        raise PunktForLangtUnna(punkt, beste_avstand, maks_m)
    return beste


def _korteste_kanter(nettverk: Nettverk, start: int, slutt: int) -> list[tuple[int, bool]]:
    """Dijkstra. Gir kantene langs stien som (kantindeks, forlengs)."""
    naboer: list[list[tuple[int, int, bool]]] = [[] for _ in nettverk.noder]
    for indeks, kant in enumerate(nettverk.kanter):
        if kant.fra == kant.til:
            continue
        naboer[kant.fra].append((kant.til, indeks, True))
        naboer[kant.til].append((kant.fra, indeks, False))

    avstand = {start: 0.0}
    forrige: dict[int, tuple[int, int, bool]] = {}
    ko = [(0.0, start)]
    ferdig: set[int] = set()
    while ko:
        d, node = heapq.heappop(ko)
        if node in ferdig:
            continue
        ferdig.add(node)
        if node == slutt:
            break
        for nabo, kantindeks, forlengs in naboer[node]:
            ny = d + nettverk.kanter[kantindeks].lengde_m
            if ny < avstand.get(nabo, math.inf):
                avstand[nabo] = ny
                forrige[nabo] = (node, kantindeks, forlengs)
                heapq.heappush(ko, (ny, nabo))
    if slutt not in ferdig:
        raise IngenSti(nettverk.noder[start], nettverk.noder[slutt])

    sti = []
    node = slutt
    while node != start:
        node, kantindeks, forlengs = forrige[node]
        sti.append((kantindeks, forlengs))
    return sti[::-1]


def sti_gjennom(  # AD-3
    nettverk: Nettverk, rutepunkter: Sequence[Punkt], maks_m: float = MAKS_FESTEAVSTAND_M
) -> tuple[Punkt, ...]:
    """Korteste sti gjennom rutepunktene i rekkefølge, som én sammenføyd linje.

    Segmentene snus ved behov. Ved rundtur er siste rutepunkt lik det første. Festes to
    rutepunkter etter hverandre til samme node, kommer `PunkterPaSammeNode`.
    """
    if len(rutepunkter) < 2:
        raise RuteFeil("Stien trenger minst to rutepunkter.")
    noder = [fest_punkt(nettverk, punkt, maks_m) for punkt in rutepunkter]
    linje: list[Punkt] = []
    for i, (fra, til) in enumerate(zip(noder, noder[1:], strict=False)):
        if fra == til:
            raise PunkterPaSammeNode(rutepunkter[i], rutepunkter[i + 1])
        for kantindeks, forlengs in _korteste_kanter(nettverk, fra, til):
            punkter = nettverk.kanter[kantindeks].punkter
            punkter = punkter if forlengs else punkter[::-1]
            # Første punkt er noden stien allerede står i. Punkter som gjentas rett
            # etter hverandre (det finnes i kilden), tas med én gang.
            for punkt in punkter if not linje else punkter[1:]:
                if not linje or punkt != linje[-1]:
                    linje.append(punkt)
    return tuple(linje)


def omsampl(  # AD-3
    punkter: Sequence[Punkt], steg_m: float = PUNKTAVSTAND_M
) -> tuple[tuple[float, Punkt], ...]:
    """Punkter hvert `steg_m` langs linja, med avstanden fra start.

    Første og siste punkt er alltid med. Avstanden til siste punkt er linjas lengde.
    """
    ut: list[tuple[float, Punkt]] = [(0.0, (punkter[0][0], punkter[0][1]))]
    akkumulert = 0.0
    k = 1
    for a, b in zip(punkter, punkter[1:], strict=False):
        d = avstand_m(a, b)
        if d == 0:
            continue
        while k * steg_m <= akkumulert + d:
            andel = (k * steg_m - akkumulert) / d
            punkt = (
                round(a[0] + (b[0] - a[0]) * andel, KOORDINATDESIMALER),
                round(a[1] + (b[1] - a[1]) * andel, KOORDINATDESIMALER),
            )
            ut.append((k * steg_m, punkt))
            k += 1
        akkumulert += d
    slutt = (akkumulert, (punkter[-1][0], punkter[-1][1]))
    if len(ut) > 1 and akkumulert - ut[-1][0] < MIN_REST_M:
        ut[-1] = slutt  # Et punkt helt inntil slutten erstattes av slutten selv.
    else:
        ut.append(slutt)
    return tuple(ut)


def hoydemeter_og_nedstigning(  # AD-3, FR-3
    hoyder: Sequence[float], terskel: float = STOYTERSKEL_M
) -> tuple[int, int]:
    """Stigning og nedstigning i hele meter, med støyfilter (hysterese).

    Starter med `ref = hoyder[0]`. Når en høyde avviker minst `terskel` fra `ref`, telles
    differansen opp eller ned, og `ref` flyttes dit. Til slutt telles resten
    `hoyder[-1] - ref`. Regnes i hele desimeter, så summen ikke får flyttallsfeil.
    """
    if not hoyder:
        return 0, 0
    dm = [_desimeter(h) for h in hoyder]
    terskel_dm = _desimeter(terskel)
    opp = ned = 0
    ref = dm[0]
    for z in dm[1:]:
        if abs(z - ref) >= terskel_dm:
            if z > ref:
                opp += z - ref
            else:
                ned += ref - z
            ref = z
    rest = dm[-1] - ref
    if rest > 0:
        opp += rest
    elif rest < 0:
        ned -= rest
    return (opp + 5) // 10, (ned + 5) // 10


def hoydeprofil(  # AD-3
    avstander_m: Sequence[float], hoyder: Sequence[float]
) -> tuple[tuple[int, float], ...]:
    """Profilen som (avstand i hele meter, høyde med 1 desimal) for de omsamplede punktene."""
    return tuple(
        (hele_meter(avstand), _desimeter(hoyde) / 10)
        for avstand, hoyde in zip(avstander_m, hoyder, strict=True)
    )
