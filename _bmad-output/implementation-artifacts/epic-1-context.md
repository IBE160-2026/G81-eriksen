# Epic 1 Context: Ola finner en tur som passer tiden, på nett

<!-- Compiled from planning artifacts. Edit freely. Regenerate with compile-epic-context if planning docs change. -->

## Goal

En gjest åpner den publiserte siden, velger varighet og dato og får ett turforslag i Oslo og Bærum med kart, nivå, estimert tid og en begrunnelse fra mal. Gjesten kan be om nytt forslag og får konkret hjelp når ingenting passer. Epicen bygger prosjektet fra null: kildetre, egen brukermodell i første migrering, tidlig publisering på Vercel (så hver PR får en forhåndsvisning), basismal med designtokens, turdatabasen med byggeskript, kart med kreditering og CSP. Byggeskriptet er den største risikoen og kommer tidlig. Alt annet i appen bygger på denne epicen.

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

- **Kjørbarhet:** lokal installasjon etter README uten nøkler, Node, Docker eller databaseserver (Python 3.12–3.15, testet på 3.14). Lokal kjøring skal alltid virke uten Vercel, Neon eller andre kontoer. Ingen hemmeligheter i repoet.
- **Publisering:** hver endring i `main` publiseres automatisk, og hver PR får en forhåndsvisning med egen database. Adressen står øverst i README.
- **Turdatabase:** 15 kuraterte turer (P1). Flertallet er grønne eller blå, minst én svart, minst tre toppturer og fem utsiktsturer, hver turtype har en grønn tur under 2 t der terrenget tillater det, og hvert startpunkt har minst to turer. Kilde og lisens per tur. OSM bare som supplement, under 100 objekter.
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

- **Lag:** `turforslag/` (web) → `domene/` + `tjenester/`. `skript/` → `domene/`. `domene/` er ren Python som bare importerer standardbiblioteket, uten database, nett eller klokke (dagens dato sendes inn), og en test sjekker dette. Views og byggeskript regner, filtrerer og formaterer aldri selv.
- **Stack:** Django 6.1.3, python-dotenv 1.2.4, anthropic 2.6.0 og psycopg[binary] 3.3.9, låst i `requirements.txt`. Ruff 0.17.4 bare i `requirements-dev.txt` (ikke på Vercel), med oppsettet i `pyproject.toml`. Leaflet 1.9.4 vendret i `static/vendor/leaflet/`.
- **Avhengigheter på Vercel:** Vercel installerer fra `[project].dependencies` i `pyproject.toml` når fila finnes, og hopper da over `requirements.txt`. Lista i `pyproject.toml` holdes derfor lik `requirements.txt`, og en test sjekker det. Ny pakke må legges inn begge steder. Sensor og lokal kjøring bruker `requirements.txt`.
- **Brukermodell (første migrering):** `turforslag.Bruker(AbstractUser)` med `username=None`, uten fornavn og etternavn, `USERNAME_FIELD="email"`, egen manager og `brukt_heving` (standard 0). E-post med små bokstaver, passordvalidering bare minimumslengde 8.
- **Settings:** miljøverdier leses bare i `config/settings.py`, aldri med reserveverdier i koden. Lokalt (`VERCEL` ikke satt) stopper appen med norsk melding hvis `.env` eller `DJANGO_SECRET_KEY` mangler. På Vercel: `DEBUG=False`, vakt mot manglende eller utviklingsverdi av nøkkelen, `.vercel.app`-host og CSRF-origin, `SECURE_PROXY_SSL_HEADER`, sikre cookies og logging til standard ut. `check --deploy` er ren (testet). `LANGUAGE_CODE="nb"`, `TIME_ZONE="Europe/Oslo"`, norske feilsider for 404, 403 (CSRF) og 500 med lenke til Søk.
- **Database:** samme ORM-migreringer for SQLite (lokalt og i tester) og Neon Postgres (`DATABASE_URL`, `DISABLE_SERVER_SIDE_CURSORS=True`, `DATABASE_URL_UNPOOLED` når `CI` er satt). Ingen rå SQL, ingen databasespesifikke felt, ingen GeoDjango. Geometri, høydeprofil og turtyper ligger i `JSONField`.
- **Vercel:** `.python-version` 3.14, `vercel.json` med region `fra1`, Djangos framework preset. `[tool.vercel.scripts] build` i `pyproject.toml` kjører `migrate --noinput`, og fra story 1.6 også `lastinn`. `STATIC_ROOT=staticfiles/`, og Vercel kjører `collectstatic` (ikke WhiteNoise).
- **Turdata:** `domene.tur.Tur` er en frossen dataklasse og eneste beskrivelse av en tur, med flate startpunktfelt, verdier for én vei ved tur-retur (totaler bare via funksjoner i `domene.tur`), meter og hele minutter, og `til_geojson_feature()`/`fra_geojson_feature()`.
- **Byggeskript:** `python -m skript.bygg_turdatabase` leser `data/kurateringsliste.toml` (`tomllib`). Turnavnet kommer bare derfra, og samme startpunkt-ID må ha samme navn og koordinat. Geometrien hentes fra Turrutebasens WFS (`app:Fotrute`, `srsName=EPSG:4326`, `gml:posList` lon lat, parset med `ElementTree`), og segmentene kobles ved endepunktene med toleransen dokumentert i `data/README`. Ingen omregning og ingen `pyproj`; avstand med haversine i `domene.tur`. Høyder fra Kartverket med høyst 50 punkter per kall, punkt hvert 10–25 m og støyfilter. Ved feil stopper skriptet med tur-ID i meldingen og overskriver ikke `data/turer.geojson` (som committes).
- **Modeller og lasting:** `Startpunkt` (streng-PK, `navn`, `lat`, `lon`, `hoyde_m`) og `Tur` (`startpunkt` FK med PROTECT, `turtyper` som JSON-liste). Turtype filtreres i `domene/`, ikke med JSON-oppslag. `lastinn` gjør upsert etter `id` med startpunktene først, sletter aldri og er atomisk ved ugyldig fil. Appen beregner aldri nivå, høydemeter eller tid på nytt.
- **Utvalg:** `domene.sok.Sok` → `velg_turer(...)` → `Utvalg(status, rangerte_tur_ider)` med statusene `TREFF`, `TOPPTUR_ERSTATTET`, `BARE_OVER_NIVATAK` og `INGEN_TREFF`. `domene.utvalg.foresla_endringer(sok, turer, nivatak, tidligere_treff=())` bruker `velg_turer`.
- **Søketilstand:** gyldig POST lager søke-ID (`secrets.token_urlsafe`) og sender til `/forslag/<sok_id>/`. `domene.okt.Soketilstand` (`til_dict`/`fra_dict`) ligger i økten under `"sok"`. Bare `turforslag/okt.py` leser og skriver den, alltid hele verdien, med de 10 nyeste søkene. Rangeringen fryses ved søket. `flush()`, `cycle_key()` og `clear()` brukes aldri.
- **Kart:** `kart.js` tegner bare GeoJSON fra `json_script`, uten egen logikk. Fliser fra `cache.kartverket.no` topo (webmercator, zoom høyst 18). `attributionControl: false`, og krediteringen renderes i malen. «Kartet i tekst» lages i `domene/`.
- **JS og CSP:** nøyaktig to egne JS-filer (`kart.js` og `forbedring.js`), uten rammeverk eller byggesteg. Alt virker uten JS, og serveren svarer med HTML (også fragmentet for «Nytt forslag»), aldri JSON. CSP: `default-src 'self'`, `img-src 'self' https://cache.kartverket.no`, `object-src 'none'`, `base-uri 'self'`, `form-action 'self'`, `frame-ancestors 'none'`. Ingen inline-skript og ingen `style`-attributter. Trenger Leaflet mer, begrunnes det i beslutningsloggen (`.memlog.md` for arkitekturen).
- **Konvensjoner:** domeneord på norsk uten æ/ø/å i identifikatorer. All formatering («ca. 1 t 35 min», «3,5 km totalt», «Grønn – lett») skjer i `domene/`. Alle POST følger PRG med CSRF. Tester kjøres med `python manage.py test` uten nettverk, med lagrede svar i `tests/fixtures/`. Én logger per modul.

## UX & Interaction Patterns

- **Tekst:** all brukertekst kommer fra Mikrotekst i `EXPERIENCE.md`, i jeg-form med du-tiltale. Tekster merket [ASSUMPTION] brukes, men markeres som foreløpige i en kodekommentar og i PR-en.
- **Grunnoppsett:** alle tokens fra `DESIGN.md` blir CSS-variabler i én fil, uten fargeverdier direkte i komponenter. Systemfonter. `lang="nb"`, `header`/`nav`/én `main`, sidetittel «… – Your Next Adventure». Flytende oppsett uten faste høyder og uten `overflow: hidden`. Fokusring 3 px `focus-ring` med 2 px avstand, aldri fjernet. Bevegelse av ved `prefers-reduced-motion`.
- **Komponenter:** høyst én primærknapp per visning, `aria-disabled` under innsending. Melding (info, advarsel, feil, suksess) står der saken gjelder og er aldri toast. Feltfeil står under feltet med «!», `aria-invalid` og `aria-describedby` (feil, så hjelpetekst), og fokus går til feltet. Turtypekort er en ekte radiogruppe.
- **Søk:** `h1` «Hvor lang tid har du?». Varighet (1–8 t i halvtimessteg), Dato (31 dager), Turtype og Startpunkt. Ingen fritekst i Epic 1.
- **Turforslag:** DOM-rekkefølgen er lik på alle bredder. Over 720 px sticky kart i venstre kolonne og Infokolonne til høyre; under 720 px én kolonne med kartet på ca. 60 % av skjermhøyden. Ved 1280 × 800 synes turnavn, turtype-treff, Faktarute og kart uten rulling. Forklaringspanelet er lukket som standard.
- **Kart:** kontroller på 44 px. Hjul og én finger ruller siden, Ctrl/Cmd + hjul zoomer, to fingre flytter kartet. Kartflaten har `tabindex="0"` og `role="region"`, og Tab fører alltid ut av kartet. Feiler flisene eller JS, vises en melding med «Prøv igjen», og krediteringen står fortsatt.
- **Tilstander:** Tilstandspanel (`h1`) erstatter turinnholdet ved ingen treff, gjest med nivåtak og «alle vist», og «Endre søk» er alltid med. Endringsforslag er `<button>` i små POST-skjemaer. Ved hver visningsendring oppdateres `document.title`, og fokus går til `h1`. «Nytt forslag» med JS bytter et HTML-fragment, med `aria-busy` og en `aria-live`-melding.

## Cross-Story Dependencies

- Byggerekkefølge: 1.1–1.10, så story 6.5 (kartfarger målt mot ekte fliser), så 1.11–1.12.
- 1.1 → alle. 1.2 krever 1.1 merget til `main` og at Hannah har opprettet Vercel og Neon i nettleseren. Byggesteget får `lastinn` i 1.6.
- 1.4 → 1.5 (beregningene går gjennom `domene/`) → 1.6 → 1.7. Datasettet fra 1.7 trengs for ekte data i 1.8–1.12.
- 1.8 → 1.9 → 1.10/1.11 → 1.12. `foresla_endringer` (1.12) brukes også i «alle vist» fra 1.11.
- Senere epics: lenken «Lag konto» og menypunktene kommer i Epic 2. Nivåtak for innloggede kommer i Epic 3. KI-begrunnelsen og KI-setningen i Forklaringspanelet kommer i 4.5, fritekst i 4.6–4.7. Turillustrasjonen (6.1) og `-dark`-tokenene (6.3) er P2.
