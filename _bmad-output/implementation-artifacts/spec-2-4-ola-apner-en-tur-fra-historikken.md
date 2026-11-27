---
title: 'Story 2.4: Ola åpner en tur fra historikken'
type: 'feature'
created: '2026-11-27'
status: 'done'
baseline_commit: '2f57be1ce0addfe90b33688199002f41680be840'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-2-context.md'
  - '{project-root}/_bmad-output/planning-artifacts/ux-designs/ux-G81-eriksen-2026-11-06/EXPERIENCE.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Historikk er en blindvei. Ola kan ikke åpne en tur hun har gått som turforslag eller registrere den på nytt fra tabellen (FR-17, FR-12, FR-16, FR-7, UX-DR29).

**Approach:** Handlingskolonnen i Historikk får «Åpne som turforslag» og «Registrer gjennomført tur» med skjulte tillegg. Et turforslag fra historikken på egen adresse, uavhengig av søkeøkta, med fast begrunnelse fra mal.

## Boundaries & Constraints

**Always:**
- Ny adresse `/historikk/<registrering_id>/` (GET, `login_required`, `never_cache`, `require_safe`) viser turen til den registreringen. Registreringen hentes filtrert på `request.user`; andres eller ukjent registrering gir 404, gjest sendes til Logg inn med `next`. Turen som ikke finnes via `turdata.hent_tur` gir 404.
- Visningen gjenbruker `forslag.html`/`_forslag_innhold.html` (kart, tall, nivåmerke, forklaring som vanlig) med et flagg for «fra historikken»: i stedet for søkeoppsummeringen står «Fra historikken din» (ingen «Endre søk»); ingen Turtype-treff; «Nytt forslag» er byttet ut med «Finn en ny tur» (primærknapp som GET-lenke til Søk, tomt søk); «Registrer gjennomført tur» er sekundærlenke til `/registrer/<tur_id>/`. Sidetittel «{Turnavn} – Turforslag».
- Begrunnelsen kommer fra en fast mal uten KI: «Du gikk denne turen {dato} og ga den {n} av 5.» med datoen som «12. oktober» (full måned, uten år) fra registreringen som lenken peker på. Ny ren funksjon i `domene/` (maks 300 tegn, FR-12); KI-merket viser «Begrunnelse fra mal».
- Er turen over nivåtaket, vises Melding (info) «Denne turen er over nivået jeg foreslår for deg nå.» rett etter turnavnet. Til Epic 3 er nivåtaket grønt for alle (`NIVATAK_UTEN_HISTORIKK`), så merknaden gjelder turer over grønt. Avgjørelsen ligger i en liten ren funksjon i `domene/` som story 3.2 kan bytte. Turen vises likevel (ingen `_passer`-sjekk).
- Søketilstanden røres ikke: visningen kaller ikke `okt.*`, og `session["sok"]` er uendret (FR-7).
- Historikk-tabellen: siste kolonne har lenkene «Åpne som turforslag» og «Registrer gjennomført tur» under hverandre (understreket, minst 44 px), hver med visuelt skjult tillegg «– {Turnavn}, {dato}» (dato som «7. nov.», klassen `skjult-tekst`). Kolonneoverskriften «Handlinger» er fortsatt skjult. Hver rad lenker til sin egen registrering.
- Views importerer ikke `domene`, `turdata` eller `models` (lagdelingstesten); logikk i `turforslag/registrering.py` og formatering i `domene/tekst.py`. `forbedring.js` må ikke feile når «Nytt forslag»-skjemaet mangler.

**Never:**
- ingen endring av `okt.py`, `Soketilstand`, `velg_turer` eller søkeflyten; ingen POST for å åpne turen;
- ingen krav-om-konto-flyt for gjest (2.5), ingen sletting av konto (2.6), ingen bekledningstips (Epic 5), ingen KI (Epic 4), ingen `vurder_historikk`/nivåtak fra historikk (Epic 3);
- ingen ny migrering, ingen ny JS-fil.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Åpne fra rad | innlogget, egen registrering | turforslag med «Fra historikken din», begrunnelse «Du gikk denne turen {dato} og ga den {n} av 5.», KI-merke «Begrunnelse fra mal», kart og tall, «Finn en ny tur» | N/A |
| Samme tur flere ganger | to registreringer av samme tur | hver lenke viser teksten med den radens dato og vurdering | N/A |
| Tur over grønt | blå/rød/svart tur | Melding (info) «Denne turen er over nivået jeg foreslår for deg nå.» rett etter turnavnet, turen vises likevel | N/A |
| Tur på grønt nivå | grønn tur | ingen nivåmelding | N/A |
| Andres registrering | annen brukers `registrering_id` | 404 | N/A |
| Ukjent registrering | `registrering_id` finnes ikke | 404 | N/A |
| Gjest | uinnlogget | redirect til Logg inn med `next` | N/A |
| Pågående søk | åpen fane med søk | `session["sok"]` uendret etter besøket | N/A |
| Registrer fra rad | klikk «Registrer gjennomført tur» | `/registrer/<tur_id>/` for den turen | N/A |
| Finn en ny tur | klikk på knappen | Søk (`/`), tomt skjema | N/A |

</frozen-after-approval>

## Code Map

- `turforslag/urls.py`, `views.py` -- ny rute og view `historikk_tur` (`login_required`, `never_cache`, `require_safe`, 404); ikke importer domene/models/turdata (`ViewsLagdelingTest`, `tests/web/test_forslag.py`).
- `turforslag/registrering.py` -- har `historikk(bruker)` og `oppsummering`; legg til henting av egen registrering og bygging av visning; `tekst.Historikkrad` må få `id`, `tur_id` og dato-tekst for tillegget.
- `domene/tekst.py` -- `Turvisning`/`turvisning`/`forslagsvisning` krever `Sok`/`Status`; lag variant for historikk (ingen Turtype-treff, ingen `topptur_erstattet`); `formater_dato` («12. oktober»), `formater_dato_historikk` («7. nov.»), `formater_fornoydhet` finnes.
- `domene/begrunnelse.py` -- ny ren funksjon for historikkbegrunnelsen; `domene/utvalg.py` (`NIVATAK_UTEN_HISTORIKK`, l.~20) -- liten ren funksjon «over nivåtaket».
- `turforslag/templates/turforslag/forslag.html`, `_forslag_innhold.html` -- gren for «fra historikken» (søkeoppsummering, «Endre søk», `sok_id`, «Nytt forslag», Turtype-treff); `_melding.html` (type info) etter h1; KI-merket «Begrunnelse fra mal» er hardkodet.
- `turforslag/templates/turforslag/historikk.html` -- tom siste `<td>` i hver rad; klassen `.skjult-tekst`, `.handlingslenke` finnes i `side.css`.
- `turforslag/static/forbedring.js` -- sjekk at fraværende `data-nytt-forslag` ikke feiler.
- `tests/web/test_registrering.py` (`HistorikkTest`, `test_tabell_med_en_rad` berøres), `tests/web/test_forslag.py`, `tests/domene/test_tekst.py`, `tests/domene/test_begrunnelse.py`, `tests/domene/test_utvalg.py`, `tests/web/testturer.py`.
- Ikke endre: `okt.py`, `Soketilstand`, `sokflyt.py`-søkeflyt, `Registrering`-modellen.

## Tasks & Acceptance

**Execution:**
- [x] `domene/begrunnelse.py`, `domene/utvalg.py`, `domene/tekst.py` + domenetester -- historikkbegrunnelse, «over nivåtaket», visning uten søk og `Historikkrad` med id/tur_id/dato-tekst
- [x] `turforslag/registrering.py`, `views.py`, `urls.py` -- hent egen registrering, `historikk_tur`, 404, gjest
- [x] `turforslag/templates/` -- `forslag`-mal med historikkgren, handlingskolonne i `historikk.html`, skjulte tillegg
- [x] `turforslag/static/forbedring.js` -- tåle manglende «Nytt forslag»-skjema (hvis nødvendig)
- [x] `tests/web/` -- hver rad i matrisen, to brukere, `session["sok"]` uendret, tekstjusteringer i eksisterende tester

**Acceptance Criteria:**
- Given en rad i Historikk, when jeg trykker «Åpne som turforslag», then turen vises som turforslag fra historikken med «Fra historikken din», mal-begrunnelse med radens dato og vurdering, «Begrunnelse fra mal» og «Finn en ny tur».
- Given en tur over grønt, when jeg åpner den fra historikken, then merknaden vises rett etter turnavnet og turen vises likevel.
- Given et pågående søk i en fane, when jeg åpner en tur fra historikken, then søketilstanden er uendret.
- Given en rad i Historikk, when jeg trykker «Registrer gjennomført tur», then registreringen for den turen åpnes.

## Implementation Notes

- Chrome lokalt (via DOM; skjermbilder tidsavbrøt på siden med kart): handlingslenker med skjulte tillegg og egen registrering per rad; blå tur viser «Fra historikken din», nivåmeldingen rett etter h1, «Begrunnelse fra mal», «Du gikk denne turen 7. november og ga den 4 av 5.», «Finn en ny tur» (`/`) og «Registrer gjennomført tur»; grønn tur uten nivåmelding; ukjent registrering gir 404. Ikke sett visuelt: kart og utseendet til handlingskolonnen.
- Implementert av subagent; 609 tester, ruff og `makemigrations --check` grønne. `Forslagsvisning` fikk `fra_historikk` og `over_nivatak`; `historikkvisning` i `domene/tekst.py`; `registrering.historikkvisning(bruker, id)`; ny rute `historikk/<int:registrering_id>/`; `forbedring.js` uendret (sjekker `hasAttribute`).

## Spec Change Log

## Review Triage Log

- false: `sok_url` mangler i konteksten — satt med `{% url 'turforslag:sok' as sok_url %}` øverst i `_forslag_innhold.html` (l.6); `sok_id` brukes bare i grenen som ikke er historikk.
- false: 44 px berøringsflate mangler — `.handlingslenke` har `min-height: var(--touch-target-min)`; `.historikk-handlinger` legger bare til understreking.
- false: `er_over_nivatak` kan feile på ukjent nivå — `Tur.turniva` er alltid en `Turniva`.
- avvist: rad med lenke til tur som er borte (404) er umulig i vanlig drift (PROTECT og `lastinn`-vakt); konstruert `Forslagsvisning.status`; skjøre `count=`-tester; ingen test av POST→405 og `never_cache` (dekket av dekoratorene); dato uten år (spec); FR-18-merking.

## Design Notes

Valg tatt uten spørsmål: adresse per registrering (ikke per tur), så hver rad gir sin egen dato og vurdering; «12. oktober» i begrunnelsen og «7. nov.» i skjulte tillegg; «Åpne som turforslag» er GET-lenke; «Finn en ny tur» går til tomt Søk; ingen «Tilbake»-lenke (menyen har Historikk); `aria-current` ligger ikke på menyen på denne siden.

## Verification

**Commands:**
- `venv/Scripts/python.exe manage.py makemigrations --check --dry-run` -- expected: ingen endringer
- `venv/Scripts/python.exe manage.py test` -- expected: alle tester grønne
- `venv/Scripts/python.exe -m ruff check . && venv/Scripts/python.exe -m ruff format --check .` -- expected: ingen feil

**Manual checks (if no CLI):**
- Chrome lokalt: registrer en tur, åpne den fra Historikk, se mal-begrunnelse, kart og «Finn en ny tur»; åpne et pågående søk i en annen fane og bekreft at det er uendret.
