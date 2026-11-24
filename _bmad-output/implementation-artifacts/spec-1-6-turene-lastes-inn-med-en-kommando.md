---
title: 'Story 1.6: Turene lastes inn med én kommando'
type: 'feature'
created: '2026-11-24'
status: 'done'
baseline_commit: 'c5a414ee234c0231f1ea7a9812b7f44703045b7a'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-1-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** `data/turer.geojson` finnes (1.5), men databasen har ingen turer. Sensor og Vercel trenger én kommando som laster turene inn, og appen skal senere lese nivå, høydemeter og tid fra databasen uten å regne dem på nytt (AD-3 punkt 4–6, AR-5, AR-6).

**Approach:** Nye modeller `Startpunkt` og `Tur` i `turforslag/` med migrering `0002` (bare portable felt, `JSONField` for geometri, høydeprofil og turtyper). `python manage.py lastinn` leser fila via `domene.tur.Tur.fra_geojson_feature`, validerer alt i minnet og oppretter eller oppdaterer så startpunkter og turer etter `id` i én transaksjon. Byggesteget på Vercel kjører `lastinn` etter `migrate`, og README får `lastinn` som eget steg.

**Beslutninger (Hannah, party-runde 2026-11-24):**
- **Ingen admin** for `Startpunkt` og `Tur` i 1.6. Fila er eneste kilde, og utskriften fra `lastinn` viser hva som er lastet inn.
- **Advarsel for turer som mangler i fila:** finnes det turer i databasen som ikke er i fila, skriver `lastinn` en norsk advarsel med ID-ene (sortert) og fortsetter. Ingenting slettes. Bakgrunn: testturene fra 1.5 blir ellers liggende usynlig i Neon hvis 1.7 bruker andre ID-er (avgjøres i 1.7).
- **Valideringen av hele fila ligger i `domene/tur.py`:** en ny funksjon `valider_turer(turer)` stopper ved dublett av tur-ID, samme startpunkt-ID med ulikt navn, koordinat eller høyde, og turtyper utenfor `marka`, `utsikt` og `topptur` (tom liste er lov). Den kaster `ValueError` med norsk melding og ID. Byggeskriptet kan bruke den senere, men endres ikke i 1.6.
- **Bakoverkompatible migreringer:** AD-15 punkt 4 i spinen får én setning om at migreringer bare legger til (ikke fjerner eller gir nytt navn), fordi `migrate` har endret databasen før `lastinn` kan feile. Raden i `.memlog.md` og et nytt «Avklart»-punkt i `deferred-work.md` lukker det åpne punktet fra spec 1.2.
- Specen beholdes hel (ca. 3300 tokens).

## Boundaries & Constraints

**Always:**
- `Startpunkt`: `id` (`CharField`, primærnøkkel), `navn`, `lat`/`lon` (`FloatField`), `hoyde_m` (`IntegerField`). `Tur`: `id` (`CharField`, primærnøkkel), `navn`, `startpunkt` (`ForeignKey`, `on_delete=PROTECT`), `form` og `turniva` (`CharField` med valg fra `domene.tur.Form`/`Turniva`), `turtyper`, `hoydeprofil` og `geometry` (`JSONField`), `lengde_m`, `hoydemeter_m`, `nedstigning_m` og `estimert_tid_min` (`PositiveIntegerField`), `ut_no_url` (tom tillatt), `kilde`, `lisens`. Feltnavn som i dataklassen, så omgjøringen blir én-til-én. Norsk `verbose_name`, `__str__` og `Meta.ordering = ["id"]`.
- Omgjøringen ligger i ny `turforslag/turdata.py`: `lagre_turer(turer)` (startpunkter først, så turer, `update_or_create` etter `id`) og `tur_fra_modell(modell) -> domene.tur.Tur` (lister fra JSON blir tuples). Kommandoen leser fila, kaller `domene` og `turdata` og skriver ut resultatet; den regner ikke selv (AD-2).
- Hele fila leses og valideres før noe skrives. Skrivingen skjer i `transaction.atomic()`.
- Feil gir `CommandError` med norsk melding som nevner fila og, der det gjelder, tur-ID: fila mangler eller kan ikke leses, ugyldig JSON, ikke en `FeatureCollection`, en feature som `fra_geojson_feature` avviser (`ValueError`, `KeyError`, `TypeError`, `AttributeError`), og alt `domene.tur.valider_turer` avviser.
- Utskrift ved suksess: én norsk linje med antall turer og startpunkter, fordelt på nye og oppdaterte. `lagre_turer` returnerer også ID-ene til turer i databasen som ikke er i fila, og kommandoen skriver advarselen ut fra dem.
- `--fil` (valgfri sti) gjør kommandoen testbar; standard er `data/turer.geojson` under `BASE_DIR`.
- Byggesteget blir `python manage.py migrate --noinput && python manage.py lastinn`. Testen i `tests/web/test_vercel.py` følger med.

**Never:**
- Ingen sletting av turer eller startpunkter, ingen `delete()`/gjenoppretting.
- Ingen kall til `gradering`, `tid` eller andre beregninger i `lastinn` eller `turdata`; verdiene lagres som de står i fila.
- Ingen GeoDjango, rå SQL, JSON-oppslag i spørringer eller databasespesifikke felt. `0001_initial` endres ikke.
- Ingen `Registrering`, testbruker, admin eller visning av turer (Epic 2, Epic 3, Story 1.9). Ingen endring av `data/turer.geojson` eller `skript/`.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Første kjøring | tom database, ekte `turer.geojson` (3 turer, 2 startpunkter) | 3 turer og 2 startpunkter opprettet, «nye» i utskriften | N/A |
| Andre kjøring | samme fil | samme antall, alle «oppdaterte» | N/A |
| Endret verdi | tur med nytt navn eller ny `lengde_m` i fila | raden oppdateres, antallet uendret | N/A |
| Tur mangler i fila | tur finnes i databasen, ikke i fila | turen står uendret, resten lastes inn | norsk advarsel med ID-ene, exit 0 |
| Fila mangler | `--fil` peker til ikke-eksisterende fil | databasen uendret | norsk melding, exit ≠ 0 |
| Ødelagt fil | ugyldig JSON, eller `FeatureCollection` uten `features` | databasen uendret | norsk melding |
| Ugyldig tur | feature nr. 2 mangler `lengde_m` | databasen uendret, heller ikke tur nr. 1 | norsk melding med tur-ID |
| Dublett | samme tur-ID to ganger | databasen uendret | norsk melding med tur-ID |
| Ulikt startpunkt | samme startpunkt-ID med ulikt navn | databasen uendret | norsk melding med startpunkt-ID |
| Ukjent turtype | `turtyper: ["utsiktt"]` | databasen uendret | norsk melding med tur-ID og turtype |

</frozen-after-approval>

## Code Map

- `domene/tur.py` -- `Tur` (frosset dataklasse, :28–54) med flate startpunktfelt `startpunkt_id/_navn/_lat/_lon/_hoyde_m`; `Form`, `Turniva` (`StrEnum`); `fra_geojson_feature` (:88) kaster `ValueError`/`KeyError`/`TypeError`/`AttributeError` og sjekker ikke turtyper, tomme ID-er eller dubletter.
- `turforslag/models.py` -- bare `BrukerManager` og `Bruker`. Følg stilen (norsk `verbose_name`, `Meta`). Ruff DJ-regler: `__str__` på alle modeller (DJ008), rekkefølgen felt → `Meta` → `__str__` (DJ012), ingen `null=True` på `CharField` (DJ001).
- `turforslag/migrations/0001_initial.py` -- ikke rør. Ny `0002` lages med `makemigrations`. `tests/web/test_bruker.py:115` kjører `makemigrations --check`.
- `turforslag/management/commands/` -- finnes ikke. Lag `management/__init__.py`, `commands/__init__.py` og `lastinn.py`.
- `pyproject.toml` -- `[tool.vercel.scripts] build = "python manage.py migrate --noinput"`, med kommentaren «`lastinn` kommer i story 1.6».
- `tests/web/test_vercel.py:77–80` -- `test_byggesteget_migrerer` sammenligner build-strengen eksakt.
- `README.md` -- :26 status «story 1.1–1.5»; :37–44 (Windows) og :49–56 (macOS/Linux) har `migrate` → `runserver` (sett `lastinn` mellom); :70 sier at `lastinn` kommer senere; :81 beskriver byggesteget.
- `data/README.md` -- formatet på `turer.geojson`. Legg til én linje om `lastinn`.
- `data/turer.geojson` -- `FeatureCollection` med 3 features og 2 startpunkter. Ikke rediger; `tests/skript/test_bygg_turdatabase.py:172` sjekker den mot fixtures.
- `skript/bygg_turdatabase.py` -- mønster for norske feilmeldinger (`ByggFeil`). Endres ikke i 1.6.
- `ARCHITECTURE-SPINE.md` (`_bmad-output/planning-artifacts/architecture/architecture-G81-eriksen-2026-11-07/`) AD-15 punkt 4 (ca. l. 199) og `.memlog.md` der (rader `- (decision) <dato>, story …`).
- `_bmad-output/implementation-artifacts/deferred-work.md` -- første punkt (fra spec 1.2) om bakoverkompatible migreringer. Ikke endre punktet; legg til et nytt punkt med `summary: Avklart 2026-11-24: …` (samme mønster som l. 15).
- Testmønster: `unittest.TestCase` i `tests/domene/` (uten database; `test_bare_standardbibliotek.py` dekker `domene/` automatisk), `django.test.TestCase` i `tests/web/`, krav-ID i kommentar (`# AR-5`).

## Tasks & Acceptance

**Execution:**
- [x] `domene/tur.py` og `tests/domene/test_tur.py` -- `TURTYPER` og `valider_turer(turer)` med tester for dublett, ulikt startpunkt, ukjent turtype og gyldig liste -- AD-3 punkt 5, AR-2
- [x] `turforslag/models.py` -- `Startpunkt` og `Tur` etter Always -- AD-3 punkt 5, AR-6
- [x] `turforslag/migrations/0002_*.py` -- generert med `makemigrations`, sjekket at den bare oppretter tabeller -- AR-6
- [x] `turforslag/turdata.py` -- `lagre_turer` og `tur_fra_modell` -- AD-3 punkt 4–5
- [x] `turforslag/management/commands/lastinn.py` (+ `__init__.py`-filer) -- les, valider, lagre atomisk, norsk utskrift og `CommandError` -- AR-5
- [x] `pyproject.toml` og `tests/web/test_vercel.py` -- build-streng med `lastinn` -- AD-15 punkt 4
- [x] `README.md` og `data/README.md` -- `lastinn` som eget steg, status 1.1–1.6, byggesteget -- AR-5
- [x] `ARCHITECTURE-SPINE.md` AD-15 punkt 4, `.memlog.md` og `deferred-work.md` -- setningen om bakoverkompatible migreringer, og det åpne punktet lukkes -- AD-15
- [x] `tests/web/test_lastinn.py` og `tests/web/test_turdata.py` -- én test per rad i matrisen, pluss tur-fra-modell-testene under -- AR-5, AR-6

**Acceptance Criteria:**
- Gitt den committede `data/turer.geojson`, når den lastes inn og hver tur leses tilbake med `tur_fra_modell`, så er resultatet lik `Tur.fra_geojson_feature` for samme feature.
- Gitt en tur i databasen med `turniva`, `hoydemeter_m` og `estimert_tid_min` som ikke stemmer med `domene.gradering`/`domene.tid`, når `tur_fra_modell` kjøres, så returneres de lagrede verdiene uendret, og `lastinn` og `turdata` kaller aldri `gradering.turniva` eller `tid.estimert_tid_min` (testet med `mock.patch` som kaster).
- Gitt en tur som peker på et startpunkt, når startpunktet forsøkes slettet, så stopper `ProtectedError` det.

## Design Notes

- To-trinns: `les_fil(sti) -> list[domene.tur.Tur]` (all lesing og validering) og så `lagre_turer(turer)` inne i `transaction.atomic()`. En feil i trinn 1 gjør at trinn 2 aldri starter; en feil i trinn 2 ruller tilbake.
- Modellen og dataklassen heter begge `Tur`. Importer domenet som modul (`from domene import tur as domenetur`) så navnene ikke kolliderer.

## Verification

**Commands:**
- `python manage.py test` -- forventet: alle grønne, uten nettverk
- `ruff check . && ruff format --check .` -- forventet: ingen funn
- `python manage.py makemigrations --check --dry-run` -- forventet: «No changes detected»
- `python manage.py migrate && python manage.py lastinn && python manage.py lastinn` -- forventet: 3 turer og 2 startpunkter begge ganger, «nye» første gang og «oppdaterte» andre gang

**Manual checks:**
- Byggeloggen til forhåndsvisningen på Vercel (Neon Postgres) viser at `migrate` og `lastinn` kjører uten feil.

## Implementation Notes

- 2026-11-24: Hannah godkjente specen etter party-runden (1A, 2B, 3A, 4A) og valgte å beholde den hel.
- 2026-11-24 (implementering): `Startpunkt` og `Tur` i `turforslag/models.py` med migrering `0002_startpunkt_tur` (bare to `CreateModel`). `turforslag/turdata.py` har `lagre_turer` (atomisk, returnerer `Lagret` med nye/oppdaterte og `mangler_i_fila`) og `tur_fra_modell`. `lastinn` har `--fil`; advarselen går til stderr, oppsummeringen til stdout. `CharField`-lengder: ID 100, navn 200, `ut_no_url` 500, `kilde`/`lisens` 100.
- 2026-11-24 (etter review): `valider_turer` stopper også ved ID som ikke er en ikke-tom tekst og ved negative heltall; `DatabaseError` under lagring blir `CommandError` (gammelt innhold står); fila leses som `utf-8-sig`; matrisetestene bruker `tests/fixtures/turer_lastinn.geojson`, så 1.7 kan bytte `data/turer.geojson` uten å knekke dem; «databasen uendret» sjekkes mot fulle rader etter en gyldig innlasting; importsjekk for at `turdata`/`lastinn` aldri importerer `gradering`/`tid`; regelen for nye felt (`null` eller `db_default`) står i AD-15 punkt 4.
- 2026-11-24 (verifisering): 237 tester grønne uten nett, Ruff og `makemigrations --check` rene, `lastinn` to ganger gir samme antall. Gjenstår: byggeloggen på Vercel-forhåndsvisningen (Neon Postgres) når PR-en er åpnet.

## Spec Change Log

## Review Triage Log

Første gjennomgang (2026-11-24). B = Blind Hunter, E = Edge Case Hunter, V = Verification Gap. Diffen tok ikke med workflow-filene (`epic-1-context.md`, `sprint-status.yaml`, party-minnet og denne specen).

| # | Funn | Verdikt | Begrunnelse | Rute |
|---|---|---|---|---|
| E1/E2/E3/E-krav/B3a/V-andre | Verdier som `fra_geojson_feature` godtar, men databasen avviser (negative heltall, `null` i tekstfelt, for lange strenger på Postgres), gir rå `IntegrityError`/`DataError` i stedet for norsk melding. Numerisk `id` (`1` og `"1"`) slipper gjennom `valider_turer` og overskriver hverandre stille | medium | Det er reelt: `lagre_turer` ruller tilbake, men `handle` fanger ikke `DatabaseError`, og `valider_turer` sjekker ikke typen på ID-er. Intensjonen lover norsk melding ved ugyldig fil. Rettingen er direkte: ID-er må være ikke-tomme strenger, heltallsfeltene ≥ 0, og `DatabaseError` blir `CommandError` | patch |
| V1 | Grenen «kan ikke leses» (`OSError`/`UnicodeDecodeError`) og vakten for en feature som ikke er et objekt, er ikke testet | medium | Forhåndsverifisert av VG: å fjerne grenen ville ikke fått noen test til å feile | patch |
| B5 | Testene låser antall (3/2), `sognsvann` og at to turer deler startpunkt i dagens `data/turer.geojson`. 1.7 bytter fila til 15 turer og knekker dem | medium | Det er reelt: det treffer `test_lastinn.py` og `test_turdata.py` i 1.7. Rettingen er en fast kopi i `tests/fixtures/` for matrisetestene, og at antall avledes fra fila der den ekte fila brukes | patch |
| B7 | «Databasen uendret» testes mot en tom database og bare noen kolonner | medium | Det er reelt: en implementering som endret rader før feilen, ville bestått. Rettingen er å laste gyldige data først og sammenligne hele rader | patch |
| B1 | Regelen om bakoverkompatible migreringer dekker ikke nye felt uten null eller `db_default` (Djangos `default=` finnes bare i Python) | medium | Det er reelt: gammel kode som setter inn rader, feiler mot en ny NOT NULL-kolonne. Det er en presisering av teksten i spinen, README og `.memlog.md`, i tråd med beslutningen | patch |
| B6 | Testene for «regner aldri» patcher modulattributter og fanger ikke `from domene.gradering import …` | low | Det er reelt, men i dag importerer ingen av modulene `gradering`/`tid`. Rettingen er en direkte importsjekk | patch |
| E5 | En fil med UTF-8-BOM avvises som ugyldig JSON | low | Det er reelt hvis fila redigeres i en Windows-editor. Rettingen er `utf-8-sig`, som er direkte | patch |
| B11a | README og `data/README.md` nevner verken `--fil` eller advarselen | low | Det er en direkte retting av teksten | patch |
| E13/B9 | Startpunkter i databasen som ingen tur i fila bruker, gir ingen advarsel | maybe-false | Er det sant, blir det medium i 1.9 hvis lista over startpunkter hentes fra `Startpunkt`-tabellen. Det avgjøres av hvordan 1.9 bygger startpunktvalget | defer |
| E4 | `NaN`/`Infinity` i JSON | low | Fila lages av byggeskriptet, så det skjer ikke i praksis. En vakt gir ny logikk | avvist |
| E6 | `RecursionError` ved dypt nøstet JSON | low | Det skjer ikke i praksis | avvist |
| E7 | Tom `features` laster 0 turer | low | Advarselen viser alle turer som mangler, så det synes. En vakt gir ny logikk | avvist |
| E8/E9 | `turtyper` som streng, eller samme turtype to ganger | low | Strengen stopper med norsk melding (ukjent turtype). Dubletter er ufarlige og skjer sjelden | avvist |
| E10/E11/B3b | Innholdet i `geometry` og `hoydeprofil`, og `int()` som kutter desimaltall, sjekkes ikke | low | Det finnes fra før i `fra_geojson_feature` (1.5). Fila lages av skriptet | avvist |
| E12 | Et startpunkt som oppdateres, endrer også turer som er beholdt | false | Det er meningen: startpunktet har én kilde, og turen viser til det | avvist |
| E14 | To bygg kjører `lastinn` samtidig på samme Neon-gren | low | Det skjer sjelden. Bygget feiler synlig og kan kjøres på nytt | avvist |
| E15 | Ukjent `turniva`/`form` i databasen | low | Databasen skrives bare av `lastinn` med gyldige verdier | avvist |
| B2 | Ingen test håndhever migreringsregelen | low | Det er en ny test for fremtidige stories, ikke for denne storyen. Regelen står i spinen | avvist |
| B8 | Grammatikken i utskriften («1 turer», «1 nye») | low | Det gjelder bare antall 1, og rettingen gir nye greiner | avvist |
| B10 | «Oppdaterte» teller også rader som ikke endret seg | low | Rettingen krever sammenligning før lagring | avvist |
| B11b | README sier 1.1–1.6 mens storyen er `in-progress` | false | Samme mønster som 1.5: README beskriver tilstanden etter merge | avvist |
| B12 | AD-15 punkt 4 nevner testbrukeren | false | Teksten fantes fra før og beskriver målbildet (Epic 3), noe epic-konteksten sier | avvist |
| B13 | Diffen mangler workflow-filer | false | De er tatt ut med vilje | avvist |
| B14 | Feilmeldingen for startpunkt viser rå tuples | low | Skriptet sjekker det samme før fila lages, så det skjer sjelden | avvist |
| B15 | `choices` uten norske etiketter | low | Formatering skjer i `domene/`, og etikettene vises ingen steder | avvist |
