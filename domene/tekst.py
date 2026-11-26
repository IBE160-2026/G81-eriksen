"""Norsk formatering for grensesnittet (UX-DR31, AR-16, FR-4, FR-6).

Faste formater: «ca. 1 t 35 min», «3,5 km totalt», «Grønn – lett», «2,5 t» og «2,5 timer»,
«Lørdag 7. november» og søkeoppsummeringen «Lørdag 7. nov. · 2 t · Utsikt». Views og maler
formaterer ingenting selv (AR-2).
"""

from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import date, timedelta
from decimal import ROUND_HALF_UP, Decimal
from typing import Any

from domene.okt import Soketilstand
from domene.sok import (
    DATO_DAGER_FREM,
    MAKS_VARIGHET_MIN,
    MIN_VARIGHET_MIN,
    VARIGHET_STEG_MIN,
    Sok,
)
from domene.tur import TURTYPER, Form, Tur, Turniva, total_hoydemeter_m, total_lengde_m
from domene.utvalg import Status

_NIVATEKST = {
    Turniva.GRONN: "Grønn – lett",
    Turniva.BLA: "Blå – moderat",
    Turniva.ROD: "Rød – moderat",
    Turniva.SVART: "Svart – vanskelig",
}

# Turtypevalgene fra Mikrotekst. Rekkefølgen følger `TURTYPER`.
_TURTYPENAVN = {"marka": "Marka", "utsikt": "Utsikt", "topptur": "Topptur"}

_FORMNAVN = {Form.RUNDTUR: "Rundtur", Form.TUR_RETUR: "Tur-retur"}

_UKEDAGER = ("mandag", "tirsdag", "onsdag", "torsdag", "fredag", "lørdag", "søndag")
_MANEDER = (
    "januar",
    "februar",
    "mars",
    "april",
    "mai",
    "juni",
    "juli",
    "august",
    "september",
    "oktober",
    "november",
    "desember",
)
# Forkortelsene etter Språkrådet. «mai» er hele ordet og har ikke punktum.
_MANEDER_KORT = (
    "jan.",
    "feb.",
    "mar.",
    "apr.",
    "mai",
    "jun.",
    "jul.",
    "aug.",
    "sep.",
    "okt.",
    "nov.",
    "des.",
)

# Æ, Ø og Å sorteres etter Z, i den rekkefølgen: «{», «|» og «}» kommer rett etter «z».
_NORSK_SORTERING = str.maketrans({"æ": "{", "ø": "|", "å": "}"})


def formater_tid(minutter: int) -> str:  # FR-3, UX-DR31
    """«ca. 45 min», «ca. 2 t» eller «ca. 1 t 35 min»."""
    timer, rest = divmod(minutter, 60)
    if timer == 0:
        return f"ca. {rest} min"
    if rest == 0:
        return f"ca. {timer} t"
    return f"ca. {timer} t {rest} min"


def formater_lengde(lengde_m: int) -> str:  # UX-DR31, AR-16
    """«3,5 km»: én desimal med desimalkomma, avrundet halv opp, uten «,0»."""
    km = (Decimal(lengde_m) / 1000).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
    if km == km.to_integral_value():
        return f"{int(km)} km"
    return f"{km:f}".replace(".", ",") + " km"


def formater_lengde_totalt(lengde_m: int) -> str:  # UX-DR31, AR-16
    """«3,5 km totalt»: én desimal med desimalkomma, avrundet halv opp, uten «,0».

    `lengde_m` er lengden for hele turen, ikke den lagrede lengden for én vei ved
    tur-retur. Den som kaller, regner den ut med `domene.tur.total_lengde_m` først.
    """
    return f"{formater_lengde(lengde_m)} totalt"


def formater_niva(niva: Turniva) -> str:  # FR-2, UX-DR31
    """«Grønn – lett», «Blå – moderat», «Rød – moderat» eller «Svart – vanskelig»."""
    return _NIVATEKST[niva]


def formater_hoydemeter(hoydemeter_m: int) -> str:  # FR-6, UX-DR31
    """«ca. 130»: høydemeterne for hele turen, avrundet halv opp til nærmeste 10 m."""
    tiere = (Decimal(hoydemeter_m) / 10).quantize(Decimal(1), rounding=ROUND_HALF_UP)
    return f"ca. {int(tiere) * 10}"


def _naermeste_10(verdi: float) -> int:  # FR-6
    """Avrunder halv opp til nærmeste 10. Via `str`, så flyttallet regnes slik det står."""
    tiere = (Decimal(str(verdi)) / 10).quantize(Decimal(1), rounding=ROUND_HALF_UP)
    return int(tiere) * 10


def laveste_og_hoyeste(
    hoydeprofil: Iterable[tuple[float, float]],
) -> tuple[int, int]:  # FR-6, UX-DR15
    """Laveste og høyeste punkt i høydeprofilen, avrundet til nærmeste 10 m.

    Profilen er par av (avstand, høyde). «Kartet i tekst» og Turillustrasjon (6.1) bruker
    begge denne funksjonen. Ved tur-retur dekker profilen én vei, som har de samme
    ytterpunktene som hele turen. Tom profil gir `ValueError`.
    """
    hoyder = [hoyde for _, hoyde in hoydeprofil]
    if not hoyder:
        raise ValueError("Høydeprofilen er tom, så den har ikke laveste og høyeste punkt.")
    return _naermeste_10(min(hoyder)), _naermeste_10(max(hoyder))


def formater_form(form: Form) -> str:  # FR-6
    """«Rundtur» eller «Tur-retur» (Formmerke)."""
    return _FORMNAVN[Form(form)]


def formater_turtype(turtype: str) -> str:  # FR-4
    """«Marka», «Utsikt» eller «Topptur»."""
    return _TURTYPENAVN[turtype]


def turtype_treff(turtype: str) -> str:  # FR-6
    """«Utsikt – som du ba om» (Turtype-treff)."""
    return f"{formater_turtype(turtype)} – som du ba om"


def _timer(minutter: int) -> str:  # FR-4
    """«2» eller «2,5»: hele timer eller halvtimer med desimalkomma."""
    timer, rest = divmod(minutter, 60)
    if rest == 0:
        return str(timer)
    if rest == 30:
        return f"{timer},5"
    raise ValueError(f"Varigheten må være hele eller halve timer, fikk {minutter} minutter.")


def formater_varighet(minutter: int) -> str:  # FR-4, UX-DR31
    """«1 t», «1,5 t» … «12 t»: varigheten i valglista og i søkeoppsummeringen."""
    return f"{_timer(minutter)} t"


def formater_varighet_timer(minutter: int) -> str:  # FR-12, UX-DR31
    """«1 time», «1,5 timer» eller «2 timer»: varigheten i løpende tekst."""
    return "1 time" if minutter == 60 else f"{_timer(minutter)} timer"


def varighetsvalg() -> tuple[tuple[int, str], ...]:  # FR-4
    """De 23 valgene for Varighet, 1–12 t i halvtimessteg, bygget av konstantene i `sok`."""
    return tuple(
        (minutter, formater_varighet(minutter))
        for minutter in range(MIN_VARIGHET_MIN, MAKS_VARIGHET_MIN + 1, VARIGHET_STEG_MIN)
    )


def turtypevalg() -> tuple[tuple[str, str], ...]:  # FR-4
    """Turtypene som kan velges, uten «Alle turtyper»."""
    return tuple((turtype, formater_turtype(turtype)) for turtype in TURTYPER)


def datoperiode(i_dag: date) -> tuple[date, ...]:  # FR-4
    """De 31 datoene som kan velges: fra i dag til og med i dag + 30 dager."""
    return tuple(i_dag + timedelta(days=dager) for dager in range(DATO_DAGER_FREM + 1))


def formater_dato(dato: date) -> str:  # FR-4
    """«7. november»."""
    return f"{dato.day}. {_MANEDER[dato.month - 1]}"


def formater_dato_valg(dato: date) -> str:  # FR-4. Formatet er [ASSUMPTION] i Mikrotekst.
    """«Lørdag 7. november»: teksten i datovalget."""
    return f"{_UKEDAGER[dato.weekday()].capitalize()} {formater_dato(dato)}"


def formater_dato_kort(dato: date) -> str:  # FR-6
    """«Lørdag 7. nov.»: datoen i søkeoppsummeringen."""
    ukedag = _UKEDAGER[dato.weekday()].capitalize()
    return f"{ukedag} {dato.day}. {_MANEDER_KORT[dato.month - 1]}"


def datovalg(i_dag: date) -> tuple[tuple[date, str], ...]:  # FR-4
    """De 31 valgene for Dato, med tekst som «Lørdag 7. november»."""
    return tuple((dato, formater_dato_valg(dato)) for dato in datoperiode(i_dag))


def siste_dato(i_dag: date) -> str:  # FR-4
    """«26. desember»: den siste datoen som kan velges, til feilmeldingen for Dato."""
    return formater_dato(datoperiode(i_dag)[-1])


def norsk_sorteringsnokkel(tekst: str) -> str:  # FR-4
    """Nøkkel som sorterer etter norsk alfabet: Æ, Ø og Å kommer etter Z."""
    return tekst.casefold().translate(_NORSK_SORTERING)


def sorter_startpunkter(
    startpunkter: Iterable[tuple[str, str]],
) -> tuple[tuple[str, str], ...]:  # FR-4
    """Sorterer par av (id, navn) på navnet etter norsk alfabet, og så på ID."""
    return tuple(sorted(startpunkter, key=lambda par: (norsk_sorteringsnokkel(par[1]), par[0])))


def sokeoppsummering(sok: Sok, startpunkt_navn: str | None = None) -> str:  # FR-6, UX-DR16
    """«Lørdag 7. nov. · 2 t · Utsikt», med startpunktet til slutt når det er valgt."""
    deler = [formater_dato_kort(sok.dato), formater_varighet(sok.varighet_min)]
    if sok.turtype is not None:
        deler.append(formater_turtype(sok.turtype))
    if startpunkt_navn:
        deler.append(startpunkt_navn)
    return " · ".join(deler)


def kartbeskrivelse(tur: Tur) -> str:  # FR-6, UX-DR15
    """«Kartet i tekst»: laget fra turdata, aldri av KI.

    «Rundtur på 3,5 km totalt fra Granvannet p-plass. Ruten stiger ca. 130 høydemeter,
    fra 180 til 310 moh.» Lengde og høydemeter gjelder hele turen (dobbelt ved tur-retur).
    """
    laveste, hoyeste = laveste_og_hoyeste(tur.hoydeprofil)
    lengde = formater_lengde_totalt(total_lengde_m(tur.form, tur.lengde_m))
    hoydemeter = formater_hoydemeter(
        total_hoydemeter_m(tur.form, tur.hoydemeter_m, tur.nedstigning_m)
    )
    return (
        f"{formater_form(tur.form)} på {lengde} fra {tur.startpunkt_navn}. "
        f"Ruten stiger {hoydemeter} høydemeter, fra {laveste} til {hoyeste} moh."
    )


def kart_geojson(tur: Tur) -> dict[str, Any]:  # FR-6, AR-10
    """GeoJSON-`Feature` med rutelinjen (WGS84, lon lat) til `kart.js` via `json_script`.

    `properties.start` er rutens første punkt, der startmarkøren «S» står, så `kart.js`
    ikke regner ut noe selv. Ved tur-retur er linjen den lagrede veien ut.
    """
    koordinater = [[punkt[0], punkt[1]] for punkt in tur.geometry]
    return {
        "type": "Feature",
        "geometry": {"type": "LineString", "coordinates": koordinater},
        "properties": {"start": koordinater[0] if koordinater else None},
    }


@dataclass(frozen=True)
class Turvisning:  # FR-6
    """Teksten for én tur på Turforslag. Alt er ferdig formatert."""

    id: str
    navn: str
    niva: str
    nivatekst: str
    turtype_treff: str | None
    topptur_erstattet: bool
    form: str
    startpunkt_navn: str
    lengde: str
    hoydemeter: str
    tid: str
    ut_no_url: str
    begrunnelse: str
    kartbeskrivelse: str
    kart_navn: str
    kart_geojson: dict[str, Any] = field(hash=False)


@dataclass(frozen=True)
class Forslagsvisning:  # FR-6, FR-7, FR-8
    """Det Turforslag viser: søkeoppsummeringen og enten en tur eller et Tilstandspanel."""

    sokeoppsummering: str
    status: Status
    tur: Turvisning | None

    @property
    def ingen_treff(self) -> bool:  # FR-8
        return self.status == Status.INGEN_TREFF

    @property
    def bare_over_nivatak(self) -> bool:  # FR-8
        return self.status == Status.BARE_OVER_NIVATAK


def turvisning(sok: Sok, status: Status, tur: Tur, begrunnelse: str) -> Turvisning:  # FR-6
    """Formaterer turen. Tid og nivå kommer fra turdatabasen og regnes aldri på nytt."""
    treff = None
    if sok.turtype is not None and sok.turtype in tur.turtyper:
        treff = turtype_treff(sok.turtype)
    return Turvisning(
        id=tur.id,
        navn=tur.navn,
        niva=Turniva(tur.turniva).value,
        nivatekst=formater_niva(tur.turniva),
        turtype_treff=treff,
        topptur_erstattet=status == Status.TOPPTUR_ERSTATTET,
        form=formater_form(tur.form),
        startpunkt_navn=tur.startpunkt_navn,
        lengde=formater_lengde(total_lengde_m(tur.form, tur.lengde_m)),
        hoydemeter=formater_hoydemeter(
            total_hoydemeter_m(tur.form, tur.hoydemeter_m, tur.nedstigning_m)
        ),
        tid=formater_tid(tur.estimert_tid_min),
        ut_no_url=tur.ut_no_url,
        begrunnelse=begrunnelse,
        kartbeskrivelse=kartbeskrivelse(tur),
        kart_navn=f"Kart over {tur.navn}",
        kart_geojson=kart_geojson(tur),
    )


def forslagsvisning(
    tilstand: Soketilstand,
    tur: Tur | None,
    begrunnelse: str = "",
    startpunkt_navn: str | None = None,
) -> Forslagsvisning:  # FR-6, FR-7, FR-8
    """Visningen av søketilstanden. `tur` er gjeldende tur, eller `None` ved Tilstandspanel."""
    return Forslagsvisning(
        sokeoppsummering=sokeoppsummering(tilstand.sok, startpunkt_navn),
        status=tilstand.status,
        tur=turvisning(tilstand.sok, tilstand.status, tur, begrunnelse) if tur else None,
    )
