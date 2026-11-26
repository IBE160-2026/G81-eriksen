# Epic 1 Context: Ola finner en tur som passer tiden, på nett

<!-- Compiled from planning artifacts. Edit freely. Regenerate with compile-epic-context if planning docs change. -->

## Goal

En gjest åpner den publiserte siden, velger varighet og dato og får ett turforslag i Oslo og Bærum med kart, nivå, estimert tid og en begrunnelse fra mal. Gjesten kan be om nytt forslag og får konkret hjelp når ingenting passer. Story 1.1–1.10 er levert: appen kjører lokalt og på Vercel, basismal og designtokens, gradering og tid, byggeskriptet, `lastinn`, 15 kontrollerte turer, utvalget og rangeringen (`Sok`, `velg_turer`), Søk med søketilstand i økten og forslagssiden `/forslag/<sok_id>/`, og ruten på kart med «Kartet i tekst». Story 6.5 er også levert: kartfargene er målt mot ekte fliser. Neste steg er 1.11 («Nytt forslag» og «alle vist»), og deretter 1.12 (endringsforslagene og statusene uten treff). Alle senere epics bygger på denne kjerneflyten.

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

- **Nytt forslag (1.11):**
  - «Nytt forslag» (POST med CSRF og PRG) viser neste tur i den frosne rangeringen og aldri en tur som alt er vist i dette søket.
  - Når alle treff er vist, kommer Tilstandspanel med `h1` «Du har sett alle turene som passer søket», antallet turer, «Start fra første forslag igjen» og «Endre søk». Endringsforslagene i panelet kommer i 1.12.
  - «Start fra første forslag igjen» viser første tur og starter listen over viste turer på nytt.
  - Ny innlasting gir samme forslag og samme liste over viste turer. Et nytt søk eller en annen fane påvirker ikke søket.
  - Et dobbeltklikk går bare ett steg videre.
  - Uten JS gir knappen en vanlig sideinnlasting med samme resultat.
  - Testene dekker rekkefølge, ingen gjentakelse, «alle vist», start på nytt og ny innlasting.
- **Endringsforslag (1.12):**
  - `foresla_endringer` gir høyst tre forslag i fast rekkefølge, med de andre valgene uendret:
    1. Korteste lengre varighet i halvtimessteg som gir treff. Ved 12 t blir det ikke noe forslag.
    2. «Velg startpunkt».
    3. Annen turtype: marka, utsikt, topptur, ellers «Prøv alle turtyper».
  - Et forslag tas bare med når det endrede søket gir `TREFF`. Ved «alle vist» må det også gi minst én tur utenom `tidligere_treff`.
  - Gir ingen endring treff, viser panelet bare «Endre søk» (og «Start fra første forslag igjen» ved «alle vist»).
  - Meldingene lover aldri lengre eller hardere turer.
- **Statuser:** `TREFF`, `TOPPTUR_ERSTATTET` (uansett grunn), `BARE_OVER_NIVATAK` og `INGEN_TREFF`. Ingen tur over nivåtaket (gjester: grønt) vises noen gang. Tid og nivå leses fra databasen og beregnes aldri på nytt.
- **Stabilitet:** manipulerte POST-er og dobbeltklikk krasjer aldri. All validering skjer på serveren. Alle tilstander gir et forslag eller et neste steg.
- **Mobil og UU:** WCAG 2.1 AA, reflow ved 320 px og trykkflater på minst 44 × 44 px. Hele flyten virker med tastatur. axe-core kjøres (injisert via DevTools, ingen pakke), og resultatet legges i PR-en.
- **Sporbarhet:** kode, tester og commits viser til FR-, NFR-, AR- og UX-DR-ID-er.

## Technical Decisions

- **Lag:**
  - `domene/` er ren Python uten Django, database, nett eller klokke.
  - Views regner, filtrerer og formaterer aldri. `turforslag/sokflyt.py` ligger mellom views og `domene/`, og views importerer ikke fra `domene/` (en test sjekker det).
  - Formatering ligger i `domene/tekst.py`, for eksempel varighet som «3 timer» og «2,5 timer».
  - Ingen tester gjør nettverkskall.
- **Søketilstand:**
  - `domene.okt.Soketilstand` har feltene `sok`, `status`, frosset `rangerte_tur_ider`, `viste_tur_ider`, `gjeldende_tur_id` og `nivaheving`. `fra_dict` tåler at senere felt mangler.
  - Den ligger i økten under `"sok"` som `sok_id → Soketilstand`, med de 10 nyeste søkene.
  - Bare `turforslag/okt.py` leser og skriver den, og den skriver alltid hele verdien på nytt.
  - «Nytt forslag», «Start fra første forslag igjen» og ny innlasting leser rangeringen fra økten og rangerer aldri på nytt.
  - En ukjent søke-ID eller tur sender til Søk med «Turforslaget er ikke lenger tilgjengelig. Søk på nytt for å få et forslag.».
  - `flush()`, `cycle_key()` og `clear()` brukes aldri.
  - Endringsforslag i 1.12 lager et nytt søk med en ny søke-ID. `Sok` er frozen, så `dataclasses.replace` kan brukes.
- **JS:**
  - Det finnes nøyaktig to egne JS-filer, `kart.js` og `forbedring.js`, uten rammeverk eller byggesteg.
  - `forbedring.js` gjør bare dette: «Nytt forslag» uten sideinnlasting, lasteindikator, sperre mot dobbeltklikk, tegnteller og «Vis passord».
  - «Nytt forslag» henter et HTML-fragment fra serveren (aldri JSON) og setter `document.title`, fokus og `aria-busy`. Etter byttet kalles `window.YNAKart.start(element)` fra `kart.js`, så kartet tegner den nye ruten fra den nye `json_script`-GeoJSON-en.
  - Alt virker uten JS.
- **CSP:** `default-src 'self'` og `img-src 'self' https://cache.kartverket.no`, uten inline-skript eller `style`-attributter. Nettleseren skal ikke melde CSP-brudd.
- **Kart:**
  - Leaflet 1.9.4 er vendret uendret.
  - `kart.js` tegner bare ferdig GeoJSON og har ingen fargeverdier, siden fargene ligger i CSS via `--map-*`-tokenene.
  - Kontrollene er knapper i malen, og krediteringen renderes på serveren.
  - Avviket for to-finger-flytting er ført i `.memlog.md`.
- **Database og pakker:**
  - Samme ORM brukes for SQLite og Neon, uten rå SQL.
  - Migreringer skal bare legge til.
  - En ny pakke må inn i både `requirements.txt` og `pyproject.toml`.
- **Konvensjoner:**
  - Norske identifikatorer uten æ/ø/å.
  - Alle POST følger PRG med CSRF.
  - CSS ligger i `static/css/side.css` med tokens.
  - Tester kjøres med `venv/Scripts/python.exe manage.py test`, og lint med `ruff check` og `ruff format --check`. Aldri `uv run`.

## UX & Interaction Patterns

- **Mikrotekst:** all brukertekst kommer ordrett fra Mikrotekst i `EXPERIENCE.md`, og den gjelder over mockups. [ASSUMPTION]-tekster markeres med `{# [ASSUMPTION] Mikrotekst #}` i malen og i PR-en. Tekster for 1.11:
  - Knappene «Nytt forslag» (primær) og «Registrer gjennomført tur» (sekundær, Epic 2). De fyller hele bredden på mobil.
  - Lastetekstene «Finner et nytt forslag …» [ASSUMPTION], «Finner en tur med utsikt som passer 2 timer …» [ASSUMPTION] og «Kart lastes …».
  - Overskriften «Du har sett alle turene som passer søket».
  - Ingressen «Det var fire turer med utsikt som passer 2 timer.» og «Vil du prøve noe annet?» [ASSUMPTION].
  - Knappene «Start fra første forslag igjen» og «Endre søk».
- **Tekster for 1.12:**
  - «Jeg fant ingen tur som passer søket ditt» og «Prøv å endre søket:».
  - Endringsforslagene «Prøv 3 timer», «Prøv 2,5 timer» [ASSUMPTION], «Velg startpunkt», «Prøv marka» og «Prøv alle turtyper» [ASSUMPTION].
  - «Ingen topptur passer søket ditt» og merket «Utsikt i stedet for topptur».
  - «Ingen grønne turer passer søket» med gjesteteksten. Lenken «Lag konto» kommer i Epic 2.
- **Henter nytt forslag (med JS):**
  - Det gamle forslaget står dempet, og knappen beholder fokus.
  - Visningen får `aria-busy="true"`, og lasteteksten leses opp i en `aria-live="polite"`-region utenfor beholderen.
  - Selve byttet meldes ikke i noen live-region.
  - Etter byttet er `document.title` lik «{Turnavn} – Turforslag – Your Next Adventure» (med Tilstandspanel: panelets overskrift), og fokus står på nytt `h1` (`tabindex="-1"`).
  - Kartet flyttes til den nye ruten, uten animasjon ved `prefers-reduced-motion`.
- **Lasteindikator:** viser søkeoppsummeringen, en tom kartflate og «Kart lastes …», uten spinner ved `prefers-reduced-motion`.
- **Tilstandspanel:**
  - Panelet erstatter turinnholdet ved ingen treff, nivåtak og «alle vist».
  - Overskriften er `h1`, og «Endre søk» er alltid med.
  - Endringsforslagene er `<button type="submit">` i små POST-skjemaer med CSRF, ikke lenker.
  - «Velg startpunkt» går til det forhåndsutfylte skjemaet med fokus på Startpunkt.
  - Meldinger er aldri toast.
- **Ett forslag om gangen:** ingen lister, karuseller eller uendelig rulling.
- **Turforslag:**
  - DOM-rekkefølgen er lik på alle bredder: søkeoppsummering, turnavn `h1` med Nivåmerke og Turtype-treff, meldinger, Formmerke, «Start: …», Faktarute, ut.no-lenke, kart med kreditering, begrunnelse, knapper og «Kartet i tekst».
  - Over 720 px står kartet sticky til venstre med Infokolonnen til høyre. Under 720 px er det én kolonne.
- **Kartlag:**
  - Rutelinjen `map-route` er plommelilla `#673A97`, 5 px på 9 px hvit kant.
  - Startmarkøren er en mosegrønn «S».
  - Fokusringen `map-focus-ring` har hvitt bånd på begge sider.
  - Krediteringen «© Kartverket» og «© OpenStreetMap contributors» står alltid synlig nede til høyre.

## Cross-Story Dependencies

- **Byggerekkefølge:** 1.11 → 1.12.
- **1.11** bygger på `forslag.html`, `sokflyt.py`, `okt.py` og `Soketilstand` fra 1.9 og på `kart.js` (`window.YNAKart.start`) fra 1.10.
- **1.12** bygger ut Tilstandspanelet fra 1.11 og kaller `foresla_endringer(sok, turer, nivatak, tidligere_treff=())` (bygger på `velg_turer`). Ved «alle vist» får funksjonen treffene i søket som `tidligere_treff`.
- **Senere:**
  - «Registrer gjennomført tur» og «Lag konto» kommer i Epic 2. Der beholder `login()` gjestens økt og forslag.
  - Nivåtak for innloggede, nivåheving og gåtte turer kommer i Epic 3.
  - KI-begrunnelsen kommer i 4.5.
  - Turforslag fra historikken (Epic 2) bytter «Nytt forslag» med «Finn en ny tur» og endrer ikke økten.
