# Spine Pair Review — G81-eriksen

## Overall verdict
Spine-paret er godt strukturert og nesten helt mulig å hente ut for arkitektur og story-dev. Alle fargetokens har hex og lys/mørk-par. Alle 56 tokenreferanser resolver. De 27 komponentene finnes med samme navn i både DESIGN.md og EXPERIENCE.md, og desktop først-overstyringen av NFR-3 er sporet konsekvent i Foundation, Layout, Responsive og Avvik fra PRD. De viktigste hullene gjelder Turforslagets livssyklus: hvordan gjesten kommer tilbake (UJ-2), reload eller URL, og «Åpne som turforslag» fra Historikk. Det mangler også mørk modus-tokens for elementer som ligger oppå de alltid lyse kartflisene, og spinene sier ikke at WCAG 2.1 AA (Reflow, 320 px) gjør at det stablede oppsettet likevel må virke helt ned til smal bredde. 63 [ASSUMPTION] (16 + 47) må lukkes eller aksepteres før story-dev.

## 1. Flow coverage — adequate
Sjekket: UJ-1 og UJ-2 fra PRD §2.3 samt FR-1–21 og NFR-1–8 mot Key Flows. Begge UJ-ene finnes med navngitt protagonist (Ola), nummererte steg, et klimaks og feilveier. UJ-3 (slett konto) er lagt til og logget i Avvik fra PRD. FR-1–3, FR-5 og FR-21 er systemkrav uten egen UI-flyt, og det er greit.

### Findings
- **high** UJ-2 trinn 1 hviler på en uavklart antakelse: det er ikke bestemt hvordan gjesten kommer tilbake til turforslaget dagen etter. Bak dette ligger at Turforslagets livssyklus ikke er bestemt. Er visningen adresserbar med URL? Hva skjer ved reload, når PRD-en sier at en økt slutter ved reload? Overlever forslaget en lukket fane? Dette er en arkitekturbeslutning (sesjon, lokal lagring eller URL-parametre) som story-dev ellers må finne opp selv (EXPERIENCE.md › Key Flows › UJ-2 trinn 1; Åpne punkter «Gjestens vei tilbake»). *Fix:* Bestem om Turforslag har en delbar URL, for eksempel med søket og tur-ID-en i URL-en, og hva reload gir. Skriv UJ-2 trinn 1 om etter beslutningen, og legg til en rad «Reload / direkte lenke» i State Patterns.
- **medium** I PRD-ens UJ-1 trykker Ola faktisk på «Nytt forslag» (FR-7), men i spinen er det bare et hypotetisk steg («Hadde han ikke likt forslaget …»). Ingen flyt går derfor gjennom bytte på stedet, fokusflytting, aria-live og overgangen til Tilstandspanel «alle vist» (EXPERIENCE.md › Key Flows › UJ-1 trinn 7). *Fix:* Gjør trinn 7 til et faktisk steg med det som skjer (innholdet byttes, fokus går til turnavnet), eller legg til en kort flyt for FR-7 som ender i «Du har sett alle turene som passer søket».
- **low** FR-14 «Bruker kan logge ut» har ingen flyt og ingen landingsside (EXPERIENCE.md › IA › Konto; Key Flows). *Fix:* Legg en linje i State Patterns: «Logget ut → Søk som gjest, med eller uten kvittering».

## 2. Token completeness — adequate
Sjekket: 61 fargetokens, 13 typografitokens, 5 rounded- og 14 spacing-tokens og 27 komponentobjekter. 52 referanser i DESIGN.md og 4 i EXPERIENCE.md resolver alle. Alle farger har hex. Alle har `-dark`-par unntatt `map-route`, og der er unntaket begrunnet. Kontrastmålene er oppgitt for de viktigste parene, og jeg har sjekket dem med en egen beregning: tekst, primær, nivåmerker og fokusring stemmer.

### Findings
- **high** Kreditering og kartmarkørene ligger på kartfliser som er lyse i begge moduser, men komponentene peker på tokens som byttes i mørk modus («Hver komponent bruker `-dark`-parene»). I mørk modus blir `kreditering.foreground` = `text-dark` på hvit stripe 1,2:1, lenken `primary-dark` på hvit 1,7:1 og startmarkøren `primary-dark` på lyse fliser ca. 1,5:1. Kontrasttabellen dekker ingen av disse (DESIGN.md › components.kreditering, components.kart, Components › Kart). *Fix:* Lag kartlag-tokens som ikke byttes med modus, slik som `map-route`: for eksempel `map-text`, `map-link` og `map-marker-start`, med lyse verdier i begge moduser. Bruk dem i `kreditering` og `kart`, og legg dem til i kontrasttabellen.
- **medium** `input-border` er oppgitt som 3,0:1, men bare mot `surface`. Mot `background` er den 2,7:1 og mot `surface-alt` 2,5:1. Det står ikke hvilken flate Skjemafelt, Turtypekort og Valggruppe ligger på. DESIGN.md nevner selv et «skjemakort» uten å definere det (DESIGN.md › Colors › Kontrastmål; Elevation & Depth). *Fix:* Bestem at skjemaene ligger på `surface`, eller gjør `input-border` mørkere slik at den holder ≥ 3:1 også mot `background`. Mosegrønn-tonen kan beholdes.
- **medium** Utsiktsmarkøren «▲ Utsikt» på kartet er beskrevet «i `{colors.accent}` med tekstetikett». Hvis etiketten står i aksentfarge, bryter det regelen «aldri tekst i accent», og markørens kontrast mot flisene (3:1 for grafiske objekter) er ikke oppgitt (DESIGN.md › Components › Kart). *Fix:* Si at etiketten står i `text` på en lys brikke, og oppgi eller verifiser markørkontrasten sammen med `map-route`.
- **low** Statusraden i kontrasttabellen (8,4 / 5,9 / 5,4 / 5,8 «som tekst på flate») passer med `background`, ikke med `surface` (der blir det 9,3 / 6,5 / 6,0 / 6,5) (DESIGN.md › Kontrastmål). *Fix:* Skriv hvilken flate som er målt.
- **low** `kreditering.background` er den rå verdien `rgba(255,255,255,.92)` og ikke en token. `accent-2` er definert, men ingen komponent-token bruker den, siden `turillustrasjon` bruker `gradient-2` for åsene (DESIGN.md › components). *Fix:* Lag tokenen `map-overlay` og avklar om `accent-2` faktisk brukes i Turillustrasjon.

## 3. Component coverage — adequate
Sjekket: alle komponentnavn i begge filer. Alle 27 komponent-tokens i DESIGN.md har både et prosaavsnitt i Components og en rad med reelle atferdsregler i EXPERIENCE.md › Component Patterns, og navnene er like.

### Findings
- **medium** Skjemafelt brukes til fire kontrolltyper med ulik tastaturatferd: nedtrekksliste (Varighet «Velg», «2 timer ▾» i wireframen), liste (Startpunkt «Alle startpunkt»), dato og tekstområde med teller. Spinen sier ikke hvilken kontroll hvert felt er, for eksempel native `<select>` eller `<input type="date">` mot en egen datovelger (EXPERIENCE.md › Component Patterns › Skjemafelt; DESIGN.md › Components › Skjemafelt). *Fix:* Legg en undertabell under Skjemafelt med felt, kontrolltype og tastaturatferd. Velg native kontroller der det går.
- **low** Seksjonen «Vil du ha noe annet?» under folden står i DESIGN.md › Layout & Spacing og i stille-kart-mocken, men har ingen komponentrad eller atferd og er ikke med i rekkefølgen for Infokolonne (DESIGN.md › Layout; EXPERIENCE.md › Component Patterns › Infokolonne). *Fix:* Definer den, eller fjern den fra Layout.
- **low** «skjemakortet» (DESIGN.md › Elevation & Depth) og «søkeoppsummeringens lenke-brikker» (DESIGN.md › Shapes) er nevnt, men ikke definert. Søkeoppsummering beskriver «Endre søk» som en lenke, ikke som en brikke. *Fix:* Fjern begrepene eller gjør dem til en del av komponentene som finnes.

## 4. State coverage — adequate
Sjekket: alle 7 skjermer i IA mot tilstandene første visning, laster, feil, tom, uten tilgang, offline og fokus. Alle sju tilstandene fra PRD §6 er dekket. Turforslag har en svært god dekning med 17 tilstander.

### Findings
- **high** «Åpne som turforslag» fra Historikk (FR-17, UJ-2 trinn 7) har ingen tilstand. Det står ikke hva Søkeoppsummering viser når det ikke finnes et søk, hva Begrunnelse sier når FR-12 krever at den nevner varigheten, om Turtype-treff vises, om Bekledningstips gjelder for i dag, eller hva «Nytt forslag» gjør (EXPERIENCE.md › State Patterns; Component Patterns › Historikktabell). *Fix:* Legg til raden «Åpnet fra Historikk» med regler for disse fem elementene.
- **medium** Det er ikke bestemt hvordan lasting ser ut ved «Nytt forslag». Lastetilstanden gjelder bare første søk, men hvert nytt forslag kan vente opptil 5 s på KI (FR-13) (EXPERIENCE.md › State Patterns › Laster; Component Patterns › Infokolonne). *Fix:* Bestem hva som skjer mens neste forslag hentes: om det gamle innholdet blir stående eller vises som en plassholder, og at `aria-busy` settes på Infokolonne.
- **medium** Logg inn / Registrer mangler en «første visning». Det står ikke om dette er én side med to skjemaer, faner eller en bryter. Knappene «Logg inn», «Registrer», «Lag konto og fortsett» og «Tilbake til turforslaget» kolliderer med regelen om én primærknapp per visning (EXPERIENCE.md › IA; Mikrotekst; DESIGN.md › Components › Primærknapp). *Fix:* Bestem oppsettet og hvilken knapp som er primær i hver variant.
- **medium** Flere tilstander bryter grunnregelen i NFR-2 (en forklaring og et neste steg) fordi de ikke er designet: Tom historikk, kartfliser som feiler, lasting og feil ved lasting av Historikk og Konto, og hvor brukeren lander etter «Logg ut». «Uventet feil» gjelder bare Turforslag og skjemaer (EXPERIENCE.md › State Patterns; Åpne punkter). *Fix:* Gi hver av dem minst én linje med overskrift, tekst og neste steg. Tom historikk kan bruke Tilstandspanel-mønsteret.
- **low** Brudd i nettverket og utløpt innlogging (for eksempel midt i Registrer gjennomført tur) er ikke nevnt (EXPERIENCE.md › State Patterns). *Fix:* Legg til én rad hver, eller skriv eksplisitt at de dekkes av «Uventet feil».

## 5. Visual reference coverage — adequate
Sjekket: `mockups/` har tre filer (direction-stille-kart, direction-turkort og color-themes-2), `wireframes/` har to (ia og flow-ola) og `imports/` er tom. Alle fem er lenket inne i teksten med en beskrivelse av hva de viser. Ingen er foreldreløse. Regelen om at spinen vinner ved konflikt står i begge spinene, og kjente avvik er listet i Foundation.

### Findings
- **medium** State Patterns viser til «tilstandene A–G» i flow-ola uten å si hvilken bokstav som hører til hvilken rad. Wireframen har A Feil i skjemaet, B Ingen treff, C Kun turer over nivåtaket, D Alle forslag er vist, E Uten værvarsel, F Reserveløsning og G Topptur → utsiktstur. Gjestens krav om konto er skjerm 4, ikke en bokstav (EXPERIENCE.md › State Patterns, innledning). *Fix:* Legg til kolonnen «Skisse» med A–G og skjermnummer 1–6 i tabellen.
- **low** DESIGN.md › Components har ingen lenker per komponent. Turtypekort og Tilstandspanel finnes i direction-turkort, og Infokolonne, Kart og Melding i direction-stille-kart, men lenkene står bare samlet i Brand & Style. *Fix:* Legg til «→ se mockups/…» på de 5–6 komponentene som er vist i en mock.
- **low** Listen over kjente avvik mangler at Turkort-mocken har søkeoverskriften «Når vil du på tur, og hvor lenge?», mens spinen har «Hvor lang tid har du?» (EXPERIENCE.md › Foundation › Visuelle referanser). *Fix:* Legg det til i listen.

## 6. Bloat & overspecification — adequate
### Findings
- **medium** De samme faktaene står 3–5 steder, og det gir fare for at de glir fra hverandre. KI-merke og Forklaringspanel står i Voice and Tone, Mikrotekst, Component Patterns og KI-åpenhet. Kreditering står i DESIGN Components, Mikrotekst, Component Patterns og Kreditering og lisens. Kravet om hva som skal være over folden står i DESIGN Layout, Do's, State Patterns, Responsive og UJ-1. *Fix:* Gi hver fakta ett hjem (Mikrotekst for tekst, Component Patterns for regler) og la de andre stedene vise dit.
- **low** DESIGN.md › Components gjentar verdiene fra frontmatter nesten ordrett («fyll i `{colors.primary}` og tekst i `{colors.on-primary}` … 44 px … `{rounded.md}`»). *Fix:* La prosaen handle om oppbygning og regler og la tokenene bære verdiene.
- **low** Det står pikselverdier utenfor tokens og utenfor 4 px-skalaen: `padding: 10px 18px`, `4px 10px`, høyde 46 px, 56 px mellomrom på Søk, logomerke 22 px, 3 px linje i profilen og 28 % dekkevne. *Fix:* Bruk tokens som finnes (for eksempel `{spacing.3}`/`{spacing.4}`), eller merk verdiene som bevisste unntak.
- **low** Foundation nevner Leaflet som «ikke et UX-vedtak». Kreditering og lisens gjengir lisensresearch (CC BY-NC, METs anbefaling), og ingen som bygger videre, handler på det. *Fix:* Flytt lisensspørsmålet til Åpne punkter og fjern Leaflet-setningen.

## 7. Inheritance discipline — adequate
Sjekket: alle fem kildene i frontmatter finnes. UJ-navnene er ordrett fra PRD-en med tillegget «(desktop-tilpasset)». Domeneordene fra PRD §3 (Tur, Turforslag, Begrunnelse, Nivåtak, Gjest, Bruker, Økt) brukes likt. Komponentnavnene er like i begge filene. De 4 tokenreferansene i EXPERIENCE.md resolver mot DESIGN.md.

### Findings
- **medium** Overstyringen av mobilkravet er ikke sporet fullt ut. Avvik fra PRD #1 nevner NFR-3 og UJ-1, men ikke SM-4 («En manuell test av mobilvisning … består»), som Accessibility Floor selv viser til, og heller ikke PRD §4.2 («Søkeskjemaet er kort og raskt å fylle ut på mobil») (EXPERIENCE.md › Avvik fra PRD #1; Accessibility Floor punkt 1). *Fix:* Legg SM-4 og §4.2 til i Avvik #1, slik at PRD-oppdateringen fanger dem.
- **low** Frontmatter i EXPERIENCE.md mangler `name` (og `description`), som eksempel-spinene har. *Fix:* Legg til `name: Your Next Adventure`.

## 8. Shape fit — adequate
Sjekket: DESIGN.md har alle åtte seksjonene i kanonisk rekkefølge. EXPERIENCE.md har alle standardseksjonene. Inspiration & Anti-patterns er med fordi memloggen viser referanser og forkastede retninger. Responsive & Platform er med fordi det finnes bruddpunkter. De egne seksjonene KI-åpenhet, Avvik fra PRD og Åpne punkter fortjener plassen sin.

### Findings
- **high** WCAG 2.1 AA (NFR-4), som fortsatt gjelder, omfatter 1.4.10 Reflow: innholdet skal kunne brukes ved 320 CSS-px bredde, det vil si 1280 px ved 400 % zoom, uten at man må rulle i to retninger. Spinen sier bare «200 % zoom» og at stablingen «ikke er et mobildesign», mens `info-column-width` (470 px) og `form-column-width` (560 px) er faste bredder. I praksis må det stablede oppsettet altså virke ned til 320 px selv om mobil er utsatt. Dette avgrenser hva desktop først-overstyringen faktisk kan utsette (EXPERIENCE.md › Responsive & Platform; Accessibility Floor; DESIGN.md › Layout & Spacing › Stabling). *Fix:* Skriv at under bruddpunktet er alle kolonner flytende og at oppsettet virker ned til 320 px (Reflow). Presiser i Avvik #1 at det som utsettes, er mobiloptimalisering (layout, rekkefølge og at det meste synes uten rulling på 360 px), ikke at siden virker på smal bredde.
- **low** Seksjonen Kreditering og lisens overlapper med Kreditering i Component Patterns og i Mikrotekst. Det som er nytt, er lisensspørsmålene. *Fix:* Slå den sammen (se 6).

## Mechanical notes
- **Tokenreferanser:** Alle 52 i DESIGN.md og 4 i EXPERIENCE.md resolver. Ingen referanse peker til en token som ikke finnes.
- **Farger:** Alle har hex. `-dark`-par mangler bare for `map-route`, og det er dokumentert. `gradient-3` nevnes bare som en del av spennet «`gradient-1` → `gradient-4`». `kreditering.background` er en rå `rgba`-verdi.
- **Spacing-skalaen** `1`–`8` er definert, men bare `{spacing.3}` refereres. Resten brukes som rå px-verdier.
- **Komponenter:** 27 nøkler i `components` og 27 rader i Component Patterns, med like norske visningsnavn (`knapp-primaer` = Primærknapp og så videre). «skjemakort» og «lenke-brikker» er nevnt, men ikke definert.
- **Kilder:** Alle 5 stiene i `sources` finnes, og de er like i begge filene. Frontmatter i EXPERIENCE.md mangler `name`.
- **Visuelle referanser:** 5/5 filer er lenket med relative stier som resolver. `.working/` (inkludert den forkastede direction-rolig-oversikt og color-themes-1) er ikke lenket, og det er riktig.
- **Mermaid:** brukes ikke. Excalidraw-filene parser som JSON (74 og 515 elementer).
- **[ASSUMPTION]:** 16 i DESIGN.md og 47 i EXPERIENCE.md. Mange er knappetekster og plassering. De som påvirker arkitekturen, er Turforslagets livssyklus, Bekreft sletting som visning eller dialog, og bruddpunktet.
- **Desktop først (NFR-3):** Overstyringen er håndtert likt i DESIGN Layout, EXPERIENCE Foundation, Responsive & Platform, Avvik #1 og UJ-titlene. Spinene beholder knappehøyden på 44 px, og det er bra. Avvikene som gjenstår, er SM-4 og PRD §4.2 (se 7) og Reflow (se 8).
- **Kjente navneforskjeller:** «Finn tur» (meny) og «Finn en tur» (knapp) er begge godkjent, men det kan være lurt å si at det er med vilje. Fornøydhet er «4 av 5» i wireframen og 5 i journeyen, og det står allerede som et kjent avvik.
