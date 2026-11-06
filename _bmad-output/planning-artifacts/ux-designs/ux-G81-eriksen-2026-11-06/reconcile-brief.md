# Avstemming: product brief (norsk) mot spines

Kilde: `docs/product-brief-your-next-adventure-no.md`.
Spines: **E** = EXPERIENCE.md, **D** = DESIGN.md. PRD-en vinner ved konflikt (PRD §0 og §9); punkter PRD-en har erstattet, står under Avvik som «erstattet», ikke som mistet.

## 1. Dekket

- Nybegynnere i Oslo-området som primærbruker → D Brand & Style («rolig turkompis for folk som ikke er turvante ennå»), E UJ-1.
- Rute på kart, beregnet tid, bekledningstips fra værvarsel, kort forklaring (SC 1) → E «Infokolonne».
- Bare turer fra turdatabasen; regelbasert reserve når KI feiler (SC 2, Kvalitetskrav) → E KI-åpenhet, E State «Reserveløsning».
- Tidsestimat ikke lengre enn oppgitt tid (SC 3) → E Mikrotekst/«Faktarute» (estimat fra system).
- DNT-fargeskala grønn/blå/rød/svart → D Turnivå.
- Ny bruker får grønne turer (SC 5) → E Mikrotekst «Som ny bruker får du grønne turer …».
- «Siden står aldri tom»; ingen treff gir forslag til justering → E IA «Felles for alle skjermer», «Tilstandspanel».
- Værdata mangler → forslag uten tips og med melding → E State «Uten værvarsel».
- Slette konto med all historikk → E UJ-3.
- WCAG 2.1 AA, tastatur, skjemaetiketter, alt-tekst for kart og bilder → E Accessibility Floor, «Kartbeskrivelse», «Turillustrasjon».
- Ærlig om fortrinnet, ikke overselge (What Makes This Different) → E Voice «KI skal synes, men ikke overselges».
- «Alltid viser hvorfor en tur er foreslått» (Vision) → E «Begrunnelse», KI-åpenhet.
- Konkurrenter er «statiske … filtrere i lister» → E Inspiration «Forkastet: filtrering i lister».

## 2. Avvik

**Bevisste UX-avvik:**
- «Nettsiden er responsiv og fungerer på mobil, siden brukerne ofte sjekker turen på vei ut» (Kvalitetskrav – Mobil) → mobil utsatt. Memlog (override) Plattform, l. 18.

**Erstattet av PRD (ikke mistet):**
- Fritekst som hovedinput («skriver rett og slett inn hvor de vil dra …», «en rolig skogstur på et par timer») → skjema + valgfritt fritekstønske (PRD §9, FR-4/FR-11). Spines legger fritekst sist i skjemaet, i tråd med PRD.
- «Lokasjon» som input og feilmelding for sted utenfor Oslo → startpunkt fra liste (PRD §9).
- «konkrete forslag» / «minst ett forslag» → ett om gangen med «Nytt forslag» (PRD §9, FR-7).
- *for lett / passe / for hard* og *likte / likte ikke* → *lett / moderat / vanskelig*, fornøydhet 1–5, brukt tid (PRD §9).
- «lagre tidligere turer» / «lagre en gjennomført tur» → «registrere gjennomført tur» (PRD §9).
- «likte ikke blir ikke foreslått igjen» (SC 8) → rangeres sist (PRD §9, FR-5).
- Neste nivå «foreslått først» (SC 6) → nivåtak som hard grense (PRD §9, FR-19).
- «skogstur» → «marka» (PRD §9); E forbyr «skogstur».
- «praktiske tips» → bare bekledningstips (PRD §9).
- Norsk/engelsk → bare norsk (PRD §9).
- Brukerkonto påkrevd → konto valgfri, gjesteflyt (PRD §9).
- Brukertest «4 av 5» → 75 % (PRD §9).

## 3. Mistet

1. **Hjelp til å forstå tallene.** Who This Serves: nybegynnere «mangler erfaring til å vurdere lengde, stigning og vanskelighetsgrad selv» og er «usikre på hva de takler». Spines viser rå tall (km, høydemeter) og en nivåforklaring som sier *hvordan* nivået er regnet ut, ikke *hva det betyr* for brukeren (f.eks. «passer for nybegynnere», «slak stigning»). Høydeprofilen hjelper bare delvis.
2. **Personvern synlig for brukeren.** Kvalitetskrav – Personvern: «Turhistorikk og vurderinger er personopplysninger … Brukerens posisjon spores ikke». Ingen tekst om dette på Registrer eller Konto.
3. **Riktig tur «for akkurat denne dagen».** The Problem: «riktig vanskelighetsgrad for akkurat denne dagen». Været brukes bare til klesråd; spines kobler ikke været til selve forslaget (f.eks. et varsel ved sterk vind på en topptur). Heller ikke i PRD-en, så dette er en bevisst innsnevring som bør nevnes, ikke et krav.
4. **Personaliseringen som noe som vokser.** Who This Serves: forslag som «blir bedre tilpasset dem jo mer de bruker tjenesten»; Vision: «forstå brukeren, ikke bare stedet». Spines viser personalisering bare i begrunnelsen når en regel slo inn. Brukeren ser aldri hvor hen står (nivåtak, fremgang mot neste nivå). Se også reconcile-tilbakemelding.

## 4. Konflikter (ikke loggført)

Ingen nye. Alle konflikter mellom brief og PRD er løst i PRD §9, og spines følger PRD-en. Merk bare at briefens «Oslomarka» (Scope) og PRD-ens «Oslo og Bærum» (FR-1) er forskjellige avgrensninger; spines sier «Oslo-området» (D description), som dekker begge.
