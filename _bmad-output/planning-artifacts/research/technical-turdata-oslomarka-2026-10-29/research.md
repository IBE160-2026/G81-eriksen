---
title: 'technical research: Turdata for Oslomarka'
type: 'technical'
topic: 'Turdata for Oslomarka'
decision: 'Kan vi bygge en kuratert database med 20–30 nybegynnerturer i Oslomarka (rutelinje, lengde, høydemeter) fra åpne data – og hvilken kilde og fremgangsmåte bør vi velge?'
source: 'native run'
status: complete
preset: 'standard'
validation: 'normal'
shape: 'select'
created: '2026-10-29'
updated: '2026-10-29'
claims_verified: 3
claims_unverified: 4
claims_overturned: 1
---

# Teknisk research: Turdata for Oslomarka

**Beslutningen denne researchen skal støtte:** Kan vi bygge en kuratert database med 20–30 nybegynnerturer i Oslomarka (rutelinje, lengde, høydemeter) fra åpne data – og hvilken kilde og fremgangsmåte bør vi velge?

## Sammendrag

**Ja, det er gjennomførbart – men ingen åpen kilde leverer «nybegynnerturer» ferdig. Kurateringen må gruppen gjøre selv.** Anbefalt løsning:

1. **Kartverkets Turrutebasen som kilde for rutelinjer og navn.** Den er åpen (CC BY 4.0), oppdatert ukentlig (sist 2026-10-23), og kan lastes ned for Oslo og Bærum uten innlogging [1][2][13]. Den vant beslutningsmatrisen (3,65 mot 2,9 for OSM).
2. **Kartverkets høyde-API for høydemeter.** Gratis, uten nøkkel, 1 m terrengmodell, maks 50 punkter per kall [11].
3. **Egen, regelbasert vanskelighetsgrad og tidsestimat.** Turrutebasen har gradering på bare 11,7 % av fotrute-segmentene i Oslo, og de store DNT-rutene i Nordmarka og Østmarka er ugraderte [2]. OSM har ingen vanskelighetsgrad på turrelasjonene [6]. Gruppen må derfor sette vanskelighetsgrad selv, f.eks. etter UT/DNTs tommelfingerregel for grønn tur (≤5 km, ≤300 høydemeter – lav tillit) [23].

**Tre funn bærer anbefalingen:** (a) Turrutebasen er den eneste kilden som er både åpen, fersk og lett å hente ut; (b) ingen kilde har brukbar vanskelighetsgrad for Oslomarka; (c) ut.no har ikke lenger noe åpent API [10].

**Største forbehold:** Turrutebasen lagrer geometri per *segment*, ikke per tur. En tur må settes sammen av segmenter, og flere populære nybegynnerturer finnes ikke som egne ruter i OSM [6]. Turrutebasen har derimot ruter til Kolsås (Bærum) og Ullevålseter (f.eks. «Sognsvann – Blanksjø – Ullevålseter») [2], mens Vettakollen ikke ble funnet under eget navn i noen av kildene. Regn med manuelt arbeid – f.eks. å tegne turen over eksisterende stier i et verktøy som geojson.io – for en del av de 20–30 turene.

## D1 – Datakilder og dekning

**Kandidater:** Turrutebasen (Kartverket), OpenStreetMap, ut.no/DNT. Øvrige kilder (Oslo kommune, Skiforeningen) ble vurdert og forkastet: Oslo kommunes data dekker bynære turveier, ikke Marka, og Skiforeningens data gjelder vinterløyper og er ikke åpne (lav–middels tillit).

**Turrutebasen (målt i Oslo og Bærum, 2026-10-29) [2]:**

| Måling | Oslo (0301) | Bærum (3201) |
|---|---|---|
| Fotrute-segmenter | 3 254 (711,9 km) | 1 864 (376,7 km) |
| Segmenter med gradering G/B/R/S | 11,7 % (ingen R/S) | 14,5 % |
| Merking = JA | 97,1 % | 100 % |
| Ruter (gruppert på nummer + navn) | 186, hvorav 41 heter «Ukjent» | 59, hvorav 29 «Ukjent» |
| Rutelengde | median 1,3 km, p90 7,5 km | – |

- Graderte ruter er mest bynære turveier langs elver. Hovedrutene til DNT er ugraderte [2].
- `merking` skiller ikke rutene, siden nesten alle er merket. `rutetype` er en kode for skiløyper, ikke turtype. `underlagstype` finnes i skjemaet, men har ingen verdier i Oslo og Bærum [2][4].
- **Nyttig felt:** `ruteFølger` (ST = sti, BV = bilvei, GS = gang-/sykkelvei osv.) sier noe om underlaget og kan brukes som en indikator på vanskelighetsgrad [2][4].
- Eksempler på navngitte ruter: Sognsvann Brekke turvei (2,3 km, G), Rundtur Ulsrudvann (1,7 km, G), Brennarunden (4,5 km), Frognerseteren–Studenterhytta (6,9 km) [2].
- 64–76 % av segmentene kommer fra Kartverkets FKB-stidata. Resten er digitalisert fra turkart og meldt inn av lag og foreninger. Dette er målt i Valdres og Gudbrandsdalen, ikke i Oslo [5] (lav tillit for Oslomarka).

**OpenStreetMap (målt i boksen 59,85–60,20 N / 10,40–11,05 Ø, 2026-10-29) [6]:**
- 307 relasjoner for fotturer (`route=hiking`/`foot`). 158 av dem er DNT-segmenter (OSL1–OSL217) **uten navn**. Ingen relasjon har vanskelighetsgrad eller tidsbruk. Bare 8 har oppgitt lengde.
- Rundt 20–25 navngitte relasjoner kan passe for nybegynnere (Sognsvann natursti, Bogstadvannet rundt, Ulsrudvann rundt, Losbyrunden lille). At de passer for nybegynnere, er en vurdering, ikke målt.
- 76 189 sti-/vei-segmenter. `sac_scale` er satt på 1,2 %, `trail_visibility` på 10,8 %.
- 3 av 4 klassiske nybegynnerturer (Vettakollen, Kolsåstoppen, Ullevålseter) finnes bare som stier og punkter, ikke som ruter.
- Stinettet er tett og godt skiltet (2 897 veivisere) – OSM er et godt *kart*, men ikke en ferdig *turliste* [6][7].
- OSM-wikiens egen side om Oslomarka er fra 2018 og nevner ikke turrelasjoner eller vanskelighetstagger, så den kan ikke brukes som dokumentasjon på dekning i dag [9].

**ut.no / DNT:** Nasjonal Turbase-API-et ser ut til å ha vært ute av drift siden ca. 2020. GitHub-organisasjonen ble sist oppdatert i mars 2020, og nasjonalturbase.no avviste tilkobling 2026-10-29 [10]. Dette bygger på fravær av bevis (ingen offisiell nedleggelse funnet), så tilliten er middels. Turbeskrivelser fra ut.no kan brukes som inspirasjon ved kurateringen, ikke som datakilde.

## D2 – Uthenting, format og høydemeter

- **Turrutebasen** [2][3]:
  - Bestilles via `POST https://nedlasting.geonorge.no/api/order` (kommune 0301/3201). Lenken til filen kommer i svaret.
  - GML finnes **kun i EPSG:25832/25833** (UTM). WGS84 (EPSG:4326, det Leaflet bruker) finnes bare som GPX – ikke testet.
  - Alternativ: WFS `https://wfs.geonorge.no/skwms1/wfs.turogfriluftsruter` med `typeNames=app:Fotrute` og bbox i 4326 – fungerte i testen.
  - *Rettelse:* en tidlig påstand (D2 runde 1) om at GML kunne lastes ned i 4326, ble motbevist ved faktisk bestilling.
- **OSM** [8]:
  - Overpass API holder godt for ~30 turer (grense ca. 10 000 kall/dag). Send egen User-Agent og ikke kjør parallelle kall.
  - Overpass turbo eksporterer GeoJSON [27].
  - GPX fra Waymarked Trails mangler ofte høydedata og kan ha segmenter i feil rekkefølge [28] (middels tillit; bygger delvis på forumposter fra 2013–2020).
- **Høydemeter** [11]:
  - API: `GET https://ws.geonorge.no/hoydedata/v1/punkt?koordsys=4258&punkter=[[lon,lat],…]` – maks 50 punkter per kall.
  - Bekreftet med eget kall: punkt i Nordmarka → 461,87 moh, datakilde `dtm1` (terreng: skog).
  - Ubehandlet høydedata gir for mye stigning. Et eksempel fra GPS Visualizer: 1 080 m reell stigning ble 1 434 m fra terrengmodell uten terskel [12]. Bruk en terskel (2–10 m) eller glatting, og kontroller mot publiserte høydeprofiler (middels tillit).
- **Lengde og lagring:**
  - Lengde kan beregnes med `turf.length` (km som standard) [24].
  - For 20–30 statiske turer holder én GeoJSON-FeatureCollection med ferdigberegnede egenskaper. PostGIS er ikke nødvendig – dette er en uverifisert vurdering, ingen kilde sammenligner direkte.

## D3 – Lisens og vilkår

| Kilde | Lisens | Krav for vår bruk |
|---|---|---|
| Turrutebasen / Kartverket | CC BY 4.0 [13] | Kreditering «© Kartverket», helst med lenke. Metadataene sier bare «No conditions apply» [1] – vilkårssiden er mer presis og nyere, så vi følger den. |
| OSM-data | ODbL 1.0 [14] | En offentlig nettside er «Publicly Use» → en *avledet database* utløser deling på samme vilkår (§4.4) og krav om å tilby hele databasen (§4.6). **Men:** uvesentlige uttrekk kan brukes fritt (§6.2), og OSMF regner <100 objekter, hentet ut én gang og håndplukket, som uvesentlig [15]. Egne felt (lengde, høydemeter, vanskelighetsgrad fra ikke-OSM-kilder) kan trolig holdes adskilt [16] – en tolkning, ikke uttrykkelig avklart. |
| OSM-kartfliser | OSMF tile policy [18] | Synlig kreditering, gyldig Referer/User-Agent, ingen masse-nedlasting. Ingen tallgrenser og ingen oppetidsgaranti. Leaflet med standard kreditering oppfyller kravene. |
| Kartverkets topografiske kart (WMTS) | CC BY 4.0 [26] (middels tillit) | «© Kartverket». Bruk ut over «normal bruk» av detaljerte kartdata (zoom 12–20, Geovekst) krever tillatelse [13]. Kontroller gjeldende adresse før bruk. |

Kreditering for OSM: «© OpenStreetMap contributors» med lenke til openstreetmap.org/copyright, synlig på kartet [17].

## D4 – Tidsestimat

| Formel | Regel | Kommentar |
|---|---|---|
| Naismith (1892) | 5 km/t + 1 t per 600 høydemeter [19] | Klassikeren. Gir rimelig total tid for erfarne turgåere [19] |
| Tobler (1993) | v = 6·e^(−3,5·\|S+0,05\|) km/t [25][19] | Hastighet som funksjon av helning. Krever høydeprofil |
| Sveitsisk BFU-regel | 15 min/km + 15 min per 100 m opp + 15 min per 200 m ned [21] | Mer forsiktig (ca. 4 km/t) – bedre for nybegynnere (middels tillit) |
| DNT fellesturer | ca. 3 km/t [22] | Referanse for gruppetempo (lav–middels tillit, kun snippet) |

- Den største studien (7 636 GPS-spor) fant at både Naismith og Tobler bommer med **13,5–15,5 %** på hele turer, og at de beskriver en «gjennomsnittlig» turgåer [20].
- Ingen studie isolerer nybegynnere. Begge studiene bygger på GPS-spor lastet opp av sporty turgåere, så formlene **undervurderer trolig tiden for nybegynnere**. Dette er en uverifisert slutning.
- Alle formlene er rene funksjoner av lengde og stigning, og passer derfor kravet om at KI ikke skal gjette tid.

## Beslutningsmatrise

Krav (fra brief og faglærers tilbakemelding). **Absolutte krav:** gratis, lovlig i et studentprosjekt, rutegeometri for Oslomarka, kan hentes ut uten betalt nøkkel. ut.no strykes fordi det ikke har noe åpent API.

| Kriterium (vekt) | Turrutebasen | OSM |
|---|---|---|
| Datakvalitet og aktualitet (30 %) | 4 – offisiell, ukentlig oppdatert, delvis navngitt | 4 – tettest stinett, men turene mangler navn |
| Enkel uthenting (25 %) | 4 – API/WFS virker, men koordinatsystem (UTM) og segmenter krever arbeid | 3 – Overpass virker, men turer må settes sammen eller tegnes selv |
| Nybegynner-felt (20 %) | 2 – gradering på 11,7 % | 1 – ingen |
| Enkel lisens (15 %) | 5 – CC BY | 3 – ODbL, ok under 100 objekter |
| Høydedata (10 %) | 3 – via eget API | 3 – via eget API |
| **Vektet sum** | **3,65** | **2,90** |

**Valg:** Turrutebasen. **Andrevalg:** OSM, for turer som mangler i Turrutebasen (f.eks. Vettakollen, som ikke ble funnet under eget navn [2]). Da tegner gruppen ruten over OSM-stier, holder seg under 100 objekter i ett engangsuttrekk, og krediterer OSM. **Sterkeste motargument:** begge kildene krever like mye manuell kurering, så kildevalget betyr mindre enn kurateringsprosessen. **Billigste sikring:** lagre `kilde` og `lisens` per tur i databasen. Da kan enkeltturer byttes ut uten at resten påvirkes.

## Innsikt på tvers av dimensjonene

- **Nybegynnerverdien ligger i kurateringen, ikke i kilden.** Ingen kilde har vanskelighetsgrad som fungerer i Oslomarka (D1). Høydemeter og lengde kan beregnes pålitelig (D2), og tidsformler er deterministiske (D4). Gruppens regelbaserte vanskelighetsgrad blir derfor både *nødvendig* og et *fortrinn* – og den passer kravet om at KI bare velger blant kjente turer.
- **Lisens styrer arkitekturen.** Kartverket-data (CC BY) kan fritt kombineres med egne felt. OSM-data bør holdes til et lite engangsuttrekk med tydelig kildefelt (D3). Det taler for én statisk GeoJSON med `kilde` per tur, fremfor å hente OSM-data løpende.

## Anbefalinger

| # | Anbefaling | Mottaker | Tillit |
|---|---|---|---|
| 1 | Bruk Turrutebasen som primærkilde for geometri og navn; OSM som reserve for enkeltturer | PRD (scope/datakilde), arkitektur | Høy – bygger på målte data |
| 2 | Kuratér 20–30 turer manuelt: sett sammen segmenter, gi dem navn, og sett vanskelighetsgrad etter en fast regel (forslag: grønn ≤5 km og ≤300 hm; blå ≤10 km og ≤600 hm) | PRD (funksjonelle krav), epics | Middels – terskelverdiene bygger på en usikker kilde [23] |
| 3 | Beregn høydemeter fra Kartverkets høyde-API med terskel/glatting; lengde med turf.js. Beregn ved import, ikke ved kjøring | Arkitektur | Høy (API), middels (terskelverdi) |
| 4 | Tidsestimat: start med Naismith eller den sveitsiske regelen, legg til et påslag for nybegynnere, og vis «pauser ikke inkludert» | PRD (forretningsregler) | Middels – påslaget er ikke forskningsbasert |
| 5 | Lagre turene som statisk GeoJSON med feltene `kilde`, `lisens`, `lengde_km`, `hoydemeter`, `gradering`, `estimert_tid` | Arkitektur | Middels |
| 6 | Vis kreditering for Kartverket og OSM på kartet | Arkitektur, UX | Høy |
| 7 | Oppdater briefen: «rutelinjer hentet fra OpenStreetMap» bør bli «fra Kartverkets Turrutebasen (OSM som supplement)» | Brief / PRD | Høy |

## Åpne spørsmål

- **Dekning i resten av Oslomarka** (Lillestrøm, Nittedal, Nordre Follo, Lunner): ikke målt. Bestill fylke 32 (Akershus) på samme måte for å sjekke.
- **GPX i EPSG:4326** fra Geonorge: ikke testet. Ellers må UTM regnes om, f.eks. med proj4js eller QGIS.
- **Betydning av gradering I og S:** ikke funnet i skjemaet. Trolig «ikke gradert» og «svart». Sjekk Merkehåndboka.
- **UT/DNTs regel for gradering og tid:** hjelpesidene på hjelp.ut.no returnerte 403. Åpne dem i nettleser for å bekrefte grensene ≤5 km / ≤300 hm.
- **Riktig terskel for høydemeter i Marka-terreng:** test på 2–3 turer med kjent høydeprofil.
- **ODbL §6.2-ordlyd:** ble parafrasert av verktøyet, ikke sitert direkte. Les originalteksten før dere skriver lisensavsnittet.

## Kilder

| # | Støtter | Utgiver | Publisert | Lest | Tillit |
|---|---|---|---|---|---|
| [1] | Turrutebasen-metadata: åpne data, formater, ukentlig oppdatering | [Geonorge / Kartverket](https://kartkatalog.geonorge.no/api/getdata/d1422d17-6d95-4ef1-96ab-8af31744dd63) | 2026-10-23 | 2026-10-29 | høy |
| [2] | Egen måling av Turrutebasen Oslo/Bærum via nedlastings-API | [Kartverket (Geonorge nedlasting)](https://nedlasting.geonorge.no/api/codelists/area/d1422d17-6d95-4ef1-96ab-8af31744dd63) | data 2026-10-23 / 2026-09-13 | 2026-10-29 | høy |
| [3] | WFS for Turrutebasen | [Kartverket](https://wfs.geonorge.no/skwms1/wfs.turogfriluftsruter) | – | 2026-10-29 | høy |
| [4] | Kodelister (gradering, rutetype, ruteFølger) | [Kartverket SOSI-skjema 20171210](https://skjema.geonorge.no/SOSI/produktspesifikasjon/TurOgFriluftsruter/20171210/turogfriluftsruter.xsd) | 2018-01 | 2026-10-29 | høy |
| [5] | Opphav til Turrutebasen-geometri, import-status i OSM | [OSM-wiki No:Turrutebasen](https://wiki.openstreetmap.org/wiki/No:Turrutebasen) | 2026-08-25 | 2026-10-29 | middels |
| [6] | Egen måling av OSM-relasjoner og tagger i Oslomarka | [Overpass API / OSM-bidragsytere](https://overpass-api.de/api/interpreter) | data 2026-10-29 | 2026-10-29 | høy |
| [7] | Waymarked Trails: nesten bare unavngitte DNT-segmenter (48 av 50) | [Waymarked Trails](https://hiking.waymarkedtrails.org/) | – | 2026-10-29 | middels |
| [8] | Overpass bruksgrenser og formater | [OSM-wiki Overpass API](https://wiki.openstreetmap.org/wiki/Overpass_API) | 2026-10-24 | 2026-10-29 | høy |
| [9] | Eldre beskrivelse av Oslomarka i OSM | [OSM-wiki No:Oslomarka](https://wiki.openstreetmap.org/wiki/No:Oslomarka) | 2018-04-06 | 2026-10-29 | lav |
| [10] | Nasjonal Turbase inaktiv | [GitHub Turbasen](https://github.com/Turbasen) | 2020-03-27 | 2026-10-29 | middels |
| [11] | Høyde-API (punkt, 50 punkter, dtm1) – verifisert med eget kall | [Kartverket](https://ws.geonorge.no/hoydedata/v1/openapi.json) | 2026 | 2026-10-29 | høy |
| [12] | Støy gir for mye stigning; terskel | [GPS Visualizer](https://gpsvisualizer.com/tutorials/elevation_gain.php) | udatert | 2026-10-29 | middels |
| [13] | Kartverket CC BY 4.0, «© Kartverket» – verifisert | [Kartverket – vilkår for bruk](https://www.kartverket.no/api-og-data/vilkar-for-bruk) | 2026-07-21 | 2026-10-29 | høy |
| [14] | ODbL §4.4, §4.5, §4.6, §6.2, «Publicly» | [Open Data Commons – ODbL 1.0](https://opendatacommons.org/licenses/odbl/1-0/) | 2009 | 2026-10-29 | høy |
| [15] | <100 objekter = uvesentlig uttrekk | [OSMF Substantial Guideline](https://osmfoundation.org/wiki/Licence/Community_Guidelines/Substantial_-_Guideline) | 2014-06-06 | 2026-10-29 | høy |
| [16] | Egne felt som Collective Database | [OSMF Collective Database Guideline](https://osmfoundation.org/wiki/Licence/Community_Guidelines/Collective_Database_Guideline_Guideline) | 2016-06-17 | 2026-10-29 | middels |
| [17] | Krav til OSM-kreditering | [OSMF Attribution Guidelines](https://osmfoundation.org/wiki/Licence/Attribution_Guidelines) | 2026-09-10 | 2026-10-29 | høy |
| [18] | Bruksvilkår for OSM-kartfliser | [OSMF Operations](https://operations.osmfoundation.org/policies/tiles/) | udatert | 2026-10-29 | høy |
| [19] | Naismith-formel; sammenligning med Langmuir og Tobler | [Pharoah, bioRxiv](https://www.biorxiv.org/content/10.1101/188417v2.full) | 2017-09-14 | 2026-10-29 | middels |
| [20] | Formlene bommer 13,5–15,5 % på hele turer | [Wood et al., arXiv](https://arxiv.org/abs/2303.16065) | 2023 | 2026-10-29 | middels |
| [21] | Sveitsisk tommelfingerregel | [BFU / Schweizer Wanderwege](https://www.srf.ch/static/radio/modules/data/attachments/3.010_PB_Bergwandern_de.pdf) | udatert | 2026-10-29 | middels |
| [22] | DNT ca. 3 km/t på fellesturer | [DNT](https://www.dnt.no/contentassets/eb277e829991484c8d212f6127df351c/graderingen-av-fellesturer.pdf) | udatert | 2026-10-29 | lav |
| [23] | UT: gradering følger nasjonale standarder; grenseverdiene ≤5 km / ≤300 hm kommer fra et søkesnippet fra en annen, ikke identifisert UT-artikkel (kilde-URL usikker) | [UT.no hjelp](https://hjelp.ut.no/hc/no/articles/15697246353938-Sjekklister-for-kvalitetssjekk-av-innhold) | udatert | 2026-10-29 | lav |
| [24] | turf.length | [Turf.js](https://turfjs.org/docs/api/length) | v7.4.0 | 2026-10-29 | middels |
| [25] | Toblers originalreferanse | [Tobler, NCGIA TR 93-1](https://escholarship.org/uc/item/05r820mz) | 1993-02 | 2026-10-29 | høy |
| [26] | Kartverkets topografiske WMTS er CC BY 4.0 | [data.norge.no](https://data.norge.no/en/data-services/e3454491-066a-3276-a482-f63069728021) | ca. 2026-03 | 2026-10-29 | middels |
| [27] | Overpass turbo-eksport (GeoJSON, GPX) | [OSM-wiki Overpass turbo](https://wiki.openstreetmap.org/wiki/Overpass_turbo) | 2026-10-25 | 2026-10-29 | høy |
| [28] | Waymarked Trails-GPX uten høyde / feil rekkefølge | [OSM-wiki Waymarked Trails](https://wiki.openstreetmap.org/wiki/Waymarked_Trails) | eldre (2013–2020) | 2026-10-29 | middels |

## Ferskhetskart

Beregnet med `recon_kit.py staleness`. Vinduer: API-status 1 mnd, datakvalitet 6 mnd, lisens 12 mnd, bruksvilkår 6 mnd, formler 24 mnd.

| Påstand | Klasse | Kildedato | Sjekk igjen |
|---|---|---|---|
| Nedlastings-API for Turrutebasen virker | api-status | 2026-10-29 | **2026-11-29** |
| Høyde-API gratis, 50 punkter/kall | api-status | 2026-10-29 | **2026-11-29** |
| Gradering 11,7 % i Oslo | datakvalitet | 2026-10-23 | 2027-04-23 |
| OSM-relasjoner uten vanskelighetsgrad | datakvalitet | 2026-10-29 | 2027-04-29 |
| Bruksvilkår for OSM-kartfliser | bruksvilkår | 2026-10-29 | 2027-04-29 |
| Kartverket CC BY 4.0 | lisens | 2026-07-21 | 2027-07-21 |
| ut.no har ikke åpent API | api-status | 2020-03-27 | **foreldet** – bygger på fravær av bevis; sjekk før dere avskriver UT helt |
| OSMF-retningslinje om <100 objekter | lisens | 2014-06-06 | **foreldet etter vinduet**, men retningslinjen er fortsatt gjeldende; lest 2026-10-29 |
| Naismith/Tobler-feil 13,5–15,5 % | formel | 2023-03-28 | **foreldet etter vinduet**; formler endrer seg sjelden |

Tidligste reelle ny-sjekk: **2026-11-29** (API-status). Kjør Refresh før byggestart hvis det er gått mer enn en måned.
