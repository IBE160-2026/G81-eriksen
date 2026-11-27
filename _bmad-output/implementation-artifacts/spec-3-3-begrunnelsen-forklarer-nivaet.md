---
title: 'Story 3.3: Begrunnelsen forklarer nivået'
type: 'feature'
created: '2026-11-27'
status: 'done'
baseline_commit: '974aca51a35ffb9d5eea3c70bf16be1bc00f8168'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-3-context.md'
  - '{project-root}/_bmad-output/implementation-artifacts/spec-3-2-soket-bruker-nivataket-og-historikken.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Når forslaget er tilpasset vurderingene til Ola, får hun ikke vite det eller hvorfor. Meldingen når ingen turer passer, er den samme for alle (FR-8, FR-12, FR-19, UX-DR22, UX-DR31).

**Approach:** Begrunnelsen fra reservemalen får en personaliseringssetning (heving, nådd nivå eller sperre) lagt til etter malteksten. Grunnlaget (nivåtak, grunnnivå, sperre, `nivaheving`, `har_historikk`) fryses i `Soketilstand`. `BARE_OVER_NIVATAK` får tre varianter (gjest, innlogget uten historikk, innlogget med historikk) med tittel og tekst fra `domene/tekst.py`.

## Boundaries & Constraints

**Always:**
- Personaliseringssetning, i denne rekkefølgen, aldri flere samtidig, ingen tall i malene, nivåord bøyd i `domene/` (en blå tur, de tre siste grønne turene, blått nivå; grønn/grønne/grønt, blå/blå/blått, rød/røde/rødt, svart/svarte/svart):
  1. Aktiv sperre (turforslag fra søk): «Du får en {turnivå} tur igjen fordi den siste {sperreturens nivå} turen føltes vanskelig.» Eksempel: «Du får en grønn tur igjen fordi den siste blå turen føltes vanskelig.»
  2. Ellers `nivaheving=True` og turens nivå lik nivåtaket og over grønt: «Du får en blå tur fordi de tre siste grønne turene var lette for deg.» (nivået under turens nivå). Eksempel rød: «… en rød tur … de tre siste blå turene …».
  3. Ellers turens nivå over grønt: «Du får en blå tur fordi du har nådd blått nivå.»
  4. Ellers ingen setning: grønn tur uten sperre, gjest, bruker uten historikk, turforslag fra historikken, eldre økter uten grunnlaget.
- Hele begrunnelsen slik brukeren ser den er høyst 300 tegn. En test dekker lengste kombinasjon av mal, turtype, varighet og setning. «Begrunnelse fra mal» uendret. `reservebegrunnelse(sok, tur)` beholder signaturen (testen låser den); setningen lages i egen funksjon i `domene/` og legges til i `sokflyt`.
- `Soketilstand` får `grunnniva`, `sperre` (`domene.niva.Sperre` eller `None`) og `har_historikk`, med standard grønt, `None`, `False`; skrives i `til_dict`, leses tolerant i `fra_dict` (ugyldige verdier gir `ValueError`). `utfor_sok` fryser dem fra `NivaStatus`. Ny innlasting, «Nytt forslag» og ny registrering i annen fane gir samme tekst.
- `BARE_OVER_NIVATAK` (tittel i `<h1>`, `<title>` og `data-tittel` fra ett felt i `domene/tekst.py`, fokus på `h1`):
  - Gjest: uendret (tittel «Ingen grønne turer passer søket», teksten med «Lag konto» som i dag).
  - Innlogget uten registreringer: samme tittel, «Som ny bruker får du grønne turer. Registrer og vurder turene du går, så tilpasser jeg forslagene etter hvordan turene kjentes for deg.», ingen «Lag konto», «Endre søk».
  - Innlogget med registrering: «Akkurat nå foreslår jeg turer opp til {nivåtak} nivå, og ingen av dem passer søket.» (intetkjønn, «grønt nivå», «blått nivå»; med aktiv sperre er nivåtaket sperrenivået). Tittel ved grønt tak «Ingen grønne turer passer søket», ellers «Ingen turer opp til blått nivå passer søket».
- Ingen tekst lover lengre eller hardere turer (SM-C1). PR-en lister tekstene merket [ASSUMPTION] som tas i bruk: nådd nivå, sperre, innlogget uten historikk, med historikk, tittel ved høyere tak. De står også som kommentar i koden.

**Never:**
- Ingen endring av `historikkbegrunnelse`, gjesteteksten, KI-merket, rangering/utvalg, `brukt_heving`, testbruker eller turtypepreferanse (3.4–3.5). Ingen migrasjon.
- Ingen logikk i `views.py`.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Første søk etter heving | blå tur, `nivaheving=True`, tak blått | mal + «Du får en blå tur fordi de tre siste grønne turene var lette for deg.» | N/A |
| Senere søk | blå tur, `nivaheving=False`, tak blått | mal + «… fordi du har nådd blått nivå.» | N/A |
| Aktiv sperre | grønn tur, sperre grønn fra blå tur | mal + «Du får en grønn tur igjen fordi den siste blå turen føltes vanskelig.» | N/A |
| Grønn tur / gjest / historikk-tur | – | ingen setning | N/A |
| Lengste kombinasjon | alle turtyper × varigheter × setninger | ≤ 300 tegn | N/A |
| Eldre økt | tilstand uten nye felt | ingen setning, gjeste-/grønn-visning | N/A |
| `BARE_OVER_NIVATAK` gjest | – | uendret tekst og tittel | N/A |
| `BARE_OVER_NIVATAK` ny bruker | innlogget, ingen registreringer | variant uten «Lag konto» | N/A |
| `BARE_OVER_NIVATAK` med historikk | tak blått / sperre grønn | «opp til blått nivå» / «opp til grønt nivå», tilsvarende tittel | N/A |

</frozen-after-approval>

## Code Map

- `domene/begrunnelse.py` -- `reservebegrunnelse` (l.24, signatur låst), `MAKS_TEGN`; ny funksjon for personaliseringssetning (bruker `domene.niva.Sperre`).
- `domene/tekst.py` -- `_NIVATEKST`/`formater_niva` (l.26,100): ny bøyning; `Forslagsvisning` (l.286), `forslagsvisning` (l.375): nytt felt for tittel og tekst ved `BARE_OVER_NIVATAK`.
- `domene/okt.py` -- `Soketilstand`, `til_dict`, `fra_dict`, `ny_soketilstand` (nøkkelordargumenter, eksisterende kall uendret).
- `turforslag/sokflyt.py` -- `utfor_sok` (fryser fra `NivaStatus` og `bool(registreringer)`), `forslagsvisning` (legger setningen til, l.100-154).
- `turforslag/templates/turforslag/_tilstandspanel.html`, `_tittel.html` -- hardkodet overskrift/tekst for `BARE_OVER_NIVATAK` byttes mot feltene fra `tekst.py`. Ellers divergerer `<title>` og `<h1>`.
- Tester: `tests/domene/test_begrunnelse.py` (lengdetest), `test_okt.py` (eksakt `til_dict`), `test_tekst.py`, `tests/web/test_forslag.py` (l.263 og l.1004 gjest, skal være uendret), `tests/web/test_niva_sok.py`.
- Kilde for tekst: `EXPERIENCE.md` Mikrotekst l.122-137.

## Tasks & Acceptance

**Execution:**
- [ ] `domene/okt.py` -- frys grunnniva, sperre, har_historikk med tolerant lesing -- AD-5, NFR-2
- [ ] `domene/tekst.py`, `domene/begrunnelse.py` -- bøying, setninger, tittel og tekst for `BARE_OVER_NIVATAK` -- FR-12, FR-8, AR-16
- [ ] `turforslag/sokflyt.py`, maler -- koble setning og varianter, én tittelkilde -- UX-DR22, UX-DR25
- [ ] Tester i `tests/domene/` og `tests/web/` for setningene, bøyning, lengde (300), tre varianter, ny innlasting og «Nytt forslag» (samme tekst), eldre økt, gjesteteksten uendret; viser til FR-8, FR-12, SM-2

**Acceptance Criteria:**
- Given hele testsuiten og ruff, when de kjøres, then er alt grønt, og gjestetestene (`tests/web/test_forslag.py` l.263, l.1004) er uendret.
- Given tittelen ved `BARE_OVER_NIVATAK`, when siden vises, then er `<title>`, `data-tittel` og `<h1>` lik, og fokus står på `h1`.

## Implementation Notes

- Endret: `domene/okt.py`, `domene/tekst.py` (`nivaord`, `nivatak_tittel`, `nivatak_tekst`), `domene/begrunnelse.py` (`personaliseringssetning`), `turforslag/sokflyt.py`, `_tilstandspanel.html`, `_tittel.html`. Tester utvidet; én eksisterende test i `test_konto.py` oppdatert til ny tekst for ny bruker. 696 tester forventet OK.
- [ASSUMPTION]-tekster tatt i bruk: nådd nivå, sperre, innlogget uten historikk, med historikk, tittel ved høyere tak.

## Spec Change Log

## Review Triage Log

- patch (medium): ingen webtest for `BARE_OVER_NIVATAK` med nivåtak over grønt (tittel i `<h1>`, `<title>`, `data-tittel` og tekst). Lagt til `test_bare_over_nivatak_med_bla_tak` (via økten, siden testturene ikke har rød tur). Rettet.
- patch (low): `test_eldre_okt_uten_grunnlaget_viser_ingen_setning` sjekket bare status 200. Erstattet av en test som fjerner alle nye felt fra den lagrede økten og sjekker tur uten «Du får en». Rettet.
- false: sperresetning på tur over sperrenivået. Turer filtreres til høyst nivåtaket, som med sperre er sperrenivået, så det kan ikke skje.
- false: historikktur får setning. `historikkvisning` går via `registrering.py`, ikke `sokflyt.forslagsvisning`, og har egen begrunnelse.
- false: `grunnniva` er ubrukt. Spec krever at det fryses; 3.4/3.5 og senere visning kan bruke det.
- rejected low: eldre økt med historikk får «ny bruker»-tekst (AC krever standard `har_historikk=False`), `user.is_authenticated` i mal mot frosset tilstand (gjest som logger inn midt i søket, sjeldent), runtime-lengdekontroll av begrunnelsen (dekket av test), `nivaord` som `Literal`, `har_historikk` som ikke-bool, duplisert gjestetekst i mal, testrenhet (nøstede løkker, dobbel assert).

## Design Notes

Avklart uten å spørre (følger AC og PRD FR-12 ordrett): setningen kommer bare på turer over grønt, og hevingssetningen bare når turen er på nivåtaket i første søk etter heving (ellers ville «de tre siste X turene» være feil for en tur under taket); sperresetningen gjelder alle søketurer ved aktiv sperre; «igjen» beholdes slik Mikrotekst har det. Alle [ASSUMPTION]-tekster er foreløpige til produkteier har godkjent dem.

## Verification

**Commands:**
- `venv/Scripts/python.exe manage.py test` -- expected: alle grønne
- `venv/Scripts/python.exe -m ruff check .` -- expected: ingen funn
