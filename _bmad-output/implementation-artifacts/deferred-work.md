- source_spec: `_bmad-output/implementation-artifacts/spec-1-2-appen-er-publisert-pa-vercel.md`
  summary: AD-15 punkt 4 i spinen lover at «forrige publisering blir stående» når byggingen feiler, men `migrate` har da alt endret databasen. Teksten bør si at migreringer må være bakoverkompatible.
  evidence: Byggesteget kjører `migrate` før Vercels `collectstatic`, og `lastinn` kommer etter fra story 1.6. Feiler et senere steg, kjører den gamle koden mot det nye skjemaet. Teksten fantes før story 1.2.
