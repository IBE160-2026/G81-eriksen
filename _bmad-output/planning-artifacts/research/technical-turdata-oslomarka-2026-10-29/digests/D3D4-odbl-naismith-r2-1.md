# D3/D4 digest: ODbL, Naismith/Tobler, and the ut.no time estimate (round 2, run 1)

Accessed 2026-10-29. 15 tool calls. Classes: P = primary, S = secondary, G = official guideline, T = tertiary/search snippet.

## Q1: ODbL 1.0 and the OSMF guidelines

| # | Claim | Source | Publisher | Pub date | Conf. | Class |
|---|---|---|---|---|---|---|
| 1 | Under ODbL, "Publicly" means to persons other than You or entities under Your control (>50% ownership or power to direct). A public web app is therefore "Publicly Use". §4.5 says internal use within an organisation is not public use. | https://opendatacommons.org/licenses/odbl/1-0/ | Open Data Commons | 2009 (v1.0) | High | P |
| 2 | §4.4 share-alike: a Derivative Database that is Publicly Used must be licensed under ODbL, a later similar version, or a compatible licence. A Produced Work made from a Derivative Database and Publicly Used also triggers this. | same | ODC | 2009 | High | P |
| 3 | §4.5: share-alike does not apply to Collective Databases, though ODbL still covers the OSM part inside them. Making a Produced Work does not by itself create a Derivative Database (§4.5b). | same | ODC | 2009 | High | P |
| 4 | §4.6: anyone who Publicly Uses a Derivative Database, or a Produced Work from one, must offer recipients the whole Derivative Database in machine-readable form, or a file of the changes. It must be free online. | same | ODC | 2009 | High | P |
| 5 | §6.2: lawful users may extract and reuse insubstantial parts of the Contents for any purpose, explicitly including building a Derivative Database, subject to other rights. Repeated or systematic extraction of insubstantial parts can add up to a Substantial part. "Substantial" is judged by quantity, quality, or both. So an insubstantial extract falls outside the licence's share-alike. | same | ODC | 2009 | High (paraphrased by the fetch tool; check the verbatim text before quoting) | P |
| 6 | The OSMF Substantial Guideline treats an extraction as insubstantial if it has fewer than 100 Features (a way counts as one feature). More than 100 can qualify if the extraction is non-systematic and uses your own selection criteria. The extraction must be "one-off and not repeated over time for the same or a similar project". "We regard repeated small extractions as one big extraction!" Board-endorsed 2014-06-06. | https://osmfoundation.org/wiki/Licence/Community_Guidelines/Substantial_-_Guideline | OSM Foundation | 2014-06-06 (edited 2018-02-27) | High | G |
| 7 | Implication for 20–30 hand-curated hiking routes: about 20–30 ways or relations, chosen by the team's own criteria, extracted once, is well under the 100-feature threshold. That is likely insubstantial, so share-alike would not attach. Attribution to OSM is still good practice. Risk: "systematic extraction of all [X] within an area" is not insubstantial, so "all marked trails in Oslomarka" would not qualify. | inference from #5–6 | — | — | Medium | inference |
| 8 | The Horizontal Map Layers Guideline (endorsed 2014-06-06) covers only rendered 2D maps (Produced Works). Share-alike is decided per Feature Type: if a feature type is entirely non-OSM, it is not shared-alike. Data that improves or corrects OSM, or is built by comparing against OSM, must be shared. It does NOT address adding your own attributes to OSM geometries. | https://osmfoundation.org/wiki/Licence/Community_Guidelines/Horizontal_Map_Layers_-_Guideline | OSMF | 2014-06-06 | High | G |
| 9 | The Collective Database Guideline (endorsed 2016-06-17) is the relevant one for own attributes. OSM and non-OSM data combined by reference (key or ID join) stay a Collective Database only when, for each data type in a regional cut, the data is all-OSM or all-non-OSM. Adding or replacing a property on an OSM feature qualifies if that property comes wholly from OSM or wholly from non-OSM data. So team-computed length, elevation gain, difficulty, and time attributes from non-OSM sources (e.g. Kartverket DEM, own computation) joined to OSM geometries can plausibly stay a Collective Database. | https://osmfoundation.org/wiki/Licence/Community_Guidelines/Collective_Database_Guideline_Guideline | OSMF | 2016-06-17 | Medium-High | G |

## Q2: The formulas

| # | Claim | Source | Publisher | Pub date | Conf. | Class |
|---|---|---|---|---|---|---|
| 10 | Naismith's rule original: W. W. Naismith, "Excursions", Scottish Mountaineering Club Journal vol. 2 no. 3, p. 136 (1892). It is about 1 h per 3 miles plus 1 h per 2000 ft of ascent. The SI restatement is t(min) = 12·d(km) + 10·ascent(m)/100, which is 5 km/h plus 1 h per 600 m. | https://www.biorxiv.org/content/10.1101/188417v2.full | Pharoah, bioRxiv | 2017-09-14 | High (secondary citation of the 1892 original; the original was not retrieved) | S |
| 11 | Langmuir corrections (Langmuir 1984, Mountaincraft and Leadership): base 5 km/h. For descents of 5–12°, subtract 10 min per 300 m. For descents steeper than 12°, add 10 min per 300 m. The preprint's own wording of the thresholds is somewhat inconsistent. | same | Pharoah | 2017 | Medium | S |
| 12 | Tobler original: W. Tobler, Three Presentations on Geographical Analysis and Modeling, NCGIA Technical Report 93-1, Santa Barbara, Feb 1993. The walking function was "estimated from empirical data given by Imhof (1950, pp 217-220)". In the HTML copy the formula appears only as an image. The commonly cited form is v = 6·exp(−3.5·abs(S+0.05)) km/h (stated in Pharoah). | https://escholarship.org/uc/item/05r820mz ; https://geodyssey.neocities.org/papers/tobler93 | UC eScholarship / NCGIA | 1993-02 | High (reference); Medium (formula text, not read verbatim in the original) | P |

## Q3: Do the formulas fit real or novice walkers?

| # | Claim | Source | Publisher | Pub date | Conf. | Class |
|---|---|---|---|---|---|---|
| 13 | Pharoah (Wikiloc and blog GPS tracks, 193 tracks, about 2,970 km): Naismith performs "reasonably well" for total duration. Tobler and Langmuir are weaker. The data "likely reflect enthusiastic hikers", not casual walkers, and the tracks were filtered to 10–25 miles and >1,500 ft of gain. So the study is NOT representative of beginners on short Oslomarka routes. | https://www.biorxiv.org/content/10.1101/188417v2.full | bioRxiv (not peer-reviewed) | 2017 | Medium | S |
| 14 | Wood et al. (Univ. Edinburgh) used 7,636 tracks and about 88,000 km from Hikr.org and OSM GPS traces in England and Wales. Naismith overestimates ascent time and underestimates descent time. Its mean point-speed error is 26.4% (RMSE 1.27 km/h); Tobler's is 26.2%. For whole routes all models were off by 13.5–15.5% on average. Models describe an "average individual". Fitness, age, group size and weather are not modelled, and novices are not discussed. | https://arxiv.org/abs/2303.16065 (read via ar5iv) | arXiv preprint | 2023 | Medium-High | S |
| 15 | Neither study isolates novice or recreational walkers. Both are self-selected GPS uploaders, likely fitter than average. Hypothesis (unverified): formulas fitted to these data underestimate time for beginners, families and groups with breaks, so a safety margin or a "pauses not included" note is advisable. | inference | — | — | Low (unverified) | inference |

## Q4: ut.no / DNT time estimate

| # | Claim | Source | Publisher | Pub date | Conf. | Class |
|---|---|---|---|---|---|---|
| 16 | UT's quality checklist for turforslag requires that "Gradering og tidsbruk følger nasjonale standarder". This suggests the author sets time and grade against a national standard rather than a published UT formula. Seen only as a search snippet, because hjelp.ut.no returns 403 to fetches. | https://hjelp.ut.no/hc/no/articles/15697246353938-Sjekklister-for-kvalitetssjekk-av-innhold | UT.no / DNT | n.d. | Low-Medium | T |
| 17 | National grading as seen in a snippet from hjelp.ut.no: green (enkel) is for beginners and usually ≤5 km and ≤300 m ascent. Blue is usually ≤10 km and ≤600 m. Red is "krevende". | hjelp.ut.no (exact article unclear: 14650428708754 / 14658022079378 / 360012690380) | UT.no | n.d. | Low-Medium | T |

## Leads worth chasing
- The verbatim ODbL §6.2 text and the Produced Work notice (§4.3), to confirm the paraphrase in #5.
- The OSM wiki "Legal FAQ" and "Open Database License/Use Cases" pages (not fetched because of budget).
- The national standard for trail marking and grading (Merkehåndboka, Norsk Friluftsliv/DNT) may define both grading and how tidsbruk is estimated. Search "Merkehåndboka gradering tidsbruk".
- Open the hjelp.ut.no articles in a real browser, since they 403 for WebFetch.
- Scarf (2008) on the Naismith distance–climb equivalence, and the Langmuir 1984 primary text.
- Andrew Wood's PhD thesis (Edinburgh) for fitness and individual variation.

## Looked for but could not find
- The primary 1892 SMC Journal text, which is not online in the results.
- Any documented ut.no/DNT formula for "beregnet tid". None is public, and it appears to be author-set against the national standard (unconfirmed).
- Studies specifically on novice or recreational walkers vs Naismith/Tobler. None were found. Existing GPS studies use self-selected, likely fitter uploaders.
- A statement in the Horizontal Layers guideline on own attributes on OSM geometries. It is absent there and is covered instead by the Collective Database Guideline.
