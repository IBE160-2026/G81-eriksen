---
title: "Sprint Change Proposal: rettinger etter readiness gate"
status: approved
approved: 2026-11-22
approved_by: Hannah (produkteier)
created: 2026-11-22
workflow: bmad-correct-course
mode: batch
scope: moderate
trigger: "Readiness gate i bmad-sprint-planning 2026-11-20 (CONCERNS, 6 funn) og kompileringen av epic-1-context.md (10 uklarheter)"
---

# Sprint Change Proposal: rettinger etter readiness gate (2026-11-22)

## Beslutninger og godkjenning

Hannah (produkteier) godkjente forslaget 2026-11-22, med disse avklaringene:

1. **Kreditering der Turillustrasjon vises uten kart** (nytt funn 3) tas med: EP-29, UXE-03 og UXE-05.
2. **«Start fra første forslag igjen»** blir en POST-knapp: EP-10 og UXD-01.
3. **Ruff:** En ny fil, `requirements-dev.txt`, med `ruff==0.17.4` (låst, fra Stack) erstatter `requirements-bygg.txt`. Vercel installerer den ikke. Installasjonen i AD-12 og README sier at `pip install -r requirements-dev.txt` trengs for utvikling og for å kjøre `ruff check .` og `ruff format --check .`. Endringene står som EP-03, EP-14, EP-30, EP-31, EP-32, SP-06, SP-08, SP-11, SP-17, SP-18, DOC-03, DOC-04 og ML-01.

Endringene i seksjon 4 er lagt inn i planfilene 2026-11-22. Restene fra kontrollen etterpå står i seksjon 6.

## 1. Sammendrag av problemet

**Hva utløste endringen.** Readiness gate i `bmad-sprint-planning` 2026-11-20 ga **CONCERNS** med 6 funn. Da `_bmad-output/implementation-artifacts/epic-1-context.md` ble kompilert, kom det fram 10 uklarheter til. Ingen story er startet, og det finnes ingen kode. Hannah valgte å rette planen før implementeringen begynner. Modus: samlet (batch).

**Problemet.** Planartefaktene (PRD, epics, spinen, UX og `docs/arkitektur.md`) er uenige med hverandre på flere punkter, eller de mangler en regel som Epic 1 trenger. Funnene fra de to kildene er slått sammen og merket A–L. Funn 10 fra kompileringen (CSP mot Leaflet) står for seg selv.

| Funn | Kort beskrivelse | Bevis |
|---|---|---|
| A | Spinen sier at Turrutebasen bare finnes i UTM, og at `pyproj` derfor trengs. WFS-en gir WGS84 direkte. Hver rute består av flere segmenter, og ingen story sier hvordan de settes sammen | WFS testet 2026-11-22: HTTP 200, GML 3.2.1 i EPSG:4326, `gml:posList` i rekkefølgen lon lat. Spinen AD-3 punkt 2, Stack og Story 1.5 forutsetter UTM og `pyproj` |
| B | Sjekken av `.env` (Story 1.1, AD-12 punkt 3) ville stoppe appen på Vercel, der det ikke finnes noen `.env` | Epics linje 326, spinen linje 173, AD-15 punkt 5 |
| C | P2-merkingen i overskriftene | Vurdert og droppet, se seksjon 3 |
| D | Story 6.5 ligger i Epic 6, men skal bygges før 1.11 | Vurdert og droppet, se seksjon 3 |
| E | Ingen regel for *hvilke* endringer som foreslås når ingen tur passer. Lenker kan ikke sende det endrede søket som POST | Story 1.12, FR-8, `EXPERIENCE.md` (Tilstandspanel), `DESIGN.md` linje 596 |
| F | Datamodellen for startpunkt og turtype er uklar. ER-diagrammet har egne entiteter, AD-3 har flate felt, og Story 1.6 sier «modellene for startpunkt og tur» | Spinen linje 75–78 og 293–294, epics linje 477 og 513 |
| G | Spinen sier at det er én krediteringslinje i basismalen. UX og Story 1.10 sier at krediteringen står på kartet, nede til høyre | Spinen linje 219, `EXPERIENCE.md` linje 195, `DESIGN.md` linje 577–580 |
| H | «Data fra MET Norge» vises fra Story 1.10, men værdata kommer først i Epic 5, som er P2 og kan kuttes | Epics linje 241, 290, 675 og 1857–1869 |
| I | Spinen og AR-7 siterer navnet på raden i Mikrotekst som om det var teksten | Spinen linje 108, epics linje 108, `EXPERIENCE.md` linje 150 |
| J | Formatet på kurateringslista er ikke valgt (CSV, YAML eller TOML) | Spinen linje 357, epics linje 102 og 475. Testbrukeren er alt valgt som TOML i Story 3.4 |
| K | Feltene i søkeskjemaet står i ulik rekkefølge i FR-4 og i `DESIGN.md`, UX-DR10 og Story 1.9 | PRD linje 157–161, `DESIGN.md` linje 529 |
| L | `lastinn` er beskrevet som innlasting «i SQLite», men på Vercel er databasen Postgres | Spinen linje 90, `docs/arkitektur.md` linje 64 |
| 10 | CSP (`default-src 'self'`, ingen `style`-attributter) kan komme i konflikt med Leaflet | Spinen › Konvensjon Content-Security-Policy |

## 2. Konsekvenser

**Epics.**
- Epic 1 kan fullføres som planlagt etter rettingene. Story 1.1, 1.5, 1.6, 1.9, 1.10, 1.11 og 1.12 får presiseringer.
- Epic 5 flytter MET-krediteringen inn i Story 5.3.
- Epic 6 får én presisering i Story 6.1 (kreditering der turillustrasjonen vises uten kart) og én i Story 6.5 (henvisningen til `requirements-bygg.txt` fjernes).
- Epic 2, 3 og 4 får ingen endringer. Story 3.4 bruker allerede `data/testbruker.toml`.
- Ingen epic blir overflødig, og ingen nye trengs. Byggerekkefølgen er uendret: 1.1–1.10, så 6.5, så 1.11–1.12.

**Stories.** Ingen story er påbegynt, så ingenting må rulles tilbake. Endringene er presiseringer i akseptansekriteriene (detaljer i seksjon 4.1).

**Artefakter som må rettes.**
- PRD: FR-4, NFR-7, endringsloggen og et notat i addendumet.
- Spinen: AD-2, AD-3, AD-5, AD-12, AD-15, konvensjonen for kreditering, Stack, kildetreet, ER-diagrammet, Capability-tabellen og Deferred.
- Beslutningsloggen (`.memlog.md`): nye linjer legges til, og ingen gamle endres.
- `EXPERIENCE.md` og `DESIGN.md`.
- `docs/arkitektur.md`.
- `epic-1-context.md` må kompileres på nytt.

**Teknisk.**
- `requirements-bygg.txt` og `pyproj` forsvinner. Byggeskriptet bruker bare `requirements.txt` (HTTP-klienten) og standardbiblioteket (`xml.etree.ElementTree`, `tomllib`).
- Lengde og punktavstand må regnes i WGS84 med en avstandsfunksjon i `domene.tur`, for eksempel haversine.
- Byggeskriptet trenger WFS-fixtures med flere segmenter.
- Kartverkets høyde-API får nå WGS84-punkter i stedet for UTM. Hvilken `koordsys`-parameter API-et skal ha, må verifiseres i Story 1.5.
- Ingenting endres i infrastruktur eller publisering, bortsett fra at det er én kravfil mindre.

## 3. Anbefalt løsning

**Valg: direkte justering.** Eksisterende stories og dokumenter rettes. Ingen tilbakerulling og ingen ny MVP-vurdering.

- **Hvorfor:** Ingen kode finnes. Alle funn er uklarheter eller motstrider i teksten, og ingen av dem endrer scope eller prioritet. Løsningene er godkjent av Hannah.
- **Innsats:** omtrent 2–3 timer med mekaniske endringer etter seksjon 4, pluss ny kompilering av `epic-1-context.md` og en ny readiness gate.
- **Risiko:** lav. Det som kan gå galt:
  - Toleransen for å koble WFS-segmenter er ikke fastsatt. Den settes i Story 1.5 og står i Deferred.
  - `koordsys` i høyde-API-et må verifiseres.
  - CSP mot Leaflet (funn 10).
- **Tidsplan:** Story 1.1 starter etter at endringene er gjort og den nye readiness gate har gått gjennom. Forsinkelsen er omtrent én dag.

**Vurdert og droppet:**
- **C (P2-merking i overskriftene):** ingen endring. Parseren i sprint planning tolker overskrifter som «Story 5.1 (P2): …» riktig.
- **D (Story 6.5 i Epic 6):** ingen endring. Byggerekkefølgen (1.1–1.10, 6.5, 1.11–1.12) står allerede i epics og i `epic-1-context.md`.
- **Funn 10 (CSP mot Leaflet):** ingen planendring. Det noteres som en risiko som testes i Story 1.10, der et kriterium allerede sier at nettleseren ikke skal melde CSP-brudd, og at en eventuell utvidelse begrunnes i beslutningsloggen. Når krediteringen renderes på serveren (G), trenger den ingen Leaflet-kontroll.

## 4. Detaljerte endringsforslag

Hver endring er en eksakt erstatning: teksten under GAMMEL (finnes nøyaktig én gang i fila) byttes med teksten under NY. Der en linje settes inn, er GAMMEL en ankerlinje som gjentas først i NY. «*(slettes)*» betyr at linjen fjernes, med linjeskiftet. Linjenumrene gjelder filene slik de var 2026-11-22. Sti-forkortelser:

- **epics** = `_bmad-output/planning-artifacts/epics.md`
- **prd** = `…/prds/prd-G81-eriksen-2026-10-29/prd.md`
- **addendum** = `…/prds/prd-G81-eriksen-2026-10-29/addendum.md`
- **spine** = `…/architecture/architecture-G81-eriksen-2026-11-07/ARCHITECTURE-SPINE.md`
- **memlog** = `…/architecture/architecture-G81-eriksen-2026-11-07/.memlog.md`
- **experience** = `…/ux-designs/ux-G81-eriksen-2026-11-06/EXPERIENCE.md`
- **design** = `…/ux-designs/ux-G81-eriksen-2026-11-06/DESIGN.md`
- **arkitektur** = `docs/arkitektur.md`

### 4.1 Stories og krav i epics.md

#### EP-01 · epics › Krav, FR-4 (linje 32) · funn K
GAMMEL:
~~~text
Startpunkt (valgfritt, liste over startpunktene i turdatabasen, med fast hjelpetekst om at turene foreløpig bare dekker Oslo-området), Turtype (valgfritt, «Alle turtyper» forvalgt)
~~~
NY:
~~~text
Turtype (valgfritt, «Alle turtyper» forvalgt), Startpunkt (valgfritt, liste over startpunktene i turdatabasen, med fast hjelpetekst om at turene foreløpig bare dekker Oslo-området)
~~~
Begrunnelse: Rekkefølgen blir den samme som i `DESIGN.md` (linje 529), UX-DR10 og Story 1.9.

#### EP-02 · epics › Krav, NFR-7 (linje 84) · funn H
GAMMEL:
~~~text
«© OpenStreetMap contributors» med lenke og «Data fra MET Norge».
~~~
NY:
~~~text
«© OpenStreetMap contributors» med lenke, og «Data fra MET Norge» der værdata vises.
~~~
Begrunnelse: Endringen følger PRD-02. Værdata kan kuttes (P2).

#### EP-03 · epics › AR-1 (linje 96) · funn A og B, beslutning 3
GAMMEL:
~~~text
`requirements-bygg.txt` har i tillegg pyproj 3.8.0. Ruff 0.17.4 i `pyproject.toml`.
~~~
NY:
~~~text
Byggeskriptet trenger ingen pakker utover `requirements.txt`. `requirements-dev.txt` har `ruff==0.17.4` for utvikling og installeres ikke på Vercel. Oppsettet for Ruff står i `pyproject.toml`.
~~~
GAMMEL:
~~~text
Installasjon: `venv`, `pip install`, kopiere `.env`, `migrate`, `lastinn`, `runserver`.
~~~
NY:
~~~text
Installasjon: `venv`, `pip install`, kopiere `.env`, `migrate`, `lastinn`, `runserver`. For utvikling og Ruff trengs i tillegg `pip install -r requirements-dev.txt`.
~~~
GAMMEL:
~~~text
Mangler `.env`, stopper settings med en norsk melding.
~~~
NY:
~~~text
Mangler `.env` lokalt (`VERCEL` er ikke satt), stopper settings med en norsk melding.
~~~
Begrunnelse: WGS84 fra WFS-en gjør `pyproj` overflødig, og på Vercel finnes ingen `.env` (AD-15 punkt 5 har sin egen sjekk).

#### EP-04 · epics › AR-4 (linje 102) · funn A, F og J
GAMMEL:
~~~text
leser kurateringslista i `data/` (format avgjøres i første story for turdatabasen), henter geometri fra Turrutebasen, høyder fra Kartverkets høyde-API (maks 50 punkter per kall, punkt hvert 10–25 m, terskel 2–10 m eller glatting), gjør om UTM (EPSG:25832/25833) til WGS84 med pyproj, beregner verdier via `domene/`
~~~
NY:
~~~text
leser kurateringslista `data/kurateringsliste.toml` (TOML, med `tomllib`), sjekker at samme startpunkt-ID alltid har samme navn og koordinat, henter geometri fra Turrutebasens WFS (`app:Fotrute`, `srsName=EPSG:4326`), der segmentene for hvert rutenummer settes sammen ved endepunktene og skriptet stopper hvis de ikke henger sammen, henter høyder fra Kartverkets høyde-API (maks 50 punkter per kall, punkt hvert 10–25 m, terskel 2–10 m eller glatting), beregner verdier via `domene/`
~~~
Begrunnelse: Datakilden og formatet er avgjort (A, J), og startpunktene sjekkes (F).

#### EP-05 · epics › AR-5 (linje 104) · funn F og J
GAMMEL:
~~~text
leser `turer.geojson` og `data/testbruker.*`. Turer oppdateres eller opprettes etter `id` og slettes aldri.
~~~
NY:
~~~text
leser `turer.geojson` og `data/testbruker.toml`. Startpunkter og turer oppdateres eller opprettes etter `id` (startpunktene først) og slettes aldri.
~~~
Begrunnelse: Formatet er avgjort (Story 3.4), og `Startpunkt` er en egen modell.

#### EP-06 · epics › AR-7 (linje 108) · funn I
GAMMEL:
~~~text
Ukjent søke-ID eller tur-ID gir «Forslaget finnes ikke lenger».
~~~
NY:
~~~text
Ukjent søke-ID eller tur-ID gir Søk med meldingen fra Mikrotekst › Forslaget finnes ikke lenger («Turforslaget er ikke lenger tilgjengelig. Søk på nytt for å få et forslag.»).
~~~
Begrunnelse: «Forslaget finnes ikke lenger» er navnet på raden i Mikrotekst, ikke teksten brukeren ser.

#### EP-07 · epics › AR-16 (linje 126) · funn G og H
GAMMEL:
~~~text
Én felles krediteringslinje i basismalen, og Leaflets egen attribution-prefiks er slått av.
~~~
NY:
~~~text
Krediteringen for kart og rute står på kartet og renderes på serveren, og Leaflets attribution-kontroll er slått av. «Data fra MET Norge» står i Bekledningstips. Basismalen har ingen krediteringslinje.
~~~
Begrunnelse: Endringen følger SP-09.

#### EP-08 · epics › UX-DR2 (linje 148) · funn G
GAMMEL:
~~~text
sidetittel « – Your Next Adventure», felles kreditering.
~~~
NY:
~~~text
sidetittel « – Your Next Adventure».
~~~
Begrunnelse: Basismalen skal ikke ha noen krediteringslinje (SP-09).

#### EP-09 · epics › UX-DR14 (linje 172) · funn G og H
GAMMEL:
~~~text
med understrekede lenker til Kartverket, openstreetmap.org/copyright (`lang="en"`) og MET Norge.
~~~
NY:
~~~text
med understrekede lenker til Kartverket og openstreetmap.org/copyright (`lang="en"`). Den renderes på serveren, så den vises også uten JavaScript og når flisene feiler. «Data fra MET Norge» står i Bekledningstips (story 5.3).
~~~
Begrunnelse: Endringen følger SP-09 og UXE-04.

#### EP-10 · epics › UX-DR22 (linje 188) · funn E
GAMMEL:
~~~text
«Prøv 3 timer» og «Prøv marka» kjører søket på nytt med én endring.
~~~
NY:
~~~text
«Prøv 3 timer» og «Prøv marka» er knapper i et lite POST-skjema med CSRF som sender det endrede søket, og hvilke forslag som vises, avgjør `foresla_endringer` (story 1.12). «Start fra første forslag igjen» er også en knapp (POST).
~~~
Begrunnelse: Et gyldig søk er en POST (AD-5 punkt 1), og alle POST følger Post/Redirect/Get (AR-16).

#### EP-11 · epics › FR- og NFR-dekning (linje 241) · funn H
GAMMEL:
~~~text
NFR-7 i Epic 1: all kreditering, også «Data fra MET Norge», finnes fra story 1.10, og Epic 5 legger ikke til ny kreditering.
~~~
NY:
~~~text
NFR-7 i Epic 1 (kart og rute, story 1.10) og Epic 5 («Data fra MET Norge», story 5.3).
~~~
Begrunnelse: MET-krediteringen følger med værdataene.

#### EP-12 · epics › Epic 5, NFR (linje 290) · funn H
GAMMEL:
~~~text
**NFR:** ingen nye. MET-krediteringen (NFR-7) finnes fra story 1.10, og Epic 5 legger ikke til ny kreditering
~~~
NY:
~~~text
**NFR:** NFR-7: «Data fra MET Norge» vises i Bekledningstips når det vises tips fra værvarselet (story 5.3)
~~~
Begrunnelse: Endringen følger EP-11.

#### EP-13 · epics › Story 1.1 (linje 326–328) · funn B
GAMMEL:
~~~text
**Gitt** at `.env` mangler, eller at `DJANGO_SECRET_KEY` er tom
~~~
NY:
~~~text
**Gitt** at `VERCEL` ikke er satt, og at `.env` mangler eller `DJANGO_SECRET_KEY` er tom
~~~
GAMMEL:
~~~text
**Så** stopper den med en norsk melding om å kopiere `.env.example` til `.env` (AD-12 punkt 3)
~~~
NY:
~~~text
**Så** stopper den med en norsk melding om å kopiere `.env.example` til `.env` (AD-12 punkt 3)
**Og** når `VERCEL` er satt, kreves ingen `.env`, og bare sjekken i story 1.2 gjelder (AD-15 punkt 5)
~~~
Begrunnelse: Vercel har ingen `.env`, verken under byggingen eller når appen kjører.

#### EP-14 · epics › Story 1.1 (linje 333) · funn A
GAMMEL:
~~~text
**Og** `requirements.txt` har låste versjoner fra spinen › Stack, og `requirements-bygg.txt` har i tillegg `pyproj` 3.8.0
~~~
NY:
~~~text
**Og** `requirements.txt` har låste versjoner fra spinen › Stack, og `requirements-dev.txt` har `ruff==0.17.4` for utvikling
~~~
Begrunnelse: `pyproj` trengs ikke lenger, og Ruff får sin egen kravfil (beslutning 3).

#### EP-31 · epics › Story 1.1, tester og kodestil (linje 345) · beslutning 3
GAMMEL:
~~~text
**Når** jeg kjører `python manage.py test`, `ruff check .` og `ruff format --check .`
~~~
NY:
~~~text
**Når** jeg har kjørt `pip install -r requirements-dev.txt` og kjører `python manage.py test`, `ruff check .` og `ruff format --check .`
~~~
Begrunnelse: Ruff står ikke i `requirements.txt`, så README må ha dette steget.

#### EP-32 · epics › Story 6.8, ny klone (linje 2240) · beslutning 3
GAMMEL:
~~~text
**Og** `python manage.py test`, `ruff check .` og `ruff format --check .` består i det samme miljøet (AR-15)
~~~
NY:
~~~text
**Og** etter `pip install -r requirements-dev.txt` fra README består `python manage.py test`, `ruff check .` og `ruff format --check .` i det samme miljøet (AR-15)
~~~
Begrunnelse: Den nye klonen må installere Ruff etter README for at kontrollen skal kunne bestå.

#### EP-15 · epics › Story 1.5 (linje 475 og 477) · funn A, F og J
GAMMEL:
~~~text
**Gitt** at formatet på kurateringslista er valgt (CSV, YAML eller TOML)
~~~
NY:
~~~text
**Gitt** kurateringslista `data/kurateringsliste.toml`, lest med `tomllib` fra standardbiblioteket
~~~
GAMMEL:
~~~text
**Så** har lista per tur `id`, navn, startpunkt (id, navn og koordinat), form, turtyper, kilde og kilde-ID og eventuell ut.no-URL, og formatet
~~~
NY:
~~~text
**Så** har lista per tur `id`, navn, startpunkt (id, navn og koordinat i WGS84), form, turtyper, kilde og kilde-ID og eventuell ut.no-URL. For Turrutebasen er kilde-ID en liste med ett eller flere rutenummer (`app:rutenummer`, for eksempel `F_01812_03`) i rekkefølge langs turen, og formatet
~~~
Begrunnelse: Formatet er TOML, som testbrukeren (Story 3.4), uten ny avhengighet. Kilde-ID må kunne vise til flere rutenummer.

#### EP-16 · epics › Story 1.5 (linje 489–491) · funn A
GAMMEL:
~~~text
**Gitt** geometri i UTM (EPSG:25832 eller 25833)
**Når** skriptet gjør den om
**Så** blir den WGS84 med `pyproj`, og `pyproj` står bare i `requirements-bygg.txt`
~~~
NY:
~~~text
**Gitt** en tur fra Turrutebasen
**Når** skriptet henter geometrien
**Så** henter det segmentene (features) for hvert rutenummer i kilde-ID-en fra WFS-en `https://wfs.geonorge.no/skwms1/wfs.turogfriluftsruter` med `service=WFS`, `version=2.0.0`, `request=GetFeature`, `typeNames=app:Fotrute` og `srsName=EPSG:4326`, filtrert på `app:rutenummer`. Det leser `gml:posList` (GML 3.2.1, rekkefølgen lon lat) med `xml.etree.ElementTree` og bruker HTTP-klienten fra `requirements.txt`
**Og** det setter segmentene sammen til én `LineString` ved å koble endepunkter (og snur et segment ved behov), i rekkefølgen i kilde-ID-en. Henger de ikke sammen innenfor toleransen i README-en i `data/`, stopper skriptet med en melding om hvilken tur og hvilket rutenummer det gjelder, og den gamle `turer.geojson` blir ikke overskrevet
**Og** koordinatene er allerede i WGS84, så skriptet regner ikke om og bruker ikke `pyproj`. Lengde og punktavstand regnes med en avstandsfunksjon for WGS84 (for eksempel haversine) i `domene.tur`
~~~
Begrunnelse: Datakilden er testet 2026-11-22. En rute består av flere segmenter med samme rutenummer.

#### EP-17 · epics › Story 1.5, nytt kriterium (etter linje 499) · funn F
GAMMEL:
~~~text
**Så** stopper det med en melding som sier hvilken tur det gjelder, og den gamle `turer.geojson` overskrives ikke
~~~
NY:
~~~text
**Så** stopper det med en melding som sier hvilken tur det gjelder, og den gamle `turer.geojson` overskrives ikke

**Gitt** to turer i kurateringslista med samme startpunkt-ID
**Når** skriptet leser lista
**Så** stopper det med en melding som nevner startpunkt-ID-en, hvis navnet eller koordinaten er ulik (AD-3 punkt 2)
~~~
Begrunnelse: Startpunktet står gjentatt per tur i lista, men skal bli én rad i `Startpunkt`.

#### EP-18 · epics › Story 1.5, tester (linje 503) · funn A
GAMMEL:
~~~text
**Så** bruker de lagrede svar i `tests/fixtures/` uten nettverkskall, og beregningene går gjennom `domene/` (AR-2, AR-15)
~~~
NY:
~~~text
**Så** bruker de lagrede svar i `tests/fixtures/` uten nettverkskall, også et WFS-svar der en rute har flere segmenter og et der segmentene ikke henger sammen, og beregningene går gjennom `domene/` (AR-2, AR-15)
~~~
Begrunnelse: Sammensettingen er den nye risikoen i byggeskriptet.

#### EP-19 · epics › Story 1.6 (linje 513, 515 og 520) · funn F
GAMMEL:
~~~text
**Gitt** modellene for startpunkt og tur
~~~
NY:
~~~text
**Gitt** modellene `Startpunkt` (`id` som stabil streng og primærnøkkel, `navn`, `lat`, `lon`, `hoyde_m`) og `Tur` i `turforslag/`, der `Tur.startpunkt` er en `ForeignKey` med `on_delete=PROTECT` og `Tur.turtyper` er et `JSONField` med en liste av `marka`, `utsikt` og `topptur` (AD-3 punkt 5)
~~~
GAMMEL:
~~~text
**Så** lagres geometri og høydeprofil i `JSONField`, uten GeoDjango eller SpatiaLite
~~~
NY:
~~~text
**Så** lagres geometri, høydeprofil og turtyper i `JSONField`, uten GeoDjango eller SpatiaLite
~~~
GAMMEL:
~~~text
**Og** en tur som mangler i fila, slettes ikke
~~~
NY:
~~~text
**Og** en tur som mangler i fila, slettes ikke
**Og** startpunktene opprettes eller oppdateres etter `id` før turene, ut fra de flate startpunktfeltene i `domene.tur.Tur`, og et startpunkt slettes ikke
~~~
Begrunnelse: Modellen er avgjort av Hannah. Dataklassen i `domene/` beholder de flate feltene.

#### EP-20 · epics › Story 1.9 (linje 612) · funn F
GAMMEL:
~~~text
og Startpunkt («Alle startpunkt» og hjelpeteksten om Oslo-området)
~~~
NY:
~~~text
og Startpunkt («Alle startpunkt» og startpunktene fra modellen `Startpunkt`, med hjelpeteksten om Oslo-området)
~~~
Begrunnelse: Nedtrekkslista får verdiene sine fra den nye modellen.

#### EP-21 · epics › Story 1.10, kartet (linje 675) · funn G og H
GAMMEL:
~~~text
Krediteringen er alltid synlig, med understrekede lenker til Kartverket, OpenStreetMap (`lang="en"`) og MET Norge, uten Leaflets egen prefiks
~~~
NY:
~~~text
Krediteringen er alltid synlig, med understrekede lenker til Kartverket og OpenStreetMap (`lang="en"`). Den renderes på serveren i malen, og Leaflets attribution-kontroll er slått av (`attributionControl: false`)
~~~
Begrunnelse: Krediteringen skal vises også uten JavaScript, og værdata finnes ikke i Epic 1.

#### EP-22 · epics › Story 1.10, kartet feiler (linje 693) · funn G
GAMMEL:
~~~text
og resten av forslaget vises som vanlig (AD-1)
~~~
NY:
~~~text
krediteringen står fortsatt nede til høyre, og resten av forslaget vises som vanlig (AD-1)
~~~
Begrunnelse: «Alltid synlig» (`EXPERIENCE.md` linje 195) skal gjelde også når kartet feiler.

#### EP-23 · epics › Story 1.11, alle vist (linje 713) · funn E
GAMMEL:
~~~text
antallet turer, endringsforslag, «Start fra første forslag igjen» og «Endre søk» (FR-7, UX-DR22)
~~~
NY:
~~~text
antallet turer, «Start fra første forslag igjen» og «Endre søk» (FR-7, UX-DR22)
**Og** endringsforslagene fra `foresla_endringer` legges til i story 1.12. Der må en endring gi minst én tur som ikke var blant treffene i søket
~~~
Begrunnelse: Funksjonen lages i Story 1.12, som bygges etter 1.11. Det samme mønsteret brukes alt for «Lag konto», som legges til i Epic 2.

#### EP-24 · epics › Story 1.12, ingen treff (linje 756) · funn E
GAMMEL:
~~~text
**Og** et forslag vises bare når endringen gir minst ett treff. Det avgjøres av en ren funksjon i `domene/`
~~~
NY:
~~~text
**Og** forslagene lages av `domene.utvalg.foresla_endringer(sok, turer, nivatak, tidligere_treff=())`. Den gir høyst tre forslag i fast rekkefølge, med de andre valgene uendret, og tar bare med et forslag når `velg_turer` gir status `TREFF` for det endrede søket: (1) Varighet: den korteste varigheten i lista (halvtimessteg) som er lengre enn søket og gir treff, for eksempel «Prøv 3 timer» eller «Prøv 2,5 timer». Ved 8 t blir det ikke noe forslag. (2) Startpunkt: bare når et startpunkt er valgt, og minst ett annet startpunkt eller «Alle startpunkt» gir treff: «Velg startpunkt». (3) Turtype: bare når en turtype er valgt. Første turtype i rekkefølgen marka, utsikt, topptur som ikke er valgt og gir treff («Prøv marka»), ellers «Prøv alle turtyper» hvis det gir treff
**Og** ved «alle vist» (story 1.11) får funksjonen treffene i søket som `tidligere_treff`, og et forslag tas bare med når det gir minst én tur som ikke er blant dem
**Og** gir ingen endring treff, viser panelet bare «Endre søk» (og «Start fra første forslag igjen» ved «alle vist»)
**Og** varigheten formateres i `domene/` (hele timer som «3 timer», halvtimer som «2,5 timer»). «Prøv 2,5 timer» og «Prøv alle turtyper» er [ASSUMPTION] i Mikrotekst
~~~
Begrunnelse: FR-8 og mocken forutsetter konkrete verdier, og regelen må være deterministisk og testbar i `domene/` (AD-2).

#### EP-25 · epics › Story 1.12, trykk på forslag (linje 760) · funn E
GAMMEL:
~~~text
**Så** kjøres søket på nytt med én endring og en ny søke-ID
~~~
NY:
~~~text
**Så** sender knappen det endrede søket i et lite POST-skjema med CSRF, søket kjøres på nytt med én endring og en ny søke-ID, og svaret følger Post/Redirect/Get (AR-7, AR-16)
**Og** forslagene er knapper (`<button type="submit">`), ikke lenker, og de virker likt uten JavaScript
~~~
Begrunnelse: En lenke (GET) kan ikke lage et gyldig søk (AD-5 punkt 1).

#### EP-26 · epics › Story 1.12, tester (linje 774) · funn E
GAMMEL:
~~~text
**Så** dekker de hver status og endringsforslagene (SM-2)
~~~
NY:
~~~text
**Så** dekker de hver status og endringsforslagene, også halvtimer, 8 t, «alle vist» med `tidligere_treff` og tilfellet uten forslag (SM-2)
~~~
Begrunnelse: Regelen i EP-24 har kanttilfeller.

#### EP-27 · epics › Story 5.3, kreditering (linje 1857, 1859 og 1860) · funn H
GAMMEL:
~~~text
**Gitt** et turforslag med bekledningstips eller med en melding uten værvarsel
~~~
NY:
~~~text
**Gitt** et turforslag med bekledningstips fra værvarselet
~~~
GAMMEL:
~~~text
**Så** finnes bare den felles krediteringslinjen fra story 1.10, med «Data fra MET Norge» som lenke til MET Norge, og storyen legger ikke til en ny kreditering (NFR-7, AR-16)
~~~
NY:
~~~text
**Så** står «Data fra MET Norge» som lenke til MET Norge rett etter grunnlagslinjen i Bekledningstips (NFR-7, AR-16)
~~~
GAMMEL:
~~~text
**Og** en test sjekker at «Data fra MET Norge» står nøyaktig én gang på siden, også i turforslag fra historikken
~~~
NY:
~~~text
**Og** uten tips (melding uten værvarsel, `PASSERT` eller Tilstandspanel) står ikke «Data fra MET Norge» på siden. En test sjekker at teksten står nøyaktig én gang når tips vises, også i turforslag fra historikken, og ikke i det hele tatt uten tips
~~~
Begrunnelse: Krediteringen vises bare der MET-data faktisk vises.

#### EP-28 · epics › Story 5.3, kutt (linje 1869) · funn H
GAMMEL:
~~~text
**Og** krediteringen fra story 1.10 står uendret, og testene for de leverte storyene i Epic 1–4 består uendret
~~~
NY:
~~~text
**Og** krediteringen på kartet fra story 1.10 står uendret, «Data fra MET Norge» står ikke på siden, og testene for de leverte storyene i Epic 1–4 består uendret
~~~
Begrunnelse: Kuttes Epic 5, skal siden ikke kreditere data den ikke bruker.

#### EP-29 · epics › Story 6.1, turillustrasjon uten kart (etter linje 1937) · nytt funn 3
GAMMEL:
~~~text
**Så** har den den lille varianten, uten bildetekst og med `aria-hidden="true"`, fordi navn, nivå, form, lengde og estimert tid står som tekst i kortet (UX-DR28)
~~~
NY:
~~~text
**Så** har den den lille varianten, uten bildetekst og med `aria-hidden="true"`, fordi navn, nivå, form, lengde og estimert tid står som tekst i kortet (UX-DR28)
**Og** når illustrasjonen vises uten kartet på samme side (Turoppsummering og pyntvarianten på Søk), står en krediteringslinje i `caption` etter turens `kilde`: «Rute: © Kartverket» eller «Rute: © OpenStreetMap contributors» med lenke. Teksten er [ASSUMPTION] i Mikrotekst (NFR-7)
~~~
Begrunnelse: Forutsetningen om at Turoppsummering står på samme side som kartet, stemmer ikke. Den vises på Registrer gjennomført tur og på Logg inn / Lag konto (`EXPERIENCE.md` linje 210), og pyntvarianten på Søk tegner en ekte tur (epics linje 1932). Illustrasjonen er laget av rutedata, så den må krediteres der den står. Dette gjelder bare P2 (Story 6.1).

#### EP-30 · epics › Story 6.5 (linje 2117) · funn A
GAMMEL:
~~~text
**Og** målingen krever ingen ny pakke i `requirements.txt` eller `requirements-bygg.txt`
~~~
NY:
~~~text
**Og** målingen krever ingen ny pakke i `requirements.txt` eller `requirements-dev.txt`
~~~
Begrunnelse: `requirements-dev.txt` erstatter `requirements-bygg.txt` (SP-06).

### 4.2 PRD

#### PRD-01 · prd › FR-4, tabell (linje 159–161) · funn K
GAMMEL:
~~~text
| Startpunkt | nei | Velges fra en liste som bare viser startpunkter i turdatabasen. Under lista står en fast hjelpetekst om at turene foreløpig bare dekker Oslo-området |
| Turtype | nei | Én av turtypene eller «Alle turtyper». «Alle turtyper» er forvalgt |
| Fritekstønske | nei | Maks 200 tegn. P2: feltet finnes bare med FR-11 |
~~~
NY:
~~~text
| Turtype | nei | Én av turtypene eller «Alle turtyper». «Alle turtyper» er forvalgt |
| Startpunkt | nei | Velges fra en liste som bare viser startpunkter i turdatabasen. Under lista står en fast hjelpetekst om at turene foreløpig bare dekker Oslo-området |
| Fritekstønske | nei | Maks 200 tegn. P2: feltet finnes bare med FR-11 |

Rekkefølgen og oppsettet i skjemaet står i `DESIGN.md` › Layout & Spacing.
~~~
Begrunnelse: FR-4 skal ikke motsi rekkefølgen i UX.

#### PRD-02 · prd › NFR-7 (linje 386) · funn H
GAMMEL:
~~~text
«© OpenStreetMap contributors» med lenke og «Data fra MET Norge» (MET anbefaler «Data from MET Norway»).
~~~
NY:
~~~text
«© OpenStreetMap contributors» med lenke, og «Data fra MET Norge» der værdata vises (MET anbefaler «Data from MET Norway»).
~~~
Begrunnelse: Værdata er P2 og kan kuttes.

#### PRD-03 · prd › Endringslogg (etter linje 573) og frontmatter (linje 5)
GAMMEL:
~~~text
Presisering uten ny regel, godkjent av produkteier 2026-11-15 |
~~~
NY:
~~~text
Presisering uten ny regel, godkjent av produkteier 2026-11-15 |
| 1.13 | 2026-11-22 | Correct course etter readiness gate (`sprint-change-proposal-2026-11-22.md`): FR-4 viser feltene i skjemarekkefølgen fra `DESIGN.md`, og NFR-7 sier at «Data fra MET Norge» vises der værdata vises. Presiseringer uten ny regel, godkjent av produkteier 2026-11-22 |
~~~
GAMMEL:
~~~text
updated: 2026-11-15
~~~
NY:
~~~text
updated: 2026-11-22
~~~
Begrunnelse: PRD-en fører alle endringer i endringsloggen.

#### ADD-01 · addendum › Til arkitekturen, Koordinater (linje 80) · funn A
GAMMEL:
~~~text
Konverteringen avgjøres i arkitekturen.
~~~
NY:
~~~text
Konverteringen avgjøres i arkitekturen. **Merk (2026-11-22):** WFS-en `wfs.turogfriluftsruter` gir `app:Fotrute` som GML 3.2.1 i EPSG:4326 (testet 2026-11-22), så ingen omregning trengs (spinen AD-3 punkt 2).
~~~
Begrunnelse: Funnet fra researchen står historisk riktig, men gjelder ikke WFS-en. Det får derfor et notat i stedet for å skrives om.

### 4.3 Arkitektur

#### SP-01 · spine › AD-2 (linje 60) · funn E
GAMMEL:
~~~text
Hver regel har enhetstester som viser til FR-ID-en.
~~~
NY:
~~~text
Endringsforslagene ved ingen treff og «alle vist» lages av én funksjon, `foresla_endringer`, som bruker `velg_turer` (FR-7, FR-8). Hver regel har enhetstester som viser til FR-ID-en.
~~~
Begrunnelse: Regelen hører hjemme i `domene/` som én funksjon (EP-24).

#### SP-02 · spine › AD-3 punkt 2 (linje 88) · funn A, F og J
GAMMEL:
~~~text
  2. **Bygging:** Kurateringslista i `data/` gir id, navn, startpunkt, form, turtyper, kilde-ID og ut.no-URL. Turnavnet hentes aldri fra kilden. `skript/bygg_turdatabase.py` (kjøres med `python -m skript.bygg_turdatabase`) henter geometri, henter høyder (Kartverket, maks 50 punkter per kall, punkt hvert 10–25 m, støyfiltrering), gjør om UTM (EPSG:25832/25833) til WGS84 med `pyproj`, beregner verdiene via `domene/` og skriver `data/turer.geojson`, som committes.
~~~
NY:
~~~text
  2. **Bygging:** Kurateringslista `data/kurateringsliste.toml` (TOML, lest med `tomllib`) gir id, navn, startpunkt (id, navn, koordinat), form, turtyper, kilde-ID og ut.no-URL. For Turrutebasen er kilde-ID en liste med ett eller flere rutenummer (`app:rutenummer`) i rekkefølge. Turnavnet hentes aldri fra kilden. `skript/bygg_turdatabase.py` (kjøres med `python -m skript.bygg_turdatabase`) sjekker at samme startpunkt-ID alltid har samme navn og koordinat. Det henter segmentene for hvert rutenummer fra Turrutebasens WFS (`https://wfs.geonorge.no/skwms1/wfs.turogfriluftsruter`, `typeNames=app:Fotrute`, `srsName=EPSG:4326`, GML 3.2.1 med `gml:posList` i rekkefølgen lon lat) og setter dem sammen til én linje ved å koble endepunkter. Henger de ikke sammen, stopper skriptet med en melding. Deretter henter det høyder (Kartverket, maks 50 punkter per kall, punkt hvert 10–25 m, støyfiltrering), beregner verdiene via `domene/` og skriver `data/turer.geojson`, som committes. Koordinatene er allerede i WGS84, så ingen omregning trengs. Skriptet bruker bare pakkene i `requirements.txt` og standardbiblioteket (`xml.etree.ElementTree`, `tomllib`).
~~~
Begrunnelse: Kilde, format og sjekk av startpunktene er avgjort av Hannah 2026-11-22.

#### SP-03 · spine › AD-3 punkt 4 (linje 90) · funn F, J og L
GAMMEL:
~~~text
`python manage.py lastinn` leser `turer.geojson` og `data/testbruker.*` inn i SQLite. Turer oppdateres eller opprettes etter `id`, aldri slettet og gjenopprettet.
~~~
NY:
~~~text
`python manage.py lastinn` leser `turer.geojson` og `data/testbruker.toml` inn i databasen (SQLite lokalt, Postgres på Vercel, AD-4). Startpunkter og turer oppdateres eller opprettes etter `id`, startpunktene først, og de blir aldri slettet og gjenopprettet.
~~~
Begrunnelse: AD-15 punkt 4 kjører `lastinn` mot Neon, og `Startpunkt` er en egen modell.

#### SP-04 · spine › AD-3 punkt 5 (linje 91) · funn F
GAMMEL:
~~~text
  5. Geometri og høydeprofil lagres i `JSONField`. Ingen GeoDjango eller SpatiaLite.
~~~
NY:
~~~text
  5. **Modeller:** `turforslag.Startpunkt` har `id` (stabil streng, primærnøkkel), `navn`, `lat`, `lon` og `hoyde_m`. `turforslag.Tur` har `startpunkt` som `ForeignKey` til `Startpunkt` med `on_delete=PROTECT`, og `turtyper` som `JSONField` med en liste av `marka`, `utsikt`, `topptur`. Turtype filtreres i `domene/`, ikke med JSON-oppslag i databasen (AD-4). `domene.tur.Tur` beholder de flate startpunktfeltene, og `lastinn` og omgjøringen i `turforslag/` mapper mellom dataklassen og modellene. Geometri og høydeprofil lagres i `JSONField`. Ingen GeoDjango eller SpatiaLite.
~~~
Begrunnelse: Én datamodell i stedet for tre ulike beskrivelser. JSON-oppslag virker ulikt på SQLite og Postgres.

#### SP-05 · spine › AD-5 punkt 4 (linje 108) · funn I
GAMMEL:
~~~text
En ukjent søke-ID, eller en tur-ID som ikke lenger finnes, gir «Forslaget finnes ikke lenger».
~~~
NY:
~~~text
En ukjent søke-ID, eller en tur-ID som ikke lenger finnes, gir Søk med meldingen fra Mikrotekst › Forslaget finnes ikke lenger («Turforslaget er ikke lenger tilgjengelig. Søk på nytt for å få et forslag.»).
~~~
Begrunnelse: All brukertekst kommer fra Mikrotekst (konvensjonen for tekst).

#### SP-06 · spine › AD-12 punkt 2 (linje 172) · funn A
GAMMEL:
~~~text
`requirements.txt` har låste versjoner og bare det appen trenger; `requirements-bygg.txt` har i tillegg `pyproj`.
~~~
NY:
~~~text
`requirements.txt` har låste versjoner og bare det appen og byggeskriptet trenger. `requirements-dev.txt` har i tillegg `ruff==0.17.4` for utvikling, og den installeres ikke på Vercel.
~~~
Begrunnelse: Uten `pyproj` blir den gamle kravfila tom, og Ruff trenger en egen kravfil (beslutning 3).

#### SP-07 · spine › AD-12 punkt 3 (linje 173) · funn B
GAMMEL:
~~~text
Mangler `.env` eller `DJANGO_SECRET_KEY`, stopper `config/settings.py` med en norsk melding om å kopiere `.env.example` til `.env`, ikke med Djangos engelske feil.
~~~
NY:
~~~text
Når `VERCEL` ikke er satt, og `.env` eller `DJANGO_SECRET_KEY` mangler, stopper `config/settings.py` med en norsk melding om å kopiere `.env.example` til `.env`, ikke med Djangos engelske feil. På Vercel leses ingen `.env`, og bare sjekken i AD-15 punkt 5 gjelder.
~~~
Begrunnelse: Vercel har ingen `.env`.

#### SP-08 · spine › AD-15 punkt 1 (linje 196) · funn A
GAMMEL:
~~~text
`pyproj` og Ruff installeres ikke på Vercel.
~~~
NY:
~~~text
`requirements-dev.txt` (Ruff) installeres ikke på Vercel.
~~~
Begrunnelse: `pyproj` finnes ikke lenger, og Ruff ligger i `requirements-dev.txt`.

#### SP-09 · spine › Konvensjon Kreditering (linje 219) · funn G og H
GAMMEL:
~~~text
| Kreditering | Én felles krediteringslinje i basismalen med «© Kartverket», «© OpenStreetMap contributors» og «Data fra MET Norge», med lenker. Leaflets egen attribution-prefiks er slått av |
~~~
NY:
~~~text
| Kreditering | Krediteringen for kart og rute («© Kartverket · © OpenStreetMap contributors», med lenker) renderes på serveren som et eget element i kartflatens nedre høyre hjørne, så den vises også uten JavaScript og når flisene feiler. Leaflets attribution-kontroll er slått av (`attributionControl: false`). «Data fra MET Norge» står i Bekledningstips og bare når det vises tips fra værvarselet. Der Turillustrasjon vises uten kart, står en krediteringslinje etter turens `kilde` (story 6.1). Basismalen har ingen krediteringslinje |
~~~
Begrunnelse: UX plasserer krediteringen på kartet. Leaflets kontroll forsvinner uten JavaScript, og værdata kan kuttes.

#### SP-10 · spine › Stack (linje 238) · funn A
GAMMEL:
~~~text
| pyproj (bare byggeskript) | 3.8.0 |
~~~
NY:
~~~text
| Turrutebasen (Geonorge WFS `wfs.turogfriluftsruter`, `app:Fotrute`, bare byggeskript) | WFS 2.0.0, GML 3.2.1 |
~~~
Begrunnelse: `pyproj` faller bort, og den nye eksterne kilden føres opp med versjon, slik de andre er.

#### SP-11 · spine › Kildetre (linje 252) · funn A
GAMMEL:
~~~text
  requirements-bygg.txt     # i tillegg for byggeskriptet (pyproj)
~~~
NY:
~~~text
  requirements-dev.txt      # i tillegg for utvikling (ruff), ikke på Vercel
~~~
Begrunnelse: `requirements-dev.txt` erstatter `requirements-bygg.txt` (beslutning 3).

#### SP-12 · spine › Kildetre, `data/` (linje 265) · funn J
GAMMEL:
~~~text
# kurateringsliste, osm-uttrekk.geojson, turer.geojson, testbruker
~~~
NY:
~~~text
# kurateringsliste.toml, osm-uttrekk.geojson, turer.geojson, testbruker.toml
~~~
Begrunnelse: Filnavnene er nå avgjort.

#### SP-13 · spine › Kjerneentiteter (linje 293–294 og 300) · funn F
GAMMEL:
~~~text
    STARTPUNKT ||--o{ TUR : "har"
    TUR }o--o{ TURTYPE : "har"
~~~
NY:
~~~text
    STARTPUNKT ||--o{ TUR : "har (PROTECT)"
~~~
GAMMEL:
~~~text
    SESSION
```
~~~
NY:
~~~text
    SESSION
```

Turtypene er en liste i `Tur.turtyper` (`JSONField`), ikke en egen entitet (AD-3 punkt 5).
~~~
Begrunnelse: Diagrammet skal vise modellene slik de faktisk blir.

#### SP-14 · spine › Capability-tabellen, NFR-7 (linje 351) · funn G og H
GAMMEL:
~~~text
| NFR-7 Kreditering | basismal, `data/` | AD-3, konvensjon Kreditering |
~~~
NY:
~~~text
| NFR-7 Kreditering | turforslagsmalen (kartet), Bekledningstips, Turillustrasjon uten kart, `data/` | AD-3, konvensjon Kreditering |
~~~
Begrunnelse: Endringen følger SP-09.

#### SP-15 · spine › Deferred (linje 357) · funn A og J
GAMMEL:
~~~text
| Format på kurateringslista og testbrukerfila (CSV, YAML eller TOML) | Bare byggeskriptet og `lastinn` leser dem; avgjøres i første story for turdatabasen |
~~~
NY:
~~~text
| Toleranse for å koble Turrutebasen-segmenter ved endepunktene | Settes i story 1.5 når de første rutene settes sammen, og står i README-en i `data/` |
~~~
Begrunnelse: Formatet er avgjort (TOML). Toleransen er det nye åpne tallet.

#### SP-16 · spine › frontmatter (linje 9)
GAMMEL:
~~~text
updated: '2026-11-15'
~~~
NY:
~~~text
updated: '2026-11-22'
~~~
Begrunnelse: Spinen er endret.

#### SP-17 · spine › AD-12 punkt 1 (linje 171) · beslutning 3
GAMMEL:
~~~text
`python manage.py lastinn`, `python manage.py runserver`.
~~~
NY:
~~~text
`python manage.py lastinn`, `python manage.py runserver`. For utvikling og for å kjøre `ruff check .` og `ruff format --check .` trengs i tillegg `pip install -r requirements-dev.txt`.
~~~
Begrunnelse: Installasjonen i README skal si hvor Ruff kommer fra.

#### SP-18 · spine › Stack, Ruff (linje 239) · beslutning 3
GAMMEL:
~~~text
| Ruff (utvikling) | 0.17.4 |
~~~
NY:
~~~text
| Ruff (utvikling, `requirements-dev.txt`) | 0.17.4 |
~~~
Begrunnelse: Stack skal vise hvor den låste versjonen står.

#### ML-01 · memlog › nye linjer etter siste linje (linje 54) · funn A, B, F, G, H og J
Legg til nederst i fila (ingen eksisterende linjer endres):
~~~text
- (decision) 2026-11-22, correct course etter readiness gate (`sprint-change-proposal-2026-11-22.md`), valgt av Hannah: Turrutebasen hentes via WFS wfs.geonorge.no/skwms1/wfs.turogfriluftsruter (app:Fotrute, srsName=EPSG:4326, GML 3.2.1 med posList lon lat, testet 2026-11-22). Segmenter med samme rutenummer settes sammen ved endepunktene, og kilde-ID er en liste av rutenummer. Erstatter beslutningen om UTM til WGS84 med pyproj. pyproj og requirements-bygg.txt fjernes. Ny requirements-dev.txt med ruff==0.17.4 for utvikling, ikke installert på Vercel. README og AD-12 punkt 1 har steget pip install -r requirements-dev.txt.
- (decision) 2026-11-22, samme kilde: egen modell turforslag.Startpunkt (id streng, navn, lat, lon, hoyde_m), Tur.startpunkt ForeignKey med PROTECT, Tur.turtyper JSONField-liste. TURTYPE er ikke en egen entitet. domene.tur.Tur beholder flate felt. Kurateringslista er data/kurateringsliste.toml og testbrukeren data/testbruker.toml (tomllib).
- (decision) 2026-11-22, samme kilde: krediteringen for kart og rute renderes på serveren på kartet, uten Leaflets attribution-kontroll og uten linje i basismalen. «Data fra MET Norge» står i Bekledningstips, bare når det vises tips. .env-sjekken gjelder bare når VERCEL ikke er satt. Endringsforslag er POST-knapper fra domene-funksjonen foresla_endringer.
~~~
Begrunnelse: Beslutningsloggen føres bare med nye linjer. Linje 36 blir stående som historikk.

#### DOC-01 · arkitektur › flytdiagram for turdatabasen (linje 64) · funn L
GAMMEL:
~~~text
    fil -->|"python manage.py lastinn"| db[("SQLite")]
~~~
NY:
~~~text
    fil -->|"python manage.py lastinn"| db[("Databasen (SQLite lokalt / Postgres på Vercel)")]
~~~
Begrunnelse: Endringen følger SP-03.

#### DOC-02 · arkitektur › Turdatabasen punkt 1 og 2 (linje 67–68) · funn A og J
GAMMEL:
~~~text
1. **Kurateringslista** er en fil der
~~~
NY:
~~~text
1. **Kurateringslista** (`data/kurateringsliste.toml`) er en fil der
~~~
GAMMEL:
~~~text
henter rutelinjen og høydene, gjør om UTM-koordinatene i kartdataene til vanlige GPS-koordinater, og beregner
~~~
NY:
~~~text
henter rutelinjen fra Turrutebasen (via WFS, allerede i vanlige GPS-koordinater) og høydene, setter sammen delene av hver rute, og beregner
~~~
Begrunnelse: Endringen følger SP-02.

#### DOC-03 · arkitektur › Teknologi (linje 165) og Mappestruktur (linje 177) · funn A
GAMMEL:
~~~text
| pyproj (bare byggeskriptet) | 3.8.0 |
~~~
NY:
~~~text
*(slettes)*
~~~
GAMMEL:
~~~text
  manage.py, requirements.txt, requirements-bygg.txt, pyproject.toml, .env.example, README.md
~~~
NY:
~~~text
  manage.py, requirements.txt, requirements-dev.txt, pyproject.toml, .env.example, README.md
~~~
Begrunnelse: `pyproj` fjernes, og `requirements-dev.txt` erstatter `requirements-bygg.txt`.

#### DOC-04 · arkitektur › Teknologi, Ruff (linje 166) · beslutning 3
GAMMEL:
~~~text
| Ruff (kodestil) | 0.17.4 |
~~~
NY:
~~~text
| Ruff (kodestil, i `requirements-dev.txt`) | 0.17.4 |
~~~
Begrunnelse: Endringen følger SP-18.

### 4.4 UI/UX

#### UXE-01 · experience › Mikrotekst, endringsforslag (etter linje 141) · funn E
GAMMEL:
~~~text
| Endringsforslag | «Prøv 3 timer», «Velg startpunkt», «Prøv marka», «Start fra første forslag igjen» | Godkjent (mock, Turkort) |
~~~
NY:
~~~text
| Endringsforslag | «Prøv 3 timer», «Velg startpunkt», «Prøv marka», «Start fra første forslag igjen» | Godkjent (mock, Turkort) |
| Endringsforslag, halvtimer og alle turtyper | «Prøv 2,5 timer» (halvtimer med komma), «Prøv alle turtyper» | [ASSUMPTION] |
~~~
Begrunnelse: Varigheten går i halvtimessteg, og kildene har ingen tekst for halvtimer eller «alle turtyper».

#### UXE-02 · experience › Mikrotekst, MET-kreditering (etter linje 143) · funn H
GAMMEL:
~~~text
| Grunnlag for tips | «Etter værvarselet for startpunktet kl. 10–16.» | Godkjent (mock) |
~~~
NY:
~~~text
| Grunnlag for tips | «Etter værvarselet for startpunktet kl. 10–16.» | Godkjent (mock) |
| Kreditering for værdata | «Data fra MET Norge» (lenke til MET Norge), rett etter grunnlagslinjen | PRD (NFR-7). MET-formen: Godkjent (memlog) |
~~~
Begrunnelse: MET-krediteringen flyttes til værdataene.

#### UXE-03 · experience › Mikrotekst, Kreditering (linje 178) · funn G, H og nytt funn 3
GAMMEL:
~~~text
| Kreditering | «© Kartverket · © OpenStreetMap contributors · Data fra MET Norge» | PRD (NFR-7). MET-formen: Godkjent (memlog) |
~~~
NY:
~~~text
| Kreditering (på kartet) | «© Kartverket · © OpenStreetMap contributors» | PRD (NFR-7) |
| Kreditering for turillustrasjon uten kart | «Rute: © Kartverket» eller «Rute: © OpenStreetMap contributors», etter turens kilde | [ASSUMPTION] |
~~~
Begrunnelse: Endringen følger SP-09 og EP-29.

#### UXE-04 · experience › Component Patterns, Kreditering (linje 195) · funn G og H
GAMMEL:
~~~text
| Kreditering | Turforslag (på kartet) | Alltid synlig på kartet. Lenkene er understreket: Kartverket til Kartverkets lisensside, «OpenStreetMap contributors» (`lang="en"`) til openstreetmap.org/copyright og «Data fra MET Norge» til MET Norge. |
~~~
NY:
~~~text
| Kreditering | Turforslag (på kartet) | Alltid synlig på kartet, også uten JavaScript og når flisene feiler, fordi den renderes på serveren. Lenkene er understreket: Kartverket til Kartverkets lisensside og «OpenStreetMap contributors» (`lang="en"`) til openstreetmap.org/copyright. «Data fra MET Norge» står i Bekledningstips. |
~~~
Begrunnelse: Endringen følger SP-09.

#### UXE-05 · experience › Component Patterns, Turillustrasjon (linje 198) · nytt funn 3
GAMMEL:
~~~text
Tegnes fra rutelinjen og høydeprofilen.
~~~
NY:
~~~text
Tegnes fra rutelinjen og høydeprofilen. Vises den uten kartet på siden (Søk, Turoppsummering), står krediteringslinjen fra Mikrotekst under den (story 6.1).
~~~
Begrunnelse: Endringen følger EP-29.

#### UXE-06 · experience › Component Patterns, Bekledningstips (linje 206) · funn H
GAMMEL:
~~~text
grunnlaget i én linje og ett eller flere tips etter FR-9, ordrett.
~~~
NY:
~~~text
grunnlaget i én linje med lenken «Data fra MET Norge» rett etter, og ett eller flere tips etter FR-9, ordrett.
~~~
GAMMEL:
~~~text
Mangler værvarsel, byttes listen ut med en Melding (info) under samme overskrift.
~~~
NY:
~~~text
Mangler værvarsel, byttes listen ut med en Melding (info) under samme overskrift, uten «Data fra MET Norge».
~~~
Begrunnelse: Krediteringen vises bare der MET-data vises.

#### UXE-07 · experience › Component Patterns, Tilstandspanel (linje 208) · funn E
GAMMEL:
~~~text
«Prøv 3 timer» og «Prøv marka» kjører søket på nytt med én endring.
~~~
NY:
~~~text
«Prøv 3 timer» og «Prøv marka» er knapper i et lite POST-skjema med CSRF som kjører søket på nytt med én endring. Hvilke endringer som foreslås (høyst tre, og bare når de gir treff), står i story 1.12 (`foresla_endringer`).
~~~
Begrunnelse: Endringen følger EP-24 og EP-25.

#### UXE-08 · experience › frontmatter (linje 5)
GAMMEL:
~~~text
updated: 2026-11-15
~~~
NY:
~~~text
updated: 2026-11-22
~~~
Begrunnelse: Dokumentet er endret.

#### UXD-01 · design › Components, Tilstandspanel (linje 596) · funn E
GAMMEL:
~~~text
Hver rad har tekst til venstre og en handlingslenke til høyre, med `border` mellom radene.
~~~
NY:
~~~text
Hver rad har tekst til venstre og en handling til høyre, med `border` mellom radene. Forslag som kjører søket på nytt («Prøv 3 timer», «Prøv marka») og «Start fra første forslag igjen» er knapper i et lite POST-skjema med CSRF, stylet som en handlingslenke. «Velg startpunkt» og «Endre søk» er vanlige lenker.
~~~
GAMMEL:
~~~text
updated: 2026-11-06
~~~
NY:
~~~text
updated: 2026-11-22
~~~
Begrunnelse: En lenke kan ikke sende søket som POST (AD-5 punkt 1).

### 4.5 Andre artefakter

- **`_bmad-output/implementation-artifacts/epic-1-context.md`:** kompileres på nytt med `compile-epic-context` etter endringene. Linjene om `pyproj` (Stack) og kreditering (Requirements) blir ellers feil. Fila redigeres ikke for hånd.
- **`requirements-bygg.txt`:** finnes ikke ennå. Den skal ikke lages. I stedet lages `requirements-dev.txt` med `ruff==0.17.4` i Story 1.1.
- **Steder som nevner `requirements-bygg.txt` eller hvor Ruff installeres, og som blir rettet over:** epics 96, 333, 345, 491, 2117 og 2240, spine 171, 172, 196, 239 og 252, og arkitektur 166 og 177. Historiske filer (`.logs/`, `reviews/`, research og PRD-uttrekk) endres ikke.

## 5. Overlevering til implementering

**Omfang: Moderate.** Flere artefakter endres, men scope og prioritet er de samme, og ingen epics planlegges om.

| Rolle | Ansvar |
|---|---|
| Claude (dev) | Gjør endringene i seksjon 4 mekanisk på grenen `planlegging/readiness-rettinger`, i rekkefølgen 4.3, 4.2, 4.1, 4.4, slik at spinen er bindende først. Én commit per artefakt med henvisning til ID-ene (for eksempel `SP-02`). Kompilerer `epic-1-context.md` på nytt. |
| Hannah (produkteier) | Godkjenner dette dokumentet og PR-en, og godkjenner [ASSUMPTION]-tekstene senere (UXE-01, UXE-03). |
| Etterpå | Ny `bmad-sprint-planning` med readiness gate, deretter `bmad-build` for Story 1.1. |

**Kriterier for at endringene er gjort:**
1. Hver GAMMEL-tekst i seksjon 4 er borte fra fila si, og hver NY-tekst finnes der.
2. `grep -rn "pyproj\|requirements-bygg\|UTM" epics.md ARCHITECTURE-SPINE.md docs/arkitektur.md` gir ingen treff (memlog linje 36 og addendumets notat er unntatt).
3. `grep -n "CSV, YAML\|testbruker\.\*\|TURTYPE\|basismalen med" ` i spinen og epics gir ingen treff.
4. «Data fra MET Norge» finnes ikke i Story 1.10, UX-DR14 eller i spinens konvensjon for kart.
5. `epic-1-context.md` er kompilert på nytt, og den nye readiness gate gir PASS, eller bare CONCERNS som ikke gjelder funnene A–L.

## 6. Gjennomføring og kontroll (2026-11-22)

**Lagt inn.** Alle endringene i seksjon 4 er lagt inn med et skript. For hvert par byttet det eksakt GAMMEL med NY, og det ville stoppet hvis GAMMEL ikke fantes nøyaktig én gang. Ingen endring feilet. Linjeskiftene (CRLF) er beholdt.

| Fil | Erstatninger |
|---|---|
| epics.md | 40 |
| ARCHITECTURE-SPINE.md | 19 |
| EXPERIENCE.md | 9 |
| docs/arkitektur.md | 6 |
| prd.md | 4 |
| DESIGN.md | 2 |
| addendum.md | 1 |
| .memlog.md | 1 (3 nye linjer) |

**Kontroll med grep** etter `pyproj` (uten `pyproject`), `requirements-bygg`, `25832`, `25833`, `UTM`, `YAML`, `TURTYPE`, `inn i SQLite` og `MET Norge` i planfilene og `docs/`. Alle treffene som står igjen, skal stå der:

- **Ny tekst etter forslaget:**
  - spine:219
  - epics:84, 126, 172, 241, 290, 494 («bruker ikke `pyproj`»), 1872, 1873 og 1882
  - prd:388
  - experience:145, 198 og 209
  - arkitektur `.memlog.md`:56–57
- **Historikk som ikke skal endres:**
  - arkitektur `.memlog.md`:18, 24, 36, 43 og 44. Disse er erstattet av de nye linjene 55–57.
  - addendum:80, der den opprinnelige teksten beholdes og notatet fra 2026-11-22 er lagt til.
  - UX `.memlog.md`:62, som er beslutningen om MET-formen.
- **Research, review, extract og reconcile:** 33 treff. Dette er historiske uttrekk og skal ikke endres.
- **Gjelder ikke denne appen:** `architecture/technology.md` (treffet er bare `pyproject`).

Det var ingen rester som måtte rettes.

**Sprint planning (dry-run):** `sprint_plan.py generate … --dry-run` gir 6 epics og 41 stories (47 backlog, 6 optional). Den eneste advarselen gjelder overskriften `## Epic-liste` (epics:243). Den samme advarselen kommer på den committede versjonen av `epics.md`, så ingen advarsel er ny.

## Vedlegg: status per punkt i sjekklisten

| Punkt | Status | Merknad |
|---|---|---|
| 1.1 Utløsende story | [x] | Ingen story. Utløseren var readiness gate (2026-11-20) og kompileringen av `epic-1-context.md` |
| 1.2 Kjerneproblem | [x] | Uklare krav og motstrider mellom artefaktene, pluss en ny teknisk opplysning (WFS i WGS84) |
| 1.3 Bevis | [x] | Linjehenvisninger i seksjon 1, og WFS-testen 2026-11-22 |
| 2.1 Gjeldende epic | [x] | Epic 1 kan fullføres med presiseringer |
| 2.2 Endringer på epic-nivå | [x] | Bare stories endres. Ingen epics legges til eller fjernes |
| 2.3 Senere epics | [x] | Epic 5 (5.3) og Epic 6 (6.1, 6.5). Epic 2–4 er uendret |
| 2.4 Overflødige eller nye epics | [x] | Ingen |
| 2.5 Rekkefølge og prioritet | [x] | Uendret. C og D er vurdert og droppet |
| 3.1 PRD | [x] | FR-4, NFR-7 og addendumet. MVP er uendret |
| 3.2 Arkitektur | [x] | AD-2, AD-3, AD-5, AD-12, AD-15, konvensjonen, Stack, kildetreet, ER-diagrammet og Deferred |
| 3.3 UI/UX | [x] | `EXPERIENCE.md` (Mikrotekst og komponenter) og `DESIGN.md` (Tilstandspanel) |
| 3.4 Andre artefakter | [!] | `epic-1-context.md` må kompileres på nytt. `docs/arkitektur.md` og memlog er med i seksjon 4 |
| 4.1 Direkte justering | [x] | Valgt |
| 4.2 Tilbakerulling | [N/A] | Ingen kode eller ferdige stories |
| 4.3 MVP-vurdering | [N/A] | Scope er uendret |
| 4.4 Valgt vei | [x] | Direkte justering |
| 5.1 Sammendrag | [x] | Seksjon 1 |
| 5.2 Konsekvenser | [x] | Seksjon 2 |
| 5.3 Anbefaling | [x] | Seksjon 3 |
| 5.4 MVP og plan | [x] | MVP er ikke berørt. Planen står i seksjon 5 |
| 5.5 Overlevering | [x] | Seksjon 5 |
| 6.1 Sjekklisten fullført | [x] | Alle relevante punkter er gått gjennom |
| 6.2 Forslaget er riktig | [x] | GAMMEL-tekstene er hentet ordrett fra filene 2026-11-22 |
| 6.3 Godkjenning fra brukeren | [x] | Godkjent av Hannah 2026-11-22, med beslutning 1–3 |
| 6.4 sprint-status.yaml | [N/A] | Fila finnes ikke ennå. Den lages i den nye sprint planning |
| 6.5 Neste steg | [x] | Grenen `planlegging/readiness-rettinger`, så sprint planning, så `bmad-build` for Story 1.1 |
