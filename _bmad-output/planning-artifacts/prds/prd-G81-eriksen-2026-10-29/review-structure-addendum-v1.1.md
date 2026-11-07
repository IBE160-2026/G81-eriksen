# Strukturgjennomgang – addendum.md v1.1 (bmad-review, lens structure)

Modell: Reference/Database. 1 066 ord. 9 anbefalinger, alle godtatt.

Fasilitatorens svar på QUESTION: 300-tegnsgrensen (FR-12) gjelder **hele begrunnelsen slik brukeren ser den** — etter innsetting av verdier og etter at personaliseringssetningen er lagt til. Valideringen sjekker den sammensatte teksten; overskrides grensen, brukes malen (FR-13).

1. CONDENSE §Tall og nivå → nummerert liste i flytrekkefølge: (1) KI bruker plassholdere `{tid}`, `{varighet}`, `{lengde}`, `{nivå}`; (2) validering (FR-13) forkaster sifre, tallord for tid/lengde eller nivåord utenfor plassholdere → mal; (3) systemet setter inn verdier fra turdatabasen (FR-2, FR-3) og søket i faste formater; (4) personaliseringssetningen (FR-12) legges til fra fast mal; (5) 300 tegn sjekkes på den ferdige teksten (se svar over).
2. MOVE §Input-form «Mekanisme»-avsnittet (malen) til KI-seksjonen, som får navnet «KI-begrunnelsen: plassholdere, validering og mal»; malen først i mekanismen. Input-form blir rent beslutningsnotat.
3. MERGE høydeprofil/startpunkt inn i «Høydedata» og «Lagring» (komplett feltliste), pluss kort punkt «Bruk i visningen (PRD FR-6, UJ-1, EXPERIENCE.md)».
4. PRESERVE «Utsiktspunkter og en skrevet rutebeskrivelse trengs ikke.»
5. PRESERVE eksemplet, men vis hele setningen etter innsetting inkl. nivåordet.
6. CONDENSE versjonsmerker: fjern «(v1.1)» fra overskrift/punkt; `version: 1.1` i frontmatter og én endringslinje etter innledningen.
7. CONDENSE merker: felles «Mekanisme:»; fjern «(til arkitekturen)».
8. MOVE «Om formelvarianter» som `###` under «Formel for estimert tid», og «Utsatt: personlig tidsestimat» rett etter.
9. PRESERVE «Graderingsregel».
