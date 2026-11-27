---
title: 'Story 4.3: Forkastede KI-svar logges uten personopplysninger'
type: 'feature'
created: '2026-11-27'
status: 'done'
baseline_commit: 'd3e9237c407701db5778e982581a95855b2cca71'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-4-context.md'
  - '{project-root}/_bmad-output/implementation-artifacts/spec-4-2-systemet-sjekker-ki-teksten.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Hannah kan ikke forbedre prompten uten å se hvilke KI-svar som ble forkastet og hvorfor, men ingenting om brukerne kan lagres (FR-13, NFR-5, AD-10 punkt 8, AD-13).

**Approach:** Ny modul `tjenester/ki/logg.py` med funksjonen `logg_forkastet(kalltype, arsak, svar)`. Lokalt skrives én linje per forkastet svar til `logs/ki.log`, som roteres hver midnatt og ryddes etter 30 dager. På Vercel går linjen til standard ut. Funksjonen kobles ikke inn her (det gjør 4.5).

## Boundaries & Constraints

**Always:**
- Signatur `logg_forkastet(kalltype: str, arsak: str, svar: str | None)`. Ingen annen parameter. Kalltype er `tolking` eller `begrunnelse` (konstanter i `domene/ki.py`). Årsak er en av `KI_FEILARSAKER` eller en `Forkastelse`-verdi. Ukjent kalltype eller årsak gir `ValueError` (feilen vises tidlig, og fritekst kan ikke snike seg inn som årsak).
- Linjeformat, felt skilt med tab: `tidspunkt<TAB>kalltype<TAB>arsak<TAB>svar`. Tidspunkt er ISO 8601 i Europe/Oslo med sekunder og forskyvning (`2026-11-27T21:05:09+01:00`). `svar=None` gir tomt felt, ellers er svaret hele teksten uavkortet. Tegnene `\`, linjeskift (`\n`, `\r`, og andre Unicode-linjeskift), og tab escapes (`\\`, `\n`, `\r`, `\t`) så hver hendelse er nøyaktig én linje med fire felt.
- Logger: `logging.getLogger(__name__)` i `logg.py`. Funksjonen skriver med `INFO`.
- Lokalt (`VERCEL` ikke satt): fil `logs/ki.log` (mappen lages ved første skriving, ikke ved import eller testkjøring). `TimedRotatingFileHandler`-underklasse: `when="midnight"`, ingen `backupCount`, rotert fil heter `ki.log.<åååå-mm-dd>`, UTF-8. Handleren legges på loggeren første gang den trengs (lat), aldri to ganger.
- Opprydding: ren funksjon `filer_a_slette(filnavn, i_dag)` gir navnene som skal slettes: bare `ki.log.<dato>` med dato mer enn 30 dager før `i_dag` (nøyaktig 30 beholdes). Alle andre navn, også `ki.log` og `ki.log.ugyldig`, gir aldri sletting. Handleren kaller den ved oppstart og i `doRollover`, med dagens dato i Europe/Oslo.
- Vercel (`VERCEL` satt): samme linjeformat til standard ut, ingen fil og ingen mappe. Legg til `settings.VERCEL` (leses fra `MILJO.vercel`).
- README «Publisering på Vercel» sier at kjøreloggen slettes etter 1 time hos Vercel, så kvalitetssikring av KI-svar gjøres lokalt med `logs/ki.log`.

**Never:**
- Ingen søke-ID, e-post, bruker-ID, fritekst eller IP som parameter eller felt. Ingen kobling til `sokflyt`, visning, KI-kall eller grense (4.4–4.5). Ingen ny avhengighet, modell eller migrasjon. Ingen endring av `.gitignore` (dekker allerede `logs/` og `*.log`). Ikke slett filer utenfor `ki.log.<dato>`.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Forkastet tekst | `begrunnelse`, `siffer`, «Turen er 5 km.» | `2026-11-27T21:05:09+01:00⇥begrunnelse⇥siffer⇥Turen er 5 km.` | N/A |
| Tidsavbrudd | `tolking`, `tidsavbrudd`, `None` | Linje med tomt siste felt | N/A |
| Linjeskift og tab i svar | «a\nb\tc\\d» | Én linje, svar `a\nb\tc\\d` (escapet) | N/A |
| Ukjent kalltype/årsak | `fritekst`, `Ola@x.no` | Ingenting skrives | `ValueError` |
| Dato 30 dager gammel | `ki.log.2026-10-28`, i dag 2026-11-27 | Beholdes | N/A |
| 31 dager gammel | `ki.log.2026-10-27` | Slettes | N/A |
| Andre navn / ugyldig dato | `notater.txt`, `ki.log`, `ki.log.2026-13-45` | Aldri slettet | N/A |
| Vercel | `VERCEL` satt | Linje på stdout, `logs/` finnes ikke | N/A |

</frozen-after-approval>

## Code Map

- `domene/ki.py` -- `ARSAK_*`, `KI_FEILARSAKER`; legg til `KALLTYPE_TOLKING`, `KALLTYPE_BEGRUNNELSE`, `KALLTYPER`.
- `domene/ki_validering.py` -- `Forkastelse` (StrEnum), gyldige årsaker fra valideringen. «ugyldig» finnes i begge, og er én verdi.
- `tjenester/ki/logg.py` -- NY. `logg_forkastet`, `filer_a_slette`, handler-underklasse, formatering.
- `config/settings.py` -- legg til `VERCEL = MILJO.vercel`. `LOGGING` under `MILJO.vercel` er uendret (root INFO til stdout fanger loggeren).
- `README.md` -- avsnittet «Publisering på Vercel».
- `tests/tjenester/test_ki_logg.py` -- NY. Midlertidig mappe (`tmp_path`/`TemporaryDirectory`), faste datoer, ingen `logs/` i repoet.

## Tasks & Acceptance

**Execution:**
- [ ] `domene/ki.py` -- kalltype-konstanter -- delt av logg og 4.5
- [ ] `tjenester/ki/logg.py` -- funksjon, format, handler, opprydding -- AC under
- [ ] `config/settings.py` -- `VERCEL` -- velger stdout mot fil
- [ ] `README.md` -- Vercel-logg slettes etter 1 t -- NFR-5
- [ ] `tests/tjenester/test_ki_logg.py` -- format, escape, tom svar, avvisning, rotasjon (navn `ki.log.<dato>`, ingen `backupCount`), opprydding med faste datoer og en pause på flere uker, andre filer urørt, stdout på Vercel uten fil, ingen personfelt i signaturen (FR-13, NFR-5)

**Acceptance Criteria:**
- Given `logg_forkastet`, when signaturen inspiseres, then den har bare `kalltype`, `arsak` og `svar`.
- Given lokal kjøring, when en linje logges, then `logs/ki.log` finnes med nøyaktig én linje, og importen alene lager ingen mappe.
- Given `VERCEL`, when en linje logges, then den står på standard ut og ingen fil eller mappe er laget.
- Given appen starter etter flere ukers pause, when handleren opprettes, then rotert fil eldre enn 30 dager er slettet.

## Implementation Notes

## Spec Change Log

## Review Triage Log

| Funn | Verdict | Rute | Evidens |
|------|---------|------|---------|
| Vercel-linjer kan droppes (logger-nivå) | false | avvist | `LOGGING` under Vercel setter root INFO, loggeren arver. Test utvidet med `propagate`. |
| OSError velter kallet | medium | patch | mkdir/handler/iterdir uten fangst. Fikset. |
| `logs/` ikke i .gitignore | false | avvist | `.gitignore` har `logs/` (linje 43). |
| doRollover/rydd utestet | medium | patch | Fjerning av `rydd()` ga grønne tester. Test lagt til. |
| Svar kan inneholde personopplysninger, ubegrenset | low | avvist | Spec: svaret logges uavkortet; ingen søkedata sendes til KI. |
| Andre kontrolltegn ikke escapet; surrogater | low | avvist | Utenfor spec; logging fanger kodefeil i handleError. |
| Rotasjon i lokal tid vs Oslo | low | avvist | Ingen fil på Vercel; lokalt er tidssonen Oslo. |
| Handler ikke trådsikker | low | patch | Direkte rettelse med lås. |
| Flerprosess-rotasjon | low | avvist | Ikke et reelt scenario lokalt. |
| README mangler detaljer; ingen kaller | low | avvist | Kobling er 4.5 (spec Never). |
| Uhashbar årsak gir TypeError | low | avvist | Utenfor reell bruk. |

## Verification

**Commands:**
- `venv/Scripts/python.exe -m pytest tests -q` -- expected: alle grønne
- `venv/Scripts/python.exe -m ruff check . && venv/Scripts/python.exe -m ruff format --check .` -- expected: ingen funn
