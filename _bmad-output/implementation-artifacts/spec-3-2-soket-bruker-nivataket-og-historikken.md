---
title: 'Story 3.2: Søket bruker nivåtaket og historikken'
type: 'feature'
created: '2026-11-27'
status: 'done'
baseline_commit: '78652caa7114b1a451e18f40d62a09694fbe9e39'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-3-context.md'
  - '{project-root}/_bmad-output/implementation-artifacts/spec-3-1-vurderingene-bestemmer-nivatak.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Søket bruker fast grønt nivåtak og ser ikke på hva Ola har gått. `vurder_historikk` (3.1) brukes ingen steder, og `Bruker.brukt_heving` lagres aldri (FR-5, FR-19, FR-17, NFR-8, AD-11).

**Approach:** Ved hvert gyldig søk av en innlogget bruker hentes egne registreringer i `turforslag/`, omgjøres til `domene.niva.Registrering` og går til `vurder_historikk`. `NivaStatus.nivatak` styrer filteret i `velg_turer`. Nye rangeringspunkter (ikke gått først, nivåheving) brukes, og `brukt_heving` lagres i samme forespørsel. Merknaden i historikkvisningen bruker samme nivåtak.

## Boundaries & Constraints

**Always:**
- Omgjøring modell → domeneobjekt og lagring av `brukt_heving` ligger i `turforslag/registrering.py`/`sokflyt.py`, aldri i `views.py` (strukturtesten i `tests/web/test_forslag.py` skal bestå). Registreringer filtreres på brukeren (NFR-8). Gjest: ingen registreringer, grønt tak, `nivaheving=False`, ingenting lagres.
- `velg_turer` får bare nøkkelordargumentene `registreringer` (standard tom) og `nivaheving` (standard `False`). Kall og tester fra Epic 1 virker uendret. Nivåtaket er fortsatt tredje posisjonsargument og kommer fra `NivaStatus.nivatak`.
- Rangering: (1) ikke gåtte turer først, så gåtte med fornøydhet 3–5, så 1–2. Fornøydheten er den i siste registrering for turen (dato, deretter id). (3) Ved `nivaheving=True` kommer turer med turnivå lik nivåtaket foran lavere, etter (1). Deretter eksisterende tid og tur-ID. Gåtte turer utelukkes aldri. Status er fortsatt `TREFF` når alle er gått, også for utsiktsturene ved `TOPPTUR_ERSTATTET`.
- Ren funksjon i `domene.niva` avgjør heving fra `NivaStatus` og `brukt_heving`: `antall_hevinger > brukt_heving` og ingen sperre gir `True`, ellers `False`. `brukt_heving` settes alltid til `antall_hevinger` ved et gyldig søk fra innlogget bruker (også `INGEN_TREFF`, `BARE_OVER_NIVATAK`, aktiv sperre og når en tidligere dato har fjernet en heving).
- `nivaheving` og nivåtaket fryses i `Soketilstand` (nytt felt `nivatak`, standard grønt; eldre lagrede tilstander leses uten feil). Ny innlasting, «Nytt forslag», «Start fra første forslag igjen» og visning bruker det frosne taket og endrer verken rangering eller `brukt_heving`. Ugyldig søk endrer ikke `brukt_heving`. Et endringsforslag (story 1.12, f.eks. «Prøv 3 timer») er et nytt gyldig søk og regnes ut på nytt fra historikken. Kandidatene i `foresla_endringer` bruker samme nivåtak.
- Merknaden i historikkvisningen («Denne turen er over nivået jeg foreslår for deg nå.», teksten uendret) bruker `NivaStatus.nivatak` fra `vurder_historikk`, også med aktiv sperre.

**Never:**
- Ingen endring av begrunnelsestekster, meldinger, maler, testbruker eller turtypepreferanse (3.3–3.5). Ingen migrasjon (`brukt_heving` finnes).
- Ikke fjern `NIVATAK_UTEN_HISTORIKK` hvis tester fra Epic 1 bruker den. Gjest og tomme tilfeller kan bruke den som standard.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Gjest søker | ikke innlogget | grønt tak, `nivaheving=False`, ingen lagring | N/A |
| Grunnnivå blått, ingen sperre | innlogget, gyldig søk | blå og grønne turer, aldri røde/svarte | N/A |
| Aktiv sperre grønn, grunnnivå blått | gyldig søk | bare turer til og med sperrenivået. Hevingen regnes brukt, `nivaheving=False` | N/A |
| Ny heving | `antall_hevinger=1`, `brukt_heving=0`, ingen sperre | `nivaheving=True`, `brukt_heving` lagres som 1. Neste søk gir `False` | N/A |
| Heving fjernet av tidligere dato | `antall_hevinger < brukt_heving` | `nivaheving=False`, `brukt_heving` settes ned | N/A |
| Ikke gått foran gått | ikke gått grønn, gått blå (`nivaheving=True`, tak blått) | grønn først (punkt 1 før 3) | N/A |
| Alle treff gått | alle gåtte | status `TREFF`, ingen utelukket | N/A |
| Bare over taket / ingen treff | gyldig søk | `BARE_OVER_NIVATAK`/`INGEN_TREFF`, `brukt_heving` lagres likevel | N/A |
| Ugyldig søk, innlasting, «Nytt forslag» | – | `brukt_heving` og rangering uendret | N/A |
| Eldre økt | tilstand uten `nivatak` | leses med grønt tak | N/A |

</frozen-after-approval>

## Code Map

- `domene/niva.py` (3.1) -- legg til ren funksjon for `nivaheving` (`NivaStatus`, `brukt_heving`).
- `domene/utvalg.py` -- `velg_turer` (l.83), `_rangeringsnokkel` (l.73), `_rangerte_ider` (l.78), `foresla_endringer`/`_gir_treff`, `er_over_nivatak` (l.47, tak som parameter med standard grønt). Utsiktsturene ved `TOPPTUR_ERSTATTET` går gjennom `_rangerte_ider`, så ny rangering gjelder også der.
- `domene/okt.py:23-68` -- `Soketilstand` (har `nivaheving`), `til_dict`/`fra_dict` (`data.get`-mønster), `ny_soketilstand`: nytt felt `nivatak`.
- `turforslag/sokflyt.py` -- `utfor_sok` (l.33, får bruker), `_endringsforslag`/`endre_sok` (l.327-355), `_passer`/`_gyldig`/`forslagsvisning` bruker frosset tak. `velg_turer` må fortsatt importeres her (testene mocker `turforslag.sokflyt.velg_turer`).
- `turforslag/registrering.py` -- `historikk`, `historikkvisning` (l.524-558). Ny funksjon modell → `domene.niva.Registrering` (alias mot modellen `Registrering`, `Turniva(r.tur.turniva)`), brukes av både søk og historikkvisning. Lagre med `bruker.save(update_fields=["brukt_heving"])` (`Bruker.save` er overstyrt, `models.py:70`).
- `turforslag/views.py:56-128` -- `sok`/`endre` sender `request.user` videre, ingen logikk her.
- Tester: `tests/domene/test_utvalg.py`, `test_okt.py`, `tests/web/test_sok.py`, `test_forslag.py`, `test_registrering.py` (l.340-405).

## Tasks & Acceptance

**Execution:**
- [ ] `domene/niva.py` -- ren `nivaheving`-funksjon -- AD-11 punkt 2
- [ ] `domene/utvalg.py` -- rangering punkt 1 og 3, `registreringer`/`nivaheving` i `velg_turer`, tak som parameter i `er_over_nivatak` -- FR-5
- [ ] `domene/okt.py` -- `nivatak` i `Soketilstand` med tolerant lesing -- AD-5, NFR-2
- [ ] `turforslag/registrering.py`, `sokflyt.py`, `views.py` -- hent historikk, vurder, lagre `brukt_heving`, frys taket, bruk i endringsforslag og historikkmerknad -- FR-19, FR-17
- [ ] Tester i `tests/domene/` og `tests/web/` for alle matriserader, inkludert de 12 FR-19-slutttilstandene mot `velg_turer`, `brukt_heving` lagret, annen bruker upåvirket, annen fane og ugyldig søk. De viser til FR-5, FR-19 og SM-C1

**Acceptance Criteria:**
- Given sluttilstanden i hvert av de 12 eksemplene i FR-19, when `velg_turer` kalles, then er ingen tur over nivåtaket med i noe utvalg, og statusen er `BARE_OVER_NIVATAK` når bare slike turer passer (SM-C1).
- Given hele testsuiten og ruff, when de kjøres, then er alt grønt og Epic 1-testene er uendret.

## Implementation Notes

- Endret: `domene/niva.py` (`nivaheving`), `domene/utvalg.py`, `domene/okt.py` (`nivatak`), `turforslag/registrering.py`, `sokflyt.py`, `views.py`. Nye tester: `tests/domene/test_utvalg_niva.py`, `tests/web/test_niva_sok.py`; `test_okt.py` utvidet. 678 tester OK, ruff OK.

## Spec Change Log

## Review Triage Log

- patch (low): `velg_turer`-docstringen nevnte ikke `registreringer`/`nivaheving`. Rettet.
- defer (low): `avgjor_nivaheving` er ikke atomisk. To samtidige søk fra samme bruker (to faner) kan begge få `nivaheving=True`. Konsekvensen er at hevingen prioriteres to ganger, uten datatap. Fiks: betinget `UPDATE ... WHERE brukt_heving < antall_hevinger`. Ført i deferred-work.md.
- false: `endre_sok` mister `nivaheving`. Spec og epics sier at neste gyldige søk etter en brukt heving har `nivaheving=False`.
- false: `nivaheving` brukes ikke i UI. Hører til story 3.3.
- false: `sokflyt` importerer `turforslag.registrering`. Spec plasserer omgjøring og lagring der, og strukturtesten på `views.py` består.
- rejected low: ugyldig `nivatak` i lagret økt (`ValueError` fanges i `hent_sok` og gir ukjent søke-ID), turnivå utenfor `Turniva` i databasen (fanges av `lastinn`), `bruker=None` uten annotasjon, ekstra spørringer ved historikkvisning, `brukt_heving` lagres før økten, ekstra testtilfeller (gjest via `endre`, ugyldig `nivatak`). Ingen konkret skade vist, og fiksene ville legge til guards.
- Verification Gap-reviewer: ingen hull.

## Design Notes

Avklart uten å spørre (valg Ola ikke merker): bare `nivatak` fryses i tilstanden nå (grunnnivå og sperre legges til i 3.3 når begrunnelsen trenger dem). `brukt_heving` settes alltid til `antall_hevinger` ved gyldig søk, også med aktiv sperre, slik AC sier. Merknadsteksten beholdes slik AC og tester har den.

## Verification

**Commands:**
- `venv/Scripts/python.exe manage.py test` -- expected: alle grønne
- `venv/Scripts/python.exe -m ruff check .` -- expected: ingen funn
