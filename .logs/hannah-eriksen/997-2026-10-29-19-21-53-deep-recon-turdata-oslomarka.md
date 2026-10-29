# Deep recon: turdata for Oslomarka

## 2026-10-29 kl. 19:21 — Hannah Eriksen

### Oppgave
Kjørte `bmad-help` for å finne neste steg (svaret var PRD). Brukeren valgte å kjøre en teknisk deep recon på turdata først, for å avklare om en kuratert database med 20–30 nybegynnerturer i Oslomarka kan bygges fra åpne data, og hvilken kilde som bør brukes.

### Plan
- `bmad-deep-recon`, type `technical`, form *select*, preset `standard`, validering `normal`.
- Dimensjoner: D1 datakilder og dekning, D2 uthenting, format og høydemeter, D3 lisens, D4 tidsestimat.
- Runde 1 med tre parallelle agenter. Runde 2 med egne målinger: nedlasting av Turrutebasen for Oslo og Bærum, og telling i OSM via Overpass. I tillegg en ny gjennomgang av ODbL og Naismith.
- Kontroll av kildehenvisningene i to trinn, først maskinelt, deretter en uavhengig agent.

### Resultat
- Rapport: `_bmad-output/planning-artifacts/research/technical-turdata-oslomarka-2026-10-29/research.md`, med HTML-versjonen `research-briefing.html`. Grunnlagsdata ligger i `digests/` og prosesslogg i `.memlog.md`.
- **Valg:** Kartverkets Turrutebasen (CC BY 4.0) som kilde for rutegeometri og navn. Den fikk 3,65 i den vektede matrisen, mot 2,90 for OSM. OSM er reserve for turer som mangler. Høydemeter hentes fra Kartverkets høyde-API, som er gratis og ikke krever nøkkel.
- **Hovedfunn:** Ingen kilde har brukbar vanskelighetsgrad for Oslomarka. Gradering finnes på bare 11,7 % av fotrute-segmentene i Oslo, og ingen av OSM-relasjonene har det. Gruppen må derfor kuratere og gradere turene selv etter en fast regel. ut.no har ikke noe åpent API.
- Påstandene i rapporten: 3 verifisert, 4 uverifisert og 1 motbevist. Den motbeviste gjaldt GML i EPSG:4326, som ikke finnes. Kontrollagenten fant 7 avvik i kildehenvisningene, og alle er rettet i rapporten.
- `_bmad-output/` er ikke committet.
- Briefen er oppdatert etterpå: `docs/product-brief-your-next-adventure-no.md` (The Solution og Scope). Rutelinjene kommer nå fra Kartverkets Turrutebasen med OSM som supplement, høydemeter fra Kartverkets høydedata, og vanskelighetsgrad settes etter faste regler. Den engelske briefen er ikke endret, fordi den er en eldre versjon. Endringen i briefen er ikke committet.

### Åpne punkter
- Avklar UT/DNTs grenseverdier for gradering (≤5 km / ≤300 hm for grønn) i nettleser. hjelp.ut.no returnerte 403.
- Dekningen av Turrutebasen i resten av Oslomarka (Akershus, fylke 32) er ikke målt.
- `bmad-review` (structure, prose) er ikke kjørt på rapporten. Det er valgfri polering.
- Neste påkrevde BMAD-steg er `bmad-prd`.
