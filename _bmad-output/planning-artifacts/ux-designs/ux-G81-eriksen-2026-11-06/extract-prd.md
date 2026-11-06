---
title: "PRD-uttrekk for UX: Your Next Adventure"
kilde: prds/prd-G81-eriksen-2026-10-29/prd.md (v1.0, status final) + addendum.md
created: 2026-11-06
---

# PRD-uttrekk for UX

Alle punkter er hentet fra PRD-en. Ingenting er lagt til. «Add.» betyr addendum.md.

## 1. Produkt og målgruppe

- **Produktet:** En nettside på norsk for nybegynnere som vil gå tur i Oslo-området. Brukeren oppgir varighet og dato, og kan i tillegg velge startpunkt og turtype og skrive et fritekstønske. Tjenesten svarer med **ett** turforslag: rute på kart, estimert tid, bekledningstips og en begrunnelse (§1).
- **Målgruppe:** Nybegynnere på fottur i Oslo-området (§1, §2).
  - Jobber brukeren vil få gjort (§2.1): finne en tur som passer tid og form, uten å lete lenge. Føle seg trygg på at turen ikke blir for krevende. Bestemme seg raskt, ofte spontant eller *på mobilen på vei ut*. Få bedre tilpassede forslag over tid og finne igjen turer hen likte.
- **Persona:** PRD-en har bare én navngitt person: **Ola** (UJ-1 og UJ-2, §2.3). Han kjenner ikke marka godt og bruker mobilen. PRD-en har ingen formelle personas utover ham.
- **Ikke målgruppe i v1:** erfarne turgåere, turister, tilflyttere og alle som vil gå utenfor Oslo-området (§2.2).

## 2. Funksjonelle krav som trenger en flate

| ID | Hva flaten skal gjøre | § |
|---|---|---|
| FR-4 | Søkeskjema med varighet (påkrevd, 1–8 t i halvtimessteg), dato (påkrevd, standard i dag, fra i dag til 30 dager frem), startpunkt (valgfritt, fra liste), turtype (valgfri) og fritekstønske (valgfritt, maks 200 tegn). Alle felt har synlige etiketter. Feilmelding vises ved feltet. Gjest og bruker ser samme skjema | §4.2 |
| FR-6 | Visning av turforslaget. Innholdet står i avsnitt 6 under | §4.3 |
| FR-7 | Knappen «Nytt forslag». Når alle treff er vist: en melding, forslag til endringer og et valg om å starte fra første forslag igjen | §4.3 |
| FR-8 | Meldinger når det er ingen treff, når bare turer over nivåtaket passer, og når en utsiktstur vises i stedet for topptur | §4.3 |
| FR-9 | Bekledningstips i turforslaget. Flere tips kan vises samtidig | §4.4 |
| FR-10 | Turforslag uten bekledningstips, med en melding om hvorfor | §4.4 |
| FR-12 | Begrunnelse, maks 300 tegn. Nevner varigheten, og turtype og fritekstønske hvis de er oppgitt. Nevner personaliseringsregelen hvis den har påvirket valget | §4.5 |
| FR-13 | Melding når fritekstønsket ble ignorert | §4.5 |
| FR-14 | Registrering med e-post og passord (minst 8 tegn), innlogging og utlogging. En gjest som prøver en kontofunksjon, blir bedt om å logge inn eller registrere seg, og turforslaget beholdes | §4.6 |
| FR-15 | Slette konto med bekreftelse. All historikk slettes permanent | §4.6 |
| FR-16 | Registrere gjennomført tur, fra turforslaget eller fra historikken. Alle fire felt er påkrevd: dato (standard i dag, ikke frem i tid), brukt tid (10 min–24 t), opplevd vanskelighet og fornøydhet (1–5) | §4.7 |
| FR-17 | Historikk med tur, dato og vurdering. Brukt tid vises **sammen med** estimert tid. En tur kan åpnes som turforslag igjen | §4.7 |
| FR-18–20 | Nivåtak, sperre og turtypepreferanse. Disse har ingen egen skjerm, men synes i begrunnelsen (FR-12) og i meldingen om nivåtak (FR-8) | §4.8 |
| FR-21 | Testbruker med oppdiktet historikk. Innloggingsdataene står i README | §4.9 |

## 3. §6 Plattform, skjermer og tone (gjengitt nøyaktig)

- Nettside på norsk. V1 har ingen mobilapp.
- **Skjermer:** søk · turforslag · logg inn / registrer · registrer gjennomført tur · historikk · konto, med sletting.
- **Tilstander som skal designes:** laster · feil i skjemaet (FR-4) · ingen treff og ingen treff innenfor nivåtaket (FR-8) · alle forslag er vist (FR-7) · uten værvarsel (FR-10) · reserveløsning (FR-13) · gjest som møter krav om konto (FR-14).
- «Wireframes lages i UX-fasen, og PRD-en skal vise til dem når de finnes.»
- **Tone:** «Innbydende og trygg. Tjenesten overselger ikke KI eller «læring», og forklarer alltid hvorfor en tur blir foreslått.»

## 4. Brukerreiser og scenarier

- **UJ-1. Ola tar en spontan tur uten konto (§2.3).** Han åpner siden på mobilen uten å logge inn og fyller inn 3 timer, i dag og «utsikt». Startpunkt hopper han over. Han får kart med rute, «tur-retur, 7,2 km totalt, ca. 2 t 40 min (pauser ikke inkludert)», «Grønn – lett», bekledningstips, en begrunnelse og en lenke til ut.no. Han trykker «Nytt forslag», og det neste forslaget passer.
  - *Kanttilfelle:* Ba han om topptur, og ingen passet innenfor tre timer, får han en utsiktstur og beskjed om at toppturer krever mer tid.
- **UJ-2. Ola kommer tilbake (§2.3).** Han lager konto og registrerer brukt tid, vanskelighet (*lett / moderat / vanskelig*) og fornøydhet (1–5) etter hver tur. Nye søk prioriterer turer han ikke har gått. Etter tre grønne turer vurdert *lett* får han blå turer, og begrunnelsen sier hvorfor. I historikken finner han favoritturen igjen og går den på nytt.
- **Kjerneflyt (§3):** søke som gjest → få turforslag → registrere seg → registrere turen som gjennomført med vurdering → søke på nytt.
- **Overgang fra gjest til konto:** Turforslaget beholdes gjennom registrering og innlogging (FR-14, §4.6).

## 5. Tilstander og kanttilfeller

| Tilstand | Hva PRD-en sier | § |
|---|---|---|
| Laster | Står på listen over tilstander. Innholdet er ikke spesifisert | §6 |
| Feil i skjemaet | Feilmelding ved feltet, og søket sendes ikke. Ugyldig betyr manglende varighet eller dato, dato utenfor tillatt periode eller fritekst over 200 tegn. Validering skjer også på serveren | FR-4 |
| Ingen topptur passer varigheten | Viser en utsiktstur og meldingen «Toppturer krever mer tid enn du har oppgitt». Passer heller ingen utsiktstur, gjelder «ingen treff» | FR-8 |
| Bare turer over nivåtaket passer | Melding, ingen tur. For gjester og brukere uten historikk: «Som ny bruker får du grønne turer. Lag konto og vurder turene dine for å låse opp lengre turer.» | FR-8 |
| Ingen treff | Konkrete forslag: lengre varighet, et annet startpunkt eller en annen turtype | FR-8 |
| Alle forslag er vist | «Du har sett alle turene som passer søket», med endringsforslag og et valg om å starte fra første forslag igjen. Ingen tur vises to ganger i samme økt | FR-7 |
| Vær utilgjengelig | MET mangler varsel for datoen (i praksis mer enn ca. 9–10 dager frem) eller svarer ikke. Turforslaget vises uten bekledningstips og med en melding om hvorfor | FR-10; Add. MET |
| KI feiler eller er utilgjengelig | Svaret forkastes ved tur utenfor treffene, tomt eller ugyldig svar, begrunnelse over 300 tegn eller tidsavbrudd etter 5 sekunder. Da ignoreres fritekstønsket, og begrunnelsen lages fra mal | FR-13 |
| Testmodus uten KI-nøkkel | Samme reserveløsning. Hele kjerneflyten skal fungere uten nøkkel. Kart, vær og turdatabase fungerer uten nøkler | FR-13, §4.5, NFR-1, SM-3 |
| Fritekstønsket ble ignorert | «Vi kunne ikke ta hensyn til ønsket ditt denne gangen». Malteksten viser aldri til fritekstønsket. Eksempel på mal: «Turen tar ca. 2 t og har utsikt, som du ba om» | FR-13; Add. Input-form |
| Gjest møter krav om konto | Blir bedt om å logge inn eller registrere seg. Turforslaget beholdes | FR-14 |
| E-posten er allerede registrert | «Kunne ikke registrere – prøv å logge inn» | FR-14 |
| Feil innlogging | «Feil e-post eller passord», uten å si hvilket av dem som er feil | FR-14 |
| Sletting av konto | Krever bekreftelse | FR-15 |
| Tur uten ut.no-lenke | Lenken vises bare hvis turen har en. Forslaget fungerer uten | FR-6; Add. ut.no |
| Robusthet | Tåler feil input, gjentatte handlinger og dobbel innsending. Hver tilstand viser enten et turforslag eller en forklaring med neste steg | NFR-2 |

## 6. Domeneterminologi som UI-et skal bruke ordrett

- **Turnivå (§3, FR-2, FR-6):** farge **og** tekst. Grønn = *lett*, blå = *moderat*, rød = *moderat*, svart = *vanskelig*. Rekkefølgen er grønn < blå < rød < svart. Format: «Blå – moderat».
  - Fast forklaringstekst: «Beregnet av tjenesten etter Merkehåndbokas mal ut fra lengde og høydemeter. Terreng og føre er ikke vurdert.»
- **Graderingsgrenser (FR-2):** Grønn: under 5 km og under 300 høydemeter. Blå: under 10 km og under 600. Rød: under 20 km og under 1000. Svart: over grensen for rød. Turen får den strengeste fargen, og verdier akkurat på en grense graderes opp.
- **Estimert tid (FR-3):** 15 min/km + 15 min per 100 høydemeter + 15 min per 200 m nedstigning, × 1,15, avrundet til nærmeste 5 minutter.
  - Format: «ca. 2 t 20 min». Vises **alltid** med «pauser ikke inkludert».
  - KI beregner aldri tid eller nivå.
- **Form (§3, FR-6):** «tur-retur» eller «rundtur», tydelig merket. Total lengde vises for hele turen, for eksempel «7,2 km totalt».
- **Turtyper (§3):** *marka*, *utsikt* og *topptur*. «Skogstur» brukes ikke (§9).
- **Vurdering (§3, FR-16):** opplevd vanskelighet *lett / moderat / vanskelig*, fornøydhet 1–5 og brukt tid.
- **Feltnavn (FR-4, FR-16):** Varighet, Dato, Startpunkt, Turtype, Fritekstønske. Brukt tid, opplevd vanskelighet, fornøydhet.
- **Faste begreper (§3):** Tur, Turforslag, Begrunnelse, Bekledningstips, Gjennomført tur, Historikk, Nivåtak, Sperre, Gjest, Bruker. Handlingen heter «registrere gjennomført tur», ikke «lagre» (§9).
- **Knappetekst:** «Nytt forslag» (UJ-1, §9).
- **Bekledningstips, ordrett (FR-9).** Gjelder dagtid kl. 10–16 for startpunktet:
  - nedbør ≥ 0,5 mm: «Fare for nedbør – husk regntøy»
  - laveste temperatur under 5 °C: «Kaldt – ta med lue, votter og et varmt mellomlag»
  - laveste temperatur 5–15 °C: «Ta med et ekstra lag»
  - høyeste temperatur over 20 °C: «Varmt – ta med drikke og solbeskyttelse»
  - vind ≥ 8 m/s: «Mye vind – ta med vindtett jakke»
  - alltid: «Gode sko og litt mat og drikke».
- **Eksempel på begrunnelse med personalisering (FR-12):** «Du får en blå tur fordi de tre siste grønne turene var lette for deg.»

## 7. Ikke-funksjonelle krav som påvirker UX

- **Mobil (NFR-3):**
  - fungerer ned til 360 px bredde uten horisontal rulling
  - kart, turnivå, estimert tid og bekledningstips er synlige uten mye rulling
  - knapper er minst 44 × 44 px.
- **Universell utforming (NFR-4):** Målet er WCAG 2.1 AA:
  - kontrast på minst 4,5:1
  - hele kjerneflyten kan gjøres med tastatur
  - feilmeldinger er koblet til feltet og leses opp av skjermleser
  - kartet holder ikke på tastaturfokus
  - informasjon gis aldri bare med farge.

  Kartet har en tekstbeskrivelse for skjermlesere (FR-6). Kravet verifiseres med et automatisk verktøy og en manuell sjekkliste (SM-4).
- **Språk:** bare norsk (§6, §7.2, §9).
- **Plattform:** nettside, ingen mobilapp (§6).
- **Personvern (NFR-5):** Systemet lagrer bare e-post, passord som hash, historikk og vurderinger. Det sporer ikke posisjon. Ingen personopplysninger sendes til KI.
- **Kreditering i UI-et (NFR-7, FR-6):** minst «© Kartverket», «© OpenStreetMap contributors» med lenke og «Data fra MET Norge» (MET anbefaler «Data from MET Norway», gjerne med lenke, Add. MET). Krediteringen vises på turforslaget.
- **Sikkerhet (NFR-8):** En bruker ser bare sin egen historikk og konto.
- **Kjørbarhet (NFR-1, FR-21):** Sensor kjører appen uten nøkler og bruker testbrukeren til å se personaliseringen.
- **Suksessmål som angår UX:**
  - SM-1: minst 75 % av testerne klarer kjerneflyten uten hjelp og vurderer første forslag som relevant
  - SM-C1: ingen testere vurderer første forslag som *vanskelig* (§8).

## 8. Utenfor scope

**Utenfor v1 (§7.2):**
- turer utenfor Oslo-området
- ruter laget av KI eller turer utenfor turdatabasen
- henting av turdata mens appen kjører
- andre målgrupper enn nybegynnere
- værvarsling som egen tjeneste
- terrengstatus og føre
- mobilapp
- sosiale funksjoner
- offline-navigering
- booking og transport
- flere språk enn norsk.

**Senere fase (§7.2):**
- personlig justering av estimert tid (faktisk tid logges likevel i v1, Add.)
- velge startpunkt ved å klikke i kartet
- glemt passord.

**Også utelatt:** lagring av planlagte turer (§9) og «praktiske tips» utover bekledningstips (§9).

**P2, kuttes først hvis tiden ikke strekker til (§7.1):**
1. FR-11 (KI-tolking av fritekst)
2. FR-9 og FR-10 (bekledningstips)
3. FR-20 (turtypepreferanse).

UX bør derfor tåle at disse delene mangler.

## 9. Åpne spørsmål, notater og antakelser

- **Åpne spørsmål:** PRD-en sier «Det er ingen åpne spørsmål igjen». Alle antakelser er godkjent av produkteier 2026-11-06 (§10).
- **[NOTE FOR UX]:** PRD-en har ingen slike merknader.
- **Det eneste UX-oppdraget:** Wireframes lages i UX-fasen, og PRD-en skal vise til dem (§6).
- **Ikke spesifisert i PRD-en, og må avklares eller designes:**
  - hvordan lastetilstanden ser ut
  - ordlyden i meldingen om manglende værvarsel (FR-10)
  - ordlyden i bekreftelsen ved sletting av konto (FR-15)
  - meldingen om nivåtak for brukere *med* historikk (FR-8 gir bare teksten for gjester og nye brukere)
  - navigasjon og meny mellom skjermene
  - hvordan og hvor krediteringen plasseres.
- **Antakelser som påvirker UI-et:**
  - Graderingen tar ikke hensyn til terreng, eksponering eller føre, og det må stå i UI-et (FR-2, FR-6).
  - Formlene for tid bommer med omtrent ±15 % (§9; Add.).
