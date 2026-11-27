---
title: 'Story 4.1: KI-tjenesten har ett grensesnitt med tre varianter'
type: 'feature'
created: '2026-11-27'
status: 'done'
baseline_commit: 'cb57e2165c7b5f503d4a51373d2fb438cee5cf60'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-4-context.md'
  - '{project-root}/_bmad-output/planning-artifacts/architecture/architecture-G81-eriksen-2026-11-07/ARCHITECTURE-SPINE.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Appen har ingen felles inngang til KI. Uten den kan ikke Epic 4 bygge validering, logg og grense (4.2–4.4) eller la KI skrive begrunnelsen (4.5), og testene ville trenge nett og nøkkel (FR-13, NFR-5, AD-10, AD-13, AR-12, AR-15, AR-16).

**Approach:** Ny pakke `tjenester/ki/` med ett grensesnitt for kall B (begrunnelse) og tre varianter: ekte (Anthropic), reserve og falsk. Valget av variant ligger i grensesnittet, og nøkkelen leses fra `settings.ANTHROPIC_API_KEY`. Turforslaget ber til 4.5 alltid om reservevarianten, så brukeren ser ingen endring og den publiserte siden sender ingen KI-kall.

## Boundaries & Constraints

**Always:**
- Frosne dataklasser i `domene/` (bare standardbiblioteket) for inndata: `KiSok` (`varighet_min`, `dato`, `turtype`, `startpunkt_id`) og `KiTur` (`id`, `navn`, `turtyper`, `form`), ingen andre felt (ingen e-post, bruker-ID, historikk, fritekst). Et feilresultat/svar som aldri kaster: tekst, og ved feil årsaken `tidsavbrudd`, `feil` eller `ugyldig`. En test sammenligner feltene med en fast liste (NFR-5).
- Kall B har signaturen `begrunnelse(sok: KiSok, tur: KiTur, reserve: str)`: `reserve` er ferdig reservetekst fra `reservebegrunnelse`. Reservevarianten gir `reserve` uendret tilbake (samme tekst som i dag). `turforslag/sokflyt.py` legger personaliserings- og preferansesetningene til som i dag. KI-merket er «Begrunnelse fra mal». Ingen kall A (tolking, fritekst) nå.
- Valg av variant: `hent_ki(tving_reserve=...)` i `tjenester/ki/`. Mangler `ANTHROPIC_API_KEY`, er tom eller bare mellomrom (`strip()`), brukes reserve og ingen Anthropic-klient lages. Turforslaget kaller med `tving_reserve=True` (kommentar: til story 4.5), også når nøkkel finnes.
- Ekte variant: `anthropic` 2.6.0 (finnes i `pyproject.toml`), modell `claude-haiku-5-5`, `timeout=5.0`, `max_retries=0`, `output_config={"effort": "low"}`, ingen sampling-parametere, ingen prefill, `max_tokens` satt. Bare her importeres `anthropic`. Tidsavbrudd, tilkoblingsfeil, feilstatus (401, 429, 529 …) og svar uten tekst gir feilresultat (`tidsavbrudd`, `feil`, `feil`, `ugyldig`), aldri unntak mot viewet. Prompten er enkel og foreløpig, forfines i 4.5.
- Falsk variant for tester: bestemmer svaret (også tomt, tidsavbrudd og feil), og lar testen lese inndata og antall kall (AR-15). Testene for den ekte varianten bruker `httpx2.Client(transport=httpx2.MockTransport(...))` (anthropic 2.6.0 bruker `httpx2`, ikke `httpx`), uten nettverk (AD-13).
- Importregler: `tjenester/` importerer bare `domene/` og Django, aldri `turforslag/`. `turforslag/` og views kaller bare grensesnittet. Nøkkelen leses bare i `config/settings.py`.

**Never:**
- Ingen nøkkel i repoet, ingen ekte KI-kall i tester, bygg eller på publisert side. Ingen validering, logg eller grense (4.2–4.4), ingen endring av brukerens visning, ingen migrasjon, ingen ny avhengighet.
- Ikke send `Tur`/`Sok`/`Soketilstand` til KI, bare `KiSok`/`KiTur`.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Ingen nøkkel | mangler, `""` eller `"   "` | reservevariant, ingen klient | N/A |
| Nøkkel og `tving_reserve=True` | nøkkel satt | reservevariant, ingen klient | N/A |
| Nøkkel, ekte variant | gyldig svar fra falsk transport | teksten fra modellen | N/A |
| Tidsavbrudd | transport kaster timeout | feilresultat `tidsavbrudd` | kaster aldri |
| Feilstatus | 401, 429, 529, tilkobling | feilresultat `feil` | kaster aldri |
| Svar uten tekst | 200 uten tekstblokk | feilresultat `ugyldig` | kaster aldri |
| Turforslag i dag | nøkkel finnes eller ei | samme tekst som før, «Begrunnelse fra mal» | N/A |
| Dataklasser | KI-inndata | har bare de oppgitte feltene | test feiler ved nytt felt |

</frozen-after-approval>

## Code Map

- `tjenester/` (har `__init__.py`, `apps.py`, står i `INSTALLED_APPS`): ny pakke `tjenester/ki/` (grensesnitt/valg, `ekte`, `reserve`, `falsk`).
- `domene/` -- ny modul for `KiSok`, `KiTur`, resultat (bare stdlib, `tests/domene/test_bare_standardbibliotek.py`).
- `config/settings.py:22` -- `ANTHROPIC_API_KEY = MILJO.anthropic_api_key` finnes. `config/miljo.py` stripper ikke, så `hent_ki` stripper selv.
- `turforslag/sokflyt.py` `forslagsvisning` (l.~165–178) -- erstatter direkte `reservebegrunnelse`-bruk med kall til grensesnittet (reserve), personaliseringssetninger som før.
- `domene/begrunnelse.py` -- `reservebegrunnelse` (urørt). `domene/sok.py` `Sok`, `domene/tur.py` `Tur` (19 felt, urørt).
- `tests/tjenester/` (bare `__init__.py`), `tests/test_kildetre.py` (`anthropic==2.6.0` i requirements), `tests/web/test_forslag.py`/`test_registrering.py` (skal bestå uendret).
- Nye tester: `tests/tjenester/` for valg av variant, klientinnstillinger (`timeout=5.0`, `max_retries=0`, modell, `effort`), hver feiltype, AST-test av at `anthropic` bare importeres i den ekte varianten, og at `tjenester/` ikke importerer `turforslag/`; `tests/domene/` for dataklassenes felt. Viser til FR-13 og NFR-5.

## Tasks & Acceptance

**Execution:**
- [ ] `domene/` -- `KiSok`, `KiTur`, resultat -- NFR-5, AD-10
- [ ] `tjenester/ki/` -- grensesnitt, `hent_ki`, ekte/reserve/falsk -- AR-12, AR-15, AR-16
- [ ] `turforslag/sokflyt.py` -- kall grensesnittet med `tving_reserve=True` -- FR-13
- [ ] Tester i `tests/tjenester/` og `tests/domene/` for matriserader og AC, ingen nettverkskall -- SM-2, AD-13

**Acceptance Criteria:**
- Given turforslag etter denne storyen, when de vises, then er teksten og «Begrunnelse fra mal» uendret, og testene fra Epic 1–3 består uendret.
- Given hele testsuiten og ruff, when de kjøres, then er alt grønt uten nett og uten nøkkel.

## Implementation Notes

- Nye filer: `domene/ki.py`, `tjenester/ki/` (`grensesnitt`, `ekte`, `reserve`, `falsk`), `tests/domene/test_ki.py`, `tests/tjenester/test_ki.py`, `tests/web/test_ki_forslag.py`. Endret: `turforslag/sokflyt.py`. Spec-ens frontmatter pekte på feil sti til ARCHITECTURE-SPINE (rettet). Den ekte varianten er bare testet mot falsk transport, aldri mot det ekte API-et.

## Spec Change Log

## Review Triage Log

- patch (medium): ingen test låste at `forslagsvisning` ber om reserve (`tving_reserve=True`) selv med nøkkel. Lagt til `tests/web/test_ki_forslag.py` (kallet, teksten og `KiSok`/`KiTur`). Rettet.
- patch (low): `sokflyt` brukte `.tekst` uten å sjekke `ok`, så en KI-feil kunne gi tom begrunnelse i 4.5. Bruker nå reserveteksten ved feil eller tom tekst, med test. Rettet.
- patch (low): `hent_ki` kunne kaste ved opprettelse av klienten. Faller nå tilbake til `ReserveKi`, med test. Rettet.
- patch (low): personvern (NFR-5) var bare testet på feltnavn. Ny test av forespørselskroppen til `EkteKi`: turnavn, turtype, form og varighet, ikke «@», «bruker», «nivåtak» eller reserveteksten. Rettet.
- false: `httpx2` er feil avhengighet. anthropic 2.6.0 bruker `httpx2`, bekreftet i venv.
- false: ingen logging av KI-feil. Hører til story 4.3 (forkastede svar logges).
- false: 300 tegn og avkortet svar (`max_tokens`) valideres ikke. Hører til story 4.2.
- rejected low: klienten bygges per kall (reserve brukes i dag), `FalskKi`/`KiSvar` uten validering av feltene, prompten bruker ikke `dato`/`startpunkt_id` (foreløpig prompt, forfines i 4.5), importregeltesten som traverserer hele repoet, modell-ID som konstant, tom `except Exception` uten logg.

## Design Notes

Avklart uten å spørre (valg brukeren ikke ser): kall B tar den ferdige reserveteksten som tredje argument, så reservevarianten gir identisk tekst og `sokflyt` beholder personaliseringssetningene (nivå, sperre og preferanser når aldri KI-dataklassene). Plassholderne `{tid}`, `{varighet}`, `{lengde}` og `{nivå}` og valideringen kommer i 4.2/4.5. Kall A og fritekst kommer i 4.6–4.7.

## Verification

**Commands:**
- `venv/Scripts/python.exe manage.py test` -- expected: alle grønne
- `venv/Scripts/python.exe -m ruff check .` -- expected: ingen funn
