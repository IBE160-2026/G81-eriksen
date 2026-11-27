from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models.functions import Now
from django.utils import timezone

from domene import tur as domenetur


class BrukerManager(BaseUserManager):
    """Manager for `Bruker`, med e-post som brukernavn (AR-9, AD-7)."""

    use_in_migrations = True

    @classmethod
    def normalize_email(cls, email):
        # AD-7: hele e-postadressen lagres med små bokstaver.
        return (email or "").strip().lower()

    def get_by_natural_key(self, username):
        # AD-7: innlogging og createsuperuser finner brukeren uansett store og små bokstaver.
        return super().get_by_natural_key(self.normalize_email(username))

    def _lag_bruker(self, email, password, **ekstra):
        if not email:
            raise ValueError("Brukeren må ha en e-postadresse.")
        bruker = self.model(email=self.normalize_email(email), **ekstra)
        bruker.set_password(password)
        bruker.save(using=self._db)
        return bruker

    def create_user(self, email, password=None, **ekstra):
        ekstra.setdefault("is_staff", False)
        ekstra.setdefault("is_superuser", False)
        return self._lag_bruker(email, password, **ekstra)

    def create_superuser(self, email, password=None, **ekstra):
        ekstra.setdefault("is_staff", True)
        ekstra.setdefault("is_superuser", True)
        if ekstra.get("is_staff") is not True:
            raise ValueError("En superbruker må ha is_staff=True.")
        if ekstra.get("is_superuser") is not True:
            raise ValueError("En superbruker må ha is_superuser=True.")
        return self._lag_bruker(email, password, **ekstra)


class Bruker(AbstractUser):
    """Egen brukermodell fra første migrering (AR-9, AD-7)."""

    username = None
    first_name = None
    last_name = None
    email = models.EmailField("e-postadresse", unique=True)
    # Antall nivåhevinger brukeren har fått. Brukes av AD-11.
    brukt_heving = models.IntegerField(default=0, verbose_name="brukte nivåhevinger")

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = BrukerManager()

    class Meta:
        verbose_name = "bruker"
        verbose_name_plural = "brukere"

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        # AD-7: e-post med små bokstaver også når modellen lagres direkte.
        self.email = BrukerManager.normalize_email(self.email)
        super().save(*args, **kwargs)


class Startpunkt(models.Model):
    """Et startpunkt fra turdatabasen. ID-en er stabil og kommer fra kurateringslista (AR-6)."""

    id = models.CharField("startpunkt-ID", max_length=100, primary_key=True)
    navn = models.CharField("navn", max_length=200)
    lat = models.FloatField("breddegrad")
    lon = models.FloatField("lengdegrad")
    hoyde_m = models.IntegerField("høyde (m)")

    class Meta:
        verbose_name = "startpunkt"
        verbose_name_plural = "startpunkter"
        ordering = ["id"]

    def __str__(self):
        return self.navn


class Tur(models.Model):
    """En tur fra `data/turer.geojson`, lastet inn med `lastinn` (AD-3 punkt 4–5, AR-6).

    Feltene heter som i `domene.tur.Tur`. Nivå, høydemeter og tid lagres som de står i
    fila og regnes aldri på nytt i appen. Geometri, høydeprofil og turtyper er JSON, så
    modellen virker likt på SQLite og Postgres.
    """

    id = models.CharField("tur-ID", max_length=100, primary_key=True)
    navn = models.CharField("navn", max_length=200)
    startpunkt = models.ForeignKey(
        Startpunkt,
        on_delete=models.PROTECT,
        related_name="turer",
        verbose_name="startpunkt",
    )
    form = models.CharField(
        "form", max_length=20, choices=[(f.value, f.value) for f in domenetur.Form]
    )
    turtyper = models.JSONField("turtyper", default=list)
    lengde_m = models.PositiveIntegerField("lengde (m)")
    hoydemeter_m = models.PositiveIntegerField("høydemeter (m)")
    nedstigning_m = models.PositiveIntegerField("nedstigning (m)")
    hoydeprofil = models.JSONField("høydeprofil", default=list)
    turniva = models.CharField(
        "turnivå", max_length=20, choices=[(n.value, n.value) for n in domenetur.Turniva]
    )
    estimert_tid_min = models.PositiveIntegerField("estimert tid (min)")
    ut_no_url = models.CharField("ut.no-adresse", max_length=500, blank=True)
    kilde = models.CharField("kilde", max_length=100)
    lisens = models.CharField("lisens", max_length=100)
    geometry = models.JSONField("geometri")

    class Meta:
        verbose_name = "tur"
        verbose_name_plural = "turer"
        ordering = ["id"]

    def __str__(self):
        return self.navn


class Innloggingsforsok(models.Model):
    """Et mislykket innloggingsforsøk, også for e-poster uten konto (AR-9, NFR-8)."""

    epost = models.CharField("e-post", max_length=254)
    tidspunkt = models.DateTimeField("tidspunkt", default=timezone.now, db_default=Now())

    class Meta:
        verbose_name = "innloggingsforsøk"
        verbose_name_plural = "innloggingsforsøk"
        indexes = [models.Index(fields=["epost", "tidspunkt"], name="innloggingsforsok_epost_tid")]

    def __str__(self):
        return f"{self.epost} {self.tidspunkt:%Y-%m-%d %H:%M:%S}"
