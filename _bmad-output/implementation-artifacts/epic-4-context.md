# Epic 4 Context: KI skriver begrunnelsen og forstår ønsket

<!-- Compiled from planning artifacts. Edit freely. Regenerate with compile-epic-context if planning docs change. -->

## Goal

Med nøkkel skriver KI begrunnelsen for turforslaget, og (P2) tolker et fritekstønske. Alt KI-svar valideres av systemet, reservemalen tar over ved feil, og kostnaden har et tak. KI får aldri personopplysninger, og kjerneflyten virker uten nøkkel. Story 4.1–4.5 er P1. Story 4.6–4.7 (fritekstønske) er P2 og bygges sist.

## Stories

- Story 4.1: KI-tjenesten har ett grensesnitt med tre varianter
- Story 4.2: Systemet sjekker KI-teksten før den vises
- Story 4.3: Forkastede KI-svar logges uten personopplysninger
- Story 4.4: KI-kallene har en grense per nettleser og per døgn
- Story 4.5: KI skriver begrunnelsen
- Story 4.6 (P2): Ola kan skrive et fritekstønske
- Story 4.7 (P2): KI tolker fritekstønsket

## Requirements & Constraints

- Begrunnelsen nevner varigheten, og turtypen og fritekstønsket hvis de er oppgitt. Maks 300 tegn slik brukeren ser den. KI bruker plassholderne `{tid}`, `{varighet}`, `{lengde}` og `{nivå}`, og systemet setter inn verdiene. KI beregner aldri tid eller nivå.
- KI-merket viser «✦ Skrevet med KI» eller «Begrunnelse fra mal». Forklaringspanelet sier at KI skriver og kan ta feil.
- Et KI-svar forkastes hvis det viser til en tur utenfor treffene, er tomt eller ugyldig, er over 300 tegn, har tall eller turnivå utenfor plassholderne, ikke nevner valgt turtype, eller kommer etter 5 sekunder.
- Forkastes tolkingen av ønsket, ignoreres ønsket for hele søket, begrunnelsen kommer fra reservemalen, og en melding forteller om det. Forkastes bare begrunnelsen for én tur, brukes reservemalen for den turen uten melding. Reserve brukes også uten nøkkel og når grensen er nådd.
- Fritekstønske: maks 200 tegn, valgfritt, validert også på serveren. Ønsket er data, aldri instruksjoner.
- Personvern: KI får bare søket og de filtrerte turene (id, navn, turtyper, form). Aldri e-post, bruker-ID, historikk eller nivåtak. Loggen har bare tidspunkt, kalltype, årsak og svar, aldri fritekst, søke-ID, e-post eller bruker-ID. Filer eldre enn 30 dager slettes.
- Grense for KI-kall: maks 20 per nettleser siste 60 min og maks 200 per kalenderdøgn (Europe/Oslo). Et kall teller når det sendes.
- Turforslag fra historikken og tilstandene uten tur (ingen treff, over nivåtak, alle vist) kaller aldri KI.
- Kjerneflyten og alle tester virker uten nøkkel og uten nettverkskall.

## Technical Decisions

- `tjenester/ki/` har ett grensesnitt med variantene ekte (Anthropic, `anthropic` 2.6.0, `claude-haiku-5-5`), reserve og falsk (tester). `anthropic` importeres bare i den ekte varianten. Uten nøkkel (tom eller bare mellomrom) brukes reserve. Nøkkelen leses bare i `config/settings.py`.
- Ekte klient: `timeout=5.0`, `max_retries=0`, lav effort, ingen sampling-parametere, ingen prefill. Feil gir feilresultat (`tidsavbrudd`, `feil`, `ugyldig`) og kastes aldri videre til view.
- Kall A (tolking): én gang per gyldig søk med fritekst, nøkkel og treff, før rangeringen. Svar er liste med tur-ID-er fra treffene (tom liste er gyldig). Kall B (begrunnelse): én gang per vist tur, lagres i søketilstanden (`turforslag/okt.py`), så ny innlasting og «Nytt forslag» ikke kaller på nytt. Søketilstand uten nye felt må leses uten feil.
- KI-dataene er frosne dataklasser i `domene/` uten andre felt enn de tillatte. Prompter ligger i egne filer i git, og fritekst er avgrenset data der avgrensertegn fjernes eller escapes.
- Validering er én ren funksjon i `domene/`. Rekkefølge: tom, plassholdere (`{varighet}` påkrevd), sifre, tallord, nivåord, turtype (ved `TOPPTUR_ERSTATTET` må utsikt nevnes), innsetting, personaliseringssetning, 300 tegn (linjeskift og doble mellomrom blir ett). Årsaker: `tom`, `ugyldig`, `siffer`, `tallord`, `nivaord`, `turtype`, `for_lang`. Ordlistene er konstanter i `domene/`, og treffer bare hele ord.
- Personaliseringssetningen kommer fra funksjonene i Epic 3 og sjekkes ikke. Formatene («ca. 1 t 35 min», «2 timer», «grønn») er de samme som reservemalen bruker.
- Logg: én funksjon (kalltype, årsak, svar), én logger per modul. Lokalt `logs/ki.log` (i `.gitignore`) med `TimedRotatingFileHandler` ved midnatt uten `backupCount`, og sletting av filer eldre enn 30 dager ved oppstart og rotasjon via ren funksjon. Når `VERCEL` er satt, går linjene til standard ut. Vercel-loggen slettes etter 1 time, så KI-kvalitetssikring gjøres lokalt.
- Grense: ren funksjon i `domene/`. Grensene er `KI_MAKS_PER_NETTLESER_TIME = 20` og `KI_MAKS_PER_DOGN = 200` i `settings`. Tidspunkter i økten under `"ki_kall"`. Modellen `KiForbruk(dato, antall)` med unik `dato` gjør `tjenester/` til en Django-app. Telling med `get_or_create` og `F("antall") + 1` i én transaksjon, før kallet sendes. Én logglinje første gang totalgrensen nås per døgn. `tjenester/` importerer aldri `turforslag/`. Reserve teller ikke.
- `velg_turer` får bare nøkkelordargumentet `onsket_tur_ider` (standard tomt sett). Ønskede turer kommer etter «ikke gåtte først» og før nivåheving, foretrukne turtyper, tid og tur-ID.
- `FRITEKST_AKTIV` i `settings` er `False` etter 4.6 og settes `True` i 4.7. Med `False` skjules feltet, og serveren ignorerer ønsket.
- Til 4.5 ber viewet alltid om reservevarianten, så publisert side ikke sender kall før validering, logg og grense er på plass.
- På Vercel finnes `ANTHROPIC_API_KEY` bare i produksjon, så forhåndsvisninger bruker reserve. Grensene gjelder per database.
- Tester: `tests/domene/` uten database, `tests/tjenester/` og `tests/web/` med falsk variant og falsk HTTP-transport. Tester viser til FR-/NFR-ID-ene. Django-malen escaper KI-tekst.

## UX & Interaction Patterns

- KI-merket står rett over `h2` «Begrunnelse», og ✦ er `aria-hidden`. Forklaringspanelet «Slik lager jeg forslaget» er `<details>`, lukket som standard. Setning 3 er «KI skriver begrunnelsen, og den kan ta feil.» (foreløpig tekst, [ASSUMPTION]) til 4.7 gjør den til «KI tolker ønsket ditt og skriver begrunnelsen, og den kan ta feil.»
- Fritekstønske: `<textarea>` etter Startpunkt, etikett «Fritekstønske (valgfritt)», hjelpetekst «Jeg prøver å ta hensyn til ønsket ditt.», uten `maxlength`. Teller «{n} / 200 tegn» fra `forbedring.js`, og overskridelse meldes én gang i `aria-live="polite"`. Feil over 200 tegn følger skjemamønsteret (feilmelding ved feltet, `aria-invalid`, fokus), også uten JavaScript. `\r\n` blir `\n` og kantmellomrom fjernes før telling.
- Ignorert ønske: infomelding «Jeg kunne ikke ta hensyn til ønsket ditt denne gangen» rett etter turnavn og Turtype-treff på hver tur i søket. KI-feil ellers gir aldri feilmelding.
- «Endre søk» og endringsforslag («Prøv 3 timer») beholder ønsket.

## Cross-Story Dependencies

- 4.1 bygger på reservemalen fra story 1.9 og personaliseringssetningene fra Epic 3 (3.3, og 3.5 hvis levert).
- 4.2 (validering), 4.3 (logg) og 4.4 (grense) må være på plass før 4.5 slår på ekte KI-kall.
- 4.5 bruker 4.1–4.4, lagring i søketilstanden (AD-5) og Forklaringspanelet fra Epic 1. Den inneholder en manuell testplan i `docs/` som krever Anthropic-konto (kan merges uten).
- 4.6 uten 4.7 viser ikke feltet. 4.7 bygger på 4.6, kall A i 4.1, grensen i 4.4, rangeringen fra story 1.8/3.2 og endringsforslagene fra story 1.12, og utvider testplanen fra 4.5.
- Epic 1–3 og testene deres må bestå uendret. Epic 5 er uavhengig.
