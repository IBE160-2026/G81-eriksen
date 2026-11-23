"""Grunnoppsett: tokens, stilark, Toppmeny, knapper, fokusring og Melding.

UX-DR1–5, UX-DR21, UX-DR33, NFR-3, NFR-4, AR-18.
"""

import re
from html.parser import HTMLParser
from pathlib import Path

from django.test import Client, SimpleTestCase, override_settings

ROT = Path(__file__).resolve().parents[2]
STATIC = ROT / "turforslag" / "static"
TOKENS_CSS = STATIC / "css" / "tokens.css"
SIDE_CSS = STATIC / "css" / "side.css"
FORBEDRING_JS = STATIC / "forbedring.js"
MALMAPPER = [ROT / "turforslag" / "templates", ROT / "tests" / "web" / "maler"]

# Faste lister over tokens fra DESIGN.md (frontmatter). UX-DR1.
FARGER_MED_DARK = [
    "background",
    "surface",
    "surface-alt",
    "text",
    "text-muted",
    "primary",
    "on-primary",
    "accent",
    "accent-2",
    "accent-soft",
    "border",
    "input-border",
    "focus-ring",
    "success",
    "info",
    "warning",
    "error",
    "profile-fill",
    "sun",
    "gradient-1",
    "gradient-2",
    "gradient-3",
    "gradient-4",
]
NIVA_MED_DARK = [
    f"level-{niva}{del_}" for niva in ("gronn", "bla", "rod", "svart") for del_ in ("", "-on")
]
KARTLAG_UTEN_DARK = [
    "map-overlay-surface",
    "map-overlay-text",
    "map-overlay-link",
    "map-marker-start",
    "map-route",
    "map-focus-ring",
]
TYPOGRAFIROLLER = [
    "display",
    "headline-lg",
    "headline-md",
    "headline-sm",
    "brand",
    "body-lg",
    "body-md",
    "label",
    "button",
    "fact-value",
    "eyebrow",
    "caption",
]
TYPOGRAFI = [
    f"{rolle}-{egenskap}"
    for rolle in TYPOGRAFIROLLER
    for egenskap in ("font-family", "font-size", "font-weight", "line-height")
] + ["eyebrow-letter-spacing"]
ROUNDED = [f"rounded-{navn}" for navn in ("sm", "md", "lg", "xl", "full")]
SPACING = [f"spacing-{trinn}" for trinn in range(1, 9)]
LAYOUT = [
    "page-margin",
    "breakpoint-stack",
    "touch-target-min",
    "header-min-height",
    "info-column-max-width",
    "info-column-padding",
    "form-max-width",
    "content-max-width",
    "side-illustration-max-width",
    "map-control-size",
]

# CSS-fargenavn (CSS Color 4). `currentColor` og `transparent` er lov.
NAVNGITTE_FARGER = set(
    """aliceblue antiquewhite aqua aquamarine azure beige bisque black blanchedalmond blue
    blueviolet brown burlywood cadetblue chartreuse chocolate coral cornflowerblue cornsilk
    crimson cyan darkblue darkcyan darkgoldenrod darkgray darkgreen darkgrey darkkhaki
    darkmagenta darkolivegreen darkorange darkorchid darkred darksalmon darkseagreen
    darkslateblue darkslategray darkslategrey darkturquoise darkviolet deeppink deepskyblue
    dimgray dimgrey dodgerblue firebrick floralwhite forestgreen fuchsia gainsboro ghostwhite
    gold goldenrod gray green greenyellow grey honeydew hotpink indianred indigo ivory khaki
    lavender lavenderblush lawngreen lemonchiffon lightblue lightcoral lightcyan
    lightgoldenrodyellow lightgray lightgreen lightgrey lightpink lightsalmon lightseagreen
    lightskyblue lightslategray lightslategrey lightsteelblue lightyellow lime limegreen linen
    magenta maroon mediumaquamarine mediumblue mediumorchid mediumpurple mediumseagreen
    mediumslateblue mediumspringgreen mediumturquoise mediumvioletred midnightblue mintcream
    mistyrose moccasin navajowhite navy oldlace olive olivedrab orange orangered orchid
    palegoldenrod palegreen paleturquoise palevioletred papayawhip peachpuff peru pink plum
    powderblue purple rebeccapurple red rosybrown royalblue saddlebrown salmon sandybrown
    seagreen seashell sienna silver skyblue slateblue slategray slategrey snow springgreen
    steelblue tan teal thistle tomato turquoise violet wheat white whitesmoke yellow
    yellowgreen""".split()
)
HEX = re.compile(r"(?<!&)#[0-9a-fA-F]{3,8}\b")  # ikke HTML-entiteter som &#8211;
FARGEFUNKSJON = re.compile(r"\b(rgba?|hsla?|hwb|lab|lch|oklab|oklch|color)\(", re.IGNORECASE)
SVG_FARGEATTRIBUTT = re.compile(
    r"\s(fill|stroke|stop-color|color|flood-color|lighting-color)\s*=\s*([\"'])(.*?)\2",
    re.IGNORECASE,
)


def uten_kommentarer(css):
    return re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)


def regler(css):
    """Enkel CSS-leser: liste over (media, selektorer, deklarasjoner). Tåler ett nivå @media."""
    resultat = []

    def les_blokk(tekst, media):
        pos = 0
        while True:
            start = tekst.find("{", pos)
            if start == -1:
                return
            hode = tekst[pos:start].strip()
            dybde, slutt = 1, start + 1
            while dybde:
                dybde += {"{": 1, "}": -1}.get(tekst[slutt], 0)
                slutt += 1
            kropp = tekst[start + 1 : slutt - 1]
            if hode.startswith("@media"):
                les_blokk(kropp, hode)
            else:
                deklarasjoner = {}
                for linje in kropp.split(";"):
                    navn, kolon, verdi = linje.partition(":")
                    if kolon:
                        deklarasjoner[navn.strip()] = " ".join(verdi.split())
                selektorer = [s.strip() for s in hode.split(",")]
                resultat.append((media, selektorer, deklarasjoner))
            pos = slutt

    les_blokk(uten_kommentarer(css), None)
    return resultat


def deklarasjoner_for(css, selektor, media=None):
    samlet = {}
    for regel_media, selektorer, deklarasjoner in regler(css):
        if regel_media == media and selektor in selektorer:
            samlet.update(deklarasjoner)
    return samlet


class Tagger(HTMLParser):
    """Samler alle starttagger med attributter, og teksten i Melding-titlene."""

    def __init__(self):
        super().__init__()
        self.tagger = []
        self.meldinger = []
        self._venter_tittel = False

    def handle_starttag(self, tag, attrs):
        attributter = dict(attrs)
        self.tagger.append((tag, attributter))
        klasser = (attributter.get("class") or "").split()
        if tag == "div" and "melding" in klasser:
            self.meldinger.append({"attrs": attributter, "svg": None, "tittel": ""})
        elif tag == "svg" and self.meldinger and self.meldinger[-1]["svg"] is None:
            self.meldinger[-1]["svg"] = attributter
        elif tag == "p" and "melding-tittel" in klasser:
            self._venter_tittel = True

    def handle_data(self, data):
        if self._venter_tittel:
            self.meldinger[-1]["tittel"] += data
            self._venter_tittel = False

    def finn(self, tag, **krav):
        return [
            attrs
            for navn, attrs in self.tagger
            if navn == tag and all(attrs.get(k.replace("_", "-")) == v for k, v in krav.items())
        ]


def les_html(svar):
    tagger = Tagger()
    tagger.feed(svar.content.decode())
    return tagger


class SideTest(SimpleTestCase):
    def assert_toppmeny(self, svar):
        tagger = les_html(svar)
        self.assertEqual(len(tagger.finn("header")), 1)
        self.assertEqual(len(tagger.finn("nav", aria_label="Hovedmeny")), 1)
        logo = tagger.finn("a", **{"class": "logo"})
        self.assertEqual(len(logo), 1)
        self.assertEqual(logo[0]["href"], "/")
        stilark = [attrs["href"] for attrs in tagger.finn("link", rel="stylesheet")]
        self.assertEqual(len(stilark), 2)
        self.assertTrue(stilark[0].endswith("css/tokens.css"))
        self.assertTrue(stilark[1].endswith("css/side.css"))
        return tagger

    def test_sok_har_toppmeny_og_aktiv_logo(self):  # UX-DR2, UX-DR3
        svar = self.client.get("/")
        tagger = self.assert_toppmeny(svar)
        logo = tagger.finn("a", **{"class": "logo"})[0]
        self.assertEqual(logo.get("aria-current"), "page")
        self.assertContains(svar, "<main>", count=1)
        self.assertContains(svar, "Your Next Adventure</span>")

    def test_forbedring_lastes_med_defer(self):  # AR-18
        skript = les_html(self.client.get("/")).finn("script")
        self.assertEqual(len(skript), 1)
        self.assertTrue(skript[0]["src"].endswith("forbedring.js"))
        self.assertIn("defer", skript[0])

    def test_404_har_toppmeny_uten_aria_current(self):  # UX-DR3
        svar = self.client.get("/finnes-ikke/")
        self.assertEqual(svar.status_code, 404)
        self.assert_toppmeny(svar)
        self.assertNotContains(svar, "aria-current", status_code=404)

    def test_403_har_toppmeny_uten_aria_current(self):  # UX-DR3
        svar = Client(enforce_csrf_checks=True).post("/")
        self.assertEqual(svar.status_code, 403)
        self.assert_toppmeny(svar)
        self.assertNotContains(svar, "aria-current", status_code=403)

    @override_settings(ROOT_URLCONF="tests.web.urls_feil")
    def test_500_har_toppmeny_uten_aria_current(self):  # UX-DR3
        with self.assertLogs("django.request", "ERROR"):
            svar = Client(raise_request_exception=False).get("/feil/")
        self.assertEqual(svar.status_code, 500)
        self.assert_toppmeny(svar)
        self.assertNotContains(svar, "aria-current", status_code=500)

    def test_basismalen_bruker_ikke_url_oppslag(self):  # 500-siden skal virke uten oppslag
        base = (ROT / "turforslag" / "templates" / "base.html").read_text(encoding="utf-8")
        self.assertNotIn("{% url", base)


@override_settings(ROOT_URLCONF="tests.web.urls_komponenter")
class KomponenterTest(SimpleTestCase):
    def meldinger(self):
        svar = self.client.get("/komponenter/")
        self.assertEqual(svar.status_code, 200)
        return {melding["tittel"]: melding for melding in les_html(svar).meldinger}

    def test_knapper(self):  # UX-DR4
        tagger = les_html(self.client.get("/komponenter/"))
        self.assertEqual(len(tagger.finn("button", **{"class": "knapp-primaer"})), 1)
        self.assertEqual(len(tagger.finn("button", **{"class": "knapp-sekundaer"})), 1)
        self.assertEqual(tagger.finn("a", **{"class": "logo"})[0].get("aria-current"), None)

    def test_post_sender_videre(self):  # PRG
        svar = self.client.post("/komponenter/", {"handling": "primaer"})
        self.assertRedirects(svar, "/komponenter/", fetch_redirect_response=False)

    def test_melding_pa_samme_side(self):  # UX-DR21
        meldinger = self.meldinger()
        for type_, rolle in (
            ("Info", "status"),
            ("Advarsel", "alert"),
            ("Feil", "alert"),
            ("Suksess", "status"),
        ):
            with self.subTest(type=type_):
                melding = meldinger[f"{type_} på siden"]
                self.assertEqual(melding["attrs"].get("role"), rolle)
                self.assertIn(f"melding-{type_.lower()}", melding["attrs"]["class"].split())
                self.assertNotIn("tabindex", melding["attrs"])
                self.assertNotIn("data-fokus", melding["attrs"])
                self.assertEqual(melding["svg"].get("aria-hidden"), "true")

    def test_melding_etter_navigering(self):  # UX-DR21
        meldinger = self.meldinger()
        for type_ in ("Info", "Advarsel", "Feil", "Suksess"):
            with self.subTest(type=type_):
                melding = meldinger[f"{type_} etter navigering"]
                self.assertNotIn("role", melding["attrs"])
                self.assertEqual(melding["attrs"].get("tabindex"), "-1")
                self.assertIn("data-fokus", melding["attrs"])
                self.assertEqual(melding["svg"].get("aria-hidden"), "true")

    def test_melding_har_tekst_bare_nar_den_er_gitt(self):  # UX-DR21
        svar = self.client.get("/komponenter/")
        self.assertContains(svar, '<p class="melding-tekst">Brødtekst til feil.</p>', html=True)
        self.assertContains(svar, 'class="melding-tekst"', count=3)


class TokensTest(SimpleTestCase):
    def setUp(self):
        self.tokens = deklarasjoner_for(TOKENS_CSS.read_text(encoding="utf-8"), ":root")

    def test_tokens_css_har_bare_root(self):  # UX-DR1
        alle = regler(TOKENS_CSS.read_text(encoding="utf-8"))
        self.assertEqual(
            [(media, selektorer) for media, selektorer, _ in alle], [(None, [":root"])]
        )

    def test_alle_tokens_finnes(self):  # UX-DR1
        for navn in TYPOGRAFI + ROUNDED + SPACING + LAYOUT + KARTLAG_UTEN_DARK:
            with self.subTest(token=navn):
                self.assertIn(f"--{navn}", self.tokens)

    def test_farger_og_turniva_har_dark_par(self):  # UX-DR1
        for navn in FARGER_MED_DARK + NIVA_MED_DARK:
            with self.subTest(token=navn):
                self.assertIn(f"--{navn}", self.tokens)
                self.assertIn(f"--{navn}-dark", self.tokens)

    def test_kartlag_har_ikke_dark_par(self):  # UX-DR1, DESIGN.md › Kartlag
        for navn in KARTLAG_UTEN_DARK:
            with self.subTest(token=navn):
                self.assertNotIn(f"--{navn}-dark", self.tokens)

    def test_utvalgte_verdier(self):  # UX-DR1
        self.assertEqual(self.tokens["--focus-ring"].lower(), "#b0624a")
        self.assertEqual(self.tokens["--touch-target-min"], "44px")
        self.assertEqual(self.tokens["--rounded-md"], "8px")
        self.assertEqual(self.tokens["--page-margin"], "clamp(16px, 5vw, 64px)")


class StilarkTest(SimpleTestCase):
    def setUp(self):
        self.css = SIDE_CSS.read_text(encoding="utf-8")

    def test_ingen_fargeverdier_utenfor_tokens_css(self):  # UX-DR1
        css_filer = [fil for fil in sorted(STATIC.rglob("*.css")) if fil != TOKENS_CSS]
        self.assertIn(SIDE_CSS, css_filer)
        for fil in css_filer:
            tekst = uten_kommentarer(fil.read_text(encoding="utf-8"))
            with self.subTest(fil=fil.name):
                self.assertIsNone(HEX.search(tekst))
                self.assertIsNone(FARGEFUNKSJON.search(tekst))
                for _, _, deklarasjoner in regler(tekst):
                    for verdi in deklarasjoner.values():
                        ord_ = re.findall(
                            r"(?<![\w-])[a-z]+(?![\w-])", re.sub(r"var\([^)]*\)", "", verdi.lower())
                        )
                        self.assertFalse(NAVNGITTE_FARGER & set(ord_), verdi)

    def test_ingen_fargeverdier_i_malene(self):  # UX-DR1
        maler = [mal for mappe in MALMAPPER for mal in sorted(mappe.rglob("*.html"))]
        self.assertTrue(maler)
        for mal in maler:
            tekst = mal.read_text(encoding="utf-8")
            with self.subTest(mal=mal.name):
                self.assertIsNone(HEX.search(tekst))
                self.assertIsNone(FARGEFUNKSJON.search(tekst))
                for _, _, verdi in SVG_FARGEATTRIBUTT.findall(tekst):
                    self.assertRegex(verdi, r"^(currentColor|none|url\(#[\w-]+\))$")

    def test_fokusring(self):  # UX-DR5
        fokus = deklarasjoner_for(self.css, ":focus-visible")
        self.assertEqual(fokus["outline"], "3px solid var(--focus-ring)")
        self.assertEqual(fokus["outline-offset"], "2px")

    def test_fokusringen_fjernes_aldri(self):  # UX-DR5
        for _, selektorer, deklarasjoner in regler(self.css):
            with self.subTest(selektorer=selektorer):
                for navn in ("outline", "outline-style", "outline-width"):
                    verdi = deklarasjoner.get(navn, "").replace("!important", "").strip()
                    self.assertNotRegex(verdi, r"^(none|0(px)?)\b")

    def test_reduced_motion_slar_av_bevegelse(self):  # UX-DR33
        media = "@media (prefers-reduced-motion: reduce)"
        bevegelse = deklarasjoner_for(self.css, "*", media)
        self.assertEqual(bevegelse["animation"], "none !important")
        self.assertEqual(bevegelse["transition"], "none !important")

    def test_knapper_er_minst_44_px_med_8_px_hjorner(self):  # UX-DR4, NFR-3
        for knapp in (".knapp-primaer", ".knapp-sekundaer"):
            with self.subTest(knapp=knapp):
                regel = deklarasjoner_for(self.css, knapp)
                self.assertEqual(regel["min-height"], "var(--touch-target-min)")
                self.assertEqual(regel["min-width"], "var(--touch-target-min)")
                self.assertEqual(regel["border-radius"], "var(--rounded-md)")

    def test_display_og_headline_lg_er_28_px_under_720_px(self):  # UX-DR2, DESIGN.md › Typography
        for selektor in ("h1", ".display", ".headline-lg"):
            with self.subTest(selektor=selektor):
                regel = deklarasjoner_for(self.css, selektor, "@media (max-width: 719.98px)")
                self.assertEqual(regel["font-size"], "28px")

    def test_ingen_overflow_hidden(self):  # NFR-4, WCAG 1.4.10 og 1.4.12
        for _, selektorer, deklarasjoner in regler(self.css):
            for navn in ("overflow", "overflow-x", "overflow-y"):
                with self.subTest(selektorer=selektorer, egenskap=navn):
                    verdi = deklarasjoner.get(navn, "").replace("!important", "")
                    self.assertNotRegex(verdi, r"\b(hidden|clip)\b")

    def test_logomerket_far_gradient_fra_tokens(self):  # UX-DR3
        for trinn in range(1, 5):
            regel = deklarasjoner_for(self.css, f".logo-stopp-{trinn}")
            self.assertEqual(regel["stop-color"], f"var(--gradient-{trinn})")


class ForbedringTest(SimpleTestCase):
    def test_sperre_og_fokus(self):  # AR-18, UX-DR21. Oppførselen sjekkes manuelt i Chrome.
        js = FORBEDRING_JS.read_text(encoding="utf-8")
        self.assertIn('addEventListener("submit"', js)
        self.assertIn('setAttribute("aria-disabled", "true")', js)
        self.assertIn("preventDefault()", js)
        self.assertIn('querySelector("[data-fokus]")', js)
        self.assertNotIn("import ", js)
