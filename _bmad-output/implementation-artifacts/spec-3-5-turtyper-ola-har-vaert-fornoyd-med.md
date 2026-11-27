---
title: 'Story 3.5 (P2): Turtyper Ola har vært fornøyd med, kommer først'
type: 'feature'
created: '2026-11-27'
status: 'done'
baseline_commit: '6ce8201748a75b1c70f58d5a1ee5c56647802bc8'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-3-context.md'
  - '{project-root}/_bmad-output/implementation-artifacts/spec-3-4-testbrukeren-viser-personaliseringen.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Turtypene Ola har vært fornøyd med påvirker ikke forslagene, og begrunnelsen sier ingenting om det (FR-20, FR-5 punkt 4, FR-12).

**Approach:** `vurder_historikk` samler `foretrukne_turtyper` (turtypene til turer med minst én registrering med fornøydhet 4–5). `velg_turer` rangerer turer med en foretrukket turtype foran andre, etter punkt 1 og 3 og før tid og tur-ID. Begrunnelsen får en preferansesetning etter en eventuell nivåsetning. Preferansen fryses i søketilstanden, og testbrukeren viser den.

## Boundaries & Constraints

**Always:**
- `domene.niva.Registrering` får `turtyper: tuple[str, ...] = ()` sist, og `NivaStatus` får `foretrukne_turtyper: frozenset[str] = frozenset()` sist. Eksisterende posisjonelle kall virker uendret. Fornøydhet 1–3 gir ingen preferanse. En senere lav fornøydhet fjerner ikke en preferanse. Ingen registreringer og gjester gir tomt sett. Omgjøringen i `turforslag/` (også `turforslag/testbruker.py::historikk`) fyller `turtyper` fra turen.
- `velg_turer` får bare nøkkelordargumentet `foretrukne_turtyper` (standard tomt sett). Rekkefølge i nøkkelen: gått-gruppe (1), nivåheving (3), foretrukket turtype (4), tid, tur-ID. Gåtte turer med fornøydhet 1–2 er fortsatt sist, og nivåhevingen går foran preferansen. Gjelder også utsiktsturene ved `TOPPTUR_ERSTATTET`. Tester fra 1.8 og 3.2 virker uendret.
- Preferansesetning, lagt til etter en eventuell nivåsetning (ny egen funksjon, `personaliseringssetning` beholder signaturen): «Du får en utsiktstur fordi du har vært fornøyd med utsiktsturer før.» Ordet er turens første turtype (rekkefølgen marka, utsikt, topptur) som også er blant de foretrukne: markatur/markaturer, utsiktstur/utsiktsturer, topptur/toppturer. Setningen kommer bare når den viste turen har en foretrukket turtype og minst ett annet treff i søket ikke har det. Ingen setning når alle treff har en foretrukket turtype, for gjester, for turforslag fra historikken, eller uten preferanse. Treffene slås opp på nytt fra turdatabasen, og turer som ikke finnes lenger, ignoreres.
- Hele begrunnelsen (mal + nivåsetning + preferansesetning) er høyst 300 tegn, med test for lengste kombinasjon. Teksten er [ASSUMPTION]: føres i Mikrotekst (EXPERIENCE.md er allerede merket), som kommentar i koden og i PR-en.
- `Soketilstand` får `foretrukne_turtyper: tuple[str, ...] = ()` (sortert), skrevet i `til_dict` og lest tolerant i `fra_dict` (eldre økter gir tom liste, ugyldig verdi gir `ValueError`). `utfor_sok` fryser dem sammen med resten av grunnlaget, så ny innlasting og «Nytt forslag» gir samme tekst.
- Testbrukerfila: registreringene med fornøydhet 4–5 skal gi bare utsikt som foretrukket turtype. Bytt de to lette `sognsvann-brekke` til `vettakollen-fuglemyrhytta` (grønn, bare utsikt, fornøydhet 4 og 5), og sett den moderate `rundtur-ulsrudvann` til fornøydhet 3. Nivåstatusen (grunnnivå og tak blått, ingen sperre, 1 heving) er uendret, og det er fortsatt tre lette registreringer på to turer. Oppdater kommentarer og README. README beskriver et søk som viser preferansen (etter at hevingen er brukt), og en test i `tests/web/` kjører det og sjekker setningen.

**Never:**
- Ingen endring av nivåreglene eller nivåsetningene (3.1–3.3). Ingen fritekst (story 4.7). Ingen migrasjon. Ikke prioriter preferansen over nivåheving eller over ikke-gåtte turer.
- Ingen logikk i `views.py`.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Preferanse bygges | registrering fornøydhet 4–5 på utsiktstur | `foretrukne_turtyper` inneholder `utsikt` | N/A |
| Lav fornøydhet | 1–3, eller senere lav på samme turtype | ingen preferanse / preferansen beholdes | N/A |
| Ingen / gjest | ingen registreringer | tomt sett, ingen setning | N/A |
| Rangering | ikke gått med foretrukket type vs. ikke gått uten | foretrukket først. Nivåheving foran preferanse. Gått 1–2 sist | N/A |
| Preferansesetning | vist tur har foretrukket type, et annet treff har ikke | «Du får en utsiktstur …» etter nivåsetning | N/A |
| Alle treff foretrukket | – | ingen preferansesetning | N/A |
| Historikktur | turforslag fra historikken | ingen preferansesetning | N/A |
| Lengste begrunnelse | sperre/heving + preferanse, 715 min | ≤ 300 tegn | N/A |
| Eldre økt | tilstand uten feltet | leses med tom liste | N/A |
| README-søk | testbruker, hevingen brukt | utsiktstur først med setningen | N/A |

</frozen-after-approval>

## Code Map

- `domene/niva.py` -- `Registrering` (l.19), `NivaStatus` (l.35), `vurder_historikk` (l.62): samle preferanse i løkka.
- `domene/utvalg.py` -- `_rangerte_ider` (nøkkel l.101–121), `velg_turer` (begge `_rangerte_ider`-kall inkl. `TOPPTUR_ERSTATTET`), `foresla_endringer` uendret. `Tur.turtyper` (`domene/tur.py:53`), `TURTYPER`.
- `domene/begrunnelse.py` -- `personaliseringssetning` (l.43, uendret signatur, 12 tester kaller den posisjonelt): ny funksjon for preferansesetning, turtypeord i `domene/` (`_TURTYPE_I_SETNING` finnes allerede for mal).
- `domene/okt.py` -- `Soketilstand`, `til_dict`/`fra_dict`, `ny_soketilstand`.
- `turforslag/registrering.py` (`domeneregistreringer`), `turforslag/sokflyt.py` (`utfor_sok`, `forslagsvisning` l.~150–170, `turdata.hent_tur`), `turforslag/testbruker.py` (`historikk` l.157).
- `data/testbruker.toml`, `README.md` l.80–90, `data/README.md`, `tests/web/test_testbruker.py` (`FilhistorikkTest`, `ReadmeSokTest`, `SOK`). Eksisterende krav: ≥5 registreringer, nøyaktig 3 lette, 2 unike lette tur-ID-er, minst én med fornøydhet ≤2, kommentar per registrering.
- Tester: `tests/domene/test_niva.py`, `test_utvalg_niva.py`, `test_okt.py` (eksakt dict l.46), `test_begrunnelse.py` (300 tegn l.60).
- README-søk foreslått (må verifiseres): etter at hevingen er brukt, uten startpunkt og 3,5 timer. `ostmarksetra-mariholtet` (marka, 210 min) er først uten preferanse, med utsikt-preferanse kommer `kolsastoppen` (195 min, utsikt) først.

## Tasks & Acceptance

**Execution:**
- [ ] `domene/niva.py`, `domene/utvalg.py` -- `turtyper`, `foretrukne_turtyper`, rangering punkt 4 -- FR-20, FR-5
- [ ] `domene/begrunnelse.py`, `domene/okt.py`, `turforslag/sokflyt.py`, `turforslag/registrering.py` -- setning, frysing, omgjøring -- FR-12, AD-5
- [ ] `data/testbruker.toml`, `turforslag/testbruker.py`, README -- utsikt-preferanse og søk -- FR-21
- [ ] Tester i `tests/domene/` og `tests/web/` for matriserader og alle kantene i AC (a–g), med henvisning til FR-20 og FR-5 -- SM-2

**Acceptance Criteria:**
- Given hele testsuiten og ruff, when de kjøres, then er alt grønt og testene for 3.1–3.4 er uendret (bortsett fra de som direkte avhenger av testbrukerfilens fornøydhet og turer).
- Given at FR-20 kuttes, when storyen tas ut, then faller bare punkt 4, preferansesetningen og testbrukerens preferanse bort.

## Implementation Notes

- Endret: `domene/niva.py`, `domene/utvalg.py`, `domene/begrunnelse.py` (`preferansesetning`), `domene/okt.py`, `turforslag/sokflyt.py`, `registrering.py`, `testbruker.py`, `data/testbruker.toml` (to lette `vettakollen-fuglemyrhytta`, moderat fornøydhet 3), README. [ASSUMPTION]: preferansesetningen.

## Spec Change Log

## Review Triage Log

- patch (low): nye testklasser lå etter `unittest.main()`-blokken i `test_niva.py` og `test_utvalg_niva.py`. Blokken flyttet sist. Rettet.
- patch (medium): 300-tegnstesten dekket bare turtypen marka. Utvidet til alle turtyper og til `TOPPTUR_ERSTATTET`, og lagt til test av at ordlisten dekker `TURTYPER`. Rettet.
- patch (low): `data/README.md` hadde urealistisk `brukt_tid_min` for ny tur-ID. Rettet.
- false: setningen sjekker ikke at preferansen avgjorde rangeringen. Spec og epics definerer «prioritert av preferansen» som at turen har en foretrukket type og minst ett annet treff ikke har det.
- false: historikkturer får preferansesetning. `historikkvisning` går via `registrering.py`, ikke `sokflyt.forslagsvisning`.
- rejected low: validering av turtyper i `fra_dict` mot `TURTYPER`, `turtyper` som `None` på en tur (JSONField har standard liste), foreldede treff-ID-er som ikke lenger passer søket, README som kan drive fra testbrukerfila, to terskler for fornøydhet (`FORNOYD_FRA`, `LAV_FORNOYDHET`), ekstra webtester.

## Design Notes

Avklart uten å spørre: setningen bruker turtypen som både turen og brukeren har (ellers ville den påstå noe galt om turen). Preferansen veies innenfor hver gått-gruppe og etter nivåheving, så «ikke gått» alltid vinner først. Testbrukeren får bare utsikt-preferanse ved å bytte de to lette turene til `vettakollen-fuglemyrhytta`, og nivåstatusen er uendret fordi begge er grønne lette turer.

## Verification

**Commands:**
- `venv/Scripts/python.exe manage.py test` -- expected: alle grønne
- `venv/Scripts/python.exe -m ruff check .` -- expected: ingen funn
