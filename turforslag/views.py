"""Søk og Turforslag (FR-4, FR-5, FR-6, FR-7, AD-5).

Views regner, filtrerer og formaterer ingenting selv (AR-2). De validerer med `SokForm`,
kaller `sokflyt` og lagrer og henter søketilstanden med `okt`. Alle POST følger PRG.
"""

from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods, require_safe

from turforslag import okt, sokflyt
from turforslag.forms import SokForm

# Nøkkelen for meldingen «Turforslaget er ikke lenger tilgjengelig …» på Søk. Teksten står i malen.
FORSLAG_UTILGJENGELIG = "forslag-utilgjengelig"


@require_http_methods(["GET", "HEAD", "POST"])
def sok(request):  # FR-4, FR-5
    """Søk. GET viser skjemaet (forhåndsutfylt med `?sok=<id>`), POST søker og sender videre."""
    i_dag = timezone.localdate()
    startpunkter = sokflyt.startpunktvalg()
    utilgjengelig = False
    if request.method == "POST":
        skjema = SokForm(i_dag, startpunkter, data=request.POST)
        if skjema.is_valid():
            tilstand = sokflyt.utfor_sok(skjema.til_sok())
            sok_id = okt.lagre_sok(request, tilstand)
            return redirect("turforslag:forslag", sok_id=sok_id)
    else:
        sok_id = request.GET.get("sok")
        tidligere = okt.hent_sok(request, sok_id) if sok_id else None
        skjema = SokForm(i_dag, startpunkter, tilstand=tidligere)
        meldinger = [melding.message for melding in messages.get_messages(request)]
        utilgjengelig = FORSLAG_UTILGJENGELIG in meldinger
    return render(
        request, "turforslag/sok.html", {"skjema": skjema, "utilgjengelig": utilgjengelig}
    )


@require_safe
def forslag(request, sok_id):  # FR-6, FR-7
    """Turforslaget for søke-ID-en, uten ny rangering. Ukjent ID eller tur gir Søk."""
    tilstand = okt.hent_sok(request, sok_id)
    visning = sokflyt.forslagsvisning(tilstand) if tilstand else None
    if visning is None:
        messages.info(request, FORSLAG_UTILGJENGELIG)
        return redirect("turforslag:sok")
    return render(request, "turforslag/forslag.html", {"visning": visning, "sok_id": sok_id})
