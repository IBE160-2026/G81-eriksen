---
title: 'Story 2.6: Ola sletter kontoen'
type: 'feature'
created: '2026-11-27'
status: 'done'
baseline_commit: 'f007f904b6142d95b570321fb236f49e4ae988f5'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-2-context.md'
  - '{project-root}/_bmad-output/planning-artifacts/ux-designs/ux-G81-eriksen-2026-11-06/EXPERIENCE.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Ola kan lage konto, men ikke slette den og alt hun har registrert. Hun bestemmer ikke over dataene sine (FR-15, AR-9, NFR-5, NFR-8, UX-DR30).

**Approach:** «Slett konto» på Konto fører til en egen bekreftelsesside. «Slett kontoen» sletter bruker, e-post, passord-hash, registreringer og innloggingsforsøk i én transaksjon, kaller `logout()` og sender henne til Søk med «Kontoen din er slettet.».

## Boundaries & Constraints

**Always:**
- Ny adresse `/konto/slett/` (`login_required`, `never_cache`, `require_http_methods` GET/HEAD/POST). GET viser bekreftelsessiden uten sideeffekt; POST sletter. Ikke innlogget POST (for eksempel dobbeltklikk etter sletting) gir redirect til Søk uten melding, som `logg_ut`.
- «Slett konto» på Konto er en lenke (`.handlingslenke`, minst 44 px) i egen seksjon under «Logg ut», uten rød flate.
- Bekreftelsessiden: `h1` «Vil du slette kontoen?» (som Historikk, `tabindex="-1"`), teksten «All historikken din slettes for godt, og det kan ikke angres.», primærknappen «Slett kontoen» (POST med CSRF) og «Avbryt» (lenke til Konto, ingenting endret). «Slett kontoen» står ikke på samme sted som «Slett konto» på Konto. Ingen rød flate, ingen advarselsikon, ingen passord- eller e-postfelt. Menypunktet «Konto» er aktivt.
- Slettingen ligger i ny modul `turforslag/kontosletting.py` (views importerer ikke `domene`, `turdata` eller `models`): i én `transaction.atomic()` slettes alle `Innloggingsforsok` for brukerens e-post (e-posten tas fra brukeren før sletting) og brukeren, og registreringene følger med (CASCADE). Etter at transaksjonen er fullført kalles `logout()`, deretter `messages.success` med nøkkelen `SLETTET`, og redirect (PRG) til Søk.
- Søk viser Melding (suksess) «Kontoen din er slettet.» med fokus, bare én gang; den kolliderer ikke med «Du er logget ut.» eller «Turforslaget er ikke lenger tilgjengelig» (bare én `data-fokus` per side).
- Feiler slettingen, rulles alt tilbake: ingenting slettes, brukeren er fortsatt innlogget, bekreftelsessiden vises på nytt (status 200) med Melding (feil) «Kontoen ble ikke slettet. Prøv igjen.» ([ASSUMPTION], legges i Mikrotekst). «Slett kontoen» står igjen og er selve «Prøv igjen».
- Andre brukeres data og innloggingsforsøk påvirkes ikke (NFR-8). Andre økter for samme bruker (annen enhet) ryddes ikke aktivt; de blir ugyldige fordi brukeren ikke finnes.
- Ingen `flush`/`cycle_key`/`clear` direkte; bare `logout()`.

**Never:**
- ingen ny migrering eller innstilling, ingen endring av `Registrering`, `Bruker` eller `okt.py`;
- ingen krav om passord eller e-post, ingen e-post om sletting, ingen «angre» eller karensperiode;
- ingen blokkering av `is_staff`-brukere (kan slette seg selv; dokumentert som utsatt);
- ingen endring av innloggingsgrensen, `next`-sjekken eller registreringsflyten.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Åpne bekreftelse | innlogget, GET `/konto/slett/` | h1, tekst, «Slett kontoen» (POST), «Avbryt» til Konto, ingen felt; ingenting endres | N/A |
| Slett | innlogget, POST | bruker, registreringer og innloggingsforsøk for e-posten slettet i én transaksjon, `logout()`, redirect til Søk med «Kontoen din er slettet.» i fokus | N/A |
| Melding bare én gang | last Søk på nytt | meldingen er borte | N/A |
| Avbryt | klikk «Avbryt» | Konto, ingenting endret | N/A |
| Feil i transaksjonen | `delete` kaster | ingenting slettet, fortsatt innlogget, 200 med Melding (feil) «Kontoen ble ikke slettet. Prøv igjen.» | rollback |
| Annen brukers data | to brukere | bare egen bruker, registreringer og forsøk slettes | N/A |
| Gjest | uinnlogget GET | redirect til Logg inn med `next=/konto/slett/` | N/A |
| Dobbel POST | andre POST etter sletting | redirect til Søk uten melding | N/A |
| GET endrer ikke | GET `/konto/slett/` | bruker og data uendret | N/A |

</frozen-after-approval>

## Code Map

- `turforslag/templates/turforslag/konto.html` -- har e-post, «Personvern» og «Logg ut» (kommentar: «Slett konto» kommer i 2.6); legg til lenken i egen seksjon.
- `turforslag/views.py`, `urls.py` -- `konto`, `logg_ut` (mønster: `require_POST`, `logout()`, `messages.success(UTLOGGET)`), `UTLOGGET`-konstanten; legg til `slett_konto`-view og `SLETTET`; lagdelingstesten `ViewsLagdelingTest` (`tests/web/test_forslag.py`) forbyr domene/models/turdata og `objects.` i views.
- `turforslag/kontosletting.py` (ny) -- `slett_konto(bruker)` i `transaction.atomic()`; bruker `innloggingsgrense.slett_forsok(epost)`; `Registrering.bruker` er CASCADE.
- `turforslag/templates/turforslag/slett_konto.html` (ny), `sok.html` (`utlogget`/`utilgjengelig`-grener, `_melding.html` med `fokus=True`).
- `turforslag/static/css/side.css` -- `.handlingslenke`, `.knapp-primaer`, `.knapp-sekundaer`; ingen rød variant skal lages.
- `EXPERIENCE.md` Mikrotekst -- legg inn «Kontoen ble ikke slettet. Prøv igjen.» som [ASSUMPTION].
- `tests/web/test_konto.py` (`KontoTest`, `lag_ola()`, `logg_inn()`, mønster fra `test_logg_ut_er_post_og_gir_melding_med_fokus`), `tests/web/test_registrering.py` (`RegistreringTestBase`), `test_konto_viser_epost_personvern_og_logg_ut` utvides med lenken.
- `deferred-work.md` -- legg inn: `is_staff`-bruker kan slette seg selv (siste superbruker); andre økter ryddes ikke.
- Ikke endre: `okt.py`, `Registrering`, `Bruker`, innloggingsgrense og registreringsflyt.

## Tasks & Acceptance

**Execution:**
- [x] `turforslag/kontosletting.py` -- sletting i én transaksjon
- [x] `turforslag/views.py`, `urls.py` -- `slett_konto`, `SLETTET`, feilhåndtering, dobbel POST
- [x] `turforslag/templates/` -- `slett_konto.html`, lenke i `konto.html`, melding i `sok.html`
- [x] `EXPERIENCE.md`, `deferred-work.md` -- ny Mikrotekst og utsatte punkter
- [x] `tests/web/` -- hver rad i matrisen (sletting, avbryt, feil i transaksjonen med rollback, annen brukers data, dobbel POST, melding én gang)

**Acceptance Criteria:**
- Given Konto, when jeg trykker «Slett konto», then en egen side med «Vil du slette kontoen?», teksten, «Slett kontoen» og «Avbryt» åpnes, uten felt og uten rød flate.
- Given bekreftelsessiden, when jeg trykker «Slett kontoen», then bruker, registreringer og innloggingsforsøk er slettet, og jeg er på Søk som gjest med «Kontoen din er slettet.» i fokus.
- Given at slettingen feiler, then ingenting er slettet og jeg får en feilmelding med «Prøv igjen».
- Given en annen bruker, then dens data er uberørt.

## Implementation Notes

- Implementert av subagent; 626 tester, ruff og `makemigrations --check` grønne. `turforslag/kontosletting.py` (én `transaction.atomic()`), `slett_konto`-view med manuell `is_authenticated`-sjekk (gjest GET → Logg inn med `next`, gjest POST → Søk uten melding), bred `except Exception` med `logger.exception` og 200-rerendring ved feil; `SLETTET` i `sok.html`; `deferred-work.md` og `EXPERIENCE.md` oppdatert.

- Chrome lokalt: Konto med lenken «Slett konto» under «Logg ut»; bekreftelsessiden uten felt, rød flate eller ikon; «Slett kontoen» ga Søk som gjest med «Kontoen din er slettet.» i fokus og menyen «Logg inn»; bruker og registrering var borte fra databasen. Ikke prøvd i nettleser: «Avbryt», feil i transaksjonen, axe og 44 px (dekket av tester der det går).

## Spec Change Log

## Review Triage Log

- false: testimporter mangler — testklassen kjører (626 grønne); e-post i `Innloggingsforsok` er normalisert (lagres fra `LoggInnForm`), så rydding treffer.
- false: ingen varsling ved feil — `_melding.html` type feil har `role="alert"`.
- avvist: `logout()`/melding feiler etter commit; samtidige POST-er (dobbel POST er spesifisert og testet sekvensielt); `request.user` halvmodifisert etter rollback (Collector endrer pk først etter vellykket sletting); manglende PRG ved feil (200-rerendring er spesifisert); ikon i feilmeldingen (standard Melding, ikke advarselsikon på bekreftelsen); manuell `is_authenticated` i stedet for `login_required` (oppførsel som i matrisen); 405/CSRF/HEAD-tester (dekket av Django-dekoratorer/middleware); `<section>` uten overskrift.
- defer (allerede i deferred-work.md): `is_staff` kan slette seg selv; andre økter ryddes ikke.

## Design Notes

Valg tatt uten spørsmål: innloggingsforsøk for e-posten slettes også (personopplysning, NFR-5); GET viser bekreftelse, POST sletter; feilmelding er tekst uten egen knapp; `is_staff` kan slette seg selv (utsatt); dobbel POST gir stille redirect til Søk; ingen migrering.

## Verification

**Commands:**
- `venv/Scripts/python.exe manage.py makemigrations --check --dry-run` -- expected: ingen endringer
- `venv/Scripts/python.exe manage.py test` -- expected: alle tester grønne
- `venv/Scripts/python.exe -m ruff check . && venv/Scripts/python.exe -m ruff format --check .` -- expected: ingen feil

**Manual checks (if no CLI):**
- Chrome lokalt: lag konto og registrer en tur, slett kontoen, se «Kontoen din er slettet.» i fokus, forsøk å logge inn igjen (feil), kontroller at «Avbryt» går til Konto.
