"""URL-er bare for 500-testen: alle vanlige URL-er og én som kaster et unntak."""

from django.urls import path

from config.urls import urlpatterns as vanlige


def kast_unntak(request):
    raise RuntimeError("Testfeil for 500-siden")


urlpatterns = [*vanlige, path("feil/", kast_unntak)]
