---
title: 'Story 1.11: Ola kan be om nytt forslag'
type: 'feature'
created: '2026-11-26'
status: 'done'
baseline_commit: '65b3a2593888f19a2134d5981e2860d24a67d12a'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-1-context.md'
  - '{project-root}/_bmad-output/planning-artifacts/ux-designs/ux-G81-eriksen-2026-11-06/EXPERIENCE.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Turforslaget viser bare den første turen i søket. Frister den ikke, må Ola søke på nytt (FR-7, AR-7, UX-DR22–25, NFR-2, SM-2).

**Approach:**
- «Nytt forslag» er et POST-skjema med CSRF og PRG. Det går ett steg videre i den frosne rangeringen i økten og viser aldri en tur som alt er vist.
- Når alle er vist, kommer Tilstandspanel «alle vist» med «Start fra første forslag igjen» og «Endre søk».
- Med JS bytter `forbedring.js` innholdet med et HTML-fragment fra serveren. Uten JS blir det en vanlig sideinnlasting.

**Beslutninger (Hannah, 2026-11-26):**
1. **Lasteindikatoren (1A):** den vises på forslagssiden.
   - Søkeoppsummeringen står der med en gang.
   - Kartflaten viser «Kart lastes …» til første flis er lastet, med `aria-busy="true"` på kartflaten. Teksten står i `_kart.html` med `hidden`. `kart.js` viser den og setter `aria-busy` ved start, og skjuler den og fjerner `aria-busy` ved første `load` (eller ved flisfeil, der meldingen fra 1.10 tar over). Uten JS vises den aldri.
   - Ingen spinner, og ingen animasjon ved `prefers-reduced-motion`.
   - «Finner en tur med … …» ([ASSUMPTION]) brukes ikke. Søk-siden får ingen lasteblokk.
2. **Spec-en beholdes hel** (ca. 3000 tokens).

## Boundaries & Constraints

**Always:**
- Rangeringen leses bare fra `Soketilstand` i økten og rangeres aldri på nytt.
- Hver handling skriver hele `Soketilstand` på nytt via `turforslag/okt.py`. Det oppdaterte søket blir det nyeste av de 10.
- **Dobbeltklikk:** skjemaet sender gjeldende tur som skjult felt `tur`. Serveren går bare videre når `tur` er lik `gjeldende_tur_id`. Ellers sender den bare videre til GET, uten å endre noe.
- «Alle vist» er `gjeldende_tur_id = None` med status `TREFF` eller `TOPPTUR_ERSTATTET`, og alle i `rangerte_tur_ider` er vist. Det er ikke det samme som en ukjent søke-ID.
- En tur som ikke lenger finnes eller ikke består SM-C1-sjekken, hoppes over (markeres som vist).
- **Mikrotekst ordrett fra EXPERIENCE.md** (:112, :139–141). [ASSUMPTION]-tekster markeres i malen.
- **Ingressen:**
  - «Det var {antall} {turer} [med {turtype}] som passer {varighet}.» og «Vil du prøve noe annet?».
  - Antall 1–12 skrives med bokstaver («én tur», «fire turer»), og fra 13 med siffer.
  - Formuleringen ligger i en ren funksjon i `domene/tekst.py`.
- **Fragment:**
  - `fetch` sender POST med headeren `X-Fragment: 1` og følger redirecten.
  - `forslag` renderer bare innholdet i `<main>` (en ny partial) når headeren finnes. GET uten headeren er uendret.
  - Etter byttet kaller JS `window.YNAKart.start(element)` hvis det finnes et `[data-kart]`, setter `document.title` fra fragmentet og gir fokus til ny `h1`.
  - Feiler henting, sendes skjemaet vanlig.
- «Start fra første forslag igjen» er et vanlig POST-skjema uten fragment. Panelet har ikke `kart.js`.
- Views importerer ikke `domene` (testen gjelder fortsatt). Logikken ligger i `domene/okt.py` (rene funksjoner) og `turforslag/sokflyt.py`.
- CSP er uendret: ingen inline-skript og ingen `style`-attributter.

**Never:**
- ingen JSON-endepunkt og ingen ny JS-fil eller pakke;
- ingen endring i `velg_turer`;
- ingen endringsforslag (1.12);
- ingen knapp for «Registrer gjennomført tur» (Epic 2);
- `flush`, `cycle_key` og `clear` brukes ikke.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Neste | rangert A,B,C; vist A; gjeldende A; POST `tur=A` | gjeldende B, vist A,B; 302 til forslag | – |
| Siste | vist A,B,C; gjeldende C; POST `tur=C` | gjeldende None → «alle vist»-panel, «Det var tre turer …» | – |
| Dobbeltklikk | gjeldende B; POST `tur=A` (gammel) | ingen endring; 302 til forslag (viser B) | – |
| Start på nytt | «alle vist»; POST forfra | gjeldende A, vist A | – |
| Ny innlasting | GET etter neste | samme tur B, samme liste | – |
| Ukjent søk | POST eller GET med ukjent `sok_id` | 302 til Søk med «Turforslaget er ikke lenger tilgjengelig …» | ingen 500 |
| Manipulert | `tur` mangler, ukjent tur eller GET til POST-URL | ingen endring; 302 til forslag eller 405 for GET | ingen 500 |
| Borte tur | neste tur er slettet eller feiler SM-C1 | hoppes over; neste gyldige eller «alle vist» | – |
| Fragment | POST med `X-Fragment: 1` | 302, og GET med headeren gir bare innholdet i `<main>` | – |
| Én tur | rangert A; POST `tur=A` | «alle vist», «Det var én tur …» | – |

</frozen-after-approval>

## Code Map

- `domene/okt.py:17-80` -- `Soketilstand` (frozen) og `ny_soketilstand`.
  - Nye rene funksjoner: `neste_forslag(tilstand, fra_tur_id, gyldig: Callable[[str], bool])`, `start_pa_nytt(tilstand)` og `alle_vist(tilstand)`.
  - Bruk `dataclasses.replace`.
- `turforslag/okt.py:21-50` -- `hent_sok` og `lagre_sok`. Legg til `oppdater_sok(request, sok_id, tilstand)`, som flytter søket bakerst før `nyeste_10`.
- `turforslag/sokflyt.py:21-45` -- `utfor_sok` og `forslagsvisning`.
  - `forslagsvisning` returnerer i dag `None` når `gjeldende_tur_id` er `None` (:38). Den skal gi en visning med `alle_vist=True`, antall og ingress.
  - Legg til `nytt_forslag(tilstand, fra_tur_id)` og `forfra(tilstand)`, som bruker `turdata.hent_tur` og SM-C1-sjekken (:40-44) som `gyldig`.
- `domene/tekst.py:286` -- `Forslagsvisning`: legg til `alle_vist` og `ingress_alle_vist`. Ny funksjon `alle_vist_ingress(antall, turtype, varighet_min, status)`. Gjenbruk `formater_varighet_timer` (:161).
- `turforslag/views.py:19-70` og `turforslag/urls.py` -- nye `POST forslag/<sok_id>/nytt/` (`nytt_forslag`) og `POST forslag/<sok_id>/forfra/` (`forfra`), med `@require_POST` og PRG. `forslag` gir fragment-mal ved `X-Fragment: 1`.
- `turforslag/templates/turforslag/forslag.html` -- flytt innholdet i `<main>` til `_forslag_innhold.html`.
  - Skjemaet «Nytt forslag» (`knapp-primaer`, skjult `tur`) legges etter Kartbeskrivelse, slik rekkefølgen i EXPERIENCE.md :264 sier.
  - Tittelblokken må kunne leses fra fragmentet, for eksempel `data-tittel` på rotelementet.
  - Leaflet og `kart.js` lastes bare når siden har en tur (:20-26). Det er uendret.
- `turforslag/templates/turforslag/_tilstandspanel.html` -- «alle vist» har `h1`, ingress, skjemaet «Start fra første forslag igjen» og lenken «Endre søk» (`?sok=`).
- `turforslag/static/forbedring.js` -- ES5 IIFE.
  - Ny handler for `form[data-nytt-forslag]`. Den demper beholderen (klasse), setter `aria-busy`, skriver lasteteksten i en `aria-live="polite"`-region utenfor beholderen (i `base.html` eller `forslag.html`), sender med `fetch` og bytter innholdet.
  - Ved feil sendes skjemaet vanlig.
  - Gjenbruk sperren `data-sendes` mot dobbeltklikk.
- `turforslag/static/kart.js:6, :37, :90-100, :189` -- `fliser.on("loading"/"load")` finnes allerede (1.10): bruk `load` til å skjule «Kart lastes …» (1A). `YNAKart.start(element)` stopper og starter kartet på nytt. Det fikser fast `json_script`-id, fordi det gamle elementet er fjernet før `start` kalles.
- `turforslag/static/css/side.css:196-240, 1050-1080` -- knapper og tilstandspanel. Legg til en dempet tilstand (`[aria-busy="true"]`, opacity via token) og skru av overgangen ved reduced-motion.
- `tests/domene/test_okt.py`, `tests/web/test_forslag.py` (:47-81, :209, :442-460) og `tests/web/test_grunnoppsett.py` (`ForbedringTest` :603).
  - :80-81 sjekker at «Nytt forslag» ikke finnes. Det må nå snus.
  - CSRF-tester bruker `Client(enforce_csrf_checks=True)`.

## Tasks & Acceptance

**Execution:**
- [x] `domene/okt.py` + `tests/domene/test_okt.py` -- `neste_forslag`, `start_pa_nytt` og `alle_vist` med matrisetilfellene (neste, siste, dobbeltklikk, én tur, borte tur) -- ren logikk.
- [x] `domene/tekst.py` + test -- `alle_vist_ingress` (entall/flertall, tallord 1–12, med og uten turtype, topptur erstattet) og `Forslagsvisning.alle_vist` -- mikrotekst.
- [x] `turforslag/okt.py`, `turforslag/sokflyt.py` -- `oppdater_sok`, `nytt_forslag`, `forfra` og «alle vist» i `forslagsvisning`.
- [x] `turforslag/views.py`, `urls.py` + `tests/web/test_forslag.py` -- POST-viewene, fragmentmodus og matrisen ende til ende (CSRF håndheves, ny innlasting, manipulerte POST-er, 405 for GET).
- [x] maler (`forslag.html`, `_forslag_innhold.html`, `_tilstandspanel.html`) -- knapp, panel og `data-tittel`.
- [x] `forbedring.js`, `side.css` + tekstsjekker i `test_grunnoppsett.py` -- fragmentbytte, `aria-busy`, live-region, fokus, tittel og `YNAKart.start`.
- [x] `_kart.html`, `kart.js`, `side.css` + tekstsjekk -- «Kart lastes …» på kartflaten med `aria-busy` til første flis er lastet (beslutning 1A).

**Acceptance Criteria:**
- Gitt et turforslag med JS, når Ola trykker «Nytt forslag», så dempes det gamle forslaget, knappen beholder fokus, visningen får `aria-busy="true"` og «Finner et nytt forslag …» leses opp utenfor beholderen. Etter byttet er `document.title` «{Turnavn} – Turforslag – Your Next Adventure» (eller panelets `h1`), fokus står på ny `h1`, og kartet viser den nye ruten. Konsollen viser ingen CSP-brudd.
- Gitt samme flyt uten JS, når Ola trykker knappen, så gir en vanlig sideinnlasting samme resultat.
- Gitt Tilstandspanel «alle vist», når siden vises, så er `h1` «Du har sett alle turene som passer søket», med ingress med antallet, «Start fra første forslag igjen» og «Endre søk». Panelet fungerer med tastatur, og axe-core gir 0 brudd.

## Implementation Notes

- «Nytt forslag» står i `infokolonne-bunn` etter Forklaringspanel og **før** Kartbeskrivelse. Det følger EXPERIENCE.md :264 (punkt 9 før punkt 10) og testen som krever at Kartbeskrivelse står sist. Code Map sa «etter Kartbeskrivelse», men begrunnet det med samme liste.
- Rotelementet i fragmentet er `.forslag` eller `.tilstand` med `data-tittel` (fra `_tittel.html`). Live-regionen `[data-lastestatus]` står i `<main>` i `forslag.html`, utenfor rotelementet. `forbedring.js` bytter bare rotelementet.
- Ny token `--busy-opacity: 0.5` i `tokens.css`. Den finnes ikke i DESIGN.md-frontmatter ennå.
- `forslag` setter `Vary: X-Fragment`.

- **Hovedøkten (2026-11-26):** turtypen i ingressen er rettet til naturlig norsk: «turer med utsikt», «turer i marka» og «toppturer» (var «med marka» og «med topptur»).
- **Chrome lokalt (hovedøkten, 2026-11-26):**
  - Søk på 4 timer ga 9 treff.
  - Første «Nytt forslag» ble sendt med Enter på knappen. Mens hentingen pågikk, hadde `.forslag` `aria-busy="true"`, og «Finner et nytt forslag …» kom i live-regionen. Etter byttet var tittelen «Kolsåstoppen fra Gjettum – Turforslag – Your Next Adventure», og fokus sto på ny `h1`. Kartet ble startet på nytt med én `#kart-geojson` og én `.leaflet-container`, og `aria-busy` på kartflaten ble fjernet etter `load`.
  - Videre «Nytt forslag» viste alle de ni turene én gang hver. Så kom panelet «Du har sett alle turene som passer søket» med fokus på `h1` og ingressen «Det var ni turer som passer 4 timer. Vil du prøve noe annet?».
  - Ingen CSP-brudd underveis (`securitypolicyviolation`).
  - axe-core 4.10.2 (WCAG 2.1 A/AA) ga 0 brudd, både på panelet og på et turforslag.
  - Uten JS-håndtering (native `submit`): «Start fra første forslag igjen» ga første tur, og «Nytt forslag» ga neste. Ny innlasting ga samme tur.
  - Ved 360 px (srcdoc-iframe) var det ingen sidelengs rulling, og knappen var 306 × 44 px.

## Spec Change Log

## Review Triage Log

Første gjennomgang (2026-11-26). BH = Blind Hunter, EC = Edge Case Hunter, VG = Verification Gap.

| # | Funn (lag) | Verdikt | Begrunnelse | Rute |
|---|---|---|---|---|
| 1 | «Alle vist»-ingressen teller turer som ble hoppet over (slettet eller utenfor SM-C1) (VG, EC, BH) | medium | `tekst.forslagsvisning` bruker `len(rangerte_tur_ider)`. I `test_tur_som_ikke_lenger_passer_hoppes_over` ble én tur vist, men panelet sier «tre turer». | patch |
| 2 | Toppturformuleringen bygges med `str.replace`, og entall («én topptur») er ikke testet (VG, BH) | low | Sletting av `.replace(" tur", " topptur")` lar alle testene passere. | patch |
| 3 | En synkron feil i `hentForslag` etter `preventDefault` gjør skjemaet dødt (BH) | low | Den ytre `catch` sender ikke skjemaet, og sperren står. | patch |
| 4 | `forfra` når alle turene i rangeringen er borte, er ikke testet (BH) | low | Bare en manglende første tur er testet. | patch |
| 5 | `--busy-opacity` mangler i DESIGN.md (BH) | low | Kommentaren i `tokens.css` sier det selv. | patch |
| 6 | Navnet `alle_vist` brukes både om funksjonen og feltet i `domene/tekst.py` (BH) | low | Det virker, men er lett å lese feil i `forslagsvisning`. | patch |
| 7 | Fragmentbyttet og «Kart lastes …» er bare testet som tekst i kildekoden (VG, BH) | medium | Repoet har ingen JS-runner. Chrome-sjekken i Implementation Notes er verifiseringen. | defer |
| 8 | Det gamle Leaflet-kartet ryddes ikke ved bytte (EC, BH) | low | Den frakoblede instansen beholder resize-lytteren. Brukeren merker det ikke (høyst 15 per søk), og fiksen krever ny `YNAKart.stopp` og endret test. | avvist |
| 9 | Ingen timeout eller abort på `fetch` (BH) | low | Nettleseren har egen timeout. Fiksen gir mer kode. | avvist |
| 10 | Svaret sjekkes ikke mot forslags-URL, og flash-meldingen brukes opp (BH) | low | Det virker i dag (Søk har ingen `[data-tittel]`, og serveren legger meldingen inn på nytt). Det er sjeldent. | avvist |
| 11 | Feiler både `fetch` og reserveinnsendingen (offline), står siden dempet (EC) | false | Offline viser nettleseren sin feilside ved innsendingen. | avvist |
| 12 | «Kart lastes …» kan bli stående hvis `load` aldri kommer (EC) | low | Kartflaten har alltid størrelse (CSS), og flisfeil gir også `load`. | avvist |
| 13 | To faner som poster samtidig: den siste vinner (EC) | low | Det er økt-designet fra 1.9 og sjeldent. | avvist |
| 14 | Testene er bundet til eksakt kildetekst (BH) | low | Det er etablert konvensjon (KartJsTest og ForbedringTest). | avvist |
| 15 | `button.handlingslenke` mangler farge (BH) | false | `.handlingslenke` setter `color: var(--primary)` (`side.css:588-594`). | avvist |

## Design Notes

**Dobbeltklikk** stoppes på to nivåer. Klienten sender bare én gang (`data-sendes`). Serveren sammenligner `tur` med `gjeldende_tur_id`, så en gammel POST er idempotent og aldri en feil.

Fragmentet hentes ved å følge PRG-redirecten. Det holder POST-viewene like med og uten JS:
```js
fetch(form.action, {method: "POST", body: new FormData(form), headers: {"X-Fragment": "1"}, credentials: "same-origin"})
  .then(function (svar) { if (!svar.ok) throw svar; return svar.text(); })
```

## Verification

**Commands:**
- `venv/Scripts/python.exe manage.py test` -- expected: alle grønne (443 + nye)
- `venv/Scripts/python.exe -m ruff check . && venv/Scripts/python.exe -m ruff format --check .` -- expected: rent

**Manual checks:**
- Hovedøkten sjekker i Chrome lokalt:
  - Nytt forslag med og uten JS (sandboxed iframe), helt til «alle vist» og «Start fra første forslag igjen».
  - Tittel og fokus, kartet med ny rute og ingen CSP-brudd.
  - axe-core på panelet, og 360 px.
