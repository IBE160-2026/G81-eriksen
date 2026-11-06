# PRD-kvalitetsgjennomgang – Your Next Adventure

Vurdert mot `prd-validation-checklist.md`. Kalibrert for et fagprosjekt i IBE160 (én person, kompakt PRD på 4–6 sider). Kilder: `prd.md` (oppdatert 2026-11-06) og `addendum.md`.

## Samlet vurdering

PRD-en er konkret, ærlig om omfanget og har en tydelig tese: én forklarbar anbefaling for nybegynnere, med KI som et avgrenset tillegg. Beslutningene er synlige i §9 og i addendumet, og avgrensningene i §7.2 er gode. Risikoen ligger i kjernelogikken. Rangeringen i FR-5 bestemmer ikke hvilken tur som vises først, det er uklart om nivåreglene i FR-19 utelukker turer eller bare rangerer dem, og formelen for estimert tid (FR-3) er ikke endelig avklart. Disse tre punktene påvirker både implementeringen og testene i SM-2, og de bør rettes før stories skrives.

## Beslutningsklarhet – sterk

Beslutningene står som beslutninger. §9 lister hver endring fra briefen med begrunnelse, og addendumet viser tre vurderte alternativer for input-formen, med arbeid, risiko og hva som ble valgt bort («Produktet mister det som skiller det fra andre»). Utsettelsen av personlig tidsestimat er begrunnet med omfanget, og det står at faktisk tid likevel logges. Motmålet SM-C1 viser at forfatteren har tenkt på hva som ikke skal optimaliseres. Det er sjeldent i en PRD av denne størrelsen.

Svakheten er at §10 sier «Det er ingen åpne spørsmål som blokkerer videre arbeid», mens addendumet («Formel for estimert tid») sier at formelen «må kontrolleres mot den offisielle sveitsiske kilden» før implementering. Det er et reelt åpent spørsmål som er gjemt i addendumet.

### Funn
- **medium** Åpent spørsmål skjult i addendum (§10, addendum «Formel for estimert tid») – §10 erklærer at det ikke er noen åpne spørsmål, men summen eller maks + halvparten av minste er fortsatt uavklart. *Fiks:* Før spørsmålet opp i §10 med en eier og en frist, eller avgjør det og fjern forbeholdet i addendumet.

## Innhold fremfor kulisser – sterk

Lite pynt. Visjonen (§1) er spesifikk for produktet: én tur, Oslo-området, nybegynnere og forklarbare regler, og den kan ikke flyttes til en annen PRD uten endringer. Det er én protagonist (Ola) i to brukerreiser, og begge driver konkrete krav (gjest uten konto → FR-4 og FR-14, «Nytt forslag» → FR-7, kanttilfellet for topptur → FR-8). Jobbene i §2.1 er korte og kobler til konkrete valg, som mobil og spontan bruk. NFR-1 har en reell terskel («under 20 minutter, uten ekte nøkler»). Noen NFR-er er likevel adjektiver.

### Funn
- **medium** NFR-2, NFR-3 og NFR-4 mangler grenser (§5) – «fungerer på mobilskjerm», «forståelige feilmeldinger» og WCAG som «rettesnor» kan ikke testes som de står. *Fiks:* Angi en minste skjermbredde (for eksempel 360 px uten horisontal rulling), si at WCAG 2.1 AA gjelder for bestemte suksesskriterier (kontrast 4.5:1, alle skjemaelementer kan nås med tastatur), og knytt NFR-2 til konkrete feiltilfeller (MET nede, KI-tidsavbrudd, ugyldig input), slik at hver av dem gir en bestemt melding.

## Strategisk sammenheng – adekvat

Tesen er tydelig: Planlegging tar for lang tid for nybegynnere, og et enkelt forslag med regelbasert, forklarbar tilpasning løser det bedre enn verktøy som «viser det samme til alle». Prioriteringen følger tesen. Konto er valgfritt for å senke terskelen, KI er avgrenset slik at kjernen virker uten nøkkel, og scope er et MVP som løser et problem. SM-1 måler både om kjerneflyten fungerer og om første forslag oppleves relevant, og det validerer tesen og ikke bare aktivitet.

Svakheten er at koblingen mellom suksessmålene og personaliseringen, som er det som skiller produktet fra andre (§1, tredje avsnitt), er svakere enn den ser ut.

### Funn
- **medium** SM-1 hevder å teste FR-19, men flyten kan ikke utløse regelen (§8 SM-1) – Kjerneflyten har én vurdering før nytt søk, mens nivåheving krever tre vurderinger med *lett*. FR-15 (slette konto) er også med i «FR-14 til FR-19» uten å være del av flyten. *Fiks:* Endre til «FR-4 til FR-8, FR-14, FR-16 og FR-18», og la personaliseringen verifiseres av SM-2 og testbrukeren (FR-21). Eventuelt kan et eget steg i brukertesten bruke testbrukeren.
- **medium** Motmålet SM-C1 kan ikke måles (§8 SM-C1) – «Andelen turforslag som blir vurdert *vanskelig*, skal holdes lav» har ingen terskel, ingen datakilde og ingen periode, og med 3–5 testere blir det ingen meningsfull andel. *Fiks:* Gjør det til en regelsjekk som kan testes («ingen bruker får foreslått en tur over nivåtaket før vilkåret i FR-19 er oppfylt»), eller sett en terskel som måles på testbrukeren eller i brukertesten.

## Klarhet om når et krav er ferdig – tynn

De fleste FR-ene har testbare konsekvenser. FR-2 har eksakte terskler og regel for grenseverdier, FR-4 sier når søket avvises, FR-10 gir en konkret reserveoppførsel, FR-16 sier at alle felt er påkrevd og FR-19 har tellereglene. Problemet er at de tre kravene som hele forslagsmotoren hviler på (FR-3, FR-5 og FR-19), har hull. En utvikler vil måtte gjette, og SM-2 kan ikke skrives som entydige tester.

### Funn
- **high** FR-5 bestemmer ikke hvilken tur som vises først (§4.3 FR-5) – For en gjest uten fritekst og uten turtype er alle grønne turer som passer tiden, like etter rangeringsreglene. Ingen regel sier hva som skjer da. Det finnes heller ingen regel om hvor godt turen fyller varigheten, så en tur på 40 min kan vises når brukeren oppgir tre timer. UJ-1 forutsetter derimot at forslaget (2 t 40 min av 3 t) fyller tiden. *Fiks:* Legg til et siste rangeringskriterium, for eksempel «nærmest varigheten først, deretter alfabetisk/ID», og si om rekkefølgen er deterministisk eller tilfeldig.
- **high** Uklart om nivåreglene utelukker eller bare rangerer turer (FR-5, FR-18, FR-19) – FR-5 sier at turer som overholder nivåreglene «kommer først» og at ingenting utelukkes helt. FR-19 sier at systemet «foreslår ingen turer over den turens nivå» etter en *vanskelig*-vurdering, og det leses som en hard sperre. Det er også uklart om sperren senker nivåtaket eller bare legger et midlertidig tak oppå det. *Fiks:* Skriv eksplisitt: «Nivåtak og sperre påvirker bare rangeringen. Turer over taket kan vises etter at alle turer innenfor er vist.» Alternativt: «Turer over taket filtreres bort.» Definer også effektivt tak = min(nivåtak, sperrenivå).
- **high** Formelen for estimert tid er ikke fastsatt (FR-3, addendum) – Summering og «maks + halvparten av minste» gir ulike tider, og estimert tid er filteret i FR-5. Derfor bestemmer formelen hvilke turer som i det hele tatt kan foreslås, og hva testene i SM-2 skal forvente. *Fiks:* Velg én variant, skriv den i FR-3 (ikke bare i addendumet) og legg ved ett regneeksempel med forventet svar.
- **medium** Lengde for rundtur er ikke definert (FR-1, FR-2, FR-3) – FR-1 sier at «lengden lagres én vei», men for en rundtur finnes det ingen «vei tilbake». FR-3 dobler bare for tur-retur. Det blir uklart om en rundtur på 8 km graderes som 8 km eller 4 km. *Fiks:* Skriv at for en rundtur lagres hele lengden, og at den brukes uendret i FR-2 og FR-3.
- **medium** Varighet har ingen form eller gyldighetsregel (FR-4) – «Hvis varighet mangler eller er ugyldig» forutsetter en definisjon som mangler: timer eller minutter, fritt felt eller faste valg, minimum og maksimum. *Fiks:* Angi formatet (for eksempel faste valg fra 1 til 8 timer i halvtimessteg) og hva som regnes som ugyldig.
- **medium** Fritekst rangerer i FR-11, men avgjør bare likt treff i FR-5 – FR-11 sier at KI «rangerer» blant de filtrerte turene, mens FR-5 gir fritekstønsket lavest prioritet, bare ved likt treff etter turtypepreferanse. *Fiks:* La FR-11 si at KI bare skiller mellom turer som står likt etter de andre kriteriene i FR-5.
- **medium** Bekledningsreglene er ikke spesifisert (FR-9) – «enkle, faste regler» med ett eksempel. Endringsloggen sier at antakelsen er bekreftet, men reglene står ikke i PRD-en eller i addendumet, så FR-9 kan ikke testes. *Fiks:* Legg inn en kort tabell med terskler for temperatur, nedbør og vind og tilhørende råd, i FR-9 eller i addendumet.
- **medium** Tidsgrensen for KI mangler (FR-13) – «kommer etter tidsgrensen» har ingen verdi, og PRD-en har ellers ingen krav til svartid. *Fiks:* Angi en grense (for eksempel 5 sekunder) og et mål for hvor lang tid det tar å vise et forslag uten KI.
- **medium** Hva vises når FR-7 går tom? (FR-7, FR-8) – FR-7 viser til FR-8 når det ikke er flere treff, men FR-8 beskriver bare «ingen treff i det hele tatt». Det er uklart om brukeren får meldingen, starter forfra eller får den siste turen igjen. FR-8 sier heller ikke hva som skjer hvis heller ingen utsiktstur passer når topptur mangler. *Fiks:* Legg til ett punkt for hver av de to situasjonene.
- **low** Dato for gjennomført tur (FR-16, FR-17) – FR-17 viser «dato», men FR-16 registrerer ingen dato. *Fiks:* Si at det er registreringsdatoen, eller legg dato til som felt.
- **low** Passordkrav og duplikat e-post (FR-14) – Det står ingen minstelengde og ingen oppførsel ved e-post som allerede er registrert. *Fiks:* Én setning for hvert av punktene.

## Ærlig omfang – sterk

§7.2 lister elleve ting som er utenfor v1, og «Senere fase» gir begrunnelser (glemt passord ville vært «den femte eksterne avhengigheten»). Avvikene fra briefen er åpent dokumentert i §9 i stedet for å være gjort stille. Tettheten av åpne punkter er lav og passer et fagprosjekt. Ett forhold svekker sporbarheten: §10 sier at alle antakelser ble bekreftet, men lister ikke hvilke. Bare endringsloggen nevner FR-9, FR-19 og FR-20.

### Funn
- **low** Antakelsene er ikke indeksert (§10) – Leseren kan ikke se hva som ble antatt og bekreftet uten å lese endringsloggen. *Fiks:* List de bekreftede antakelsene i §10 med dato, én linje hver.
- **low** «Et fåtall toppturer» er vagt (FR-1) – Det står ikke hvor mange, selv om FR-8 og UJ-1 forutsetter at toppturer finnes. *Fiks:* Angi et minimum (for eksempel minst tre toppturer og minst fem utsiktsturer), slik at reserven i FR-8 alltid har noe å vise.

## Nytte for senere arbeid – adekvat

Begrepslisten i §3 er god og brukes stort sett konsekvent. ID-ene er sammenhengende (UJ-1–2, FR-1–21, NFR-1–6, SM-1–3, SM-C1), hver FR sier hvilken UJ den gjelder, og NFR-6 krever sporbarhet til stories og tester. Kryssreferansene går via ID-er og ikke via «se over». Noen begreper er likevel ikke definert eller brukes i to betydninger, og det vil gi uklare stories.

### Funn
- **medium** «Bruker» brukes både om innloggede brukere og generelt (§3, FR-4, FR-5, FR-8) – §3 definerer *Bruker* som innlogget, men FR-4 («får brukeren en feilmelding»), FR-5 («Turer brukeren ikke har gått») og FR-8 gjelder også gjester. *Fiks:* Bruk «gjest eller bruker» eller innfør et samlebegrep (for eksempel «besøkende») der begge menes.
- **low** Begreper som mangler i begrepslisten (§3) – *varighet*, *økt* (FR-7), *rundtur*/*tur-retur* og *sperre* (FR-19, FR-21) er ikke definert. *Fiks:* Legg dem til i §3.

## Passende form – sterk

Formen passer produktet: et forbrukerprodukt med reell UX, men et lite prosjekt for én person. To brukerreiser med én protagonist er nok, og de bærer kravene. FR-21 (testbruker) og §9 tar hensyn til sensor som en faktisk interessent uten å lage en egen persona. Lengden passer en kompakt PRD, og teknisk detalj er flyttet til addendumet. Ingen funn.

## Mekaniske merknader

- **Synonymer:** «Bekledningstips» (§3, FR-6, FR-9) og «klesråd» (§1, UJ-1, §4.4, §3-definisjonen) brukes om hverandre. «Kuratert» (tittelen på FR-1, addendum «Lenke til ut.no») og «kontrollert» (§3) brukes også om hverandre. Velg ett ord for hvert.
- **Referanser i SM-1:** «FR-14 til FR-19» tar med FR-15 og FR-17, som ikke er del av kjerneflyten (se funn under Strategisk sammenheng).
- **Kryssreferanser:** `research-gradering.md`, `addendum.md` og `.memlog.md` finnes i arbeidsmappen. Kildeangivelsen i addendumet (`research/technical-turdata-oslomarka-2026-10-29`, «D34a F10») er ikke kontrollert her.
- **Brief-koblinger:** §4.8 viser til «SC 5–8» i briefen. Det fungerer for den som har briefen, men PRD-en bør kunne leses alene, og FR-19 gjengir allerede reglene, så referansen kan stå som kilde.
- **Endringslogg:** Den har to rader med samme dato (2026-11-06). Det er greit, men den siste raden er i praksis antakelsesindeksen og bør speiles i §10.
