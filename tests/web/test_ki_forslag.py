"""Turforslaget ber alltid om reservevarianten til story 4.5 (FR-13, NFR-5)."""

from datetime import date
from unittest import mock

from django.test import TestCase, override_settings

from domene.begrunnelse import personaliseringssetning, reservebegrunnelse
from domene.ki import KiSok, KiSvar, KiTur
from domene.sok import Sok
from tests.web.testturer import lagre_testturer
from tjenester.ki.falsk import FalskKi
from turforslag import sokflyt, turdata


class KiForslagTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        lagre_testturer()

    def tilstand(self):
        sok = Sok(varighet_min=180, dato=date(2026, 11, 28))
        return sokflyt.utfor_sok(sok)

    def visning(self, falsk):
        with mock.patch("turforslag.sokflyt.hent_ki", return_value=falsk) as hent:
            visning = sokflyt.forslagsvisning(self.tilstand())
        return hent, visning

    def forventet(self):
        t = self.tilstand()
        tur = turdata.hent_tur(t.gjeldende_tur_id)
        tekst = reservebegrunnelse(t.sok, tur)
        setning = personaliseringssetning(tur.turniva, t.nivatak, t.nivaheving, t.sperre)
        return t, tur, f"{tekst} {setning}" if setning else tekst

    @override_settings(ANTHROPIC_API_KEY="sk-test")
    def test_tvinger_reserve_og_sender_bare_ki_data(self):
        falsk = FalskKi()
        hent, visning = self.visning(_Reserve(falsk))
        hent.assert_called_once_with(tving_reserve=True)
        t, tur, forventet = self.forventet()
        self.assertEqual(visning.tur.begrunnelse, forventet)
        sok, ki_tur, reserve = falsk.kall[0]
        self.assertEqual(sok, KiSok(180, date(2026, 11, 28), None, None))
        self.assertEqual(ki_tur, KiTur(tur.id, tur.navn, tur.turtyper, tur.form.value))
        self.assertEqual(reserve, reservebegrunnelse(t.sok, tur))

    def test_feilresultat_gir_reservetekst(self):
        for falsk in (FalskKi.feil(), FalskKi.tidsavbrudd(), FalskKi("")):
            with self.subTest(svar=falsk.svar):
                _, visning = self.visning(falsk)
                self.assertEqual(visning.tur.begrunnelse, self.forventet()[2])


class _Reserve:
    """Som en variant som gir reserveteksten, men registrerer kallet i `falsk`."""

    def __init__(self, falsk):
        self.falsk = falsk

    def begrunnelse(self, sok, tur, reserve):
        self.falsk.begrunnelse(sok, tur, reserve)
        return KiSvar(tekst=reserve)
