"""`domene/` er ren Python som bare importerer standardbiblioteket (AR-2, AD-2)."""

import ast
import sys
import unittest
from pathlib import Path

DOMENE = Path(__file__).resolve().parents[2] / "domene"
TILLATTE_EGNE = {"domene"}


def ikke_standard_importer(kildetekst: str) -> list[str]:
    """Gir modulene som verken er i standardbiblioteket eller i `domene` selv."""
    funn = []
    for node in ast.walk(ast.parse(kildetekst)):
        if isinstance(node, ast.Import):
            navn = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            navn = [node.module]
        else:
            continue
        for modul in navn:
            topp = modul.split(".")[0]
            if topp not in sys.stdlib_module_names and topp not in TILLATTE_EGNE:
                funn.append(modul)
    return funn


class BareStandardbibliotekTest(unittest.TestCase):
    def test_domene_importerer_bare_standardbiblioteket(self):  # AR-2
        filer = sorted(DOMENE.rglob("*.py"))
        self.assertTrue(filer, "domene/ skal ha minst __init__.py")
        for fil in filer:
            with self.subTest(fil=fil.name):
                self.assertEqual(ikke_standard_importer(fil.read_text(encoding="utf-8")), [])

    def test_sjekken_finner_importer_utenfor_standardbiblioteket(self):
        kilde = "import json\nimport django\nfrom requests import get\nfrom . import tur\n"
        self.assertEqual(ikke_standard_importer(kilde), ["django", "requests"])

    def test_sjekken_godtar_standardbiblioteket_og_domene(self):
        kilde = "import datetime\nfrom dataclasses import dataclass\nfrom domene.tur import Tur\n"
        self.assertEqual(ikke_standard_importer(kilde), [])
