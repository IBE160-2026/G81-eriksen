---
title: 'Story 2.3: Ola registrerer en gjennomført tur og ser den i historikken'
type: 'feature'
created: '2026-11-27'
status: 'done'
baseline_commit: 'e41bb3694ee4ae03cc08c3fbb9376a0ccafe012c'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-2-context.md'
  - '{project-root}/_bmad-output/planning-artifacts/ux-designs/ux-G81-eriksen-2026-11-06/EXPERIENCE.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Innlogget Ola kan ikke registrere en tur hun har gått eller finne den igjen (FR-16, FR-17, AR-5, AD-14, AR-14, NFR-8, UX-DR8, UX-DR27–29).

**Approach:** Ny modell `Registrering`, siden `/registrer/<tur_id>/` med validert skjema og engangstoken, og siden `/historikk/` med tabell over egne registreringer. `lastinn` nekter å la en tur med registreringer forsvinne.

## Boundaries & Constraints

**Always:**
- `Registrering`: `bruker` (FK, CASCADE), `tur` (FK, `on_delete=PROTECT`), `dato`, `brukt_tid_min`, `vanskelighet` (lett/moderat/vanskelig), `fornoydhet` (1–5), indeks for `(bruker, -dato, -id)`. Migrering `0004`, bare additiv (AD-15).
- «Registrer gjennomført tur» er sekundærknapp (lenke) på turforslaget, bare for innlogget; «Nytt forslag» er fortsatt primær. Knappen ligger inni `[data-tittel]` så fragmentbyttet tar den med.
- `/registrer/<tur_id>/` og `/historikk/` krever innlogging (`login_required`, gjest sendes til Logg inn med `next`; «rett tilbake» og krav om konto for gjest er story 2.5). Ukjent `tur_id` gir 404. Tur-ID tas alltid fra URL-en, aldri fra økta (AR-7).
- Skjema: Turoppsummering øverst (navn, nivå, form, lengde, estimert tid), «Alle fire felt er påkrevd.», dato (`<input type="date">`, i dag forvalgt, `max` i dag, hjelpetekst «I dag eller tidligere»), brukt tid (`fieldset` «Brukt tid» med Timer og Minutter, `inputmode="numeric"`, hjelpetekst «10 min–24 t»), opplevd vanskelighet (Lett/Moderat/Vanskelig) og fornøydhet (1–5 med ankertekst «1 = ikke fornøyd, 5 = svært fornøyd») som Valggruppe med `fieldset` og `legend`. Knappene «Registrer gjennomført tur» (primær) og «Avbryt» (sekundær, til Historikk). Sidetittel «Registrer gjennomført tur: {Turnavn}».
- Validering (Mikrotekst, [ASSUMPTION]): «Velg datoen du gikk turen», «Datoen kan ikke være frem i tid», «Brukt tid må være mellom 10 minutter og 24 timer», «Velg hvor vanskelig turen føltes», «Velg hvor fornøyd du var». Ingen nedre grense på dato. Timer og Minutter: begge tomme = mangler; bare ett utfylt = det andre er 0; totalt 10–1440 min. Ved feil lagres ingenting, feilen står ved feltet, og fokus går til første felt med feil (rekkefølge: dato, timer, minutter, vanskelighet, fornøydhet).
- Engangstoken (AD-14): lages ved visning (GET) og ligger i økta i en egen nøkkel (ikke `session["sok"]`), følger skjemaet som skjult felt. Første gyldige POST med riktig token lagrer og forbruker det; brukt eller ukjent token sender til Historikk uten å lagre. Ugyldig skjema beholder tokenet. Sammenlign med `secrets.compare_digest`. Ingen `flush`/`cycle_key`/`clear`.
- Gyldig skjema: lagre, redirect (PRG) til `/historikk/` med Melding (suksess) «Turen er registrert i historikken din.» som får fokus (messages-mønsteret fra «Du er logget ut.»).
- Historikk: h1 «Historikk», `<table>` i `<div role="region" aria-label="Historikk" tabindex="0">` (ruller sidelengs under 720 px), én rad per registrering, nyeste først (`-dato`, `-id`), også når samme tur er gått flere ganger. Kolonner: Tur (`<th scope="row">`, Nivåmerke under), Dato («7. nov.»), Brukt tid («1 t 50 min» med «estimert ca. …» fra turen under), Opplevd vanskelighet, Fornøydhet («5 av 5»), og skjult overskrift «Handlinger» (kolonnen er tom til 2.4). Under tabellen: «Nye søk prioriterer turer du ikke har gått.» Tom historikk: Tilstandspanel «Du har ikke registrert noen turer ennå.» med «Finn tur».
- Alt hentes filtrert på `request.user` (NFR-8). «Historikk» i toppmenyen mellom «Finn tur» og «Konto», med `aria-current` på siden.
- `lastinn`: mangler en tur som har registreringer i `turer.geojson`, stopper kommandoen med `CommandError` som navngir turen, før noe lagres. Turer uten registreringer beholder dagens advarsel.
- Formatering i `domene/tekst.py` (views formaterer ikke): brukt tid uten «ca.», dato «7. nov.», «5 av 5», vanskelighetstekst, «estimert ca. …». Views importerer ikke `domene`-formatering.

**Omfang:** Hannah valgte å beholde 2.3 som én story (ikke delt).

**Never:**
- ingen «Åpne som turforslag» (2.4), ingen krav-om-konto-flyt for gjest (2.5), ingen sletting av konto (2.6), ingen fremgangslinje, ingen vurderingslogikk (`vurder_historikk`, Epic 3);
- ingen endring av `velg_turer`, `okt.py`s `session["sok"]`, CSP, `Bruker` eller innloggingsgrensen;
- ingen ny JS-fil; skjemaet virker uten JS (AR-18).

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Gyldig registrering | innlogget, alle felt, riktig token | `Registrering` lagret for meg og turen, redirect til Historikk med suksessmelding i fokus | N/A |
| Mangler felt | tomt dato/tid/vanskelighet/fornøydhet | ingenting lagres, feil ved feltet, fokus på første feil | 200 med skjema |
| Dato frem i tid | dato i morgen | «Datoen kan ikke være frem i tid» | 200 med skjema |
| Brukt tid utenfor 10–1440 min | 5 min / 24 t 1 min / ikke-tall | «Brukt tid må være mellom 10 minutter og 24 timer» | 200 med skjema |
| Dobbeltinnsending | samme skjema/token to ganger | én registrering; andre POST → Historikk uten lagring | N/A |
| Ukjent token | feil eller manglende token | Historikk, ingenting lagres | N/A |
| Ukjent tur | `/registrer/finnes-ikke/` | 404 | N/A |
| Gjest | `/registrer/…`, `/historikk/` uinnlogget | redirect til Logg inn med `next` | N/A |
| Andres data | to brukere | Historikk viser bare egne rader | N/A |
| Samme tur flere ganger | to registreringer | to rader, nyeste først | N/A |
| Tom historikk | ingen registreringer | Tilstandspanel med «Finn tur» | N/A |
| `lastinn` | tur med registrering mangler i fila | `CommandError` med tur-ID, ingenting lagret | tur uten registrering: advarsel som før |

</frozen-after-approval>

## Code Map

- `turforslag/models.py`, `migrations/0004_registrering.py` -- ny modell; `tests/web/test_bruker.py::MigreringTest` krever migrering.
- `turforslag/forms.py` -- `RegistreringForm` (dato, timer, minutter, vanskelighet, fornoydhet; `i_dag` inn; `forste_feil` for fokus); mønster fra `SokForm`.
- `turforslag/views.py`, `urls.py` -- `registrer`, `historikk` (`login_required`, `never_cache`, PRG, messages); `turforslag/okt.py` eller egen modul for tokenet.
- `turforslag/templates/turforslag/` -- `registrer.html`, `historikk.html`, ny `_valggruppe.html`, evt. `_nivamerke.html` (nivåmerket er i dag inline i `_forslag_innhold.html`); `_forslag_innhold.html` (`.forslag-knapper`, kommentaren «Registrer … kommer i Epic 2»); `base.html` (meny, `meny_historikk`-blokk); `_melding.html`, `_tekstfelt.html` (trenger `min`/`max`), `_feltfeil.html`.
- `turforslag/static/css/side.css` -- ingen tabell-, Valggruppe- eller Turoppsummering-CSS finnes; DESIGN.md `valggruppe` og Historikk (~l.537).
- `domene/tekst.py` -- `formater_tid`, `formater_dato`, `formater_niva` finnes; legg til brukt tid uten «ca.», «7. nov.», «5 av 5», vanskelighetstekst og en visningsdataklasse for Historikk-rad.
- `turforslag/management/commands/lastinn.py`, `turdata.py` -- `Lagret.mangler_i_fila` gir i dag bare advarsel; `tests/web/test_lastinn.py:140` skal fortsatt passe for tur uten registrering.
- `tests/web/test_konto.py` (meny: `["/", "/konto/"]` må bli `["/", "/historikk/", "/konto/"]`), `test_grunnoppsett.py`, `tests/web/testturer.py`, `tests/domene/test_tekst.py`.
- Ikke endre: `session["sok"]`/`okt.py`-logikk, `velg_turer`, `LoggInnForm`, `_tilstandspanel.html` for forslag.

## Tasks & Acceptance

**Execution:**
- [x] `turforslag/models.py`, `migrations/0004_...` -- `Registrering`
- [x] `domene/tekst.py` + `tests/domene/test_tekst.py` -- formatering for Historikk og Turoppsummering
- [x] `turforslag/forms.py`, `views.py`, `urls.py`, token -- registrering, validering, engangstoken, Historikk, filtrering på bruker
- [x] `turforslag/templates/`, `static/css/side.css` -- skjema, Valggruppe, tabell, tomtilstand, meny, knapp på turforslaget
- [x] `turforslag/management/commands/lastinn.py` -- stopp når tur med registreringer mangler
- [x] `tests/web/` -- hver rad i matrisen, to brukere, token, 404, gjest, meny, `lastinn`, tekstjusteringer

**Acceptance Criteria:**
- Given innlogget bruker på et turforslag, when hun trykker «Registrer gjennomført tur», then siden `/registrer/<tur_id>/` åpnes med Turoppsummering og de fire feltene.
- Given gyldig skjema, when det sendes (også to ganger), then det finnes én `Registrering`, og hun er på Historikk med «Turen er registrert i historikken din.» i fokus.
- Given Historikk, then tabellen viser bare egne registreringer, nyeste først, og er en ekte tabell i en rullbar region.

## Implementation Notes

- Implementert av subagent; 599 tester, ruff og `makemigrations --check` grønne før review. Nye moduler: `turforslag/engangstoken.py` (10 nyeste tokens i egen sesjonsnøkkel), `turforslag/registrering.py`; `_nivamerke.html` trukket ut av `_forslag_innhold.html`.
- Fornøydhet har ankerteksten «1 = ikke fornøyd, 5 = svært fornøyd» som hjelpetekst (`aria-describedby`), ikke egne etiketter under 1 og 5.
- Chrome-sjekk gjort lokalt: skjema og feil (fokus på første felt med feil), gyldig registrering med dobbeltklikk gir én rad, Historikk med suksessmelding i fokus, tabell i rullbar region, knappen på turforslaget. Ikke testet: viewport under 720 px.

## Spec Change Log

## Review Triage Log

- patch/low: `date.fromisoformat` godtar andre formater og år 0001 — streng YYYY-MM-DD og minimum 1900.
- avvist: token for tur A kan postes til tur B (bare egen registrering; tur-ID fra URL per AR-7); token forbrukt før `lagre` feiler (bruker prøver på nytt fra GET); melding forbrukt av HEAD (nettlesere sender ikke HEAD); feilplassering på Timer når bare Minutter er fylt ut; `lastinn` TOCTOU (én operatør); `lastinn`-vakt vs docstring (AD-3 punkt 4 krever vakten); hardkodet «10 min–24 t»; manglende `aria-describedby` på enkeltfeltene i Brukt tid.
- avvist (spec): stille redirect ved brukt/ukjent token er spesifisert (AD-14); dato uten år er spesifisert («7. nov.»); estimert tid fra turen er valgt og dokumentert.
- defer: samtidig dobbel POST mot DB-lagret økt kan gi to registreringer (klienten sperrer dobbeltklikk); ingen `CheckConstraint` på `fornoydhet`/`brukt_tid_min`; Historikk uten paginering; år i datoen når historikken spenner over flere år; `historikk` konsumerer alle meldinger.

## Design Notes

Valg tatt uten spørsmål: knappen vises bare for innlogget (gjesteflyt = 2.5); ukjent tur gir 404; ingen nedre dato; «Avbryt» går til Historikk; estimert tid hentes fra turen (endres hvis `lastinn` endrer turen); tom handlingskolonne til 2.4; token i egen sesjonsnøkkel.

## Verification

**Commands:**
- `venv/Scripts/python.exe manage.py makemigrations --check --dry-run` -- expected: ingen endringer
- `venv/Scripts/python.exe manage.py test` -- expected: alle tester grønne
- `venv/Scripts/python.exe -m ruff check . && venv/Scripts/python.exe -m ruff format --check .` -- expected: ingen feil

**Manual checks (if no CLI):**
- Chrome lokalt: registrer tur, dobbeltklikk, se Historikk smalt og bredt, tastaturfokus til første feil.
