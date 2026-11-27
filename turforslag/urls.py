from django.urls import path

from turforslag import views

app_name = "turforslag"

urlpatterns = [
    path("", views.sok, name="sok"),
    path("forslag/<str:sok_id>/", views.forslag, name="forslag"),
    path("forslag/<str:sok_id>/nytt/", views.nytt_forslag, name="nytt_forslag"),
    path("forslag/<str:sok_id>/forfra/", views.forfra, name="forfra"),
    path("forslag/<str:sok_id>/endre/", views.endre, name="endre"),
    path("logg-inn/", views.logg_inn, name="logg_inn"),
    path("lag-konto/", views.lag_konto, name="lag_konto"),
    path("konto/", views.konto, name="konto"),
    path("logg-ut/", views.logg_ut, name="logg_ut"),
]
