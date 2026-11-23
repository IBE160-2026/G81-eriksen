---
title: 'Story 1.5: Byggeskriptet lager turdatabasen fra Kartverket'
type: 'feature'
created: '2026-11-23'
status: 'done'
baseline_commit: 'c7638a1a2ccd7eb6d1ea6f343f77c843829c835e'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-1-context.md'
  - '{project-root}/_bmad-output/implementation-artifacts/spike-1-5/README.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Det finnes ingen turdatabase. Appen skal aldri hente turdata mens den kjører. Derfor trengs et byggeskript som henter rute og høyder fra Kartverket, beregner verdiene gjennom `domene/` og skriver `data/turer.geojson` likt hver gang (AD-3, AR-2, AR-15).

**Approach:** `python -m skript.bygg_turdatabase` leser `data/kurateringsliste.toml` og gjør dette for hver tur:
1. henter segmentene fra WFS-en for Turrutebasen;
2. velger stien gjennom nettverket mellom rutepunktene;
3. henter høyder langs stien og filtrerer støy;
4. regner lengde, høydemeter, nivå og tid i `domene/`.

Alt skrives atomisk. Testene bruker lagrede svar.

**Beslutninger (Hannah, party-runde og spike 2026-11-23, se `spike-1-5/README.md`):**
- **Rutepunkter i stedet for kobling i rekkefølge.** Ett rutenummer er et nettverk av delte, usorterte segmenter med forgreininger. Hver tur har derfor `rutenummer` (en liste, som brukes til å hente segmentene) og `rutepunkter`:
  - `fra` og `til`, og valgfrie `via`, som `[lat, lon]`.
  - Rundtur har ikke `til`, slutter i `fra` og krever minst ett `via`. Tur-retur krever `til`, som er vendepunktet.
  - Skriptet finner korteste sti mellom hvert par av punkter. Dette erstatter «kobler endepunkter i rekkefølgen i kilde-ID-en» i Story 1.5 i epics.md.
- Rutepunktene festes til nærmeste node i nettverket innenfor **50 m**. Ellers stopper skriptet med tur-ID og avstand. Segmentenes endepunkter regnes som samme node innenfor **1 m**. Finnes det ingen sti mellom to punkter, stopper skriptet med tur-ID og rutenummer.
- Startpunktet (id, navn og koordinat, det Ola ser, for eksempel en holdeplass) er uavhengig av rutepunktene.
- Høyder hentes hvert **25 m**, med terskel **5 m**, og rest-differansen på slutten telles med.
- HTTP går via `urllib.request` fra standardbiblioteket, ikke `httpx2`.
- WFS-filteret bruker `app:fotruteInfo/app:FotruteInfo/app:rutenummer`.
- Høyde-API-et brukes med `koordsys=4258`, punktene som `[lon, lat]` og høyst 50 per kall.
- **Testturer:** Frognervassdraget (`F_01812_03`, tur-retur), Sognsvann–Brekke turvei og Rundtur Ulsrudvann (rundtur). Rutenummer og rutepunkter slås opp med ekte kall. Finnes en av dem ikke som Fotrute i Turrutebasen, brukes en annen grønn tur i Oslo eller Bærum med samme form, og valget noteres i Implementation Notes. Turene byttes ut i 1.7.
- Specen beholdes hel (ca. 3500 tokens).

## Boundaries & Constraints

**Always:**
- `skript/` importerer bare standardbiblioteket og `domene`. Alt som regner, går gjennom `domene/` (AR-2):
  - avstand med haversine (`domene.tur.avstand_m`, R = 6 371 008,8 m);
  - nettverk, festing og korteste sti, omsampling og støyfilter (ny modul `domene/rute.py`);
  - `gradering.turniva` og `tid.estimert_tid_min`.
- Ved tur-retur lagres geometri og verdier for én vei (`fra` → `til`). Ved rundtur lagres hele runden.
- `hoydeprofil` er de samme omsamplede punktene som høydemeterne regnes fra: `(avstand_m: int, hoyde_m: float med 1 desimal)`.
- `startpunkt_hoyde_m` hentes fra høyde-API-et ved startpunktets koordinat.
- `Tur` lages med tuples (ikke lister) og `Form(...)`. Turnavnet kommer bare fra lista.
- `kilde="turrutebasen"` og `lisens="CC BY 4.0"`. En `ut_no_url` som mangler, blir `""`.
- Lista valideres før noe hentes:
  - Samme startpunkt-ID med ulikt navn eller ulik koordinat gir stopp med startpunkt-ID-en.
  - Rundtur uten `via`, og tur-retur uten `til`, gir stopp med tur-ID.
- `data/osm-uttrekk.geojson` leses bare hvis fila finnes. 100 objekter eller flere gir stopp (AD-3 punkt 3). OSM-turer er ikke med i 1.5.
- Feil (HTTP, tidsavbrudd 60 s, 0 segmenter for et rutenummer, et punkt utenfor 50 m eller ingen sti) gir en norsk melding med tur-ID, og rutenummer der det gjelder, og exit-kode ≠ 0.
- Alt beregnes i minnet før noe skrives. Fila skrives til en midlertidig fil i `data/`, og `os.replace` bytter den inn. Den gamle `turer.geojson` blir aldri delvis overskrevet.
- Logging bruker én logger per modul. User-Agent er en konstant, `YourNextAdventure/0.1 https://github.com/IBE160-2026/G81-eriksen`, uten kontaktinfo.

**Never:**
- Ingen `pyproj`, ingen omregning, ingen nye pakker, ingen `httpx2` i skriptet og ingen nettverkskall i testene.
- Ingen `lastinn` og ingen modeller (1.6). Den endelige lista med 15 turer kommer i 1.7.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Gyldig liste | 2–3 testturer, svar fra fixtures | `turer.geojson` med alle feltene i AD-3, lengde = stiens lengde | N/A |
| Forgreinet nettverk | fixture `F_01812_03`, `fra` og `til` på samme komponent | stien går gjennom nettverket via korteste vei | N/A |
| Ingen sti | `fra` og `til` på hver sin komponent | ingen fil skrives | stopp med tur-ID og rutenummer |
| Punkt for langt unna | `via` > 50 m fra nærmeste node | ingen fil skrives | stopp med tur-ID og avstand |
| Ukjent rutenummer | WFS-svar med 0 features | gammel fil står | stopp med tur-ID og rutenummer |
| API feiler | HTTP 500 eller tidsavbrudd | gammel fil står | stopp med tur-ID |
| Ulikt startpunkt | samme startpunkt-ID med ulikt navn | ingenting hentes | stopp med startpunkt-ID |
| OSM ≥ 100 | `osm-uttrekk.geojson` med 100 objekter | ingenting skrives | stopp (AD-3 punkt 3) |
| Støy | profil med svingninger under 5 m | de teller ikke, men resten på slutten telles | N/A |

</frozen-after-approval>

## Code Map

- `domene/tur.py` -- `Tur`, `Form`, `Turniva`, `til_geojson_feature()` (`geometry` er en tuple av (lon, lat)) og totalfunksjonene. Legg til `avstand_m(a, b)` (haversine, `# AR-3`).
- `domene/gradering.py:27` `turniva(lengde_m, hoydemeter_m)` og `domene/tid.py:39` `estimert_tid_min(form, lengde_m, hoydemeter_m, nedstigning_m)` -- tar verdier for én vei.
- `domene/` -- ny `rute.py`. `tests/domene/test_bare_standardbibliotek.py` dekker den automatisk.
- `skript/__init__.py` -- finnes og er tom. Ny `skript/bygg_turdatabase.py`.
- `data/` og `tests/fixtures/` -- har bare `.gitkeep`. `tests/skript/` finnes ikke og trenger `__init__.py`.
- `spike-1-5/` -- `wfs_F_01812_03.xml` (22 segmenter, 2 komponenter), `hoyde_4258.json` og skriptene `s2.py`–`s5.py` med fungerende kall. `s5.py` dropper resten på slutten, og det skal ikke kopieres.
- `ARCHITECTURE-SPINE.md` l. 88 (AD-3 punkt 2) og Deferred l. 358–360 -- utdatert etter spiken. Oppdateres med en henvisning til denne specen.
- Mønster for tester: `unittest.TestCase`, med krav-ID i en kommentar. Ingen tester mocker nettverk i dag. Bruk én funksjon som henter fra nettet (`hent(url) -> bytes`), og bytt den ut i testene.

## Tasks & Acceptance

**Execution:**
- [x] `domene/tur.py` -- `avstand_m` (haversine) -- AR-3
- [x] `domene/rute.py`:
  - nettverk fra segmenter (noder innenfor 1 m);
  - `fest_punkt` (≤ 50 m) og korteste sti (Dijkstra) mellom rutepunktene, med sammenføyd `LineString` der segmenter snus ved behov;
  - omsampling hvert 25 m;
  - `hoydemeter_og_nedstigning(hoyder, terskel=5)` med resten på slutten;
  - høydeprofil.

  Feil gir egne unntak med nok informasjon til meldingen -- AR-2, AD-3
- [x] `skript/bygg_turdatabase.py`:
  - les og valider lista med `tomllib`;
  - `hent(url)` med `urllib.request`;
  - WFS-oppslag per rutenummer og parsing av `gml:posList` med `ElementTree`;
  - høyder i bolker på 50;
  - sjekk av OSM-uttrekket;
  - bygg `Tur`;
  - atomisk skriving;
  - `main()` med norsk melding og exit-kode -- AD-3, AR-2
- [x] `data/kurateringsliste.toml` og `data/turer.geojson` -- testturene, bygget med ekte kall -- AD-3 punkt 2
- [x] `data/README.md` -- formatet på lista, med feltene, rutepunktene og reglene for rundtur og tur-retur. Også toleransen på 1 m, festingen innenfor 50 m, punktavstanden på 25 m og terskelen på 5 m med begrunnelse fra spiken, og krediteringen (© Kartverket, CC BY 4.0) -- Deferred
- [x] `tests/fixtures/` -- lagrede WFS-svar:
  - et med flere segmenter (gjenbruk `F_01812_03`);
  - et med to komponenter, uten sti mellom punktene;
  - et med 0 features;
  - svar fra høyde-API-et for testturene.
- [x] `tests/skript/__init__.py` og `test_bygg_turdatabase.py`, `tests/domene/test_rute.py` og en test for `avstand_m` -- én test per rad i matrisen, med `hent` byttet ut og en midlertidig `data/`-mappe. Det skal også testes at `skript/` bare importerer standardbiblioteket og `domene` -- AR-2, AR-15
- [x] `ARCHITECTURE-SPINE.md` AD-3 punkt 2 og Deferred, og `.memlog.md` -- rutepunkter, korteste sti, toleranse, terskel, punktavstand og `urllib.request`, med henvisning til spiken

**Acceptance Criteria:**
- Gitt fixtures for testturene, når skriptet kjøres to ganger, så er `turer.geojson` byte for byte lik (deterministisk rekkefølge og avrunding).
- Gitt en hvilken som helst feil i matrisen, når skriptet stopper, så er innholdet i den gamle `turer.geojson` uendret, og det ligger ingen midlertidig fil igjen.
- Gitt `turer.geojson`, når hver feature leses med `Tur.fra_geojson_feature`, så lykkes det, og nivå og tid er lik det `domene/` gir for de lagrede verdiene.

## Implementation Notes

- 2026-11-23: Hannah godkjente specen og valgte å beholde den hel.
- 2026-11-23 (implementering): Alle tre testturene finnes som Fotrute og ble slått opp med ekte kall, så ingen ble byttet ut: Frognervassdraget `F_01812_03` (tur-retur, fra nordenden ved Sognsvann til Gaustad, 2213 m), Sognsvann–Brekke turvei `F_20220203_01` (tur-retur på den vestre av to komponenter, 1112 m) og Rundtur Ulsrudvann `F_20200422_1` (rundtur med to `via`, 1652 m). Startpunktene (Sognsvann holdeplass og Østmarksetra) er slått opp i Kartverkets stedsnavn-API.
- Små tillegg utover specen: punkter som gjentas rett etter hverandre i kilden (finnes i `F_01812_03`), tas med én gang i den sammenføyde linja; ligger siste omsamplede punkt under 0,5 m fra slutten, erstattes det av slutten; rutepunkter og startpunkt må ligge innenfor Norge (lat 57–72, lon 4–32), som fanger `[lon, lat]` skrevet feil vei; en test sjekker at committet `data/turer.geojson` er lik det fixturene gir.
- Fixture for ingen sti er `wfs_F_20220203_01.xml` (to komponenter), og fixture for 0 features er `wfs_tom.xml` (ekte svar for et ukjent rutenummer). Høydene ligger i `hoyder_testturer.json` som oppslag fra `lon,lat` til `z`.
- 2026-11-23 (etter review): alle lese-, hente- og skrivefeil blir `ByggFeil` med norsk melding (exit 1, gammel fil står); ukjente felt i lista gir stopp; to rutepunkter etter hverandre på samme node gir `PunkterPaSammeNode` i stedet for å hoppe over punktet; Østmarksetra har nå full koordinat (59.889997, 10.864696, regnet om fra stedsnavn-API-ets UTM 33-punkt, siden 4258-svaret er avrundet); 25 m / 5 m står som åpen Deferred-rad til kontroll i 1.7.

- 2026-11-23 (verifisering): etter rettingene fra gjennomgangen er 199 tester grønne uten nett. Ruff og migreringssjekken er rene. To ekte kjøringer gir lik `turer.geojson`.

## Spec Change Log

## Review Triage Log

Første gjennomgang (2026-11-23). B = Blind Hunter, E = Edge Case Hunter, V = Verification Gap. Diffen tok ikke med `tests/fixtures/` og `data/turer.geojson`, fordi de er rådata eller genererte filer. De dekkes av testene.

| # | Funn | Verdikt | Begrunnelse | Rute |
|---|---|---|---|---|
| E1/E2/E6/E7/E10/E17/B4 | Flere feil gir en Python-traceback i stedet for en norsk melding: `float(z)` utenfor `try`, `HTTPException` fra `read()`, `UnicodeDecodeError`/`OSError` på lista og OSM-fila, `OSError` fra `skriv_atomisk` | medium | Det er reelt: `main` fanger bare `ByggFeil`. Den frosne intensjonen lover en norsk melding og exit ≠ 0. Rettingene er direkte | patch |
| V1/V2/V3/B12a | Feilveiene i `hent_hoyder`, `les_segmenter` og `hent` (URLError uten tidsavbrudd, ConnectionReset) er ikke testet | medium | Det er reelt (VG har verifisert det): å fjerne vaktene ville ikke fått noen test til å feile | patch |
| E8/B5 | Ukjente nøkler i lista (for eksempel `vai`) ignoreres stille | medium | En skrivefeil gir en annen sti uten stopp, og 1.7 skal kurere 15 turer. Rettingen er en direkte sjekk | patch |
| E14/B6b | Et `via` som festes til samme node som forrige punkt, forsvinner stille | medium | Det er reelt: `if fra == til: continue`. Rettingen (stopp i stedet) er direkte | patch |
| B8 | Startpunktet ved Østmarksetra har bare 2 desimaler (±500 m) | medium | Det er reelt: kartmarkøren og `startpunkt_hoyde_m` blir feil i committede data | patch |
| B12b | To rutenummer med delte segmenter er ikke testet | low | README lover at dubletter tas med én gang. Testen er direkte | patch |
| B9 | «Halvparten så mange kall» er feil, 25 m gir 40 % | low | Det er en direkte retting av teksten | patch |
| B11 | Eksempelet i README har et oppdiktet `via` | low | Det er en direkte retting | patch |
| B10 | Deferred-raden om publiserte høydeprofiler er fjernet, men sammenligningen er ikke gjort | low | Det er reelt: et åpent punkt ble lukket uten å være gjort. Rettingen er en direkte retting av teksten (holdes åpent til 1.7) | patch |
| E4/B2 | WFS-svaret sjekkes ikke for avkorting eller paging | false | GetCapabilities har ingen `CountDefault`, og `ImplementsResultPaging` er FALSE. Serveren kutter ikke svaret | avvist |
| B6a | Ingen sjekk av at en rundtur faktisk går i ring (samme kanter ut og inn) | low | Det er en sjekk av kurateringen som hører til 1.7, når de 15 turene kontrolleres. Den krever ny logikk | defer |
| E11/E12/B7 | Lukkede segmenter (ring) faller bort, og T-kryss eller festing midt på et segment er ikke mulig | maybe-false | Specen sier at punktene festes til noder. Om Turrutebasen har ringsegmenter eller T-kryss som trengs for turene i 1.7, avgjøres når de turene kureres. Hvis det stemmer, er det medium | defer |
| E13 | Første node innenfor 1 m vinner, ikke den nærmeste | low | Spiken viste at endepunktene treffer eksakt (0 m), så det skjer ikke i praksis | avvist |
| E15 | En rundtur kan få `geometry[0] != geometry[-1]` innenfor 1 m | low | Avviket er under 1 m. GeoJSON krever ikke at en `LineString` er lukket | avvist |
| E16 | Avrunding til desimeter før terskelen lar 4,95 m telle | low | Det utgjør høyst 0,05 m, langt under målenøyaktigheten | avvist |
| E3 | Høyde-API-et kan svare i en annen rekkefølge | low | API-et svarer i samme rekkefølge som punktene ble sendt (spiken), og sjekken av antall finnes | avvist |
| E5 | `gml:pos` i stedet for `posList` | low | Alle svarene i spiken og i fixtures bruker `posList` | avvist |
| E9 | Like turtyper | low | Skjer sjelden og er ufarlig | avvist |
| B3 | `datakilde` som ikke er `dtm1`, sjekkes ikke | low | Oslo og Bærum dekkes av `dtm1`. En sjekk gir ny logikk | avvist |
| B13 | Ingen nye forsøk eller hurtigbuffer, og Sognsvann hentes to ganger | low | En kjøring som feiler, kjøres på nytt og skriver ikke halve filer. Hurtigbufferen sparer ett kall | avvist |
| B14 | Høydedataene har ikke egen kreditering i fila | false | Både ruter og høyder er fra Kartverket med CC BY 4.0. «© Kartverket» dekker begge, og README nevner høydedataene | avvist |
| B1 | Fixtures, data og `skript/__init__.py` mangler i diffen | false | De er tatt ut av diffen med vilje (rådata), og `skript/__init__.py` finnes fra 1.1. Alt committes | avvist |

## Design Notes

- Omsamplingen gir alle punktene langs hele stien. Lengden er summen av haversine-avstandene langs den sammenføyde geometrien, avrundet til hele meter.
- Støyfilteret med hysterese: start med `ref = z[0]`. Når `|z - ref| ≥ terskel`, legges differansen til opp eller ned, og `ref = z`. Til slutt legges `z[-1] - ref` til hvis den ikke er 0.
- Rekkefølgen i fila følger lista. JSON skrives med `ensure_ascii=False`, `indent=2` og sorterte nøkler i `properties`, så diffen blir stabil.

## Verification

**Commands:**
- `python manage.py test` -- forventet: alle grønne, uten nettverk
- `ruff check . && ruff format --check .` -- forventet: ingen funn
- `python -m skript.bygg_turdatabase` (med nett) -- forventet: `data/turer.geojson` for testturene. En ny kjøring gir ingen diff
