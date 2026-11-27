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

- source_spec: `_bmad-output/implementation-artifacts/spec-1-7-turdatabasen-har-15-kontrollerte-turer.md`
  summary: Avklart 2026-11-25: byggeskriptet stopper nå en rundtur der mer enn halve lengden gås to ganger (`domene.rute.andel_gatt_to_ganger`, `ByggFeil` med tur-ID og andel). Punktet fra 1.5 om at byggeskriptet ikke sjekker at en rundtur går i ring, er løst.
  evidence: Sjekken fant at kandidaten `vettakollen-rundtur` gikk 100 % to ganger med de opprinnelige via-punktene. Den går nå opp vestsiden (`F_20171026_02`) og har 17 %. `dalivann-rundt` har 38 % (stilken fra Gjettum) og `nordmarksrunden` 12 %. Se `docs/kontroll-turdatabasen.md`.
- source_spec: `_bmad-output/implementation-artifacts/spec-1-7-turdatabasen-har-15-kontrollerte-turer.md`
  summary: Avklart 2026-11-25: festing bare i segmentender holdt for alle 15 turene. Ingen tur trengte et punkt midt på et segment eller en lukket ring. Punktet fra 1.5 om at rutepunktene bare kan festes til noder (segmentender), er løst for v1; det tas opp igjen hvis en ny tur i story 6.2 trenger det.
  evidence: Alle rutepunktene i `data/kurateringsliste.toml` ligger på noder. Der to rutenumre ikke møtes (Ullevålseter), brukes korte koblinger på høyst 10 m i stedet for å dele segmenter.
- source_spec: `_bmad-output/implementation-artifacts/spec-1-7-turdatabasen-har-15-kontrollerte-turer.md`
  summary: Byggeskriptet er sårbart for treg eller nedetid i WFS-en til Turrutebasen. Det finnes ingen buffer for rutenumre som hentes flere ganger, og ingen nye forsøk, og `osl` (3435 segmenter, ca. 75 s) er nær tidsavbruddet på 60 s per lesing.
  evidence: WFS-en var nede ca. 35 min 2026-11-25 under byggingen i 1.7. Fire turer bruker `osl`. Det gjelder bare den manuelle byggingen (ikke appen) og stopper med en tydelig melding. Tas opp før story 6.2 utvider lista.
- source_spec: `_bmad-output/implementation-artifacts/spec-1-10-ola-ser-ruten-pa-kart-og-i-tekst.md`
  summary: Oppførselen i `kart.js` (berøring, flisfeil, kontrollene og «Prøv igjen») testes bare som tekst og i manuelle sjekker i Chrome.
  evidence: Repoet har med vilje ingen JS-kjøring (ingen package.json). En regresjon, for eksempel ombyttet enable/disable eller et nytt navn på `data-kart-handling`, ville gått gjennom testene. Vurder en liten DOM-test med Leaflet, eller en fast manuell sjekkliste per PR. Medium hvis det stemmer.
- source_spec: `_bmad-output/implementation-artifacts/spec-1-11-ola-kan-be-om-nytt-forslag.md`
  summary: Fragmentbyttet i forbedring.js («Nytt forslag») og «Kart lastes …» i kart.js testes bare som kildetekst; ingen kjøretest av bytte, tittel, fokus og reserveinnsending.
  evidence: Gjennomgang 1.11 (VG, BH): sletting av importNode eller invertering av svar.ok lar alle testene passere. Repoet har ingen JS-runner; Chrome-sjekken er verifiseringen inntil videre (vurder Playwright i 6.6).

- source_spec: `_bmad-output/implementation-artifacts/spec-1-12-ola-far-hjelp-nar-ingen-tur-passer.md`
  summary: Endringsforslag gjenbruker `dato` fra det lagrede søket uten å sjekke mot dagens dato.
  evidence: En fane som står åpen over midnatt kan gi et søk med dato i fortiden; ikke verifisert om `Sok` avviser det.
- source_spec: `_bmad-output/implementation-artifacts/spec-1-12-ola-far-hjelp-nar-ingen-tur-passer.md`
  summary: `foresla_endringer` kjører `velg_turer` opptil ~25 ganger per visning av Tilstandspanelet.
  evidence: Ikke et problem med 15 turer; kan måles og caches om turdatabasen vokser.

- source_spec: `_bmad-output/implementation-artifacts/spec-2-1-ola-lager-konto-logger-inn-og-logger-ut.md`
  summary: Tester for IntegrityError-race ved samtidig kontooppretting og for fokusrekkefølge når både «Forslaget er utilgjengelig» og «Du er logget ut.» ligger i meldingskøen.
  evidence: Verification-gap-reviewer: grenene i LagKontoForm.lag_bruker og sok.html er ikke dekket av tester; sjeldne tilfeller.
- source_spec: `_bmad-output/implementation-artifacts/spec-2-1-ola-lager-konto-logger-inn-og-logger-ut.md`
  summary: Toppmenyen på 500/403-sider viser gjestmeny også for innlogget bruker.
  evidence: base.html er hardkodet uten request.user på feilsider med vilje (500 unngår oppslag); lav alvorlighet.

## Fra story 2.2

- Ingen sperre på Lag konto: duplikatmeldingen («Kunne ikke lage konto – prøv å logge inn») kan brukes til å liste opp hvilke e-poster som har konto. Utsatt bevisst (spec 2.2, Never).

- source_spec: `_bmad-output/implementation-artifacts/spec-2-2-innloggingen-har-en-grense-for-mislykkede-forsok.md`
  summary: Admin-innloggingen (`/admin/`) bruker samme `Bruker`-kontoer men er ikke omfattet av forsøksgrensen.
  evidence: Edge-/verification-reviewer: bare `logg_inn` kaller `authenticate()` via grensen; admin-skjemaet går utenom. Gjelder kontoer med `is_staff`.
- source_spec: `_bmad-output/implementation-artifacts/spec-2-2-innloggingen-har-en-grense-for-mislykkede-forsok.md`
  summary: `Innloggingsforsok` kan vokse ved flom av tilfeldige e-poster; opprydding kjører bare på innloggings-POST og sletter globalt per forespørsel.
  evidence: Edge-case-reviewer; lav alvorlighet på Hobby/Neon Free, ingen IP-grense (AD-10).

- source_spec: `_bmad-output/implementation-artifacts/spec-2-3-ola-registrerer-en-gjennomfort-tur-og-ser-den-i-historikken.md`
  summary: Samtidig dobbel POST mot en DB-lagret økt kan gi to registreringer, siden engangstokenet leses og skrives uten lås.
  evidence: Review (alle tre lag): `engangstoken.bruk` er read-modify-write på økta; sekvensiell dobbel POST er testet, `forbedring.js` sperrer dobbeltklikk i nettleseren. Vurder unik nøkkel eller lås.
- source_spec: `_bmad-output/implementation-artifacts/spec-2-3-ola-registrerer-en-gjennomfort-tur-og-ser-den-i-historikken.md`
  summary: `Registrering` mangler `CheckConstraint` for fornøydhet 1–5 og brukt tid 10–1440 min; Historikk har ingen paginering; dato i Historikk vises uten år.
  evidence: Review: reglene ligger bare i skjema/mal; ubegrenset spørring og «7. nov.» uten år blir tvetydig over flere år.

## Fra story 2.6

- source_spec: `_bmad-output/implementation-artifacts/spec-2-6-ola-sletter-kontoen.md`
  summary: En `is_staff`-bruker kan slette seg selv, også som siste superbruker.
  evidence: Spec 2.6 (Never): ingen blokkering av `is_staff`. Vurder vern mot å slette siste superbruker.
- source_spec: `_bmad-output/implementation-artifacts/spec-2-6-ola-sletter-kontoen.md`
  summary: Andre økter for den slettede brukeren (annen enhet) ryddes ikke aktivt.
  evidence: De blir ugyldige fordi brukeren ikke finnes; sesjonsrader blir liggende til de utløper.

- source_spec: `_bmad-output/implementation-artifacts/spec-3-2-soket-bruker-nivataket-og-historikken.md`
  summary: `avgjor_nivaheving` er ikke atomisk: to samtidige søk fra samme bruker kan begge få `nivaheving=True`.
  evidence: leser `brukt_heving` og lagrer uten lås. Skade er bare dobbel prioritering. Fiks: betinget UPDATE på `brukt_heving < antall_hevinger` og bruk radantall som resultat.

- source_spec: `_bmad-output/implementation-artifacts/spec-3-4-testbrukeren-viser-personaliseringen.md`
  summary: `lastinn` sletter kontoen med testbrukerens e-post uten å vite om den er laget av `lastinn`.
  evidence: `testbruker.slett` slår opp på e-post alene. En ekte bruker som registrerer `testbruker@example.com` mister kontoen ved neste bygg. Fiks krever en markering (felt/migrasjon) eller å sperre e-posten ved kontooppretting.
