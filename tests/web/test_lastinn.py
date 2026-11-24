"""`python manage.py lastinn`: én test per rad i matrisen i spec 1.6 (AR-5, AD-3 punkt 4).

Matrisetestene bruker en fast kopi av turfila fra story 1.5
(`tests/fixtures/turer_lastinn.geojson`), så de ikke brytes når `data/turer.geojson` byttes ut
i story 1.7. Én test kjører kommandoen med standardfila og regner forventet antall ut fra
innholdet.
"""

import ast
import copy
import json
import tempfile
import unittest
from io import StringIO
from pathlib import Path
from unittest import mock

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import CommandError
from django.db import DatabaseError
from django.test import TestCase

from turforslag.models import Startpunkt, Tur

ROT = Path(settings.BASE_DIR)
TURFIL = ROT / "data" / "turer.geojson"
FIXTUR = ROT / "tests" / "fixtures" / "turer_lastinn.geojson"


def fixturdata() -> dict:
    return json.loads(FIXTUR.read_text(encoding="utf-8"))


def rader() -> tuple[list[dict], list[dict]]:
    """Alle kolonner i alle rader, så en delvis oppdatering ikke kan gå upåaktet hen."""
    return (
        list(Tur.objects.order_by("id").values()),
        list(Startpunkt.objects.order_by("id").values()),
    )


class LastinnTest(TestCase):
    def setUp(self):
        mappe = tempfile.TemporaryDirectory()
        self.addCleanup(mappe.cleanup)
        self.mappe = Path(mappe.name)

    def skriv(self, innhold, navn="turer.geojson", encoding="utf-8") -> Path:
        sti = self.mappe / navn
        if isinstance(innhold, bytes):
            sti.write_bytes(innhold)
            return sti
        tekst = innhold if isinstance(innhold, str) else json.dumps(innhold, ensure_ascii=False)
        sti.write_text(tekst, encoding=encoding)
        return sti

    def lastinn(self, *argumenter) -> tuple[str, str]:
        ut, feil = StringIO(), StringIO()
        call_command("lastinn", *argumenter, stdout=ut, stderr=feil)
        return ut.getvalue(), feil.getvalue()

    def lastinn_fixtur(self) -> tuple[str, str]:
        return self.lastinn("--fil", str(FIXTUR))

    def ugyldig(self, data_eller_tekst) -> str:
        """Laster inn fixturen, kjører så `lastinn` med en ugyldig fil og sjekker at alle
        rader er nøyaktig som før."""
        self.lastinn_fixtur()
        for_feil = rader()
        sti = self.skriv(data_eller_tekst)
        with self.assertRaises(CommandError) as feil:
            self.lastinn("--fil", str(sti))
        self.assertEqual(rader(), for_feil)
        melding = str(feil.exception)
        self.assertIn(str(sti), melding)
        return melding

    def test_standardfila_lastes_inn(self):  # AR-5
        data = json.loads(TURFIL.read_text(encoding="utf-8"))
        antall_turer = len(data["features"])
        antall_startpunkter = len({f["properties"]["startpunkt_id"] for f in data["features"]})
        ut, _ = self.lastinn()
        self.assertEqual(Tur.objects.count(), antall_turer)
        self.assertEqual(Startpunkt.objects.count(), antall_startpunkter)
        self.assertIn(f"{antall_turer} turer ({antall_turer} nye, 0 oppdaterte)", ut)
        self.assertIn(str(TURFIL), ut)

    def test_forste_kjoring_oppretter_alle_turer_og_startpunkter(self):  # AR-5
        ut, feil = self.lastinn_fixtur()
        self.assertEqual(Tur.objects.count(), 3)
        self.assertEqual(Startpunkt.objects.count(), 2)
        self.assertIn("3 turer (3 nye, 0 oppdaterte)", ut)
        self.assertIn("2 startpunkter (2 nye, 0 oppdaterte)", ut)
        self.assertEqual(feil, "")

    def test_andre_kjoring_gir_samme_antall_og_alle_oppdaterte(self):  # AR-5, AD-3 punkt 4
        self.lastinn_fixtur()
        ut, _ = self.lastinn_fixtur()
        self.assertEqual(Tur.objects.count(), 3)
        self.assertEqual(Startpunkt.objects.count(), 2)
        self.assertIn("3 turer (0 nye, 3 oppdaterte)", ut)
        self.assertIn("2 startpunkter (0 nye, 2 oppdaterte)", ut)

    def test_fil_med_bom_godtas(self):  # AR-5
        sti = self.skriv(fixturdata(), encoding="utf-8-sig")
        ut, _ = self.lastinn("--fil", str(sti))
        self.assertIn("3 turer (3 nye, 0 oppdaterte)", ut)

    def test_endret_verdi_oppdaterer_raden(self):  # AR-5, AD-3 punkt 4
        self.lastinn_fixtur()
        data = fixturdata()
        forste = data["features"][0]
        forste["properties"]["navn"] = "Nytt navn"
        forste["properties"]["lengde_m"] += 100
        self.lastinn("--fil", str(self.skriv(data)))
        tur = Tur.objects.get(id=forste["id"])
        self.assertEqual(tur.navn, "Nytt navn")
        self.assertEqual(tur.lengde_m, forste["properties"]["lengde_m"])
        self.assertEqual(Tur.objects.count(), 3)

    def test_tur_som_mangler_i_fila_beholdes_med_advarsel(self):  # AR-5, AD-3 punkt 4
        self.lastinn_fixtur()
        data = fixturdata()
        bort = sorted(feature["id"] for feature in data["features"][1:])
        data["features"] = data["features"][:1]
        for_endring = list(Tur.objects.filter(id__in=bort).order_by("id").values())

        ut, feil = self.lastinn("--fil", str(self.skriv(data)))

        self.assertIn("1 turer (0 nye, 1 oppdaterte)", ut)
        self.assertIn("Advarsel", feil)
        self.assertIn(", ".join(bort), feil)
        self.assertEqual(list(Tur.objects.filter(id__in=bort).order_by("id").values()), for_endring)
        self.assertEqual(Tur.objects.count(), 3)

    def test_fila_mangler(self):  # AR-5
        self.lastinn_fixtur()
        for_feil = rader()
        sti = self.mappe / "finnes-ikke.geojson"
        with self.assertRaisesRegex(CommandError, "Fant ikke turfila"):
            self.lastinn("--fil", str(sti))
        self.assertEqual(rader(), for_feil)

    def test_fila_kan_ikke_leses(self):  # AR-5
        melding = self.ugyldig("æ".encode("latin-1"))
        self.assertIn("Kunne ikke lese", melding)

    def test_ugyldig_json(self):  # AR-5
        melding = self.ugyldig('{"type": "FeatureCollection", "features": [')
        self.assertIn("ikke gyldig JSON", melding)

    def test_featurecollection_uten_features(self):  # AR-5
        melding = self.ugyldig({"type": "FeatureCollection"})
        self.assertIn("FeatureCollection", melding)

    def test_ikke_en_featurecollection(self):  # AR-5
        self.ugyldig([])
        self.ugyldig({"type": "Feature", "features": []})

    def test_feature_som_ikke_er_et_objekt(self):  # AR-5
        melding = self.ugyldig({"type": "FeatureCollection", "features": ["x"]})
        self.assertIn("tur nr. 1", melding)

    def test_ugyldig_tur_stopper_alt_ogsa_tur_nr_1(self):  # AR-5
        data = fixturdata()
        data["features"][0]["properties"]["navn"] = "Skal ikke lagres"
        andre = data["features"][1]
        del andre["properties"]["lengde_m"]
        melding = self.ugyldig(data)
        self.assertIn(andre["id"], melding)
        self.assertIn("lengde_m", melding)

    def test_feature_som_fra_geojson_feature_avviser(self):  # AR-5
        tilfeller = {
            "ValueError": lambda f: f["properties"].update(form="enveis"),
            "TypeError": lambda f: f["properties"].update(lengde_m=None),
            "AttributeError": lambda f: f.update(geometry=None),
        }
        for navn, endre in tilfeller.items():
            with self.subTest(navn):
                data = fixturdata()
                endre(data["features"][0])
                self.assertIn(data["features"][0]["id"], self.ugyldig(data))

    def test_negativ_verdi(self):  # AR-5, AD-3 punkt 5
        data = fixturdata()
        data["features"][0]["properties"]["lengde_m"] = -5
        melding = self.ugyldig(data)
        self.assertIn(data["features"][0]["id"], melding)
        self.assertIn("negativ", melding)

    def test_dublett_av_tur_id(self):  # AR-5, AD-3 punkt 5
        data = fixturdata()
        data["features"].append(copy.deepcopy(data["features"][0]))
        melding = self.ugyldig(data)
        self.assertIn(data["features"][0]["id"], melding)

    def test_ulikt_startpunkt(self):  # AR-5, AD-3 punkt 5
        data = fixturdata()
        kopi = copy.deepcopy(data["features"][0])
        kopi["id"] = "ny-tur"
        kopi["properties"]["startpunkt_navn"] = "Et annet navn"
        data["features"].append(kopi)
        melding = self.ugyldig(data)
        self.assertIn(kopi["properties"]["startpunkt_id"], melding)

    def test_ukjent_turtype(self):  # AR-5, AD-3 punkt 5
        data = fixturdata()
        data["features"][0]["properties"]["turtyper"] = ["utsiktt"]
        melding = self.ugyldig(data)
        self.assertIn(data["features"][0]["id"], melding)
        self.assertIn("utsiktt", melding)

    def test_verdi_databasen_avviser_gir_norsk_melding(self):  # AR-5
        data = fixturdata()
        data["features"][1]["properties"]["kilde"] = None
        melding = self.ugyldig(data)
        self.assertIn("Kunne ikke lagre turene", melding)

    def test_feil_midt_i_lagringen_ruller_tilbake(self):  # AR-5
        self.lastinn_fixtur()
        for_feil = rader()
        data = fixturdata()
        for feature in data["features"]:
            feature["properties"]["navn"] += " (endret)"
            feature["properties"]["startpunkt_navn"] += " (endret)"
        sti = self.skriv(data)

        ekte = Tur.objects.update_or_create
        kall = []

        def feiler_pa_andre_tur(*args, **kwargs):
            kall.append(kwargs.get("id"))
            if len(kall) == 2:
                raise DatabaseError("test")
            return ekte(*args, **kwargs)

        with (
            mock.patch(
                "turforslag.models.Tur.objects.update_or_create", side_effect=feiler_pa_andre_tur
            ),
            self.assertRaisesRegex(CommandError, "Kunne ikke lagre turene"),
        ):
            self.lastinn("--fil", str(sti))
        self.assertEqual(len(kall), 2)
        self.assertEqual(rader(), for_feil)

    def test_lastinn_regner_aldri_niva_eller_tid(self):  # AD-3 punkt 6, AD-2
        with (
            mock.patch("domene.gradering.turniva", side_effect=AssertionError("gradering")),
            mock.patch("domene.tid.estimert_tid_min", side_effect=AssertionError("tid")),
        ):
            self.lastinn_fixtur()
            self.lastinn_fixtur()
        self.assertEqual(Tur.objects.count(), 3)


class ImporterIkkeBeregningerTest(unittest.TestCase):
    """`lastinn` og `turdata` importerer verken `domene.gradering` eller `domene.tid` (AD-3
    punkt 6), så de kan ikke regne nivå eller tid på nytt."""

    FORBUDT = {"domene.gradering", "domene.tid"}
    FILER = [
        ROT / "turforslag" / "turdata.py",
        ROT / "turforslag" / "management" / "commands" / "lastinn.py",
    ]

    def importerte_moduler(self, sti: Path) -> set[str]:
        moduler = set()
        for node in ast.walk(ast.parse(sti.read_text(encoding="utf-8"))):
            if isinstance(node, ast.Import):
                moduler.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                moduler.add(node.module)
                moduler.update(f"{node.module}.{alias.name}" for alias in node.names)
        return moduler

    def test_ingen_import_av_gradering_eller_tid(self):  # AD-3 punkt 6, AD-2
        for sti in self.FILER:
            with self.subTest(fil=sti.name):
                moduler = self.importerte_moduler(sti)
                self.assertIn("domene.tur", moduler)  # sjekken ser faktisk importene
                self.assertEqual(moduler & self.FORBUDT, set())
