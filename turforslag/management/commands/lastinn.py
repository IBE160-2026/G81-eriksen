"""`python manage.py lastinn`: laster `data/turer.geojson` inn i databasen (AR-5, AD-3 punkt 4).

To trinn: `les_fil` leser og validerer hele fila i minnet via `domene.tur`, og først når
alt er i orden, lagrer `turforslag.turdata.lagre_turer` startpunkter og turer i én
transaksjon. Ved feil stopper kommandoen med en norsk melding, og databasen er uendret.
Kommandoen regner ingenting selv (AD-2) og sletter aldri noe. Mangler en tur som har
registreringer i fila, stopper den før noe lagres.
"""

import json
from pathlib import Path

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.db import DatabaseError, transaction
from django.utils import timezone

from domene import tur as domenetur
from turforslag import testbruker as testbrukermodul
from turforslag import turdata


def standard_fil() -> Path:
    return settings.BASE_DIR / "data" / "turer.geojson"


def standard_testbrukerfil() -> Path:
    return settings.BASE_DIR / "data" / "testbruker.toml"


def les_fil(sti: Path) -> list[domenetur.Tur]:  # AR-5
    """Leser og validerer hele turfila. Alle feil blir `CommandError` med norsk melding."""
    try:
        # utf-8-sig godtar også en fil med BOM.
        tekst = sti.read_text(encoding="utf-8-sig")
    except FileNotFoundError as feil:
        raise CommandError(f"Fant ikke turfila {sti}.") from feil
    except (OSError, UnicodeDecodeError) as feil:
        raise CommandError(f"Kunne ikke lese turfila {sti}: {feil}") from feil

    try:
        data = json.loads(tekst)
    except json.JSONDecodeError as feil:
        raise CommandError(
            f"Turfila {sti} er ikke gyldig JSON (linje {feil.lineno}, kolonne {feil.colno})."
        ) from feil

    if (
        not isinstance(data, dict)
        or data.get("type") != "FeatureCollection"
        or not isinstance(data.get("features"), list)
    ):
        raise CommandError(
            f"Turfila {sti} er ikke en GeoJSON-«FeatureCollection» med en liste «features»."
        )

    turer = []
    for nr, feature in enumerate(data["features"], start=1):
        tur_id = feature.get("id") if isinstance(feature, dict) else None
        try:
            turer.append(domenetur.Tur.fra_geojson_feature(feature))
        except KeyError as feil:
            raise CommandError(
                f"Turfila {sti}: tur nr. {nr} (tur-ID {tur_id!r}) mangler feltet {feil}."
            ) from feil
        except (ValueError, TypeError, AttributeError) as feil:
            raise CommandError(
                f"Turfila {sti}: tur nr. {nr} (tur-ID {tur_id!r}) er ugyldig: {feil}"
            ) from feil

    try:
        domenetur.valider_turer(turer)
    except ValueError as feil:
        raise CommandError(f"Turfila {sti}: {feil}") from feil
    return turer


class Command(BaseCommand):
    help = "Laster turene i data/turer.geojson inn i databasen (oppretter eller oppdaterer)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--fil",
            type=Path,
            default=None,
            help="Turfila som skal lastes inn. Standard er data/turer.geojson.",
        )
        parser.add_argument(
            "--testbruker",
            type=Path,
            nargs="?",
            const=True,
            default=None,
            help="Gjenskaper testbrukeren fra fila (standard data/testbruker.toml). Uten "
            "--fil gjøres det alltid; med --fil bare når dette er oppgitt.",
        )

    def handle(self, *args, **options):  # AR-5, FR-21
        sti = options["fil"] or standard_fil()
        turer = les_fil(sti)

        valg = options["testbruker"]
        if valg is None and options["fil"] is None:
            valg = True
        testbruker = None
        testbrukerfil = None
        if valg is not None:
            testbrukerfil = standard_testbrukerfil() if valg is True else valg
            try:
                testbruker = testbrukermodul.les_og_valider(
                    testbrukerfil, {tur.id for tur in turer}, timezone.localdate()
                )
            except testbrukermodul.TestbrukerFeil as feil:
                raise CommandError(f"{feil} Ingenting er endret.") from feil

        try:
            with transaction.atomic():
                if testbruker is not None:
                    # Slettes først, så registreringene hennes ikke hindrer at turer går ut.
                    testbrukermodul.slett(testbruker)
                mangler = turdata.mangler_med_registreringer(turer)
                if mangler:
                    raise CommandError(
                        f"Turfila {sti} mangler {', '.join(mangler)}, som har registreringer i "
                        "historikken. Ingenting er endret."
                    )
                lagret = turdata.lagre_turer(turer)
                if testbruker is not None:
                    testbrukermodul.opprett(testbruker, turer)
        except (DatabaseError, ValidationError) as feil:
            # Transaksjonen er rullet tilbake, så databasen er uendret.
            raise CommandError(
                f"Kunne ikke lagre turene fra {sti} i databasen. Ingenting er endret: {feil}"
            ) from feil

        if lagret.mangler_i_fila:
            self.stderr.write(
                self.style.WARNING(
                    f"Advarsel: {len(lagret.mangler_i_fila)} tur(er) i databasen finnes ikke i "
                    f"{sti} og er beholdt uendret: {', '.join(lagret.mangler_i_fila)}."
                )
            )
        self.stdout.write(
            self.style.SUCCESS(
                f"Lastet inn {len(turer)} turer ({lagret.nye_turer} nye, "
                f"{lagret.oppdaterte_turer} oppdaterte) og "
                f"{lagret.nye_startpunkter + lagret.oppdaterte_startpunkter} startpunkter "
                f"({lagret.nye_startpunkter} nye, {lagret.oppdaterte_startpunkter} oppdaterte) "
                f"fra {sti}."
            )
        )
        if testbruker is not None:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Gjenskapte testbrukeren {testbruker.epost} med "
                    f"{len(testbruker.registreringer)} registreringer fra {testbrukerfil}."
                )
            )
