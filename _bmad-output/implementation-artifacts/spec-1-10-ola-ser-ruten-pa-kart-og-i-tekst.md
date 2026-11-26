---
title: 'Story 1.10: Ola ser ruten på kart og i tekst'
type: 'feature'
created: '2026-11-26'
status: 'done'
baseline_commit: 'e6bac6575df060241340bcfa03210d9533c225df'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-1-context.md'
  - '{project-root}/_bmad-output/planning-artifacts/ux-designs/ux-G81-eriksen-2026-11-06/EXPERIENCE.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Turforslaget (1.9) viser ikke hvor turen går. Ola trenger ruten på et norsk turkart og en tekstversjon som virker med tastatur, skjermleser og uten JS (FR-6, AR-10, UX-DR12, UX-DR13, UX-DR15).

**Approach:**
- Leaflet 1.9.4 legges inn i `turforslag/static/vendor/leaflet/`.
- `kart.js` tegner turens GeoJSON fra `json_script` på Kartverkets topokart.
- Malen renderer kartflaten, kontrollene, krediteringen og en melding for når kartet ikke kan vises.
- `domene/` lager «Kartet i tekst» og laveste og høyeste punkt.
- Forslagssiden får to kolonner med sticky kart fra 720 px.

**Beslutninger (Hannah, 2026-11-26):**
1. **Berøring (1A):** en liten handler i `kart.js` (ca. 30 linjer, ingen plugin).
   - På berøringsskjerm er flytting med én finger slått av (`dragging` er av ved berøring), og én finger viser hintet «Bruk to fingre for å flytte kartet» i 1,5 s uten å blokkere rullingen av siden.
   - Når to fingre er på skjermen, slås `map.dragging` på, og når fingrene slippes, slås den av igjen. Klyping zoomer som vanlig (`touchZoom`).
   - Avviket fra «Leaflets innebygde valg» føres i `.memlog.md` med begrunnelse.
2. **Nedlasting:** Hannah godkjenner nedlasting av `leaflet.js`, `leaflet.css` og `LICENSE` for leaflet@1.9.4 fra `cdn.jsdelivr.net/npm/leaflet@1.9.4/`. Filene committes uendret.

Spec-en beholdes hel (ca. 3600 tokens).

## Boundaries & Constraints

**Always:**
- **Leaflet 1.9.4** fra `turforslag/static/vendor/leaflet/`: `leaflet.js`, `leaflet.css` og `LICENSE` (BSD-2), uendret. Ingen `images/`: startmarkøren er en `divIcon` med «S» og CSS-klasse. Ingen CDN, ingen npm og ingen plugin.
- **`turforslag/static/kart.js`:**
  - Det er den andre og siste egne JS-fila (AD-1).
  - Den er ES5-stil, ligger i en IIFE med `try/catch` og leser GeoJSON fra `json_script`. Den filtrerer, beregner og henter ingenting annet enn fliser.
  - Kartet bygges med `attributionControl: false`, maks zoom 18 og fliser fra `https://cache.kartverket.no/v1/wmts/1.0.0/topo/default/webmercator/{z}/{y}/{x}.png`. Hele ruten vises.
  - Den eksporterer `window.YNAKart.start(element)`, så 1.11 kan starte kartet på nytt etter et fragmentbytte.
- **Farger bare i CSS:**
  - Rutelinjen er plommelilla, 5 px på 9 px hvit kant. Det løses med to polylinjer med `className`, og CSS-en bruker kart-tokenene fra `tokens.css` (`--map-*`).
  - Ingen fargeverdier i `kart.js`.
- **Malen** (`forslag.html` og en include for kartet):
  - Kartflaten har `tabindex="0"`, `role="region"` og `aria-label="Kart over {turnavn}"`.
  - Lenken «Kartet i tekst» står oppe til venstre. «Vis hele ruten» og zoom + og − står oppe til høyre, med `aria-label` «Zoom inn» og «Zoom ut», alle 44 × 44 px. Målestokken står nede til venstre.
  - Krediteringen renderes på serveren nede til høyre og er alltid synlig: «© Kartverket» med lenke til `https://www.kartverket.no/api-og-data/vilkar-for-bruk` og «© OpenStreetMap contributors» med lenke til `https://www.openstreetmap.org/copyright` og `lang="en"`. Begge er understreket.
  - Kontrollene er knapper i malen (ikke Leaflets), og `kart.js` kobler dem til. Uten JS er de skjult.
- **Uten JS eller ved feil i flisene:** kartflaten viser Melding (info) «Kartet kunne ikke lastes. Ruten er beskrevet i "Kartet i tekst".» med en lenke til `#kartet-i-tekst` og «Prøv igjen».
  - Uten JS er «Prøv igjen» en lenke til samme side.
  - Med JS prøver `kart.js` å laste flisene på nytt.
  - Krediteringen står fortsatt, og resten av forslaget vises som vanlig.
- **Tastatur:** rekkefølgen er «Kartet i tekst», kartflaten, «Vis hele ruten», zoom og krediteringslenkene. Piltastene flytter kartet, og + og − zoomer (Leaflets `keyboard`). Tab fører alltid ut av kartet. Markørene er dekorative (`interactive: false`, `keyboard: false`).
- **Mus:** hjulet ruller siden (`scrollWheelZoom: false`). Ctrl/Cmd + hjul zoomer, med en liten handler i `kart.js` som kaller `zoomIn`/`zoomOut` og `preventDefault`.
- **`prefers-reduced-motion`:** ingen animasjon (`zoomAnimation`, `fadeAnimation`, `markerZoomAnimation` og `animate` er `false`).
- **«Kartet i tekst»** er en `h2` med `id="kartet-i-tekst"`, nederst i DOM-en (EXPERIENCE :254-265).
  - Teksten kommer fra `domene/tekst.py`: «{Form} på {lengde totalt} fra {startpunkt}. Ruten stiger ca. {høydemeter} høydemeter, fra {laveste} til {høyeste} moh.»
  - Laveste og høyeste punkt kommer fra én funksjon i `domene/`, `laveste_og_hoyeste(hoydeprofil)`, som 6.1 skal bruke igjen. Verdiene avrundes til nærmeste 10 m.
- **Layout:**
  - Fra 720 px har forslagssiden en grid med kartet til venstre (`position: sticky`) og Infokolonne til høyre (340–470 px). «Kartet i tekst» står under kartet i venstre kolonne, plassert med grid, mens DOM-rekkefølgen står.
  - Under 720 px står kartet innenfor sidemargen med `height: 60vh` og 1 px kant.
  - `main` og `.forslag` blir bredere på forslagssiden.
  - Ingen faste høyder utenom kartets høyde i `vh`, og ingen `overflow: hidden` i `side.css`. Den i `leaflet.css` er Leaflets egen.
- **CSP:** policyen forblir uendret, med mindre nettleseren melder brudd. Da utvides den bare med det som trengs, og begrunnelsen skrives i `.memlog.md`, i `test_innstillinger.py` og i PR-en.
- **Tester:** testene for farger og `overflow` i `test_grunnoppsett.py` hopper over `static/vendor/`. Kartknappene tas med i sjekken av 44 px. `kart.js` får en statisk sjekk som `forbedring.js` har.

**Never:**
- Ingen høydeprofil eller turillustrasjon (6.1), ingen «Nytt forslag» (1.11), ingen endringer i modeller eller migreringer, ingen nye pakker utover Leaflet-filene og ingen inline-skript eller `style`-attributter i malene.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Forslag med tur | GET forslaget | kartflate, `json_script` med GeoJSON, `leaflet.css`/`leaflet.js`/`kart.js` bare på denne siden, og kreditering | N/A |
| Uten JS | HTML uten skript | meldingen med lenke og «Prøv igjen» (lenke), kontrollene skjult, kreditering synlig | N/A |
| Kartet i tekst | rundtur og tur-retur | riktig form, total lengde (dobbel ved tur-retur), høydemeter og laveste/høyeste fra profilen | N/A |
| Laveste og høyeste | profil `((0,183.2),(500,311.7))` | `(180, 310)` | tom profil gir `ValueError` |
| Tilstandspanel | INGEN_TREFF | ingen kart og ingen Leaflet-filer | N/A |
| Søk og feilsider | GET `/`, 404 | ingen Leaflet og fortsatt nøyaktig 1 skript | N/A |
| Berøring | én finger, så to fingre (`touchstart` med 1 eller 2 berøringer) | én finger viser hintet, og `dragging` er av. To fingre slår `dragging` på, og `touchend` slår den av | manuell sjekk |
| CSP | header og malene | uendret policy (eller begrunnet utvidelse) og ingen `style=` | N/A |

</frozen-after-approval>

## Code Map

- `turforslag/templates/turforslag/forslag.html:19-68` -- kartet går mellom Faktaruta (:54) og Begrunnelse (:56), og Kartbeskrivelse går sist før :68 (EXPERIENCE :254-265). Kommentaren på :7 nevner 1.10.
- `turforslag/templates/base.html` -- bare blokkene `tittel`, `logo_aktiv` og `innhold`. Legg til `{% block hode %}{% endblock %}` for CSS og skript som bare forslagssiden trenger.
- `domene/tekst.py` -- `Turvisning` (:211-226) og `turvisning()` (:246). Legg til `kartbeskrivelse`, `kart_geojson` (dict) og `kart_navn`. Gjenbruk `formater_lengde_totalt` (:89), `formater_hoydemeter` (:103) og `formater_form` (:109).
- `domene/tur.py:38-65` -- `geometry` (lon, lat), `hoydeprofil` ((avstand, høyde) …), `til_geojson_feature()`, `total_lengde_m` (:174) og `total_hoydemeter_m` (:179).
- `turforslag/sokflyt.py:26-45` -- henter `Tur` og bygger visningen.
- `config/settings.py:95-102` -- CSP. `tests/web/test_innstillinger.py:11-18` (`FORVENTET_CSP`) og :71-81 (`style=` og inline-skript).
- `tests/web/test_grunnoppsett.py` -- farger (:341-354), 44 px (:393-409), `overflow` (:417-422), stilark og skript på `/` (:203-228) og den statiske sjekken av `forbedring.js` (:431-437).
- `turforslag/static/css/side.css` -- `main` (:30-35) og `.forslag` (:533-546). `tokens.css:73-79` og :163 har kart-tokenene og `--map-control-size`.
- EXPERIENCE.md: Mikrotekst (:111, :148-150, :184), kreditering (:202), oppførsel (:236-252) og feil i flisene (:300). DESIGN.md: komponentene (:247-282), layout (:525-527) og kontrollene (:573-581). Mockupen `key-turforslag.html` (grid :71-85, kart :134-151 og :226-247). Ignorer «Data fra MET Norge» i mockupen (spinen :219).

## Tasks & Acceptance

**Execution:**
- [x] `turforslag/static/vendor/leaflet/` -- `leaflet.js`, `leaflet.css` og `LICENSE` fra leaflet@1.9.4 (npm-pakken via jsDelivr), uendret -- AR-10
- [x] `domene/tekst.py` (og eventuelt `domene/tur.py`) -- `laveste_og_hoyeste` og `kartbeskrivelse`, med `kart_geojson` og `kart_navn` på `Turvisning` -- FR-6, UX-DR15
- [x] `turforslag/templates/base.html`, `forslag.html` og `_kart.html` -- kartflaten, kontrollene, krediteringen, meldingen uten JS, «Kartet i tekst» og `json_script` -- UX-DR12, UX-DR13
- [x] `turforslag/static/kart.js` -- etter Always-reglene og beslutningen om berøring -- AR-10, NFR-4
- [x] `turforslag/static/css/side.css` -- grid og sticky, høyde under 720 px, rute- og markørklasser, kontrollene, krediteringen, meldingen, `.no-js` og reduced motion -- UX-DR12
- [x] `_bmad-output/planning-artifacts/architecture/architecture-G81-eriksen-2026-11-07/.memlog.md` -- avviket for berøring og eventuelt CSP-endringen, med begrunnelse -- AR-17
- [x] Tester -- `tests/domene/test_tekst.py` (laveste og høyeste, kartbeskrivelsen), `tests/web/test_forslag.py` (matrisen), `test_grunnoppsett.py` og `test_innstillinger.py` (unntak for vendor, 44 px og `kart.js`) -- SM-2

**Acceptance Criteria:**
- Gitt de nye filene, når `python manage.py test` kjøres, så er alle grønne (2 hoppet over lokalt).
- Gitt en lokal server i Chrome på 1280 × 800, med et søk med turtype og det lengste turnavnet, så synes turnavn, Turtype-treff, Faktarute og kart uten rulling. Konsollen viser ingen CSP-brudd eller JS-feil. Et skjermbilde legges i PR-en.
- Gitt samme visning, så viser kartet hele ruten med plommelilla linje og «S». Tastaturrekkefølgen er som i Always, og axe-core gir 0 alvorlige eller kritiske brudd.

## Verification

**Commands:**
- `venv/Scripts/python.exe manage.py test` -- forventet: alle grønne, 2 hoppet over
- `venv/Scripts/python.exe -m ruff check . && venv/Scripts/python.exe -m ruff format --check .` -- forventet: ingen funn
- Kjør aldri `uv run` i repoet. Implementeringsagenten åpner ikke nettleseren. De manuelle sjekkene gjøres av hovedøkten.

**Manual checks:**
- Chrome på 1280 × 800 og 360 px (iframe-måling, se 1.9): kartet, kontrollene, krediteringen, konsollen, tastaturet, uten JS, at flisene ikke lastes (blokker `cache.kartverket.no` i DevTools), reduced motion og axe-core.

## Implementation Notes

- Leaflet-filene er lastet ned fra jsDelivr (`leaflet@1.9.4/dist/leaflet.js`, `dist/leaflet.css` og `LICENSE`) og er byte for byte like (SHA-256 stemmer med den publiserte SRI-en). `leaflet.css` og `LICENSE` har CRLF fra pakken, så `.gitattributes` setter `-text` på `turforslag/static/vendor/**`, ellers ville `core.autocrlf` endret linjeskiftene ved commit.
- `{% block hode %}` står i `base.html` mellom `tokens.css` og `side.css`, så `side.css` overstyrer Leaflets regler med samme spesifisitet (blant annet `touch-action`).
- Startmarkøren «S» står på rutens første punkt (`properties.start` i GeoJSON fra `domene/tekst.py`), ikke på startpunktets koordinat. For de 15 turene ligger startpunktet 21–458 m fra rutens start.
- DOM-en har to Infokolonne-deler (`infokolonne-topp` før kartet og `infokolonne-bunn` etter), så grid kan plassere kartet i venstre kolonne uten å endre rekkefølgen. Rad 2 er `1fr`, så ekstra høyde fra kartet havner under Begrunnelse.
- Uten JS styres av klassen `no-js` på `.kart` (kart.js fjerner den). `@media (scripting: enabled)` skjuler meldingen til kart.js har startet, så den ikke blinker. Feiler alle flisene i en runde (`load` uten `tileload`), eller kaster kart.js, får `.kart` klassen `kart-feil`.
- `kart.js` er røyktestet i Node med en falsk `L` og DOM (ingen pakker): ingen unntak, `no-js` fjernes, riktige kartvalg. Oppførselen i en ekte nettleser er ikke sjekket (se Manual checks).

- Chrome-sjekk 2026-11-26 (hovedøkten, lokal server):
  - **To feil funnet og rettet:**
    - (1) `markor.getElement()` var `undefined` før `fitBounds`, så `kart.js` havnet i `catch`. Nå kjøres `fitBounds` først, med null-sjekk og statisk test.
    - (2) Gridet `minmax(340px, 470px)` ga et kart på ca. 170 px ved 767 px. Nå er det `clamp(340px, 40%, 470px)`.
  - **Etter rettingene:**
    - 6–18 fliser lastet, rute med kant, «S» med `aria-hidden` og ingen CSP-meldinger i konsollen.
    - 1280 × 800, målt i en iframe fordi skjermen har 125 % skalering og bare ca. 730 px høyde, med det lengste turnavnet (Nordmarksrunden) satt inn: h1 slutter ved 233, Turtype-treff ved 322, Faktarute ved 416, kartet går fra 93 til 780 og krediteringen ender ved 775, alt ≤ 797. Skjermbildet ligger i `skjermbilder/1-10-turforslag-1280x800.png`.
    - 360 × 780: kartet er 466 px (60vh), uten vannrett rulling.
    - Tab-rekkefølgen: Kartet i tekst → kartflaten (region) → Vis hele ruten → Zoom inn → Zoom ut → Kartverket → OpenStreetMap (`lang="en"`). Piltastene flytter kartet, knappene er 44 px og markøren har `tabIndex` −1.
    - Blokkerte fliser (CSP-meta `img-src 'self'`): `kart-feil`, og meldingen og krediteringen er synlige.
    - Uten JS (sandkasset iframe med serverens HTML): meldingen er synlig, «Prøv igjen» er en lenke til samme side, kontrollene er skjult, og krediteringen og lenken til «Kartet i tekst» er synlige.
    - axe-core 4.10.2: 0 brudd (39 beståtte regler).
  - **Ikke testet på en ekte berøringsskjerm:** handleren for to fingre er bare sjekket statisk. Reduced motion er sjekket i koden og med statisk test.

## Spec Change Log

## Review Triage Log

Gjennomgang 2026-11-26 i tre lag (Blind Hunter = BH, Edge Case Hunter = ECH, Verification Gap = VG). Løkke 0.

| # | Lag | Funn | Vurdering | Begrunnelse | Rute |
|---|---|---|---|---|---|
| 1 | VG, BH, ECH | En tom høydeprofil gir 500 på forslagssiden (`kartbeskrivelse` → `ValueError`), og `valider_turer` slipper den gjennom | medium | Verifisert av VG: `valider_turer([lag_tur(hoydeprofil=())])` passerer. Det er en ny feilvei i 1.10. | patch |
| 2 | BH, ECH | «Prøv igjen» gjør ingenting når `start()` havner i `catch` (lytteren registreres etter `L.map`) | medium | `catch` viser knappen via `kart-feil`, men ingen lytter finnes. | patch |
| 3 | BH, ECH | `dragging.enable()` for to fingre har ingen effekt | low | Leaflet `Draggable._onDown` avbryter ved `touches.length !== 1`. Flytting med to fingre kommer fra `touchZoom`, så beslutning 1A oppfylles, men koden og loggen er misvisende. | patch (fjern grenen, rett `.memlog.md` og Deferred i spinen) |
| 4 | BH | Deferred-raden (spinen :359) sier fortsatt «Leaflets innebygde valg» | low | Det motsier beslutningen i `.memlog.md`. Det er en direkte retting. | patch (sammen med 3) |
| 5 | BH | Målestokken har `background: none` og ingen garantert kontrast mot flisene | low | De andre kartelementene ligger på `--map-overlay-surface`. Det er en direkte CSS-retting. | patch |
| 6 | ECH | Ctrl/Cmd + hjul over kontrollene og krediteringen gir nettleserzoom, ikke kartzoom | low | Lytteren ligger på `flate` og ikke på `.kart`. Det er en direkte retting. | patch |
| 7 | VG, BH | Oppførselen i `kart.js` (berøring, flisfeil og knappene) testes bare som tekst | medium (uverifisert) | Repoet har med vilje ingen JS-kjøring. Sjekkene i Chrome står i Implementation Notes. | defer |
| 8 | ECH | `kart.js` lastes aldri (404 eller blokkert): meldingen er skjult av `@media (scripting: enabled)` | low | Egen statisk fil. Lenken til «Kartet i tekst» står fortsatt. Rettingen snur logikken. | avvist |
| 9 | BH | Livesonen annonseres ikke når meldingen bare blir synlig | low | Gjelder bare når flisene feiler, og «Kartet i tekst» finnes. Rettingen krever ny logikk. | avvist |
| 10 | BH | Ingen hint for hjul uten Ctrl, og Ctrl + hjul tar sidezoomen over kartet | false | AC-en krever at Ctrl/Cmd + hjul zoomer kartet. | avvist |
| 11 | BH | Kartflaten mangler `aria-describedby` med instruksjoner | low | Spec-en og AC-en sier hvilke attributter flaten skal ha. Lenken «Kartet i tekst» står rett før. | avvist |
| 12 | BH | Rette anførselstegn i feilmeldingen | false | Mikrotekst (:148) har nettopp `"Kartet i tekst"` inne i «». | avvist |
| 13 | BH | «stiger ca. 0 høydemeter, fra 100 til 100» for flate turer | low | Den flateste turen har 6 hm, som gir «ca. 10». | avvist |
| 14 | BH | Bred layout via `main:has(> .forslag)` uten reserve | low | Alle nåværende nettlesere støtter `:has()`, og det er verifisert i Chrome. | avvist |
| 15 | ECH | Penn på en enhet med grov peker kan ikke flytte kartet | low | Sjelden enhetskombinasjon. | avvist |
| 16 | ECH | Nettlesere med PointerEvent uten TouchEvent | false | Alle berøringsnettlesere (Chrome Android, Safari iOS) har TouchEvent. | avvist |
| 17 | ECH | Fliser som henger uten svar gir et grått kart uten melding | low | Krever en tidsgrense. Lite sannsynlig. | avvist |
