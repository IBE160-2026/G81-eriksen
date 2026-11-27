# Epic 3 Context: Forslagene tilpasser seg nivået til Ola

<!-- Compiled from planning artifacts. Edit freely. Regenerate with compile-epic-context if planning docs change. -->

## Goal

Forslagene skal følge hvordan turene faktisk kjentes for den innloggede brukeren. Vurderingene (lett, moderat, vanskelig) styrer et nivåtak med heving, sperre og oppheving. Søket prioriterer det nye nivået og turer brukeren ikke har gått, og begrunnelsen forklarer regelen. En testbruker med ferdig historikk lar sensor se alt dette uten å gå turer. Preferanse for turtyper brukeren har vært fornøyd med (P2) kommer sist og kan kuttes uten å påvirke resten.

## Stories

- Story 3.1: Vurderingene bestemmer nivåtaket etter faste regler
- Story 3.2: Søket bruker nivåtaket og historikken
- Story 3.3: Begrunnelsen forklarer nivået
- Story 3.4: Testbrukeren viser personaliseringen
- Story 3.5 (P2): Turtyper Ola har vært fornøyd med, kommer først

## Requirements & Constraints

- Gjester og brukere uten historikk har alltid grønt nivåtak.
- Nivåtaket er grunnnivået, eller sperrenivået mens en sperre er aktiv. Tre turer på grunnnivået vurdert *lett* (ikke nødvendigvis etter hverandre, *moderat* teller ikke og nullstiller ikke) hever grunnnivået ett nivå. Svart heves ikke.
- *Vanskelig* nullstiller telleren og senker nivåtaket til nivået under turens nivå (aldri under grønt), hvis det er lavere. Neste *lett* eller *moderat* opphever sperren, men teller ikke som heving. Hver registrering teller, også gjentakelser.
- Registreringer behandles etter dato, deretter registrerings-ID. Resultatet er uavhengig av innkommende rekkefølge, og en registrering med tidligere dato kan endre nivåtaket.
- Ingen bruker får foreslått en tur over nivåtaket (SM-C1). Meldinger og begrunnelser lover aldri lengre eller hardere turer.
- Rangering: (1) ikke gåtte turer først, gåtte med fornøydhet 1–2 sist, (3) nivåheving: i første søk etter en heving kommer turer på nivåtaket først, (4) foretrukne turtyper (P2), deretter tid nærmest varigheten og tur-ID. Gåtte turer utelukkes aldri.
- De 12 eksemplene i PRD-ens FR-19 er egne testtilfeller, navngitt med eksempelnummer og med henvisning til FR-ID.
- Begrunnelsen er maks 300 tegn slik brukeren ser den, også med personaliseringssetning. Nivåord bøyes i `domene/`, og malene har ingen tall.
- Tre nye meldingsvarianter for `BARE_OVER_NIVATAK` (ny bruker uten registreringer, bruker med historikk, ulike overskrifter etter nivåtak).
- Tekster merket [ASSUMPTION] i Mikrotekst (sperresetning, nådd-nivå-setning, preferansesetning, overskrift ved høyere nivåtak) brukes som foreløpige og listes i PR-en til produkteier har godkjent dem.
- Brukere ser bare egne data (filtrert på `request.user`). Tester bruker ikke nettverk.
- Prioritet: Story 3.1–3.4 er P1. Story 3.5 (FR-20) er P2 og kuttes sist av P2-ene. Å ta den ut skal ikke endre testene for 3.1–3.4.

## Technical Decisions

- `domene.niva.vurder_historikk(registreringer) -> NivaStatus` er eneste kilde til nivåtak, grunnnivå, sperre, antall hevinger, teller (og senere foretrukne turtyper). Ren Python, frossen dataklasse, uten database, nettverk eller klokke. Ugyldige verdier gir `ValueError` med norsk melding.
- `domene.niva.Registrering` er en frossen dataklasse (id, dato, tur_id, turniva, vanskelighet, fornoydhet 1–5). Omgjøring fra modell til domeneobjekt ligger i `turforslag/`, ikke i viewet. `sperre` er `None` eller har sperrenivå og turnivået som ga sperren.
- Nivåheving avgjøres bare ved et gyldig søk av en ren funksjon i `domene.niva`: `antall_hevinger > Bruker.brukt_heving` uten aktiv sperre gir `nivaheving=True`. `brukt_heving` lagres som `antall_hevinger` i samme forespørsel, også ved `INGEN_TREFF` og `BARE_OVER_NIVATAK`. Med aktiv sperre regnes hevingen som brukt, men `nivaheving=False`. Har en tidligere datert registrering fjernet en heving, settes `brukt_heving` ned. Opphevet sperre er ikke en heving. Gjester har alltid `False`, og ingenting lagres.
- Ugyldig søk, ny innlasting, «Nytt forslag», «Start fra første forslag igjen» og turforslag fra historikken endrer verken `brukt_heving` eller rangeringen.
- `velg_turer` utvides bare med nøkkelordargumentene `registreringer` (standard tom), `nivaheving` (standard `False`) og i 3.5 `foretrukne_turtyper` (standard tomt sett). Kall og tester fra Epic 1 skal virke uendret. Status er `Utvalg(status, rangerte_tur_ider)` med `TREFF`, `TOPPTUR_ERSTATTET`, `BARE_OVER_NIVATAK`, `INGEN_TREFF`. Siste avgjører er tur-ID.
- Søketilstanden (`Soketilstand`, Django-økten under `"sok"`, bare lest og skrevet av `turforslag/okt.py`) fryser grunnlaget for begrunnelse og meldinger: nivåtak, grunnnivå, sperre, `nivaheving`, om brukeren har historikk og (3.5) foretrukne turtyper. Ny innlasting og «Nytt forslag» gir da samme tekst, også etter ny registrering i en annen fane. Eldre lagrede tilstander uten de nye feltene må leses uten feil, med standardverdier (grønt nivåtak, ingen sperre, `False`, ingen historikk, tom liste).
- Turforslag fra historikken bruker `NivaStatus.nivatak` (også med sperre) for merknaden «Denne turen er over nivåtaket jeg foreslår for deg nå.», og får ingen personaliseringssetning og ingen KI-kall.
- Begrunnelsen (reservemalen, KI-merket «Begrunnelse fra mal») får personaliseringssetning lagt til etter malteksten: heving, nådd nivå eller sperre, aldri flere av disse samtidig. Preferansesetningen (3.5) kommer etter nivåsetningen.
- Testbruker: `data/testbruker.toml` (leses med `tomllib`, kommentar per registrering). Historikken gir grunnnivå blått, ingen aktiv sperre, `antall_hevinger` 1: tre grønne *lett* (én registrert to ganger), en blå *vanskelig* (sperre), en *moderat* (oppheving), og minst én gått tur med fornøydhet 1–2. Faste datoer i fortiden. `lastinn` laster turene først, sletter og gjenskaper testbrukeren (passord som hash) ved hver kjøring, og setter `brukt_heving` til `antall_hevinger − 1` (minst 0). Idempotent, rører ikke andre brukere. Ugyldig fil stopper med norsk melding uten databaseendring. På Vercel kjører `lastinn` i byggesteget, så endringer i testbrukeren forsvinner ved publisering.
- Konvensjoner: domeneord på norsk uten æ/ø/å i identifikatorer, formatering (nivåord, «blått nivå») bare i `domene/`, tester viser til FR-ID, domenetester uten database (`tests/domene/`), web-tester i `tests/web/`.

## UX & Interaction Patterns

- `BARE_OVER_NIVATAK` vises som Tilstandspanel med `h1`, `document.title` lik overskriften og fokus på `h1`. Ny bruker uten registreringer: «Ingen grønne turer passer søket», ingen «Lag konto», med «Endre søk». Bruker med historikk: nivåtaket nevnes i intetkjønn («blått nivå», ved sperre sperrenivået), og overskriften nevner nivåtaket når det er høyere enn grønt.
- Brukertekst kommer fra Mikrotekst i `EXPERIENCE.md`, i jeg-form med du-tiltale. Eksempel på formen: «Du får en blå tur fordi de tre siste grønne turene var lette for deg.»
- Begrunnelsen er alltid merket «Begrunnelse fra mal» i denne epicen.

## Cross-Story Dependencies

- 3.2 bygger på 3.1 (`vurder_historikk`, `Registrering`) og på `velg_turer` fra story 1.8, søketilstanden og søkeflyten fra Epic 1, og historikk-visningen fra story 2.4.
- 3.3 bygger på 3.2 (`nivaheving`, `NivaStatus` i søketilstanden) og på begrunnelsesmalen fra Epic 1. Statusmeldingene bygger videre på story 1.12 og 2.1 (gjestetekst uendret).
- 3.4 bygger på 3.1–3.3 og på `lastinn` (story 1.6), og dekker FR-21 og SM-4. Den utvides i 3.5 uten at nivåstatusen endres.
- 3.5 (P2) utvider 3.1 (`foretrukne_turtyper`, `Registrering.turtyper`), 3.2 (rangering), 3.3 (begrunnelse) og 3.4 (testbruker). Fritekstpunktet i rangeringen kommer i Epic 4 (story 4.7).
- Epic 4 (KI skriver begrunnelsen) bygger videre på personaliseringssetningene her, og setningene legges til etter KI-teksten og telles med i 300-tegnsgrensen.
- Epic 2 (registrering, historikk, `Bruker.brukt_heving`) må være ferdig.
