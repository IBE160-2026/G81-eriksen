# Avstemming: PRD mot sensorveiledning IBE160 – Del 1

Kilde: `extract-sensorveiledning.md` (uttrekk av `C:\IBE160\Sensorveiledning IBE160 - Del 1 applikasjon og prosess.pdf`). Sidetall viser til PDF-en.
Avstemt mot: `prd.md` (oppdatert 2026-11-06), `addendum.md`, `.memlog.md`. Briefens innhold er sjekket via `extract-brief.md` der det gjelder endringer fra briefen.
Dato: 2026-11-06. Perspektiv: sensor, som leser brief/PRD først og deretter sjekker at dokumentene henger sammen med koden (s. 2).

Alvorlighet: **høy** = sensor kan trekke direkte på et kriterium. **middels** = svekker en A–B-vurdering. **lav** = pynt eller konsistens.

---

## 1. Det PRD-en allerede dekker godt

| Hva veiledningen belønner | Hvor i PRD-en | Vurdering |
|---|---|---|
| Sporbare ID-er (s. 2, 3) | §0, UJ/FR/NFR/SM, NFR-6 | Godt. Alle krav har ID, og SM-1/SM-2 viser til FR-er |
| Endringer fra plan med begrunnelse (s. 3) | §9 | Godt, men ufullstendig (se G2) |
| Kjørbarhet uten nøkler (s. 2, 5) | NFR-1, FR-13, SM-3, addendum (input-form) | Svært godt. Kjerneflyt uten KI-nøkkel er et eksplisitt krav |
| Stabilitet og feilhåndtering (s. 3–4) | NFR-2, FR-4, FR-8, FR-10, FR-13 | Godt. Tomtilstand, manglende vær og KI-feil er dekket |
| Ansvarlig KI-validering (s. 2) | FR-11, FR-13, §1, addendum | Godt. KI rangerer bare blant filtrerte treff |
| Ikke-trivielle regler (s. 3) | FR-2, FR-3, FR-5, FR-19, FR-20 | Godt. Gir uttelling for omfang og kompleksitet |
| Datalagring, roller, integrasjoner (s. 3) | FR-1, FR-14–17, FR-9 (MET), FR-11 (KI) | Godt |
| Testdata/testbruker (s. 5) | FR-21 | Godt |
| UU og responsivt (s. 4) | NFR-3, NFR-4, FR-4 (etiketter), FR-6 (kartbeskrivelse) | Godt grunnlag, men se G5 |
| Levende dokument (s. 2, 6) | Endringslogg, `.memlog.md` | Godt grunnlag, men se G9 |
| Manuell test dokumentert (s. 4) | SM-1 | Godt |

---

## 2. Gap på PRD-nivå

### G1. Ingen prioritering eller kuttrekkefølge for en enmannsgruppe — **høy**
- **Veiledningen:** Funksjonalitet måles mot proposal og eget ambisjonsnivå. Omfang klart mindre enn lovet *uten begrunnelse* gir D–F på kriterium 2 (s. 3). Kjerneflyter skal fungere fra start til slutt (s. 3). Avvik fra planen skal forklares (s. 2). Uttrekket pkt. 3: «Ikke lov mer enn dere rekker».
- **PRD:** §7.1 lister alle 21 FR-er som likeverdige v1-krav. Faglæreren har advart om at omfanget er stort for én person (extract-brief §8). Addendum nevner det bare for det utsatte tidsestimatet.
- **Risiko:** Hvis tiden ikke strekker til, vil leveransen avvike fra PRD-en uten planlagt begrunnelse. Dette er varseltegnet «planleggingsdokumenter som beskriver en annen app enn den som er levert» (s. 6).
- **Forslag:** Legg til prioritet per FR i §7.1, for eksempel:
  - **P1 (kjerneflyt, må fungere):** FR-1–FR-8, FR-13 (reserveløsning), FR-14, FR-16, FR-18, FR-19, FR-21.
  - **P2:** FR-9, FR-10, FR-11, FR-12 (KI-tekst), FR-15, FR-17, FR-20.
  - Angi kuttrekkefølge (for eksempel FR-11 → FR-20 → FR-17) og regelen om at hvert kutt føres i §9 og endringsloggen med begrunnelse.

### G2. Avvik fra briefen som ikke står i §9 — **høy** (lett å rette)
- **Veiledningen:** Utelatt eller endret funksjonalitet fra proposal skal beskrives og begrunnes (s. 3). Sensor leser briefen først (s. 2).
- **PRD:** §9 mangler disse endringene:
  1. Briefen SC 8: *likte ikke* → «turen foreslås ikke igjen». I PRD-en blir turer med fornøydhet 1–2 bare rangert sist og aldri utelukket (FR-5). Beslutningen står i `.memlog.md`, men ikke i §9.
  2. Turtypen *skogstur* i briefen er blitt *marka* (§3).
  3. Briefen la bare språk utover norsk/engelsk utenfor scope. PRD-en har bare norsk (§6, §7.2).
  4. Briefens kjerneflyt («beskrive → forslag → lagre → vurdere») er endret til SM-1-flyten med gjestesøk og registrering.
- **Forslag:** Legg til en rad med begrunnelse for hvert punkt i §9-tabellen.

### G3. Akseptansekriterier som ikke kan testes direkte — **middels**
- **Veiledningen:** Testene skal dekke sentral logikk. Systematisk QA belønnes (s. 4). Uttrekket pkt. 8: kriteriene skal kunne bli tester eller manuelle testplaner.
- **PRD, konkrete steder:**
  - FR-9: Reglene for klesråd mangler terskler (temperatur, nedbør, vind). Det finnes bare ett eksempel.
  - FR-13: «etter tidsgrensen» har ingen verdi (for eksempel 5 s).
  - FR-10: «omtrent 9–10 dager» bør heller være «når MET ikke har data for datoen».
  - FR-12: «viser til konkrete verdier» – det står ikke hvilke felt begrunnelsen *minst* må nevne.
  - FR-14: Det mangler krav til passord (minstelengde), oppførsel ved e-post som allerede finnes, og feilmelding ved feil innlogging.
  - FR-7: «samme økt» er ikke definert i §3. Gjelder det fanen, nettlesersesjonen eller søket?
  - NFR-2, NFR-3 og NFR-4 mangler verifiseringsmetode. Eksempler: «ingen horisontal rulling ved 360 px bredde», «alle kjerneflyt-handlinger kan gjøres med tastatur», «kontrast kontrollert med verktøy X».
- **Forslag:** Tallfest de punktene som står over. Legg en kolonne eller linje «Verifiseres ved: automatisk test / manuell testplan» til NFR-ene.

### G4. UX-spor: ingen skjermliste, skisser eller tilstandsoversikt — **middels**
- **Veiledningen:** Skisser, wireframes eller UX-beskrivelser i planleggingsdokumentene (s. 4). Forståelige tilbakemeldinger, feilmeldinger og tomtilstander (s. 4). Uttrekket pkt. 6.
- **PRD:** Har gode brukerreiser (UJ-1, UJ-2), men ingen oversikt over skjermbilder, ingen navigasjonsstruktur og ingen lastetilstand mens MET- og KI-kall pågår. Faglæreren pekte på tre implisitte skjermer: søk, forslag med kart og turhistorikk.
- **Forslag:** Legg til et kort UX-avsnitt (eller en lenke til et eget UX-dokument), med:
  - skjermene: søk, turforslag, logg inn/registrer, registrer gjennomført tur, historikk og konto
  - tilstandene: laster, feil i skjema, ingen treff (FR-8), uten vær (FR-10), KI-reserve (FR-13), gjest som møter kontokrav (FR-14)
  - en henvisning til wireframes når de finnes.

### G5. UU: turnivå formidles med farge — **middels**
- **Veiledningen:** Grunnleggende UU: kontrast, tastatur, alt-tekst og etiketter (s. 4). Tilgjengelighet er en del av A–B på kriterium 4 (s. 4–5).
- **PRD:** Turnivå er DNT-farger (§3, FR-6). Det står ikke at nivået også skal vises som tekst. Informasjon bare i farge bryter WCAG 2.1 (1.4.1). Det står heller ikke at feilmeldinger i FR-4 skal knyttes programmatisk til feltet, eller at kartet ikke skal fange tastaturfokus.
- **Forslag:** I FR-6: «Turnivå vises med farge **og** tekst (for eksempel “Blå – middels”)». I NFR-4: feilmeldinger er knyttet til feltene og leses opp av skjermleser, og kartet stopper ikke tastaturnavigasjonen.

### G6. Sikkerhet utover «ingen hemmeligheter» — **middels**
- **Veiledningen:** Feilhåndtering og validering av input, og bevissthet om sikkerhet (s. 4).
- **PRD:** NFR-1 (hemmeligheter) og FR-14 (hash) er dekket. Dette mangler:
  - maks lengde på fritekstønsket og håndtering av prompt-injeksjon (friteksten går til KI)
  - tilgangskontroll: en bruker ser og endrer bare sin egen historikk (FR-16, FR-17)
  - validering av brukt tid i FR-16 (ikke negativ, rimelig maksimum)
  - beskyttelse mot dobbel innsending, som henger sammen med «gjentatte handlinger» i NFR-2.
- **Forslag:** Legg til **NFR-7 Sikkerhet** med disse punktene, eller legg dem inn i FR-11, FR-14 og FR-16.

### G7. Ansvarlig KI: begrunnelsestekst og data som sendes til KI — **middels**
- **Veiledningen:** Kritisk styring og validering av KI (s. 2). Uttrekket pkt. 7: beskriv hvordan KI-forslag valideres.
- **PRD:** FR-13 validerer *valget* av tur, men ikke *innholdet* i begrunnelsen. KI kan påstå at turen går «ved vann» eller oppgi feil tid eller lengde. NFR-5 sier heller ikke hva som sendes til KI-leverandøren. Det bør være bare søket og kandidatturene, ikke e-post eller historikk.
- **Forslag:**
  - I FR-12/FR-13: Tall (tid, distanse, nivå) i begrunnelsen settes inn av systemet og skrives ikke av KI. Begrunnelser lengre enn N tegn forkastes.
  - I NFR-5: Ingen personopplysninger sendes til KI.
  - Eventuelt: forkastede KI-svar logges. Det gir QA-eksempler til kriterium 3.

### G8. Automatiske tester dekker ikke reserveløsning og validering — **middels**
- **Veiledningen:** Testene skal være relevante og dekke sentral logikk (s. 4). Dokumenterte manuelle testplaner der automatiske tester ikke passer (s. 4).
- **PRD:** SM-2 dekker FR-2, FR-3, FR-5 og FR-18–20. Det mangler tester for:
  - FR-13 (KI-svar utenfor treff, tomt svar, timeout, manglende nøkkel). Dette er den viktigste sikkerhetsmekanismen.
  - FR-4 (skjemavalidering), FR-7 (ingen gjentakelse) og FR-8 (topptur-reserve og ingen treff).
  - En manuell testplan for NFR-3 og NFR-4.
- **Forslag:** Utvid SM-2 med FR-4, FR-7, FR-8 og FR-13, med KI mocket. Legg til SM-4: manuell UU- og mobiltest etter en dokumentert sjekkliste.

### G9. Levende dokument: versjoner og selvmotsigelse om åpne punkter — **lav**
- **Veiledningen:** BMAD-dokumentene skal være brukt og oppdatert og ikke «generert én gang» (s. 2). Varseltegn: dokumenter som tydelig er laget i etterkant (s. 6).
- **PRD:**
  - Endringsloggen har datoer, men ingen versjonsnummer. Status er `draft`.
  - §10 sier at det ikke finnes åpne spørsmål, men addendumet sier at formelen for estimert tid må kontrolleres mot offisiell kilde før implementering.
  - Det mangler en regel for hvordan PRD-en oppdateres når implementeringen avviker.
- **Forslag:**
  - Legg til en versjonskolonne (v0.1, v0.2, v1.0 ved godkjenning).
  - Før formelkontrollen opp som et åpent punkt i §10, med eier og frist (før FR-3-storyen).
  - Legg en setning i §0: «Avvik under implementering føres i §9 og endringsloggen med henvisning til story/PR».

### G10. Sporbarhet tilbake til briefen — **lav**
- **Veiledningen:** Funksjoner skal kunne spores tilbake til krav (s. 2). Sensor sammenligner leveransen med det som er lovet (s. 2–3).
- **PRD:**
  - Det finnes ingen kobling fra briefens SC 1–10 til FR/SM. Bare §4.8 viser til SC 5–8.
  - «Gjelder UJ-…» mangler på flere FR-er (FR-2, FR-3, FR-5–FR-10, FR-13–FR-15, FR-18–FR-21).
  - NFR-6 nevner kode, tester og stories, men ikke commits og PR-er.
- **Forslag:**
  - Legg til en liten tabell «Brief SC → PRD-ID» (for eksempel SC 2 → FR-13, SC 9 → FR-21, SC 10 → SM-1).
  - Legg til UJ-henvisninger konsekvent.
  - Utvid NFR-6 til commits og PR-er.

### G11. Kildehenvisning og lisens i grensesnittet — **lav**
- **Veiledningen:** Bevissthet om sikkerhet og forsvarlig bruk av konfigurasjon og avhengigheter (s. 4–5). Dette er ikke et eksplisitt krav.
- **PRD:** FR-1 registrerer kilde og lisens per tur. Det står ikke at kartet og værdataene skal vise kildehenvisning, slik lisensene krever: OSM (ODbL), Kartverket og MET (CC BY 4.0 / NLOD).
- **Forslag:** I FR-6 og FR-9: «Kilde vises (© OpenStreetMap, Kartverket, MET Norway)».

### G12. Kjørbarhet: kart og turdatabase uten oppsett — **lav**
- **Veiledningen:** Sensor kjører appen bare ved hjelp av README på 15–20 minutter (s. 2, 5).
- **PRD:** NFR-1 er god, men sier ikke at kart og vær er nøkkelfrie, eller at den ferdige turdatabasen og testbrukeren følger med repoet (seed) og ikke krever import fra eksterne kilder.
- **Forslag:** Legg til i NFR-1: «Kart, vær og turdatabase fungerer uten nøkler. Turdatabasen og testbrukeren lastes automatisk ved oppstart eller med én kommando».

---

## 3. Påminnelser for senere arbeid (ikke PRD-gap) — **lav**

Disse hører hjemme i README, arkitektur eller repo, men veiledningen belønner dem direkte:

- **README (s. 5–6):** hva appen er, med skjermbilde; forutsetninger med versjoner; kommandoer som kan kopieres; `.env.example`; innlogging for testbrukeren (FR-21); hvordan testene kjøres; mappestruktur; **lenke til PRD-en, addendumet, arkitekturen og prompts/KI-økter**. Test README-en i et rent miljø på under 20 minutter.
- **Arkitektur (s. 2, 5):** begrunn valg av stack, database, KI-leverandør, kartbibliotek (Leaflet + OSM?) og testmodus for KI. Mappestrukturen må samsvare med dokumentet. MET krever en egen `User-Agent`-header. Valider sveitsisk regel før FR-3.
- **Repo (s. 6–7):** `.gitignore` for `node_modules`, `venv`, build og `.env`. Ingen nøkler i historikken. Ingen løse filer i rotmappen.
- **Prosess (s. 2–3, 7):** commits, PR-er og issues med FR-ID-er; små commits over tid; lagrede prompts koblet til konkrete endringer; eksempler på avviste eller rettede KI-forslag. `.memlog.md` og sesjonsloggene er et godt spor, så lenk til dem.
- **QA (s. 4):** PR-beskrivelser eller en QA-logg med konkrete feil i KI-generert kode og hvordan de ble rettet. Resultatet av SM-1 dokumentert i repoet.
- **Epics/stories:** hver story viser til FR-ID og har akseptansekriterier hentet fra PRD-en.
