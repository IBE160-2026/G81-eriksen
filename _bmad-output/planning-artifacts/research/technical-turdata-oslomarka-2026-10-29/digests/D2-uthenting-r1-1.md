# D2 – Extraction, format, elevation (round 1, agent 1)

Accessed for all sources: 2026-10-29. Tool calls used: 15 of 15.

## Findings

### OSM extraction (Q1)

1. **Claim:** The public Overpass main instance (overpass-api.de) asks one-off users to stay under about 10,000 queries/day, 1 GB/day of downloads and about 10 min/day of processing time, with regular use about 100x lower. Clients should send a User-Agent or Referer, avoid running scripts in parallel, and wait 30 s after an HTTP 429/406. Commercial use should go to other servers. The wiki warns the server is overloaded and "do not expect high reliability". For about 30 routes this is far below the limits.
   - Source: https://wiki.openstreetmap.org/wiki/Overpass_API | OSM Wiki | last edited 2026-10-24 | confidence: high | class: api-usage
2. **Claim:** Overpass API outputs XML (default), JSON and CSV natively. GeoJSON and GPX are not native and need a converter such as osmtogeojson. The default timeout is 180 s and can be raised.
   - Source: same as #1 | confidence: high | class: format
3. **Claim:** The overpass turbo web UI exports GeoJSON, GPX (for GPX it advises adding `center` so features become points, which suits waypoints, not route lines), raw OSM XML/JSON, a direct interpreter link, JOSM and a GitHub gist. No KML is mentioned, and there is no specific guidance on exporting route relations.
   - Source: https://wiki.openstreetmap.org/wiki/Overpass_turbo | OSM Wiki | last edited 2026-10-25 | confidence: high | class: tooling
4. **Claim:** Waymarked Trails (hiking.waymarkedtrails.org) lets you select an OSM route relation and download it as GPX. Caveats: the exported GPX often has no elevation even though the site shows a profile. Route members are not reordered, so messy relations can give out-of-order or gapped tracks. Some trails are missing.
   - Source: https://wiki.openstreetmap.org/wiki/Waymarked_Trails and forum threads such as https://community.openstreetmap.org/t/export-route-to-gpx-file/82732 and https://lists.openstreetmap.org/pipermail/talk-it/2020-September/070788.html | OSM Wiki / OSM community | dates vary, forum posts 2013–2020 (OLD, behaviour may have changed) | confidence: medium | class: tooling

### Kartverket Turrutebasen (Q2)

5. **Claim:** The dataset formerly called "Nasjonal database for tur- og friluftsruter" is now listed as **Turrutebasen** (Kartverket, made with Geovekst, the municipalities and DNT). It covers foot trails (fotruter), ski trails, cycle routes, other routes and facilities. Kartkatalog uuid: d1422d17-6d95-4ef1-96ab-8af31744dd63.
   - Source: https://kartkatalog.geonorge.no/api/getdata/d1422d17-6d95-4ef1-96ab-8af31744dd63 ; https://wiki.openstreetmap.org/wiki/No:Turrutebasen | Geonorge/Kartverket ; OSM Wiki | metadata updated 2026-10-29 | confidence: high | class: format
6. **Claim:** Turrutebasen download formats are **FGDB, GML, GPX, PostGIS (dump), SOSI**. **GeoJSON is not offered.** CRS options: EPSG 25832 (default), 25833, 25835, 3035, 4258 and **4326 (WGS84)**. The data is split by county, by municipality, or as one national file. Downloads go through the Geonorge cart or the nedlasting.geonorge.no API (Atom feeds per format). The data was updated 2026-10-23 and is maintained weekly. Access is open data. Choosing EPSG:4326 at download avoids reprojection for Leaflet. EPSG:4258 (ETRS89) is practically the same as WGS84 at web-map precision (unverified belief, not checked this run).
   - Source: https://kartkatalog.geonorge.no/api/getdata/d1422d17-6d95-4ef1-96ab-8af31744dd63 | Geonorge/Kartverket | 2026-10-29 | confidence: high | class: format
7. **Claim:** The metadata lists a WMS (https://wms.geonorge.no/skwms1/wms.friluftsruter2) but **no WFS or OGC API endpoint**. A search snippet from data.norge.no mentions a WFS at wfs.geonorge.no ("turogfriluftsruter", GML output), but this could not be confirmed and may be an old service.
   - Source: kartkatalog (as #6) ; https://data.norge.no/en/data-services/23121ee5-e389-3069-8021-d3eca08070e9 | Geonorge ; data.norge.no | confidence: medium (WMS) / low (WFS) | class: api-usage
8. **Claim:** Licence: the OSM wiki reports Kartverket confirmed in 2021 that Turrutebasen may be used in OSM. Geonorge lists the data as open; other Kartverket open data is typically CC BY 4.0, but the exact licence string was not checked this run.
   - Source: https://wiki.openstreetmap.org/wiki/No:Turrutebasen | OSM Wiki | confidence: medium | class: format

### Elevation (Q3)

9. **Claim:** Kartverket runs a free, **keyless** "Åpent API for høyde- og dybdedata" at `https://ws.geonorge.no/hoydedata/v1` (OpenAPI 3.0.3, API version 1.1.1). `GET /punkt` takes `koordsys` (EPSG, e.g. 4258 or 25833), `nord`/`ost` or `punkter=[[e,n],...]` (**max 50 points per request**) and optional `geojson=true`. It returns z in metres above sea level, plus the data source and terrain type. Uptime is not guaranteed per data source. Breaking changes are announced at least 3 months ahead via Geonorge-Tjenestevarsler. A 300-vertex route needs about 6 requests.
   - Source: https://ws.geonorge.no/hoydedata/v1/openapi.json | Kartverket | fetched 2026-10-29 | confidence: high | class: elevation
10. **Claim:** Data sources behind the elevation API: **dtm1 (1 m digital terrain model)**, dom1 (1 m surface model), hoydekurver (interpolated contours), innsjohoyde (lake heights) and dybdekurver. `/punkt` picks the "best available" source. Oslomarka is expected to have DTM1 laser coverage (unverified belief). Use the DTM (terrain), not the DOM (surface, which includes trees).
   - Source: https://ws.geonorge.no/hoydedata/v1/datakilder | Kartverket | 2026-10-29 | confidence: high | class: elevation
11. **Claim:** Kartverket also offers an Elevation WPS with elevationJSON, elevationXML and elevationChart (PNG) profile processes. Its metadata describes 1 m grid interpolation in FKB areas and 20 m elsewhere. The exact endpoint and parameters were not found.
   - Source: https://geonorge.no/geonetworktest/srv/api/records/92299496-8836-4fc1-b685-6d14bd0eb749 ; https://data.norge.no/en/data-services/17072b71-0723-3b36-8433-3a8dcabae40a | Geonorge (test catalogue) | date unknown | confidence: low–medium | class: elevation
12. **Claim:** Raw elevation sums inflate gain. GPS Visualizer's example: a loop with about 1080 m of true gain gave 2326 m from raw GPS and 1434 m from DEM data. A threshold of 1–2 m gets closer, and about 10 m worked best on that track. AlpineQuest shows +2535 m (no noise reduction) vs +1717 m (medium) vs +1634 m (strong). visugpx is reported to default to a 10 m threshold. No standard threshold exists, so tune it per dataset. With 1 m DTM sampling the main risk is micro-relief and sampling noise rather than GPS error, so a threshold or moving-average smoothing is still needed.
   - Source: https://gpsvisualizer.com/tutorials/elevation_gain.php ; https://alpinequest.net/en/help/v2/landmarks/statistics ; https://www.alpinequest.net/forum/viewtopic.php?p=4188 | GPS Visualizer / AlpineQuest (tool vendors, practitioner docs) | dates unknown, likely older than 6 months | confidence: medium | class: elevation
13. **Claim:** OpenTopoData's API supports `interpolation=nearest|bilinear|cubic` (bilinear by default). A public test API exists at api.opentopodata.org, but its limits and dataset list were not on the fetched page (the datasets page returned 404). For Norway, the Kartverket API (#9) is the higher-resolution and more relevant choice.
   - Source: https://www.opentopodata.org/api/ | OpenTopoData | confidence: medium | class: elevation

### Storage and length (Q4)

14. **Claim:** `turf.length(geojson, {units})` (Turf 7.4.0 docs) takes a LineString/MultiLineString Feature and returns km by default. The docs do not state the method or CRS. Turf assumes WGS84 lon/lat (unverified belief, not stated on the page), so lengths must be computed on EPSG:4326 data, or computed in UTM (25833) before reprojecting.
   - Source: https://turfjs.org/docs/api/length | Turf.js | v7.4.0 | confidence: medium | class: tooling
15. **Claim (storage):** No evidence was retrieved this run comparing PostGIS with plain GeoJSON for small apps. Unverified belief: for 20–30 static routes, a single GeoJSON FeatureCollection (or a JSON/JSONB column) with precomputed length and gain properties is enough, and PostGIS adds value only if spatial queries are needed. Turrutebasen does ship a PostGIS dump option (#6).
   - Source: none (inference) | confidence: low | class: format

## Suggested simplest workflow (synthesis, partly inferential)
1. Pick about 30 routes. Either download Turrutebasen for Oslo plus the surrounding Marka municipalities (GPX or GML in EPSG:4326) and filter for fotrute, or query OSM route relations (`route=hiking`) in overpass turbo and export to GeoJSON, or use Waymarked Trails GPX for each relation.
2. Convert to GeoJSON (ogr2ogr, QGIS, or osmtogeojson / togeojson), then merge and clean the line ordering in QGIS.
3. Compute length with turf.length (WGS84) or in UTM33.
4. Densify or sample points about every 10–25 m, call `ws.geonorge.no/hoydedata/v1/punkt` in batches of 50, smooth the result or apply a 2–5 m threshold, and sum the positive deltas. Sanity-check the result against UT.no or Waymarked Trails profiles.
5. Store the results as a static GeoJSON FeatureCollection with properties (name, length_km, gain_m, source, licence attribution).

## Leads worth chasing
- Check the Turrutebasen licence string (CC BY 4.0?) and the attribution text, and whether a WFS/OGC API Features endpoint exists (wfs.geonorge.no "turogfriluftsruter").
- Check whether Turrutebasen attributes carry a route name or DNT marking for Oslomarka (product specification PDF: register.geonorge.no ... produktspesifikasjon-kv-tur-og-friluftsruter-2-5-1).
- Look for any documented rate limit or fair-use policy on ws.geonorge.no/hoydedata (none in the OpenAPI spec).
- Check the OSM coverage of `route=hiking` relations in Oslomarka (count via overpass turbo) against Turrutebasen.
- BRouter / GraphHopper public instances for building routes between points (not researched; budget exhausted).
- Geofabrik Norway extract plus osmium (not researched this run; overkill for 30 routes, unverified).
- The Kartverket Elevation WPS endpoint and parameters (may be legacy).

## Looked for but could not find
- A WFS or OGC API endpoint listed in the current Turrutebasen metadata (only WMS is listed).
- GeoJSON as a Turrutebasen download format (not offered).
- Usage limits for ws.geonorge.no/hoydedata and for api.opentopodata.org.
- The calculation method used by turf.length (not stated in the docs).
- An authoritative recommendation on an elevation-gain threshold (sources say it depends on the data).
- Evidence-based guidance on PostGIS vs GeoJSON for small apps.
