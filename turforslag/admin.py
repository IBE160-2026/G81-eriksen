from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import AdminUserCreationForm, UserChangeForm

from turforslag.models import Bruker


class BrukerOpprettSkjema(AdminUserCreationForm):
    class Meta:
        model = Bruker
        fields = ("email",)


class BrukerEndreSkjema(UserChangeForm):
    class Meta:
        model = Bruker
        fields = "__all__"


@admin.register(Bruker)
class BrukerAdmin(UserAdmin):
    """Admin for `Bruker` uten brukernavn, fornavn og etternavn (AR-9)."""

    form = BrukerEndreSkjema
    add_form = BrukerOpprettSkjema
    ordering = ("email",)
    list_display = ("email", "is_staff", "is_active", "brukt_heving")
    search_fields = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Tilganger",
            {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")},
        ),
        ("Nivå", {"fields": ("brukt_heving",)}),
        ("Datoer", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "usable_password", "password1", "password2"),
            },
        ),
    )
