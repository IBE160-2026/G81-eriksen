"""Egne testturer for Søk og Turforslag (story 1.9). Leser ikke `data/turer.geojson`.

| ID           | Turtype | Nivå  | Tid     | Startpunkt  | ut.no |
|--------------|---------|-------|---------|-------------|-------|
| marka-lang   | marka   | grønn | 170 min | Bråten      | ja    |
| utsikt-kort  | utsikt  | grønn | 140 min | Åsen        | nei   |
| topptur-lang | topptur | grønn | 300 min | Åsen        | nei   |
| bla-marka    | marka   | blå   | 200 min | Øvresetra   | nei   |

Startpunktet «Aaa uten turer» har ingen turer og skal ikke kunne velges.
"""

from dataclasses import replace

from domene.tur import Form, Tur, Turniva
from turforslag import turdata
from turforslag.models import Startpunkt

STARTPUNKTER = {
    "brate": ("Bråten", 59.95, 10.70, 200),
    "asen": ("Åsen", 59.96, 10.71, 210),
    "ovre": ("Øvresetra", 59.97, 10.72, 220),
}


def lag_tur(tur_id: str, startpunkt_id: str, **endringer) -> Tur:
    navn, lat, lon, hoyde = STARTPUNKTER[startpunkt_id]
    tur = Tur(
        id=tur_id,
        navn=f"Tur {tur_id}",
        startpunkt_id=startpunkt_id,
        startpunkt_navn=navn,
        startpunkt_lat=lat,
        startpunkt_lon=lon,
        startpunkt_hoyde_m=hoyde,
        form=Form.TUR_RETUR,
        turtyper=("marka",),
        lengde_m=1750,
        hoydemeter_m=60,
        nedstigning_m=5,
        hoydeprofil=((0, hoyde), (1750, hoyde + 60)),
        turniva=Turniva.GRONN,
        estimert_tid_min=120,
        ut_no_url="",
        kilde="turrutebasen",
        lisens="CC BY 4.0",
        geometry=((lon, lat), (lon + 0.01, lat + 0.01)),
    )
    return replace(tur, **endringer)


TURER = (
    lag_tur(
        "marka-lang",
        "brate",
        navn="Rundt Bråtenvann",
        form=Form.RUNDTUR,
        lengde_m=3500,
        hoydemeter_m=128,
        estimert_tid_min=170,
        ut_no_url="https://ut.no/turforslag/123",
    ),
    lag_tur("utsikt-kort", "asen", navn="Åsen utsikt", turtyper=("utsikt",), estimert_tid_min=140),
    lag_tur("topptur-lang", "asen", navn="Åstoppen", turtyper=("topptur",), estimert_tid_min=300),
    lag_tur("bla-marka", "ovre", navn="Øvresetra blå", turniva=Turniva.BLA, estimert_tid_min=200),
)


def lagre_testturer() -> None:
    turdata.lagre_turer(TURER)
    Startpunkt.objects.create(id="uten-turer", navn="Aaa uten turer", lat=60, lon=10, hoyde_m=1)
