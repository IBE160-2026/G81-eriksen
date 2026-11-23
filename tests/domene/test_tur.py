"""`domene.tur`: dataklassen, GeoJSON-omformingen og totalene (AR-3, FR-3)."""

import json
import unittest
from dataclasses import FrozenInstanceError, fields, replace

from domene.tur import (
    Form,
    Tur,
    Turniva,
    avstand_m,
    total_hoydemeter_m,
    total_lengde_m,
    total_nedstigning_m,
)


def lag_tur(**endringer) -> Tur:
    tur = Tur(
        id="kolsastoppen",
        navn="Kolsåstoppen",
        startpunkt_id="sorkedalen",
        startpunkt_navn="Sørkedalen",
        startpunkt_lat=59.9876,
        startpunkt_lon=10.6543,
        startpunkt_hoyde_m=180,
        form=Form.TUR_RETUR,
        turtyper=("marka", "utsikt"),
        lengde_m=3000,
        hoydemeter_m=150,
        nedstigning_m=0,
        hoydeprofil=((0, 180), (1500, 260), (3000, 330)),
        turniva=Turniva.GRONN,
        estimert_tid_min=140,
        ut_no_url="",
        kilde="turrutebasen",
        lisens="CC BY 4.0",
        geometry=((10.6543, 59.9876), (10.66, 59.99), (10.67, 60.0)),
    )
    return replace(tur, **endringer)


class TurDataklasseTest(unittest.TestCase):
    def test_feltene_er_i_rekkefolgen_fra_ad_3(self):  # AR-3
        self.assertEqual(
            [felt.name for felt in fields(Tur)],
            [
                "id",
                "navn",
                "startpunkt_id",
                "startpunkt_navn",
                "startpunkt_lat",
                "startpunkt_lon",
                "startpunkt_hoyde_m",
                "form",
                "turtyper",
                "lengde_m",
                "hoydemeter_m",
                "nedstigning_m",
                "hoydeprofil",
                "turniva",
                "estimert_tid_min",
                "ut_no_url",
                "kilde",
                "lisens",
                "geometry",
            ],
        )

    def test_turen_er_frossen(self):  # AR-3
        tur = lag_tur()
        with self.assertRaises(FrozenInstanceError):
            tur.lengde_m = 4000

    def test_turen_kan_hashes(self):  # AR-3
        self.assertEqual(hash(lag_tur()), hash(lag_tur()))
        self.assertEqual(len({lag_tur(), lag_tur()}), 1)

    def test_form_og_turniva_har_verdiene_fra_ad_3(self):  # AR-3, FR-2
        self.assertEqual([f.value for f in Form], ["rundtur", "tur-retur"])
        self.assertEqual([n.value for n in Turniva], ["gronn", "bla", "rod", "svart"])


class GeojsonTest(unittest.TestCase):
    def test_feature_har_id_geometri_og_alle_andre_felt_som_properties(self):  # AR-3
        feature = lag_tur().til_geojson_feature()
        self.assertEqual(feature["type"], "Feature")
        self.assertEqual(feature["id"], "kolsastoppen")
        self.assertEqual(feature["geometry"]["type"], "LineString")
        self.assertEqual(feature["geometry"]["coordinates"][0], [10.6543, 59.9876])
        andre = {felt.name for felt in fields(Tur)} - {"id", "geometry"}
        self.assertEqual(set(feature["properties"]), andre)
        self.assertEqual(feature["properties"]["form"], "tur-retur")
        self.assertEqual(feature["properties"]["turniva"], "gronn")

    def test_feature_kan_gjores_om_til_json_med_lister(self):  # AR-3
        feature = lag_tur().til_geojson_feature()
        self.assertEqual(json.loads(json.dumps(feature)), feature)
        self.assertIsInstance(feature["properties"]["turtyper"], list)
        self.assertIsInstance(feature["properties"]["hoydeprofil"][0], list)
        self.assertIsInstance(feature["geometry"]["coordinates"][0], list)

    def test_omforming_fram_og_tilbake_gir_lik_tur(self):  # AR-3
        tur = lag_tur()
        self.assertEqual(Tur.fra_geojson_feature(tur.til_geojson_feature()), tur)

    def test_omforming_via_json_tekst_gir_lik_tur_med_tuples_og_enum(self):  # AR-3
        tur = lag_tur(form=Form.RUNDTUR, turniva=Turniva.SVART, ut_no_url="https://ut.no/x")
        tilbake = Tur.fra_geojson_feature(json.loads(json.dumps(tur.til_geojson_feature())))
        self.assertEqual(tilbake, tur)
        self.assertIs(tilbake.form, Form.RUNDTUR)
        self.assertIs(tilbake.turniva, Turniva.SVART)
        self.assertIsInstance(tilbake.turtyper, tuple)
        self.assertIsInstance(tilbake.hoydeprofil[0], tuple)
        self.assertIsInstance(tilbake.geometry[0], tuple)

    def test_feil_featuretype_gir_valueerror(self):  # AR-3
        feature = lag_tur().til_geojson_feature()
        feature["type"] = "FeatureCollection"
        with self.assertRaises(ValueError):
            Tur.fra_geojson_feature(feature)

    def test_annen_geometri_enn_linestring_gir_valueerror(self):  # AR-3
        feature = lag_tur().til_geojson_feature()
        feature["geometry"] = {"type": "Point", "coordinates": [10.6543, 59.9876]}
        with self.assertRaises(ValueError):
            Tur.fra_geojson_feature(feature)

    def test_ukjent_form_gir_valueerror(self):  # AR-3
        feature = lag_tur().til_geojson_feature()
        feature["properties"]["form"] = "enveis"
        with self.assertRaises(ValueError):
            Tur.fra_geojson_feature(feature)

    def test_ukjent_turniva_gir_valueerror(self):  # AR-3, FR-2
        feature = lag_tur().til_geojson_feature()
        feature["properties"]["turniva"] = "lilla"
        with self.assertRaises(ValueError):
            Tur.fra_geojson_feature(feature)


class TotalerTest(unittest.TestCase):
    def test_tur_retur_dobler_lengde_og_bytter_opp_og_ned(self):  # FR-3, AR-3
        form = Form.TUR_RETUR
        self.assertEqual(total_lengde_m(form, 2000), 4000)
        self.assertEqual(total_hoydemeter_m(form, 100, 40), 140)
        self.assertEqual(total_nedstigning_m(form, 100, 40), 140)

    def test_rundtur_bruker_de_lagrede_verdiene(self):  # FR-3, AR-3
        form = Form.RUNDTUR
        self.assertEqual(total_lengde_m(form, 2000), 2000)
        self.assertEqual(total_hoydemeter_m(form, 100, 40), 100)
        self.assertEqual(total_nedstigning_m(form, 100, 40), 40)


class AvstandTest(unittest.TestCase):
    def test_en_breddegrad_er_r_ganger_pi_delt_pa_180(self):  # AR-3
        # Haversine med R = 6 371 008,8 m: 1° langs en meridian er 111 195,08 m.
        self.assertAlmostEqual(avstand_m((10.0, 59.0), (10.0, 60.0)), 111_195.08, places=2)

    def test_lengdegrad_krymper_med_cos_til_breddegraden(self):  # AR-3
        # Ved 60° nord er 1° øst-vest omtrent halvparten av 1° nord-sør.
        self.assertAlmostEqual(avstand_m((10.0, 60.0), (11.0, 60.0)), 55_596, delta=5)

    def test_samme_punkt_gir_0_og_rekkefolgen_spiller_ingen_rolle(self):  # AR-3
        a, b = (10.717187, 59.953615), (10.715769, 59.953129)
        self.assertEqual(avstand_m(a, a), 0.0)
        self.assertEqual(avstand_m(a, b), avstand_m(b, a))
        self.assertAlmostEqual(avstand_m(a, b), 95.2, delta=0.5)
