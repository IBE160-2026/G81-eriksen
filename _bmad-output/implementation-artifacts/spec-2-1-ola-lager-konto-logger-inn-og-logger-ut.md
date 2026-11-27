---
title: 'Story 2.1: Ola lager konto, logger inn og logger ut'
type: 'feature'
created: '2026-11-27'
status: 'done'
baseline_commit: 'ac69cb42506e162dcdb363f6aa54b40d6820a29f'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-2-context.md'
  - '{project-root}/_bmad-output/planning-artifacts/ux-designs/ux-G81-eriksen-2026-11-06/EXPERIENCE.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Ola er alltid gjest. Hun kan ikke lage konto, logge inn eller ut, så turene hennes kan ikke knyttes til henne senere (FR-14, AR-9, NFR-5, NFR-8, UX-DR3, UX-DR26, UX-DR30).

**Approach:** Bruk den eksisterende `Bruker`-modellen (e-post som brukernavn, ingen ny migrering) og Djangos `login()`/`logout()`. Nye visninger Logg inn, Lag konto og Konto, toppmeny som skiller gjest og innlogget, og «Vis passord» i `forbedring.js`.

## Boundaries & Constraints

**Always:**
- Egne skjema (ikke `UserCreationForm`/`AuthenticationForm`) med Mikrotekst fra EXPERIENCE.md; norske feiltekster. Skjemaene bruker `novalidate`, `autocomplete` som i AC, og virker uten JS (AR-18).
- Ruter i `turforslag`: `logg-inn/`, `lag-konto/`, `konto/` (krever innlogging; gjest sendes til Logg inn med `next`), `logg-ut/` (bare POST). Sett `LOGIN_URL`. Allerede innlogget som åpner Logg inn/Lag konto, sendes til Søk.
- `next` valideres med `url_has_allowed_host_and_scheme(allowed_hosts={request.get_host()}, require_https=request.is_secure())`; ellers Søk (NFR-8). Gjelder både innlogging og kontooppretting.
- E-post trimmes og lagres med små bokstaver; passord kun som hash; min. 8 tegn (eksisterende validator). `login()` beholder økta, så gjestens turforslag er uendret (AR-7). Innlogging varer to uker (standard `SESSION_COOKIE_AGE`), ingen inaktivitetsgrense (AD-6, AR-8).
- Innloggingsfeil: Melding (feil) «Feil e-post eller passord» uten å si hvilket felt; e-posten står i feltet, passordet tømmes. E-post som finnes fra før: Melding (feil) «Kunne ikke lage konto – prøv å logge inn», ingen konto lages. Ugyldig e-post og kort passord gir feil ved feltet («Skriv inn e-postadressen din», «E-postadressen må ha med @, for eksempel ola@eksempel.no», «Passordet må ha minst 8 tegn»; [ASSUMPTION] i Mikrotekst).
- Logg ut: POST, `logout()`, så `messages.info`/suksess «Du er logget ut.» på Søk som `_melding` med `fokus=True`.
- Toppmeny: gjest = logo + «Logg inn»; innlogget = logo + «Finn tur» + «Konto». «Historikk» kommer i 2.3. `aria-current` følger siden.
- Konto: e-post, `h2` «Personvern» med personverntekst fra Mikrotekst, knappen «Logg ut».
- «Vis passord» lages av `forbedring.js` (ren forbedring, ingen ny JS-fil, CSP uendret). Nivåtakmeldingen fra 1.12: teksten «Som ny bruker …» og lenken «Lag konto» vises bare for gjester; innlogget får en nøytral variant uten kontoløfte (inntil historikk i 2.3) (beslutning: Hannah, alternativ a).
- Views er tynne og importerer ikke `domene`; `okt.py` er fortsatt eneste som rører `session["sok"]`.

**Never:**
- ingen ny migrering, ingen endring av `Bruker`/`0001`;
- ingen Innloggingsforsok/grense (2.2), Historikk/Registrering (2.3–2.4), krav om konto med retur (2.5), «Slett konto» (2.6);
- ingen flush/cycle_key/clear utenom Djangos `login()`/`logout()`;
- ingen endring av `velg_turer`, kart.js, CSP eller passordvalidatorer.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Lag konto | ny e-post (store bokstaver), passord ≥ 8 | konto med e-post i små bokstaver, innlogget, redirect til `next` eller Søk; gjestens forslag uendret | N/A |
| E-post finnes | eksisterende e-post | Melding (feil) «Kunne ikke lage konto – prøv å logge inn», ingen ny konto | 200 med skjema |
| Ugyldig felt | e-post uten @ / passord < 8 | feil ved feltet, e-post bevart | 200 med skjema |
| Logg inn | riktig e-post (ulik case) + passord | innlogget, redirect til `next` eller Søk | N/A |
| Feil innlogging | feil e-post eller passord | «Feil e-post eller passord», e-post bevart | 200 med skjema |
| Åpen redirect | `next=https://annet.no/` | Søk | N/A |
| Logg ut | POST som innlogget | økta tømt, Søk med «Du er logget ut.» i fokus | GET gir 405 |
| Konto som gjest | GET `konto/` | redirect til Logg inn med `next=/konto/` | N/A |

</frozen-after-approval>

## Code Map

- `turforslag/models.py` -- `Bruker` finnes (email unik, lowercased i manager/save). Ikke endre.
- `config/settings.py` -- legg til `LOGIN_URL`; sesjon/hashers/validatorer uendret.
- `turforslag/urls.py`, `views.py`, `forms.py` -- nye ruter/views/skjema; følg 1.9–1.12-mønster (PRG, `@require_http_methods`, `FEIL_*`-konstanter, `aria-describedby`).
- `turforslag/templates/base.html` -- toppmeny (i dag bare logo); `logo_aktiv`-blokk og `aria-current` flyttes til «Finn tur» (kommentar i `sok.html`).
- `turforslag/templates/turforslag/_melding.html`, `_feltfeil.html`, `sok.html` -- gjenbruk for feil og «Du er logget ut.» (`fokus=True`, mønster fra `FORSLAG_UTILGJENGELIG`).
- `turforslag/templates/turforslag/_tilstandspanel.html` (~l.26–28) -- lenke «Lag konto» for gjest.
- `turforslag/static/forbedring.js` -- legg til «Vis passord» (ES5, IIFE); `static/css/side.css` -- input-stil mangler, `.skjemafelt`, `.knapp-primaer`, `.handlingslenke` finnes.
- `turforslag/okt.py` -- ikke endre; `tests/web/test_grunnoppsett.py`, `test_sider.py` -- toppmenytester må justeres; `tests/web/test_bruker.py` -- modelltester finnes.
- `EXPERIENCE.md` Mikrotekst l.159–180 -- tekstkilde; skriv [ASSUMPTION]-kommentar der teksten ikke er godkjent.

## Tasks & Acceptance

**Execution:**
- [x] `turforslag/forms.py` -- `LoggInnForm`, `LagKontoForm` med Mikrotekst-feil -- AC 1–4
- [x] `turforslag/views.py`, `urls.py`, `config/settings.py` -- logg-inn, lag-konto, konto, logg-ut, `next`-sjekk, `LOGIN_URL` -- AC 1–8
- [x] `turforslag/templates/` -- `logg_inn.html`, `lag_konto.html`, `konto.html`, toppmeny i `base.html`, lenke i `_tilstandspanel.html` -- UX-DR3, UX-DR26, UX-DR30
- [x] `turforslag/static/forbedring.js`, `side.css` -- «Vis passord», input-stil
- [x] `tests/web/test_konto.py` (+ justerte menytester) -- kontooppretting, duplikat, feil innlogging, utlogging, `next` til annet nettsted, turforslag beholdt gjennom innlogging (NFR-6), toppmeny gjest/innlogget, Konto som gjest, 405 på GET logg-ut, JS-kildesjekk

**Acceptance Criteria:**
- Given skjermen Logg inn/Lag konto, when den åpnes fra «Logg inn», then feltene, autocomplete, knapper og lenke «Har du ikke konto? Lag konto» (og «Minst 8 tegn» på Lag konto) er som i epics.md, og skjemaene virker uten JS.
- Given innlogget bruker, when hun ser toppmenyen, then den viser logo, «Finn tur» og «Konto»; gjest ser logo og «Logg inn».
- Given Konto, then den viser e-post, `h2` «Personvern» med personverntekst og «Logg ut» (POST).
- Given gjest med turforslag, when hun logger inn eller lager konto, then forslaget er det samme.

## Implementation Notes

- Implementert av subagent; 548 tester og ruff grønne etter review-patcher.
- [ASSUMPTION]-tekster som Hannah bør godkjenne: «Jeg foreslår bare grønne turer foreløpig.» (innlogget nivåtak), «Passordet kan ha høyst 128 tegn», «Har du allerede konto? Logg inn».
- Chrome-sjekk («Vis passord», fokus på «Du er logget ut.», `next` til annet nettsted, visuell stil/axe) er ikke gjort.

## Spec Change Log

## Review Triage Log

- patch/medium: innlogget nivåtak ikke rendret-testet (verification-gap) — test lagt til.
- patch/medium: «Logg inn» aria-current på Lag konto — blokk fjernet.
- patch/medium: ingen max_length på passord/e-post — satt 128/254.
- patch/low: konto/logg inn uten never_cache — lagt på.
- patch/low: logg_ut uten innlogging viste «Du er logget ut.» — redirect uten melding.
- patch/low: feilkant på avkrysningsboks; bfcache-synk av «Vis passord» — rettet.
- false: case-sensitiv duplikatsjekk — `BrukerManager.normalize_email` lowercaser hele adressen (models.py:15).
- false: `forEach` ikke ES5 — brukes fra før i forbedring.js.
- false/avvist: kontoopplisting (FR-14 krever teksten); forsøksgrense (story 2.2); innlogget med `next` går til Søk (spec); `next` til /logg-ut/ og gjenstående utloggingsmelding ved ugyldig POST (usannsynlig, fiks ville legge til grener).
- defer: tester for IntegrityError-race og meldingsfokus-rekkefølge; meny for innlogget på 500/403-sider.

## Design Notes

Valg tatt uten spørsmål (ikke synlige for Ola): to separate URL-er for Logg inn og Lag konto, innlogget bruker på dem sendes til Søk, innloggingsfeil som Melding (feil), «Vis passord» på begge skjema.

## Verification

**Commands:**
- `venv/Scripts/python.exe manage.py test` -- expected: alle tester grønne
- `venv/Scripts/python.exe -m ruff check . && venv/Scripts/python.exe -m ruff format --check .` -- expected: ingen feil

**Manual checks (if no CLI):**
- Chrome: opprett konto, logg ut, logg inn, «Vis passord», fokus på «Du er logget ut.», `next` til annet nettsted.
