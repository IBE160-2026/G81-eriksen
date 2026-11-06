---
title: Your Next Adventure — DESIGN
status: final
created: 2026-11-06
updated: 2026-11-06
name: Your Next Adventure
description: Rolig, kartnær nettside på norsk som gir nybegynnere ett turforslag om gangen i Oslo-området. Desktop først med en enkel, stablet mobilutgave. Fargetema Granskog – Mosegrønn, serif-overskrifter og sans-serif brødtekst i systemfonter, egne illustrasjoner laget fra turdata.
sources:
  - _bmad-output/planning-artifacts/prds/prd-G81-eriksen-2026-10-29/prd.md
  - _bmad-output/planning-artifacts/prds/prd-G81-eriksen-2026-10-29/addendum.md
  - _bmad-output/planning-artifacts/research/technical-turdata-oslomarka-2026-10-29/research.md
  - docs/product-brief-your-next-adventure-no.md
  - docs/tilbakemelding-product-brief.md
colors:
  # Granskog – Mosegrønn. Lys verdi uten suffiks, mørk modus med suffikset -dark.
  # Mørk modus følger systeminnstillingen (prefers-color-scheme). Lav prioritet i v1.
  background: '#F3F3EC'
  background-dark: '#141A15'
  surface: '#FFFEFA'
  surface-dark: '#1C231D'
  surface-alt: '#E7EADF'
  surface-alt-dark: '#262F27'
  text: '#1F2A22'
  text-dark: '#E8ECE4'
  text-muted: '#4F5B50'
  text-muted-dark: '#AAB4A8'
  primary: '#355146'
  primary-dark: '#ADCEC0'
  on-primary: '#FFFFFF'
  on-primary-dark: '#19241F'
  accent: '#D6936E'
  accent-dark: '#E3A784'
  accent-2: '#C99AA6'
  accent-2-dark: '#D9AAB5'
  accent-soft: '#F6E4D8'
  accent-soft-dark: '#3B2D27'
  border: '#CFD4C5'
  border-dark: '#333D33'
  input-border: '#6F7A72'
  input-border-dark: '#AAB4A8'
  focus-ring: '#B0624A'
  focus-ring-dark: '#F0B79C'
  success: '#2E4D3C'
  success-dark: '#B0CDBA'
  info: '#3F5F86'
  info-dark: '#97B6E0'
  warning: '#865A16'
  warning-dark: '#E5BA6E'
  error: '#A5383A'
  error-dark: '#EF9A92'
  profile-fill: '#CEE1D9'
  profile-fill-dark: '#374B43'
  sun: '#EEC7B0'
  sun-dark: '#8F6D5C'
  gradient-1: '#355146'
  gradient-1-dark: '#263931'
  gradient-2: '#7C9087'
  gradient-2-dark: '#4A5E55'
  gradient-3: '#D9A48A'
  gradient-3-dark: '#8F6D5C'
  gradient-4: '#EEC7B0'
  gradient-4-dark: '#B48B74'
  # Turnivå – faste domenefarger. Alltid farge OG tekst («Grønn – lett»).
  level-gronn: '#1A7F37'
  level-gronn-dark: '#34C35F'
  level-gronn-on: '#FFFFFF'
  level-gronn-on-dark: '#111418'
  level-bla: '#0A5BD3'
  level-bla-dark: '#4C93FF'
  level-bla-on: '#FFFFFF'
  level-bla-on-dark: '#111418'
  level-rod: '#C8221B'
  level-rod-dark: '#FF5D52'
  level-rod-on: '#FFFFFF'
  level-rod-on-dark: '#111418'
  level-svart: '#111111'
  level-svart-dark: '#050505'
  level-svart-on: '#FFFFFF'
  level-svart-on-dark: '#FFFFFF'
  # Kartlag: alt som ligger oppå kartflisene. Flisene er lyse i begge moduser,
  # så disse tokenene har bevisst INGEN -dark-par og er like i lys og mørk modus.
  map-overlay-surface: '#FFFFFF'
  map-overlay-text: '#1F2A22'
  map-overlay-link: '#355146'
  map-marker-start: '#355146'
  map-route: '#6A3D9A'           # plommelilla; ikke rød/oransje (stier og veier i kartet) og ikke blå (vann, nivå Blå)
  map-focus-ring: '#B0624A'
typography:
  # Systemfonter, ingen webfont. Serif-stabel på overskrifter, systemets sans-serif på resten.
  display:
    fontFamily: 'Georgia, "Iowan Old Style", "Palatino Linotype", "Times New Roman", serif'
    fontSize: 42px
    fontWeight: '400'
    lineHeight: '1.1'
  headline-lg:
    fontFamily: 'Georgia, "Iowan Old Style", "Palatino Linotype", "Times New Roman", serif'
    fontSize: 36px
    fontWeight: '400'
    lineHeight: '1.15'
  headline-md:
    fontFamily: 'Georgia, "Iowan Old Style", "Palatino Linotype", "Times New Roman", serif'
    fontSize: 28px            # turnavnet i infokolonnen, på alle bredder (mockups/key-turforslag.html)
    fontWeight: '400'
    lineHeight: '1.15'
  headline-sm:
    fontFamily: 'Georgia, "Iowan Old Style", "Palatino Linotype", "Times New Roman", serif'
    fontSize: 22px
    fontWeight: '400'
    lineHeight: '1.25'
  brand:
    fontFamily: 'Georgia, "Iowan Old Style", "Palatino Linotype", "Times New Roman", serif'
    fontSize: 20px
    fontWeight: '400'
    lineHeight: '1.2'
  body-lg:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.5'
  body-md:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    fontSize: 14.5px
    fontWeight: '400'
    lineHeight: '1.45'
  label:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    fontSize: 15px
    fontWeight: '600'
    lineHeight: '1.4'
  button:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    fontSize: 15px
    fontWeight: '600'
    lineHeight: '1.3'
  fact-value:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    fontSize: 18px
    fontWeight: '600'
    lineHeight: '1.2'
  eyebrow:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    fontSize: 12px
    fontWeight: '600'
    lineHeight: '1.4'
    letterSpacing: 0.06em
  caption:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    fontSize: 12.5px
    fontWeight: '400'
    lineHeight: '1.4'
rounded:
  sm: 6px
  md: 8px
  lg: 12px
  xl: 16px
  full: 9999px
spacing:
  '1': 4px
  '2': 8px
  '3': 12px
  '4': 16px
  '5': 24px
  '6': 32px
  '7': 48px
  '8': 64px
  # Flytende regler i stedet for faste bredder. Ingen faste høyder på innhold.
  page-margin: 'clamp(16px, 5vw, 64px)'
  breakpoint-stack: 720px
  touch-target-min: 44px
  header-min-height: 60px
  info-column-max-width: 470px
  info-column-padding: 28px
  form-max-width: 560px
  content-max-width: 960px          # Historikk (mockups/key-historikk.html) og Konto
  side-illustration-max-width: 440px
  map-control-size: 44px
components:
  toppmeny:
    background: '{colors.surface}'
    foreground: '{colors.text}'
    border-bottom: '1px solid {colors.border}'
    min-height: '{spacing.header-min-height}'
    padding-inline: '{spacing.page-margin}'
    brand-typography: '{typography.brand}'
    logo-mark-size: '{spacing.5}'
    active-item: '{colors.primary} + 2px understrek'
    item-min-target: '{spacing.touch-target-min}'
  knapp-primaer:
    background: '{colors.primary}'
    foreground: '{colors.on-primary}'
    border: '1.5px solid {colors.primary}'
    radius: '{rounded.md}'
    typography: '{typography.button}'
    padding: '{spacing.2} {spacing.4}'
    min-height: '{spacing.touch-target-min}'
    min-width: '{spacing.touch-target-min}'
  knapp-sekundaer:
    background: 'transparent'
    foreground: '{colors.primary}'
    border: '1.5px solid {colors.primary}'
    radius: '{rounded.md}'
    typography: '{typography.button}'
    padding: '{spacing.2} {spacing.4}'
    min-height: '{spacing.touch-target-min}'
    min-width: '{spacing.touch-target-min}'
  fokusring:
    outline: '3px solid {colors.focus-ring}'
    offset: 2px
    map-variant: '3px solid {colors.map-focus-ring} + 3px ytre kant i {colors.map-overlay-surface}'
  skjemafelt:
    background: '{colors.surface}'
    foreground: '{colors.text}'
    border: '1px solid {colors.input-border}'
    radius: '{rounded.md}'
    min-height: '{spacing.7}'
    label-typography: '{typography.label}'
    hint-typography: '{typography.caption}'
    hint-color: '{colors.text-muted}'
    placeholder-color: '{colors.text-muted}'
    error-color: '{colors.error}'
    error-border: '1px solid {colors.error}'
    error-typography: '{typography.body-md} + vekt 600'
    error-icon: '«!» i fylt sirkel, 18 px, {colors.error}'
    error-placement: 'rett under feltet, over hjelpeteksten'
  turtypekort:
    background: '{colors.surface}'
    border: '1px solid {colors.input-border}'
    radius: '{rounded.lg}'
    min-height: '{spacing.touch-target-min}'
    selected-border: '2px solid {colors.primary}'
    selected-background: '{colors.surface-alt}'
    selected-label: '«Valgt» i {colors.primary}'
    icon-colors: '{colors.primary}, {colors.accent}, {colors.accent-2}'
  valggruppe:
    background: '{colors.surface}'
    border: '1px solid {colors.input-border}'
    radius: '{rounded.md}'
    min-target: '{spacing.touch-target-min}'
    selected-background: '{colors.primary}'
    selected-foreground: '{colors.on-primary}'
    selected-marker: 'hake ✓ + vekt 600'
  sokeoppsummering:
    foreground: '{colors.text-muted}'
    typography: '{typography.caption}'
    link-color: '{colors.primary}'
    link-decoration: 'understrek'
  kart:
    background: 'lyse kartfliser i begge moduser'
    route: '{colors.map-route}'
    route-width: 5px
    route-casing: '{colors.map-overlay-surface}'
    route-casing-width: 9px
    start-marker: '{colors.map-marker-start}'
    start-marker-border: '2px solid {colors.map-overlay-surface}'
    start-marker-label: '{colors.map-overlay-surface}'
    controls-background: '{colors.map-overlay-surface}'
    controls-foreground: '{colors.map-overlay-text}'
    controls-border: '1px solid {colors.map-overlay-text}'
    controls-radius: '{rounded.md}'
    controls-size: '{spacing.map-control-size}'
    controls-inset: '{spacing.3}'
    text-link-background: '{colors.map-overlay-surface}'
    text-link-color: '{colors.map-overlay-link}'
    text-link-typography: '{typography.caption}'
    text-link-radius: '{rounded.md}'
    text-link-min-height: '{spacing.touch-target-min}'
    scale-color: '{colors.map-overlay-text}'
    focus: '{components.fokusring.map-variant}'
    mobile-margin-inline: '{spacing.page-margin}'
    mobile-border: '1px solid {colors.border}'
    mobile-height: 'ca. 60 % av skjermhøyden'
  kreditering:
    background: '{colors.map-overlay-surface}'
    foreground: '{colors.map-overlay-text}'
    link-color: '{colors.map-overlay-link}'
    link-decoration: 'understrek'
    typography: '{typography.caption}'
    radius: '{rounded.md} bare øverst til venstre; ligger kant i kant med kartets nedre høyre hjørne'
  kartbeskrivelse:
    background: '{colors.surface}'
    border: '1px solid {colors.border}'
    radius: '{rounded.lg}'
    heading-typography: '{typography.headline-sm}'
  infokolonne:
    background: '{colors.surface}'
    border-left: '1px solid {colors.border}'
    max-width: '{spacing.info-column-max-width}'
    padding: '{spacing.info-column-padding}'
    gap: '{spacing.3}'
  turillustrasjon:
    background: '{colors.surface-alt}'
    profile-fill: '{colors.profile-fill}'
    profile-line: '{colors.primary}'
    ridge: '{colors.gradient-2}'
    sun: '{colors.sun}'
    start-marker: '{colors.primary}'
    label-color: '{colors.text}'
    axis-color: '{colors.text-muted}'
    border: '1px solid {colors.border}'
    radius: '{rounded.md}'
  nivamerke:
    background: '{colors.level-gronn} | {colors.level-bla} | {colors.level-rod} | {colors.level-svart}'
    foreground: '{colors.level-gronn-on} | {colors.level-bla-on} | {colors.level-rod-on} | {colors.level-svart-on}'
    radius: '{rounded.sm}'
    typography: '{typography.button}'
    padding: '{spacing.1} {spacing.2}'
    dark-svart-outline: 'inset 0 0 0 1.5px {colors.text-muted-dark}'
  turtype-treff:
    background: '{colors.accent-soft}'
    foreground: '{colors.text}'
    border: '1px solid {colors.accent}'
    radius: '{rounded.full}'
    icon-color: '{colors.accent}'
  formmerke:
    background: '{colors.surface-alt}'
    foreground: '{colors.text}'
    radius: '{rounded.full}'
  faktarute:
    background: '{colors.surface-alt}'
    radius: '{rounded.md}'
    value-typography: '{typography.fact-value}'
    label-typography: '{typography.caption}'
    label-color: '{colors.text-muted}'
  begrunnelse:
    eyebrow-typography: '{typography.eyebrow}'
    eyebrow-color: '{colors.text-muted}'
    body-typography: '{typography.body-md}'
    foreground: '{colors.text}'
  ki-merke:
    foreground: '{colors.text-muted}'
    typography: '{typography.eyebrow}'
    glyph: '✦'
  forklaringspanel:
    border-top: '1px solid {colors.border}'
    trigger-color: '{colors.primary}'
    body-typography: '{typography.body-md}'
  bekledningstips:
    eyebrow-typography: '{typography.eyebrow}'
    bullet-color: '{colors.accent}'
    body-typography: '{typography.body-md}'
  melding:
    background: '{colors.surface}'
    border: '1px solid {colors.border}'
    border-left: '4px solid {colors.info} | {colors.warning} | {colors.error} | {colors.success}'
    radius: '{rounded.md}'
    foreground: '{colors.text}'
    padding: '{spacing.3} {spacing.4}'
    title-typography: '{typography.body-lg} + vekt 600'
    icon: 'alltid ikon + tekst'
    icon-size: 20px
  tilstandspanel:
    heading-typography: '{typography.headline-lg}'
    body-typography: '{typography.body-lg}'
    row-border: '1px solid {colors.border}'
    action-color: '{colors.primary}'
    row-min-height: '{spacing.touch-target-min}'
  lasteindikator:
    foreground: '{colors.text-muted}'
    placeholder-background: '{colors.surface-alt}'
  turoppsummering:
    background: '{colors.surface}'
    border: '1px solid {colors.border}'
    radius: '{rounded.lg}'
    title-typography: '{typography.headline-sm}'
    meta-typography: '{typography.caption}'
  historikktabell:
    background: '{colors.surface}'
    border: '1px solid {colors.border}'
    radius: '{rounded.md}'
    header-color: '{colors.text-muted}'
    header-typography: '{typography.eyebrow}'
    row-heading-typography: '{typography.body-lg} + vekt 600'
    cell-typography: '{typography.body-md}'
    cell-padding: '{spacing.3} {spacing.4}'
    row-border: '1px solid {colors.border}'
    level-badge: '{components.nivamerke} under turnavnet'
    secondary-line-color: '{colors.text-muted}'
    link-color: '{colors.primary}'
    link-decoration: 'understrek'
    action-min-target: '{spacing.touch-target-min}'
    footnote-typography: '{typography.caption}'
    footnote-color: '{colors.text-muted}'
  slettebekreftelse:
    background: '{colors.surface}'
    border: '1px solid {colors.border}'
    radius: '{rounded.lg}'
    heading-typography: '{typography.headline-sm}'
    confirm-button: '{components.knapp-primaer}'
    cancel-button: '{components.knapp-sekundaer}'
---

## Brand & Style

Your Next Adventure er en rolig turkompis for folk som ikke er turvante ennå. Siden skal kjennes som et godt turkart og en side i en turbok: luftig, ryddig og trygg. Ingen skjærende farger og ingen mas. Stemningen er en vintersolnedgang over skogen. Dus grågrønn mose er grunnfargen, og aprikos og støvrosa er varme aksenter. Skumringsblått brukes til info.

To designretninger er slått sammen:

- **Stille kart** gir oppsettet på turforslaget: et stort kart og en rolig infokolonne.
- **Turkort** gir resten: det redaksjonelle søkeskjemaet med illustrerte turtypekort, tilstandsmønsteret («Du har sett alle turene …» med endringsforslag) og de varme serif-overskriftene, som brukes på alle skjermer.

Inspirasjonen er UT.no: ryddig oppsett og fine illustrasjoner av turene. Vi forenkler i stedet for å kopiere, og vi bruker ingen bilder fra UT.no.

**Illustrasjoner.** Hver tur får en egen, enkel illustrasjon tegnet fra turdataene: en stilisert rute og en høydeprofil som viser formen på turen før du går. Vi bruker ingen fotografier (se **Turillustrasjon**).

### Visuelle referanser

**Ved konflikt vinner DESIGN.md og EXPERIENCE.md over mocker og wireframes.**

- **Nøkkelskjermer** (laget fra designdokumentene DESIGN.md og EXPERIENCE.md, i lys modus):
  - [mockups/key-sok.html](mockups/key-sok.html): Søk på desktop, utfylt og med feil i skjemaet (Varighet mangler).
  - [mockups/key-turforslag.html](mockups/key-turforslag.html): Turforslag på desktop 1280 px og mobil 375 px side om side, med folden.
  - [mockups/key-historikk.html](mockups/key-historikk.html): Historikk etter registrering, med Melding (suksess), fremgangslinje og Historikktabell.
- **Retninger og palett** (eldre: forrige Granskog-palett og gamle eksempeltall):
  - [mockups/direction-stille-kart.html](mockups/direction-stille-kart.html): turforslaget og tilstanden uten værvarsel.
  - [mockups/direction-turkort.html](mockups/direction-turkort.html): søkeskjemaet, tilstanden «alle forslag er vist» og serif-stilen.
  - [mockups/color-themes-2.html](mockups/color-themes-2.html): paletten (avsnittet «Mosegrønn») med kontrasttabeller.
- **Wireframes:** [wireframes/ia-2026-11-06.excalidraw](wireframes/ia-2026-11-06.excalidraw) (skjermer og ruter) og [wireframes/flow-ola-2026-11-06.excalidraw](wireframes/flow-ola-2026-11-06.excalidraw) (UJ-1, UJ-2 og kanttilstander).

Kjente avvik i mockene:

- Retningsmockene viser utsiktsmarkør på kartet, tre turtypekort i stedet for fire og pilleknapper i Turkort, og de viser bare desktop.
- Fremgangslinjen i key-historikk har eldre ordlyd.
- Merkene «Eksempel» og rammene rundt (nettleser, telefon, fold, merknader), med skyggene sine, hører bare til mockene.

## Colors

Paletten er **Granskog – Mosegrønn** ([mockups/color-themes-2.html](mockups/color-themes-2.html), steg 2). Hvert token har en lys og en mørk verdi (`-dark`), unntatt kartlag-tokenene. Mørk modus følger systeminnstillingen, og det finnes ingen egen bryter.

- **Mosegrønn primær (`#355146` / `#ADCEC0`)** brukes på handlinger (Primærknapp, lenker, aktivt menypunkt) og på linjen i høydeprofilen. Den er dempet med vilje og ligger langt fra nivåfargen Grønn (ΔE 21,3 / 21,7).
- **Bakgrunn, flate og alternativ flate (`#F3F3EC` / `#FFFEFA` / `#E7EADF`)** er en varm, kremaktig bunn. Skjemaene ligger direkte på `background`. Infokolonne, kort og felt ligger på `surface`. Faktarute, Formmerke og illustrasjonsflaten ligger på `surface-alt`.
- **Aprikos aksent (`#D6936E`)** og **støvrosa aksent-2 (`#C99AA6`)** er solnedgangen. De brukes **bare som dekor**: kant og ikon på Turtype-treff, prikker i Bekledningstips og ikonene i Turtypekort. De er aldri tekst (aksent mot `surface` er 2,5:1).
- **Myk aksent (`#F6E4D8` / `#3B2D27`)** er bakgrunnen til **Turtype-treff**.
- **Gradient (`gradient-1` → `gradient-4`)** går fra mose til aprikos. Den brukes i logomerket, i en tynn himmelstripe og i åsene i illustrasjonen, aldri bak tekst.
- **Status:** `success`, `info` (skumringsblå), `warning` og `error`. Suksess og primær ligger nær hverandre (ΔE 3,3). Det er greit fordi begge betyr «gå videre», men **suksessmeldinger har alltid ikon og tekst**.
- **Fokusring (`#B0624A` / `#F0B79C`)** er en varm rustfarge, lysere i mørk modus, som synes på alle flater.
- **`input-border` (`#6F7A72` / `#AAB4A8`)** er kanten på felt, valg og turtypekort. Den holder minst 3:1 mot alle tre flatene i begge moduser. `border` (`#CFD4C5`, 1,5:1 mot `surface`) skiller bare flater og bærer aldri mening alene.
- **Lenker** i løpende tekst er alltid understreket. Unntak: menypunkter i Toppmeny og knapper. `primary` mot `text` er bare 1,7:1, så fargen alene skiller ikke lenken fra teksten.

### Kartlag

Kartflisene er lyse i begge moduser. **Alt som ligger oppå flisene bruker kartlag-tokenene, som er like i lys og mørk modus**: Kreditering, målestokk, zoomknapper, startmarkør, rutelinje og fokusring på kartet.

- **Rutelinje (`map-route`, plommelilla `#6A3D9A`)** er 5 px på en 9 px hvit kantlinje (`map-overlay-surface`). Den er verken rød eller oransje (som stier og veier i kartet) eller blå (som vann og nivået Blå).
- **Startmarkør (`map-marker-start`)**: mosegrønn sirkel med «S» og 2 px hvit kant.
- **Kartlagsflate, tekst og lenke (`map-overlay-surface`, `map-overlay-text`, `map-overlay-link`)**: helt hvit flate (ingen gjennomsiktighet), mørk tekst og mosegrønne, understrekede lenker.
- **Fokusring på kartet (`map-focus-ring`)**: 3 px fokusring med 3 px hvit ytre kant, så den synes mot både lyse og mørke partier i kartet.

### Turnivå – faste domenefarger

| Token | Lys | Mørk | Tekst på (lys / mørk) | Tekst i UI |
|---|---|---|---|---|
| `level-gronn` | `#1A7F37` | `#34C35F` | `#FFFFFF` / `#111418` | «Grønn – lett» |
| `level-bla` | `#0A5BD3` | `#4C93FF` | `#FFFFFF` / `#111418` | «Blå – moderat» |
| `level-rod` | `#C8221B` | `#FF5D52` | `#FFFFFF` / `#111418` | «Rød – moderat» |
| `level-svart` | `#111111` | `#050505` | `#FFFFFF` / `#FFFFFF` | «Svart – vanskelig» |

Regel: **turnivå vises alltid med farge og tekst**, aldri med farge alene. Nivåfargene og rutelinjen er de eneste mettede fargene i produktet. Nivåfargene brukes ikke til noe annet.

### Kontrastmål (WCAG 2.1 AA)

Tekst skal ha minst 4,5:1, og komponenter som ikke er tekst, minst 3:1. Alle tall er regnet med WCAG relativ luminans.

| Par | Lys | Mørk | Krav |
|---|---|---|---|
| `text` på `surface` / `background` | 14,7 / 13,3 | 13,4 / 14,8 | 4,5 |
| `text-muted` på `surface` / `background` / `surface-alt` | 7,1 / 6,4 / 5,9 | 7,5 / 8,2 / 6,5 | 4,5 |
| `on-primary` på `primary` (Primærknapp) | 8,7 | 9,4 | 4,5 |
| `primary` på `surface` / `background` / `surface-alt` | 8,6 / 7,8 / 7,1 | 9,5 / 10,4 / 8,1 | 4,5 |
| `text` på `accent-soft` (Turtype-treff) | 12,0 | 11,0 | 4,5 |
| `text` på `surface-alt` (Faktarute, Formmerke) | 12,2 | 11,6 | 4,5 |
| `success` / `info` / `warning` / `error` som tekst på `surface` | 9,3 / 6,5 / 6,0 / 6,4 | 9,4 / 7,7 / 8,9 / 7,4 | 4,5 |
| Nivåmerke Grønn / Blå / Rød / Svart | 5,1 / 6,1 / 5,7 / 18,9 | 8,0 / 6,1 / 6,1 / 20,4 | 4,5 |
| `focus-ring` mot `surface` / `background` / `surface-alt` | 4,4 / 4,0 / 3,7 | 9,1 / 10,1 / 7,9 | 3,0 |
| `input-border` mot `surface` / `background` / `surface-alt` | 4,4 / 4,0 / 3,7 | 7,5 / 8,2 / 6,5 | 3,0 |
| `primary` (linje) på `profile-fill` (Turillustrasjon) | 6,4 | 5,5 | 3,0 |
| `map-overlay-text` / `map-overlay-link` på `map-overlay-surface` | 14,9 / 8,7 | likt | 4,5 |
| `map-route` mot hvit kant / OSM land / OSM skog / skog* / vann* | 7,6 / 6,7 / 4,5 / 5,7 / 4,8 | likt | 3,0 |
| `map-marker-start` mot de samme flatene | 8,7 / 7,6 / 5,1 / 6,4 / 5,5 | likt | 3,0 |
| `map-focus-ring` mot sin hvite ytre kant | 4,5 | likt | 3,0 |

\* Skog `#CDE6B4` og vann `#A8D3EE` er antatte flisfarger, og OSM-fargene (`#F2EFE9`, `#ADD19E`) er stedfortredere. **Rutefargen og markøren må måles mot de ekte flisene når fliskilden er valgt** (se Åpne punkter i EXPERIENCE.md).

Nivåmerket Svart i mørk modus ligger nesten i samme tone som flaten (1,3:1). Derfor får det en innvendig kant i `text-muted-dark` (9,5:1 mot merket).

## Typography

Overskrifter er i serif og brødtekst i sans-serif, på alle skjermer. Begge er **systemfonter**, og vi laster ingen webfont. Serifen gir den varme turbokstemmen fra Turkort. Sans-serifen holder tall, skjema og meldinger klare.

| Rolle | Token | Brukes til |
|---|---|---|
| Display | `display` (serif 42/1,1) | Søkeoverskriften «Hvor lang tid har du?» |
| Stor overskrift | `headline-lg` (serif 36) | Tilstandspanel og sideoverskrifter (Historikk, Konto, Registrer gjennomført tur, Logg inn) |
| Turnavn | `headline-md` (serif 28) | Turnavnet i infokolonnen, likt på desktop og mobil ([mockups/key-turforslag.html](mockups/key-turforslag.html)) |
| Liten overskrift | `headline-sm` (serif 22) | «Kartet i tekst», turnavnet i Turoppsummering, Slettebekreftelse |
| Logo | `brand` (serif 20) | Ordmerket «Your Next Adventure» |
| Brødtekst | `body-lg` 16 / `body-md` 14,5 | Skjema og tilstandstekst / infokolonnen |
| Etikett | `label` (600) | Feltetiketter |
| Knapp | `button` (600) | Alle knapper og Nivåmerke |
| Tall | `fact-value` (sans 18/600) | Lengde, høydemeter og estimert tid i Faktarute |
| Overlinje | `eyebrow` (12, store bokstaver, 0,06em) | «Begrunnelse», «Bekledningstips for lørdag», KI-merke, tabellhoder |
| Bildetekst | `caption` (12,5) | Hjelpetekst, nivåforklaring, søkeoppsummering, kreditering, lenken «Kartet i tekst» på kartet og linjen under Historikktabell |
| Feiltekst | `body-md` med vekt 600 i `error` | Feilmeldingen under et felt |

Regler:

- «pauser ikke inkludert» står alltid ved estimert tid, i `caption`.
- Valgfrie felt merkes «(valgfritt)» i normal vekt og `text-muted`.
- Ingen tekst under 12 px.
- Under `{spacing.breakpoint-stack}` skaleres Display og Stor overskrift ned til 28 px [ASSUMPTION].
- Typografirollene er visuelle. Overskriftsnivåene står i EXPERIENCE.md: `h1` i IA-tabellen og `h2` under Accessibility Floor. «Begrunnelse» og «Bekledningstips» ser ut som overlinjer, men er `h2`.

## Layout & Spacing

Skalaen bygger på 4 px: 4 · 8 · 12 · 16 · 24 · 32 · 48 · 64. **Desktop kommer først, med en enkel, stablet mobilutgave i v1.** Referanseskjermen er 1280 × 800.

**Bruddpunkt.** Under `{spacing.breakpoint-stack}` (720 px) stables oppsettet i én kolonne. «Under bruddet» betyr under denne bredden i resten av dokumentet. Faktarute har i tillegg et eget brudd ved ca. 360 px (se Components), og Display og Stor overskrift skaleres ned under bruddet (se Typography).

**Flytende regler.** Ingen kolonne har fast bredde, og intet innhold har fast høyde.

- Sidemargen er `{spacing.page-margin}`: 64 px på desktop, ned til 16 px på smal skjerm.
- Infokolonne er høyst `{spacing.info-column-max-width}`. Skjemasider er høyst `{spacing.form-max-width}`. Historikk og Konto er høyst `{spacing.content-max-width}` og midtstilt.
- Felt, knapper, Toppmeny, merker og Infokolonne bruker `min-height` og padding, aldri `height` med `overflow: hidden`. Tekst skal tåle økt tekstavstand (WCAG 1.4.12) uten å bli klippet.
- Alt man kan trykke på utenfor løpende tekst, er minst `{spacing.touch-target-min}` × `{spacing.touch-target-min}`.

**Folden.** Folden er et designmål ved 1280 × 800 og 100 % zoom, aldri en høydegrense. På referanseskjermen skal turnavn, Turtype-treff, Faktarute, Turillustrasjon og kartet synes uten rulling (klimakset i UJ-1). Begrunnelse og knapper bør også synes. Dette er det eneste stedet kravet står; andre steder viser hit. Folden er tegnet inn i [mockups/key-turforslag.html](mockups/key-turforslag.html).

**Turforslag (Stille kart).** Over `{spacing.breakpoint-stack}`: to kolonner. Infokolonne står til høyre (mellom ca. 340 px og `{spacing.info-column-max-width}`). Kartet fyller resten av bredden til venstre og er `position: sticky`. Kartbeskrivelse står under kartet. Under bruddet stables alt i én kolonne i rekkefølgen fra EXPERIENCE.md (Component Patterns › Turforslag – rekkefølge). Kartet står da **innenfor sidemargen** (`{spacing.page-margin}` på begge sider) med 1 px `border` og er ca. 60 % av skjermhøyden. Margen ved siden av kartet gjør at siden alltid kan rulles med fingeren. Begge bredder: [mockups/key-turforslag.html](mockups/key-turforslag.html).

**Søk (Turkort).** Skjemaet står til venstre, og en pyntillustrasjon (høyst `{spacing.side-illustration-max-width}`, `{spacing.7}` fra skjemaet) står til høyre. Rekkefølgen i skjemaet er Varighet og Dato side om side, så Turtype (fire kort i én rad når det er plass, ellers to per rad), så Startpunkt og så Fritekstønske. Under bruddet stables Varighet og Dato, og pyntillustrasjonen skjules. → [mockups/key-sok.html](mockups/key-sok.html)

**Tilstandspanel (Turkort).** Forklaringen står til venstre og endringsforslagene til høyre. Under bruddet står de under hverandre.

**Historikk.** Én midtstilt kolonne på høyst `{spacing.content-max-width}`. Rekkefølgen er `h1`, Melding (suksess) når brukeren kommer fra en registrering, fremgangslinjen i `body-lg` (valgfri), Historikktabell og til slutt linjen «Nye søk prioriterer …» i `caption` og `text-muted`. Avstanden er `{spacing.3}` fra Melding til fremgangslinjen og `{spacing.5}` fra fremgangslinjen til tabellen. → [mockups/key-historikk.html](mockups/key-historikk.html)

**Registrer gjennomført tur, Konto, Bekreft sletting og Logg inn / Lag konto.** Én kolonne. Disse skjermene har ingen mock og bygges fra designdokumentene og wireframene.

**Toppmeny.** Logoen står til venstre og menypunktene til høyre. Når plassen ikke strekker til, brytes menypunktene til en egen linje under logoen. Det finnes ingen hamburgermeny.

## Elevation & Depth

Dybde kommer fra tonelag og tynne linjer, ikke fra skygger. Lagene er `background`, så `surface`, så `surface-alt`. Flatene skilles med 1 px `border`. Appflatene har ingen skygger. Kartkontrollene og Kreditering ligger flatt oppå kartet på `map-overlay-surface`.

## Shapes

Hjørnene er myke, men ikke runde. De minner om et brettet turkart.

- `rounded.sm` (6 px): **Nivåmerke**.
- `rounded.md` (8 px): knapper, Skjemafelt, Valggruppe, Faktarute, Melding, kartkontroller og Turillustrasjon i Infokolonne. Knappene har 8 px hjørner, ikke pilleform.
- `rounded.lg` (12 px): Turtypekort, Turoppsummering, Kartbeskrivelse og Slettebekreftelse.
- `rounded.xl` (16 px): store illustrasjonsflater på søkesiden.
- `rounded.full`: Turtype-treff og Formmerke.

## Components

Komponentnavnene er de samme som i EXPERIENCE.md under Component Patterns, som eier oppførselen. Verdiene står i frontmatter. Her står oppbygning og visuelle regler. Komponentene bruker `-dark`-parene i mørk modus, unntatt det som ligger på kartet (se Kartlag).

### Grunnelementer

- **Toppmeny** (`toppmeny`): ordmerket i `brand` med et lite gradient-logomerke. Det aktive punktet har vekt 600 og 2 px understrek. → [mockups/direction-turkort.html](mockups/direction-turkort.html)
- **Primærknapp** (`knapp-primaer`): fylt mosegrønn knapp. Høyst én per visning.
- **Sekundærknapp** (`knapp-sekundaer`): gjennomsiktig med mosegrønn kant og tekst.
- **Fokusring** (`fokusring`): `outline` (ikke `box-shadow`, som forsvinner i høykontrastmodus) på alt man kan fokusere på. På kartet brukes kartvarianten (se Kartlag).

### Valg i skjema

- **Skjemafelt** (`skjemafelt`): synlig etikett over feltet, hjelpetekst under og plassholder i `text-muted`. Ved feil står feilmeldingen **rett under feltet og over hjelpeteksten**, i `body-md` med vekt 600 i `error` og med et «!»-ikon i fylt sirkel foran. Kanten blir `error`. Ikonet og teksten gjør at feilen ikke bare vises med farge. Det finnes ingen feiloppsummering øverst i skjemaet. → [mockups/key-sok.html](mockups/key-sok.html) (feiltilstanden)
- **Turtypekort** (`turtypekort`): fire like kort (Alle turtyper, Marka, Utsikt, Topptur), hver med en liten egen illustrasjon. Det valgte kortet får 2 px kant i `primary`, bakgrunn i `surface-alt`, navnet i vekt 600 og ordet «Valgt» under navnet. → [mockups/key-sok.html](mockups/key-sok.html), og illustrasjonsstilen i [mockups/direction-turkort.html](mockups/direction-turkort.html)
- **Valggruppe** (`valggruppe`): segmenter for opplevd vanskelighet og fornøydhet. Valgt segment har fyll i `primary`, vekt 600 og en hake, så valget også synes i Windows høykontrastmodus der fyll forsvinner. Ankerteksten for fornøydhet (se EXPERIENCE.md) står under 1 og 5.

### Turforslag

- **Søkeoppsummering** (`sokeoppsummering`): én linje øverst i `caption` og `text-muted`, med lenken «Endre søk» til høyre.
- **Kart** (`kart`): lyse kartfliser med rutelinje (med hvit kant) og startmarkør «S». Alt som ligger oppå, bruker kartlag-tokenene. Kontrollene står `{spacing.3}` fra kanten. Kreditering ligger kant i kant med hjørnet.
  - oppe til venstre: lenken «Kartet i tekst» i `caption` på `map-overlay-surface` med `rounded.md` og minst 44 px høyde;
  - oppe til høyre: zoomknappene + og − stablet loddrett i én ramme, og «Vis hele ruten» som egen knapp **til venstre for zoomstabelen**;
  - nede til venstre: målestokken, rett på flisene i `map-overlay-text`;
  - nede til høyre: Kreditering.

  Mobiloppsett: se Layout & Spacing. → [mockups/key-turforslag.html](mockups/key-turforslag.html) (desktop og mobil), og den eldre retningen i [mockups/direction-stille-kart.html](mockups/direction-stille-kart.html)
- **Kreditering** (`kreditering`): én linje i `caption` på hvit flate, med understrekede lenker. Den ligger kant i kant med kartets nedre høyre hjørne og har bare det øvre venstre hjørnet rundet. På smal skjerm brytes den over flere linjer, høyrejustert.
- **Kartbeskrivelse** (`kartbeskrivelse`): et kort med overskriften «Kartet i tekst» i `headline-sm` og en kort, datagenerert tekst i `body-md`.
- **Infokolonne** (`infokolonne`): `surface` med 1 px kant mot kartet. Innholdet har `{spacing.3}` mellomrom. Under bruddet fyller den hele bredden og mister venstrekanten. → [mockups/key-turforslag.html](mockups/key-turforslag.html)
- **Turillustrasjon** (`turillustrasjon`): en liten stilisert rute og en høydeprofil tegnet fra data. Profilen har fyll i `profile-fill` og en linje i `primary` (3 px, bevisst unntak fra skalaen). Åsene er i `gradient-2` med 28 % dekkevne, og solen er i `sun`. Startpunktet er en prikk i `primary` med kant i `surface`. Bildeteksten under oppgir turens form og laveste og høyeste punkt. Samme tegning brukes i en stor variant på Søk og en liten i Turoppsummering. Den store pyntvarianten på Søk har `rounded.xl` og **ingen bildetekst**.
- **Nivåmerke** (`nivamerke`): et rektangulært merke i nivåfargen med nivåteksten («Grønn – lett» osv.) og et lite ikon. Den faste nivåforklaringen står ved siden av i `caption`. I mørk modus får Svart en innvendig kant.
- **Turtype-treff** (`turtype-treff`): en pille i `accent-soft` med kant og solikon i `accent`. Teksten står i `text` med vekt 600.
- **Formmerke** (`formmerke`): en pille i `surface-alt` med «Rundtur» eller «Tur-retur».
- **Faktarute** (`faktarute`): tre ruter side om side for total lengde, høydemeter og estimert tid, med verdi i `fact-value` og etikett under. Under ca. 360 px brytes de til én per rad.
- **Begrunnelse** (`begrunnelse`): overlinjen «Begrunnelse» og teksten i `body-md`, uten ramme.
- **KI-merke** (`ki-merke`): «✦ Skrevet med KI» eller «Begrunnelse fra mal» i `eyebrow` og `text-muted`, rett over Begrunnelse.
- **Forklaringspanel** (`forklaringspanel`): utfellbart panel med utløseren «Slik lager jeg forslaget» i `primary` og en pil.
- **Bekledningstips** (`bekledningstips`): overlinjen «Bekledningstips for {dag}», en linje i `caption` om hva tipsene bygger på og en liste der hvert tips har en liten prikk i `accent`.

### Meldinger og tilstander

- **Melding** (`melding`): `surface` med 1 px kant og 4 px venstrekant i statusfargen. Den har alltid et 20 px ikon i fylt sirkel («i» for info, «!» for advarsel og feil, hake for suksess) og en fet tittel. Brødtekst er valgfri: en suksessmelding kan være bare tittelen, for eksempel «Turen er registrert i historikken din.». → [mockups/key-historikk.html](mockups/key-historikk.html) (suksess) og [mockups/direction-stille-kart.html](mockups/direction-stille-kart.html) (info)
- **Tilstandspanel** (`tilstandspanel`): overskrift i `headline-lg`, forklaring i `body-lg` og en liste med endringsforslag. Hver rad har tekst til venstre og en handlingslenke til høyre, med `border` mellom radene. → [mockups/direction-turkort.html](mockups/direction-turkort.html)
- **Lasteindikator** (`lasteindikator`): `surface-alt` der kartet kommer, med teksten «Kart lastes …» i `text-muted`. Ingen spinner når `prefers-reduced-motion` er på.

### Historikk og konto

- **Turoppsummering** (`turoppsummering`): et lite kort med liten Turillustrasjon, turnavn i `headline-sm` og en linje med Nivåmerke · form · lengde · estimert tid.
- **Historikktabell** (`historikktabell`): tabellen ligger på `surface` med 1 px `border` og `rounded.md`. Tabellhodet står i `eyebrow` og `text-muted`. Turnavnet står i `body-lg` med vekt 600, med Nivåmerke på egen linje under. De andre cellene står i `body-md`. Under brukt tid står «estimert ca. …» på egen linje i `text-muted`. Den siste kolonnen har handlingslenkene under hverandre, understreket i `primary` og minst 44 px høye. → [mockups/key-historikk.html](mockups/key-historikk.html)
- **Slettebekreftelse** (`slettebekreftelse`): et rolig kort på egen side med overskrift, forklaring, Primærknapp «Slett kontoen» og Sekundærknapp «Avbryt». Ingen rød flate og ingen advarselsikoner som roper.

## Do's and Don'ts

| Gjør | Ikke gjør |
|---|---|
| Vis turnivå med farge **og** tekst («Grønn – lett») | Vis nivå bare med farge, en prikk eller et ikon |
| Bruk nivåfargene bare til turnivå | Bruk Grønn, Blå, Rød eller Svart til status, knapper eller dekor |
| Hold paletten dus; bare nivåfargene og rutelinjen er mettede | Bruk skjærende, mettede farger utenom nivåfargene |
| Bruk aprikos og støvrosa bare som dekor | Sett tekst i `accent` eller `accent-2` |
| Tegn illustrasjoner fra turdata med temaets tokens | Bruk fotografier, og særlig ikke bilder fra UT.no |
| Nå foldmålet på 1280 × 800 (se Layout & Spacing) | Gi kolonner fast høyde for å tvinge innhold over folden |
| Bruk max-width, flytende kolonner og stabling under `{spacing.breakpoint-stack}` | Bruk faste bredder som gir sidelengs rulling ved 320 px |
| Bruk kartlag-tokenene på alt oppå kartet, i begge moduser | Bruk `-dark`-tokens oppå de lyse kartflisene |
| Tegn rutelinjen i plommelilla med hvit kant | Tegn ruten rød eller oransje, så den ligner stier og veier i kartet |
| Understrek lenker i løpende tekst | Skill lenker fra tekst bare med farge |
| Bruk serif på overskrifter og sans-serif på tall og skjema | Bruk serif på tall, knapper eller skjemafelt |
| Gi suksess, info, advarsel og feil både ikon og tekst | Signaliser status bare med farge |
| Vis Kreditering på turforslaget | Skjul krediteringen bak en lenke eller et ikon |
| Bruk høyst én Primærknapp per visning | Sett to like sterke handlinger ved siden av hverandre |
| Skap dybde med tonelag og 1 px kanter | Bruk skygger som hierarki eller gradient bak tekst |
