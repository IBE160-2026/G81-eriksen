# Strukturgjennomgang: PRD Your Next Adventure

**Linse:** Editorial Structure (bmad-review) · **Dato:** 2026-11-06 · **Gjennomgått fil:** `prd.md` (4 535 ord, målt med `word_metrics.py`)

**Lesing av formålet:** Dokumentet skal hjelpe studenten, sensor og BMAD-arbeidsflytene som kommer etter (arkitektur, epics, stories), med å se nøyaktig hva v1 skal levere, hvorfor, og hvordan leveransen skal verifiseres. Kravene skal kunne spores med faste ID-er.

**Strukturmodell:** Strategic/Context (Pyramid). Den er justert for to typer lesere: mennesker (sensor) og LLM-arbeidsflyter (avhengigheter først, fast skjema per krav). Kravs-ID-ene (UJ, FR, NFR, SM) beholdes slik de er. Ingen av forslagene endrer nummereringen.

**Innhold:** Innholdet er ikke vurdert. Forslagene gjelder bare plassering, sammenslåing og fortetting.

| Pass | Original Text | Revised Text | Changes |
|---|---|---|---|
| structure | §10 «Lukkede punkter», første kulepunkt (MET-vilkår: kall via egen server med mellomlagring, påkrevd User-Agent, maks 4 desimaler) (~45 ord) | MOVE til §4.4 Vær og bekledning (Beskrivelse) eller som et punkt under NFR | Dette er føringer for arkitekturen, men de ligger gjemt i en liste over lukkede spørsmål. Arkitektur-arbeidsflyten leser §4 og §5 og kan gå glipp av dem. 0 ord netto |
| structure | Begrepet «kjerneflyten» er definert først i SM-1 (§8), men brukes allerede i §4.5, SM-3, NFR-2 og NFR-4 | MOVE definisjonen (søke som gjest → få forslag → registrere seg → registrere tur med vurdering → søke på nytt) til §3 Begreper. SM-1 viser til §3 | Nøkkelbegrepet blir definert før det brukes, slik §0 lover («Begrepene i §3 brukes konsekvent»). Det gir mindre rom for feiltolkning nedstrøms. 0 ord netto |
| structure | §7 Scope, særlig P1/P2-prioriteringen (~190 ord), står etter NFR og plattform | MOVE §7 opp, rett etter §2 (eller §1), og behold nummereringen av §-ene om ønskelig | I pyramidemodellen skal omfang og prioritet komme tidlig. Det er det første epics-arbeidsflyten og sensor trenger, og det rammer inn lesingen av FR-ene. 0 ord netto |
| structure | §10 «Bekreftede antakelser» og «Standardverdier godkjent av produkteier» (~110 ord) | CONDENSE til én linje i §10 («Alle antakelser er bekreftet og alle standardverdier godkjent 2026-11-06, se endringsloggen 0.3 og 0.5. Ingen åpne spørsmål.»). Selve listene kan flyttes til endringsloggen eller addendum | Punktene gjentar innhold som allerede står i FR-5, FR-19 og FR-20. Overskriften «Antakelser og åpne spørsmål» lover åpne punkter som ikke finnes. Sparer ca. 90 ord |
| structure | Plasseringen av «Gjelder UJ-x» varierer: i Beskrivelse (4.2, 4.3, 4.4, 4.6), i første linje (FR-1, FR-16) og i siste linje (FR-11, FR-17). 4.7 og 4.9 har ingen Beskrivelse | CONDENSE til ett fast skjema: «Gjelder UJ-x» står på samme sted i hver §4.x-Beskrivelse (eller i hver FR) | Med et fast skjema kan stories-arbeidsflyten hente sporingen mekanisk. Ca. 0–10 ord |
| structure | §4.8 Beskrivelse, oversettelsen av vurderingsskalaen (*for lett → lett* osv.), og siste setning i FR-20 («“Likte” i briefen tilsvarer fornøydhet 4–5») (~35 ord) | MOVE til §9, der det samme allerede står (rad 3 og 4). La §4.8 og FR-20 vise til §9 | Avvikene fra briefen hører hjemme i §9. Kravene blir rene krav. Sparer ca. 30 ord |
| structure | NFR-2, andre kulepunkt, gjentar listen over tilstander fra §6 «Tilstander som skal designes» (~35 ord) | CONDENSE NFR-2 til: «Alle tilstander i §6 viser enten et turforslag eller en forklaring med neste steg.» | Listen finnes da bare ett sted. Sparer ca. 25 ord |
| structure | §7.1, listen over områder med FR-intervall (~45 ord), gjentar overskriftene i §4 | CONDENSE: behold bare prioriteringen. Den nevner allerede alle FR-ene | Fjerner en ren innholdsfortegnelse uten ny informasjon. Sparer ca. 45 ord |
| structure | Endringsloggen: rad 0.6 står før rad 0.5 | MOVE rad 0.5 over rad 0.6 | Versjonene får riktig kronologisk rekkefølge. 0 ord |
| structure | §3 Begreper (393 ord) står før §4 Funksjoner | PRESERVE | Begrepene kommer før de brukes. Det trengs for LLM-arbeidsflytene og for presise FR-er (FR-1 og FR-2 bygger på *Tur* og *Tur-retur*) |
| structure | §1 Visjon, siste avsnitt («På sikt …»), og §7.2 «Senere fase» | PRESERVE | Gir sensor retning og avgrensning. Teksten er kort og overlapper ikke |
| structure | §9 Endringer fra product brief (407 ord, den største seksjonen) | PRESERVE plasseringen bakerst | §0 lover at avvikene står her. Seksjonen er en levende logg som sensor trenger for å følge sporingen fra briefen, og den forstyrrer ikke kravlesingen |

**Oppsummering:** 12 rader (9 endringer og 3 PRESERVE). Hvis alle endringene godtas, blir dokumentet ca. 190–200 ord kortere (ca. 4 % av 4 535 ord). Det ble ikke oppgitt noe lengdemål. Ingen av forslagene går ut over forståelsen. Det viktigste med forslagene er bedre rekkefølge (scope først, kjerneflyten definert i §3, MET-føringene synlige for arkitekturen) og ett fast skjema for sporing, ikke å gjøre dokumentet kortere.
