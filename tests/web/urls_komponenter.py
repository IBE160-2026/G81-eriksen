"""URL-er bare for komponenttestene (UX-DR4, UX-DR21): alle vanlige URL-er og en testside.

Testsiden har en primærknapp, en sekundærknapp og Melding i alle fire typer og begge
modusene. Appen får ingen synlig komponentside. Malen ligger under `tests/web/maler/`
og lastes direkte, så malinnstillingene er uendret.
"""

from pathlib import Path

from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import engines
from django.urls import path

from config.urls import urlpatterns as vanlige

MAL = Path(__file__).resolve().parent / "maler" / "komponenter.html"


def komponenter(request):
    if request.method == "POST":
        return redirect(request.path)  # PRG
    mal = engines["django"].from_string(MAL.read_text(encoding="utf-8"))
    return HttpResponse(mal.render({}, request))


urlpatterns = [*vanlige, path("komponenter/", komponenter, name="komponenter")]
