"""Grensen for mislykkede innloggingsforsøk (AR-2, AR-9, NFR-8).

Ren avgjørelse uten database: tidspunktene og klokkeslettet kommer inn utenfra.
"""

from collections.abc import Iterable
from datetime import datetime, timedelta


def er_sperret(
    tidspunkter: Iterable[datetime], na: datetime, maks_forsok: int, sperretid_min: int
) -> bool:
    """Sant når minst `maks_forsok` tidspunkter er strengt nyere enn `na − sperretid_min`."""
    grense = na - timedelta(minutes=sperretid_min)
    return sum(1 for tidspunkt in tidspunkter if tidspunkt > grense) >= maks_forsok
