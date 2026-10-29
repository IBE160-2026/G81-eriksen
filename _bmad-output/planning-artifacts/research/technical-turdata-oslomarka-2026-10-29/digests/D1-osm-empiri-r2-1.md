# D1 – OSM empirical check, Oslomarka (round 2, lead 1)

Accessed 2026-10-29. Endpoint: `https://overpass-api.de/api/interpreter` (POST, UA `IBE160-student-research/1.0`). Publisher: OpenStreetMap contributors (ODbL), served by Overpass API 0.7.62.11. Data timestamps (`timestamp_osm_base`): 2026-10-29T18:08:36Z to 18:13:36Z. BBox for all queries: `(59.85,10.40,60.20,11.05)`, which includes urban Oslo/Bærum. Raw files are in `C:\Users\hanna\AppData\Local\Temp\claude\C--IBE160\1fe98eaa-5fce-48bd-854f-0eb0393a8a7e\scratchpad\overpass\` (q1, q2, q3, q4, q6 json).

## Queries used
- **Q1:** `[out:json][timeout:60];(relation["route"~"^(hiking|foot)$"](bbox););out tags;`
- **Q2 (counts):** `way["highway"~"^(path|footway|track)$"](bbox)->.w; .w out count; way.w["sac_scale"];out count; …` with the same pattern for trail_visibility, osmc:symbol, trailblazed, marked_trail, name, surface, informal, ski, piste:type, and per highway value.
- **Q3:** `nwr["name"~"Sognsvann|Vettakoll|Kolsås|Ullevålseter|Ullevålsseter",i](bbox);out tags;`
- **Q4:** `nwr["name"~"Kols..?s|Ullev..?ls?eter|rundt"](bbox);out tags;`. Regex patterns with non-ASCII characters (å) returned 0 hits when sent from Git Bash curl on Windows. This looks like an encoding problem, so I swapped `å` for `.`.
- **Q6:** `… way.w["trail_visibility"];out tags; way.w["trailblazed"];out tags; node["information"="guidepost"](bbox);out count;`
- **Q5** (sac_scale values with `out tags`) failed with HTTP 502 three times, so I don't have the sac_scale value distribution.

## Findings

| # | Claim | Source | Confidence | Class |
|---|---|---|---|---|
| 1 | 307 route relations intersect the bbox. 268 are `route=hiking`: 158 rwn, 39 with no network, 29 lwn, 8 nwn. 73 are `route=foot`: 70 lwn, 3 with no network. | Q1, ts 18:08:36Z | High | measured |
| 2 | 158 of the relations are DNT segments (operator "Den Norske Turistforening", network rwn, `ref` OSL1 to OSL217). They have **no `name`**, only `from`/`to` (e.g. OSL1 Losby→Røyrivannskoia), `colour` #6cbff1 and a dead-looking `website` (www2.turistforeningen.no/trail.php?tr_code=…). They are network legs between junctions, not curated hikes. | Q1 | High | measured |
| 3 | Only 153 of the 307 relations have a `name`. Only **8 have `distance`**, **25 have `roundtrip`**, **5 have `description`**, **0 have `wikidata`** and 18 have `osmc:symbol`. No relation carries a difficulty or duration tag. | Q1, key frequency | High | measured |
| 4 | Most `foot`/lwn relations are urban "Turvei" corridors: about 58 from Oslo kommune Bymiljøetaten (refs A1 to E24) and about 20 from Bærum kommune. These are city green-way links, not forest hikes. | Q1 | High | measured |
| 5 | Named relations that could plausibly be beginner hikes: Sognsvann natursti (2015333, roundtrip=yes), Bogstadvannet rundt (2910680), Ulsrudvann rundt (9713193, DNT), Brennarunden (7899395, DNT), Losbyrunden lille 5.6 km and store 9.8 km, Kobberhaugtjern natursti (DNT Barnas Turlag), Bogstad / Ulsrudvann / Kirkeby / Årvollåsen / Ammerud / Bånkallia natursti, Maridalen kultur- og natursti, Skjærsjøelva kulturminnesti, Sæteren gård natur-/eventyrsti, Glittre-runden, Skoklefallrunden, Maridalsrunden (21 km). That is about 20 to 25 candidates. Most have no distance and none has difficulty. | Q1 | High (existence), Medium (beginner suitability is my judgment) | measured + interpretation |
| 6 | 76,189 highway=path/footway/track ways in the bbox: 42,656 footway, 28,629 path, 4,904 track. | Q2, ts 18:09:36Z | High | measured |
| 7 | Attribute coverage on those 76,189 ways: `surface` 45,264 (59%), `trail_visibility` 8,249 (10.8%), `trailblazed` 3,922 (5.1%; 3,906 are "yes"), `name` 1,999 (2.6%), `sac_scale` **894 (1.2%)**, `informal` 458, `marked_trail` 6, **`osmc:symbol` 0** on ways (it lives on relations), `piste:type` 4,410. | Q2 | High | measured |
| 8 | trail_visibility values: intermediate 3,820, good 1,931, bad 1,740, excellent 987, horrible 265, no 54, plus a few odd values. | Q6, ts 18:11:36Z | High | measured |
| 9 | 2,897 `information=guidepost` nodes in the bbox. Spot checks show DNT Oslo og Omegn guideposts with grid refs (e.g. "Ullevålseter" NM954537, "Sognsvann P" NM969492, "Kolsåstoppen nordre NØ" NM851446). This is a dense, well-maintained signpost layer. | Q6 count; Q3/Q4 tags | High (count), Medium (share that is DNT: not measured) | measured |
| 10 | Spot checks. **Sognsvann rundt:** no relation by that name. The loop exists as "Sognsvann natursti" (route=hiking, roundtrip) and "Sognsvann natursti (rullestol)" (route=wheelchair, 2023998). **Vettakollen:** peak nodes only (419 m; nodes 301173327 and 7874571394, apparently a duplicate) plus guideposts, no route relation. **Kolsåstoppen:** peaks Nordre 379 m and Søndre 342 m, a nature reserve and DNT guideposts, no route relation. **Ullevålseter:** cafe node with website, 7 DNT guideposts, no route relation. So 3 of the 4 classic beginner hikes exist only as a path network plus POIs. A curated route would have to be drawn by the team. | Q3, Q4, Q1 | High | measured |
| 11 | Waymarked Trails (hiking) shows the same data. For a Nordmarka-south bbox (EPSG:3857 1180000,8398700,1202250,8417300) the API returned 50 results (the limit): 2 NAT (Jotunheimstien, Rondanestien) and 48 REG, all unnamed OSLxxx refs. The API bbox has to be in EPSG:3857; a WGS84 bbox returned an empty result. | https://hiking.waymarkedtrails.org/api/v1/list/by_area?bbox=… | High | measured |

## Bottom line (interpretation)
OSM is strong in Oslomarka as **network geometry and POIs**: about 28.6k paths, DNT marked-trail segments, about 2.9k guideposts, and peaks with elevation. It is weak as a **curated hike catalogue**: few named round trips, almost no distance, difficulty or description tags, and sac_scale on about 1% of ways. A database of 20 to 30 beginner hikes is feasible if the team composes routes over OSM paths (e.g. with BRouter/GraphHopper) and writes its own name, distance, difficulty and description fields. Copying OSM route relations directly would not give a usable catalogue.

## Leads worth chasing
- DNT relation `website` tags point at www2.turistforeningen.no. Check whether that is dead and whether UT.no / Nasjonal turbase has an open replacement API with curated "turforslag".
- Kartverket / Geonorge "Tur- og friluftsruter" dataset (official Norwegian trail data, likely NLOD). Compare its coverage and attributes, which may include difficulty and grading.
- Oslo kommune Bymiljøetaten natursti / turvei data, probably on Oslo open data.
- Retry Q5 (sac_scale value distribution) off-peak, or use a smaller bbox (Nordmarka only) so urban footways don't dilute the percentages.
- Measure coverage on a forest-only bbox or Marka-boundary polygon. The "markagrensen" polygon may be in OSM as a boundary relation.

## Looked for but could not find
- No route relation named "Sognsvann rundt", and no route relation for Vettakollen, Kolsåstoppen or Ullevålseter.
- No difficulty or grading tag on any relation. No `wikidata` on any hiking/foot relation.
- No sac_scale value distribution (Overpass returned 502 three times).
- No `osmc:symbol` on any path/footway/track way.
