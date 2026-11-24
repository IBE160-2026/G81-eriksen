---
title: 'Story 1.7: Turdatabasen har 15 kontrollerte turer'
type: 'feature'
created: '2026-11-24'
status: 'draft'
baseline_commit: 'b33948cdba0a5b4aa3a35a6315e45a27f627a029'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-1-context.md'
  - '{project-root}/_bmad-output/implementation-artifacts/research-1-7/kandidater.md'
  - '{project-root}/data/README.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** `data/turer.geojson` har bare de tre testturene fra 1.5. FR-1 krever minst 15 kontrollerte turer i Oslo og Bærum med en bestemt sammensetning, manuell kontroll av hver rutelinje og sammenligning med publiserte høydeprofiler. Ellers har søket i 1.8–1.12 for lite å velge mellom.

**Approach:** `data/kurateringsliste.toml` får 15 turer valgt fra `research-1-7/kandidater.md`, med rutepunkter som ligger nøyaktig på noder i nettverket. `data/turer.geojson` bygges med ekte kall. En test sjekker sammensetningen. `data/README.md` får turtabellen og begrunnede unntak, og `docs/` får en datert kontrolliste for rutelinjene og sammenligningen med høydeprofilene. Testene som i dag er låst til de tre testturene, flyttes til faste kopier i `tests/fixtures/`.

## Boundaries & Constraints

**Always:**
- Sammensetningen (FR-1):
  - flertallet grønne eller blå;
  - minst én svart, minst tre toppturer og minst fem utsiktsturer;
  - hvert startpunkt har minst to turer;
  - hver turtype har en grønn tur under 2 t (`estimert_tid_min < 120`), unntatt der et unntak er begrunnet i `data/README.md` og står i testen.
- Tur-ID-er er permanente når de er bygget. Navn og ID er på norsk uten æ, ø og å i ID-en.
- Startpunktene ligger i Oslo eller Bærum. Navnet er det Ola kjenner igjen, for eksempel en holdeplass eller en kjent plass. Koordinaten slås opp i Kartverkets stedsnavn-API eller tas fra kandidatlista, og samme ID har alltid samme navn og koordinat.
- `kilde="turrutebasen"` og `lisens="CC BY 4.0"` på alle turene. Det finnes ikke noe OSM-uttrekk (0 objekter, under 100).
- Sammenligningen med publiserte høydeprofiler gjelder tre turer: `vettakollen-topp`, `noklevann-rundt` og `frognerseteren-kobberhaughytta`. Kolsåstoppen er reserve.
  - For hver tur sammenlignes lengde, høydemeter og laveste og høyeste punkt mot ut.no, som oppgir sidenummer.
  - 25 m og 5 m endres bare hvis høydemeterne våre avviker mer enn 15 % fra den publiserte verdien på minst to av de tre. Da oppdateres konstantene i `domene/rute.py`, fixtures lages på nytt, og begrunnelsen skrives i `data/README.md`.
  - Resultatet og Deferred-raden i spinen (l. 365) oppdateres.
- Kontrollisten ligger i `docs/kontroll-turdatabasen.md` og har én rad per tur:
  - dato;
  - om ruten henger sammen;
  - avstanden fra startpunktet til rutens første punkt (flagges over 500 m);
  - formen, det vil si om rundturen går i ring, og om den har en del som gås to ganger;
  - laveste og høyeste punkt mot kartet;
  - hvem som kontrollerte.
- Testen for sammensetningen leser `data/turer.geojson` og går uten nett. Den antar ikke nøyaktig 15 turer (`epics.md`), bare minst 15.
- Byggeskriptets tester bruker `tests/fixtures/kurateringsliste_testturer.toml`, en kopi av dagens liste. Testen for «committet fil lik bygget fil» sammenligner med `tests/fixtures/turer_lastinn.geojson`, så de fortsatt går uten nett.

**Never:**
- Ingen nettkall i testene, og ingen nye pakker.
- Ingen turer utenfor Oslo og Bærum, og ingen OSM-turer.
- Ingen turtype som ikke stemmer med ruten. Ruten til Tryvann når for eksempel ikke toppen og skal ikke merkes som topptur.
- Ingen endring av `lastinn`, modellene eller migreringene.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Bygging | 15 turer i lista, ekte kall | `turer.geojson` med 15 turer; to kjøringer gir lik fil | stopp med tur-ID ved feil (fra 1.5) |
| Sammensetning ok | dagens `turer.geojson` | testen er grønn og viser antall per nivå og turtype | N/A |
| Regelbrudd | kopi der den svarte turen er fjernet | testen feiler og sier hvilken regel som brytes | N/A |
| Unntak | turtype uten grønn tur under 2 t | godtas bare hvis turtypen står i unntakslista i testen | feiler og nevner turtypen |
| Startpunkt med én tur | kopi med én tur fjernet fra et startpunkt | testen feiler med startpunkt-ID | N/A |
| `lastinn` etter bytte | Neon med de gamle testturene | turer som ikke er med i fila, gir advarsel og står (fra 1.6) | se Open Questions 1 |

</frozen-after-approval>

## Open Questions

1. **Testturene fra 1.5** (`frognervassdraget`, `sognsvann-brekke`, `rundtur-ulsrudvann`):
   - **(A)** Behold alle tre uendret blant de 15. `sognsvann-brekke` tar plassen til `sognsvann-ullevalseter`. Da blir det ingen gamle turer i Neon.
   - **(B)** Dropp `sognsvann-brekke`, som er en triviell tur på 1,1 km. Den blir da liggende i Neon for alltid og gir en advarsel ved hver bygging.
   - **(C)** Dropp den og slett den én gang for hånd i Neon. Det er trygt nå, fordi ingen registreringer peker på den, men det er et unntak fra «sletter aldri».
2. **Den svarte turen.** Svart krever 20 km eller mer, eller 1000 høydemeter eller mer. Ingen tur her kommer i nærheten av 1000 hm, så det må bli en lang rundtur.
   - **(A)** `nordmarksrunden-alt` (26,4 km). Den kan bygges i dag, men 5,4 km av den gås to ganger, som en «stilk» ut og inn.
   - **(B)** `nordmarksrunden` (23 km), som er en ren runde. Den trenger tre små segmenter på 2–9 m ved Ullevålseter som ikke har rutenummer, så lista må få et nytt valgfritt felt for korte koblinger (≤ 10 m) med endringer i skriptet og `domene/rute.py`.
   - **(C)** Hent segmenter innenfor et område rundt et punkt. Det er en større endring i skriptet.
3. **Grønn tur under 2 t for topptur og utsikt.** Ingen sammenhengende tur fra en holdeplass klarer dette. Tidsformelen gir 15 % påslag, og en topp krever 150 høydemeter eller mer. Vettakollen er nærmest med 2 t 10 min.
   - **(A)** Godta to unntak på grunn av terrenget, begrunnet i `data/README.md`. Tryvann droppes, og `frognerseteren-skjennungstua` (blå, marka) tas inn i stedet.
   - **(B)** Let videre, med mer research og muligens kortere og mindre kjente topper.
4. **Rundturer med stilk** (`vettakollen-rundtur`, `dalivann-rundt`, og den svarte hvis 2A velges):
   - **(A)** Godta dem som rundtur. Legg til en sjekk i `domene/rute.py` som stopper en rundtur der mer enn halve lengden gås to ganger. Det lukker det åpne punktet fra 1.5.
   - **(B)** Godta dem uten kodesjekk. Stilken noteres i kontrollisten, og punktet lukkes med den manuelle kontrollen.
5. **Hvem kontrollerer rutelinjene mot kartet?**
   - **(A)** Claude kontrollerer i Chrome mot Norgeskart og ut.no, fyller ut kontrollisten med dato og «kontrollert av Claude», og Hannah bekrefter i PR-en.
   - **(B)** Hannah kontrollerer alt selv ut fra en mal med kartlenker.

## Code Map

- `data/kurateringsliste.toml` -- dagens tre testturer. Startpunktene er `sognsvann` (59.96711, 10.73382) og `ostmarksetra` (59.889997, 10.864696). Header-kommentaren på l. 4–5 gjelder 1.5 og skal oppdateres.
- `research-1-7/kandidater.md` -- 24 kandidater med nøyaktige noder (`fra`/`via`/`til`) og rutenummer, så de kan limes rett inn. Tallene er beregnet med 50 m punktavstand, mens skriptet bruker 25 m, så høydemeterne kan bli litt høyere (Kolsåstoppen har 292 hm og kan bli blå). Gjettum-koordinaten må sjekkes (stedsnavn-API-et gir tre treff).
- `skript/bygg_turdatabase.py` -- skjemaet står på :63–67 og valideringen på :236–338. `KILDE`/`LISENS` står på :68–69. Ukjente nøkler gir stopp.
- `domene/rute.py` -- `NODETOLERANSE_M` (:24), `MAKS_FESTEAVSTAND_M` (:25), `PUNKTAVSTAND_M = 25` (:26) og `STOYTERSKEL_M = 5` (:27). En lukket ring hoppes over (:153), og det finnes bare noder i segmentender.
- `domene/gradering.py:13–18` -- grønn er under 5 km og 300 hm, blå under 10 km og 600 hm, rød under 20 km og 1000 hm, ellers svart. `domene/tid.py` beregner tiden. `domene/tur.py` har `TURTYPER`, `Turniva` og `fra_geojson_feature`.
- `tests/skript/test_bygg_turdatabase.py` -- disse er låst til de tre testturene:
  - `bruk_ekte_liste` (:93–94);
  - ID-lista (:115–119);
  - endepunkter og ringen (:149–157);
  - høyden ved Sognsvann (:159–163);
  - committet fil lik fixture-bygget (:172–177);
  - `F_20200422_1` (:235–240).

  Hvis 25 m endres, må `tests/fixtures/hoyder_testturer.json` (nøklet på omsamplede punkter) og `tests/domene/test_rute.py:133–138` følge med.
- `tests/web/test_lastinn.py` og `test_turdata.py` -- bruker allerede fixturen eller avleder antall fra fila, så de er trygge.
- `data/README.md` -- «Høyder og støyfilter» (:68, notatet om 1.7 på :75) og «Testturene (story 1.5)» (:83). Den siste erstattes av «Turene» og «Sammensetning og unntak».
- `docs/` -- inneholder bare `arkitektur.md` og briefene. Kontrollisten er ny. `epics.md:1985–1986` forventer laveste og høyeste punkt mot kartet.
- `ARCHITECTURE-SPINE.md` Deferred l. 365 (25/5 mot publiserte profiler) og `deferred-work.md` (rundtur i ring, festing bare i segmentender) lukkes eller oppdateres med resultatet.

## Tasks & Acceptance

**Execution:**
- [ ] `tests/fixtures/kurateringsliste_testturer.toml` og `tests/skript/test_bygg_turdatabase.py` -- testene bruker kopien og `turer_lastinn.geojson` i stedet for `data/` -- AR-15
- [ ] `data/kurateringsliste.toml` -- 15 turer etter beslutningene, med Gjettum-koordinaten verifisert -- FR-1
- [ ] `data/turer.geojson` -- bygget med `python -m skript.bygg_turdatabase` (ekte kall), og to kjøringer gir lik fil -- FR-1, AD-3
- [ ] `tests/skript/test_sammensetning.py` -- reglene for sammensetningen, med unntakslista og testene for regelbrudd fra matrisen (på kopier i minnet) -- FR-1
- [ ] `data/README.md` -- turtabell (ID, navn, startpunkt, form, km, hm, nivå, tid, turtyper, ut.no), unntak med begrunnelse og resultatet av sammenligningen med høydeprofilene -- FR-1
- [ ] `docs/kontroll-turdatabasen.md` -- kontrolliste for 15 rutelinjer og tabell for sammenligningen med høydeprofilene, med kilder -- FR-1
- [ ] `ARCHITECTURE-SPINE.md` (Deferred l. 365), `.memlog.md` og `deferred-work.md` -- resultatet av sjekken av 25/5 og av rundturene -- AD-3

**Acceptance Criteria:**
- Gitt den nye `data/turer.geojson`, når `python manage.py test` kjøres uten nett, så er alle tester grønne, inkludert sammensetningstesten.
- Gitt den nye fila, når `python manage.py lastinn` kjøres mot en database som allerede har testturene, så lastes 15 turer inn, og advarselen viser bare turer som er bevisst fjernet.
- Gitt kontrollisten, når den leses, så har alle 15 turene en datert rad uten åpne avvik, og tre turer er sammenlignet med ut.no med sidenummer.

## Verification

**Commands:**
- `python manage.py test` -- forventet: alle grønne, uten nett
- `ruff check . && ruff format --check .` -- forventet: ingen funn
- `python -m skript.bygg_turdatabase` to ganger (med nett) -- forventet: ingen diff i `data/turer.geojson` etter andre kjøring
- `python manage.py lastinn` -- forventet: 15 turer lastet inn

**Manual checks:**
- Kontrollisten i `docs/` er utfylt for alle turene. Byggeloggen til forhåndsvisningen på Vercel viser 15 turer.

## Implementation Notes

## Spec Change Log

## Review Triage Log
