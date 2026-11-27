"""Lagring og sletting av mislykkede innloggingsforsøk (AR-9, NFR-8, NFR-5).

Avgjørelsen ligger i `domene.innlogging`. Her er bare databasen.
"""

from datetime import timedelta

from django.conf import settings

from domene.innlogging import er_sperret
from turforslag.models import Innloggingsforsok


def rydd_gamle(na) -> None:
    """Sletter alle forsøk eldre enn sperretiden, for alle e-poster (NFR-5)."""
    grense = na - timedelta(minutes=settings.INNLOGGING_SPERRETID_MIN)
    Innloggingsforsok.objects.filter(tidspunkt__lte=grense).delete()


def er_epost_sperret(epost: str, na) -> bool:
    tidspunkter = Innloggingsforsok.objects.filter(epost=epost).values_list("tidspunkt", flat=True)
    return er_sperret(
        tidspunkter, na, settings.INNLOGGING_MAKS_FORSOK, settings.INNLOGGING_SPERRETID_MIN
    )


def lagre_forsok(epost: str, na) -> None:
    Innloggingsforsok.objects.create(epost=epost, tidspunkt=na)


def slett_forsok(epost: str) -> None:
    Innloggingsforsok.objects.filter(epost=epost).delete()
