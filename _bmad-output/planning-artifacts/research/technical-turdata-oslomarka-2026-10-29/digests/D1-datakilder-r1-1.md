# D1 – Data sources & coverage (round 1, digest 1)

Accessed for all sources: 2026-10-29. Tool calls used: 14 of 15.

## Findings

1. **Claim:** Kartverket "Tur- og friluftsruter" (Turrutebasen) is a nationwide dataset of hiking routes, ski trails, bicycle routes, other routes and outdoor-recreation facilities. Its metadata record lists status "On going", weekly maintenance, revision date 2026-10-23 and metadata date 2026-10-28. It is actively maintained as of this month.
   - Source: https://geonorge.no/geonetworktest/srv/api/records/d1422d17-6d95-4ef1-96ab-8af31744dd63 (Geonorge GeoNetwork record. Note: this is the "geonetworktest" endpoint, because the production kartkatalog page did not render for the fetch tool.)
   - Publisher: Kartverket / Geonorge · pub_date: revision 2026-10-23 · confidence: medium-high (the record is on a test host, but its dates are fresh) · class: version / api-status

2. **Claim:** Turrutebasen is open data. The record says "noLimitations / noConditionsApply" (Åpne data). It is distributed as FGDB, GML, **GPX**, PostGIS and SOSI, by county, by municipality or as national files, via nedlasting.geonorge.no (ATOM feeds and the Geonorge download API). The record also lists a separate WFS record (882e96f2-…).
   - Source: same as #1. WFS record: https://geonorge.no/geonetworktest/srv/api/records/882e96f2-94c9-4119-91ed-692a09adbcf9 (not fetched)
   - Publisher: Kartverket · pub_date: 2026-10 · confidence: high · class: api-status / license

3. **Claim:** Turrutebasen has attributes that suit beginners. They include **gradering** (difficulty in Merkehåndbok colours: G = easy/green, B = medium/blue, R = demanding/red, S = expert/black, I = not graded), **merking** (JA/NEI, whether the route is physically marked), **rutetype**, **rutebetydning**, **underlagstype** (surface), **vedlikeholdsansvarlig** (maintainer) and **rutenummer**. Route information sits in nested FotruteInfo blocks, and one segment can belong to up to 8 routes. Per the OSM wiki analysis, **gradering is often empty**.
   - Sources: https://wiki.openstreetmap.org/wiki/No:Turrutebasen (OSM wiki, last edited 2026-08-25) and the metadata in #1
   - Publisher: OSM Norway community / Kartverket · pub_date: 2026-08-25 · confidence: medium-high (the "often empty" claim was measured in Valdres and Gudbrandsdalen, not Oslo) · class: attributes

4. **Claim:** Turrutebasen geometry is mostly derived from FKB-TraktorvegSti (64–76% of segments in the areas analysed). It also draws on N50 and digitised hiking maps, and content is largely reported by clubs, associations and individuals via "Rett i kartet". Quality depends on the capture method.
   - Sources: OSM wiki No:Turrutebasen (2026-08-25). Kartverket product sheet: https://register.geonorge.no/data/documents/produktark_turrutebasen_v5_turrutebasen-2_.pdf (only the search snippet was read, and the sheet is undated, so it may be old)
   - Publisher: OSM wiki / Kartverket · confidence: medium · class: coverage / quality

5. **Claim:** Kartverket confirmed in 2014, and renewed in 2021 regarding CC BY 4.0 vs ODbL, that its open datasets, including Turrutebasen, may be used in OSM with `source=Kartverket`. No geometry import into OSM has been approved. The community recommends attribute enrichment only, and the mapping of `gradering` to an OSM tag is unresolved.
   - Source: https://wiki.openstreetmap.org/wiki/No:Turrutebasen
   - Publisher: OSM wiki · pub_date: 2026-08-25 · confidence: high · class: license / attributes

6. **Claim:** **Oslo/Oslomarka coverage in Turrutebasen was not verified.** The OSM wiki coverage comparison (76% Valdres / 70% Gudbrandsdalen within 25 m of OSM paths) does not mention Oslo.
   - Source: OSM wiki No:Turrutebasen · confidence: high (that the gap exists) · class: coverage

7. **Claim:** In OSM, Oslomarka is described as having blue-marked routes, signposted junctions, nature and culture trails, good coverage of near-urban paths, ski trails with grooming info, and huts and shelters. Oslo kommune's signposted trails are included, but **Bærum's trails were "not yet entered"**. The page does not mention hiking route relations, sac_scale, trail_visibility or osmc:symbol for Oslomarka. **The page was last edited 2018-04-06 and is stale**, so it is no evidence of current state.
   - Source: https://wiki.openstreetmap.org/wiki/No:Oslomarka
   - Publisher: OSM wiki · pub_date: 2018-04-06 (FLAG: >12 months) · confidence: low for the current state · class: coverage

8. **Claim:** Oslo kommune released turveier (urban walking trails) and cycle data under PDDL/NLOD, and the turveier were "grovimport" (rough-imported) into OSM in 2011. Bymiljøetaten has an ArcGIS open-data hub (oslokommune-bym.opendata.arcgis.com), but no current turvei/Marka trail layer was confirmed there.
   - Sources: https://wiki.openstreetmap.org/wiki/Cycle_network_in_Oslo and https://community.openstreetmap.org/t/tillatelse-fra-oslo-kommune-bymiljoetaten/84603/1 (both undated or old in the snippets)
   - Publisher: OSM wiki / OSM forum · confidence: low-medium · class: coverage / other-sources

9. **Claim:** In OSM, `sac_scale` is designed for mountain trails. Community members warn against tagging easy or paved paths with it, so it is a weak beginner signal in lowland forest like Marka. Path segments for routes should be tied together by route relations.
   - Source: https://community.openstreetmap.org/t/another-sac-scale-poll-t5-or-t6-or-beyond-scale/121826/6
   - Publisher: OSM Community Forum · pub_date: not captured (thread ~2024–25) · confidence: medium · class: attributes

10. **Claim:** DNT's Nasjonal Turbase, the backend of ut.no, was historically an open REST API (JSON/GeoJSON, CC BY-SA, API key required). It now looks dormant. The GitHub org "Turbasen" was last updated 2020-03-27, with the Developer repo at 2018-04-04 and the site repo at 2018-06-07; one repo is archived. nasjonalturbase.no refused the connection on 2026-10-29. **No current public ut.no API or open export was found.** ut.no help pages cover contributor publishing only (post@ut.no).
    - Sources: https://github.com/Turbasen ; https://pypi.org/project/turbasen/1.0.3/ ; https://speakerdeck.com/starefossen/apen-tur-og-friluftsdata (2015, FLAG: old) ; https://hjelp.ut.no/hc/no/articles/14703333053970-Om-turm%C3%A5l-og-steder-i-UT-admin
    - Publisher: DNT / community · pub_date: 2015–2020 · confidence: medium (it is absence of evidence, plus a dead host and stale repos; there was no official deprecation notice) · class: api-status

11. **Claim:** Skiforeningen manages about 2,200 km of ski trails, mainly inside the Markagrensa (2024). Its trail map and grooming data (iMarka / skisporet-type service, map built by Geodata) are winter-focused. No open-data download or licence for its summer trails was found.
    - Source: https://www.skiforeningen.no/globalassets/2024_2025/horinger/2024/2024-horingssvar-endringer-i-markaloven.pdf
    - Publisher: Skiforeningen · pub_date: 2024 · confidence: medium · class: other-sources

## Interim assessment (for the decision; not a conclusion)

Turrutebasen is the only candidate confirmed this run as **open + current (2026-10) + GPX/GML download + difficulty (gradering) and marking (merking) attributes**. Its risks are that gradering is often empty and that Oslo coverage is unverified. OSM is the likely best source for **geometry density** in Marka (licence ODbL, which needs attribution and share-alike on the database), but this run found no current evidence of Oslomarka route-relation or difficulty tagging. ut.no/Nasjonal Turbase appears unusable as an API.

## Leads worth chasing

- Download the Turrutebasen GPX/GML for Oslo (0301) and the Bærum/Nordre Follo/Lillestrøm/Nittedal municipalities, and count routes, the fraction with gradering ≠ empty/I, and the fraction with merking=JA. This is the decisive coverage test.
- Use Overpass to query Oslomarka's bbox for `route=hiking` relations, `operator`/`network` values (DNT Oslo og Omegn, Skiforeningen), `sac_scale` and `trail_visibility` counts. Also check waymarkedtrails.org for Oslo.
- Read the current Turrutebasen product specification (SOSI 4.x/5.x version on Geonorge register) for exact gradering and rutetype code lists.
- Check whether the Turrutebasen WFS (record 882e96f2-…) is live, since it would allow bbox queries without a bulk download.
- Look at the Oslo kommune BYM ArcGIS hub for a "turveier / skilting i marka" layer, and at Oslo og Omland Friluftsråd for a skilting/tursti dataset.
- Find any official DNT statement on Nasjonal Turbase shutdown or successor (e.g., DNT tech blog, GitHub Turistforeningen org).
- The production Geonorge kartkatalog page (kartkatalog.geonorge.no/metadata/…/d1422d17-…) did not render, so the dates should be re-verified there.

## Looked for but could not find

- Any current (2025–2026) official ut.no/DNT public API documentation or open data export.
- An official deprecation notice for Nasjonal Turbase.
- An Oslo/Oslomarka-specific coverage or quality figure for Turrutebasen.
- Recent (≤12 months) evidence on OSM hiking-route-relation coverage and difficulty tagging in Oslomarka.
- A Skiforeningen or Friluftsråd open-data download for summer trails (Marka sommerkart).
- An Oslo kommune open dataset of Marka trails with difficulty attributes.
