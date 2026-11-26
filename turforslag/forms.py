"""Søkeskjemaet, validert på serveren (FR-4, NFR-2).

Valglistene og datoene kommer fra `domene/`. Dagens dato sendes inn, så skjemaet aldri leser
klokka selv. Manipulerte verdier (ukjent turtype eller startpunkt, dato utenfor perioden,
varighet utenfor listen) gir feil ved feltet og krasjer aldri.
"""

from django import forms

from domene import tekst
from domene.okt import Soketilstand
from domene.sok import Sok

# Feilmeldinger fra EXPERIENCE.md › Mikrotekst.
FEIL_VARIGHET = "Velg varighet"
FEIL_DATO = "Velg en dato fra i dag til {dato}"  # [ASSUMPTION] Mikrotekst
FEIL_TURTYPE = "Velg en turtype fra listen"  # [ASSUMPTION] Mikrotekst
FEIL_STARTPUNKT = "Velg et startpunkt fra listen"  # [ASSUMPTION] Mikrotekst

FELTREKKEFOLGE = ("varighet", "dato", "turtype", "startpunkt")


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
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.i_dag = i_dag
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
    def forste_feil(self) -> str | None:  # FR-4: fokus til første felt med feil
        if not self.is_bound:
            return None
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
