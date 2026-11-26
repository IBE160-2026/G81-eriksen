---
title: 'Story 1.8: Systemet velger og rangerer turer som passer søket'
type: 'feature'
created: '2026-11-25'
status: 'done'
baseline_commit: '914d2bfb3c21dbc2f1fd0be7a85fa164d033eab9'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-1-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Det finnes ingen kode som velger turer for et søk. 1.9 (søk og forslag), 1.11 (nytt forslag) og 1.12 (endringsforslag) trenger én ren funksjon som filtrerer, rangerer og gir en status, så Ola bare får turer som passer tiden, turtypen, startpunktet og nivåtaket (FR-5, FR-8, FR-18).

**Approach:** `domene/sok.py` får `Sok`. `domene/utvalg.py` får `Status`, `Utvalg` og `velg_turer(sok, turer, nivatak)`, og nivåtaket uten historikk er grønt. Alt er ren Python med enhetstester i `tests/domene/`, uten database, nett eller klokke.

**Beslutninger (Hannah, 2026-11-26, etter party-runde):**
1. Erstatningen går foran nivåtaket. Er topptur valgt og ingen topptur passer innenfor taket, men en utsiktstur gjør det, blir statusen `TOPPTUR_ERSTATTET`. Det gjelder også når en topptur over taket passer (1A).
2. «Ingen topptur passer» gjelder uansett grunn: tid, startpunkt eller nivåtak. Utsiktsturene går gjennom de samme filtrene (tid, nivåtak og startpunkt), med turtypen byttet til `utsikt` (2A). Meldingen i 1.9 og 1.12 må derfor si «passer søket ditt», ikke «passer tiden».
3. Når topptur er valgt og ingenting passer innenfor taket, gir bare toppturer over taket `BARE_OVER_NIVATAK`. Utsiktsturer over taket teller ikke, og da blir det `INGEN_TREFF` (3A).
4. Maks varighet økes fra 8 t til **12 t** (720 min), så den svarte og den røde turen (580 og 575 min) kan foreslås, og det er plass til lengre turer i 6.2 (alternativ b fra party-runden, 4B).
5. Grensene ligger i konstanter i `domene/sok.py` (`MIN_VARIGHET_MIN = 60`, `MAKS_VARIGHET_MIN = 720`, `VARIGHET_STEG_MIN = 30`). `bmad-correct-course` kjøres rett etter 1.8, før 1.9 bygger valglista, og oppdaterer «1–8 t» i PRD-en, EXPERIENCE.md og epics.md (5A). 1.8 endrer ikke disse dokumentene.

## Boundaries & Constraints

**Always:**
- Filter (FR-5): `estimert_tid_min <= sok.varighet_min` (lik tid er med), turnivå ≤ nivåtak i rekkefølgen grønn < blå < rød < svart, turtypen i `tur.turtyper` når `sok.turtype` er satt, og `tur.startpunkt_id == sok.startpunkt_id` når startpunktet er satt. Det finnes ingen minstetid.
- Rangering (FR-5 punkt 5 og 6): størst `estimert_tid_min` først (nærmest varigheten, siden alle er ≤), deretter tur-ID stigende som tekst. Samme input gir alltid samme liste.
- `Utvalg.rangerte_tur_ider` er en tuple. Den er tom ved `BARE_OVER_NIVATAK` og `INGEN_TREFF`, og ved `TOPPTUR_ERSTATTET` har den utsiktsturene. **Ingen tur over nivåtaket er noen gang med** (SM-C1).
- Gjest eller bruker uten historikk har grønt nivåtak (FR-18).
- `velg_turer` kan utvides senere med nøkkelordargumenter med standardverdi (`registreringer`, `nivaheving`, `foretrukne_turtyper`, `onsket_tur_ider`) uten at testene fra 1.8 endres. Rangeringen er derfor én sorteringsnøkkel som senere kan få flere ledd foran.
- `Sok` er frozen, så `dataclasses.replace` kan brukes i 1.12, og valideres i `__post_init__` (`ValueError` på norsk). Varigheten er et heltall i minutter, 60–720 i steg på 30 (konstantene fra beslutning 5). Turtypen er `None` eller en verdi i `TURTYPER`. Startpunktet er `None` eller en tekst som ikke er tom. Datoen er en `date`.
- Testene viser til FR-5, FR-8 og FR-18 (SM-2) og bruker egne `Tur`-objekter. De leser ikke `data/turer.geojson`.

**Never:**
- Ingen Django, database, nett eller klokke i `domene/`. Dagens dato brukes ikke i utvalget.
- Ingen `foresla_endringer` (den kommer i 1.12), ingen `domene/niva.py` eller `vurder_historikk` (3.1), og ingen views, maler eller økt.
- Ingen sammenligning av `Turniva` med `<` (StrEnum sammenligner alfabetisk).

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Treff | 3 t, alle turtyper, grønt tak | `TREFF`, grønne turer ≤ 180 min, lengst tid først | N/A |
| Lang tur | svart tur på 580 min, varighet 720, svart tak | turen er med | N/A |
| Lik tid | tur på 150 min, varighet 150 | turen er med | N/A |
| Lik tid, ulik ID | to turer på 120 min | ID stigende | N/A |
| Over nivåtaket | blå tur passer alt, grønt tak | blå tur er aldri med | N/A |
| Turtype og startpunkt | turtype `marka` og startpunkt satt | bare turer med begge | N/A |
| Topptur erstattet | topptur, ingen topptur passer, men en utsiktstur gjør det | `TOPPTUR_ERSTATTET` med utsiktsturene rangert | N/A |
| Topptur over taket, utsikt innenfor | topptur, bare en blå topptur passer, og en grønn utsiktstur passer, grønt tak | `TOPPTUR_ERSTATTET` med utsiktsturen (beslutning 1) | N/A |
| Topptur, feil startpunkt | topptur og startpunkt X, X har ingen topptur, men en utsiktstur som passer | `TOPPTUR_ERSTATTET` med utsiktsturen fra X (beslutning 2) | N/A |
| Topptur, bare utsikt over taket | topptur, ingenting passer innenfor taket, og bare en blå utsiktstur passer over det | `INGEN_TREFF` (beslutning 3) | N/A |
| Topptur, topptur over taket | topptur, ingenting passer innenfor taket, men en blå topptur passer | `BARE_OVER_NIVATAK`, tom liste | N/A |
| Bare over nivåtaket | turer passer alt unntatt taket | `BARE_OVER_NIVATAK`, tom liste | N/A |
| Ingen treff | ingen tur passer, heller ikke over taket | `INGEN_TREFF`, tom liste | N/A |
| Ugyldig søk | varighet 45, 75 eller 750, turtype `fjell`, tomt startpunkt | — | `ValueError` |

</frozen-after-approval>

## Code Map

- `domene/tur.py` -- `TURTYPER` (:17) og `Turniva(StrEnum)` (:25–29), uten rekkefølge. `Tur` (:32–58) har `id`, `startpunkt_id`, `turtyper`, `turniva` og `estimert_tid_min` (minutter). Legg til `NIVAREKKEFOLGE = (GRONN, BLA, ROD, SVART)` her, ved enumen, og bruk den til sammenligning. Resten endres ikke.
- `domene/gradering.py`, `domene/tid.py` -- regner ut nivå og tid. Brukes ikke i utvalget, fordi tallene er lagret på turen (AD-3 punkt 6).
- `tests/domene/test_tur.py:20` -- `lag_tur(**endringer)` med `replace`. Lag en tilsvarende lokal hjelper i den nye testfila.
- `tests/domene/test_bare_standardbibliotek.py:31` -- dekker nye moduler i `domene/` automatisk.
- Spinen AD-2 (l. 62) og AD-11.1 (l. 161, `vurder_historikk` kommer i 3.1). epics.md :765 viser `foresla_endringer` i 1.12. Den kaller `velg_turer` mange ganger med `replace(sok, …)`.

## Tasks & Acceptance

**Execution:**
- [x] `domene/tur.py` -- `NIVAREKKEFOLGE` -- FR-5
- [x] `domene/sok.py` -- konstantene for varighet og frozen `Sok(varighet_min, dato, turtype=None, startpunkt_id=None)` med validering -- FR-5
- [x] `domene/utvalg.py` -- `Status` (StrEnum: `TREFF`, `TOPPTUR_ERSTATTET`, `BARE_OVER_NIVATAK`, `INGEN_TREFF`), frozen `Utvalg(status, rangerte_tur_ider)`, `NIVATAK_UTEN_HISTORIKK = Turniva.GRONN` og `velg_turer(sok, turer, nivatak)` etter beslutningene -- FR-5, FR-8, FR-18
- [x] `tests/domene/test_sok.py`, `tests/domene/test_utvalg.py` -- én test per rad i matrisen og per beslutning, med FR-ID i kommentaren. Testene sjekker også at ingen tur over taket er med for hvert tak og hver status -- SM-2

**Acceptance Criteria:**
- Gitt de nye modulene, når `python manage.py test` kjøres, så er alle testene grønne, og importsjekken for `domene/` passerer.
- Gitt samme søk og turliste i ulik rekkefølge, når `velg_turer` kalles, så er resultatet likt.

## Verification

**Commands:**
- `venv/Scripts/python.exe manage.py test` -- forventet: alle grønne, uten nett
- `venv/Scripts/python.exe -m ruff check . && venv/Scripts/python.exe -m ruff format --check .` -- forventet: ingen funn
- Kjør aldri `uv run` i repoet (det lager `.venv` og `uv.lock`)

## Implementation Notes

## Spec Change Log

## Review Triage Log

Gjennomgang 2026-11-26 i tre lag (Blind Hunter = BH, Edge Case Hunter = ECH, Verification Gap = VG). Løkke 0.

| # | Lag | Funn | Vurdering | Begrunnelse | Rute |
|---|---|---|---|---|---|
| 1 | VG | Ingen test sjekker at et toppturssøk med en topptur som passer, gir `TREFF` | medium | Verifisert av VG med mutant: en flytting av topptur-blokken over TREFF-sjekken gir grønne tester. | patch |
| 2 | BH | Egenskapstesten sjekker ikke turtype, startpunkt, rekkefølge eller dubletter for `TREFF` | low | Matrisetestene dekker hvert filter, men egenskapstesten ville fanget kombinasjoner. Det er en direkte utvidelse av en eksisterende test. | patch |
| 3 | ECH, BH | `startpunkt_id` med mellomrom foran eller bak godtas, men treffer aldri | low | `Sok` sjekker bare `strip()` mot tom tekst. Det er en direkte retting i samme betingelse. | patch |
| 4 | BH | Docstringen for steg 3 i `velg_turer` er misvisende | low | Steget gjelder også uten turtype og krever tid og startpunkt. | patch |
| 5 | BH | Testverdien `690 + 45` tester ikke steg innenfor intervallet | low | 735 er bare over maks. Bruk 705 og −60. | patch |
| 6 | ECH, BH | Ukjent nivåtak gir en engelsk `ValueError` fra enumen | low | Bare kode kaller `velg_turer` (1.9 sender `NIVATAK_UTEN_HISTORIKK`), og feilen er høylytt. Lite sannsynlig, og rettingen legger til en vakt. | avvist |
| 7 | ECH | En tur med ukjent nivå eller ugyldig tid krasjer utvalget | false | Turene kommer fra databasen etter `valider_turer` i `lastinn` (1.6), som avviser ukjente nivåer og negative verdier. | avvist |
| 8 | ECH, BH | Samme tur-ID to ganger gir dublett i lista | false | Tur-ID er primærnøkkel i databasen, og `valider_turer` avviser dubletter i fila. | avvist |
| 9 | ECH, BH | Ukjent startpunkt gir `INGEN_TREFF`, som ikke skiller seg fra en ekte tom liste | false | 1.9 validerer startpunktet mot kjente startpunkter før søket lages (epic: manipulerte POST-er). | avvist |
| 10 | BH | `TOPPTUR` og `"utsikt"` er hardkodet uten sjekk mot `TURTYPER` | low | At en turtype får nytt navn, er lite sannsynlig, og rettingen krever en ny test. | avvist |
| 11 | BH | `Turniva` sorterer fortsatt alfabetisk, og testen sikrer `BLA < GRONN` | low | Spec-en valgte bevisst `NIVAREKKEFOLGE` og at resten av `tur.py` ikke endres. Testen dokumenterer faren. | avvist |
| 12 | BH | Få negative tester for `BARE_OVER_NIVATAK` (for lang tid, feil turtype) | low | `_passer` er felles for alle filtrene, så en slik mutant er lite sannsynlig. Det krever nye tester. | avvist |
| 13 | BH | `Utvalg` håndhever ikke at lista er tom ved enkelte statuser | low | Bare `velg_turer` lager `Utvalg`, og egenskapstesten sjekker det. Rettingen legger til en vakt. | avvist |
| 14 | BH | Beslutning 1 skjuler at det finnes en topptur over taket | false | Hannah avgjorde dette i party-runden (1A). Det er intensjon, ikke en feil. | avvist |
| 15 | BH | Henvisningene til beslutningene er ulike | false | `sok.py` (5), `test_grensene` (4 og 5) og `test_lang_tur` (4) stemmer med beslutning 4 (12 t) og 5 (konstantene). | avvist |
| 16 | BH | `test_samme_sok_gir_samme_liste` er en svak sjekk | low | Den faste forventede tuplen under er det som tester noe. Ufarlig. | avvist |
