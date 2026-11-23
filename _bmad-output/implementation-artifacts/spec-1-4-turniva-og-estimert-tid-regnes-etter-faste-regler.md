---
title: 'Story 1.4: Turnivå og estimert tid regnes etter faste regler'
type: 'feature'
created: '2026-11-23'
status: 'done'
baseline_commit: 'baab1324eeb452b81661fc028905dad5c0d77732'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-1-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** `domene/` er tom. Turdatabasen (1.5–1.7), utvalget (1.8) og visningen (1.9–1.10) trenger én felles beskrivelse av en tur, og nivå og tid må regnes likt overalt etter offentlige regler (FR-2, FR-3, AR-3, AR-19, UX-DR31).

**Approach:** Ren Python i `domene/`:
- dataklassen `Tur` med GeoJSON-omforming og totaler;
- gradering etter Merkehåndboka;
- tid etter sveitsisk regel;
- norsk formatering for tid, lengde og nivå.

Alt testes uten database.

**Beslutninger (Hannah, 2026-11-23):**
- `estimert_tid_min` lagrer tiden avrundet til nærmeste 5 minutter (regneeksempelet gir 140). Det som vises, er det som søket i 1.8 filtrerer på.
- Hele kilometer vises uten «,0» («6 km totalt»). Andre lengder vises med én desimal («3,5 km totalt»).
- Specen beholdes hel.

## Boundaries & Constraints

**Always:**
- `domene/` importerer bare standardbiblioteket og `domene` (eksisterende test). Ingen Django, ingen klokke og ingen nettverk. Én regel er én funksjon, og hver regel og test viser til FR- eller AR-ID.
- `domene/tur.py`:
  - `Tur` er `@dataclass(frozen=True)` med feltene i AD-3 punkt 1, i den rekkefølgen: `id`, `navn`, `startpunkt_id`, `startpunkt_navn`, `startpunkt_lat`, `startpunkt_lon`, `startpunkt_hoyde_m`, `form`, `turtyper`, `lengde_m`, `hoydemeter_m`, `nedstigning_m`, `hoydeprofil`, `turniva`, `estimert_tid_min`, `ut_no_url`, `kilde`, `lisens` og `geometry`.
  - Meter og minutter er `int`. Lister lagres som tuples, så `Tur` kan hashes.
  - `Form` (`RUNDTUR="rundtur"`, `TUR_RETUR="tur-retur"`) og `Turniva` (`GRONN="gronn"`, `BLA`, `ROD`, `SVART`) er `StrEnum`.
  - Ved tur-retur gjelder verdiene én vei.
- Totaler regnes bare i `domene.tur`: `total_lengde_m`, `total_hoydemeter_m` og `total_nedstigning_m`. Ved tur-retur gjelder:
  - lengden ganges med 2;
  - høydemeter = `hoydemeter_m + nedstigning_m`;
  - nedstigning = `nedstigning_m + hoydemeter_m`.
- GeoJSON:
  - `til_geojson_feature()` gir `{"type": "Feature", "id": <id>, "geometry": <geometry>, "properties": {…alle andre felt…}}`, som kan gjøres om til JSON (lister, ikke tuples).
  - `fra_geojson_feature()` gjør om til tuples og enum igjen, så omformingen fram og tilbake gir lik tur.
- Gradering (`domene/gradering.py`):
  - Grensene i meter med «<»: grønn under 5000 m og under 300 hm, blå under 10 000 og under 600, rød under 20 000 og under 1000. Ellers svart (AR-19: ≥).
  - Den strengeste av lengde og høydemeter vinner.
  - Tur-retur graderes etter verdiene for én vei, og rundtur etter hele runden, altså de lagrede feltene i begge tilfeller.
- Tid (`domene/tid.py`):
  - (15 min/km + 15 min/100 hm opp + 15 min/200 m ned) × 1,15 regnes på totalene.
  - Rå tid avrundes halv opp til nærmeste 5 minutter. Hele 2,5 runder opp; `round()` brukes ikke, fordi den runder halve tall til nærmeste partall.
  - Regneeksempelet gir 142,3 min, som blir 140.
- Formatering (`domene/tekst.py`):
  - Tid: «ca. 45 min», «ca. 2 t», «ca. 1 t 35 min».
  - Lengde: «3,5 km totalt», med desimalkomma og én desimal, avrundet halv opp. Blir desimalen 0, droppes «,0» («6 km totalt»).
  - Nivå: «Grønn – lett», «Blå – moderat», «Rød – moderat», «Svart – vanskelig», med tankestrek.

**Never:**
- Haversine og avstandsfunksjonen kommer i 1.5. Høydeprofil, nivåtak, bøying av nivå og formatering av varighet kommer i senere stories.
- Ingen Django-modeller, ingen migreringer og ingen nye pakker.
- Appen beregner aldri nivå eller tid på nytt (AD-3 punkt 6). Funksjonene brukes av byggeskriptet.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Grønn | 4900 m, 299 hm | `GRONN` | N/A |
| Grense opp | 5000 m, 0 hm, eller 0 m, 300 hm | `BLA` | N/A |
| Rød / svart | 10 000 m eller 600 hm / 20 000 m eller 1000 hm | `ROD` / `SVART` | N/A |
| Strengeste | 3000 m, 650 hm | `ROD` | N/A |
| Regneeksempel | tur-retur, 3000 m, 150 hm, 0 ned | rå 142,3 min → 140 → «ca. 2 t 20 min» | N/A |
| Halv opp | rå tid 137,5 min | 140 | N/A |
| Format | 95 / 45 / 120 min, 3500 m, 6000 m, 5960 m | «ca. 1 t 35 min» / «ca. 45 min» / «ca. 2 t» / «3,5 km totalt» / «6 km totalt» / «6 km totalt» | N/A |
| Omforming | gyldig `Tur` | `fra_geojson_feature(t.til_geojson_feature()) == t` | Ukjent `form` eller `turniva` gir `ValueError` |

</frozen-after-approval>

## Code Map

- `domene/__init__.py` -- er tom. Nye moduler: `tur.py`, `gradering.py`, `tid.py` og `tekst.py`, som er navnene i kildetreet i spinen (l. 263).
- `tests/domene/test_bare_standardbibliotek.py` -- går gjennom alle `domene/**/*.py` med `ast` og godtar bare `sys.stdlib_module_names` og `domene`. Relative importer er tillatt. Ikke endre den.
- `tests/domene/` -- bruker `unittest.TestCase`, med krav-ID i en kommentar på hver test (`# FR-2`). Testene kjøres med `python manage.py test`.
- `ARCHITECTURE-SPINE.md` l. 69–92 -- AD-3 punkt 1 (feltene) og punkt 6. PRD `prd.md` l. 122–146 -- FR-2 og FR-3 med regneeksempelet.
- Det finnes ennå ingen kurateringsliste eller data. Testene lager `Tur` selv.

## Tasks & Acceptance

**Execution:**
- [x] `domene/tur.py` -- `Form`, `Turniva`, `Tur` med `til_geojson_feature`/`fra_geojson_feature` (klassemetode) og de tre totalfunksjonene -- AR-3
- [x] `domene/gradering.py` -- `turniva(lengde_m, hoydemeter_m) -> Turniva` med grensene som navngitte konstanter -- FR-2, AR-19
- [x] `domene/tid.py` -- `ra_tid_min(lengde_m, opp_m, ned_m) -> float`, `avrund_til_5(min) -> int` og `estimert_tid_min(tur-verdier eller Tur) -> int` på totalene -- FR-3
- [x] `domene/tekst.py` -- `formater_tid(min)`, `formater_lengde_totalt(m)` og `formater_niva(Turniva)` -- UX-DR31, AR-16
- [x] `tests/domene/test_tur.py`, `test_gradering.py`, `test_tid.py` og `test_tekst.py` -- én test per rad i matrisen og per AC, uten database, hver med FR- eller AR-ID -- AR-15, NFR-6

**Acceptance Criteria:**
- Gitt `domene/`, når `test_bare_standardbibliotek` kjøres, så består den med de nye modulene.
- Gitt tur-retur med 2000 m, 100 hm og 40 m ned, når totalene regnes, så blir de 4000 m, 140 hm opp og 140 m ned.
- Gitt en `Tur`, når et felt forsøkes endret, så kastes `FrozenInstanceError`.

## Implementation Notes

- 2026-11-23: Hannah godkjente specen og valgte å beholde den hel.

- 2026-11-23 (implementering):
  - `Tur.geometry` lagrer bare koordinatene, som tuples av `(lon, lat)`, fordi en GeoJSON-dict ikke kan hashes. `til_geojson_feature()` pakker dem inn i `{"type": "LineString", "coordinates": [...]}`. Byggeskriptet (1.5) og `lastinn` (1.6) må vite dette.
  - Totalfunksjonene og `estimert_tid_min(form, lengde_m, hoydemeter_m, nedstigning_m)` tar enkle verdier, ikke en `Tur`. Byggeskriptet må regne ut nivå og tid før `Tur` kan lages.
  - `fra_geojson_feature` gir også `ValueError` når Feature-typen er feil, eller geometrien ikke er en `LineString`.
  - Testen for halv opp har med 142,5, som blir 145. Der ville `round()` gitt feil svar, mens 137,5 gir 140 også med `round()`.
- 2026-11-23 (verifisering): etter rettingene fra gjennomgangen er 131 tester grønne, 38 av dem nye i `tests/domene/`. Ruff og migreringssjekken er rene.

## Spec Change Log

## Review Triage Log

Første gjennomgang (2026-11-23). B = Blind Hunter, E = Edge Case Hunter, V = Verification Gap.

| # | Funn | Verdikt | Begrunnelse | Rute |
|---|---|---|---|---|
| V1 | Alle tidstestene har lik opp og ned, så om `opp` og `ned` byttes i `estimert_tid_min`, merker ingen test det | medium | Det er reelt: for tur-retur er totalene alltid like, og begge rundtur-testene er symmetriske. En feil ville gitt feil lagret tid for rundturer | patch |
| V2/B1 | `ValueError` ved feil Feature-type eller geometri er ikke testet | low | Det er reelt: å fjerne sjekkene ville ikke fått noen test til å feile. Testene er direkte å legge til | patch |
| E4/B5 | `formater_lengde_totalt` kan få lengden for én vei og vise halve distansen | low | Navnet lover totallengde, men funksjonen tar en ren lengde. En docstring som peker til `total_lengde_m` er en direkte retting. Å endre signaturen ville endret specen | patch |
| B4 | Graderingstestene for tur-retur og rundtur tester ikke `form` | low | `turniva()` tar ikke `form`, med vilje: de lagrede verdiene er allerede én vei eller hele runden. Testnavnene villeder, og å endre dem er direkte | patch |
| B11 | Testturen heter `granvann-rundt`, men er tur-retur | low | Navnet villeder, og å endre det er direkte | patch |
| E1 | `formater_tid` med flyttall gir «2.0 t» | low | Typen er `int`, og den lagrede verdien er alltid heltall. En vakt gir mer kompleksitet | avvist |
| E2/E5/E7/E9/B9 | Negative verdier, 0 min og under 50 m gir rare tekster eller grønt nivå | low | Lengder og høyder fra byggeskriptet er aldri negative, og 0 min krever en tur under ca. 145 m. Rettingene er nye vakter | avvist |
| E3 | Svært korte turer viser «ca. 0 min» | low | Det krever en rå tid under 2,5 min (under ca. 145 m). Ingen tur i databasen er så kort | avvist |
| E6 | Ukjent nivå i `formater_niva` gir `KeyError` | low | Typen er `Turniva`, og verdiene kommer fra `fra_geojson_feature`, som validerer | avvist |
| E8 | NaN eller uendelig i `avrund_til_5` gir en uklar feil | low | Verdien kommer bare fra heltall via `Fraction` | avvist |
| E10 | En rå streng som `'TUR_RETUR'` faller i grenen for rundtur | low | Byggeskriptet (1.5) lager `Form` fra kurateringslista, og `Form(...)` validerer der. En vakt her gjelder en tilstand som ikke finnes ennå | avvist |
| E11/E12/E13/E14/B2 | Ugyldig GeoJSON (null-geometri, nøkler som mangler, streng som `turtyper`, flyttall eller None) gir `KeyError`, `TypeError` eller stille feil | low | Fila lages av vårt eget byggeskript og committes. Et unntak stopper `lastinn` uansett, og 1.6 krever atomisk lasting. Full validering er ny kompleksitet. Relevant for 1.6 | avvist |
| E15 | Nøstede lister i `hoydeprofil` er fortsatt lister | false | `tuple(punkt)` på `[avstand, hoyde]` gir en tuple av tall. Formatet har ikke dypere nøsting | avvist |
| E16 | `Tur` laget direkte med lister kan ikke hashes | low | Specen sier at listene lagres som tuples. Byggeskriptet i 1.5 må sende tuples (eller bruke `fra_geojson_feature`). `__post_init__` er en vakt mot en tilstand som ikke er vist | avvist |
| E17/B3 | Lagret nivå og tid sjekkes ikke mot reglene, og `Tur` har ingen invarianter | low | AD-3 punkt 6: nivå og tid regnes bare i byggeskriptet med de samme funksjonene. Validering er ny overflate | avvist |
| E18 | Specen lar `estimert_tid_min` ta en `Tur`, men implementasjonen tar verdier | false | Specen sier «tur-verdier eller Tur». Verdier oppfyller det, og byggeskriptet har ingen `Tur` ennå (Implementation Notes) | avvist |
| B6 | Tur-retur på 6 km totalt er grønn | false | Bestemt i FR-2: tur-retur graderes etter én vei | avvist |
| B7 | «Blå – moderat» og «Rød – moderat» er like | false | Bestemt i PRD §3 og DESIGN.md. Teksten skiller med «Blå» og «Rød», så farge er ikke eneste kjennetegn | avvist |
| B8 | «Sveitsisk regel» kan være feil navn | false | PRD FR-3 kaller regelen dette og definerer summen. Docstringen viser til FR-3 | avvist |
| B10 | Feltlista står tre steder | false | Et nytt felt uten standardverdi får konstruktøren i `fra_` til å feile, og testen for property-settet fanger `til_`. Testene oppdager altså forskjeller | avvist |

## Design Notes

Halv opp uten flyttallsfeil: `int(Decimal(str(x / 5)).quantize(Decimal("1"), ROUND_HALF_UP)) * 5`, eller tilsvarende `math.floor(x / 5 + 0.5) * 5`. Det siste er nok fordi x ≥ 0.

## Verification

**Commands:**
- `python manage.py test tests.domene` -- forventet: alle grønne
- `python manage.py test` -- forventet: alle grønne (minst 93 + de nye)
- `ruff check . && ruff format --check .` -- forventet: ingen funn
