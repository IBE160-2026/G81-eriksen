---
title: 'Story 3.4: Testbrukeren viser personaliseringen'
type: 'feature'
created: '2026-11-27'
status: 'done'
baseline_commit: 'a97840603f8ceaf064dc698a1205db8bd991d507'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-3-context.md'
  - '{project-root}/_bmad-output/implementation-artifacts/spec-3-3-begrunnelsen-forklarer-nivaet.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Sensor må gå turer for å se nivåheving, sperre og prioritering. Det finnes ingen testbruker med ferdig historikk (FR-21, SM-4, AR-5, AR-20).

**Approach:** `data/testbruker.toml` (leses med `tomllib`) beskriver testbrukeren og registreringene hennes. `lastinn` laster turene først, validerer filen, og sletter og gjenskaper testbrukeren med registreringene ved hver kjøring, også i Vercel-byggesteget. README forklarer søket som viser heving, og hvordan sperren vises.

## Boundaries & Constraints

**Always:**
- Filen har `epost`, `passord` og `[[registrering]]` med `tur_id`, `dato` (ISO), `brukt_tid_min`, `vanskelighet`, `fornoydhet`, og en kommentar per registrering om hva den viser (AR-5). Passordet lagres bare som hash. Passord og e-post står i README (NFR-1: ikke en hemmelighet, ikke brukt til annet). Formatet og valget av TOML står i `data/README.md`.
- Historikken, i rekkefølge: tre *lette* grønne registreringer fordelt på to turer (én tur to ganger, gjentakelse teller), en blå *vanskelig* (sperre), en *moderat* (oppheving), og minst én gått tur med fornøydhet 1–2. Alle datoer faste og i fortiden. `vurder_historikk` gir grunnnivå blått, nivåtak blått, ingen sperre og `antall_hevinger` 1. En test sjekker dette uten database.
- `lastinn` (standardfil): først turene som i dag, så testbrukeren. Testbrukerfilen valideres fullt ut før noe skrives: finnes, gyldig TOML, e-post, passord (Djangos passordregler, minst 8 tegn), kjent tur-ID (blant turene som lastes), dato ikke frem i tid (mot dagens dato ved kjøring) og gyldige verdier etter FR-16 (brukt tid, vanskelighet, fornøydhet). Feil gir `CommandError` med norsk melding som sier hva som er feil, og ingenting i databasen endres, heller ikke turene.
- Testbruker-steget er én `transaction.atomic`: slett eksisterende testbruker med registreringer og innloggingsforsøk (gjenbruk `kontosletting`), opprett på nytt, lagre registreringene, sett `brukt_heving` til `max(antall_hevinger − 1, 0)` fra `vurder_historikk`. To kjøringer gir én testbruker med samme registreringer. Andre brukere og deres registreringer endres ikke.
- Med egen `--fil` (turfil) leses testbruker bare når `--testbruker` er oppgitt, slik at eksisterende `lastinn`-tester virker uendret. Ingen endring i byggekommandoen i `pyproject.toml` (den kjører allerede `lastinn`).
- README.md (rot) erstatter «Innlogging for testbrukeren … kommer i senere stories» med e-post, passord, hva historikken viser, at testbrukeren lages på nytt ved hver kjøring og publisering (endringer, også sletting av kontoen, forsvinner), søket som viser en blå tur først med hevingssetningen, og sperren: registrer en blå tur som *vanskelig* og søk på nytt. `data/README.md` får testbrukeravsnittet.
- Webtester: last testbrukeren, logg inn, gjør README-søket og sjekk blå tur først med hevingssetningen. Neste søk har hevingen brukt (`brukt_heving` = 1) og Historikk viser alle registreringene. En ny registrering vurdert *vanskelig* på en blå tur gir sperresetningen i neste søk.

**Never:**
- Ingen migrasjon, ingen endring av nivåreglene, rangering eller tekster i 3.1–3.3. Ingen ny avhengighet. Ingen refaktorering av `RegistreringForm` (valideringen for filen ligger i egen modul og gjenbruker konstantene i `domene/tekst.py` og `domene.niva`).
- `lastinn` sletter aldri andre brukere eller turer.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Første kjøring | tom DB | turer + testbruker med 5+ registreringer, `brukt_heving` 0 | N/A |
| Gjentatt kjøring | testbruker finnes (evt. endret/slettet) | gjenskapt, samme registreringer, én bruker | N/A |
| Andre brukere | Ola har egne registreringer | uendret | N/A |
| Fil mangler / ødelagt TOML | – | stopp, norsk melding, ingen DB-endring | `CommandError` |
| Ukjent tur-ID / dato frem i tid / ugyldig verdi / passord < 8 | – | stopp, norsk melding som peker på registrering/felt, ingen DB-endring (heller ikke turene) | `CommandError` |
| README-søket | innlogget testbruker, `brukt_heving` 0 | blå tur først, hevingssetning | N/A |
| Neste søk | `brukt_heving` 1 | grønn tur først, ingen hevingssetning | N/A |
| Ny blå tur *vanskelig* | registrert av testbrukeren | neste søk har sperresetning | N/A |

</frozen-after-approval>

## Code Map

- `turforslag/management/commands/lastinn.py` -- `handle`, `les_fil`, `standard_fil`; legg til testbruker-steget etter `lagre_turer`, nytt `--testbruker`.
- `turforslag/turdata.py` -- `lagre_turer` (atomic), `mangler_med_registreringer`.
- Ny modul i `turforslag/` (f.eks. `testbruker.py`) -- les/valider fil, opprett testbruker. Gjenbruk `turforslag/registrering.py::lagre`/`vurder_bruker`, `turforslag/kontosletting.py::slett_konto`, `Bruker.objects.create_user`, `domene/tekst.py` (konstanter for brukt tid og vanskelighet), `domene/niva.py`.
- `data/testbruker.toml` (ny), `data/README.md`, `README.md` (l.78–88), ev. `docs/arkitektur.md` (testbruker-omtale).
- Verifisert mot `data/turer.geojson`: grønne `sognsvann-brekke` (lett, to ganger) og `frognervassdraget` (lett, fornøydhet 2), blå `frognerseteren-skjennungstua` (vanskelig), grønn `rundtur-ulsrudvann` (moderat). Gir blått tak, ingen sperre, 1 heving. Søk med startpunkt Østmarksetra og varighet 4 timer gir `noklevann-rundt` først med heving og `ostmarksetra-mariholtet` uten. Implementer verifiserer igjen.
- `tests/web/test_lastinn.py`, `tests/web/test_niva_sok.py`, `tests/web/test_vercel.py` (byggestrengen uendret), `tests/domene/` (historikk fra fila).

## Tasks & Acceptance

**Execution:**
- [ ] `data/testbruker.toml` + `data/README.md` -- fila med kommentarer og formatbegrunnelse -- AR-5
- [ ] ny modul i `turforslag/`, `lastinn.py` -- validering og atomisk gjenskaping, norske feil -- FR-14, NFR-2, AD-11
- [ ] `README.md` -- testbruker, søk, sperre-oppskrift -- FR-21, AR-20
- [ ] Tester: filhistorikken gir blått/ingen sperre/1 (uten DB), idempotens, andre brukere urørt, alle ugyldige filer uten DB-endring, `brukt_heving`, passord bare hash, README-søket og sperre via web -- SM-2, SM-4

**Acceptance Criteria:**
- Given hele testsuiten og ruff, when de kjøres, then er alt grønt og eksisterende `lastinn`-tester er uendret.
- Given to kjøringer av `lastinn`, when jeg teller brukere og registreringer, then finnes én testbruker med de samme registreringene.

## Implementation Notes

- Nye filer: `data/testbruker.toml`, `turforslag/testbruker.py`, `tests/web/test_testbruker.py`. Endret: `lastinn.py` (`--testbruker`, atomisk gjenskaping), `README.md`, `data/README.md`. E-post `testbruker@example.com`, passord `Testbruker2026`. `pyproject.toml` uendret.

## Spec Change Log

## Review Triage Log

- patch (medium): ingen test for feil etter `slett` inne i transaksjonen. Lagt til to tester (manglende tur med annen brukers registrering, og `DatabaseError` fra `opprett`) som sjekker at testbruker, registreringer og turer er uendret. Rettet.
- patch (low): bare `DatabaseError` ble omgjort til `CommandError`. `ValidationError` lagt til. Rettet.
- defer (low): `slett` finner testbrukeren på e-post alene. En ekte bruker som registrerer `testbruker@example.com` slettes ved neste `lastinn`. En trygg løsning trenger en markering i databasen (migrasjon), som spec-en utelukker. Ført i deferred-work.md.
- false: offentlig passord i produksjon. Kreves av AC (NFR-10, NFR-1).
- false: historikken blir gammel, og rekkefølgen i fila er ikke validert. Nivåreglene bruker ikke tidsvinduer, og `historikk()` og databasen bruker begge filrekkefølgen som id-rekkefølge.
- rejected low: ukjente nøkler i TOML-fila, e-postnormalisering i `slett`, samtidige bygg mot samme database, `--testbruker` som `bool | Path`, tester som sjekker README-tekst, kommentarfinnes-testen, varsel i kjøringen om offentlig passord.

## Design Notes

Avklart uten å spørre: «tre grønne turer, én registrert to ganger» er tre registreringer på to turer (viser at gjentakelser teller). E-post `testbruker@example.com` og passord `Testbruker2026` (implementer kan velge andre verdier som oppfyller reglene og lister dem i README). Hele filen valideres før turene lagres, så en feil i testbrukerfilen aldri etterlater halvt lastet data. Eksisterende `--fil`-kall uten `--testbruker` hopper over testbruker.

## Verification

**Commands:**
- `venv/Scripts/python.exe manage.py test` -- expected: alle grønne
- `venv/Scripts/python.exe -m ruff check .` -- expected: ingen funn
