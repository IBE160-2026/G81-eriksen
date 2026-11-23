# Spike før Story 1.5: Turrutebasen (WFS) og høyde-API-et

Kjørt 2026-11-23 med `urllib.request` fra standardbiblioteket og en generisk User-Agent. Skriptene og de rå svarene ligger i denne mappa.

## WFS: `https://wfs.geonorge.no/skwms1/wfs.turogfriluftsruter`

- `GetFeature` med `typeNames=app:Fotrute` og `srsName=EPSG:4326` gir GML 3.2.1 i UTF-8. `gml:posList` har rekkefølgen **lon lat**, og koordinatene har 6 desimaler.
- **`app:rutenummer` ligger ikke rett under `Fotrute`.** Filteret må bruke stien `app:fotruteInfo/app:FotruteInfo/app:rutenummer` (FES 2.0 `PropertyIsEqualTo`, med `namespaces=xmlns(app,…)`). Med `app:rutenummer` alene svarer tjenesten 400 `InvalidParameterValue`.
- **Ett rutenummer gir mange usorterte segmenter.** `F_01812_03` (Frognervassdraget-langs) ga 22 features, 4357 m til sammen:
  - Segmenter **deles mellom ruter**. Ett segment kan ha flere `FotruteInfo` (for eksempel `F_01812_01`, `_02` og `_03`, og til og med `hed1` Rondanestien).
  - Nettverket har **2 komponenter, 6 ender og 2 forgreininger**. Det er altså ikke én sti som kan kobles ende mot ende.
  - Endepunktene stemmer **eksakt** (ingen forskjell med toleranse 0 m og 1 m). Med 5 m smelter flere noder sammen og gir falske forgreininger.
- Punktavstanden langs segmentene er median 8,9 m og maks 55 m.

**Konsekvens for specen:** AC-en «kobler endepunkter i rekkefølgen i kilde-ID-en» holder ikke. Byggeskriptet må velge en sti gjennom nettverket, og kurateringslista må si nok til å gjøre valget entydig.

## Høyde-API-et: `https://ws.geonorge.no/hoydedata/v1/punkt`

- `koordsys=4258` og `koordsys=4326` godtas begge og gir like høyder. Punktene sendes som `[[lon, lat], …]` i parameteren `punkter`, med `geojson=false`.
- Maks 50 punkter per kall er bekreftet: 51 punkter gir 422 med en norsk feilmelding.
- Datakilden er `dtm1` (terrengmodell med 1 m oppløsning). `terreng` kan være `null`.

## Støy (lengste segment, 1754 m, nettofall 51,9 m)

| Punktavstand | Terskel 0 m | 2 m | 5 m | 10 m |
|---|---|---|---|---|
| 10 m (177 punkter) | opp 20 / ned 72 | 7 / 58 | 0 / 51 | 0 / 43 |
| 25 m (72 punkter) | 15 / 67 | 6 / 56 | 0 / 50 | 0 / 50 |

- Uten filter blir stigningen blåst opp med 15–20 m på en sti som går jevnt nedover langs en elv.
- Terskel 5 m treffer nettofallet nesten nøyaktig.
- 10 m teller for lite når punktene ligger tett. Spike-algoritmen dropper i tillegg den siste rest-differansen, og det må byggeskriptet ta med.
- **Anbefaling:** 25 m punktavstand (halvparten så mange kall) og terskel 5 m. Begge skal stå i `data/README`.
