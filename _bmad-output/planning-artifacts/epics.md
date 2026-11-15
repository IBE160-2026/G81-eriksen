---
status: draft
stepsCompleted: [step-01-validate-prerequisites, step-02-design-epics]
inputDocuments:
  - _bmad-output/planning-artifacts/prds/prd-G81-eriksen-2026-10-29/prd.md
  - _bmad-output/planning-artifacts/prds/prd-G81-eriksen-2026-10-29/addendum.md
  - _bmad-output/planning-artifacts/prds/prd-G81-eriksen-2026-10-29/research-gradering.md
  - _bmad-output/planning-artifacts/prds/prd-G81-eriksen-2026-10-29/extract-sensorveiledning.md
  - _bmad-output/planning-artifacts/architecture/architecture-G81-eriksen-2026-11-07/ARCHITECTURE-SPINE.md
  - _bmad-output/planning-artifacts/ux-designs/ux-G81-eriksen-2026-11-06/DESIGN.md
  - _bmad-output/planning-artifacts/ux-designs/ux-G81-eriksen-2026-11-06/EXPERIENCE.md
---

# Your Next Adventure – epics og stories

## Oversikt

Dette dokumentet deler kravene i PRD-en, UX-spesifikasjonen (`DESIGN.md` og `EXPERIENCE.md`) og arkitekturen (`ARCHITECTURE-SPINE.md`) inn i epics og stories som kan implementeres.

ID-ene for krav er de samme som i kildene: FR og NFR fra PRD-en, AD fra spinen. Nye ID-er her er AR (tilleggskrav fra arkitektur og andre kilder) og UX-DR (krav fra UX-spesifikasjonen). Ved motstrid gjelder kildene, ikke dette dokumentet.

## Kravoversikt

### Funksjonelle krav

FR-1: Turdatabasen har 15–30 kuraterte turer i Oslo og Bærum. Tur 1–15 er P1 og oppfyller sammensetningen, og tur 16–30 er P2. Hver tur har alle feltene i PRD §3 (Tur), med kilde og lisens. Rutelinjene kommer fra Turrutebasen. OSM brukes bare som supplement, i ett engangsuttrekk med færre enn 100 objekter. Høydemeter, nedstigning og høydeprofil beregnes fra Kartverkets høydedata med støyfiltrering, og minst tre turer kontrolleres mot en publisert høydeprofil. Sammensetning: flertallet er grønne eller blå, minst én svart tur, minst tre toppturer og minst fem utsiktsturer, hver turtype har minst én grønn tur under 2 timer der terrenget tillater det, og hvert startpunkt har minst to turer. Hver rutelinje er kontrollert manuelt for sammenheng og riktig startpunkt.

FR-2: Turnivået settes etter Merkehåndboka: grønn under 5 km og under 300 hm, blå under 10 km og under 600 hm, rød under 20 km og under 1000 hm, svart over grensen for rød. Den strengeste av fargene for lengde og høydemeter gjelder, og en verdi akkurat på grensen graderes opp. Tur-retur graderes etter én vei, rundtur etter hele runden. Terreng, eksponering og føre tas ikke med.

FR-3: Estimert tid for hele turen beregnes med sveitsisk regel (15 min per km + 15 min per 100 hm + 15 min per 200 m nedstigning), med 15 % påslag for nybegynnere, avrundet til nærmeste 5 minutter. For tur-retur regnes begge veier: høydemeterne tilbake er lik nedstigningen ut, og omvendt. Regneeksempelet (3 km, 150 hm, 0 m ned, tur-retur) gir 142,3 min, som vises som «ca. 2 t 20 min». Tiden vises alltid med «pauser ikke inkludert». KI beregner aldri tid eller nivå.

FR-4: Søkeskjemaet har Varighet (påkrevd, 1–8 t i halvtimessteg), Dato (påkrevd, i dag som standard, fra i dag til 30 dager frem), Startpunkt (valgfritt, liste over startpunktene i turdatabasen, med fast hjelpetekst om at turene foreløpig bare dekker Oslo-området), Turtype (valgfritt, «Alle turtyper» forvalgt) og Fritekstønske (valgfritt, maks 200 tegn, P2 med FR-11). Alle felt har synlige etiketter. Ugyldige felt gir feilmelding ved feltet, og søket sendes ikke. Valideringen skjer også på serveren.

FR-5: Utvalget filtrerer på estimert tid ≤ varighet, turnivå ≤ nivåtaket og valgt turtype og startpunkt. Rangeringen går i denne rekkefølgen: (1) ikke gåtte turer før gåtte, og gåtte med fornøydhet 1–2 sist, (2) turer som passer fritekstønsket (P2), (3) nivåheving: i første søk etter en heving kommer turer på det nye nivåtaket først, (4) foretrukne turtyper (P2), (5) estimert tid nærmest varigheten, (6) tur-ID. Gåtte turer utelukkes aldri helt. «Nytt forslag» går nedover i rangeringen.

FR-6: Turforslaget viser rutelinjen på kart, turillustrasjon (P2), turnivå med farge og tekst og en fast nivåforklaring, treff på valgt turtype, form (tur-retur eller rundtur), «Start: {startpunkt}», total lengde, estimert tid med «pauser ikke inkludert», bekledningstips (P2), begrunnelse med KI-merke og forklaringspanel, ut.no-lenke hvis turen har en, kreditering og «Kartet i tekst» (minst startpunkt, form, total lengde, høydemeter og laveste og høyeste punkt). Turillustrasjonen og «Kartet i tekst» lages av systemet fra turdata, aldri av KI.

FR-7: «Nytt forslag» gir neste tur i rangeringen, aldri en tur som alt er vist i samme økt. Når alle treff er vist, vises en melding med endringsforslag og valget «Start fra første forslag igjen». Ny innlasting beholder forslaget og listen over viste turer. Det finnes ingen delbar lenke. Å åpne en tur fra historikken endrer ikke økten.

FR-8: Passer ingen topptur varigheten, vises en utsiktstur og en melding om at toppturer krever mer tid (passer heller ingen utsiktstur, gjelder ingen treff). Passer bare turer over nivåtaket, vises en melding og ingen tur, med egne budskap for gjest, bruker uten historikk og bruker med historikk. Meldingene lover ikke lengre eller hardere turer (SM-C1). Ingen treff i det hele tatt gir konkrete endringsforslag: lengre varighet, annet startpunkt eller annen turtype.

FR-9 (P2): Bekledningstips lages med faste regler fra MET-varselet for startpunktet kl. 10–16 på valgt dato, for turforslag fra historikken for i dag. Nedbør ≥ 0,5 mm: «Fare for nedbør – husk regntøy». Laveste temperatur under 5 °C: «Kaldt – ta med lue, votter og et varmt mellomlag». Laveste temperatur 5–15 °C: «Ta med et ekstra lag». Høyeste temperatur over 20 °C: «Varmt – ta med drikke og solbeskyttelse». Vind ≥ 8 m/s: «Mye vind – ta med vindtett jakke». Alltid: «Gode sko og litt mat og drikke». Flere tips kan vises samtidig.

FR-10 (P2): Har MET ikke varsel for datoen (mer enn ca. 9–10 dager frem), eller svarer ikke, vises turforslaget uten bekledningstips og med en melding om hvorfor.

FR-11 (P2): KI tolker fritekstønsket og får bare ønsket og de filtrerte turene. KI svarer med ID-ene til turene som passer, og svaret brukes som punkt 2 i rangeringen. Ønsket er data, aldri instruksjoner.

FR-12: Begrunnelsen nevner minst varigheten, og turtypen og fritekstønsket hvis de er oppgitt (reservemalen nevner aldri ønsket). Den er maks 300 tegn slik brukeren ser den. KI skriver den når KI er tilgjengelig, ellers brukes reservemalen. KI bruker plassholderne `{tid}`, `{varighet}`, `{lengde}` og `{nivå}`, og systemet setter inn verdiene. Har en personaliseringsregel påvirket valget, legges en personaliseringssetning til. KI-merket viser «✦ Skrevet med KI» eller «Begrunnelse fra mal». Forklaringspanelet «Slik lager jeg forslaget» er lukket som standard og sier at rute, tid og nivå kommer fra Kartverkets turdata og faste formler, at KI tolker og skriver og kan ta feil, og at tiden kan bomme med rundt 15 %.

FR-13: Et KI-svar forkastes hvis det viser til en tur utenfor treffene, er tomt eller ugyldig, gir en begrunnelse over 300 tegn, har tall eller turnivå utenfor plassholderne eller kommer etter 5 sekunder. Da ignoreres fritekstønsket, og begrunnelsen lages fra reservemalen. Reserveløsningen brukes også uten nøkkel og når grensen for KI-kall er nådd. Forkastede svar logges. Ble et fritekstønske ignorert, vises en melding om det.

FR-14: En gjest kan lage konto med e-post og passord (minst 8 tegn, lagres bare som hash), logge inn og logge ut. En e-post som finnes fra før, gir en melding med forslag om å logge inn. Feil innlogging sier ikke hvilket felt som er feil. En gjest som bruker en kontofunksjon, blir bedt om å logge inn, og turforslaget beholdes. En gjest som har trykket «Registrer gjennomført tur», går etter innlogging rett inn i registreringen av den turen.

FR-15: En bruker kan slette kontoen etter bekreftelse på en egen side. Konto, e-post, passord-hash, historikk og vurderinger slettes permanent. Brukeren logges ut og får en kvittering som gjest. Feiler slettingen, slettes ingenting, og brukeren får en feilmelding med neste steg. Avbryt endrer ingenting.

FR-16: En bruker kan registrere en gjennomført tur fra turforslaget eller historikken med dato (i dag som standard, ikke frem i tid), brukt tid (10 min–24 t), opplevd vanskelighet (*lett / moderat / vanskelig*) og fornøydhet (1–5). Alle felt er påkrevd.

FR-17: En bruker ser historikken med tur, dato og vurdering, og brukt tid ved siden av estimert tid. En tur kan åpnes som turforslag fra historikken, også over nivåtaket, med en merknad om det. Avvik fra vanlig turforslag: «Fra historikken din» i stedet for søkeoppsummeringen, begrunnelse fra fast mal uten KI (for eksempel «Du gikk denne turen 12. oktober og ga den 5 av 5.») med «Begrunnelse fra mal», bekledningstips for i dag, og «Finn en ny tur» i stedet for «Nytt forslag».

FR-17.1 (P2): Historikken kan vise hvor nær brukeren er neste nivåheving etter FR-19 og FR-5.

FR-18: Gjest og bruker uten historikk har grønt nivåtak.

FR-19: Nivåtaket er lik grunnnivået, eller sperrenivået mens en sperre er aktiv. Heving: tre turer med turnivå lik grunnnivået, vurdert *lett* uten aktiv sperre, hever grunnnivået ett nivå. De telles fra siste heving eller siste *vanskelig*. *Moderat* verken teller eller nullstiller, og svart heves ikke. Sperre: *vanskelig* nullstiller telleren og senker nivåtaket til nivået under turens nivå (aldri under grønt), hvis det er lavere. Oppheving: neste *lett* eller *moderat* opphever sperren, men teller ikke mot heving. Turer over nivåtaket foreslås aldri. Hver registrering teller, også gjentakelser. Registreringene behandles i datorekkefølge og deretter registreringsrekkefølge. De 12 eksemplene i PRD-en er testtilfeller.

FR-20 (P2): Turtyper fra gjennomførte turer med fornøydhet 4–5 er foretrukne turtyper og gir høyere rangering.

FR-21: Systemet leveres med en testbruker med oppdiktet historikk som viser nivåheving, sperre og turtypepreferanse. Innloggingsdataene står i README.

### Ikke-funksjonelle krav

NFR-1 Kjørbarhet: Appen installeres og startes lokalt etter README på under 20 minutter, uten ekte nøkler. Kart, vær og turdatabase virker uten nøkler. Turdatabasen og testbrukeren lastes med én kommando. `.env.example` følger med, og hemmeligheter ligger aldri i repoet eller i git-historikken.

NFR-2 Stabilitet: Appen tåler feil input, gjentatte handlinger og dobbel innsending uten å krasje. Alle tilstander viser et turforslag eller en forklaring med neste steg.

NFR-3 Mobil: Siden virker ned til 360 px bredde uten sidelengs rulling (bare kartet og historikktabellen ruller i egen beholder). På mobil synes turnivå, estimert tid og turtype-treff uten rulling. Kartet og bekledningstipsene nås med kort rulling. Knapper er minst 44 × 44 px.

NFR-4 Universell utforming: WCAG 2.1 AA, minst: kontrast 4,5:1, hele kjerneflyten med tastatur, feilmeldinger koblet til feltet og lest opp, kartet holder ikke på fokus, aldri informasjon bare med farge, og reflow ved 320 px. Det verifiseres med et automatisk verktøy og sjekklisten i `EXPERIENCE.md` › Accessibility Floor.

NFR-5 Personvern: Systemet lagrer bare e-post, passord-hash, historikk og vurderinger, og sporer ikke posisjon. KI får ingen personopplysninger, bare søket og turene som kan foreslås. Loggen over forkastede KI-svar har tidspunkt, kalltype, årsak og svaret, aldri fritekst, e-post eller bruker-ID. Lokalt ligger den i en fil som aldri legges i git, og linjer eldre enn 30 dager slettes. På Vercel går den til kjøreloggen, som slettes etter 1 time, så kvalitetssikringen av KI-svar gjøres lokalt. På den publiserte siden lagres dataene i EU. Konto-skjermen viser en kort personverntekst.

NFR-6 Sporbarhet: Kode, tester, stories, commits og PR-er viser til FR- og NFR-ID-ene.

NFR-7 Kreditering: Appen viser «© Kartverket», «© OpenStreetMap contributors» med lenke og «Data fra MET Norge».

NFR-8 Sikkerhet: En bruker ser og endrer bare sin egen historikk og konto. All input valideres på serveren. Fritekst er data, ikke instruksjoner, og KI-svar valideres alltid. Grense for KI-kall: maks 20 per nettleser de siste 60 minuttene og maks 200 totalt per kalenderdøgn. Et kall teller når det sendes. Over grensen brukes reserveløsningen med de vanlige meldingene. Grense for innloggingsforsøk: etter 5 mislykkede innlogginger med samme e-post på 15 minutter avvises nye forsøk med den e-posten resten av perioden, med en melding som ikke sier om e-posten har en konto.

NFR-9 Mørk modus (P2): Siden følger innstillingen for lys eller mørk modus på enheten, uten egen bryter.

NFR-10 Publisering: Appen publiseres på Vercel. Hver endring i `main` publiseres automatisk, og adressen står i README. Den publiserte siden har hele kjerneflyten, også testbrukeren (lages på nytt ved hver publisering) og KI innenfor NFR-8. Hver PR får en forhåndsvisning med egen database. Hemmeligheter ligger bare hos Vercel. Lokal kjøring (NFR-1) er fortsatt et krav.

### Tilleggskrav

**Starter-mal: Arkitekturen har ingen starter-mal.** Prosjektet starter fra null med Django (`startproject` til `config/`) og kildetreet i spinen › Structural Seed. Det må bygges i **Epic 1, Story 1**, sammen med egen brukermodell i første migrering (AR-9). Fordi publisering nå er et krav (NFR-10), bør den første publiseringen på Vercel komme tidlig, så hver PR får en forhåndsvisning fra starten (AR-24).

AR-1 Oppsett (AD-12, Structural Seed): Kildetreet `config/`, `turforslag/`, `domene/`, `tjenester/`, `data/`, `skript/`, `tests/`, `docs/`. `requirements.txt` med låste versjoner fra spinen › Stack (Django 6.1.3, anthropic 2.6.0, python-dotenv 1.2.4). `requirements-bygg.txt` har i tillegg pyproj 3.8.0. Ruff 0.17.4 i `pyproject.toml`. `.env.example` virker uten endring (`DJANGO_SECRET_KEY` med lokal verdi, `DEBUG=True`, tom `ANTHROPIC_API_KEY`, `MET_USER_AGENT` med appnavn og repo-URL). Mangler `.env`, stopper settings med en norsk melding. `LANGUAGE_CODE="nb"`, `TIME_ZONE="Europe/Oslo"`, norske maler for 404, 500 og CSRF-feil. Installasjon: `venv`, `pip install`, kopiere `.env`, `migrate`, `lastinn`, `runserver`. Lokal kjøring virker alltid uten Vercel, Neon eller andre kontoer. Publiseringen står i AR-24.

AR-2 Lagdeling (AD-2, Design Paradigm): `domene/` er ren Python og importerer bare standardbiblioteket. Hver regel er én funksjon uten database, nettverk eller klokke, og dagens dato sendes inn. Views og byggeskript regner, filtrerer og formaterer ikke selv. `tjenester/` importerer bare `domene/`. Hver regel har enhetstester som viser til FR-ID-en.

AR-3 Turdatatype (AD-3 punkt 1): `domene.tur.Tur` er en frossen dataklasse med feltene i spinen (verdier for én vei ved tur-retur, totaler bare fra funksjoner i `domene.tur`) og `til_geojson_feature()` og `fra_geojson_feature()`.

AR-4 Byggeskript (AD-3 punkt 2–3, addendum): `python -m skript.bygg_turdatabase` leser kurateringslista i `data/` (format avgjøres i første story for turdatabasen), henter geometri fra Turrutebasen, høyder fra Kartverkets høyde-API (maks 50 punkter per kall, punkt hvert 10–25 m, terskel 2–10 m eller glatting), gjør om UTM (EPSG:25832/25833) til WGS84 med pyproj, beregner verdier via `domene/` og skriver `data/turer.geojson`, som committes. Høydeprofilen lages fra de samme filtrerte punktene. Turnavnet kommer bare fra kurateringslista. OSM leses fra `data/osm-uttrekk.geojson` (committet, med ODbL-kreditering), og skriptet stopper ved 100 objekter eller flere.

AR-5 Lasting (AD-3 punkt 4, AD-11 punkt 3): `python manage.py lastinn` leser `turer.geojson` og `data/testbruker.*`. Turer oppdateres eller opprettes etter `id` og slettes aldri. `Registrering.tur` har `on_delete=PROTECT`. Mangler en tur som har registreringer, stopper kommandoen med en melding. Testbrukeren slettes og lages på nytt, og `brukt_heving` settes til én mindre enn antall hevinger.

AR-6 Lagring (AD-4, AD-3 punkt 5–6): All tilstand ligger i én database via Django-modeller og migreringer: SQLite (`db.sqlite3`, ikke i git) lokalt og i tester, og Postgres (Neon) når `DATABASE_URL` finnes. Ingen rå SQL og ingen databasespesifikke felt, så de samme migreringene virker på begge. Geometri og høydeprofil ligger i `JSONField`, uten GeoDjango eller SpatiaLite. Appen beregner aldri turnivå, høydemeter eller tid på nytt.

AR-7 Søketilstand (AD-5): Et gyldig søk (POST) lager en tilfeldig søke-ID (`secrets.token_urlsafe`) og sender videre til `/forslag/<sok_id>/`. `Soketilstand` (`domene.okt`) lagres i Django-økten under `"sok"`, og bare `turforslag/okt.py` leser og skriver den. Rangeringen fryses ved søket, og de 10 nyeste søkene beholdes. Ukjent søke-ID eller tur-ID gir «Forslaget finnes ikke lenger». Ingen `flush()`, `cycle_key()` eller `clear()`. Registrering tar tur-ID fra URL-en (`/registrer/<tur_id>/`).

AR-8 Innlogging (AD-6): `SESSION_COOKIE_AGE` er Djangos standard (to uker), uten inaktivitetsgrense. Utlogging er en synlig knapp (POST). Utløpt innlogging sender til Logg inn med `next`.

AR-9 Brukermodell (AD-7): `turforslag.Bruker` arver `AbstractUser` med `username=None`, uten fornavn og etternavn, med `USERNAME_FIELD="email"`, egen manager og feltet `brukt_heving`. Den må finnes i **første migrering**. E-post lagres med små bokstaver. Passordvalidering har bare minimumslengde 8. Data hentes filtrert på `request.user`. Kontosletting: slett bruker og registreringer i én transaksjon, så `logout()`, så kvittering og redirect. Grense for innloggingsforsøk: modellen `Innloggingsforsok(epost, tidspunkt)` og en ren funksjon i `domene/` som avgjør før `authenticate()` (5 forsøk innenfor 15 min, verdiene i `settings`). En vellykket innlogging sletter forsøkene for e-posten.

AR-10 Kart (AD-8): Fliser fra `https://cache.kartverket.no/v1/wmts/1.0.0/topo/default/webmercator/{z}/{y}/{x}.png`, zoom høyst 18, uten nøkkel. Leaflet 1.9.4 ligger i `static/vendor/leaflet/`. `kart.js` får GeoJSON for én tur via `json_script` og tegner den, uten egen logikk. Turillustrasjon og høydeprofil er inline SVG fra serveren. «Kartet i tekst» lages av `domene/`.

AR-11 Vær (AD-9, addendum): Bare `tjenester/met.py` kaller MET Locationforecast 2.0, med koordinater rundet til 4 desimaler og startpunktets høyde som `altitude`. Svarene bufres i en Django-modell med `Expires` og `Last-Modified` per koordinat, og nytt kall går først etter `Expires`, med `If-Modified-Since`. User-Agent fra `MET_USER_AGENT`. Tidsavbrudd 5 s. Tjenesten returnerer `Varsel` eller `IngenVarsel(FOR_LANGT_FREM | UTILGJENGELIG)`. Tipsregelen ligger i `domene/` og bruker timeverdiene kl. 10–16 Europe/Oslo.

AR-12 KI (AD-10, addendum): Grensesnitt i `tjenester/ki/` med variantene ekte (Anthropic, `claude-haiku-5-5`), reserve og falsk. Reserve brukes uten nøkkel. Kall A (tolking) skjer én gang per søk, bare med fritekst og nøkkel, før rangeringen. Kall B (begrunnelse) skjer én gang per vist tur når nøkkel finnes, og lagres i søketilstanden. Turforslag fra historikken kaller aldri KI. KI får bare søket og treffene (id, navn, turtyper, form). Prompten ligger i en fil i git, og friteksten er avgrenset data. Klienten har `timeout=5.0`, `max_retries=0`, lav effort, ingen sampling-parametere og ingen prefill. Validering i `domene/` følger addendumet: plassholdere, sifre, tallord og nivåord, så innsetting, så personaliseringssetning, så grensen på 300 tegn. Loggen `logs/ki.log` roteres ved midnatt, og filer eldre enn 30 dager slettes ved oppstart og rotasjon. På Vercel går de samme linjene til standard ut. Grensen er 20 kall per nettleser per 60 min (`"ki_kall"` i økten) og 200 per døgn (`KiForbruk` med unik `dato`, `get_or_create` og `F("antall") + 1` i én transaksjon). Avgjørelsen er en ren funksjon i `domene/`, grensene ligger i `settings`, og første gang totalgrensen nås, logges én linje.

AR-13 Nivå (AD-11): `domene.niva.vurder_historikk(registreringer) → NivaStatus` er eneste kilde til nivåtak, sperre, antall hevinger, fremgang og foretrukne turtyper. Nivåheving i rangeringen avgjøres bare ved et gyldig søk (`antall_hevinger > brukt_heving`). Gjester har alltid `False`. En opphevet sperre er ingen heving. Hevingen regnes som brukt selv om søket ikke gir treff. `velg_turer` returnerer `Utvalg(status, rangerte_tur_ider)` med statusene `TREFF`, `TOPPTUR_ERSTATTET`, `BARE_OVER_NIVATAK` og `INGEN_TREFF`.

AR-14 Engangstoken (AD-14): Skjemaet for registrering har et engangstoken i økten. En POST med brukt eller ukjent token lagrer ingenting og sender til historikken. Dette dekkes av en test.

AR-15 Tester og kodestil (AD-13): Testene kjøres med `python manage.py test` og ligger i `tests/` (`domene/`, `tjenester/`, `web/`, `fixtures/`). Domenetester bruker ikke databasen. KI byttes med den falske varianten og MET med lagrede svar. Ingen test gjør nettverkskall. Ruff er linter og formatter. Logging bruker `logging` med én logger per modul.

AR-16 Konvensjoner (spinen › Consistency Conventions): Domeneord på norsk uten æ/ø/å i identifikatorer. All brukertekst kommer fra `EXPERIENCE.md` › Mikrotekst. Formatering («ca. 1 t 35 min», «3,5 km», «grønn») skjer bare i `domene/`. Meter og hele minutter i data. Django-skjemaer validerer alt, alle POST følger Post/Redirect/Get, og CSRF er på. `tjenester/` kaster aldri videre til view. Miljøverdier leses bare i `config/settings.py`. Én felles krediteringslinje i basismalen, og Leaflets egen attribution-prefiks er slått av. Nettleserstøtte: de to nyeste versjonene av Chrome, Edge, Firefox og Safari, også på mobil, uten polyfills.

AR-17 Content-Security-Policy (spinen › Consistency Conventions): Djangos innebygde CSP med `default-src 'self'`, `img-src 'self' https://cache.kartverket.no`, `object-src 'none'`, `base-uri 'self'`, `form-action 'self'` og `frame-ancestors 'none'`. Ingen inline-skript og ingen `style`-attributter i maler. Trenger Leaflet mer, utvides policyen i kartstoryen med en begrunnelse.

AR-18 JavaScript (AD-1): Nøyaktig to egne JS-filer uten rammeverk eller byggesteg. `kart.js` tegner kartet. `forbedring.js` gjør bare dette: «Nytt forslag» uten sideinnlasting (HTML-fragment fra serveren, `document.title`, fokus, `aria-busy`), lasteindikator, sperre mot dobbeltklikk, tegnteller og «Vis passord». Alle sider og skjemaer virker fullt uten JavaScript. Serveren svarer med HTML, aldri JSON, til egne sider.

AR-19 Gradering (`research-gradering.md`): Grensene skrives med «<», en verdi akkurat på grensen graderes opp, og svart betyr ≥ 20 km eller ≥ 1000 hm.

AR-20 Repo og README (sensorveiledningen, AD-12 punkt 6): `.gitignore` dekker `node_modules`, `venv`, build, `.env`, `db.sqlite3`, `logs/`, `staticfiles/` og `.vercel/`. Ingen løse filer i rotmappen. README har adressen til den publiserte siden, hva appen gjør og for hvem (gjerne med skjermbilde), krav med versjoner (Python 3.12–3.15, testet på 3.14), kommandoer som kan kopieres, miljøvariabler og `.env.example`, testbrukerens innlogging, hvordan testene kjøres, mappeoversikt, hvordan KI-nøkkelen legges inn og lenker til PRD, UX og arkitektur. README testes i et rent miljø før innlevering.

AR-21 Kvalitetssikring (PRD §8, sensorveiledningen): SM-1 er en manuell brukertest med 3–5 nybegynnere, dokumentert i repoet. SM-2 er automatiske tester for FR-2, FR-3 (med regneeksempelet), FR-4, FR-5, FR-7, FR-8, FR-13 med KI mocket (også når grensen er nådd) og FR-18 til FR-20 (med de 12 eksemplene i FR-19). SM-3: kjerneflyten virker uten KI-nøkkel. SM-4 er en manuell test av mobil og UU etter Accessibility Floor, og personaliseringen vises med testbrukeren. SM-C1: ingen bruker får foreslått en tur over nivåtaket (testes i SM-2). Manuelle testplaner der automatiske tester ikke passer, og spor av kodegjennomgang i PR-er.

AR-22 Prioritering (PRD §7.1): P1 er FR-1 til FR-8 (FR-1 med 15 turer, FR-6 uten turillustrasjon), FR-12, FR-13, FR-14 til FR-19 (uten FR-17.1), FR-21, NFR-1 til NFR-8 og NFR-10. P2 kuttes i denne rekkefølgen: (1) FR-17.1, (2) NFR-9, (3) turillustrasjonen i FR-6, (4) FR-11, (5) FR-9 og FR-10, (6) FR-20. Tur 16–30 er også P2. Følgene av hvert kutt står i PRD §7.1, og hvert kutt føres i PRD §9 og i endringsloggen.

AR-23 Utenfor v1 (PRD §7.2, spinen › Deferred): eget domene, e-post, glemt passord, sletting og redigering av enkeltregistreringer, personlig tidsestimat, startpunkt valgt i kart og turer utenfor Oslo og Bærum. Det lages ingen stories for disse.

AR-24 Publisering på Vercel (AD-15, NFR-10): Ett Vercel-prosjekt (Hobby) eid av Hannah, med Djangos framework preset. `.python-version` er `3.14`, og `requirements.txt` har `psycopg[binary]` 3.3.9. `vercel.json` setter region `fra1`. Neon kobles til fra Vercel Marketplace i Frankfurt, med egen gren per forhåndsvisning. Appen bruker `DATABASE_URL` med `DISABLE_SERVER_SIDE_CURSORS = True`, og byggingen (`CI` er satt) bruker `DATABASE_URL_UNPOOLED`. Byggesteget i `pyproject.toml` (`[tool.vercel.scripts] build`) kjører `migrate --noinput` og `lastinn`. `STATIC_ROOT = staticfiles/`, og Vercel kjører `collectstatic`. Når `VERCEL` er satt: `DEBUG = False`, oppstartsvakt mot manglende eller utviklingsverdi av `DJANGO_SECRET_KEY`, `ALLOWED_HOSTS = [".vercel.app"]`, `CSRF_TRUSTED_ORIGINS = ["https://*.vercel.app"]`, `SECURE_PROXY_SSL_HEADER` og sikre cookies, og `check --deploy` dekkes av en test. Miljøvariabler hos Vercel: `DJANGO_SECRET_KEY` og `MET_USER_AGENT` overalt, `ANTHROPIC_API_KEY` bare i produksjon. Adressen står i README. Kontoene hos Vercel og Neon opprettes og kobles til av Hannah i nettleseren.

### UX-krav

UX-DR1 Designtokens: Alle tokens fra `DESIGN.md` (frontmatter) blir CSS-variabler: farger med `-dark`-par, kartlag-tokens uten `-dark`-par, typografiroller (systemfonter, serif på overskrifter og sans-serif på resten, ingen webfont), spacing-skala på 4 px, `rounded` og layoutverdier (`page-margin`, `breakpoint-stack` 720 px, `touch-target-min` 44 px og maksbreddene).

UX-DR2 Basismal og landemerker: `<html lang="nb">`, `header` med `nav`, én `main` per visning, sidetittel « – Your Next Adventure», felles kreditering. Flytende oppsett uten faste høyder (`min-height` og padding). Reflow ved 320 px, tekstavstand etter WCAG 1.4.12 og 200 % tekstzoom. Display og Stor overskrift skaleres til 28 px under 720 px.

UX-DR3 Toppmeny: Gjest ser logo og «Logg inn». Innlogget ser logo, «Finn tur», «Historikk» og «Konto». `aria-current="page"` på aktivt punkt, med vekt 600 og 2 px understrek. Menypunktene brytes til ny linje, uten hamburgermeny. Logoen fører til Søk.

UX-DR4 Knapper: Primærknapp (fylt `primary`) og Sekundærknapp (kant), 8 px hjørner, minst 44 × 44 px, høyst én primærknapp per visning. Under innsending får knappen `aria-disabled="true"`, beholder fokus og ignorerer nye klikk.

UX-DR5 Fokusring: `outline` på 3 px i `focus-ring` med 2 px avstand ved `:focus-visible` på alt som kan få fokus, aldri fjernet. Kartvarianten har 3 px hvit ytre kant.

UX-DR6 Skjemafelt: Synlig etikett over feltet og hjelpetekst under. Feilmelding rett under feltet og over hjelpeteksten, med «!»-ikon og vekt 600 i `error`. `aria-describedby` peker på feil og så hjelpetekst, og feltet får `aria-invalid="true"`. Fokus går til første felt med feil. Ingen feiloppsummering. Kontrolltypene følger tabellen i `EXPERIENCE.md`: `<select>` for Varighet, Dato (31 dager) og Startpunkt, `<input type="date">` med `max` for registreringsdato, `fieldset` med Timer og Minutter for brukt tid, og `autocomplete` på e-post og passord.

UX-DR7 Turtypekort: Ekte radiogruppe med fire kort (Alle turtyper, Marka, Utsikt, Topptur) med egen liten illustrasjon. Valgt kort har 2 px `primary`-kant, `surface-alt` og «Valgt» (`aria-hidden`). Piltastene flytter valget.

UX-DR8 Valggruppe: Radiogrupper med `fieldset` og `legend` for opplevd vanskelighet og fornøydhet. Valgt segment har `primary`-fyll, vekt 600 og hake. Fornøydhet har forklaringen koblet til gruppen og ankertekst under 1 og 5.

UX-DR9 Fritekstønske med teller (P2, FR-11): `<textarea>` som ikke stopper inntastingen. Telleren viser «{n} / 200 tegn». At grensen er passert, meldes én gang i en `aria-live="polite"`-region. Over 200 tegn gir feil ved innsending.

UX-DR10 Søk-skjermen: `h1` «Hvor lang tid har du?» og ingress. Varighet og Dato side om side, så Turtype, Startpunkt med hjelpetekst og Fritekstønske. Pyntillustrasjon til høyre, skjult under 720 px. Tilstander: første visning, forhåndsutfylt etter «Endre søk», feil i skjemaet, logget ut og konto slettet (melding som får fokus), og «Forslaget finnes ikke lenger».

UX-DR11 Søkeoppsummering: Én linje («Lørdag 7. nov. · 2 t · Utsikt») med lenken «Endre søk» til forhåndsutfylt skjema. Den vises også under lasting. Ved turforslag fra historikken står «Fra historikken din» uten «Endre søk».

UX-DR12 Turforslag-oppsett: To kolonner over 720 px (Stille kart) med kartet til venstre (`position: sticky`) og Infokolonne til høyre (ca. 340–470 px). Kartbeskrivelse står under kartet. Én kolonne under 720 px. DOM-rekkefølgen er den samme på alle bredder: (1) søkeoppsummering, (2) turnavn `h1`, Nivåmerke og Turtype-treff, (3) meldinger, (4) Formmerke, «Start: …», Faktarute og ut.no-lenke, (5) Turillustrasjon, (6) kart med kreditering, (7) KI-merke, Begrunnelse og Forklaringspanel, (8) Bekledningstips, (9) knappene, (10) Kartbeskrivelse. Foldmålet ved 1280 × 800 er turnavn, Turtype-treff, Faktarute, Turillustrasjon og kart uten rulling.

UX-DR13 Kart: «Kartet i tekst»-lenke oppe til venstre, «Vis hele ruten» og zoom + og − oppe til høyre, målestokk nede til venstre og kreditering nede til høyre. Kartkontrollene er 44 px. Rutelinjen er plommelilla (5 px på 9 px hvit kant), og startmarkøren er «S». Kartflaten har `tabindex="0"`, `role="region"` og `aria-label="Kart over {turnavn}"`. Piltastene flytter og + og − zoomer. Rullehjulet ruller siden, og Ctrl/Cmd + rullehjul zoomer. Én finger på berøringsskjerm ruller siden og viser et hint, to fingre flytter kartet. Kartet holder aldri på fokus og fanger aldri siderullingen. Markørene kan ikke få fokus. Norske tekster og ingen reklamelenker. Ingen animasjon ved `prefers-reduced-motion`. Feiler flisene, vises en melding med «Prøv igjen» og lenke til Kartbeskrivelse. På mobil står kartet innenfor sidemargen, med høyde ca. 60 % av skjermen.

UX-DR14 Kreditering: Alltid synlig på kartet på hvit flate, med understrekede lenker til Kartverket, openstreetmap.org/copyright (`lang="en"`) og MET Norge. Den brytes høyrejustert på smal skjerm.

UX-DR15 Kartbeskrivelse: `h2` «Kartet i tekst» med tekst laget fra turdata, for eksempel «Rundtur på 3,5 km totalt fra Granvannet p-plass. Ruten stiger ca. 130 høydemeter, fra 180 til 310 moh.»

UX-DR16 Nivåmerke og nivåforklaring: Rektangulært merke i nivåfargen med tekst («Grønn – lett» osv.) og et lite ikon. I mørk modus får Svart en innvendig kant. Nivåforklaringen står ved siden av i `caption`. Nivåfargene brukes bare til turnivå.

UX-DR17 Infokolonne-elementer: Turtype-treff («{Turtype} – som du ba om») som pille i `accent-soft`, eller merket «Utsikt i stedet for topptur». Formmerke («Rundtur» eller «Tur-retur»). «Start: {startpunkt}». Faktarute med tre ruter (total lengde, høydemeter og estimert tid med «pauser ikke inkludert»), én per rad under ca. 360 px. ut.no-lenken «Se turen på ut.no ↗» har skjult tillegg «(åpnes på ut.no)», og `↗` er `aria-hidden`.

UX-DR18 Turillustrasjon (P2): Inline SVG fra rutelinjen og høydeprofilen med tokenfargene. På turforslaget er den en `figure` med `figcaption` (form og laveste og høyeste punkt), og SVG-en er `aria-hidden`. Stor pyntvariant på Søk (`aria-hidden`, uten bildetekst) og liten variant i Turoppsummering. Kuttes den, faller den bort uten tomrom.

UX-DR19 Begrunnelse, KI-merke og Forklaringspanel: KI-merket står rett over `h2` «Begrunnelse» (som ser ut som en overlinje). `<details>`/`<summary>` med «Slik lager jeg forslaget», lukket som standard, med de tre setningene fra `EXPERIENCE.md`.

UX-DR20 Bekledningstips (P2): `h2` «Bekledningstips for {dag}», grunnlagslinjen «Etter værvarselet for startpunktet kl. 10–16.» og liste med aprikos-prikker. Uten varsel byttes listen ut med en infomelding i to varianter (for langt frem, MET svarer ikke). Kuttes den, faller seksjonen bort uten tomrom.

UX-DR21 Melding: Info, advarsel, feil og suksess med 4 px venstrekant i statusfarge, 20 px ikon og fet tittel. Brødteksten er valgfri. Den står der saken gjelder, aldri som toast. `role="status"` eller `role="alert"` på samme side. En melding som følger en navigering, får fokus i stedet for `h1`.

UX-DR22 Tilstandspanel: Erstatter turinnholdet for ingen treff, nivåtak og alle vist. Overskriften er `h1` i `headline-lg`. Forklaringen står til venstre og endringsforslagene til høyre (stablet under 720 px). «Prøv 3 timer» og «Prøv marka» kjører søket på nytt med én endring. «Velg startpunkt» går til skjemaet med fokus på Startpunkt. «Start fra første forslag igjen» og «Endre søk». Nivåtaket har tre tekstvarianter (gjest med «Lag konto», innlogget uten historikk og bruker med historikk).

UX-DR23 Lasting: Søkeoppsummeringen vises med en gang, `surface-alt`-flate der kartet kommer, «Kart lastes …» og lastetekst. `aria-busy="true"` på visningen og lastemelding i en `aria-live="polite"`-region utenfor. Ingen spinner ved `prefers-reduced-motion`.

UX-DR24 «Nytt forslag» uten sideinnlasting (`forbedring.js`): Det gamle forslaget dempes, knappen beholder fokus, og «Finner et nytt forslag …» leses opp. Så byttes innholdet, `document.title` oppdateres, fokus går til nytt `h1`, og kartet viser ny rute. Uten JavaScript lastes en vanlig side med samme resultat.

UX-DR25 Sidetitler og fokus: `document.title` følger IA-tabellen ved hver visningsendring, også «Nytt forslag» og Tilstandspanel. Fokus flyttes til `h1` (`tabindex="-1"`). Tilbakeknappen virker mellom alle visninger.

UX-DR26 Logg inn / Lag konto: Én rute med to visninger og hver sin primærknapp («Logg inn» og «Lag konto og fortsett»). Hjelpeteksten «Minst 8 tegn» vises alltid, og bryteren «Vis passord» kommer fra `forbedring.js`. Feil innlogging, «e-posten finnes fra før» og for mange innloggingsforsøk (NFR-8) gir feilmelding. Krav om konto viser Turoppsummering, «Logg inn for å registrere», «Turforslaget er tatt vare på.» og «Tilbake til turforslaget». Ruter som krever konto, sender til innlogging og tilbake.

UX-DR27 Registrer gjennomført tur: Egen side (ikke dialog) med Turoppsummering øverst, «Alle fire felt er påkrevd.», feltene med kontrolltyper og hjelpetekster, og knappene «Registrer gjennomført tur» og «Avbryt». Etter lagring går brukeren til Historikk med suksessmelding som får fokus.

UX-DR28 Turoppsummering: Lite kort med liten Turillustrasjon (hvis den ikke er kuttet), turnavn i `headline-sm` og linjen Nivåmerke · form · lengde · estimert tid. Ikke interaktiv.

UX-DR29 Historikk: Midtstilt kolonne på høyst 960 px: `h1`, suksessmelding, fremgangslinje (P2, FR-17.1, varianter underveis og målet nådd), tabell og linjen «Nye søk prioriterer turer du ikke har gått.». Ekte `<table>`, nyeste først, én rad per registrering. Turnavnet er `<th scope="row">` med Nivåmerke under. Handlingskolonnen har skjult overskrift «Handlinger» og skjulte tillegg (for eksempel «– Granåsen rundt, 7. nov.»). Tabellen ruller sidelengs i egen beholder (`role="region"`, `aria-label="Historikk"`, `tabindex="0"`). Formater fra Mikrotekst. Tom historikk viser Tilstandspanel med «Finn tur».

UX-DR30 Konto og Bekreft sletting: Konto viser e-post, `h2` «Personvern» med personverntekst, «Logg ut» (POST) og «Slett konto». Bekreft sletting er en egen side med «Vil du slette kontoen?», forklaringen, «Slett kontoen» (ikke på samme sted som «Slett konto») og «Avbryt» tilbake til Konto. Ingen rød flate og ingen inntasting av e-post. Feiler slettingen, vises en feilmelding med «Prøv igjen».

UX-DR31 Mikrotekst og stemme: All tekst i grensesnittet kommer fra `EXPERIENCE.md` › Mikrotekst, i jeg-form med du-tiltale. Faste formater: «Grønn – lett», «ca. 1 t 35 min», «3,5 km totalt». Bare ✦, ↗ og 🎉, alle `aria-hidden`. Tekster merket [ASSUMPTION] bekreftes i storyen som bruker dem.

UX-DR32 Mørk modus (P2, NFR-9): `-dark`-tokenene brukes via `prefers-color-scheme`, uten bryter. Kartflisene og alt oppå dem forblir lyse.

UX-DR33 Bevegelse: Rolig og kort bevegelse, og alt slås av ved `prefers-reduced-motion`, også i kartet.

UX-DR34 Verifisering av UU: Automatisk verktøy, sjekklisten i Accessibility Floor og manuell test av mobil (SM-4), dokumentert i repoet.

UX-DR35 Kartfarger: `map-route`, `map-marker-start` og `map-focus-ring` måles mot ekte Kartverket topo-fliser (skog, myr, vann og bebyggelse) og justeres om nødvendig (åpent punkt i `EXPERIENCE.md`).

### Dekning av FR

FR-1: Epic 1 – turdatabase med 15 turer (P1). Epic 6 – tur 16–30 (P2)
FR-2: Epic 1 – gradering etter Merkehåndboka
FR-3: Epic 1 – estimert tid med sveitsisk regel og påslag
FR-4: Epic 1 – søkeskjema uten fritekst. Epic 4 – fritekstfeltet (P2, med FR-11)
FR-5: Epic 1 – filter og rangering (punkt 5 og 6). Epic 3 – gåtte turer, nivåheving og preferanse (punkt 1, 3 og 4). Epic 4 – fritekst (punkt 2, P2)
FR-6: Epic 1 – visning med kart, nivå, fakta, «Kartet i tekst», ut.no og kreditering. Epic 5 – bekledningstips (P2). Epic 6 – turillustrasjon (P2)
FR-7: Epic 1 – nytt forslag, økt og «alle forslag er vist»
FR-8: Epic 1 – topptur erstattet, ingen treff og nivåtak for gjest. Epic 3 – nivåtak for innloggede
FR-9: Epic 5 – bekledningstips (P2)
FR-10: Epic 5 – mangler værvarsel (P2)
FR-11: Epic 4 – KI-tolking av fritekstønske (P2)
FR-12: Epic 1 – begrunnelse fra mal, KI-merke og forklaringspanel. Epic 3 – personaliseringssetning. Epic 4 – KI-skrevet begrunnelse
FR-13: Epic 1 – reserve uten nøkkel. Epic 4 – validering, logg og reserve ved feil eller grense
FR-14: Epic 2 – lage konto, logge inn og ut, turforslaget beholdes
FR-15: Epic 2 – slette konto
FR-16: Epic 2 – registrere gjennomført tur
FR-17: Epic 2 – historikk og turforslag fra historikken. Epic 5 – bekledningstips for i dag (P2)
FR-17.1: Epic 6 – fremgang mot neste nivå (P2)
FR-18: Epic 1 – grønt nivåtak for gjest og ny bruker
FR-19: Epic 3 – nivåregler
FR-20: Epic 3 – turtypepreferanse (P2)
FR-21: Epic 3 – testbruker

**NFR:** NFR-1 og NFR-10 i Epic 1 (ferdig README i Epic 6). NFR-2, NFR-3, NFR-4 og NFR-6 i alle epics (manuell UU- og mobiltest i Epic 6). NFR-5 i Epic 2 og 4. NFR-7 i Epic 1 (MET-kreditering i Epic 5). NFR-8 i Epic 2 (innlogging) og Epic 4 (KI). NFR-9 i Epic 6.

## Epic-liste

Rekkefølgen følger PRD §7.1: P1 først, og P2 sist i motsatt rekkefølge av kuttlista, så det som kuttes først, bygges sist. Ingen epic trenger en senere epic for å virke, og hver epic kan publiseres når den er ferdig.

### Epic 1: Ola finner en tur som passer tiden, på nett (P1)

En gjest åpner den publiserte siden, fyller ut søket og får ett turforslag med kart, nivå, tid og begrunnelse fra mal. Gjesten kan be om nytt forslag og får hjelp når ingenting passer. Epicen bygger prosjektet fra null (AR-1), med egen brukermodell i første migrering (AR-9), basismal og designtokens, kart med kreditering og CSP. Publiseringen på Vercel (AR-24) kommer tidlig i epicen, så hver PR får en forhåndsvisning. Byggeskriptet for turdatabasen er den største risikoen og kommer tidlig.

**FR dekket:** FR-1 (15 turer), FR-2, FR-3, FR-4 (uten fritekst), FR-5 (punkt 5 og 6), FR-6 (uten turillustrasjon og bekledningstips), FR-7, FR-8 (gjest), FR-12 (mal, KI-merke, forklaringspanel), FR-13 (reserve uten nøkkel), FR-18
**NFR:** NFR-1, NFR-7, NFR-10

### Epic 2: Ola lager konto og registrerer turene sine (P1)

Gjesten lager konto uten å miste forslaget, registrerer gjennomførte turer med vurdering, ser historikken, åpner en tur fra historikken og kan slette kontoen. Innloggingen har en grense for mislykkede forsøk, og registreringen tåler dobbeltklikk.

**FR dekket:** FR-14, FR-15, FR-16, FR-17
**NFR:** NFR-5 (personverntekst), NFR-8 (grense for innloggingsforsøk)

### Epic 3: Forslagene tilpasser seg nivået til Ola (P1, med P2 sist)

Vurderingene styrer nivåtaket med heving, sperre og oppheving. Søket prioriterer det nye nivået og turer brukeren ikke har gått, og begrunnelsen forklarer regelen. Testbrukeren viser alt dette uten at noen må gå turer. Turtypepreferansen (P2) er siste story.

**FR dekket:** FR-5 (punkt 1, 3 og 4), FR-8 (innloggede), FR-12 (personaliseringssetning), FR-19, FR-21, FR-20 (P2)

### Epic 4: KI skriver begrunnelsen og forstår ønsket (P1, med P2 sist)

Med nøkkel skriver KI begrunnelsen. Svaret valideres alltid, reserven tar over ved feil, og kostnaden har et tak. KI får aldri personopplysninger. Tolking av fritekstønsket (P2) er siste story.

**FR dekket:** FR-12 (KI), FR-13 (validering, logg og reserve), FR-11 og fritekstfeltet i FR-4 (P2)
**NFR:** NFR-5 (prompt og logg), NFR-8 (grense for KI-kall)

### Epic 5: Ola får bekledningstips ut fra været (P2)

Turforslaget viser tips for startpunktet kl. 10–16 på valgt dato, også for turforslag fra historikken (for i dag), og forklarer hvorfor når varselet mangler.

**FR dekket:** FR-9, FR-10, FR-6 og FR-17 (bekledningstips)
**NFR:** NFR-7 (MET-kreditering)

### Epic 6: Rikere turforslag og klar for sensor (P2 og kvalitetssikring)

Turillustrasjon, tur 16–30, mørk modus og fremgang mot neste nivå. Til slutt måling av kartfarger mot ekte fliser, brukertest (SM-1), UU- og mobiltest (SM-4) og README testet i et rent miljø.

**FR dekket:** FR-6 (turillustrasjon), FR-1 (tur 16–30), FR-17.1
**NFR:** NFR-9, NFR-1 (README-test), NFR-3 og NFR-4 (manuell test)

## Epic 1: Ola finner en tur som passer tiden, på nett

En gjest åpner den publiserte siden, fyller ut søket og får ett turforslag med kart, nivå, tid og begrunnelse fra mal. Gjesten kan be om nytt forslag og får hjelp når ingenting passer.

### Story 1.1: Appen starter lokalt etter README

Som sensor,
vil jeg installere og starte appen lokalt bare ved hjelp av README,
slik at jeg kan teste den uten nøkler, Node, Docker eller databaseserver.

**Akseptansekriterier:**

**Gitt** et rent miljø med Python 3.12–3.15
**Når** jeg følger README: `python -m venv`, `pip install -r requirements.txt`, kopierer `.env.example` til `.env`, `python manage.py migrate` og `python manage.py runserver`
**Så** starter appen på `http://127.0.0.1:8000/`, og forsiden viser `h1` «Hvor lang tid har du?»
**Og** ingen steg krever nøkler, Node, Docker eller databaseserver (NFR-1, AR-1)

**Gitt** repoet
**Når** jeg ser på mappene
**Så** finnes `config/`, `turforslag/`, `domene/`, `tjenester/`, `data/`, `skript/`, `tests/` og `docs/` som i spinen › Structural Seed
**Og** en test sjekker at `domene/` bare importerer standardbiblioteket (AR-2)

**Gitt** den første migreringen
**Når** den kjøres
**Så** finnes `turforslag.Bruker` med `username=None`, `USERNAME_FIELD="email"`, uten fornavn og etternavn, med egen manager og feltet `brukt_heving` (standard 0), og `AUTH_USER_MODEL` peker på den (AR-9)
**Og** e-post lagres med små bokstaver, og passordvalideringen har bare minimumslengde 8

**Gitt** at `.env` mangler, eller at `DJANGO_SECRET_KEY` er tom
**Når** jeg starter appen
**Så** stopper den med en norsk melding om å kopiere `.env.example` til `.env` (AD-12 punkt 3)

**Gitt** `.env.example` kopiert uendret
**Når** jeg leser den
**Så** har den `DJANGO_SECRET_KEY` med en lokal utviklingsverdi, `DEBUG=True`, tom `ANTHROPIC_API_KEY` og `MET_USER_AGENT` med appnavn og repo-URL, uten personlig e-post
**Og** `requirements.txt` har låste versjoner fra spinen › Stack, og `requirements-bygg.txt` har i tillegg `pyproj` 3.8.0

**Gitt** at appen kjører
**Når** jeg åpner en adresse som ikke finnes, sender et skjema med ugyldig CSRF-token eller serveren feiler
**Så** vises norske feilsider (404, CSRF og 500) med lenke til Søk
**Og** `LANGUAGE_CODE` er `"nb"` og `TIME_ZONE` er `"Europe/Oslo"` (AD-12 punkt 5)

**Gitt** at appen kjører
**Når** jeg ser på svarhodene for en side
**Så** har den Content-Security-Policy etter konvensjonen i spinen (AR-17)

**Gitt** repoet
**Når** jeg kjører `python manage.py test`, `ruff check .` og `ruff format --check .`
**Så** består alle, uten nettverkskall (AR-15)
**Og** README › Installasjon og kjøring har kommandoene over, klare til å kopieres (AR-20)

### Story 1.2: Appen er publisert på Vercel

Som faglærer og sensor,
vil jeg åpne appen på en adresse på nett,
slik at jeg kan vurdere den uten å installere noe, og se hver endring i en forhåndsvisning.

**Akseptansekriterier:**

**Gitt** at koden fra story 1.1 er merget til `main`, og at Hannah har godkjent at prosjektet opprettes
**Når** `vercel link` og `vercel git connect` kjøres
**Så** finnes ett Vercel-prosjekt for repoet under teamet `hannah-eriksen`, med Djangos framework preset (AD-15 punkt 1)

**Gitt** at Hannah har koblet til Neon fra Vercel Marketplace i Frankfurt, med forhåndsvisningsgrener
**Når** appen kjører på Vercel
**Så** bruker den Postgres via `DATABASE_URL` med `DISABLE_SERVER_SIDE_CURSORS = True`, og byggingen (`CI` er satt) bruker `DATABASE_URL_UNPOOLED`
**Og** lokalt, uten `DATABASE_URL`, brukes SQLite som før (AR-6)

**Gitt** en endring som merges til `main`
**Når** Vercel bygger
**Så** kjører byggesteget i `pyproject.toml` `python manage.py migrate --noinput`, Vercel kjører `collectstatic` med `STATIC_ROOT = staticfiles/`, og forsiden vises på `<prosjekt>.vercel.app` over HTTPS
**Og** `.python-version` er `3.14`, `vercel.json` setter `"regions": ["fra1"]`, og `requirements.txt` har `psycopg[binary]` 3.3.9

**Gitt** at `VERCEL` er satt
**Når** appen starter
**Så** er `DEBUG` alltid `False`, `ALLOWED_HOSTS` er `[".vercel.app"]`, `CSRF_TRUSTED_ORIGINS` er `["https://*.vercel.app"]`, `SECURE_PROXY_SSL_HEADER` er satt, og cookies for økt og CSRF er sikre
**Og** mangler `DJANGO_SECRET_KEY`, eller er den lik verdien i `.env.example`, stopper appen med en norsk melding
**Og** logging går til standard ut (AD-15 punkt 7)

**Gitt** en test som setter `VERCEL` og en gyldig nøkkel
**Når** `python manage.py test` kjører
**Så** gir `python manage.py check --deploy` ingen advarsler uten en begrunnelse i en kommentar i settings

**Gitt** en pull request
**Når** Vercel lager forhåndsvisningen
**Så** bruker den en egen Neon-gren, og den krever innlogging hos Vercel (AD-15 punkt 3)
**Og** `ANTHROPIC_API_KEY` finnes bare i produksjon, og `DJANGO_SECRET_KEY` (ulik for produksjon og forhåndsvisning) og `MET_USER_AGENT` finnes i alle miljøer, uten at noen verdi står i repoet (NFR-10)

**Gitt** README
**Når** sensor leser den
**Så** står adressen til den publiserte siden øverst, med en kort forklaring av publiseringen
**Og** lokal kjøring virker fortsatt uten Vercel, Neon, Vercel CLI eller Node (NFR-1)

### Story 1.3: Siden har et rolig og tilgjengelig grunnoppsett

Som Ola, som er nybegynner,
vil jeg ha en rolig og lesbar side som virker med tastatur og på mobil,
slik at jeg føler meg trygg og finner fram.

**Akseptansekriterier:**

**Gitt** `DESIGN.md`
**Når** stilarket lastes
**Så** finnes alle tokens som CSS-variabler i én fil: farger med `-dark`-par, kartlag-tokens uten `-dark`-par, typografiroller med systemfonter, spacing, `rounded` og layoutverdier (UX-DR1)
**Og** ingen komponent bruker fargeverdier direkte (`-dark`-verdiene tas i bruk med mørk modus i Epic 6)

**Gitt** en hvilken som helst side
**Når** den vises
**Så** har den `<html lang="nb">`, `header` med `nav`, én `main` og en sidetittel som slutter på « – Your Next Adventure» (UX-DR2)
**Og** toppmenyen har logoen, som fører til Søk. Den bryter til ny linje uten hamburgermeny, og det aktive punktet får `aria-current="page"` (UX-DR3; menypunktene kommer med kontofunksjonene i Epic 2)

**Gitt** en primær- eller sekundærknapp
**Når** den vises og brukes
**Så** er den minst 44 × 44 px med 8 px hjørner, og det er høyst én primærknapp per visning (UX-DR4, NFR-3)
**Og** under innsending får den `aria-disabled="true"`, beholder fokus og ignorerer nye klikk via `forbedring.js`, mens skjemaet fortsatt virker uten JavaScript (AR-18)

**Gitt** tastaturbruk
**Når** et element får fokus
**Så** vises en fokusring med `outline` på 3 px i `focus-ring` og 2 px avstand ved `:focus-visible`, og den fjernes aldri (UX-DR5)

**Gitt** komponenten Melding
**Når** den vises som info, advarsel, feil eller suksess
**Så** har den ikon og tittel, en 4 px venstrekant i statusfargen, står der saken gjelder og brukes aldri som toast (UX-DR21)
**Og** på samme side bruker den `role="status"` eller `role="alert"`, og når den følger med en navigering, får den fokus i stedet for `h1`

**Gitt** en bredde på 320 px, 200 % tekstzoom eller økt tekstavstand (WCAG 1.4.12)
**Når** siden vises
**Så** ruller ikke siden sidelengs, og ingen tekst klippes eller overlapper (NFR-4)
**Og** Display og Stor overskrift er 28 px under 720 px

**Gitt** `prefers-reduced-motion`
**Når** siden vises
**Så** er all bevegelse slått av (UX-DR33)

**Gitt** forsiden
**Når** et automatisk UU-verktøy kjøres
**Så** finner det ingen feil, og resultatet står i PR-en (NFR-4)

### Story 1.4: Turnivå og estimert tid regnes etter faste regler

Som Ola,
vil jeg at nivå og tid alltid regnes likt etter offentlige regler,
slik at jeg kan stole på at turen passer meg.

**Akseptansekriterier:**

**Gitt** `domene.tur.Tur`
**Når** en tur gjøres om med `til_geojson_feature()` og tilbake med `fra_geojson_feature()`
**Så** er resultatet lik den opprinnelige turen, og dataklassen er frossen med feltene og enhetene i AD-3 punkt 1 (AR-3)

**Gitt** gradering etter FR-2 og AR-19
**Når** testene kjøres
**Så** gir 4,9 km og 299 hm grønn, 5,0 km eller 300 hm blå (verdien på grensen graderes opp), 10,0 km eller 600 hm rød, og 20,0 km eller 1000 hm svart
**Og** den strengeste fargen vinner (3 km og 650 hm gir rød)
**Og** tur-retur graderes etter verdiene for én vei, og rundtur etter hele runden

**Gitt** estimert tid etter FR-3
**Når** regneeksempelet beregnes (tur-retur, 3 km én vei, 150 hm og 0 m nedstigning ut)
**Så** blir tiden 142,3 min, som vises som «ca. 2 t 20 min»
**Og** for tur-retur er høydemeterne tilbake lik nedstigningen ut og omvendt, påslaget er 15 %, og tiden avrundes til nærmeste 5 minutter

**Gitt** formateringen i `domene/`
**Når** verdier vises
**Så** blir de «ca. 1 t 35 min», «ca. 45 min», «3,5 km totalt», «Grønn – lett», «Blå – moderat», «Rød – moderat» og «Svart – vanskelig» (UX-DR31)

**Gitt** testene i `tests/domene/`
**Når** de kjøres
**Så** bruker de ikke databasen, og hver test viser til FR-2 eller FR-3 (AR-15, NFR-6)

### Story 1.5: Byggeskriptet lager turdatabasen fra Kartverket

Som Hannah, som bygger appen,
vil jeg ha et byggeskript som henter rute og høyder og beregner verdiene,
slik at turdatabasen blir lik hver gang, og appen aldri henter turdata mens den kjører.

**Akseptansekriterier:**

**Gitt** at formatet på kurateringslista er valgt (CSV, YAML eller TOML)
**Når** jeg åpner `data/`
**Så** har lista per tur `id`, navn, startpunkt (id, navn og koordinat), form, turtyper, kilde og kilde-ID og eventuell ut.no-URL, og formatet er beskrevet i en README i `data/` (AD-3 punkt 2)

**Gitt** en kurateringsliste med 2–3 testturer
**Når** jeg kjører `python -m skript.bygg_turdatabase`
**Så** skrives `data/turer.geojson` med alle feltene i AD-3 punkt 1, geometri i WGS84 og verdier for én vei ved tur-retur
**Og** turnavnet kommer bare fra kurateringslista

**Gitt** høydedata fra Kartverket
**Når** skriptet henter høyder
**Så** sender det høyst 50 punkter per kall, med et punkt hvert 10–25 m, filtrerer støy (terskel 2–10 m eller glatting) og lager høydeprofilen fra de samme filtrerte punktene
**Og** de valgte verdiene for terskel og punktavstand står i README-en i `data/` (spinen › Deferred)

**Gitt** geometri i UTM (EPSG:25832 eller 25833)
**Når** skriptet gjør den om
**Så** blir den WGS84 med `pyproj`, og `pyproj` står bare i `requirements-bygg.txt`

**Gitt** `data/osm-uttrekk.geojson` med ODbL-kreditering
**Når** uttrekket har 100 objekter eller flere
**Så** stopper skriptet med en melding (AD-3 punkt 3)

**Gitt** en kilde-ID som ikke finnes, eller et API som ikke svarer
**Når** skriptet kjører
**Så** stopper det med en melding som sier hvilken tur det gjelder, og den gamle `turer.geojson` overskrives ikke

**Gitt** testene for byggeskriptet
**Når** de kjøres
**Så** bruker de lagrede svar i `tests/fixtures/` uten nettverkskall, og beregningene går gjennom `domene/` (AR-2, AR-15)

### Story 1.6: Turene lastes inn med én kommando

Som sensor,
vil jeg laste turdatabasen med én kommando,
slik at appen har turer rett etter installasjonen.

**Akseptansekriterier:**

**Gitt** modellene for startpunkt og tur
**Når** migreringen kjøres
**Så** lagres geometri og høydeprofil i `JSONField`, uten GeoDjango eller SpatiaLite, og migreringen virker på både SQLite og Postgres (AR-6)

**Gitt** `data/turer.geojson`
**Når** jeg kjører `python manage.py lastinn` to ganger
**Så** opprettes eller oppdateres turene etter `id`, og antallet er det samme etter andre kjøring (AR-5)
**Og** en tur som mangler i fila, slettes ikke

**Gitt** en ugyldig eller ødelagt fil
**Når** `lastinn` kjøres
**Så** stopper kommandoen med en norsk melding, og ingenting i databasen endres

**Gitt** publiseringen på Vercel
**Når** Vercel bygger
**Så** kjører byggesteget `lastinn` etter `migrate` (AD-15 punkt 4)

**Gitt** appen
**Når** turene vises
**Så** leses turnivå, høydemeter og estimert tid fra databasen og beregnes aldri på nytt (AR-6)
**Og** README har `python manage.py lastinn` som eget steg

### Story 1.7: Turdatabasen har 15 kontrollerte turer

Som Ola,
vil jeg kunne få forslag blant nok turer i Oslo og Bærum,
slik at jeg finner en tur som passer tiden og turtypen.

**Akseptansekriterier:**

**Gitt** kurateringslista med 15 turer
**Når** turdatabasen bygges
**Så** er flertallet grønne eller blå. Den har minst én svart tur, minst tre toppturer og minst fem utsiktsturer, hver turtype har minst én grønn tur under 2 timer der terrenget gjør det mulig, og hvert startpunkt har minst to turer (FR-1)
**Og** en test sjekker sammensetningen mot `data/turer.geojson`, og unntak på grunn av terrenget er begrunnet i README-en i `data/`

**Gitt** hver rutelinje
**Når** den kontrolleres manuelt mot kartet
**Så** henger den sammen og starter ved riktig startpunkt, og kontrollen står med dato i en sjekkliste i `docs/`

**Gitt** tre av turene
**Når** høydemeterne og høydeprofilen sammenlignes med en publisert høydeprofil
**Så** er avvikene dokumentert, og terskelen for støyfiltrering er justert om det trengs (FR-1)

**Gitt** turene
**Når** jeg ser på kilde og lisens
**Så** har hver tur dem registrert, og OSM-uttrekket har færre enn 100 objekter totalt

### Story 1.8: Systemet velger og rangerer turer som passer søket

Som Ola,
vil jeg at systemet bare foreslår turer som passer tiden, turtypen og startpunktet mitt,
slik at jeg kan stole på forslaget.

**Akseptansekriterier:**

**Gitt** et søk (`domene.sok.Sok` med varighet, dato og eventuelt startpunkt og turtype), turene og et nivåtak
**Når** `velg_turer` kalles
**Så** returnerer den `Utvalg(status, rangerte_tur_ider)` uten database, nettverk eller klokke (AR-2, AR-13)

**Gitt** filteret i FR-5
**Når** turene filtreres
**Så** er bare turer med estimert tid kortere enn eller lik varigheten med (en tur med tid lik varigheten er med), og turnivået er aldri høyere enn nivåtaket
**Og** valgt turtype og valgt startpunkt filtreres når de er oppgitt

**Gitt** flere treff
**Når** de rangeres
**Så** kommer turen med estimert tid nærmest varigheten først, og deretter avgjør tur-ID-en, så samme søk alltid gir samme rekkefølge (FR-5 punkt 5 og 6)

**Gitt** en gjest eller en bruker uten historikk
**Når** nivåtaket bestemmes
**Så** er det grønt (FR-18)

**Gitt** turtypen topptur, ingen topptur som passer, men minst én utsiktstur som passer
**Når** `velg_turer` kalles
**Så** er statusen `TOPPTUR_ERSTATTET`, og utsiktsturene er rangert (FR-8)
**Og** passer heller ingen utsiktstur, er statusen `INGEN_TREFF`

**Gitt** at turer passer alt unntatt nivåtaket
**Når** `velg_turer` kalles
**Så** er statusen `BARE_OVER_NIVATAK`, og ingen tur over nivåtaket er med (FR-8, SM-C1)

**Gitt** at ingen tur passer, heller ikke over nivåtaket
**Når** `velg_turer` kalles
**Så** er statusen `INGEN_TREFF`

**Gitt** testene i `tests/domene/`
**Når** de kjøres
**Så** dekker de hvert kriterium over og viser til FR-5, FR-8 og FR-18 (SM-2)

### Story 1.9: Ola søker og får ett turforslag

Som Ola, som gjest,
vil jeg fylle ut varighet og dato og få ett konkret turforslag,
slik at jeg raskt kan bestemme meg.

**Akseptansekriterier:**

**Gitt** Søk-skjermen
**Når** den vises første gang
**Så** har den `h1` «Hvor lang tid har du?», ingressen og feltene i rekkefølgen fra `DESIGN.md`: Varighet (`<select>` med «Velg» og 1–8 t i halvtimessteg), Dato (`<select>` med de 31 aktuelle dagene, i dag forvalgt), Turtype (Turtypekort, «Alle turtyper» forvalgt) og Startpunkt («Alle startpunkt» og hjelpeteksten om Oslo-området) (FR-4, UX-DR6, UX-DR7, UX-DR10)
**Og** det finnes ikke noe fritekstfelt (det kommer i Epic 4)

**Gitt** et søk uten varighet
**Når** jeg trykker «Finn en tur»
**Så** sendes ikke søket. «Velg varighet» står under feltet med «!», feltet har `aria-invalid="true"` og `aria-describedby` til feil og så hjelpetekst, og fokus står i feltet
**Og** en dato utenfor perioden eller et ukjent startpunkt eller ukjent turtype i en manipulert POST gir feil ved feltet, uten krasj (FR-4, NFR-2, NFR-8)

**Gitt** et gyldig søk
**Når** jeg sender det
**Så** lages en tilfeldig søke-ID, søketilstanden med frosset rangering lagres i økten under `"sok"` via `turforslag/okt.py`, og jeg sendes videre til `/forslag/<sok_id>/` uten søket i adressen (AR-7)
**Og** økten beholder de 10 nyeste søkene

**Gitt** turforslaget
**Når** det vises
**Så** står i rekkefølge: søkeoppsummering med «Endre søk» (til forhåndsutfylt skjema), turnavn som `h1`, Nivåmerke med nivåforklaring, Turtype-treff (bare når en turtype er valgt), Formmerke, «Start: …», Faktarute med «pauser ikke inkludert», ut.no-lenke (skjult uten URL), KI-merket «Begrunnelse fra mal», `h2` «Begrunnelse» og Forklaringspanel, lukket som standard (FR-6, FR-12, UX-DR11, UX-DR12, UX-DR16, UX-DR17, UX-DR19)
**Og** sidetittelen er «{Turnavn} – Turforslag – Your Next Adventure»

**Gitt** at det ikke finnes KI-nøkkel
**Når** begrunnelsen lages
**Så** kommer den fra reservemalen i `domene/`, nevner varigheten og eventuell turtype, er høyst 300 tegn og nevner aldri fritekst (FR-12, FR-13)

**Gitt** et vist turforslag
**Når** jeg laster siden på nytt
**Så** vises samme tur uten ny rangering, og to faner med hvert sitt søk viser hvert sitt forslag (FR-7)

**Gitt** en ukjent søke-ID, eller en tur som ikke lenger finnes
**Når** jeg åpner adressen
**Så** vises Søk med meldingen «Turforslaget er ikke lenger tilgjengelig. Søk på nytt for å få et forslag.», og meldingen får fokus

**Gitt** en skjerm på 360 px
**Når** turforslaget vises
**Så** synes turnivå, estimert tid og Turtype-treff uten rulling, og alle trykkflater er minst 44 × 44 px (NFR-3)

**Gitt** testene i `tests/web/`
**Når** de kjøres
**Så** dekker de validering, videresending, søketilstand, ny innlasting og ukjent søke-ID, og views regner eller formaterer ingenting selv (AR-2)

### Story 1.10: Ola ser ruten på kart og i tekst

Som Ola,
vil jeg se ruten på et norsk turkart og kunne lese den som tekst,
slik at jeg vet hvor turen går, også med tastatur eller skjermleser.

**Akseptansekriterier:**

**Gitt** turforslaget
**Når** kartet lastes
**Så** tegner `kart.js` ruten fra GeoJSON i `json_script` med Leaflet 1.9.4 fra `static/vendor/leaflet/`. Kartflisene kommer fra Kartverket topo (zoom høyst 18, uten nøkkel), rutelinjen er plommelilla (5 px på 9 px hvit kant), startmarkøren er «S», og hele ruten vises (AR-10, UX-DR13)
**Og** nettleseren melder ingen CSP-brudd. Trenger Leaflet mer i CSP-en, er det begrunnet i beslutningsloggen (AR-17)

**Gitt** en bredde på 720 px eller mer
**Når** turforslaget vises
**Så** står kartet i venstre kolonne med `position: sticky` og Infokolonne til høyre. Under 720 px står kartet innenfor sidemargen med høyde ca. 60 % av skjermen (UX-DR12)

**Gitt** kartet
**Når** det vises
**Så** står lenken «Kartet i tekst» oppe til venstre, «Vis hele ruten» og zoom + og − oppe til høyre (44 px), målestokken nede til venstre og krediteringen nede til høyre. Krediteringen er alltid synlig, med understrekede lenker til Kartverket, OpenStreetMap (`lang="en"`) og MET Norge, uten Leaflets egen prefiks og med norske tekster på kontrollene (NFR-7, UX-DR14)

**Gitt** tastaturbruk
**Når** jeg tabber gjennom kartet
**Så** er rekkefølgen «Kartet i tekst», «Vis hele ruten», zoom og krediteringslenker. Kartflaten har `tabindex="0"`, `role="region"` og `aria-label="Kart over {turnavn}"`, piltastene flytter kartet, og + og − zoomer
**Og** Tab fører alltid videre ut av kartet, og markørene kan ikke få fokus (NFR-4)

**Gitt** mus eller berøring
**Når** jeg ruller med hjulet eller én finger over kartet
**Så** ruller siden. Ctrl/Cmd + hjul zoomer, én finger viser hintet «Bruk to fingre for å flytte kartet», og to fingre flytter kartet
**Og** dette løses med Leaflets innebygde valg. Går det ikke, er avviket begrunnet i beslutningsloggen (spinen › Deferred)

**Gitt** turforslaget
**Når** det vises
**Så** står `h2` «Kartet i tekst» med en tekst laget i `domene/` som nevner startpunkt, form, total lengde, høydemeter og laveste og høyeste punkt (FR-6, UX-DR15)

**Gitt** at kartflisene ikke lastes, eller at JavaScript er slått av
**Når** turforslaget vises
**Så** viser kartflaten en infomelding med «Prøv igjen» og lenke til «Kartet i tekst», og resten av forslaget vises som vanlig (AD-1)

**Gitt** `prefers-reduced-motion`
**Når** kartet flyttes
**Så** skjer det uten animasjon

### Story 1.11: Ola kan be om nytt forslag

Som Ola,
vil jeg kunne be om et nytt forslag uten å søke på nytt,
slik at jeg kan velge en annen tur hvis den første ikke frister.

**Akseptansekriterier:**

**Gitt** et turforslag
**Når** jeg trykker «Nytt forslag»
**Så** vises neste tur i den frosne rangeringen, aldri en tur som alt er vist i dette søket, og POST følger Post/Redirect/Get (FR-7, AR-7)

**Gitt** at alle treff er vist
**Når** jeg trykker «Nytt forslag»
**Så** vises Tilstandspanel med `h1` «Du har sett alle turene som passer søket», antallet turer, endringsforslag, «Start fra første forslag igjen» og «Endre søk» (FR-7, UX-DR22)

**Gitt** Tilstandspanel for «alle vist»
**Når** jeg trykker «Start fra første forslag igjen»
**Så** vises første forslag igjen, og listen over viste turer starter på nytt

**Gitt** et forslag etter «Nytt forslag»
**Når** jeg laster siden på nytt
**Så** vises samme forslag, og listen over viste turer er den samme. Et nytt søk eller en annen fane påvirker ikke dette søket

**Gitt** JavaScript
**Når** jeg trykker «Nytt forslag»
**Så** henter `forbedring.js` et HTML-fragment fra serveren. Det gamle forslaget dempes, knappen beholder fokus, visningen får `aria-busy="true"`, og «Finner et nytt forslag …» leses opp i en `aria-live="polite"`-region utenfor
**Og** etter byttet er `document.title` oppdatert, fokus står på nytt `h1`, og kartet viser den nye ruten (UX-DR23, UX-DR24, UX-DR25)
**Og** uten JavaScript gir knappen en vanlig sideinnlasting med samme resultat

**Gitt** et søk som sendes
**Når** forslaget hentes
**Så** vises lasteindikatoren med søkeoppsummeringen, en tom kartflate og «Kart lastes …», uten spinner ved `prefers-reduced-motion` (UX-DR23)

**Gitt** et dobbeltklikk på «Nytt forslag»
**Når** det sendes
**Så** går forslaget bare ett steg videre (NFR-2)

**Gitt** testene
**Når** de kjøres
**Så** dekker de rekkefølge, ingen gjentakelse, «alle vist», start på nytt og ny innlasting (SM-2)

### Story 1.12: Ola får hjelp når ingen tur passer

Som Ola,
vil jeg få vite hvorfor jeg ikke får en tur og hva jeg kan endre,
slik at jeg ikke står fast.

**Akseptansekriterier:**

**Gitt** status `TOPPTUR_ERSTATTET`
**Når** forslaget vises
**Så** vises en utsiktstur med merket «Utsikt i stedet for topptur» og Melding (advarsel) «Toppturer krever mer tid enn du har oppgitt» rett etter turnavnet (FR-8, UX-DR17)

**Gitt** status `INGEN_TREFF`
**Når** forslaget vises
**Så** vises Tilstandspanel med `h1` «Jeg fant ingen tur som passer søket ditt», «Prøv å endre søket:» og konkrete endringsforslag for lengre varighet, et annet startpunkt og en annen turtype (FR-8, UX-DR22)
**Og** et forslag vises bare når endringen gir minst ett treff. Det avgjøres av en ren funksjon i `domene/`

**Gitt** et endringsforslag som «Prøv 3 timer» eller «Prøv marka»
**Når** jeg trykker på det
**Så** kjøres søket på nytt med én endring og en ny søke-ID
**Og** «Velg startpunkt» går til det forhåndsutfylte skjemaet med fokus på Startpunkt

**Gitt** status `BARE_OVER_NIVATAK` for en gjest
**Når** forslaget vises
**Så** vises Tilstandspanel med `h1` «Ingen grønne turer passer søket» og gjesteteksten fra Mikrotekst, uten løfte om lengre eller hardere turer (FR-8, SM-C1)
**Og** lenken «Lag konto» i teksten legges til i Epic 2, når kontoopprettelsen finnes

**Gitt** et Tilstandspanel
**Når** det vises
**Så** er `document.title` lik overskriften, fokus står på `h1`, og «Endre søk» er alltid med (UX-DR25, NFR-2)

**Gitt** testene i `tests/web/`
**Når** de kjøres
**Så** dekker de hver status og endringsforslagene (SM-2)

## Epic 2: Ola lager konto og registrerer turene sine

Gjesten lager konto uten å miste forslaget, registrerer gjennomførte turer med vurdering, ser historikken, åpner en tur fra historikken og kan slette kontoen. Innloggingen har en grense for mislykkede forsøk, og registreringen tåler dobbeltklikk.

### Story 2.1: Ola lager konto, logger inn og logger ut

Som Ola, som gjest,
vil jeg lage konto med e-post og passord og kunne logge inn og ut,
slik at jeg senere kan registrere turene mine.

**Akseptansekriterier:**

**Gitt** skjermen Logg inn / Lag konto
**Når** den åpnes fra «Logg inn» i toppmenyen
**Så** vises visningen «Logg inn» med e-post (`type="email"`, `autocomplete="email"`), passord (`autocomplete="current-password"`), primærknappen «Logg inn» og lenken «Har du ikke konto? Lag konto». Visningen «Lag konto» har `autocomplete="new-password"`, hjelpeteksten «Minst 8 tegn» og primærknappen «Lag konto og fortsett» (UX-DR26)
**Og** «Vis passord» kommer fra `forbedring.js`, og skjemaet virker uten JavaScript (AR-18)

**Gitt** en ny e-post og et passord på minst 8 tegn
**Når** jeg lager konto
**Så** lagres e-posten med små bokstaver og passordet bare som hash, jeg blir logget inn og kommer tilbake dit jeg var (FR-14, AR-9)
**Og** et turforslag jeg så på som gjest, er det samme etter innloggingen, fordi Djangos `login()` beholder økten (AR-7)

**Gitt** en e-post som allerede har konto
**Når** jeg prøver å lage konto med den
**Så** vises Melding (feil) «Kunne ikke lage konto – prøv å logge inn», og ingen konto lages (FR-14)
**Og** et passord under 8 tegn eller en ugyldig e-post gir feil ved feltet, med teksten fra Mikrotekst

**Gitt** feil e-post eller feil passord
**Når** jeg logger inn
**Så** vises «Feil e-post eller passord», uten å si hvilket felt som er feil, og e-posten står fortsatt i feltet (FR-14)

**Gitt** at jeg er innlogget
**Når** jeg ser på toppmenyen
**Så** viser den logo, «Finn tur» og «Konto», og gjester ser logo og «Logg inn» (UX-DR3). «Historikk» kommer i story 2.3

**Gitt** skjermen Konto
**Når** jeg åpner den
**Så** viser den e-posten min, `h2` «Personvern» med personverntekst fra Mikrotekst og knappen «Logg ut» (NFR-5, UX-DR30)
**Og** «Logg ut» er en POST som tømmer økten, og jeg havner på Søk med «Du er logget ut.», som får fokus (AD-6)

**Gitt** innloggingen
**Når** jeg ikke gjør noe på lenge
**Så** varer innloggingen i to uker uten grense for inaktivitet (AD-6)

**Gitt** nivåtakmeldingen for gjester fra story 1.12
**Når** den vises
**Så** har den lenken «Lag konto» til visningen «Lag konto»

**Gitt** testene i `tests/web/`
**Når** de kjøres
**Så** dekker de kontooppretting, duplisert e-post, feil innlogging, utlogging og at turforslaget beholdes gjennom innloggingen (NFR-6)

### Story 2.2: Innloggingen har en grense for mislykkede forsøk

Som Ola,
vil jeg at ingen kan prøve ut passordet mitt i det uendelige,
slik at kontoen min er trygg på den publiserte siden.

**Akseptansekriterier:**

**Gitt** modellen `Innloggingsforsok(epost, tidspunkt)`
**Når** en innlogging mislykkes
**Så** lagres forsøket med e-posten i små bokstaver, også når e-posten ikke har konto (AR-9)

**Gitt** 5 mislykkede forsøk med samme e-post de siste 15 minuttene
**Når** jeg prøver å logge inn igjen med den e-posten
**Så** kalles ikke `authenticate()`, og Melding (feil) viser «Det har vært for mange forsøk på å logge inn med denne e-postadressen. Vent 15 minutter, og prøv igjen.», uten å si om e-posten har konto (NFR-8)
**Og** e-posten står fortsatt i feltet, men passordet er tømt

**Gitt** at grensen er nådd
**Når** 15 minutter har gått siden det eldste av de fem forsøkene
**Så** kan jeg prøve igjen

**Gitt** en vellykket innlogging
**Når** den skjer
**Så** slettes forsøkene for e-posten, og forsøk eldre enn sperretiden slettes ved hver sjekk

**Gitt** avgjørelsen
**Når** den tas
**Så** gjøres den av en ren funksjon i `domene/`, som får tidspunktene og klokkeslettet inn, med `INNLOGGING_MAKS_FORSOK` og `INNLOGGING_SPERRETID_MIN` fra `settings` (AR-2)
**Og** testene dekker grensen, at sperren slutter, og at den gjelder like mye for e-poster uten konto

### Story 2.3: Ola registrerer en gjennomført tur og ser den i historikken

Som Ola, som er innlogget,
vil jeg registrere en tur jeg har gått, med hvordan den kjentes,
slik at tjenesten kan bruke vurderingen og jeg kan finne turen igjen.

**Akseptansekriterier:**

**Gitt** et turforslag mens jeg er innlogget
**Når** jeg trykker «Registrer gjennomført tur»
**Så** åpnes en egen side på `/registrer/<tur_id>/` med Turoppsummering øverst (navn, nivå, form, lengde og estimert tid), «Alle fire felt er påkrevd.» og feltene dato (`<input type="date">`, i dag forvalgt, `max` i dag), brukt tid (`fieldset` med Timer og Minutter, hjelpetekst «10 min–24 t»), opplevd vanskelighet og fornøydhet som Valggruppe med `fieldset` og `legend` (FR-16, UX-DR8, UX-DR27, UX-DR28)
**Og** «Registrer gjennomført tur» er sekundærknapp på turforslaget, og «Nytt forslag» er primær

**Gitt** en dato frem i tid, brukt tid under 10 minutter eller over 24 timer, eller et felt som mangler
**Når** jeg sender skjemaet
**Så** lagres ingenting, feilen står ved feltet med teksten fra Mikrotekst, og fokus går til første felt med feil (FR-16, NFR-2)

**Gitt** et gyldig skjema
**Når** jeg sender det
**Så** lagres en `Registrering` for meg og turen, med `on_delete=PROTECT` mot turen, og jeg sendes til Historikk med Melding (suksess) «Turen er registrert i historikken din.», som får fokus (AR-5, UX-DR21)
**Og** tur-ID-en tas fra URL-en, aldri fra økten (AR-7)

**Gitt** et engangstoken i økten
**Når** jeg dobbeltklikker eller sender samme skjema to ganger
**Så** blir det bare én registrering, og et brukt eller ukjent token sender meg til Historikk uten å lagre noe (AD-14, AR-14)

**Gitt** Historikk
**Når** jeg åpner den fra «Historikk» i toppmenyen
**Så** viser en ekte `<table>` registreringene mine, nyeste først, med én rad per registrering, også når samme tur er gått flere ganger. Kolonnene er Tur (`<th scope="row">`, med Nivåmerke under), Dato, Brukt tid (med «estimert ca. …» under), Opplevd vanskelighet og Fornøydhet («5 av 5»), og handlingskolonnen har skjult overskrift «Handlinger» (FR-17, UX-DR29)
**Og** under 720 px ruller tabellen sidelengs i egen beholder (`role="region"`, `aria-label="Historikk"`, `tabindex="0"`), og under tabellen står «Nye søk prioriterer turer du ikke har gått.»

**Gitt** at jeg ikke har registrert noen turer
**Når** jeg åpner Historikk
**Så** vises Tilstandspanel med «Du har ikke registrert noen turer ennå.» og «Finn tur»

**Gitt** en annen brukers registrering
**Når** jeg prøver å se den
**Så** ser jeg den ikke, fordi alt hentes filtrert på `request.user` (NFR-8)

**Gitt** en tur med registreringer som mangler i `turer.geojson`
**Når** `lastinn` kjøres
**Så** stopper kommandoen med en melding som sier hvilken tur det gjelder, og ingenting slettes (AD-3 punkt 4)

### Story 2.4: Ola åpner en tur fra historikken

Som Ola,
vil jeg kunne åpne en tur jeg har gått før og registrere den igjen,
slik at jeg lett kan gå favoritturene mine på nytt.

**Akseptansekriterier:**

**Gitt** en rad i Historikk
**Når** jeg trykker «Åpne som turforslag»
**Så** vises turen som turforslag fra historikken, med «Fra historikken din» i stedet for søkeoppsummeringen, uten Turtype-treff, og med kart og tall som vanlig (FR-17)
**Og** handlingene har skjulte tillegg, for eksempel «– Granåsen rundt, 7. nov.» (UX-DR29)

**Gitt** et turforslag fra historikken
**Når** begrunnelsen vises
**Så** kommer den fra en fast mal uten KI, for eksempel «Du gikk denne turen 12. oktober og ga den 5 av 5.», og KI-merket viser «Begrunnelse fra mal» (FR-17, FR-12)
**Og** «Nytt forslag» er byttet ut med «Finn en ny tur», som går til Søk

**Gitt** en tur over nivåtaket mitt
**Når** jeg åpner den fra historikken
**Så** vises den likevel, med Melding (info) «Denne turen er over nivået jeg foreslår for deg nå.» rett etter turnavnet (FR-17)

**Gitt** et pågående søk i en fane
**Når** jeg åpner en tur fra historikken
**Så** endres ikke søketilstanden for søket (FR-7)

**Gitt** en rad i Historikk
**Når** jeg trykker «Registrer gjennomført tur»
**Så** åpnes registreringen for den turen (FR-16)

### Story 2.5: Gjesten blir bedt om å logge inn og kommer rett tilbake

Som Ola, som gjest,
vil jeg kunne trykke «Registrer gjennomført tur» før jeg har konto,
slik at jeg ikke mister turen jeg nettopp har valgt.

**Akseptansekriterier:**

**Gitt** et turforslag som gjest
**Når** jeg trykker «Registrer gjennomført tur»
**Så** kommer jeg til Logg inn / Lag konto med Turoppsummering, «Logg inn for å registrere», «Turforslaget er tatt vare på.» og lenken «Tilbake til turforslaget» (FR-14, UX-DR26)

**Gitt** den siden
**Når** jeg logger inn eller lager konto
**Så** går jeg rett inn i registreringen av den samme turen (FR-14)
**Og** «Tilbake til turforslaget» viser det samme forslaget som før

**Gitt** at jeg er gjest
**Når** jeg åpner Historikk, Konto eller en registreringsside direkte
**Så** sendes jeg til Logg inn med `next`, og etter innloggingen tilbake dit (AD-6)

**Gitt** at innloggingen har utløpt
**Når** jeg åpner en side som krever konto
**Så** sendes jeg til Logg inn og tilbake til samme side etterpå. Om utfylte felt beholdes, avgjøres og dokumenteres i denne storyen (åpent punkt i `EXPERIENCE.md`)

**Gitt** en `next`-adresse til et annet nettsted
**Når** jeg logger inn
**Så** sendes jeg til Søk i stedet, så ingen kan bruke innloggingen til å sende brukere videre (NFR-8)

### Story 2.6: Ola sletter kontoen

Som Ola,
vil jeg kunne slette kontoen og alt jeg har registrert,
slik at jeg bestemmer over dataene mine.

**Akseptansekriterier:**

**Gitt** Konto
**Når** jeg trykker «Slett konto»
**Så** åpnes en egen side med `h1` «Vil du slette kontoen?», «All historikken din slettes for godt, og det kan ikke angres.», primærknappen «Slett kontoen» og «Avbryt» (FR-15, UX-DR30)
**Og** «Slett kontoen» står ikke på samme sted som «Slett konto» på Konto, siden har ingen rød flate, og jeg må ikke skrive inn e-posten

**Gitt** bekreftelsessiden
**Når** jeg trykker «Avbryt»
**Så** kommer jeg tilbake til Konto, og ingenting er endret

**Gitt** bekreftelsessiden
**Når** jeg trykker «Slett kontoen»
**Så** slettes brukeren, e-posten, passord-hashen og alle registreringer i én transaksjon. Deretter kalles `logout()`, og jeg havner på Søk som gjest med «Kontoen din er slettet.», som får fokus (FR-15, AR-9)

**Gitt** at slettingen feiler
**Når** transaksjonen rulles tilbake
**Så** slettes ingenting, og jeg får Melding (feil) med «Prøv igjen» (FR-15, NFR-2)

**Gitt** testene
**Når** de kjøres
**Så** dekker de sletting, avbryt og feil i transaksjonen, og at en annen brukers data ikke påvirkes (NFR-8)
