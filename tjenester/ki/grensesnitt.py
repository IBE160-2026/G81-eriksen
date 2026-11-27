"""Ett grensesnitt for KI med tre varianter: ekte, reserve og falsk (AR-12, AR-15, AR-16)."""

from typing import Protocol

from django.conf import settings

from domene.ki import KiSok, KiSvar, KiTur
from tjenester.ki.reserve import ReserveKi


class Ki(Protocol):
    def begrunnelse(self, sok: KiSok, tur: KiTur, reserve: str) -> KiSvar:
        """Kall B. `reserve` er ferdig reservetekst. Kaster aldri."""
        ...


def hent_ki(tving_reserve: bool = False) -> Ki:  # FR-13
    """Reserve uten nøkkel (mangler, tom eller bare mellomrom) eller når `tving_reserve`."""
    nokkel = (getattr(settings, "ANTHROPIC_API_KEY", None) or "").strip()
    if tving_reserve or not nokkel:
        return ReserveKi()
    try:
        from tjenester.ki.ekte import EkteKi

        return EkteKi(nokkel)
    except Exception:  # noqa: BLE001 - KI-feil når aldri viewet
        return ReserveKi()
