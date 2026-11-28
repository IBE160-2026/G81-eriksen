"""Reservevarianten: gir den ferdige reserveteksten uendret tilbake (FR-13)."""

from domene.ki import KiSok, KiSvar, KiTur


class ReserveKi:
    def begrunnelse(
        self, sok: KiSok, tur: KiTur, reserve: str, *, topptur_erstattet: bool = False
    ) -> KiSvar:
        return KiSvar(tekst=reserve)
