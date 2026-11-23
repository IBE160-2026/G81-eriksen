---
title: 'Story 1.3: Siden har et rolig og tilgjengelig grunnoppsett'
type: 'feature'
created: '2026-11-23'
status: 'done'
baseline_commit: '70d5b68719811d6b52289d2f08e280d21e1daf6c'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-1-context.md'
  - '{project-root}/_bmad-output/planning-artifacts/ux-designs/ux-G81-eriksen-2026-11-06/DESIGN.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** `base.html` har bare `lang`, tittel og `main`. Det finnes ingen CSS, ingen designtokens, ingen toppmeny og ingen felles komponenter. Alle senere sider trenger et rolig og tilgjengelig grunnoppsett å bygge på (UX-DR1–5, UX-DR21, UX-DR33, NFR-3, NFR-4, AR-18).

**Approach:** Tokens fra `DESIGN.md` blir CSS-variabler i én fil. Basismalen får header med nav og logo, og et felles stilark for grunnoppsett, knapper, fokus, Melding og responsivitet. `forbedring.js` får sperren mot dobbeltinnsending. Melding blir en gjenbrukbar delmal.

**Beslutninger (Hannah, 2026-11-23):**
- Knapp, sperren og Melding testes med testmaler og en test-URLconf (`tests/web/urls_komponenter.py`, samme mønster som `urls_feil.py`). Appen får ingen synlig komponentside. `forbedring.js` sjekkes manuelt i Chrome med en midlertidig lokal side som ikke committes.
- UU-verktøyet er Lighthouse via `npx` med installert Chrome (`--only-categories=accessibility`), kjørt mot `runserver`. Ingenting kommer i repoet, og resultatet legges i PR-en.
- Specen beholdes hel (ca. 2500–3000 tokens).

## Boundaries & Constraints

**Always:**
- Tokens:
  - `turforslag/static/css/tokens.css` har bare `:root` med alle tokens fra frontmatter i `DESIGN.md`. Navnene følger token-navnene der.
  - Farger og turnivå har `-dark`-par, men kartlagene har ikke det. Typografirollene har størrelse, vekt og linjehøyde, med systemfontstablene. Spacing 1–8, `rounded` og layout er også med.
  - Ingen fargeverdi (hex, `rgb()`, `hsl()` eller navngitt farge) står utenfor `tokens.css`, heller ikke i SVG i malene. Bruk `currentColor` eller `var()`.
- CSP-en er uendret. Det er ingen inline-skript, ingen `<style>` og ingen `style=` eller `on*=`. CSS og JS lenkes med `{% static %}`, og JS lastes med `defer`.
- Grunnoppsettet er flytende:
  - Ingen faste høyder med `overflow: hidden`, og ingen sidelengs rulling ved 320 px, 200 % tekstzoom eller WCAG 1.4.12-avstand.
  - Display og `headline-lg` er 28 px under 720 px. Breakpointet skrives direkte i `@media`.
- Fokusring: `:focus-visible { outline: 3px solid var(--focus-ring); outline-offset: 2px }`. Den fjernes aldri, heller ikke med `outline: none` andre steder.
- `@media (prefers-reduced-motion: reduce)` slår av all animasjon og overgang.
- Knapper:
  - `.knapp-primaer` og `.knapp-sekundaer` er minst 44 × 44 px med `rounded-md` (8 px), etter `DESIGN.md`.
  - `forbedring.js` setter `aria-disabled="true"` på innsendingsknappen ved første `submit` og stopper senere `submit` på samme skjema. Knappen beholder fokus. Uten JS sendes skjemaet som vanlig.
- Melding (`turforslag/templates/turforslag/_melding.html`, brukt med `{% include … with %}`):
  - Typen er info, advarsel, feil eller suksess, med tittel, tekst og ikon (sirkel med «i», «!» eller hake, inline SVG med `aria-hidden="true"` og `currentColor`).
  - 4 px venstrekant i statusfargen.
  - På samme side: `role="status"` (info/suksess) eller `role="alert"` (advarsel/feil).
  - Etter navigering (`fokus=True`): ingen `role`, men `tabindex="-1"` og `data-fokus`. `forbedring.js` gir den fokus ved innlasting.
- Toppmeny:
  - `<header>` med `<nav aria-label="Hovedmeny">`. Logoen (ordmerket «Your Next Adventure» og et gradientmerke med `stop-color` fra CSS-variabler) er en lenke til `/`, med fast adresse som i `500.html`.
  - På Søk får logolenken `aria-current="page"`.
  - Menyen bryter linje uten hamburgermeny.
- Eksisterende tester for sider, CSP og maler fortsetter å virke. `main` og `h1` beholdes uten attributter, eller testene oppdateres med samme hensikt.

**Never:**
- Menypunktene «Logg inn», «Finn tur», «Historikk» og «Konto» kommer i Epic 2. Mørk modus kommer i Epic 6, og `-dark`-variablene defineres bare.
- Ingen nye Python-pakker, ingen Node eller `package.json` i repoet og ingen eksterne fonter.
- Ingen endring av `SECURE_CSP`, migreringene, `_bmad/`, `.claude/` eller planleggingsartefaktene.
- Ingen toast. Ingen `outline: none` uten en synlig erstatning.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Søk | GET `/` | header/nav, én `main`, logolenke med `aria-current="page"`, `tokens.css` + stilark + `forbedring.js` lenket | N/A |
| Feilside | 404, 403 eller 500 | Samme header uten `aria-current`. 500 bruker ingen URL-oppslag i basismalen | N/A |
| Melding på siden | `type="feil"` | `role="alert"`, tittel, ikon `aria-hidden` | N/A |
| Melding etter navigering | `type="suksess" fokus=True` | ingen `role`, `tabindex="-1"`, `data-fokus` | N/A |
| Dobbeltklikk | to `submit` raskt | én innsending, knappen `aria-disabled="true"` med fokus | Uten JS: vanlig innsending |

</frozen-after-approval>

## Code Map

- `turforslag/templates/base.html` -- 14 linjer. Har `lang="nb"`, tittelblokken `tittel` med « – Your Next Adventure» og `<main>{% block innhold %}`. Får `{% load static %}`, lenker, header og nav. Blokknavnene skal beholdes.
- `turforslag/templates/500.html` -- lenker til `/`, fordi URL-oppslaget kan være feilen. Basismalen må heller ikke bruke `{% url %}`. `request` kan mangle her, så sjekken for `aria-current` må tåle at den er borte (`request.resolver_match.url_name == "sok"`).
- `turforslag/templates/turforslag/sok.html` -- har bare `h1`. Ikke endre teksten.
- `turforslag/static/` -- finnes ikke. Opprettes med `css/tokens.css`, `css/side.css` og `forbedring.js`. Filene finnes via APP_DIRS-finderen, siden `STATICFILES_DIRS` mangler. `kart.js` og `vendor/` kommer i 1.10.
- `config/settings.py:95-102` -- `SECURE_CSP`. Ikke endre.
- `tests/web/test_sider.py` -- `assertContains("<main>", count=1)` og `"<h1>"` count=1, eksakt markup, og `LENKE_TIL_SOK = '<a href="/">Gå til Søk</a>'`. Logolenken må ha annen tekst, så den ikke gir et dobbelt treff.
- `tests/web/test_innstillinger.py` -- `test_malene_har_ingen_inline_stil_eller_skript` går gjennom alle maler. Mønster for nye tester: `SimpleTestCase`, krav-ID i en kommentar, og stier via `Path(__file__).resolve().parents[2]`.
- `DESIGN.md` frontmatter, linje 14–176 -- alle tokens. Komponentene står i linje 178–209 (toppmeny og knapper) og 341–350 (Melding). Ikonene i Melding står i linje 595. Logomerket står i linje 433 og 559, og mocken `mockups/key-historikk.html` linje 92–109.
- `EXPERIENCE.md` linje 192–195 og 213 (komponenter), og linje 353–373 (tilgjengelighetskravene).

## Tasks & Acceptance

**Execution:**
- [x] `turforslag/static/css/tokens.css` -- alle tokens fra `DESIGN.md` som variabler i `:root` -- UX-DR1
- [x] `turforslag/static/css/side.css` -- grunnoppsett (systemfonter, `page-margin`, `content-max-width`), typografiroller, toppmeny, knapper, fokusring, Melding, 28 px under 720 px og reduced-motion. Bare `var()` for farger -- UX-DR2–5, 21, 33, NFR-3, NFR-4
- [x] `turforslag/static/forbedring.js` -- sperre mot dobbeltinnsending og fokus på `[data-fokus]`. Ren ES, uten avhengigheter, og den feiler stille -- AR-18, UX-DR21
- [x] `turforslag/templates/base.html` -- lenker, header, nav og logo (inline SVG uten farger), `aria-current` på Søk -- UX-DR2, UX-DR3
- [x] `turforslag/templates/turforslag/_melding.html` -- komponenten Melding etter matrisen -- UX-DR21
- [x] `tests/web/urls_komponenter.py` og testmalen `tests/web/maler/komponenter.html` (eller tilsvarende, lagt inn med `override_settings`) -- skjema med én primærknapp og én sekundærknapp, og Melding i alle fire typer og begge modusene. Den brukes av testene og ved den manuelle sjekken av `forbedring.js` -- UX-DR4, UX-DR21
- [x] `tests/web/test_grunnoppsett.py` -- tester for matrisen, at alle token-navn (en fast liste i testen) finnes i `tokens.css` med `-dark` der det skal være, at det ikke er noen fargeverdier utenfor `tokens.css` (CSS og maler), fokusregelen, reduced-motion, 44 px og 28 px-regelen, og at `forbedring.js` lastes med `defer` -- UX-DR1–5, 21, 33
- [x] `README.md` -- én linje om hvor stilene og tokens ligger, og status for story 1.3 -- AD-12 punkt 6

**Acceptance Criteria:**
- Gitt en hvilken som helst side, når den vises ved 320 px, 200 % zoom og 1.4.12-avstand, så ruller den ikke sidelengs, og ingen tekst klippes.
- Gitt tastaturbruk, når Tab trykkes på Søk, så får logolenken en synlig fokusring på 3 px.
- Gitt forsiden, når UU-verktøyet kjøres, så finner det ingen feil, og resultatet legges i PR-en.

## Implementation Notes

- 2026-11-23: Hannah godkjente specen og valgte å beholde den hel.
- 2026-11-23 (implementering): `aria-current` på logoen settes med blokken `logo_aktiv` i `sok.html`, ikke med `request.resolver_match`. Grunnen: CSRF-feil ved POST til `/` gir 403-siden med `resolver_match` for Søk, og da fikk feilsiden `aria-current`. Blokken virker også på 500-siden uten `request`.
- 2026-11-23 (implementering): `h1` får `headline-lg` som standard. Søk-overskriften får rollen `display` når skjemaet kommer i 1.9, så `h1` i `sok.html` er uendret.

- 2026-11-23 (verifisering): 93 tester er grønne, og Ruff og migreringssjekken er rene.
  - Lighthouse 12.8.2 (`npx`, Chrome uten vindu, bare tilgjengelighet) mot `/` gir 100 og ingen feilede revisjoner. JSON-fila ligger utenfor repoet og legges i PR-en.
  - Manuelt i Chrome: et dobbeltklikk gir én POST med `aria-disabled` og beholdt fokus, og `data-fokus` får fokus. Reflow ved 320 CSS-px med tekstavstand etter 1.4.12 er sjekket via zoom.
  - Gjenstår manuelt: reduced-motion i DevTools, og 320 px og 200 % i et ekte vindu. Statiske filer på Vercel sjekkes på forhåndsvisningen av PR-en.

## Spec Change Log

## Review Triage Log

Første gjennomgang (2026-11-23). B = Blind Hunter, E = Edge Case Hunter, V = Verification Gap.

| # | Funn | Verdikt | Begrunnelse | Rute |
|---|---|---|---|---|
| V1/B5 | `forbedring.js` testes bare som tekst. Sperren, `pageshow` og fokus kjøres aldri i en test, og det mangler en oppskrift for den manuelle sjekken | medium | Det er reelt: en snudd betingelse ville passert testene. Den frosne beslutningen sier at JS sjekkes manuelt, og repoet har ingen JS-kjører. Sjekken i Chrome er gjort (én POST ved dobbeltklikk, fokus på `data-fokus`) | defer |
| V-a | Ingenting sjekker at de statiske filene serveres på Vercel | maybe-false | Dette er første story med statiske filer. Det avgjøres ved å hente `/static/css/tokens.css` på forhåndsvisningen av PR-en | defer (sjekkes på forhåndsvisningen) |
| B11 | De statiske filene har ingen cache-busting, så endringer kan nå brukerne sent | maybe-false | Det avhenger av `Cache-Control` fra Vercel for `/static/`. Det avgjøres ved å lese hodet på forhåndsvisningen. Hvis det stemmer, er det medium | defer |
| E1/B6a | Sperren slippes aldri når innsendingen ikke navigerer (`target=_blank`, nedlasting, 204, Esc) | low | Alle skjemaene i appen følger PRG med navigering. Esc under innsending er sjeldent, og rettingen (tidsavbrudd eller vakt) gir mer kompleksitet | avvist |
| E2 | En annen lytter kan kalle `preventDefault` etter at skjemaet er sperret | false | Det finnes ingen andre submit-lyttere. AD-1 tillater bare `kart.js` og `forbedring.js`, og `kart.js` har ingen skjemaer | avvist |
| E3 | Uten `submitter` (Safari før 15.4) merkes første knapp | low | Bare `aria-disabled` havner på feil knapp i gamle nettlesere, og rettingen gir en ny lytter | avvist |
| E4 | Bare første `[data-fokus]` får fokus | low | Med vilje: høyst én Melding etter navigering, rett under `h1` (EXPERIENCE.md linje 369). Dokumentert i delmalen | patch |
| E5/B7a | Ukjent `type` i Melding gir `role=alert` og ingen statusfarge | low | Det skjer bare ved en skrivefeil hos utvikleren. Rettingen (en vakt eller reserveverdi) skjuler feilen i stedet for å vise den | avvist |
| B7b | `fokus=True` uten JS gir verken `role` eller fokus | low | Den frosne matrisen bestemmer dette («ingen role»). Meldingen står rett under `h1` og leses i rekkefølge. Rettingen ville endret specen | avvist |
| E6 | Testparseren tar mellomrom som tittel når tittelen er tom | low | Testsiden har alltid titler, og dette treffer ikke i bruk | avvist |
| E7/B9a | CSS-parseren i testen tåler ikke ubalanserte klammer, strenger, `url()` eller nøstede at-regler | low | `side.css` har ingenting av dette, og rettingen gjør testhjelperen mer kompleks | avvist |
| E8/B9b | Testene for fokusring og overflow overser `!important`, `0px`, `clip` og verdier med to ledd | low | Rettingen i regex er direkte | patch |
| E9/B2 | Fargetesten for maler overser `style="color:…"` og `fill='red'` med enkle anførselstegn | low | `style=` er allerede forbudt av `test_malene_har_ingen_inline_stil_eller_skript`. Enkle anførselstegn er et reelt hull, og rettingen er direkte | patch |
| B2b | `forbedring.js` sjekkes ikke for fargeverdier | low | Skriptet setter ingen stiler, og en slik sjekk er ny kompleksitet | avvist |
| B3 | `HEX` slår ut på `&#8211;` | low | Det ville gitt en falsk feil ved første numeriske entitet, og lookbehind er en direkte retting | patch |
| B1a | Statuslinja i README sier «til gjennomgang» og blir utdatert | low | Den er direkte å rette | patch |
| B1b | README sier at `config/` og `tests/` «kommer med implementeringen» | low | Teksten fantes før denne storyen (fra 1.1), og den står allerede som åpent punkt i `issues.md` (mappestruktur i README) | defer |
| B4 | Token-listene i testen er kopiert for hånd fra DESIGN.md | low | Specen sier «en fast liste i testen». Rettingen ville endret specen | avvist |
| B6b | `vedVisning` fjerner `aria-disabled` fra alle knapper i skjemaet | low | Ingen knapp får `aria-disabled` fra serveren, så det er en vakt mot en tilstand som ikke finnes | avvist |
| B6c | Ingen synlig «Sender…»-tilstand, bare `cursor: progress` | low | EXPERIENCE.md linje 193 definerer bare `aria-disabled` og fokus, ingen visuell tilstand | avvist |
| B8a | Ingen «Hopp til innhold»-lenke | low | Landemerkene (`header`, `nav`, `main`) dekker 2.4.1, og menyen har bare logoen. Lighthouse består | avvist |
| B8b | Logoen står ikke på linje med innholdet på brede skjermer | false | Mocken (`key-historikk.html` linje 51 og 59) har nøyaktig samme oppsett: headeren i full bredde med 64 px marg, og innholdet sentrert på 960 px | avvist |
| B9c | Hardkodet 28 px, 600, 20 px og 1.5 px, en overgang uten virkning og ingen `:active` | low | Regelen i specen gjelder bare farger. Verdiene følger DESIGN.md, og ingen konkret skade er vist | avvist |
| B10 | Fjellet i logoen glir over i sirkelen | false | Merket er identisk med mocken (`key-historikk.html` linje 93: samme gradient, fjellet i `#355146`) | avvist |

## Design Notes

- I Epic 1 er logoen det eneste i `nav`. Derfor får den `aria-current="page"` på Søk. Når «Finn tur» kommer i Epic 2, flyttes `aria-current` dit.
- Gradientmerket: `<stop class="logo-stopp-1">` i SVG, og i `side.css` `.logo-stopp-1 { stop-color: var(--gradient-1) }`. Ingen hex i malen.
- Det finnes ingen faste titler per Melding-type. Tittelen sendes inn fra Mikrotekst.

## Verification

**Commands:**
- `python manage.py test` -- forventet: alle grønne
- `ruff check . && ruff format --check .` -- forventet: ingen funn
- `npx lighthouse http://127.0.0.1:8000/ --only-categories=accessibility --chrome-flags="--headless" --output=json` (kjøres utenfor repoet, med `runserver` i gang) -- forventet: poengsum 100 og ingen feilede revisjoner

**Manual checks:**
- I Chrome:
  - 320 px, 200 % zoom og et bokmerke med tekstavstand etter 1.4.12 gir ingen sidelengs rulling.
  - Tab viser fokusringen.
  - Et dobbeltklikk på primærknappen gir én innsending.
  - Med reduced-motion emulert er det ingen bevegelse.
