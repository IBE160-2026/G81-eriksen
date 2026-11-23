"""Bygger `data/turer.geojson` fra kurateringslista og Kartverket (AD-3 punkt 2, AR-2).

Kjøres med `python -m skript.bygg_turdatabase` og krever nett. For hver tur i
`data/kurateringsliste.toml`:

1. henter segmentene for hvert rutenummer fra WFS-en for Turrutebasen;
2. velger den korteste stien gjennom nettverket mellom rutepunktene (`domene.rute`);
3. henter høyder hvert 25 m langs stien og filtrerer støy;
4. regner lengde, høydemeter, nivå og tid i `domene/`.

Alt beregnes i minnet før noe skrives. Fila skrives til en midlertidig fil i `data/` og
byttes inn med `os.replace`, så den gamle fila aldri blir delvis overskrevet. Ved feil
stopper skriptet med en norsk melding med tur-ID og exit-kode 1.

Skriptet importerer bare standardbiblioteket og `domene` (AR-2). Format og regler for
lista står i `data/README.md`.
"""

import http.client
import json
import logging
import math
import os
import sys
import tempfile
import tomllib
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape

from domene import gradering, rute, tid
from domene.tur import Form, Tur

logger = logging.getLogger(__name__)

DATA = Path(__file__).resolve().parents[1] / "data"
KURATERINGSLISTE = "kurateringsliste.toml"
TURER = "turer.geojson"
OSM_UTTREKK = "osm-uttrekk.geojson"
MAKS_OSM_OBJEKTER = 100  # AD-3 punkt 3: 100 eller flere gir stopp.

USER_AGENT = "YourNextAdventure/0.1 https://github.com/IBE160-2026/G81-eriksen"
TIDSAVBRUDD_S = 60

WFS_URL = "https://wfs.geonorge.no/skwms1/wfs.turogfriluftsruter"
APP_NS = "http://skjema.geonorge.no/SOSI/produktspesifikasjon/TurOgFriluftsruter/20171210"
GML_NS = "http://www.opengis.net/gml/3.2"
FES_NS = "http://www.opengis.net/fes/2.0"
# `app:rutenummer` ligger under FotruteInfo, ikke rett under Fotrute (spiken før 1.5).
RUTENUMMER_STI = "app:fotruteInfo/app:FotruteInfo/app:rutenummer"

HOYDE_URL = "https://ws.geonorge.no/hoydedata/v1/punkt"
HOYDE_KOORDSYS = "4258"
MAKS_PUNKTER_PER_KALL = 50

TURTYPER = ("marka", "utsikt", "topptur")
TUR_FELT = frozenset(
    {"id", "navn", "form", "turtyper", "rutenummer", "ut_no_url", "startpunkt", "rutepunkter"}
)
STARTPUNKT_FELT = frozenset({"id", "navn", "lat", "lon"})
RUTEPUNKT_FELT = frozenset({"fra", "via", "til"})
KILDE = "turrutebasen"
LISENS = "CC BY 4.0"

Hent = Callable[[str], bytes]
Punkt = tuple[float, float]


class ByggFeil(Exception):  # AD-3
    """Stopper byggingen. Meldingen er norsk og vises til den som kjører skriptet."""


class HentFeil(Exception):  # AD-3
    """Et kall mot Kartverket feilet (HTTP-feil, nettverksfeil eller tidsavbrudd)."""


@dataclass(frozen=True)
class KuratertTur:  # AD-3 punkt 2
    """Én tur fra kurateringslista, validert. `rutepunkter` er (lon, lat) i rekkefølge, og
    ved rundtur er siste punkt lik det første."""

    id: str
    navn: str
    startpunkt_id: str
    startpunkt_navn: str
    startpunkt_lat: float
    startpunkt_lon: float
    form: Form
    turtyper: tuple[str, ...]
    rutenummer: tuple[str, ...]
    rutepunkter: tuple[Punkt, ...]
    ut_no_url: str


# --- Henting -------------------------------------------------------------------------


def hent(url: str) -> bytes:  # AD-3
    """Henter `url` med `urllib.request`. Eneste funksjon som går mot nettet; testene
    sender inn en egen funksjon i stedet."""
    vert = urllib.parse.urlsplit(url).netloc
    foresporsel = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(foresporsel, timeout=TIDSAVBRUDD_S) as svar:
            return svar.read()
    except urllib.error.HTTPError as feil:
        raise HentFeil(f"{vert} svarte med HTTP {feil.code}.") from feil
    except urllib.error.URLError as feil:
        if isinstance(feil.reason, TimeoutError):
            raise HentFeil(f"{vert} svarte ikke innen {TIDSAVBRUDD_S} s.") from feil
        raise HentFeil(f"Fikk ikke kontakt med {vert} ({feil.reason}).") from feil
    except TimeoutError as feil:
        raise HentFeil(f"{vert} svarte ikke innen {TIDSAVBRUDD_S} s.") from feil
    except http.client.HTTPException as feil:
        raise HentFeil(f"Svaret fra {vert} ble brutt ({type(feil).__name__}).") from feil
    except OSError as feil:
        raise HentFeil(f"Nettverksfeil mot {vert} ({feil}).") from feil


def wfs_url(rutenummer: str) -> str:  # AD-3 punkt 2
    filter_xml = (
        f'<fes:Filter xmlns:fes="{FES_NS}" xmlns:app="{APP_NS}">'
        f"<fes:PropertyIsEqualTo><fes:ValueReference>{RUTENUMMER_STI}</fes:ValueReference>"
        f"<fes:Literal>{escape(rutenummer)}</fes:Literal></fes:PropertyIsEqualTo></fes:Filter>"
    )
    parametre = {
        "service": "WFS",
        "version": "2.0.0",
        "request": "GetFeature",
        "typeNames": "app:Fotrute",
        "srsName": "EPSG:4326",
        "namespaces": f"xmlns(app,{APP_NS})",
        "filter": filter_xml,
    }
    return f"{WFS_URL}?{urllib.parse.urlencode(parametre)}"


def les_segmenter(xml_bytes: bytes) -> list[tuple[Punkt, ...]]:  # AD-3 punkt 2
    """Segmentene i et WFS-svar. `gml:posList` har rekkefølgen lon lat."""
    try:
        rot = ET.fromstring(xml_bytes)
    except ET.ParseError as feil:
        raise ValueError(f"WFS-svaret er ikke gyldig XML ({feil}).") from feil
    if not rot.tag.endswith("FeatureCollection"):
        raise ValueError(f"WFS-svaret er ikke en FeatureCollection ({rot.tag}).")
    segmenter = []
    for fotrute in rot.iter(f"{{{APP_NS}}}Fotrute"):
        for poslist in fotrute.iter(f"{{{GML_NS}}}posList"):
            tall = [float(verdi) for verdi in (poslist.text or "").split()]
            if len(tall) % 2:
                raise ValueError("En gml:posList har et oddetall koordinater.")
            segmenter.append(tuple(zip(tall[0::2], tall[1::2], strict=True)))
    return segmenter


def hoyde_url(punkter: Sequence[Punkt]) -> str:  # AD-3 punkt 2
    parametre = {
        "koordsys": HOYDE_KOORDSYS,
        "punkter": json.dumps([[lon, lat] for lon, lat in punkter], separators=(",", ":")),
        "geojson": "false",
    }
    return f"{HOYDE_URL}?{urllib.parse.urlencode(parametre)}"


def hent_hoyder(punkter: Sequence[Punkt], hent: Hent) -> list[float]:  # AD-3 punkt 2
    """Høyder for punktene, i bolker på høyst 50 per kall."""
    hoyder: list[float] = []
    for start in range(0, len(punkter), MAKS_PUNKTER_PER_KALL):
        bolk = punkter[start : start + MAKS_PUNKTER_PER_KALL]
        try:
            svar = json.loads(hent(hoyde_url(bolk)))
            verdier = [punkt["z"] for punkt in svar["punkter"]]
        except (ValueError, KeyError, TypeError) as feil:
            raise HentFeil(f"Høyde-API-et ga et svar som ikke kunne leses ({feil}).") from feil
        if len(verdier) != len(bolk):
            raise HentFeil(f"Høyde-API-et ga {len(verdier)} høyder for {len(bolk)} punkter.")
        for punkt, z in zip(bolk, verdier, strict=True):
            try:
                hoyde = float(z)
            except (TypeError, ValueError):
                hoyde = math.nan
            if not math.isfinite(hoyde) or isinstance(z, bool):
                raise HentFeil(
                    f"Høyde-API-et har ingen gyldig høyde for punktet {_lat_lon(punkt)} ({z!r})."
                )
            hoyder.append(hoyde)
    return hoyder


# --- Kurateringslista ----------------------------------------------------------------


def _lat_lon(punkt: Punkt) -> str:
    return f"[{punkt[1]}, {punkt[0]}]"


def _koordinat(verdi: Any, hva: str) -> Punkt:
    """Gjør `[lat, lon]` fra lista om til (lon, lat)."""
    if (
        not isinstance(verdi, list)
        or len(verdi) != 2
        or not all(isinstance(x, int | float) and not isinstance(x, bool) for x in verdi)
    ):
        raise ByggFeil(f"{hva} må være [lat, lon], fikk {verdi!r}.")
    lat, lon = float(verdi[0]), float(verdi[1])
    # Lat er alltid større enn lon i Norge. Det fanger [lon, lat] skrevet feil vei.
    if not (57.0 <= lat <= 72.0 and 4.0 <= lon <= 32.0):
        raise ByggFeil(f"{hva} må være [lat, lon] i Norge, fikk {verdi!r}.")
    return lon, lat


def _tekst(tabell: dict[str, Any], felt: str, hva: str, *, pakrevd: bool = True) -> str:
    verdi = tabell.get(felt, None if pakrevd else "")
    if not isinstance(verdi, str) or (pakrevd and not verdi.strip()):
        raise ByggFeil(f"{hva} mangler feltet «{felt}» (tekst).")
    return verdi


def _tekstliste(tabell: dict[str, Any], felt: str, hva: str) -> tuple[str, ...]:
    verdi = tabell.get(felt)
    if (
        not isinstance(verdi, list)
        or not verdi
        or not all(isinstance(x, str) and x.strip() for x in verdi)
    ):
        raise ByggFeil(f"{hva} mangler feltet «{felt}» (en liste med tekst).")
    return tuple(verdi)


def _sjekk_felt(tabell: dict[str, Any], lov: frozenset[str], hva: str) -> None:
    """En skrivefeil i et feltnavn (for eksempel «vai») skal stoppe, ikke ignoreres."""
    ukjente = sorted(set(tabell) - lov)
    if ukjente:
        raise ByggFeil(
            f"{hva} har ukjente felt: {', '.join(ukjente)} (lov: {', '.join(sorted(lov))})."
        )


def _les_tur(rad: Any, nummer: int) -> KuratertTur:  # AD-3 punkt 2
    if not isinstance(rad, dict):
        raise ByggFeil(f"Tur nummer {nummer} i lista er ikke en tabell.")
    tur_id = _tekst(rad, "id", f"Tur nummer {nummer} i lista")
    hva = f"Turen «{tur_id}»"
    _sjekk_felt(rad, TUR_FELT, hva)
    navn = _tekst(rad, "navn", hva)

    startpunkt = rad.get("startpunkt")
    if not isinstance(startpunkt, dict):
        raise ByggFeil(f"{hva} mangler tabellen «startpunkt» med id, navn, lat og lon.")
    _sjekk_felt(startpunkt, STARTPUNKT_FELT, f"{hva}: startpunktet")
    start_lon, start_lat = _koordinat(
        [startpunkt.get("lat"), startpunkt.get("lon")], f"{hva}: startpunktets lat og lon"
    )

    try:
        form = Form(rad.get("form"))
    except ValueError:
        raise ByggFeil(f"{hva} har ukjent form {rad.get('form')!r} (rundtur/tur-retur).") from None

    turtyper = _tekstliste(rad, "turtyper", hva)
    ukjente = sorted(set(turtyper) - set(TURTYPER))
    if ukjente:
        raise ByggFeil(f"{hva} har ukjente turtyper {ukjente} (lov: {', '.join(TURTYPER)}).")

    rutepunkter = rad.get("rutepunkter")
    if not isinstance(rutepunkter, dict) or "fra" not in rutepunkter:
        raise ByggFeil(f"{hva} mangler tabellen «rutepunkter» med minst «fra».")
    _sjekk_felt(rutepunkter, RUTEPUNKT_FELT, f"{hva}: rutepunktene")
    fra = _koordinat(rutepunkter["fra"], f"{hva}: rutepunktet «fra»")
    via_raa = rutepunkter.get("via", [])
    if not isinstance(via_raa, list):
        raise ByggFeil(f"{hva}: «via» må være en liste av [lat, lon].")
    via = [_koordinat(punkt, f"{hva}: et via-punkt") for punkt in via_raa]
    if form == Form.RUNDTUR:
        if "til" in rutepunkter:
            raise ByggFeil(f"{hva} er en rundtur og skal ikke ha «til» (den slutter i «fra»).")
        if not via:
            raise ByggFeil(f"{hva} er en rundtur og må ha minst ett «via»-punkt.")
        punkter = (fra, *via, fra)
    else:
        if "til" not in rutepunkter:
            raise ByggFeil(f"{hva} er tur-retur og må ha «til» (vendepunktet).")
        punkter = (fra, *via, _koordinat(rutepunkter["til"], f"{hva}: rutepunktet «til»"))

    return KuratertTur(
        id=tur_id,
        navn=navn,
        startpunkt_id=_tekst(startpunkt, "id", f"{hva}: startpunktet"),
        startpunkt_navn=_tekst(startpunkt, "navn", f"{hva}: startpunktet"),
        startpunkt_lat=start_lat,
        startpunkt_lon=start_lon,
        form=form,
        turtyper=turtyper,
        rutenummer=_tekstliste(rad, "rutenummer", hva),
        rutepunkter=punkter,
        ut_no_url=_tekst(rad, "ut_no_url", hva, pakrevd=False),
    )


def les_kurateringsliste(sti: Path) -> list[KuratertTur]:  # AD-3 punkt 2
    """Leser og validerer hele lista før noe hentes."""
    try:
        with sti.open("rb") as fil:
            innhold = tomllib.load(fil)
    except FileNotFoundError:
        raise ByggFeil(f"Fant ikke kurateringslista {sti}.") from None
    except (tomllib.TOMLDecodeError, UnicodeDecodeError) as feil:
        raise ByggFeil(f"Kurateringslista er ikke gyldig TOML i UTF-8 ({feil}).") from None
    except OSError as feil:
        raise ByggFeil(f"Kunne ikke lese kurateringslista {sti} ({feil}).") from None

    rader = innhold.get("tur")
    if not isinstance(rader, list) or not rader:
        raise ByggFeil("Kurateringslista har ingen turer ([[tur]]).")
    turer = [_les_tur(rad, nummer) for nummer, rad in enumerate(rader, start=1)]

    sett: set[str] = set()
    for tur in turer:
        if tur.id in sett:
            raise ByggFeil(f"Tur-ID-en «{tur.id}» står flere ganger i lista.")
        sett.add(tur.id)

    startpunkter: dict[str, tuple[str, float, float]] = {}
    for tur in turer:
        verdi = (tur.startpunkt_navn, tur.startpunkt_lat, tur.startpunkt_lon)
        forrige = startpunkter.setdefault(tur.startpunkt_id, verdi)
        if forrige != verdi:
            raise ByggFeil(
                f"Startpunktet «{tur.startpunkt_id}» har ulikt navn eller ulik koordinat i "
                f"lista ({forrige} og {verdi}, sist ved turen «{tur.id}»)."
            )
    return turer


def sjekk_osm_uttrekk(data: Path) -> None:  # AD-3 punkt 3
    """Leser `osm-uttrekk.geojson` bare hvis fila finnes. 100 objekter eller flere gir stopp."""
    sti = data / OSM_UTTREKK
    if not sti.exists():
        return
    try:
        innhold = json.loads(sti.read_text(encoding="utf-8"))
        features = innhold["features"]
    except (OSError, ValueError, KeyError, TypeError) as feil:
        raise ByggFeil(f"{OSM_UTTREKK} kunne ikke leses ({feil}).") from None
    if not isinstance(features, list):
        raise ByggFeil(f"{OSM_UTTREKK} har ikke en liste i «features».")
    antall = len(features)
    if antall >= MAKS_OSM_OBJEKTER:
        raise ByggFeil(
            f"{OSM_UTTREKK} har {antall} objekter. OSM er bare et supplement og skal ha "
            f"færre enn {MAKS_OSM_OBJEKTER} (AD-3 punkt 3)."
        )


# --- Bygging -------------------------------------------------------------------------


def hent_segmenter(tur: KuratertTur, hent: Hent) -> list[tuple[Punkt, ...]]:  # AD-3
    segmenter = []
    for nummer in tur.rutenummer:
        logger.info("Henter rutenummer %s for «%s» fra Turrutebasen.", nummer, tur.id)
        try:
            nye = les_segmenter(hent(wfs_url(nummer)))
        except (HentFeil, ValueError) as feil:
            raise ByggFeil(f"Turen «{tur.id}», rutenummer {nummer}: {feil}") from None
        if not nye:
            raise ByggFeil(
                f"Turen «{tur.id}»: rutenummer {nummer} ga 0 segmenter i Turrutebasen. "
                "Sjekk rutenummeret."
            )
        segmenter.extend(nye)
    return segmenter


def bygg_tur(tur: KuratertTur, hent: Hent) -> Tur:  # AD-3 punkt 2, AR-2
    segmenter = hent_segmenter(tur, hent)
    rutenummer = ", ".join(tur.rutenummer)
    try:
        sti = rute.sti_gjennom(rute.lag_nettverk(segmenter), tur.rutepunkter)
    except rute.PunktForLangtUnna as feil:
        raise ByggFeil(
            f"Turen «{tur.id}»: rutepunktet {_lat_lon(feil.punkt)} ligger "
            f"{feil.avstand_m:.0f} m fra nærmeste node i nettverket for rutenummer "
            f"{rutenummer} (maks {feil.maks_m:.0f} m)."
        ) from None
    except rute.IngenSti as feil:
        raise ByggFeil(
            f"Turen «{tur.id}»: ingen sti mellom {_lat_lon(feil.fra)} og {_lat_lon(feil.til)} "
            f"i nettverket for rutenummer {rutenummer}."
        ) from None
    except rute.PunkterPaSammeNode as feil:
        raise ByggFeil(
            f"Turen «{tur.id}»: rutepunktene {_lat_lon(feil.fra)} og {_lat_lon(feil.til)} "
            f"festes til samme node i nettverket for rutenummer {rutenummer}. "
            "Flytt eller fjern ett av dem."
        ) from None
    except rute.RuteFeil as feil:
        raise ByggFeil(f"Turen «{tur.id}», rutenummer {rutenummer}: {feil}") from None

    omsamplet = rute.omsampl(sti)
    logger.info("Henter %d høyder for «%s».", len(omsamplet), tur.id)
    try:
        hoyder = hent_hoyder([punkt for _, punkt in omsamplet], hent)
        startpunkt_hoyde = hent_hoyder([(tur.startpunkt_lon, tur.startpunkt_lat)], hent)[0]
    except HentFeil as feil:
        raise ByggFeil(f"Turen «{tur.id}»: {feil}") from None

    lengde_m = rute.hele_meter(rute.linjelengde_m(sti))
    hoydemeter_m, nedstigning_m = rute.hoydemeter_og_nedstigning(hoyder)
    return Tur(
        id=tur.id,
        navn=tur.navn,
        startpunkt_id=tur.startpunkt_id,
        startpunkt_navn=tur.startpunkt_navn,
        startpunkt_lat=tur.startpunkt_lat,
        startpunkt_lon=tur.startpunkt_lon,
        startpunkt_hoyde_m=rute.hele_meter(startpunkt_hoyde),
        form=tur.form,
        turtyper=tur.turtyper,
        lengde_m=lengde_m,
        hoydemeter_m=hoydemeter_m,
        nedstigning_m=nedstigning_m,
        hoydeprofil=rute.hoydeprofil([avstand for avstand, _ in omsamplet], hoyder),
        turniva=gradering.turniva(lengde_m, hoydemeter_m),
        estimert_tid_min=tid.estimert_tid_min(tur.form, lengde_m, hoydemeter_m, nedstigning_m),
        ut_no_url=tur.ut_no_url,
        kilde=KILDE,
        lisens=LISENS,
        geometry=sti,
    )


def geojson_tekst(turer: Sequence[Tur]) -> str:  # AD-3
    """Samme turer gir samme tekst: rekkefølgen følger lista, og nøklene er sortert."""
    samling = {
        "type": "FeatureCollection",
        "features": [tur.til_geojson_feature() for tur in turer],
    }
    return json.dumps(samling, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def skriv_atomisk(sti: Path, tekst: str) -> None:  # AD-3
    """Skriver til en midlertidig fil i samme mappe og bytter den inn med `os.replace`."""
    fd, midlertidig = tempfile.mkstemp(dir=sti.parent, prefix=f".{sti.name}.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fil:
            fil.write(tekst)
            fil.flush()
            os.fsync(fil.fileno())
        os.replace(midlertidig, sti)
    except BaseException:
        Path(midlertidig).unlink(missing_ok=True)
        raise


def bygg(data: Path = DATA, hent: Hent = hent) -> list[Tur]:  # AD-3 punkt 2
    """Validerer lista, bygger alle turene i minnet og skriver `turer.geojson` til slutt."""
    kuraterte = les_kurateringsliste(data / KURATERINGSLISTE)
    sjekk_osm_uttrekk(data)
    turer = [bygg_tur(tur, hent) for tur in kuraterte]
    try:
        skriv_atomisk(data / TURER, geojson_tekst(turer))
    except OSError as feil:
        raise ByggFeil(f"Kunne ikke skrive {TURER} ({feil}).") from None
    return turer


def main() -> int:  # AD-3
    try:
        turer = bygg(DATA, hent)
    except ByggFeil as feil:
        logger.error("Byggingen stoppet: %s", feil)
        logger.error("%s er ikke endret.", TURER)
        return 1
    for tur in turer:
        logger.info(
            "%s: %d m, %d hm opp, %d m ned, %s, %d min.",
            tur.id,
            tur.lengde_m,
            tur.hoydemeter_m,
            tur.nedstigning_m,
            tur.turniva.value,
            tur.estimert_tid_min,
        )
    logger.info("Skrev %d turer til data/%s.", len(turer), TURER)
    return 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    sys.exit(main())
