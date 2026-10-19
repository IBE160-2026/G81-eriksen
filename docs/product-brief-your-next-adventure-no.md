# Product Brief: Your Next Adventure

## Executive Summary

Your Next Adventure er en nettside som hjelper folk med å planlegge sin neste fottur i naturen. I stedet for å lete gjennom generelle kart eller store turdatabaser, skriver brukeren rett og slett inn hvor de vil dra, hvor mye tid de har, og hva slags opplevelse de er ute etter — en krevende topptur, en rolig skogstur, eller noe midt imellom. Tjenesten svarer med konkrete forslag: rute på kart, tidsbruk og praktiske tips.

Det som gjør Your Next Adventure annerledes er at den blir smartere jo mer den brukes. Med en brukerkonto lagres tidligere turer, og systemet lærer hva brukeren faktisk likte og hvordan de opplevde vanskelighetsgraden — ikke bare hva et objektivt turkart sier om stigning og lengde. Over tid gir dette forslag som er tilpasset den enkelte, ikke bare stedet.

## The Problem

Å planlegge en tur i naturen tar ofte mer tid enn selve turen burde kreve. Man vet gjerne omtrent hvor man vil dra og hvor mye tid man har, men å finne en rute som faktisk passer — riktig lengde, riktig type opplevelse, riktig vanskelighetsgrad for akkurat denne dagen — betyr å lete gjennom flere kilder: turkart, blogger, AllTrails, ut.no, Google Maps.

I dag løser folk dette ved å bruke god tid på research, spørre venner, eller rett og slett velge en tur de allerede kjenner fordi det er tryggere enn å lete. Konsekvensen er at man enten bruker mye tid man ikke har, eller ender opp med turer som ikke matcher det man faktisk hadde lyst til den dagen (for lett, for hardt, feil type natur). Ingen av de eksisterende verktøyene tar hensyn til hvem brukeren er og hva de har likt tidligere — de er statiske databaser, ikke noe som lærer av deg.

## The Solution

Your Next Adventure lar brukeren beskrive turen de har lyst på — lokasjon, tilgjengelig tid, og ønsket type opplevelse (f.eks. topptur, skogstur, tur med utsikt) — og få konkrete, ferdige forslag tilbake: rute vist på kart, estimert tidsbruk, og relevante tips for turen, inkludert bekledningstips basert på værvarselet for turdagen.

Med innlogging kan brukeren lagre tidligere turer. Systemet bruker denne historikken, sammen med brukerens egen vurdering av hvor lett eller hardt en tur faktisk var, til å forstå brukerens preferanser og treffsikkerhet på vanskelighetsgrad. Neste gang brukeren spør om et forslag, er anbefalingen tilpasset dem — ikke en generisk liste over turer i området.

## What Makes This Different

Turdatabaser og kartverktøy som finnes i dag (ut.no, AllTrails, Google Maps) er gode på å vise hva som finnes et sted, men de er statiske: samme resultat uansett hvem som spør. Your Next Adventure sitt fortrinn er personalisering basert på faktisk brukerhistorikk og selvrapportert opplevelse — koblet med at brukeren kan uttrykke ønsket i vanlig språk ("en rolig skogstur på et par timer") i stedet for å filtrere i lister.

Vi skal være ærlige om hva fortrinnet er: det ligger ikke i en unik teknisk oppfinnelse, men i hvor godt vi kombinerer eksisterende data (kart, stiinformasjon) med brukerens egen historikk og tilbakemelding, og i hvor raskt og treffsikkert vi kan levere det som en sammenhengende opplevelse.

## Who This Serves

Primærbruker: folk som liker å gå turer i naturen — fra nybegynnere som er usikre på hva de takler, til erfarne turgåere som vil ha raske, treffsikre forslag uten å bruke tid på research. Felles for dem er at de vet omtrent hva de har lyst til (tid, sted, type opplevelse), men ikke nødvendigvis den konkrete ruten. Suksess for dem er å få et forslag de stoler på og faktisk bruker, og som blir bedre tilpasset dem jo mer de bruker tjenesten.

Sekundærbruker: turister eller tilflyttere som ikke kjenner området godt, og som trenger konkrete forslag tilpasset hvor mye tid de har til rådighet.

## Success Criteria

- En bruker kan oppgi lokasjon, tid og ønsket type tur, og få et konkret forslag med kart, tidsestimat og tips.
- Brukere kan opprette konto og lagre gjennomførte turer.
- Forslag blir merkbart mer treffsikre for en bruker med turhistorikk enn for en ny bruker (personalisering fungerer).
- Testbrukere vurderer forslagene som relevante og vanskelighetsgraden som riktig oppfattet, målt gjennom enkel tilbakemelding etter tur.
- Prosjektet leverer en fungerende demo som dekker kjerneflyten (input → forslag → lagring → forbedret forslag).

## Scope

**Med i første versjon:**
- Input for lokasjon, tilgjengelig tid og ønsket turtype/opplevelse
- AI-genererte turforslag med kart, tidsestimat og tips
- Værbaserte bekledningstips til turforslaget, hentet fra Yr/MET sitt værvarsel-API for turens lokasjon og tidspunkt
- Brukerkonto med innlogging
- Lagring av tidligere turer og enkel tilbakemelding (f.eks. opplevd vanskelighetsgrad, likte/likte ikke)
- Grunnleggende personalisering av forslag basert på lagret historikk

**Eksplisitt utenfor for første versjon:**
- Værvarsel som egen varslingstjeneste (push-varsler, beredskapsmeldinger) — vær brukes kun som input til turforslaget, ikke som et selvstendig varslingsprodukt
- Presis terrengstatus/føremelding (snø, is, gjørme) — for upresist til å love i v1; vurderes senere
- Mobilapp (kun nettside i første omgang)
- Sosiale funksjoner (deling, følge andre brukere, kommentarer)
- Offline GPS-navigering underveis på tur
- Booking/logistikk (overnatting, transport, utleie av utstyr)
- Støtte for flere språk enn norsk/engelsk

## Vision

Om to-tre år er Your Next Adventure det første stedet folk går for å planlegge en tur i naturen — ikke fordi den har flest stier i databasen, men fordi den kjenner brukeren godt nok til å foreslå akkurat den turen de trenger denne dagen. Personaliseringen har blitt så treffsikker at brukere stoler blindt på forslagene, og tjenesten har utvidet til flere regioner og etter hvert flere typer friluftsaktiviteter enn fottur — ski, sykkel, padling — alltid med samme kjerneidé: forstå brukeren, ikke bare stedet.
