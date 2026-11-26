---
title: 'Story 1.12: Ola får hjelp når ingen tur passer'
type: 'feature'
created: '2026-11-26'
status: 'done'
baseline_commit: 'c4ad7d60aca9d1aed976441d6e1e5f1a7bd6b03f'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-1-context.md'
  - '{project-root}/_bmad-output/planning-artifacts/ux-designs/ux-G81-eriksen-2026-11-06/EXPERIENCE.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Når ingen tur passer, får Ola bare «Endre søk» og vet ikke hva hun kan endre (FR-8, UX-DR17, UX-DR22, UX-DR25, SM-C1, SM-2).

**Approach:**
- `domene.utvalg.foresla_endringer(sok, turer, nivatak, tidligere_treff=())` gir høyst tre endringsforslag i fast rekkefølge: varighet, startpunkt, turtype. Et forslag tas bare med når `velg_turer` gir `TREFF` for det endrede søket (og, ved «alle vist», minst én tur som ikke er i `tidligere_treff`).
- Tilstandspanelet for `INGEN_TREFF` og «alle vist» viser forslagene som knapper i små POST-skjema. Søket kjøres på nytt med én endring og ny søke-ID (PRG).
- `TOPPTUR_ERSTATTET` og `BARE_OVER_NIVATAK` finnes fra før og verifiseres med tester.

## Boundaries & Constraints

**Always:**
- Forslag: (1) Varighet: korteste varighet i halvtimessteg som er lengre enn søket og gir treff («Prøv 3 timer», «Prøv 2,5 timer»); ved 12 t ikke noe forslag. (2) Startpunkt: bare når et startpunkt er valgt og minst ett annet startpunkt eller «Alle startpunkt» gir treff: «Velg startpunkt». (3) Turtype: bare når en turtype er valgt; første i rekkefølgen marka, utsikt, topptur som ikke er valgt og gir treff («Prøv marka»), ellers «Prøv alle turtyper» hvis det gir treff. De andre valgene er uendret.
- Varighet formateres i `domene/` med `formater_varighet_timer`. «Prøv 2,5 timer» og «Prøv alle turtyper» er [ASSUMPTION] i Mikrotekst.
- Ved «alle vist» er `tidligere_treff` lik `rangerte_tur_ider`. Gir ingen endring treff, vises bare «Endre søk» (og «Start fra første forslag igjen» ved «alle vist»).
- Forslagsknapper er `<button type="submit">` i POST-skjema med CSRF, uten `data-nytt-forslag` (full sideinnlasting, virker uten JS). Serveren validerer feltet og verdien mot den lagrede søke-ID-en og bruker `okt.lagre_sok` (ny søke-ID), deretter redirect til `turforslag:forslag`.
- «Velg startpunkt» er en lenke til `?sok=<id>&fokus=startpunkt`: forhåndsutfylt søk med fokus på Startpunkt. `fokus` valideres mot en liste.
- Tilstandspanel: `document.title` = h1, fokus på h1, «Endre søk» alltid med og bare én gang. Gjest ved `BARE_OVER_NIVATAK` får «Ingen grønne turer passer søket» uten løfte om lengre eller hardere turer.
- Views importerer ikke `domene`; logikken går via `turforslag/sokflyt.py`. CSP er uendret.

**Never:**
- ingen endring i `velg_turer`;
- ingen «Lag konto»-lenke (Epic 2);
- ingen ny JS-fil eller JSON-endepunkt;
- ingen `flush`, `cycle_key` eller `clear`.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Lengre varighet | INGEN_TREFF, 2 t; 3 t gir treff | knapp «Prøv 3 timer» | – |
| Halvtime | 2,5 t gir treff, ikke før | «Prøv 2,5 timer» | – |
| 12 t | søk på 12 t | ingen varighetsforslag | – |
| Startpunkt | valgt startpunkt; annet gir treff | «Velg startpunkt» (lenke) | – |
| Turtype | valgt topptur; marka gir treff | «Prøv marka»; ellers «Prøv alle turtyper» | – |
| Alle vist | `tidligere_treff` = treffene | bare forslag som gir ny tur | – |
| Ingen endring gir treff | alle tre faller bort | bare «Endre søk» | – |
| Trykk forslag | POST felt+verdi | nytt søk, ny søke-ID, 302 til forslag | ukjent felt/verdi eller ukjent søke-ID: 302 til Søk, ingen 500 |
| BARE_OVER_NIVATAK gjest | kun over nivåtak | «Ingen grønne turer passer søket», ingen løfte | – |

</frozen-after-approval>

## Code Map

- `domene/utvalg.py` -- `velg_turer`, `Status`; legg til `foresla_endringer` og et lite `Endringsforslag`-objekt (felt, verdi, etikett). Ikke endre `velg_turer`.
- `domene/sok.py` -- `Sok` er frozen: bruk `dataclasses.replace`; `VARIGHET_STEG_MIN`, `MAKS_VARIGHET_MIN`.
- `domene/tekst.py` -- `Forslagsvisning` (nytt felt for forslag), `formater_varighet_timer`, `formater_turtype`, `turtypevalg`.
- `turforslag/sokflyt.py` -- `forslagsvisning`, `utfor_sok`: kall `foresla_endringer` med `turdata.alle_turer()` og `NIVATAK_UTEN_HISTORIKK`; ny `endre_sok(tilstand, felt, verdi)`.
- `turforslag/views.py`, `turforslag/urls.py` -- ny `POST forslag/<sok_id>/endre/`; `sok` leser `fokus`.
- `turforslag/forms.py`, `templates/turforslag/_velgfelt.html`, `sok.html` -- fokus på Startpunkt.
- `templates/turforslag/_tilstandspanel.html` (+ `static` CSS `side.css`:1091-1132) -- forslagsknapper og «Prøv å endre søket:»; behold «Endre søk» én gang.
- `templates/turforslag/_forslag_innhold.html` -- `TOPPTUR_ERSTATTET` finnes allerede (verifiser rekkefølge).
- Tester: `tests/domene/test_utvalg.py`, `tests/web/test_forslag.py` (+ `testturer.py`).

## Tasks & Acceptance

**Execution:**
- [x] `domene/utvalg.py` -- `foresla_endringer` etter reglene over -- ren funksjon
- [x] `domene/tekst.py` -- etiketter og visning med forslag -- formatering i `domene/`
- [x] `turforslag/sokflyt.py` -- koble forslag til visning og `endre_sok` -- views importerer ikke `domene`
- [x] `turforslag/views.py`, `urls.py`, `forms.py` -- POST-endepunkt og `fokus=startpunkt`
- [x] `_tilstandspanel.html`, `sok.html`, `side.css` -- knapper og fokus
- [ ] tester -- hver status, halvtimer, 12 t, «alle vist» med `tidligere_treff`, tilfellet uten forslag, CSRF, ugyldig input

**Acceptance Criteria:**
- Given `TOPPTUR_ERSTATTET`, when forslaget vises, then merket «Utsikt i stedet for topptur» og advarselen «Ingen topptur passer søket ditt» står rett etter turnavnet.
- Given `INGEN_TREFF`, when panelet vises, then h1 «Jeg fant ingen tur som passer søket ditt», «Prøv å endre søket:» og forslagene står der, med fokus på h1 og `document.title` lik h1.
- Given et forslag trykkes, when POST er gyldig, then søket kjøres på nytt med én endring og ny søke-ID, og svaret er en redirect.

## Implementation Notes

- `Endringsforslag(felt, verdi, etikett)` bygger etiketten i `domene/utvalg.py` med lokal import fra `domene.tekst` (tekst.py importerer `Status` fra utvalg).
- `endre_sok` godtar bare felt og verdi som er blant forslagene for den lagrede tilstanden akkurat nå.
- `side.css` trengte ingen endring: `.handlingslenke` og `button.handlingslenke` dekker knappene.
- Etter review: positiv test for «Prøv alle turtyper» (domene og web), og villedende testnavn rettet.

## Spec Change Log

## Review Triage Log

| Funn | Verdict | Rute | Evidens |
|------|---------|------|---------|
| «Prøv alle turtyper» uten positiv test (verification-gap, edge-case, blind) | medium | patch | Ingen test ga forslaget eller sendte `verdi=""`. Lagt til domenetest og webtest; navnet på den villedende testen rettet. |
| Forslag som er utdatert gir «ikke lenger tilgjengelig» | low | avvist | Matrisen i spec (ukjent felt/verdi) krever 302 til Søk med den meldingen. |
| Etiketter i utvalg.py og lokal import (blind) | low | avvist | Bevisst valg, dokumentert; ren Python, ingen kjøretidsfeil. |
| CSS mangler (blind) | false | – | `.handlingslenke` (side.css:588) og `button.handlingslenke` (:1119) finnes og dekker knappene. |
| Session vokser uten grense (edge, blind) | false | – | `okt.MAKS_SOK=10` begrenser lagrede søk. |
| `?fokus=startpunkt` uten gyldig `?sok=` | low | avvist | Harmløst autofokus på tomt skjema. |
| Gammel `dato` i endret søk | low | defer | Se deferred-work. |
| Gjentatte `velg_turer`-kjøringer per visning | low | defer | Se deferred-work; 15 turer. |
| Prosessuelle punkter (avkrysning, logger, statusfiler) | low | patch | Gjort i denne runden. |

## Verification

**Commands:**
- `venv/Scripts/python.exe manage.py test` -- expected: alle tester grønne
