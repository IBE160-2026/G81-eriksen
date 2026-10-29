# Digest D3/D4 – Licensing & terms, hiking-time formulas (round 1, researcher 1)

Accessed for all: 2026-10-29. Budget used: 15 tool calls, ~11 sources.

## D3 – Licensing & terms

### F1. OSM attribution wording and placement
- **Claim:** Attribution must name "OpenStreetMap" and make clear the data is available under ODbL. Linking "OpenStreetMap" to openstreetmap.org/copyright is one accepted way to do this. "© OpenStreetMap contributors" and "Map data from OpenStreetMap" are both acceptable. On interactive maps it goes in a map corner (lower-right is traditional) or next to the map. It may collapse after interaction or after 5 s, but must stay findable (for example via an info button). It must be legible (WCAG recommended).
- **Source:** https://osmfoundation.org/wiki/Licence/Attribution_Guidelines
- **Publisher:** OSMF (board-adopted 2021-06-25)
- **pub_date:** last edited 2026-09-10
- **Confidence:** high
- **Class:** license

### F2. Produced Work vs. database (ODbL)
- **Claim:** The test is purpose. Output "intended for the extraction of the original data" is a database, otherwise it is a Produced Work. Raster images and rendered maps are usually Produced Works, and "Database dumps are usually not Produced Works." The page has no example covering route geometries. *Interpretation (not stated by OSMF):* the team's curated DB (route geometry + length/elevation), if published or served as GeoJSON that can be extracted, is likely a Derivative Database. A Leaflet map showing it is a Produced Work, which needs attribution only.
- **Source:** https://osmfoundation.org/wiki/Licence/Community_Guidelines/Produced_Work_-_Guideline
- **Publisher:** OSMF (endorsed 2014-06-06)
- **pub_date:** last edited 2016-07-31
- **Confidence:** high (the definition) / medium (applying it to this case)
- **Class:** license

### F3. Collective vs. Derivative Database
- **Claim:** OSM and non-OSM data stay independent (Collective Database, share-alike only on the OSM part) when, for a given data type within a regional cut, the data is either all OSM or all non-OSM. The guideline also lists other conditions, such as the datasets not referencing each other. A publicly used Derivative Database "can trigger share-alike with respect to the non-OSM data." The guideline does not decide whether adding properties such as length, elevation or difficulty to OSM geometries makes a derivative.
- **Source:** https://osmfoundation.org/wiki/Licence/Community_Guidelines/Collective_Database_Guideline_Guideline
- **Publisher:** OSMF (endorsed 2016-06-17)
- **pub_date:** last edited 2016-07-31
- **Confidence:** medium
- **Class:** license

### F4. Substantial extract threshold
- **Claim:** Fewer than 100 Features is treated as not Substantial if the extraction is one-off and not repeated for the same or a similar project. More than 100 is OK only if the selection is non-systematic and based on the user's own qualitative criteria. Ways count as Features, but nodes inside ways do not. "Repeated small extractions" count as one big extraction. 20–30 hand-picked routes (possibly a few ways each) are plausibly under the threshold, but this is not confirmed. The guideline does not say which ODbL clauses the threshold switches off. The reading that an insubstantial extract escapes share-alike is unverified this run (ODbL §4.4/§6 were not fetched).
- **Source:** https://osmfoundation.org/wiki/Licence/Community_Guidelines/Substantial_-_Guideline
- **Publisher:** OSMF (endorsed 2014-06-06)
- **pub_date:** not captured
- **Confidence:** medium
- **Class:** license

### F5. Turrutebasen ("Tur- og friluftsruter") licence metadata
- **Claim:** Geonorge metadata (UUID d1422d17-6d95-4ef1-96ab-8af31744dd63) gives:
  - Access: "Åpne data".
  - Use constraint: "Lisens", linked to the INSPIRE code "No conditions apply to access and use". No named licence appears in the metadata.
  - Owner: Kartverket.
  - Updated weekly. Formats: FGDB, GML, GPX, PostGIS, SOSI, plus WMS and WFS.
  - Dataset updated 2026-10-23.

  This conflicts with Kartverket's general rule (F6), which puts free products under CC BY 4.0. Resolution: Kartverket's terms page is the more specific and more recent licence statement (2026-07-21), so treat the dataset as CC BY 4.0 and attribute "© Kartverket". Attributing costs nothing even if no conditions apply.
- **Source:** https://kartkatalog.geonorge.no/api/getdata/d1422d17-6d95-4ef1-96ab-8af31744dd63
- **Publisher:** Geonorge / Kartverket
- **pub_date:** metadata 2026-10-29
- **Confidence:** high (metadata content) / medium (which licence actually governs)
- **Class:** license

### F6. Kartverket licence and attribution for free products
- **Claim:**
  - Free Kartverket products are under CC BY 4.0.
  - Required attribution is "© Kartverket", with a link to the website where possible.
  - Screenshots from norgeskart.no must credit "©norgeskart.no".
  - For WMS and cache services at zoom 12–20, the data comes from Geovekst. Copying or other use "beyond normal use" needs permission from the rights holders (post@kartverket.no).
  - The page sets no numeric request limits. Technical limits are stated per service.
- **Source:** https://www.kartverket.no/api-og-data/vilkar-for-bruk
- **Publisher:** Kartverket
- **pub_date:** 2026-07-21
- **Confidence:** high
- **Class:** license / usage-policy

### F7. Kartverket topographic WMTS (cache.kartverket.no)
- **Claim:** The topographic WMTS cache is listed as CC BY 4.0. Capabilities: https://cache.kartverket.no/v1/wmts/1.0.0/WMTSCapabilities.xml. Geonorge notices (May 2025, now marked retired) describe a URL change to the `/v1/service?...` form. Check the current endpoint before building.
- **Sources:**
  - https://data.norge.no/en/data-services/e3454491-066a-3276-a482-f63069728021 (data.norge.no, updated around March 2026)
  - https://register.geonorge.no/varsler/topografisk-norgeskart-wmts-cache/63a7a1b9-e9c0-49d8-ac58-4657d66e8123
- **Publisher:** Digdir/data.norge.no; Geonorge
- **pub_date:** 2025–2026
- **Confidence:** medium (secondary catalogue; terms text not seen on the service itself)
- **Class:** usage-policy / license

### F8. OSM standard tile server (tile.openstreetmap.org) policy
- **Claim:**
  - Show attribution clearly on the map. Do not hide it behind toggles or off-screen.
  - Use HTTPS.
  - Send a distinct, stable User-Agent naming the app. Library defaults and browser impersonation are not allowed. For websites, keep the Referer intact and avoid restrictive Referrer-Policy settings.
  - Honour cache headers, or cache tiles for at least 7 days. Do not bypass caches.
  - No bulk downloading, pre-seeding, prefetching of tiles the user isn't viewing, or offline use.
  - No numeric limits. Access "may [be] block[ed] without notice" if usage degrades the service. "Availability is best-effort: there is no SLA."

  A small student app using Leaflet in the browser fits the policy if it keeps Leaflet's default attribution and does not set a no-referrer policy.
- **Source:** https://operations.osmfoundation.org/policies/tiles/
- **Publisher:** OSMF Operations Working Group
- **pub_date:** not shown
- **Confidence:** high
- **Class:** usage-policy

## D4 – Hiking-time estimate

### F9. Naismith, Langmuir and Tobler compared
- **Claim:**
  - **Naismith:** base speed 5 km/h on the flat. Its known flaw is that predicted speed does not change on descents.
  - **Langmuir:** corrections to Naismith that subtract time on moderate descents and add time on steep ones. It implies about 12 km/h on shallow descents and a sudden jump down to 3 km/h, which the paper calls "very unrealistic".
  - **Tobler:** W = 6·exp(−3.5·|S + 0.05|) km/h, where S is the slope as dz/dx. It gives about 5 km/h on the flat and peaks at about 6 km/h on a roughly 3° descent; the paper says that peak may be unrealistic. Tobler is now more popular for computed (not hand-calculated) estimates.
  - **Off-path:** a factor of about 0.6 is used for off-path travel.
  - The ascent term of Naismith (1 h per 600 m) was **not verified from a source this run** and remains an unverified belief.
- **Source:** https://arxiv.org/pdf/2303.16065v6 (arXiv paper comparing the walking-speed functions)
- **Publisher:** arXiv preprint
- **pub_date:** 2023 (v6 later)
- **Confidence:** medium
- **Class:** formula

### F10. Swiss Wanderwege formula and rules of thumb
- **Claim:**
  - **Official Swiss formula:** official signpost times (introduced 2006) use a polynomial in slope (terms up to S¹⁵) multiplied by horizontal distance. Times are adjusted manually above about 40% slope.
  - **Leistungskilometer:** 1 km horizontal plus 1 km per 100 m ascent (and per 400 m descent, i.e. ×2.5). Count 10–15 min per Leistungskilometer depending on fitness.
  - **BFU / Schweizer Wanderwege rule of thumb:** 15 min per km, plus 15 min per 100 m ascent, plus 15 min per 200 m descent. Example: 6 km with ±800 m takes 4.5 h. This is notably more conservative than Naismith (4 km/h; about 1 h per 400 m ascent), which suits beginners.
- **Sources:**
  - https://www.beobachter.ch/ausfluge-freizeit/wanderwegweiser-die-gelben-zeiten (Beobachter, secondary)
  - https://www.burgenverein-untervaz.ch/_files/ugd/405a1e_8def2d28fe7240799700626cb2eb6ea0.pdf
  - https://www.chemie.de/lexikon/Leistungskilometer.html (Wikipedia-derived)
  - https://www.srf.ch/static/radio/modules/data/attachments/3.010_PB_Bergwandern_de.pdf (BFU leaflet)
- **pub_date:** various
- **Confidence:** medium (BFU leaflet is primary-ish; polynomial coefficients not verified)
- **Class:** formula

### F11. DNT reference pace
- **Claim:** A DNT document on grading group trips states an average marching pace of "ca. 3 km i timen" for group trips in summer and winter. No DNT ascent rule was found.
- **Source:** https://www.dnt.no/contentassets/eb277e829991484c8d212f6127df351c/graderingen-av-fellesturer.pdf
- **Publisher:** DNT
- **pub_date:** not captured
- **Confidence:** medium (seen via search snippet, not fetched)
- **Class:** formula / guidance

### Synthesis for the decision (inference, not a sourced claim)
For beginners, a deterministic Swiss/BFU-style rule (4 km/h + 15 min/100 m up + 15 min/200 m down) or Naismith scaled toward DNT's 3 km/h group pace is more conservative than raw Naismith or Tobler, both of which assume about 5 km/h. Each candidate formula is a pure function of length and ascent (plus descent), so all are compatible with the "no AI" requirement.

## Leads worth chasing
- The ODbL 1.0 legal text (§4.4 share-alike, §4.6, §6) at opendatacommons.org. Use it to confirm whether an insubstantial extract is exempt and what "Publicly Use" a Derivative Database means.
- The OSM wiki page "Legal FAQ" or the "Horizontal Layers" guideline, which covers combining OSM geometries with own attributes.
- Kartverket's per-service technical limits for cache.kartverket.no, and the current endpoint (the v1/wmts vs v1/service confusion).
- The original Naismith (1892, SMC Journal) and Langmuir (*Mountaincraft and Leadership*) sources for the exact 600 m/h ascent term and the descent corrections.
- Tobler 1993, "Three presentations on geographical analysis and modeling" (NCGIA Technical Report 93-1), as the original source.
- The Schweizer Wanderwege official "Berechnung der Wanderzeit" document with the polynomial coefficients.
- How ut.no/DNT computes "beregnet gåtid", for example on ut.no help pages or via the Nasjonal turbase API docs.
- The bioRxiv preprint (10.1101/188417), which fits a model to Wikiloc tracks and compares it with Naismith, Tobler and Langmuir. It could give evidence on bias.

## Looked for but could not find
- An explicit DNT/ut.no rule-of-thumb formula for hiking time that includes ascent.
- Evidence on whether these formulas under- or overestimate times for novices. No study was retrieved this run. The belief that Naismith underestimates for unfit or novice walkers is unverified.
- A named licence (CC BY 4.0 / NLOD) in the Turrutebasen metadata itself. It only says "No conditions apply".
- A last-updated date on the OSM tile usage policy page.
- A Kartverket terms page specific to cache.kartverket.no, with request limits.
