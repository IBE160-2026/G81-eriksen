---
title: '6.8 del 1: README, rotmappe og kutt-føring'
type: 'chore'
created: '2026-11-28'
status: 'done'
baseline_commit: '5ad2c2a2e35d5c50fee701a05f9006c20db905eb'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/planning-artifacts/epics.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** README er utdatert (sier «neste er epic 2»), har ingen P2-status, mangler lenker til docs fra 6.5–6.7 og har feil mappeoversikt. PRD §9 og endringsloggen har ingen kutt-føring (AR-22), og kuttede stories er ikke merket i epics.md. Sensor kan ikke se hva som er levert.

**Approach:** Oppdater README til å stemme med repoet (AR-20, AD-12 pkt 6, AR-22), før P2-status i PRD §9 + endringslogg + epics.md, og rett rotmappen mot Structural Seed. Resten av 6.8 (rent miljø, historikksjekk, commit-ID-kontroll, nettlesertest) er utsatt i deferred-work.md.

## Boundaries & Constraints

**Always:** Norsk. Tall og påstander i README kontrolleres mot repoet (15 turer, antall stories, sprint-status). Begge kommandovarianter (Windows og macOS/Linux) beholdes. Alle lokale lenker virker. Testbrukeren og søket fra README (FR-21) står i README.

**Beslutning (Hannah 2026-11-28):** Alle P2-stories skal fortsatt gjennomføres. Ingen story føres som kuttet nå; README viser dem som «planlagt» i kuttrekkefølgen fra PRD §7.1. PRD §9 og endringsloggen får kutt-føring først når en story faktisk droppes, men README forklarer rekkefølgen og at status oppdateres underveis.

**Never:** Ingen endring i appkode, maler eller tester. Ikke endre `<frozen>`-blokker i andre spec-filer. Ikke commit `.claude/skills/refleksjonsnotat/`. Ikke påstå at rent-miljø-testen, nettlesertesten eller historikksjekken er gjort. Ikke lag filene docs/ for del 2–4.

</frozen-after-approval>

## Code Map

- `README.md` -- statusrad l. 29 og «Hva appen kan nå» utdatert; mangler P2-status, lenker til `docs/kartfarger.md`, `docs/brukertest-testplan.md`, `docs/skjermbilder/`, `docs/ki-testplan.md`; mappeoversikt ca. l. 105–130 har utdatert «Tjenester … epic 4 og 5», mangler `.env.example`, `pyproject.toml`, `vercel.json`, `requirements*.txt`, `CLAUDE.md`, `.gitattributes`; `docs/` er beskrevet for smalt.
- `_bmad-output/planning-artifacts/prds/prd-G81-eriksen-2026-10-29/prd.md` -- §9 (l. ~503–541) og endringslogg (l. ~554, siste rad v1.14): legg til kuttføring med årsak (§7.1 krever det) og ny rad.
- `_bmad-output/planning-artifacts/epics.md` -- P2-overskrifter l. 1234, 1569, 1613, 1689, 1740, 1815, 1893, 1961, 2013, 2063: legg til merking for kuttede stories. 
- `_bmad-output/implementation-artifacts/sprint-status.yaml` -- kilde for status (last_updated 11-27); ikke endre statusverdier.
- `tests/test_kildetre.py` -- sjekker mapper og installasjonsfiler mot spinen; kjør, ikke endre.
- `ARCHITECTURE-SPINE.md` (Structural Seed l. 244–269) -- `tjenester/` har i tillegg `models.py`, `apps.py`, `migrations/`; forklares i README (ikke endre spinen).

## Tasks & Acceptance

**Execution:**
- [x] `README.md` -- oppdater status (epic 1–4 og 6.5/6.7 ferdig, 4.6/4.7 og 5.x ikke), «Hva appen kan nå» (konto, personalisering og KI-begrunnelse levert; vær ikke), legg inn P2-tabell (levert/planlagt) med lenke til PRD §9, antall turer (15), lenker til docs for 6.5–6.7 -- AR-22
- [x] `README.md` -- rett mappeoversikten til å stemme med `git ls-files` og mapper, inkl. rotfiler og at `tjenester/` har modeller/migrasjoner -- AR-20
- [x] `README.md` -- legg ett samlet «prøv dette»-søk (FR-21) nær toppen, uten å fjerne README-søkene i resten av teksten
- [x] `prd.md` -- ny endringsloggrad (v1.15, 2026-11-28): ingen kutt ført, alle P2 planlagt, kuttrekkefølge uendret (§7.1) -- AR-22
- [x] `epics.md` -- ingen kutt-merking nå; legg til én linje under P2-stories om at kuttføring skjer i PRD §9 når en story droppes
- [x] `_bmad-output/implementation-artifacts/deferred-work.md` -- allerede oppdatert (del 2–4); committes

**Acceptance Criteria:**
- Given README, when den leses, then status, P2-tabell, antall turer og docs-lenker stemmer med sprint-status og `docs/`, og alle lokale lenker finnes på disk.
- Given mappeoversikten, when den sammenlignes med `git ls-files` og rotmappen, then hver sporet rotfil og mappe står der, og ingen mappe står der som ikke finnes.
- Given PRD §9, endringsloggen og epics.md, when de sammenlignes med README, then samme P2-status står i README, endringslogg v1.15 og epics.md (levert: 3.5; planlagt: resten). PRD §9 endres først når en story faktisk kuttes.
- Given repoet, then `venv/Scripts/python.exe manage.py test` og `ruff check .` består uendret.

## Implementation Notes

## Spec Change Log

## Review Triage Log

| Funn | Verdikt | Evidens |
|---|---|---|
| Spec sier PRD §9, diff rører ikke §9 | medium → patch | Beslutning overstyrer Approach; AC i spec og README-tekst justert (§9 først ved faktisk kutt) |
| Testbrukeren-lenke peker på hele seksjonen | low → patch | Tekst endret til «avsnittet Testbrukeren under Installasjon og kjøring» |
| Status «6.8 pågår» blir utdatert | low → patch | Omformulert til «delvis gjort, se sprint-status» |
| Tur 16–30 og 6.6–6.8 mangler forklaring | low → patch | Notat under P2-tabellen |
| Merknad i epics.md står etter 3.4 | low → patch | Flyttet til Epic-liste |
| Mangler begrensninger i README | medium → patch | «Kjente begrensninger» lagt til |
| source_spec: none i deferred-work | low → patch | Pekt på denne spec-en |
| «Nøklevann rundt» først er ikke testet | low → false | Setningen er flyttet uendret fra tidligere README (story 3.2/3.4), test dekker setningen |
| Ingen automatisk test for lenker/status | medium → defer | Lagt i deferred-work.md |
| ARCHITECTURE-SPINE.md mangler i rot | false | Ikke sporet i rot (git ls-files) |
| Rot-trær viser ikke ignorerte filer | false | Ignorerte filer er ikke i repoet sensor kloner |
| Kutt 3 (illustrasjon) kalt kjernekrav; «Planlagt» uklart; sprint-status-klokkeslett | low → avvist | Ingen konkret skade; ordlyd følger PRD §7.1 |

## Verification

**Commands:**
- `venv/Scripts/python.exe manage.py test tests.test_kildetre` -- expected: OK
- `venv/Scripts/python.exe -m ruff check . && venv/Scripts/python.exe -m ruff format --check .` -- expected: All checks passed
- lenkesjekk: alle `](lokal-sti)` i README.md finnes på disk -- expected: ingen manglende
