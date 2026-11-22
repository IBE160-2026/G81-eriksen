"""Leser miljøverdiene for appen (AD-12 punkt 3, NFR-1).

Miljøverdier leses bare i `config/`. `last_inn` tar inn `base_dir` og `environ`,
så testene kan kjøre uten å røre den ekte `.env`.
"""

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured
from dotenv import dotenv_values

MELDING_MANGLER_ENV = (
    "Fant ikke .env med DJANGO_SECRET_KEY. Kopier .env.example til .env, "
    "og start appen på nytt (se README › Installasjon og kjøring)."
)

SANNE_VERDIER = {"1", "true", "yes", "on", "ja"}


@dataclass(frozen=True)
class Miljo:
    secret_key: str
    debug: bool
    anthropic_api_key: str
    met_user_agent: str


def _som_bool(verdi: str | None) -> bool:
    return (verdi or "").strip().lower() in SANNE_VERDIER


def last_inn(base_dir: Path, environ: Mapping[str, str]) -> Miljo:
    """Gir miljøverdiene, eller kaster `ImproperlyConfigured` med en norsk melding.

    Lokalt (`VERCEL` ikke satt) må `.env` finnes og ha en `DJANGO_SECRET_KEY`.
    Verdier i miljøet går foran verdier i `.env`, som med `load_dotenv`.
    Når `VERCEL` er satt, leses ingen `.env` (AD-15 punkt 5, sjekken kommer i story 1.2).
    """
    verdier: dict[str, str] = {}
    if not environ.get("VERCEL"):
        env_fil = Path(base_dir) / ".env"
        if not env_fil.is_file():
            raise ImproperlyConfigured(MELDING_MANGLER_ENV)
        verdier.update({k: v for k, v in dotenv_values(env_fil).items() if v is not None})
        verdier.update(environ)
        if not verdier.get("DJANGO_SECRET_KEY", "").strip():
            raise ImproperlyConfigured(MELDING_MANGLER_ENV)
    else:
        verdier.update(environ)

    return Miljo(
        secret_key=verdier.get("DJANGO_SECRET_KEY", ""),
        debug=_som_bool(verdier.get("DEBUG")),
        anthropic_api_key=verdier.get("ANTHROPIC_API_KEY", ""),
        met_user_agent=verdier.get("MET_USER_AGENT", ""),
    )
