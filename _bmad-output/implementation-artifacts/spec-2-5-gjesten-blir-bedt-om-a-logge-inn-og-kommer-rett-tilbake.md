---
title: 'Story 2.5: Gjesten blir bedt om å logge inn og kommer rett tilbake'
type: 'feature'
created: '2026-11-27'
status: 'done'
baseline_commit: '6d115918fb234e04a9547acd8dedcb755b6f58fe'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-2-context.md'
  - '{project-root}/_bmad-output/planning-artifacts/ux-designs/ux-G81-eriksen-2026-11-06/EXPERIENCE.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Gjesten ser ikke «Registrer gjennomført tur», og når hun åpner en side som krever konto, får hun bare en vanlig innloggingsside uten å vite hvorfor eller hvor hun havner etterpå (FR-14, AD-6, AR-8, NFR-8, UX-DR26).

**Approach:** «Registrer gjennomført tur» vises også for gjester og fører til Logg inn / Lag konto med Turoppsummering, «Logg inn for å registrere», «Turforslaget er tatt vare på.» og «Tilbake til turforslaget». Etter innlogging eller ny konto går hun rett inn i registreringen av samme tur.

## Boundaries & Constraints

**Always:**
- Gjesteknappen (sekundær, samme sted som for innlogget) peker til `/logg-inn/?next=/registrer/<tur_id>/&sok=<sok_id>`; for innlogget er den uendret (`/registrer/<tur_id>/`). Tur-ID tas fra `next`-adressen, aldri fra økta (AR-7).
- `logg_inn` og `lag_konto` gjenkjenner at en trygg `next` peker til registreringsruten (`resolve()` på stien, ikke tekstmatching). Da vises: Turoppsummering (delmal trukket ut av `registrer.html`), h1/tekst «Logg inn for å registrere» og, når det finnes et gyldig `sok`, «Turforslaget er tatt vare på.» med lenken «Tilbake til turforslaget». Ukjent tur gir vanlig Logg inn/Lag konto uten oppsummering.
- `sok` er en rå id i URL-en. Den valideres med `okt.hent_sok(request, sok_id)`; bare da vises «tatt vare på» og lenken (bygd med `reverse`, ikke fra rå tekst). Ellers utelates begge. `okt.py` er fortsatt eneste som rører `session["sok"]`.
- `next` og `sok` bæres videre mellom «Logg inn» og «Lag konto» (krysslenkene og skjult felt), slik at «Tilbake til turforslaget» også virker etter bytte av visning.
- `next` valideres som i 2.1 (`_neste`: samme vert, ellers Søk). Etter innlogging eller opprettelse går hun til `/registrer/<tur_id>/`; `login()` beholder økta, så forslaget er det samme (AR-7).
- Gjest som åpner Historikk, Konto eller en registreringsside direkte sendes til Logg inn med `next` og tilbake dit etterpå (AD-6, AR-8); for registreringssiden vises Turoppsummering og «Logg inn for å registrere» (uten «tatt vare på» når `sok` mangler).
- Utløpt innlogging: økta er borte, og systemet kan ikke skille utløpt fra «aldri innlogget». Hun sendes til Logg inn med `next` og tilbake til samme side etterpå (AR-8), uten egen «Innlogging utløpt»-melding.
- Utfylte felt i registreringsskjemaet beholdes ikke når innloggingen har utløpt (avgjørelse: Hannah, alternativ a; Mikrotekst-linjen «…så tar jeg vare på det du har fylt inn» tas ut av v1); avgjørelsen dokumenteres i EXPERIENCE.md (Mikrotekst og åpent punkt) og ARCHITECTURE-SPINE.md.
- `login_required` beholdes på `registrer`, `historikk`, `historikk_tur` og `konto`; engangstokenet lages bare for innlogget.

**Never:**
- ingen ny URL for «krev konto»-siden, ingen ny modell eller migrering, ingen cookie/langtidsmarkør for å skille utløpt innlogging;
- ingen lagring av skjemadata for gjester, ingen bruk av `Referer`, ingen redirect bygd fra rå `sok_id` eller `tur_id`;
- ingen endring av innloggingsgrensen (2.2), `okt.py`-logikken, `next`-sjekken eller registreringsskjemaet (2.3);
- ingen sletting av konto (2.6).

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Gjest på turforslag | uinnlogget, forslag med `sok_id` | «Registrer gjennomført tur» vises (sekundær) og lenker til Logg inn med `next` og `sok` | N/A |
| Krav-om-konto-side | `/logg-inn/?next=/registrer/<tur>/&sok=<gyldig>` | Turoppsummering, «Logg inn for å registrere», «Turforslaget er tatt vare på.», «Tilbake til turforslaget» til samme forslag | N/A |
| Ukjent/utløpt `sok` | `sok` finnes ikke i økta | som over, men uten «tatt vare på» og uten «Tilbake»-lenke | N/A |
| Logg inn herfra | riktig e-post og passord | innlogget, rett inn i `/registrer/<tur>/`, forslaget i økta uendret | feil innlogging: som i 2.1/2.2, `next` og `sok` bevares |
| Lag konto herfra | ny e-post og passord ≥ 8 | konto, innlogget, rett inn i registreringen; krysslenken bærer `next` og `sok` | duplikat/ugyldig: som i 2.1 |
| Åpne registreringsside direkte | gjest på `/registrer/<tur>/` | redirect til Logg inn med `next`; Turoppsummering og «Logg inn for å registrere» uten «tatt vare på» | ukjent tur: 404 som før |
| Åpne Historikk/Konto direkte | gjest | Logg inn med `next`; tilbake dit etter innlogging | N/A |
| Utløpt innlogging | POST/GET mot side som krever konto uten økt | Logg inn med `next`, tilbake til siden etterpå; utfylte felt er tapt | N/A |
| Ekstern `next` | `next=https://annet.no/` | Søk etter innlogging | N/A |

</frozen-after-approval>

## Code Map

- `turforslag/templates/turforslag/_forslag_innhold.html` (~l.80–82: knapp bare for `user.is_authenticated`) -- vis også for gjest med lenke til Logg inn; `views.forslag` har `sok_id` i konteksten, `historikk_tur` har ikke (der er brukeren alltid innlogget).
- `turforslag/views.py` (`_neste`, `_etter_innlogging`, `_kontoside`, `logg_inn`, `lag_konto`, `registrer`) -- gjenkjenn registreringsruten i `next` med `resolve()`, valider `sok` med `okt.hent_sok`, send `oppsummering`/`sok_id` til malene; views importerer ikke domene/models/turdata (lagdelingstesten): hent oppsummering via `turforslag/registrering.py` (`oppsummering(tur_id)`).
- `turforslag/templates/turforslag/logg_inn.html`, `lag_konto.html` -- viser Turoppsummering, tekster og lenke; bærer `next` og `sok` videre (skjult felt og krysslenker).
- `turforslag/templates/turforslag/registrer.html` (Turoppsummering inline l.~11–19) -- trekk ut til `_turoppsummering.html` som begge sidene bruker.
- `turforslag/okt.py` -- `hent_sok` finnes; ikke endre.
- `EXPERIENCE.md` (Mikrotekst «Innlogging utløpt» l.~166, «Utfylte felt beholdes» l.~312, åpent punkt l.~494) og `ARCHITECTURE-SPINE.md` (l.~359) -- oppdater avgjørelsen.
- `tests/web/test_konto.py`, `test_registrering.py` (l.~78–92: gjest sees ikke knappen og redirect-forventning må justeres), `test_forslag.py` (l.~86 og ~1003), `test_grunnoppsett.py`.
- Ikke endre: `okt.py`, `Registrering`, `engangstoken.py`, `InnloggingsgrenseTest`, `LoggInnForm`-logikk.

## Tasks & Acceptance

**Execution:**
- [x] `turforslag/templates/turforslag/_turoppsummering.html`, `registrer.html` -- trekk ut Turoppsummering
- [x] `turforslag/views.py`, `registrering.py` -- gjenkjenn `next` til registreringsruten, valider `sok`, send oppsummering og `sok_id`
- [x] `turforslag/templates/` (`logg_inn`, `lag_konto`, `_forslag_innhold`) -- krav-om-konto-visning, «Tilbake til turforslaget», gjesteknapp, `next`/`sok` videre
- [x] `_bmad-output/planning-artifacts/.../EXPERIENCE.md`, `ARCHITECTURE-SPINE.md` -- dokumenter avgjørelsen om utløpt innlogging
- [x] `tests/web/` -- hver rad i matrisen, `next`-sjekk, gyldig/ugyldig `sok`, forslaget uendret, justering av eksisterende gjest-tester

**Acceptance Criteria:**
- Given et turforslag som gjest, when jeg trykker «Registrer gjennomført tur», then jeg ser Logg inn / Lag konto med Turoppsummering, «Logg inn for å registrere», «Turforslaget er tatt vare på.» og «Tilbake til turforslaget».
- Given den siden, when jeg logger inn eller lager konto, then jeg er i registreringen av samme tur, og forslaget er det samme.
- Given en gjest som åpner Historikk, Konto eller en registreringsside direkte, when hun logger inn, then hun er tilbake på siden; en `next` til et annet nettsted gir Søk.

## Implementation Notes

- Implementert av subagent; 619 tester, ruff og `makemigrations --check` grønne. `_krav_om_konto` i `views.py` (resolve() på stien i `next`, `sok` valideres med `okt.hent_sok`, «Tilbake»-lenke med `reverse`); `_turoppsummering.html` trukket ut; `EXPERIENCE.md` og `ARCHITECTURE-SPINE.md` oppdatert med avgjørelsen «utfylte felt beholdes ikke».
- Chrome lokalt: gjest søker, «Registrer gjennomført tur» (sekundær) → Logg inn for å registrere med Turoppsummering, «Turforslaget er tatt vare på.» og «Tilbake til turforslaget»; Lag konto bærer oppsummering og «Tilbake» videre; ny konto herfra gir rett inn i `/registrer/<tur>/`; innlogging på eksisterende konto herfra beholder forslaget (samme forslags-URL fungerer etterpå); testklient bekrefter det samme etter kontoopprettelse. Ikke prøvd i nettleser: «Tilbake»-lenken etter klikk, utløpt innlogging, ekstern `next` (dekket av tester).
- Gjest på `/registrer/<ukjent-tur>/` redirectes av `login_required` til Logg inn før 404-sjekken og ser vanlig Logg inn uten oppsummering.

## Spec Change Log

## Review Triage Log

- false: diffen er ufullstendig, `sok_id` mangler i konteksten — `views.forslag` hadde `sok_id` fra før; 619 tester (inkl. `KravOmKontoTest`) beviser flyten.
- false: delt cache kan servere gjesteknappen til innlogget — Django legger `Vary: Cookie` når økta leses, og `forslag` leser `request.user`.
- avvist: `sok` for annen tur enn `next` (krever at brukeren endrer adressen selv, påvirker bare egen økt); `sok` i URL (økt-token, ubrukelig uten økta; samme som `/?sok=`); lengdegrense på `sok`; `resolve()` med uvanlige stier (`url_has_allowed_host_and_scheme` er foran); utløpstest via `logout()` er likeverdig (anonym uten økt); `h1` «Lag konto» på Lag konto (spec: h1/tekst); skjøre tester (`split('/')`, hardkodet slug); Mikrotekst-kolonnen «Avgjort».
- avvist (spec): gjest på ukjent tur gir Logg inn uten oppsummering.

## Design Notes

Valg tatt uten spørsmål: ingen ny URL (Logg inn / Lag konto med to visninger, som i epic-konteksten); `sok` følger som GET-parameter og valideres mot økta; «tatt vare på» vises bare når forslaget faktisk finnes; ingen skille mellom utløpt og aldri innlogget (økta er borte, og et skille ville krevd en langtidscookie).

## Verification

**Commands:**
- `venv/Scripts/python.exe manage.py makemigrations --check --dry-run` -- expected: ingen endringer
- `venv/Scripts/python.exe manage.py test` -- expected: alle tester grønne
- `venv/Scripts/python.exe -m ruff check . && venv/Scripts/python.exe -m ruff format --check .` -- expected: ingen feil

**Manual checks (if no CLI):**
- Chrome lokalt: søk som gjest, trykk «Registrer gjennomført tur», se Turoppsummering, logg inn og havn i registreringen; «Tilbake til turforslaget» viser samme forslag.
