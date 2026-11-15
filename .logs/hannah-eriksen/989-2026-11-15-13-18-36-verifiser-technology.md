# verifiser-technology

## 2026-11-15 kl. 13:18 — Hannah Eriksen

### Oppgave
Brukeren ba om en ny branch for å verifisere `architecture/technology.md` (referanse fra faglærer om `pytagoras-website-v2`) mot våre egne BMAD-produkter.

### Plan
- Opprette branchen `planlegging/verifiser-technology` fra oppdatert `main`.
- Gå gjennom hvert kapittel i `technology.md` og sjekke hvert valg mot PRD v1.9, `DESIGN.md`, `EXPERIENCE.md`, `ARCHITECTURE-SPINE.md` (AD-1 til AD-14), `.memlog.md` og `docs/arkitektur.md`.
- Kontrollere påstandene i `architecture/README.md` om hvilke mønstre som er tatt med og valgt bort.
- Samle resultatet i et eget dokument, uten å endre PRD, UX eller spinen.

### Resultat
- Nytt dokument: `_bmad-output/planning-artifacts/architecture/verifisering-technology.md`. Det har lenke fra `architecture/README.md`. Commit `f22caeb` på `planlegging/verifiser-technology`. Ikke pushet.
- Ingen motstrid som krever endring i PRD, UX eller arkitektur. Hvert valg i referansen er enten med i enklere form, valgt bort med begrunnelse eller utenfor v1.
- Alle påstandene i `architecture/README.md` stemmer med spinen og beslutningsloggen.
- Fem hull:
  - **H-1 (høy):** `.gitignore` mangler databasefilen og `logs/` (AD-12 punkt 4). `*.log` stopper ikke roterte KI-logger (`ki.log.2026-11-14`), så de kan havne i git (NFR-5). Blokken for Next.js/Node er rester fra malen.
  - **H-2:** Deferred i spinen nevner ikke oppstartsvakt mot standard-`SECRET_KEY`, grense for innloggingsforsøk eller at testbrukeren ikke skal lastes ved en eventuell deploy.
  - **H-3:** Ingen Content-Security-Policy (valgfri, Djangos innebygde CSP).
  - **H-4:** AD-10 punkt 9 sier ikke hvordan døgnets første `KiForbruk`-rad lages (`get_or_create` med unik `dato`).
  - **H-5:** Det står ikke hva som skjer hvis `.env` mangler (NFR-1).

### Åpne punkter
- Rett `.gitignore` etter AD-12 punkt 4 (databasefil, `logs/`) og fjern Node-blokken (H-1).
- Avgjør om Deferred i spinen skal utvides med sikring før en eventuell deploy (H-2).
- Avgjør om appen skal ha en CSP (H-3).
- Presiser opprettelsen av døgnets `KiForbruk`-rad i storyen for KI-grensen (H-4).
- Avgjør oppførsel når `.env` mangler, i storyen for oppsett (H-5).

## 2026-11-15 kl. 13:23 — Hannah Eriksen

### Oppgave
Brukeren ba meg rette manglene (H-1 til H-5) fra verifiseringen av `technology.md`.

### Plan
- H-1 rettes i `.gitignore` og sjekkes med `git check-ignore`.
- Siden koden ikke finnes ennå, løses H-2 til H-5 som regler i spinen, med en beslutning i `.memlog.md` og en oppdatering av `docs/arkitektur.md`.
- Kjøre `lint_spine.py` etterpå.

### Resultat
- Commit `b9917af` på `planlegging/verifiser-technology`. Ikke pushet.
- **H-1:** `.gitignore` har fått `db.sqlite3`, `db.sqlite3-journal` og `logs/`. Blokken for Next.js/Node er fjernet, men `build/` og `dist/` er flyttet til Python-blokken. `git check-ignore` viser at `logs/ki.log.2026-11-14` og `db.sqlite3` ignoreres, mens `.logs/` og `.env.example` er sporet. AD-4 og AD-12 punkt 4 navngir `db.sqlite3`.
- **H-2:** Deferred-raden for produksjonsdeploy krever oppstartsvakt, grense for innloggingsforsøk og ingen testbruker før en eventuell deploy.
- **H-3:** Ny konvensjon i spinen for Content-Security-Policy med Djangos innebygde CSP (`self`, pluss `cache.kartverket.no` for bilder, ingen inline-skript, `json_script` for turdata).
- **H-4:** AD-10 punkt 9: `KiForbruk.dato` er unik, og raden lages med `get_or_create` før `F()`-økningen i samme transaksjon.
- **H-5:** AD-12 punkt 3: mangler `.env` eller `DJANGO_SECRET_KEY`, stopper appen med en norsk melding. Reserveverdier i koden er forkastet.
- Spinen har `updated: 2026-11-15`. Beslutningen står i `.memlog.md`. `docs/arkitektur.md` › Sikkerhet og `verifisering-technology.md` (nytt kapittel om rettelsene) er oppdatert.
- `lint_spine.py`: bare de seks gamle falske treffene på plassholdere, ingen nye.
- De fem åpne punktene fra forrige seksjon er lukket i `issues.md`.

### Åpne punkter
- Sjekk i kartstoryen at Leaflet virker med CSP-en, og utvid den med begrunnelse hvis det trengs.
