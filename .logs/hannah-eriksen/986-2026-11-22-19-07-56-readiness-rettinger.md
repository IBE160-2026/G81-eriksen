# Readiness-rettinger

## 2026-11-22 kl. 19:07 — Hannah Eriksen

### Oppgave
Hannah ba om å starte implementeringen av Epic 1. Readiness-sjekken i sprint planning ga CONCERNS, og Hannah valgte å rette planen før noe kode skrives.

### Plan
- `bmad-sprint-planning`: readiness gate (subagent) ga CONCERNS med 6 funn. Kompileringen av `epic-1-context.md` (subagent) fant 10 uklarheter til.
- Testet begge måtene å hente fra Turrutebasen på: WFS-en (`app:Fotrute`, `srsName=EPSG:4326`) gir WGS84 direkte, med `rutenummer` per segment. Nedlastings-API-et virker også, men gir UTM.
- `bmad-correct-course` i samlet modus: en subagent skrev endringsforslagene, og Hannah tok beslutningene.
- Plandokument: [`sprint-change-proposal-2026-11-22.md`](../../_bmad-output/planning-artifacts/sprint-change-proposal-2026-11-22.md), godkjent 2026-11-22.

### Resultat
- Hannahs beslutninger:
  - Rutelinjene hentes med WFS. `pyproj` og UTM-omregningen er fjernet.
  - `Startpunkt` er en egen modell, og `turtyper` er et `JSONField`.
  - `data/kurateringsliste.toml` og `data/testbruker.toml` leses med `tomllib`.
  - `requirements-dev.txt` med `ruff==0.17.4` erstatter `requirements-bygg.txt`.
  - Turillustrasjonen får en kildelinje på sider uten kart (story 6.1).
  - «Start fra første forslag igjen» er en POST-knapp.
- Andre rettinger:
  - `.env`-sjekken gjelder bare lokalt.
  - `foresla_endringer` er regelen for endringsforslag (story 1.12), og forslagene er POST-knapper.
  - Krediteringen lages på serveren, på kartet. MET-krediteringen er flyttet til story 5.3.
  - Mindre rettinger i FR-4, AD-3, AD-5 og `docs/arkitektur.md`.
- 82 endringer i 8 filer: epics, spinen, `EXPERIENCE.md`, `DESIGN.md`, PRD (nå v1.13), addendum, arkitektur-memlog og `docs/arkitektur.md`. Grep etter rester gir treff bare i historikk. Prøvekjøring av sprint-parseren: 6 epics og 41 stories.
- Commit `bea0db0` på `planlegging/readiness-rettinger`, pushet. PR #23: https://github.com/IBE160-2026/G81-eriksen/pull/23
- `_bmad-output/implementation-artifacts/epic-1-context.md` er ikke committet, og den er utdatert etter rettingene. `sprint-status.yaml` er ikke laget ennå.
- Lukket i `issues.md`: formatet på kurateringslista og testbrukerfila (TOML).

### Åpne punkter
- Etter merge av PR #23: lag `epic-1-context.md` på nytt, kjør sprint planning og start `bmad-build` for Story 1.1. Dette dekkes av det åpne punktet om sprint planning.
- Story 1.5: fastsett toleransen for å koble sammen WFS-segmenter, og verifiser `koordsys` for høyde-API-et med WGS84-punkter.
