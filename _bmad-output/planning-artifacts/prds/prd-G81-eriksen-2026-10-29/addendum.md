---
title: "Addendum til PRD: Your Next Adventure"
created: 2026-11-06
updated: 2026-11-06
---

# Addendum til PRD: Your Next Adventure

Dette addendumet tar vare på begrunnelser og tekniske detaljer som hører hjemme i arkitektur og løsningsdesign, ikke i selve PRD-en.

## Input-form: vurderte alternativer (2026-11-06)

| Alternativ | Arbeid | Risiko | Vurdering |
|---|---|---|---|
| a) Bare skjema | Lite: bare regler og database | Lav | Avviker fra briefen («KI tolker vanlig språk»), så avviket må begrunnes. Produktet mister det som skiller det fra andre |
| b) Bare fritekst med KI | Mye: KI-integrasjon, prompt, sjekk av svaret, reserveløsning og testmodus | Høy: hele kjerneflyten avhenger av KI | Faglæreren har allerede advart om omfanget |
| **c) Skjema + valgfritt fritekstfelt (valgt)** | Middels | Lav: kjernen fungerer uten KI | Følger briefen, og KI-delen er avgrenset |

Begrunnelse for valget: Sensor har ikke vår API-nøkkel og kjører appen bare ved hjelp av README. Kjerneflyten må derfor fungere uten KI (sensorveiledningen s. 2 og 5). KI kan bare rangere blant turer som allerede har bestått reglene. Slik blir KI-svaret validert, og KI kan ikke finne på turer.

Mekanisme (til arkitekturen): Mangler nøkkelen, eller feiler eller tidsavbrytes KI-kallet, blir friteksten ignorert, og begrunnelsen lages fra en fast mal, for eksempel «Turen tar ca. 2 t og har utsikt, som du ba om».

## Lenke til ut.no

Lenken til ut.no lagres som en fast URL for hver tur i den kuraterte turdatabasen. Appen henter ingenting fra ut.no mens den kjører. Å lenke til en side er ikke det samme som å kopiere innholdet, så det oppstår ingen lisensspørsmål. Lenken er valgfri, og et forslag fungerer også uten den.

## Utsatt: personlig tidsestimat

Ideen er å bruke forholdet mellom faktisk og estimert tid, for eksempel snittet over minst tre turer, som en faktor på nye estimater. Det er teknisk enkelt, men det er én regel til som må testes og dokumenteres. Den er derfor flyttet til en senere fase fordi omfanget allerede er stort for én person (tilbakemeldingen fra faglærer). Faktisk tid logges likevel i v1.

## Formel for estimert tid (sveitsisk regel)

Formelen er hentet fra researchen (`research/technical-turdata-oslomarka-2026-10-29/digests/D3D4-lisens-tid-r1-1.md`, F10): 15 min per km, pluss 15 min per 100 høydemeter opp og 15 min per 200 høydemeter ned. Det tilsvarer omtrent 4 km/t på flat mark. Leddene summeres. Researchens eksempel bekrefter dette: 6 km med ±800 m gir 4,5 t. For tur-retur legges lengde, stigning og nedstigning for begge veier sammen.

Påslag for nybegynnere: +15 % på den beregnede tiden, valgt 2026-11-06. Formlene bommer med 13,5–15,5 % på hele turer og beskriver en «gjennomsnittlig» turgåer. Påslaget er ikke forskningsbasert, men en bevisst forsiktig margin.

## Graderingsregel

Kilder, sitater og forbehold står i `research-gradering.md`. Regelen er gjengitt i PRD FR-2.

## OpenStreetMap og ODbL

Turrutebasen er primærkilden. OSM-data er lisensiert under ODbL, og en database som kan hentes ut som GeoJSON, regnes trolig som en *avledet database*. Bruken av OSM holdes derfor uvesentlig: ett håndplukket engangsuttrekk med færre enn 100 objekter (OSMF-veiledning, researchen D3). Egne felt som lengde, høydemeter og gradering holdes adskilt fra OSM-geometrien (Collective Database, §4.5). Dette er en tolkning, ikke en juridisk vurdering. Turdatabasen tilbys ikke som en nedlastbar fil.

## MET: vilkår (verifisert 2026-11-06)

Kilder: api.met.no/doc/TermsOfService og api.met.no/doc/License.

- **Lisens:** NLOD 2.0 og CC BY 4.0. MET anbefaler krediteringen «Data from MET Norway», gjerne med lenke. Værsymbolene har MIT-lisens.
- **Identifikasjon:** En identifiserende User-Agent er påkrevd, med appnavn og kontaktinformasjon (e-post eller nettside). Falsk eller tilfeldig identifikasjon kan føre til permanent utestengelse.
- **Mellomlagring:** Samme forespørsel skal ikke sendes på nytt før tidspunktet i `Expires`, og `If-Modified-Since` skal brukes. Den samlede trafikken skal holdes under 20 forespørsler per sekund.
- **Koordinater:** Maks 4 desimaler. Nye produkter får 403 ved 5 desimaler eller flere.
- **Nettleser:** Nettlesere bør ikke kalle API-et direkte, men gå via en egen server (proxy). CORS-preflight støttes ikke. **Følge for arkitekturen:** Backend henter og mellomlagrer værdata for startpunktene.
- **Pris og driftsgaranti:** Ingen pris er oppgitt, og det finnes ingen SLA. Det støtter reserveløsningen i FR-10.

## Til arkitekturen: datauttrekk og beregning ved import

- **Ferskhet:** Kartverkets høyde-API (`ws.geonorge.no/hoydedata/v1/punkt`) svarte 200 med datakilde `dtm1` 2026-11-06. Turrutebasen finnes i Geonorge-katalogen (uuid d1422d17-6d95-4ef1-96ab-8af31744dd63). Selve nedlastingen må testes når turdatabasen bygges.
- **Koordinater:** GML finnes bare i UTM (25832/25833), mens WGS84 bare finnes som GPX. Konverteringen avgjøres i arkitekturen.
- **Høydedata:** API-et tar maks 50 punkter per kall. Sample hvert 10–25 m, og bruk en terskel på 2–10 m eller glatting. Uten filtrering kan stigningen bli 33 % for høy.
- **Lagring:** Statisk GeoJSON med feltene `kilde`, `lisens`, `lengde_km`, `hoydemeter`, `nedstigning`, `form`, `gradering` og `estimert_tid`. Verdiene beregnes ved import og ikke mens appen kjører.
- **Dekning:** Bare Oslo og Bærum er målt. Andre markakommuner krever en ny dekningssjekk.

## Om formelvarianter

Varianten «største av horisontal og vertikal tid + halvparten av den minste» er DIN 33466/DAV, ikke BFU. Offisielle sveitsiske skilttider bruker et helningspolynom. Prosjektet velger bevisst tommelfingerregelen med summering, fordi den er enkel å forklare og å teste.
