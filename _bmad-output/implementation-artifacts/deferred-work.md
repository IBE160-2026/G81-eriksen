- source_spec: `_bmad-output/implementation-artifacts/spec-1-2-appen-er-publisert-pa-vercel.md`
  summary: AD-15 punkt 4 i spinen lover at «forrige publisering blir stående» når byggingen feiler, men `migrate` har da alt endret databasen. Teksten bør si at migreringer må være bakoverkompatible.
  evidence: Byggesteget kjører `migrate` før Vercels `collectstatic`, og `lastinn` kommer etter fra story 1.6. Feiler et senere steg, kjører den gamle koden mot det nye skjemaet. Teksten fantes før story 1.2.

- source_spec: `_bmad-output/implementation-artifacts/spec-1-3-siden-har-et-rolig-og-tilgjengelig-grunnoppsett.md`
  summary: `forbedring.js` (sperre, `pageshow`, fokus på `data-fokus`) har bare tekstsjekker og ingen oppskrift for den manuelle sjekken i nettleseren.
  evidence: En snudd betingelse i `vedInnsending` eller `vedVisning` ville passert `ForbedringTest`. Ta det opp i story 1.9, når søkeskjemaet blir den første ekte brukeren, med en kjørbar sjekk eller en dokumentert manuell sjekk.
- source_spec: `_bmad-output/implementation-artifacts/spec-1-3-siden-har-et-rolig-og-tilgjengelig-grunnoppsett.md`
  summary: Statiske filer på Vercel er ikke verifisert, verken at de serveres eller hvordan de bufres (ingen cache-busting).
  evidence: Story 1.3 er den første med statiske filer. Sjekk at `/static/css/tokens.css` gir 200, og les `Cache-Control` på forhåndsvisningen. Bufres filene lenge uten hash i navnet, er det medium.
- source_spec: `_bmad-output/implementation-artifacts/spec-1-3-siden-har-et-rolig-og-tilgjengelig-grunnoppsett.md`
  summary: README sier fortsatt at mappene for appen (`config/`, `tests/` med flere) «kommer med implementeringen».
  evidence: Teksten fantes før story 1.3. Den henger sammen med det åpne punktet om mappestruktur i README i `.logs/hannah-eriksen/issues.md`.
