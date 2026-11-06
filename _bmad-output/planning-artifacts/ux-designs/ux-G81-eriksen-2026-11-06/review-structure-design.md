# Strukturgjennomgang – DESIGN.md (bmad-review, lens structure)

Strukturmodell: Reference/Database. 4 463 ord (frontmatter 1 119, brødtekst 3 344).

| Pass | Original | Revidert | Begrunnelse |
|---|---|---|---|
| structure | §Brand & Style: «Visuelle referanser:» + avsnittet «Retningsmockene og fargetemaet er eldre …» … «Ved konflikt vinner …» | MOVE + CONDENSE: egen `### Visuelle referanser` med konfliktregelen først; mockenes alder i etiketten «Retninger og palett (eldre: Granskog-paletten og gamle eksempeltall)»; «Kjente avvik i mockene: …» (utsiktsmarkør, tre turtypekort, pilleknapper, kun desktop; eldre fremgangsordlyd i key-historikk; «Eksempel»-merker og rammer hører bare til mockene). | Viktigste regel først. |
| structure | §Layout & Spacing: «Under bruddet» brukes uten innføring | MOVE (stillas): innfør `{spacing.breakpoint-stack}` (720 px) etter åpningen; nevn Faktarute-brudd ~360 px og nedskalering i Typography. Do's and Don'ts viser til tokenet. | Alle bruddpunkter ett sted. |
| structure | §Components: 27 komponenter i flat liste | QUESTION→godtatt: h3-grupper Grunnelementer · Valg i skjema · Turforslag · Meldinger og tilstander · Historikk og konto, uten å flytte rekkefølge. | Skumbarhet. |
| structure | Atferd i visuelle seksjoner (ut.no-lenke, gjest ser «Logg inn», ankertekst 1 og 5, høydeprofil beregnes fra høydedata) | QUESTION→godtatt: flytt til EXPERIENCE.md hvis ikke der; ellers henvisning. | Én eier per opplysning. |
| structure | §Brand & Style **Illustrasjoner.** | CONDENSE: «Hver tur får en egen, enkel illustrasjon tegnet fra turdataene: en stilisert rute og en høydeprofil som viser formen på turen før du går. Vi bruker ingen fotografier (se **Turillustrasjon**).» | Duplikat. |
| structure | §Components intro: «Nøkkelskjermene viser komponentene i bruk: …» | CUT | Gjentakelse. |
| structure | Historikktabell: «Linjen «Nye søk prioriterer …» står under tabellen …» | CUT | Står i Layout. |
| structure | §Typography: «Tall i turforslaget står i sans-serif (`fact-value`).» | CUT | Står i tabellen og Do's. |
| structure | Kart: «På mobil står kartet innenfor sidemargen med 1 px `border` …» | CONDENSE: «Mobiloppsett: se Layout & Spacing.» | Duplikat. |
| structure | Toppmeny: «Menypunktene står til høyre.» | CUT | Står i Layout. |
| structure | «To designretninger er slått sammen» | PRESERVE | Nøkkel til etikettene. |
| structure | Kontrastmål | PRESERVE | Bevisgrunnlag. |
| structure | Do's and Don'ts | PRESERVE | Påkrevd. |

Små gjentakelser i tillegg: fokusring på kart (Kartlag + Fokusring), «ingen bildetekst» for pyntillustrasjonen (3 steder), «Skyggene i mockene» (§Elevation) vs rammemerknaden.
