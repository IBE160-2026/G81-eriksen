"""`domene.rute`: nettverk, festing, korteste sti, omsampling og støyfilter (AD-3, AR-2)."""

import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from domene import rute
from domene.tur import avstand_m

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"
APP_NS = "http://skjema.geonorge.no/SOSI/produktspesifikasjon/TurOgFriluftsruter/20171210"
GML_NS = "http://www.opengis.net/gml/3.2"

# Omtrent 1 m i breddegrad.
GRAD_PER_METER = 1 / 111_195


def segmenter_fra_fixture(navn: str) -> list[tuple[tuple[float, float], ...]]:
    """Leser segmentene direkte, så testene av `domene` ikke avhenger av `skript`."""
    rot = ET.parse(FIXTURES / navn).getroot()
    segmenter = []
    for poslist in rot.iter(f"{{{GML_NS}}}posList"):
        tall = [float(v) for v in poslist.text.split()]
        segmenter.append(tuple(zip(tall[0::2], tall[1::2], strict=True)))
    return segmenter


def nord(punkt, meter):
    return (punkt[0], punkt[1] + meter * GRAD_PER_METER)


A = (10.70, 59.95)
B = nord(A, 100)
C = nord(A, 200)
D = (10.702, 59.95 + 120 * GRAD_PER_METER)  # ca. 110 m øst og 20 m nord for B


class LagNettverkTest(unittest.TestCase):
    def test_endepunkter_innenfor_1_m_blir_samme_node(self):  # AD-3
        nettverk = rute.lag_nettverk([(A, B), (nord(B, 0.5), C)])
        self.assertEqual(len(nettverk.noder), 3)
        self.assertEqual(len(nettverk.kanter), 2)

    def test_endepunkter_2_m_fra_hverandre_er_ulike_noder(self):  # AD-3
        nettverk = rute.lag_nettverk([(A, B), (nord(B, 2), C)])
        self.assertEqual(len(nettverk.noder), 4)

    def test_like_og_snudde_segmenter_tas_med_en_gang(self):  # AD-3
        nettverk = rute.lag_nettverk([(A, B), (B, A), (A, B), (B, C)])
        self.assertEqual(len(nettverk.kanter), 2)

    def test_rekkefolgen_i_kilden_endrer_ikke_nettverket(self):  # AD-3
        segmenter = segmenter_fra_fixture("wfs_F_01812_03.xml")
        self.assertEqual(rute.lag_nettverk(segmenter), rute.lag_nettverk(list(reversed(segmenter))))

    def test_ingen_segmenter_gir_feil(self):  # AD-3
        with self.assertRaises(rute.TomtNettverk):
            rute.lag_nettverk([])


class FestPunktTest(unittest.TestCase):
    def setUp(self):
        self.nettverk = rute.lag_nettverk([(A, B), (B, C)])

    def test_punkt_festes_til_naermeste_node(self):  # AD-3
        self.assertEqual(self.nettverk.noder[rute.fest_punkt(self.nettverk, nord(B, 30))], B)

    def test_punkt_lenger_unna_enn_50_m_gir_feil_med_avstand(self):  # AD-3
        punkt = (A[0] + 0.0015, A[1])  # ca. 84 m øst for A
        with self.assertRaises(rute.PunktForLangtUnna) as feil:
            rute.fest_punkt(self.nettverk, punkt)
        self.assertEqual(feil.exception.punkt, punkt)
        self.assertAlmostEqual(feil.exception.avstand_m, avstand_m(A, punkt))
        self.assertGreater(feil.exception.avstand_m, 50)


class KortesteStiTest(unittest.TestCase):
    def test_velger_korteste_vei_og_snur_segmenter(self):  # AD-3
        # A–B–C rett nord, og en omvei A–D–C. Segmentet B–C ligger snudd i kilden.
        nettverk = rute.lag_nettverk([(A, B), (C, B), (A, D), (D, C)])
        self.assertEqual(rute.sti_gjennom(nettverk, [A, C]), (A, B, C))
        self.assertEqual(rute.sti_gjennom(nettverk, [C, A]), (C, B, A))

    def test_via_punkt_tvinger_stien_innom(self):  # AD-3
        nettverk = rute.lag_nettverk([(A, B), (B, C), (A, D), (D, C)])
        self.assertEqual(rute.sti_gjennom(nettverk, [A, D, C]), (A, D, C))

    def test_rundtur_slutter_der_den_startet(self):  # AD-3
        nettverk = rute.lag_nettverk([(A, B), (B, C), (A, D), (D, C)])
        sti = rute.sti_gjennom(nettverk, [A, B, D, A])
        self.assertEqual(sti[0], sti[-1])
        self.assertEqual(sti, (A, B, C, D, A))

    def test_forgreinet_nettverk_fra_turrutebasen(self):  # AD-3
        # F_01812_03: 22 segmenter, 2 komponenter og forgreininger (spiken før 1.5).
        nettverk = rute.lag_nettverk(segmenter_fra_fixture("wfs_F_01812_03.xml"))
        fra, til = (10.72659, 59.969076), (10.716583, 59.952655)
        sti = rute.sti_gjennom(nettverk, [fra, til])
        self.assertEqual((sti[0], sti[-1]), (fra, til))
        # Stikkveiene til de andre endene er ikke med.
        self.assertNotIn((10.715134, 59.956346), sti)
        self.assertNotIn((10.727392, 59.962502), sti)
        self.assertEqual(rute.hele_meter(rute.linjelengde_m(sti)), 2213)
        # Ingen punkter gjentas, og stien hopper aldri.
        self.assertEqual(len(set(sti)), len(sti))
        self.assertLess(max(avstand_m(a, b) for a, b in zip(sti, sti[1:], strict=False)), 60)

    def test_ingen_sti_mellom_komponenter_gir_feil(self):  # AD-3
        nettverk = rute.lag_nettverk(segmenter_fra_fixture("wfs_F_20220203_01.xml"))
        fra, til = (10.733128, 59.971026), (10.761513, 59.969127)
        with self.assertRaises(rute.IngenSti) as feil:
            rute.sti_gjennom(nettverk, [fra, til])
        self.assertEqual((feil.exception.fra, feil.exception.til), (fra, til))

    def test_to_rutepunkter_pa_samme_node_gir_feil(self):  # AD-3
        # Et via-punkt 3 m fra «fra» ville ellers forsvunnet uten varsel.
        nettverk = rute.lag_nettverk([(A, B), (B, C)])
        via = nord(A, 3)
        with self.assertRaises(rute.PunkterPaSammeNode) as feil:
            rute.sti_gjennom(nettverk, [A, via, C])
        self.assertEqual((feil.exception.fra, feil.exception.til), (A, via))

    def test_rundtur_med_via_pa_startnoden_gir_feil(self):  # AD-3
        nettverk = rute.lag_nettverk([(A, B), (B, C)])
        with self.assertRaises(rute.PunkterPaSammeNode):
            rute.sti_gjennom(nettverk, [A, nord(A, 3), A])

    def test_ett_rutepunkt_gir_feil(self):  # AD-3
        with self.assertRaises(rute.RuteFeil):
            rute.sti_gjennom(rute.lag_nettverk([(A, B)]), [A])


class KoblingerTest(unittest.TestCase):
    def test_kobling_blir_rett_segment_som_binder_nettverket(self):  # AD-3, beslutning 2
        b2 = nord(B, 6)  # 6 m: ulike noder uten koblingen
        segmenter = [(A, B), (b2, C)]
        with self.assertRaises(rute.IngenSti):
            rute.sti_gjennom(rute.lag_nettverk(segmenter), [A, C])
        med = rute.med_koblinger(segmenter, [(B, b2)])
        self.assertEqual(med[-1], (B, b2))
        self.assertEqual(rute.sti_gjennom(rute.lag_nettverk(med), [A, C]), (A, B, b2, C))

    def test_kobling_over_10_m_gir_feil_med_avstand(self):  # AD-3, beslutning 2
        langt = nord(B, 10.5)
        with self.assertRaises(rute.KoblingForLang) as feil:
            rute.med_koblinger([(A, B)], [(B, langt)])
        self.assertEqual((feil.exception.fra, feil.exception.til), (B, langt))
        self.assertAlmostEqual(feil.exception.avstand_m, 10.5, delta=0.05)
        self.assertEqual(feil.exception.maks_m, rute.MAKS_KOBLING_M)

    def test_kobling_pa_10_m_godtas(self):  # AD-3
        rute.sjekk_koblinger([(B, nord(B, 9.99))])
        self.assertEqual(rute.med_koblinger([(A, B)], []), [(A, B)])


class GattToGangerTest(unittest.TestCase):
    def test_ren_ring_gir_0(self):  # AD-3, beslutning 4
        self.assertEqual(rute.andel_gatt_to_ganger((A, B, C, D, A)), 0.0)

    def test_samme_vei_tilbake_gir_1(self):  # AD-3
        self.assertEqual(rute.andel_gatt_to_ganger((A, B, C, B, A)), 1.0)

    def test_stilk_gir_andelen_av_lengden(self):  # AD-3, beslutning 4
        # Stilk A–B (ca. 100 m) gås to ganger, ringen B–C–D–B én gang.
        linje = (A, B, C, D, B, A)
        total = rute.linjelengde_m(linje)
        dobbelt = 2 * avstand_m(A, B)
        self.assertAlmostEqual(rute.andel_gatt_to_ganger(linje), dobbelt / total)
        self.assertLess(rute.andel_gatt_to_ganger(linje), rute.MAKS_ANDEL_GATT_TO_GANGER)

    def test_tom_eller_kort_linje_gir_0(self):  # AD-3
        self.assertEqual(rute.andel_gatt_to_ganger(()), 0.0)
        self.assertEqual(rute.andel_gatt_to_ganger((A,)), 0.0)


class OmsamplingTest(unittest.TestCase):
    def test_punkt_hvert_25_m_med_forste_og_siste(self):  # AD-3
        omsamplet = rute.omsampl((A, nord(A, 60), nord(A, 110)))
        avstander = [avstand for avstand, _ in omsamplet]
        lengde = rute.linjelengde_m((A, nord(A, 60), nord(A, 110)))
        self.assertEqual(avstander[:5], [0.0, 25, 50, 75, 100])
        self.assertAlmostEqual(avstander[-1], lengde)
        self.assertEqual(omsamplet[0][1], A)
        self.assertEqual(omsamplet[-1][1], nord(A, 110))
        for avstand, punkt in omsamplet[1:-1]:
            self.assertAlmostEqual(avstand_m(A, punkt), avstand, delta=0.2)

    def test_siste_punkt_tas_ikke_med_to_ganger(self):  # AD-3
        omsamplet = rute.omsampl((A, nord(A, 50)), steg_m=25)
        self.assertEqual(len(omsamplet), 3)


class HoydemeterTest(unittest.TestCase):
    def test_stoy_under_5_m_teller_ikke_men_resten_pa_slutten_gjor(self):  # AD-3
        # Svingninger under 5 m. Nettoen fra ref (100) til siste høyde (102) telles.
        self.assertEqual(rute.hoydemeter_og_nedstigning([100, 103, 101, 104, 99, 102]), (2, 0))

    def test_endring_pa_terskelen_telles(self):  # AD-3
        self.assertEqual(rute.hoydemeter_og_nedstigning([100, 105, 100]), (5, 5))
        self.assertEqual(rute.hoydemeter_og_nedstigning([100, 104.9, 100]), (0, 0))

    def test_stigning_og_nedstigning_med_hysterese(self):  # AD-3
        hoyder = [100, 106, 108, 103, 120, 117, 90, 92]
        # 100→106 (+6), 106→120 (+14, 108 og 103 er støy), 120→90 (−30), rest 90→92 (+2).
        self.assertEqual(rute.hoydemeter_og_nedstigning(hoyder), (22, 30))

    def test_rest_nedover_telles(self):  # AD-3
        self.assertEqual(rute.hoydemeter_og_nedstigning([200, 210, 207]), (10, 3))

    def test_desimaler_gir_ikke_flyttallsfeil(self):  # AD-3
        self.assertEqual(rute.hoydemeter_og_nedstigning([0.1, 5.2, 10.3, 15.4]), (15, 0))
        self.assertEqual(rute.hoydemeter_og_nedstigning([]), (0, 0))


class HoydeprofilTest(unittest.TestCase):
    def test_hele_meter_og_en_desimal(self):  # AD-3
        profil = rute.hoydeprofil([0.0, 25.0, 37.5], [154.2, 147.39, 147.36])
        self.assertEqual(profil, ((0, 154.2), (25, 147.4), (38, 147.4)))
        self.assertIsInstance(profil[0][0], int)

    def test_hele_meter_runder_halv_opp(self):  # AD-3
        self.assertEqual(rute.hele_meter(2.5), 3)
        self.assertEqual(rute.hele_meter(3.5), 4)
        self.assertEqual(rute.hele_meter(2.49), 2)
