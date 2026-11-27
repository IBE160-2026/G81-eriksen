"""Testbrukeren fra `data/testbruker.toml` (FR-21, SM-4, AR-5, AD-11).

`les_og_valider` sjekker hele fila uten database. `slett` og `opprett` fjerner og gjenskaper
testbrukeren med registreringene, og setter `brukt_heving` så første søk viser hevingen.
`lastinn` kaller dem i samme transaksjon som turene.
"""

import re
import tomllib
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import transaction

from domene import tekst
from domene.niva import NivaStatus, vurder_historikk
from domene.niva import Registrering as DomeneRegistrering
from domene.tur import Tur, Turniva
from turforslag import kontosletting, registrering
from turforslag.models import Bruker

MIN_AR = 2000


class TestbrukerFeil(ValueError):
    """Ugyldig testbrukerfil. Meldingen er på norsk og sier hva som er feil."""

    __test__ = False


@dataclass(frozen=True)
class TestbrukerRegistrering:
    __test__ = False

    tur_id: str
    dato: date
    brukt_tid_min: int
    vanskelighet: str
    fornoydhet: int


@dataclass(frozen=True)
class Testbruker:
    __test__ = False

    epost: str
    passord: str
    registreringer: tuple[TestbrukerRegistrering, ...]


def _heltall(verdi) -> bool:
    return isinstance(verdi, int) and not isinstance(verdi, bool)


def _dato(verdi, feil) -> date:
    if isinstance(verdi, datetime):
        raise feil("«dato» må være en dato (ÅÅÅÅ-MM-DD), ikke et klokkeslett.")
    if isinstance(verdi, str):
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", verdi, re.ASCII):
            raise feil(f"«dato» {verdi!r} må være ÅÅÅÅ-MM-DD.")
        try:
            return date.fromisoformat(verdi)
        except ValueError:
            raise feil(f"«dato» {verdi!r} er ikke en gyldig dato.") from None
    if isinstance(verdi, date):
        return verdi
    raise feil("«dato» må være en dato (ÅÅÅÅ-MM-DD).")


def _registrering(nr: int, rad, tur_ider: set[str], i_dag: date) -> TestbrukerRegistrering:
    def feil(melding: str):
        return TestbrukerFeil(f"registrering nr. {nr}: {melding}")

    if not isinstance(rad, dict):
        raise feil("må være en tabell.")
    for felt in ("tur_id", "dato", "brukt_tid_min", "vanskelighet", "fornoydhet"):
        if felt not in rad:
            raise feil(f"mangler feltet «{felt}».")

    tur_id = rad["tur_id"]
    if not isinstance(tur_id, str) or tur_id not in tur_ider:
        raise feil(f"tur-ID {tur_id!r} finnes ikke blant turene som lastes inn.")

    dato = _dato(rad["dato"], feil)
    if dato.year < MIN_AR:
        raise feil(f"«dato» {dato.isoformat()} er for tidlig.")
    if dato > i_dag:
        raise feil(f"«dato» {dato.isoformat()} er frem i tid.")

    tid = rad["brukt_tid_min"]
    if not _heltall(tid) or not tekst.MIN_BRUKT_TID_MIN <= tid <= tekst.MAKS_BRUKT_TID_MIN:
        raise feil(
            f"«brukt_tid_min» må være et helt tall mellom {tekst.MIN_BRUKT_TID_MIN} og "
            f"{tekst.MAKS_BRUKT_TID_MIN}."
        )

    gyldige = [verdi for verdi, _ in tekst.vanskelighetsvalg()]
    if rad["vanskelighet"] not in gyldige:
        raise feil(f"«vanskelighet» må være en av {', '.join(gyldige)}.")

    fornoydhet = rad["fornoydhet"]
    if not _heltall(fornoydhet) or not tekst.MIN_FORNOYDHET <= fornoydhet <= tekst.MAKS_FORNOYDHET:
        raise feil(
            f"«fornoydhet» må være et helt tall mellom {tekst.MIN_FORNOYDHET} og "
            f"{tekst.MAKS_FORNOYDHET}."
        )
    return TestbrukerRegistrering(tur_id, dato, tid, rad["vanskelighet"], fornoydhet)


def les_og_valider(sti: Path, tur_ider: set[str], i_dag: date) -> Testbruker:  # AR-5, NFR-2
    """Leser og validerer hele fila. Alle feil blir `TestbrukerFeil`. Rører ikke databasen."""
    try:
        with open(sti, "rb") as fil:
            data = tomllib.load(fil)
    except FileNotFoundError:
        raise TestbrukerFeil(f"Fant ikke testbrukerfila {sti}.") from None
    except tomllib.TOMLDecodeError as feil:
        raise TestbrukerFeil(f"Testbrukerfila {sti} er ikke gyldig TOML: {feil}") from feil
    except (OSError, UnicodeDecodeError) as feil:
        raise TestbrukerFeil(f"Kunne ikke lese testbrukerfila {sti}: {feil}") from feil

    epost = data.get("epost")
    if not isinstance(epost, str) or not epost.strip():
        raise TestbrukerFeil(f"Testbrukerfila {sti}: «epost» mangler.")
    epost = Bruker.objects.normalize_email(epost)
    try:
        validate_email(epost)
    except ValidationError:
        raise TestbrukerFeil(f"Testbrukerfila {sti}: «epost» {epost!r} er ikke gyldig.") from None

    passord = data.get("passord")
    if not isinstance(passord, str) or not passord:
        raise TestbrukerFeil(f"Testbrukerfila {sti}: «passord» mangler.")
    try:
        validate_password(passord, user=Bruker(email=epost))
    except ValidationError as feil:
        raise TestbrukerFeil(
            f"Testbrukerfila {sti}: «passord» godtas ikke: {' '.join(feil.messages)}"
        ) from feil

    rader = data.get("registrering")
    if not isinstance(rader, list) or not rader:
        raise TestbrukerFeil(f"Testbrukerfila {sti}: minst én [[registrering]] kreves.")
    try:
        registreringer = tuple(
            _registrering(nr, rad, tur_ider, i_dag) for nr, rad in enumerate(rader, start=1)
        )
    except TestbrukerFeil as feil:
        raise TestbrukerFeil(f"Testbrukerfila {sti}: {feil}") from feil
    return Testbruker(epost, passord, registreringer)


def historikk(testbruker: Testbruker, turer: list[Tur]) -> NivaStatus:
    """Nivåstatusen fra registreringene i fila. Ren Python, uten database."""
    nivaer = {tur.id: Turniva(tur.turniva) for tur in turer}
    return vurder_historikk(
        tuple(
            DomeneRegistrering(
                id=nr,
                dato=r.dato,
                tur_id=r.tur_id,
                turniva=nivaer[r.tur_id],
                vanskelighet=r.vanskelighet,
                fornoydhet=r.fornoydhet,
            )
            for nr, r in enumerate(testbruker.registreringer, start=1)
        )
    )


def slett(testbruker: Testbruker) -> None:
    """Sletter testbrukeren med registreringer og innloggingsforsøk. Andre brukere røres ikke."""
    gammel = Bruker.objects.filter(email=testbruker.epost).first()
    if gammel is not None:
        kontosletting.slett_konto(gammel)


def opprett(testbruker: Testbruker, turer: list[Tur]) -> Bruker:  # AD-11
    """Oppretter testbrukeren (passord som hash) med registreringene. Turene må finnes."""
    status = historikk(testbruker, turer)
    with transaction.atomic():
        bruker = Bruker.objects.create_user(testbruker.epost, testbruker.passord)
        for r in testbruker.registreringer:
            registrering.lagre(
                bruker, r.tur_id, r.dato, r.brukt_tid_min, r.vanskelighet, str(r.fornoydhet)
            )
        bruker.brukt_heving = max(status.antall_hevinger - 1, 0)
        bruker.save(update_fields=["brukt_heving"])
    return bruker
