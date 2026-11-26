---
title: 'Story 6.5: Kartfargene er målt mot ekte kartfliser'
type: 'chore'
created: '2026-11-26'
status: 'done'
baseline_commit: 'ce6bafcdaf01e53f985891300243393223bcd65b'
route: 'dispatch'
review_loop_iteration: 1
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-6-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Kontrastmålene for kartlaget i `DESIGN.md` bygger på antatte flisfarger (skog `#CDE6B4`, vann `#A8D3EE`) og OSM-stedfortredere. Det er ikke vist at rutelinjen, startmarkøren og fokusringen er tydelige på Kartverkets topo-fliser (UX-DR35, NFR-4, NFR-7, UX-DR1).

**Approach:** Last ned ekte fliser fra AR-10-adressen for skog, myr, vann og bebyggelse, på minst to steder og to zoomnivåer (13 og 15). Les pikselfargene med et lite skript som bare bruker Python-stdlib. Regn ut WCAG-kontrast for hvert token mot hver flate, og dokumenter resultatet i `docs/kartfarger.md` med tabell og skjermbilder. Oppdater så Kontrastmål i `DESIGN.md` og det åpne punktet i `EXPERIENCE.md`.

**Forhåndsmåling (2026-11-26, 16 fliser):** `map-route` har 3,07–7,6 og `map-marker-start` 3,49–8,7 mot alle flatene, også mot den mørkeste skyggeleggingen (1. persentil). Markøren har 8,7 mot hvit «S». `map-focus-ring` har 4,5 mot sin hvite ytre kant, men bare 1,8–2,8 rett mot skog.

**Beslutninger (Hannah, 2026-11-26):**
1. **Fokusringen (1A):**
   - Den hvite ytre kanten godtas. Ringen ligger alltid mellom hvit knapp eller flate og 3 px hvit ytre kant, så nabofargene er hvite (WCAG 1.4.11).
   - Tabellen viser både ringen mot den hvite kanten (kravet, 4,5) og ringen rett mot hver flate (til informasjon). Fotnoten forklarer dette.
   - `map-focus-ring` endres ikke.
2. **Måleskriptet (2A):**
   - `skript/mal_kartfarger.py` committes. Det bruker bare stdlib og kan gjenta målingen.
   - Testene dekker luminans og kontrast, og PNG-lesing med en PNG laget i minnet, uten nettverk.
3. **Spec-en beholdes hel** (ca. 2400 tokens).
4. **Rutefargen (B, under implementering):** målingen viste at `map-route` `#6A3D9A` har 2,998:1 mot den mørkeste skogen (`#9BA95F`, Østmarka z15).
   - `map-route` endres til `#673A97`. Den er fortsatt plommelilla og gir 3,13 mot `#9BA95F` og 8,0 mot hvit.
   - Endringen gjøres bare i `DESIGN.md` (frontmatter, Kartlag, Kontrastmål) og i `tokens.css`.
   - Skjermbilder før og etter i skog, myr, vann og bebyggelse ligger i `docs/skjermbilder/` og i PR-en.
   - Hannah godkjenner som produkteier i PR-en.
5. **Fokusringen på kartflaten (A, etter gjennomgangen):** gjennomgangen viste at ringen på `.kart-flate` bare har hvit kant på utsiden. Rett innenfor ligger flisene (1,75 mot mørkeste skog), så begrunnelsen i 1A holdt bare for kontrollene og lenkene.
   - `.kart .kart-flate:focus-visible::after` i `turforslag/static/css/side.css` får et hvitt bånd også på innsiden av ringen (`inset box-shadow` i `--map-overlay-surface`, uten nye farger). Da ligger ringen mellom hvitt på begge sider overalt på kartet, og 1A gjelder slik den står.
   - Arbeidet som allerede er gjort, beholdes. Bare fokusringen og patchene fra gjennomgangen legges til.
   - Fokusen på kartet sjekkes i Chrome.

## Boundaries & Constraints

**Always:**
- Flisadresser oppgis som `z/x/y`, selv om URL-en har `{z}/{y}/{x}`.
- Hver flate oppgis med en typisk farge (vanligste piksel) og den mørkeste skyggevarianten (1. persentil av luminans). Kravet gjelder den mørkeste.
- Myr er hvit flate med blå skravur; flaten er den hvite.
- Bebyggelse er boligfelt (`#EAD3BF`-tonen) og grå bebygd flate.
- Symboler er ikke flater. Det gjelder blå bygninger, røde og svarte veier og stier og tekst. De vurderes visuelt i skjermbildene.
- Skjermbildene viser «© Kartverket».
- Commits, docs og PR viser til UX-DR35, NFR-4, NFR-7 og UX-DR1.

**Never:**
- ingen ny pakke i `requirements*.txt`, og ingen endring i CSP, `kart.js` eller maler;
- ingen nettverkskall i tester;
- endrer et token seg, skjer det bare i `DESIGN.md` (frontmatter, Kartlag, Kontrastmål) og `turforslag/static/css/tokens.css`;
- `--focus-ring` utenfor kartet endres ikke;
- ingen `uv run`.

</frozen-after-approval>

## Code Map

- `_bmad-output/planning-artifacts/ux-designs/ux-G81-eriksen-2026-11-06/DESIGN.md` -- :82–87 map-tokens i frontmatter, :439–446 Kartlag, :476–481 Kontrastmål (rad 477 route, 478 marker, 479 fokusring, fotnote 481). Det finnes ingen rad for markør mot «S».
- `…/EXPERIENCE.md:492` -- «Kartfliser og målinger», merket «Delvis løst 2026-11-08». Konvensjonen er `**Løst YYYY-MM-DD:** …` i Punkt-cella og `–` i Blokkerer. Lenken til docs er `../../../../docs/kartfarger.md`.
- `turforslag/static/css/tokens.css:74-79` -- `--map-*` (små hex). Bare `--map-route` endres, til `#673a97` (beslutning 4).
- `turforslag/static/kart.js:10-15` -- flis-URL og `MAKS_ZOOM = 18`. `fitBounds` har ingen `maxZoom`, så turene får zoom 11–16. Kun til lesing.
- `turforslag/static/css/side.css:755-778, 899-920` -- fokusring med hvit kant, rute (5 px på 9 px hvit) og markør. Bare `.kart .kart-flate:focus-visible::after` endres: hvitt bånd på innsiden (beslutning 5).
- `tests/web/test_grunnoppsett.py:318-360, 451-462` -- tokentester, uendret.
- `skript/bygg_turdatabase.py` -- modell for stilen i et skript i `skript/` (docstring, `main`, norsk). Testmønsteret finner du i `tests/` (se hvordan `bygg_turdatabase` testes).
- `docs/kontroll-turdatabasen.md` -- modell for stilen: «Slik er … gjort», tabell, «Kontrollert <dato> av Claude. Hannah bekrefter i PR-en.»
- `data/turer.geojson` -- turområdene.
- Målesteder (lat, lon):
  - vann: Sognsvann (59.9725, 10.730) og Nøklevann (59.885, 10.870);
  - skog: Nordmarka (60.010, 10.690) og Østmarka (59.893, 10.895);
  - myr: ved Fuglemyrhytta (59.985, 10.697) og Lillomarka (59.985, 10.850);
  - bebyggelse: Grorud (59.9614, 10.882) og Gjettum (59.9105, 10.5277).
- Prototype: `C:/Users/hanna/.claude/jobs/82d45a23/tmp/flisfarger.py` -- PNG-leser med stdlib (filtre 0–4, RGB/RGBA/palett), luminans og kontrast. Den er grunnlaget for `skript/mal_kartfarger.py`.

## Tasks & Acceptance

**Execution:**
- [x] `skript/mal_kartfarger.py` + test i `tests/` -- skriptet henter flisene til en midlertidig mappe og skriver en markdown-tabell. Testene dekker luminans og kontrast mot kjente par (hvit/svart = 21, `#6A3D9A`/hvit ≈ 7,6) og dekoding av en PNG laget i minnet -- gjør målingen etterprøvbar.
- [x] `docs/kartfarger.md` -- metode, flistabell (`z/x/y`, sted, flate, typisk og mørkeste farge), kontrasttabell (token × flate, mørkeste og typisk), markør mot «S», vurderingen av om ruten skiller seg fra stier, veier og vann, og «Målt 2026-11-26 av Claude. Hannah bekrefter i PR-en.» -- dokumentasjon for UX-DR35.
- [x] `docs/skjermbilder/6-5-*.png` -- minst ruten mot sti/vei og ruten langs vann, med «© Kartverket» synlig (hovedøkten tar dem i Chrome) -- NFR-7.
- [x] `DESIGN.md` -- Kontrastmål rad 477–479 med målte flater (skog, myr, vann, bebyggelse, hvit kant), ny verdi for markør mot «S» = 8,7 og ny fotnote om dato, metode, lenke og hvorfor fokusringen måles mot sin hvite kant (1A). Frontmatter og Kartlag får ny `map-route` (`#673A97`), og ingen andre verdier endres.
- [x] `EXPERIENCE.md:492` -- `**Løst 2026-11-26:**` med lenke til `docs/kartfarger.md`, Blokkerer `–`.

**Acceptance Criteria:**
- Gitt AR-10-flisene, når de er målt, så har `docs/kartfarger.md` minst 2 steder × 2 zoomnivåer for hver av skog, myr, vann og bebyggelse, med `z/x/y` og hex, og ingen `requirements*.txt` er endret.
- Gitt de målte fargene, når kontrasten regnes ut, så står `map-route`, `map-marker-start` og `map-focus-ring` mot hver flate i tabellen, og alle krav i Kontrastmål er oppfylt (route og markør ≥ 3:1 mot hver flate, markør ≥ 4,5:1 mot «S», fokusring ≥ 3:1 mot sin hvite kant), og bare `map-route` er endret (til `#673A97`).
- Gitt dokumentasjonen, når den åpnes, så har skjermbildene «© Kartverket», og vurderingen av ruten mot stier, veier og vann står der.
- Gitt `DESIGN.md` og `EXPERIENCE.md`, når de leses, så står ingen antatte eller OSM-verdier igjen i Kontrastmål, og det åpne punktet er merket løst med dato og lenke.

## Implementation Notes

## Spec Change Log

- **Gjennomgang 1 (2026-11-26), funn 1, intent_gap:** begrunnelsen for 1A («nabofargene er hvite») var feil for `.kart-flate`, fordi flisene ligger rett innenfor ringen. Hannah valgte A (beslutning 5): et hvitt bånd på innsiden i `side.css`, og arbeidet beholdes. Det avverger at fokusringen på kartflaten ligger mot fliser med 1,75:1 mens docs sier at den bare grenser mot hvitt.
  - Endret: den frosne blokken (beslutning 5) og Code Map (`side.css` skal endres).
  - **KEEP:** målingen, `skript/mal_kartfarger.py`, testene, tabellene i `docs/kartfarger.md`, de fire skjermbildene, `map-route` `#673A97` og `EXPERIENCE.md`.

## Review Triage Log

Første gjennomgang (2026-11-26). BH = Blind Hunter, EC = Edge Case Hunter, VG = Verification Gap.

| # | Funn (lag) | Verdikt | Begrunnelse | Rute |
|---|---|---|---|---|
| 1 | Fokusringen på `.kart-flate` har flisene på innsiden, ikke hvitt; 1A-begrunnelsen «nabofargene er hvite» holder ikke der (BH, EC) | medium | `side.css:759-768`: `::after` har 3 px hvit `border` (0–3 px) og ringen med `outline-offset: -6px` (3–6 px). Innenfor 6 px er det fliser (1,75 mot mørkeste skog). På `.kartlag`, lenker og knapper (`:770-777`) stemmer det: hvit knapp inni og 6 px hvit `box-shadow` utenfor. | intent_gap |
| 2 | DESIGN-fotnoten sier «den kraftigste skyggeleggingen», men 1. persentil er ikke den mørkeste (`#92A056` finnes, 2,81 mot ny rute) (BH) | low | Stemmer: ca. 1 % av skogpikslene på Østmarka z15 er mørkere. Metoden (1. persentil) står i den frosne blokken; det er bare ordlyden som overdriver. | patch |
| 3 | DESIGN.md runder opp (4,47→4,5, 8,68→8,7, 3,35→3,4) mot regelen «rundet ned» i docs (BH, EC) | low | Stemmer for kartradene. | patch |
| 4 | Ingen test kjører `krav_oppfylt` på de ekte verdiene i `tokens.css` mot de målte flatene; tilbakestilling til `#6a3d9a` fanges ikke (VG, BH) | medium | VG viste at `[]` blir `['map-route mot skog: 2.998']` ved tilbakestilling, uten at noen test feiler. | patch |
| 5 | `oppsummer` er ikke testet (VG) | low | Ingen test i `tests/` kaller den; `min`→`max` ville passert. | patch |
| 6 | Exit-koden fra `main()` er ikke testet (VG) | low | Ingen test kaller `main`. | patch |
| 7 | En flate som ikke finnes på noen flis hoppes over, og skriptet gir likevel exit 0 (VG, EC) | low | `mal_alle` logger bare en advarsel, og `krav_oppfylt` løkker over de flatene som finnes. | patch |
| 8 | «Typisk» for boligfelt avgjøres av rekkefølgen når alle flisene har ulik typisk farge (BH, EC) | low | Alle fire er unike, så `most_common(1)` velger den første. | patch |
| 9 | Docs sier at tabellene er skrevet av skriptet, men overskrift og vannflate-raden i symboltabellen er ulike (VG, BH) | low | Stemmer. | patch |
| 10 | Godkjenningen står som gitt («godkjente i PR-en») før PR-en finnes (BH) | low | Stemmer, både i `docs/kartfarger.md` og i DESIGN-fotnoten. | patch |
| 11 | Fargesyn: rød sti mot rute (1,52) skilles bare med fargetone for protanoper (BH) | low | Ruten skilles også av hvit kant, bredde og heltrukket mot stiplet linje, men docs nevner ikke dette for fargesyn. | patch |
| 12 | Myr: 17 piksler, og 1. persentil blir da minimum (BH, EC) | low | Docs nevner 17 piksler, men ikke at persentilen da er den mørkeste pikselen. | patch |
| 13 | Korrupt flis (`zlib.error`/`struct.error`) eller manglende token gir traceback i stedet for loggmelding (BH, EC) | false | Det er et utviklerskript som feiler høylytt; det gir ikke feil resultat. | avvist |
| 14 | Zoom 16 er ikke målt (BH) | false | Den frosne blokken velger zoom 13 og 15, og AC krever minst to nivåer. | avvist |
| 15 | Sprint-status er `in-progress`, ikke `review` (BH) | false | Steg 5 i bmad-build setter status. | avvist |
| 16 | Mockups og `epic-6-context.md` har fortsatt `#6A3D9A` (BH) | false | Storyen sier at tokenet bare endres i DESIGN.md og `tokens.css` (UX-DR1). | avvist |
| 17 | `MAKS_SKYGGE` kan stille droppe dypere skygge (EC) | false | Den kraftigste skyggen i flisene er 77 < 96, så ingen piksler droppes. | avvist |
| 18 | `persentil == 1.0` gir IndexError (EC) | false | `PERSENTIL` er en konstant på 0,01; ingen kaller med 1,0. | avvist |
| 19 | Flyttallsfeil kan gi 2,99 i tabellen mens kravet holder (EC) | false | `krav_oppfylt` bruker samme flyttall mot `< 3.0`, så tabell og exit-kode følger hverandre i praksis; ingen målt verdi ligger på grensen. | avvist |
| 20 | To målesteder på samme flis (EC) | false | Alle åtte stedene gir ulike fliser (se flistabellen). | avvist |
| 21 | Skjermbildene er ikke i diffen (VG) | false | De er utenfor diffen med vilje (binære) og committes med resten. | avvist |
| 22 | Testene bruker den gamle `#6A3D9A` som `PLOMME` (BH) | false | Det er en testvektor for kontrastberegningen, ikke tokenet; funn 4 dekker selve tokenet. | avvist |

Andre gjennomgang (2026-11-26, etter beslutning 5 og patchene).

| # | Funn (lag) | Verdikt | Begrunnelse | Rute |
|---|---|---|---|---|
| 23 | `krav_oppfylt` har ingen negativ test for markør mot flatene, markør mot «S» og fokusring mot hvit (VG) | low | VG viste at sletting av hver sjekk lar alle 29 testene passere. | patch |
| 24 | `main()` er bare testet på feilstiene, ikke på exit 0 (BH) | low | Stemmer. | patch |
| 25 | Docs forklarer ikke hvorfor ruten måles mot flisene, mens fokusringen måles mot hvitt (BH) | low | Storyens AC krever at `map-route` har minst 3:1 mot alle flatene og den hvite kanten. Fokusringen følger 1A og 5. Docs sier ikke dette. | patch |
| 26 | Docstringen til `mal_alle` sier at flisene kan åpnes etterpå, men `main` sletter dem (BH) | low | `TemporaryDirectory` sletter mappa. | patch |
| 27 | DESIGN-fotnoten viser til beslutning 1A, 4 og 5 uten lenke (BH) | low | Beslutningene står i spec-fila, som committes. Det mangler bare en lenke. | patch |
| 28 | Rute under 3:1 mot de mørkeste ~1 % av skogpikslene (BH) | carried | Samme som rad 2, og ordlyden er rettet. | (patch, ferdig) |
| 29 | Korrupt eller avkortet flis gir traceback (BH, EC) | carried | Samme som rad 13. | avvist |
| 30 | `persentil` ≥ 1 eller < 0 (EC) | carried | Samme som rad 18. | avvist |
| 31 | Skjermbildene er ikke i diffen (BH, EC) | carried | Samme som rad 21. | avvist |
| 32 | Testene bruker den gamle fargen som testvektor (BH, VG) | carried | Samme som rad 22. Testen med de ekte tokenene fanger en tilbakestilling (VG regnet 2,9976). | avvist |
| 33 | «Myr» kan være annen hvit flate (BH) | low | Det har ingen følge: hvitt mot alle tokenene er ≥ 6,6, langt over kravet. Små utvalg er nevnt i docs (rad 12). | avvist |
| 34 | Symbolfargene er hardkodet, mens docs sier «lest ut av de samme flisene» (BH) | false | Fargene er plukket fra de nedlastede flisene, så påstanden stemmer. | avvist |
| 35 | Det 9 px hvite båndet kan dekke kontrollene (BH) | false | Leaflet-kontrollene har 10 px marg. Chrome-sjekken viste at zoom, kreditering og målestokk er fri. | avvist |
| 36 | Overlay-raden i DESIGN endret (14,8 / 8,6), selv om den ikke er regnet ut av skriptet (BH, EC) | false | Det er nedrunding av 14,87 og 8,69 (kontrollregnet), i tråd med regelen. Verdiene er riktige. | avvist |
| 37 | EXPERIENCE er merket «Løst» før godkjenningen i PR-en (BH) | false | Hannah valgte B (beslutning 4) i økten. PR-en bekrefter det. | avvist |
| 38 | Testen er avhengig av rekkefølgen (`adresser[4]`, hardkodet 16) (BH, EC) | low | Testene er deterministiske, og MALESTEDER endres sjelden. Fiksen gir mer kode. | avvist |
| 39 | Uavgjort om vanligste farge på én flis (EC) | low | Det påvirker bare kolonnen «typisk», ikke kravet. | avvist |

## Design Notes

Kravet bruker den mørkeste skyggevarianten (1. persentil), fordi topo-flisene har skyggelegging som gjør skogen 10–20 % mørkere i bratte lier. En «typisk» farge alene ville overvurdere kontrasten. Zoom 13 og 15 dekker `fitBounds`-spennet for turene (11–16).

## Verification

**Commands:**
- `venv/Scripts/python.exe manage.py test` -- expected: alle grønne (2 hoppet over lokalt)
- `venv/Scripts/python.exe -m ruff check . && venv/Scripts/python.exe -m ruff format --check .` -- expected: rent
- `git diff --stat ce6bafcdaf01e53f985891300243393223bcd65b -- requirements.txt requirements-dev.txt turforslag/static/kart.js turforslag/templates` -- expected: tomt
- Chrome: fokus på kartflaten med Tab -- expected: ringen har hvitt på begge sider

**Manual checks:**
- Les `docs/kartfarger.md` mot AC-ene. Åpne skjermbildene og se at «© Kartverket» er synlig.
