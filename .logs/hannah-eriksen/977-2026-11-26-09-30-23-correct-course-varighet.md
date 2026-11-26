# Correct course: varighet 1–12 t og melding ved topptur-erstatning

## 2026-11-26 kl. 09:30 — Hannah Eriksen

### Oppgave
Hannah ba om å starte neste steg etter Story 1.8. Det var `bmad-correct-course`, som hun bestemte i 5A, for å oppdatere planleggingsdokumentene før Story 1.9.

### Plan
- `bmad-correct-course` i inkrementell modus på `planlegging/correct-course-varighet`.
- En subagent fant alle stedene med «1–8 t» og den gamle meldingen.
- Hannah godkjente tre forslag:
  1. ny melding, «Ingen topptur passer søket ditt»;
  2. varighet 1–12 t;
  3. historiske filer står urørt.
- [`sprint-change-proposal-2026-11-26.md`](../../_bmad-output/planning-artifacts/sprint-change-proposal-2026-11-26.md)

### Resultat
- **Commit:** `2684f1c`
- **PR:** [#32](https://github.com/IBE160-2026/G81-eriksen/pull/32). Den har også statuscommiten for 1.8 (`3b69714`) og loggen (`a4955a5`).
- **Endret:**
  - PRD-en til v1.14: FR-4, FR-8, UJ-1, §9 og endringsloggen;
  - epics.md: FR-4, FR-8, Story 1.9 og 1.12;
  - EXPERIENCE.md;
  - wireframen `flow-ola` (.svg og .excalidraw), `key-sok.html` og `epic-1-context.md`.
- **Kontroll:** grep gir ingen treff på den gamle teksten i de gjeldende dokumentene, og .excalidraw er gyldig JSON. Ingen kode er endret, fordi `domene/sok.py` allerede har 720 min.
- **Omfang:** lite (direkte justering). `sprint-status.yaml` er uendret.

### Åpne punkter
- Merge PR #32 før Story 1.9. Neste er `bmad-build` for Story 1.9: Ola søker og får ett turforslag. Valglista får 23 valg (60–720 min) fra konstantene i `domene/sok.py`.
