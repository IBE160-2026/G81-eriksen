from django.urls import path

from turforslag import views

app_name = "turforslag"

urlpatterns = [
    path("", views.sok, name="sok"),
    path("forslag/<str:sok_id>/", views.forslag, name="forslag"),
]
