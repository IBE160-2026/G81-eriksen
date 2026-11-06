---
title: Your Next Adventure — Tilgjengelighetsgjennomgang (WCAG 2.1 AA)
status: review
created: 2026-11-06
reviewer: adversarial tilgjengelighetsgjennomgang (BMAD UX)
scope:
  - DESIGN.md
  - EXPERIENCE.md
  - mockups/direction-stille-kart.html
  - mockups/direction-turkort.html
method: Lesing av spinene mot WCAG 2.1 AA. Kontrastverdier er regnet på nytt fra hex-tokenene (WCAG relativ luminans). Flisfarger er antatte (se Vedlegg) fordi ekte Kartverket-fliser ikke finnes i spinene.
---

# Tilgjengelighetsgjennomgang — WCAG 2.1 AA

## Samlet vurdering

Spinene har et uvanlig godt gulv for tekstkontrast, fargebruk på nivå og status, skjemaetiketter og «ingen fokusfelle i kartet». Men de oppfyller **ikke** NFR-4 slik de står. Reflow ned til 320 CSS px er ikke spesifisert (bare 200 % zoom), og mørk modus gjør teksten i krediteringen og flere kartelementer uleselige (1,2:1). I tillegg er kartet, sideovergangene og statusmeldingene etter navigering de stedene der en ærlig implementasjon av spinene vil feile en manuell WCAG-test.

**Antall funn:** Kritisk 2 · Høy 6 · Middels 11 · Lav 10

---

## Kritisk

### K1. Reflow ved 320 CSS px er ikke spesifisert, og faste bredder bryter den
- **WCAG:** 1.4.10 Reflow (AA), 1.4.4 Endre tekststørrelse (AA)
- **Hvor:** EXPERIENCE.md → Responsive & Platform, Accessibility Floor («virker ved 200 % zoom»); DESIGN.md → Layout & Spacing, `spacing.info-column-width` (470), `form-column-width` (560), `side-illustration-width` (440), `page-margin` (64)
- **Scenario:** En svaksynt bruker på 1280 px-skjerm zoomer til 400 % (= 320 CSS px). Tabellen sier «Infokolonnen beholder bredden» og stopper ved «< ca. 720 px». Infokolonnen på 470 px, sidemarg 2 × 64 px, Varighet + Dato side om side, tre Turtypekort side om side, tre Faktaruter side om side og en toppmeny med logo og tre menypunkter gir horisontal rulling på hele siden. Spinen sier eksplisitt at stablingen «bare finnes for at zoom skal virke» og at 200 % er målet. 1.4.10 krever 320 px. Desktop-først gir ikke unntak.
- **Fix:** Skriv inn i Accessibility Floor og Responsive & Platform: «Alt innhold virker uten horisontal rulling ved 320 CSS px bredde (400 % zoom på 1280).» Alle faste bredder blir `max-width`, og infokolonnen blir `width: 100%` i stablet oppsett. Sidemargen faller til 16 px under ca. 480 px. Faktaruter, Turtypekort og Varighet/Dato brytes til én kolonne. Toppmenyen brytes på flere linjer eller samles, uten at noe skjules. Kart og Historikktabell er 2D-innhold og kan rulle **i egen beholder**, men siden selv kan ikke rulle sidelengs. Dette er ikke et mobildesign. Det er et WCAG-krav.

### K2. Mørk modus gjør kreditering, målestokk, startmarkør og fokusring på kartet uleselige
- **WCAG:** 1.4.3 Kontrast (AA), 1.4.11 Ikke-tekstlig kontrast (AA), 2.4.7 Synlig fokus (AA)
- **Hvor:** DESIGN.md → `components.kreditering` (bakgrunn `rgba(255,255,255,.92)` hardkodet, `foreground: {colors.text}`, `link-color: {colors.primary}`), Components-innledningen («Hver komponent bruker `-dark`-parene i mørk modus»), `components.kart`, `components.fokusring`; EXPERIENCE.md → Foundation («Kartflisene forblir lyse»)
- **Scenario:** Systemet står i mørk modus. Kartflisene er lyse, men tokenene bytter:
  - Krediteringen: `text-dark` #E8ECE4 på nesten hvit stripe = **1,2:1**. Lenkene i `primary-dark` #ADCEC0 på hvitt = **1,7:1**. Krediteringen er pålagt (NFR-7) og er tekst.
  - Målestokken: ingen token er gitt. Arver den `text`, blir den `text-dark` på lyse fliser (**ca. 1,0:1**).
  - Startmarkøren «S» i `primary-dark` på lys flis = **1,5:1**.
  - Fokusringen på zoomknappene og krediteringslenkene: `focus-ring-dark` #F0B79C mot lys flis = **1,0–1,8:1**. En tastaturbruker ser ikke hvor fokus er på kartet.
- **Fix:** Innfør en egen, modusløs kartgruppe i DESIGN.md (som `map-route`, uten `-dark`): `map-overlay-surface` #FFFFFF, `map-overlay-text` = `text` lys, `map-overlay-link` = `primary` lys, `map-start` = `primary` lys, og en fokusring for kart som er `focus-ring` lys med hvit kant (for eksempel `outline: 3px solid #B0624A` + `box-shadow: 0 0 0 5px #FFFFFF`). Alt som ligger oppå flisene bruker disse i begge moduser. Skriv det inn som regel under Colors: «Alt som ligger oppå kartflisene bruker lyse verdier, også i mørk modus.» Zoomknappene kan beholde `surface-dark` fordi kanten mot flisen da får høy kontrast, men det må velges bevisst.

---

## Høy

### H1. Rutelinje, utsiktsmarkør og lys fokusring er under 3:1 mot skog og vann
- **WCAG:** 1.4.11 Ikke-tekstlig kontrast (AA), 2.4.7 Synlig fokus (AA)
- **Hvor:** DESIGN.md → `colors.map-route` [ASSUMPTION], kontrasttabellen («3,4 mot plassholder, ikke verifisert»), `components.kart` (utsiktsmarkør i `{colors.accent}`); EXPERIENCE.md → Åpne punkter
- **Scenario:** Oslomarka er nesten bare skog og vann. Med antatte flisfarger (se Vedlegg) får `map-route` #C0694A **2,3:1** mot OSM-skog, **2,9:1** mot lys skog og **2,5:1** mot vann. Ruten er selve informasjonen på kartet, og den forsvinner der den går gjennom skog. I tillegg tegner Kartverket stier som rød stiplet linje og veier i oransje. En terrakotta rute kan forveksles med kartets egne linjer. Utsiktsmarkøren i `accent` er **1,5–2,2:1** mot flisene. Etiketten «▲ Utsikt» har ingen tekstfarge i spinen (mocken bruker #6B3A22, som ikke er en token). Hvis den arver `accent`, er det tekst i aksentfarge, noe DESIGN.md selv forbyr. Den lyse fokusringen er **2,6:1** mot OSM-skog og **2,8:1** mot vann, så fokus på zoomknappene kan forsvinne.
- **Fix:** Gjør hvit kant (casing) til en del av komponenten, slik mocken gjør (10 px hvit under 5 px rute). Da er kontrasten rute mot hvit = **3,9:1** og hvit mot flis (mørkere flater) ≥ 3:1. Legg inn `map-route-casing: #FFFFFF` og bredder i `components.kart`. Velg en rutefarge som ikke er rød eller oransje (for eksempel en mørk lilla eller blå) etter at den er målt mot ekte Kartverket-fliser i skog, myr, vann og bebyggelse. Gi utsiktsmarkøren hvit fyll med `primary` kant (som i mocken) og etiketten `text` på hvit pille. Fokusringen på kartelementer får hvit ytre kant (se K2). Flytt «ikke verifisert» fra Åpne punkter til et krav om måling før arkitektur.

### H2. Sidetitler og fokus ved sideoverganger er ikke spesifisert
- **WCAG:** 2.4.2 Sidetittel (A), 2.4.3 Fokusrekkefølge (A), 4.1.3 Statusmeldinger (AA)
- **Hvor:** EXPERIENCE.md → Information Architecture, Interaction Primitives («uten å laste siden på nytt»), Accessibility Floor
- **Scenario:** Ordet «sidetittel» eller `<title>` finnes ikke i spinene. Turforslaget byttes uten sidelasting, så en klientruting er sannsynlig. En skjermleserbruker trykker «Finn en tur». Fanen heter fortsatt «Your Next Adventure», fokus står på en deaktivert knapp som har forsvunnet, og ingenting leses opp før lastingen er ferdig. Det samme skjer ved Turforslag → Logg inn, Logg inn → Registrer gjennomført tur (FR-14-omdirigeringen), Registrer → Historikk, Konto → Bekreft sletting og Bekreft sletting → Søk. Floor dekker bare «Nytt forslag» og «lasting ferdig».
- **Fix:** Legg til en tabell over sidetitler, for eksempel «Hvor lang tid har du? – Your Next Adventure», «Granåsen rundt – Turforslag – Your Next Adventure», «Registrer gjennomført tur: Granåsen rundt – …», «Bekreft sletting av konto – …». Tittelen oppdateres ved «Nytt forslag» og ved tilstandspanel («Ingen tur passer – …»). Skriv én regel for alle overganger: «Ved hver visningsendring settes `document.title`, og fokus flyttes til visningens `h1` (`tabindex="-1"`).» Nettleserens Tilbake skal gi fokus tilbake til elementet som startet overgangen, eller til `h1`.

### H3. Suksessmeldinger etter navigering blir ikke lest opp
- **WCAG:** 4.1.3 Statusmeldinger (AA)
- **Hvor:** EXPERIENCE.md → Component Patterns: Melding («`role="status"`»); State Patterns: Registrert, Konto slettet; UJ-2 trinn 4, UJ-3 trinn 5
- **Scenario:** Ola registrerer turen og lander i Historikk. Meldingen «Turen er registrert i historikken din.» rendres sammen med den nye visningen med `role="status"`. Live-regioner som finnes allerede når innholdet settes inn, leses ikke opp av NVDA, JAWS eller VoiceOver. Det samme gjelder «Kontoen din er slettet.» på Søk. Klimakset i UJ-3 («Han ser tydelig at alt er borte») når ikke en skjermleserbruker. Ved FR-14 («Turforslaget er tatt vare på.») gjelder det samme.
- **Fix:** Skriv at meldinger som følger med en navigering, enten (a) får fokus selv (`tabindex="-1"` og plassert rett under `h1`), eller (b) settes inn i en live-region som allerede fantes i DOM-en, etter at visningen er rendret. Velg én metode og bruk den overalt. Kombiner den med H2 slik at fokus og opplesing ikke krangler.

### H4. Fast høyde til folden bryter zoom, tekstavstand og utfellbart innhold
- **WCAG:** 1.4.4 Endre tekststørrelse (AA), 1.4.10 Reflow (AA), 1.4.12 Tekstavstand (AA)
- **Hvor:** DESIGN.md → Layout & Spacing («Kolonnen fyller høyden til folden (ca. 660 px)», «Over folden må dette synes …»), `skjemafelt.height: 46px`, `spacing.header-height: 60px`, Do's and Don'ts («Hold illustrasjon, kart og Turtype-treff over folden»); mockene bruker `height:660px` og `height:200px`
- **Scenario:** Mange bærbare kjører 1366 × 768 med 125 % skalering, altså ca. 1093 × 614 CSS px, og zoom på 150 % gir 853 × 533. Begge holder to kolonner (≥ 720 px), men infokolonnen må nå få plass til ca. 660 px innhold i ca. 470 px høyde. Med fast høyde blir innholdet enten klippet (tap av innhold) eller får en indre rulleflate som ikke alltid kan nås med tastatur. Bokmerkelet for tekstavstand (linjehøyde 1,5, avsnitt 2×, bokstav 0,12 em og ord 0,16 em) gjør det samme med fast feltheight 46 px, faste 36 px kartknapper, 60 px toppmeny og piller. Når Forklaringspanel åpnes, vokser kolonnen ut av rammen.
- **Fix:** Skriv at folden er et **designmål på 1280 × 800 ved 100 %** og aldri en høydebegrensning. Infokolonnen bruker naturlig høyde (`min-height`, aldri `height` med `overflow: hidden`). Kartet kan være `position: sticky` ved siden av. Felt, knapper, toppmeny og merker bruker `min-height` og padding, ikke fast høyde. Legg inn en testregel i Accessibility Floor: «Ingen tekst klippes eller overlapper med tekstavstand etter 1.4.12.»

### H5. Turtypekort kan ikke velges bort med tastatur
- **WCAG:** 2.1.1 Tastatur (A), 4.1.2 Navn, rolle, verdi (A)
- **Hvor:** EXPERIENCE.md → Component Patterns: Turtypekort («Velg null eller én … virker som en radiogruppe med piltaster. Klikker man på et valgt kort, fjernes valget [ASSUMPTION]»)
- **Scenario:** Ola velger Utsikt med piltastene og ombestemmer seg. I en radiogruppe velger piltastene alltid et nytt alternativ, og Mellomrom på et valgt alternativ gjør ingenting. «Ingen turtype» kan bare nås med mus (klikk på valgt kort). Skjermlesere melder «radioknapp, valgt, 2 av 3» og gir ingen hint om at valget kan fjernes. «Valgt»-teksten blir også en del av navnet («Utsikt Valgt, radioknapp, valgt»).
- **Fix:** Legg til et fjerde valg, «Alle turtyper» eller «Ingen bestemt», som er valgt som standard. Da er det en ekte radiogruppe uten skjult oppførsel. Alternativt brukes tre veksleknapper med `aria-pressed` som utelukker hverandre, men det er en svakere løsning. «Valgt» får `aria-hidden="true"`, fordi tilstanden kommer fra `checked`.

### H6. `input-border` er under 3:1 mot bakgrunn og alternativ flate, og har ingen margin mot `surface`
- **WCAG:** 1.4.11 Ikke-tekstlig kontrast (AA)
- **Hvor:** DESIGN.md → `colors.input-border` [ASSUMPTION], kontrasttabellen («`input-border` mot `surface` 3,0»), `components.skjemafelt`, `turtypekort`, `valggruppe`, Layout & Spacing (bakgrunnen på skjemasider er ikke bestemt)
- **Scenario:** Regnet på nytt: #8C978F mot `surface` = **3,00:1** (akkurat på grensen, før antialiasing av en 1 px kant). Mot `background` #F3F3EC = **2,72:1** og mot `surface-alt` = **2,48:1**. Søket i Turkort og skjemasidene ligger på sidens `background`. Feltets innside (`surface`) skiller seg bare 1,1:1 fra bakgrunnen, så kanten er det eneste som viser at feltet finnes, og den må ha 3:1 mot det som ligger rundt. Turtypekortene har samme kant mot sidebakgrunnen.
- **Fix:** Mørkne `input-border` til ca. #7A857D (gir ≥ 3,5:1 mot `background`, regn på nytt) eller legg skjemaene på et `surface`-kort, og skriv hvilken flate hvert skjema ligger på. Legg paret `input-border` mot `background` og `surface-alt` inn i kontrasttabellen.

---

## Middels

### M1. Leaflet-standarder er på engelsk og gir ukontrollerte fokusstopp
- **WCAG:** 3.1.2 Språk i deler (AA), 4.1.2 Navn, rolle, verdi (A), 2.4.3 Fokusrekkefølge (A)
- **Hvor:** EXPERIENCE.md → Component Patterns: Kart, Kreditering; Foundation (Leaflet nevnt)
- **Scenario:** Leaflet gir zoomknappene `aria-label`/`title` «Zoom in» / «Zoom out», markørene får `alt="Marker"` og er fokuserbare, og krediteringen får en «Leaflet»-lenke. En norsk skjermleser leser engelsk med norsk uttale, og tab-rekkefølgen i kartet får stopp spinen ikke kjenner til. Mocken setter kartkontrollene til `aria-hidden="true"`, noe som ville gjort knappene usynlige for skjermlesere.
- **Fix:** Spesifiser navnene «Zoom inn» og «Zoom ut», markørnavnene «Start og mål: Granvannet p-plass» og «Utsiktspunkt: Granåsen, 410 moh» (eller markørene som ikke-fokuserbare dekor, fordi Kartbeskrivelse dekker dem), og fjern Leaflet-prefikset eller gi det norsk tekst. «OpenStreetMap contributors» får `lang="en"`. Skriv `<html lang="nb">` inn i Foundation (mockene har det, men spinene sier det ikke).

### M2. Kartet kan ikke panoreres med tastatur, og `aria-describedby` på kartet virker ikke
- **WCAG:** 2.1.1 Tastatur (A), 1.3.1 Info og relasjoner (A), 1.1.1 Ikke-tekstlig innhold (A)
- **Hvor:** EXPERIENCE.md → Component Patterns: Kart («dras og zoomes med knappene + og −», «viser til Kartbeskrivelse med `aria-describedby`»), Kartbeskrivelse
- **Scenario:** Musbrukeren drar kartet. Tastaturbrukeren kan bare zoome, og zoom skjer rundt midten, så når hen zoomer inn, havner start eller utsikt utenfor bildet uten vei tilbake. `aria-describedby` på en `div` uten rolle leses ikke av de fleste skjermlesere. Innholdet i Kartbeskrivelse er bare «en kort beskrivelse av ruten», så det er ikke sikret at det gir det kartet gir.
- **Fix:** Behold Leaflets tastaturpanorering (kartflaten får `tabindex="0"`, piltaster panorerer og Tab går videre, altså ingen felle) og gi kartflaten Fokusring. Legg til en knapp «Vis hele ruten». Gi kartet `role="region"` og `aria-label="Kart over Granåsen rundt"` og en synlig lenke «Kartet i tekst» som hopper til beskrivelsen. Spesifiser minimumsinnholdet i Kartbeskrivelse: startpunkt (navn og hvordan man finner det), form og retning, utsiktspunkt med avstand, høyeste punkt og total lengde. Skriv om den genereres fra data eller av KI. Hvis KI skriver den, gjelder KI-merket også her.

### M3. Overskriftsnivåer og landemerker er ikke definert
- **WCAG:** 1.3.1 Info og relasjoner (A), 2.4.6 Overskrifter og etiketter (AA), 2.4.1 Hoppe over blokker (A)
- **Hvor:** DESIGN.md → Typography (bare visuelle roller); EXPERIENCE.md → Component Patterns: Infokolonne, Begrunnelse, Bekledningstips; mocken bruker `<aside aria-label="Turforslag">` for hovedinnholdet og `<b>` for «Begrunnelse» og «Bekledningstips»
- **Scenario:** Ingen skjerm har en definert `h1`. «Begrunnelse» og «Bekledningstips for lørdag» er overlinjer i `eyebrow` og blir sannsynligvis `<b>` eller `<span>`, som i mocken. Skjermleserbrukeren kan ikke hoppe mellom delene av forslaget. Hvis infokolonnen blir `aside` (som i mocken), havner hovedinnholdet i et «komplementært» landemerke.
- **Fix:** Legg til en kolonne for semantikk: Søk `h1` = «Hvor lang tid har du?». Turforslag `h1` = turnavnet, `h2` = Begrunnelse, Bekledningstips, Kartet i tekst og Vil du ha noe annet?. Tilstandspanel `h1` = panelets overskrift. Skjemasidene `h1` = sideoverskriften. Landemerker: `header` med `nav` (Toppmeny), `main` (hele visningen, med kart og infokolonne), `region` for kartet. Ingen `aside` for turforslaget.

### M4. Lenker skilles bare med farge
- **WCAG:** 1.4.1 Bruk av farge (A)
- **Hvor:** DESIGN.md → Colors (primær brukes på lenker), `kreditering.link-color`, `sokeoppsummering.link-color`, `tilstandspanel.action-color`, `historikktabell` («lenker i `{colors.primary}`»)
- **Scenario:** `primary` mot `text` = **1,71:1**, og mot `text-muted` = **1,22:1** (regnet). I krediteringslinjen «© Kartverket · © OpenStreetMap contributors · Data fra MET Norge» står lenkene inne i tekst og skilles bare med en farge som ikke er 3:1 fra teksten rundt. Det samme gjelder «Lag konto» i nivåtak-teksten og handlingslenkene i Tilstandspanel.
- **Fix:** Skriv i DESIGN.md: «Lenker er alltid understreket», med unntak bare for menypunkter og knapper. Tykkelse og avstand på understreken kan styles for å holde roen.

### M5. «Nytt forslag»: fokusmål, dobbel opplesing og deaktivert knapp
- **WCAG:** 2.4.3 Fokusrekkefølge (A), 4.1.3 Statusmeldinger (AA)
- **Hvor:** EXPERIENCE.md → Component Patterns: Infokolonne («Fokus flyttes til turnavnet, og byttet meldes i en `aria-live`-region [ASSUMPTION]»), Primærknapp («Under innsending er den deaktivert»), Lasteindikator («`aria-busy` og en `aria-live`-melding»)
- **Scenario:**
  1. Ola trykker «Nytt forslag». Knappen får `disabled` mens han står på den. Fokus faller til `body`, og skjermleseren blir stille eller hopper til toppen.
  2. Fokus flyttes til turnavnet, og samtidig meldes byttet i live-regionen. Navnet leses to ganger, eller den ene opplesingen avbryter den andre.
  3. Det siste «Nytt forslag» gir Tilstandspanel «Du har sett alle turene …». Da finnes ikke noe turnavn å flytte fokus til.
  4. Ligger lastemeldingen inne i en beholder med `aria-busy="true"`, holder flere skjermlesere den tilbake til lastingen er ferdig. Med KI-reserven på 5 sekunder kan det bli flere sekunders stillhet.
- **Fix:** Bruk `aria-disabled="true"` og ignorer klikk i stedet for `disabled` på knappen som har fokus. Velg én kanal: fokus til `h1` (turnavn **eller** tilstandspanelets overskrift) og ingen live-melding for selve byttet. Lastemeldingen («Finner et nytt forslag …») ligger i en live-region **utenfor** beholderen med `aria-busy`. Fjern [ASSUMPTION] og gjør dette til regel.

### M6. Meldinger i turforslaget har ingen plass i den faste rekkefølgen
- **WCAG:** 1.3.2 Meningsfull rekkefølge (A), 4.1.3 Statusmeldinger (AA)
- **Hvor:** EXPERIENCE.md → Component Patterns: Infokolonne (fast rekkefølge), State Patterns: Topptur passer ikke, Reserveløsning, Uten værvarsel
- **Scenario:** «Toppturer krever mer tid enn du har oppgitt» (advarsel) og «Vi kunne ikke ta hensyn til ønsket ditt denne gangen» (info) er avgjørende for at Ola forstår forslaget, men de står ikke i den faste rekkefølgen. Havner de over turnavnet, hopper fokusflyttingen til turnavnet forbi dem. Havner de nederst, leser han hele forslaget før han får vite at det ikke er det han ba om.
- **Fix:** Plasser meldingene i rekkefølgen rett etter turnavnet og Turtype-treff (eller merket «Utsikt i stedet for topptur»), slik at de leses rett etter `h1`. Skriv også hvor info-meldingen om værvarsel står (der Bekledningstips ellers står, med samme `h2`).

### M7. Feiltekstene som skal gi forslag til retting er ikke skrevet
- **WCAG:** 3.3.3 Forslag ved feil (AA), 3.3.1 Identifikasjon av feil (A)
- **Hvor:** EXPERIENCE.md → Mikrotekst («Feil i skjemaet: «Velg varighet» [ASSUMPTION]»), State Patterns: Feil i skjemaet (FR-4, FR-16), Passord for kort
- **Scenario:** Bare én feiltekst finnes. Datoen utenfor perioden, fritekst over 200 tegn, dato frem i tid ved registrering, brukt tid utenfor 10 min–24 t og passord under 8 tegn har ingen tekst. Utviklere skriver da «Ugyldig dato», som ikke sier hvordan feilen rettes.
- **Fix:** Skriv alle feiltekstene med grensen i teksten, for eksempel «Velg en dato fra i dag til 6. desember», «Datoen kan ikke være frem i tid», «Brukt tid må være mellom 10 minutter og 24 timer», «Passordet må ha minst 8 tegn». Feiltekst og hjelpetekst kobles begge med `aria-describedby`.

### M8. Ingen `autocomplete` på e-post og passord
- **WCAG:** 1.3.5 Identifiser formålet med input (AA)
- **Hvor:** EXPERIENCE.md → Component Patterns: Skjemafelt; State Patterns: Logg inn / Registrer
- **Scenario:** Spinene sier ingenting om formål. En bruker med kognitive vansker eller motoriske vansker får ikke autofyll og passordbehandler som virker riktig, og nytt passord blir ikke foreslått.
- **Fix:** Skriv inn `autocomplete="email"` (eller `username`) på e-post, `current-password` ved innlogging og `new-password` ved registrering. Passordfeltet bør ha «Vis passord» (ikke krav, men det reduserer feil).

### M9. Fornøydhet 1–5 har ingen ankertekst
- **WCAG:** 3.3.2 Etiketter eller instruksjoner (A), 1.3.1 Info og relasjoner (A)
- **Hvor:** EXPERIENCE.md → Component Patterns: Valggruppe; DESIGN.md → `components.valggruppe`
- **Scenario:** Skjermleseren leser «Fornøydhet, gruppe, 1, radioknapp, 1 av 5». Ingen vet om 1 er best eller dårligst. Seende brukere har samme problem. Personaliseringen bygger på svaret.
- **Fix:** Legg ankertekst i `legend` eller hjelpetekst koblet til gruppen: «Fornøydhet (1 = ikke fornøyd, 5 = svært fornøyd)». Gi gjerne 1 og 5 et synlig navn («1 – ikke fornøyd», «5 – svært fornøyd»). Valgt segment er bare fyll. Legg til vekt 600 og en hake eller understrek, slik at tilstanden også synes i Windows høykontrastmodus (der fyll forsvinner).

### M10. Inndataformat for dato og brukt tid er ikke bestemt
- **WCAG:** 3.3.2 Etiketter eller instruksjoner (A), 2.1.1 Tastatur (A), 2.1.2 Ingen tastaturfelle (A)
- **Hvor:** EXPERIENCE.md → Skjemafelt, State Patterns: Registrer gjennomført tur; mockene viser Dato som nedtrekk «Lørdag 7. november ▾»
- **Scenario:** Mockene antyder en egen datovelger. Egne kalenderwidgeter er den vanligste kilden til tastaturfeller og stille fokus. «Brukt tid» skal gi «1 t 50 min», men spinen sier ikke om det er ett tekstfelt, to tall eller nedtrekk. Med ett fritt tekstfelt vet ingen hvilket format som godtas.
- **Fix:** Bestem native `<input type="date">` (med `min`/`max`) eller en `<select>` med de 31 aktuelle dagene. Brukt tid blir to tallfelt «Timer» og «Minutter» i et `fieldset` med `legend` «Brukt tid» og hjelpeteksten «10 min–24 t».

### M11. Utsiktsmarkørens etikett og flere markører har ingen definert farge
- **WCAG:** 1.4.3 Kontrast (AA), 1.4.11 Ikke-tekstlig kontrast (AA)
- **Hvor:** DESIGN.md → `components.kart` («utsiktsmarkøren «▲ Utsikt» er i `{colors.accent}` med tekstetikett»), `turillustrasjon.view-marker`
- **Scenario:** Spinen kan leses som at både markøren og teksten er i `accent` (2,2:1 mot land). I Turillustrasjon er utsiktsprikken `accent` mot `profile-fill` = **1,86:1**. Bildeteksten sier hvor utsikten kommer, så illustrasjonen klarer seg, men kartet har ingen slik tekst ved siden av.
- **Fix:** Gi etiketten `text` på hvit pille med `accent` kant (som i mocken, men med token). Behold `accent` bare til dekor og legg til en kant på prikken i `primary`, eller godta 1,86:1 i illustrasjonen fordi bildeteksten bærer informasjonen. Skriv det valget ned.

---

## Lav

### L1. Øktlengde er ikke bestemt
- **WCAG:** 2.2.1 Justerbar tidsbegrensning (A)
- **Hvor:** EXPERIENCE.md → Interaction Primitives, IA (FR-14)
- **Scenario:** Ola fyller ut «Registrer gjennomført tur» sakte. Økten går ut, han sendes til innlogging, og skjemaet er tomt. KI-grensen på 5 sekunder er på serveren og er grei.
- **Fix:** Skriv at innloggingsøkten varer i minst 20 timer, eller at skjemadata beholdes gjennom ny innlogging, på samme måte som turforslaget i FR-14.

### L2. Tegntelleren stopper stille ved 200
- **WCAG:** 3.3.1 Identifikasjon av feil (A), 4.1.3 Statusmeldinger (AA)
- **Hvor:** EXPERIENCE.md → Skjemafelt («stopper ved 200»), State Patterns (feil når fritekst er over 200)
- **Scenario:** Med `maxlength` kuttes innlimt tekst uten varsel, og feilen «over 200 tegn» kan aldri inntreffe. En skjermleserbruker vet ikke at teksten ble kuttet.
- **Fix:** Tillat skriving over 200 og vis feilen, eller behold stoppen og meld «Du har nådd 200 tegn» i en høflig live-region. Telleren meldes ikke for hvert tastetrykk.

### L3. Lenkene i Historikktabell er like på hver rad
- **WCAG:** 2.4.4 Formålet med lenken (i kontekst) (A)
- **Hvor:** EXPERIENCE.md → Component Patterns: Historikktabell
- **Scenario:** I en liste over lenker hører brukeren «Åpne som turforslag, Registrer gjennomført tur, Åpne som turforslag …». Kolonneoverskrifter alene knytter ikke lenken til turen.
- **Fix:** Turnavnet blir `<th scope="row">`, eller lenkene får skjult tilleggstekst («– Granåsen rundt, 7. nov.»).

### L4. Tegnene ✦ og ↗ leses opp
- **WCAG:** 1.1.1 Ikke-tekstlig innhold (A)
- **Hvor:** EXPERIENCE.md → Voice and Tone, KI-merke, ut.no-lenke
- **Scenario:** «Svart firtakket stjerne Skrevet med KI», «Se turen på ut.no nordøstpil».
- **Fix:** `aria-hidden="true"` på glyfene. På ↗ legges skjult tekst «(åpnes på ut.no)» til, og «(ny fane)» hvis den åpnes i ny fane.

### L5. Sletting og registrering kan utløses ved et uhell
- **WCAG:** 3.3.4 Forebygging av feil (AA)
- **Hvor:** EXPERIENCE.md → Slettebekreftelse, Interaction Primitives («Ingen bekreftelse unntatt ved sletting»), UJ-3 («Enkeltturer kan ikke slettes»)
- **Scenario:** «Slett konto» på Konto og «Slett kontoen» på neste visning kan havne på samme sted, så et dobbeltklikk kan slette kontoen. Fokus på overskriften beskytter bare tastaturbrukere. En registrering med feil fornøydhet kan ikke rettes og styrer personaliseringen. Kravet er formelt oppfylt fordi skjemaet valideres, men det er tynt.
- **Fix:** Ignorer klikk på «Slett kontoen» de første ca. 500 ms etter visningen, eller plasser knappen et annet sted. Vurder å la siste registrering kunne endres eller angres en stund (oppfølging i PRD).

### L6. Plassholderfarge er ikke spesifisert
- **WCAG:** 1.4.3 Kontrast (AA)
- **Hvor:** EXPERIENCE.md → Mikrotekst (plassholder i fritekst); DESIGN.md → `components.skjemafelt`
- **Scenario:** Nettleserens standardplassholder (#757575) er **3,49:1** mot `surface-dark`.
- **Fix:** `::placeholder` i `text-muted` / `text-muted-dark`.

### L7. Samme funksjon har forskjellige navn
- **WCAG:** 3.2.4 Konsekvent identifikasjon (AA)
- **Hvor:** EXPERIENCE.md → IA, Mikrotekst
- **Scenario:** «Finn tur» (meny), «Finn en ny tur» (Historikk) og logoen går alle til Søk. «Slett konto» og «Slett kontoen» ligner, men gjør forskjellige ting. «Registrer gjennomført tur» er både en lenke til siden og send-knappen på siden.
- **Fix:** Bruk «Finn tur» for navigering til Søk overalt. Behold forskjellen mellom «Slett konto» (åpner bekreftelse) og «Slett kontoen» bare hvis det er bevisst, og skriv det ned.

### L8. Tekstalternativet til Turillustrasjon er dobbelt, og malen brekker uten utsikt
- **WCAG:** 1.1.1 Ikke-tekstlig innhold (A)
- **Hvor:** EXPERIENCE.md → Component Patterns: Turillustrasjon; DESIGN.md → Turillustrasjon (bildeteksten gir de samme tallene)
- **Scenario:** Skjermleseren leser alternativteksten og så den synlige bildeteksten med de samme tallene. For en tur uten utsiktspunkt gir malen «utsikt etter ca. … km». Formen (rundtur eller tur-retur) i den lille rutetegningen er ikke med.
- **Fix:** Bruk `figure` med `figcaption`, og la SVG-en få `role="img"` med `aria-labelledby` til bildeteksten, eller gjør SVG-en `aria-hidden` når bildeteksten er komplett. Legg formen inn i bildeteksten og lag en variant uten utsikt.

### L9. Tabrekkefølgen i stablet oppsett følger ikke det visuelle
- **WCAG:** 2.4.3 Fokusrekkefølge (A), 1.3.2 Meningsfull rekkefølge (A)
- **Hvor:** EXPERIENCE.md → Interaction Primitives («infokolonnen kommer før kartkontrollene [ASSUMPTION]»), Responsive & Platform («kartet står over infokolonnen»)
- **Scenario:** Ved 200 % zoom står kartet øverst, men fokus går gjennom infokolonnen først og hopper så opp til kartknappene.
- **Fix:** Godta det bevisst (infokolonnen er viktigst) og la stablet oppsett vise infokolonnen **over** kartet, så DOM, tab og visuell rekkefølge er like.

### L10. Rullehjulzoom og animasjoner i kartet
- **WCAG:** 2.3.3 Animasjon fra interaksjoner (AAA, ikke krav), merknad om brukbarhet ved zoom
- **Hvor:** EXPERIENCE.md → Interaction Primitives («Bevegelse … slås av ved `prefers-reduced-motion`»), Kart
- **Scenario:** Leaflets `scrollWheelZoom` fanger rullehjulet. Ved 200 % zoom fyller kartet hele bredden, og brukeren som ruller siden, zoomer kartet i stedet. Ved «Nytt forslag» flyr kartet animert til ny rute.
- **Fix:** Slå av `scrollWheelZoom` (eller krev Ctrl + rulling) og bruk `zoomAnimation`/`flyTo` bare når `prefers-reduced-motion` ikke er satt. AAA-kravet er allerede godt ivaretatt i spinen. Dette er bare presisering for kartet.

---

## Godt dekket

- Turnivå med farge **og** tekst, status med ikon **og** tekst, valgt Turtypekort med «Valgt», feltfeil med ikon, tekst og kant (1.4.1).
- Tekstkontrast: alle par i DESIGN.md-tabellen stemmer innenfor avrunding (se Vedlegg). Nivåmerkene er 5,0–6,1:1 i lys og 6,1–8,0:1 i mørk modus. Den innvendige kanten på Svart i mørk modus (9,5:1) er riktig løst.
- Fokusring på 3 px med 2 px avstand, aldri fjernet, `:focus-visible`, og `outline` i stedet for mockenes `box-shadow` (som forsvinner i høykontrastmodus) (2.4.7).
- «Kartet holder aldri på tastaturfokus», ingen modale dialoger, ingen toasts som forsvinner og ingen omdirigeringer med tidsur (2.1.2, 2.2.1).
- Synlige etiketter, «(valgfritt)», «Alle fire felt er påkrevd.», `fieldset`/`legend` på valggrupper, feilmeldinger koblet med `aria-describedby` og fokus til første feil (3.3.1, 3.3.2).
- Kontosletting med egen bekreftelsesvisning, «Avbryt» tilbake til Konto og fokus på overskriften i stedet for sletteknappen (3.3.4).
- Historikk som ekte `<table>` med kolonneoverskrifter (1.3.1).
- `aria-current="page"` i Toppmeny, `aria-expanded` på Forklaringspanel, ingen informasjon bare ved hover (1.4.13).
- Turillustrasjon på Søk er `aria-hidden`, og bare nivå-, KI- og tallinformasjon er «tekst først».
- `prefers-reduced-motion` respekteres (2.3.3 er AAA og ikke et krav).
- Toppmenyen er konsekvent innenfor hver rolle (3.2.3). Forskjellen mellom gjest og innlogget er tillatt.

---

## Vedlegg: kontroll av kontrast

Regnet med WCAG 2.1 relativ luminans. Skriptet ligger i scratchpaden for økten.

| Par | Regnet | DESIGN.md sier | Merknad |
|---|---|---|---|
| `focus-ring` mot `surface` / `background` / `surface-alt` | 4,44 / 4,02 / 3,67 | 4,0 | OK. Tabellen bør vise alle tre. |
| `focus-ring-dark` mot `surface-dark` | 9,15 | 9,1 | OK |
| `focus-ring-dark` mot lys flis (#FFFFFF / OSM-land #F2EFE9 / OSM-skog #ADD19E) | 1,76 / 1,53 / 1,04 | – | **Feiler** (K2) |
| `focus-ring` mot OSM-skog / antatt vann #A8D3EE | 2,64 / 2,82 | – | **Feiler** (H1) |
| `input-border` mot `surface` / `background` / `surface-alt` | 3,00 / 2,72 / 2,48 | 3,0 | **Feiler** mot bakgrunn (H6) |
| `input-border-dark` mot `surface-dark` | 7,50 | 7,5 | OK |
| `text-dark` på krediteringsstripe (hvit .92) | 1,18 | – | **Feiler** (K2) |
| `primary-dark` (lenke) på hvit stripe | 1,70 | – | **Feiler** (K2) |
| `primary-dark` (startmarkør) mot OSM-land | 1,48 | – | **Feiler** (K2) |
| `map-route` mot hvit / plassholder / OSM-land | 3,92 / 3,41 / 3,41 | 3,4 | OK |
| `map-route` mot OSM-skog / antatt Kartverket-skog #CDE6B4 / antatt vann | 2,31 / 2,91 / 2,47 | ikke verifisert | **Feiler** (H1) |
| `accent` (utsiktsmarkør) mot OSM-land / OSM-skog | 2,22 / 1,50 | – | **Feiler** (H1, M11) |
| `accent` mot `profile-fill` (utsiktsprikk i illustrasjonen) | 1,86 | – | Bildeteksten bærer informasjonen (M11) |
| `primary` mot `text` (lenke i tekst) | 1,71 | – | Under 3:1 (M4) |
| `primary` mot `profile-fill` | 6,37 | 6,4 | OK |
| Nivåmerker lys (Grønn / Blå / Rød) | 5,08 / 6,09 / 5,67 | 5,1 / 6,1 / 5,7 | OK |
| Nivåmerker mørk (Grønn / Blå / Rød) | 8,02 / 6,09 / 6,10 | 8,0 / 6,1 / 6,1 | OK |
| `level-svart-dark` mot `surface-dark` / innvendig kant | 1,27 / 9,51 | 1,2 / 9,5 | OK med kant |
| `text-muted` mot `surface` / `surface-alt` | 7,07 / 5,85 | 7,1 / 5,9 | OK |
| Status som tekst (success / info / warning / error) | 9,28 / 6,52 / 5,97 / 6,45 | 8,4 / 5,9 / 5,4 / 5,8 | OK. Tabellen undervurderer litt (sannsynligvis målt mot en annen flate). |
| Standard plassholder #757575 mot `surface-dark` | 3,49 | – | **Feiler** (L6) |

Flisfarger: OSM-standard (land #F2EFE9, skog #ADD19E) er brukt som stedfortreder. Kartverket-skog (#CDE6B4) og vann (#A8D3EE) er **antatte** verdier. Ekte Kartverket topo-fliser må måles før rutefarge og fokusring på kart godkjennes.
