---
title: Avstemming av arkitekturspinen mot kildene
reviewed: ARCHITECTURE-SPINE.md (updated 2026-11-08)
against: prd.md v1.3, addendum.md v1.1, EXPERIENCE.md, DESIGN.md, extract-sensorveiledning.md, .memlog.md
date: 2026-11-08
---

# Avstemming: hva landet ikke i spinen

## Konklusjon

**Må rettes før spinen settes til ADOPTED.** Strukturen er god: lagdelingen, turdatabasen, MET-proxyen, KI-grensesnittet og de fleste UX-punktene som var adressert til arkitekturen (flis-kilde, nettlesere, øktlengde, turnavn, UTM) er lukket og sporbare til memloggen. Tre funn er likevel motstrid mot kildene som vil gi feil kode hvis en agent bygger rett etter spinen:

1. Sekvensdiagrammet kaller KI bare når det finnes fritekst, mens FR-12 og UJ-1 krever KI-begrunnelse også uten fritekst.
2. AD-1 forbyr JavaScript utenfor kartet. Memloggen tillot små progressive forbedringer, og EXPERIENCE.md krever flere av dem.
3. «Økt» i FR-7 (slutter når fanen lukkes, gjelder én fane) lar seg ikke oppfylle med en delt Django-session som lever i to uker (AD-5 + AD-6). Spinen sier ikke hvordan avviket håndteres.

Resten er stille krav som spinen lar være ustyrt: kreditering, ODbL, MET-identifikasjon, dobbel innsending, README-innhold, testbruker, personvern og Djangos standardtekster.

Alvorlighet: **Høy** = motstrid som gir feil oppførsel. **Middels** = krav uten styring som sannsynligvis blir gjort feil eller ulikt. **Lav** = presisering eller ryddepunkt.

---

## Høy

### H1. KI kalles bare ved fritekst, men FR-12 krever KI-begrunnelse uten fritekst

- **Kilde:** PRD FR-12 («Når KI er tilgjengelig, skriver KI begrunnelsen»), UJ-1 (Ola hopper over fritekst og får «✦ Skrevet med KI»), EXPERIENCE › KI-merke, memlog linje 29.
- **Spinen:** Sekvensdiagrammet, `V->>K: fritekst + treff (bare hvis fritekst og nøkkel)`. AD-10 sier ikke når KI kalles eller hvor mange kall et forslag gir.
- **Hull i tillegg:**
  - FR-11 (tolking: hvilke treff passer ønsket) skjer **før** rangeringen. Begrunnelsen gjelder turen som vinner **etter** rangeringen. Ett kall kan ikke gjøre begge deler uten at begrunnelser for alle treff skrives på forhånd.
  - «Nytt forslag» (FR-7) gir en ny tur, som trenger en ny begrunnelse. Spinen sier ikke om KI kalles igjen.
  - Verste ventetid er ikke beskrevet. To KI-kall og ett MET-kall, med 5 s tidsgrense hver, kan gi 15 s.
- **Fiks:** Skriv i AD-10 en egen regel for når KI kalles:
  - Kall A, tolking: én gang per søk, bare med fritekst og nøkkel. Svaret er ID-er og lagres i økten.
  - Kall B, begrunnelse: én gang per vist forslag når nøkkel finnes, også uten fritekst og også ved «Nytt forslag». Svaret lagres i økten, så reload ikke gir nytt kall.
  - Turforslag fra historikken kaller aldri KI (FR-17).
  - Rett sekvensdiagrammet. Ta med hvor lang den samlede ventetiden høyst kan bli, og bind den til Lasteindikator (se H2).

### H2. «JavaScript bare i kartmodulen» er i strid med memloggen og EXPERIENCE.md

- **Kilde:** Memlog linje 20: «JavaScript kun for kart (og evt. små progressive forbedringer)». EXPERIENCE krever:
  - «Nytt forslag» bytter innholdet på stedet uten å laste siden på nytt, setter `document.title`, flytter fokus til `h1` og bruker `aria-busy` og en live-region (Interaction Primitives og Accessibility Floor › Sidetitler og fokus)
  - Lasteindikator med søkeoppsummering med en gang (PRD §6 «laster»)
  - Primærknapp med `aria-disabled` som ignorerer nye klikk (NFR-2)
  - teller for fritekst med `aria-live` (`{n} / 200 tegn`)
  - bryteren «Vis passord»
  - «Prøv igjen» når kartflisene feiler
- **Spinen:** AD-1 sier «JavaScript brukes bare i kartmodulen (AD-8)». Sekvensdiagrammet viser POST → redirect → GET, altså en ny side for hvert søk og «Nytt forslag». Da kan ingen lastetilstand vises: brukeren ser en tom side mens KI og MET svarer (opptil 10–15 s, se H1).
- **Fiks:** Velg ett av to og skriv det i memloggen:
  - (a) Gjenopprett unntaket fra memloggen i AD-1. Tillat én liten fil `static/forbedring.js` uten rammeverk. Den skal bare gjøre progressiv forbedring: knappesperre, teller, «Vis passord», lastetekst før innsending og fokus og tittel etter at siden er lastet. Siden skal virke uten den. «Nytt forslag» kan da være en vanlig POST/redirect, der fokus settes på `h1` når siden lastes. Det ligger nær EXPERIENCE, men er ikke «på stedet».
  - (b) Behold forbudet, og før avvikene inn i EXPERIENCE.md (Nytt forslag gir ny side, lastetilstanden er nettleserens egen, ingen teller i sanntid).
  - Anbefalt: (a). Den følger memloggen og WCAG-flyten i UX uten et JSON-API.

### H3. Økten ender ikke når fanen lukkes, og alle faner deler den

- **Kilde:** PRD §3 Økt («til et nytt søk sendes eller fanen lukkes»), FR-7 og EXPERIENCE › State Patterns «Fanen er lukket, eller adressen er åpnet direkte → Det finnes ikke noe forslag». UJ-2 sier i tillegg at Ola har søkt «i andre faner».
- **Spinen:** AD-5 legger søket i Djangos session. AD-6 gir den samme cookien 2 ukers levetid. Følgene:
  - Lukker brukeren fanen og åpner adressen igjen, vises forslaget i inntil to uker. Tilstanden «Forslaget finnes ikke lenger» oppstår bare etter utlogging eller sletting.
  - Alle faner deler én økt. Et søk i fane B erstatter forslaget i fane A. Da kan «Registrer gjennomført tur» i fane A (UJ-2 steg 1) registrere feil tur hvis lenken leser turen fra økten.
- **Fiks:**
  1. Lenken «Registrer gjennomført tur» bærer alltid tur-ID-en (`/registrer/<tur-id>/`) og leser aldri «gjeldende forslag» fra økten. Det løser UJ-2 og FR-14 (gjest → innlogging → rett inn i registreringen via `next`).
  2. Bestem hvordan «fanen lukkes» skal oppfylles, og skriv det inn i AD-5. Enten:
     - en tilfeldig nøkkel per søk i URL-en (`/turforslag/<søk-id>/`) som bare finnes i den innloggede eller anonyme økten, så flere faner har hver sin økt og lenken ikke kan deles, eller
     - et akseptert avvik (økten varer til nytt søk, utlogging eller utløp), ført i PRD §9 og EXPERIENCE. Sensor sjekker at dokumentene stemmer med koden (sensorveiledningen s. 2 og 6).

---

## Middels

### M1. Dobbel innsending av registrering gir to registreringer og kan heve nivået

- **Kilde:** NFR-2 (dobbel innsending), EXPERIENCE UJ-2 feilvei («Han dobbeltklikker … Det blir bare én registrering»), FR-19 (hver registrering teller).
- **Spinen:** Bare PRG og CSRF. PRG hindrer ikke to POST-er som er på vei samtidig, og knappesperren i JS mangler (H2). To like registreringer teller dobbelt mot nivåhevingen, og dermed mot SM-C1.
- **Fiks:** Legg til i konvensjonen Skjema og validering: «POST som oppretter noe (registrering, konto) har et engangstoken i skjemaet som lagres i økten og brukes opp ved første innsending. En ny POST med samme token gir redirect til resultatet, uten ny rad.» Skriv en test for det (SM-2).

### M2. Kreditering (NFR-7) er bare halvveis styrt

- **Kilde:** NFR-7 (minst «© Kartverket», «© OpenStreetMap contributors» med lenke og «Data fra MET Norge»), FR-6, EXPERIENCE › Kreditering (alltid synlig på kartet, tre lenker, `lang="en"` på OSM-teksten), addendum (MET anbefaler lenke), FR-1 (kilde og lisens per tur).
- **Spinen:** AD-8 nevner bare «© Kartverket». AD-9 sier ingenting om kreditering, selv om kapabilitetskartet viser NFR-7 → AD-9. Feltene `kilde` og `lisens` lagres, men ingen regel sier hvor de brukes.
- **Fiks:** Lag én regel (i AD-8 eller en ny konvensjonsrad): «Krediteringslinjen er én felles maldel som alltid viser alle tre kreditteringene med lenker. Leaflets egen attribusjonsprefiks (`Leaflet`-lenken) slås av. Turens `kilde` og `lisens` vises (for eksempel i Kartet i tekst eller i en fotnote) når turen kommer fra OSM.» Bestem også om OSM-kreditten vises på alle turer (som i EXPERIENCE) eller bare på OSM-turer.

### M3. ODbL: den committede `turer.geojson` bryter to av vernene i addendumet

- **Kilde:** Addendum › OpenStreetMap og ODbL: «Egne felt … holdes adskilt fra OSM-geometrien (Collective Database)», «Turdatabasen tilbys ikke som en nedlastbar fil», «ett håndplukket engangsuttrekk med færre enn 100 objekter».
- **Spinen:** AD-3 skriver OSM-geometri og egne beregnede felt i samme Feature i én fil, og filen committes til repoet, som sensor og andre kan laste ned. Byggeskriptet «henter geometri» hver gang det kjøres, så uttrekket er ikke et engangsuttrekk.
- **Fiks:** I AD-3:
  - Råuttrekket fra OSM lagres én gang (for eksempel `data/kilder/osm/`, med en ODbL-merknad) og leses lokalt ved nye bygg.
  - Byggeskriptet stopper hvis antall OSM-objekter er 100 eller flere.
  - Egne felt og OSM-geometri holdes i adskilte deler (egen fil, eller adskilt med tur-ID).
  - `data/README` eller `NOTICE` oppgir lisensen for hver kilde.
  - Før i addendumet eller memloggen at commit til emnerepoet er vurdert og akseptert, eller endre formuleringen «ikke nedlastbar».

### M4. MET: User-Agent i `.env.example` og to ulike «ingen data»

- **Kilde:** Addendum › MET (falsk eller tilfeldig identifikasjon kan gi permanent utestengelse, under 20 forespørsler/s), NFR-1 (vær virker uten nøkler), EXPERIENCE (to tilstander: «for langt frem» og «MET svarer ikke», med ulik tekst).
- **Spinen:**
  - AD-9 leser `MET_USER_AGENT` fra `.env`, men sier ikke hva `.env.example` inneholder, eller hva som skjer når verdien er tom. Sensor kopierer eksempelfila. En plassholder som `kontakt@example.com` er nettopp falsk identifikasjon.
  - AD-9 returnerer én «ingen data», så UX-variantene kan ikke skilles.
  - Grensen på 20 forespørsler/s fra memloggen er falt ut.
- **Fiks:**
  - `.env.example` har en ekte, ikke-hemmelig User-Agent (appnavn + repo-URL eller prosjektets kontaktadresse). Er verdien tom, brukes den samme faste verdien fra `config/settings.py`, aldri en plassholder.
  - Tjenesten returnerer en type med årsak: `IngenVarsel(arsak=FOR_LANGT_FREM | UTILGJENGELIG)`. Datoen sjekkes mot varselets siste tidspunkt.
  - Skriv i AD-9 at appen henter høyst ett varsel per startpunkt og forespørsel, så den holder seg langt under 20 forespørsler/s.

### M5. Sensors krav til README og kjøring er bare delvis styrt (kriterium 5–7)

- **Kilde:** Sensorveiledningen s. 5. README skal ha: hva appen gjør og for hvem, forutsetninger med versjoner, kommandoer som kan kopieres, miljøvariabler, **testbrukere**, hvordan testene kjøres, **oversikt over mappestrukturen** og **lenker til planleggings- og prosessdokumentasjonen**. `.gitignore` skal dekke `venv`. Ingen løse filer i roten. FR-21: innloggingen til testbrukeren står i README. NFR-2: alle tilstander gir forklaring og neste steg.
- **Spinen:** AD-12 gir bare installasjonskommandoene. Det mangler:
  - **en innholdsliste for README**
  - **Python-versjon:** Stack låser 3.14. Sensor har trolig 3.12 eller 3.13, og en ny Python-installasjon spiser av de 20 minuttene (NFR-1). Django 6.1 støtter 3.12–3.15.
  - **`DEBUG`:** Variabelen står ikke i `.env.example`. Med `DEBUG=True` ser sensor Djangos gule feilside i stedet for «Uventet feil» (NFR-2). Med `DEBUG=False` serverer `runserver` ikke statiske filer, så Leaflet og CSS forsvinner.
  - **`ALLOWED_HOSTS`**
  - **`.gitignore`** for `venv/`, `.venv/` og `__pycache__/`
  - **kommandoer for både Windows og macOS** (aktivering av venv er ulik)
- **Fiks:**
  - Legg en README-kontrakt til AD-12, med punktene over, og en lenke til `_bmad-output/` og spinen.
  - Skriv «Python 3.12–3.14 støttes, testet på 3.14».
  - Bestem `DEBUG` (for eksempel `DJANGO_DEBUG=True` i `.env.example` og egne maler for 404, 500 og CSRF-feil som testes med `DEBUG=False`). Det andre alternativet er WhiteNoise.
  - Utvid `.gitignore`-listen.

### M6. Nivåhevingen kan forsvinne midt i et søk

- **Kilde:** FR-5 punkt 2.3 (det *første søket* etter heving), FR-5 («Nytt forslag» går videre nedover i *rangeringen*), FR-12 (personaliseringssetning når hevingen har prioritert turen).
- **Spinen:** AD-11 oppdaterer «sist viste nivåtak» ved første søk etter heving. AD-5 lagrer viste ID-er, men ikke rangeringen. Regnes rangeringen på nytt ved «Nytt forslag», er hevingen allerede «brukt», så rekkefølgen og personaliseringssetningen endrer seg mitt i søket. Det samme skjer ved reload.
- **Fiks:** I AD-5 og AD-11: «Ved søk regnes hele den rangerte lista og flagget for nivåheving én gang og lagres i økten. Nytt forslag, reload og Start fra første forslag igjen leser lista. Ingenting regnes på nytt før et nytt søk.» Da blir også testene for FR-7 deterministiske.

### M7. Testbrukeren er ikke spesifisert

- **Kilde:** FR-21 (viser nivåheving, **sperre** og turtypepreferanse, innloggingen i README), SM-4, NFR-1 (lastes med én kommando), NFR-1 og sensorveiledningen (ingen hemmeligheter).
- **Spinen:** «`data/` … testbruker» og `lastinn`. Det er ikke avklart:
  - Hvordan passordet lagres. Det skal hashes med `set_password` ved innlasting. I fila står et demopassord som er merket som demo og ikke er en hemmelighet.
  - Hva som skjer når `lastinn` kjøres på nytt («samme resultat»). Settes testbrukerens historikk tilbake, så sensor kan prøve igjen, eller blir registreringene sensor har lagt til, stående?
  - Hvordan én historikk viser både heving og sperre. Den nåværende tilstanden er bare én av dem. Trengs det to testbrukere, eller en README-oppskrift («registrer en moderat tur for å oppheve sperren»)?
  - Hvilken verdi «sist viste nivåtak» har ved innlasting, så første søk viser hevingen.
- **Fiks:** Lag en egen regel (eller et punkt i AD-3 og AD-11) som svarer på de fire spørsmålene, og en test som laster fixturen og sjekker nivåtak, sperre og preferanse.

### M8. Djangos standardoppførsel bryter Mikrotekst og PRD

- **Kilde:** Konvensjonen «All brukertekst hentes fra Mikrotekst», FR-14 (bare minst 8 tegn, «Feil e-post eller passord»), `<html lang="nb">`, NFR-2 og EXPERIENCE «Uventet feil».
- **Spinen:** Sier ingenting om Djangos standardverdier, som slår inn hvis ingen endrer dem:
  - `LANGUAGE_CODE` er `en-us`, så valideringstekstene blir engelske.
  - `AUTH_PASSWORD_VALIDATORS` har fire validatorer og avviser passord som PRD-en godtar, med tekster som ikke står i Mikrotekst.
  - `AuthenticationForm` har sin egen feiltekst.
  - CSRF-feil gir en engelsk 403-side. Det skjer lett når en innlogging i en annen fane bytter token, og bryter med NFR-2.
  - Det finnes ingen egne `handler404` og `handler500`.
- **Fiks:** Legg til en konvensjonsrad: `LANGUAGE_CODE='nb'`, `TIME_ZONE='Europe/Oslo'`, bare `MinimumLengthValidator(8)`, feiltekstene i auth-skjemaene overstyres med Mikrotekst, og egne maler for `CSRF_FAILURE_VIEW`, 404 og 500 med nøktern tekst og neste steg. E-post normaliseres til små bokstaver, så duplikater fanges (FR-14).

### M9. Personvern: spinen lagrer mer enn personverntekst og NFR-5 lover

- **Kilde:** NFR-5 (lagrer *bare* e-post, passord-hash, historikk og vurderinger, sporer ikke posisjon) og personverntekst på Konto.
- **Spinen:**
  - AD-7 sier «ingen andre persondata», men en Django-brukermodell har `last_login`, og `AbstractUser` har også navn og `date_joined`.
  - Databasesesjonene lagrer søk med fritekst i to uker og blir liggende til `clearsessions` kjøres.
  - Loggen over forkastede KI-svar kan inneholde fritekst, som kan inneholde personopplysninger.
  - Ved kontosletting blir andre sesjoner for samme bruker liggende.
- **Fiks:** I AD-7:
  - Bruk `AbstractBaseUser` + `PermissionsMixin` med bare `email`.
  - Godta `last_login` med en merknad, eller koble fra `update_last_login`.
  - Kontosletting fjerner også sesjonene til brukeren.
  - Loggen lagrer begrunnelse for forkasting, tur-ID-er og KI-svaret, men ikke friteksten (eller bare lengden).
  - `kart.js` bruker aldri geolokasjon.
  - Er noe av dette akseptert, må personverntekst i Mikrotekst justeres.

---

## Lav

### L1. UX-punktet om innlogging utløpt er bare halvveis lukket
EXPERIENCE › Åpne punkter spør også «om utfylte felt kan beholdes gjennom ny innlogging». Mikrotekst lover «så tar jeg vare på det du har fylt inn». AD-6 gjør tilfellet sjeldent, men svarer ikke. **Fiks:** Bestem enten at POST-data lagres i økten før redirect til innlogging og fylles inn igjen etterpå, eller at tilstanden og teksten fjernes fra EXPERIENCE. Merk at `SESSION_COOKIE_AGE` regnes fra sist økten ble endret. Sett `SESSION_SAVE_EVERY_REQUEST=True` hvis to uker skal være fra siste aktivitet.

### L2. Kartdetaljer som trenger mer enn Leaflet-kjernen
- **Zoomgrenser:** EXPERIENCE spør om zoom 12–20, mens Stack sier 0–18. Skriv `maxZoom: 18` (og eventuelt `minZoom`) i AD-8.
- **Bevegelser:** «Bruk to fingre for å flytte kartet» og Ctrl + rullehjul for zoom finnes ikke i Leaflet 1.9.4 uten et tillegg (for eksempel Leaflet.GestureHandling) eller egen kode. Legg tillegget til i Stack og vendre det, eller skriv det i `kart.js`.
- **Norske tekster:** Leaflets engelske tekster (zoomknappenes `title`) og attribusjonsprefikset skal byttes eller fjernes. Det hører til M2.
- **Kartfarger:** Memloggen har følgekravet «UX-måling av kartfarger gjøres mot Kartverket topo». Det mangler i spinen og blokkerer kartfargene i DESIGN.md. Før det inn under Deferred, med eier.

### L3. KI-tone og prompt er ikke bundet
Tonen i PRD §6 (jeg-form, du, overselger ikke KI eller «læring», nøktern) gjelder også KI-tekst. Spinen utsetter all prompttekst. **Fiks:**
- Krav til prompten i AD-10: jeg-form, du-tiltale, ingen tall, ingen påstand om at tjenesten lærer.
- Prompten ligger i en egen versjonert fil (for eksempel `tjenester/ki/prompt.txt`), så endringene kan spores i git (sensor kriterium 1).
- Valideringen avviser også ukjente krøllparenteser og et tomt eller uleselig svar (FR-13).
- Plassholderne settes inn med eksplisitt erstatning, ikke `str.format`. Det unngår krasj på `{` i KI-teksten (NFR-2) og identifikatoren `nivå` med å (konvensjonen Språk i koden).

### L4. Bevis for kvalitetssikring havner utenfor repoet
FR-13 logger forkastede KI-svar «slik at de kan brukes i kvalitetssikringen», og sensors kriterium 3 krever konkrete eksempler i repoet. `logs/` er i `.gitignore`. **Fiks:** Skriv i AD-13 at utvalgte forkastede svar flyttes til et QA-dokument (for eksempel `docs/qa/`) med henvisning til fiksen.

### L5. Hull i kapabilitetskartet
- Turillustrasjon (SVG fra rutelinje og høydeprofil) og «Kartet i tekst» lages av systemet, aldri av KI (FR-6). Ingen av dem er plassert. Forslag: tekst og punktserier i `domene/`, og SVG i en maldel.
- Turforslag fra historikken (FR-17) trenger en egen rute som ikke rører økten (AD-5). Skriv ruten, for eksempel `/historikk/<tur-id>/`, og at den krever innlogging.
- Hjelpeteksten om Oslo-området i FR-4 (PRD v1.3) er bare mikrotekst og er greit dekket. Ingen endring.

### L6. Ryddepunkter i frontmatter og memlog
- `sources` viser til `docs/extract-sensorveiledning.md`, som ikke finnes. Riktig sti er `_bmad-output/planning-artifacts/prds/prd-G81-eriksen-2026-10-29/extract-sensorveiledning.md`.
- Memloggens kildelinje sier «PRD v1.2», mens gjeldende versjon er v1.3. Linje 41 bruker v1.3.
- AD-7, AD-11 og AD-13 mangler `[ADOPTED]`, mens memloggens linje 44 registrerer dem som beslutninger. Merk dem, eller skriv at de venter på godkjenning.
- `.gitignore` i AD-12 bør også nevne at migreringene **committes**, mens databasefilen ikke gjør det.

---

## Avstemt og i orden (ingen tiltak)

- **UX-punkter adressert til arkitekturen:** kartflis-kilde (AD-8), nettleserstøtte (konvensjon), øktlengde og WCAG 2.2.1 (AD-6, se L1), turnavn (AD-3.1), UTM → WGS84 (AD-3.2), Turrutebasen-dekning (Deferred og memlog).
- **MET:** proxy, buffer, `Expires` og `If-Modified-Since`, 4 desimaler og tidsavbrudd (AD-9).
- **KI:** valgfri, ingen personopplysninger, fritekst som data, validering, reserve og falsk variant i tester (AD-10, utenom H1).
- **Turdatabasen:** statisk, beregnet ved import, appen regner ingenting på nytt (AD-3).
- **Kontosletting:** atomisk (AD-7). Tilgang filtreres på `request.user` (NFR-8).
- **Sporbarhet:** FR- og NFR-ID-er i kode, tester og commits (NFR-6).
- **Mappestrukturen** speiler lagene (sensor kriterium 5). Ingen Node, ingen Docker, ingen nøkler (NFR-1).
- **Systemfonter og vendret Leaflet:** ingen CDN, i tråd med DESIGN.md.
