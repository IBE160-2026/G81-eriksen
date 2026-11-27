# Epic 2 Context: Ola lager konto og registrerer turene sine

<!-- Compiled from planning artifacts. Edit freely. Regenerate with compile-epic-context if planning docs change. -->

## Goal

Gjesten lager konto uten å miste turforslaget, logger inn og ut, registrerer gjennomførte turer med vurdering, ser historikken, åpner en tur fra historikken som turforslag og kan slette kontoen og alle dataene. Innloggingen har en grense for mislykkede forsøk, og registreringen tåler dobbeltklikk. Vurderingene som lagres her, er grunnlaget for nivåtaket i Epic 3. Epic 1 er levert, og Epic 2 bygger på søkeflyten og Tilstandspanelet derfra.

## Stories

- Story 2.1: Ola lager konto, logger inn og logger ut
- Story 2.2: Innloggingen har en grense for mislykkede forsøk
- Story 2.3: Ola registrerer en gjennomført tur og ser den i historikken
- Story 2.4: Ola åpner en tur fra historikken
- Story 2.5: Gjesten blir bedt om å logge inn og kommer rett tilbake
- Story 2.6: Ola sletter kontoen

## Requirements & Constraints

- **Konto:**
  - E-post og passord, passordet minst 8 tegn og lagret bare som hash. E-post lagres med små bokstaver.
  - Duplisert e-post gir en melding om at kontoen ikke kunne lages, med forslag om å logge inn.
  - Feil innlogging sier aldri hvilket felt som er feil, og e-posten står igjen i feltet.
  - Innloggingen varer i to uker uten inaktivitetsgrense. Utlogging er en POST-knapp på Konto.
  - Gjestens turforslag og søk beholdes gjennom oppretting og innlogging.
- **Innloggingsgrense:** 5 mislykkede forsøk med samme e-post på 15 minutter sperrer nye forsøk med den e-posten, også for e-poster uten konto, og meldingen avslører ikke om kontoen finnes. Vellykket innlogging sletter forsøkene.
- **`next`-adresser:** adresser til andre nettsteder avvises, og brukeren sendes til Søk.
- **Registrering:**
  - Dato (ikke frem i tid, i dag forvalgt), brukt tid (10 min–24 t), opplevd vanskelighet (lett, moderat, vanskelig) og fornøydhet (1–5). Alle felt er påkrevd.
  - Feil gir ingen lagring, feilen står ved feltet, og fokus går til første felt med feil.
  - Dobbeltklikk eller dobbel POST gir bare én registrering.
- **Historikk:**
  - Nyeste først, én rad per registrering (også når samme tur er gått flere ganger), og brukt tid vises sammen med estimert tid.
  - Brukeren ser bare sine egne data. Alt hentes filtrert på `request.user`.
- **Turforslag fra historikken:**
  - Vises med «Fra historikken din» i stedet for søkeoppsummeringen, uten Turtype-treff og med «Finn en ny tur» i stedet for «Nytt forslag».
  - Begrunnelsen kommer fra en fast mal uten KI («Begrunnelse fra mal»).
  - Turer over nivåtaket kan åpnes, men får en infomelding. Til Epic 3 er nivåtaket grønt for alle.
  - Åpningen endrer ikke et pågående søk.
- **Sletting:**
  - Bekreftes på en egen side, og «Avbryt» endrer ingenting.
  - Bruker og registreringer slettes i én transaksjon, deretter `logout()` og kvittering på Søk. Feiler transaksjonen, slettes ingenting og brukeren får en feilmelding med «Prøv igjen».
- **Personvern:** Konto viser personverntekst, og personopplysninger lagres i EU (Neon i Frankfurt).
- **Tester:** kontooppretting, duplikat, feil innlogging, utlogging, `next` til annet nettsted, grensen og at den slutter, dobbel registrering, andres data, sletting, avbryt og feil i transaksjon.
- **Epic 1-kravene gjelder fortsatt:** WCAG 2.1 AA, reflow ved 320 px, trykkflater på minst 44 × 44 px, tastaturflyt, axe-core i PR-en, sporbarhet til FR-, NFR-, AR- og UX-DR-ID-er, all brukertekst ordrett fra Mikrotekst i `EXPERIENCE.md`.

## Technical Decisions

- **Brukermodell:** `turforslag.Bruker` arver `AbstractUser` med `USERNAME_FIELD="email"`, uten `username`, `first_name` og `last_name`, og med egen manager. Den ligger allerede i første migrering. Passordvalidering er bare minimumslengde 8.
- **Innloggingsgrense:**
  - Modellen `Innloggingsforsok(epost, tidspunkt)` lagrer også forsøk for ukjente e-poster.
  - En ren funksjon i `domene/` avgjør sperren, får tidspunktene og klokkeslettet inn, og kjøres før `authenticate()`.
  - `INNLOGGING_MAKS_FORSOK` og `INNLOGGING_SPERRETID_MIN` ligger i `settings`, så tester kan senke dem.
  - Forsøk eldre enn sperretiden slettes ved hver sjekk.
- **`Registrering`:** `on_delete=PROTECT` mot `Tur`, og en bruker-FK som slettes sammen med brukeren. Tur-ID kommer alltid fra URL-en (`/registrer/<tur_id>/`), aldri fra økten.
- **`lastinn`:** stopper med melding om en tur med registreringer mangler i `turer.geojson`, og sletter ingenting.
- **Engangstoken:** lagres i økten når skjemaet vises og brukes opp ved første gyldige POST. Et brukt eller ukjent token lagrer ingenting og sender til Historikk.
- **Økt og innlogging:**
  - Djangos `login()` beholder økten og dermed gjestens søk. `logout()` tømmer den.
  - `flush()`, `cycle_key()` og `clear()` kalles aldri direkte, og `turforslag/okt.py` er fortsatt eneste som leser og skriver `"sok"`.
  - En utløpt innlogging sender til Logg inn med `next` og tilbake til samme side.
- **Lag:** `domene/` er ren Python. Views regner og formaterer ikke, og formatering ligger i `domene/tekst.py`. Alle POST følger PRG med CSRF.
- **JS:** bare `forbedring.js` (blant annet «Vis passord»). Skjemaene virker uten JS.
- **CSP, database og konvensjoner:**
  - CSP uten inline-skript og `style`-attributter.
  - Samme ORM for SQLite og Neon, og migreringer som bare legger til.
  - Norske identifikatorer uten æ/ø/å.
  - Tester med `venv/Scripts/python.exe manage.py test`, og lint med `ruff check` og `ruff format --check`.

## UX & Interaction Patterns

- **Toppmeny:** gjester ser logo og «Logg inn». Innloggede ser logo, «Finn tur», «Historikk» (fra 2.3) og «Konto». «Logg ut» står på Konto, ikke i menyen.
- **Logg inn / Lag konto:**
  - Én rute med to visninger («Logg inn» er standard) og én primærknapp i hver («Logg inn», «Lag konto og fortsett»).
  - Feil står under feltet.
  - Ved krav om konto vises Turoppsummering, «Logg inn for å registrere», «Turforslaget er tatt vare på.» og «Tilbake til turforslaget».
- **Registrer gjennomført tur:** egen side, ikke dialog. Turoppsummering øverst, `fieldset` og `legend` for Brukt tid og for Valggruppene, og etter lagring Historikk med suksessmelding som får fokus.
- **Historikktabell:**
  - Ekte `<table>` med `<th scope="row">` for Tur og skjult overskrift «Handlinger».
  - Handlingene har skjulte tillegg med turnavn og dato.
  - Under 720 px ruller tabellen sidelengs i en `role="region"`-beholder med `tabindex="0"`.
  - Tom historikk viser Tilstandspanel med «Finn tur».
- **Sletting:** «Slett konto» (Konto) og «Slett kontoen» (bekreftelsessiden) står på ulike steder. Siden har ingen rød flate og ber ikke om e-post. Etter sletting og utlogging får «Kontoen din er slettet.» fokus.
- **Utlogging:** «Du er logget ut.» på Søk får fokus.
- **Meldinger:** aldri toast. Nivåtakmeldingen for gjester (1.12) får lenken «Lag konto».
- **Utløpt innlogging:** tekst finnes i Mikrotekst. Om utfylte felt beholdes, avgjøres og dokumenteres i story 2.5.

## Cross-Story Dependencies

- **Rekkefølge:** 2.1 → 2.2 (kobler seg på innloggingen) → 2.3 → 2.4 → 2.5 → 2.6. 2.3 legger «Historikk» i menyen. 2.5 bruker registreringssiden fra 2.3 og `next`-sjekken fra 2.1.
- **Fra Epic 1:**
  - 2.1 legger «Lag konto»-lenken i nivåtakmeldingen fra 1.12.
  - 2.3 og 2.5 legger «Registrer gjennomført tur» (sekundærknapp) på turforslaget fra 1.9–1.11.
  - 2.4 bruker `forslag.html` og kartet (`window.YNAKart.start`), og må ikke endre `Soketilstand`.
- **Til senere epics:**
  - Epic 3 bytter nivåtaket i 2.4 til taket fra historikken og leser `Registrering` via `vurder_historikk`.
  - Epic 4 gir KI-begrunnelser, men turforslag fra historikken beholder malen.
  - Epic 5 gir bekledningstips for i dag på turforslag fra historikken.
  - 6.4 viser fremgang i Historikk.
- **`lastinn`:** `Registrering.tur` med `PROTECT` begrenser hvordan turer kan fjernes fra `turer.geojson`.
