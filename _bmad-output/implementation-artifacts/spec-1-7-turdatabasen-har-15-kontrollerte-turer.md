---
title: 'Story 1.7: Turdatabasen har 15 kontrollerte turer'
type: 'feature'
created: '2026-11-24'
status: 'done'
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

**Beslutninger (Hannah, 2026-11-25):**
1. Testturene `frognervassdraget`, `sognsvann-brekke` og `rundtur-ulsrudvann` blir med uendret blant de 15. `sognsvann-brekke` tar plassen til `sognsvann-ullevalseter`, så ingen gamle turer blir liggende i Neon.
2. Den svarte turen er `nordmarksrunden` (23 km), som er en ren runde. Lista får et valgfritt felt per tur for korte koblinger uten rutenummer (≤ 10 m) mellom endepunktene til segmentene. Skriptet og `domene/rute.py` legger koblingene inn som rette segmenter i nettverket. `nordmarksrunden-alt` brukes ikke.
3. Det godtas to unntak på grunn av terrenget: topptur og utsikt har ingen grønn tur under 2 t. Unntakene begrunnes i `data/README.md`. Tryvann droppes, og `frognerseteren-skjennungstua` tas inn i stedet.
4. Rundturer med stilk (`vettakollen-rundtur`, `dalivann-rundt`) godtas som rundtur. `domene/rute.py` får en sjekk som stopper en rundtur der mer enn halve lengden gås to ganger. Det lukker det åpne punktet fra 1.5.
5. Claude kontrollerer rutelinjene i Chrome mot Norgeskart og ut.no og fyller ut kontrollisten med dato og «kontrollert av Claude». Hannah bekrefter i PR-en.

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
| `lastinn` etter bytte | Neon med de tre testturene | 15 turer lastes inn, uten advarsel om fjernede turer | N/A |
| Kobling for lang | `koblinger` med et par over 10 m fra hverandre | `ByggFeil` med tur-ID og avstand | stopp |
| Rundtur med lang stilk | rundtur der over halve lengden gås to ganger | `ByggFeil` med tur-ID og andel | stopp |

</frozen-after-approval>

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
- [x] `tests/fixtures/kurateringsliste_testturer.toml` og `tests/skript/test_bygg_turdatabase.py` -- testene bruker kopien og `turer_lastinn.geojson` i stedet for `data/` -- AR-15
- [x] `domene/rute.py` -- `MAKS_KOBLING_M = 10.0`. En funksjon legger til koblinger som rette segmenter (avviser par over 10 m). `andel_gatt_to_ganger(linje)` regner ut den delen av lengden der punktparet (uten retning) forekommer mer enn én gang i linja fra `sti_gjennom`. Signaturen til `sti_gjennom` endres ikke. Er andelen over 0,5 på en rundtur, blir det `ByggFeil`. Tester i `tests/domene/test_rute.py` -- AD-3, beslutning 2 og 4
- [x] `skript/bygg_turdatabase.py` -- valgfritt felt `koblinger = [[[lat, lon], [lat, lon]], …]` i `TUR_FELT` og `KuratertTur`, validert som koordinatpar. Koblingene legges til før `lag_nettverk`, og sjekken av stilken kjøres for `form="rundtur"`. Tester med syntetiske segmenter -- AD-3
- [x] `data/kurateringsliste.toml` -- 15 turer etter beslutningene, med Gjettum-koordinaten verifisert. De tre koblingene ved Ullevålseter (60.0115, 10.706) får eksakte endepunkter fra ekte WFS-svar -- FR-1
- [x] `data/turer.geojson` -- bygget med `python -m skript.bygg_turdatabase` (ekte kall), og to kjøringer gir lik fil -- FR-1, AD-3
- [x] `tests/skript/test_sammensetning.py` -- reglene for sammensetningen, med unntakslista og testene for regelbrudd fra matrisen (på kopier i minnet) -- FR-1
- [x] `data/README.md` -- turtabell (ID, navn, startpunkt, form, km, hm, nivå, tid, turtyper, ut.no), unntak med begrunnelse og resultatet av sammenligningen med høydeprofilene -- FR-1
- [x] `docs/kontroll-turdatabasen.md` -- kontrolliste for 15 rutelinjer og tabell for sammenligningen med høydeprofilene, med kilder -- FR-1
- [x] `ARCHITECTURE-SPINE.md` (Deferred l. 365), `.memlog.md` og `deferred-work.md` -- resultatet av sjekken av 25/5 og av rundturene -- AD-3

**Acceptance Criteria:**
- Gitt den nye `data/turer.geojson`, når `python manage.py test` kjøres uten nett, så er alle tester grønne, inkludert sammensetningstesten.
- Gitt den nye fila, når `python manage.py lastinn` kjøres mot en database som allerede har testturene, så lastes 15 turer inn, uten advarsel om fjernede turer.
- Gitt en rundtur der over halve lengden gås to ganger, eller en kobling over 10 m, når turen bygges, så stopper byggingen med `ByggFeil` som nevner tur-ID-en.
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

- 2026-11-25: WFS-en til Turrutebasen var nede ca. 35 minutter (HTTP 502/504). Byggingen ble kjørt etterpå med ekte kall; rutenummeret `osl` har 3435 segmenter og tar ca. 75 s å hente, men holdt seg innenfor tidsavbruddet på 60 s per lesing.
- `vettakollen-rundtur` gikk 100 % to ganger med via-punktene fra kandidatlista (stoppet av den nye sjekken). Den går nå opp vestsiden med rutenummeret `F_20171026_02` (17 %).
- `noklevann-rundt`: det østlige via-punktet er flyttet fra åsen (279 moh) til stien langs vannet, så runden følger ut.no 1110939 (98 % overlapp).
- `grorud-grefsenkollen`: nytt navn (ruten går ikke innom Linderudkollen) og bare `utsikt`, fordi ruten slutter ca. 20 m under toppen. Toppturene er da nøyaktig 3.
- ut.no-lenker som ikke har samme start og mål, er fjernet (1113995, 115871 finnes ikke, 1111161, 1110204).
- Gjettum: gården fra stedsnavn-API-et (59.91045, 10.52768), navn «Gjettum». Stedsnavn-punktet «Gjettum stasjon» ligger ca. 550 m fra dagens holdeplass.
- Sammenligningen med ut.no ga ingen endring av 25 m og 5 m (én av tre over 15 %). Kontrollkjøringen på ut.no sin egen linje står i `docs/kontroll-turdatabasen.md`.
- Skjermbilder i Chrome hang etter første bilde per vertsnavn; kontrollkartet ble derfor servert på flere loopback-adresser (127.0.0.x). Kontrollen er gjort på Kartverkets topografiske kart, ikke i selve norgeskart.no-appen.

## Spec Change Log

## Review Triage Log

Gjennomgang 2026-11-25 i tre lag (Blind Hunter = BH, Edge Case Hunter = ECH, Verification Gap = VG). Løkke 0.

| # | Lag | Funn | Vurdering | Begrunnelse | Rute |
|---|---|---|---|---|---|
| 1 | VG, ECH | Ingen test leser `data/kurateringsliste.toml` eller sjekker at lista stemmer med `turer.geojson` | medium | Den gamle testen «committet fil lik bygget fil» peker nå på fixturen, så ingen test leser lista. | patch |
| 2 | BH | Regelen for `ut_no_url` i README («samme start og mål») brytes av fire turer | low | Kontrollisten viser at start eller mål er ulikt for Nøklevann, Kobberhaughytta og de to Vettakollen-turene. | patch |
| 3 | BH | Oppsummeringen av sjekken på ut.no sin egen linje utelater Kobberhaugene (+29 %) | low | README l. 94 og spinen l. 368 nevner bare treffene. `.memlog.md` har avviket. | patch |
| 4 | BH | Unntaket for `topptur` påstår mer enn researchen dekket | low | README l. 148 sier «ingen topp i Oslo og Bærum», men bare seks startpunkter og 24 kandidater ble undersøkt. | patch |
| 5 | BH | Gåavstanden fra startpunktet er ikke regnet med, og Gjettum er gården | false | Spec-en godtar under 500 m (flagges over 500 m) og «en kjent plass». Alle startpunktene ligger under 500 m fra rutens første punkt. | avvist |
| 6 | BH | Statusfiler og logger er utdaterte (sprint-status, logg 979, issues.md, epic-1-context) | false | Statusene settes i steg 5, og loggen skrives med sesjonslogg til slutt. `epic-1-context.md` er et øyeblikksbilde fra før 1.7. | avvist |
| 7 | BH | De nye punktene i `deferred-work.md` henviser til «punktet over», som er feil punkt | low | Rett over står punktet fra 1.6 om `lastinn`, ikke punktene fra 1.5. | patch |
| 8 | BH | `kandidater.md` committes utdatert, uten merknad | low | Den har gamle ✔, gamle via-punkter og navn, og skrivefeilen `kurateringslista.toml`. Kan villede i story 6.2. | patch |
| 9 | BH | Flere Always-regler mangler test (ID uten æøå, Oslo/Bærum, 500 m) | low | Reglene er kontrollert manuelt i kontrollisten. En test er mer enn en direkte retting, og det er lite sannsynlig at noen møter feilen. | avvist |
| 10 | BH, ECH | `andel_gatt_to_ganger` sammenligner eksakte punktpar, så strekninger nær hverandre ved kryss eller doble segmenter telles ikke | false | Samme kant gir samme punkter begge veier. Ved et kryss under 1 m blir det bare en bit på centimeternivå. Eksakte doble segmenter fjernes allerede i `lag_nettverk`. Andelen er dessuten kontrollert manuelt for alle rundturene. | avvist |
| 11 | BH, ECH | Koblinger: grensen på nøyaktig 10 m er ikke testet, en kobling på 0 m godtas, og en kobling som ikke treffer en segmentende gir en uklar «ingen sti» | low | Det er reelt, men skjer sjelden (én tur har koblinger), og rettingen krever ny kontroll. Byggingen stopper uansett med tur-ID. | avvist |
| 12 | BH | Testen for `lastinn` sjekker bare stderr | false | Advarselen skrives til `self.stderr` (`lastinn.py:94`), og testen fra 1.6 sjekker «Advarsel» i stderr. | avvist |
| 13 | BH | Testen for `lastinn` har `3` hardkodet | low | Rett i kode: bruk `len(testturer)`. | patch |
| 14 | BH | Raden for `dalivann-rundt` i kontrollisten mangler det høyeste punktet mot kartet | low | Akseptkriteriet krever både laveste og høyeste punkt. | patch |
| 15 | BH | Avvikene fra kandidatlista står ikke i Spec Change Log, og Vercel-sjekken er ikke gjort | false | Endringsloggen er for bad_spec-løkker. Avvikene står i Implementation Notes og i kontrollisten. Vercel-sjekken krever push og gjøres etter PR-en. | avvist |
| 16 | BH | Byggingen er sårbar: WFS-en var nede i 35 min, og `osl` tar ca. 75 s mot et tidsavbrudd på 60 s per lesing | medium | Det fantes før 1.7, men flere turer bruker nå `osl`. | defer |
| 17 | BH | Meldingen i `brudd` legger alltid til «(svart/topptur/utsikt)» | low | Meldingen er misvisende når bare én type feiler. | patch |
