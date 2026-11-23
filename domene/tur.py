"""Turen som dataklasse, GeoJSON-omforming og totaler (AR-3, AD-3 punkt 1).

Ved tur-retur lagres lengde, høydemeter og nedstigning for én vei. Totalene for hele
turen regnes bare av funksjonene i denne modulen.
"""

import math
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

# Middelradius for jorda (IUGG), brukt i haversine (AR-3).
JORDRADIUS_M = 6_371_008.8


class Form(StrEnum):  # AR-3
    RUNDTUR = "rundtur"
    TUR_RETUR = "tur-retur"


class Turniva(StrEnum):  # AR-3, FR-2
    GRONN = "gronn"
    BLA = "bla"
    ROD = "rod"
    SVART = "svart"


@dataclass(frozen=True)
class Tur:  # AR-3
    """Eneste beskrivelse av en tur. Lister lagres som tuples, så turen kan hashes.

    `geometry` er koordinatene i GeoJSON-`LineString`-en (WGS84, lon lat), lagret som
    tuples. `til_geojson_feature()` gir det fulle GeoJSON-objektet.
    """

    id: str
    navn: str
    startpunkt_id: str
    startpunkt_navn: str
    startpunkt_lat: float
    startpunkt_lon: float
    startpunkt_hoyde_m: int
    form: Form
    turtyper: tuple[str, ...]
    lengde_m: int
    hoydemeter_m: int
    nedstigning_m: int
    hoydeprofil: tuple[tuple[float, float], ...]
    turniva: Turniva
    estimert_tid_min: int
    ut_no_url: str
    kilde: str
    lisens: str
    geometry: tuple[tuple[float, ...], ...]

    def til_geojson_feature(self) -> dict[str, Any]:  # AR-3
        """Gir en GeoJSON-`Feature` som kan gjøres om til JSON (lister, ikke tuples)."""
        properties = {
            "navn": self.navn,
            "startpunkt_id": self.startpunkt_id,
            "startpunkt_navn": self.startpunkt_navn,
            "startpunkt_lat": self.startpunkt_lat,
            "startpunkt_lon": self.startpunkt_lon,
            "startpunkt_hoyde_m": self.startpunkt_hoyde_m,
            "form": self.form.value,
            "turtyper": list(self.turtyper),
            "lengde_m": self.lengde_m,
            "hoydemeter_m": self.hoydemeter_m,
            "nedstigning_m": self.nedstigning_m,
            "hoydeprofil": [list(punkt) for punkt in self.hoydeprofil],
            "turniva": self.turniva.value,
            "estimert_tid_min": self.estimert_tid_min,
            "ut_no_url": self.ut_no_url,
            "kilde": self.kilde,
            "lisens": self.lisens,
        }
        return {
            "type": "Feature",
            "id": self.id,
            "geometry": {
                "type": "LineString",
                "coordinates": [list(punkt) for punkt in self.geometry],
            },
            "properties": properties,
        }

    @classmethod
    def fra_geojson_feature(cls, feature: dict[str, Any]) -> "Tur":  # AR-3
        """Gjør en GeoJSON-`Feature` om til `Tur`. Ukjent form eller nivå gir `ValueError`."""
        if feature.get("type") != "Feature":
            raise ValueError(f"Forventet GeoJSON-type «Feature», fikk {feature.get('type')!r}.")
        geometri = feature["geometry"]
        if geometri.get("type") != "LineString":
            raise ValueError(f"Forventet geometri «LineString», fikk {geometri.get('type')!r}.")
        p = feature["properties"]
        return cls(
            id=feature["id"],
            navn=p["navn"],
            startpunkt_id=p["startpunkt_id"],
            startpunkt_navn=p["startpunkt_navn"],
            startpunkt_lat=float(p["startpunkt_lat"]),
            startpunkt_lon=float(p["startpunkt_lon"]),
            startpunkt_hoyde_m=int(p["startpunkt_hoyde_m"]),
            form=Form(p["form"]),
            turtyper=tuple(p["turtyper"]),
            lengde_m=int(p["lengde_m"]),
            hoydemeter_m=int(p["hoydemeter_m"]),
            nedstigning_m=int(p["nedstigning_m"]),
            hoydeprofil=tuple(tuple(punkt) for punkt in p["hoydeprofil"]),
            turniva=Turniva(p["turniva"]),
            estimert_tid_min=int(p["estimert_tid_min"]),
            ut_no_url=p["ut_no_url"],
            kilde=p["kilde"],
            lisens=p["lisens"],
            geometry=tuple(tuple(punkt) for punkt in geometri["coordinates"]),
        )


def total_lengde_m(form: Form, lengde_m: int) -> int:  # FR-3, AR-3
    """Lengden for hele turen. Ved tur-retur gås lengden to ganger."""
    return lengde_m * 2 if form == Form.TUR_RETUR else lengde_m


def total_hoydemeter_m(form: Form, hoydemeter_m: int, nedstigning_m: int) -> int:  # FR-3, AR-3
    """Høydemeter for hele turen. Ved tur-retur er høydemeterne tilbake lik nedstigningen ut."""
    return hoydemeter_m + nedstigning_m if form == Form.TUR_RETUR else hoydemeter_m


def total_nedstigning_m(form: Form, hoydemeter_m: int, nedstigning_m: int) -> int:  # FR-3, AR-3
    """Nedstigning for hele turen. Ved tur-retur er nedstigningen tilbake lik høydemeterne ut."""
    return nedstigning_m + hoydemeter_m if form == Form.TUR_RETUR else nedstigning_m


def avstand_m(a: tuple[float, ...], b: tuple[float, ...]) -> float:  # AR-3
    """Avstanden i meter mellom to punkter (lon, lat) i WGS84, med haversine.

    Punktene har samme rekkefølge som i `geometry` og GeoJSON. Ingen omregning trengs.
    """
    lon1, lat1 = math.radians(a[0]), math.radians(a[1])
    lon2, lat2 = math.radians(b[0]), math.radians(b[1])
    h = (
        math.sin((lat2 - lat1) / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    )
    return 2 * JORDRADIUS_M * math.asin(math.sqrt(min(1.0, h)))
