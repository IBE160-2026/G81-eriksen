"""Søkeskjemaet, validert på serveren (FR-4, NFR-2).

Valglistene og datoene kommer fra `domene/`. Dagens dato sendes inn, så skjemaet aldri leser
klokka selv. Manipulerte verdier (ukjent turtype eller startpunkt, dato utenfor perioden,
varighet utenfor listen) gir feil ved feltet og krasjer aldri.
"""

import re
from datetime import date

from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from domene import tekst
from domene.okt import Soketilstand
from domene.sok import Sok
from turforslag.models import Bruker

# Feilmeldinger fra EXPERIENCE.md › Mikrotekst.
FEIL_VARIGHET = "Velg varighet"
FEIL_DATO = "Velg en dato fra i dag til {dato}"  # godkjent 2026-11-28, Mikrotekst
FEIL_TURTYPE = "Velg en turtype fra listen"  # godkjent 2026-11-28, Mikrotekst
FEIL_STARTPUNKT = "Velg et startpunkt fra listen"  # godkjent 2026-11-28, Mikrotekst

FELTREKKEFOLGE = ("varighet", "dato", "turtype", "startpunkt")

# Felt som kan få fokus via `?fokus=` (FR-8: «Velg startpunkt»). Andre verdier ignoreres.
FOKUSFELT = ("startpunkt",)


class SokForm(forms.Form):  # FR-4
    """Varighet, Dato, Turtype og Startpunkt. Tom turtype og tomt startpunkt betyr «alle»."""

    varighet = forms.ChoiceField()
    dato = forms.ChoiceField()
    turtype = forms.ChoiceField(required=False)
    startpunkt = forms.ChoiceField(required=False)

    def __init__(
        self,
        i_dag,
        startpunkter,
        *args,
        tilstand: Soketilstand | None = None,
        fokus: str | None = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.i_dag = i_dag
        self.fokus = fokus if fokus in FOKUSFELT else None
        datoer = tekst.datovalg(i_dag)
        startpunkt_ider = {startpunkt_id for startpunkt_id, _ in startpunkter}

        varighet = self.fields["varighet"]
        varighet.choices = [("", "Velg")] + [
            (str(minutter), navn) for minutter, navn in tekst.varighetsvalg()
        ]
        dato = self.fields["dato"]
        dato.choices = [(d.isoformat(), navn) for d, navn in datoer]
        self.fields["turtype"].choices = [("", "Alle turtyper"), *tekst.turtypevalg()]
        self.fields["startpunkt"].choices = [("", "Alle startpunkt"), *startpunkter]

        datofeil = FEIL_DATO.format(dato=tekst.siste_dato(i_dag))
        for navn, melding in (
            ("varighet", FEIL_VARIGHET),
            ("dato", datofeil),
            ("turtype", FEIL_TURTYPE),
            ("startpunkt", FEIL_STARTPUNKT),
        ):
            self.fields[navn].error_messages = {"required": melding, "invalid_choice": melding}

        # Første visning: i dag og «alle». Etter «Endre søk»: søket, når verdiene er gyldige.
        self.initial = {"varighet": "", "dato": i_dag.isoformat(), "turtype": "", "startpunkt": ""}
        if tilstand is not None:
            sok = tilstand.sok
            self.initial["varighet"] = str(sok.varighet_min)
            if any(d == sok.dato for d, _ in datoer):
                self.initial["dato"] = sok.dato.isoformat()
            self.initial["turtype"] = sok.turtype or ""
            if sok.startpunkt_id in startpunkt_ider:
                self.initial["startpunkt"] = sok.startpunkt_id

    def _valg(self, navn: str) -> list[tuple[str, str, bool]]:  # FR-4
        """(verdi, tekst, valgt) for feltet. Er ingen verdi valgt, er det første valget valgt."""
        verdi = self[navn].value()
        verdi = "" if verdi is None else str(verdi)
        valg = [(str(v), tekst_, str(v) == verdi) for v, tekst_ in self.fields[navn].choices]
        if not any(valgt for _, _, valgt in valg):
            valg[0] = (valg[0][0], valg[0][1], True)
        return valg

    @property
    def varighetsvalg(self):  # FR-4
        return self._valg("varighet")

    @property
    def datovalg(self):  # FR-4
        return self._valg("dato")

    @property
    def turtypevalg(self):  # FR-4
        return self._valg("turtype")

    @property
    def startpunktvalg(self):  # FR-4
        return self._valg("startpunkt")

    @property
    def forste_feil(self) -> str | None:  # FR-4: fokus til første felt med feil, eller `?fokus=`
        if not self.is_bound:
            return self.fokus
        return next((navn for navn in FELTREKKEFOLGE if navn in self.errors), None)

    def til_sok(self) -> Sok:  # FR-5
        """Søket fra et gyldig skjema."""
        data = self.cleaned_data
        return Sok(
            varighet_min=int(data["varighet"]),
            dato=next(d for d in tekst.datoperiode(self.i_dag) if d.isoformat() == data["dato"]),
            turtype=data["turtype"] or None,
            startpunkt_id=data["startpunkt"] or None,
        )


# Konto (FR-14). Tekstene er fra EXPERIENCE.md › Mikrotekst.
FEIL_INNLOGGING = "Feil e-post eller passord"
FEIL_FOR_MANGE_FORSOK = (  # NFR-8, godkjent 2026-11-28, Mikrotekst
    "Det har vært for mange forsøk på å logge inn med denne e-postadressen. "
    "Vent 15 minutter, og prøv igjen."
)
FEIL_KONTO_FINNES = "Kunne ikke lage konto – prøv å logge inn"
FEIL_EPOST_MANGLER = "Skriv inn e-postadressen din"  # godkjent 2026-11-28, Mikrotekst
FEIL_EPOST_UGYLDIG = "E-postadressen må ha med @, for eksempel ola@eksempel.no"
FEIL_PASSORD = "Passordet må ha minst 8 tegn"  # godkjent 2026-11-28, Mikrotekst
FEIL_PASSORD_LANGT = "Passordet kan ha høyst 128 tegn"  # godkjent 2026-11-28, Mikrotekst


class LoggInnForm(forms.Form):  # FR-14
    """E-post og passord. Ingen feltfeil: all feil er «Feil e-post eller passord»."""

    epost = forms.CharField(required=False, max_length=254)
    passord = forms.CharField(required=False, strip=False, max_length=128)

    def clean_epost(self):
        return Bruker.objects.normalize_email(self.cleaned_data["epost"])


class LagKontoForm(forms.Form):  # FR-14, AR-9
    """E-post og passord (minst 8 tegn). E-posten trimmes og lagres med små bokstaver."""

    epost = forms.EmailField(
        max_length=254,
        error_messages={"required": FEIL_EPOST_MANGLER, "invalid": FEIL_EPOST_UGYLDIG},
    )
    passord = forms.CharField(
        strip=False,
        max_length=128,
        error_messages={"required": FEIL_PASSORD, "max_length": FEIL_PASSORD_LANGT},
    )

    def clean_epost(self):
        return Bruker.objects.normalize_email(self.cleaned_data["epost"])

    def clean_passord(self):
        passord = self.cleaned_data["passord"]
        try:
            validate_password(passord)
        except ValidationError:
            raise ValidationError(FEIL_PASSORD) from None
        return passord

    def lag_bruker(self) -> Bruker | None:
        """Lager kontoen, eller None når e-posten finnes fra før (ingen konto lages)."""
        data = self.cleaned_data
        if Bruker.objects.filter(email=data["epost"]).exists():
            return None
        try:
            with transaction.atomic():
                return Bruker.objects.create_user(data["epost"], data["passord"])
        except IntegrityError:  # to samtidige forsøk med samme e-post
            return None


# Registrer gjennomført tur (FR-16). Tekstene er fra EXPERIENCE.md › Mikrotekst.
FEIL_REG_DATO = "Velg datoen du gikk turen"  # godkjent 2026-11-28, Mikrotekst
FEIL_REG_DATO_FREMTID = "Datoen kan ikke være frem i tid"  # godkjent 2026-11-28, Mikrotekst
FEIL_REG_TID = "Brukt tid må være mellom 10 minutter og 24 timer"  # godkjent 2026-11-28, Mikrotekst
FEIL_REG_VANSKELIGHET = "Velg hvor vanskelig turen føltes"  # godkjent 2026-11-28, Mikrotekst
FEIL_REG_FORNOYDHET = "Velg hvor fornøyd du var"  # godkjent 2026-11-28, Mikrotekst

MIN_REG_AR = 1900
REG_FELTREKKEFOLGE = ("dato", "timer", "minutter", "vanskelighet", "fornoydhet")


def _heltall(verdi: str) -> int | None:
    """Et heltall fra siffer (ASCII), ellers `None`. Svært lange verdier gir `None`."""
    verdi = verdi.strip()
    if verdi.isascii() and verdi.isdigit() and len(verdi) <= 6:
        return int(verdi)
    return None


class RegistreringForm(forms.Form):  # FR-16
    """Dato, brukt tid (timer og minutter), opplevd vanskelighet og fornøydhet. Alle er påkrevd.

    Dagens dato sendes inn, så skjemaet aldri leser klokka selv. Feil i brukt tid står på
    Timer, eller på Minutter når det feltet er ugyldig for seg selv.
    """

    dato = forms.CharField(required=False)
    timer = forms.CharField(required=False)
    minutter = forms.CharField(required=False)
    vanskelighet = forms.ChoiceField(required=False)
    fornoydhet = forms.ChoiceField(required=False)

    def __init__(self, i_dag, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.i_dag = i_dag
        self.fields["vanskelighet"].choices = tekst.vanskelighetsvalg()
        self.fields["fornoydhet"].choices = tekst.fornoydhetsvalg()
        self.initial = {"dato": i_dag.isoformat()}

    def clean(self):
        data = super().clean()
        self._rens_dato(data)
        self._rens_tid(data)
        for felt, melding in (
            ("vanskelighet", FEIL_REG_VANSKELIGHET),
            ("fornoydhet", FEIL_REG_FORNOYDHET),
        ):
            if not data.get(felt):
                self.errors.pop(felt, None)
                self.add_error(felt, melding)
        return data

    def _rens_dato(self, data):
        verdi = (data.get("dato") or "").strip()
        try:
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", verdi, re.ASCII):
                raise ValueError(verdi)
            dato = date.fromisoformat(verdi)
            if dato.year < MIN_REG_AR:
                raise ValueError(verdi)
        except ValueError:
            self.add_error("dato", FEIL_REG_DATO)
            return
        if dato > self.i_dag:
            self.add_error("dato", FEIL_REG_DATO_FREMTID)
        else:
            data["dato"] = dato

    def _rens_tid(self, data):
        timer_tekst = (data.get("timer") or "").strip()
        minutter_tekst = (data.get("minutter") or "").strip()
        if not timer_tekst and not minutter_tekst:
            self.add_error("timer", FEIL_REG_TID)
            return
        timer = _heltall(timer_tekst) if timer_tekst else 0
        minutter = _heltall(minutter_tekst) if minutter_tekst else 0
        if timer is None:
            self.add_error("timer", FEIL_REG_TID)
        elif minutter is None:
            self.add_error("minutter", FEIL_REG_TID)
        elif not tekst.MIN_BRUKT_TID_MIN <= timer * 60 + minutter <= tekst.MAKS_BRUKT_TID_MIN:
            self.add_error("timer", FEIL_REG_TID)
        else:
            data["brukt_tid_min"] = timer * 60 + minutter

    @property
    def dato_verdi(self) -> str:  # FR-16: i dag er forvalgt, og det som ble sendt, beholdes
        return self["dato"].value() or ""

    @property
    def tid_feil(self) -> str | None:  # FR-16: én feil for Brukt tid, under fieldset
        for navn in ("timer", "minutter"):
            if navn in self.errors:
                return self.errors[navn][0]
        return None

    def _valg(self, navn: str) -> list[tuple[str, str, bool]]:  # FR-16
        verdi = self[navn].value()
        verdi = "" if verdi is None else str(verdi)
        return [(v, tekst_, v == verdi) for v, tekst_ in self.fields[navn].choices]

    @property
    def vanskelighetsvalg(self):  # FR-16
        return self._valg("vanskelighet")

    @property
    def fornoydhetsvalg(self):  # FR-16
        return self._valg("fornoydhet")

    @property
    def forste_feil(self) -> str | None:  # FR-16: fokus til første felt med feil
        if not self.is_bound:
            return None
        return next((navn for navn in REG_FELTREKKEFOLGE if navn in self.errors), None)
