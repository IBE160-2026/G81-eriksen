---
title: 'Story 2.2: Innloggingen har en grense for mislykkede forsøk'
type: 'feature'
created: '2026-11-27'
status: 'done'
baseline_commit: '0a583aaca6f3a8f08a12024eb84817763232e6cc'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-2-context.md'
  - '{project-root}/_bmad-output/planning-artifacts/ux-designs/ux-G81-eriksen-2026-11-06/EXPERIENCE.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Innloggingen fra 2.1 har ingen grense, så noen kan prøve passord i det uendelige på den publiserte siden (AR-9, NFR-8, AR-2).

**Approach:** Ny modell `Innloggingsforsok(epost, tidspunkt)` og en ren funksjon i `domene/` som avgjør om e-posten er sperret. `logg_inn` sjekker sperren før `authenticate()`, lagrer mislykkede forsøk og sletter dem ved vellykket innlogging.

## Boundaries & Constraints

**Always:**
- `domene/innlogging.py` er ren Python (bare standardbiblioteket): `er_sperret(tidspunkter, na, maks_forsok, sperretid_min)` (navn kan justeres) får tidspunktene (aware `datetime`) og klokkeslettet inn og returnerer om e-posten er sperret. Sperret når minst `maks_forsok` tidspunkter er nyere enn `na − sperretid_min` (strengt nyere; et forsøk på akkurat sperretiden teller ikke lenger).
- `INNLOGGING_MAKS_FORSOK = 5` og `INNLOGGING_SPERRETID_MIN = 15` i `config/settings.py`. Viewet leser dem og sender dem inn; viewet kaller `timezone.now()` én gang.
- Modell `Innloggingsforsok`: `epost` (små bokstaver, indeksert), `tidspunkt` (`default=timezone.now`, `db_default` for bakoverkompatibilitet), indeks på `(epost, tidspunkt)`. Ny migrering `0003`, bare additiv (AD-15). Ingen admin.
- Rekkefølge i `logg_inn`: skjema gyldig og e-post oppgitt → slett alle forsøk eldre enn sperretiden (globalt, ikke bare for e-posten; personvern, NFR-5) → er e-posten sperret? → ellers `authenticate()`.
- Sperret: `authenticate()` kalles ikke, ingenting lagres (sperren forlenges ikke av nye forsøk), Melding (feil) «Det har vært for mange forsøk på å logge inn med denne e-postadressen. Vent 15 minutter, og prøv igjen.» (ordrett fra EXPERIENCE.md, teksten hardkodet), uten å si om e-posten har konto; e-posten står i feltet, passordet er tomt. Samme oppførsel for e-poster uten konto og for riktig passord mens sperret.
- Mislykket `authenticate()` lagrer ett forsøk med e-posten normalisert (små bokstaver), også når e-posten ikke har konto. Vellykket innlogging sletter alle forsøk for e-posten.
- Ugyldig skjema eller tom e-post lagres ikke og teller ikke; de gir fortsatt «Feil e-post eller passord» som i 2.1.
- Views importerer ikke `domene`-formatering utover den nye avgjørelsen; logikken for lagring/sletting ligger i en liten hjelper utenfor viewet om det passer (følg `okt.py`/`sokflyt.py`-mønsteret).

**Never:**
- ingen sperre på IP (AD-10), ingen sperre på Lag konto (utsatt), ingen CAPTCHA, ingen e-post om sperre;
- ingen låsing mot samtidige forsøk (akseptert: to parallelle forsøk kan gå ett over grensen);
- ingen rå SQL, ingen endring av `Bruker`, `login()`-flyt eller `next`-sjekk fra 2.1;
- ingen visning i admin.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Første feil | feil passord, 0 tidligere forsøk | «Feil e-post eller passord», ett forsøk lagret (små bokstaver) | N/A |
| Ukjent e-post | e-post uten konto, feil | samme melding, forsøk lagret | N/A |
| Fjerde → femte feil | 4 forsøk siste 15 min, feil passord | «Feil e-post eller passord», forsøk nr. 5 lagret | N/A |
| Grensen nådd | 5 forsøk siste 15 min, riktig eller feil passord | sperremelding, `authenticate()` kalles ikke, ingenting lagres, e-post bevart, passord tomt | 200 med skjema |
| Sperre likt | 5 forsøk, e-post uten konto / annen case | sperremelding uten å si om konto finnes; case teller likt | N/A |
| Sperren slutter | eldste av de fem er 15 min gammelt | innlogging mulig igjen | N/A |
| Vellykket | riktig passord under grensen | innlogget, forsøk for e-posten slettet | N/A |
| Ugyldig skjema | tom e-post / for lang | «Feil e-post eller passord», ingenting lagres | N/A |
| Opprydding | forsøk eldre enn sperretiden (også andre e-poster) | slettes ved neste sjekk | N/A |

</frozen-after-approval>

## Code Map

- `turforslag/views.py` (`logg_inn` ~l.133), `forms.py` (`LoggInnForm`, `FEIL_INNLOGGING`; ny konstant for sperremelding) -- legg sperre/lagring/sletting; `_melding.html` og `_tekstfelt.html` viser feil og tømmer passord allerede.
- `turforslag/models.py`, `migrations/0003_innloggingsforsok.py` -- ny modell; `tests/web/test_bruker.py::MigreringTest` krever at migreringen finnes.
- `domene/innlogging.py` (ny), `tests/domene/test_innlogging.py`; `tests/domene/test_bare_standardbibliotek.py` krever ren stdlib.
- `config/settings.py` -- `INNLOGGING_*`; testene bruker `override_settings`.
- `tests/web/test_konto.py` -- `KontoTest.logg_inn`, `lag_ola()`; sjekk at eksisterende tester ikke gjør 5+ feil mot samme e-post.
- Ikke endre: `okt.py`, `Bruker`, `next`-sjekk, `LagKontoForm`.

## Tasks & Acceptance

**Execution:**
- [x] `domene/innlogging.py` + `tests/domene/test_innlogging.py` -- ren avgjørelse; grense 4/5, kantcase 15 min, tom liste, lav grense -- AR-2
- [x] `turforslag/models.py`, `migrations/0003_...`, `config/settings.py` -- modell og innstillinger -- AR-9
- [x] `turforslag/views.py`, `forms.py` -- sperre før `authenticate()`, lagring, sletting, global opprydding, meldingstekst
- [x] `tests/web/test_konto.py` -- sperre etter 5, `authenticate` ikke kalt, ukjent e-post, case, sperre slutter, sletting ved suksess, ugyldig skjema teller ikke, opprydding av andre e-posters gamle forsøk
- [x] `_bmad-output/implementation-artifacts/deferred-work.md` -- legg inn: ingen sperre på Lag konto (kontoopplisting via duplikatmeldingen)

**Acceptance Criteria:**
- Given fem mislykkede forsøk med samme e-post siste 15 min, when jeg prøver igjen, then `authenticate()` kalles ikke og sperremeldingen vises uten å si om kontoen finnes.
- Given at 15 minutter er gått siden det eldste av de fem, when jeg prøver igjen, then innlogging er mulig.
- Given en vellykket innlogging, then forsøkene for e-posten er slettet.

## Implementation Notes

- Implementert av subagent; 564 tester, ruff og `makemigrations --check` grønne. Ny hjelper `turforslag/innloggingsgrense.py` (databasedelen) ved siden av `domene/innlogging.py`; `__str__` på modellen kreves av ruff (DJ008).
- Chrome-sjekk gjort lokalt: forsøk 1–5 gir «Feil e-post eller passord», forsøk 6 sperremeldingen (e-post uten konto, annen case), e-post bevart og passord tomt.

## Spec Change Log

## Review Triage Log

- patch/low: redundant `db_index` på `epost` ved siden av sammensatt indeks — fjernet.
- false: `timezone` ikke importert i views.py — importert (l.14).
- false: e-post ikke lowercaset — `LoggInnForm.clean_epost` → `BrukerManager.normalize_email` lowercaser hele adressen.
- false: `if epost:` er dødkode — `LoggInnForm` har `required=False`, så tom e-post passerer `is_valid()`; vakten trengs.
- avvist: sletting av forsøk før `login()` (login feiler ikke i praksis); samtidighet og målrettet utestenging (akseptert i spec); timing-forskjell (Djangos `authenticate`, samme som før); innstillinger leses i hjelper, ikke view (dokumentasjon); manglende «gjenstående tid» i melding (Mikrotekst er ordrett).
- defer: ingen sperre på admin-innlogging (`/admin/`, samme `Bruker`-kontoer); vekst i `Innloggingsforsok` ved flom av tilfeldige e-poster (opprydding kjører kun på innloggings-POST).

## Design Notes

Valg tatt uten spørsmål (ikke synlige for Ola): bare mislykket `authenticate()` teller; sperrede forsøk lagres ikke; opprydding er global; teksten hardkodet «15 minutter»; én sperre per e-post (kjent kompromiss: andre kan sperre Ola ute); ingen admin.

## Verification

**Commands:**
- `venv/Scripts/python.exe manage.py makemigrations --check --dry-run` -- expected: ingen endringer
- `venv/Scripts/python.exe manage.py test` -- expected: alle tester grønne
- `venv/Scripts/python.exe -m ruff check . && venv/Scripts/python.exe -m ruff format --check .` -- expected: ingen feil

**Manual checks (if no CLI):**
- Chrome lokalt: fem feil innlogginger, den sjette viser sperremeldingen med e-posten i feltet.
