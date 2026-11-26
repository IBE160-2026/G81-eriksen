"""Søk og Turforslag (FR-4, FR-5, FR-6, FR-7, AD-5).

Views regner, filtrerer og formaterer ingenting selv (AR-2). De validerer med `SokForm`,
kaller `sokflyt` og lagrer og henter søketilstanden med `okt`. Alle POST følger PRG.
«Nytt forslag» og «Start fra første forslag igjen» (1.11) er POST med CSRF som sender
videre til Turforslag. Med headeren `X-Fragment: 1` gir Turforslag bare innholdet i `<main>`,
som `forbedring.js` bytter inn uten sideinnlasting.
"""

from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.cache import patch_vary_headers
from django.views.decorators.http import require_http_methods, require_POST, require_safe

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
        return _utilgjengelig(request)
    mal = "turforslag/forslag.html"
    if request.headers.get("X-Fragment") == "1":  # 1.11: innholdet i <main> til forbedring.js
        mal = "turforslag/_forslag_innhold.html"
    svar = render(request, mal, {"visning": visning, "sok_id": sok_id})
    patch_vary_headers(svar, ["X-Fragment"])
    return svar


@require_POST
def nytt_forslag(request, sok_id):  # FR-7, NFR-2
    """«Nytt forslag»: neste tur i den frosne rangeringen. Skjult felt `tur` er turen som
    vises. Er den ikke gjeldende tur (dobbeltklikk, gammel fane), endres ingenting."""
    return _handling(request, sok_id, lambda t: sokflyt.nytt_forslag(t, request.POST.get("tur")))


@require_POST
def forfra(request, sok_id):  # FR-7
    """«Start fra første forslag igjen» ved «alle vist». Ellers endres ingenting."""
    return _handling(request, sok_id, sokflyt.forfra)


def _handling(request, sok_id, endring):  # FR-7, AD-5, PRG
    tilstand = okt.hent_sok(request, sok_id)
    if tilstand is None:
        return _utilgjengelig(request)
    ny = endring(tilstand)
    if ny != tilstand:
        okt.oppdater_sok(request, sok_id, ny)
    return redirect("turforslag:forslag", sok_id=sok_id)


def _utilgjengelig(request):  # FR-7, UX-DR21
    messages.info(request, FORSLAG_UTILGJENGELIG)
    return redirect("turforslag:sok")
