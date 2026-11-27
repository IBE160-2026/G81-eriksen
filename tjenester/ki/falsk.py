"""Den falske varianten for tester: testen bestemmer svaret og leser inndata (AR-15)."""

from domene.ki import ARSAK_FEIL, ARSAK_TIDSAVBRUDD, KiSok, KiSvar, KiTur


class FalskKi:
    def __init__(self, svar: KiSvar | str = "") -> None:
        self.svar = KiSvar(tekst=svar) if isinstance(svar, str) else svar
        self.kall: list[tuple[KiSok, KiTur, str]] = []

    @classmethod
    def tidsavbrudd(cls) -> "FalskKi":
        return cls(KiSvar(arsak=ARSAK_TIDSAVBRUDD))

    @classmethod
    def feil(cls) -> "FalskKi":
        return cls(KiSvar(arsak=ARSAK_FEIL))

    @property
    def antall_kall(self) -> int:
        return len(self.kall)

    def begrunnelse(self, sok: KiSok, tur: KiTur, reserve: str) -> KiSvar:
        self.kall.append((sok, tur, reserve))
        return self.svar
