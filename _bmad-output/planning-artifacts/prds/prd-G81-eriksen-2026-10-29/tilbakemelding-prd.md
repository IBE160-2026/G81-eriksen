# Tilbakemelding på PRD

| | |
|---|---|
| **Gruppe** | G81 – G81-eriksen |
| **PRD vurdert** | `_bmad-output/planning-artifacts/prds/prd-G81-eriksen-2026-10-29/prd.md` (status i frontmatter: final, sist endret 2026-11-08, commit 802e8d3) |
| **Dato** | 2026-11-12 |
| **Type** | Formativ tilbakemelding, ikke karakter |

## 1. Samlet inntrykk

Dette er en sterk PRD med en klar tese: nybegynnere får ett turforslag fra en kuratert database, og KI får bare tolke ønsker og skrive begrunnelser. Valgene er begrunnet, kravene er stort sett testbare, og scope har en reell prioritering. Risikoen er at kjernen i personaliseringen (FR-19) ikke er helt entydig, at omfanget er stort for én person, og at KI-kostnad og misbruk ikke er behandlet.

## 2. Dette fungerer godt

- **Tesen bæres av kravene.** «KI velger aldri en tur utenfor den kuraterte turdatabasen» (§1) følges opp av FR-11 («KI får bare fritekstønsket og turene som har kommet gjennom filteret»), FR-12 («KI skriver aldri tall eller turnivå») og FR-13 (fem forkastingsregler og reserveløsning). KI-kontrollen er konkret og kan bli testtilfeller.
- **Regnbare krav.** FR-2 har en gradertabell med regel for grenseverdier, og FR-3 har et regneeksempel som stemmer ((90 + 22,5 + 11,25) × 1,15 ≈ 142 min, vist som 2 t 20 min). SM-2 bruker eksempelet som testtilfelle.
- **Ærlig scope.** §7.1 deler kravene i P1 og P2 med kutt-rekkefølge og «Følger av kutt». §7.2 har både «Utenfor v1» og «Senere fase». SM-C1 er et ekte motmål: tjenesten skal ikke presse nybegynnere oppover.

## 3. Oversikt per dimensjon

| Dimensjon | Vurdering | Kort begrunnelse |
|---|---|---|
| Beslutningsklarhet | sterk | §9 viser hvert avvik fra briefen med årsak, og addendum viser vurderte alternativer for input-form. |
| Substans | sterk | Én persona som driver alle tre brukerreisene. NFR-ene har tall (360 px, 44 × 44 px, 20 minutter). |
| Strategisk sammenheng | sterk | Kjerneflyten i §3 og P1/P2 følger tesen. SM-1 og SM-C1 måler tesen, ikke aktivitet. |
| Testbarhet | god | De fleste FR-er er testbare, men FR-19 har uavklarte kanttilfeller og FR-17.1 har ingen målbar konsekvens. |
| Scope og avgrensning | god | Eksplisitt og prioritert, men totalomfanget er stort for én person, og dataarbeidet i FR-1 er ikke synlig som risiko. |
| Brukbarhet for neste fase | god | ID-ene er konsistente og begrepsbruken er jevn. Dokumentet er langt, og ordlyd og budskap er delt mellom PRD og `EXPERIENCE.md`. |
| Formtilpasning | god | Brukerreiser passer et forbrukerprodukt. Endringsloggen og detaljnivået gjør formen tung for én gruppe. |

## 4. Viktigste forbedringer

### 4.1 Nivåreglene i FR-19 har uavklarte kanttilfeller
- **Alvorlighet:** høy
- **Hvor:** §4.8 FR-19: «Sperren oppheves når en tur, uansett hvilken, er vurdert *moderat*» og «telles fra siste nivåendring»
- **Problem og hvorfor det betyr noe:** Personaliseringen er det som skiller produktet fra andre turapper (SM-4, FR-21, SM-C1). Likevel står det ikke hva nivåtaket blir når sperren oppheves, om en sperre eller opphevelse nullstiller telleren for heving, eller hva som skjer på svart nivå. Uten dette må den som koder, gjette, og testbrukeren (FR-21) kan komme til å vise noe annet enn det SM-2 tester.
- **Forslag:** Legg til konsekvenser som kan bli tester, for eksempel:
  - «Tak grønt og tre registreringer av grønne turer vurdert *lett* gir tak blått. Telleren nullstilles.»
  - «Tak blått og en blå tur vurdert *vanskelig* gir tak grønt. Når en tur senere vurderes *moderat*, går taket tilbake til blått.» (Avgjør om dette er riktig, og skriv det.)
  - «Tak svart: ingen heving. Lett-vurderinger av turer under taket teller ikke mot heving.»

### 4.2 Omfanget er stort, og dataarbeidet i FR-1 er skjult
- **Alvorlighet:** medium
- **Hvor:** §4.1 FR-1 («20–30 turer … Hver rutelinje er kontrollert manuelt») og §7.1 P1
- **Problem og hvorfor det betyr noe:** P1 omfatter 21 FR-er pluss KI, vær, kart, konto og personalisering. Å bygge en turdatabase med høydeprofiler fra Kartverket, støyfiltrering, kontroll mot publisert profil og håndplukket OSM er et arbeid som kan ta like mye tid som resten. Vurderingen i briefen var «gjennomførbart med justert omfang», og her ligger risikoen i dataene.
- **Forslag:** Sett en nedre grense i P1 («minst 15 turer ferdigstilt før funksjonene bygges, resten er P2») og vurder å flytte turillustrasjonen (FR-6) til P2, mens «Kartet i tekst» beholdes som UU-krav.

### 4.3 KI-kostnad, misbruk og logging er ikke kravfestet
- **Alvorlighet:** medium
- **Hvor:** §0 («Valg av språkmodell, kostnad og repostruktur avgjøres i arkitekturen»), FR-13 («Forkastede KI-svar logges») og NFR-5/NFR-8
- **Problem og hvorfor det betyr noe:** Gjester kan søke uten konto, så hvem som helst kan utløse KI-kall. Det finnes ingen grense per økt eller per time, og ingen beskrivelse av hva som skjer når grensen nås. Loggen over forkastede svar kan inneholde fritekstønsker, men NFR-5 sier at systemet bare lagrer e-post, hash, historikk og vurderinger.
- **Forslag:** Legg til et krav i NFR-8, for eksempel: «Systemet gjør maks 10 KI-kall per økt og 100 per døgn totalt. Over grensen brukes reserveløsningen (FR-13) uten feilmelding.» Presiser i NFR-5 hva loggen inneholder og hvor lenge den lagres.

### 4.4 P2-kutt og kravene som viser til dem henger ikke helt sammen
- **Alvorlighet:** lav
- **Hvor:** §7.1 «Følger av kutt» mot FR-6, UJ-1 og UJ-2
- **Problem og hvorfor det betyr noe:** FR-6 (P1) lister bekledningstips og UJ-1 viser dem, men FR-9 og FR-10 kan kuttes. UJ-2 bruker fritekstønsket (FR-11), som også er P2. Den som lager stories, kan dermed få et P1-krav som forutsetter et P2-krav.
- **Forslag:** Utvid «Følger av kutt» med én linje om FR-6 («uten FR-9 vises ingen bekledningstips, og kravet om dem i FR-6 faller bort») og merk de berørte setningene i UJ-1 og UJ-2.

### 4.5 Én kilde for ordlyd og budskap
- **Alvorlighet:** lav
- **Hvor:** §0 («Ved motstrid gjelder PRD-en for krav og budskap, og `EXPERIENCE.md` › Mikrotekst for ordlyd»), FR-8, FR-12
- **Problem og hvorfor det betyr noe:** Ferdige meldinger står både i PRD-en og i `EXPERIENCE.md`. Regelen om hvem som gjelder er god, men PRD-en på ca. 6000 ord er tung å bruke som kilde for stories.
- **Forslag:** La PRD-en nøye seg med budskapet i én setning per melding, og la ordlyden bo i `EXPERIENCE.md`. Det kutter lengden og fjerner dobbeltvedlikehold.

## 5. Mekaniske funn

- ID-ene er sammenhengende: FR-1–FR-21, NFR-1–NFR-9, UJ-1–UJ-3, SM-1–SM-4 og SM-C1. De fleste krysshenvisninger løser seg. `FR-17.1` bryter heltallsnummereringen, men er forklart.
- Glossaret er brukt jevnt. «Nivå», «turnivå» og «nivåtak» holdes stort sett ryddig fra hverandre.
- Ingen inline `[ASSUMPTION]`-tagger og ingen egen antakelsesindeks. Antakelsene er i stedet godkjent og logget (§10). Det fungerer, men det er vanskeligere å se hva som fortsatt er en antakelse.
- UJ-2 henviser ikke til FR-16 eller FR-17.1 med ID, og scenen forutsetter ekstra registrerte turer («For å holde reisen kort antar vi …»). Det går bra som forenkling, men vis at oppsettet tilsvarer testbrukeren (FR-21).

## 6. Før dere går videre

**Må avklares før epics og stories:**
- Kanttilfellene i FR-19 (4.1).
- Grense for KI-kall og hva loggen inneholder (4.3).
- Minste antall turer i P1 (4.2).

**Kan vente:** ordlyd i tekster merket som antakelser i `EXPERIENCE.md` (står allerede i §10 som ikke-blokkerende).

**Oppfølging av tilbakemeldingen på product brief:** Ja. Kuratert turdatabase, ett område (Oslo og Bærum), nybegynnere som primærbruker, testbare personaliseringsregler, regelbasert reserveløsning for KI og testbruker er alle fulgt opp. Kostnad er bare delvis fulgt opp, siden den skyves til arkitekturen.

## 7. Refleksjonsspørsmål

1. FR-19 beskriver reglene i prosa. Hvordan ville dere sjekket at en KI-assistent som koder dem, har forstått «sperre» og «heving» likt, og ikke bare skrevet kode som ser riktig ut?
2. PRD-en har gått gjennom mange KI-assisterte gjennomganger (versjon 1.0 til 1.3). Hvilke forslag fra gjennomgangene valgte dere bort, og hva var begrunnelsen?

_Vurdert mot kvalitetsrubrikken i bmad-prd. Dette er veiledning, ikke sensur._
