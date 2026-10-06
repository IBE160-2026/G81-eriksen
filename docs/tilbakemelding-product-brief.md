# Tilbakemelding på product brief

| | |
|---|---|
| **Gruppe** | G81 – G81-eriksen |
| **Product brief** | `docs/product-brief-your-next-adventure-en.md` (commit `65465e9`) |
| **Tilbakemelding fra** | Faglærer i IBE160 (utarbeidet med KI-støtte) |
| **Dato** | 2026-10-06 |

## Samlet vurdering

- **Godt utgangspunkt med justeringer.** Gruppen kan gå videre og innarbeide punktene under.

**Det som er bra:**

1. Problemet er godt beskrevet og lett å kjenne seg igjen i: man vet omtrent hvor man vil og hvor lang tid man har, men må lete i ut.no, AllTrails, blogger og Google Maps for å finne en tur som passer. Eksempelet «a relaxed forest walk for a couple of hours» viser godt hva det betyr å beskrive turen med vanlig språk.
2. Scope har en tydelig og gjennomtenkt «out of scope»-liste (ingen mobilapp, ingen sosiale funksjoner, ingen offline-navigasjon, ingen føremeldinger), og værdata er avgrenset til klesråd for turdagen fra Yr/MET. Det viser at dere har tenkt på hva som ikke skal med.

**De viktigste endringene:**

1. Bestem hvor turforslagene kommer fra. Briefen sier «AI-generated trip suggestions with a map», men ikke hvilke turdata appen bygger på. Lar dere en språkmodell finne på ruter og tidsestimater, kan den foreslå stier som ikke finnes – det er både vanskelig å kontrollere og potensielt farlig i fjellet. Bruk en fast, kjent turdatabase (for eksempel en egen, kuratert liste med 20–50 turer i ett område, eller åpne kartdata), og la KI velge og forklare blant disse.
2. Gjør suksesskriteriene testbare. «Suggestions become noticeably more accurate» og «test users rate the suggestions as relevant» kan ikke måles i emnet. Beskriv personaliseringen som en regel som kan testes, for eksempel «en bruker som har vurdert tre lette skogsturer som ‘for lett’, får ikke foreslått en lett skogstur først».
3. Avgrens geografien og brukergruppen for v1. «People who enjoy hiking», fra nybegynnere til erfarne, pluss turister, er bredt. Velg ett område (for eksempel Molde-regionen) og én primærbruker, slik at både turdata og design kan bli gode.

## Vanskelighetsgrad og gjennomførbarhet

### Vurdert vanskelighetsgrad

- **Middels**

**Sammenlignbart med:** 2) AI CV- og søknadsassistent (middels). Som CV-assistenten har appen flere sammenhengende funksjoner (forslag, lagring, tilbakemelding og tilpasning), innlogging og KI-svar med krav til kvalitet. I tillegg kommer kart og en værintegrasjon. Uten en fast turdatabase vil prosjektet bevege seg mot vanskelig.

**Begrunnelse:**

| Faktor | Nivå (lav / middels / høy) | Kommentar |
|---|---|---|
| Domenelogikk – hvor mange og hvor kompliserte regler og beregninger må stemme? | Middels | Tidsestimat, vanskelighetsgrad, matching mot ønsket turtype og regler for personalisering basert på tidligere vurderinger. |
| Datamodell – antall entiteter og relasjoner mellom dem | Middels | Bruker, tur/rute, gjennomført tur, vurdering (vanskelighet, likte/likte ikke) og forslag. |
| Brukere, roller og innlogging | Middels | Én rolle, men innlogging og lagring av historikk per bruker. |
| KI-funksjonalitet i appen, f.eks. kall til språkmodell, prompts i koden og håndtering av usikre svar | Høy | Tolkning av fritekst, forslag og tips, pluss personalisering. Risikoen for oppdiktede ruter må håndteres. |
| Integrasjoner og eksterne tjenester, f.eks. API-er, betaling og e-post | Høy | Kartvisning, turdata, MET/Yr-værvarsel og en språkmodell – fire eksterne avhengigheter. |
| Sanntid, samtidighet eller flere brukere som påvirker hverandre | Lav | Hver bruker har sin egen historikk. |
| Filhåndtering, f.eks. opplasting, PDF-lesing og eksport | Lav | Ingen filhåndtering beskrevet. Eventuelle GPX-filer for ruter er en mulig, men ikke nødvendig del. |
| Sikkerhet og personvern | Middels | Innlogging og turhistorikk (hvor brukeren har vært) er personopplysninger. Det bør nevnes kort i briefen. |

**Hva vanskelighetsgraden betyr for dere:**

- _Middels:_ Et godt balansert valg. Pass på at kjerneflyten blir ferdig og stabil før dere legger til mer: beskriv ønsket tur → få et forslag med kart, tid og klesråd → lagre turen og vurder den → få et bedre tilpasset forslag neste gang.

### Gjennomførbarhet med BMAD og Claude Code

Dere skal planlegge med BMAD (product brief → PRD → arkitektur → epics og stories) og implementere med Claude Code. Vurderingen under tar hensyn til at det må være tid til hele denne flyten, og til testing, retting og README til slutt.

| Spørsmål | Vurdering (OK / risiko / stor risiko) | Kommentar |
|---|---|---|
| **Tid og omfang** – kan v1 realistisk bli ferdig og stabil i løpet av semesteret, med tid til flere iterasjoner? | Risiko | Seks v1-punkter med fire integrasjoner er mye for en gruppe på én person. Realistisk hvis turdatabasen er liten og kuratert, og personaliseringen er regelbasert. |
| **BMAD-flyten** – er briefen konkret nok til at PRD, arkitektur og stories kan lages uten store hull, og blir det overkommelig mange stories? | Risiko | Funksjonene er tydelige, men det største hullet – hvor turdataene kommer fra – må avklares før arkitekturen. |
| **Egnet for Claude Code** – bruker løsningen en vanlig, godt dokumentert teknologistakk som Claude Code håndterer godt, eller krever den nisjeteknologi, spesialmaskinvare eller mye manuell konfigurasjon? | OK | Nettside med innlogging, database, kartbibliotek (for eksempel Leaflet med OpenStreetMap) og MET-API er godt dokumentert. |
| **Kontroll på KI-ens arbeid** – kan gruppen selv avgjøre om koden gjør det riktige? Krever domenet kunnskap gruppen ikke har, f.eks. avanserte beregninger eller fagregler, så er det vanskelig å kvalitetssikre. | Risiko | Med en kjent turdatabase kan dere sjekke at forslagene finnes og passer. Med KI-genererte ruter kan dere ikke kontrollere at de er riktige. |
| **Testbarhet** – finnes det tydelige regler og forventede resultater som tester kan skrives mot? | Risiko | Lagring, innlogging, værhenting og en regelbasert personalisering kan testes. «Noticeably more accurate» kan ikke testes før det er definert som regler. |
| **Kjørbar for sensor** – kan appen kjøres lokalt etter README, uten gruppens nøkler, betalte kontoer eller egen infrastruktur? | Risiko | MET-API er gratis, og OpenStreetMap-kart krever ikke nøkkel. Språkmodellen krever trolig nøkkel – legg inn en testmodus med forhåndslagrede svar eller en enkel regelbasert reserve. |
| **Avhengigheter og kostnader** – krever løsningen betalte API-er, f.eks. språkmodeller, og finnes det en plan for kostnad, testmodus eller mock-data? | Risiko | Ikke nevnt. Velg språkmodell i arkitekturen og planlegg kostnad og testmodus. Unngå kart- eller turtjenester som krever betalt nøkkel. |

**Konklusjon om gjennomførbarhet:**

- **Gjennomførbart med justert omfang.** Se forslagene under.

**Forslag til justering av omfang eller vanskelighetsgrad:**

1. Bygg v1 på en egen, kuratert turdatabase for ett område (navn, startpunkt, rute, lengde, høydemeter, turtype og vanskelighetsgrad). La KI tolke brukerens ønske og velge og forklare blant disse turene, i stedet for å lage nye ruter.
2. Gjør personaliseringen regelbasert i v1 (for eksempel at brukerens egne vurderinger justerer hvilken vanskelighetsgrad som foreslås), og vis brukeren hvorfor et forslag passer. Mer avansert «læring» kan stå i Vision.

## Hvorfor product brief er viktig for mappen

Product brief er utgangspunktet for PRD, arkitektur, stories og til slutt koden. Del 1 av mappen vurderes blant annet på om sensor kan følge en sporbar vei fra plan til ferdig app. Den vurderes også på om appen gjør det dere har beskrevet, om den er testet, om den er godt designet, og om den kan kjøres etter README. Et uklart, for stort eller for lite brief gjør alt dette vanskeligere senere. Det er mye enklere å rette nå enn sent i semesteret.

## 1. Gjennomgang av briefens deler

| Del av brief | Status | Kommentar |
|---|---|---|
| Executive Summary – er det klart hva appen er, og hvilket problem den løser? | OK | Klart hva tjenesten gjør, og hva som skal skille den ut (personalisering basert på historikk). |
| The Problem – er problemet konkret, med reelle situasjoner og brukere? | OK | Konkret og troverdig, med navngitte alternativer og konsekvensene av dagens løsninger. |
| The Solution – beskriver løsningen brukeropplevelsen, ikke bare teknologi? | Juster | Godt beskrevet fra brukerens side, men det står ikke hvor rutene og tidsestimatene kommer fra. Legg til én setning om datagrunnlaget. |
| What Makes This Different – er vurderingen ærlig og realistisk? | OK | Ærlig om at fordelen ligger i sammensetningen, ikke i en unik teknologi. |
| Who This Serves – er primærbrukerne tydelige, og vet vi hva de trenger? | Juster | Primærbrukeren spenner fra nybegynnere til erfarne. Velg én konkret primærbruker og ett område for v1. |
| Success Criteria – kan kriteriene faktisk sjekkes eller testes? | Endre | De to første og det siste kriteriet er greie. Kriteriene om «noticeably more accurate» og vurderinger fra testbrukere må gjøres om til konkrete, testbare regler. |
| Scope – er det klart hva som er med i første versjon, og hva som ikke er det? | Endre | Tydelig inndeling, men turdatakilden mangler, og v1 bør avgrenses geografisk. |
| Vision – henger visjonen sammen med resten uten å blåse opp omfanget? | OK | Flere regioner og aktiviteter er tydelig plassert utenfor v1. |

## 2. Utgangspunkt for del 1 av mappen

Punktene følger kriteriene i sensorveiledningen for del 1. Vektene i parentes viser hvor mye hvert kriterium teller i del 1.

| Kriterium i del 1 | Hva briefen bør legge til rette for | Status | Kommentar |
|---|---|---|---|
| **1. Prosess og KI-styring** (30 %) | Brief som er presis nok til at PRD og stories kan bygges direkte på den, slik at krav kan spores fra brief til kode. | Juster | Briefen er ryddig, men er lagt inn som en engelsk oversettelse uten originalen. Legg inn den gjeldende versjonen i repoet, gjerne i BMAD-strukturen, og oppdater den der, så historikken viser utviklingen. |
| **2. Funksjonalitet og omfang** (20 %) | Realistisk omfang for gruppen og semesteret: en tydelig kjerneflyt som kan bli ferdig og stabil, og nok innhold til å vise reell funksjonalitet. | Juster | God kjerneflyt med nok innhold. Avgrens datagrunnlag og område så den kan bli stabil. |
| **3. Kvalitetssikring og testing** (15 %) | Suksesskriterier og funksjoner som er konkrete nok til å bli testtilfeller. | Endre | Personaliseringen må beskrives som testbare regler, og forslagene må kunne sjekkes mot en kjent turdatabase. |
| **4. Design og brukeropplevelse** (10 %) | Tydelige brukere og brukssituasjoner som designet kan bygges rundt, gjerne med de viktigste skjermbildene eller flytene skissert. | Juster | Skjermbildene kan utledes (søk, forslag med kart, min turhistorikk). Tenk på mobilbruk ute på tur, selv om v1 er en nettside. |
| **5. Kodekvalitet og arkitektur** (10 %) | Teknologivalg som er begrunnet og ikke mer komplekse enn appen trenger. | Juster | Teknologi er ikke valgt. Velg gratis og nøkkelfrie tjenester for kart og vær, og hold arkitekturen enkel. |
| **6. README og kjørbarhet** (10 %) | Løsning som andre kan kjøre lokalt uten betalte kontoer, og uten tilgang til gruppens egne tjenester og nøkler. | Juster | Planlegg testmodus for språkmodellen og en testbruker med ferdig turhistorikk, slik at sensor kan se personaliseringen uten å bruke appen i flere uker. |
| **7. Ryddighet i repoet** (5 %) | En plan for hvor hemmeligheter, testdata og dokumentasjon skal ligge. | Juster | Ikke beskrevet. Bruk `.env.example` for nøkler, og legg turdatabasen og testdata i egne, tydelige mapper. |

## 3. Neste steg for gruppen

1. Bestem datagrunnlaget for turer (kuratert liste eller åpne kartdata) og ett geografisk område, og skriv det inn i Solution og Scope.
2. Skriv om suksesskriteriene for personalisering og forslag til konkrete, testbare regler, og lag en testbruker med eksempelhistorikk.
3. Velg språkmodell, kartbibliotek og værkilde i arkitekturen, og beskriv hvordan sensor kan kjøre appen uten deres nøkler.

Oppdater product brief i repoet når dere har gjort endringene, slik at historikken viser hvordan planen utviklet seg. Det er en del av prosessen sensor ser etter.
