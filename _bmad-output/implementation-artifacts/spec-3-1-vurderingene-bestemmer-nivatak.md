---
title: 'Story 3.1: Vurderingene bestemmer nivåtaket etter faste regler'
type: 'feature'
created: '2026-11-27'
status: 'done'
baseline_commit: '61b2e8d92912a781623f1b1f12a7ba5b23c04bb0'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-3-context.md'
  - '{project-root}/_bmad-output/planning-artifacts/prds/prd-G81-eriksen-2026-10-29/prd.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Forslagene har et fast nivåtak (grønt). Det finnes ingen regler som lar vurderingene til Ola heve eller sperre nivået (FR-18, FR-19, AD-11, AR-13).

**Approach:** Ny ren domenemodul `domene/niva.py` med `Registrering`, `Sperre`, `NivaStatus` (alle frosne dataklasser) og `vurder_historikk(registreringer)`. Den går gjennom registreringene sortert på (dato, id) og bruker reglene i FR-19. Ingen kobling til søk, database eller visning i denne storyen.

## Boundaries & Constraints

**Always:**
- Kun standardbiblioteket og `domene.tur.Turniva`/`NIVAREKKEFOLGE`. Ingen DB, nett eller klokke. Nivåer sammenlignes via posisjon i `NIVAREKKEFOLGE`, aldri med `<`.
- `Registrering(id, dato, tur_id, turniva, vanskelighet, fornoydhet)`; `Sperre(niva, turniva)` (sperrenivå og turnivået som ga sperren); `NivaStatus(nivatak, grunnniva, sperre, antall_hevinger, teller)`. `nivatak` = `sperre.niva` med aktiv sperre, ellers `grunnniva`.
- Regler per registrering, i rekkefølge (dato, id), startstatus grønt/grønt/ingen sperre/0/0:
  - Aktiv sperre + *lett* eller *moderat* (uansett turnivå): sperren oppheves. Telleren er uendret, `antall_hevinger` er uendret, registreringen teller ikke.
  - *Vanskelig*: telleren settes til 0. Kandidat = nivået under turnivået, aldri under grønt. Er kandidaten lavere enn nåværende nivåtak, settes `Sperre(kandidat, turnivå)` (erstatter en eksisterende, grunnnivået uendret). Ellers uendret (også eksisterende sperre).
  - Uten sperre + *lett* + turnivå lik grunnnivået + grunnnivå ikke svart: teller +1. Ved 3 heves grunnnivået ett nivå, `antall_hevinger` +1, teller 0.
  - *Moderat* uten sperre verken teller eller nullstiller. Turer under/over grunnnivået teller ikke. Samme tur flere ganger teller hver gang.
- Ukjent turnivå eller vanskelighet, eller fornøydhet utenfor 1–5: `ValueError` med norsk melding, ingen status. Valider alle før behandling.

**Never:**
- Ikke endre `domene/utvalg.py` (`er_over_nivatak`, `NIVATAK_UTEN_HISTORIKK`), `turforslag/`, modeller, migrasjoner, maler eller søkeflyt. Det er story 3.2.
- Ikke lagre telleren eller nivåtaket i databasen: status utledes alltid fra historikken.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Tom historikk | `[]` | grønt/grønt, ingen sperre, 0 hevinger, teller 0 | N/A |
| Heving (FR-19 #1, #12) | 3 *lette* på grunnnivået, evt. med *moderat* imellom | grunnnivå +1, hevinger 1, teller 0 | N/A |
| Sperre (#4, #7, #9) | *vanskelig* over grønt | `sperre` satt, grunnnivå uendret, teller 0 | N/A |
| Ingen sperre (#8) | *vanskelig* grønn tur ved nivåtak grønt | ingen sperre, teller 0 | N/A |
| Oppheving (#5) | *lett*/*moderat* med aktiv sperre | sperre `None`, nivåtak = grunnnivå, hevinger uendret | N/A |
| Svart (#11) | *lett* svart tur, grunnnivå svart | uendret | N/A |
| Rekkefølge | tilfeldig innsendt rekkefølge, tidlig dato inn sist | samme status som sortert; kan endre nivåtaket | N/A |
| Ugyldig input | ukjent turnivå/vanskelighet, fornøydhet 0 eller 6 | ingen status | `ValueError` (norsk) |

</frozen-after-approval>

## Code Map

- `domene/tur.py:25-34` -- `Turniva`, `NIVAREKKEFOLGE`: gjenbrukes, ikke endres.
- `domene/tekst.py:423-443` -- verdier for vanskelighet og fornøydhet 1–5 (`MIN_FORNOYDHET`/`MAKS_FORNOYDHET`): sjekk om de kan importeres uten å bryte domenets avhengigheter, ellers lokale konstanter.
- `domene/utvalg.py:20,47` -- nåværende faste tak. Urørt.
- `tests/domene/test_bare_standardbibliotek.py`, `tests/test_kildetre.py` -- sjekk at ny modul oppfyller reglene.
- `tests/domene/test_utvalg.py` -- stil og FR-referanser å følge.

## Tasks & Acceptance

**Execution:**
- [ ] `domene/niva.py` -- ny modul med dataklassene og `vurder_historikk` -- AD-11, AR-13
- [ ] `tests/domene/test_niva.py` -- 12 FR-19-eksempler som egne tester med nummer i navnet og FR-19-henvisning (Før bygges av registreringer og sjekkes først; #9 = 3 grønne + 3 blå *lette*), pluss tom historikk, rekkefølge, gjentakelse, ugyldig input -- SM-2, NFR-6
- [ ] `_bmad-output/implementation-artifacts/sprint-status.yaml` -- 3-1 til in-progress, så review -- sporing

**Acceptance Criteria:**
- Given historikk i vilkårlig rekkefølge, when `vurder_historikk` kalles, then resultatet er likt som for sortert rekkefølge (dato, id).
- Given testene i `tests/domene/`, when de kjøres, then bruker de ikke databasen og viser til FR-18 og FR-19.
- Given hele testsuiten og ruff, when de kjøres, then er alt grønt.

## Implementation Notes

- Nye filer: `domene/niva.py`, `tests/domene/test_niva.py`. Lokale konstanter for fornøydhet (1–5) for å unngå kobling til `tekst.py`. Tester kjøres med `manage.py test` (pytest er ikke installert); Verification-kommandoene i spec-en må leses slik.
- `fornoydhet` avvises også når den ikke er `int` (inkludert `bool`).
- FR-19 #11 kan ikke bygges med teller 2 (teller er alltid 0 på svart). Testen bygger grunnnivå svart og viser at tre nye lette svarte turer gir uendret status.

## Spec Change Log

## Review Triage Log

- patch (medium): `test_tidlig_dato_registrert_sist_kan_endre_nivataket` viste ikke at nivåtaket endres (etter == før). Testen er skrevet om: v alene gir grønt tak, med seks tidlige lette turer gir den sperre blått. Rettet.
- patch (low): `fornoydhet=True` og `3.5` var utestet. Lagt til i ugyldig-input-testen. Rettet.
- patch (low): villedende kommentarer i `test_samme_dato_avgjores_av_id`. Rettet.
- false: `"bla"` som ren streng slipper gjennom som `Turniva`. `Turniva` er StrEnum, så den er lik `Turniva.BLA` og sammenlignes riktig.
- false: `fornoydhet` brukes ikke i beregningen. Spec og epics krever feltet og valideringen (brukes av 3.3/3.5).
- false: ingen vurdering av oppheving + teller. Dekket av eksempel 5 og spec Design Notes.
- rejected low: duplikat-id, ugyldig `dato`/`id`/`None` gir `TypeError`. Id er primærnøkkel i DB og typene settes av én mapper i 3.2. Guard ville være ny kode for en uvist nådd tilstand.
- rejected low: lokale konstanter `MIN_FORNOYDHET`/`MAKS_FORNOYDHET` i stedet for import fra `tekst.py`. Bevisst for å unngå kobling. Driftrisiko er liten.
- rejected low: `VANSKELIGHETER` som strenger i stedet for enum, feilmelding uten id, ytterligere tester (kjeder av sperrer, mange registreringer). Ingen konkret skade vist.
- rejected: «ingen integrasjonspunkt», sprint-status uten `last_updated`. Bevisst ren domenestory, koblingen er story 3.2.

## Design Notes

Avklart ut fra PRD: opphevings-*lett* teller ikke (#5), og telleren røres ikke av oppheving (den er 0 fordi *vanskelig* nullstilte den). Ny *vanskelig* under aktiv sperre kan senke den videre (kandidat lavere enn sperrenivået); er den lik eller høyere (#6) er alt uendret, og `sperre.turniva` beholdes. Svart er aldri tellende, så telleren er alltid 0 på svart.

## Verification

**Commands:**
- `venv/Scripts/python.exe -m pytest tests/domene -q` -- expected: alle grønne
- `venv/Scripts/python.exe -m pytest -q` -- expected: alle grønne
- `venv/Scripts/python.exe -m ruff check .` -- expected: ingen funn
