# Epic 1 Context: Ola finner en tur som passer tiden, på nett

<!-- Compiled from planning artifacts. Edit freely. Regenerate with compile-epic-context if planning docs change. -->

## Goal

En gjest åpner den publiserte siden, velger varighet og dato og får ett turforslag i Oslo og Bærum med kart, nivå, estimert tid og en begrunnelse fra mal. Gjesten kan be om nytt forslag og får konkret hjelp når ingenting passer. Story 1.1–1.7 er levert: appen kjører lokalt og på Vercel (med forhåndsvisning per PR), basismal og designtokens, gradering og tid, byggeskriptet, `lastinn` og en turdatabase med 15 kontrollerte turer. Neste steg er 1.8, utvalget og rangeringen i `domene/`. Etter det kommer søket, turforslaget, kartet, «Nytt forslag» og tilstandene uten treff. Alle senere epics bygger på denne kjerneflyten.

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

- **Utvalg:** bare turer med estimert tid ≤ varigheten (lik tid er med), turnivå ≤ nivåtaket og valgt turtype og startpunkt når de er oppgitt. Rangering i Epic 1: tid nærmest varigheten, deretter tur-ID, så samme søk alltid gir samme rekkefølge. Gjester og brukere uten historikk har grønt nivåtak. **Ingen tur over nivåtaket vises noen gang** (det testes).
- **Statuser:** `TREFF`; `TOPPTUR_ERSTATTET` (topptur valgt, ingen topptur passer, men en utsiktstur gjør det); `BARE_OVER_NIVATAK` (bare turer over nivåtaket passer, og ingen tur vises); `INGEN_TREFF` (ingenting passer, heller ikke over nivåtaket, og heller ingen utsiktstur ved topptur).
- **Senere utvidelse av rangeringen:** den fulle rekkefølgen er (1) ikke gåtte turer før gåtte, og gåtte med fornøydhet 1–2 sist, (2) fritekst-treff (P2), (3) nivåheving, (4) foretrukne turtyper (P2), (5) tid nærmest varigheten og (6) tur-ID. Epic 1 lager bare punkt 5 og 6, men utvalget må kunne utvides uten omskriving.
- **Nytt forslag:** neste tur i den frosne rangeringen, aldri en tur som alt er vist i søket. «Alle vist» gir et Tilstandspanel med «Start fra første forslag igjen». Ny innlasting beholder forslaget og listen over viste turer. Forslaget kan ikke deles som lenke.
- **Endringsforslag:** høyst tre, i fast rekkefølge: korteste lengre varighet som gir treff, «Velg startpunkt» og en annen turtype (marka, utsikt, topptur, ellers alle). Et forslag tas bare med når det endrede søket gir `TREFF`. Ved «alle vist» må det også gi minst én tur som ikke er blant de tidligere treffene. Meldingene lover aldri lengre eller hardere turer.
- **Begrunnelse uten KI-nøkkel:** reservemal som nevner varigheten og eventuell turtype, høyst 300 tegn, aldri fritekst, med merket «Begrunnelse fra mal».
- **Tid og nivå** leses fra databasen og beregnes aldri på nytt. Tiden vises alltid med «pauser ikke inkludert».
- **Turdatabasen:** 15 turer med to begrunnede unntak: topptur og utsikt har ingen grønn tur under 2 t. Det betyr noe for `TOPPTUR_ERSTATTET` og endringsforslagene. Tur-ID-er er permanente.
- **Stabilitet og sikkerhet:** feil input, manipulerte POST-er (ukjent startpunkt eller turtype, dato utenfor perioden) og dobbeltklikk krasjer aldri. All validering skjer på serveren. Alle tilstander gir et forslag eller neste steg.
- **Mobil og UU:** WCAG 2.1 AA, reflow ved 320 px og trykkflater på minst 44 × 44 px. På 360 px synes nivå, tid og turtype-treff uten rulling. Hele flyten virker med tastatur. Et automatisk UU-verktøy kjøres, og resultatet legges i PR-en.
- **Kreditering:** «© Kartverket» og «© OpenStreetMap contributors» med lenker, alltid synlig på kartet.
- **Sporbarhet:** kode, tester og commits viser til FR- og NFR-ID-er (f.eks. `# FR-5`).

## Technical Decisions

- **Lag:** `domene/` er ren Python som bare importerer standardbiblioteket, uten database, nett eller klokke (dagens dato sendes inn). Views, kommandoer og skript regner, filtrerer og formaterer aldri selv. Domenetester bruker ikke databasen. Ingen tester gjør nettverkskall.
- **Utvalg:** `domene.sok.Sok` (varighet, dato, valgfri turtype og valgfritt startpunkt; fritekst kommer i Epic 4) → `velg_turer(...)` → `Utvalg(status, rangerte_tur_ider)`. Funksjonen tar søket, turene (`domene.tur.Tur`) og nivåtaket. `domene.utvalg.foresla_endringer(sok, turer, nivatak, tidligere_treff=())` bruker `velg_turer` og brukes både ved ingen treff og ved «alle vist». Turtype filtreres i `domene/`, aldri med JSON-oppslag i databasen.
- **Søketilstand:** en gyldig POST lager en søke-ID (`secrets.token_urlsafe`) og sender til `/forslag/<sok_id>/`. `domene.okt.Soketilstand` (`til_dict`/`fra_dict`, datoer som ISO-strenger) har søket, `rangerte_tur_ider` (frosset), `viste_tur_ider`, `gjeldende_tur_id` og `nivaheving`, og senere KI-felt. Den ligger i økten under `"sok"`. Bare `turforslag/okt.py` leser og skriver den, alltid hele verdien, med de 10 nyeste søkene. `flush()`, `cycle_key()` og `clear()` brukes aldri. En ukjent søke-ID eller tur-ID gir Søk med meldingen «Turforslaget er ikke lenger tilgjengelig …».
- **Modeller:** `Startpunkt` (id som streng-PK, navn, lat, lon, hoyde_m) og `Tur` (FK `startpunkt` med PROTECT, `turtyper` som `JSONField` med `marka`/`utsikt`/`topptur`, geometri og høydeprofil i `JSONField`). Omgjøringen mellom modell og `domene.tur.Tur` ligger i `turforslag/`. `lastinn` sletter aldri, så startpunkter som ingen tur bruker kan bli liggende. Bygg startpunktvalget i 1.9 med det i tankene.
- **Database og publisering:** samme ORM og migreringer for SQLite lokalt og i tester og Neon Postgres på Vercel. Ingen rå SQL og ingen databasespesifikke felt. Byggingen på Vercel kjører `migrate` og så `lastinn`, så **migreringer må være bakoverkompatible**: de legger bare til, og nye felt er `null` eller har `db_default`. En ny pakke må inn både i `requirements.txt` og i `[project].dependencies` i `pyproject.toml`.
- **Kart:** Leaflet 1.9.4 vendret i `static/vendor/leaflet/`. Fliser fra `cache.kartverket.no` topo, zoom høyst 18. `kart.js` tegner bare GeoJSON fra `json_script`, uten egen logikk, med `attributionControl: false`. Krediteringen renderes i malen. «Kartet i tekst» lages i `domene/`.
- **JS og CSP:** nøyaktig to egne JS-filer (`kart.js` og `forbedring.js`), uten rammeverk eller byggesteg. Alt virker uten JS, og serveren svarer med HTML, aldri JSON. CSP: `default-src 'self'`, `img-src 'self' https://cache.kartverket.no`, `object-src 'none'`, `base-uri 'self'`, `form-action 'self'`, `frame-ancestors 'none'`. Ingen inline-skript og ingen `style`-attributter. Trenger Leaflet mer, utvides policyen med en begrunnelse.
- **Konvensjoner:** domeneord på norsk uten æ/ø/å i identifikatorer. All formatering («ca. 1 t 35 min», «3,5 km totalt», «Grønn – lett», «3 timer»/«2,5 timer») skjer i `domene/`. Alle POST følger PRG med CSRF. Testene kjøres med `python manage.py test`. Én logger per modul.

## UX & Interaction Patterns

- **Tekst:** all brukertekst kommer fra Mikrotekst i `EXPERIENCE.md`, i jeg-form med du-tiltale. Tekster merket [ASSUMPTION] brukes, men markeres som foreløpige i en kodekommentar og i PR-en.
- **Komponenter:** høyst én primærknapp per visning, `aria-disabled` under innsending. Meldinger står der saken gjelder og er aldri toast. Feltfeil står under feltet med «!», `aria-invalid` og `aria-describedby` (feil, så hjelpetekst), og fokus går til feltet. Turtypekort er en ekte radiogruppe.
- **Søk:** `h1` «Hvor lang tid har du?». Varighet (`<select>`, 1–8 t i halvtimessteg), Dato (31 dager, i dag forvalgt), Turtype («Alle turtyper» forvalgt) og Startpunkt (med hjelpetekst om Oslo-området). Ingen fritekst i Epic 1.
- **Turforslag:** DOM-rekkefølgen er lik på alle bredder: søkeoppsummering med «Endre søk», turnavn `h1`, Nivåmerke og Turtype-treff, meldinger, Formmerke, «Start: …», Faktarute og ut.no-lenke, kart med kreditering, KI-merke, Begrunnelse og Forklaringspanel (lukket), knapper og Kartbeskrivelse. Over 720 px står kartet sticky til venstre og Infokolonne til høyre. Under 720 px er det én kolonne med kartet på ca. 60 % av skjermhøyden. Ved 1280 × 800 synes turnavn, turtype-treff, Faktarute og kart uten rulling.
- **Kart:** kontrollene er 44 px. Hjul og én finger ruller siden, Ctrl/Cmd + hjul zoomer, og to fingre flytter kartet. Kartflaten har `tabindex="0"` og `role="region"`, og Tab fører alltid ut. Feiler flisene eller JS, vises en melding med «Prøv igjen», og krediteringen står fortsatt.
- **Tilstander:** Tilstandspanel (`h1`) erstatter turinnholdet ved ingen treff, gjest med nivåtak og «alle vist», og «Endre søk» er alltid med. Endringsforslag er `<button>` i små POST-skjemaer. Ved hver visningsendring oppdateres `document.title`, og fokus går til `h1`. «Nytt forslag» med JS bytter et HTML-fragment, med `aria-busy` og en `aria-live`-melding.

## Cross-Story Dependencies

- Byggerekkefølge: 1.8 → 1.9 → 1.10, så story 6.5 (kartfargene målt mot ekte fliser), så 1.11 → 1.12.
- 1.8 bygger på `domene.tur`, `domene.gradering` og `domene.tid` (1.4) og bruker de 15 turene fra 1.7 som realistiske data. 1.9 trenger `velg_turer` og lagrer den frosne rangeringen. 1.11 og 1.12 bruker statusene og `foresla_endringer`, også ved «alle vist».
- Senere epics: «Lag konto», menypunktene og `Registrering` kommer i Epic 2. Nivåtak for innloggede, nivåheving, gåtte turer i rangeringen og testbrukeren kommer i Epic 3. KI-begrunnelsen kommer i 4.5, og fritekst i 4.6–4.7. Turillustrasjonen (6.1) og mørk modus (6.3) er P2.
