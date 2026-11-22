from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


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
