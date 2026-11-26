# Sprint Change Proposal: varighet 1–12 t og melding ved topptur-erstatning

- **Dato:** 2026-11-26
- **Utløst av:** Story 1.8, party-runden 2026-11-26 (beslutning 2A, 4B og 5A i [spec 1.8](../implementation-artifacts/spec-1-8-systemet-velger-og-rangerer-turer-som-passer-soket.md))
- **Modus:** inkrementell. Alle tre forslagene er godkjent av Hannah.
- **Omfang:** liten. Bare tekst i planleggings- og UX-dokumentene endres, og koden er allerede riktig.

## 1. Problemet

To beslutninger i Story 1.8 gjør at dokumentene ikke lenger stemmer:

1. **Maks varighet på 8 t stenger ute de lengste turene.** `nordmarksrunden` (svart, 580 min) og `grorud-grefsenkollen` (rød, 575 min) kan aldri foreslås når varigheten er høyst 480 min. Da gir kravet i FR-1 om minst én svart tur ingen mening for Ola. Hannah valgte 12 t (720 min), med halvtimessteg (beslutning 4B).
2. **Meldingen ved topptur-erstatning oppgir feil grunn.** Erstatningen med utsiktstur gjelder nå uansett hvorfor ingen topptur passer: tid, startpunkt eller nivåtak (beslutning 2A). Teksten «Toppturer krever mer tid enn du har oppgitt» er derfor ikke alltid sann.

Mary oppdaget i party-runden at de lengste turene aldri kunne vises. Amelia viste at ingen av statuskantene slår inn med dagens 15 turer og grønt tak. De betyr noe først når nivåtaket blir høyere for innloggede brukere (Epic 3), og når flere turer kommer i story 6.2.

**Bevis:**
- `data/turer.geojson`: 580 og 575 min.
- `domene/sok.py`: `MAKS_VARIGHET_MIN = 720`, merget i PR #31.

## 2. Konsekvenser

- **Epics:** Epic 1 fullføres som planlagt. Teksten i Story 1.9 (valglista for Varighet) og Story 1.12 (meldingen, grensen for endringsforslag og testene) endres. Ingen epic kommer til, forsvinner eller bytter rekkefølge, og `sprint-status.yaml` endres ikke.
- **PRD:** FR-4 (varighet), FR-8 (topptur) og kanttilfellet i UJ-1. MVP-en er uendret.
- **Arkitektur:** ingen endring. Spinen nevner verken varigheten eller meldingsteksten.
- **UX:** Mikrotekst og søkeskjemaet i EXPERIENCE.md, wireframen `flow-ola` (.svg og .excalidraw) og mockupen `key-sok.html`.
- **Teknisk:** ingen. `domene/sok.py` og `domene/utvalg.py` følger allerede beslutningene.

## 3. Anbefalt vei

**Direkte justering (alternativ 1):** teksten oppdateres i de gjeldende dokumentene.
- Innsats: lav. Risiko: lav. Ingen forsinkelse.
- Rulle tilbake og gjennomgå MVP-en er ikke aktuelt.

## 4. Endringene

### Forslag 1: ny melding når topptur blir erstattet (godkjent)

Den nye teksten er **«Ingen topptur passer søket ditt»**. Merket «Utsikt i stedet for topptur» beholdes, og meldingen lover ikke lengre eller hardere turer (SM-C1).

| Dokument | Sted | Gammelt | Nytt |
|---|---|---|---|
| PRD | FR-8 (:211) | «**Ingen topptur passer varigheten:** … en melding om at toppturer krever mer tid enn brukeren har oppgitt» | «**Ingen topptur passer søket:** Gjelder uansett grunn (tid, startpunkt eller nivåtak). Systemet viser en utsiktstur som passer søket og en melding om at ingen topptur passer søket …» |
| PRD | UJ-1, kanttilfelle (:60) | «… en melding om at toppturer krever mer tid enn han har oppgitt» | «… en melding om at ingen topptur passer søket hans» |
| epics.md | FR-8 (:40) | «Passer ingen topptur varigheten, vises en utsiktstur og en melding om at toppturer krever mer tid» | «Passer ingen topptur søket (tid, startpunkt eller nivåtak), vises en utsiktstur og en melding om at ingen topptur passer søket» |
| epics.md | Story 1.12 (:760) | Melding «Toppturer krever mer tid enn du har oppgitt» | Melding «Ingen topptur passer søket ditt» |
| EXPERIENCE.md | Mikrotekst (:131) | «Toppturer krever mer tid enn du har oppgitt» (PRD-budskap) | «Ingen topptur passer søket ditt» (beslutning 2026-11-26, Story 1.8) |
| EXPERIENCE.md | UJ-kanttilfelle (:391) | meldingen «Toppturer krever mer tid enn du har oppgitt» | meldingen «Ingen topptur passer søket ditt» |
| Wireframe `flow-ola` | .svg :508 og :527, .excalidraw | meldingen og notatet «passer varigheten» | ny melding og «passer søket» |
| epic-1-context.md | :27 | `TOPPTUR_ERSTATTET` uten grunn | «uansett grunn» og den nye meldingen |

### Forslag 2: varighet fra 1 til 12 timer (godkjent)

| Dokument | Sted | Gammelt | Nytt |
|---|---|---|---|
| PRD | §9 og endringsloggen | — | ny rad i §9 (avvik under implementeringen) og versjon 1.14 i endringsloggen, slik PRD-en krever i §0 |
| PRD | FR-4-tabellen (:157) | «fra 1 til 8 timer, i halvtimessteg» | «fra 1 til 12 timer, i halvtimessteg (endret 2026-11-26, Story 1.8 …)» |
| epics.md | FR-4 (:32) | «1–8 t i halvtimessteg» | «1–12 t i halvtimessteg» |
| epics.md | Story 1.9 (:620) | «1–8 t i halvtimessteg» | «1–12 t i halvtimessteg» |
| epics.md | Story 1.12 (:765) | «Ved 8 t blir det ikke noe forslag.» | «Ved 12 t blir det ikke noe forslag.» |
| epics.md | Story 1.12 (:787) | «også halvtimer, 8 t, …» | «også halvtimer, 12 t, …» |
| EXPERIENCE.md | Hjelpetekst (:102) og søkeskjema (:224) | «1–8 timer» og «1–8 t» | «1–12 timer» og «1–12 t» |
| Wireframe `flow-ola` | .svg :27, .excalidraw | «1–8 timer» | «1–12 timer» |
| Mockup `key-sok.html` | :121 og :205 | «1–8 timer» | «1–12 timer» |
| epic-1-context.md | :54 | «1–8 t i halvtimessteg» | «1–12 t i halvtimessteg» |

### Forslag 3: historiske dokumenter (godkjent, ikke endret)

Disse filene er øyeblikksbilder av tidligere arbeid. De beholder «1–8 t» og den gamle meldingen med vilje:
- `ux-designs/.../mockups/direction-stille-kart.html` og `direction-turkort.html`, som ble brukt til å velge visuell retning;
- `ux-designs/.../reconcile-prd.md` og `extract-prd.md`;
- `prds/.../review-rubric.md`, `review-prose.md` og `reconcile-ux.md`;
- `sprint-change-proposal-2026-11-22.md` (:474);
- kopiene i `ux-designs/.../.working/`.

**Ikke en del av denne endringen (andre budskap):**
- «Vi fant ingen tur som passer søket ditt» (ingen treff);
- «Ingen grønne turer passer søket» (nivåtak);
- «Du har sett alle turene som passer søket» (FR-7);
- merket «Utsikt i stedet for topptur».

## Gjennomført

Hannah godkjente forslaget 2026-11-26, og tekstendringene er gjort på `planlegging/correct-course-varighet`. Ingen gjeldende dokumenter sier lenger «1–8 t» eller «krever mer tid» (sjekket med grep). Excalidraw-fila er fortsatt gyldig JSON.

## 5. Overlevering

- **Omfang:** liten. Utvikleren gjør tekstendringene direkte på branchen `planlegging/correct-course-varighet`, og de merges med en PR før Story 1.9.
- **Ferdig når:**
  - ingen gjeldende dokument (PRD-en, epics.md, EXPERIENCE.md, `flow-ola` .svg og .excalidraw, `key-sok.html` og `epic-1-context.md`) sier «1–8 t» eller «krever mer tid»;
  - .svg og .excalidraw for `flow-ola` har samme tekst;
  - Story 1.9 bygger valglista med 23 valg (60–720 min) fra konstantene i `domene/sok.py`.
