"""Måler kartlag-fargene mot Kartverkets topo-fliser (story 6.5, UX-DR35, NFR-4, NFR-7, UX-DR1).

Kjøres med `python -m skript.mal_kartfarger` og krever nett. Skriptet

1. henter flisene for hvert målested på zoom 13 og 15 fra AR-10-adressen til en midlertidig
   mappe (adressen har raden før kolonnen, `{z}/{y}/{x}`, men tabellene oppgir `z/x/y`);
2. leser pikslene med en PNG-leser som bare bruker standardbiblioteket;
3. finner flaten på hver flis og oppgir den vanligste fargen (typisk) og den mørkeste
   skyggevarianten (1. persentil av relativ luminans);
4. regner WCAG-kontrasten mellom kartlag-tokenene i `tokens.css` og hver flate, og skriver
   tabellene som markdown til standard ut (grunnlaget for `docs/kartfarger.md`).

**Slik finnes flaten.** Topo-flisene skyggelegger terrenget ved å trekke omtrent like mye fra
alle tre kanalene. Fargetonen, målt som `(g − r, r − b)`, er derfor den samme i lys og skygge.
En piksel hører til en flate når tonen er innenfor ±1 av flatens grunnfarge (den lyseste,
uskyggede fargen), og den er høyst `MAKS_SKYGGE` mørkere. Symboler (stier, veier, bygninger,
tekst og koter) har andre toner og telles ikke. Hvitt har samme tone som grå og svart tekst,
så for myr telles bare piksler der alle fire naboene også er hvit flate, og der ingen kanal
skiller seg mer enn `MAKS_NABOSPRANG` fra naboen. Det tar bort kantene rundt tekst og streker.

Skriptet importerer bare standardbiblioteket og endrer ingen filer i repoet.
"""

import logging
import math
import re
import struct
import sys
import tempfile
import urllib.request
import zlib
from collections import Counter
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)

ROT = Path(__file__).resolve().parents[1]
TOKENS_CSS = ROT / "turforslag" / "static" / "css" / "tokens.css"

# AR-10. Samme adresse som `kart.js`: raden (y) står før kolonnen (x).
FLIS_URL = "https://cache.kartverket.no/v1/wmts/1.0.0/topo/default/webmercator/{z}/{y}/{x}.png"
USER_AGENT = "YourNextAdventure/0.1 https://github.com/IBE160-2026/G81-eriksen"
TIDSAVBRUDD_S = 30

# `fitBounds` gir turene zoom 11–16; 13 og 15 dekker spennet (spec 6.5, Design Notes).
ZOOMNIVAER = (13, 15)
PERSENTIL = 0.01
MAKS_SKYGGE = 96  # Kraftigste skygge på skog i flisene er 77 (#DFEDA3 → #92A056).
MAKS_NABOSPRANG = 4
KRAV = 3.0  # WCAG 1.4.11, komponenter som ikke er tekst.
KRAV_TEKST = 4.5  # «S» i startmarkøren er tekst.

PNG_SIGNATUR = b"\x89PNG\r\n\x1a\n"

RGB = tuple[int, int, int]


@dataclass(frozen=True)
class Flate:
    navn: str
    grunnfarge: str  # Den lyseste, uskyggede fargen i flisene.
    glatt: bool = False  # Krev at naboene er samme flate (hvitt deler tone med tekst).


@dataclass(frozen=True)
class Malested:
    sted: str
    flatetype: str
    lat: float
    lon: float


@dataclass(frozen=True)
class Maling:
    flis: str  # z/x/y
    sted: str
    flate: str
    typisk: RGB
    morkest: RGB
    antall: int  # Piksler av flaten på flisen (av 256 × 256).


FLATER: dict[str, tuple[Flate, ...]] = {
    "skog": (Flate("skog", "#DFEDA3"),),
    "myr": (Flate("myr (hvit flate)", "#FEFEFE", glatt=True),),
    "vann": (Flate("vann", "#E0FEFE"),),
    "bebyggelse": (Flate("boligfelt", "#FBE4D0"), Flate("bebygd (grå)", "#FEFEED")),
}

MALESTEDER = (
    Malested("Sognsvann", "vann", 59.9725, 10.730),
    Malested("Nøklevann", "vann", 59.885, 10.870),
    Malested("Nordmarka", "skog", 60.010, 10.690),
    Malested("Østmarka", "skog", 59.893, 10.895),
    Malested("ved Fuglemyrhytta", "myr", 59.985, 10.697),
    Malested("Lillomarka", "myr", 59.985, 10.850),
    Malested("Grorud", "bebyggelse", 59.9614, 10.882),
    Malested("Gjettum", "bebyggelse", 59.9105, 10.5277),
)

# Linjer og symboler i flisene som ruten ikke skal forveksles med (DESIGN.md › Kartlag).
# Fargene er lest ut av de samme flisene; de er ikke flater og vurderes også i skjermbildene.
SYMBOLER = (
    ("sti og vei, rød", "#D2232A"),
    ("vei, oransje", "#D68723"),
    ("vei, gul", "#FAEB00"),
    ("kote, brun", "#D8A97D"),
    ("bekk og myrskravur, blå", "#9ACBE7"),
    ("vannskrift, blå", "#005CE6"),
    ("bygning, blå", "#5A87DE"),
    ("løype, grønn", "#00CC00"),
)

KARTLAG_TOKENER = ("map-route", "map-marker-start", "map-focus-ring", "map-overlay-surface")


# --- Farger og kontrast (WCAG 2.1) ------------------------------------------------------


def hex_til_rgb(verdi: str) -> RGB:
    """`#6A3D9A` eller `#6a3d9a` → (106, 61, 154)."""
    if not re.fullmatch(r"#[0-9A-Fa-f]{6}", verdi):
        raise ValueError(f"Ikke en sekssifret hex-farge: {verdi!r}")
    return (int(verdi[1:3], 16), int(verdi[3:5], 16), int(verdi[5:7], 16))


def rgb_til_hex(rgb: RGB) -> str:
    return "#{:02X}{:02X}{:02X}".format(*rgb)


def luminans(rgb: RGB) -> float:
    """Relativ luminans etter WCAG 2.1."""

    def kanal(verdi: int) -> float:
        v = verdi / 255
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4

    r, g, b = (kanal(v) for v in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def kontrast(a: RGB, b: RGB) -> float:
    """Kontrastforholdet etter WCAG 2.1, fra 1 til 21."""
    lys, mork = sorted((luminans(a), luminans(b)), reverse=True)
    return (lys + 0.05) / (mork + 0.05)


def fargetone(rgb: RGB) -> int:
    """Fargetonen i grader (HSV), avrundet."""
    r, g, b = (v / 255 for v in rgb)
    storst, minst = max(r, g, b), min(r, g, b)
    if storst == minst:
        return 0
    d = storst - minst
    if storst == r:
        h = ((g - b) / d) % 6
    elif storst == g:
        h = (b - r) / d + 2
    else:
        h = (r - g) / d + 4
    return round(h * 60) % 360


def les_tokens(css: str, navn: Iterable[str] = KARTLAG_TOKENER) -> dict[str, RGB]:
    """Leser `--navn: #rrggbb;` fra token-fila (UX-DR1: fargene står bare der)."""
    tokener = {}
    for token in navn:
        treff = re.search(rf"--{re.escape(token)}:\s*(#[0-9A-Fa-f]{{6}})\s*;", css)
        if not treff:
            raise ValueError(f"Fant ikke --{token} i tokens.css.")
        tokener[token] = hex_til_rgb(treff.group(1))
    return tokener


# --- PNG ---------------------------------------------------------------------------------


@dataclass(frozen=True)
class Bilde:
    bredde: int
    hoyde: int
    piksler: list[tuple[int, int, int, int]]  # RGBA, rad for rad

    def piksel(self, x: int, y: int) -> tuple[int, int, int, int]:
        return self.piksler[y * self.bredde + x]


def _paeth(a: int, b: int, c: int) -> int:
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    return b if pb <= pc else c


def les_png(data: bytes) -> Bilde:
    """Leser en PNG med 8 bit per kanal uten interlacing (gråtone, RGB, palett, med og uten
    alfa). Det dekker Kartverkets fliser (RGBA) og holder skriptet uten nye pakker."""
    if data[:8] != PNG_SIGNATUR:
        raise ValueError("Ikke en PNG-fil.")
    pos, idat, palett, gjennomsiktig = 8, bytearray(), b"", b""
    hode = None
    while pos < len(data):
        (lengde,) = struct.unpack(">I", data[pos : pos + 4])
        typ = data[pos + 4 : pos + 8]
        innhold = data[pos + 8 : pos + 8 + lengde]
        if typ == b"IHDR":
            hode = struct.unpack(">IIBBBBB", innhold)
        elif typ == b"PLTE":
            palett = innhold
        elif typ == b"tRNS":
            gjennomsiktig = innhold
        elif typ == b"IDAT":
            idat += innhold
        elif typ == b"IEND":
            break
        pos += 12 + lengde
    if hode is None:
        raise ValueError("PNG-fila mangler IHDR.")
    bredde, hoyde, dybde, fargetype, _, _, interlace = hode
    kanaler = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}.get(fargetype)
    if dybde != 8 or interlace != 0 or kanaler is None:
        raise ValueError(
            f"Støtter ikke PNG med dybde {dybde}, fargetype {fargetype}, interlace {interlace}."
        )

    raa = zlib.decompress(bytes(idat))
    stride = bredde * kanaler
    forrige = bytearray(stride)
    piksler = []
    i = 0
    for _ in range(hoyde):
        filter_ = raa[i]
        rad = bytearray(raa[i + 1 : i + 1 + stride])
        i += 1 + stride
        for x in range(stride):
            venstre = rad[x - kanaler] if x >= kanaler else 0
            over = forrige[x]
            over_venstre = forrige[x - kanaler] if x >= kanaler else 0
            if filter_ == 1:
                rad[x] = (rad[x] + venstre) & 255
            elif filter_ == 2:
                rad[x] = (rad[x] + over) & 255
            elif filter_ == 3:
                rad[x] = (rad[x] + (venstre + over) // 2) & 255
            elif filter_ == 4:
                rad[x] = (rad[x] + _paeth(venstre, over, over_venstre)) & 255
            elif filter_ != 0:
                raise ValueError(f"Ukjent PNG-filter {filter_}.")
        for x in range(bredde):
            p = rad[x * kanaler : (x + 1) * kanaler]
            if fargetype == 6:
                piksler.append((p[0], p[1], p[2], p[3]))
            elif fargetype == 2:
                piksler.append((p[0], p[1], p[2], 255))
            elif fargetype == 0:
                piksler.append((p[0], p[0], p[0], 255))
            elif fargetype == 4:
                piksler.append((p[0], p[0], p[0], p[1]))
            else:
                idx = p[0]
                r, g, b = palett[idx * 3 : idx * 3 + 3]
                alfa = gjennomsiktig[idx] if idx < len(gjennomsiktig) else 255
                piksler.append((r, g, b, alfa))
        forrige = rad
    return Bilde(bredde, hoyde, piksler)


# --- Fliser og flater --------------------------------------------------------------------


def flis_for(lat: float, lon: float, z: int) -> tuple[int, int]:
    """Web Mercator-flisen (x, y) som dekker punktet på zoomnivå z."""
    n = 2**z
    x = int((lon + 180) / 360 * n)
    y = int((1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n)
    return x, y


def flis_url(z: int, x: int, y: int) -> str:
    return FLIS_URL.format(z=z, x=x, y=y)


def _tone(rgb: RGB) -> tuple[int, int]:
    r, g, b = rgb
    return (g - r, r - b)


def i_flaten(rgb: RGB, grunnfarge: RGB) -> bool:
    """Samme tone som grunnfargen (±1) og høyst `MAKS_SKYGGE` mørkere."""
    tone, grunntone = _tone(rgb), _tone(grunnfarge)
    if abs(tone[0] - grunntone[0]) > 1 or abs(tone[1] - grunntone[1]) > 1:
        return False
    return 0 <= grunnfarge[1] - rgb[1] <= MAKS_SKYGGE


def piksler_i_flaten(bilde: Bilde, flate: Flate) -> list[RGB]:
    grunn = hex_til_rgb(flate.grunnfarge)
    b, h = bilde.bredde, bilde.hoyde
    medlem = [p[3] == 255 and i_flaten(p[:3], grunn) for p in bilde.piksler]
    funnet = []
    for y in range(h):
        for x in range(b):
            if not medlem[y * b + x]:
                continue
            rgb = bilde.piksel(x, y)[:3]
            if flate.glatt:
                naboer = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
                if any(not (0 <= nx < b and 0 <= ny < h) for nx, ny in naboer):
                    continue
                if not all(
                    medlem[ny * b + nx]
                    and max(abs(c - n) for c, n in zip(rgb, bilde.piksel(nx, ny)[:3], strict=True))
                    <= MAKS_NABOSPRANG
                    for nx, ny in naboer
                ):
                    continue
            funnet.append(rgb)
    return funnet


def mork_persentil(farger: Sequence[RGB], persentil: float = PERSENTIL) -> RGB:
    """Fargen ved gitt persentil av relativ luminans, regnet fra den mørkeste."""
    if not farger:
        raise ValueError("Ingen piksler å regne persentil av.")
    sortert = sorted(farger, key=luminans)
    return sortert[int(len(sortert) * persentil)]


def mal_flis(bilde: Bilde, flate: Flate) -> tuple[RGB, RGB, int] | None:
    """(typisk, mørkest, antall piksler) for flaten på flisen, eller None hvis den ikke finnes."""
    farger = piksler_i_flaten(bilde, flate)
    if not farger:
        return None
    typisk = Counter(farger).most_common(1)[0][0]
    return typisk, mork_persentil(farger), len(farger)


def hent(url: str) -> bytes:
    foresporsel = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(foresporsel, timeout=TIDSAVBRUDD_S) as svar:
        return svar.read()


def mal_alle(hent_: Callable[[str], bytes], mappe: Path) -> list[Maling]:
    """Henter og måler hver flis. Flisene lagres i `mappe` så lenge den finnes; `main` bruker en
    midlertidig mappe som slettes etter kjøringen."""
    malinger = []
    for sted in MALESTEDER:
        for z in ZOOMNIVAER:
            x, y = flis_for(sted.lat, sted.lon, z)
            data = hent_(flis_url(z, x, y))
            (mappe / f"{z}-{x}-{y}.png").write_bytes(data)
            bilde = les_png(data)
            for flate in FLATER[sted.flatetype]:
                resultat = mal_flis(bilde, flate)
                if resultat is None:
                    logger.warning("Fant ikke %s på %d/%d/%d (%s).", flate.navn, z, x, y, sted.sted)
                    continue
                typisk, morkest, antall = resultat
                malinger.append(
                    Maling(f"{z}/{x}/{y}", sted.sted, flate.navn, typisk, morkest, antall)
                )
    return malinger


# --- Tabeller ----------------------------------------------------------------------------


def _tall(verdi: float) -> str:
    """Kontrast med to desimaler, rundet ned: WCAG runder ikke opp, så 2,998 er under 3."""
    return f"{math.floor(verdi * 100) / 100:.2f}".replace(".", ",")


def oppsummer(malinger: Sequence[Maling]) -> dict[str, tuple[RGB, RGB]]:
    """Per flate: typisk (den typiske fargen fra flisen med flest piksler av flaten) og mørkest
    (den mørkeste 1. persentilen blant flisene, så kravet gjelder flisen med kraftigst skygge).
    1. persentil betyr at om lag 1 % av flatens piksler på den flisen er enda mørkere."""
    flater: dict[str, list[Maling]] = {}
    for maling in malinger:
        flater.setdefault(maling.flate, []).append(maling)
    return {
        navn: (
            max(liste, key=lambda m: m.antall).typisk,
            min((m.morkest for m in liste), key=luminans),
        )
        for navn, liste in flater.items()
    }


def flistabell(malinger: Sequence[Maling]) -> str:
    linjer = [
        "| Flis (`z/x/y`) | Sted | Flate | Piksler | Typisk | Mørkest (1. persentil) |",
        "|---|---|---|---|---|---|",
    ]
    for m in malinger:
        linjer.append(
            f"| `{m.flis}` | {m.sted} | {m.flate} | {m.antall} "
            f"| `{rgb_til_hex(m.typisk)}` | `{rgb_til_hex(m.morkest)}` |"
        )
    return "\n".join(linjer)


def kontrasttabell(oppsummert: dict[str, tuple[RGB, RGB]], tokener: dict[str, RGB]) -> str:
    """Token × flate. Første tall er mot den mørkeste varianten (kravet), andre mot typisk."""
    hvit = tokener["map-overlay-surface"]
    linjer = [
        "| Flate | Mørkest / typisk | `map-route` | `map-marker-start` | `map-focus-ring`¹ |",
        "|---|---|---|---|---|",
        f"| hvit kant (`map-overlay-surface`) | `{rgb_til_hex(hvit)}` "
        + "".join(
            f"| **{_tall(kontrast(tokener[t], hvit))}** "
            for t in ("map-route", "map-marker-start", "map-focus-ring")
        )
        + "|",
    ]
    for navn, (typisk, morkest) in oppsummert.items():
        celler = "".join(
            f"| {_tall(kontrast(tokener[t], morkest))} / {_tall(kontrast(tokener[t], typisk))} "
            for t in ("map-route", "map-marker-start", "map-focus-ring")
        )
        linjer.append(f"| {navn} | `{rgb_til_hex(morkest)}` / `{rgb_til_hex(typisk)}` {celler}|")
    return "\n".join(linjer)


def symboltabell(tokener: dict[str, RGB]) -> str:
    rute = tokener["map-route"]
    linjer = [
        f"| Symbol | Farge | Fargetone | Kontrast mot `map-route` (tone {fargetone(rute)}°) |",
        "|---|---|---|---|",
    ]
    for navn, verdi in SYMBOLER:
        rgb = hex_til_rgb(verdi)
        linjer.append(f"| {navn} | `{verdi}` | {fargetone(rgb)}° | {_tall(kontrast(rute, rgb))} |")
    return "\n".join(linjer)


def krav_oppfylt(oppsummert: dict[str, tuple[RGB, RGB]], tokener: dict[str, RGB]) -> list[str]:
    """Kravene i DESIGN.md › Kontrastmål. Gir en liste med brudd (tom når alt holder)."""
    hvit = tokener["map-overlay-surface"]
    brudd = [
        f"{flate.navn} ble ikke funnet på noen flis."
        for flater in FLATER.values()
        for flate in flater
        if flate.navn not in oppsummert
    ]
    for token in ("map-route", "map-marker-start"):
        flater = {"hvit kant": hvit} | {navn: mork for navn, (_, mork) in oppsummert.items()}
        for navn, farge in flater.items():
            if kontrast(tokener[token], farge) < KRAV:
                brudd.append(f"{token} mot {navn}: {kontrast(tokener[token], farge):.3f}")
    if kontrast(tokener["map-marker-start"], hvit) < KRAV_TEKST:
        brudd.append("map-marker-start mot «S» er under 4,5.")
    if kontrast(tokener["map-focus-ring"], hvit) < KRAV:
        brudd.append("map-focus-ring mot den hvite ytre kanten er under 3.")
    return brudd


def main() -> int:  # UX-DR35, NFR-4
    tokener = les_tokens(TOKENS_CSS.read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory(prefix="kartfliser-") as mappe:
        try:
            malinger = mal_alle(hent, Path(mappe))
        except (OSError, ValueError) as feil:
            logger.error("Målingen stoppet: %s", feil)
            return 1
    oppsummert = oppsummer(malinger)
    print("## Flisene\n")
    print(flistabell(malinger))
    print("\n## Kontrast\n")
    print(kontrasttabell(oppsummert, tokener))
    hvit = tokener["map-overlay-surface"]
    print(
        f"\n`map-marker-start` mot hvit «S»: {_tall(kontrast(tokener['map-marker-start'], hvit))}"
    )
    print("\n## Symboler\n")
    print(symboltabell(tokener))
    brudd = krav_oppfylt(oppsummert, tokener)
    for linje in brudd:
        logger.error("Under kravet: %s", linje)
    return 1 if brudd else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # Tabellene har æøå, også i Windows-konsollen.
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    sys.exit(main())
