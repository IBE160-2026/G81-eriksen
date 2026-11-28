"""Søk og Turforslag (FR-4, FR-5, FR-6, FR-7, AD-5).

Views regner, filtrerer og formaterer ingenting selv (AR-2). De validerer med `SokForm`,
kaller `sokflyt` og lagrer og henter søketilstanden med `okt`. Alle POST følger PRG.
«Nytt forslag» og «Start fra første forslag igjen» (1.11) er POST med CSRF som sender
videre til Turforslag. Med headeren `X-Fragment: 1` gir Turforslag bare innholdet i `<main>`,
som `forbedring.js` bytter inn uten sideinnlasting.
"""

import logging
from urllib.parse import urlsplit

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import Resolver404, resolve, reverse
from django.utils import timezone
from django.utils.cache import patch_vary_headers
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods, require_POST, require_safe

from turforslag import (
    engangstoken,
    innloggingsgrense,
    kontosletting,
    okt,
    registrering,
    sokflyt,
)
from turforslag.forms import (
    FEIL_FOR_MANGE_FORSOK,
    FEIL_INNLOGGING,
    FEIL_KONTO_FINNES,
    LagKontoForm,
    LoggInnForm,
    RegistreringForm,
    SokForm,
)

# Nøkkelen for meldingen «Turforslaget er ikke lenger tilgjengelig …» på Søk. Teksten står i malen.
FORSLAG_UTILGJENGELIG = "forslag-utilgjengelig"
logger = logging.getLogger(__name__)
# Nøkkelen for «Du er logget ut.» på Søk (FR-14, AD-6). Teksten står i malen.
UTLOGGET = "utlogget"
# Nøkkelen for «Kontoen din er slettet.» på Søk (FR-15). Teksten står i malen.
SLETTET = "slettet"
# Nøkkelen for «Turen er registrert i historikken din.» på Historikk (FR-16). Teksten står i malen.
REGISTRERT = "registrert"


@require_http_methods(["GET", "HEAD", "POST"])
def sok(request):  # FR-4, FR-5
    """Søk. GET viser skjemaet (forhåndsutfylt med `?sok=<id>`), POST søker og sender videre."""
    i_dag = timezone.localdate()
    startpunkter = sokflyt.startpunktvalg()
    utilgjengelig = utloggetmelding = slettet = False
    if request.method == "POST":
        skjema = SokForm(i_dag, startpunkter, data=request.POST)
        if skjema.is_valid():
            tilstand = sokflyt.utfor_sok(skjema.til_sok(), request.user)
            sok_id = okt.lagre_sok(request, tilstand)
            return redirect("turforslag:forslag", sok_id=sok_id)
    else:
        sok_id = request.GET.get("sok")
        tidligere = okt.hent_sok(request, sok_id) if sok_id else None
        skjema = SokForm(i_dag, startpunkter, tilstand=tidligere, fokus=request.GET.get("fokus"))
        meldinger = [melding.message for melding in messages.get_messages(request)]
        utilgjengelig = FORSLAG_UTILGJENGELIG in meldinger
        utloggetmelding = UTLOGGET in meldinger
        slettet = SLETTET in meldinger
    return render(
        request,
        "turforslag/sok.html",
        {
            "skjema": skjema,
            "utilgjengelig": utilgjengelig,
            "utlogget": utloggetmelding,
            "slettet": slettet,
        },
    )


@require_safe
def forslag(request, sok_id):  # FR-6, FR-7
    """Turforslaget for søke-ID-en, uten ny rangering. Ukjent ID eller tur gir Søk."""
    tilstand = okt.hent_sok(request, sok_id)
    if tilstand is not None and request.method == "GET":  # FR-12: bare GET kan sende KI-kall
        ny = sokflyt.sikre_begrunnelse(tilstand, request.session)
        if ny != tilstand:
            # Tilstanden kan ha endret seg under KI-kallet: bare begrunnelsen skrives inn.
            fersk = okt.hent_sok(request, sok_id)
            if fersk is not None:
                tilstand = sokflyt.flett_begrunnelse(fersk, ny)
                okt.oppdater_sok(request, sok_id, tilstand)
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


@require_POST
def endre(request, sok_id):  # FR-8, NFR-2
    """Et endringsforslag fra Tilstandspanelet: søket kjøres på nytt med én endring og får en
    ny søke-ID. Ukjent søke-ID, felt eller verdi gir Søk. Svaret er alltid en redirect."""
    tilstand = okt.hent_sok(request, sok_id)
    if tilstand is None:
        return _utilgjengelig(request)
    felt, verdi = request.POST.get("felt"), request.POST.get("verdi")
    ny = (
        sokflyt.endre_sok(tilstand, felt, verdi, request.user)
        if felt is not None and verdi is not None
        else None
    )
    if ny is None:
        return _utilgjengelig(request)
    return redirect("turforslag:forslag", sok_id=okt.lagre_sok(request, ny))


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


def _neste(request) -> str:  # NFR-8, AR-8
    """`next` fra POST eller GET, bare når den peker til dette nettstedet. Ellers tom streng."""
    adresse = request.POST.get("next") or request.GET.get("next") or ""
    trygg = url_has_allowed_host_and_scheme(
        adresse, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    )
    return adresse if trygg else ""


def _etter_innlogging(request):  # FR-14, PRG
    return redirect(_neste(request) or "turforslag:sok")


def _krav_om_konto(request, neste: str) -> dict:  # FR-14, AD-6, AR-8, UX-DR26
    """Kontekst for «krev konto»-visningen når `neste` peker til en registreringsside for en
    kjent tur: Turoppsummering og, med et gyldig `sok`, «tatt vare på» og lenken tilbake.
    `sok` er en rå id og valideres mot økta; lenken bygges med `reverse`. Ellers tom."""
    if not neste:
        return {}
    try:
        funnet = resolve(urlsplit(neste).path)
    except Resolver404:
        return {}
    if funnet.view_name != "turforslag:registrer":
        return {}
    oppsummering = registrering.oppsummering(funnet.kwargs["tur_id"])
    if oppsummering is None:
        return {}
    sok_id = request.POST.get("sok") or request.GET.get("sok") or ""
    gyldig = bool(sok_id) and okt.hent_sok(request, sok_id) is not None
    return {
        "oppsummering": oppsummering,
        "sok_id": sok_id if gyldig else "",
        "tilbake_url": reverse("turforslag:forslag", kwargs={"sok_id": sok_id}) if gyldig else "",
    }


def _kontoside(request, mal, skjema, neste, **ekstra):
    return render(
        request,
        mal,
        {"skjema": skjema, "neste": neste, **_krav_om_konto(request, neste), **ekstra},
    )


@never_cache
@require_http_methods(["GET", "HEAD", "POST"])
def logg_inn(request):  # FR-14, AR-8, NFR-8
    """Logg inn. `login()` beholder økten, så gjestens turforslag er uendret (AR-7)."""
    if request.user.is_authenticated:
        return redirect("turforslag:sok")
    feil = False
    skjema = LoggInnForm()
    if request.method == "POST":
        skjema = LoggInnForm(request.POST)
        if skjema.is_valid():
            data = skjema.cleaned_data
            epost = data["epost"]
            na = timezone.now()
            if epost:
                innloggingsgrense.rydd_gamle(na)
                if innloggingsgrense.er_epost_sperret(epost, na):
                    feil = FEIL_FOR_MANGE_FORSOK
                    return _kontoside(
                        request, "turforslag/logg_inn.html", skjema, _neste(request), feil=feil
                    )
            bruker = authenticate(request, username=epost, password=data["passord"])
            if bruker is not None:
                innloggingsgrense.slett_forsok(epost)
                login(request, bruker)
                return _etter_innlogging(request)
            if epost:
                innloggingsgrense.lagre_forsok(epost, na)
        feil = FEIL_INNLOGGING
    return _kontoside(request, "turforslag/logg_inn.html", skjema, _neste(request), feil=feil)


@never_cache
@require_http_methods(["GET", "HEAD", "POST"])
def lag_konto(request):  # FR-14, AR-9
    """Lag konto og logg inn. Finnes e-posten, lages ingen konto."""
    if request.user.is_authenticated:
        return redirect("turforslag:sok")
    feil = False
    skjema = LagKontoForm()
    if request.method == "POST":
        skjema = LagKontoForm(request.POST)
        if skjema.is_valid():
            bruker = skjema.lag_bruker()
            if bruker is not None:
                login(request, bruker, backend="django.contrib.auth.backends.ModelBackend")
                return _etter_innlogging(request)
            feil = FEIL_KONTO_FINNES
    return _kontoside(request, "turforslag/lag_konto.html", skjema, _neste(request), feil=feil)


@login_required
@never_cache
@require_safe
def konto(request):  # NFR-5, UX-DR30
    return render(request, "turforslag/konto.html")


@require_POST
def logg_ut(request):  # FR-14, AD-6
    if not request.user.is_authenticated:
        return redirect("turforslag:sok")
    logout(request)
    messages.success(request, UTLOGGET)
    return redirect("turforslag:sok")


@never_cache
@require_http_methods(["GET", "HEAD", "POST"])
def slett_konto(request):  # FR-15, AR-9, NFR-5
    """Bekreftelse (GET) og sletting (POST). Gjest som sender POST (dobbeltklikk) går stille
    til Søk. Feiler slettingen, er alt rullet tilbake og siden vises på nytt med en feil."""
    if not request.user.is_authenticated:
        if request.method == "POST":
            return redirect("turforslag:sok")
        return redirect_to_login(request.get_full_path(), reverse("turforslag:logg_inn"))
    feil = False
    if request.method == "POST":
        try:
            kontosletting.slett_konto(request.user)
        except Exception:
            logger.exception("Kunne ikke slette konto")
            feil = True
        else:
            logout(request)
            messages.success(request, SLETTET)
            return redirect("turforslag:sok")
    return render(request, "turforslag/slett_konto.html", {"feil": feil})


@login_required
@never_cache
@require_http_methods(["GET", "HEAD", "POST"])
def registrer(request, tur_id):  # FR-16, AD-14, NFR-8
    """Registrer gjennomført tur. Tur-ID kommer fra URL-en, aldri fra økten (AR-7).

    GET lager et engangstoken som følger skjemaet. Første gyldige POST med tokenet lagrer og
    bruker det opp. Brukt eller ukjent token sender til Historikk uten å lagre. Ugyldig
    skjema beholder tokenet.
    """
    oppsummering = registrering.oppsummering(tur_id)
    if oppsummering is None:
        raise Http404
    i_dag = timezone.localdate()
    if request.method == "POST":
        token = request.POST.get("token", "")
        if not engangstoken.er_gyldig(request, token):
            return redirect("turforslag:historikk")
        skjema = RegistreringForm(i_dag, data=request.POST)
        if skjema.is_valid():
            if engangstoken.bruk(request, token):
                data = skjema.cleaned_data
                registrering.lagre(
                    request.user,
                    tur_id,
                    data["dato"],
                    data["brukt_tid_min"],
                    data["vanskelighet"],
                    data["fornoydhet"],
                )
                messages.success(request, REGISTRERT)
            return redirect("turforslag:historikk")
    else:
        skjema = RegistreringForm(i_dag)
        token = engangstoken.lag(request)
    return render(
        request,
        "turforslag/registrer.html",
        {"skjema": skjema, "oppsummering": oppsummering, "token": token, "i_dag": i_dag},
    )


@login_required
@never_cache
@require_safe
def historikk(request):  # FR-17, NFR-8
    """Historikk: brukerens egne registreringer, nyeste først."""
    meldinger = [melding.message for melding in messages.get_messages(request)]
    return render(
        request,
        "turforslag/historikk.html",
        {"rader": registrering.historikk(request.user), "registrert": REGISTRERT in meldinger},
    )


@login_required
@never_cache
@require_safe
def historikk_tur(request, registrering_id):  # FR-17, FR-7, NFR-8
    """Turen fra en av brukerens egne registreringer som turforslag. Rører ikke søketilstanden."""
    visning = registrering.historikkvisning(request.user, registrering_id)
    if visning is None:
        raise Http404
    return render(request, "turforslag/forslag.html", {"visning": visning})
