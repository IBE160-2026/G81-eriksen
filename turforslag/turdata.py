"""Omgjøring mellom `domene.tur.Tur` og modellene `Startpunkt` og `Tur` (AD-3 punkt 4–5).

Dataklassen har flate startpunktfelt, modellene har en egen `Startpunkt`. Verdiene lagres
og leses som de er. Ingenting regnes på nytt her (AD-2): nivå, høydemeter og tid kommer
fra turdatabasen.
"""

from collections.abc import Sequence
from dataclasses import dataclass

from django.db import transaction

from domene import tur as domenetur
from turforslag.models import Startpunkt, Tur


@dataclass(frozen=True)
class Lagret:  # AR-5
    """Hva `lagre_turer` gjorde. `mangler_i_fila` er tur-ID-er i databasen som ikke var med."""

    nye_turer: int
    oppdaterte_turer: int
    nye_startpunkter: int
    oppdaterte_startpunkter: int
    mangler_i_fila: tuple[str, ...]


@transaction.atomic
def lagre_turer(turer: Sequence[domenetur.Tur]) -> Lagret:  # AD-3 punkt 4, AR-5
    """Oppretter eller oppdaterer startpunkter og så turer etter `id`, i én transaksjon.

    Turene må være validert med `domene.tur.valider_turer` først. Ingenting slettes:
    turer som finnes i databasen, men ikke i `turer`, står uendret og returneres sortert.
    """
    startpunkter: dict[str, domenetur.Tur] = {}
    for tur in turer:
        startpunkter.setdefault(tur.startpunkt_id, tur)

    nye_startpunkter = 0
    for startpunkt_id, tur in startpunkter.items():
        _, ny = Startpunkt.objects.update_or_create(
            id=startpunkt_id,
            defaults={
                "navn": tur.startpunkt_navn,
                "lat": tur.startpunkt_lat,
                "lon": tur.startpunkt_lon,
                "hoyde_m": tur.startpunkt_hoyde_m,
            },
        )
        nye_startpunkter += ny

    nye_turer = 0
    for tur in turer:
        _, ny = Tur.objects.update_or_create(
            id=tur.id,
            defaults={
                "navn": tur.navn,
                "startpunkt_id": tur.startpunkt_id,
                "form": tur.form.value,
                "turtyper": list(tur.turtyper),
                "lengde_m": tur.lengde_m,
                "hoydemeter_m": tur.hoydemeter_m,
                "nedstigning_m": tur.nedstigning_m,
                "hoydeprofil": [list(punkt) for punkt in tur.hoydeprofil],
                "turniva": tur.turniva.value,
                "estimert_tid_min": tur.estimert_tid_min,
                "ut_no_url": tur.ut_no_url,
                "kilde": tur.kilde,
                "lisens": tur.lisens,
                "geometry": [list(punkt) for punkt in tur.geometry],
            },
        )
        nye_turer += ny

    mangler = Tur.objects.exclude(id__in=[tur.id for tur in turer]).order_by("id")
    return Lagret(
        nye_turer=nye_turer,
        oppdaterte_turer=len(turer) - nye_turer,
        nye_startpunkter=nye_startpunkter,
        oppdaterte_startpunkter=len(startpunkter) - nye_startpunkter,
        mangler_i_fila=tuple(mangler.values_list("id", flat=True)),
    )


def tur_fra_modell(modell: Tur) -> domenetur.Tur:  # AD-3 punkt 5, AR-6
    """Gjør en `Tur`-modell om til dataklassen. Lister fra JSON blir tuples."""
    startpunkt = modell.startpunkt
    return domenetur.Tur(
        id=modell.id,
        navn=modell.navn,
        startpunkt_id=startpunkt.id,
        startpunkt_navn=startpunkt.navn,
        startpunkt_lat=startpunkt.lat,
        startpunkt_lon=startpunkt.lon,
        startpunkt_hoyde_m=startpunkt.hoyde_m,
        form=domenetur.Form(modell.form),
        turtyper=tuple(modell.turtyper),
        lengde_m=modell.lengde_m,
        hoydemeter_m=modell.hoydemeter_m,
        nedstigning_m=modell.nedstigning_m,
        hoydeprofil=tuple(tuple(punkt) for punkt in modell.hoydeprofil),
        turniva=domenetur.Turniva(modell.turniva),
        estimert_tid_min=modell.estimert_tid_min,
        ut_no_url=modell.ut_no_url,
        kilde=modell.kilde,
        lisens=modell.lisens,
        geometry=tuple(tuple(punkt) for punkt in modell.geometry),
    )


def alle_turer() -> tuple[domenetur.Tur, ...]:  # FR-5, AD-3 punkt 5
    """Alle turene i databasen som dataklasser, sortert på ID."""
    return tuple(tur_fra_modell(modell) for modell in Tur.objects.select_related("startpunkt"))


def hent_tur(tur_id: str) -> domenetur.Tur | None:  # FR-7
    """Turen med ID-en, eller `None` hvis den ikke finnes."""
    modell = Tur.objects.select_related("startpunkt").filter(id=tur_id).first()
    return tur_fra_modell(modell) if modell else None


def startpunkter_med_turer() -> tuple[tuple[str, str], ...]:  # FR-4
    """(id, navn) for startpunktene som har minst én tur, usortert.

    `lastinn` sletter aldri, så startpunkter uten turer kan finnes i tabellen.
    """
    return tuple(
        Startpunkt.objects.filter(turer__isnull=False).distinct().values_list("id", "navn")
    )
