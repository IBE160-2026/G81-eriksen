# Epic 1 Context: Ola finner en tur som passer tiden, på nett

<!-- Compiled from planning artifacts. Edit freely. Regenerate with compile-epic-context if planning docs change. -->

## Goal

En gjest åpner den publiserte siden, velger varighet og dato og får ett turforslag i Oslo og Bærum med kart, nivå, estimert tid og en begrunnelse fra mal. Gjesten kan be om nytt forslag og får konkret hjelp når ingenting passer. Epicen bygger prosjektet fra null: kildetre, egen brukermodell i første migrering, tidlig publisering på Vercel (så hver PR får en forhåndsvisning), basismal med designtokens, turdatabasen med byggeskript og innlasting, kart med kreditering og CSP. Byggeskriptet var den største risikoen og er levert (1.5). Alt annet i appen bygger på denne epicen.

## Stories

- Story 1.1: Appen starter lokalt etter README
- Story 1.2: Appen er publisert på Vercel
- Story 1.3: Siden har et rolig og tilgjengelig grunnoppsett
- Story 1.4: Turnivå og estimert tid regnes etter faste regler
- Story 1.5: Byggeskriptet lager turdatabasen fra Kartverket
- Story 1.6: Turene lastes inn med én kommando
- Story 1.7: Turdatabasen har 15 kontrollerte turer
- Story 1.8: Systemet velger og rangerer turer som passer søket
- Story 1.9: Ola søker og får ett turforslag
- Story 1.10: Ola ser ruten på kart og i tekst
- Story 1.11: Ola kan be om nytt forslag
- Story 1.12: Ola får hjelp når ingen tur passer

## Requirements & Constraints

- **Kjørbarhet:** lokal installasjon etter README uten nøkler, Node, Docker eller databaseserver (Python 3.12–3.15, testet på 3.14). Rekkefølgen er `venv`, `pip install`, kopiere `.env`, `migrate`, `lastinn`, `runserver`. Turdatabasen (og senere testbrukeren) lastes med én kommando. Lokal kjøring virker alltid uten Vercel, Neon eller andre kontoer. Ingen hemmeligheter i repoet.
- **Publisering:** hver endring i `main` publiseres automatisk, og hver PR får en forhåndsvisning med egen database. Adressen står øverst i README.
- **Turdatabase:** 15 kuraterte turer (P1). Flertallet er grønne eller blå, minst én svart, minst tre toppturer og fem utsiktsturer, hver turtype har en grønn tur under 2 t der terrenget tillater det, og hvert startpunkt har minst to turer. Kilde og lisens per tur. OSM bare som supplement, under 100 objekter. Tur-ID-er endres eller slettes aldri, fordi registreringer og testbrukeren viser til dem.
- **Gradering:** Merkehåndboka med «<»-grenser. En verdi på grensen graderes opp, og den strengeste av lengde og høydemeter vinner. Tur-retur graderes etter én vei, rundtur etter hele runden.
- **Tid:** sveitsisk regel (15 min/km + 15 min/100 hm + 15 min/200 m ned) + 15 %, avrundet til nærmeste 5 min. Tur-retur regnes begge veier. Fasit: tur-retur, 3 km én vei, 150 hm, 0 m ned = 142,3 min = «ca. 2 t 20 min». Tiden vises alltid med «pauser ikke inkludert».
- **Utvalg:** estimert tid ≤ varighet (lik er med), turnivå ≤ nivåtaket (alltid grønt for gjester), valgt turtype og startpunkt. Rangering: tid nærmest varigheten, deretter tur-ID (deterministisk). Ingen tur over nivåtaket vises noen gang.
- **Nytt forslag:** neste tur i den frosne rangeringen, aldri en tur som alt er vist i søket. Ny innlasting beholder forslaget. Forslaget kan ikke deles som lenke.
- **Begrunnelse:** uten KI-nøkkel brukes reservemalen. Den nevner varigheten og eventuell turtype, er høyst 300 tegn og har merket «Begrunnelse fra mal».
- **Stabilitet og sikkerhet:** feil input, manipulerte POST-er og dobbeltklikk krasjer aldri. Alle tilstander gir et forslag eller neste steg. All validering skjer på serveren.
- **Mobil og UU:** WCAG 2.1 AA, reflow ved 320 px, trykkflater på minst 44 × 44 px. På 360 px synes nivå, tid og turtype-treff uten rulling. Hele flyten virker med tastatur. Et automatisk UU-verktøy kjøres, og resultatet legges i PR-en.
- **Kreditering:** «© Kartverket» og «© OpenStreetMap contributors» med lenker, alltid synlig på kartet.
- **Sporbarhet:** kode, tester og commits viser til FR- og NFR-ID-er (f.eks. `# FR-3`).

## Technical Decisions

- **Lag:** `turforslag/` (web) → `domene/` + `tjenester/`. `skript/` → `domene/`. `domene/` er ren Python som bare importerer standardbiblioteket, uten database, nett eller klokke (dagens dato sendes inn), og en test sjekker dette. Views, kommandoer og byggeskript regner, filtrerer og formaterer aldri selv.
- **Stack:** Django 6.1.3, python-dotenv 1.2.4, anthropic 2.6.0 og psycopg[binary] 3.3.9, låst i `requirements.txt`. Ruff 0.17.4 bare i `requirements-dev.txt`, med oppsettet i `pyproject.toml`. Leaflet 1.9.4 vendret i `static/vendor/leaflet/`.
- **Avhengigheter på Vercel:** Vercel installerer fra `[project].dependencies` i `pyproject.toml` og hopper da over `requirements.txt`. Listene holdes like, og en test sjekker det. Ny pakke må inn begge steder.
- **Brukermodell (første migrering):** `turforslag.Bruker(AbstractUser)` med `username=None`, uten fornavn og etternavn, `USERNAME_FIELD="email"`, egen manager og `brukt_heving` (standard 0). E-post med små bokstaver, passordvalidering bare minimumslengde 8.
- **Settings:** miljøverdier leses bare i `config/settings.py`, aldri med reserveverdier i koden. Lokalt (`VERCEL` ikke satt) stopper appen med norsk melding hvis `.env` eller `DJANGO_SECRET_KEY` mangler. På Vercel: `DEBUG=False`, vakt mot manglende eller utviklingsverdi av nøkkelen, `.vercel.app`-host og CSRF-origin, `SECURE_PROXY_SSL_HEADER`, sikre cookies og logging til standard ut. `check --deploy` er ren (testet). `LANGUAGE_CODE="nb"`, `TIME_ZONE="Europe/Oslo"`, norske feilsider.
- **Database:** samme ORM-modeller og migreringer for SQLite (`db.sqlite3` lokalt og i alle tester, når `DATABASE_URL` mangler) og Neon Postgres (`DATABASE_URL`, `DISABLE_SERVER_SIDE_CURSORS=True`, `DATABASE_URL_UNPOOLED` når `CI` er satt). Ingen rå SQL, ingen databasespesifikke felt eller funksjoner, ingen GeoDjango eller SpatiaLite.
- **Vercel-bygging:** `.python-version` 3.14, `vercel.json` med region `fra1`. `[tool.vercel.scripts] build` i `pyproject.toml` kjører `migrate --noinput` og fra story 1.6 deretter `lastinn`. Stopper `lastinn`, feiler byggingen synlig i PR-en og forrige publisering blir stående. Åpent punkt: `migrate` har da alt endret databasen, så migreringer bør være bakoverkompatible. `STATIC_ROOT=staticfiles/`, og Vercel kjører `collectstatic` (ikke WhiteNoise).
- **Turdata:** `domene.tur.Tur` er en frossen dataklasse og eneste beskrivelse av en tur, med flate startpunktfelt (`startpunkt_id`, `_navn`, `_lat`, `_lon`, `_hoyde_m`), verdier for én vei ved tur-retur og hele runden ved rundtur (totaler bare via funksjoner i `domene.tur`), heltall meter og minutter, og `til_geojson_feature()`/`fra_geojson_feature()`. Avstand med haversine i `domene.tur`. Formatet i `data/turer.geojson` står i `data/README.md`.
- **Byggeskript (levert i 1.5):** `python -m skript.bygg_turdatabase` leser `data/kurateringsliste.toml` med `tomllib` og validerer hele lista før noe hentes. Per tur: id, navn, startpunkt (id, navn, koordinat), form, turtyper, `rutenummer` (liste av `app:rutenummer`), `rutepunkter` og ut.no-URL. Rutepunktene er `fra`, `til` og valgfrie `via` som `[lat, lon]`. Rundtur har ikke `til` og krever minst ett `via`; tur-retur krever `til` (vendepunktet). Startpunktet er uavhengig av rutepunktene, turnavnet kommer bare fra lista, og samme startpunkt-ID må ha samme navn og koordinat. Geometrien hentes fra Turrutebasens WFS (`app:Fotrute`, `srsName=EPSG:4326`, filter på `app:fotruteInfo/app:FotruteInfo/app:rutenummer`, `gml:posList` lon lat). Ett rutenummer er et usortert nettverk med forgreininger, så `domene/rute.py` lager en graf (endepunkter innenfor 1 m er samme node), fester rutepunktene til nærmeste node innenfor 50 m og velger korteste sti (Dijkstra). Høyder fra Kartverket (`koordsys=4258`, høyst 50 punkter per kall, punkt hvert 25 m, støyterskel 5 m der resten på slutten telles). Skriptet importerer bare standardbiblioteket og `domene` (`urllib.request`, `xml.etree.ElementTree`, `tomllib`), ingen `pyproj`. Ved feil stopper det med tur-ID, og `data/turer.geojson` (committet) skrives atomisk med midlertidig fil og `os.replace`.
- **Modeller (1.6):** `turforslag.Startpunkt` har `id` (stabil streng, primærnøkkel), `navn`, `lat`, `lon` og `hoyde_m`. `turforslag.Tur` har `startpunkt` som `ForeignKey` med `on_delete=PROTECT` og `turtyper` som `JSONField` med en liste av `marka`, `utsikt`, `topptur`. Geometri og høydeprofil ligger også i `JSONField`. Turtype filtreres i `domene/`, aldri med JSON-oppslag i databasen. Turtyper er ingen egen entitet.
- **Lasting (1.6):** `python manage.py lastinn` leser `data/turer.geojson` via `domene.tur`, og `lastinn` og omgjøringen i `turforslag/` mapper mellom de flate feltene i dataklassen og modellene. Startpunkter og så turer opprettes eller oppdateres etter `id` og slettes eller gjenopprettes aldri; to kjøringer gir samme antall. Ugyldig eller ødelagt fil gir en norsk melding, og ingenting endres (atomisk). Appen beregner aldri turnivå, høydemeter eller tid på nytt. Senere utvides kommandoen: `Registrering.tur` får `on_delete=PROTECT`, og mangler en tur med registreringer i fila, stopper kommandoen (Epic 2); `data/testbruker.toml` lastes etter turene, og testbrukeren slettes og lages på nytt hver kjøring (Epic 3).
- **Utvalg:** `domene.sok.Sok` → `velg_turer(...)` → `Utvalg(status, rangerte_tur_ider)` med statusene `TREFF`, `TOPPTUR_ERSTATTET`, `BARE_OVER_NIVATAK` og `INGEN_TREFF`. `domene.utvalg.foresla_endringer(sok, turer, nivatak, tidligere_treff=())` bruker `velg_turer`.
- **Søketilstand:** gyldig POST lager søke-ID (`secrets.token_urlsafe`) og sender til `/forslag/<sok_id>/`. `domene.okt.Soketilstand` (`til_dict`/`fra_dict`) ligger i økten under `"sok"`. Bare `turforslag/okt.py` leser og skriver den, alltid hele verdien, med de 10 nyeste søkene. Rangeringen fryses ved søket. `flush()`, `cycle_key()` og `clear()` brukes aldri.
- **Kart:** `kart.js` tegner bare GeoJSON fra `json_script`, uten egen logikk. Fliser fra `cache.kartverket.no` topo. `attributionControl: false`, og krediteringen renderes i malen. «Kartet i tekst» lages i `domene/`.
- **JS og CSP:** nøyaktig to egne JS-filer (`kart.js` og `forbedring.js`), uten rammeverk eller byggesteg. Alt virker uten JS, og serveren svarer med HTML, aldri JSON. CSP: `default-src 'self'`, `img-src 'self' https://cache.kartverket.no`, `object-src 'none'`, `base-uri 'self'`, `form-action 'self'`, `frame-ancestors 'none'`. Ingen inline-skript og ingen `style`-attributter.
- **Konvensjoner:** domeneord på norsk uten æ/ø/å i identifikatorer. All formatering («ca. 1 t 35 min», «3,5 km totalt», «Grønn – lett») skjer i `domene/`. Alle POST følger PRG med CSRF. Tester kjøres med `python manage.py test` uten nettverk, med lagrede svar i `tests/fixtures/`; domenetester bruker ikke databasen. Én logger per modul.

## UX & Interaction Patterns

- **Tekst:** all brukertekst kommer fra Mikrotekst i `EXPERIENCE.md`, i jeg-form med du-tiltale. Tekster merket [ASSUMPTION] brukes, men markeres som foreløpige i en kodekommentar og i PR-en.
- **Grunnoppsett:** alle tokens fra `DESIGN.md` blir CSS-variabler i én fil. Systemfonter. `lang="nb"`, `header`/`nav`/én `main`, sidetittel «… – Your Next Adventure». Flytende oppsett uten faste høyder og uten `overflow: hidden`. Fokusring 3 px med 2 px avstand, aldri fjernet. Bevegelse av ved `prefers-reduced-motion`.
- **Komponenter:** høyst én primærknapp per visning, `aria-disabled` under innsending. Melding står der saken gjelder og er aldri toast. Feltfeil under feltet med «!», `aria-invalid` og `aria-describedby`, og fokus går til feltet. Turtypekort er en ekte radiogruppe.
- **Søk:** `h1` «Hvor lang tid har du?». Varighet (1–8 t i halvtimessteg), Dato (31 dager), Turtype og Startpunkt. Ingen fritekst i Epic 1.
- **Turforslag:** DOM-rekkefølgen er lik på alle bredder. Over 720 px sticky kart til venstre og Infokolonne til høyre; under 720 px én kolonne med kartet på ca. 60 % av skjermhøyden. Ved 1280 × 800 synes turnavn, turtype-treff, Faktarute og kart uten rulling. Forklaringspanelet er lukket som standard.
- **Kart:** kontroller på 44 px. Hjul og én finger ruller siden, Ctrl/Cmd + hjul zoomer, to fingre flytter kartet. Kartflaten har `tabindex="0"` og `role="region"`, og Tab fører alltid ut. Feiler flisene eller JS, vises en melding med «Prøv igjen», og krediteringen står fortsatt.
- **Tilstander:** Tilstandspanel (`h1`) erstatter turinnholdet ved ingen treff, gjest med nivåtak og «alle vist», og «Endre søk» er alltid med. Endringsforslag er `<button>` i små POST-skjemaer. Ved hver visningsendring oppdateres `document.title`, og fokus går til `h1`. «Nytt forslag» med JS bytter et HTML-fragment, med `aria-busy` og en `aria-live`-melding.

## Cross-Story Dependencies

- Byggerekkefølge: 1.1–1.10, så story 6.5 (kartfarger målt mot ekte fliser), så 1.11–1.12.
- 1.1–1.5 er levert. 1.4 → 1.5 → 1.6 → 1.7. Datasettet fra 1.7 trengs for ekte data i 1.8–1.12.
- 1.6 bygger på `domene.tur` og `data/turer.geojson` fra 1.5 og legger `lastinn` inn i byggesteget fra 1.2. Kriteriene for 1.5 i epics-fila beskriver fortsatt rekkefølgekobling og en HTTP-klient fra `requirements.txt`; spinen (graf, rutepunkter, `urllib.request`) er gjeldende.
- 1.7 skal sjekke punktavstand (25 m) og støyterskel (5 m) mot publiserte høydeprofiler, at rundturer faktisk går i ring, og om rutepunkter som bare kan festes til segmentender er nok (lukkede ringer og T-kryss kan gi ingen sti).
- 1.8 → 1.9 → 1.10/1.11 → 1.12. `foresla_endringer` (1.12) brukes også i «alle vist» fra 1.11.
- Senere epics: «Lag konto», menypunktene og `Registrering` (med PROTECT-sjekken i `lastinn`) kommer i Epic 2. Nivåtak for innloggede og testbrukeren i `lastinn` kommer i Epic 3. KI-begrunnelsen kommer i 4.5, fritekst i 4.6–4.7. Turillustrasjonen (6.1) og `-dark`-tokenene (6.3) er P2.
