# G81 — Hannah Eriksen

**Publisert side:** <https://your-next-adventure.vercel.app> (NFR-10). Se [Publisering på Vercel](#publisering-på-vercel).

Gruppeprosjekt i **IBE160 Programmering med KI** ved Høgskolen i Molde, høsten 2026 (15 studiepoeng).

Repoet inneholder gruppens applikasjon og dokumentasjon av utvikling, testing og kvalitetssikring med KI.

## Om appen: Your Next Adventure

*Your Next Adventure* er en nettside for nybegynnere som vil på fottur i Oslo-området. Brukeren oppgir hvor lenge hen vil være ute og hvilken dag turen skal være. Hen kan også velge startpunkt og turtype og skrive ønsker i vanlig språk. Tjenesten svarer med ett konkret turforslag: rute på kart, estimert tid, bekledningstips ut fra været og en kort forklaring på hvorfor turen passer.

En bruker med konto kan registrere og vurdere turene sine. Tjenesten bruker vurderingene til å foreslå riktig nivå og variasjon neste gang. Tilpasningen følger enkle, faste regler som alltid kan forklares. KI tolker bare ønsker og formulerer begrunnelser, og velger aldri en tur utenfor den kuraterte turdatabasen.

Planlagt teknologi: Python og Django, SQLite lokalt og Postgres hos Neon på den publiserte siden, kart fra Kartverket, værvarsel fra MET og en valgfri språkmodell fra Anthropic. Appen publiseres på Vercel og skal også kunne kjøres lokalt uten nøkler. Se [arkitekturen](docs/arkitektur.md) for begrunnelsen.

## Status

| Fase | Status | Dokument |
|---|---|---|
| Product brief | Ferdig, med tilbakemelding fra faglærer | [Product brief](docs/product-brief-your-next-adventure-no.md) |
| Teknisk research | Ferdig | [Turdata i Oslomarka](_bmad-output/planning-artifacts/research/technical-turdata-oslomarka-2026-10-29/research.md) |
| PRD | Ferdig | [PRD](_bmad-output/planning-artifacts/prds/prd-G81-eriksen-2026-10-29/prd.md) |
| UX | Ferdig | [EXPERIENCE.md](_bmad-output/planning-artifacts/ux-designs/ux-G81-eriksen-2026-11-06/EXPERIENCE.md) og [DESIGN.md](_bmad-output/planning-artifacts/ux-designs/ux-G81-eriksen-2026-11-06/DESIGN.md) |
| Arkitektur | Ferdig | [Arkitektur](docs/arkitektur.md) |
| Epics og stories | Ferdig: 6 epics og 41 stories | [epics.md](_bmad-output/planning-artifacts/epics.md) |
| Implementering og testing | Pågår: story 1.1–1.6 er implementert, se sprint-status | [sprint-status.yaml](_bmad-output/implementation-artifacts/sprint-status.yaml) |

## Installasjon og kjøring

**Krav:** Python 3.12–3.15 (testet på 3.14). Du trenger ingen nøkler, Node, Docker eller databaseserver. Appen bruker SQLite, som følger med Python.

Kjør kommandoene fra mappen der du har klonet repoet.

**Windows (PowerShell eller ledetekst):**

```text
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py lastinn
python manage.py runserver
```

Stopper PowerShell `activate` fordi skript er blokkert, kjør først `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`.

**macOS og Linux:**

```text
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py lastinn
python manage.py runserver
```

Åpne så <http://127.0.0.1:8000/> i nettleseren. Stopp serveren med Ctrl+C.

**Admin (valgfritt):** `python manage.py createsuperuser` lager en admin-bruker for `/admin/`. Kommandoen spør etter e-post, ikke brukernavn.

**Miljøvariabler:** `.env.example` virker uten endring. Mangler `.env`, eller er `DJANGO_SECRET_KEY` tom, stopper appen med en melding om å kopiere `.env.example` til `.env`.

**Tester og kodestil:** Testene trenger ikke nett. Ruff ligger i `requirements-dev.txt`, som også installerer `requirements.txt`.

```text
pip install -r requirements-dev.txt
python manage.py test
ruff check .
ruff format --check .
```

**Turdatabasen:** `python manage.py lastinn` laster turene i `data/turer.geojson` inn i databasen. Kommandoen oppretter eller oppdaterer turer og startpunkter etter ID og sletter aldri noe, så den kan kjøres så ofte du vil. Er fila ugyldig, stopper den med en norsk melding, og databasen er uendret. Turer i databasen som mangler i fila, blir stående, og kommandoen skriver en advarsel med ID-ene. Med `--fil <sti>` laster du en annen fil enn `data/turer.geojson`. Se [data/README.md](data/README.md).

Innlogging for testbrukeren og hvordan en KI-nøkkel legges inn, kommer i senere stories. Kravene til denne delen står i [AD-12 i arkitekturen](_bmad-output/planning-artifacts/architecture/architecture-G81-eriksen-2026-11-07/ARCHITECTURE-SPINE.md).

## Publisering på Vercel

Appen ligger på <https://your-next-adventure.vercel.app>, med en Postgres-database hos Neon. Både appen (`fra1`) og databasen ligger i Frankfurt.

- **`main`** publiseres automatisk til adressen over etter hver merge.
- **Hver pull request** får en egen forhåndsvisning med en egen kopi av databasen (en Neon-gren). Forhåndsvisningen krever innlogging hos Vercel.
- **Byggesteget** står i `pyproject.toml` og kjører `python manage.py migrate --noinput` og så `python manage.py lastinn`, så databasen for miljøet alltid har turene fra `data/turer.geojson`. Stopper ett av stegene, feiler byggingen, og forrige publisering blir stående. Migreringene er derfor bakoverkompatible: de legger bare til, de fjerner ikke og gir ikke nytt navn, og nye felt tillater `null` eller har `db_default`. Vercel kjører `collectstatic` selv. Vercel installerer pakkene fra `[project]` i `pyproject.toml`, og den lista holdes lik `requirements.txt`.
- **Innstillingene** for Vercel gjelder bare når `VERCEL` er satt: `DEBUG` er alltid av, og appen stopper hvis `DJANGO_SECRET_KEY` mangler eller er lik nøkkelen i `.env.example`. Nøklene ligger som miljøvariabler hos Vercel, aldri i repoet.
- **Miljøvariablene** hos Vercel er `DJANGO_SECRET_KEY` (egen tilfeldig verdi for produksjon og forhåndsvisning), `MET_USER_AGENT`, og `DATABASE_URL` og `DATABASE_URL_UNPOOLED` (settes av Neon-integrasjonen). `ANTHROPIC_API_KEY` legges inn senere, bare i produksjon.

Lokal kjøring krever ingenting av dette: uten `DATABASE_URL` bruker appen SQLite, og du trenger verken Vercel, Neon, Vercel CLI eller Node. Regelen står i [AD-15 i arkitekturen](_bmad-output/planning-artifacts/architecture/architecture-G81-eriksen-2026-11-07/ARCHITECTURE-SPINE.md).

## Planlegging og prosess

Appen planlegges med [BMAD](https://github.com/bmad-code-org/BMAD-METHOD) og bygges med Claude Code.

**Planleggingsdokumenter**

- [Product brief (norsk)](docs/product-brief-your-next-adventure-no.md) og [engelsk versjon](docs/product-brief-your-next-adventure-en.md) (utdatert)
- [Tilbakemelding fra faglærer på product brief](docs/tilbakemelding-product-brief.md) og [endringsplanen etter tilbakemeldingen](notater/endringsplan-product-brief.md)
- [Teknisk research om turdata i Oslomarka](_bmad-output/planning-artifacts/research/technical-turdata-oslomarka-2026-10-29/research.md)
- [PRD](_bmad-output/planning-artifacts/prds/prd-G81-eriksen-2026-10-29/prd.md), med [addendum](_bmad-output/planning-artifacts/prds/prd-G81-eriksen-2026-10-29/addendum.md) og [verifisering av graderingsreglene](_bmad-output/planning-artifacts/prds/prd-G81-eriksen-2026-10-29/research-gradering.md)
- UX: [EXPERIENCE.md](_bmad-output/planning-artifacts/ux-designs/ux-G81-eriksen-2026-11-06/EXPERIENCE.md) (flyt og mikrotekst), [DESIGN.md](_bmad-output/planning-artifacts/ux-designs/ux-G81-eriksen-2026-11-06/DESIGN.md) (visuelt uttrykk), wireframes som SVG ([informasjonsarkitektur](_bmad-output/planning-artifacts/ux-designs/ux-G81-eriksen-2026-11-06/wireframes/ia-2026-11-06.svg) og [Olas flyt med kanttilstander](_bmad-output/planning-artifacts/ux-designs/ux-G81-eriksen-2026-11-06/wireframes/flow-ola-2026-11-06.svg), kildefiler i [Excalidraw](_bmad-output/planning-artifacts/ux-designs/ux-G81-eriksen-2026-11-06/wireframes/)) og [mockups](_bmad-output/planning-artifacts/ux-designs/ux-G81-eriksen-2026-11-06/mockups/)
- Arkitektur: [forklaring for sensor](docs/arkitektur.md), [ARCHITECTURE-SPINE.md](_bmad-output/planning-artifacts/architecture/architecture-G81-eriksen-2026-11-07/ARCHITECTURE-SPINE.md) (bindende beslutninger AD-1 til AD-15) og [beslutningsloggen](_bmad-output/planning-artifacts/architecture/architecture-G81-eriksen-2026-11-07/.memlog.md)
- [Epics og stories](_bmad-output/planning-artifacts/epics.md): 6 epics og 41 stories med akseptansekriterier, dekningskart for alle krav og byggerekkefølge

**Prosessdokumentasjon**

- [`.logs/hannah-eriksen/`](.logs/hannah-eriksen/): én logg per KI-økt, med oppgave, plan, resultat og åpne punkter. Nyeste logg ligger øverst.
- [`issues.md`](.logs/hannah-eriksen/issues.md): samlet liste over åpne punkter.
- Gjennomgangene (reviews) av hvert planleggingsdokument ligger ved siden av dokumentet i `_bmad-output/`.
- Etter første utkast av product brief er hver endring gjort på en egen gren og slått sammen med en pull request.

## Mappestruktur

```text
G81-eriksen/
  README.md
  CLAUDE.md              instruksjoner til Claude Code
  docs/                  product brief, tilbakemelding og arkitekturforklaring
  notater/               egne arbeidsnotater
  _bmad-output/          BMAD-dokumenter: research, PRD, UX og arkitektur, med gjennomganger
  _bmad/                 BMAD-rammeverket og konfigurasjonen
  .claude/skills/        BMAD-skills og egen sesjonslogg-skill for Claude Code
  .logs/                 logger fra KI-øktene og åpne punkter
```

**Stiler:** designtokens fra DESIGN.md ligger som CSS-variabler i `turforslag/static/css/tokens.css` (den eneste fila med fargeverdier), og grunnoppsett og felles komponenter i `turforslag/static/css/side.css`.

Mappene for selve appen (`config/`, `data/`, `tests/` med flere) kommer med implementeringen. Den planlagte strukturen står i [arkitekturen](docs/arkitektur.md).

## Medlemmer

- Hannah Eriksen
