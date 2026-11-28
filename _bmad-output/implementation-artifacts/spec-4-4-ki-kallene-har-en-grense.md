---
title: 'Story 4.4: KI-kallene har en grense per nettleser og per døgn'
type: 'feature'
created: '2026-11-27'
status: 'review'
baseline_commit: '5c9a1c51c46d6758bbfa42df66c972cec4996693'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-4-context.md'
  - '{project-root}/_bmad-output/implementation-artifacts/spec-4-3-forkastede-ki-svar-logges-uten-personopplysninger.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Uten tak kan KI-kall bli dyre, for eksempel ved misbruk eller feil. Overskredet tak skal ikke vise Ola noen feil (NFR-8, AD-10 punkt 9, FR-13).

**Approach:** En ren funksjon i `domene/` avgjør om et kall kan sendes. En `BegrensetKi`-omslag i `tjenester/ki/` sjekker, teller (økt og `KiForbruk`) og sender før kallet, og gir reservesvar når en grense er nådd. `hent_ki` pakker bare den ekte varianten. Ingen kobling til `sokflyt` (det gjør 4.5).

## Boundaries & Constraints

**Always:**
- Ren funksjon `kan_sende_ki(tidspunkter, antall_i_dag, na, maks_per_nettleser_time, maks_per_dogn) -> bool` i `domene/ki_grense.py` (bare standardbiblioteket). `tidspunkter` er `datetime` med tidssone. Teller bare de strengt nyere enn `na` minus 60 min (nøyaktig 60 min gammelt teller ikke). Kan sendes når antall siste time `<` per-nettleser-grensen og `antall_i_dag <` døgngrensen. Egen ren hjelper `behold_siste_time(tidspunkter, na)` gir de som teller.
- Settings: `KI_MAKS_PER_NETTLESER_TIME = 20`, `KI_MAKS_PER_DOGN = 200` (tester bruker `override_settings`).
- Modell `KiForbruk(dato DateField unique, antall PositiveIntegerField default=0, db_default=0)` i `tjenester/models.py`. `tjenester` er allerede i `INSTALLED_APPS`. Ny migrasjon `tjenester/migrations/0001_initial` (bare ny tabell, ingen RunSQL, virker på SQLite og Postgres).
- Døgnet er Europe/Oslo-kalenderdato fra `na` (`na.astimezone(ZoneInfo("Europe/Oslo")).date()`), så tellingen starter 00.00, også på dager med tidsskifte.
- Omslaget `BegrensetKi(indre, okt)` i `tjenester/ki/grense.py` følger `Ki`-grensesnittet. `okt` er et dict-lignende økt-objekt (`request.session`). Økt-nøkkel `"ki_kall"` er en liste ISO-tekster. Ved hvert kall: les defensivt (ugyldig innhold gir tom liste), fjern tidspunkter eldre enn 60 min, sjekk `kan_sende_ki` mot dagens `KiForbruk`-antall (0 uten rad). Tillatt: legg til tidspunktet, øk `KiForbruk` med `get_or_create` og `F("antall") + 1` i én `transaction.atomic`, så send til `indre`. Telling skjer før sending, så kall som forkastes eller går ut på tid teller.
- Nådd grense: `indre` får ikke kallet (falsk variant: `antall_kall` forblir 0), og omslaget gir `KiSvar(tekst=reserve)`, samme resultat som reservevarianten, uten egen feilmelding.
- Når kallet gjør at dagens antall blir lik `KI_MAKS_PER_DOGN`, skrives én linje til KI-loggen med tidspunkt og at totalgrensen er nådd (ny funksjon `logg_totalgrense_nadd()` i `tjenester/ki/logg.py`, linje `tidspunkt<TAB><TAB>totalgrense<TAB>`, ingen kalltype, søke-ID, e-post eller bruker-ID). Neste kall samme døgn gir ingen ny linje, neste døgn kan gi en.
- `hent_ki(tving_reserve=False, okt=None)`: reserve ved `tving_reserve` eller uten nøkkel (som før, reserve teller ikke). Med nøkkel: `BegrensetKi(EkteKi, okt)`. Uten `okt` med nøkkel gis reserve, så ingen ubegrenset ekte variant kan lages ved en glipp.
- Ny økt eller slettede informasjonskapsler gir tom `"ki_kall"`, men døgngrensen gjelder fortsatt.

**Never:**
- Ingen import av `turforslag/` i `tjenester/`. Ingen endring av `sokflyt`, visning, `Ki`-grensesnittet, `KiSok`/`KiTur`/`KiSvar` eller den ekte varianten. Reservevarianten teller ikke og sender ingenting. Ingen ny avhengighet.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| 19 siste time | 19 tidspunkter, døgn 0 | `True` | N/A |
| 20 siste time | 20 tidspunkter | `False` | N/A |
| Nøyaktig 60 min | 20 tidspunkter, ett er 60 min gammelt | `True` (det teller ikke) | N/A |
| 199 i dag | `antall_i_dag=199` | `True`, med 200 `False` (uansett nettleser) | N/A |
| Tidsskifte | `na` 2026-10-25 og 2026-03-29 (Oslo) | Dato er Oslo-kalenderdato, nullstilles 00.00 | N/A |
| To kall | Tom rad, to tillatte kall | Én rad, `antall == 2` | N/A |
| Grense nådd (falsk) | Senket grense | `FalskKi.antall_kall == 0`, svar er reserveteksten | N/A |
| Døgnets siste kall | Telleren blir lik grensen | Én logglinje; neste kall ingen ny | N/A |
| Skadet økt | `"ki_kall"` er tekst/søppel | Behandles som tom | Ingen unntak |
| Reserve | Uten nøkkel / uten `okt` | Ingen telling, ingen rad | N/A |

</frozen-after-approval>

## Code Map

- `domene/innlogging.py` (`er_sperret`) -- mønster for ren grensefunksjon med strengt-nyere-enn. Nytt: `domene/ki_grense.py`.
- `tests/domene/test_bare_standardbibliotek.py` -- nye domenefiler må bare bruke standardbiblioteket.
- `tjenester/ki/grensesnitt.py` (`hent_ki`, `Ki`), `ekte.py`, `reserve.py`, `falsk.py` (`antall_kall`) -- omslaget følger `Ki`.
- `tjenester/ki/logg.py` -- legg til `logg_totalgrense_nadd`, gjenbruk `_sikre_handler`, `lag_linje`-stil, OSError-fangst.
- `tjenester/apps.py` (finnes), `tjenester/models.py` og `tjenester/migrations/` -- nye. Mønster for `db_default`: `turforslag/migrations/0003_innloggingsforsok.py`.
- `config/settings.py` -- to nye innstillinger.
- `turforslag/sokflyt.py:172` -- eneste kallsted, `hent_ki(tving_reserve=True)`; ikke rør.
- `tests/tjenester/test_ki.py` -- har importgrensetest for `tjenester/` (AR-2) og hjelpere. Nye tester: `tests/domene/test_ki_grense.py`, `tests/tjenester/test_ki_grense.py` (`TestCase`).

## Tasks & Acceptance

**Execution:**
- [ ] `domene/ki_grense.py` -- `kan_sende_ki`, `behold_siste_time`
- [ ] `config/settings.py` -- `KI_MAKS_PER_NETTLESER_TIME`, `KI_MAKS_PER_DOGN`
- [ ] `tjenester/models.py` + migrasjon `0001_initial` -- `KiForbruk`
- [ ] `tjenester/ki/grense.py` -- `BegrensetKi`
- [ ] `tjenester/ki/logg.py` -- `logg_totalgrense_nadd`
- [ ] `tjenester/ki/grensesnitt.py` -- `hent_ki(..., okt=None)`
- [ ] tester -- hele matrisen, plus `makemigrations --check`, og at `tjenester/` ikke importerer `turforslag/` (AR-2, SM-2)

**Acceptance Criteria:**
- Given nøkkel og `okt`, when `hent_ki` kalles, then resultatet teller kall; uten nøkkel eller `okt` teller ingenting.
- Given `makemigrations --check`, when den kjøres, then ingen manglende migrasjoner.

## Implementation Notes

## Spec Change Log

## Review Triage Log

- Utenfor frozen-blokka: `tests/tjenester/test_ki.py` endret (`hent_ki` uten `okt` gir reserve; ekte variant er nå pakket i `BegrensetKi`), og `tests/web/test_registrering.py` endret (hardkodet søkedato i `KravOmKontoTest` var passert; bruker nå Oslo-dato i dag).
- Etter review lagt til (utenfor frozen-blokka): døgnreservasjonen er atomisk (`UPDATE ... WHERE antall < maks`), feil ved bruk av `KiForbruk` gir reservesvar (fail closed), og tidspunkter i fremtiden i økta forkastes.

## Verification

**Commands:**
- `venv/Scripts/python.exe manage.py test` -- expected: alle grønne
- `venv/Scripts/python.exe manage.py makemigrations --check --dry-run` -- expected: ingen endringer
- `venv/Scripts/python.exe -m ruff check . && venv/Scripts/python.exe -m ruff format --check .` -- expected: ingen funn
