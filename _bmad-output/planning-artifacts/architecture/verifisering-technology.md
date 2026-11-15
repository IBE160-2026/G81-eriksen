# Verifisering av `technology.md` mot BMAD-produktene

Dato: 2026-11-15. Branch: `planlegging/verifiser-technology`.

`technology.md` er en referanse fra faglærer. Den beskriver `pytagoras-website-v2`, en annen app. Her er hvert valg i referansen sjekket mot våre egne BMAD-produkter:

- PRD v1.9 (`prds/prd-G81-eriksen-2026-10-29/prd.md`)
- `DESIGN.md` og `EXPERIENCE.md` (`ux-designs/ux-G81-eriksen-2026-11-06/`)
- `ARCHITECTURE-SPINE.md` (AD-1 til AD-14) og beslutningsloggen `.memlog.md`
- `docs/arkitektur.md`

## Konklusjon

1. **Ingen motstrid som krever endring i PRD, UX eller arkitektur.** Hvert valg i referansen er enten tatt med i en enklere form, bevisst valgt bort med begrunnelse, eller utenfor v1.
2. **Påstandene i `architecture/README.md` stemmer.** Alle de tre mønstrene og bortvalgene finnes i spinen og beslutningsloggen (se tabell 1).
3. **Referansen avdekker fem hull.** Ett av dem (H-1) gjelder et krav vi allerede har, men som repoet ikke oppfylte. De andre fire er små. Alle fem er rettet 2026-11-15 (se kapittelet om rettelser).

Statusene i tabellene:

| Status | Betyr |
| --- | --- |
| **Samsvar** | Samme prinsipp finnes hos oss, ofte enklere |
| **Valgt bort** | Vurdert og forkastet, med begrunnelse i spinen eller beslutningsloggen |
| **Utenfor v1** | Funksjonen finnes ikke i PRD-en for v1 |
| **Hull** | Ikke dekket av BMAD-produktene. Se kapittelet om hull |

## 1. Kontroll av `architecture/README.md`

| Påstand i README | Funnet i | Stemmer? |
| --- | --- | --- |
| Mock-fallback: appen virker uten nøkler | AD-10 punkt 1 (ekte, reserve, falsk), AD-12 punkt 3, NFR-1 | Ja |
| Demokontoer ved oppstart = testbrukeren i `lastinn` | AD-3 punkt 4, AD-11 punkt 3, FR-21 | Ja |
| Rate limiting per nettleser og per døgn, ikke per IP | AD-10 punkt 9, NFR-8. Per IP er forkastet i `.memlog.md` (2026-11-12) fordi v1 bare kjører lokalt | Ja |
| Valgt bort: flere tjenester, Docker, Postgres, Redis, Next.js | AD-1, AD-4, AD-12, `.memlog.md` (stack-paradigme, alternativ B og C), `docs/arkitektur.md` › Viktige valg | Ja |
| Betaling, e-post og regnskap er utenfor v1 | PRD §7.2 (glemt passord og e-post i senere fase), spinen › Deferred | Ja. Betaling og regnskap står ikke ordrett i §7.2, men ingen FR krever dem |

## 2. Gjennomgang per kapittel i `technology.md`

### §1 Hva systemet er

| I referansen | Hos oss | Status |
| --- | --- | --- |
| Fullstack-app med butikk, admin, kurs, abonnement og KI-assistent | Én nettside med søk, turforslag, konto og historikk (PRD §6) | Utenfor v1 (alt utenom KI og konto) |
| Kontrollplan som utsteder tokens til en egen innholdstjeneste | Én prosess, ingen andre tjenester (AD-1) | Valgt bort |
| Zero-config / mock-fallback for alle integrasjoner | KI har reserve (AD-10). Kart og vær trenger ingen nøkkel (AD-8, AD-9). `.env.example` virker uten endring (AD-12) | Samsvar |

### §2 Tjenester og tillitsmodell

| I referansen | Hos oss | Status |
| --- | --- | --- |
| Caddy-proxy, separat backend og frontend, Redis, Postgres, Storage, backup, watchdog, Cloudflare Worker | Én Django-prosess og én SQLite-fil (AD-1, AD-4). Ingen deploy (AD-12 punkt 7) | Valgt bort |
| Single-origin, ingen CORS | Serveren svarer med HTML til egne sider, aldri JSON (AD-1). Bare kartfliser hentes fra et annet domene (AD-8) | Samsvar |
| Persondata blir i hovedappen, bare pseudonym ut | KI får aldri e-post, bruker-ID eller historikk (AD-10 punkt 5, NFR-5) | Samsvar |
| Lokal e-post/passord med bcrypt og egen JWT | Djangos auth med egen brukermodell og e-post som brukernavn (AD-7). Djangos standard hash | Samsvar (annen teknikk) |
| Admin-rolle via `ADMIN_EMAILS` | Ingen admin i PRD-en | Utenfor v1 |
| Per-IP rate limiting på KI-ruter | Per nettleser og per døgn (AD-10 punkt 9) | Samsvar |
| Per-IP rate limiting på **innlogging** | Ikke nevnt i NFR-8 eller spinen | **Hull H-2** |
| Nekter å starte utenfor lokalt miljø med standard-hemmelighet | Ingen deploy i v1. Ikke nevnt i Deferred | **Hull H-2** |

### §3 Backend

| I referansen | Hos oss | Status |
| --- | --- | --- |
| Python ≥ 3.11 | Python 3.12–3.15 (spinen › Stack) | Samsvar |
| uv med låsefil | `pip` og `requirements.txt` med låste versjoner (AD-12 punkt 2). uv er forkastet for appen fordi det gir sensor et ekstra installasjonssteg (`.memlog.md`) | Valgt bort, samme prinsipp (låste versjoner) |
| FastAPI, SQLAlchemy async, Alembic | Django med ORM og migreringer (AD-1, AD-4). FastAPI er forkastet (`.memlog.md`, alternativ B) | Valgt bort |
| Pydantic, pydantic-settings | Django-skjemaer (konvensjon Skjema). Miljøverdier leses bare i `config/settings.py` med `python-dotenv` (AD-12 punkt 3) | Samsvar (annen teknikk) |
| Stripe, Vipps, Resend, WeasyPrint, Fiken | Ingen betaling, e-post eller PDF | Utenfor v1 |
| pydantic-ai mot OpenRouter, modell kan byttes i admin | `anthropic`-SDK direkte, `claude-haiku-5-5`. Valgt fordi betalte kall ikke brukes til trening (NFR-5, `docs/arkitektur.md`). En mellomtjeneste som OpenRouter ville gitt enda en part som ser friteksten. Leverandørbytte er én ny variant i `tjenester/ki/` (Deferred) | Valgt bort |
| Redis-cache | Værbufferen er en Django-modell i SQLite (AD-9) | Samsvar (annen teknikk) |
| pytest, pytest-asyncio, in-memory SQLite | `python manage.py test`, ingen nettverkskall, falsk KI og lagrede MET-svar (AD-13) | Samsvar (annen teknikk) |
| Vertikale moduler per funksjon | Fire horisontale lag der `domene/` er ren Python (AD-2). Valgt for at reglene skal kunne testes uten database (SM-2) | Valgt bort |
| `FEATURE_*`-flagg | P2-kutt gjøres i koden og føres i PRD §9 og endringsloggen (PRD §7.1). Det trengs ingen bryter mens appen kjører | Valgt bort (ikke behov) |
| Aldri `rollback()` på delt sesjon; `INSERT … ON CONFLICT DO NOTHING` | Engangstoken mot dobbel registrering (AD-14). `F("antall") + 1` i transaksjon for KI-telling (AD-10 punkt 9). Hvordan døgnets første rad lages, står ikke | Samsvar, men se **Hull H-4** |
| Seeding ved oppstart, demokontoer bare lokalt | `lastinn` med én kommando (AD-3, NFR-1). Testbrukeren lastes alltid, siden v1 bare kjører lokalt | Samsvar. Se **Hull H-2** for en eventuell deploy |

### §4 Frontend

| I referansen | Hos oss | Status |
| --- | --- | --- |
| Next.js, React, TypeScript, TanStack Query | Django-maler, to små JS-filer uten rammeverk og byggesteg (AD-1). Next.js er forkastet fordi det ikke er Python, og React fordi sensor da trenger Node (`.memlog.md`) | Valgt bort |
| Tailwind, shadcn/ui, Radix | Egen CSS etter `DESIGN.md` (fargetema Granskog) | Valgt bort |
| `geist`-font | Systemfonter, ingen webfont (`DESIGN.md`) | Valgt bort |
| `next-themes` for mørk modus | `prefers-color-scheme`, ingen bryter (NFR-9, `DESIGN.md`) | Samsvar (enklere) |
| TipTap, Univer, ace, Recharts, dnd-kit | Høydeprofil og turillustrasjon som SVG fra serveren (AD-8) | Utenfor v1 |
| DOMPurify | Django escaper all tekst i maler automatisk, også KI-tekst. KI-svar valideres i tillegg (AD-10 punkt 7) | Samsvar |
| CSP i `next.config.ts` | Ingen Content-Security-Policy i spinen | **Hull H-3** |
| Vitest og Playwright (e2e) | Ingen e2e-tester i AD-13. NFR-4 verifiseres med et automatisk verktøy og sjekklisten i `EXPERIENCE.md` (SM-4) | Valgt bort (ikke krav) |
| Docker-bygg med `node:22-alpine` | Ingen Node og ingen Docker (AD-1, AD-12) | Valgt bort |

### §5 Infrastruktur og drift

| I referansen | Hos oss | Status |
| --- | --- | --- |
| Docker Compose lokalt | `venv`, `pip`, `migrate`, `lastinn`, `runserver` (AD-12 punkt 1) | Valgt bort |
| Railway, Supabase, Cloudflare, backup til R2, watchdog | Ingen deploy i v1 (AD-12 punkt 7, Deferred) | Utenfor v1 |
| `production`-gren som deploy-trigger, `main` som arbeidsgren | `main` og korte brancher med PR (gruppens arbeidsmåte). Ingen deploy | Utenfor v1 |

### §6 og §7 Nøkler, miljøvariabler og kontoer

| I referansen | Hos oss | Status |
| --- | --- | --- |
| Over 100 miljøvariabler i 13 grupper | Fire: `DJANGO_SECRET_KEY`, `DEBUG`, `ANTHROPIC_API_KEY` (tom) og `MET_USER_AGENT` (AD-12 punkt 3) | Samsvar (enklere) |
| Aldri hemmeligheter til nettleseren (`NEXT_PUBLIC_*`) | Bare serveren kaller MET og KI (AD-9, AD-10). Kartflisene krever ingen nøkkel (AD-8) | Samsvar |
| Ni kontoer må opprettes | Ingen for å kjøre appen. Anthropic-konto bare for ekte KI (åpent punkt i `issues.md`, 2026-11-08) | Samsvar |
| Kontaktinfo i User-Agent mot eksterne API-er (ikke nevnt i referansen) | `MET_USER_AGENT` med appnavn og repo-URL, ingen personlig e-post (AD-12 punkt 3) | Bare hos oss |
| `.env.example`-filer, hemmeligheter aldri i git | `.env.example` følger med, `.env` i `.gitignore` (AD-12 punkt 3 og 4, NFR-1) | Samsvar, men se **Hull H-1** og **H-5** |

### §8 Sjekkliste ved replikering

| Punkt | Status hos oss |
| --- | --- |
| 1. FastAPI + Next + Caddy + Postgres + Storage + Redis i Docker | Valgt bort (AD-1, AD-4, AD-12) |
| 2. Mock-fallback og feature-flagg fra dag én | Mock-fallback: samsvar (AD-10). Feature-flagg: ikke behov |
| 3. Nye nøkler, `APP_ENV=production` | Utenfor v1. Se H-2 |
| 4.–8. Supabase, Resend, Stripe/Vipps, `COMPANY_*`, backup | Utenfor v1 |
| 9. `production`-gren | Utenfor v1 |
| 10. Hopp over ekstra tjenester | Samsvar: vi har ingen |

## Hull

| ID | Hull | Hvorfor det betyr noe | Forslag | Prioritet |
| --- | --- | --- | --- | --- |
| **H-1** | `.gitignore` oppfyller ikke AD-12 punkt 4. Den mangler databasefilen og `logs/`. `*.log` stopper `logs/ki.log`, men ikke de roterte filene, som `TimedRotatingFileHandler` kaller `ki.log.2026-11-14` | De roterte KI-loggene kan havne i git. Det bryter NFR-5 («aldri i git») og AD-10 punkt 8. Databasefilen med testbrukere og kontoer kan bli committet, som bryter AD-4 | Legg til `db.sqlite3` (eller navnet som velges i `config/settings.py`) og `logs/`. Fjern samtidig blokken for Next.js/Node, som er rester fra malen og ikke passer med AD-1 | Høy. Bør gjøres før første story med logg eller database |
| **H-2** | Sikring som referansen har for drift, er ikke nevnt i Deferred: oppstartsvakt mot standard-`SECRET_KEY` med `DEBUG=False`, grense for innloggingsforsøk og at testbrukeren ikke lastes utenfor lokal kjøring | Ingen risiko i v1, som bare kjører lokalt. Men passordet til testbrukeren står i README (FR-21), og ved en senere deploy ville det vært en åpen konto | Utvid Deferred-raden «Produksjonsdeploy, HTTPS …» i spinen med disse tre punktene, så de ikke glemmes | Lav |
| **H-3** | Ingen Content-Security-Policy | KI-tekst og fritekst vises i sidene. Django escaper dem, men en CSP er et ekstra lag. Hos oss er en streng CSP enkel, fordi alt JavaScript og Leaflet ligger lokalt (AD-8) og bare kartflisene kommer fra `cache.kartverket.no` | Vurder Djangos innebygde CSP-støtte (fra Django 6.0) med `script-src 'self'` og `img-src 'self' https://cache.kartverket.no`. Sjekk at `kart.js` får GeoJSON via `json_script` og ikke inline-skript. Ikke krav i NFR-8 | Lav, valgfri |
| **H-4** | AD-10 punkt 9 sier hvordan dagens KI-telling økes, men ikke hvordan døgnets første rad i `KiForbruk` lages | To samtidige første kall i et døgn kan gi to rader eller en `IntegrityError`, altså feil telling eller krasj (NFR-2) | Presiser i storyen: `dato` er unik, raden lages med `get_or_create`, og deretter `F("antall") + 1` i samme transaksjon | Lav |
| **H-5** | Referansen «feiler aldri hardt». Hos oss står det ikke hva som skjer hvis sensor glemmer å kopiere `.env.example` til `.env` | Da mangler `DJANGO_SECRET_KEY`, og Django stopper med en engelsk feilmelding. Det kan koste tid mot 20-minuttersgrensen i NFR-1 | Enten falle tilbake til verdiene i `.env.example` når `.env` mangler, eller stoppe med en norsk melding som sier hva som må gjøres. Avgjøres i storyen for oppsett | Lav |

## Rettelser 2026-11-15

Produkteier ba om at manglene rettes. PRD-en og UX-spesifikasjonen er ikke endret, fordi ingen av hullene gjelder krav eller design.

| ID | Rettet i | Hva |
| --- | --- | --- |
| H-1 | `.gitignore`, spinen AD-4 og AD-12 punkt 4 | `db.sqlite3`, `db.sqlite3-journal` og `logs/` er lagt til. Blokken for Next.js/Node er fjernet, men `build/` og `dist/` er flyttet til Python-blokken, fordi Python-pakking også bruker dem. AD-4 navngir databasefilen. Sjekket med `git check-ignore`: `logs/ki.log.2026-11-14` og `db.sqlite3` ignoreres, mens `.logs/` og `.env.example` fortsatt er sporet |
| H-2 | Spinen › Deferred, `docs/arkitektur.md` › Sikkerhet | Raden for produksjonsdeploy krever oppstartsvakt (`DEBUG=False` med utviklingsnøkkel, `check --deploy`), grense for innloggingsforsøk og ingen testbruker før en eventuell deploy. **Erstattet samme dag:** Faglærer krever publisering på Vercel, så oppstartsvakten står nå i AD-15 og grensen for innloggingsforsøk i AD-7. Testbrukeren beholdes på nett og lages på nytt ved hver publisering (valgt av produkteier, PRD NFR-10) |
| H-3 | Spinen › Consistency Conventions, `docs/arkitektur.md` › Sikkerhet | Ny konvensjon for Content-Security-Policy med Djangos innebygde CSP. Bare `self`, pluss `cache.kartverket.no` for bilder. Ingen inline-skript eller `style`-attributter. Turdata til `kart.js` sendes med `json_script` |
| H-4 | Spinen AD-10 punkt 9 | `KiForbruk.dato` er unik. Døgnets rad lages med `get_or_create`, og deretter økes den med `F("antall") + 1`, i samme transaksjon |
| H-5 | Spinen AD-12 punkt 3, `docs/arkitektur.md` › Sikkerhet | Mangler `.env` eller `DJANGO_SECRET_KEY`, stopper appen med en norsk melding om å kopiere `.env.example`. Reserveverdier i koden er forkastet: de gir to kilder til samme verdi og kan skjule feil oppsett |

Beslutningen står i `.memlog.md` (2026-11-15). `lint_spine.py` gir bare de seks gamle falske treffene på plassholdere (`{z}/{y}/{x}` i flis-URL-en og KI-plassholderne), ingen nye.
