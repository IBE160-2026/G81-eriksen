# PRD-kvalitetsgjennomgang – Your Next Adventure (v1.1)

Vurdert mot `prd-validation-checklist.md`. Kalibrert for et fagprosjekt i IBE160 (én person, kompakt PRD som skal videre til arkitektur og stories). Kilder: `prd.md` (v1.1, oppdatert 2026-11-06), `addendum.md`, `.memlog.md` (oppføringene om Update etter UX) og `../../ux-designs/ux-G81-eriksen-2026-11-06/EXPERIENCE.md`. Forrige gjennomgang: `review-rubric.md` (v1.0). Ekstra vekt på det som endret seg i v1.1.

## Samlet vurdering

v1.1 tar inn alle de 16 avvikene fra `EXPERIENCE.md` › «Avvik fra PRD» på en ryddig måte. Tallene i eksemplene stemmer nå (UJ-1 og FR-3 er regnet etter), den nye definisjonen av *Økt* i §3 stemmer med FR-7, unntaket i FR-12 og FR-17 er speilet begge veier, og P1/P2 dekker hver FR nøyaktig én gang. Den største risikoen ligger i personaliseringen, som er det som skiller produktet fra andre. UJ-2 lover at Ola «får en tur merket Blå – moderat» etter nivåhevingen, men rangeringen i FR-5 har ingen regel som gir det resultatet. FR-17 åpner dessuten et hull i den harde grensen i FR-19. Begge bør rettes før stories skrives. Resten er middels og lave funn om delegerte tekster, prioriteringen av KI-begrunnelsen og ordbruk.

## Beslutningsklarhet – adekvat

Beslutningene fra UX-arbeidet står som beslutninger og er sporbare. Endringsloggen (rad 1.1) lister hver endring, `.memlog.md` har en `(decision)` eller `(override)` for hver av dem, og §0 sier at avvikene er tatt inn. Overstyringen av *Økt* (fra «til siden lastes på nytt» til «til fanen lukkes») er begrunnet i memloggen med innloggingen midt i flyten. Det er en god beslutning, og den er ført riktig inn i §3 og FR-7.

Svakheten er §10. Fire åpne punkter fra UX står som «ikke avgjort i v1.1», men uten eier, frist eller om de blokkerer stories, mens frontmatter sier `status: final`. Ett av punktene, retting av siste registrering, påvirker datamodellen for FR-16 og FR-19. Memloggens siste oppføring nevner i tillegg et femte uavklart punkt, «tur åpnet fra Historikk over nåværende nivåtak vs FR-19», som ikke står i §10. Og «glemt passord» er listet som uavgjort, selv om §7.2 allerede har avgjort det (senere fase). Det reelle åpne spørsmålet fra UX er hvilket neste steg NFR-2 krever ved feil innlogging.

### Funn
- **medium** Åpne punkter i §10 er ufullstendige og mangler eier (§10, `.memlog.md` siste oppføring) – Punktet om turforslag åpnet fra historikken over nivåtaket mangler i §10, «glemt passord» er avgjort i §7.2, og ingen av punktene har eier, frist eller blokkeringsstatus. Samtidig står PRD-en som `status: final`. *Fiks:* Før opp alle fem punktene i §10 med eier (PRD eller UX), frist og om de blokkerer stories. Skriv «glemt passord» om til det reelle spørsmålet: neste steg ved feil innlogging (NFR-2). Alternativt kan punktene avgjøres nå, siden de fleste er én setning hver (se funnene under Klarhet).

## Innhold fremfor kulisser – sterk

Fortsatt lite pynt. UJ-3 er fortjent: den bærer FR-15 og den nøkterne tonen i §6, og den er kort. Ola er nå én protagonist i tre reiser, og de nye detaljene i UJ-1 (PC i sofaen, «Start: Granvannet p-plass», «✦ Skrevet med KI») driver hver sitt krav (FR-6, FR-12). Den nye stemmeregelen i §6 er konkret og kan kontrolleres. NFR-5 har fått en synlig personverntekst i stedet for bare et prinsipp. Ingen funn.

## Strategisk sammenheng – adekvat

Tesen er uendret og fortsatt tydelig: ett forklarbart forslag for nybegynnere, med KI som et avgrenset tillegg. Prioriteringen i §7.1 følger tesen. Det KI-uavhengige er P1, KI-merket og forklaringspanelet er P1 fordi de gjør forklarbarheten synlig, og kuttrekkefølgen starter med det som ikke berører kjerneflyten (fremgang, mørk modus). Kuttrekkefølgen stemmer med `EXPERIENCE.md` › Foundation og utvider den med FR-20 til slutt.

Problemet er at personaliseringen, som §1 bruker som hovedargument («tjenesten bruker vurderingene til å foreslå riktig nivå»), ikke gir det resultatet UJ-2 viser.

### Funn
- **high** UJ-2 lover en blå tur som FR-5 ikke gir (UJ-2, FR-5, FR-12, FR-17) – UJ-2 sier: «Når han søker igjen, får han en tur merket «Blå – moderat»». Nivåtaket i FR-5 er bare et *tak* i filteret. Etter hevingen passerer både grønne og blå turer, og ingen av de fem rangeringskriteriene foretrekker turer på nivåtaket. Om Ola får en blå tur, avhenger derfor av kriterium 4 (estimert tid nærmest varigheten). Det følger to ting av dette: (1) Begrunnelsen «Du får en blå tur fordi …» i FR-12 forutsetter at en personaliseringsregel «har påvirket valget», men PRD-en definerer ikke når det er tilfelle, så kravet kan ikke testes i SM-2. (2) Fremgangsteksten i FR-17 («Etter én til foreslår jeg litt lengre turer.») lover en oppførsel som rangeringen ikke garanterer. *Fiks:* Velg én av to løsninger. (a) Legg til et rangeringskriterium i FR-5, for eksempel «Turer på nivåtaket kommer foran turer under det» (plasser det bevisst i forhold til «ikke gått»), og definer at en regel «har påvirket valget» når den valgte turen har turnivå lik et nivåtak som er hevet eller senket av FR-19. (b) Behold FR-5 og skriv UJ-2, FR-12-eksempelet og fremgangsteksten om til «kan få blå turer». Løsning (a) passer tesen best.
- **medium** Prioriteten til den KI-skrevne begrunnelsen er uklar, og kutt får følger for tekstene (§7.1, FR-11, FR-12, FR-13) – P1 nevner «FR-12 og FR-13 med begrunnelse fra fast mal». Begrunnelse skrevet av KI (FR-12, fjerde punkt) er derfor ikke P1, men den står heller ikke i P2-listen. Kuttes FR-11, blir forklaringspanelets punkt «KI tolker ønsket» og meldingen i FR-13 («Jeg kunne ikke ta hensyn til ønsket ditt denne gangen») feil eller overflødige. Kuttes KI helt, vises «✦ Skrevet med KI» aldri. *Fiks:* Plasser KI-skrevet begrunnelse eksplisitt i P2-listen (for eksempel sammen med FR-11 som punkt 3), og skriv én setning om hvilke tekster i FR-12 og FR-13 som justeres når punktet kuttes.

## Klarhet om når et krav er ferdig – adekvat

Klart bedre enn i v1.0. Alle tre høye funn fra forrige gjennomgang er rettet: FR-5 har en deterministisk rangering, FR-19 er en hard grense, og FR-3 har en fast formel med et regneeksempel. Tallene stemmer. FR-3-eksempelet gir (90 + 22,5 + 11,25) × 1,15 = 142,3 min ≈ «ca. 2 t 20 min». UJ-1 sin rundtur gir (52,5 + 19,5 + 9,75) × 1,15 = 94,0 min ≈ «ca. 1 t 35 min», og 3,5 km og 130 høydemeter er Grønn etter FR-2. Det nye unntaket i FR-17 er presist (fire punkter), og FR-12 viser tilbake til det.

Det som gjenstår, er to typer hull: en direkte motsigelse mellom FR-17 og FR-19, og tekster som PRD-en sender videre til `EXPERIENCE.md`, der de fortsatt er plassholdere.

### Funn
- **medium** Turforslag åpnet fra historikken kan bryte den harde grensen (FR-17, FR-19, SM-C1, §3 *Turforslag*) – §3 sier at en tur åpnet fra historikken «vises også som turforslag». FR-19 sier at turer over nivåtaket «aldri» blir foreslått, og SM-C1 skal teste at «ingen bruker får foreslått en tur over nivåtaket». Etter en sperre kan historikken inneholde blå turer over det senkede taket. FR-17 sier ikke om de kan åpnes. Punktet står i memloggen som uavklart, men ikke i §10. *Fiks:* Legg til én setning i FR-17, for eksempel «Turforslag åpnet fra historikken er brukerens eget valg og omfattes ikke av nivåtaket i FR-19 og SM-C1», eller det motsatte: «Turer over nåværende nivåtak kan ikke åpnes som turforslag, og handlingen skjules».
- **medium** Tekster som PRD-en delegerer, er plassholdere i UX (FR-8, NFR-5, §10) – FR-8 sier at ordlyden for «innlogget bruker uten historikk» og «bruker med historikk» står i `EXPERIENCE.md` › Mikrotekst, og NFR-5 sier det samme om personverntekstens ordlyd. Alle tre radene er merket `[ASSUMPTION]` der. §10 sier samtidig at «alle antakelser … ble bekreftet». En utvikler eller tester kan ikke vite om teksten er endelig. *Fiks:* Godkjenn de tre tekstene og fjern merkingen i `EXPERIENCE.md`, eller skriv i FR-8 og NFR-5 at budskapet er krav og ordlyden foreløpig, og før ordlyden opp i §10.
- **low** FR-12 og FR-13 sier ulike ting om fritekstønsket i malteksten (FR-12 første punkt, FR-13 siste punkt) – FR-12 krever at begrunnelsen nevner fritekstønsket hvis brukeren har oppgitt det. FR-13 sier at malteksten aldri viser til fritekstønsket. Fjerde punkt i FR-12 («Når KI er tilgjengelig, skriver KI begrunnelsen») tar heller ikke med unntaket for historikken, som KI-merkepunktet tar med. *Fiks:* Legg til «Unntak: reserveløsning (FR-13)» i første punkt, og «unntatt for turforslag åpnet fra historikken» i fjerde punkt.
- **low** Den nye *Økt*-definisjonen gir en tilstand som mangler i §6 (§3 *Økt*, §6, NFR-2) – Når fanen er lukket eller adressen åpnes direkte, finnes det ikke noe turforslag. `EXPERIENCE.md` har tilstanden «Forslaget finnes ikke lenger», men §6 lister den ikke, og NFR-2 viser bare til tilstandene i §6. Det er heller ikke sagt om et turforslag åpnet fra historikken starter eller avslutter en økt. *Fiks:* Legg «turforslaget finnes ikke lenger (§3 Økt)» til i §6, og én setning i §3 om at et turforslag åpnet fra historikken ikke endrer økten.
- **low** NFR-3 bruker et adjektiv (NFR-3) – «synlige uten mye rulling» har ingen grense. *Fiks:* Vis til foldmålet i `DESIGN.md` › Layout & Spacing, eller angi en grense (for eksempel «innenfor første skjermhøyde på 1280 × 800»).

## Ærlig omfang – adekvat

§7.2 er uendret og god. P1 og P2 dekker FR-1 til FR-21 nøyaktig én gang: FR-9, FR-10, FR-11 og FR-20 er P2, resten er P1, og fremgangslinjen i FR-17 og mørk modus er tydelig skilt ut som P2. Mørk modus står både i §6 og §7.1 med samme kuttplass. Regelen «hvert kutt føres i §9 og i endringsloggen» er god. Det svake punktet er hva som skjer med P1-krav som er avhengige av P2-krav (se funn under Strategisk sammenheng og funnet under).

### Funn
- **low** FR-21 (P1) og SM-2 forutsetter FR-20 (P2) (§7.1, FR-21, SM-2) – Testbrukeren skal vise turtypepreferanse, og SM-2 tester FR-18 til FR-20. Kuttes FR-20, faller deler av et P1-krav og et suksessmål bort uten at PRD-en sier det. Det samme gjelder NFR-3 og bekledningstips (P2). *Fiks:* Legg til i §7.1: «Kuttes et P2-krav, faller tilsvarende del av FR-21, SM-2 og NFR-3 bort.»

## Nytte for senere arbeid – adekvat

ID-ene er stabile og sammenhengende: UJ-1 til UJ-3, FR-1 til FR-21, NFR-1 til NFR-8, SM-1 til SM-4 og SM-C1. Ingen nye FR-ID-er, slik endringsloggen sier. Alle kryssreferanser til FR-ID-er treffer. Lenkene i §6 (`../../ux-designs/ux-G81-eriksen-2026-11-06/wireframes/…`) løses fra arbeidsmappen, og begge `.excalidraw`-filene finnes. Seksjonene det vises til i `EXPERIENCE.md` (Mikrotekst, Component Patterns › Forklaringspanel, Key Flows, Avvik fra PRD, Åpne punkter) finnes alle. Begrepslisten har fått *Økt*, *Sperre*, *Varighet*, *Tur-retur / rundtur* og *høydeprofil*, så funnene fra v1.0 er lukket.

Det som trekker ned, er to ordrette tekster som bryter med beslutninger i v1.1.

### Funn
- **low** «Registrere» brukes fortsatt om kontooppretting (FR-14) – §6 har innført skjermnavnet «logg inn / lag konto» nettopp for at kontooppretting ikke skal forveksles med «Registrer gjennomført tur» (`EXPERIENCE.md` › Avvik 6). FR-14 sier likevel «lage konto (registrere seg)», og feilmeldingen er fortsatt «Kunne ikke registrere – prøv å logge inn». *Fiks:* Endre teksten til for eksempel «Kunne ikke lage konto – prøv å logge inn», fjern «(registrere seg)» og oppdater Mikrotekst-raden i `EXPERIENCE.md`.
- **low** Nivåforklaringen i FR-6 er ikke i jeg-form (FR-6, §6 *Stemme og tone*) – §6 sier at «alle ordrette tekster i PRD-en står i jeg-form». «Beregnet av tjenesten etter Merkehåndbokas mal …» omtaler tjenesten i tredje person. Alle andre ordrette tekster er i jeg-form eller nøytrale. *Fiks:* For eksempel «Jeg har beregnet nivået etter Merkehåndbokas mal ut fra lengde og høydemeter. Terreng og føre er ikke vurdert.», eller gjør et uttrykkelig unntak for faste faktatekster.

## Passende form – sterk

Tre brukerreiser med én protagonist passer et forbrukerprodukt av denne størrelsen. UJ-3 er kort og har en tydelig feilvei («Avbryt»). Detaljflyten er flyttet til `EXPERIENCE.md` › Key Flows, slik at PRD-en holder seg kompakt. Henvisningene fra UJ-ene til FR-ene (FR-7, FR-8, FR-14, FR-15, FR-17, FR-19) gjør dem nyttige for stories.

### Funn
- **low** Forutsetningen i UJ-2 kan ikke nås med kravene slik de står (UJ-2, FR-16, §3 *Økt*) – UJ-2 sier at Ola «allerede har registrert to grønne turer», mens UJ-1 viser at kontoen ble laget kort før, og fanen med Granåsen-forslaget er fortsatt åpen. Etter FR-16 kan en tur bare registreres fra et turforslag eller fra historikken, og et nytt søk i samme fane avslutter økten. De to turene må altså ha kommet fra søk i en annen fane. «Reisen er komprimert» dekker over dette. *Fiks:* Én bisetning, for eksempel «Ola har registrert to grønne turer vurdert *lett* tidligere, fra søk han gjorde i andre faner». Alternativt kan forutsetningen flyttes til testbrukeren.

## Mekaniske merknader

- **Tall verifisert:** FR-3-eksempelet (142,3 min → «ca. 2 t 20 min») og UJ-1 (rundtur 3,5 km / 130 hm / 130 m ned → 94,0 min → «ca. 1 t 35 min», Grønn etter FR-2) stemmer. Brukt tid i UJ-2 (1 t 50 min) er innenfor FR-16 og støtter forklaringspanelets setning om at nybegynnere bruker lenger tid.
- **ID-kontinuitet:** UJ-1–3, FR-1–21, NFR-1–8, SM-1–4 og SM-C1 er sammenhengende og unike. «Gjelder UJ-…» er oppdatert i §4.6 og FR-15.
- **Lenker:** Begge wireframe-lenkene i §6 løses. Stiene skrives på tre måter: fra prosjektroten (§0), relativt fra arbeidsmappen (§6) og fra `planning-artifacts/` (endringsloggen, rad 1.1). Velg én konvensjon for tekstlige stier og bruk relative stier bare i lenker.
- **Begrepsdrift:** FR-8 sier «Innlogget bruker», men *Bruker* er per definisjon innlogget (§3). Gjesteteksten i FR-8 kaller gjesten «ny bruker». Begge er små, men teksten er ordrett og havner i grensesnittet.
- **Rekkefølge i forklaringspanelet:** FR-12 lister (rute/tid/nivå, KI, tidsavvik), mens `EXPERIENCE.md` › Forklaringspanel har (rute/tid/nivå, tidsavvik, KI). Ufarlig, men si hvilken som gjelder, siden `EXPERIENCE.md` eier ordlyden.
- **«Lengre turer»:** Ordet står både i FR-8 og i fremgangsteksten i FR-17. §10 nevner bare FR-8. Ta med FR-17 når punktet avklares.
- **Antakelsesindeks:** PRD-en har ingen inline `[ASSUMPTION]`-merker, så indeksen går opp. Men tekster PRD-en delegerer, er merket `[ASSUMPTION]` i `EXPERIENCE.md` (se funn under Klarhet).
- **Funn fra v1.0:** Alle tre høye og de fleste middels funn fra `review-rubric.md` er lukket (rangering, hard grense, formel, rundtur, varighet, bekledningstabell, tidsgrense for KI, FR-7 tom liste, passord, begreper, SM-1-referanser, SM-C1 målbar, NFR-grenser).
