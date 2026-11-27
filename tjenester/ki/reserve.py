"""Reservevarianten: gir den ferdige reserveteksten uendret tilbake (FR-13)."""

from domene.ki import KiSok, KiSvar, KiTur


class ReserveKi:
    def begrunnelse(self, sok: KiSok, tur: KiTur, reserve: str) -> KiSvar:
        return KiSvar(tekst=reserve)
