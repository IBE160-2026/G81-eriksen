# Product Brief: Your Next Adventure

## Executive Summary

Your Next Adventure er en nettside som hjelper nybegynnere med å planlegge sin neste fottur i naturen i Oslo-området. I stedet for å lete gjennom generelle kart eller store turdatabaser, skriver brukeren rett og slett inn hvor de vil dra, hvor mye tid de har, og hva slags opplevelse de er ute etter — en topptur, en rolig skogstur, eller noe midt imellom. Tjenesten svarer med konkrete forslag: rute på kart, tidsbruk og praktiske tips.

Det som gjør Your Next Adventure annerledes er at forslagene tilpasses brukeren. Med en brukerkonto lagres tidligere turer, sammen med brukerens egen vurdering av hva de likte og hvordan de opplevde vanskelighetsgraden — ikke bare hva et objektivt turkart sier om stigning og lengde. I første versjon skjer tilpasningen etter enkle, faste regler, slik at forslagene blir tilpasset den enkelte, ikke bare stedet. På sikt er målet en tjeneste som lærer av brukeren og blir smartere jo mer den brukes (se Vision).

## The Problem

Å planlegge en tur i naturen tar ofte mer tid enn selve turen burde kreve. Man vet gjerne omtrent hvor man vil dra og hvor mye tid man har, men å finne en rute som faktisk passer — riktig lengde, riktig type opplevelse, riktig vanskelighetsgrad for akkurat denne dagen — betyr å lete gjennom flere kilder: turkart, blogger, AllTrails, ut.no, Google Maps.

I dag løser folk dette ved å bruke god tid på research, spørre venner, eller rett og slett velge en tur de allerede kjenner fordi det er tryggere enn å lete. Konsekvensen er at man enten bruker mye tid man ikke har, eller ender opp med turer som ikke matcher det man faktisk hadde lyst til den dagen (for lett, for hardt, feil type natur). Ingen av de eksisterende verktøyene tar hensyn til hvem brukeren er og hva de har likt tidligere — de er statiske databaser, ikke noe som tilpasser seg deg.

## The Solution

Your Next Adventure lar brukeren beskrive turen de har lyst på — lokasjon, tilgjengelig tid, og ønsket type opplevelse (f.eks. topptur, skogstur, tur med utsikt) — og få konkrete, ferdige forslag tilbake: rute vist på kart, estimert tidsbruk, og relevante tips for turen, inkludert bekledningstips basert på værvarselet for turdagen.

Turforslagene hentes fra en kuratert turdatabase med 20–30 kontrollerte turer i Oslomarka, egnet for nybegynnere. Hver tur har faste opplysninger som navn, startpunkt, lengde, høydemeter, turtype og vanskelighetsgrad, og rutelinjene er hentet fra OpenStreetMap. KI tolker brukerens ønske i vanlig språk, og velger og forklarer blant turene i databasen, men lager ikke nye ruter. Tidsestimatet beregnes ut fra lengde og høydemeter, slik at det ikke er KI som gjetter hvor lang tid turen tar.

Med innlogging kan brukeren lagre tidligere turer. Systemet bruker denne historikken, sammen med brukerens egen vurdering av hvor lett eller hardt en tur faktisk var, til å justere forslagene etter enkle, faste regler, for eksempel hvilken vanskelighetsgrad som foreslås. Neste gang brukeren spør om et forslag, er anbefalingen tilpasset dem — ikke en generisk liste over turer i området.

## What Makes This Different

Turdatabaser og kartverktøy som finnes i dag (ut.no, AllTrails, Google Maps) er gode på å vise hva som finnes et sted, men de er statiske: samme resultat uansett hvem som spør. Your Next Adventure sitt fortrinn er personalisering basert på faktisk brukerhistorikk og selvrapportert opplevelse — koblet med at brukeren kan uttrykke ønsket i vanlig språk ("en rolig skogstur på et par timer") i stedet for å filtrere i lister.

Vi skal være ærlige om hva fortrinnet er: det ligger ikke i en unik teknisk oppfinnelse, men i hvor godt vi kombinerer eksisterende data (kart, stiinformasjon) med brukerens egen historikk og tilbakemelding, og i hvor raskt og treffsikkert vi kan levere det som en sammenhengende opplevelse.

## Who This Serves

Primærbruker: nybegynnere på tur i Oslo-området — folk som har lyst til å komme seg ut i naturen, men som er usikre på hva de takler og hvilke turer som passer for dem. De vet omtrent hva de har lyst til (tid, sted, type opplevelse), men ikke den konkrete ruten, og de mangler erfaring til å vurdere lengde, stigning og vanskelighetsgrad selv. Suksess for dem er å få et forslag de stoler på og faktisk bruker, som ikke er for krevende, og som blir bedre tilpasset dem jo mer de bruker tjenesten.

Første versjon er bygget rundt denne ene brukergruppen. Andre brukergrupper, som erfarne turgåere og turister eller tilflyttere, er beskrevet under Vision.

## Success Criteria

Vanskelighetsgrad følger DNTs fargeskala (grønn, blå, rød, svart). Kriteriene under er formulert slik at de kan testes.

**Kjerneflyt**
1. En bruker kan beskrive ønsket tur (sted i Oslo-området, tid og type tur) og får minst ett forslag med rutelinje på kart, beregnet tidsestimat, bekledningstips og en kort forklaring på hvorfor turen passer.
2. Alle forslag er turer som finnes i turdatabasen. Hvis KI foreslår noe som ikke finnes der, eller ikke svarer, brukes et regelbasert forslag i stedet.
3. Det beregnede tidsestimatet for en foreslått tur er ikke lengre enn tiden brukeren har oppgitt.
4. Brukere kan opprette konto, lagre en gjennomført tur og vurdere den som *for lett*, *passe* eller *for hard*, og som *likte* eller *likte ikke*.

**Personalisering (faste regler)**

5. En ny bruker uten historikk får bare turer med laveste vanskelighetsgrad (grønn) som førstevalg.
6. Når en bruker har vurdert tre turer på samme vanskelighetsgrad som *for lett*, blir neste vanskelighetsgrad (for eksempel blå) foreslått først.
7. Når en bruker vurderer en tur som *for hard*, foreslås ikke turer med høyere vanskelighetsgrad enn den turen før brukeren har vurdert en ny tur som *passe*.
8. En tur brukeren har vurdert som *likte ikke*, blir ikke foreslått igjen. Turtyper brukeren har likt, rangeres høyere når flere turer passer like godt.

**Demo og brukertest**

9. Appen har en testbruker med ferdig turhistorikk, der regel 6–8 synes uten at appen må brukes over tid.
10. Manuell brukertest med 3–5 nybegynnere: minst 4 av 5 klarer kjerneflyten (beskrive tur → få forslag → lagre → vurdere) uten hjelp, og vurderer det første forslaget som relevant. Resultatet dokumenteres i repoet.

## Scope

**Med i første versjon:**
- Geografisk avgrenset til Oslo-området, inkludert Oslomarka
- Input for lokasjon, tilgjengelig tid og ønsket turtype/opplevelse
- Kuratert turdatabase med 20–30 kontrollerte turer i Oslomarka, med rutelinjer fra OpenStreetMap
- Turforslag fra turdatabasen med kart, tidsestimat og tips, der KI tolker brukerens ønske og velger og forklarer blant turene
- Værbaserte bekledningstips til turforslaget, hentet fra Yr/MET sitt værvarsel-API for turens lokasjon og tidspunkt
- Brukerkonto med innlogging
- Lagring av tidligere turer og enkel tilbakemelding (opplevd vanskelighetsgrad: for lett/passe/for hard, og likte/likte ikke)
- Regelbasert personalisering av forslag basert på lagret historikk (se Success Criteria 5–8)
- Testbruker med ferdig turhistorikk
- Brukeren kan slette kontoen sin og all lagret historikk

**Eksplisitt utenfor for første versjon:**
- Turer utenfor Oslo-området
- KI-genererte ruter eller turer som ikke finnes i turdatabasen
- Henting av turdata fra eksterne tjenester mens appen kjører
- Tilpasning til andre brukergrupper enn nybegynnere (se Vision)
- Værvarsel som egen varslingstjeneste (push-varsler, beredskapsmeldinger) — vær brukes kun som input til turforslaget, ikke som et selvstendig varslingsprodukt
- Presis terrengstatus/føremelding (snø, is, gjørme) — for upresist til å love i v1; vurderes senere
- Mobilapp (kun nettside i første omgang)
- Sosiale funksjoner (deling, følge andre brukere, kommentarer)
- Offline GPS-navigering underveis på tur
- Booking/logistikk (overnatting, transport, utleie av utstyr)
- Støtte for flere språk enn norsk/engelsk

## Kvalitetskrav for første versjon

**Feilhåndtering og tomtilstander**
- Hvis ingen tur passer brukerens ønske, får brukeren beskjed om det og forslag til hva som kan justeres (for eksempel mer tid eller en annen turtype). Siden står aldri tom.
- Hvis brukeren oppgir et sted utenfor Oslo-området, får brukeren beskjed om at første versjon bare dekker Oslo-området.
- Hvis værdata ikke er tilgjengelig, vises turforslaget likevel, uten bekledningstips og med en melding om at værvarselet mangler.
- Hvis KI ikke svarer eller gir et ugyldig svar, brukes et regelbasert forslag (se Success Criteria 2).

**Mobil**
- Nettsiden er responsiv og fungerer på mobil, siden brukerne ofte sjekker turen på vei ut.

**Universell utforming**
- Nettsiden følger grunnleggende krav til universell utforming, med WCAG 2.1 nivå AA som rettesnor: lesbar kontrast, tastaturnavigasjon, skjemaetiketter og alternativ tekst for kart og bilder.

**Personvern**
- Turhistorikk og vurderinger er personopplysninger. Appen lagrer bare det som trengs for personaliseringen: e-post, passord (lagret som hash), lagrede turer og vurderinger. Brukerens posisjon spores ikke, og brukeren kan slette kontoen sin med all historikk. Testbrukeren inneholder bare oppdiktede data.

## Vision

Om to-tre år er Your Next Adventure det første stedet folk går for å planlegge en tur i naturen — ikke fordi den har flest stier i databasen, men fordi den kjenner brukeren godt nok til å foreslå akkurat den turen de trenger denne dagen. Personaliseringen har gått fra enkle, faste regler til en tjeneste som lærer av hver enkelt bruker og blir smartere jo mer den brukes. Forslagene er så treffsikre at brukerne stoler på dem, samtidig som tjenesten alltid viser hvorfor en tur er foreslått. Tjenesten har også utvidet fra Oslo-området til flere regioner. Den har også utvidet fra nybegynnere til flere brukergrupper: erfarne turgåere som vil ha raske, treffsikre forslag uten å bruke tid på research, og turister eller tilflyttere som ikke kjenner området og trenger konkrete forslag tilpasset tiden de har til rådighet. Etter hvert dekker tjenesten også flere typer friluftsaktiviteter enn fottur — ski, sykkel, padling — alltid med samme kjerneidé: forstå brukeren, ikke bare stedet.
