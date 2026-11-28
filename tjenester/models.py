from django.db import models


class KiForbruk(models.Model):
    """Antall KI-kall per kalenderdøgn (Europe/Oslo), for døgngrensen (NFR-8)."""

    dato = models.DateField("dato", unique=True)
    antall = models.PositiveIntegerField("antall", default=0, db_default=0)

    class Meta:
        verbose_name = "KI-forbruk"
        verbose_name_plural = "KI-forbruk"

    def __str__(self) -> str:
        return f"{self.dato}: {self.antall}"
