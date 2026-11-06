# Strukturgjennomgang – EXPERIENCE.md (bmad-review, lens structure)

Strukturmodell: Reference/Database med Foundation som stillas. 8 412 ord. 22 anbefalinger; mål ca. −1 280 ord.

## Beslutninger fra fasilitator (gjelder ved anvendelse)
- **Avvik fra PRD: BEHOLDES i EXPERIENCE.md** (ikke flyttet). Den er sporbarhet sensor og PRD-oppdateringen trenger. Men: fjern punkter som bare gjentar spinen (lag heller én-linjes pekere), kutt historikk («NFR-3 er ikke lenger et avvik»), og sørg for at nummereringen stemmer med henvisningene i reconcile-prd.md (eller fjern nummerhenvisningene der).
- Alle andre forslag under godtas, inkludert QUESTION om `h1` som kolonne i IA-tabellen.

## Forslag (fra structure-linsen)
1. Avvik fra PRD — se fasilitatorbeslutning over.
2. Responsive & Platform › «Regler for smal skjerm og berøring» → ett punkt: «På mobil står kartet innenfor sidemargen, ca. 60 % av skjermhøyden (`{spacing.map-mobile-height}`), så siden kan rulles med én finger ved siden av kartet. Øvrige regler: trykkflater og reflow i Accessibility Floor, kart i Kart – oppførsel, Toppmeny og Historikktabell i Component Patterns, Søk-oppsettet i DESIGN.md › Layout & Spacing.»
3. Foundation › «Visuelle referanser» + «Mock-dekning» → konfliktregel først + tabell Fil | Viser | Status og kjente avvik; «Skjermer uten mock bygges fra spinene og wireframene.» Kutt gjentakelsen i IA-innledningen.
4. KI-åpenhet → MERGE inn i Component Patterns (KI-merke-raden: merke + «Begrunnelse fra mal» ved reserveløsning/testmodus/åpnet fra Historikk; Forklaringspanel-raden: de tre setningene). Punkt 4–5 dekkes av Faktarute/Nivåmerke og Voice.
5. «Rekkefølge på Turforslag» (1–10) → MOVE til Component Patterns som «Turforslag – rekkefølge.» ved «Kart – oppførsel».
6. State Patterns-innledning → «Kolonnen «Skisse» viser til skjerm 1–6 og kanttilstand A–G i flow-ola. Mockene står i Foundation › Visuelle referanser. Tekstene står i Mikrotekst.»
7. Mikrotekst-sitater gjentatt i Component/State Patterns → erstatt med radnavn i Mikrotekst (behold sitater i Key Flows).
8. Historikktabell-cellen → kondensert tekst (ekte `<table>`, nyeste først, `th scope=row`, skjult «Handlinger», skjulte tillegg, rullebeholder `role="region"`; kolonner/formater: se Mikrotekst; rekkefølge: DESIGN.md › Layout › Historikk).
9. Fokus/live-region ved visningsbytte → eneste hjem i A11y › «Sidetitler og fokus» og «Meldinger etter navigering»; andre steder pekere; State «Henter nytt forslag» beholder bare det særegne.
10. Accessibility Floor: kutt godkjenningssetningen og punktene Kontrast, Turillustrasjon, Glyfer, Språk (gjør til pekere); behold resten som SM-4-sjekkliste.
11. Kuttrekkefølge → samlet i Foundation (fremgang, mørk modus, FR-11 → skjul Fritekstønske, FR-9/10 → Bekledningstips forsvinner uten tomrom); komponentrader peker dit.
12. Inspiration & Anti-patterns: slå sammen UT.no-bildepunktene; kutt «overselge KI» (står i Voice); flytt «skjærende farger» til DESIGN.md › Do's and Don'ts.
13. Responsive-breddetabell: kutt raden «320 px» og kolonnebredder; behold oppførsel.
14. State Patterns: kutt «Mørk modus» og «Rute som krever konto, brukt som gjest»; «Sender» → peker til Primærknapp; grupper radene etter skjerm.
15. UJ-2 steg 4: flytt metakommentar om FR-19 til Avvik fra PRD; forutsetningen («har registrert to lette grønne turer fra før») i scenebeskrivelsen.
16. Tastatur: behold listen i Interaction Primitives; A11y peker dit.
17. Mikrotekst: fjern kolonnen «PRD-original», skriv originalen i Kilde; vurder skjerm-kolonne/deloverskrifter.
18. «Kart – oppførsel» → tabell Inndata | Kartet | Siden; behold «aldri»-reglene under.
19. Åpne punkter → tabell Punkt | Avklares i (arkitektur/PRD/UX) | Blokkerer.
20. QUESTION→godtatt: `h1` som kolonne i IA-tabellen; A11y-tabellen beholder bare `h2` for Turforslag og Konto.
21. PRESERVE: Key Flows › Feilveier.
22. PRESERVE: Voice › «Bevisste navneforskjeller».
Små: «Kun norsk» i Foundation gjentar første punkt; IA › «Felles for alle skjermer» gjentar NFR-2 i Primærknapp.
