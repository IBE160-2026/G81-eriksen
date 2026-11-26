---
title: 'Story 1.9: Ola søker og får ett turforslag'
type: 'feature'
created: '2026-11-26'
status: 'done'
baseline_commit: 'b88856ae17981e4dfdc4d61f8dbc203051540cdd'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-1-context.md'
  - '{project-root}/_bmad-output/planning-artifacts/ux-designs/ux-G81-eriksen-2026-11-06/EXPERIENCE.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Søk-siden har bare en overskrift. Ola kan ikke fylle ut varighet og dato og få et turforslag, selv om `velg_turer` (1.8) og de 15 turene (1.7) finnes (FR-4, FR-5, FR-6, FR-7, FR-12, FR-13).

**Approach:** Søkeskjemaet sendes med POST, valideres på serveren og kjører `velg_turer` med grønt nivåtak. Søketilstanden med frosset rangering lagres i økten under en tilfeldig søke-ID, og Ola sendes videre til `/forslag/<sok_id>/` (PRG). Forslagssiden viser første tur med Nivåmerke, Formmerke, Faktarute, begrunnelse fra reservemalen og Forklaringspanel. All tekst og formatering kommer fra `domene/`.

**Beslutning (Hannah, 2026-11-26):** 1.9 viser en enkel versjon av statusene som ikke er vanlige treff (1A). 1.12 legger til endringsforslagene.
- `TOPPTUR_ERSTATTET`: utsiktsturen vises som et vanlig forslag, med merket «Utsikt i stedet for topptur» og Melding (advarsel) «Ingen topptur passer søket ditt» rett etter turnavnet.
- `INGEN_TREFF`: et Tilstandspanel (`h1`) på forslagssiden med tittelen «Jeg fant ingen tur som passer søket ditt» fra Mikrotekst (raden «Ingen treff», [ASSUMPTION]) og bare «Endre søk». «Prøv å endre søket:» kommer med endringsforslagene i 1.12. *(Rettet 2026-11-26 etter review, godkjent av Hannah: «Vi fant …» fra wireframen brøt med jeg-formen og Mikrotekst.)*
- `BARE_OVER_NIVATAK`: et Tilstandspanel med tittelen «Ingen grønne turer passer søket», gjesteteksten fra Mikrotekst og bare «Endre søk». Ingen tur over nivåtaket vises.
- Sidetittelen for et Tilstandspanel er «{tittel} – Your Next Adventure».

Spec-en beholdes hel (ca. 3700 tokens).

## Boundaries & Constraints

**Always:**
- **Søk** (`/`):
  - `h1` «Hvor lang tid har du?» (klasse `display`), ingressen og feltene i rekkefølgen fra DESIGN.md (:529).
  - Varighet er en `<select>` med «Velg» og 23 valg, 1–12 t i halvtimessteg, bygget av konstantene i `domene/sok.py`.
  - Dato er en `<select>` med 31 dager, fra i dag til og med i dag + 30, med i dag forvalgt.
  - Turtype er Turtypekort: en ekte radiogruppe med «Alle turtyper» forvalgt.
  - Startpunkt har «Alle startpunkt» og bare startpunkter som har turer, sortert på navn, med hjelpeteksten om Oslo-området.
  - Det finnes ikke noe fritekstfelt.
- **Tekst:** all tekst er ordrett fra EXPERIENCE.md › Mikrotekst. Ved avvik gjelder Mikrotekst over mockupene. Tekster merket [ASSUMPTION] brukes og får en kommentar `{# [ASSUMPTION] Mikrotekst #}` i malen.
- **Validering** skjer på serveren med et Django-skjema.
  - Feil vises under feltet med «!», `aria-invalid="true"` og `aria-describedby="<feil-id> <hint-id>"`. Det første ugyldige feltet får `autofocus`.
  - Tekster: «Velg varighet» og «Velg en dato fra i dag til {dato om 30 dager}».
  - Ved manipulert turtype eller startpunkt: «Velg en turtype fra listen» og «Velg et startpunkt fra listen», begge [ASSUMPTION].
  - Ingen manipulert POST krasjer. Dagens dato er `timezone.localdate()` og sendes inn i `domene/`.
- **Økt:** bare `turforslag/okt.py` leser og skriver `request.session["sok"]`, alltid hele verdien, med de 10 nyeste søkene.
  - Søke-ID-en lages med `secrets.token_urlsafe`.
  - `flush()`, `cycle_key()` og `clear()` brukes aldri.
  - En ny POST gir alltid ny søke-ID, så to faner har hvert sitt forslag.
  - Søket står aldri i URL-en.
- **`domene/okt.py` `Soketilstand`:**
  - Feltene er `sok`, `status`, `rangerte_tur_ider` (frosset), `viste_tur_ider`, `gjeldende_tur_id` og `nivaheving=False`.
  - `til_dict()` og `fra_dict()` lagrer datoen som en ISO-streng.
  - `fra_dict` tåler at felt som kommer senere (KI), mangler.
- **Forslag** (`/forslag/<sok_id>/`, GET):
  - Den viser alltid `gjeldende_tur_id` uten å rangere på nytt, så en ny innlasting gir samme tur.
  - DOM-rekkefølgen følger AC-en: søkeoppsummering med «Endre søk», turnavn `h1`, Nivåmerke med nivåforklaring, Turtype-treff (bare når en turtype er valgt), Formmerke, «Start: …», Faktarute, ut.no-lenke, KI-merke, `h2` «Begrunnelse» og Forklaringspanel.
  - Faktaruta viser tiden med «pauser ikke inkludert».
  - ut.no-lenken er skjult når turen ikke har URL. Den åpnes i samme fane, med det skjulte tillegget fra Mikrotekst.
  - KI-merket er «Begrunnelse fra mal».
  - Forklaringspanelet er en `<details>`, lukket som standard, med setning 1 og 2.
  - Sidetittelen er «{Turnavn} – Turforslag – Your Next Adventure».
- **Ukjent søke-ID eller tur:** Ola sendes til Søk (PRG). Der vises Melding (info) «Turforslaget er ikke lenger tilgjengelig. Søk på nytt for å få et forslag.» under `h1`, med fokus via `data-fokus`.
- **«Endre søk»** er en lenke til `/?sok=<sok_id>`. Søk fylles da ut fra søketilstanden. En ukjent ID gir et tomt skjema uten feil.
- **Reservemalen:** `domene/begrunnelse.py` `reservebegrunnelse(sok, tur) -> str`. Den nevner varigheten og eventuell turtype, er høyst 300 tegn og nevner aldri fritekst. Eksempel: «Turen tar ca. 2 t og har utsikt, som du ba om».
- **Lagdeling:**
  - Views regner, filtrerer og formaterer ingenting selv.
  - Formatering ligger i `domene/tekst.py`: valglistene for varighet og dato, søkeoppsummeringen («Lørdag 7. nov. · 2 t · Utsikt»), form, turtype-treff og høydemeter.
  - Ingen `style`-attributter og ingen inline-skript. CSS ligger i `static/css/side.css` med tokens, og trykkflatene er minst 44 × 44 px.

**Never:**
- Ingen kart (1.10), knapper for nytt forslag eller registrering (1.11 og Epic 2), endringsforslag eller nivåtekster for innloggede (1.12), KI (4.5) eller fritekst (4.6).
- Ingen nye pakker, ingen JSON-svar, ingen nye JS-filer og ingen endring av modeller eller migreringer.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Første visning | GET `/` | skjemaet med standardvalg, 23 varigheter, 31 datoer og startpunkter med turer | N/A |
| Mangler varighet | POST uten varighet | 200 med skjemaet. «Velg varighet» med «!», `aria-invalid` og `aria-describedby`, og `autofocus` på Varighet | ingen lagring |
| Manipulert POST | dato i går eller +31, turtype `fjell`, startpunkt `ukjent`, varighet `45` | feil ved riktig felt | ingen krasj, ingen lagring |
| Gyldig søk | 3 t, i dag | 302 til `/forslag/<id>/`, og økten har tilstanden | N/A |
| Elleve søk | 11 gyldige POST-er | økten har de 10 nyeste, og den eldste ID-en blir ukjent | N/A |
| Ny innlasting | GET `/forslag/<id>/` to ganger | samme tur | N/A |
| To faner | to POST-er med ulike søk | to ID-er, og hver viser sitt forslag | N/A |
| Ukjent ID | GET `/forslag/finnes-ikke/` | 302 til Søk med meldingen og fokus | N/A |
| Turen er slettet | tilstanden peker på en tur som ikke finnes | som ukjent ID | N/A |
| Endre søk | GET `/?sok=<id>` | skjemaet fylt ut med søket | ukjent ID gir et tomt skjema |
| Uten URL | tur uten `ut_no_url` | ingen ut.no-lenke | N/A |
| Topptur erstattet | topptur 2,5 t, ingen topptur passer, en utsiktstur gjør det | utsiktsturen med merke og melding | N/A |
| Ingen treff | topptur 2 t, grønt tak | Tilstandspanel «Jeg fant ingen tur som passer søket ditt» og «Endre søk» | N/A |
| Bare over nivåtaket | søk der bare blå turer passer | Tilstandspanel «Ingen grønne turer passer søket» med gjesteteksten, og ingen tur | N/A |

</frozen-after-approval>

## Code Map

- `turforslag/urls.py:7-9` -- bare `""` → `views.sok`. Legg til `forslag/<str:sok_id>/`.
- `turforslag/views.py:5-8` -- `sok` er `@require_safe`. Den blir GET og POST (`require_http_methods`). `tests/web/test_sider.py:24` venter i dag 405 på POST og må endres.
- `turforslag/turdata.py:215` -- `tur_fra_modell` (bruk `select_related("startpunkt")`).
- `turforslag/models.py:73-130` -- `Startpunkt` og `Tur` (relasjonsnavnet for turer på startpunktet står i modellen).
- `turforslag/templates/base.html` -- blokkene `tittel` (:6), `logo_aktiv` og `innhold`. `_melding.html` er Melding med `fokus`.
- `static/forbedring.js` -- dobbeltinnsending og `[data-fokus]`. Den endres ikke.
- `config/settings.py` -- CSP (:95-102), CSRF og `TIME_ZONE=Europe/Oslo` med `USE_TZ`. Øktene ligger i databasen (ingen `SESSION_*`).
- `domene/sok.py` (konstantene og `Sok`), `domene/utvalg.py` (`velg_turer`, `NIVATAK_UTEN_HISTORIKK`), `domene/tekst.py:18-42` (`formater_tid`, `formater_lengde_totalt`, `formater_niva`). Legg nye formateringer til her.
- Spinen AD-5 (:100-110), AD-2 (:62) og konvensjonene (:212-216).
- EXPERIENCE.md › Mikrotekst (:98-158), Component Patterns (:196-214) og DOM-rekkefølgen for Turforslag (:253-264). DESIGN.md (:518-596). Mockupene `key-sok.html` og `key-turforslag.html`. Mikrotekst gjelder ved avvik.
- `tests/web/test_turdata.py:21` -- legger inn turer fra fixturen. `test_grunnoppsett.py` sjekker CSS og maler statisk (ingen farger i maler, 44 px).

## Tasks & Acceptance

**Execution:**
- [x] `domene/okt.py` -- `Soketilstand` med `til_dict()` og `fra_dict()` -- AD-5
- [x] `domene/tekst.py` -- formateringene: varighetsvalg («1 t», «1,5 t» … som `<option>`-tekst etter Mikrotekst), datovalg («Lørdag 7. november», [ASSUMPTION]), `datoperiode(i_dag)` med 31 datoer, søkeoppsummering, form, turtype-treff og høydemeter -- FR-4, FR-6
- [x] `domene/begrunnelse.py` -- `reservebegrunnelse` -- FR-12, FR-13
- [x] `turforslag/forms.py` -- `SokForm(i_dag, startpunkter)` med valgene og feilmeldingene -- FR-4, NFR-2
- [x] `turforslag/okt.py` -- `lagre_sok`, `hent_sok` og `nyeste_10` -- AD-5, AR-7
- [x] `turforslag/views.py`, `turforslag/urls.py` -- `sok` (GET, `?sok=`, POST og PRG) og `forslag` -- FR-5, FR-7
- [x] `turforslag/templates/turforslag/sok.html`, `forslag.html` og små includes, `static/css/side.css` -- komponentene etter DESIGN.md -- UX-DR6/7/10/11/12/16/17/19, NFR-3
- [x] `turforslag/templates/turforslag/_tilstandspanel.html` og visningen av `TOPPTUR_ERSTATTET` i `forslag.html` -- etter beslutningen -- FR-8
- [x] `_bmad-output/planning-artifacts/ux-designs/ux-G81-eriksen-2026-11-06/EXPERIENCE.md` › Mikrotekst -- radene «Feil i søket, manipulert turtype/startpunkt» med «Velg en turtype fra listen» og «Velg et startpunkt fra listen» [ASSUMPTION] -- PRD §0 (Mikrotekst gjelder for ordlyd)
- [x] `tests/domene/test_okt.py`, `test_begrunnelse.py`, utvidet `test_tekst.py`; `tests/web/test_sok.py`, `test_forslag.py`; endret `test_sider.py` -- én test per rad i matrisen, og en test som viser at views ikke importerer formaterings- eller beregningsfunksjoner direkte -- AR-2, SM-2

**Acceptance Criteria:**
- Gitt de nye sidene, når `python manage.py test` kjøres, så er alle testene grønne (2 hoppes over lokalt).
- Gitt en kjørende server med de 15 turene, når Søk og et forslag åpnes i 360 px bredde i Chrome, så synes turnivå, estimert tid og Turtype-treff uten rulling.
- Gitt samme visning, når axe-core kjøres mot begge sidene (injisert via Chrome DevTools, fordi ingen pakke er lagt til), så har de ingen alvorlige eller kritiske brudd. Resultatet legges i PR-en.

## Verification

**Commands:**
- `venv/Scripts/python.exe manage.py test` -- forventet: alle grønne, 2 hoppet over
- `venv/Scripts/python.exe -m ruff check . && venv/Scripts/python.exe -m ruff format --check .` -- forventet: ingen funn
- Kjør aldri `uv run` i repoet.

**Manual checks:**
- Søk → forslag → ny innlasting → «Endre søk» i Chrome, med og uten JS. Sjekk 360 px og tastaturflyten. Kjør axe-core.

## Implementation Notes

- Manuelle sjekker 2026-11-26 i Chrome (lokal server med de 15 turene). Kjørt etter presentasjonen, med Hannahs godkjenning til å åpne Chrome og laste ned axe-core:
  - **360 px:** Chrome på Windows kan ikke gjøre vinduet smalere enn ca. 500 px. Siden ble derfor målt i en `iframe` på 360 × 780 px. Forslaget (Fuglemyrhytta) har nivået nederst ved 240 px, Turtype-treff ved 325 px og tiden ved 458 px, altså uten rulling. Ingen av sidene har vannrett rulling, og ingen trykkflater er under 44 px.
  - **axe-core 4.10.2** (WCAG 2.1 A/AA og best practice, lastet midlertidig fra egen server og slettet etterpå): 0 brudd på Søk (33 beståtte regler), på forslaget «Dælivann rundt» (29) og på tilstandspanelet «Jeg fant ingen tur …» (28).
  - **Tastaturet:** Tab går inn i turtypegruppen, og piltasten velger «Marka» med synlig fokusring (2,4 px) og «Valgt». Enter uten varighet gir «Velg varighet» med «!», `aria-invalid`, `aria-describedby="varighet-feil varighet-hint"` og fokus i Varighet. Turtypen beholdes.
- `turforslag/sokflyt.py` er et nytt, tynt lag mellom views og `domene/` (ikke nevnt i spec-en), så `views.py` ikke importerer fra `domene/`.

## Spec Change Log

## Review Triage Log

Gjennomgang 2026-11-26 i tre lag (Blind Hunter = BH, Edge Case Hunter = ECH, Verification Gap = VG). Løkke 0.

| # | Lag | Funn | Vurdering | Begrunnelse | Rute |
|---|---|---|---|---|---|
| 1 | BH | Tittelen for ingen treff er «Vi fant …», men Mikrotekst (:138) og epics 1.12 (:764) har «Jeg fant …», og raden som ble lagt til, er en dublett | medium | Feilen lå i den låste blokken (planleggingen hentet tittelen fra wireframen). | intent_gap → Hannah rettet den låste blokken (alt. 1), patch |
| 2 | ECH | Et forslag i økten kan vise en tur som etter en ny `lastinn` har nivå over taket eller tid over varigheten | medium | `lastinn` oppdaterer eksisterende rader (1.6), og `forslagsvisning` sjekker ikke filtrene på nytt. Det bryter SM-C1. | patch |
| 3 | VG | Ingen test for startpunktet i søkeoppsummeringen på Tilstandspanelet | medium | Verifisert av VG: en regresjon i `sokflyt.py:36` ville gått gjennom. | patch |
| 4 | BH | `test_frosset_rangering_tross_nye_turer` legger ikke til nye turer | low | Navnet er misvisende. Det er en direkte retting. | patch |
| 5 | BH | Kommentaren i `forslag.html` viser til `domene/` (visning), som ikke finnes | low | Det er en direkte retting. | patch |
| 6 | ECH | Samtidig POST fra to faner kan miste et søk | low | Krever nesten samtidige innsendinger. Rettingen bryter AD-5 (én nøkkel, `"sok"`). | avvist |
| 7 | ECH, BH | Navnet på startpunktet slås opp blant startpunkter med turer, så det kan forsvinne | low | Startpunktet må ha mistet alle turene etter søket. Rettingen krever en ny hjelper. | avvist |
| 8 | ECH, BH | En HEAD-forespørsel kan sette eller spise meldingen «ikke lenger tilgjengelig», og nøkkelen ligger i messages | low | Lenkeforhåndsvisninger bruker GET. Ingen mal itererer over messages. | avvist |
| 9 | ECH, BH | `nivaheving` som strengen «false» blir True, og `fra_dict` sjekker ikke sammenhengen | false | Bare `turforslag/okt.py` skriver økten, og den skriver alltid `til_dict()`. | avvist |
| 10 | ECH, BH | Den norske sorteringen håndterer ikke aksenter eller «Aa» | low | Ingen av de 6 startpunktene har slike tegn. | avvist |
| 11 | ECH | `ut_no_url` valideres ikke | false | URL-ene kommer fra vår egen kuraterte liste (1.7). | avvist |
| 12 | ECH | Meldingen ved topptur kommer ikke «rett etter turnavnet» | false | DOM-rekkefølgen i EXPERIENCE.md (:253-264) plasserer meldinger etter Nivåmerke og Turtype-treff, og malen følger den. | avvist |
| 13 | ECH | Tekst er hardkodet i malene, ikke i `domene/` | false | Spec-en sier at Mikrotekst skal stå i malen med en kommentar for [ASSUMPTION]. `domene/` gjelder formatering. | avvist |
| 14 | BH | Det er ikke ført inn i EXPERIENCE at Forklaringspanelet bare har 2 punkter i Epic 1 | low | AC-en i epics 1.9 sier det («Setningen om KI kommer med KI i story 4.5»). | avvist |
| 15 | BH | Tittelen på Tilstandspanelet står både i tittelblokken og i panelet | low | Det er bare to steder, og rettingen er en omskriving. | avvist |
| 16 | BH | Hjelpetekstene «1–12 timer» og «30 dager» er literaler | low | Mikrotekst er kilden til ordlyden, og konstantene er låst av tester. | avvist |
| 17 | BH | Begrunnelsen og merket avgjør erstatning på to måter | false | Ved `TOPPTUR_ERSTATTET` er turene alltid utsikt uten topptur. Ved `TREFF` med topptur har turen topptur. De samsvarer. | avvist |
| 18 | BH | `tekst.py` er blitt en samlesekk | low | Det er arkitekturpynt uten konkret skade nå. | avvist |
| 19 | BH | «ca. 0 høydemeter» for flate turer | low | Den laveste turen har 6 hm, som gir «ca. 10». | avvist |
| 20 | BH | Testen for 300 tegn sjekker konstanten mot seg selv | low | Testen sjekker også alle søkene. Håndhevingen i KI hører til 4.5. | avvist |
| 21 | BH | Turtypekortene mangler fokusring uten `:has()` | low | Alle nåværende nettlesere støtter `:has()`. Det sjekkes manuelt i Chrome. | avvist |
