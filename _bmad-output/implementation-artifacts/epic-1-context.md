# Epic 1 Context: Ola finner en tur som passer tiden, på nett

<!-- Compiled from planning artifacts. Edit freely. Regenerate with compile-epic-context if planning docs change. -->

## Goal

En gjest åpner den publiserte siden, velger varighet og dato og får ett turforslag i Oslo og Bærum med kart, nivå, estimert tid og en begrunnelse fra mal. Gjesten kan be om nytt forslag og får konkret hjelp når ingenting passer. Story 1.1–1.9 er levert: appen kjører lokalt og på Vercel, basismal og designtokens, gradering og tid, byggeskriptet, `lastinn`, 15 kontrollerte turer, utvalget og rangeringen (`Sok`, `velg_turer`), og nå Søk med validering, søketilstand i økten og forslagssiden `/forslag/<sok_id>/` med en enkel visning av statusene som ikke er vanlige treff. Neste steg er 1.10: ruten på kart og «Kartet i tekst». Etter det kommer story 6.5 (kartfargene målt), så «Nytt forslag» (1.11) og endringsforslagene (1.12). Alle senere epics bygger på denne kjerneflyten.

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

- **Turforslaget** viser rutelinjen på kart, nivå med farge og tekst og fast nivåforklaring, turtype-treff, form, «Start: …», total lengde, estimert tid med «pauser ikke inkludert», begrunnelse med KI-merke og Forklaringspanel, ut.no-lenke når den finnes, kreditering og «Kartet i tekst». «Kartet i tekst» lages av systemet fra turdata, aldri av KI, og nevner minst startpunkt, form, total lengde, høydemeter og laveste og høyeste punkt. Eksempel: «Rundtur på 3,5 km totalt fra Granvannet p-plass. Ruten stiger ca. 130 høydemeter, fra 180 til 310 moh.»
- **Kreditering:** «© Kartverket» og «© OpenStreetMap contributors» med understrekede lenker (OSM med `lang="en"`), alltid synlig på hvit flate nede til høyre på kartet, også uten JS og når flisene feiler.
- **Utvalg og statuser:** varighet 1–12 t i halvtimessteg (konstantene i `domene/sok.py`). Bare turer med tid ≤ varigheten og nivå ≤ nivåtaket (gjester: grønt). Rangering i Epic 1: tid nærmest varigheten, så tur-ID. **Ingen tur over nivåtaket vises noen gang.** Statusene er `TREFF`, `TOPPTUR_ERSTATTET` (uansett grunn; «Ingen topptur passer søket ditt» og merket «Utsikt i stedet for topptur»), `BARE_OVER_NIVATAK` og `INGEN_TREFF`.
- **Nytt forslag (1.11):** neste tur i den frosne rangeringen, aldri en som alt er vist. «Alle vist» gir Tilstandspanel med «Start fra første forslag igjen». Ny innlasting beholder forslaget og de viste turene. Dobbeltklikk går bare ett steg.
- **Endringsforslag (1.12):** høyst tre, i fast rekkefølge (korteste lengre varighet som gir treff, ingen ved 12 t; «Velg startpunkt»; annen turtype: marka, utsikt, topptur, ellers alle). Bare når det endrede søket gir `TREFF`, og ved «alle vist» bare når det gir en tur utenom treffene. Meldingene lover aldri lengre eller hardere turer.
- **Tid og nivå** leses fra databasen og beregnes aldri på nytt.
- **Stabilitet:** manipulerte POST-er og dobbeltklikk krasjer aldri. All validering skjer på serveren. Alle tilstander gir et forslag eller et neste steg.
- **Mobil og UU:** WCAG 2.1 AA, reflow ved 320 px, trykkflater minst 44 × 44 px. På 360 px synes nivå, tid og turtype-treff uten rulling. Hele flyten virker med tastatur. Et automatisk UU-verktøy (axe-core injisert via DevTools, ingen pakke) kjøres, og resultatet legges i PR-en.
- **Sporbarhet:** kode, tester og commits viser til FR-, NFR-, AR- og UX-DR-ID-er.

## Technical Decisions

- **Lag:** `domene/` er ren Python med bare standardbiblioteket, uten database, nett eller klokke. Views, kommandoer og skript regner, filtrerer og formaterer aldri. `turforslag/sokflyt.py` er laget mellom views og `domene/`; views importerer ikke fra `domene/`, og en test sjekker det. Ingen tester gjør nettverkskall.
- **Formatering** («ca. 1 t 35 min», «3,5 km totalt», form, høydemeter, søkeoppsummering) ligger i `domene/tekst.py`. «Kartet i tekst» lages i `domene/`. Laveste og høyeste punkt skal komme fra én funksjon som også Turillustrasjonen (6.1) skal bruke. Tur-retur lagres for én vei (geometri og verdier), og totaler regnes bare av funksjonene i `domene.tur`.
- **Søketilstand:** `domene.okt.Soketilstand` (`sok`, `status`, frosset `rangerte_tur_ider`, `viste_tur_ider`, `gjeldende_tur_id`, `nivaheving`; `fra_dict` tåler at senere felt mangler) ligger i økten under `"sok"`, med de 10 nyeste søkene. Bare `turforslag/okt.py` leser og skriver den, alltid hele verdien. `flush()`, `cycle_key()` og `clear()` brukes aldri. En ukjent søke-ID eller tur sender til Søk med «Turforslaget er ikke lenger tilgjengelig …». `foresla_endringer(sok, turer, nivatak, tidligere_treff=())` kommer i 1.12, og `Sok` er frozen, så `dataclasses.replace` kan brukes.
- **Kart (1.10):** Leaflet 1.9.4 vendret i `static/vendor/leaflet/`. Fliser fra `https://cache.kartverket.no/v1/wmts/1.0.0/topo/default/webmercator/{z}/{y}/{x}.png`, uten nøkkel, zoom høyst 18. `kart.js` får ferdig GeoJSON (WGS84 `LineString`) for én tur via `json_script` og tegner den; den filtrerer, beregner eller henter ingenting annet. `attributionControl: false`. Zoomgrenser og bevegelser (Ctrl/Cmd + hjul, to fingre) løses med Leaflets innebygde valg, uten plugin; avvik begrunnes i beslutningsloggen.
- **JS og CSP:** nøyaktig to egne JS-filer (`kart.js`, `forbedring.js`), uten rammeverk eller byggesteg. Alt virker uten JS, og serveren svarer med HTML, aldri JSON. CSP: `default-src 'self'`, `img-src 'self' https://cache.kartverket.no`, `object-src 'none'`, `base-uri 'self'`, `form-action 'self'`, `frame-ancestors 'none'`. Ingen inline-skript eller `style`-attributter. Trenger Leaflet mer, begrunnes utvidelsen i beslutningsloggen, og nettleseren skal ikke melde CSP-brudd.
- **Database og publisering:** samme ORM for SQLite lokalt og Neon Postgres på Vercel, ingen rå SQL. Migreringer må være bakoverkompatible (bare legge til). En ny pakke må inn i både `requirements.txt` og `[project].dependencies` i `pyproject.toml`.
- **Konvensjoner:** norske domeneord uten æ/ø/å i identifikatorer. Alle POST følger PRG med CSRF. CSS ligger i `static/css/side.css` med tokens. Tester og lint: `venv/Scripts/python.exe manage.py test` og `ruff check`/`ruff format --check`; aldri `uv run`.

## UX & Interaction Patterns

- **Tekst:** all brukertekst kommer ordrett fra Mikrotekst i `EXPERIENCE.md` (jeg-form, du-tiltale), som gjelder over mockups og wireframes. [ASSUMPTION]-tekster brukes og markeres med `{# [ASSUMPTION] Mikrotekst #}` i malen og i PR-en. Aktuelle for kartet: «Kartet kunne ikke lastes. Ruten er beskrevet i "Kartet i tekst".» med «Prøv igjen», «Bruk to fingre for å flytte kartet» og «Kart lastes …».
- **Turforslag:** DOM-rekkefølgen er lik på alle bredder: søkeoppsummering, turnavn `h1` med Nivåmerke og Turtype-treff, meldinger, Formmerke/«Start: …»/Faktarute/ut.no, (Turillustrasjon, P2), kart med kreditering, KI-merke/Begrunnelse/Forklaringspanel, knapper, Kartbeskrivelse. Over 720 px: kartet sticky til venstre, Infokolonne (ca. 340–470 px) til høyre, Kartbeskrivelse under kartet. Under 720 px: én kolonne, kartet innenfor sidemargen med 1 px kant og ca. 60 % av skjermhøyden. Ved 1280 × 800 synes turnavn, Turtype-treff, Faktarute og kart uten rulling, uten faste høyder og uten `overflow: hidden`.
- **Kart:** «Kartet i tekst»-lenke oppe til venstre (hopper til Kartbeskrivelse), «Vis hele ruten» og zoom + og − oppe til høyre (44 px), målestokk nede til venstre, kreditering nede til høyre. Norske tekster på kontrollene. Kartflaten har `tabindex="0"`, `role="region"` og `aria-label="Kart over {turnavn}"`; piltaster flytter, + og − zoomer, Tab fører alltid ut, og markørene kan ikke få fokus. Hjul og én finger ruller siden (med hint), Ctrl/Cmd + hjul zoomer, to fingre flytter. Ingen animasjon ved `prefers-reduced-motion`. Feiler flisene eller JS, viser kartflaten Melding (info) med «Prøv igjen» og lenke til Kartbeskrivelse, og resten vises som vanlig.
- **Kartlag:** alt oppå flisene bruker kartlag-tokenene, like i lys og mørk modus: rutelinje `map-route` (plommelilla `#6A3D9A`, 5 px på 9 px hvit kant), startmarkør `map-marker-start` (mosegrønn sirkel med «S» og 2 px hvit kant), hvit kartlagsflate med mørk tekst og understrekede lenker, og `map-focus-ring` (3 px med 3 px hvit ytre kant). Flisfargene i kontrasttabellen er antatte til story 6.5 måler dem.
- **Kartbeskrivelse:** kort med `h2` «Kartet i tekst» og datagenerert tekst.
- **Tilstander:** Tilstandspanel (`h1`) erstatter turinnholdet ved ingen treff, nivåtak og «alle vist», og «Endre søk» er alltid med. Sidetittel «{tittel} – Your Next Adventure»; for forslag «{Turnavn} – Turforslag – Your Next Adventure». Ved hver visningsendring oppdateres `document.title`, og fokus går til `h1`. «Nytt forslag» med JS bytter et HTML-fragment med `aria-busy` og en `aria-live`-melding, og kartet skal da vise den nye ruten. Meldinger er aldri toast.

## Cross-Story Dependencies

- Byggerekkefølge: 1.10 → 6.5 (kartfargene målt mot ekte fliser, kan justere `map-route`/`map-marker-start` bare i `DESIGN.md` og token-fila) → 1.11 → 1.12.
- 1.10 bygger på forslagssiden fra 1.9 (`forslag.html`, `sokflyt.py`, `domene/tekst.py`) og geometrien og høydeprofilen fra turdatabasen (1.5–1.7). 1.11 må la `kart.js` tegne den nye ruten etter fragmentbyttet. 1.11 og 1.12 bygger ut Tilstandspanelet og bruker `foresla_endringer`, også ved «alle vist».
- Senere: «Lag konto» og registrering i Epic 2; nivåtak for innloggede, nivåheving og gåtte turer i rangeringen i Epic 3 (først da slår `BARE_OVER_NIVATAK` og flere topptur-kanter inn med ekte data); KI-begrunnelsen i 4.5 og fritekst i 4.6–4.7; Turillustrasjon (6.1, bruker samme laveste/høyeste-funksjon som «Kartet i tekst») og mørk modus (6.3) er P2.
