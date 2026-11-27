"""Sletting av konto og alt brukeren har registrert (FR-15, AR-9, NFR-5, NFR-8).

Bruker, innloggingsforsøk for e-posten og registreringer (CASCADE) slettes i én transaksjon.
Feiler noe, rulles alt tilbake.
"""

from django.db import transaction

from turforslag import innloggingsgrense


def slett_konto(bruker) -> None:
    """Sletter brukeren, registreringene og innloggingsforsøkene for e-posten."""
    epost = bruker.email
    with transaction.atomic():
        innloggingsgrense.slett_forsok(epost)
        bruker.delete()
