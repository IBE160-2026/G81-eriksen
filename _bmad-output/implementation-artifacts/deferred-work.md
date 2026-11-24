- source_spec: `_bmad-output/implementation-artifacts/spec-1-2-appen-er-publisert-pa-vercel.md`
  summary: AD-15 punkt 4 i spinen lover at «forrige publisering blir stående» når byggingen feiler, men `migrate` har da alt endret databasen. Teksten bør si at migreringer må være bakoverkompatible.
  evidence: Byggesteget kjører `migrate` før Vercels `collectstatic`, og `lastinn` kommer etter fra story 1.6. Feiler et senere steg, kjører den gamle koden mot det nye skjemaet. Teksten fantes før story 1.2.
- source_spec: `_bmad-output/implementation-artifacts/spec-1-6-turene-lastes-inn-med-en-kommando.md`
  summary: Avklart 2026-11-24: AD-15 punkt 4 i spinen sier nå at migreringer er bakoverkompatible (legger bare til, fjerner ikke og gir ikke nytt navn). Punktet over om bakoverkompatible migreringer er løst.
  evidence: Story 1.6 la `lastinn` inn i byggesteget etter `migrate`. Beslutningen står i `.memlog.md` i arkitekturmappa.

- source_spec: `_bmad-output/implementation-artifacts/spec-1-3-siden-har-et-rolig-og-tilgjengelig-grunnoppsett.md`
  summary: `forbedring.js` (sperre, `pageshow`, fokus på `data-fokus`) har bare tekstsjekker og ingen oppskrift for den manuelle sjekken i nettleseren.
  evidence: En snudd betingelse i `vedInnsending` eller `vedVisning` ville passert `ForbedringTest`. Ta det opp i story 1.9, når søkeskjemaet blir den første ekte brukeren, med en kjørbar sjekk eller en dokumentert manuell sjekk.
- source_spec: `_bmad-output/implementation-artifacts/spec-1-3-siden-har-et-rolig-og-tilgjengelig-grunnoppsett.md`
  summary: Statiske filer på Vercel er ikke verifisert, verken at de serveres eller hvordan de bufres (ingen cache-busting).
  evidence: Story 1.3 er den første med statiske filer. Sjekk at `/static/css/tokens.css` gir 200, og les `Cache-Control` på forhåndsvisningen. Bufres filene lenge uten hash i navnet, er det medium.
- source_spec: `_bmad-output/implementation-artifacts/spec-1-3-siden-har-et-rolig-og-tilgjengelig-grunnoppsett.md`
  summary: README sier fortsatt at mappene for appen (`config/`, `tests/` med flere) «kommer med implementeringen».
  evidence: Teksten fantes før story 1.3. Den henger sammen med det åpne punktet om mappestruktur i README i `.logs/hannah-eriksen/issues.md`.
- source_spec: `_bmad-output/implementation-artifacts/spec-1-3-siden-har-et-rolig-og-tilgjengelig-grunnoppsett.md`
  summary: Avklart 2026-11-23: statiske filer serveres på Vercel (200), med `Cache-Control: public, max-age=0, must-revalidate`. Punktet om servering og cache-busting over er løst.
  evidence: `vercel curl` mot forhåndsvisningen av PR #26.
- source_spec: `_bmad-output/implementation-artifacts/spec-1-5-byggeskriptet-lager-turdatabasen-fra-kartverket.md`
  summary: Byggeskriptet sjekker ikke at en rundtur faktisk går i ring. Med ett `via` kan korteste vei tilbake bli samme vei som ut.
  evidence: Det er bare påkrevd minst ett `via`. Ta det opp i 1.7: se etter kanter som brukes to ganger i en rundtur, eller kontroller lengden mot ut.no.
- source_spec: `_bmad-output/implementation-artifacts/spec-1-5-byggeskriptet-lager-turdatabasen-fra-kartverket.md`
  summary: Rutepunktene kan bare festes til noder (segmentender). Lukkede ringsegmenter og T-kryss gir ingen sti.
  evidence: Det er ubekreftet (maybe-false). Det avgjøres når de 15 turene kureres i 1.7. Trengs et punkt midt på et segment eller en ring, må segmentet deles ved festepunktet (medium hvis det stemmer).

- source_spec: `_bmad-output/implementation-artifacts/spec-1-6-turene-lastes-inn-med-en-kommando.md`
  summary: `lastinn` advarer om turer i databasen som mangler i fila, men ikke om startpunkter som ingen tur i fila bruker lenger.
  evidence: Uverifisert, medium hvis det stemmer: blir startpunktvalget i 1.9 bygd fra `Startpunkt`-tabellen og ikke fra turene, kan et startpunkt uten turer dukke opp (f.eks. etter at 1.7 bytter testturene). Avgjøres når 1.9 bestemmer hvor lista over startpunkter kommer fra.
