---
title: 'Story 4.2: Systemet sjekker KI-teksten før den vises'
type: 'feature'
created: '2026-11-27'
status: 'done'
baseline_commit: '8937ba93e3a7bb4cfd11b7d8acfd0bfadbd2fff7'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-4-context.md'
  - '{project-root}/_bmad-output/implementation-artifacts/spec-4-1-ki-tjenesten-har-ett-grensesnitt.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** KI kan skrive tall, nivåord og feil turtype i begrunnelsen, og teksten kan bli for lang. Uten en sjekk kan Ola få falske opplysninger (FR-12, FR-13, AD-10, AR-12, AR-16).

**Approach:** Én ren funksjon i `domene/` validerer KI-teksten (med plassholdere) og gir enten den ferdige teksten eller en forkastelse med årsak. Verdiene settes inn fra turdata og søk i de samme formatene som reservemalen bruker. Funksjonen kobles ikke til visningen her (det gjør story 4.5).

## Boundaries & Constraints

**Always:**
- Funksjon `valider_begrunnelse(tekst, sok, tur, status, tillegg=())` i `domene/` (bare standardbiblioteket, ingen database, nett eller klokke). `sok` er `domene.sok.Sok`, `tur` er `domene.tur.Tur`, `status` er `domene.utvalg.Status`, `tillegg` er de ferdige setningene systemet lager (personaliseringssetning fra 3.3 og preferansesetning fra 3.5). Resultat: frossen dataklasse med enten ferdig `tekst` eller en `Forkastelse` (`StrEnum`: `tom`, `ugyldig`, `siffer`, `tallord`, `nivaord`, `turtype`, `for_lang`). Forkastelsene er et eget begrep, ikke `KiSvar.arsak` fra 4.1 (transportfeil).
- Rekkefølge: Unicode-normalisering (NFC) av input, så `tom`, plassholdere, `siffer`, `tallord`, `nivaord`, `turtype`, innsetting, tillegg, lengde.
- `tom`: tom eller bare mellomrom. `ugyldig`: andre plassholdere enn `{tid}`, `{varighet}`, `{lengde}`, `{nivå}` (også `{Tid}`, `{niva}`, `{pris}`), en løs `{` eller `}`, eller uten `{varighet}`. Samme plassholder kan stå flere ganger. `{tid}`, `{lengde}`, `{nivå}` er valgfrie.
- `siffer`: ethvert siffer utenfor plassholderne, også andre Unicode-sifre (`str.isdigit()`). `tallord`: «to» til «tjue», tiere til «nitti», «hundre», «tusen», «halv», «halvannen», «halvtime», «kvarter» som hele ord, uten hensyn til store/små bokstaver. «en», «én», «ett», «ei» bare rett foran time/timer/minutt/minutter/min/sekund/sekunder/km/kilometer/meter/mil. Ord som bare inneholder et tallord («toppen», «tiden») er lov. Lister i én konstant.
- `nivaord`: grønn/grønne/grønt, blå/blått, rød/røde/rødt, svart/svarte som hele ord, uten hensyn til store/små bokstaver. «Svartkulp» og «blåbær» er lov.
- `turtype`: med valgt turtype i søket forkastes teksten hvis ingen ord inneholder stammen («marka», «utsikt», «topptur», som delstreng, uten hensyn til store/små bokstaver: «Nordmarka», «utsikten», «toppturer»). Ved `TOPPTUR_ERSTATTET` må teksten nevne «utsikt». Uten valgt turtype sjekkes ingen. Stammene i én konstant.
- Innsetting etter sjekkene, i reservemalens formater: `{tid}` → `formater_tid(tur.estimert_tid_min)`, `{varighet}` → `formater_varighet_timer(sok.varighet_min)`, `{lengde}` → `formater_lengde(total_lengde_m(tur.form, tur.lengde_m))` (ikke `formater_lengde_totalt`), `{nivå}` → `nivaord(tur.turniva)` (alltid hankjønn). Sifrene og nivåordene som settes inn, gir ikke forkasting.
- Tillegg legges til etter KI-teksten (med ett mellomrom) og sjekkes ikke for tall og nivåord. Lengden telles slik brukeren ser den: etter innsetting, med tillegg, uten KI-merket. Linjeskift og gjentatte mellomrom blir ett mellomrom, mellomrom først og sist fjernes, og den normaliserte teksten returneres. 300 tegn godtas, 301 gir `for_lang`, også når KI-teksten alene er under 300.
- Eksemplet fra Mikrotekst gir nøyaktig «Turen tar ca. 1 t 35 min, så den passer innenfor 2 timer. Den har utsikt, som du ba om, og er grønn, som passer når du er ny.» (tur 95 min, grønn, utsikt; søk 120 min, turtype utsikt, status `TREFF`).

**Never:**
- Ingen kobling til `turforslag/sokflyt.py`, visning, KI-kall, logg eller grense (4.3–4.5). Ingen endring av `KiSok`/`KiTur`/`KiSvar` eller av reservemalen. Ingen ny avhengighet, ingen migrasjon.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Mikrotekst-eksempelet | gyldig KI-tekst med `{tid}`, `{varighet}`, `{nivå}` | nøyaktig ferdig tekst over | N/A |
| Tom | `""` / `"   "` | forkastet `tom` | N/A |
| Plassholder | `{Tid}`, `{niva}`, `{pris}`, løs `{`/`}`, mangler `{varighet}` | forkastet `ugyldig` | N/A |
| Siffer | «2 timer», «5 km», «1,5», arabisk-indisk siffer | forkastet `siffer` | N/A |
| Tallord | «to», «Tolv», «halvtime», «en time», «en fin tur» | forkastet (unntatt «en fin tur»); «toppen» og «tiden» lov | N/A |
| Nivåord | «grønn», «Blått», «svarte»; «Svartkulp», «blåbær» | forkastet `nivaord`; delord lov | N/A |
| Turtype | søk topptur, tekst uten «topptur»; `TOPPTUR_ERSTATTET` uten «utsikt» | forkastet `turtype`; «Alle turtyper»: ikke sjekket | N/A |
| Lengde | 300 / 301 tegn etter innsetting + tillegg | godtatt / `for_lang` | N/A |
| Tillegg gjør for lang | KI-tekst < 300, med tillegg > 300 | `for_lang` | N/A |

</frozen-after-approval>

## Code Map

- `domene/begrunnelse.py` -- `reservebegrunnelse`, `MAKS_TEGN = 300`, `personaliseringssetning`, `preferansesetning`. Ny validator her eller i ny modul i `domene/` (unngå importsyklus: `begrunnelse` importerer `tekst`, `sok`, `tur`, `utvalg`).
- `domene/tekst.py` -- `formater_tid`, `formater_varighet_timer`, `formater_lengde` (ikke `formater_lengde_totalt`), `nivaord`. `domene/tur.py` -- `total_lengde_m(form, lengde_m)`, `TURTYPER`. `domene/utvalg.py` -- `Status`, `TOPPTUR`, `ERSTATNING_FOR_TOPPTUR`. `domene/ki.py` -- urørt (har `ARSAK_UGYLDIG` for transport).
- Tester: ny `tests/domene/test_ki_validering.py` (unittest, `lag_tur` fra `tests/domene/test_utvalg`, `# FR-12, FR-13`, `subTest`), `tests/domene/test_bare_standardbibliotek.py` må bestå.
- Kommer senere: 4.5 kobler funksjonen inn i `sokflyt.forslagsvisning` (erstatter `svar.tekst if svar.ok …`), 4.3 logger forkastelsene.

## Tasks & Acceptance

**Execution:**
- [ ] `domene/` -- `Forkastelse`, resultat og `valider_begrunnelse` med ordlister som konstanter -- FR-12, FR-13, AR-12
- [ ] `tests/domene/test_ki_validering.py` -- et eget testtilfelle per årsak og kanttilfelle i matrisen (inkludert «toppen»/«tiden», «Svartkulp»/«blåbær», Unicode-siffer, 300/301, tillegg som gjør for lang, Mikrotekst-eksempelet) -- SM-2

**Acceptance Criteria:**
- Given hele testsuiten og ruff, when de kjøres, then er alt grønt og ingenting i visningen er endret.
- Given funksjonen, when den importeres, then bruker den bare standardbiblioteket og `domene/`.

## Implementation Notes

- Nye filer: `domene/ki_validering.py` (`Forkastelse`, `Valideringsresultat`, `valider_begrunnelse`, ordlister som konstanter), `tests/domene/test_ki_validering.py`. Ingen kobling til `sokflyt` (story 4.5). Valg: `isnumeric()` for siffer, «sju» og «syv», «tyve», «tredve» og «tretti» tatt med blant tallordene.

## Spec Change Log

## Review Triage Log

- patch (medium): `isdigit()` slapp gjennom «½» og «Ⅻ». Bytter til `isnumeric()`, med tester. Rettet.
- patch (medium): usynlige tegn (nullbredde, myk bindestrek) kunne dele «grønn»/«to» og skjule dem for ordsjekkene. Kategori Cf fjernes etter NFC, med tester. Rettet.
- patch (low): en plassholder limt til bokstaver («to{tid}», «Sv{varighet}artkulp») ga to adskilte ord i sjekken og ett usjekket ord i ferdig tekst. Gir nå `ugyldig`, med tester. Rettet.
- patch (low): NFC-testen testet ikke normaliseringen, og lengdetesten brukte 300/301 som literaler. Rettet.
- false: `KeyError` ved ukjent turtype. `Sok` validerer turtypen i `__post_init__`.
- false: TOPPTUR_ERSTATTET godtar «topptur» sammen med «utsikt». Spec krever bare at teksten nevner utsikt.
- false: turtypesjekk ved `BARE_OVER_NIVATAK`/`INGEN_TREFF`. Validatoren kalles bare når en tur vises.
- rejected low: sammensatte tallord («tjueto», «tretimers»), flere tallord (null, dobbel, ordenstall), «tre» og «mil» som falske positiver (listen er definert av AC), `Valideringsresultat` uten tilstandssjekk, tillegg som ikke sjekkes for tomme klammer, lat utregning av verdier, harde mellomrom, forklaringer i kommentarer.
- Verification Gap-reviewer: ingen hull.

## Design Notes

Avklart uten å spørre: preferansesetningen telles med i 300 tegn via `tillegg`; `{nivå}` settes alltid inn i hankjønn; turtypesjekken bruker delstreng, tallord og nivåord hele ord; den normaliserte teksten (ett mellomrom) er den som returneres; NFC-normalisering først, så «å» i `{nivå}` tåler begge former.

## Verification

**Commands:**
- `venv/Scripts/python.exe manage.py test` -- expected: alle grønne
- `venv/Scripts/python.exe -m ruff check .` -- expected: ingen funn
