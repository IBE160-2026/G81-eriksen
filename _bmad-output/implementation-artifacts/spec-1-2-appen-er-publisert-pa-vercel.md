---
title: 'Story 1.2: Appen er publisert på Vercel'
type: 'feature'
created: '2026-11-22'
status: 'done'
baseline_commit: '5a7d255e153ec4d3b6dd2382a7e7a1253962fae5'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-1-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Faglærer og sensor skal kunne åpne appen på en adresse på nett uten å installere noe, og hver PR skal få en forhåndsvisning (NFR-10, AR-24). I dag kjører appen bare lokalt, med SQLite.

**Approach:** Appen gjøres klar for Vercels Django-preset:
- Postgres via `DATABASE_URL`, som tolkes med standardbiblioteket.
- Egne innstillinger når `VERCEL` er satt.
- Byggesteg i `pyproject.toml`.
- `.python-version`, og `vercel.json` med `fra1`.

Hovedøkten oppretter Vercel-prosjektet, Neon-databasen og miljøvariablene på Hannahs konto etter godkjenningene under. Lokal kjøring er uendret.

**Beslutninger (Hannah, 2026-11-22):**
- Vercel installerer fra `pyproject.toml` når den finnes, og hopper da over `requirements.txt` (sjekket i Vercels kildekode). Derfor får `pyproject.toml` en `[project]`-del med de samme låste pakkene som `requirements.txt`, og en test holder de to like. Sensor bruker fortsatt `requirements.txt`. AD-15 punkt 1 presiseres.
- Prosjektet heter `your-next-adventure` under teamet `hannah-eriksen`. Claude kan opprette det og koble det til repoet (`vercel link`, `vercel git connect`).
- Neon kobles til fra Vercel Marketplace med Claude i Chrome: Frankfurt (`aws-eu-central-1`), Production og Preview, og en egen gren for hver forhåndsvisning. Claude stopper og spør før vilkår godtas og før det endelige «opprett».
- Claude legger inn miljøvariablene med Vercel CLI:
  - `DJANGO_SECRET_KEY`: tilfeldig, ulik for produksjon og forhåndsvisning.
  - `MET_USER_AGENT`: i begge miljøene.
  - `ANTHROPIC_API_KEY` legges inn senere, når Hannah har en nøkkel.

## Boundaries & Constraints

**Always:**
- Miljøverdier leses bare i `config/`. Når `VERCEL` er satt:
  - `DEBUG=False` uansett.
  - `ALLOWED_HOSTS=[".vercel.app"]` og `CSRF_TRUSTED_ORIGINS=["https://*.vercel.app"]`.
  - `SECURE_PROXY_SSL_HEADER=("HTTP_X_FORWARDED_PROTO","https")`.
  - Sikre cookies for økt og CSRF.
  - Logging til standard ut.
  - Appen stopper med en norsk `ImproperlyConfigured` hvis `DJANGO_SECRET_KEY` mangler, er tom eller er lik verdien i `.env.example` (lest fra fila, ikke hardkodet).
- Database:
  - Finnes `DATABASE_URL`, brukes Postgres med `DISABLE_SERVER_SIDE_CURSORS=True`.
  - Når `CI` er satt og `DATABASE_URL_UNPOOLED` finnes, brukes den i stedet.
  - Uten `DATABASE_URL` brukes SQLite som før. Ingen ny pakke for å tolke URL-en.
- `STATIC_ROOT = BASE_DIR / "staticfiles"`. Vercel kjører `collectstatic`. Ingen WhiteNoise.
- `check --deploy` med Vercel-innstillingene gir ingen advarsler uten en begrunnelse i en kommentar i settings.
- Ingen hemmelighet står i repoet, i logger eller i tester.

**Never:**
- Ingen `lastinn` i byggesteget. Den kommer i story 1.6.
- Ikke noe eget domene.
- Ingen `ANTHROPIC_API_KEY` i Vercel nå.
- Lokal kjøring krever aldri Vercel, Neon, Vercel CLI eller Node.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Lokalt | ingen `VERCEL`, ingen `DATABASE_URL` | SQLite og DEBUG fra `.env`, som i 1.1 | N/A |
| Vercel, gyldig | `VERCEL=1`, egen nøkkel, `DATABASE_URL` | Postgres via poolen, DEBUG False og innstillingene for Vercel | N/A |
| Bygging | `VERCEL=1`, `CI=1`, begge URL-ene | `DATABASE_URL_UNPOOLED` brukes | N/A |
| Mangler nøkkel | `VERCEL=1`, ingen eller tom `DJANGO_SECRET_KEY` | Stopper | Norsk `ImproperlyConfigured` |
| Utviklingsnøkkel | `VERCEL=1`, nøkkel lik den i `.env.example` | Stopper | Norsk `ImproperlyConfigured` |
| DEBUG på Vercel | `VERCEL=1`, `DEBUG=True` | DEBUG er False | N/A |
| Postgres-URL | `postgresql://u:p%40ss@host:5432/db?sslmode=require&channel_binding=require` | Motor postgresql, NAME `db`, USER `u`, PASSWORD `p@ss`, HOST `host`, PORT `5432`, og `OPTIONS` med `sslmode` og `channel_binding` | Ugyldig skjema gir norsk `ImproperlyConfigured` |

</frozen-after-approval>

## Code Map

- `config/miljo.py` -- `last_inn(base_dir, environ)` og `Miljo`. Vercel-grenen godtar i dag en tom nøkkel. Den skal få vakten og lese `.env.example`. `test_vercel_leser_ikke_env_fila` forventer i dag `secret_key == ""` og må skrives om.
- `config/settings.py` -- `MILJO = miljo.last_inn(...)`. `DATABASES` er hardkodet til SQLite, og `ALLOWED_HOSTS` er lokale verter. `SECURE_CSP` og resten skal ikke endres.
- `pyproject.toml` -- har bare Ruff. Ruff-oppsettet skal beholdes uendret.
- `requirements.txt` -- de tre låste pakkene. `tests/test_kildetre.py::test_pakkene_er_last` sjekker at hver linje har `==`.
- `README.md` -- adressen skal stå øverst. Avsnittet «Installasjon og kjøring» fra 1.1 skal ikke endres.
- Ikke endre `turforslag/`, malene eller migreringene.

## Tasks & Acceptance

**Execution (implementeringsagenten):**
- [x] `requirements.txt` -- legg til `psycopg[binary]==3.3.9` -- AD-15 punkt 1
- [x] `pyproject.toml` -- `[project]` med `name = "your-next-adventure"`, `version = "0.1.0"`, `requires-python = ">=3.12,<3.16"` og `dependencies` lik `requirements.txt`. Legg også til `[tool.vercel.scripts] build = "python manage.py migrate --noinput"` -- AD-15 punkt 1 og 4
- [x] `.python-version` (`3.14`) og `vercel.json` (`{"regions": ["fra1"]}`) -- AD-15 punkt 1–2
- [x] `config/miljo.py` -- vakten for Vercel, og `database_fra_url(url)` som bygger Djangos `DATABASES["default"]` med `urllib.parse`. Den legger til `DISABLE_SERVER_SIDE_CURSORS=True` og spørreparametrene som `OPTIONS`. `Miljo` får `database_url` (riktig URL for kjøring eller bygging) og `vercel: bool` -- AD-15 punkt 3 og 5
- [x] `config/settings.py` -- databasen fra `MILJO`, innstillingene for Vercel og `STATIC_ROOT`. Begrunnelser i kommentarer for advarslene fra `check --deploy` som ikke rettes: Vercel sender alltid 308 til HTTPS, og `*.vercel.app` har HSTS med preload -- AD-15 punkt 4–7
- [x] `tests/` -- tester for matrisen ovenfor, at `[project].dependencies` er lik `requirements.txt`, at `.python-version` og `vercel.json` finnes, og en test som kjører `manage.py check --deploy --fail-level WARNING` i en subprosess med `VERCEL=1` og en gyldig nøkkel og forventer exit 0 -- AR-24
- [x] `README.md` -- adressen øverst (fra Implementation Notes), med en kort forklaring av publiseringen: `main` publiseres automatisk, PR-er får en forhåndsvisning med innlogging hos Vercel, og lokal kjøring krever ingenting av dette -- NFR-10, AD-12 punkt 6
- [x] `ARCHITECTURE-SPINE.md` AD-15 punkt 1 og `.memlog.md` -- presiser at Vercel installerer fra `[project]` i `pyproject.toml`, og at `requirements.txt` holdes lik for lokal kjøring

**Execution (hovedøkten, med Hannahs godkjenning ovenfor):**
- [x] Kjør `vercel link --yes --project your-next-adventure --scope hannah-eriksen` og `vercel git connect`. Noter adressen i Implementation Notes
- [x] Koble til Neon (gjort av Hannah i nettleseren, fordi Chrome hang)
- [x] Legg inn miljøvariablene med `vercel env add`. Verdiene sendes via stdin og skrives aldri ut
- [x] Bekreft at forhåndsvisningen av PR-en bygger og er bak innlogging hos Vercel, og at produksjonen etter merge viser forsiden over HTTPS

**Acceptance Criteria:**
- Gitt PR-en, når Vercel bygger forhåndsvisningen, så går migreringen mot en egen Neon-gren, og siden krever innlogging hos Vercel.
- Gitt en merge til `main`, når Vercel bygger, så vises forsiden på `https://<prosjekt>.vercel.app/` med CSP-hodet.
- Gitt et rent `venv` lokalt, når README følges, så virker alt som før uten Vercel eller Neon.

## Implementation Notes

- 2026-11-22: Hannah godkjente specen og valgte å beholde den hel (ca. 2500 tokens).
- 2026-11-22 (hovedøkten):
  - Vercel-prosjektet `hannah-eriksen/your-next-adventure` er opprettet og koblet til `IBE160-2026/G81-eriksen` (`main` publiseres til produksjon).
  - **Adressen er `https://your-next-adventure.vercel.app`.** Den skal stå øverst i README.
  - Vercel gjenkjenner Django. Innloggingsvernet er Standard Protection (`all_except_custom_domains`).
  - `vercel link` la til `.env*` i `.gitignore`, og den linja ville skjult `.env.example`. Endringen er rullet tilbake, fordi `.env.*` og `.vercel/` allerede er ignorert.
- Hannah kobler til Neon selv i nettleseren, fordi Chrome-automatiseringen hang på Marketplace-siden.
- 2026-11-22: Hannah opprettet Neon-databasen `your-next-adventure` og koblet den til prosjektet (Production og Preview, egen gren for hver forhåndsvisning). Integrasjonen la inn `DATABASE_URL`, `DATABASE_URL_UNPOOLED`, `PG*`, `NEON_*` og `VITE_NEON_AUTH_URL`.
- 2026-11-22: Første publisering (`daced49`, grenen `implementering/story-1-2`) ble satt til **produksjon**. Vercel gjør alltid den første publiseringen i et nytt prosjekt til produksjon.
  - Byggingen brukte Python 3.14 fra `.python-version` og uv. Pakkene ble installert fra `pyproject.toml`, og `migrate` gikk mot Neon.
  - `https://your-next-adventure.vercel.app/` svarer 200, med `h1`, CSP og HSTS. 404-siden er norsk. Produksjonen er offentlig.
- 2026-11-22: Forhåndsvisningen av `adefdb0` er verifisert:
  - Uten innlogging gir den 302 til `vercel.com/sso-api`.
  - Neon-integrasjonen kjørte for forhåndsvisningen («succeeded», `envTarget: preview`), og `migrate` ga «No migrations to apply», fordi grenen er kopiert fra produksjonen.
  - Funksjonen kjører i `fra1` (`X-Vercel-Id: …::fra1::…`).
- Produksjonen kjører allerede samme kode. Når PR #25 er merget, bygges `main` på nytt, og `curl` mot produksjonen gjentas da.

## Spec Change Log

## Review Triage Log

Første gjennomgang (2026-11-22). B = Blind Hunter, E = Edge Case Hunter, V = Verification Gap. VG fant ingen hull i testene. Funnene under «Other» er tatt med.

| # | Funn | Verdikt | Begrunnelse | Rute |
|---|---|---|---|---|
| E1/E10/B1/V-a | På Vercel uten `DATABASE_URL` brukes SQLite uten at noe sies | high | Det er vist i praksis: Neon var opprettet, men ikke koblet til prosjektet, og `vercel env ls` hadde ingen `DATABASE_URL`. Byggingen ville migrert SQLite og blitt grønn, og data ville gått tapt mellom forespørsler, stikk i strid med AD-15 «Prevents». Bare én lesning er mulig, fordi «Uten DATABASE_URL brukes SQLite» gjelder lokal kjøring | patch P1 |
| E9 | `check --deploy` testes bare med SQLite | low | Rettes sammen med P1, fordi testen da må ha en Postgres-URL | patch P1 |
| E2/B2/V-b/E11 | Sjekken av utviklingsnøkkelen hoppes over hvis `.env.example` mangler | false | En endret miljøvariabel virker først etter en ny publisering. Hver publisering bygger og kjører `migrate`, som laster settings med `.env.example` til stede (testet). Nøkkelen kan derfor ikke nå kjøringen uten å passere sjekken | avvist |
| E3 | `VERCEL=0` lokalt regnes som Vercel | low | Skjer sjelden, og rettingen gir en ny regel | avvist |
| E4/B8 | `CI` leses som sann/usann uten `_som_bool` | low | Rettingen er direkte og gir samme tolkning som `DEBUG` | patch P2 |
| E5 | `DATABASE_URL` med bare mellomrom gir feil i stedet for SQLite | low | Rettingen er direkte (`strip`) | patch P2 |
| E6 | `parse_qsl` dropper tomme og doble parametre | low | Neon-URL-er har ikke slike, og rettingen gjør koden mer kompleks | avvist |
| E7 | `ALLOWED_HOSTS` avviser eget domene | false | Intensjonen utelukker eget domene (Never) | avvist |
| E8/B12a | Paritetstesten tåler ikke innrykkede kommentarer eller kommentarer på samme linje | low | Rettingen i testen er direkte | patch P5 |
| B3 | Feil AD-15-punkt i meldingen om manglende nøkkel | false | Meldingen ber om å legge inn variabelen hos Vercel, og det står i punkt 6. Henvisningen er riktig | avvist |
| B4 | `check --deploy` kjøres ikke i byggingen | low | Byggesteget er bestemt i specen og spinen, og nøklene er tilfeldige med 50 byte. Rettingen ville endret specen | avvist |
| B5 | `CSRF_TRUSTED_ORIGINS` med jokertegn stoler på alle Vercel-apper | low | Verdien er bestemt i spinen (AD-15 punkt 5). Andre apper kan ikke lese vår CSRF-cookie, så risikoen er liten. Rettingen ville endret specen | avvist |
| B6 | Begrunnelsen for W004 er unøyaktig | low | HSTS-preload gjelder hele `.app`, og Vercel sender i tillegg HSTS-hodet. Rettingen er en direkte endring av kommentaren | patch P3 |
| B7 | Feil-logger havner på stdout og får ikke feilnivå hos Vercel | low | Specen og AD-15 punkt 7 sier standard ut. Rettingen ville endret specen | avvist |
| B9 | `[project]` uten `[build-system]` kan bli bygget som pakke | false | uv behandler et prosjekt uten `[build-system]` som virtuelt og installerer det ikke som pakke | avvist |
| B10 | Spinen lover at forrige publisering står, men `migrate` har da alt endret databasen | medium | Teksten fantes før denne storyen (AD-15 punkt 4) | defer |
| B11 | README sier ikke hvilke miljøvariabler Vercel trenger | low | Én linje i README, direkte | patch P4 |
| B12b | `test_vercel_leser_ikke_env_fila` sjekker ikke meldingen | low | VG viste at testen skiller tilfellene, men å sjekke meldingen er direkte og gjør den tydeligere | patch P5 |
| B12c | Memlog-beslutningen mangler kilde | low | Kilden kan legges til direkte | patch P6 |

## Verification

**Commands:**
- `python manage.py test` -- forventet: alle grønne
- `ruff check . && ruff format --check .` -- forventet: ingen funn
- `VERCEL=1 DJANGO_SECRET_KEY=<test> python manage.py check --deploy --fail-level WARNING` -- forventet: exit 0
- `curl -sI https://<prosjekt>.vercel.app/` etter merge -- forventet: 200 og `Content-Security-Policy`
