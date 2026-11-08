# Redaksjonell gjennomgang – docs/arkitektur.md (2026-11-08)

Linser: `structure` og deretter `prose` (bmad-review). Tilleggsoppgave: avvik fra den bindende spinen (`ARCHITECTURE-SPINE.md`). `docs/arkitektur.md` er ikke endret.

- **Innhold:** dokument (docs), 1 537 ord (word_metrics.py).
- **Lesertype:** mennesker (sensor som ikke leser kode).
- **Stilguide:** prosjektets egen stil går foran Microsoft Writing Style Guide: korte, enkle setninger på bokmål, aktiv form, norske ord der de finnes.
- **Formål:** Dokumentet skal hjelpe sensor å forstå hvordan *Your Next Adventure* er bygget og hvorfor, uten å lese kode, og å spore hvert valg tilbake til spinen.
- **Strukturmodell:** Forklaring (konseptuell): fra det abstrakte til det konkrete. Dokumentet følger modellen godt: Utgangspunktet (hvorfor) → Oversikt → Lagene → Turdatabasen → flyten → temaseksjoner → referanse (Teknologi, Mappestruktur) → avgrensning.

## Dom

**Godt dokument, men tre faktafeil må rettes før det leveres.** Formen passer formålet, og språket er stort sett enkelt og aktivt. De viktigste funnene:

1. Tre påstander stemmer ikke med spinen: nettsiden «bruker de samme funksjonene for gradering og tid» (AD-3.6 sier at appen aldri beregner disse på nytt), reservemalen brukes ikke når kall A forkastes (AD-10.7), og testbrukerens historikk slettes ved `lastinn` (AD-3.4).
2. Nøkkelbegreper (nivåtak, sperre, nøkkel) brukes før de er forklart.
3. Seks av de 14 beslutningene (AD-2, 5, 6, 7, 12, 13) nevnes ikke, selv om innledningen lover sporing fra AD-1 til AD-14.

Antall: 6 struktur, 16 prosa og 9 avvik fra spinen (hvorav 3 reelle feil og 6 presiseringer eller utelatelser).

---

## Avvik fra spinen

| # | Sted | Dokumentet sier | Spinen sier | Forslag |
| --- | --- | --- | --- | --- |
| F1 | §Lagene, l. 52 | «Byggeskriptet og nettsiden bruker de samme funksjonene for gradering og tid, så verdiene kan ikke bli ulike.» | AD-3.6: «Appen beregner aldri turnivå, høydemeter eller estimert tid på nytt.» Kapabilitetskartet: gradering og tid ligger i `domene/` og brukes av `skript/`. | «Bare byggeskriptet beregner turnivå og tid. Nettsiden leser de ferdige verdiene og bruker de samme reglene til å vise dem, så verdiene kan ikke bli ulike.» |
| F2 | §KI og personvern, l. 113 | «Bryter svaret reglene, er det for langt eller kommer etter mer enn 5 sekunder, brukes reservemalen (FR-13).» | AD-10.7: når kall A (tolking) forkastes, ignoreres friteksten for hele søket. Bare når kall B (begrunnelse) forkastes, brukes reservemalen. | «Bryter et svar reglene, er det for langt, eller tar det mer enn 5 sekunder, forkaster appen svaret. Forkastes tolkingen, ser appen bort fra friteksten. Forkastes begrunnelsen, bruker appen reservemalen (FR-13).» |
| F3 | §Turdatabasen, l. 69 | «Kommandoen kan kjøres flere ganger uten å slette historikken til brukerne.» | AD-3.4: turer oppdateres og slettes aldri, men testbrukeren slettes og lages på nytt fra fil ved hver kjøring. | «Kommandoen kan kjøres flere ganger uten å slette historikken til brukerne. Bare testbrukeren lages på nytt.» |
| F4 | §Et søk, l. 94 | «Uten svar fra MET vises forslaget uten bekledningstips …» | AD-9: `IngenVarsel` har to grunner: `UTILGJENGELIG` og `FOR_LANGT_FREM` (datoen er mer enn ca. 9 dager frem). | «Uten værvarsel (MET svarer ikke, eller datoen er mer enn ca. 9 dager frem) vises forslaget uten bekledningstips …» |
| F5 | §Turdatabasen, l. 67 | «(«Ukjent» på 41 av 186 ruter)» | Tallene i researchen gjelder Oslo. I Bærum heter 29 av 59 ruter «Ukjent». | «(«Ukjent» på 41 av 186 ruter i Oslo)» |
| F6 | §Turdatabasen, l. 68 | «fra det norske UTM-formatet til vanlige GPS-koordinater» | AD-3.2: UTM (EPSG:25832/25833) til WGS84. UTM er et internasjonalt system, ikke et norsk format. | «fra UTM-koordinatene i kartdataene til vanlige GPS-koordinater» |
| F7 | §KI og personvern, l. 111 | «KI … har tre roller i koden» | AD-10.1: ett grensesnitt med tre **varianter**. KI har to oppgaver (tolking og begrunnelse), så «roller» kan forveksles med dem. | «KI er valgfri. Koden har tre varianter av KI-modulen:» |
| F8 | §Teknologi, l. 138–147 | Tabellen mangler eksterne tjenester. SQLite er oppført som «følger med Python». | Spinen har også Kartverket topo WMTS (v1), MET Locationforecast 2.0 og Kartverket høyde-API v1, og krever SQLite «3.37 eller nyere». | Legg til tre rader for tjenestene. SQLite: «3.37 eller nyere (følger med Python)». |
| F9 | §Mappestruktur, l. 155 | Rotfilene mangler `pyproject.toml`. | Kildetreet har `pyproject.toml` (Ruff-oppsett). | Legg `pyproject.toml` til rotlinja. |

---

## Funn

| Pass | Original Text | Revised Text | Changes |
| --- | --- | --- | --- |
| structure | §Personalisering (60 ord). «Nivåtak» brukes først i sekvensdiagrammet (l. 82) og valgtabellen (l. 106). «Sperre» brukes i l. 119. Ingen av dem forklares. | CONDENSE/legg til stillas: to setninger først i §Personalisering: «Nivåtaket er det høyeste turnivået appen foreslår for en bruker. En sperre senker nivåtaket for en tid etter en tur som var vanskelig.» (fra PRD §3) | Manglende stillas: sensor møter nøkkelbegrepet før det er forklart (+~25 ord) |
| structure | Hele dokumentet. AD-2, AD-5, AD-6, AD-7, AD-12 og AD-13 nevnes ikke. | Legg AD-nummer til der temaet står: §Lagene-tabellen eller l. 49 (AD-2), «Søke-ID» l. 92 (AD-5), «Innloggingen varer i to uker» l. 129 (AD-6, NFR-4), «Passord lagres» l. 125 (AD-7), «Nøkler ligger i `.env`» l. 130 (AD-12), §Testing (AD-13) | Innledningen lover sporing fra AD-1 til AD-14. Nå finner sensor bare 8 av 14 (+~10 ord) |
| structure | §Viktige valg og hvorfor (282 ord), plassert mellom flyten og temaseksjonene | MOVE: flytt seksjonen til etter §Testing, før §Teknologi | Radene for AD-10 og AD-11 viser til nivåtak, reserve og KI før §KI og §Personalisering forklarer dem. Plassert senere blir tabellen en oppsummering av det sensor allerede har lest (0 ord) |
| structure | §Viktige valg og hvorfor, selve tabellen | PRESERVE | Delvis lik tidligere tekst (SQLite, ferdigbygget turdatabase, MET), men kolonnen «Forkastet» finnes ikke andre steder. For sensor er dette den viktigste begrunnelsen |
| structure | §KI og personvern, l. 111: «Appen velger reserve automatisk når nøkkelen mangler.» | PRESERVE | Gjentar l. 93, men står i temaseksjonen der sensor vil lete. Gjentakelsen hjelper |
| structure | §Mappestruktur (45 ord), overlapper med tabellen i §Lagene | PRESERVE (rett F9) | Treet viser `config/`, `data/` og `tests/`, som lagtabellen ikke har. Treet passer som oppslag på slutten |
| prose | Tre forhold … **uten nøkler** (NFR-1). | … uten nøkler (tilgangskoder til eksterne tjenester) (NFR-1). | «Nøkkel» brukes 10 ganger og forklares aldri. Lesere uten kodebakgrunn trenger forklaringen én gang |
| prose | Reglene er skrevet slik at to KI-økter som bygger hver sin del, ikke kan lage deler som ikke passer sammen. | Arkitekturreglene er skrevet slik at to KI-økter som bygger hver sin del, lager deler som passer sammen. | Fjerner dobbelt nektelse. «Reglene» betyr ellers domenereglene (punkt 3, §Lagene), så her trengs et eget ord |
| prose | Appen er én Django-nettside som kjører på **din egen** maskin. / ID-en virker bare i **din egen** nettleser … | … som kjører lokalt på maskinen. / ID-en virker bare i nettleseren der søket ble gjort … | Resten av dokumentet omtaler «sensor» og «brukeren» i tredje person. Jevn tiltale |
| prose | sider, skjemaer, **database-modeller**, maler | sider, skjemaer, **databasemodeller**, maler | Norsk særskriving/bindestrek: sammensatt ord skrives i ett |
| prose | Reglene kan testes én og én på **brøkdelen** av et sekund | … på **en brøkdel** av et sekund | Idiomatisk bokmål |
| prose | Pilene viser hvem som får bruke hvem. `domene/` bruker ingen av de andre. **Det** har to fordeler: | Pilene viser hvilke lag som får bruke hvilke. `domene/` bruker ingen av de andre. **Dette** har to fordeler: | Lagene er ting, ikke personer. «Dette» peker tydeligere på hele setningen før |
| prose | Turnavnet **skrives selv**, fordi kildene ofte mangler navn | Turnavnet **skrives inn for hånd**, fordi kildene ofte mangler navn | «Skrives selv» er uklart: hvem skriver? Samme ord som i l. 67 og diagrammet |
| prose | slik ODbL-lisensen krever for et «uvesentlig» uttrekk | slik at det regnes som et «uvesentlig» uttrekk etter ODbL-lisensen | Lisensen krever ikke dette. Kravene avgjør bare om uttrekket regnes som uvesentlig (addendumet kaller det en tolkning) |
| prose | Slik kjører sensor appen, og hele kjerneflyten virker (SM-3). | Sensor kjører appen slik som standard, og hele kjerneflyten virker (SM-3). | «Slik kjører sensor appen» kan leses som en instruks. Gjør det tydelig at det er standardoppsettet |
| prose | **Django, én server-rendret nettside** (AD-1) | **Django, én nettside der serveren lager alle sidene** (AD-1) | «Server-rendret» er en anglisisme. §Oversikt sier det samme på vanlig norsk |
| prose | Innlogging, skjemaer, database og sikkerhet følger med, så **mindre sikkerhetskode skrives selv** | … følger med, så **utvikleren skriver mindre sikkerhetskode selv** | Aktiv form, tydelig hvem som gjør det |
| prose | Henting av turdata mens appen kjører (**utenfor scope** i PRD-en) | Henting av turdata mens appen kjører (**utenfor omfanget** i PRD-en) | Anglisisme der et norsk ord finnes |
| prose | Leaflet ligger i repoet, så **ingen CDN eller npm** | Consider: Leaflet ligger i repoet, så appen henter ingen kode fra nettet og trenger ingen JavaScript-verktøy? | «CDN» og «npm» sier ingenting til lesere uten kodebakgrunn |
| prose | **Betalte API-kall brukes ikke til trening**, så fritekst fra brukere havner ikke i treningsdata (NFR-5). | **Anthropic bruker ikke betalte API-kall til trening**, så … | Aktiv form, navngir aktøren |
| prose | **Det** kan aldri komme i utakt med registreringene | **Nivåtaket** kan aldri komme i utakt med registreringene | Uklart hva «Det» viser til (valget, tabellen eller nivåtaket) |
| prose | **All input sjekkes på serveren**, og skjemaer er beskyttet … | **Serveren sjekker alt brukeren sender inn**, og skjemaer er beskyttet … | Anglisisme («input») og passiv form |
| prose | Nøkler ligger i `.env`, som aldri **committes**. | Nøkler ligger i `.env`, som aldri **legges i git**. | Anglisisme og fagsjargong. «Git» brukes allerede i dokumentet (l. 63) |

Øvrige mindre forhold (ikke tatt med som egne rader): «repoet» (l. 28, 103) kunne vært forklart som «prosjektmappen (repoet)» ved første bruk. l. 149 nevner «npm», selv om dokumentet sier at prosjektet ikke bruker npm. Det er riktig (Leaflet-versjonen er sjekket der), men kan forvirre sensor.

### Stil som bevares

- Korte setninger, nummererte «Derfor …»-begrunnelser og tabeller med «Hvorfor/Forkastet» passer leseren godt.
- Radikale bokmålsformer (*fila*, *lista*) brukes konsekvent. Behold dem.
- Krav-ID-er i parentes (FR-, NFR-, AD-) er bevisst sporing og ikke støy.
- Engelske egennavn (*Your Next Adventure*, Django, Leaflet) og kodenavn i backticks er riktige.

## Oppsummering

- **Anbefalinger:** 6 struktur (3 endringer, 3 PRESERVE), 16 prosa og 9 avvik fra spinen.
- **Ordomfang hvis alt godtas:** dokumentet blir **ca. 60–80 ord lengre** (fra 1 537 til ca. 1 600, +4–5 %). Ingen seksjon foreslås kuttet. Økningen kommer av definisjoner (nivåtak, sperre, nøkkel), AD-henvisninger og presiseringer fra spinen. Det er ikke satt noe lengdemål.
- **Avveiinger for forståelsen:** ingen. Ingen forslag kutter diagrammer, tabeller, eksempler eller oppsummeringer. Flyttingen av §Viktige valg endrer bare rekkefølgen.
- **Bør rettes først:** F1, F2 og F3 (faktafeil mot spinen), deretter definisjonen av nivåtak og sperre og AD-henvisningene.
