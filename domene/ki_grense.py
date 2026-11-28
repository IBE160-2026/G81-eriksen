"""Grensen for KI-kall per nettleser og per døgn (FR-13, NFR-8, AD-10 punkt 9).

Ren avgjørelse uten database: tidspunktene og klokkeslettet kommer inn utenfra.
"""

from collections.abc import Iterable
from datetime import datetime, timedelta


def behold_siste_time(tidspunkter: Iterable[datetime], na: datetime) -> list[datetime]:
    """Tidspunktene som er strengt nyere enn `na − 60 min`. Tidspunkter etter `na` forkastes."""
    grense = na - timedelta(minutes=60)
    return [t for t in tidspunkter if grense < t <= na]


def kan_sende_ki(
    tidspunkter: Iterable[datetime],
    antall_i_dag: int,
    na: datetime,
    maks_per_nettleser_time: int,
    maks_per_dogn: int,
) -> bool:
    """Sant når siste time er under nettlesergrensen og dagens antall er under døgngrensen."""
    siste_time = len(behold_siste_time(tidspunkter, na))
    return siste_time < maks_per_nettleser_time and antall_i_dag < maks_per_dogn
