"""Logg over forkastede KI-svar, uten personopplysninger (FR-13, NFR-5, AD-10 punkt 8, AD-13).

Én linje per hendelse: `tidspunkt<TAB>kalltype<TAB>arsak<TAB>svar`. Lokalt skrives den til
`logs/ki.log` (rotert ved midnatt, filer eldre enn 30 dager slettes). Når `VERCEL` er satt, går
linjen til standard ut via rotloggeren.
"""

import logging
import re
import threading
from datetime import date, datetime, timedelta
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from zoneinfo import ZoneInfo

from django.conf import settings

from domene.ki import KALLTYPER, KI_FEILARSAKER
from domene.ki_validering import Forkastelse

OSLO = ZoneInfo("Europe/Oslo")
LOGGFIL = "ki.log"
BEHOLD_DAGER = 30

logger = logging.getLogger(__name__)
_lås = threading.Lock()

_ARSAKER = frozenset(KI_FEILARSAKER) | frozenset(str(f) for f in Forkastelse)
_NAVN = re.compile(r"ki\.log\.(\d{4}-\d{2}-\d{2})")
_LINJESKIFT = "\x0b\x0c\x1c\x1d\x1e\x85\u2028\u2029"


def _i_dag() -> date:
    return datetime.now(OSLO).date()


def filer_a_slette(filnavn, i_dag: date) -> list[str]:
    """Navnene som skal slettes: `ki.log.<dato>` med dato mer enn 30 dager før `i_dag`."""
    grense = i_dag - timedelta(days=BEHOLD_DAGER)
    resultat = []
    for navn in filnavn:
        treff = _NAVN.fullmatch(navn)
        if not treff:
            continue
        try:
            dato = date.fromisoformat(treff.group(1))
        except ValueError:
            continue
        if dato < grense:
            resultat.append(navn)
    return resultat


def _escape(tekst: str) -> str:
    tekst = tekst.replace("\\", "\\\\")
    for tegn in _LINJESKIFT:
        tekst = tekst.replace(tegn, "\\n")
    return tekst.replace("\r", "\\r").replace("\n", "\\n").replace("\t", "\\t")


def lag_linje(kalltype: str, arsak: str, svar: str | None) -> str:
    tid = datetime.now(OSLO).isoformat(timespec="seconds")
    return "\t".join([tid, kalltype, arsak, _escape(svar or "")])


class OpprydningsHandler(TimedRotatingFileHandler):
    """Roterer ved midnatt uten `backupCount`, og sletter egne filer eldre enn 30 dager."""

    def __init__(self, filnavn):
        super().__init__(filnavn, when="midnight", encoding="utf-8", delay=True)
        self.rydd()

    def rydd(self):
        mappe = Path(self.baseFilename).parent
        if not mappe.is_dir():
            return
        try:
            navn_i_mappen = [f.name for f in mappe.iterdir()]
        except OSError:
            return
        for navn in filer_a_slette(navn_i_mappen, _i_dag()):
            try:
                (mappe / navn).unlink()
            except OSError:
                pass

    def doRollover(self):
        super().doRollover()
        self.rydd()


def _sikre_handler() -> None:
    with _lås:
        if any(isinstance(h, OpprydningsHandler) for h in logger.handlers):
            return
        mappe = Path(settings.BASE_DIR) / "logs"
        mappe.mkdir(exist_ok=True)
        handler = OpprydningsHandler(mappe / LOGGFIL)
        handler.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)


def logg_forkastet(kalltype: str, arsak: str, svar: str | None) -> None:
    if kalltype not in KALLTYPER:
        raise ValueError(f"Ukjent kalltype: {kalltype!r}")
    if arsak not in _ARSAKER:
        raise ValueError(f"Ukjent årsak: {arsak!r}")
    if not settings.VERCEL:
        try:
            _sikre_handler()
        except OSError:
            return
    logger.info("%s", lag_linje(kalltype, arsak, svar))


def logg_totalgrense_nadd() -> None:
    """Én linje når døgnets totalgrense er nådd: `tidspunkt<TAB><TAB>totalgrense<TAB>`."""
    if not settings.VERCEL:
        try:
            _sikre_handler()
        except OSError:
            return
    tid = datetime.now(OSLO).isoformat(timespec="seconds")
    logger.info("%s", "\t".join([tid, "", "totalgrense", ""]))
