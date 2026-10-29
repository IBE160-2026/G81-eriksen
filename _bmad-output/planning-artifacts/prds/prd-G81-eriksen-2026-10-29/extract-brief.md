# Utdrag fra product brief – Your Next Adventure (grunnlag for PRD)

Kilder (forkortelser):
- **NO** = `docs/product-brief-your-next-adventure-no.md` (gjeldende, kanonisk)
- **EN** = `docs/product-brief-your-next-adventure-en.md` (utdatert v1, merket «Utdatert» i fila)
- **TB** = `docs/tilbakemelding-product-brief.md` (faglærer, 2026-10-06, gjelder EN/commit `65465e9`)
- **EP** = `notater/endringsplan-product-brief.md` (lokal endringsplan, 2026-10-19)

## 1. Produkt og visjon

- Nettside som hjelper nybegynnere med å planlegge neste fottur i Oslo-området. Brukeren oppgir sted, tid og ønsket opplevelse og får konkrete forslag: «rute på kart, tidsbruk og praktiske tips» (NO, Executive Summary).
- Kjerneidé: forslag tilpasset brukeren, «ikke bare stedet». I v1 skjer tilpasningen «etter enkle, faste regler» (NO, Executive Summary).
- Visjon (2–3 år): førstevalget for turplanlegging fordi tjenesten «kjenner brukeren godt nok»; personalisering går fra faste regler til læring; tjenesten «alltid viser hvorfor en tur er foreslått»; utvidelse til flere regioner, brukergrupper (erfarne, turister/tilflyttere) og aktiviteter (ski, sykkel, padling). Slagord: «forstå brukeren, ikke bare stedet» (NO, Vision).
- Differensiering: ærlig om at fortrinnet ikke er en teknisk oppfinnelse, men kombinasjonen av eksisterende data, brukerhistorikk og egenrapportert opplevelse, levert som sammenhengende opplevelse, pluss input i vanlig språk (NO, What Makes This Different).

## 2. Problem

- Planlegging tar mer tid enn turen burde kreve; man må lete i turkart, blogger, AllTrails, ut.no og Google Maps for å finne riktig lengde, type og vanskelighetsgrad (NO, The Problem).
- Dagens løsninger: mye research, spørre venner, eller velge en kjent tur. Konsekvens: tidsbruk, eller turer som er «for lett, for hardt, feil type natur» (NO, The Problem).
- Eksisterende verktøy er «statiske databaser», samme resultat uansett hvem som spør (NO, The Problem / What Makes This Different).
- TB vurderer problemet som konkret og troverdig (TB, Samlet vurdering pkt. 1).

## 3. Målgruppe / brukere

- **Primærbruker (eneste i v1):** nybegynnere på tur i Oslo-området; usikre på hva de takler, vet omtrent tid/sted/type, men mangler erfaring til å vurdere lengde, stigning og vanskelighetsgrad (NO, Who This Serves).
- Suksess for brukeren: et forslag de «stoler på og faktisk bruker», som ikke er for krevende og blir bedre tilpasset over tid (NO, Who This Serves).
- Senere brukergrupper (kun Vision): erfarne turgåere og turister/tilflyttere (NO, Who This Serves / Vision).
- **Navngitte personas:** ingen i noen av kildene.
- Testbruker med oppdiktet turhistorikk for demo/sensor (NO, Success Criteria 9; Personvern).
- Avvik EN: primærbruker var «beginners … to experienced hikers», sekundærbruker turister/tilflyttere (EN, Who This Serves). Innsnevret i NO etter TB.

## 4. Kjernefunksjoner (MVP)

- Input: sted i Oslo-området, tilgjengelig tid og ønsket turtype/opplevelse (f.eks. topptur, skogstur, tur med utsikt), uttrykt i vanlig språk (NO, Solution; Scope).
- KI tolker ønsket og **velger og forklarer** blant turer i databasen; lager ikke nye ruter (NO, Solution).
- Kuratert turdatabase med 20–30 kontrollerte nybegynnerturer i Oslomarka (navn, startpunkt, lengde, høydemeter, turtype, vanskelighetsgrad) (NO, Solution; Scope).
- Turforslag med: rutelinje på kart, beregnet tidsestimat, bekledningstips og kort forklaring på hvorfor turen passer; minst ett forslag (NO, SC 1).
- Tidsestimat beregnes fra lengde og høydemeter (ikke av KI), og skal ikke overstige brukerens oppgitte tid (NO, Solution; SC 3).
- Værbaserte bekledningstips fra Yr/MET-API for turens lokasjon og tidspunkt (NO, Solution; Scope).
- Regelbasert reserve: hvis KI foreslår tur utenfor databasen eller ikke svarer, brukes regelbasert forslag (NO, SC 2; Kvalitetskrav).
- Brukerkonto med innlogging (e-post + passord som hash) (NO, Scope; Personvern).
- Lagre gjennomført tur og vurdere den: *for lett / passe / for hard* og *likte / likte ikke* (NO, SC 4).
- Regelbasert personalisering (NO, SC 5–8):
  - Ny bruker uten historikk: kun grønne turer som førstevalg.
  - Tre turer på samme nivå vurdert *for lett* → neste nivå (f.eks. blå) foreslås først.
  - Tur vurdert *for hard* → ikke høyere nivå enn den turen før en ny tur vurderes *passe*.
  - *Likte ikke* → turen foreslås ikke igjen; likte turtyper rangeres høyere ved likt treff.
- Vanskelighetsgrad etter DNTs fargeskala (grønn, blå, rød, svart), satt av gruppen etter faste regler på lengde og høydemeter (NO, Success Criteria; Solution).
- Testbruker med ferdig historikk der regel 6–8 synes (NO, SC 9; Scope).
- Slette konto og all lagret historikk (NO, Scope; Personvern).
- Feilhåndtering/tomtilstander: ingen treff → melding + forslag til justering («Siden står aldri tom»); sted utenfor Oslo → beskjed; værdata mangler → forslag uten klesråd + melding; KI feiler → regelbasert forslag (NO, Kvalitetskrav).
- Responsiv nettside som fungerer på mobil (NO, Kvalitetskrav – Mobil).
- Universell utforming med WCAG 2.1 AA som rettesnor: kontrast, tastatur, skjemaetiketter, alt-tekst for kart og bilder (NO, Kvalitetskrav).

Implisitte skjermbilder (TB, del 2 kriterium 4): søk, forslag med kart, min turhistorikk.

## 5. Utenfor scope / senere faser

Eksplisitt utenfor v1 (NO, Scope):
- Turer utenfor Oslo-området
- KI-genererte ruter / turer utenfor databasen
- Henting av turdata fra eksterne tjenester mens appen kjører
- Andre brukergrupper enn nybegynnere
- Vær som egen varslingstjeneste (push, beredskap)
- Presis terrengstatus/føremelding (snø, is, gjørme) – «vurderes senere»
- Mobilapp (kun nettside)
- Sosiale funksjoner
- Offline GPS-navigering
- Booking/logistikk
- Flere språk enn norsk/engelsk

Senere faser (NO, Vision): lærende personalisering, flere regioner, flere brukergrupper, flere aktiviteter (ski, sykkel, padling).

## 6. Datakilder og tekniske føringer nevnt

- Rutelinjer: Kartverkets Turrutebasen (åpne data), OpenStreetMap som supplement (NO, Solution; Scope).
- Høydemeter: Kartverkets høydedata (NO, Solution).
- Vær: Yr/MET værvarsel-API (NO, Scope).
- Turdata lastes ikke fra eksterne tjenester under kjøring, dvs. databasen bygges på forhånd (NO, Scope).
- Språkmodell: ikke valgt (TB, Neste steg 3; EP, Del A).
- TB/EP-føringer som hører hjemme i arkitektur/README, ikke i brief: gratis, nøkkelfrie tjenester for kart og vær (f.eks. Leaflet + OSM, MET), testmodus for språkmodellen med forhåndslagrede svar eller regelbasert reserve slik at sensor kan kjøre uten nøkler, `.env.example`, egne mapper for turdatabase og testdata (TB, Gjennomførbarhet; del 2 kriterium 5–7; EP, Del A).
- Datamodell antydet av TB: bruker, tur/rute, gjennomført tur, vurdering, forslag (TB, Vanskelighetsgrad-tabell).
- GPX-filer nevnt som mulig, ikke nødvendig (TB, tabell).

## 7. Suksesskriterier / metrikker

- Testbare kriterier SC 1–9 (se pkt. 4) (NO, Success Criteria).
- SC 10: Manuell brukertest med 3–5 nybegynnere; minst 4 av 5 klarer kjerneflyten (beskrive → forslag → lagre → vurdere) uten hjelp og vurderer første forslag som relevant; resultatet dokumenteres i repoet (NO, SC 10).
- Avvik EN: hadde utestbare kriterier («noticeably more accurate», «rate the suggestions as relevant») (EN, Success Criteria) – erstattet i NO.
- Merk: «4 av 5» er uklart når utvalget er 3 eller 4 personer (se Åpne spørsmål).

## 8. Risikoer / begrensninger

- KI kan finne på stier som ikke finnes – «potensielt farlig i fjellet»; håndtert ved kuratert database + validering (TB, Viktigste endringer 1; NO, SC 2).
- Omfang: «Seks v1-punkter med fire integrasjoner er mye for en gruppe på én person» (TB, Gjennomførbarhet). Fire eksterne avhengigheter: kart, turdata, MET, språkmodell (TB, tabell).
- KI-funksjonalitet og integrasjoner vurdert som **høy** kompleksitet; samlet vanskelighetsgrad **middels** (TB).
- Kjørbarhet for sensor: språkmodell krever trolig nøkkel; kostnad og testmodus ikke planlagt (TB, Gjennomførbarhet).
- Terrengstatus for upresist til å love (NO, Scope).
- Personvern: turhistorikk er personopplysninger; dataminimering, ingen posisjonssporing (NO, Personvern).
- Varseltegn i sensorveiledningen: planleggingsdokumenter som beskriver en annen app enn levert, eller som ikke oppdateres (EP, Del B).
- Prioritet: få kjerneflyten ferdig og stabil før mer legges til (TB, «Hva vanskelighetsgraden betyr»).

## 9. Plattform / form-faktor

- Nettside, ikke mobilapp, i v1 (NO, Scope).
- Responsiv; brukerne «sjekker turen på vei ut» (NO, Kvalitetskrav – Mobil; TB, del 2 kriterium 4).
- Språk: briefen er norsk; scope antyder norsk/engelsk, men UI-språk i v1 er ikke presisert (NO, Scope).

## 10. Tilbakemelding: hovedpunkter og gjennomføring i NO-briefen

| Punkt (kilde) | Status i NO |
|---|---|
| Bestem turdatakilde; KI velger blant kjente turer (TB 1; EP A1) | **Gjennomført** – kuratert database 20–30 turer, Kartverket/OSM (NO, Solution; Scope) |
| Testbare suksesskriterier (TB 2; EP A2) | **Gjennomført** – SC 1–9 som regler (NO) |
| Avgrens område og primærbruker (TB 3; EP A3) | **Gjennomført** – Oslo-området/Oslomarka (ikke Molde som foreslått) og nybegynnere |
| Regelbasert personalisering + vis hvorfor (TB; EP A) | **Gjennomført** – SC 5–8, «kort forklaring» (SC 1) |
| Testbruker med historikk (TB; EP A) | **Gjennomført** – SC 9 |
| Personvern (TB; EP A) | **Gjennomført** – egen seksjon |
| Mobilbruk (TB; EP A, B3) | **Gjennomført** |
| Universell utforming (EP B3) | **Gjennomført** – WCAG 2.1 AA |
| Feilhåndtering/tomtilstander (EP B2) | **Gjennomført** |
| Manuell brukertest beholdt (EP B4) | **Gjennomført** – SC 10 |
| B1: fjern «lærer/blir smartere», «trust without question» (EP B1) | **Stort sett gjennomført** – Vision omformulert; men Executive Summary sier fortsatt «På sikt … en tjeneste som lærer av brukeren og blir smartere» (henvist til Vision, så akseptabelt, men verdt å holde PRD-språket regelbasert) |
| Norsk original i repoet, brief oppdatert der (TB del 2 krit. 1; EP C1) | **Gjennomført** – NO er kanonisk, EN merket utdatert |

**Uløste / ikke synlige i NO-briefen:**
- **Testmodus for språkmodellen** uten nøkkel (forhåndslagrede svar) er ikke eksplisitt beskrevet; kun regelbasert reserve ved KI-feil (NO, SC 2). Skal avklares i arkitektur (TB; EP A).
- **Valg av språkmodell, kartbibliotek, kostnadsplan** – ikke gjort (henvist til arkitektur) (TB Neste steg 3; EP A).
- **`.env.example` og mappestruktur** for turdatabase/testdata – ikke beskrevet (henvist til arkitektur/README) (EP A).
- **Endringslogg/beslutningsfil** i briefen om hva som ble endret og hvorfor (EP C3) – ingen endringslogg i NO-briefen.
- **Lagret prompt/KI-økt og små commits** (EP B5, C4) – kan ikke verifiseres fra briefen.
- Avkrysningsbokser i EP er alle uavkryssede, inkludert «Åpne valg» (område, primærbruker, datakilde, regler, språk), selv om NO-briefen faktisk har besvart dem – planen er ikke oppdatert.

## 11. Åpne spørsmål / uklarheter

- **«Tid» i input:** tilgjengelig varighet er tydelig, men værtips krever **turdato/tidspunkt** («turens lokasjon og tidspunkt») – hvordan oppgis dato/starttid? (NO, Scope)
- **Stedsinput:** fritekst, kartvalg eller forhåndsdefinerte steder? Hvordan avgjøres «utenfor Oslo-området»? (NO, Kvalitetskrav)
- **Regler for vanskelighetsgrad:** terskler for lengde/høydemeter → grønn/blå/rød/svart er ikke definert; inneholder en nybegynnerdatabase røde/svarte turer? (NO, Success Criteria; Solution)
- **Formel for tidsestimat** (f.eks. Naismith-lignende) er ikke spesifisert (NO, Solution).
- **Turtype-taksonomi** (topptur, skogstur, utsikt …) – fast liste? Kan en tur ha flere typer? (NO, Solution; SC 8)
- **Antall forslag** per søk og hva «førstevalg»/«foreslått først» betyr i en liste (NO, SC 1, 5, 6).
- **SC 6:** må de tre *for lett*-vurderingene være på rad, eller totalt? Samspill med SC 7 når begge gjelder.
- **SC 7:** gjelder «passe» på hvilken som helst tur, eller på samme nivå?
- **Lagring:** bare gjennomførte turer, eller også planlagte/«lagre til senere»? Kan en tur vurderes flere ganger? (NO, SC 4)
- **Kontofunksjoner:** glemt passord, endre e-post – ikke nevnt.
- **SC 10:** «4 av 5» ved 3–5 testere – bør uttrykkes som andel (f.eks. ≥ 80 %).
- **Språk i UI:** norsk, engelsk eller begge i v1? (NO, Scope)
- **Forklaringen «hvorfor turen passer»:** generert av KI eller regelbasert i reservemodus? (NO, SC 1–2)
- **Startpunkt/kollektiv:** startpunkt finnes, men transport til start er ikke nevnt (booking/logistikk er ute).

## 12. Kvalitative ting som lett faller ut av FR-er

- **Tillit og trygghet:** forslag brukeren «stoler på og faktisk bruker», «ikke er for krevende» – konservativ, trygg tone overfor nybegynnere (NO, Who This Serves; SC 5).
- **Åpenhet:** alltid vise *hvorfor* en tur er foreslått (NO, SC 1; Vision).
- **Vanlig språk, ikke filtre:** «en rolig skogstur på et par timer» – brukeren skal slippe å filtrere i lister (NO, What Makes This Different).
- **Følelsen av å bli kjent:** «tilpasset dem – ikke en generisk liste» (NO, Solution).
- **Spare tid / lav friksjon:** planleggingen skal ikke ta lengre tid enn turen krever (NO, The Problem).
- **Aldri tom side;** hjelpsomme forslag til hva som kan justeres (NO, Kvalitetskrav).
- **Ærlighet om hva tjenesten er** – ikke overselge KI/«læring» (NO, What Makes This Different; EP B1).
- **Ute-på-vei-kontekst:** rask sjekk på mobil før man går (NO, Kvalitetskrav – Mobil).
- **Inspirasjon/eventyr:** navnet «Your Next Adventure» og ordvalg som «topptur», «utsikt» tilsier en innbydende, oppmuntrende tone (NO, generelt).
