# Input-avstemming: UX-spines mot PRD v1.1

Finalize › Input-avstemming for Update v1.1, 2026-11-06.
Kilder: `prd.md` (v1.1), `addendum.md`, `.memlog.md` (oppføring 68–79, linje 73–84), UX-mappen `ux-designs/ux-G81-eriksen-2026-11-06/`: **E** = `EXPERIENCE.md` og **D** = `DESIGN.md`.

**Sammendrag:** Av de 16 avvikene er 15 dekket, 1 er delvis dekket og 0 mangler. Hovedfunnene står i §2 og §3: KI-eksemplet bryter FR-12, mobilrekkefølgen bryter NFR-3, et turforslag åpnet fra Historikk kan ligge over nivåtaket, turillustrasjonen mangler i FR-6, og prioriteringen av KI-skrevet begrunnelse er uklar.

## 1. De 16 avvikene i E › «Avvik fra PRD»

| # | Avvik | Status | Hvor i PRD | Merknad |
|---|---|---|---|---|
| 1 | Grønn i UJ-1 stemmer ikke (7,2 km) | Dekket | UJ-1 | Rundtur, 3,5 km, 130 hm. Kontrollregning med FR-3: (52,5 + 19,5 + 9,75) × 1,15 = 94,0 min, som vises som «ca. 1 t 35 min». Under 5 km og 300 hm gir Grønn (FR-2). |
| 2 | UJ-1 og UJ-2 skrevet om (PC i sofaen, konto til slutt) | Dekket | UJ-1, UJ-2 | Feilveien «søker på nytt hvis fanen er lukket» står bare i E. Det er greit, fordi §2.3 viser til E › Key Flows for feilveiene. |
| 3 | UJ-2 komprimerer «etter noen turer» | Dekket | UJ-2 («Reisen er komprimert …») | – |
| 4 | UJ-3 slett konto er ny | Dekket | UJ-3, FR-15 | FR-15 er tynnere enn UJ-3, se §2.4. |
| 5 | Jeg-form | Dekket | §6 Stemme og tone, FR-13 | Ingen ordrett PRD-tekst står lenger i vi-form. |
| 6 | Skjermnavnet Logg inn / Lag konto | Dekket | §6 Skjermer, endringslogg 1.1 | FR-14-teksten bruker fortsatt «registrere», se §3.6. |
| 7 | Åpne som turforslag fra Historikk | Dekket | FR-17, FR-7, FR-9, FR-12 | Ny motsigelse med nivåtaket, se §3.3. |
| 8 | Økten varer til fanen lukkes | Dekket | §3 Økt, FR-7 | – |
| 9 | «Alle turtyper» er forvalgt | Dekket | FR-4 | – |
| 10 | Startpunktets navn | Dekket | FR-6, §3 Startpunkt, addendum | – |
| 11 | Personverntekst på Konto | Dekket | NFR-5, §6 Skjermer | PRD-en viser til ordlyd som er [ASSUMPTION] i E, se §3.8. |
| 12 | Nivåtaktekst per brukertype | Dekket | FR-8 | To av tre tekster er [ASSUMPTION] i E, se §3.8. |
| 13 | Høydeprofil og startpunktets navn i turdataene | Dekket | §3 Tur, FR-1, addendum | Feltlisten i addendum › Lagring nevner fortsatt ikke høydeprofil og startpunkt. De står i punktet under. Feltnavnene bør legges inn i selve listen. |
| 14 | Mørk modus, KI-merke, Forklaringspanel og fremgang | Dekket | §6, FR-12 (P1), FR-17 (P2), §7.1 | Kuttrekkefølge 1–4 er lik i E › Foundation og §7.1. FR-20 er punkt 5 bare i PRD-en. Det er greit, fordi den ikke har noe grensesnitt. Rekkefølgen i panelet avviker, se §3.7. |
| 15 | Tekster PRD-en ikke gir | **Delvis** | §6 («Mikrotekst har tekstene …») | Tekstene er dekket ved henvisning, men de fleste er [ASSUMPTION] i E. Det gjelder blant annet nivåtak, uten værvarsel, lasting, feilmeldinger, tom historikk og innlogging utløpt. Atferden bak noen av tekstene står ikke som krav, for eksempel at innlogging utløper med bevarte felt, og at et forslag ikke lenger er tilgjengelig. PRD §10 nevner ikke at tekstene må godkjennes. |
| 16 | Wireframes i §6 | Dekket | §6 UX-spesifikasjon | Begge lenkene er på plass. |

## 2. UX-beslutninger med kravvekt som PRD-en ikke har

Listen tar bare med beslutninger som påvirker hva som skal bygges eller testes. Rene visuelle detaljer er utelatt.

1. **Turillustrasjonen mangler i FR-6.** E › UJ-1 steg 5 kaller illustrasjonen klimakset («Ja, den tar jeg»). Foldmålet i D › Layout & Spacing krever at turnavn, Turtype-treff, Faktarute, Turillustrasjon og kart synes uten rulling ved 1280 × 800. PRD-en nevner høydeprofilen bare som data (FR-1, addendum: «brukes i turillustrasjonen»). FR-6 nevner ikke illustrasjonen, og den står heller ikke i P1 eller i kuttrekkefølgen. E › Åpne punkter sier «Turillustrasjon uten reserve». **Forslag:** Legg «illustrasjon av rute og høydeprofil, tegnet fra turdata» inn i FR-6, og bestem om den er P1 eller hvor den står i kuttrekkefølgen.
2. **Kartbeskrivelsen er synlig og lages fra data.** FR-6 sier bare «Kartet har en tekstbeskrivelse for skjermlesere». E › Kartbeskrivelse beskriver en synlig seksjon «Kartet i tekst» som **genereres fra turdata og ikke av KI**. Den skal ha minst startpunkt, form, total lengde, høydemeter og laveste og høyeste punkt i moh. **Forslag:** Gjør FR-6 presis på dette. Det følger samme prinsipp som FR-3 («KI beregner aldri …»).
3. **Gjest som trykker «Registrer gjennomført tur», går rett inn i registreringen etter innlogging.** Dette står i E › IA › Ruter som krever konto. FR-14 sier bare at «turforslaget … beholdes». Kjerneflyten i SM-1 går gjennom nettopp denne overgangen. **Forslag:** Utvid FR-14 så gjesten fortsetter til handlingen hen startet, ikke bare tilbake til forslaget.
4. **Kontosletting (FR-15) er tynnere enn UJ-3 og E.** Disse punktene mangler i FR-15:
   - Hva som slettes. Det bør være e-post, passordhash **og** historikk. FR-15 sier bare «All historikk», og NFR-5 tilsier at kontodataene også skal bort.
   - At kontoen er urørt hvis slettingen feiler (E › State «Sletting feiler»). Dette er et krav om alt-eller-ingenting.
   - At brukeren ender som gjest på Søk med kvittering. Dette står bare i UJ-3.
   - At enkeltturer ikke kan slettes i v1 (E › UJ-3: «V1 har bare full kontosletting»). Dette er en scope-beslutning som hører hjemme i §7.2, og den henger sammen med det åpne punktet om retting i §10.
5. **E › Accessibility Floor stiller strengere krav enn NFR-4 og NFR-3.** Listen under «Det betyr:» i NFR-4 kan leses som komplett. E krever også:
   - reflow ved **320 px** (WCAG 1.4.10), mens NFR-3 sier 360 px
   - kontrast på 3:1 for komponenter som ikke er tekst (1.4.11)
   - 200 % tekstzoom og tekstavstand (1.4.4 og 1.4.12)
   - feilmeldinger som sier hvordan feilen rettes (3.3.3)
   - sidetittel og fokus ved hver visningsendring (2.4.2 og 2.4.3)
   - at kartet aldri fanger siderullingen
   - at `prefers-reduced-motion` respekteres (AAA, et bevisst tillegg)
   - at innlogging som utløper, ikke gjør at utfylte felt går tapt (2.2.1)

   E sier: «Listen er sjekklisten for SM-4.» SM-4 viser bare til «en dokumentert sjekkliste». **Forslag:** Skriv «minst» i NFR-4, endre NFR-3 til 320 px og la SM-4 vise til E › Accessibility Floor. Tillat også at kart og Historikktabell ruller i egen beholder. NFR-3 sier i dag «uten horisontal rulling» uten unntak.
6. **KI-åpenhet for gjester.** Teksten om at KI ikke får personopplysninger (NFR-5) står bare på Konto, som bare innloggede ser. En gjest som skriver et fritekstønske, får ikke vite hva KI-tjenesten mottar. Forklaringspanelet (FR-12, E) sier ikke noe om det. **Forslag:** Legg til et fjerde punkt i forklaringspanelet i FR-12: KI får bare søket og turene som passer, ingen personopplysninger.
7. **«Finne igjen turer jeg likte» (§2.1 Over tid) har ikke noe krav.** FR-17 sier ikke noe om rekkefølge. E viser nyeste først og har «Finne igjen favoritter» som åpent UX-punkt. UJ-2 forutsetter at Ola finner «favoritturen». **Forslag:** Velg sortering eller merking i FR-17, eller godta nyeste først og myk opp jobben i §2.1.
8. **Kutt av FR-11.** I E › Foundation punkt 3 skjules fritekstfeltet helt. §7.1 sier ikke hva kuttet betyr for grensesnittet. Se også §3.4.
9. **Turtype på turforslaget.** FR-6 krever ikke at turens turtyper vises. E viser dem bare som Turtype-treff, og E har dette som åpent punkt («Med Alle turtyper får brukeren ikke vite at turen har utsikt»). Lav prioritet, men FR-6 bør ta stilling til det.
10. **Lenke uten økt.** Er fanen lukket, eller er adressen åpnet direkte, vises Søk med «Turforslaget er ikke lenger tilgjengelig …» (E › State). PRD-en dekker dette bare generelt gjennom NFR-2 og §3 («ingen delbar lenke»). Lav prioritet. Tilstanden kan legges til i §6 › Tilstander.

## 3. Motsigelser mellom PRD v1.1 og spines

| # | PRD v1.1 | UX | Alvor | Forslag |
|---|---|---|---|---|
| 3.1 | FR-12: «Tall som estimert tid, lengde og turnivå settes inn av systemet og skrives aldri av KI.» | E › Mikrotekst «Begrunnelse (KI, eksempel fra UJ-1)»: «Turen tar **ca. 1 t 35 min** og passer de 2 timene du har. Den har utsikt, som du ba om, og er **grønn** …» E › Component Patterns › Begrunnelse sier at eksemplet viser «hva en KI-skrevet begrunnelse skal nevne». Det gjelder også PRD-eksemplet «Du får en **blå** tur fordi de **tre** siste **grønne** turene …» hvis KI skriver det. | Høy | Bestem i FR-12 at tall og nivå enten står som plassholdere som systemet fyller inn, eller at de ikke står i KI-teksten. Rett eksemplet i E. |
| 3.2 | NFR-3: «På turforslaget er kart, turnivå, estimert tid og bekledningstips synlige uten mye rulling.» | E › Turforslag – rekkefølge, som er lik på alle bredder: Bekledningstips er nummer 8, etter Turillustrasjon, kart (ca. 60 % av skjermhøyden på mobil) og Begrunnelse. D › Folden gjelder bare 1280 × 800 og tar ikke med bekledningstips. | Høy | Enten flytt Bekledningstips opp i rekkefølgen, eller skriv NFR-3 om til et foldmål for mobil som stemmer med E og D. |
| 3.3 | FR-19: «Hard grense: Turer over nivåtaket blir aldri foreslått», og SM-C1: «Ingen bruker får foreslått en tur over nivåtaket». §3 Turforslag: «En tur åpnet fra historikken vises også som turforslag (FR-17).» | E › State «Åpnet fra Historikk» har ingen nivåsjekk. Etter en sperre kan en blå tur fra Historikk vises som turforslag over nivåtaket. Memlog-oppføring 79 (linje 84) har dette som uavklart, men punktet **mangler i §10**. | Middels | Ta punktet inn i §10, eller avgjør det: FR-17 er et unntak fra FR-19 fordi brukeren selv velger turen, eller turen får en merknad. |
| 3.4 | §7.1 P1: «FR-12 og FR-13 **med begrunnelse fra fast mal** …». P2 punkt 3: «FR-11 (KI-tolking av fritekstønske)». | Den KI-skrevne begrunnelsen står verken i P1 eller i kuttlisten. Kuttes FR-11, sier E bare at feltet skjules. Da blir forklaringspanelets «KI tolker ønsket ditt …» og hjelpeteksten «Jeg prøver å ta hensyn til ønsket ditt.» feil, og det samme kan gjelde KI-merket. | Middels | Plasser «KI skriver begrunnelsen» i P2-rekkefølgen, og skriv hva forklaringspanelet sier når FR-11 eller all KI er kuttet. |
| 3.5 | §10 nevner bare ordlyden «låse opp lengre turer» **i FR-8**. FR-17 har samme ordlyd ordrett: «Etter én til foreslår jeg litt **lengre** turer.» | E bruker samme ordlyd i Voice and Tone og fremgangslinjen. Målet nådd: «Tre grønne turer som føltes lette – godt gått! 🎉 Neste gang kan du få blå turer.» | Middels | Utvid punktet i §10 til FR-8, FR-17 og E › Voice and Tone. Sjekk feiringen mot SM-C1 (se §4). |
| 3.6 | FR-14: «Kunne ikke registrere – prøv å logge inn» og «Gjest kan lage konto (registrere seg)». | Avvik 6 og E › IA: kontoopprettelse heter «Lag konto», så den ikke forveksles med «Registrer gjennomført tur». E beholder likevel PRD-teksten. | Lav | Bruk «Kunne ikke lage konto – prøv å logge inn» i FR-14 og E › Mikrotekst. |
| 3.7 | FR-12 Forklaringspanel har rekkefølgen (1) rute, tid og nivå fra data, (2) KI tolker og kan ta feil, (3) tiden kan bomme med 15 %. «Ordlyden står i `EXPERIENCE.md` › Component Patterns (Forklaringspanel).» | E har rekkefølgen (1) data, (2) tid ±15 %, (3) KI. E gir bare innholdet med egne ord, og Mikrotekst har bare utløseren. Ingen godkjent ordlyd finnes. | Lav | Skriv i FR-12 at rekkefølgen er E sin, og legg panelteksten inn i E › Mikrotekst. |
| 3.8 | §10: «Alle antakelser og standardverdier ble bekreftet …». FR-8 og NFR-5 sier «Ordlyden står i `EXPERIENCE.md` › Mikrotekst». | Nivåtak (innlogget uten historikk og bruker med historikk), personverntekst, lasting, ingen treff, uten værvarsel, feilmeldinger og sletteknapper er merket **[ASSUMPTION]** i E. E › Åpne punkter sier at de må godkjennes. | Middels | Ta godkjenning av [ASSUMPTION]-tekstene inn i §10, eller godkjenn dem i denne runden. |
| 3.9 | NFR-5: «lagrer bare e-post, passord som hash, historikk og vurderinger», og personverntekst: «Jeg lagrer bare …». FR-13: «Forkastede KI-svar logges». | Loggen kan inneholde fritekstønsket. | Lav | Skriv i FR-13 at loggen ikke kobles til en bruker, eller ta loggen med i NFR-5. |
| 3.10 | FR-17: «**Overskriften** «Fra historikken din» står i stedet for søkeoppsummeringen.» | E: teksten står der Søkeoppsummering står. `h1` er fortsatt turnavnet, og `h2` finnes bare for Begrunnelse, Bekledningstips og «Kartet i tekst». | Lav | Skriv «Teksten» eller «Linjen» i stedet for «Overskriften», så ingen lager en ekstra overskrift. |
| 3.11 | FR-8, bruker med historikk: «Meldingen sier hvilket nivå tjenesten foreslår turer opp til akkurat nå». | E › Mikrotekst «Nivåtak, tittel»: «Ingen **grønne** turer passer søket». Grønn er hardkodet, selv om nivåtaket kan være blått eller rødt. | Lav (rettes i UX) | Bruk «Ingen {nivå} turer passer søket». |

**Kontrollert og konsistent:**
- skjermnavnet Logg inn / Lag konto
- kuttrekkefølge 1–4 (fremgang, mørk modus, FR-11, FR-9/10), med FR-20 som punkt 5 bare i PRD-en
- mørk modus «med i v1» og P2, også «lav prioritet» i D
- «✦ Skrevet med KI» / «Begrunnelse fra mal», også i testmodus og for forslag åpnet fra Historikk
- «Alle turtyper»
- datoperioden: 31 valg, fra i dag til 30 dager frem
- grensen for værvarsel, ca. 9–10 dager
- «Du har sett alle turene som passer søket» og «Toppturer krever mer tid enn du har oppgitt»
- krediteringen «Data fra MET Norge»
- fire påkrevde felt og 10 min–24 t i FR-16
- eksempelturen 3,5 km, 130 hm og 1 t 35 min

## 4. Kvalitativ intensjon PRD-en mister

- **Personaen «rolig turkompis».** E og D beskriver stemmen som en personlig turkompis som er «varm, konkret og kort», med «ingen mas» og «luftig, ryddig og trygg». §6 i PRD-en sier bare «innbydende og trygg». «Kort» og «konkret» er nyttige krav til KI-teksten. De bør med i FR-12 eller §6.
- **Beslutningen tas på én skjerm.** E sier om klimakset i UJ-1: Ola ser «uten å rulle» illustrasjonen, kartet og Turtype-treff samtidig, og tenker «Ja, den tar jeg». Dette er den konkrete formen på §2.1 Emosjonelt («stole nok på forslaget»). UJ-1 i PRD-en har bare «så han bestemmer seg», og ingen FR eller NFR krever det (se §2.1 og §3.2).
- **Ingen antydning om at KI lærer.** E: «Teksten må aldri antyde at KI lærer, så «Neste tur blir enda mer din» er ikke lov.» PRD §6 sier at tjenesten ikke overselger «læring», som dekker hensikten. Det forbudte eksemplet bør likevel med, fordi §1 Visjon samtidig snakker om å «lære av brukerens historikk».
- **Nøktern også om personvern.** E nevner feil, innlogging, **personvern** og sletting. §6 i PRD-en mangler personvern. D › Slettebekreftelse sier «Ingen rød flate og ingen advarselsikoner som roper». Det betyr at slettingen verken skal skremme eller presse brukeren. Målet for UJ-3 er at brukeren «ser tydelig at alt er borte».
- **Sparsom feiring.** E tillater bare tre faste tegn (✦, ↗ og 🎉). 🎉 og «godt gått!» feirer en nivåheving. Det kan oppleves som press oppover, og det står i spenning med SM-C1 («Tjenesten skal ikke presse nybegynnere oppover»). PRD-en tar ikke stilling, fordi den bare viser til teksten (FR-17).
- **Feil som hjelper videre.** E sier at feilteksten skal si hvordan feilen rettes. FR-4 og FR-16 sier bare «feilmelding ved feltet». Se §2.5.
- **Ett tydelig valg som prinsipp.** E › Anti-patterns forkaster lister, karuseller og uendelig rulling. PRD-en dekker dette gjennom «ett forslag om gangen» (§9, FR-7). Ingen endring trengs.
