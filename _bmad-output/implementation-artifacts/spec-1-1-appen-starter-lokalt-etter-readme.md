---
title: 'Story 1.1: Appen starter lokalt etter README'
type: 'feature'
created: '2026-11-22'
status: 'done'
baseline_commit: 'f550bb73175dc675a588ff79dd3dbece8694ba85'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-1-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Repoet har ingen kode. Sensor må kunne installere og starte appen bare ved hjelp av README, uten nøkler, Node, Docker eller databaseserver (NFR-1, AR-1). Alle senere stories trenger grunnmuren: kildetreet, den egne brukermodellen i første migrering (AR-9), settings, norske feilsider, CSP og testoppsett.

**Approach:** Lag et Django 6.1.3-prosjekt etter spinen › Structural Seed, med `config/` og appene `turforslag` og `tjenester`, og de tomme pakkene `domene/` og `skript/`. Forsiden viser bare `h1` «Hvor lang tid har du?». Søkeskjemaet kommer i 1.9, og basismalen med tokens kommer i 1.3. Miljøverdiene leses i en liten testbar funksjon som `config/settings.py` kaller.

## Boundaries & Constraints

**Always:**
- Pakkeversjonene er låst etter spinen › Stack. `requirements.txt` har `Django==6.1.3`, `anthropic==2.6.0` og `python-dotenv==1.2.4`. `requirements-dev.txt` har `-r requirements.txt` og `ruff==0.17.4`.
- Miljøverdier leses bare i `config/`. Lokalt (`VERCEL` ikke satt) stopper appen med en norsk melding hvis `.env` mangler eller `DJANGO_SECRET_KEY` er tom. Ingen verdi står som reserve i koden.
- `LANGUAGE_CODE="nb"`, `TIME_ZONE="Europe/Oslo"`, `USE_TZ=True`.
- CSP settes med Djangos `ContentSecurityPolicyMiddleware` og `SECURE_CSP`: `default-src 'self'`, `img-src 'self' https://cache.kartverket.no`, `object-src 'none'`, `base-uri 'self'`, `form-action 'self'` og `frame-ancestors 'none'`. Malene har ingen inline-skript og ingen `style`-attributter.
- Identifikatorene er norske uten æ/ø/å, og koden viser til krav-ID-er (`# NFR-1`, `# AR-9`).
- Ingen test gjør nettverkskall.

**Never:**
- Ingenting for Vercel eller Neon (`psycopg`, `vercel.json`, `.python-version`, settings for `VERCEL`). Det hører til story 1.2.
- Ingen `lastinn`, turmodeller, søkeskjema, designtokens eller egne JS-filer. Det kommer i senere stories.
- Ingen Docker, Node eller npm.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Start lokalt | `.env` kopiert fra `.env.example` | `runserver` svarer på `/` med 200 og `h1` «Hvor lang tid har du?», og tittelen er «Finn tur – Your Next Adventure» | N/A |
| Mangler `.env` | `VERCEL` ikke satt, ingen `.env` | Stopper før oppstart | `ImproperlyConfigured` med norsk melding om å kopiere `.env.example` til `.env` |
| Tom nøkkel | `.env` finnes, `DJANGO_SECRET_KEY=` | Stopper | Samme norske melding |
| `VERCEL` satt | ingen `.env` | Sjekken av `.env` hoppes over. Story 1.2 legger til sin egen sjekk | N/A |
| E-post | `Ola@Eksempel.NO` | Lagres som `ola@eksempel.no` | N/A |
| Kort passord | 7 tegn | Avvises av valideringen | Bare `MinimumLengthValidator(8)` |
| Ukjent adresse | `GET /finnes-ikke/` | 404 med norsk side og lenke til Søk | N/A |
| Ugyldig CSRF | POST uten token | 403 med norsk CSRF-side og lenke til Søk | N/A |
| Serverfeil | et view kaster et unntak | 500 med norsk side og lenke til Søk | N/A |

**Beslutninger (Hannah, 2026-11-22):**
- Tekstene på feilsidene, i jeg-form, føres inn i `EXPERIENCE.md` › Mikrotekst som [ASSUMPTION]. Alle tre har lenken «Gå til Søk».
  - **404:** `h1` «Jeg fant ikke siden», med teksten «Adressen finnes ikke, eller siden er flyttet.»
  - **CSRF (403):** `h1` «Skjemaet kunne ikke sendes», med teksten «Skjemaet var for gammelt, eller nettleseren blokkerte en informasjonskapsel. Gå til Søk og prøv igjen.»
  - **500:** `h1` «Noe gikk galt», med teksten «Noe gikk galt hos meg. Prøv igjen om litt.»
- Specen beholdes hel (ca. 2400 tokens), og Story 1.1 bygges som én enhet.

</frozen-after-approval>

## Code Map

Repoet er nytt. Det finnes ingen Python-kode, og ingenting å gjenbruke. Disse filene skal ikke endres: `_bmad/`, `.claude/`, `.logs/`, `_bmad-output/planning-artifacts/`. `.gitignore` dekker allerede `.env`, `venv/`, `db.sqlite3`, `logs/`, `staticfiles/` og `.vercel/`. README-avsnittet «Installasjon og kjøring» står som «Kommer.» og skal byttes ut.

## Tasks & Acceptance

**Execution:**
- [x] `requirements.txt`, `requirements-dev.txt`, `pyproject.toml` (bare Ruff, `target-version = "py312"`) -- låste versjoner og Ruff-oppsett -- AR-1, AR-15
- [x] `.env.example` -- `DJANGO_SECRET_KEY` med en lokal utviklingsverdi, `DEBUG=True`, `ANTHROPIC_API_KEY=` og `MET_USER_AGENT=YourNextAdventure/0.1 https://github.com/IBE160-2026/G81-eriksen` -- AD-12 punkt 3
- [x] `manage.py`, `config/` (`settings.py`, `miljo.py`, `urls.py`, `wsgi.py`, `asgi.py`) -- `miljo.last_inn(base_dir, environ)` gir verdiene eller kaster en norsk `ImproperlyConfigured`. Settings har nb og Oslo, CSP, `AUTH_USER_MODEL`, passordvalidering med lengde 8 -- AD-12, AR-17
- [x] `turforslag/` (`apps.py`, `models.py`, `admin.py`, `views.py`, `urls.py`, `migrations/0001_initial.py`) -- `Bruker` (`username=None`, `first_name`/`last_name` = None, `email` unik, `brukt_heving`) med `BrukerManager` (`create_user` og `create_superuser`, e-post med små bokstaver også i `save`). Forside-view -- AR-9
- [x] `turforslag/templates/` (`base.html`, `turforslag/sok.html`, `404.html`, `403_csrf.html`, `500.html`) -- `lang="nb"`, tittelmønsteret « – Your Next Adventure», én `main`, ingen inline-stil eller inline-skript -- AD-12 punkt 5
- [x] `tjenester/` (en tom Django-app), `domene/__init__.py`, `skript/__init__.py`, `data/.gitkeep`, `tests/{domene,tjenester,web,fixtures}/` -- kildetreet -- AR-1
- [x] `tests/` -- tester for matrisen ovenfor, at mappene finnes, at `domene/` bare importerer standardbiblioteket (AST og `sys.stdlib_module_names`), CSP-hodet, at `LANGUAGE_CODE`/`TIME_ZONE` er riktige, og at `makemigrations --check` er ren -- AR-2, AR-15
- [x] `README.md` › Installasjon og kjøring -- kommandoene fra story 1.1 for Windows og macOS/Linux, `requirements-dev.txt` for Ruff og `python manage.py test` -- AR-20
- [x] `_bmad-output/planning-artifacts/ux-designs/ux-G81-eriksen-2026-11-06/EXPERIENCE.md` › Mikrotekst -- feilsidetekstene fra beslutningen, merket [ASSUMPTION]

**Acceptance Criteria:**
- Gitt et rent `venv` med Python 3.14, når README-kommandoene kjøres, så starter appen på `http://127.0.0.1:8000/`, og ingen steg krever nøkler, Node, Docker eller databaseserver.
- Gitt repoet, når `python manage.py test`, `ruff check .` og `ruff format --check .` kjøres, så består alle uten nettverkskall.
- Gitt den første migreringen, så peker `AUTH_USER_MODEL` på `turforslag.Bruker`, med `USERNAME_FIELD="email"` og `brukt_heving` med standard 0.

## Implementation Notes

- 2026-11-22, første implementering (subagent):
  - `ALLOWED_HOSTS` er satt eksplisitt til `localhost`, `127.0.0.1` og `[::1]`.
  - `DEBUG` er sann bare for `1`, `true`, `yes`, `on` og `ja`. Mangler verdien, er `DEBUG` usann.
  - Admin ligger på `/admin/` med egne skjemaer for innlogging med e-post.
  - Ruff ignorerer E501 bare i migreringer.
  - Miljøet går foran `.env`.
- Med `DEBUG=True` lokalt viser Django sin egen feilside i stedet for de norske sidene. De norske sidene vises med `DEBUG=False`, som testene bruker.
- README › Mappestruktur sier fortsatt at mappene «kommer med implementeringen». Bare installasjonsavsnittet hørte til denne storyen.

## Spec Change Log

## Review Triage Log

Første gjennomgang (2026-11-22). B = Blind Hunter, E = Edge Case Hunter, V = Verification Gap.

| # | Funn | Verdikt | Begrunnelse | Rute |
|---|---|---|---|---|
| B1/E1/V* | Innlogging med e-post i blandede bokstaver feiler | medium | `BaseUserManager.get_by_natural_key` gjør et eksakt oppslag (`base_user.py:36`), og VG viste at `authenticate("Admin@…")` gir None. Den samme feilen gjør at `createsuperuser` ikke fanger dubletter (`_validate_username` bruker `get_by_natural_key`) | patch P1 |
| B2 | Ingen test for dublett i andre bokstaver | low | Oppførselen er riktig, men ingen test låser den. Testen er enkel å legge til | patch P1 |
| E2 | Admin-skjemaet gir IntegrityError ved dublett | false | `AbstractUser.clean()` normaliserer e-posten (`models.py:504`) før `ModelForm.validate_unique`, så dubletten fanges som valideringsfeil | avvist |
| B3/E5 | HEAD mot `/` gir 405 | low | `require_GET` tillater bare GET. Rettingen er en direkte endring til `require_safe` | patch P2 |
| V2 | Ingen test låser metodene for forsiden | low | Uten dekoratoren vil POST gi 200 uten at noen test feiler. Testen legges til sammen med P2 | patch P2 |
| B4/E6 | Ingen norsk 400- eller 403-side, og 405 har tom kropp | low | Skjer sjelden ved lokal kjøring, og rettingen krever nye tekster som produkteier må godkjenne | avvist |
| B5 | Ingen `LOGGING`, så 500-tracebacks forsvinner når DEBUG=False | low | Lokalt er DEBUG=True, og da logger Django til konsollet. Logging til standard ut på Vercel er et kriterium i story 1.2 (AD-15 punkt 7) | avvist |
| B6/E8/E15 | Vercel-grenen godtar tom nøkkel, og «0»/«false» i `VERCEL` slår av `.env` | low | Det er villet: specen sier at sjekken for Vercel kommer i story 1.2. Vercel setter `VERCEL=1` | avvist |
| E10 | `ALLOWED_HOSTS` mangler Vercel-verter | false | Intensjonen utelukker alt for Vercel (Never) | avvist |
| B7 | Nøkkelen strippes i sjekken, men ikke når den lagres | false | En nøkkel med mellomrom er fortsatt en gyldig hemmelighet, og en nøkkel med bare mellomrom fanges. Ingen skade | avvist |
| B8 | `brukt_heving` kan bli negativ, og mangler `verbose_name` | low | Ingen kode skriver negative verdier, og spinen sier heltall. Merkelappen i admin er kosmetisk, men rettingen er direkte | patch P9 (bare merkelappen) |
| B9 | README sier ikke hvordan admin-bruker lages | low | Admin er tatt med og testet, men kan ikke nås uten `createsuperuser`. Én linje i README | patch P8 |
| B10 | CSRF-teksten gjentar «Gå til Søk» | low | Teksten er Hannahs beslutning i den låste delen. Rettingen ville endret specen | avvist |
| B11 | Python-versjonen håndheves ikke | low | Skjer sjelden, og rettingen gir mer oppsett | avvist |
| B12 | Testen av låste versjoner godtar nye linjer uten låst versjon | low | Rettingen er direkte: hver linje som ikke er en kommentar, må ha `==` | patch P5 |
| B13 | CSP sjekkes bare på `/` | low | Middleware legger hodet på alle svar, men det er ikke testet for feilsidene. Testen er enkel å utvide | patch P6 |
| E3 | `Bruker(email="").save()` lagrer tom e-post | low | Ingen kode gjør dette, og skjemaene krever e-post. Rettingen legger til en vakt | avvist |
| E4 | `update()`/`bulk_create` hopper over normaliseringen | low | Ingen kode bruker dem på e-post. Rettingen er kompleks | avvist |
| E7 | `{% url %}` i 500.html kan feile når URL-oppsettet er ødelagt | low | En feilside skal tåle at resten feiler, og rettingen er direkte (`href="/"`) | patch P3 |
| E9 | Tom `DJANGO_SECRET_KEY` i skallet gir en misvisende melding | low | Skjer sjelden, og rettingen gir en ny gren | avvist |
| E11 | README-kopieringen overskriver `.env` ved ny kjøring | low | Installasjonen kjøres én gang, så det skjer sjelden | avvist |
| E12 | Sjekken av inline-skript kan lures (`data-src`, `javascript:`) | low | Rettingen er en direkte endring i et regulært uttrykk | patch P7 |
| E13 | CSP-testen tåler ikke `;` til slutt | false | Django lager hodet uten `;` til slutt, og testen består | avvist |
| E14 | `importlib.import_module` slipper forbi AR-2-sjekken | low | Skjer sjelden, og rettingen gjør sjekken mer kompleks | avvist |
| V1 | `DEBUG`-tolkningen er testet bare med True og False | low | Hvis `SANNE_VERDIER` blir smalere, feiler ingen test. En tabelltest er enkel | patch P4 |

## Design Notes

`miljo.last_inn` tar `base_dir` og `environ` inn, så testene kan kjøre uten å røre den ekte `.env`. Den laster `.env` med `python-dotenv` bare når `VERCEL` ikke er satt. CSRF-siden heter `403_csrf.html`, som Djangos standard `csrf_failure` ser etter. Da trengs ikke noe eget view eller `CSRF_FAILURE_VIEW`. 500-testen bruker `override_settings(ROOT_URLCONF=...)` med en URL bare for testen som kaster et unntak, og `Client(raise_request_exception=False)`.

## Verification

**Commands:**
- `python manage.py test` -- forventet: alle grønne
- `ruff check . && ruff format --check .` -- forventet: ingen funn
- `python manage.py makemigrations --check --dry-run` -- forventet: «No changes detected»
- røyktest i et nytt `venv` etter README, `runserver` og `curl http://127.0.0.1:8000/` -- forventet: 200, `h1` og et `Content-Security-Policy`-hode
