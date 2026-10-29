# Uttrekk fra teknisk research: Turdata for Oslomarka (grunnlag for PRD)

Kilde: `_bmad-output/planning-artifacts/research/technical-turdata-oslomarka-2026-10-29/research.md` (forkortet **R**, med kildenummer [n] fra R) og digestene i `digests/` (forkortet **D1a** = D1-datakilder-r1-1, **D1o** = D1-osm-empiri-r2-1, **D1t** = D1-turrutebasen-empiri-r2-1, **D2** = D2-uthenting-r1-1, **D34a** = D3D4-lisens-tid-r1-1, **D34b** = D3D4-odbl-naismith-r2-1). Uttrukket 2026-10-29. Dette er et uttrekk, ikke en PRD.

## 1. Hovedkonklusjoner

- **Gjennomførbart, men kurateringen må gruppen gjøre selv.** Ingen åpen kilde leverer «nybegynnerturer» ferdig (R Sammendrag).
- **Primærkilde: Kartverkets Turrutebasen** (CC BY 4.0, ukentlig oppdatert, sist 2026-10-23, nedlastbar uten innlogging). Vant beslutningsmatrisen 3,65 mot 2,90 for OSM (R Sammendrag, Beslutningsmatrise; [1][2][13]).
- **OSM er andrevalg/reserve** for turer som mangler i Turrutebasen (f.eks. Vettakollen), tegnet over OSM-stier, <100 objekter, ett engangsuttrekk (R Beslutningsmatrise).
- **Høydemeter fra Kartverkets høyde-API** (gratis, uten nøkkel, 1 m DTM, maks 50 punkter/kall) (R Sammendrag [11]).
- **Vanskelighetsgrad og tid må beregnes etter egne, faste regler.** Turrutebasen har gradering på bare 11,7 % av Oslo-segmentene (ingen R/S); DNT-hovedrutene i Nordmarka/Østmarka er ugraderte; OSM-turrelasjoner har ingen vanskelighetsgrad (R D1 [2][6]).
- **ut.no/Nasjonal Turbase har ikke noe åpent API** (inaktivt siden ca. 2020) – kan kun brukes som inspirasjon (R D1 [10]; D1a #10).
- **Nybegynnerverdien ligger i kurateringen, ikke i kilden**, og regelbasert gradering passer kravet om at KI bare velger blant kjente turer (R Innsikt på tvers).
- **Lisens styrer arkitekturen:** én statisk GeoJSON med `kilde` per tur fremfor løpende OSM-henting (R Innsikt på tvers).
- **Sterkeste motargument:** begge kildene krever like mye manuell kurering – kildevalget betyr mindre enn kurateringsprosessen (R Beslutningsmatrise).

## 2. Datakilder og lisenskrav

### 2.1 Turrutebasen (Kartverket) – primærkilde
- **Lisens: CC BY 4.0.** Krav: kreditering «© Kartverket», helst med lenke (R D3 [13]; D34a F6). Metadataene sier bare «Åpne data / No conditions apply» uten navngitt lisens; Kartverkets vilkårsside (2026-07-21) er mer presis og følges (R D3 [1][13]; D34a F5).
- **NB: Ikke NLOD.** Researchen fant CC BY 4.0, ikke NLOD, for Turrutebasen. NLOD/PDDL nevnes kun for Oslo kommunes turvei-data (D1a #8, lav–middels tillit), som ble forkastet som kilde.
- Kartverket har bekreftet at Turrutebasen kan brukes i OSM (2014, fornyet 2021) – relevant hvis data blandes (D1a #5).
- Dekning målt (R D1 [2]; D1t #3–#11):
  - Oslo (0301): 3 254 fotrute-segmenter (711,9 km); 186 ruter, hvorav 41 «Ukjent»; median rutelengde 1,3 km, p90 7,5 km.
  - Bærum (3201): 1 864 segmenter (376,7 km); 59 ruter, hvorav 29 «Ukjent». Alle graderte Bærum-ruter heter «Ukjent» (D1t #11).
  - Gradering G/B/R/S: 11,7 % (Oslo), 14,5 % (Bærum). Merking=JA: 97,1 % / 100 % – skiller ikke rutene.
  - Graderte Oslo-ruter er mest bynære elvestrekninger (Oslo Elveforum); «Blåmerket sti Nordmarka» (91 km) og «Østmarka» (94 km) er ugraderte (D1t #8).
  - Nyttige felt: `ruteFølger` (ST = sti, BV = bilvei, GS = gang/sykkelvei osv.) som underlagsindikator; `spesialFotrutetype` (NT = natursti, KT = kultursti m.fl.); `tilpasning` (G = gående, B = barnevogn, R = rullestol) – sjelden i Oslo (7 poster), men 757 i Bærum (D1t #10–#12).
  - `rutetype` er en skiløypekode, ikke turtype; `underlagstype` har 0 verdier i Oslo/Bærum (R D1; D1t #10).
- Datafangst er i stor grad crowdsourcet («Rett i kartet»), manuelt kontrollert mot FKB/N50; kvaliteten varierer per rute (D1t #15).
- Eksempelruter: Sognsvann Brekke turvei (2,3 km, G), Rundtur Ulsrudvann (1,7 km, G), Brennarunden (4,5 km), Frognerseteren–Studenterhytta (6,9 km), Rundtur Frognerseteren–Holmenkollen (1,8 km, B), «Sognsvann – Blanksjø – Ullevålseter», ruter til Kolsås (R D1, Sammendrag [2]; D1t #9).

### 2.2 OpenStreetMap – reserve/supplement
- **Lisens: ODbL 1.0.** En offentlig nettside er «Publicly Use»; en avledet database utløser share-alike (§4.4) og krav om å tilby hele databasen maskinlesbart (§4.6) (R D3 [14]; D34b #1–#4).
- **Unntak:** uvesentlige uttrekk kan brukes fritt (§6.2). OSMF regner <100 Features, hentet ut én gang og håndplukket, som uvesentlig. Gjentatte små uttrekk telles som ett stort; «alle merkede stier i Oslomarka» vil *ikke* være uvesentlig (R D3 [15]; D34b #5–#7).
- Egne felt (lengde, høydemeter, vanskelighetsgrad fra ikke-OSM-kilder) kan trolig holdes som Collective Database (§4.5) – tolkning, ikke uttrykkelig avklart (R D3 [16]; D34b #9).
- **Kreditering:** «© OpenStreetMap contributors» med lenke til openstreetmap.org/copyright, synlig på kartet (typisk nede til høyre). Kan kollapse etter interaksjon/5 s, men må være lett å finne og lesbar (R D3 [17]; D34a F1).
- Dekning (R D1 [6]; D1o): 307 turrelasjoner, 158 av dem unavngitte DNT-segmenter (OSL1–OSL217); ingen vanskelighetsgrad/tidsbruk; bare 8 med lengde; ca. 20–25 navngitte kandidater (Sognsvann natursti, Bogstadvannet rundt, Ulsrudvann rundt, Losbyrunden lille 5,6 km m.fl.). 3 av 4 klassiske nybegynnerturer (Vettakollen, Kolsåstoppen, Ullevålseter) finnes bare som stier og punkter. 2 897 veivisere – godt kart, ikke ferdig turliste. `sac_scale` på 1,2 % av stiene og egner seg dårlig for lavlandsskog (D1a #9).

### 2.3 Kartgrunnlag (bakgrunnskart)
- **OSM-kartfliser** (OSMF tile policy): synlig kreditering (ikke skjult bak toggles), HTTPS, gyldig Referer/User-Agent, respekter cache (≥7 dager), ingen masse-nedlasting/forhåndslasting/offline-bruk. Ingen tallgrenser, ingen SLA, kan blokkeres uten varsel. Leaflet med standard kreditering og uten no-referrer-policy oppfyller kravene (R D3 [18]; D34a F8).
- **Kartverkets topografiske WMTS:** CC BY 4.0 (middels tillit), «© Kartverket». Bruk ut over «normal bruk» av detaljerte data (zoom 12–20, Geovekst) krever tillatelse. Endepunktet har endret seg (2025) – kontroller før bruk (R D3 [13][26]; D34a F6–F7).

### 2.4 Høydedata
- Kartverkets «Åpent API for høyde- og dybdedata»: gratis, uten nøkkel, `dtm1` (1 m terrengmodell) som beste kilde; bruk DTM, ikke DOM (som inkluderer trær). Ingen oppetidsgaranti; brytende endringer varsles ≥3 mnd i forveien via Geonorge-tjenestevarsler. Ingen dokumentert bruksgrense (R D2 [11]; D2 #9–#10). Lisens: Kartverket CC BY 4.0 → «© Kartverket» (R D3 [13]).

### 2.5 Vær
- **Ikke dekket av researchen.** Ingen værkilde (f.eks. MET/yr) eller værlisens ble undersøkt. Må avklares separat hvis vær er i scope.

### 2.6 Forkastede kilder
- **ut.no/DNT:** ingen åpent API (nasjonalturbase.no avviste tilkobling; GitHub sist oppdatert 2020-03). Bygger på fravær av bevis – middels tillit (R D1 [10]; D1a #10).
- **Oslo kommune:** bynære turveier, ikke Marka (R D1; D1a #8).
- **Skiforeningen:** vinterløyper, ikke åpne data (R D1; D1a #11).

## 3. Tidsestimat-metode og vanskelighetsgrad-regler

### 3.1 Tidsformler (R D4; D34a F9–F11; D34b #10–#15)
| Formel | Regel | Merknad |
|---|---|---|
| Naismith (1892) | 5 km/t + 1 t per 600 hm (t(min) = 12·km + 10·hm/100) | Klassiker; rimelig totaltid for erfarne (R [19]; D34b #10, #13) |
| Tobler (1993) | v = 6·e^(−3,5·\|S+0,05\|) km/t | Krever høydeprofil (R [25]) |
| Sveitsisk BFU-regel | 15 min/km + 15 min/100 m opp + 15 min/200 m ned (≈4 km/t) | Mer forsiktig, bedre for nybegynnere (R [21]; D34a F10) |
| DNT fellesturer | ca. 3 km/t | Referanse for gruppetempo, lav–middels tillit (R [22]) |
| Langmuir | Naismith-korreksjon for nedstigning | Kalt «urealistisk» ved overganger (D34a F9; D34b #11) |

- Største studie (7 636 GPS-spor): Naismith og Tobler bommer 13,5–15,5 % på hele turer og beskriver en «gjennomsnittlig» turgåer (R [20]; D34b #14).
- Ingen studie isolerer nybegynnere; formlene **undervurderer trolig tiden for nybegynnere** (uverifisert slutning) (R D4; D34b #15).
- Alle formlene er deterministiske funksjoner av lengde og stigning → forenlig med kravet om at KI ikke skal gjette tid (R D4).
- ut.no har ingen offentlig tidsformel; tidsbruk settes av forfatter etter «nasjonale standarder» (D34b #16).
- **Anbefalt:** start med Naismith eller sveitsisk regel, legg til nybegynnerpåslag, vis «pauser ikke inkludert» (R Anbefaling 4, middels tillit – påslaget er ikke forskningsbasert).

### 3.2 Vanskelighetsgrad
- Ingen kilde har brukbar gradering for Oslomarka → egen, regelbasert gradering er nødvendig (R Sammendrag, D1).
- Foreslått regel (UT/DNT-tommelfingerregel, **lav tillit**, fra søkesnippet): **grønn ≤5 km og ≤300 hm; blå ≤10 km og ≤600 hm; rød «krevende»** (R Anbefaling 2 [23]; D34b #17).
- Mulige tilleggsindikatorer: `ruteFølger` (BV/SB/GS/TV = vei/grus = lettere), lengde og DTM-stigning (D1t «Leads»).
- Turrutebasens koder: G = enkel, B = middels, R = krevende, S = trolig svart/ekspert, I = trolig ikke gradert (uverifisert; «Se Merkehåndboka») (D1t #12).

## 4. Krav som bør bli FR/NFR i PRD-en (capabilities)

**Funksjonelle krav (forslag)**
- FR: Systemet skal tilby en kuratert samling på 20–30 nybegynnerturer i Oslomarka, hver med rutelinje, navn, lengde, høydemeter, vanskelighetsgrad og estimert tid (R beslutning, Anbefaling 2, 5).
- FR: Hver tur skal vise vanskelighetsgrad satt etter én fast, dokumentert regel basert på lengde og høydemeter (R Anbefaling 2).
- FR: Hver tur skal vise estimert gåtid beregnet deterministisk fra lengde og stigning, med tydelig merknad «pauser ikke inkludert» (R Anbefaling 4, D4).
- FR: KI-funksjoner skal bare velge/anbefale blant de kuraterte turene og ikke generere tid eller gradering selv (R D4, Innsikt på tvers).
- FR: Hver tur skal ha registrert kilde og lisens, slik at enkeltturer kan byttes ut uavhengig av resten (R Beslutningsmatrise, Anbefaling 5).
- FR: Kartet skal vise turens rutelinje på et bakgrunnskart (R D3, Anbefaling 6).

**Ikke-funksjonelle krav / begrensninger (forslag)**
- NFR (lisens): Kreditering «© Kartverket» (med lenke der mulig) og «© OpenStreetMap contributors» (lenke til /copyright) skal være synlig på kartet og lesbar (R D3 [13][17]; D34a F1, F6).
- NFR (lisens): Eventuelle OSM-avledede turgeometrier skal holdes under 100 objekter, hentes én gang og være håndplukket (ellers gjelder ODbL share-alike og krav om å tilby hele databasen) (R D3 [14][15]; D34b #5–#7).
- NFR (lisens/kostnad): Kun gratis, åpne kilder uten betalt nøkkel, lovlige i et studentprosjekt (R Beslutningsmatrise – absolutte krav).
- NFR (bruksvilkår): Kartflisbruk skal følge OSMF tile policy (ingen masse-nedlasting/offline, gyldig Referer/User-Agent) (R D3 [18]).
- NFR (nøyaktighet): Høydemeter skal være støyfiltrerte og kontrollert mot publiserte høydeprofiler for et utvalg turer (R D2 [12]).
- NFR (robusthet): Appen skal ikke være avhengig av eksterne data-API-er ved kjøring for turdata (beregnes ved import) – Overpass og høyde-API gir ingen oppetidsgaranti (R Anbefaling 3; D2 #1, #9).
- NFR (aktualitet): Data og API-status sjekkes på nytt før byggestart (tidligste re-sjekk 2026-11-29) (R Ferskhetskart).

**Endring i brief/PRD-tekst:** «rutelinjer hentet fra OpenStreetMap» → «fra Kartverkets Turrutebasen (OSM som supplement)» (R Anbefaling 7).

## 5. Implementasjonsdetaljer (hører i addendum/arkitektur)

- **Turrutebasen-uthenting:** `POST https://nedlasting.geonorge.no/api/order` (kommune 0301/3201), JSON-body med metadataUuid `d1422d17-6d95-4ef1-96ab-8af31744dd63`, format GML, projeksjon 25833; svaret gir `downloadUrl` (zip 0,5–0,8 MB) (R D2 [2]; D1t «Access steps»).
- **Koordinatsystem:** GML/SOSI/FGDB kun i EPSG:25832/25833; WGS84 (4326) kun som GPX – format-navnet er `"GPX "` med etterfølgende mellomrom, ikke testet. En tidlig påstand om GML i 4326 ble motbevist (bestilling returnerte `files: []`) (R D2; D1t #1). Ellers omregning med proj4js/QGIS.
- **WFS-alternativ:** `https://wfs.geonorge.no/skwms1/wfs.turogfriluftsruter`, `typeNames=app:Fotrute`, bbox i 4326 – fungerte (WFS 2.0.0, standard-CRS 4258) (R D2 [3]; D1t #14). (D2 runde 1 fant ikke WFS i metadataene – senere bekreftet å virke.)
- **Datastruktur:** geometri per segment (1–6 `fotruteInfo` per segment); turer må settes sammen ved å gruppere på rutenummer/rutenavn og linemerge (D1t #4, «Leads»).
- **Produktspesifikasjon:** TurOgFriluftsruter 20171210 (versjon 6) (D1t #13).
- **OSM-uthenting:** Overpass API (~10 000 kall/dag, egen User-Agent, ingen parallelle kall, vent 30 s etter 429); Overpass turbo eksporterer GeoJSON; Waymarked Trails-GPX mangler ofte høyde og kan ha feil segmentrekkefølge (R D2 [8][27][28]; D2 #1–#4). Non-ASCII-regex (å) i Overpass fra Git Bash/curl ga 0 treff – kodingsproblem (D1o).
- **Høydemeter:** `GET https://ws.geonorge.no/hoydedata/v1/punkt?koordsys=4258&punkter=[[lon,lat],…]`, maks 50 punkter/kall (~6 kall for 300 punkter); sample hvert 10–25 m; terskel 2–10 m eller glatting (eksempel: 1 080 m reell stigning ble 1 434 m uten terskel) (R D2 [11][12]; D2 #9, #12).
- **Lengde:** `turf.length` (km), forutsetter WGS84 – beregn på 4326-data eller i UTM før omregning (R D2 [24]; D2 #14).
- **Lagring:** én statisk GeoJSON FeatureCollection med feltene `kilde`, `lisens`, `lengde_km`, `hoydemeter`, `gradering`, `estimert_tid`; PostGIS ikke nødvendig (uverifisert vurdering) (R D2, Anbefaling 5).
- **Manuell tegning** av manglende turer over eksisterende stier, f.eks. i geojson.io; evt. BRouter/GraphHopper (ikke undersøkt) (R Sammendrag; D1o «Bottom line»).
- **Pipeline:** beregn alt ved import, ikke ved kjøring (R Anbefaling 3).

## 6. Risikoer og åpne spørsmål

- **Manuelt kurateringsarbeid:** segmentbasert geometri og manglende ruter (Vettakollen ikke funnet under eget navn i noen kilde) gir betydelig manuelt arbeid for en del av turene (R Sammendrag).
- **Dekning i resten av Oslomarka** (Lillestrøm, Nittedal, Nordre Follo, Lunner) ikke målt – bestill fylke 32 (Akershus) (R Åpne spørsmål; D1t «Leads»).
- **Gradering-terskler** (≤5 km/≤300 hm) bygger på usikker kilde (søkesnippet, hjelp.ut.no ga 403) – bekreft i nettleser/Merkehåndboka (R Åpne spørsmål [23]).
- **Betydning av gradering I og S** uavklart (R Åpne spørsmål; D1t #12).
- **Høydemeter-terskel** for Marka-terreng ikke kalibrert – test på 2–3 turer med kjent profil (R Åpne spørsmål).
- **Tidsestimat for nybegynnere** kan være for optimistisk; påslaget er ikke forskningsbasert (R D4, Anbefaling 4).
- **ODbL §6.2-ordlyd** parafrasert av verktøy, ikke sitert – les originalen før lisensavsnitt skrives; Collective Database-tolkningen er ikke uttrykkelig avklart (R Åpne spørsmål, D3 [16]).
- **Turrutebasen-lisens:** metadata («No conditions apply») og vilkårsside (CC BY 4.0) spriker; vi følger CC BY 4.0 (R D3; D34a F5).
- **GPX i EPSG:4326** fra Geonorge ikke testet (R Åpne spørsmål).
- **API-stabilitet:** nedlastings- og høyde-API må re-sjekkes innen 2026-11-29; Overpass og OSM-fliser har ingen SLA (R Ferskhetskart; D2 #1; D34a F8).
- **ut.no-konklusjonen** bygger på fravær av bevis («foreldet» i ferskhetskartet) – sjekk før UT avskrives helt (R Ferskhetskart).
- **Datakvalitet** i Turrutebasen varierer (crowdsourcet) (D1t #15).
- **Vær** ikke undersøkt (se 2.5).

## 7. Anbefalinger (fra R, med mottaker og tillit)

| # | Anbefaling | Mottaker | Tillit |
|---|---|---|---|
| 1 | Turrutebasen som primærkilde for geometri og navn; OSM som reserve for enkeltturer | PRD (scope/datakilde), arkitektur | Høy |
| 2 | Kuratér 20–30 turer manuelt; sett vanskelighetsgrad etter fast regel (grønn ≤5 km/≤300 hm; blå ≤10 km/≤600 hm) | PRD (FR), epics | Middels |
| 3 | Høydemeter fra Kartverkets høyde-API med terskel/glatting; lengde med turf.js; beregn ved import | Arkitektur | Høy/middels |
| 4 | Tidsestimat: Naismith eller sveitsisk regel + nybegynnerpåslag + «pauser ikke inkludert» | PRD (forretningsregler) | Middels |
| 5 | Statisk GeoJSON med `kilde`, `lisens`, `lengde_km`, `hoydemeter`, `gradering`, `estimert_tid` | Arkitektur | Middels |
| 6 | Vis kreditering for Kartverket og OSM på kartet | Arkitektur, UX | Høy |
| 7 | Oppdater brief: «fra Kartverkets Turrutebasen (OSM som supplement)» | Brief/PRD | Høy |

Kilde: R Anbefalinger. I tillegg: kjør Refresh av researchen før byggestart hvis det er gått mer enn en måned (R Ferskhetskart).
