"""`turforslag.turdata` og modellene `Startpunkt` og `Tur` (AR-6, AD-3 punkt 4–6)."""

import json
from dataclasses import replace
from pathlib import Path
from unittest import mock

from django.conf import settings
from django.db.models import ProtectedError
from django.test import TestCase

from domene import tur as domenetur
from turforslag import turdata
from turforslag.models import Startpunkt, Tur

TURFIL = Path(settings.BASE_DIR) / "data" / "turer.geojson"
# Fast kopi av turfila fra story 1.5, så testene ikke brytes når turfila byttes ut i 1.7.
FIXTUR = Path(settings.BASE_DIR) / "tests" / "fixtures" / "turer_lastinn.geojson"


def les_turer(sti: Path = FIXTUR) -> list[domenetur.Tur]:
    data = json.loads(sti.read_text(encoding="utf-8"))
    return [domenetur.Tur.fra_geojson_feature(feature) for feature in data["features"]]


class TurFraModellTest(TestCase):
    def test_ekte_turer_leses_tilbake_likt(self):  # AR-6, AD-3 punkt 5
        turer = les_turer(TURFIL)
        turdata.lagre_turer(turer)
        for tur in turer:
            with self.subTest(tur=tur.id):
                modell = Tur.objects.select_related("startpunkt").get(id=tur.id)
                tilbake = turdata.tur_fra_modell(modell)
                self.assertEqual(tilbake, tur)
                self.assertIsInstance(tilbake.turtyper, tuple)
                self.assertIsInstance(tilbake.hoydeprofil[0], tuple)
                self.assertIsInstance(tilbake.geometry[0], tuple)
                self.assertIs(type(tilbake.form), domenetur.Form)
                self.assertIs(type(tilbake.turniva), domenetur.Turniva)

    def test_lagrede_verdier_regnes_ikke_pa_nytt(self):  # AD-3 punkt 6, AD-2
        # Verdier som ikke stemmer med domene.gradering og domene.tid, skal komme uendret ut.
        tur = replace(
            les_turer()[0],
            turniva=domenetur.Turniva.SVART,
            hoydemeter_m=1,
            estimert_tid_min=7,
        )
        with (
            mock.patch("domene.gradering.turniva", side_effect=AssertionError("gradering")),
            mock.patch("domene.tid.estimert_tid_min", side_effect=AssertionError("tid")),
        ):
            turdata.lagre_turer([tur])
            tilbake = turdata.tur_fra_modell(Tur.objects.get(id=tur.id))
        self.assertEqual(tilbake.turniva, domenetur.Turniva.SVART)
        self.assertEqual(tilbake.hoydemeter_m, 1)
        self.assertEqual(tilbake.estimert_tid_min, 7)
        self.assertEqual(tilbake, tur)


class LagreTurerTest(TestCase):
    def test_teller_nye_og_oppdaterte(self):  # AR-5
        turer = les_turer()
        forste = turdata.lagre_turer(turer)
        self.assertEqual((forste.nye_turer, forste.oppdaterte_turer), (3, 0))
        self.assertEqual((forste.nye_startpunkter, forste.oppdaterte_startpunkter), (2, 0))
        andre = turdata.lagre_turer(turer)
        self.assertEqual((andre.nye_turer, andre.oppdaterte_turer), (0, 3))
        self.assertEqual((andre.nye_startpunkter, andre.oppdaterte_startpunkter), (0, 2))
        self.assertEqual(andre.mangler_i_fila, ())

    def test_turer_som_mangler_returneres_sortert_og_slettes_ikke(self):  # AR-5
        turer = les_turer()
        turdata.lagre_turer(turer)
        lagret = turdata.lagre_turer(turer[:1])
        self.assertEqual(lagret.mangler_i_fila, tuple(sorted(t.id for t in turer[1:])))
        self.assertEqual(Tur.objects.count(), 3)

    def test_startpunktet_oppdateres(self):  # AR-6
        tur = les_turer()[0]
        turdata.lagre_turer([tur])
        turdata.lagre_turer([replace(tur, startpunkt_navn="Nytt navn", startpunkt_hoyde_m=1)])
        startpunkt = Startpunkt.objects.get(id=tur.startpunkt_id)
        self.assertEqual((startpunkt.navn, startpunkt.hoyde_m), ("Nytt navn", 1))


class ModellTest(TestCase):
    def test_startpunkt_med_turer_kan_ikke_slettes(self):  # AR-6, AD-3 punkt 5
        turer = les_turer()
        turdata.lagre_turer(turer)
        startpunkt = Startpunkt.objects.get(id=turer[0].startpunkt_id)
        with self.assertRaises(ProtectedError):
            startpunkt.delete()
        self.assertTrue(Startpunkt.objects.filter(id=turer[0].startpunkt_id).exists())

    def test_str_og_rekkefolge(self):  # AR-6
        turer = les_turer()
        turdata.lagre_turer(turer)
        startpunkt = Startpunkt.objects.get(id=turer[0].startpunkt_id)
        self.assertEqual(str(startpunkt), turer[0].startpunkt_navn)
        ider = list(Tur.objects.values_list("id", flat=True))
        self.assertEqual(ider, sorted(ider))
        self.assertEqual(str(Tur.objects.first()), Tur.objects.first().navn)
