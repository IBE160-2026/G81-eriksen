"""Omslag som begrenser KI-kall per nettleser og per døgn (FR-13, NFR-8, AD-10 punkt 9)."""

from datetime import datetime
from zoneinfo import ZoneInfo

from django.conf import settings
from django.db import transaction
from django.db.models import F

from domene.ki import KiSok, KiSvar, KiTur
from domene.ki_grense import behold_siste_time, kan_sende_ki
from tjenester.ki.logg import logg_totalgrense_nadd
from tjenester.models import KiForbruk

OSLO = ZoneInfo("Europe/Oslo")
NOKKEL = "ki_kall"


def _les_okt(okt) -> list[datetime]:
    """Leser tidspunktene defensivt: ugyldig innhold gir tom liste."""
    try:
        rå = okt.get(NOKKEL, [])
        if not isinstance(rå, list):
            return []
        resultat = []
        for tekst in rå:
            try:
                tid = datetime.fromisoformat(tekst)
            except (TypeError, ValueError):
                continue
            if tid.tzinfo is None:
                continue
            resultat.append(tid)
        return resultat
    except Exception:  # noqa: BLE001 - skadet økt skal aldri velte kallet
        return []


class BegrensetKi:
    def __init__(self, indre, okt) -> None:
        self.indre = indre
        self.okt = okt

    def begrunnelse(self, sok: KiSok, tur: KiTur, reserve: str) -> KiSvar:
        na = datetime.now(OSLO)
        dato = na.date()
        tidspunkter = behold_siste_time(_les_okt(self.okt), na)
        try:
            nettleser_ok = kan_sende_ki(
                tidspunkter,
                0,
                na,
                settings.KI_MAKS_PER_NETTLESER_TIME,
                settings.KI_MAKS_PER_DOGN,
            )
            slapp_inn, ny_verdi = (False, 0)
            if nettleser_ok:
                slapp_inn, ny_verdi = self._reserver(dato)
        except Exception:  # noqa: BLE001 - feil i telling gir reserve, aldri unntak
            slapp_inn, ny_verdi = False, 0
        self.okt[NOKKEL] = [t.isoformat() for t in tidspunkter + ([na] if slapp_inn else [])]
        if not slapp_inn:
            return KiSvar(tekst=reserve)
        if ny_verdi == settings.KI_MAKS_PER_DOGN:
            logg_totalgrense_nadd()
        return self.indre.begrunnelse(sok, tur, reserve)

    @staticmethod
    def _reserver(dato) -> tuple[bool, int]:
        """Øker dagens teller atomisk hvis den er under døgngrensen."""
        maks = settings.KI_MAKS_PER_DOGN
        with transaction.atomic():
            rad, _ = KiForbruk.objects.get_or_create(dato=dato)
            traff = KiForbruk.objects.filter(pk=rad.pk, antall__lt=maks).update(
                antall=F("antall") + 1
            )
            if not traff:
                return False, 0
            return True, KiForbruk.objects.values_list("antall", flat=True).get(pk=rad.pk)
