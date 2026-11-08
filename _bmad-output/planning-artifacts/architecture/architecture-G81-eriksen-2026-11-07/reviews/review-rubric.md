# Rubric Review — Architecture Spine, Your Next Adventure (G81-eriksen)

Gjennomgått: `ARCHITECTURE-SPINE.md` (oppdatert 2026-11-08), `.memlog.md`, PRD v1.3 (`prd.md`), og der det trengtes `addendum.md` og `EXPERIENCE.md`. Spinen er ikke endret.

## Overall verdict

Spinen er god og passer godt til prosjektet: én prosess, én database og ren Python i `domene/` er riktig vei for en nybegynner som bygger med KI-hjelp, og nesten alle AD-er har en regel som kan sjekkes i kode. Driftsrammene er avgjort (bare lokal kjøring, deploy utsatt). Hullene ligger i kontraktene *mellom* enhetene som ulike stories skal bygge. AD-1 forbyr JavaScript utenfor kartet, men `EXPERIENCE.md` krever at «Nytt forslag» bytter innhold uten ny sideinnlasting. KI-kallet har ingen fast protokoll, og sekvensdiagrammet strider mot FR-12. Feltene i `turer.geojson` er ikke låst, og enhetene strider mot addendumet (`lengde_km` mot «lengde i meter»). Økten (AD-5) kan ikke oppfylle PRD-tilstanden «fanen er lukket». **Anbefaling: rett de fire high-funnene før epics og stories lages. Resten kan rettes samtidig eller tas i første story.**

## 1. Divergenspunkter for nivået under — delvis dekket

Sjekket: hvert sted der to stories (eller to KI-økter) må bli enige om noe uten å snakke sammen: grensen mellom byggeskript og `lastinn`, økten, KI-kallet, nivåtaket, modeller, URL-er og JavaScript.

### Findings

- **high — AD-1 strider mot UX-spesifikasjonen for «Nytt forslag» og lastetilstanden.** AD-1 sier at JavaScript *bare* brukes i kartmodulen og at det ikke finnes JSON-API for egne sider. `EXPERIENCE.md` sier derimot at «"Nytt forslag" bytter innholdet på stedet uten å laste siden på nytt», at `document.title` settes og fokus flyttes til `h1` ved hver visningsendring, at visningen har `aria-busy="true"` mens forslaget hentes, og at Laster-tilstanden viser Søkeoppsummering og en tom kartflate med en gang (EXPERIENCE.md › Interaction Principles, Accessibility Floor › Sidetitler og fokus, State Patterns › Laster og Henter nytt forslag). Memloggen skrev «JavaScript kun for kart (og evt. små progressive forbedringer)», men den delen falt bort i spinen. Den som bygger FR-7, må nå enten bryte AD-1 (fetch, HTMX eller et eget skript) eller bryte UX-spesifikasjonen med full sideinnlasting. To stories vil velge ulikt. *Fix:* Velg én vei og skriv den inn i AD-1. Enten (a) tillat én liten progressiv forbedring, `static/forslag.js`, som henter et HTML-fragment fra serveren (ikke JSON), bytter innholdet, setter tittel og fokus og håndterer `aria-busy`, med vanlig POST og full side som fallback uten JS. Eller (b) behold full sideinnlasting og før avviket inn i `EXPERIENCE.md` (fokus til `h1` med `autofocus`/`tabindex`, tittelen settes av serveren, ingen egen lastetilstand utover nettleserens). Velg også hvordan Laster-tilstanden blir til med server-rendring.

- **high — KI-kallet har ingen fast protokoll, og sekvensdiagrammet strider mot FR-12.** Diagrammet «Flyt for ett turforslag» sier at KI kalles «bare hvis fritekst og nøkkel». FR-12 sier at KI skriver begrunnelsen *når KI er tilgjengelig*, også uten fritekst. Diagrammet filtrerer og rangerer dessuten *før* KI-kallet, mens FR-11 bruker KI-svaret som kriterium 2 i rangeringen. Spinen sier ikke om tolking og begrunnelse er ett kall eller to, hvilken tur begrunnelsen skrives for (den velges først etter rangeringen), om «Nytt forslag» gir et nytt KI-kall for den nye turens begrunnelse, eller om 5-sekundersgrensen gjelder per kall eller per søk. Med ulike svar her får stories for FR-5, FR-7, FR-11 og FR-12 ulike grensesnitt mot `tjenester/ki/`. *Fix:* Legg en punktliste i AD-10 med kallprotokollen. Forslag: kall 1 (bare med fritekst) skjer ved søk og gir ID-ene som passer, og svaret lagres i økten. Så rangeres treffene. Kall 2 skjer for hvert turforslag som vises (også etter «Nytt forslag») og gir begrunnelsen for én tur-ID; det lagres i økten per tur-ID. Hvert kall har 5 s grense, og feil i ett kall gir reserve bare for den delen. Rett sekvensdiagrammet etter dette.

- **high — Feltene i `turer.geojson` er ikke låst, og enhetene strider mot addendumet.** `turer.geojson` er kontrakten mellom byggeskriptet og `lastinn`, som trolig bygges i ulike stories. AD-3 sier «feltene i addendumet pluss `kilde` og `lisens`». Addendumet har allerede `kilde` og `lisens`, men lister `lengde_km` og bare `startpunkt` (navn). Konvensjonen «Tid og tall» sier derimot at lengde lagres i meter, og AD-3 punkt 1 sier at startpunktet har navn *og* koordinat (som MET-proxyen trenger). Tur-ID, turnavn, turtyper og ut.no-URL står ikke i addendumets liste. Det står heller ikke hvordan `hoydeprofil` er formet, eller at lengde for tur-retur lagres for én vei (PRD §3). *Fix:* Legg feltlisten med navn, type og enhet inn i spinen (Structural Seed eller AD-3), og si at den gjelder foran addendumet. For eksempel: `id` (str), `navn`, `startpunkt` {`id`, `navn`, `lat`, `lon`}, `form` (`tur-retur`|`rundtur`), `turtyper` [..], `lengde_m`, `hoydemeter`, `nedstigning` (én vei for tur-retur), `hoydeprofil` [[avstand_m, hoyde_m], ...], `turniva`, `estimert_tid_min` (hele turen), `ut_url` (valgfri), `kilde`, `lisens`, med geometri i WGS84.

- **high — AD-5 og AD-6 kan ikke oppfylle PRD-tilstanden «fanen er lukket».** PRD §3 og §6 sier at økten varer til et nytt søk eller til fanen lukkes, og at «turforslaget finnes ikke lenger, fordi fanen er lukket eller adressen er åpnet direkte» er en egen tilstand. AD-5 legger søkeøkten i Djangos session, og AD-6 gir den samme cookien to ukers levetid. Da overlever forslaget at fanen lukkes, og adressen åpnet i en ny fane viser det samme forslaget. Serveren kan ikke se at en fane lukkes. Én story kan legge til `sessionStorage`-JS, en annen godtar oppførselen. *Fix:* Avgjør det i AD-5. Enten (a) godta at økten varer til nytt søk eller utlogging, og før avviket fra PRD §3/§6 inn i PRD §9 og `EXPERIENCE.md`. Eller (b) gi hvert søk en tilfeldig søke-ID i et skjult felt eller i stien og la «finnes ikke lenger» gjelde når ID-en ikke finnes i økten (dekker «adressen åpnet direkte», men ikke lukket fane).

- **medium — Når nivåtaket regnes som «hevet», kan forveksles med at en sperre oppheves.** AD-11 sier at søket er det første etter heving når beregnet nivåtak er høyere enn «sist viste nivåtak». Men nivåtaket stiger også når en sperre oppheves (FR-19), og det er ikke en heving. Regelen sier heller ikke om lagret verdi oppdateres når nivåtaket synker under en sperre. Uten dette vil to implementasjoner gi ulik rangering etter en sperre. *Fix:* La domenefunksjonen gi ut et tellertall eller registrerings-ID-en for siste *heving* (ikke selve nivåtaket). Lagre «siste heving sett» på brukeren, og la søket være det første etter heving når tallet er nytt.

- **medium — `lastinn` kan slette historikk.** AD-3 sier at `lastinn` kan kjøres flere ganger med samme resultat, men ikke hvordan. Sletter og laster kommandoen turene på nytt, blir registreringene slettet med dem (CASCADE) eller kommandoen krasjer (PROTECT). *Fix:* Skriv i AD-3 at `lastinn` oppdaterer eller oppretter etter tur-ID og aldri sletter turer som har registreringer, og at `Registrering.tur` har `on_delete=PROTECT`. Testbrukeren opprettes eller nullstilles etter e-post.

- **medium — Lagring av geometri og høydeprofil i SQLite er ikke avgjort.** AD-4 forbyr rå SQL, men ikke GeoDjango eller SpatiaLite. En agent som «lagrer rutelinje» kan fort hente inn GeoDjango, og på Windows krever det GDAL og SpatiaLite. Det bryter NFR-1 (under 20 min, ingen ekstra installasjon). *Fix:* Legg til i AD-4: geometri og høydeprofil lagres som `JSONField` (GeoJSON og liste), og GeoDjango og SpatiaLite brukes ikke.

- **low — Dobbel innsending av en registrering teller dobbelt.** FR-19 sier at hver registrering teller, også gjentakelser. Post/Redirect/Get hindrer ikke et dobbeltklikk, og da kan to registreringer heve nivåtaket. NFR-2 krever bare at appen ikke krasjer. *Fix:* Bestem en mekanisme i konvensjonen Skjema, for eksempel et engangstoken i skjemaet som lagres i økten og forbrukes ved første POST.

- **low — E-post er ikke normalisert.** AD-7 sier e-post som innloggingsfelt, men ikke om `Ola@` og `ola@` er samme konto. Én story lagrer med små bokstaver, en annen søker uten. *Fix:* I AD-7: e-post lagres med små bokstaver, er unik og slås opp uten skille mellom store og små bokstaver.

- **low — URL-er og navnene på dem er ikke fastsatt.** Stories lenker til hverandre med `{% url %}`. Når hver story velger egne stier og navn, gir det brudd. *Fix:* Legg en kort rutetabell i Structural Seed (sti, URL-navn, krever innlogging), avledet fra IA-tabellen i `EXPERIENCE.md`. Ta også med regelen for `next` etter innlogging (FR-14: rett inn i registreringen av turen).

## 2. Kan reglene håndheves, og hindrer de divergensen? — for det meste

Sjekket: hver AD sin Rule mot Prevents.

### Findings

- **medium — Regelen i AD-10 punkt 4, «svar innen 5 s», er ikke nok med SDK-en slik den er satt opp som standard.** `anthropic`-SDK-en prøver på nytt to ganger som standard, så et kall med 5 s grense kan ta opptil 15 s før reserven slår inn. *Fix:* Legg til «klienten opprettes med `timeout=5` og `max_retries=0`» i AD-10.
- **low — Konvensjonen Konfigurasjon og byggeskriptet passer ikke sammen.** Konvensjonen sier at bare `config/settings.py` leser miljøvariabler. Byggeskriptet kjører utenfor Django (AD-3) og trenger likevel en identifiserende User-Agent mot Kartverket og OSM. *Fix:* Legg til unntaket «`skript/` leser sine egne verdier fra `.env` med `python-dotenv`», eller la byggeskriptet få User-Agent som argument.
- **low — Hvordan byggeskriptet startes, er ikke avgjort.** `python skript/bygg_turdatabase.py` gjør at `import domene` feiler, fordi `sys.path[0]` blir `skript/`. Det er en typisk felle for nybegynnere og KI-agenter. *Fix:* Skriv kommandoen i AD-3: `python -m skript.bygg_turdatabase` fra repo-roten (med `skript/__init__.py`).
- **low — AD-7, AD-11 og AD-13 mangler statusmerke.** De andre AD-ene er merket `[ADOPTED]`. Memloggen sier at disse tre ble avledet under destilleringen og meldt til brukeren, men ikke at de er godkjent. *Fix:* Merk dem `[ADOPTED]` når Hannah har bekreftet dem, ellers `[PROPOSED]`.

Det som fungerer: AD-2 (ingen Django-import i `domene/`) kan sjekkes med grep eller en Ruff-regel. AD-3 punkt 4, AD-8 (fliser uten nøkkel, vendret Leaflet) og AD-9 (avrunding, buffernøkkel, User-Agent) er konkrete og kan testes. AD-13 gir tester uten nett.

## 3. Deferred — ok

Alle seks utsatte punkter gjelder én enhet (byggeskriptet eller ordlyden i prompten) eller ligger utenfor v1. Ingen av dem kan få to enheter til å gjøre ulikt, så lenge feltene i `turer.geojson` blir låst (se 1). Leverandørbytte for KI er godt avgrenset til én ny variant.

## 4. Teknologi — plausibel og oppdatert

Sjekket mot memloggens versjonssjekker (PyPI og djangoproject.com, 2026-11-07/08). Django 6.1.3 på Python 3.14 er en støttet kombinasjon med støtte gjennom prosjektperioden. Leaflet 1.9.4 er riktig stabil versjon (2.0 er beta). httpx 0.28.1, python-dotenv 1.2.4, Ruff 0.17.4, pyproj 3.8.0 (med cp314-hjul for Windows), `anthropic` 2.6.0 og `claude-haiku-5-5` er alle sjekket og datert i memloggen. Jeg har ikke sjekket PyPI på nytt. Kartverket WMTS og høyde-API og MET Locationforecast 2.0 er riktige.

### Findings

- **low — Python 3.14 står som eksakt versjon, men README trenger en minsteversjon.** Sensor kan ha 3.12 eller 3.13, og Django 6.1 støtter begge. *Fix:* Skriv «utviklet på 3.14, krever ≥ 3.12» i Stack og i AD-12.
- **low — Hvordan byggeskriptet henter Turrutebasen og OSM-data, er ikke navngitt.** Addendumet sier at nedlastingen fra Geonorge må testes, og at OSM hentes som ett engangsuttrekk (Overpass?). Det gjelder bare én enhet, så det kan utsettes. *Fix:* Legg det til i Deferred med «avgjøres i story for turdatabasen».

## 5. Dekning av PRD-ens funksjoner — god, med ett hull

Capability-kartet dekker FR-1 til FR-21, FR-17.1 og NFR-1 til NFR-9.

### Findings

- **medium — Turillustrasjonen (FR-6) har ikke noe hjem.** Den er en SVG med rute og høydeprofil (EXPERIENCE.md › Turillustrasjon) og bærer klimakset i UJ-1. Spinen sier ikke om SVG-en lages på serveren eller i JS. Med AD-1 er ett svar riktig, men en agent kan fort hente inn et JS-diagrambibliotek. *Fix:* Legg til en rad i Capability-kartet: SVG-en lages på serveren som inline SVG i malen, og koordinatene til stien regnes ut av en ren funksjon i `domene/`. Ingen JS.
- **low — Verktøyet for automatisk UU-sjekk (NFR-4) er ikke valgt.** Det er et testverktøy, ikke en del av appen. *Fix:* Legg det i Deferred (for eksempel axe DevTools eller Lighthouse, manuelt), slik at det ikke blir en npm-avhengighet.

## 6. Dimensjoner som dette nivået eier — driftsrammene er dekket, men utviklingsoppsettet er tomt

Avgjort: deploy og miljøer (bare lokalt, AD-12; produksjon, HTTPS og e-post utsatt), infrastruktur (ingen; SQLite-fil), hemmeligheter (`.env`, `.gitignore`), logging (AD-13), testing og kodestil, nettleserstøtte, tidssone, eksterne avhengigheter med feilhåndtering (AD-9, AD-10, konvensjonen Feil fra eksterne tjenester).

### Findings

- **medium — Django-innstillingene for lokal kjøring er ikke avgjort.** `DEBUG`, `ALLOWED_HOSTS`, `LANGUAGE_CODE` og hvordan statiske filer serveres, er ikke nevnt. Det har konsekvenser: med `DEBUG=False` serverer `runserver` ikke `static/`, og da forsvinner Leaflet og CSS. Med `LANGUAGE_CODE` på engelsk kommer Djangos egne feilmeldinger i skjema og passordvalidering på engelsk. `.env.example` må også inneholde verdier som virker uten endring: en hemmelig nøkkel for utvikling og en gyldig `MET_USER_AGENT` med prosjektets kontaktinfo. Ellers kan MET svare 403, og «vær uten nøkler» (NFR-1) feiler. *Fix:* Legg en linje i AD-12: `DEBUG=True` som standard i `.env.example`, `ALLOWED_HOSTS=["localhost","127.0.0.1"]`, `LANGUAGE_CODE="nb"`, `TIME_ZONE="Europe/Oslo"`, `USE_TZ=True`, og at alle verdier i `.env.example` virker som de er, unntatt `ANTHROPIC_API_KEY`.
- **low — Det finnes ikke noe tidsbudsjett for ett søk.** KI (5 s, og kanskje to kall) og MET (5 s) kjøres etter hverandre i samme forespørsel. Det verste tilfellet blir 10–15 s før svaret. Det påvirker lastetilstanden (se 1). *Fix:* Skriv et samlet tak i sekvensdiagrammet eller AD-9/AD-10, for eksempel «ett søk venter maks ca. 10 s; MET-feil eller treg MET gir svar uten tips».

## 7. Mermaid-diagrammer — gyldige

Sjekket mot grammatikken til Mermaid for hånd (ikke kjørt i en renderer):

- Lagdiagrammet (`flowchart TD`): labels i anførselstegn med `/` og parenteser, og stiplet kant med label `-. "..." .->`. Gyldig.
- System og omgivelser (`flowchart LR`): sylindernoden `db[("SQLite")]` og kant-labels i anførselstegn. Gyldig.
- Kjerneentiteter (`erDiagram`): relasjoner med labels i anførselstegn og entitetene `VAERBUFFER` og `SESSION` uten relasjoner. Gyldig i gjeldende Mermaid. *Merknad:* `STARTPUNKT` har ingen ID i kurateringslista (AD-3 punkt 1 gir bare navn og koordinat). Det hører til låsingen av feltene i `turer.geojson` (se 1).
- Flyt for ett turforslag (`sequenceDiagram`): aliaser med parenteser, en selvmelding `V->>V` og «» i meldingstekst. Gyldig syntaks, men innholdet må rettes (se det andre high-funnet i 1).

Literalene `{tid}`, `{varighet}`, `{lengde}`, `{nivå}` og `{z}/{y}/{x}` er brukt med vilje og er ikke funn.
