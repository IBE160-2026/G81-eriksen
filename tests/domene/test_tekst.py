"""`domene.tekst`: faste norske formater (UX-DR31, AR-16, FR-4, FR-6)."""

import unittest
from datetime import date

from domene import tekst
from domene.okt import Soketilstand
from domene.sok import Sok
from domene.tekst import formater_lengde_totalt, formater_niva, formater_tid
from domene.tur import Form, Turniva
from domene.utvalg import Status
from tests.domene.test_utvalg import lag_tur

I_DAG = date(2026, 11, 26)  # torsdag


class FormaterTidTest(unittest.TestCase):
    def test_timer_og_minutter(self):  # FR-3, UX-DR31
        self.assertEqual(formater_tid(95), "ca. 1 t 35 min")

    def test_bare_minutter(self):  # FR-3, UX-DR31
        self.assertEqual(formater_tid(45), "ca. 45 min")

    def test_hele_timer(self):  # FR-3, UX-DR31
        self.assertEqual(formater_tid(120), "ca. 2 t")


class FormaterLengdeTest(unittest.TestCase):
    def test_en_desimal_med_desimalkomma(self):  # UX-DR31, AR-16
        self.assertEqual(formater_lengde_totalt(3500), "3,5 km totalt")

    def test_hele_km_uten_komma_null(self):  # UX-DR31, AR-16
        self.assertEqual(formater_lengde_totalt(6000), "6 km totalt")

    def test_avrunding_til_hel_km_droppes_komma_null(self):  # UX-DR31, AR-16
        self.assertEqual(formater_lengde_totalt(5960), "6 km totalt")

    def test_halv_runder_opp(self):  # UX-DR31, AR-16
        self.assertEqual(formater_lengde_totalt(3450), "3,5 km totalt")
        self.assertEqual(formater_lengde_totalt(3449), "3,4 km totalt")


class FormaterNivaTest(unittest.TestCase):
    def test_alle_nivaer_med_tankestrek(self):  # FR-2, UX-DR31
        self.assertEqual(formater_niva(Turniva.GRONN), "Grønn – lett")
        self.assertEqual(formater_niva(Turniva.BLA), "Blå – moderat")
        self.assertEqual(formater_niva(Turniva.ROD), "Rød – moderat")
        self.assertEqual(formater_niva(Turniva.SVART), "Svart – vanskelig")


class VarighetTest(unittest.TestCase):
    def test_varighetsvalg_har_23_valg_i_halvtimessteg(self):  # FR-4
        valg = tekst.varighetsvalg()
        self.assertEqual(len(valg), 23)
        self.assertEqual(valg[0], (60, "1 t"))
        self.assertEqual(valg[1], (90, "1,5 t"))
        self.assertEqual(valg[2], (120, "2 t"))
        self.assertEqual(valg[-1], (720, "12 t"))

    def test_varighet_i_lopende_tekst(self):  # FR-12, UX-DR31
        self.assertEqual(tekst.formater_varighet_timer(60), "1 time")
        self.assertEqual(tekst.formater_varighet_timer(90), "1,5 timer")
        self.assertEqual(tekst.formater_varighet_timer(180), "3 timer")

    def test_annet_enn_hele_og_halve_timer_gir_value_error(self):  # FR-4
        with self.assertRaises(ValueError):
            tekst.formater_varighet(75)


class DatoTest(unittest.TestCase):
    def test_datoperiode_har_31_datoer_fra_i_dag(self):  # FR-4
        datoer = tekst.datoperiode(I_DAG)
        self.assertEqual(len(datoer), 31)
        self.assertEqual(datoer[0], I_DAG)
        self.assertEqual(datoer[-1], date(2026, 12, 26))

    def test_datovalg(self):  # FR-4
        valg = tekst.datovalg(I_DAG)
        self.assertEqual(valg[0], (I_DAG, "Torsdag 26. november"))
        self.assertEqual(valg[2], (date(2026, 11, 28), "Lørdag 28. november"))
        self.assertEqual(valg[-1], (date(2026, 12, 26), "Lørdag 26. desember"))

    def test_over_arsskiftet(self):  # FR-4
        self.assertEqual(tekst.datoperiode(date(2026, 12, 20))[-1], date(2027, 1, 19))
        self.assertEqual(tekst.siste_dato(date(2026, 12, 20)), "19. januar")

    def test_siste_dato_til_feilmeldingen(self):  # FR-4
        self.assertEqual(tekst.siste_dato(I_DAG), "26. desember")

    def test_kort_dato(self):  # FR-6
        self.assertEqual(tekst.formater_dato_kort(date(2026, 11, 7)), "Lørdag 7. nov.")
        self.assertEqual(tekst.formater_dato_kort(date(2026, 5, 4)), "Mandag 4. mai")
        self.assertEqual(tekst.formater_dato_kort(date(2026, 3, 1)), "Søndag 1. mar.")


class SokeoppsummeringTest(unittest.TestCase):
    def test_eksempelet_fra_mikrotekst(self):  # FR-6, UX-DR16
        sok = Sok(120, date(2026, 11, 7), turtype="utsikt")
        self.assertEqual(tekst.sokeoppsummering(sok), "Lørdag 7. nov. · 2 t · Utsikt")

    def test_alle_turtyper_og_startpunkt(self):  # UX-DR16
        sok = Sok(150, date(2026, 11, 7), startpunkt_id="sognsvann")
        self.assertEqual(tekst.sokeoppsummering(sok), "Lørdag 7. nov. · 2,5 t")
        self.assertEqual(
            tekst.sokeoppsummering(sok, "Sognsvann"), "Lørdag 7. nov. · 2,5 t · Sognsvann"
        )


class TurteksterTest(unittest.TestCase):
    def test_form(self):  # FR-6
        self.assertEqual(tekst.formater_form(Form.RUNDTUR), "Rundtur")
        self.assertEqual(tekst.formater_form(Form.TUR_RETUR), "Tur-retur")

    def test_turtype_treff(self):  # FR-6
        self.assertEqual(tekst.turtype_treff("utsikt"), "Utsikt – som du ba om")
        self.assertEqual(tekst.turtype_treff("marka"), "Marka – som du ba om")
        self.assertEqual(tekst.turtype_treff("topptur"), "Topptur – som du ba om")

    def test_turtypevalg(self):  # FR-4
        self.assertEqual(
            tekst.turtypevalg(), (("marka", "Marka"), ("utsikt", "Utsikt"), ("topptur", "Topptur"))
        )

    def test_hoydemeter(self):  # FR-6, UX-DR31
        self.assertEqual(tekst.formater_hoydemeter(130), "ca. 130")
        self.assertEqual(tekst.formater_hoydemeter(128), "ca. 130")
        self.assertEqual(tekst.formater_hoydemeter(125), "ca. 130")
        self.assertEqual(tekst.formater_hoydemeter(124), "ca. 120")
        self.assertEqual(tekst.formater_hoydemeter(4), "ca. 0")

    def test_lengde_uten_totalt(self):  # UX-DR31
        self.assertEqual(tekst.formater_lengde(3500), "3,5 km")
        self.assertEqual(tekst.formater_lengde(6000), "6 km")

    def test_startpunkter_sorteres_etter_norsk_alfabet(self):  # FR-4
        startpunkter = [
            ("a", "Åsen"),
            ("o", "Østmarksetra"),
            ("e", "Ærfuglen"),
            ("z", "Zakken"),
            ("s", "sognsvann"),
        ]
        self.assertEqual(
            [navn for _, navn in tekst.sorter_startpunkter(startpunkter)],
            ["sognsvann", "Zakken", "Ærfuglen", "Østmarksetra", "Åsen"],
        )


class ForslagsvisningTest(unittest.TestCase):
    def test_tur_retur_viser_totalene_og_lagret_tid(self):  # FR-3, FR-6, AD-2
        tur = lag_tur(
            form=Form.TUR_RETUR,
            lengde_m=1750,
            hoydemeter_m=100,
            nedstigning_m=30,
            estimert_tid_min=7,
            turtyper=("utsikt",),
            turniva=Turniva.BLA,
        )
        sok = Sok(120, I_DAG, turtype="utsikt")
        visning = tekst.turvisning(sok, Status.TREFF, tur, "Begrunnelse.")
        self.assertEqual(visning.lengde, "3,5 km")
        self.assertEqual(visning.hoydemeter, "ca. 130")
        self.assertEqual(visning.tid, "ca. 7 min")  # lagret verdi, aldri regnet på nytt
        self.assertEqual(visning.nivatekst, "Blå – moderat")
        self.assertEqual(visning.niva, "bla")
        self.assertEqual(visning.form, "Tur-retur")
        self.assertEqual(visning.turtype_treff, "Utsikt – som du ba om")
        self.assertFalse(visning.topptur_erstattet)

    def test_turtype_treff_bare_nar_turtype_er_valgt(self):  # FR-6
        tur = lag_tur(turtyper=("utsikt",))
        self.assertIsNone(tekst.turvisning(Sok(180, I_DAG), Status.TREFF, tur, "").turtype_treff)

    def test_topptur_erstattet(self):  # FR-8
        tur = lag_tur(turtyper=("utsikt",))
        sok = Sok(180, I_DAG, turtype="topptur")
        visning = tekst.turvisning(sok, Status.TOPPTUR_ERSTATTET, tur, "")
        self.assertTrue(visning.topptur_erstattet)
        self.assertIsNone(visning.turtype_treff)

    def test_tilstandspanel_uten_tur(self):  # FR-8
        tilstand = Soketilstand(Sok(120, I_DAG, turtype="topptur"), Status.INGEN_TREFF, ())
        visning = tekst.forslagsvisning(tilstand, None)
        self.assertIsNone(visning.tur)
        self.assertTrue(visning.ingen_treff)
        self.assertFalse(visning.bare_over_nivatak)
        self.assertEqual(visning.sokeoppsummering, "Torsdag 26. nov. · 2 t · Topptur")


class AlleVistTest(unittest.TestCase):
    """Tilstandspanel «alle vist» (FR-7, UX-DR19), Mikrotekst «Alle forslag er vist, ingress»."""

    def test_eksempelet_fra_experience(self):  # FR-7
        self.assertEqual(
            tekst.alle_vist_ingress(4, "utsikt", 120, Status.TREFF),
            "Det var fire turer med utsikt som passer 2 timer.",
        )

    def test_entall_og_uten_turtype(self):  # FR-7
        self.assertEqual(
            tekst.alle_vist_ingress(1, None, 60, Status.TREFF),
            "Det var én tur som passer 1 time.",
        )
        self.assertEqual(
            tekst.alle_vist_ingress(3, None, 150, Status.TREFF),
            "Det var tre turer som passer 2,5 timer.",
        )

    def test_turtypene(self):  # FR-7
        self.assertEqual(
            tekst.alle_vist_ingress(2, "marka", 180, Status.TREFF),
            "Det var to turer i marka som passer 3 timer.",
        )
        self.assertEqual(
            tekst.alle_vist_ingress(2, "topptur", 180, Status.TREFF),
            "Det var to toppturer som passer 3 timer.",
        )

    def test_entall_for_topptur_og_marka(self):  # FR-7
        self.assertEqual(
            tekst.alle_vist_ingress(1, "topptur", 180, Status.TREFF),
            "Det var én topptur som passer 3 timer.",
        )
        self.assertEqual(
            tekst.alle_vist_ingress(1, "marka", 180, Status.TREFF),
            "Det var én tur i marka som passer 3 timer.",
        )

    def test_antall_kan_gis_til_forslagsvisning(self):  # FR-7, SM-C1
        tilstand = Soketilstand(
            Sok(180, I_DAG), Status.TREFF, ("a", "b", "c"), viste_tur_ider=("a", "b", "c")
        )
        visning = tekst.forslagsvisning(tilstand, None, antall=1)
        self.assertEqual(visning.ingress_alle_vist, "Det var én tur som passer 3 timer.")

    def test_topptur_erstattet_gir_utsikt(self):  # FR-7, FR-8
        self.assertEqual(
            tekst.alle_vist_ingress(2, "topptur", 180, Status.TOPPTUR_ERSTATTET),
            "Det var to turer med utsikt som passer 3 timer.",
        )

    def test_tallord_1_til_12_og_siffer_fra_13(self):  # FR-7, UX-DR31
        forventet = [
            "én tur",
            "to turer",
            "tre turer",
            "fire turer",
            "fem turer",
            "seks turer",
            "sju turer",
            "åtte turer",
            "ni turer",
            "ti turer",
            "elleve turer",
            "tolv turer",
            "13 turer",
            "15 turer",
        ]
        self.assertEqual([tekst.antall_turer(n) for n in [*range(1, 14), 15]], forventet)
        with self.assertRaises(ValueError):
            tekst.antall_turer(0)

    def test_forslagsvisning_alle_vist(self):  # FR-7
        tilstand = Soketilstand(
            Sok(120, I_DAG, turtype="utsikt"),
            Status.TREFF,
            ("a", "b", "c", "d"),
            viste_tur_ider=("a", "b", "c", "d"),
        )
        visning = tekst.forslagsvisning(tilstand, None)
        self.assertIsNone(visning.tur)
        self.assertTrue(visning.alle_vist)
        self.assertFalse(visning.ingen_treff)
        self.assertEqual(
            visning.ingress_alle_vist, "Det var fire turer med utsikt som passer 2 timer."
        )

    def test_ikke_alle_vist_ved_ingen_treff(self):  # FR-7, FR-8
        tilstand = Soketilstand(Sok(120, I_DAG), Status.INGEN_TREFF, ())
        visning = tekst.forslagsvisning(tilstand, None)
        self.assertFalse(visning.alle_vist)
        self.assertEqual(visning.ingress_alle_vist, "")


class LavesteOgHoyesteTest(unittest.TestCase):
    def test_avrundet_til_naermeste_10_m(self):  # FR-6, UX-DR15
        self.assertEqual(tekst.laveste_og_hoyeste(((0, 183.2), (500, 311.7))), (180, 310))

    def test_halv_runder_opp(self):  # FR-6
        self.assertEqual(tekst.laveste_og_hoyeste(((0, 185), (10, 174.9))), (170, 190))

    def test_rekkefolgen_i_profilen_spiller_ingen_rolle(self):  # FR-6
        profil = ((0, 250.0), (25, 199.6), (50, 320.4), (75, 240.0))
        self.assertEqual(tekst.laveste_og_hoyeste(profil), (200, 320))

    def test_lister_fra_json_virker(self):  # FR-6: profilen kan komme som lister
        self.assertEqual(tekst.laveste_og_hoyeste([[0, 99.0]]), (100, 100))

    def test_tom_profil_gir_value_error(self):  # FR-6
        with self.assertRaises(ValueError):
            tekst.laveste_og_hoyeste(())


class KartbeskrivelseTest(unittest.TestCase):
    def test_eksempelet_fra_experience(self):  # FR-6, UX-DR15
        tur = lag_tur(
            form=Form.RUNDTUR,
            startpunkt_navn="Granvannet p-plass",
            lengde_m=3500,
            hoydemeter_m=128,
            nedstigning_m=128,
            hoydeprofil=((0, 183.2), (1700, 311.7), (3500, 183.2)),
        )
        self.assertEqual(
            tekst.kartbeskrivelse(tur),
            "Rundtur på 3,5 km totalt fra Granvannet p-plass. "
            "Ruten stiger ca. 130 høydemeter, fra 180 til 310 moh.",
        )

    def test_tur_retur_har_totalene_for_hele_turen(self):  # FR-3, FR-6
        tur = lag_tur(
            form=Form.TUR_RETUR,
            startpunkt_navn="Sørkedalen",
            lengde_m=1750,
            hoydemeter_m=100,
            nedstigning_m=30,
            hoydeprofil=((0, 180), (1750, 254)),
        )
        self.assertEqual(
            tekst.kartbeskrivelse(tur),
            "Tur-retur på 3,5 km totalt fra Sørkedalen. "
            "Ruten stiger ca. 130 høydemeter, fra 180 til 250 moh.",
        )


class KartvisningTest(unittest.TestCase):
    def test_turvisningen_har_kartet(self):  # FR-6, AR-10, UX-DR13
        tur = lag_tur(navn="Granåsen rundt", geometry=((10.65, 59.98, 180.0), (10.67, 60.0)))
        visning = tekst.turvisning(Sok(180, I_DAG), Status.TREFF, tur, "")
        self.assertEqual(visning.kart_navn, "Kart over Granåsen rundt")
        self.assertEqual(visning.kartbeskrivelse, tekst.kartbeskrivelse(tur))
        self.assertEqual(
            visning.kart_geojson,
            {
                "type": "Feature",
                "geometry": {"type": "LineString", "coordinates": [[10.65, 59.98], [10.67, 60.0]]},
                "properties": {"start": [10.65, 59.98]},
            },
        )
