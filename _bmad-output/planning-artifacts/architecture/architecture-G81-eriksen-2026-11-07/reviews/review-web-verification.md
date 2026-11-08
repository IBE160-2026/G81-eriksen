# Webverifisering — Architecture Spine, Your Next Adventure (G81-eriksen)

Gjennomgått: `ARCHITECTURE-SPINE.md` (oppdatert 2026-11-08) og `.memlog.md`. Spinen er ikke endret.
Linse: Er hvert bindende valg (versjoner, teknologier, standardverdier og eksterne vilkår) sjekket mot nettet eller gjeldende dokumentasjon, eller er det bare påstått ut fra treningsdata?
Sjekket 2026-11-08 mot PyPI JSON, npm-registeret, djangoproject.com, Django-kildekoden (tag 6.1.3), platform.claude.com, python.org og direkte HTTP-kall mot Kartverket, Geonorge og MET. Kallene til api.met.no brukte User-Agent `G81-eriksen-review`.

## Overall verdict

**Godkjent, med rettelser.** Alle versjonsnumre i Stack stemmer med det som er nyeste i dag. Ingen pakker er trukket tilbake (yanked), og alle URL-er og grenser svarer slik spinen sier. Memloggen viser at versjonene faktisk ble slått opp (2026-11-07/08). Det er likevel tre steder der spinen bygger på en standardverdi eller en antakelse om hvordan noe passer sammen, som ikke ble sjekket, og som ikke holder helt:

1. `httpx` 0.28.1 er riktig nummer, men feil pakke. Anthropic-SDK-en har gått over til `httpx2`.
2. KI-modellens standardoppsett (adaptiv tenkning, effort `medium`, SDK-tidsavbrudd på 10 min og 2 nye forsøk) passer ikke med 5-sekundersgrensen i AD-10.
3. Påstanden «Django anbefaler egen brukermodell» står ikke i dagens Django-dokumentasjon. Valget er likevel riktig.

Ingen av funnene er blokkerende. De bør rettes før stories skrives, fordi de bestemmer hva en KI-agent vil skrive i `requirements.txt` og i `tjenester/ki/`.

## Verifiseringstabell

| # | Påstand i spinen | Resultat i dag | Kilde | Status |
| --- | --- | --- | --- | --- |
| 1 | Django 6.1.3 | Nyeste på PyPI, lastet opp 2026-11-03, ikke yanked. `requires_python >=3.12` | https://pypi.org/pypi/django/json, https://www.djangoproject.com/download/ | OK |
| 2 | Django 6.1 støtter Python 3.14 | «Django 6.1 supports Python 3.12, 3.13, 3.14, and 3.15 (as of 6.1.3)». Mainstream-støtte til april 2027, utvidet til desember 2027 | https://docs.djangoproject.com/en/6.1/releases/6.1/ | OK |
| 3 | `SESSION_COOKIE_AGE` standard 1 209 600 s | «Default: 1209600 (2 weeks, in seconds)». Merk at `SESSION_EXPIRE_AT_BROWSER_CLOSE=False` og `SESSION_SAVE_EVERY_REQUEST=False` også er standard | https://docs.djangoproject.com/en/6.1/ref/settings/ | OK, men se F5 |
| 4 | `login()` beholder øktdata | Stemmer for gjest → innlogging: `cycle_key()` beholder dataene. Økten tømmes (`flush()`) hvis en *annen* bruker var logget inn, og `logout()` tømmer alt | https://docs.djangoproject.com/en/6.1/topics/auth/default/, kildekode `django/contrib/auth/__init__.py` på tag 6.1.3 | OK, se F5 |
| 5 | «Django anbefaler egen brukermodell før første migrering» | Dokumentasjonen for 6.1 (og 5.2) sier «you **can** set up a custom user model», ikke «highly recommended». Advarselen om at det er vanskelig å bytte `AUTH_USER_MODEL` senere står fortsatt | https://docs.djangoproject.com/en/6.1/topics/auth/customizing/ | Overdrevet, se F3 |
| 6 | anthropic 2.6.0 | Nyeste, lastet opp 2026-11-05. Krever Python >=3.10. **Avhenger av `httpx2>=2.0.0,<3`**, ikke av `httpx` | https://pypi.org/pypi/anthropic/json, CHANGELOG 1.0.0 | OK (men se F1) |
| 7 | Modell `claude-haiku-5-5`, 0,10/0,50 USD per MTok | Gyldig Claude API-ID, «Active (latest)», lansert 2026-10-07, pensjoneres tidligst 2027-10-07. Prisen gjelder prompter opp til 100 000 tokens (over det 0,50/2,50). **Adaptiv tenkning er på som standard, standard effort er `medium`. `temperature`/`top_p`/`top_k` skal utelates** | https://platform.claude.com/docs/en/models/haiku-5-5/overview | OK, se F2 |
| 8 | httpx 0.28.1 | Nyeste httpx, men utgitt 2024-12-06 (snart to år). Klassifisert bare opp til Python 3.12. Pydantic viderefører prosjektet som `httpx2` (2.16.0, 2026-10-21) på grunn av «limited activity» i httpx | https://pypi.org/pypi/httpx/json, https://pypi.org/pypi/httpx2/json | Utdatert valg, se F1 |
| 9 | python-dotenv 1.2.4 | Nyeste, 2026-10-01, støtter 3.14 | https://pypi.org/pypi/python-dotenv/json | OK |
| 10 | Leaflet 1.9.4 er nyeste stabile | npm `dist-tags.latest` = 1.9.4 (2023-05-18). `beta` = 2.0.0-beta.2 (2026-11-06) | https://registry.npmjs.org/leaflet | OK, se F8 |
| 11 | Kartverket topo WMTS, uten nøkkel, CC BY 4.0, zoom 0–18 | Flis z10/297/542 (Oslo) og z18 gir 200 `image/png`, uten nøkkel og med CORS `*`. z19 gir 400. GetCapabilities: `.../topo/default/{TileMatrixSet}/{TileMatrix}/{TileRow}/{TileCol}.png`, så rekkefølgen `{z}/{y}/{x}` er riktig. «Fees: Ingen», «AccessConstraints: Ingen». Vilkårene: CC BY 4.0, kreditering «©Kartverket» | https://cache.kartverket.no/v1/wmts/1.0.0/WMTSCapabilities.xml, https://proxy.kartverket.no/en/api-and-data/terms-of-use | OK |
| 12 | MET Locationforecast 2.0-vilkår | Identifiserende User-Agent med kontakt (falske eller tilfeldige strenger forbudt). Aldri gjenta kall før `Expires`. `If-Modified-Since` lik forrige `Last-Modified`. «truncate all coordinates to max 4 decimals». Under 20 forespørsler/s totalt. 2.0 er gjeldende versjon, uten varslet slutt. Live-kall: 200 med `Expires` og `Last-Modified` | https://api.met.no/doc/TermsOfService, https://api.met.no/weatherapi/locationforecast/2.0/documentation | OK, se F6 |
| 13 | Høyde-API, maks 50 punkter per kall | OpenAPI: «Flere punkter (maks 50)». Live-test: 2 punkter gir 200 (`datakilde: dtm1`), 51 punkter gir **422**. Ingen innlogging | https://ws.geonorge.no/hoydedata/v1/openapi.json | OK |
| 14 | pyproj 3.8.0 med Windows-hjul for 3.14 | Nyeste, 2026-09-05. `cp314-cp314-win_amd64.whl` finnes (også for cp315) | https://pypi.org/pypi/pyproj/json | OK |
| 15 | Ruff 0.17.4 | Nyeste, 2026-11-05, `py3-none-win_amd64` | https://pypi.org/pypi/ruff/json | OK |
| 16 | SQLite som følger med Python 3.14 holder for Django 6.1 | Django 6.1 krever minst SQLite 3.37.0. Lokal Python 3.14.7 (Windows) har SQLite **3.50.4** | https://docs.djangoproject.com/en/6.1/releases/6.1/ | OK, se F7 |
| 17 | Python 3.14 | 3.14 er i bugfix-fase (siste 3.14.10, 2026-10-25). **3.15 ble utgitt 2026-10-09** (nå 3.15.2) og er det python.org tilbyr som standard | https://www.python.org/downloads/ | OK, se F7 |
| 18 | Betalte API-kall brukes ikke til trening (NFR-5-begrunnelsen) | Anthropic Privacy Center: API-input og -output brukes ikke til trening som standard | https://privacy.claude.com/en/articles/7996868-is-my-data-used-for-model-training | OK |
| 19 | Startkreditt på ca. 5 USD (merket som antakelse i memloggen) | Fortsatt bare tredjepartskilder. Ingen offisiell Anthropic-side funnet | f.eks. https://aireiter.com/blog/claude-api-free-credits-every-way | Uverifisert (riktig merket) |

## Findings

### F1 — medium — `httpx` 0.28.1 er riktig nummer, men feil pakke

Spinen (Stack og memlogg (f)) fester `httpx==0.28.1` for MET-proxyen og byggeskriptet. Tallet er det nyeste for `httpx`, men pakken er i praksis erstattet:

- `anthropic` 2.6.0 avhenger av `httpx2>=2.0.0,<3`, ikke av `httpx` (endret i SDK 1.0.0: «upgrade to httpx2»). SDK-en sjekker også spesifikt og gir feil hvis den får et `httpx`-objekt der den venter `httpx2`.
- Følgen er at `requirements.txt` får to nesten like HTTP-biblioteker med ulike unntaksklasser (`httpx.TimeoutException` og `httpx2.TimeoutException`). Det er lett for en KI-agent å blande dem. En `except` i `tjenester/` kan da treffe feil klasse, og testverktøy som mocker `httpx` dekker ikke SDK-en.
- `httpx` har ikke hatt en utgivelse siden 2024-12-06 og er bare klassifisert opp til Python 3.12. Pydantic viderefører prosjektet som `httpx2` nettopp på grunn av «limited activity».

Memloggen sjekket versjonsnummeret (2026-11-08), men ikke om pakken passer med SDK-en.
*Fix:* Bytt `httpx 0.28.1` med `httpx2` i Stack og i memlogg (f), festet til den versjonen pip velger sammen med `anthropic==2.6.0` (nyeste er 2.16.0). Skriv `import httpx2` i MET-proxyen og byggeskriptet. Den er allerede installert som avhengighet av SDK-en, så det blir én HTTP-pakke færre. Et alternativ er `urllib.request` fra standardbiblioteket for de to enkle GET-kallene.
Kilder: https://pypi.org/pypi/anthropic/json · https://pypi.org/pypi/httpx2/json · https://github.com/anthropics/anthropic-sdk-python/blob/main/CHANGELOG.md (1.0.0)

### F2 — medium — Standardoppsettet for KI-modellen og SDK-en passer ikke med 5-sekundersgrensen i AD-10

AD-10 punkt 4 krever svar innen 5 s, ellers brukes reserven. Spinen sier ikke hvordan kallet konfigureres, og standardverdiene trekker i motsatt retning:

- Claude Haiku 5.5 har **adaptiv tenkning på som standard, med effort `medium`**. Tenketokens kommer før svaret og gir lengre ventetid. Med standardoppsettet vil en del kall bruke mer enn 5 s og falle til reserve. SM-3 og FR-12 blir da sjeldnere oppfylt enn planlagt.
- SDK-en har `DEFAULT_TIMEOUT = 10 min` og `DEFAULT_MAX_RETRIES = 2`. Et tidsavbrudd prøves på nytt, så et naivt `Anthropic(timeout=5)` kan blokkere viewet i opptil ca. 15 s.
- Modellen gir 400-feil på `temperature`, `top_p` og `top_k` som ikke er standard, og på prefill. KI-agenter legger ofte til `temperature=0` «for determinisme».

Memloggen sjekket modell-ID og pris, men ikke disse standardverdiene.
*Fix:* Legg en linje i AD-10 eller Stack: klienten lages med `timeout=5.0, max_retries=0`. Kallet sender `output_config={"effort": "low"}` (eller slår av tenkning, som Haiku 5.5 tillater ved effort `high` eller lavere). Ingen sampling-parametere og ingen prefill. Bruk `max_tokens` som passer til ≤300 tegn. Tidsgrensen gjelder hele kallet, inkludert nye forsøk.
Kilder: https://platform.claude.com/docs/en/models/haiku-5-5/overview · https://raw.githubusercontent.com/anthropics/anthropic-sdk-python/main/src/anthropic/_constants.py

### F3 — low — «Django anbefaler egen brukermodell» står ikke i dagens dokumentasjon, og basisklassen er ikke valgt

Memlogg (a) begrunner AD-7 med at «Django anbefaler egen modell før første migrering». I dokumentasjonen for 6.1 (og 5.2) står det «If you're starting a new project, you **can** set up a custom user model …». Den sterke anbefalingen er borte, men advarselen om at det er vanskelig å bytte `AUTH_USER_MODEL` senere står fortsatt. Valget er riktig, fordi e-post som innloggingsfelt krever egen modell, men begrunnelsen er hentet fra eldre dokumentasjon.

Spinen sier heller ikke *hvordan* modellen skal se ut. Dokumentasjonens eksempel med e-post bruker `AbstractBaseUser`. Det krever egen `BaseUserManager` og egne `UserCreationForm`/`UserChangeForm`, og admin kan ikke bruke `UserAdmin` direkte. Med `AbstractUser`, `username = None` og `USERNAME_FIELD = "email"` følger mer med ferdig. To stories vil velge ulikt.
*Fix:* Endre begrunnelsen til «Django-dokumentasjonen advarer om at det er vanskelig å bytte brukermodell etter første migrering, og e-post som innloggingsfelt krever egen modell». Legg til i AD-7: `class Bruker(AbstractUser)` med `username = None`, `email = EmailField(unique=True)`, `USERNAME_FIELD = "email"`, `REQUIRED_FIELDS = []`, egen manager og `AUTH_USER_MODEL` satt i den første migreringen (`0001_initial`).
Kilde: https://docs.djangoproject.com/en/6.1/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project

### F4 — low — `login()` stemmer, men spinen sier ikke hva `logout()` gjør med søkeøkten

Kildekoden i Django 6.1.3 bekrefter at `login()` beholder gjestens data (`cycle_key()`). Men `logout()` tømmer *hele* økten, og innlogging som en annen bruker i samme nettleser gjør det samme (`flush()`). Det betyr at «Logg ut» og kontosletting (som logger ut, jf. PRD-reisen) også fjerner det gjeldende turforslaget og listen over viste turer. Dette passer med PRD-reisen ved kontosletting, men bør stå i AD-5 så ingen story prøver å «redde» økten over utlogging.
*Fix:* Legg til i AD-5: «Utlogging tømmer økten, også søk og forslag (Djangos `logout()`).»
Kilde: https://docs.djangoproject.com/en/6.1/topics/auth/default/ · `django/contrib/auth/__init__.py` (tag 6.1.3)

### F5 — info (dekket av review-rubric) — Standardverdiene for session gjør økten per nettleser og to uker lang

Webverifiseringen bekrefter grunnlaget for high-funnet om AD-5/AD-6 i `review-rubric.md`: `SESSION_EXPIRE_AT_BROWSER_CLOSE=False` og samme cookie på 1 209 600 s gjør at søkeøkten overlever at fanen lukkes. I tillegg deles økten av alle faner i samme nettleser. Et nytt søk i én fane erstatter derfor forslaget i en annen fane (PRD-reisen nevner søk «i andre faner»). Ingen ny fix utover den i review-rubric. Valget bør bare nevne begge effektene.
Kilde: https://docs.djangoproject.com/en/6.1/ref/settings/

### F6 — low — MET: detaljer som ikke er tatt med

Vilkårene er riktig gjengitt i AD-9. Avrunding til 4 desimaler oppfyller «max 4 decimals» like godt som avkutting. Tre ting mangler:

- `altitude` anbefales for presise temperaturer, ellers brukes en grov terrengmodell. Startpunktets høyde finnes allerede fra byggeskriptet (høyde-API-et), så den kan sendes med. Det påvirker bekledningstipsene.
- Varselet går **9 dager** frem. Søk med dato lenger frem gir ingen værdata. Det bør gå inn i FR-10-stien, ikke som en feil.
- User-Agent må identifisere appen og ha kontakt (e-post eller nettside), og falske eller generiske strenger er forbudt. `.env.example` bør derfor ha en ferdig verdi som virker for sensor uten endring, f.eks. `YourNextAdventure/1.0 (+<repo-URL>)`, og ingen personlig e-post.

*Fix:* Legg til de tre punktene i AD-9 / `.env.example`.
Kilder: https://api.met.no/weatherapi/locationforecast/2.0/documentation · https://api.met.no/doc/TermsOfService

### F7 — low — Python-versjon: 3.15 er ute, og kravet til SQLite er ikke skrevet ned

- Python 3.15 kom 2026-10-09, og python.org tilbyr nå 3.15.2 som standard. Sensor kan derfor installere 3.15. Alle festede pakker virker på 3.15 (Django 6.1.3 støtter 3.15, og pyproj, pydantic-core og jiter har `cp315-win_amd64`-hjul), så det er ingen blokkering. Men «Python 3.14» uten område kan få sensor til å tro at 3.15 ikke er støttet. Lokalt er 3.14.7 installert, mens siste 3.14 er 3.14.10.
- Django 6.1 krever SQLite ≥ 3.37.0. Windows-Python 3.14.7 har 3.50.4, så alt er i orden. På Linux bruker Python fra distribusjonen systemets SQLite, som kan være eldre.

*Fix:* I Stack/README: «Python 3.12–3.15 (utviklet og testet på 3.14.x); SQLite ≥ 3.37 (følger med python.org-installasjonen)». Et alternativ er `requires-python = ">=3.12"` i `pyproject.toml`.
Kilder: https://www.python.org/downloads/ · https://docs.djangoproject.com/en/6.1/releases/6.1/

### F8 — info — Kartverket og Leaflet

- Kartverket: URL, nøkkelfrihet, zoom 0–18 og kreditering «©Kartverket» er bekreftet live. Varselet fra mai 2025 som memloggen nevner, er markert som **tilbaketrukket** i Geonorge-registeret, og det finnes ingen nye varsler. Vilkårene sier at data på zoom 12–20 kommer fra Geovekst, og at «kopiering eller annen bruk» krever egen tillatelse. Visning av flisene i en webapp regnes ikke som kopiering, men lagre eller bufre ikke flisene lokalt. Høyde-API-et varsler større endringer minst 3 måneder i forveien på Geonorge-Tjenestevarsler.
- Leaflet: 2.0.0-beta.2 kom 2026-11-06. Behold 1.9.4 vendret, og ikke oppgrader til 2.0 i prosjektperioden (2.0 har et annet API).

Kilder: https://register.geonorge.no/varsler/navn/ff1e976f-0d4f-4578-bb9b-9603e1514e8c · https://proxy.kartverket.no/en/api-and-data/terms-of-use · https://registry.npmjs.org/leaflet

### F9 — info — Startkreditten er fortsatt bare bekreftet av tredjepart

Memloggen merker dette riktig som antakelse, og Deferred har en plan B. Det finnes fortsatt ingen offisiell Anthropic-side om kreditten. Kildene nevner telefonverifisering og mulig utløpstid. Ingen endring er nødvendig, men sjekk i Console før KI-storyen starter.

## Hva memloggen faktisk dokumenterer som sjekket

| Valg | Sjekket ifølge memloggen? |
| --- | --- |
| Django-versjon, Python-støtte og støtteperiode | Ja (2026-11-07) |
| PyPI-versjoner (anthropic, httpx, dotenv, ruff, pyproj, Django) | Ja (2026-11-08), men bare versjonsnummeret, ikke avhengighetene (F1) |
| Modell-ID og pris | Ja (2026-11-07), men ikke standardverdiene for tenkning og effort (F2) |
| Kartverket WMTS og Leaflet | Ja (2026-11-07) |
| MET-vilkår, høyde-API maks 50 | Hentet fra PRD (v0.6: «MET-vilkår og Kartverkets API-er er verifisert»), ikke sjekket på nytt i arkitekturen. Nå bekreftet live |
| `SESSION_COOKIE_AGE`, `login()`, egen brukermodell, SQLite-minimum | Ikke sjekket, bare påstått. Nå bekreftet, med nyanser (F3, F4, F5, F7) |
