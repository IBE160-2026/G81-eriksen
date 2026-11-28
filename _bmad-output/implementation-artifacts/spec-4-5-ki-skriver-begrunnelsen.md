---
title: 'Story 4.5: KI skriver begrunnelsen'
type: 'feature'
created: '2026-11-28'
status: 'done'
baseline_commit: '14517f2ee41b804ae5c6e74606d1c921b00407c9'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-4-context.md'
  - '{project-root}/_bmad-output/implementation-artifacts/spec-4-4-ki-kallene-har-en-grense.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Turforslaget ber fortsatt alltid om reservemalen (`hent_ki(tving_reserve=True)`), så KI skriver ingen begrunnelse selv om grensesnittet (4.1), valideringen (4.2), loggen (4.3) og grensen (4.4) nå er på plass. Ola ser derfor aldri «✦ Skrevet med KI» (FR-12, FR-13, NFR-8, AD-10).

**Approach:** `sokflyt` kaller `hent_ki(okt=request.session)` én gang for hver tur som vises første gang i et søk, validerer svaret med `valider_begrunnelse` og lagrer den ferdige teksten og om den er skrevet av KI i `Soketilstand`. Forkastet svar, feil, tidsavbrudd, nådd grense og manglende nøkkel gir reservemalen, uten feilmelding. Malen viser KI-merket og setning 3 i Forklaringspanelet. Prompten får sin egen fil, og en manuell testplan i `docs/` dekker sjekken mot ekte KI.

## Boundaries & Constraints

**Always:**
- `Soketilstand` får feltet `begrunnelser: tuple[LagretBegrunnelse, ...] = ()` der `LagretBegrunnelse(tur_id: str, tekst: str, ki: bool)` er en frossen dataklasse i `domene/okt.py`. `til_dict` skriver listen `begrunnelser` med ordbøker `{"tur_id", "tekst", "ki"}`. `fra_dict` bruker `data.get("begrunnelser", [])`, så tilstand fra før 4.5 leses uten feil (NFR-2, AD-5). Enkeltoppføringer som ikke er `{str, str, bool}`, har tom tekst, eller har samme `tur_id` som en tidligere oppføring, hoppes over uten unntak. Hele feltet som ikke er en liste gir tom tuple. Et ugyldig felt gjør aldri hele søket ukjent.
- Ny ren hjelper `med_begrunnelse(tilstand, tur_id, tekst, ki) -> Soketilstand` i `domene/okt.py` (erstatter en eksisterende oppføring for samme tur, ellers legger til) og `lagret_begrunnelse(tilstand, tur_id) -> LagretBegrunnelse | None`. `neste_forslag` og `start_pa_nytt` beholder `begrunnelser` (de bruker `replace`), så «Start fra første forslag igjen» bruker lagret tekst og merke og ikke kaller KI på nytt.
- Ny funksjon `sokflyt.sikre_begrunnelse(tilstand, okt) -> Soketilstand`. Den gjør ingenting (returnerer samme objekt, ingen `hent_ki`) når: status ikke er `TREFF` eller `TOPPTUR_ERSTATTET`, `gjeldende_tur_id` er `None` («alle vist»), turen ikke finnes eller ikke lenger passer (`_passer`), eller turen alt har en lagret begrunnelse. Ellers:
  1. Lag reserveteksten (`reservebegrunnelse`) og tilleggssetningene (`personaliseringssetning`, `preferansesetning`, uendret logikk fra i dag).
  2. `svar = hent_ki(okt=okt).begrunnelse(KiSok(...), KiTur(...), reserve, topptur_erstattet=status == TOPPTUR_ERSTATTET)`.
  3. `svar.tekst == reserve` og `svar.ok` er reserve (uten nøkkel, nådd grense, feil i telling): bruk reserve + tillegg, `ki=False`, ingen validering og ingen logging.
  4. `svar.ok` med annen tekst: `valider_begrunnelse(svar.tekst, sok, tur, status, tillegg)`. Ved `ok` er den ferdige teksten brukt med `ki=True`. Ved forkastelse: `logg_forkastet("begrunnelse", str(forkastelse), svar.tekst)`, og reserve + tillegg brukes med `ki=False`.
  5. `svar` med `arsak` (`tidsavbrudd`, `feil`, `ugyldig`): `logg_forkastet("begrunnelse", svar.arsak, None)`, reserve + tillegg, `ki=False`.
  6. Resultatet (også reserve etter forkastelse, feil eller nådd grense) lagres med `med_begrunnelse`, så ny innlasting ikke prøver igjen (FR-12, AD-10 punkt 3).
  Unntak fra `hent_ki` eller logging fanges, gir reserve + tillegg, og når aldri viewet.
- `sokflyt.forslagsvisning(tilstand)` er fortsatt ren og kaller aldri KI. Den bruker `lagret_begrunnelse` for gjeldende tur og sender `ki` videre til visningen. Finnes ingen lagret begrunnelse, bygges reserve + tillegg som i dag, med merket «Begrunnelse fra mal». Tilleggssetningene legges ikke til på nytt på en lagret tekst.
- `views.forslag` (GET): `ny = sokflyt.sikre_begrunnelse(tilstand, request.session)`. Er `ny != tilstand`, kalles `okt.oppdater_sok(request, sok_id, ny)` før visningen lages fra `ny`. Bare `GET` kan sende kall (en `HEAD` bruker `forslagsvisning` uten `sikre_begrunnelse`). `nytt_forslag`, `forfra`, `endre` og `sok` sender ingen kall selv, og kallet skjer når Ola ser turen (også for fragmentet fra `forbedring.js`, `X-Fragment: 1`).
- Turforslag fra historikken (`historikkvisning`), og tilstandene `INGEN_TREFF`, `BARE_OVER_NIVATAK` og «alle vist» kaller aldri `hent_ki`, og viser «Begrunnelse fra mal» der det er en begrunnelse (FR-17, AD-10 punkt 4).
- Ny parameter på grensesnittet: `Ki.begrunnelse(sok, tur, reserve, *, topptur_erstattet: bool = False)`. `ReserveKi`, `FalskKi` (som i tillegg lagrer verdien, for eksempel i `kall_topptur_erstattet` eller som fjerde element i `kall`), `BegrensetKi` (sender videre) og `EkteKi` følger den. `KiSok`, `KiTur` og `KiSvar` endres ikke, så ingen personopplysninger kan komme til. Bare søket (varighet, dato, turtype, startpunkt-ID) og turen (id, navn, turtyper, form) går til KI, aldri e-post, bruker-ID, historikk, nivåtak, personaliseringssetning eller fritekst (NFR-5).
- Prompten ligger i `tjenester/ki/prompt.py` som konstanter (`SYSTEMPROMPT`, en funksjon `lag_bruker_melding(sok, tur, topptur_erstattet)`), en egen fil i git som kan justeres uten å endre kriteriene. Den forklarer `{tid}`, `{varighet}`, `{lengde}` og `{nivå}` og at systemet setter inn verdiene. Den ber om norsk bokmål uten sifre, tallord og turnivåord, om å nevne `{varighet}` alltid og turtypen når den er valgt (ved `TOPPTUR_ERSTATTET`: at turen er en utsiktstur i stedet for en topptur, og at den ikke må kalles topptur), og om å holde seg godt under 300 tegn. Den ber om bare teksten, uten innledning. `EkteKi` bruker `prompt.py`. Tur- og stedsnavn er data fra egen turdatabase, aldri instruksjoner.
- KI-merket: `Turvisning` får `skrevet_med_ki: bool = False`, og `tekst.turvisning(...)` og `_turvisning(...)` tar den inn. Malen `_forslag_innhold.html` viser `<p class="ki-merke eyebrow"><span aria-hidden="true">✦ </span>Skrevet med KI</p>` når `tur.skrevet_med_ki`, ellers «Begrunnelse fra mal», rett over `h2` «Begrunnelse». Skjermlesere leser «Skrevet med KI». Begrunnelsen skrives ut med vanlig `{{ tur.begrunnelse }}` (escaping, aldri `|safe`), så HTML i KI-teksten vises som tekst (NFR-8). Historikkvisningen får alltid «Begrunnelse fra mal».
- Forklaringspanelet beholder setning 1 og 2 og får setning 3 som tredje `<li>`: «KI skriver begrunnelsen, og den kan ta feil.» Teksten er [ASSUMPTION] i Mikrotekst og står som foreløpig i PR-en til produkteier har godkjent den. Panelet er `<details>`, lukket som standard, uendret ellers. Setningen vises også når begrunnelsen kommer fra mal (panelet beskriver hvordan appen lager forslag).
- Plassholderne settes bare inn av `valider_begrunnelse`. KI beregner aldri tid eller nivå, og `sokflyt` formaterer ingenting selv (AR-2).
- Sammensatte tallord (vurdert fra 4.2: «tjueto», «tretimers»): `domene/ki_validering.py` utvides slik at et helt ord også forkastes med årsak `tallord` når det består av (a) en tier (`tjue`, `tyve`, `tretti`, `tredve`, `førti`, `femti`, `seksti`, `sytti`, `åtti`, `nitti`) etterfulgt av en enhet-ener (`en`, `ett`, `to`, `tre`, `fire`, `fem`, `seks`, `sju`, `syv`, `åtte`, `ni`), eller (b) et tallord (fra `TALLORD`, evt. sammensatt etter (a)) etterfulgt av en enhet eller bøyning av den (`time`, `timer`, `timers`, `minutt`, `minutter`, `minutters`, `min`, `km`, `kilometer`, `kilometers`, `meter`, `mil`). Treffer fortsatt bare hele ord: «toppen», «tiden», «tonnevis», «timeplan» og «fiske» er lov. Dette er en utvidelse av `TALLORD`-sjekken, ikke en ny årsak, og den er utenfor den frosne «tallord»-definisjonen i 4.2 bare ved å være strengere.
- Tester bruker bare `FalskKi`, `mock` av `hent_ki` og falsk HTTP-transport (`httpx2.MockTransport`), uten nøkkel og uten nettverk. Tester viser til FR-12, FR-13, NFR-5 eller NFR-8. Eksisterende tester for story 1–4.4 består uendret, med unntak av de som uttrykkelig dekker «alltid reserve» (`tests/web/test_ki_forslag.py`, panelteksten i `tests/web/test_forslag.py`, og `EkteKi`-testene som sjekker prompten).
- Manuell testplan i `docs/ki-testplan.md`: minst 10 søk med ulike varigheter og turtyper (inkludert én gruppe som ber om topptur så `TOPPTUR_ERSTATTET` oppstår), en tabell for resultatet (antall «✦ Skrevet med KI», antall «Begrunnelse fra mal», forkastede svar og årsak fra `logs/ki.log`, nevnte begrunnelsen varigheten og turtypen), oppskrift for å lese loggen, kontroll at nøkkelen bare er satt for produksjon hos Vercel (`vercel env ls`), og en rad for fritekstønsket som 4.7 fyller ut. Planen krever Anthropic-kontoen. Storyen kan merges uten at den er utfylt.
- README forklarer hvordan nøkkelen legges inn i `.env` (aldri i git), at appen bruker reservemalen uten den, og at `ANTHROPIC_API_KEY` hos Vercel bare settes for Production (ikke Preview eller Development), så forhåndsvisninger bruker reserve (AR-20, SM-3). Setningen «legges inn senere» og «kommer i en senere story» fjernes.

**Never:**
- Ingen ekte nettverkskall eller krav om nøkkel i tester eller i `manage.py test`. Ingen nøkkelverdi i filer, logger, testplan eller meldinger.
- Ingen personopplysninger (e-post, bruker-ID, historikk, nivåtak, personaliseringssetning, søke-ID) i kall, prompt eller loggen. Ingen endring av logglinjenes format (4.3) eller av grensen (4.4).
- Ingen KI-kall fra `forslagsvisning`, `nytt_forslag`, `forfra`, `endre`, `utfor_sok`, `historikkvisning` eller for tilstander uten tur. Ingen kall for en tur som alt har lagret begrunnelse.
- Ingen feilmelding til Ola når KI svikter. `tjenester/` importerer ikke `turforslag/`. `anthropic` importeres bare i `tjenester/ki/ekte.py`. Ingen ny avhengighet. Ingen kall A (tolking) og ingen fritekstfelt (4.6 og 4.7). `FRITEKST_AKTIV` innføres ikke her.
- Ingen `|safe` eller `mark_safe` på begrunnelsen.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Godkjent svar | Nøkkel, grense ikke nådd, svar med `{varighet}` | Ferdig tekst med innsatte verdier, «✦ Skrevet med KI», lagret med `ki=True`, ett kall | N/A |
| Ny innlasting | Samme søke-ID etter godkjent svar | Samme tekst og merke, `FalskKi.antall_kall` forblir 1 | N/A |
| «Nytt forslag», så «Start fra første forslag igjen» | Tur 1 vist, tur 2 vist, alle vist, forfra | Tur 1 bruker lagret tekst og merke, to kall totalt | N/A |
| Forkastet svar | Svar med siffer / tallord / nivåord / feil turtype / for langt / tomt / manglende `{varighet}` | Reservemalen + tillegg, «Begrunnelse fra mal», ingen melding, lagret med `ki=False`, én logglinje med kalltype `begrunnelse` og årsaken | `logg_forkastet` feiler: ignoreres |
| Tidsavbrudd / feil / ugyldig | `FalskKi.tidsavbrudd()` / `feil()` / `KiSvar(arsak="ugyldig")` | Reserve, «Begrunnelse fra mal», lagret, logglinje med årsak og tomt svar | Ingen unntak til view |
| Nådd grense | `BegrensetKi` gir `KiSvar(tekst=reserve)` | Reserve, ingen validering, ingen forkastelseslogg (4.4 logger bare totalgrensen), lagret | N/A |
| Uten nøkkel | `ANTHROPIC_API_KEY` tom/mangler | `hent_ki` gir `ReserveKi`, reserve, «Begrunnelse fra mal», ingen telling | N/A |
| Forhåndsvisning på Vercel | Ingen nøkkel i Preview | Som uten nøkkel | N/A |
| Topptur erstattet | Status `TOPPTUR_ERSTATTET` | `topptur_erstattet=True` i kallet. Svar uten «utsikt» forkastes med `turtype`, svar som kaller turen topptur uten «utsikt» også | N/A |
| Gammel tilstand | Lagret søk uten `begrunnelser` | Leses uten feil, første visning av gjeldende tur gjør ett kall, så lagres tekst | N/A |
| Skadet felt | `begrunnelser` er tekst, eller en oppføring mangler `tekst` | Ugyldige oppføringer hoppes over, søket er fortsatt gyldig, ny begrunnelse lages | Ingen `ValueError` |
| Historikk | `/historikk` åpner turforslag | Ingen kall (`antall_kall == 0`), «Begrunnelse fra mal» | N/A |
| Tilstander uten tur | `INGEN_TREFF`, `BARE_OVER_NIVATAK`, «alle vist» | Ingen kall | N/A |
| Tur slettet eller utenfor tid/nivåtak | `forslagsvisning` gir `None` i dag | Ingen kall, «Søk» som før (SM-C1) | N/A |
| HTML i svar | `<script>alert(1)</script> {varighet}` | Vises som tekst (escaped) og ikke kjørt | N/A |
| Personvern | Innlogget bruker med historikk | `FalskKi.kall` og loggfilen har ingen e-post, bruker-ID, søke-ID, nivåtak eller historikk | N/A |
| Sammensatte tallord | «tjueto minutter», «en tretimers tur» | `tallord` | N/A |
| Lovlige ord | «toppen», «tiden», «timeplan» | Ikke forkastet av tallordsjekken | N/A |
| Økt mister `ki_kall` | Ny økt | Døgngrensen gjelder (4.4), lagrede begrunnelser lever med søket | N/A |

</frozen-after-approval>

## Code Map

- `turforslag/sokflyt.py:172` -- eneste kallsted: `hent_ki(tving_reserve=True)` byttes ut med `sikre_begrunnelse`; `forslagsvisning` leser lagret begrunnelse. Importerer `valider_begrunnelse`, `logg_forkastet` (via `tjenester.ki`, legg `logg_forkastet` til i `tjenester/ki/__init__.py`).
- `turforslag/views.py` (`forslag`) -- kaller `sikre_begrunnelse(tilstand, request.session)` og `okt.oppdater_sok` ved endring, bare på GET.
- `turforslag/okt.py` -- uendret API; `oppdater_sok` skriver hele tilstanden (flytter søket sist av de 10, som i dag).
- `domene/okt.py` -- `LagretBegrunnelse`, feltet `begrunnelser`, `til_dict`/`fra_dict` (mønster: `foretrukne_turtyper` og `data.get`), `med_begrunnelse`, `lagret_begrunnelse`. Docstringen nevner allerede at KI-feltet kommer.
- `domene/ki_validering.py` (`valider_begrunnelse`, `TALLORD`, `_har_tallord`) -- sammensatte tallord. `tests/domene/test_ki_validering.py` utvides.
- `domene/tekst.py` (`Turvisning`, `turvisning`, `_turvisning`, `forslagsvisning`, `historikkvisning`) -- `skrevet_med_ki`.
- `turforslag/templates/turforslag/_forslag_innhold.html:53-60` -- KI-merket og Forklaringspanelet. Merket styles av `.ki-merke` i `turforslag/static/css/side.css:753`.
- `tjenester/ki/grensesnitt.py` (`Ki`, `hent_ki`), `reserve.py`, `falsk.py`, `grense.py`, `ekte.py` -- `topptur_erstattet`-parameteren. Ny `tjenester/ki/prompt.py`. `SYSTEMPROMPT` i `ekte.py` er foreløpig («forfines i story 4.5»).
- `tjenester/ki/logg.py` (`logg_forkastet`) -- brukes uendret. Gyldige årsaker er `KI_FEILARSAKER` og `Forkastelse`.
- `domene/begrunnelse.py` (`reservebegrunnelse`, `personaliseringssetning`, `preferansesetning`, `MAKS_TEGN`) -- uendret.
- `tests/web/test_ki_forslag.py` -- erstattes av tester mot `sikre_begrunnelse`/view med `mock.patch("turforslag.sokflyt.hent_ki", return_value=falsk)` (mønster i dagens fil). `tests/web/test_forslag.py:95-110, ~424` -- panelteksten og merkerekkefølgen. `tests/web/maler/komponenter.html` -- sjekk om merket vises der.
- `tests/domene/test_okt.py` -- `begrunnelser` rundtur og gammel tilstand. `tests/tjenester/test_ki.py` -- `EkteKi` mot `MockTransport`: prompt, `topptur_erstattet`, ingen personopplysninger i forespørselen. `tests/tjenester/test_ki_logg.py` -- ingen søke-ID, e-post eller bruker-ID i logglinjer fra flyten.
- `README.md:88,98` og ny `docs/ki-testplan.md`.

## Tasks & Acceptance

**Execution:**
- [ ] `domene/okt.py` -- `LagretBegrunnelse`, `begrunnelser`, serialisering, `med_begrunnelse`, `lagret_begrunnelse`
- [ ] `domene/ki_validering.py` -- sammensatte tallord (tier+ener, tallord+enhet), med lovlige ord som tester
- [ ] `tjenester/ki/` -- `topptur_erstattet` i `Ki`, `ReserveKi`, `FalskKi`, `BegrensetKi`, `EkteKi`; `prompt.py`; eksporter `logg_forkastet`
- [ ] `turforslag/sokflyt.py` -- `sikre_begrunnelse`, `forslagsvisning` leser lagret tekst og merke
- [ ] `turforslag/views.py` -- `forslag` kaller `sikre_begrunnelse` (GET) og lagrer
- [ ] `domene/tekst.py` + `_forslag_innhold.html` -- `skrevet_med_ki`, merket, setning 3
- [ ] tester -- hele matrisen. Egne tester: ingen kall fra historikk og de tre tilstandene uten tur, ny innlasting og «Nytt forslag» gir ikke nytt kall, gammel tilstand, HTML escapes, loggen uten søke-ID/e-post/bruker-ID, `FalskKi` ser ingen personopplysninger for innlogget bruker med historikk, grensen senket via `override_settings` gir reserve og ett kall mindre, `makemigrations --check` (ingen modellendring)
- [ ] `README.md` -- nøkkel i `.env`, reserve uten nøkkel, nøkkelen bare i produksjon hos Vercel
- [ ] `docs/ki-testplan.md` -- manuell testplan

**Acceptance Criteria:**
- Given nøkkel og grense ikke nådd, when en tur vises første gang i et søk, then ett kall B sendes, godkjent svar vises med «✦ Skrevet med KI» over `h2` «Begrunnelse», og ✦ er `aria-hidden`.
- Given forkastet svar, tidsavbrudd, feil eller nådd grense, when turen vises, then reservemalen vises med «Begrunnelse fra mal» uten feilmelding, forkastelser og feil er logget med kalltype `begrunnelse`, og teksten er lagret.
- Given en lagret begrunnelse, when siden lastes på nytt, «Nytt forslag» går tilbake til turen via «Start fra første forslag igjen», eller fragmentet hentes, then KI kalles ikke på nytt, og en tilstand fra før 4.5 leses uten feil.
- Given turforslag fra historikken, `INGEN_TREFF`, `BARE_OVER_NIVATAK` eller «alle vist», when de vises, then `FalskKi.antall_kall == 0`.
- Given at `ANTHROPIC_API_KEY` mangler, when hele kjerneflyten gås gjennom, then alt virker som før med «Begrunnelse fra mal».

## Implementation Notes

- Valg for å skille reserve fra KI-svar: `BegrensetKi` og `ReserveKi` gir `KiSvar(tekst=reserve)`, som mangler plassholdere og ville blitt forkastet og logget som `ugyldig`. `sokflyt` sammenligner derfor `svar.tekst == reserve` før validering. Alternativet er et nytt felt på `KiSvar` (`reserve: bool`), men det rører den frosne dataklassen fra 4.1 og ble ikke valgt.
- Implementert 2026-11-28 (de tre åpne spørsmålene er besvart med JA): reserve lagres også uten nøkkel, sammensatte tallord er med i `domene/ki_validering.py` (`_sammensatt_tallord`), og bare startpunkt-ID går til KI.
- `tests/__init__.py` setter `settings.ANTHROPIC_API_KEY = ""` for hele testpakken. Uten den ville en ekte nøkkel i `.env` gitt nettverkskall fra webtestene som nå går gjennom `GET forslag`. Tester som trenger nøkkel bruker `override_settings`.
- `sokflyt.sikre_begrunnelse` er delt i `_kall_ki` (kall, validering, logging) og en ytre `try/except` som gir reserve. `logg_forkastet` kalles via `_logg` som svelger feil. Reserveteksten fra `ReserveKi`/`BegrensetKi` kjennes igjen ved `svar.tekst == reserve` (ingen nytt felt på `KiSvar`).
- `FalskKi` lagrer `topptur_erstattet` i `kall_topptur_erstattet` (egen liste, `kall` er uendret med tre elementer).
- Prompt (`tjenester/ki/prompt.py`): søk og tur sendes som JSON-data, med én ekstra linje ved erstattet topptur. Prompten er ikke prøvd mot ekte KI. Det gjøres med `docs/ki-testplan.md`.
- Ved ventetid: kallet skjer i `GET forslag` etter redirect, med `timeout=5.0` og `max_retries=0`. Lastetekst finnes alt i `forbedring.js` («Finner et nytt forslag …»).
- To faner som åpner samme nye søk samtidig kan gi to kall (grensen i 4.4 begrenser skaden). Sist lagrede tilstand vinner. Ikke løst her.
- `.env` inneholder en ekte nøkkel. Testplanen og README skal aldri gjengi nøkkelverdier, og `.env` skal ikke committes (`.gitignore`).

## Spec Change Log

## Review Triage Log

Utført (patch): `tests/__init__.py` setter `DJANGO_SETTINGS_MODULE`, `views.forslag` leser tilstanden på nytt etter KI-kallet og skriver bare begrunnelsen inn (`sokflyt.flett_begrunnelse`), prompten ber om maks ca. 180 tegn, unntak i `sikre_begrunnelse` logges med typenavn, og personvernstesten sjekker den faktisk sendte meldingen.

Utsatt, ingen kode:
- «tre» og «halv» kan gi falske positiver i valideringen, og ordenstall, «enogtjue» og «tohundre» slipper gjennom. Dette er 4.2-valg og trygt.
- Nivåord «svarte» og «grønne» (trygt).
- Reserve kjennes igjen ved tekstlikhet (`svar.tekst == reserve`), et spec-valg.
- Lagret tekst foreldes hvis turdata endres etter at begrunnelsen er lagret.
- To faner som åpner samme nye søk samtidig kan gi to kall.

## Open Questions

1. **Lagre reserve også uten nøkkel?** Anbefaling: ja, uniform lagring (enklere, samme kodevei i tester). Kostnad er litt større økt (maks 10 søk × turer × ≤300 tegn). Alternativ: bare lagre når `hent_ki` ga en annen variant enn `ReserveKi`.
2. **Skal valideringen strammes inn med sammensatte tallord i denne storyen?** Anbefaling: ja, siden ekte KI nå slås på og 4.2 bevisst avviste det som «lavt». Endringen er liten og ligger i `domene/`. Utsett til egen story hvis produkteier vil holde 4.2s liste fast.
3. **Startpunkt til KI:** `KiSok` har bare `startpunkt_id`, ikke navn, så prompten kan ikke nevne startpunktet pent. Anbefaling: send ID-en (som AC sier) og la begrunnelsen ikke nevne startpunkt. Å sende navnet krever et nytt felt og endrer 4.1.

## Verification

**Commands:**
- `venv/Scripts/python.exe manage.py test` -- expected: alle grønne, uten nøkkel og uten nettverk
- `venv/Scripts/python.exe manage.py makemigrations --check --dry-run` -- expected: ingen endringer
- `venv/Scripts/python.exe -m ruff check . && venv/Scripts/python.exe -m ruff format --check .` -- expected: ingen funn

**Manual checks:**
- Følg `docs/ki-testplan.md` lokalt med nøkkel i `.env` (krever Anthropic-konto, kan utsettes). Sjekk `logs/ki.log` for forkastelser, og at ingen linje har e-post, bruker-ID eller søke-ID.
- `vercel env ls`: `ANTHROPIC_API_KEY` finnes bare for Production. En forhåndsvisning viser «Begrunnelse fra mal».

- Lagt til etter review (utenfor frozen-blokka): `views.forslag` fletter bare begrunnelsen inn i fersk tilstand (`flett_begrunnelse`) for å unngå lost update mot «Nytt forslag».
