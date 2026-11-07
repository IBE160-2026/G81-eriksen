---
title: "PRD: Your Next Adventure"
status: final
created: 2026-10-29
updated: 2026-11-07
---

# PRD: Your Next Adventure

## 0. Om dokumentet

Denne PRD-en beskriver versjon 1 (v1) av *Your Next Adventure*. Prosjektet er et fagprosjekt i IBE160. Dokumentet bygger på:
- product brief (`docs/product-brief-your-next-adventure-no.md`)
- tilbakemeldingen fra faglærer (`docs/tilbakemelding-product-brief.md`)
- den tekniske researchen om turdata i Oslomarka (`_bmad-output/planning-artifacts/research/`)
- UX-spesifikasjonen (`_bmad-output/planning-artifacts/ux-designs/ux-G81-eriksen-2026-11-06/`), se §6.

**Der PRD-en avviker fra briefen, gjelder PRD-en.** Alle avvik står i §9. Avvik som oppstår under implementeringen, føres også i §9 og i endringsloggen, med henvisning til story eller PR. Ved motstrid gjelder PRD-en for krav og budskap, og `EXPERIENCE.md` › Mikrotekst for ordlyd.

Alle krav har faste ID-er: UJ for brukerreiser, FR for funksjonelle krav, NFR for ikke-funksjonelle krav og SM for suksessmål. Begrepene i §3 brukes konsekvent. Antakelser og åpne spørsmål samles i §10.

Bakgrunnen for valgene og tekniske detaljer ligger i `addendum.md`, og verifiseringen av graderingsreglene ligger i `research-gradering.md`. Valg av språkmodell, kostnad og repostruktur avgjøres i arkitekturen.

## 1. Visjon

*Your Next Adventure* er en nettside for nybegynnere som vil på fottur i Oslo-området. Brukeren oppgir hvor lenge hen vil være ute og hvilken dag turen skal være. Hen kan også velge startpunkt og turtype og skrive ønsker i vanlig språk. Tjenesten svarer med ett konkret turforslag: rute på kart, estimert tid, bekledningstips ut fra været og en kort forklaring på hvorfor turen passer.

Problemet er at planleggingen tar for lang tid. Nybegynnere må lete på ut.no, i turkart, i blogger og på Google Maps, og likevel ender de ofte på en tur som er for lett, for hard eller av feil type. Eksisterende verktøy viser det samme til alle.

*Your Next Adventure* tilpasser seg brukeren. En bruker med konto vurderer turene sine, og tjenesten bruker vurderingene til å foreslå riktig nivå og variasjon neste gang. I v1 skjer tilpasningen etter enkle, faste regler som alltid kan forklares. KI hjelper bare med å tolke ønsker og formulere begrunnelser. KI velger aldri en tur utenfor den kuraterte turdatabasen.

På sikt kan tilpasningen gå fra faste regler til å lære av brukerens historikk. Tjenesten kan også utvides til flere regioner og aktiviteter. Ett prinsipp ligger fast: tjenesten forklarer alltid hvorfor en tur blir foreslått.

## 2. Målgruppe

### 2.1 Jobber brukeren vil få gjort

- **Funksjonelt:** Finne en tur som passer tiden og formen min, uten å bruke lang tid på å lete.
- **Emosjonelt:** Føle meg trygg på at turen ikke blir for krevende, og stole nok på forslaget til faktisk å gå turen.
- **Kontekst:** Bestemme meg raskt, ofte spontant, hjemme på PC-en før en fin dag eller på mobilen på vei ut.
- **Over tid:** Få forslag som blir bedre tilpasset meg, og finne igjen turer jeg likte.

### 2.2 Ikke-brukere i v1

Disse er ikke målgruppen i v1: erfarne turgåere, turister, tilflyttere og alle som vil gå turer utenfor Oslo-området.

### 2.3 Brukerreiser

Den detaljerte flyten for hver reise, med feilveier, står i `EXPERIENCE.md` › Key Flows. Eksempelturen «Granåsen rundt» er oppdiktet.

**UJ-1. Ola tar en spontan tur en fin dag, uten konto.**
Ola er ikke turvant og kjenner ikke marka godt. Han sitter i sofaen med PC-en og vil på tur til helgen, men han vil ikke bruke tid på å planlegge. Han åpner nettsiden som gjest, og søkeskjemaet møter ham med en gang. Han velger to timer, lørdag og turtypen *utsikt*. Startpunkt og fritekstønske hopper han over.

Han får ett turforslag: «Granåsen rundt», med start på Granvannet p-plass. Han ser ruten på kart, merket «rundtur, 3,5 km totalt, ca. 130 høydemeter, ca. 1 t 35 min (pauser ikke inkludert)», og turnivået «Grønn – lett». Han ser også bekledningstips for lørdag, en kort begrunnelse merket «✦ Skrevet med KI» og en lenke til turen på ut.no. Turen passer de to timene han har, og den har utsikt, så han bestemmer seg.

Han vil registrere turen etterpå, så han lager konto med e-post og passord. Han kommer tilbake til det samme turforslaget (FR-14) og lar fanen stå åpen.

**Kanttilfelle:** Hadde Ola bedt om *topptur*, og ingen topptur passet innenfor to timer, ville han fått en utsiktstur og meldingen «Toppturer krever mer tid enn du har oppgitt» (FR-8).

**UJ-2. Ola kommer tilbake og får bedre forslag.**
Lørdag ettermiddag, rett etter turen, sitter Ola hjemme ved PC-en, og fanen med turforslaget er fortsatt åpen. For å holde reisen kort antar vi at Ola allerede har registrert to grønne turer vurdert *lett*, fra søk han gjorde i andre faner.

Han trykker «Registrer gjennomført tur» og oppgir dato, brukt tid (1 t 50 min), hvor vanskelig turen føltes (*lett / moderat / vanskelig*) og hvor fornøyd han var (1–5). Han velger *lett* og 5. I historikken står turen øverst, med brukt tid sammen med estimert tid. Dette er hans tredje grønne tur vurdert *lett*, så nivåtaket heves til blått (FR-19).

Når han søker igjen, kommer blå turer først, fordi nivåtaket nettopp er hevet (FR-5). Han får en tur merket «Blå – moderat», og begrunnelsen sier: «Du får en blå tur fordi de tre siste grønne turene var lette for deg.» Tjenesten prioriterer turer han ikke har gått. Hadde Ola heller villet ha en lett tur, kunne han skrevet «helst en lett tur» som fritekstønske (FR-11) eller trykket «Nytt forslag», som etter hvert også gir grønne turer. Senere åpner han favoritturen fra historikken. Den vises under «Fra historikken din», med bekledningstips for i dag, og han går den igjen (FR-17).

**UJ-3. Ola sletter kontoen.**
Ola vil ikke lenger bruke tjenesten. Han går til Konto og trykker «Slett konto». En egen side spør i nøktern tone «Vil du slette kontoen?» og sier at hele historikken slettes for godt og ikke kan angres. Han bekrefter. Han blir logget ut, står på søkesiden som gjest og får en kvittering på at kontoen er slettet (FR-15).

## 3. Begreper

- **Tur:** En kuratert fottur i turdatabasen. Hver tur har navn, startpunkt, rutelinje, lengde, høydemeter, nedstigning, høydeprofil, form (tur-retur eller rundtur), turnivå, én eller flere turtyper, estimert tid og en valgfri ut.no-lenke.
- **Tur-retur / rundtur:** En tur-retur går samme vei tilbake. Lengde, høydemeter og nedstigning lagres da for én vei. En rundtur går i ring. Da lagres verdiene for hele runden.
- **Høydemeter:** Samlet stigning. **Nedstigning:** Samlet nedstigning.
- **Turdatabase:** En samling på 20–30 turer i Oslo-området som er kuratert på forhånd.
- **Startpunkt:** Et navngitt sted der en eller flere turer starter. Velges fra en liste.
- **Turtype:** *marka*, *utsikt* eller *topptur*. En tur kan ha flere turtyper.
- **Turnivå:** Farge (grønn, blå, rød eller svart) satt etter Merkehåndbokas graderingsmal (FR-2). Rekkefølgen er grønn < blå < rød < svart. Hver farge har et vurderingsord: grønn = *lett*, blå og rød = *moderat*, svart = *vanskelig*.
- **Varighet:** Hvor lenge brukeren vil være ute, valgt i halvtimessteg (FR-4).
- **Kjerneflyt:** søke som gjest → få turforslag → lage konto → registrere turen som gjennomført med vurdering → søke på nytt (UJ-1 og UJ-2).
- **Søk:** Det brukeren sender inn: varighet, dato, og eventuelt startpunkt, turtype og fritekstønske.
- **Økt:** Perioden fra et søk sendes til et nytt søk sendes eller fanen lukkes (FR-7).
- **Fritekstønske:** Valgfri tekst i vanlig språk, for eksempel «helst ved vann». Tolkes av KI.
- **Turforslag:** Én tur vist som svar på et søk, med begrunnelse.
- **Turforslag fra historikken:** En tur brukeren selv åpner fra historikken. Den vises som et turforslag, men regnes ikke som et forslag fra tjenesten i FR-5, FR-19 og SM-C1 (FR-17).
- **Begrunnelse:** En kort tekst om hvorfor turen passer søket. Skrives av KI eller lages fra en fast mal (FR-12, FR-13, FR-17).
- **Estimert tid:** Gangtid for hele turen, beregnet med sveitsisk regel og påslag for nybegynnere (FR-3). Pauser er ikke inkludert.
- **Bekledningstips:** Råd om klær og utstyr ut fra værvarselet for startpunktet og datoen (FR-9).
- **Gjest:** En person som ikke er logget inn.
- **Bruker:** En person med konto som er logget inn. Der «brukeren» står om søk og turforslag, gjelder det både gjest og bruker.
- **Gjennomført tur:** En tur som brukeren har registrert som gått, med dato og vurdering.
- **Vurdering:** Brukt tid, opplevd vanskelighet (*lett / moderat / vanskelig*) og fornøydhet (1–5).
- **Historikk:** Brukerens liste over gjennomførte turer med vurderinger.
- **Nivåtak:** Det høyeste turnivået systemet foreslår for en bruker. Nivåtaket er en hard grense (FR-19).
- **Sperre:** En midlertidig senking av nivåtaket etter en tur vurdert *vanskelig* (FR-19).
- **Reserveløsning:** Regelbasert oppførsel når KI mangler eller feiler (FR-13).
- **Testbruker:** En ferdig konto med oppdiktet historikk som viser personaliseringen.

## 4. Funksjoner

### 4.1 Turdatabase

**Beskrivelse:** All turdata kommer fra turdatabasen, som er kuratert og bygget på forhånd. Appen henter ingen turdata fra eksterne tjenester mens den kjører.

#### FR-1: Kuratert turdatabase
Systemet har en turdatabase med 20–30 turer i Oslo og Bærum. Gjelder UJ-1 og UJ-2.
- **Felt:** Hver tur har alle feltene som er listet under *Tur* i §3. Kilde og lisens er registrert for hver tur.
- **Kilder:**
  - Rutelinjene kommer fra Turrutebasen fra Kartverket.
  - OpenStreetMap (OSM) brukes bare som supplement for turer som mangler i Turrutebasen. OSM-data hentes i ett håndplukket engangsuttrekk med færre enn 100 OSM-objekter totalt (ODbL, se addendum).
  - Høydemeter, nedstigning og høydeprofil beregnes fra Kartverkets høydedata med støyfiltrering når turdatabasen bygges (se addendum). For minst tre turer kontrolleres verdiene mot en publisert høydeprofil.
- **Sammensetning:**
  - Flertallet av turene er grønne eller blå.
  - Databasen har minst én svart tur, minst tre toppturer og minst fem utsiktsturer.
  - Hver turtype har minst én grønn tur med estimert tid under 2 timer, der terrenget gjør det mulig.
  - Hvert startpunkt har minst to turer.
- Hver rutelinje er kontrollert manuelt for sammenheng og riktig startpunkt.

#### FR-2: Gradering etter fast regel
Systemet setter turnivå ut fra lengde og høydemeter etter Merkehåndboka (2019, s. 100–101).

| Turnivå | Lengde | Høydemeter |
|---|---|---|
| Grønn | under 5 km | under 300 |
| Blå | under 10 km | under 600 |
| Rød | under 20 km | under 1000 |
| Svart | over grensen for rød | over grensen for rød |

- Turen får den strengeste av de to fargene som lengden og høydemeterne gir. En verdi som ligger akkurat på en grense, graderes opp.
- Tur-retur graderes etter verdiene for én vei, og rundtur etter verdiene for hele runden, slik standarden gjør.
- Graderingen tar ikke hensyn til terreng, eksponering eller føre (se FR-6).

#### FR-3: Estimert tid
Systemet beregner estimert tid for hele turen slik:
- **Sveitsisk regel:** 15 min per km, pluss 15 min per 100 høydemeter, pluss 15 min per 200 m nedstigning. Leddene summeres.
- **Påslag for nybegynnere:** 15 %.
- **Avrunding:** Tiden vises avrundet til nærmeste 5 minutter.

Detaljer:
- For tur-retur regnes lengde, høydemeter og nedstigning for begge veier. Høydemeterne tilbake er lik nedstigningen ut, og nedstigningen tilbake er lik høydemeterne ut.
- **Regneeksempel:** En tur-retur er 3 km én vei, med 150 høydemeter og 0 m nedstigning ut. Hele turen blir da 6 km med 150 høydemeter og 150 m nedstigning. Det gir (90 + 22,5 + 11,25) × 1,15 = 142,3 min, som vises som «ca. 2 t 20 min».
- Estimert tid vises alltid med teksten «pauser ikke inkludert».
- KI beregner aldri estimert tid eller turnivå.

### 4.2 Søk

**Beskrivelse:** Søkeskjemaet er kort og raskt å fylle ut, både på PC og på mobil. Gjest og bruker ser det samme skjemaet. Gjelder UJ-1.

#### FR-4: Søkeskjema
Gjest eller bruker kan søke etter tur ved å oppgi:

| Felt | Påkrevd | Regler |
|---|---|---|
| Varighet | ja | Velges fra en liste med verdier fra 1 til 8 timer, i halvtimessteg |
| Dato | ja | Standardverdi er i dag. Tillatt periode er fra i dag til 30 dager frem |
| Startpunkt | nei | Velges fra en liste |
| Turtype | nei | Én av turtypene eller «Alle turtyper». «Alle turtyper» er forvalgt |
| Fritekstønske | nei | Maks 200 tegn |

- Alle felt har synlige etiketter.
- Hvis et felt er ugyldig, vises en feilmelding ved feltet, og søket sendes ikke. Ugyldig betyr manglende varighet eller dato, en dato utenfor tillatt periode eller et for langt fritekstønske.
- Valideringen skjer også på serveren.

### 4.3 Turforslag

**Beskrivelse:** Tjenesten viser ett turforslag om gangen. Systemet filtrerer først turdatabasen med faste regler og rangerer deretter turene som er igjen. Gjelder UJ-1 og UJ-2.

#### FR-5: Utvalg og rangering
1. **Filter (harde krav):**
   - Estimert tid er kortere enn eller lik varigheten.
   - Turnivået er ikke høyere enn brukerens nivåtak (FR-19).
   - Turen passer valgt turtype og valgt startpunkt, hvis brukeren har valgt dem.
2. **Rangering, i denne rekkefølgen:**
   1. Turer brukeren ikke har gått, kommer foran gjennomførte turer. Gjennomførte turer med fornøydhet 1–2 kommer sist.
   2. Turer som passer fritekstønsket (FR-11), kommer foran andre. Et ønske som «helst en lett tur» går derfor foran punkt 3.
   3. **Nivåheving:** I det første søket etter at nivåtaket er hevet (FR-19), kommer turer med turnivå lik det nye nivåtaket foran turer under det.
   4. Turer med en foretrukket turtype (FR-20) kommer foran andre.
   5. Står turene fortsatt likt, vinner turen med estimert tid nærmest varigheten.
   6. Står turene fortsatt likt, avgjør tur-ID-en, slik at rekkefølgen alltid er den samme.
- Rangeringen utelukker aldri gjennomførte turer helt.
- «Nytt forslag» (FR-7) går videre nedover i rangeringen. Etter en nivåheving kan brukeren derfor fortsatt få grønne turer.

#### FR-6: Visning av turforslag
Turforslaget viser:
- rutelinjen på kart
- en turillustrasjon: en forenklet tegning av ruten og høydeprofilen, laget fra turdataene (FR-1)
- turnivå med farge **og** tekst, for eksempel «Blå – moderat», og en kort forklaring: «Jeg har beregnet nivået etter Merkehåndbokas mal ut fra lengde og høydemeter. Terreng og føre er ikke vurdert.»
- treff på valgt turtype, hvis brukeren har valgt en
- om turen er tur-retur eller rundtur, tydelig merket
- startpunktets navn, for eksempel «Start: Granvannet p-plass»
- total lengde for hele turen
- estimert tid med «pauser ikke inkludert»
- bekledningstips (FR-9)
- begrunnelsen med KI-merke og forklaringspanel (FR-12)
- lenke til ut.no, hvis turen har en
- kreditering av kart-, rute- og værdata (NFR-7)
- «Kartet i tekst»: en synlig tekstbeskrivelse av ruten som minst nevner startpunkt, form, total lengde, høydemeter og laveste og høyeste punkt. Den er også kartets tekstalternativ for skjermlesere.

Turillustrasjonen og «Kartet i tekst» lages av systemet fra turdataene, aldri av KI.

#### FR-7: Nytt forslag
Brukeren kan be om et nytt turforslag. Hen får da neste tur i rangeringen, aldri en tur som allerede er vist i samme økt. Når alle treff er vist, kommer meldingen «Du har sett alle turene som passer søket», med forslag til hva hen kan endre (FR-8) og et valg om å starte fra første turforslag igjen.
- **Økt (§3):** Ny innlasting av siden beholder turforslaget og listen over turer som er vist. Et turforslag lever bare i økten, og det finnes ingen delbar lenke til det. Å åpne et turforslag fra historikken endrer ikke økten.

#### FR-8: Ingen treff og utsiktstur i stedet for topptur
- **Ingen topptur passer varigheten:** Systemet viser en utsiktstur og meldingen «Toppturer krever mer tid enn du har oppgitt». Passer heller ingen utsiktstur, gjelder punktet om ingen treff.
- **Bare turer over nivåtaket passer søket:** Systemet viser en melding om det, ikke en tur over nivåtaket. Meldingen tilpasses brukertypen:
  - **Gjest:** «Som ny bruker får du grønne turer. Lag konto og vurder turene dine, så tilpasser jeg forslagene etter hvordan turene kjentes for deg.»
  - **Bruker uten historikk:** Samme budskap, men meldingen ber brukeren registrere og vurdere turene hen går, i stedet for å lage konto.
  - **Bruker med historikk:** Meldingen sier hvilket turnivå tjenesten nå foreslår turer opp til, og at ingen av disse turene passer søket.

  Budskapet er et krav. Ordlyden for bruker uten historikk og bruker med historikk står i `EXPERIENCE.md` › Mikrotekst og er foreløpig (§10).
- **Ingen treff i det hele tatt:** Systemet viser konkrete forslag til hva brukeren kan endre: lengre varighet, et annet startpunkt eller en annen turtype.

### 4.4 Vær og bekledning

**Beskrivelse:** Systemet henter værvarsel fra MET (Yr) for startpunktet og datoen og bruker varselet til bekledningstips. MET-vilkårene krever tre ting: værdata hentes via appens egen server og mellomlagres, kallene har en identifiserende User-Agent, og koordinatene har maks 4 desimaler (detaljer i addendum). Gjelder UJ-1.

#### FR-9: Bekledningstips
Turforslaget viser bekledningstips ut fra værvarselet for startpunktet på dagtid (kl. 10–16) på den valgte datoen. For et turforslag fra historikken gjelder tipsene i dag (FR-17). Tipsene lages etter faste regler, ikke av KI. Flere tips kan vises samtidig.

| Vilkår | Bekledningstips |
|---|---|
| Nedbør ≥ 0,5 mm i perioden | «Fare for nedbør – husk regntøy» |
| Laveste temperatur under 5 °C | «Kaldt – ta med lue, votter og et varmt mellomlag» |
| Laveste temperatur 5–15 °C | «Ta med et ekstra lag» |
| Høyeste temperatur over 20 °C | «Varmt – ta med drikke og solbeskyttelse» |
| Vind ≥ 8 m/s | «Mye vind – ta med vindtett jakke» |
| Alltid | «Gode sko og litt mat og drikke» |

#### FR-10: Mangler værvarsel
Hvis MET ikke har varsel for datoen (i praksis mer enn ca. 9–10 dager frem), eller ikke svarer, viser systemet turforslaget uten bekledningstips og med en melding om hvorfor.

### 4.5 KI-assistanse

**Beskrivelse:** KI er et tillegg og ikke en forutsetning. Kjerneflyten fungerer fullt ut uten KI-nøkkel. Bakgrunnen for dette valget står i addendum.

#### FR-11: Tolking av fritekstønske
Når brukeren har skrevet et fritekstønske, får KI bare fritekstønsket og turene som har kommet gjennom filteret i FR-5. KI svarer med ID-ene til turene som passer ønsket, og svaret brukes som kriterium 2 i rangeringen. Fritekstønsket behandles som data og aldri som instruksjoner til systemet. Gjelder UJ-1.

#### FR-12: Begrunnelse
- Begrunnelsen nevner minst varigheten, og turtypen og fritekstønsket hvis brukeren har oppgitt dem. Unntak: reservemalen nevner ikke fritekstønsket (FR-13).
- Når KI er tilgjengelig, skriver KI begrunnelsen. Ellers lages den fra reservemalen (FR-13).
- Begrunnelsen har maks 300 tegn. Grensen gjelder hele begrunnelsen slik brukeren ser den, etter innsetting av verdier og med personaliseringssetningen. Overskrides grensen, brukes reservemalen (FR-13).
- Har en personaliseringsregel påvirket valget, legger systemet til en personaliseringssetning fra setningsmalen. Eksempel: «Du får en blå tur fordi de tre siste grønne turene var lette for deg.» En regel har påvirket valget når den valgte turen har et turnivå som bare er tillatt fordi nivåtaket er hevet (FR-19), eller når turen er prioritert av nivåhevingen i FR-5. Teksten ved sperre og turtypepreferanse er et åpent punkt (§10).
- KI skriver aldri tall eller turnivå. KI-teksten har plassholderne `{tid}`, `{varighet}`, `{lengde}` og `{nivå}`, og systemet setter inn verdiene fra turdatabasen (FR-1 til FR-3) og søket (se addendum).
- **KI-merke:** Rett over begrunnelsen står «✦ Skrevet med KI» når KI har skrevet den. Er begrunnelsen laget fra en mal, står «Begrunnelse fra mal» i stedet.
- Turforslag fra historikken følger FR-17.
- **Forklaringspanel:** Brukeren kan felle ut «Slik lager jeg forslaget». Panelet er lukket som standard, og teksten sier i jeg-form at
  - ruten, tiden og nivået kommer fra Kartverkets turdata og faste formler, ikke fra KI
  - KI tolker ønsket og skriver begrunnelsen, og KI kan ta feil
  - tiden kan bomme med rundt 15 %, og nybegynnere bruker ofte lenger tid enn beregnet.

  Ordlyden står i `EXPERIENCE.md` › Component Patterns (Forklaringspanel).

#### FR-13: Validering og reserveløsning
- Systemet forkaster et KI-svar som:
  - viser til en tur utenfor de filtrerte treffene
  - er tomt eller ugyldig
  - gir en begrunnelse over 300 tegn slik brukeren ser den, etter innsetting av verdier og med personaliseringssetningen (FR-12)
  - har tall eller turnivå i begrunnelsen utenfor plassholderne (FR-12)
  - kommer etter tidsgrensen på 5 sekunder.
- Da brukes reserveløsningen: fritekstønsket ignoreres, og begrunnelsen lages fra reservemalen. Forkastede KI-svar logges, slik at de kan brukes i kvalitetssikringen.
- Reserveløsningen brukes også når KI-nøkkelen mangler.
- Har brukeren skrevet et fritekstønske som ble ignorert, viser systemet meldingen «Jeg kunne ikke ta hensyn til ønsket ditt denne gangen». KI-merket viser «Begrunnelse fra mal» (FR-12). Reservemalen viser aldri til fritekstønsket.

### 4.6 Konto

**Beskrivelse:** Konto er valgfri. Den gir vurdering, historikk og personalisering. Gjelder UJ-1, UJ-2 og UJ-3.

#### FR-14: Lage konto, logge inn og logge ut
- Gjest kan lage konto med e-post og passord. Passordet må ha minst 8 tegn og lagres bare som hash.
- Hvis e-posten allerede er registrert, viser systemet «Kunne ikke lage konto – prøv å logge inn».
- Ved feil innlogging viser systemet «Feil e-post eller passord», uten å si hvilket av dem som er feil.
- Bruker kan logge ut.
- Når en gjest prøver en funksjon som krever konto, blir hen bedt om å logge inn eller lage konto. Turforslaget gjesten så på, beholdes gjennom kontooppretting og innlogging.
- En gjest som har trykket «Registrer gjennomført tur», går etter innlogging eller kontooppretting rett inn i registreringen av den turen (FR-16).

#### FR-15: Slette konto
Bruker kan slette kontoen sin etter å ha bekreftet det på en egen side. Gjelder UJ-3.
- Da slettes kontoen permanent, sammen med e-post, passord-hash og all historikk og alle vurderinger. Brukeren blir logget ut og får som gjest en kvittering på at kontoen er slettet.
- Feiler slettingen, slettes ingenting, og brukeren får en feilmelding med neste steg.
- Avbryter brukeren, endres ingenting.

### 4.7 Vurdering og historikk

#### FR-16: Registrere gjennomført tur
Bruker kan registrere en tur som gjennomført, enten direkte fra turforslaget eller fra historikken. Gjelder UJ-2.
- Bruker oppgir:
  - dato (standardverdi er i dag, og datoen kan ikke være frem i tid)
  - brukt tid (fra 10 minutter til 24 timer)
  - opplevd vanskelighet (*lett / moderat / vanskelig*)
  - fornøydhet (1–5).
- Alle feltene er påkrevd.

#### FR-17: Se historikk
Bruker kan se historikken sin med tur, dato og vurdering, der brukt tid vises sammen med estimert tid. Bruker kan åpne en tur fra historikken og få den vist som turforslag fra historikken (§3). Gjelder UJ-2.
- **Over nivåtaket:** Bruker kan åpne en tur fra historikken også når turnivået er over det nåværende nivåtaket. Det er brukerens eget valg, så den harde grensen i FR-19 og kontrollen i SM-C1 gjelder ikke. Turforslaget viser da merknaden «Denne turen er over nivået jeg foreslår for deg nå.»
- **Turforslag fra historikken** avviker fra et vanlig turforslag:
  - Linjen «Fra historikken din» står i stedet for søkeoppsummeringen.
  - Begrunnelsen lages fra en fast mal uten KI, for eksempel «Du gikk denne turen 12. oktober og ga den 5 av 5.» KI-merket viser «Begrunnelse fra mal» (FR-12), og kravet i FR-12 om å nevne varigheten gjelder ikke.
  - Bekledningstipsene gjelder i dag (FR-9).
  - «Nytt forslag» (FR-7) er byttet ut med «Finn en ny tur», som går til søket.

#### FR-17.1: Fremgang mot neste nivå (P2, §7.1)
Historikken kan vise hvor nær brukeren er neste nivåheving etter FR-19 og FR-5. Ordlyden står i `EXPERIENCE.md` › Mikrotekst. Gjelder UJ-2.

### 4.8 Personalisering

**Beskrivelse:** Personaliseringen bruker faste regler som kan forklares. Reglene bygger på briefen (SC 5–8), og endringene står i §9.

#### FR-18: Startnivå
Gjest og bruker uten historikk har grønt nivåtak. De får altså bare grønne turer.

#### FR-19: Nivåregler
- **Heving:** Når tre gjennomførte turer med turnivå lik nivåtaket er vurdert *lett*, hever systemet nivåtaket ett nivå. Vurderingene trenger ikke komme etter hverandre, men telles fra siste nivåendring.
- **Sperre:** Når en tur er vurdert *vanskelig*, senkes nivåtaket midlertidig til turnivået for den turen, hvis nivåtaket var høyere. Sperren oppheves når en tur, uansett hvilken, er vurdert *moderat*.
- **Hard grense:** Turer over nivåtaket blir aldri foreslått (FR-5). Turforslag fra historikken følger FR-17.
- **Gjentakelser:** Hver registrering av en gjennomført tur teller, også når samme tur registreres flere ganger.

#### FR-20: Turtypepreferanse
Turtyper fra gjennomførte turer med fornøydhet 4–5 er foretrukne turtyper. Turer med slike turtyper rangeres høyere (FR-5).

### 4.9 Testbruker

#### FR-21: Testbruker
Systemet leveres med en testbruker med oppdiktet historikk. Testbrukeren viser nivåheving, sperre og turtypepreferanse (FR-18 til FR-20) uten at noen må gå turer. Innloggingsdataene står i README.

## 5. Tverrgående ikke-funksjonelle krav

- **NFR-1 Kjørbarhet:**
  - Appen kan installeres og startes lokalt med README som eneste veiledning, på under 20 minutter og uten ekte nøkler.
  - Kart, vær og turdatabase fungerer uten nøkler.
  - Turdatabasen og testbrukeren lastes automatisk ved oppstart eller med én kommando.
  - `.env.example` følger med, og hemmeligheter ligger aldri i repoet eller i git-historikken.
- **NFR-2 Stabilitet:**
  - Appen tåler feil input, gjentatte handlinger og dobbel innsending uten å krasje.
  - Alle tilstander i §6 viser enten et turforslag eller en forklaring med neste steg.
- **NFR-3 Mobil:**
  - Siden fungerer ned til 360 px bredde uten horisontal rulling. Bare kartet og historikktabellen kan rulle i egen beholder.
  - På mobil er turnivået, den estimerte tiden og treff på valgt turtype synlige uten rulling. Kartet og bekledningstipsene nås med kort rulling. Rekkefølgen står i `EXPERIENCE.md` › Turforslag – rekkefølge.
  - Knapper er minst 44 × 44 px.
- **NFR-4 Universell utforming:** WCAG 2.1 AA er målet. Det betyr minst:
  - kontrast på minst 4,5:1
  - alle handlinger i kjerneflyten kan gjøres med tastatur
  - feilmeldinger er koblet til feltet og leses opp av skjermleser
  - kartet holder ikke på tastaturfokus
  - informasjon gis aldri bare med farge
  - dynamisk tilpasning (reflow) ved 320 px bredde.

  Kravet verifiseres med et automatisk verktøy og sjekklisten i `EXPERIENCE.md` › Accessibility Floor (SM-4).
- **NFR-5 Personvern:**
  - Systemet samler inn så lite data som mulig. Det lagrer bare e-post, passord som hash, historikk og vurderinger.
  - Systemet sporer ikke posisjon.
  - Ingen personopplysninger sendes til KI-leverandøren. KI får bare søket og turene som kan foreslås.
  - Skjermen Konto viser en kort personverntekst i jeg-form om punktene over. Ordlyden står i `EXPERIENCE.md` › Mikrotekst og er foreløpig (§10).
- **NFR-6 Sporbarhet:** Kode, tester, stories, commits og PR-er viser til FR- og NFR-ID-ene i denne PRD-en.
- **NFR-7 Kreditering:** Appen viser kreditering slik lisensene krever, minst «© Kartverket», «© OpenStreetMap contributors» med lenke og «Data fra MET Norge» (MET anbefaler «Data from MET Norway»).
- **NFR-8 Sikkerhet:**
  - En bruker kan bare se og endre sin egen historikk og konto.
  - All input valideres på serveren.
  - Fritekstønsket behandles som data og ikke som instruksjoner (FR-11). KI-svar valideres alltid (FR-13).
- **NFR-9 Mørk modus (P2, §7.1):** Siden følger innstillingen for lys eller mørk modus på enheten. Det finnes ingen egen bryter.

## 6. Plattform, skjermer og tone

Nettside på norsk. Den lages for PC først, med en enkel, stablet mobilutgave i v1. NFR-3 gjelder fullt ut, og mørk modus står i NFR-9. V1 har ingen mobilapp.

**Skjermer:**
- Søk
- Turforslag
- Logg inn / Lag konto
- Registrer gjennomført tur
- Historikk
- Konto, med personverntekst (NFR-5) og sletting med egen bekreftelsesside (FR-15)

**Tilstander som skal designes:**
- laster
- feil i skjemaet (FR-4)
- ingen treff og ingen treff innenfor nivåtaket (FR-8)
- alle forslag er vist (FR-7)
- uten værvarsel (FR-10)
- reserveløsning (FR-13)
- gjest som møter krav om konto (FR-14)
- turforslag fra historikken, også over nivåtaket (FR-17)
- turforslaget finnes ikke lenger, fordi fanen er lukket eller adressen er åpnet direkte (FR-7)

**UX-spesifikasjon:** `DESIGN.md` og `EXPERIENCE.md` i `../../ux-designs/ux-G81-eriksen-2026-11-06/` er UX-spesifikasjonen. `EXPERIENCE.md` › Mikrotekst har tekstene i grensesnittet som PRD-en ikke gir. Wireframes:
- [Skjermer, ruter og tilgang](../../ux-designs/ux-G81-eriksen-2026-11-06/wireframes/ia-2026-11-06.excalidraw)
- [UJ-1, UJ-2 og kanttilstander](../../ux-designs/ux-G81-eriksen-2026-11-06/wireframes/flow-ola-2026-11-06.excalidraw)

**Stemme og tone:** Tjenesten snakker i jeg-form, og brukeren tiltales med du. Tonen er innbydende og trygg, og nøktern ved feil, innlogging og sletting. Tjenesten overselger ikke KI eller «læring» og forklarer alltid hvorfor en tur blir foreslått.

## 7. Scope

### 7.1 Med i v1

Alle funksjonene i §4 (FR-1 til FR-21 og FR-17.1) og alle NFR-ene i §5 (NFR-1 til NFR-9).

**Prioritering:**
- **P1, må leveres:** FR-1 til FR-8, FR-12 og FR-13 (begrunnelse skrevet av KI og begrunnelse fra mal som reserveløsning, KI-merke og forklaringspanel), FR-14 til FR-19 (uten FR-17.1), FR-21 og NFR-1 til NFR-8.
- **P2, kuttes først hvis tiden ikke strekker til**, i denne rekkefølgen:
  1. FR-17.1 (fremgang mot neste nivå)
  2. NFR-9 (mørk modus)
  3. FR-11 (KI-tolking av fritekstønske)
  4. FR-9 og FR-10 (bekledningstips)
  5. FR-20 (turtypepreferanse)
- **Følger av kutt:**
  - Kuttes FR-11, skjules fritekstfeltet, og forklaringspanelet mister setningen om at KI tolker ønsket. Etter en nivåheving (FR-5) får brukeren da grønne turer bare med «Nytt forslag».
  - Kuttes et P2-krav, faller tilsvarende del av FR-21, SM-2 og NFR-3 bort, for eksempel turtypepreferansen hos testbrukeren og bekledningstipsene i NFR-3.
- Hvert kutt føres i §9 og i endringsloggen, med årsak.

### 7.2 Utenfor v1

- Turer utenfor Oslo-området
- Ruter laget av KI og turer utenfor turdatabasen
- Henting av turdata mens appen kjører
- Andre målgrupper enn nybegynnere
- Værvarsling som egen tjeneste
- Terrengstatus og føre
- Mobilapp
- Sosiale funksjoner
- Offline-navigering
- Booking og transport
- Flere språk enn norsk

**Senere fase:**
- Personlig justering av estimert tid ut fra brukt tid
- Valg av startpunkt med klikk i kartet
- Glemt passord, som krever en e-posttjeneste og ville blitt den femte eksterne avhengigheten
- Sletting av enkeltregistreringer i historikken (v1 har bare full kontosletting, FR-15)
- Redigering og angring av registreringer

## 8. Suksessmål

**Primært mål**
- **SM-1:** Manuell brukertest med 3–5 nybegynnere.
  - **Mål:** Minst 75 % klarer kjerneflyten (§3) uten hjelp og vurderer det første turforslaget som relevant. Med 3 testere må alle 3 klare det, med 4 må 3 klare det, og med 5 må 4 klare det.
  - Resultatet dokumenteres i repoet. Målet validerer FR-4 til FR-8, FR-14, FR-16 og FR-18.

**Sekundære mål**
- **SM-2:** Automatiserte tester dekker disse kravene, og alle testene består:
  - gradering (FR-2) og estimert tid (FR-3), med regneeksempelet som testtilfelle
  - skjemavalidering (FR-4)
  - utvalg og rangering (FR-5)
  - nytt forslag og ingen treff (FR-7 og FR-8)
  - KI-validering og reserveløsning med KI mocket (FR-13)
  - startnivå, nivåregler og turtypepreferanse (FR-18 til FR-20).
- **SM-3:** Hele kjerneflyten fungerer uten KI-nøkkel (FR-13, NFR-1).
- **SM-4:** Mobilvisning og universell utforming (UU) består en manuell test etter sjekklisten i `EXPERIENCE.md` › Accessibility Floor (NFR-3, NFR-4). Personaliseringen demonstreres med testbrukeren (FR-21).

**Motmål (skal ikke optimaliseres)**
- **SM-C1:** Hvor raskt brukere rykker opp i nivå. Tjenesten skal ikke presse nybegynnere oppover for å se «smart» ut. Kontrollen har to deler:
  - Ingen bruker får foreslått en tur over nivåtaket (testes i SM-2).
  - Ingen testere i SM-1 vurderer det første turforslaget som *vanskelig*.

  Motmålet veier opp mot SM-1.

## 9. Endringer fra product brief

| Endring | Årsak |
|---|---|
| Konto er valgfri, og gjester kan søke | Lavere terskel for spontan bruk (UJ-1). Gjør det også enklere for sensor å teste |
| Søket gjøres i et skjema med valgfritt fritekstønske, ikke bare som fritekst | Kjerneflyten fungerer uten KI-nøkkel, og KI-delen er avgrenset (se addendum) |
| Vurderingen er *lett / moderat / vanskelig*, fornøydhet 1–5 og brukt tid, i stedet for *for lett / passe / for hard* og *likte / likte ikke* | Mer informasjon per tur. Nivåreglene beholdes med nye ord: *for lett* → *lett*, *passe* → *moderat*, *for hard* → *vanskelig*. «Likte» tilsvarer fornøydhet 4–5 (FR-19, FR-20) |
| «Likte ikke» (fornøydhet 1–2) gjør at turen rangeres sist, men den utelukkes ikke | Brukeren kan ha endret mening, og turen finnes fortsatt i historikken |
| Nivåtaket er en hard grense, ikke bare en rangering | Tryggest for nybegynnere |
| Ett forslag om gangen, med mulighet for «Nytt forslag» | Raskere valg for brukeren |
| Lenke til ut.no | Brukeren kan se mer om ruten |
| Startpunkt velges fra en liste | Brukeren kan ikke havne utenfor Oslo-området, så feilmeldingen fra briefen om steder utenfor området trengs ikke |
| Turtypen «skogstur» er erstattet med «marka» | Faste turtyper: marka, utsikt og topptur |
| Terskler og formel for estimert tid er fastsatt, med 15 % påslag for nybegynnere | Tersklene er verifisert mot Merkehåndboka. Sveitsisk regel passer nybegynnere. Formlene bommer med omtrent ±15 % |
| Turrutebasen er primærkilde, og OSM er bare et supplement | Åpen lisens, oppdatert jevnlig, og den vant sammenligningen i researchen. ODbL begrenser bruken av OSM |
| Kreditering av kart- og værdata er et krav (NFR-7) | Lisensene krever det |
| «Praktiske tips» er avgrenset til bekledningstips i v1 | Mindre omfang |
| Bare norsk i v1, ikke norsk og engelsk | Mindre omfang |
| Steget «lagre» er erstattet med «registrere gjennomført tur» | Lagring av planlagte turer gir lite verdi ved spontan bruk |
| Brukertestmålet er 75 % i stedet for «4 av 5» | Fungerer med 3–5 testere |

**Sporing fra briefens suksesskriterier:**

| Brief | PRD |
|---|---|
| SC 1 | FR-6 |
| SC 2 | FR-13 |
| SC 3 | FR-3, FR-5 |
| SC 4 | FR-16 |
| SC 5 | FR-18 |
| SC 6 | FR-19 |
| SC 7 | FR-19 |
| SC 8 | FR-5, FR-20 |
| SC 9 | FR-21 |
| SC 10 | SM-1 |

## 10. Antakelser og åpne spørsmål

Antakelsene og standardverdiene i kravene, endringene i v1.1 og rettingene etter gjennomgangen av v1.1 ble godkjent av produkteier 2026-11-06 (`.memlog.md`). Tekster merket `[ASSUMPTION]` i `EXPERIENCE.md` › Mikrotekst bekreftes under implementeringen. Disse punktene er fortsatt åpne:

| Åpent punkt | Eier | Blokkerer stories |
|---|---|---|
| Ordlyden i tekster merket som antakelser i `EXPERIENCE.md` › Mikrotekst, blant annet nivåtakmeldingene (FR-8) og personverntekst (NFR-5). Budskapet er avgjort | UX | nei |
| Tekst i begrunnelsen ved sperre (FR-19) og turtypepreferanse (FR-20), og om disse reglene regnes som å ha påvirket valget (FR-12) | UX | nei |

Åpne punkter som bare gjelder UX eller arkitektur, står i `EXPERIENCE.md` › Åpne punkter.

## Endringslogg

| Versjon | Dato | Endring |
|---|---|---|
| 0.1 | 2026-10-29 | Arbeidsmappe opprettet. Kildene er hentet ut |
| 0.2 | 2026-11-06 | Første fullstendige utkast, skrevet etter en coaching-økt basert på brukerreiser. Beslutningene står i `.memlog.md` |
| 0.3 | 2026-11-06 | Antakelsene om bekledningstips (FR-9), nivåregler (FR-19) og turtypepreferanse (FR-20) er bekreftet. Gjentatte registreringer teller |
| 0.4 | 2026-11-06 | Rettet etter gjennomgangen: hard nivågrense, rangering med best tidsutnyttelse, påslag for nybegynnere, prioritering P1/P2, ærlighet når KI feiler, kreditering og overgang fra gjest til konto |
| 0.5 | 2026-11-06 | Standardverdier for middels funn: sammensetning av turdatabasen, terskler for bekledningstips, grenser for KI-svar, kontoregler, målbare NFR-er, NFR-8 Sikkerhet, skjermer og tilstander, SM-4 og sporing fra briefen |
| 0.6 | 2026-11-06 | MET-vilkår og Kartverkets API-er er verifisert, og de åpne punktene i §10 er lukket |
| 1.0 | 2026-11-06 | Struktur- og språkgjennomgang. 41 språkfunn er vurdert: 40 er rettet, og «Scope» er beholdt som BMAD-begrep. PRD-en er markert som ferdig |
| 1.1 | 2026-11-06 | Oppdatert etter UX-arbeidet (`ux-designs/ux-G81-eriksen-2026-11-06/`) og rettet etter gjennomgangen av v1.1 (`review-rubric-v1.1.md`, `reconcile-ux.md`). Berørt: UJ-1 til UJ-3 (UJ-3 er ny), §3, FR-1, FR-4 til FR-9, FR-12 til FR-17, FR-19, NFR-3 til NFR-5, §6, §7, SM-4, SM-C1, §10 og addendum. Struktur- og språkgjennomgang 2026-11-07 (`review-structure-v1.1.md`, `review-prose-v1.1.md`) med nye ID-er FR-17.1 og NFR-9 (begge P2). Beslutningene står i `.memlog.md` |
| 1.2 | 2026-11-07 | Ny gjestetekst i FR-8: «låse opp lengre turer» er erstattet, fordi et høyere turnivå også kan skyldes høydemeter (FR-2), og teksten ikke skal presse nybegynnere (SM-C1). Punktet er fjernet fra §10 |
