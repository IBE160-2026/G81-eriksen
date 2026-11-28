"""KI-tjenesten: `hent_ki()` gir ekte, reserve eller falsk variant (AD-10)."""

from tjenester.ki.grensesnitt import Ki, hent_ki
from tjenester.ki.logg import logg_forkastet

__all__ = ["Ki", "hent_ki", "logg_forkastet"]
