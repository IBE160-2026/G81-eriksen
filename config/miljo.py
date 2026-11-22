"""Leser miljøverdiene for appen (AD-12 punkt 3, AD-15, NFR-1, NFR-10).

Miljøverdier leses bare i `config/`. `last_inn` tar inn `base_dir` og `environ`,
så testene kan kjøre uten å røre den ekte `.env`.
"""

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import parse_qsl, unquote, urlsplit

from django.core.exceptions import ImproperlyConfigured
from dotenv import dotenv_values

MELDING_MANGLER_ENV = (
    "Fant ikke .env med DJANGO_SECRET_KEY. Kopier .env.example til .env, "
    "og start appen på nytt (se README › Installasjon og kjøring)."
)

MELDING_VERCEL_MANGLER_NOKKEL = (
    "DJANGO_SECRET_KEY mangler eller er tom på Vercel. Legg inn en egen, tilfeldig nøkkel "
    "under Settings › Environment Variables i Vercel-prosjektet (AD-15 punkt 6)."
)

MELDING_VERCEL_UTVIKLINGSNOKKEL = (
    "DJANGO_SECRET_KEY på Vercel er lik utviklingsnøkkelen i .env.example. Legg inn en egen, "
    "tilfeldig nøkkel under Settings › Environment Variables i Vercel-prosjektet (AD-15 punkt 5)."
)

MELDING_VERCEL_MANGLER_DATABASE = (
    "DATABASE_URL mangler på Vercel. Koble Neon-databasen til prosjektet under "
    "Storage › Connect Project (AD-15 punkt 3)."
)

MELDING_UGYLDIG_DATABASE_URL = (
    "DATABASE_URL må være en Postgres-adresse som begynner med postgres:// eller postgresql://, "
    "med vert og databasenavn."
)

SANNE_VERDIER = {"1", "true", "yes", "on", "ja"}
POSTGRES_SKJEMAER = {"postgres", "postgresql"}


@dataclass(frozen=True)
class Miljo:
    secret_key: str
    debug: bool
    anthropic_api_key: str
    met_user_agent: str
    database_url: str
    vercel: bool


def _som_bool(verdi: str | None) -> bool:
    return (verdi or "").strip().lower() in SANNE_VERDIER


def _utviklingsnokkel(base_dir: Path) -> str | None:
    """Nøkkelen i `.env.example`, lest fra fila så den ikke står to steder."""
    eksempel = Path(base_dir) / ".env.example"
    if not eksempel.is_file():
        return None
    return dotenv_values(eksempel).get("DJANGO_SECRET_KEY") or None


def _sjekk_nokkel_pa_vercel(base_dir: Path, nokkel: str) -> None:
    """AD-15 punkt 5: nøkkelen må være satt og ulik utviklingsverdien.

    Fila `.env.example` finnes alltid under byggingen, der `migrate` laster settings,
    så en utviklingsnøkkel stopper byggingen før noe publiseres.
    """
    if not nokkel.strip():
        raise ImproperlyConfigured(MELDING_VERCEL_MANGLER_NOKKEL)
    utvikling = _utviklingsnokkel(base_dir)
    if utvikling is not None and nokkel.strip() == utvikling.strip():
        raise ImproperlyConfigured(MELDING_VERCEL_UTVIKLINGSNOKKEL)


def _velg_database_url(verdier: Mapping[str, str]) -> str:
    """AD-15 punkt 3: poolen under kjøring, den direkte adressen under bygging (`CI`)."""
    direkte = verdier.get("DATABASE_URL_UNPOOLED", "").strip()
    if _som_bool(verdier.get("CI")) and direkte:
        return direkte
    return verdier.get("DATABASE_URL", "").strip()


def database_fra_url(url: str) -> dict:
    """Bygger Djangos `DATABASES["default"]` fra en Postgres-URL (AD-4, AD-15 punkt 3).

    Tolkes med `urllib.parse`, uten egen pakke. Spørreparametrene (f.eks. `sslmode`)
    blir `OPTIONS`. `DISABLE_SERVER_SIDE_CURSORS` fordi Neons pool kjører i transaksjonsmodus.
    """
    try:
        deler = urlsplit(url.strip())
        port = deler.port
    except ValueError as feil:
        raise ImproperlyConfigured(MELDING_UGYLDIG_DATABASE_URL) from feil
    navn = unquote(deler.path.lstrip("/"))
    if deler.scheme not in POSTGRES_SKJEMAER or not deler.hostname or not navn:
        raise ImproperlyConfigured(MELDING_UGYLDIG_DATABASE_URL)
    return {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": navn,
        "USER": unquote(deler.username or ""),
        "PASSWORD": unquote(deler.password or ""),
        "HOST": deler.hostname,
        "PORT": str(port) if port is not None else "",
        "DISABLE_SERVER_SIDE_CURSORS": True,
        "OPTIONS": dict(parse_qsl(deler.query)),
    }


def last_inn(base_dir: Path, environ: Mapping[str, str]) -> Miljo:
    """Gir miljøverdiene, eller kaster `ImproperlyConfigured` med en norsk melding.

    Lokalt (`VERCEL` ikke satt) må `.env` finnes og ha en `DJANGO_SECRET_KEY`.
    Verdier i miljøet går foran verdier i `.env`, som med `load_dotenv`.
    Når `VERCEL` er satt, leses ingen `.env`. Nøkkelen må da være satt og ulik den i
    `.env.example`, og `DEBUG` er alltid av (AD-15 punkt 5).
    """
    vercel = bool(environ.get("VERCEL"))
    verdier: dict[str, str] = {}
    if not vercel:
        env_fil = Path(base_dir) / ".env"
        if not env_fil.is_file():
            raise ImproperlyConfigured(MELDING_MANGLER_ENV)
        verdier.update({k: v for k, v in dotenv_values(env_fil).items() if v is not None})
        verdier.update(environ)
        if not verdier.get("DJANGO_SECRET_KEY", "").strip():
            raise ImproperlyConfigured(MELDING_MANGLER_ENV)
    else:
        verdier.update(environ)
        _sjekk_nokkel_pa_vercel(base_dir, verdier.get("DJANGO_SECRET_KEY", ""))

    database_url = _velg_database_url(verdier)
    if vercel and not database_url:
        # SQLite på Vercel mister data mellom forespørsler (AD-15 Prevents).
        raise ImproperlyConfigured(MELDING_VERCEL_MANGLER_DATABASE)

    return Miljo(
        secret_key=verdier.get("DJANGO_SECRET_KEY", ""),
        debug=False if vercel else _som_bool(verdier.get("DEBUG")),
        anthropic_api_key=verdier.get("ANTHROPIC_API_KEY", ""),
        met_user_agent=verdier.get("MET_USER_AGENT", ""),
        database_url=database_url,
        vercel=vercel,
    )
