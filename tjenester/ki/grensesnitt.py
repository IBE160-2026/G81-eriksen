"""Ett grensesnitt for KI med tre varianter: ekte, reserve og falsk (AR-12, AR-15, AR-16)."""

from typing import Protocol

from django.conf import settings

from domene.ki import KiSok, KiSvar, KiTur
from tjenester.ki.reserve import ReserveKi


class Ki(Protocol):
    def begrunnelse(self, sok: KiSok, tur: KiTur, reserve: str) -> KiSvar:
        """Kall B. `reserve` er ferdig reservetekst. Kaster aldri."""
        ...


def hent_ki(tving_reserve: bool = False, okt=None) -> Ki:  # FR-13
    """Reserve uten nøkkel (mangler, tom eller bare mellomrom), ved `tving_reserve` eller uten `okt`

    Med nøkkel og `okt` pakkes den ekte varianten i `BegrensetKi` (grense per nettleser og døgn).
    """
    nokkel = (getattr(settings, "ANTHROPIC_API_KEY", None) or "").strip()
    if tving_reserve or not nokkel or okt is None:
        return ReserveKi()
    try:
        from tjenester.ki.ekte import EkteKi
        from tjenester.ki.grense import BegrensetKi

        return BegrensetKi(EkteKi(nokkel), okt)
    except Exception:  # noqa: BLE001 - KI-feil når aldri viewet
        return ReserveKi()
