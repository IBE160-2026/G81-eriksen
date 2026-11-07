---
title: "Addendum til PRD: Your Next Adventure"
version: 1.1
created: 2026-11-06
updated: 2026-11-07
---

# Addendum til PRD: Your Next Adventure

Dette addendumet tar vare på begrunnelser og tekniske detaljer som hører hjemme i arkitektur og løsningsdesign, ikke i selve PRD-en.

Endret i v1.1: KI-begrunnelsen med plassholdere, validering og mal er ny, og høydeprofil og startpunkt er lagt til i turdataene (etter UX-arbeidet og gjennomgangen av v1.1).

## Input-form: vurderte alternativer (2026-11-06)

| Alternativ | Arbeid | Risiko | Vurdering |
|---|---|---|---|
| a) Bare skjema | Lite: bare regler og database | Lav | Avviker fra briefen («KI tolker vanlig språk»), så avviket må begrunnes. Produktet mister det som skiller det fra andre turapper |
| b) Bare fritekst med KI | Mye: KI-integrasjon, prompt, sjekk av svaret, reserveløsning og testmodus | Høy: hele kjerneflyten avhenger av KI | Faglæreren har allerede advart om omfanget |
| **c) Skjema + valgfritt fritekstfelt (valgt)** | Middels | Lav: kjernen fungerer uten KI | Følger briefen, og KI-delen er avgrenset |

Begrunnelse for valget: Sensor har ikke vår API-nøkkel og kjører appen bare ved hjelp av README. Kjerneflyten må derfor fungere uten KI (sensorveiledningen s. 2 og 5). KI kan bare rangere blant turer som allerede har bestått reglene. Slik blir KI-svaret validert, og KI kan ikke finne på turer.

## KI-begrunnelsen: plassholdere, validering og mal

KI skriver aldri tall eller turnivå (PRD FR-12).

Mekanisme:

- **Reservemalen (FR-13):** Hvis API-nøkkelen mangler, KI-kallet feiler eller tidsavbrytes, eller valideringen forkaster svaret, ignoreres friteksten. Begrunnelsen lages da fra reservemalen, for eksempel «Turen tar ca. 2 t og har utsikt, som du ba om».
- **Når KI svarer**, går begrunnelsen gjennom disse stegene:
  1. KI får beskjed om å bruke plassholdere der tall og nivå skal stå: `{tid}` (estimert tid), `{varighet}` (varigheten brukeren søkte på), `{lengde}` (total lengde) og `{nivå}` (turnivå).
  2. Valideringen (FR-13) sjekker KI-teksten. Har den sifre, tallord for tid eller lengde eller nivåord (grønn, blå, rød, svart) utenfor plassholderne, forkastes den, og reservemalen brukes.
  3. Systemet erstatter plassholderne med verdier fra turdatabasen (FR-2, FR-3) og søket i faste formater, for eksempel «ca. 1 t 35 min» og «grønn».
  4. Har en personaliseringsregel påvirket valget, legger systemet til personaliseringssetningen (FR-12) etter KI-teksten. Systemet lager den fra en fast setningsmal.
  5. Valideringen sjekker grensen på 300 tegn (FR-12, FR-13) på den ferdige teksten, slik brukeren ser den: etter innsetting og med personaliseringssetningen. Er teksten for lang, brukes reservemalen.

Eksempel: KI skriver «Turen tar {tid}, så den passer innenfor {varighet}. Den har utsikt, som du ba om, og er {nivå}, som passer når du er ny.» Brukeren ser «Turen tar ca. 1 t 35 min, så den passer innenfor 2 timer. Den har utsikt, som du ba om, og er grønn, som passer når du er ny.»

## Lenke til ut.no

Lenken til ut.no lagres som en fast URL for hver tur i den kuraterte turdatabasen. Appen henter ingenting fra ut.no mens den kjører. Å lenke til en side er ikke det samme som å kopiere innholdet, så det oppstår ingen lisensspørsmål. Lenken er valgfri, og et forslag fungerer også uten den.

## Formel for estimert tid (sveitsisk regel)

Formelen er hentet fra researchen (`research/technical-turdata-oslomarka-2026-10-29/digests/D3D4-lisens-tid-r1-1.md`, F10): 15 min per km, pluss 15 min per 100 høydemeter opp og 15 min per 200 høydemeter ned. Leddene summeres. 15 min per km tilsvarer omtrent 4 km/t på flat mark. Researchens eksempel bekrefter regelen: 6 km med 800 m opp og 800 m ned gir 4,5 t. For tur-retur legges lengde, stigning og nedstigning for begge veier sammen.

Påslag for nybegynnere: +15 % på den beregnede tiden, valgt 2026-11-06. Naismith og Tobler bommer i snitt med 13,5–15,5 % på hele turer og beskriver en «gjennomsnittlig» turgåer. Researchen oppgir ingen fast retning for dette avviket. Den slutter at formlene trolig undervurderer tiden for nybegynnere, men slutningen er ikke verifisert. Påslaget er ikke forskningsbasert, men en bevisst forsiktig margin.

### Om formelvarianter

Varianten «største av horisontal og vertikal tid + halvparten av den minste» er DIN 33466/DAV, ikke sveitsisk regel fra BFU. Offisielle sveitsiske skilttider bruker et helningspolynom. Prosjektet velger bevisst sveitsisk regel med summering, fordi den er enkel å forklare og å teste.

### Utsatt: personlig tidsestimat

Ideen er å bruke forholdet mellom faktisk og estimert tid, for eksempel snittet over minst tre turer, som en faktor på nye estimater. Det er teknisk enkelt, men det er én regel til som må testes og dokumenteres. Funksjonen er derfor utsatt til en senere fase, fordi omfanget allerede er stort for én person (tilbakemelding fra faglæreren). Faktisk tid logges likevel i v1.

## Graderingsregel

Kilder, sitater og forbehold står i `research-gradering.md`. Regelen er gjengitt i PRD FR-2.

## OpenStreetMap og ODbL

Turrutebasen er primærkilden. OSM-data er lisensiert under ODbL, og en database som kan hentes ut som GeoJSON, regnes trolig som en *avledet database*. Bruken av OSM holdes derfor «uvesentlig» i ODbL-forstand (*insubstantial*): ett håndplukket engangsuttrekk med færre enn 100 objekter (OSMF-veiledning, researchen D3). Egne felt som lengde, høydemeter og gradering holdes adskilt fra OSM-geometrien (Collective Database, §4.5). Dette er en tolkning, ikke en juridisk vurdering. Turdatabasen tilbys ikke som en nedlastbar fil.

## MET: vilkår (verifisert 2026-11-06)

Kilder: api.met.no/doc/TermsOfService og api.met.no/doc/License.

- **Lisens:** NLOD 2.0 og CC BY 4.0. MET anbefaler krediteringen «Data from MET Norway», gjerne med lenke. Værsymbolene har MIT-lisens.
- **Identifikasjon:** En identifiserende User-Agent er påkrevd, med appnavn og kontaktinformasjon (e-post eller nettside). Falsk eller tilfeldig identifikasjon kan føre til permanent utestengelse.
- **Mellomlagring:** Samme forespørsel skal ikke sendes på nytt før tidspunktet i `Expires`, og `If-Modified-Since` skal brukes. Den samlede trafikken skal holdes under 20 forespørsler per sekund.
- **Koordinater:** Maks 4 desimaler. Nye produkter får 403 ved 5 desimaler eller flere.
- **Nettleser:** Nettlesere bør ikke kalle API-et direkte, men gå via en egen server (proxy). CORS-preflight støttes ikke. **Følge for arkitekturen:** Backend henter og mellomlagrer værdata for startpunktene.
- **Pris og driftsgaranti:** Ingen pris er oppgitt, og det finnes ingen SLA. Dette begrunner reserveløsningen i FR-10.

## Til arkitekturen: datauttrekk og beregning ved import

- **Ferskhet:** Kartverkets høyde-API (`ws.geonorge.no/hoydedata/v1/punkt`) svarte 2026-11-06 med HTTP 200 og datakilde `dtm1`. Turrutebasen finnes i Geonorge-katalogen (uuid d1422d17-6d95-4ef1-96ab-8af31744dd63). Selve nedlastingen må testes når turdatabasen bygges.
- **Koordinater:** GML finnes bare i UTM (EPSG:25832/25833), mens WGS84 bare finnes som GPX. Konverteringen avgjøres i arkitekturen.
- **Høydedata:** API-et tar maks 50 punkter per kall. Hent høyden for et punkt hvert 10–25 m, og bruk en terskel på 2–10 m for høydeendringer som telles, eller glatting. Uten filtrering kan stigningen bli 33 % for høy. Høydeprofilen beregnes ved import fra de samme filtrerte punktene som høydemeterne, og lagres som en forenklet serie med avstand og høyde.
- **Lagring:** Statisk GeoJSON med feltene `kilde`, `lisens`, `lengde_km`, `hoydemeter`, `nedstigning`, `hoydeprofil`, `startpunkt` (navn), `form`, `gradering` og `estimert_tid`. Verdiene beregnes ved import og ikke mens appen kjører. Turdatabasen trenger ikke utsiktspunkter eller en skrevet rutebeskrivelse.
- **Bruk i visningen (PRD FR-6, UJ-1, `EXPERIENCE.md`):** Høydeprofilen brukes i turillustrasjonen og i «Kartet i tekst», som viser laveste og høyeste punkt. Startpunktets navn vises som «Start: …».
- **Dekning:** Dekningen er bare sjekket for Oslo og Bærum. Andre markakommuner krever en ny dekningssjekk.
