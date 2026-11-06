---
title: "PRD: Your Next Adventure"
status: final
created: 2026-10-29
updated: 2026-11-06
---

# PRD: Your Next Adventure

## 0. Om dokumentet

Denne PRD-en beskriver versjon 1 (v1) av *Your Next Adventure*. Prosjektet er et fagprosjekt i IBE160. Dokumentet bygger på:
- product brief (`docs/product-brief-your-next-adventure-no.md`)
- tilbakemeldingen fra faglærer (`docs/tilbakemelding-product-brief.md`)
- den tekniske researchen om turdata i Oslomarka (`_bmad-output/planning-artifacts/research/`).

**Der PRD-en avviker fra briefen, gjelder PRD-en.** Alle avvik står i §9. Avvik som oppstår under implementeringen, føres også i §9 og i endringsloggen, med henvisning til story eller PR.

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
- **Kontekst:** Bestemme meg raskt, ofte spontant en fin dag, eller på mobilen på vei ut.
- **Over tid:** Få forslag som blir bedre tilpasset meg, og finne igjen turer jeg likte.

### 2.2 Ikke-brukere i v1

Disse er ikke målgruppen i v1: erfarne turgåere, turister, tilflyttere og alle som vil gå turer utenfor Oslo-området.

### 2.3 Brukerreiser

**UJ-1. Ola tar en spontan tur en fin dag, uten konto.**
Ola kjenner ikke marka godt. Det er strålende vær, og han trenger frisk luft, men han vil ikke bruke tid på å planlegge. Han åpner nettsiden på mobilen uten å logge inn, og fyller inn at han har tre timer, at turen skal være i dag, og at han vil ha *utsikt*. Startpunktet hopper han over.

Han får ett turforslag: et kart med ruten, merket «tur-retur, 7,2 km totalt, ca. 2 t 40 min (pauser ikke inkludert)», turnivået «Grønn – lett», bekledningstips for dagens vær, en kort begrunnelse og en lenke til turen på ut.no. Han liker ikke helt forslaget og trykker «Nytt forslag». Det neste forslaget passer, så han pakker og går.

**Kanttilfelle:** Hadde Ola bedt om *topptur*, og ingen topptur passet innenfor tre timer, ville han fått en utsiktstur og beskjed om at toppturer krever mer tid.

**UJ-2. Ola kommer tilbake og får bedre forslag.**
Etter noen turer lager Ola en konto. Etter hver tur registrerer han hvor lang tid han brukte, hvor vanskelig turen føltes (*lett / moderat / vanskelig*) og hvor fornøyd han var (1–5). Når han søker igjen, prioriterer tjenesten turer han ikke har gått. Etter tre grønne turer vurdert *lett* får han tilgang til blå turer, og begrunnelsen sier hvorfor. I historikken finner han igjen favoritturen fra i vår og går den igjen.

## 3. Begreper

- **Tur:** En kuratert fottur i turdatabasen. Hver tur har navn, startpunkt, rutelinje, lengde, høydemeter, nedstigning, form (tur-retur eller rundtur), turnivå, én eller flere turtyper, estimert tid og en valgfri ut.no-lenke.
- **Tur-retur / rundtur:** En tur-retur går samme vei tilbake. Lengde, høydemeter og nedstigning lagres da for én vei. En rundtur går i ring. Da lagres verdiene for hele runden.
- **Høydemeter:** Samlet stigning. **Nedstigning:** Samlet nedstigning.
- **Turdatabase:** En samling på 20–30 turer i Oslo-området som er kuratert på forhånd.
- **Startpunkt:** Et navngitt sted der en eller flere turer starter. Velges fra en liste.
- **Turtype:** *marka*, *utsikt* eller *topptur*. En tur kan ha flere turtyper.
- **Turnivå:** Farge (grønn, blå, rød eller svart) satt etter Merkehåndbokas graderingsmal (FR-2). Rekkefølgen er grønn < blå < rød < svart. Hver farge har et vurderingsord: grønn = *lett*, blå og rød = *moderat*, svart = *vanskelig*.
- **Varighet:** Hvor lenge brukeren vil være ute, valgt i halvtimessteg (FR-4).
- **Kjerneflyt:** søke som gjest → få turforslag → registrere seg → registrere turen som gjennomført med vurdering → søke på nytt (UJ-1 og UJ-2).
- **Søk:** Det brukeren sender inn: varighet, dato, og eventuelt startpunkt, turtype og fritekstønske.
- **Økt:** Perioden fra et søk sendes, til et nytt søk sendes eller siden lastes på nytt.
- **Fritekstønske:** Valgfri tekst i vanlig språk, for eksempel «helst ved vann». Tolkes av KI.
- **Turforslag:** Én tur vist som svar på et søk, med begrunnelse.
- **Begrunnelse:** En kort tekst om hvorfor turen passer søket. Skrives av KI eller lages fra en fast mal.
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
  - Høydemeter og nedstigning beregnes fra Kartverkets høydedata med støyfiltrering. For minst tre turer kontrolleres verdiene mot en publisert høydeprofil.
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

**Beskrivelse:** Søkeskjemaet er kort og raskt å fylle ut på mobil. Gjest og bruker ser det samme skjemaet. Gjelder UJ-1.

#### FR-4: Søkeskjema
Gjest eller bruker kan søke etter tur ved å oppgi:

| Felt | Påkrevd | Regler |
|---|---|---|
| Varighet | ja | Velges fra en liste med verdier fra 1 til 8 timer, i halvtimessteg |
| Dato | ja | Standardverdi er i dag. Tillatt periode er fra i dag til 30 dager frem |
| Startpunkt | nei | Velges fra en liste |
| Turtype | nei | Én av turtypene |
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
   2. Turer som passer fritekstønsket (FR-11), kommer foran andre.
   3. Turer med en foretrukket turtype (FR-20) kommer foran andre.
   4. Står turene fortsatt likt, vinner turen som utnytter varigheten best, det vil si den med estimert tid nærmest varigheten.
   5. Er turene fortsatt like, avgjør tur-ID-en, slik at rekkefølgen alltid er den samme.
- Rangeringen utelukker aldri gjennomførte turer helt.

#### FR-6: Visning av turforslag
Turforslaget viser:
- rutelinjen på kart
- turnivå med farge **og** tekst, for eksempel «Blå – moderat», og en kort forklaring: «Beregnet av tjenesten etter Merkehåndbokas mal ut fra lengde og høydemeter. Terreng og føre er ikke vurdert.»
- om turen er tur-retur eller rundtur, tydelig merket
- total lengde for hele turen
- estimert tid med «pauser ikke inkludert»
- bekledningstips (FR-9)
- begrunnelsen (FR-12)
- lenke til ut.no, hvis turen har en
- kreditering av kart-, rute- og værdata (NFR-7).

Kartet har en tekstbeskrivelse for skjermlesere.

#### FR-7: Nytt forslag
Brukeren kan be om et nytt turforslag. Hen får da neste tur i rangeringen, aldri en tur som allerede er vist i samme økt. Er alle treff vist, viser systemet meldingen «Du har sett alle turene som passer søket», med forslag til hva hen kan endre (FR-8) og et valg om å starte fra første turforslag igjen.

#### FR-8: Ingen treff og utsiktstur i stedet for topptur
- **Ingen topptur passer varigheten:** Systemet viser en utsiktstur og meldingen «Toppturer krever mer tid enn du har oppgitt». Passer heller ingen utsiktstur, gjelder punktet om ingen treff.
- **Bare turer over nivåtaket passer søket:** Systemet viser en melding om det, ikke en tur over nivåtaket. For gjester og brukere uten historikk sier meldingen: «Som ny bruker får du grønne turer. Lag konto og vurder turene dine for å låse opp lengre turer.»
- **Ingen treff i det hele tatt:** Systemet viser konkrete forslag til hva brukeren kan endre: lengre varighet, et annet startpunkt eller en annen turtype.

### 4.4 Vær og bekledning

**Beskrivelse:** Systemet henter værvarsel fra MET (Yr) for startpunktet og datoen og bruker varselet til bekledningstips. MET-vilkårene krever tre ting: værdata hentes via appens egen server og mellomlagres, kallene har en identifiserende User-Agent, og koordinatene har maks 4 desimaler (detaljer i addendum). Gjelder UJ-1.

#### FR-9: Bekledningstips
Turforslaget viser bekledningstips ut fra værvarselet for startpunktet på dagtid (kl. 10–16) på den valgte datoen. Tipsene lages etter faste regler, ikke av KI. Flere tips kan vises samtidig.

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
- Begrunnelsen nevner minst varigheten, og turtypen og fritekstønsket hvis brukeren har oppgitt dem.
- Har en personaliseringsregel påvirket valget, nevner begrunnelsen regelen. Eksempel: «Du får en blå tur fordi de tre siste grønne turene var lette for deg.»
- Tall som estimert tid, lengde og turnivå settes inn av systemet og skrives aldri av KI.
- Når KI er tilgjengelig, skriver KI begrunnelsen, med maks 300 tegn. Ellers lages den fra en fast mal.

#### FR-13: Validering og reserveløsning
- Systemet forkaster et KI-svar som:
  - viser til en tur utenfor de filtrerte treffene
  - er tomt eller ugyldig
  - har en begrunnelse over 300 tegn
  - kommer etter tidsgrensen på 5 sekunder.
- Da brukes reserveløsningen: fritekstønsket ignoreres, og begrunnelsen lages fra malen. Forkastede KI-svar logges, slik at de kan brukes i kvalitetssikringen.
- Reserveløsningen brukes også når KI-nøkkelen mangler.
- Har brukeren skrevet et fritekstønske som ble ignorert, viser systemet meldingen «Vi kunne ikke ta hensyn til ønsket ditt denne gangen». Malteksten viser aldri til fritekstønsket.

### 4.6 Konto

**Beskrivelse:** Konto er valgfri. Den gir vurdering, historikk og personalisering. Gjelder UJ-2.

#### FR-14: Registrere, logge inn og logge ut
- Gjest kan registrere seg med e-post og passord. Passordet må ha minst 8 tegn og lagres bare som hash.
- Hvis e-posten allerede er registrert, viser systemet «Kunne ikke registrere – prøv å logge inn».
- Ved feil innlogging viser systemet «Feil e-post eller passord», uten å si hvilket av dem som er feil.
- Bruker kan logge ut.
- Når en gjest prøver en funksjon som krever konto, blir hen bedt om å logge inn eller registrere seg. Turforslaget gjesten så på, beholdes gjennom registrering og innlogging.

#### FR-15: Slette konto
Bruker kan slette kontoen sin etter å ha bekreftet det. All historikk slettes da permanent.

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
Bruker kan se historikken sin med tur, dato og vurdering, der brukt tid vises sammen med estimert tid. Bruker kan åpne en tur fra historikken og få den vist som turforslag på nytt. Gjelder UJ-2.

### 4.8 Personalisering

**Beskrivelse:** Personaliseringen bruker faste regler som kan forklares. Reglene bygger på briefen (SC 5–8), og endringene står i §9.

#### FR-18: Startnivå
Gjest og bruker uten historikk har grønt nivåtak. De får altså bare grønne turer.

#### FR-19: Nivåregler
- **Heving:** Når tre gjennomførte turer med turnivå lik nivåtaket er vurdert *lett*, hever systemet nivåtaket ett nivå. Vurderingene trenger ikke komme etter hverandre, men telles fra siste nivåendring.
- **Sperre:** Når en tur er vurdert *vanskelig*, senkes nivåtaket midlertidig til turnivået for den turen, hvis nivåtaket var høyere. Sperren oppheves når en tur, uansett hvilken, er vurdert *moderat*.
- **Hard grense:** Turer over nivåtaket blir aldri foreslått (FR-5).
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
  - Siden fungerer ned til 360 px bredde uten horisontal rulling.
  - På turforslaget er kart, turnivå, estimert tid og bekledningstips synlige uten mye rulling.
  - Knapper er minst 44 × 44 px.
- **NFR-4 Universell utforming:** WCAG 2.1 AA er målet. Det betyr:
  - kontrast på minst 4,5:1
  - alle handlinger i kjerneflyten kan gjøres med tastatur
  - feilmeldinger er koblet til feltet og leses opp av skjermleser
  - kartet holder ikke på tastaturfokus
  - informasjon gis aldri bare med farge.

  Kravet verifiseres med et automatisk verktøy og en manuell sjekkliste (SM-4).
- **NFR-5 Personvern:**
  - Systemet samler inn så lite data som mulig. Det lagrer bare e-post, passord som hash, historikk og vurderinger.
  - Systemet sporer ikke posisjon.
  - Ingen personopplysninger sendes til KI-leverandøren. KI får bare søket og turene som kan foreslås.
- **NFR-6 Sporbarhet:** Kode, tester, stories, commits og PR-er viser til FR- og NFR-ID-ene i denne PRD-en.
- **NFR-7 Kreditering:** Appen viser kreditering slik lisensene krever, minst «© Kartverket», «© OpenStreetMap contributors» med lenke og «Data fra MET Norge» (MET anbefaler «Data from MET Norway»).
- **NFR-8 Sikkerhet:**
  - En bruker kan bare se og endre sin egen historikk og konto.
  - All input valideres på serveren.
  - Fritekstønsket behandles som data og ikke som instruksjoner (FR-11). KI-svar valideres alltid (FR-13).

## 6. Plattform, skjermer og tone

Nettside på norsk. V1 har ingen mobilapp.

**Skjermer:**
- søk
- turforslag
- logg inn / registrer
- registrer gjennomført tur
- historikk
- konto, med sletting

**Tilstander som skal designes:**
- laster
- feil i skjemaet (FR-4)
- ingen treff og ingen treff innenfor nivåtaket (FR-8)
- alle forslag er vist (FR-7)
- uten værvarsel (FR-10)
- reserveløsning (FR-13)
- gjest som møter krav om konto (FR-14)

Wireframes lages i UX-fasen, og PRD-en skal vise til dem når de finnes.

**Tone:** Innbydende og trygg. Tjenesten overselger ikke KI eller «læring», og forklarer alltid hvorfor en tur blir foreslått.

## 7. Scope

### 7.1 Med i v1

Alle funksjonene i §4 (FR-1 til FR-21) og alle NFR-ene i §5.

**Prioritering:**
- **P1, må leveres:** FR-1 til FR-8, FR-12 og FR-13 med begrunnelse fra fast mal og reserveløsning, FR-14 til FR-19, FR-21 og alle NFR-er.
- **P2, kuttes først hvis tiden ikke strekker til**, i denne rekkefølgen:
  1. FR-11 (KI-tolking av fritekstønske)
  2. FR-9 og FR-10 (bekledningstips)
  3. FR-20 (turtypepreferanse)
- Hvert kutt føres i §9 og i endringsloggen, med årsak.

### 7.2 Utenfor v1

- Turer utenfor Oslo-området
- Ruter laget av KI, eller turer utenfor turdatabasen
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
- Velge startpunkt ved å klikke i kartet
- Glemt passord. Dette krever en e-posttjeneste, som ville blitt den femte eksterne avhengigheten.

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
- **SM-4:** En manuell test av mobilvisning og universell utforming (UU) etter en dokumentert sjekkliste består (NFR-3, NFR-4). Personaliseringen demonstreres med testbrukeren (FR-21).

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

Alle antakelser og standardverdier ble bekreftet og godkjent av produkteier 2026-11-06. De står i kravene de gjelder. De åpne punktene om MET-vilkår og Kartverkets API-er ble lukket samme dag (§4.4 og addendum). Det er ingen åpne spørsmål igjen.

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
