# Epic 6 Context: Rikere turforslag og klar for sensor

<!-- Compiled from planning artifacts. Edit freely. Regenerate with compile-epic-context if planning docs change. -->

## Goal

Epic 6 gjør turforslaget rikere og prosjektet klart for innlevering. P2-delen er turillustrasjon (6.1), tur 16–30 (6.2), mørk modus (6.3) og fremgang mot neste nivå (6.4). Story 6.5–6.8 er P1 og kuttes aldri. 6.5 måler kartfargene mot ekte Kartverket-fliser og bygges rett etter kartet i 1.10, før 1.11. Til slutt kommer UU- og mobiltesten (6.6, SM-4), brukertesten med nybegynnere (6.7, SM-1) og README testet i et rent miljø (6.8). Story 1.1–1.10 er levert, og 6.5 er neste story. Den gjør målingen og eventuelle tokenjusteringer. Ingen ny funksjon kommer til.

## Stories

- Story 6.1 (P2): Turforslaget viser en turillustrasjon
- Story 6.2 (P2): Turdatabasen får tur 16–30
- Story 6.3 (P2): Siden følger mørk modus på enheten
- Story 6.4 (P2): Historikken viser fremgangen mot neste nivå
- Story 6.5: Kartfargene er målt mot ekte kartfliser
- Story 6.6: UU og mobil er testet og dokumentert
- Story 6.7: Nybegynnere har testet kjerneflyten
- Story 6.8: Repoet og README er klare for sensor

## Requirements & Constraints

- **Kartfarger (6.5):** `map-route`, `map-marker-start` og `map-focus-ring` måles mot ekte Kartverket topo-fliser i skog, myr, vann og bebyggelse. Hver flate måles med fargeplukker på minst to steder i turområdene og på minst to zoomnivåer som turforslaget bruker. Kontrasten regnes med WCAG relativ luminans og må være minst 3:1 (WCAG 1.4.11). `map-marker-start` må i tillegg ha minst 4,5:1 mot den hvite «S»-en. Målingen krever ingen ny pakke i `requirements.txt` eller `requirements-dev.txt`.
- **Dokumentasjon (6.5):** lag en tabell i `docs/` med flisadressene, de målte fargene og kontrastforholdene for hvert token mot hver flate. Legg ved skjermbilder av ruten mot stier, veier og vann, med «© Kartverket» synlig, og en kort vurdering av om ruten skiller seg fra dem. Holder alle forholdene, erstattes de antatte verdiene i tabellen Kontrastmål i `DESIGN.md` med de målte, og fotnoten forteller når og hvordan de ble målt. Det åpne punktet «Kartfliser og målinger» i `EXPERIENCE.md` merkes som løst, med dato og lenke til målingen.
- **Antatte verdier som skal erstattes:** skog `#CDE6B4` og vann `#A8D3EE` er antatte flisfarger. OSM-fargene land `#F2EFE9` og skog `#ADD19E` er stedfortredere. Dagens forhold for `map-route` er 7,6 mot hvit kant, 6,7 mot OSM land, 4,5 mot OSM skog, 5,7 mot skog og 4,8 mot vann. For `map-marker-start` er de 8,7 / 7,6 / 5,1 / 6,4 / 5,5, og `map-focus-ring` har 4,5 mot sin hvite ytre kant. Myr og bebyggelse er ikke målt ennå.
- **Ved under 3:1:** endre tokenverdien bare i `DESIGN.md` (frontmatter, Kartlag og Kontrastmål) og i token-fila `turforslag/static/css/tokens.css`, ingen andre steder. Ny `map-route` må fortsatt være plommelilla, verken rød, oransje eller blå, og ha minst 3:1 mot alle flatene og den hvite kanten. Produkteier godkjenner endringen i PR-en, og PR-en har skjermbilder av ruten i skog, myr, vann og bebyggelse før og etter.
- **Mørk modus:** flisene og kartlaget er like i begge moduser. Målingen i 6.5 gjelder derfor også for 6.3, som ikke trenger noen ny måling.
- **UU og mobil:** målet er WCAG 2.1 AA, med 4,5:1 for tekst og 3:1 for komponenter som ikke er tekst. Siden skal ha reflow ved 320 px og virke ned til 360 px uten sidelengs rulling. Trykkflatene er minst 44 × 44 px. Kjerneflyten skal virke med bare tastatur, og kartet holder ikke på fokus. Informasjon vises aldri bare med farge. Det automatiske UU-verktøyet er axe-core, injisert via DevTools uten pakke, og resultatet legges i PR-en.
- **Kreditering:** «© Kartverket» og «© OpenStreetMap contributors» står på kartet, også på skjermbildene i dokumentasjonen.
- **P2-kutt** skjer i fast rekkefølge: FR-17.1 (6.4), så mørk modus (6.3), så turillustrasjonen (6.1). Tur 16–30 er også P2. Hvert kutt føres i PRD §9 og i endringsloggen, og siden får ikke tomrom etter det som er kuttet.
- **Sporbarhet:** kode, tester, commits og PR-er viser til FR-, NFR-, AR- og UX-DR-ID-er. For 6.5 gjelder UX-DR35, NFR-4, NFR-7 og UX-DR1.

## Technical Decisions

- **Fliskilde:** `https://cache.kartverket.no/v1/wmts/1.0.0/topo/default/webmercator/{z}/{y}/{x}.png`, uten nøkkel og med zoom høyst 18. URL-en har raden (`y`) før kolonnen (`x`). Tabellen skal likevel oppgi `z/x/y`, så rekkefølgen må gjøres om riktig.
- **Leaflet 1.9.4** ligger i `static/vendor/leaflet/`. `kart.js` tegner bare ferdig GeoJSON for én tur og kjører `fitBounds` på hele ruten. Rutelinjen er to polylinjer med `className`, 5 px plommelilla oppå en 9 px hvit kant. Startmarkøren er en mosegrønn sirkel med «S» og 2 px hvit kant. CSS-en henter fargene fra `--map-*`-variablene i `tokens.css`. `attributionControl` er av.
- **CSP:** `default-src 'self'`, `img-src 'self' https://cache.kartverket.no`, `object-src 'none'`, `base-uri 'self'`, `form-action 'self'` og `frame-ancestors 'none'`. Maler har ingen inline-skript og ingen `style`-attributter. Fargemålingen skal ikke endre policyen. En utvidelse krever en begrunnelse i beslutningsloggen.
- **Tokener:** fargeverdier står bare i token-fila, og en test sjekker det. Kartlag-tokenene har ingen `-dark`-par.
- **Ingen nettverkskall i tester.** Kontrastberegningen kan gjøres manuelt eller med et lite skript, men uten ny avhengighet.
- **Tester og lint** kjøres med `venv/Scripts/python.exe manage.py test`, `ruff check` og `ruff format --check`. Bruk aldri `uv run`.
- **6.1:** illustrasjonen regnes ut av en ren funksjon i `domene/`, og laveste og høyeste punkt kommer fra samme funksjon som «Kartet i tekst». Den er inline SVG med farger fra CSS-klasser og uten `style`, med `aria-hidden` og `figure`/`figcaption`.
- **6.2:** én tur per commit, aldri over 30 turer, og eksisterende tur-ID-er endres aldri. Ingen test forutsetter nøyaktig 15 turer.
- **6.3:** `-dark`-tokenene brukes via `prefers-color-scheme`, med `color-scheme` satt og uten bryter eller JS. Kartflisene får ikke filter.
- **6.4:** fremgangen regnes ut av en ren funksjon i `domene.niva` fra `NivaStatus`, uten nye felt.

## UX & Interaction Patterns

- **Kartlag:** alt oppå flisene bruker kartlag-tokenene, likt i lys og mørk modus. Det gjelder rutelinjen, startmarkøren, «Kartet i tekst»-lenken, «Vis hele ruten», zoom, målestokken, krediteringen og fokusringen. Kartlagsflaten `map-overlay-surface` er helt hvit uten gjennomsiktighet, med mørk tekst (`map-overlay-text`, 14,9:1) og mosegrønne, understrekede lenker (`map-overlay-link`, 8,7:1). Fokusringen på kartet er 3 px `map-focus-ring` med 3 px hvit ytre kant.
- **Dagens verdier:** `map-route` er `#6A3D9A`, `map-marker-start` og `map-overlay-link` er `#355146`, `map-focus-ring` er `#B0624A` og `map-overlay-text` er `#1F2A22`.
- **Farger skal ikke forveksles:** rutelinjen skal ikke ligne stier og veier (rød og oransje), vann eller nivået Blå (blå). Nivåfargene og rutelinjen er de eneste mettede fargene i produktet.
- **Tekst** kommer ordrett fra Mikrotekst i `EXPERIENCE.md`. Tekster merket [ASSUMPTION] godkjennes av produkteier, senest i 6.8.

## Cross-Story Dependencies

- **Byggerekkefølge:** 1.10 (levert), så 6.5, så 1.11–1.12, Epic 2, 3.1–3.4 og 4.1–4.5. P2 bygges i rekkefølgen 3.5, Epic 5, 4.6–4.7, 6.1, 6.3 og 6.4. Story 6.6–6.8 kommer helt til slutt.
- 6.5 bygger på kartet fra 1.10 og tokenene fra 1.3. En justert tokenverdi slår inn overalt via `--map-*`.
- 6.3 bruker målingen fra 6.5. 6.1 og 6.2 må beholde foldmålet ved 1280 × 800 og testbrukerens oppførsel fra 3.4.
- 6.6 kjører UU-verktøyet i begge moduser hvis 6.3 er levert. 6.8 lenker til dokumentasjonen fra 6.5–6.7 i README.
