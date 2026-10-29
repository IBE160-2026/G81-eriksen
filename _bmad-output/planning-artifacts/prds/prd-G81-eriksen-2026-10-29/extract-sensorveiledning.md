# Uttrekk: Sensorveiledning IBE160 – Del 1 (applikasjon og prosess)

Kilde: `C:\IBE160\Sensorveiledning IBE160 - Del 1 applikasjon og prosess.pdf` (7 sider, høst 2026). Sidetall i parentes.
Prosjekt: *Your Next Adventure*, en KI-assistert nettside med turforslag for nybegynnere i Oslomarka (BMAD-metoden).

Del 1 ("Prosjektkode og funksjonalitet") teller **70 %** av samlet karakter. Refleksjonsrapporten (del 2) teller 30 % (s. 1, 7). Emnet handler om å *styre* KI-assistert utvikling. Sporene av prosessen vurderes derfor like tungt som sluttproduktet (s. 1). Veiledningen er støtte for faglig skjønn og ingen mekanisk sjekkliste. Kravene vurderes opp mot oppgaven og ambisjonsnivået gruppen selv har valgt (s. 1).

---

## 1. Hva som vurderes (kriterier og vekting)

| Nr | Kriterium | Hva det handler om | Vekt |
|---|---|---|---|
| 1 | Prosess og KI-styring | Sporbar vei fra plan til kode: commits, prompts, iterasjoner, beslutninger | **30 %** |
| 2 | Funksjonalitet og omfang | Hva appen gjør, målt mot proposal og valgt oppgave | **20 %** |
| 3 | Kvalitetssikring og testing | Tester, kodegjennomgang, retting av KI-generert kode | **15 %** |
| 4 | Design og brukeropplevelse | Visuelt uttrykk, konsistens, brukervennlighet, tilgjengelighet | 10 % |
| 5 | Kodekvalitet og arkitektur | Lesbar, strukturert og sammenhengende kode | 10 % |
| 6 | README og kjørbarhet | Hvordan appen installeres og kjøres | 10 % |
| 7 | Ryddighet i repoet | Struktur, riktige filer, ingen hemmeligheter eller byggeartefakter | 5 % |

(s. 1)

- Kriteriene 1, 6 og 7 (prosess og etterprøvbarhet) utgjør til sammen **45 %**. Kriteriene 2–5 (produkt) utgjør **55 %** (s. 1).
- Utregning: A=5, B=4, C=3, D=2, E=1, F=0. Hver karakter ganges med vekten og summeres. Terskler: A ≥ 4,5, B ≥ 3,5, C ≥ 2,5, D ≥ 1,5, E ≥ 0,5, F < 0,5. Sensor kan avvike fra summen med kort begrunnelse (s. 7).
- Eksempel fra veiledningen: (B, C, C, A, C, B, D) gir 3,55, altså B (s. 7).

### Sensors fremgangsmåte (s. 2)
1. Leser proposal og eventuell product brief for å se hva gruppen har lovet å lage.
2. Kloner repoet i IBE160-2026 og sjekker ut **siste commit før fristen**.
3. Installerer og starter appen i et rent miljø **bare etter README.md**.
4. Tester kjerneflytene og prøver **feil input og uventet bruk**.
5. Vurderer designet, gjerne på flere skjermstørrelser.
6. Går gjennom historikken: git log, GitHub Insights, branches, PR-er og issues.
7. Leser prosessdokumentasjonen: BMAD-dokumenter, prompts og KI-økter, beslutninger og QA. **Sjekker at dokumentene henger sammen med koden.**
8. Kjører testene slik README beskriver.
9. Stikkprøver koden.

Sensor bruker omtrent 15–20 minutter på å få appen til å kjøre. Det som ikke kan løses ved hjelp av README, regnes som feil i README. Kjører ikke appen, trekker det tydelig ned på kriterium 6 og begrenser hvor høyt kriterium 2 kan vurderes (s. 2).

---

## 2. Krav til applikasjonen

**Merk:** Veiledningen setter **ingen eksplisitte minimumskrav** til innlogging, database, KI-funksjon i appen eller deploy/hosting. Funksjonaliteten måles mot **proposal og valgt ambisjonsnivå** (s. 1, 3). Det som står:

- **Kjerneflyter fra proposal og README skal fungere fra start til slutt** (s. 3).
- **Omfang og kompleksitet** vurderes opp mot oppgaven. Eksempler på det som teller: *datalagring, flere brukerroller, integrasjoner, ikke-trivielle regler* (s. 3). Innlogging/roller, database og integrasjoner gir altså uttelling for omfang, men er ikke absolutte krav.
- **Stabilitet:** Appen skal tåle vanlig bruk, feil input og gjentatte handlinger uten å krasje (s. 3).
- **Utelatt eller endret funksjonalitet** fra proposal skal beskrives og begrunnes (s. 3).
- **Feilhåndtering og validering av input**, og bevissthet om sikkerhet: ingen hemmeligheter i koden (s. 4).
- **Design og UX:** konsistent visuelt uttrykk, tydelig navigasjon, forståelige tilbakemeldinger, feilmeldinger og tomtilstander. Grunnleggende **universell utforming**: kontrast, tastaturnavigasjon, alt-tekst og skjemaetiketter. **Responsivt** der det er relevant (s. 4).
- **Kjørbarhet:** Appen skal kunne installeres og startes lokalt etter README, med `.env.example` uten ekte nøkler (s. 5). Deploy nevnes ikke. Sensor kjører appen selv.
- **Automatiserte tester** (enhets-, integrasjons- eller E2E-tester) som kjøres etter README og tester meningsfull logikk (s. 4).
- **Kode:** mappestruktur som samsvarer med den beskrevne arkitekturen, lite duplisering eller død kode, gjerne linter/formatter, fornuftig håndtering av konfigurasjon og avhengigheter (s. 5).
- **Repo:** `.gitignore` for `node_modules`, `venv` og build, **ingen API-nøkler eller .env i repoet eller historikken**, ingen løse filer i rotmappen (s. 6–7).

---

## 3. Krav til prosess og dokumentasjon

**Planlegging (BMAD)** (s. 2)
- BMAD-dokumenter (product brief, **PRD**, arkitektur, epics, stories) skal være **brukt og oppdatert** og ikke *generert én gang*.
- **Sammenheng mellom plan og kode:** Funksjoner skal kunne spores tilbake til krav og stories. **Avvik fra planen skal forklares.**
- **Beslutninger:** Valg av teknologi, arkitektur og løsninger skal dokumenteres med begrunnelse.

**KI-bruk** (s. 2, 7)
- **Lagrede prompts og KI-økter.**
- Konkrete eksempler på at gruppen har **presisert krav, avvist, rettet eller forbedret KI-forslag**.
- KI-dokumentasjonen skal knyttes til **konkrete endringer i repoet**. Generell tekst er et varseltegn (s. 7).

**Git-arbeidsflyt** (s. 2)
- Jevn utvikling over tid med små, avgrensede commits og beskrivende meldinger.
- Branches, pull requests og issues eller tilsvarende.
- Historikken skal vise at gruppen har gjort arbeidet over tid. Skjev commit-statistikk gir alene ikke trekk.

**Kvalitetssikring** (s. 4)
- Dokumenterte manuelle tester eller testplaner der automatiske tester ikke passer.
- Spor av kodegjennomgang: PR-kommentarer og beskrivelser av feil i KI-kode og hvordan de ble rettet.

**Design i prosessen** (s. 4)
- Skisser, wireframes eller UX-beskrivelser i planleggingsdokumentene.

**README** (s. 5)
- Hva appen gjør og for hvem, gjerne med skjermbilde.
- Forutsetninger med versjoner.
- Kommandoer steg for steg som kan kopieres.
- Miljøvariabler og `.env.example`.
- Testdata eller testbrukere, og hvordan testene kjøres.
- Oversikt over mappestrukturen.
- **Lenker til planleggings- og prosessdokumentasjonen.**
- Tilpasset prosjektet og oppdatert.

---

## 4. Hva som skiller god fra svak karakter

| Kriterium | A–B | D–F |
|---|---|---|
| 1 Prosess (s. 3) | Prosessen kan følges tydelig fra plan til ferdig app. Jevn, iterativ historikk. Prompts og beslutninger er **koblet til konkrete endringer**. **Flere tydelige eksempler** på kritisk styring og korrigering av KI | Planen ser ut til å være generert én gang og ikke brukt. Få prompts. Commits samlet i få perioder (F: bare opplasting av ferdig kode) |
| 2 Funksjonalitet (s. 3) | Kjernen er komplett og stabil. Omfanget **svarer til eller overgår** proposal | Sentrale funksjoner mangler eller feiler, eller omfanget er klart mindre uten begrunnelse |
| 3 QA (s. 4) | Testene er relevante, kjører uten feil og dekker sentral logikk. **Systematisk og dokumentert QA med konkrete eksempler på feil som ble funnet og rettet** | Få tester, tester som feiler eller trivielle tester. QA er knapt dokumentert |
| 4 Design (s. 4–5) | Gjennomarbeidet, konsistent og intuitivt. Bevisste valg tilpasset målgruppen. Tilgjengelighet er ivaretatt | Uoversiktlig eller vanskelig å bruke uten forklaring |
| 5 Kode (s. 5) | Godt strukturert. **Arkitekturen samsvarer med dokumentasjonen** | Mye duplisering, død kode, uklar struktur |
| 6 README (s. 6) | Sensor får appen til å kjøre **uten avvik** | Betydelig innsats nødvendig, eller appen kan ikke kjøres |
| 7 Repo (s. 6) | Ryddig, bare relevante filer, ingen hemmeligheter | Byggeartefakter eller avhengigheter i repoet (F: ekte hemmeligheter som ikke er håndtert) |

**Varseltegn** (s. 6–7):
- Nesten all kode lagt inn i én eller noen få commits rett før fristen.
- **Planleggingsdokumenter som beskriver en annen app enn den som er levert, eller som tydelig er laget i etterkant.**
- README-mal eller kommandoer som ikke virker.
- Committede nøkler eller `.env`.
- `node_modules`, `venv` eller build i repoet.
- Tester som feiler eller er trivielle.
- Død kode eller rester fra forkastede KI-forsøk.
- Generell KI-dokumentasjon uten kobling til repoet.

---

## 5. Konkrete implikasjoner for PRD-en (Your Next Adventure)

1. **Sporbare krav:** Gi hvert funksjonelle krav en ID (f.eks. FR-01), slik at epics, stories, commits, PR-er og tester kan vise til det. Det dekker *sammenheng mellom plan og kode* (s. 2) og A–B på kriterium 1 (s. 3).
2. **Forankring i proposal:** Vis hvordan PRD-en svarer til eller utvider proposal og product brief. Ha et eget avsnitt for **endringer og utelatelser med begrunnelse** (s. 3).
3. **MVP vs. senere:** Avgrens kjerneflytene tydelig, for eksempel at en nybegynner oppgir preferanser, får KI-genererte turforslag i Oslomarka og ser turdetaljer. Sensor tester nettopp disse flytene fra start til slutt (s. 2–3). Ikke lov mer enn dere rekker. Omfang under proposal uten begrunnelse trekker ned.
4. **Omfang og kompleksitet:** Beskriv eksplisitt datalagring (turdata, lagrede favoritter), eventuelle brukerroller eller innlogging, integrasjoner (KI-API, kart- eller værdata) og ikke-trivielle regler, som filtrering på vanskelighetsgrad, lengde og kollektivtilgang for nybegynnere. Dette er eksemplene veiledningen gir på omfang (s. 3).
5. **Ikke-funksjonelle krav:**
   - Stabilitet og håndtering av feil input, inkludert tomme eller ugyldige KI-svar, timeout og fallback (s. 3–4).
   - Sikkerhet: API-nøkler i miljøvariabler og `.env.example` (s. 4–5).
   - Universell utforming: kontrast, tastatur, alt-tekst og skjemaetiketter (s. 4).
   - Responsivt design, der mobil er relevant for turgåere (s. 4).
6. **UX-seksjon:** Ta med brukerreiser og personas (nybegynner), wireframes eller skisser, og tilstander for tilbakemelding, feil og tom visning. Det gir *spor av designarbeid* (s. 4).
7. **Ansvarlig KI-bruk i produktet:** Beskriv hvordan KI-forslag valideres. Det henger sammen med kriteriet om kritisk KI-styring (s. 2).
8. **Akseptansekriterier som kan testes:** Skriv kriterier som kan bli automatiske tester eller manuelle testplaner. Det støtter kriterium 3 (s. 4).
9. **Tekniske beslutninger med begrunnelse:** Begrunn eller vis til valg av stack, database og KI-leverandør. Detaljene kan ligge i arkitekturdokumentet (s. 2).
10. **Levende dokument:** Ta med endringslogg og versjonshistorikk i PRD-en, og oppdater den når planen endres. Lagre promptene og KI-øktene som ble brukt til å lage PRD-en. Det motvirker varseltegnet om at dokumentene er "generert én gang" eller "i etterkant" (s. 2, 6).
11. **Kjørbarhet som krav:** Lokal oppstart etter README skal være et krav. Deploy er ikke påkrevd, men sensor må kunne kjøre appen på 15–20 minutter (s. 2, 5–6).
12. **Samsvar med leveransen:** PRD-en må beskrive den appen som faktisk blir levert (s. 6).
