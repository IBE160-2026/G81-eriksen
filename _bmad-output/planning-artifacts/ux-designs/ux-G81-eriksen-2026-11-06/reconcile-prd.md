# Avstemming: PRD mot spines

Kilde: `prds/prd-G81-eriksen-2026-10-29/prd.md` (v1.0) og `addendum.md`.
Spines: **E** = EXPERIENCE.md, **D** = DESIGN.md. Memlog-henvisninger gjelder `.memlog.md` (linjenummer per 2026-11-06 10:41).

## 1. Dekket

- Seks skjermer og alle sju tilstander i §6 → E Information Architecture, E State Patterns.
- Søkeskjema FR-4 (felt, påkrevd, 1–8 t i halvtimessteg, dato i dag til +30 d, 200 tegn, synlige etiketter, feil ved feltet, servervalidering) → E Component Patterns «Skjemafelt», E State «Feil i skjemaet».
- Ett forslag om gangen, «Nytt forslag», aldri samme tur i økten, «Du har sett alle turene som passer søket» med «start fra første» (FR-7) → E Interaction Primitives, E State «Alle forslag er vist».
- FR-6-innholdet: rutelinje, nivå med farge og tekst + fast forklaring, tur-retur/rundtur, total lengde, «pauser ikke inkludert», bekledningstips, begrunnelse, ut.no-lenke, kreditering, tekstbeskrivelse av kart → E «Infokolonne», «Faktarute», «Formmerke», «Kartbeskrivelse»; D Turnivå.
- FR-8 tre varianter (topptur → utsikt, nivåtak, ingen treff med konkrete endringer) → E State Patterns, «Tilstandspanel».
- FR-9/FR-10 tips ordrett, kl. 10–16, uten værvarsel med forklaring, P2-kutt uten tomrom → E «Bekledningstips», E State «Uten værvarsel».
- FR-11–13: KI tolker bare, tall settes av systemet, maks 300 tegn, reserveløsning med «Vi kunne ikke ta hensyn …», testmodus uten nøkkel → E KI-åpenhet, E State «Reserveløsning».
- FR-14 meldinger ordrett, turforslaget beholdes gjennom innlogging → E IA «Ruter som krever konto», E Mikrotekst.
- FR-15 sletting med bekreftelse → E UJ-3, «Slettebekreftelse».
- FR-16/FR-17 registrering (fire påkrevde felt, dato ikke frem i tid, 10 min–24 t), historikk med brukt vs. estimert tid, «Åpne som turforslag», hver registrering egen rad → E «Valggruppe», «Historikktabell».
- FR-12 personaliseringsregel i begrunnelsen («Du får en blå tur fordi …») → E Mikrotekst, UJ-2.
- FR-21 testbruker via vanlig innlogging → E IA.
- NFR-2 (dobbel innsending, alltid neste steg) → E «Primærknapp», «Sender», E State Patterns (innledningen).
- NFR-4 WCAG 2.1 AA (kontrast, tastatur, feil koblet til felt, kart uten fokusfelle, aldri bare farge) → E Accessibility Floor, D Kontrastmål.
- NFR-7 kreditering synlig på kartet → E Kreditering og lisens, D «Kreditering».
- §6 tone «innbydende og trygg», ikke overselge KI → E Voice and Tone, D Brand & Style.
- §3 domeneord ordrett, «registrere gjennomført tur», marka/utsikt/topptur → E Voice and Tone.
- Addendum: ut.no-lenke valgfri, malbegrunnelse-eksempel, MET-kreditering → E Mikrotekst, E State «Uten ut.no-lenke», E Åpne punkter (MET-form).

## 2. Avvik (bevisste)

- **Mobil utsatt** – NFR-3 (360 px, 44 px, kart/nivå/tid/tips uten mye rulling på mobil) og UJ-1 på mobil. Memlog (override) Plattform, l. 18 → E Avvik fra PRD.
- **UJ-1/UJ-2 tilpasset desktop** (sofa, 2 t, lørdag, utsikt; «etter noen turer» komprimert) – memlog (decision) Journey desktop, l. 16 og UJ-2, l. 50 → E Avvik fra PRD.
- **UJ-3 slett konto lagt til** – memlog l. 51 → E Avvik fra PRD.
- **Grønn i UJ-1 (7,2 km) feil mot FR-2** – memlog (assumption) l. 21 → E Avvik fra PRD.
- **Mørk modus i v1** (ikke i PRD) – memlog (change) l. 26.
- **Egen KI-åpenhet** (merke, panel) utover PRD – memlog l. 47.
- **Jeg-form vs. PRD-tekstenes vi-form** – memlog (decision) Stemme, l. 42 → E Avvik fra PRD.

## 3. Mistet

1. **Startpunktet vises ikke i tekst på turforslaget.** §3 Tur: «Hver tur har navn, startpunkt …»; UJ-1: «så han pakker og går». E «Infokolonne» har fast rekkefølge uten startpunkt; bare markøren «S» på kartet. Brukeren får ikke vite hvor han skal møte opp (navn på p-plass/holdeplass) uten å lese kartet.
2. **Sperre (FR-19) har ingen tekst eller tilstand.** «Når en tur er vurdert *vanskelig*, senkes nivåtaket midlertidig …». E har bare heving som eksempel; «Sperre» mangler også i domeneordlisten i E Voice and Tone. Begrunnelse ved sperre, og ved oppheving, er ikke skrevet.
3. **Turens turtyper vises bare som treff.** §3: «én eller flere turtyper». E «Turtype-treff» vises bare når brukeren valgte turtype; uten valg får brukeren aldri vite at turen f.eks. har utsikt.
4. **Inndata for brukt tid er ikke designet.** FR-16: «brukt tid (fra 10 minutter til 24 timer)». E sier bare «Skjemafelt»; kontrollen (timer + minutter? nedtrekk?) og formatet «1 t 50 min» er ikke spesifisert.
5. **Personvern er usynlig i grensesnittet.** NFR-5: lagrer bare e-post, hash, historikk; «sporer ikke posisjon»; «Ingen personopplysninger sendes til KI-leverandøren». Ingen tekst på Registrer/Konto om hva som lagres, og «Slik lager jeg forslaget» sier ikke hva KI får se.
6. **Grunnlaget for bekledningstips sies ikke til brukeren.** FR-9: «for startpunktet på dagtid (kl. 10–16)». E kjenner regelen, men overlinjen er bare «Bekledningstips for {dag}».
7. **«Finne igjen turer jeg likte» (§2.1 Over tid; UJ-2 «favoritturen fra i vår»).** Historikk er bare sortert nyeste først [ASSUMPTION]; ingen sortering/markering etter fornøydhet, så favoritten må letes fram i en lang liste.
8. **Nedstigning** (§3 Tur) vises ikke i Faktarute. FR-6 krever det ikke, men på tur-retur med stor nedstigning påvirker den tiden; lav prioritet.

## 4. Konflikter (ikke loggført)

1. **«Åpne som turforslag» fra Historikk (FR-17) har ikke noe søk.** Søkeoppsummering, «Nytt forslag» (FR-7: «neste tur i rangeringen»), dato for bekledningstips (FR-9) og begrunnelsen som «nevner minst varigheten» (FR-12) forutsetter et søk. Ikke avklart i E.
2. **Økt (§3: «til … siden lastes på nytt») mot sidebasert flyt.** Innlogging/registrering er egne sider (memlog l. 38–39), og nettleserens Tilbake skal virke mellom Søk og Turforslag (E Interaction). Hvis navigasjonen laster siden på nytt, nullstilles økten og «Nytt forslag» kan gjenta turer etter retur. FR-14 sier bare at *forslaget* beholdes.
3. **Nivåtaksmeldingen sier «Lag konto» til innloggede.** FR-8 gir samme tekst til «gjester og brukere uten historikk»; E legger til lenken «Lag konto» for «gjest eller ny bruker». En innlogget bruker uten historikk får beskjed om å lage konto.
4. **«Lengre turer» stemmer ikke med nivåregelen.** FR-8-teksten «låse opp lengre turer» og E-eksemplet «foreslår jeg litt lengre turer» – men FR-19 hever *nivåtak* (lengde **eller** høydemeter), og varigheten styres fortsatt av brukeren. Ordlyden «låse opp» trekker også mot SM-C1 («skal ikke presse nybegynnere oppover»).
5. **Mobilavviket er ufullstendig ført.** E Avvik fra PRD nevner NFR-3 og UJ-1, men ikke SM-4 («manuell test av mobilvisning»), FR-4-beskrivelsen («raskt å fylle ut på mobil») eller §2.1 Kontekst («på mobilen på vei ut»). Alle må med i PRD-oppdateringen.
6. **Glemt passord mot NFR-2.** §7.2 flytter glemt passord til senere fase, men NFR-2 krever forklaring med neste steg i alle tilstander. E «Feil innlogging» gir ingen vei videre for den som har glemt passordet.
7. **Spines krever data PRD-en ikke har.** Turillustrasjon (høydeprofil, «utsikt etter ca. … km»), utsiktsmarkør på kartet og Kartbeskrivelse-tekst per tur forutsetter høydeprofil, utsiktspunkt og fritekstbeskrivelse. §3 Tur og addendum («Statisk GeoJSON med feltene `kilde`, `lisens`, `lengde_km` …») har bare aggregerte verdier.
