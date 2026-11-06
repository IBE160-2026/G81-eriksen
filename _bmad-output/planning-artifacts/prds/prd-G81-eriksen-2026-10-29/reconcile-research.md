---
title: "Input-avstemming: teknisk research turdata Oslomarka mot PRD"
created: 2026-11-06
input: "_bmad-output/planning-artifacts/research/technical-turdata-oslomarka-2026-10-29/ (research.md + digests/)"
checked_against: "prd.md, addendum.md, .memlog.md, research-gradering.md (versjon 2026-11-06)"
---

# Input-avstemming: teknisk research (turdata Oslomarka) mot PRD

**Metode:** Hvert funn, hver anbefaling og hver risiko i `research.md` (og relevante digests) er sjekket mot `prd.md`, `addendum.md` og `.memlog.md`. Beslutninger i memloggen og i `research-gradering.md` er nyere og overstyrer researchen bevisst. Slike avvik regnes ikke som hull når de er logget.

**Alvorlighet:** *Høy* = PRD mangler et krav eller en begrensning som påvirker lovlighet, korrekthet eller testbarhet. *Middels* = PRD-nivå, men kan løses med en kort presisering. *Lav* = hører hjemme i addendum/arkitektur, eller er bare en ryddejobb.

Kortnavn for kilder: **R** = `research.md`, **F10** = `digests/D3D4-lisens-tid-r1-1.md` funn F10, **RG** = `research-gradering.md`.

---

## 1. Kontroll av formel for estimert tid (FR-3 / addendum)

| Punkt | Research | PRD/addendum | Status |
|---|---|---|---|
| Regel | BFU: 15 min/km + 15 min per 100 m opp + 15 min per 200 m ned (R D4 [21], F10) | Addendum: samme | **Samsvarer** |
| Tempo | ca. 4 km/t, mer forsiktig enn Naismith (R D4, F10) | Addendum: «omtrent 4 km/t på flat mark» | **Samsvarer** |
| Summering eller maks+halv | F10 sitt eksempel «6 km med ±800 m tar 4,5 t» gir 90 + 120 + 60 = 270 min, altså **summering** | Addendum sier at formelen må kontrolleres fordi noen varianter bruker «største + halvparten av minste» | Samsvarer med summering. Forbeholdet i addendum gjelder DIN 33466/DAV-varianten, ikke BFU-regelen. F10 sier også at de *offisielle* sveitsiske skilttidene bruker et helningspolynom, og at BFU-regelen er en tommelfingerregel. Verifiseringsnotatet kan derfor presiseres (se H-9). |
| Tur-retur | – (researchen sier ikke noe om dette) | FR-3: lengde og stigning for begge veier | OK. UJ-1-eksemplet (7,2 km, 2 t 40 min) gir ca. 230 hm opp én vei, noe som er konsistent med grønt nivå. |
| Tillit | Middels. Formlene bommer 13,5–15,5 % og undervurderer trolig tiden for nybegynnere (R D4 [20]) | Ikke nevnt | Se H-4 |
| Kildehenvisning | Funnet ligger i `digests/D3D4-lisens-tid-r1-1.md`, F10 | Addendum viser til «D34a F10» | Feil filnavn i henvisningen (lav, H-9) |

**Konklusjon:** Formelen i addendum stemmer med researchen. Det som mangler, er at PRD-en ikke har et felt for **nedstigning** (se H-3) og ikke tar stilling til påslaget for nybegynnere (H-4).

## 2. Kontroll av graderingsregel (FR-2)

| Punkt | Research (R) | research-gradering (RG, nyere) | PRD FR-2 | Status |
|---|---|---|---|---|
| Terskler | ≤5 km / ≤300 hm grønn, ≤10/≤600 blå, lav tillit [23] (R anbefaling 2) | <5/<300, <10/<600, <20/<1000, ellers svart (høy tillit, Merkehåndboka 2019 s. 100–101) | Som RG | **Samsvarer**. R er bevisst overstyrt (memlog: «Research-subagent ferdig … Graderingsregel …») |
| Strengeste farge, grad opp ved grense | – | Ja | Ja | Samsvarer |
| Lengde én vei | – | Én vei, men **hele lengden for rundturer** | «Lengden måles én vei» | Uklart for rundtur (H-5) |
| Hva «høydemeter» betyr | – | **Samlet stigning** for hele ruta (sum av alle oppstigninger, ikke høydeforskjell start–topp) | Ikke definert i §3 eller FR-2 | Mangler (H-5) |
| Forbehold om ren tallregel | – | Ja | Ja, i FR-2 | Samsvarer |
| Formulering mot bruker | – | Si «basert på DNT/Merkehåndbokas nasjonale graderingsmal», ikke «gradert av DNT» | Ikke nevnt | Lav (H-8) |
| Gradering fra kilden | Turrutebasen har gradering på bare 11,7 % av segmentene. OSM har ingen. Gruppen må gradere selv (R D1) | – | FR-2 setter egen regel | Samsvarer |

---

## 3. Hull

### H-1. Synlig kreditering av datakilder og kart (Kartverket CC BY 4.0, OSM ODbL) — **Høy**
- **Kilde:** R D3 (tabell og «Kreditering for OSM»), R anbefaling 6 (tillit høy), [13], [17], [18]. D3D4 F1: OSM-kreditering skal ligge i hjørnet av kartet, kan skjules etter interaksjon, men må være lett å finne og lesbar.
- **PRD i dag:** FR-1 sier bare at «kilde og lisens er registrert for hver tur». FR-6 og NFR-ene krever ikke at kreditering *vises*. Kartgrunnlaget (OSM-fliser eller Kartverkets WMTS) er ikke nevnt noe sted.
- **Hvorfor PRD:** Kreditering er en lisensbetingelse og en synlig del av brukergrensesnittet, ikke bare implementasjon. Uten krav blir den ikke testet.
- **Forslag:** Legg til et krav, enten nytt FR eller nytt punkt i FR-6: «Kartet viser kreditering for alle datakilder som brukes, synlig og lesbart: ‘© Kartverket’ for Turrutebasen og høydedata, ‘© OpenStreetMap contributors’ med lenke til openstreetmap.org/copyright når OSM-data eller OSM-kartfliser brukes, og kreditering for kartgrunnlaget.» Valg av kartgrunnlag og flisvilkår (User-Agent, ingen masse-nedlasting) hører hjemme i addendum/arkitektur.
- **Plassering:** PRD (krav) + addendum (valg av kartgrunnlag og flisvilkår).

### H-2. ODbL-begrensning på bruk av OSM-data — **Middels**
- **Kilde:** R D3 (ODbL §4.4/§4.6/§6.2, OSMF: under 100 objekter, engangsuttrekk og håndplukket regnes som uvesentlig [15]), R beslutningsmatrise («Andrevalg: OSM … under 100 objekter i ett engangsuttrekk»), R anbefaling 1 (Turrutebasen primær, OSM reserve), R «Lisens styrer arkitekturen». D3D4 F2/F3: en database som kan hentes ut som GeoJSON er trolig en *avledet database*.
- **PRD i dag:** §4.1 sier at rutelinjene hentes fra «Turrutebasen og OpenStreetMap» som likeverdige kilder. Ingen begrensning på omfanget av OSM-bruken, og ingen logget beslutning om ODbL.
- **Hvorfor PRD:** Begrensningen styrer omfanget av kurateringen og er en lovlighetsbetingelse (et absolutt krav i researchens kravramme). Detaljene om hvordan egne felt holdes adskilt (Collective Database) hører hjemme i addendum.
- **Forslag:** Presiser §4.1/FR-1: «Turrutebasen er primærkilde. OSM brukes bare som supplement for enkeltturer som mangler der, i ett håndplukket engangsuttrekk med færre enn 100 OSM-objekter totalt.» Legg ODbL-tolkningen (Collective Database, at turdatabasen ikke tilbys som nedlastbar fil, forbeholdet om at §6.2-ordlyden ikke er sitert direkte) i addendum.
- **Plassering:** PRD (begrensning) + addendum (lisensvurdering).

### H-3. Turdatabasen mangler nedstigning, som tidsformelen trenger — **Høy**
- **Kilde:** R D4 og F10: formelen bruker «15 min per 200 m **ned**». R anbefaling 5 lister feltet `hoydemeter`. RG: høydemeter = samlet stigning.
- **PRD i dag:** §3 *Tur* har bare «høydemeter». FR-3 sier «lengde og stigning for begge veier». Addendum bruker «stigning og nedstigning for begge veier». For en rundtur er samlet nedstigning ≈ samlet stigning. For en tur-retur er nedstigningen tilbake lik stigningen ut, men turen ut kan også ha nedstigning, så tallet kan ikke utledes av ett felt alene.
- **Hvorfor PRD:** Feltlisten i §3 er datakontrakten for FR-1 og FR-3, og SM-2 krever tester av FR-3. Uten nedstigning er FR-3 ikke entydig.
- **Forslag:** Utvid *Tur* i §3: «… høydemeter (samlet stigning) og samlet nedstigning, begge for én vei eller for hele rundturen …». Juster FR-3: «For tur-retur legges stigning og nedstigning for begge retninger sammen (opp tilbake = ned ut, ned tilbake = opp ut).»
- **Plassering:** PRD.

### H-4. Usikkerhet i tidsestimatet og påslag for nybegynnere — **Middels**
- **Kilde:** R anbefaling 4 («legg til et påslag for nybegynnere», mottaker **PRD**, forretningsregler). R D4: formlene bommer 13,5–15,5 % [20] og undervurderer trolig tiden for nybegynnere (uverifisert slutning). DNT fellesturer går ca. 3 km/t [22], mens BFU-regelen tilsvarer ca. 4 km/t.
- **PRD i dag:** Memloggen valgte sveitsisk regel «fordi den passer nybegynnere», men verken memlogg, PRD eller addendum sier at påslaget er vurdert og forkastet. FR-5-filteret bruker «estimert tid ≤ varighet» uten margin, så en nybegynner kan få en tur som i praksis tar lengre tid enn hen har.
- **Hvorfor PRD:** Dette er en forretningsregel som påvirker filteret (FR-5) og motmålet SM-C1.
- **Forslag:** Ta et eksplisitt valg og logg det. Enten (a) «Sveitsisk regel brukes uten påslag fordi den allerede er forsiktig (ca. 4 km/t). Faktisk tid logges (FR-16) og kan brukes til å kalibrere senere.» Eller (b) legg inn et fast påslag eller en margin i FR-5-filteret, for eksempel estimert tid ≤ 90 % av varigheten. Nevn usikkerheten (±15 %) som forbehold i addendum.
- **Plassering:** PRD (valget og eventuell margin) + addendum (begrunnelse).

### H-5. Definisjon av høydemeter og lengde for rundtur ved gradering — **Middels**
- **Kilde:** RG §1.1 (fotnoten i Merkehåndboka) og RG §4: hm = samlet stigning for hele ruta. Lengde = én vei, men **hele rundturen** for rundturer.
- **PRD i dag:** FR-1: «Lengden lagres én vei». FR-2: «Lengden måles én vei, slik standarden gjør». Rundturer er ikke nevnt, og høydemeter er ikke definert.
- **Forslag:** I FR-2: «Lengde og høydemeter (samlet stigning) måles én vei for tur-retur og for hele runden for rundturer.» Legg til samme definisjon i §3.
- **Plassering:** PRD.

### H-6. Støyfiltrering og kontroll av høydedata — **Middels** (krav) / detaljer i addendum
- **Kilde:** R D2 [12]: ubehandlet terrengmodell ga 1 434 m i stedet for 1 080 m stigning (+33 %). Bruk terskel (2–10 m) eller glatting, og kontroller mot publiserte høydeprofiler. R anbefaling 3. R åpne spørsmål: «Riktig terskel for høydemeter i Marka-terreng: test på 2–3 turer».
- **PRD i dag:** §4.1 sier bare at høydemeterne hentes fra «Kartverkets høydedata». Ingen krav til kvalitet eller kontroll.
- **Hvorfor PRD (delvis):** Graderingen (FR-2) og tiden (FR-3) avhenger direkte av høydemeterne. Et avvik på 33 % kan flytte en tur fra grønn (<300 hm) til blå, og det rammer nybegynnere (SM-C1). Hvordan filtreringen gjøres, er en teknisk detalj.
- **Forslag:** I FR-1: «Høydemeter beregnes med støyfiltrering, og verdiene kontrolleres mot en publisert høydeprofil for minst 2–3 turer før databasen tas i bruk.» Legg terskel/glatting, høyde-API (50 punkter per kall) og beregning ved import i addendum/arkitektur.
- **Plassering:** PRD (kvalitetskrav, kort) + addendum (metode).

### H-7. Krav til kurateringen og sammensetningen av turdatabasen — **Middels**
- **Kilde:** R sammendrag og «Innsikt på tvers»: «Nybegynnerverdien ligger i kurateringen, ikke i kilden». Turer må settes sammen av segmenter, og noen må tegnes manuelt (Vettakollen). R anbefaling 2 (mottaker PRD/epics).
- **PRD i dag:** FR-1 krever 20–30 turer, minst én svart og et fåtall toppturer. Det er ingen krav til at det finnes nok grønne og blå turer i ulike lengder, at alle turtyper og startpunkter er dekket, eller at hver tur er kontrollert (sammenhengende rutelinje, riktig startpunkt). FR-8 og UJ-1 forutsetter at grønne turer som passer korte varigheter finnes.
- **Forslag:** Legg til akseptkriterier i FR-1, for eksempel: «Flertallet av turene er grønne eller blå. Det finnes minst én grønn tur under 2 timer for hver turtype. Hvert startpunkt har minst to turer. Hver rutelinje er kontrollert manuelt for sammenheng og riktig startpunkt.» Selve arbeidsflyten (sette sammen segmenter, geojson.io, koordinatsystem) hører hjemme i addendum/arkitektur.
- **Plassering:** PRD (akseptkriterier) + addendum (prosess).

### H-8. Formulering om DNT-gradering mot brukeren — **Lav**
- **Kilde:** RG §4 forbehold: fargene skal beskrives som «basert på DNT/Merkehåndbokas nasjonale graderingsmal», ikke som offisielt gradert av DNT.
- **PRD i dag:** §3 *Turnivå* sier «DNT-farge». FR-6 viser turnivå uten slik forklaring.
- **Forslag:** Ett punkt i FR-6 eller §6: «Turnivået forklares som beregnet av tjenesten etter Merkehåndbokas mal, ikke som en offisiell DNT-gradering.»
- **Plassering:** PRD (kort) / UX.

### H-9. Ryddepunkter i addendum — **Lav**
- Kildehenvisningen «D34a F10» skal være `digests/D3D4-lisens-tid-r1-1.md` F10.
- Verifiseringsnotatet kan presiseres: varianten «største + halvparten av minste» er DIN 33466/DAV, ikke BFU. BFU-eksemplet i F10 (6 km, ±800 m = 4,5 t) bekrefter summering. Notatet bør nevne at offisielle sveitsiske skilttider bruker et helningspolynom, og at prosjektet bevisst velger tommelfingerregelen.
- **Plassering:** Addendum.

### H-10. Ferskhet i API-er, koordinatsystem og lagring — **Lav** (arkitektur)
- **Kilde:** R Ferskhetskart: API-status for nedlasting og høyde-API må sjekkes igjen **2026-11-29**, og «Kjør Refresh før byggestart». R D2: GML finnes bare i UTM (25832/25833), WGS84 bare som GPX (ikke testet). Statisk GeoJSON med `kilde`, `lisens`, `lengde_km`, `hoydemeter`, `gradering`, `estimert_tid` (R anbefaling 5). Turf.js for lengde.
- **PRD i dag:** Ikke nevnt, og det er riktig at dette ikke står i PRD-en. Det bør likevel stå i addendum så det blir med til arkitekturen.
- **Forslag:** Kort avsnitt i addendum: «Til arkitekturen: datauttrekk og beregning ved import».
- **Plassering:** Addendum/arkitektur.

### H-11. Dekning utenfor Oslo og Bærum er ikke målt — **Lav**
- **Kilde:** R åpne spørsmål: Lillestrøm, Nittedal, Nordre Follo og Lunner er ikke målt.
- **PRD i dag:** «Oslo-området» er ikke avgrenset. Siden startpunktene velges fra en liste (§9), er risikoen liten.
- **Forslag:** Antakelse i §10 eller addendum: «Turene hentes fra Oslo og Bærum (målt dekning). Andre markakommuner krever en ny dekningssjekk.»
- **Plassering:** Addendum (eventuelt §10).

### H-12. Datakilde endret fra brief er ikke med i §9 — **Lav**
- **Kilde:** R anbefaling 7: briefens «rutelinjer hentet fra OpenStreetMap» bør bli «fra Kartverkets Turrutebasen (OSM som supplement)».
- **PRD i dag:** §4.1 nevner begge kilder, men tabellen i §9 sier ikke at primærkilden er endret.
- **Forslag:** Ny rad i §9: «Turrutebasen er primærkilde, OSM er supplement | Åpen CC BY-lisens, oppdatert ukentlig, vant beslutningsmatrisen 3,65 mot 2,9».
- **Plassering:** PRD §9.

### H-13. Lisens og kreditering for værdata fra MET (NLOD/CC BY) — **Middels** (utenfor researchen)
- **Kilde:** *Ikke dekket av researchen.* Memloggen («Åpne punkter … værkilde+lisens (ikke dekket i research)») har dette som åpent punkt, men det er aldri lukket med en beslutning. MET Norges data er lisensiert under NLOD 2.0 og CC BY 4.0 og krever kreditering. API-vilkårene krever også en identifiserende User-Agent og at svar mellomlagres (caching). Dette er hentet fra generell kunnskap og må verifiseres mot api.met.no/doc/TermsOfService.
- **PRD i dag:** FR-9 og FR-10 bruker MET, men det finnes ikke noe krav om kreditering.
- **Forslag:** Ta MET med i kravet fra H-1, for eksempel «Værdata fra MET Norge», og legg API-vilkårene (User-Agent, caching) i addendum. Logg at det åpne punktet er lukket.
- **Plassering:** PRD (kreditering) + addendum (API-vilkår).

---

## 4. Funn som er dekket eller bevisst overstyrt (ingen handling)

- ut.no har ikke åpent API: PRD og addendum bruker en statisk lenke og henter ingenting under kjøring. **Samsvarer.**
- Ingen henting av turdata under kjøring og statisk database: §4.1 og §7.2. **Samsvarer.**
- KI beregner ikke tid eller nivå. Formlene er deterministiske: FR-3. **Samsvarer.**
- Kilde og lisens per tur («billigste sikring»): FR-1. **Samsvarer.**
- Tersklene ≤ fra R anbefaling 2 (lav tillit) er erstattet av < fra RG (høy tillit). **Overstyrt med logget beslutning.**
- Valgfri halv vekt for nedstigning i bratt terreng og manuell oppgradering for terreng: RG anbefaler ikke dette som standard. FR-2 sier at terreng ikke er med, og forbeholdet er dokumentert. **Overstyrt med logget beslutning.**

## 5. Oppsummering etter alvorlighet

| # | Hull | Alvorlighet | PRD / addendum |
|---|---|---|---|
| H-1 | Synlig kreditering (Kartverket, OSM, kartgrunnlag) | Høy | PRD + addendum |
| H-3 | Nedstigning mangler i datamodellen, men FR-3 trenger den | Høy | PRD |
| H-2 | ODbL: OSM bare som supplement, under 100 objekter, engangsuttrekk | Middels | PRD + addendum |
| H-4 | Påslag for nybegynnere / usikkerhet i tidsestimatet ikke avgjort | Middels | PRD + addendum |
| H-5 | Definisjon av hm (samlet stigning) og lengde for rundtur | Middels | PRD |
| H-6 | Støyfiltrering og kontroll av høydedata | Middels | PRD (kort) + addendum |
| H-7 | Akseptkriterier for kurateringen og sammensetningen | Middels | PRD + addendum |
| H-13 | Kreditering og vilkår for MET (utenfor researchen, åpent punkt i memlogg) | Middels | PRD + addendum |
| H-8 | Formulering «basert på Merkehåndbokas mal» | Lav | PRD/UX |
| H-9 | Kildehenvisning og formelnotat i addendum | Lav | Addendum |
| H-10 | API-ferskhet, UTM/WGS84, GeoJSON-felt | Lav | Addendum/arkitektur |
| H-11 | Dekning utenfor Oslo/Bærum | Lav | Addendum/§10 |
| H-12 | Endret datakilde ikke med i §9 | Lav | PRD §9 |
