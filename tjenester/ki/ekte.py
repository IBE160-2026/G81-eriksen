"""Den ekte varianten (Anthropic). Bare her importeres `anthropic` (AR-12, AD-10)."""

import anthropic

from domene.ki import ARSAK_FEIL, ARSAK_TIDSAVBRUDD, ARSAK_UGYLDIG, KiSok, KiSvar, KiTur
from tjenester.ki.prompt import SYSTEMPROMPT, lag_bruker_melding

MODELL = "claude-haiku-5-5"
TIMEOUT_SEKUNDER = 5.0
MAKS_TOKENS = 400


class EkteKi:
    def __init__(self, api_key: str, http_client=None) -> None:
        self.klient = anthropic.Anthropic(
            api_key=api_key,
            timeout=TIMEOUT_SEKUNDER,
            max_retries=0,
            http_client=http_client,
        )

    def begrunnelse(
        self, sok: KiSok, tur: KiTur, reserve: str, *, topptur_erstattet: bool = False
    ) -> KiSvar:
        prompt = lag_bruker_melding(sok, tur, topptur_erstattet)
        try:
            svar = self.klient.messages.create(
                model=MODELL,
                max_tokens=MAKS_TOKENS,
                system=SYSTEMPROMPT,
                messages=[{"role": "user", "content": prompt}],
                # Uten dette bruker modellen tokens på tenkeblokker (målt: tomme eller avkuttede
                # svar og engelsk resonnement i teksten), og kallet nærmer seg tidsgrensen.
                thinking={"type": "disabled"},
                output_config={"effort": "low"},
            )
        except anthropic.APITimeoutError:
            return KiSvar(arsak=ARSAK_TIDSAVBRUDD)
        except Exception:  # noqa: BLE001 - KI-feil når aldri viewet
            return KiSvar(arsak=ARSAK_FEIL)
        try:
            tekst = "".join(b.text for b in svar.content if getattr(b, "type", None) == "text")
        except Exception:  # noqa: BLE001
            return KiSvar(arsak=ARSAK_UGYLDIG)
        if not tekst.strip():
            return KiSvar(arsak=ARSAK_UGYLDIG)
        return KiSvar(tekst=tekst.strip())
