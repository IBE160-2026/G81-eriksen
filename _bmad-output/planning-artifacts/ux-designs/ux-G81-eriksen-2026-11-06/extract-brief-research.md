# Uttrekk for UX: brief, tilbakemelding og turdata-research

Kilder (forkortet):
- **[B]** `docs/product-brief-your-next-adventure-no.md`
- **[T]** `docs/tilbakemelding-product-brief.md` (gjelder den engelske briefen, commit `65465e9`)
- **[R]** `_bmad-output/planning-artifacts/research/technical-turdata-oslomarka-2026-10-29/research.md`

**Forrang:** PRD-en (`prds/prd-G81-eriksen-2026-10-29/prd.md`, v1.0) vinner ved konflikt. Briefen bruker allerede Turrutebasen ([B] The Solution), slik [R] anbefaling 7 ba om. Sannsynlige konflikter med PRD-en er merket **⚠ PRD**. Jeg har bare søkt i PRD-en etter nøkkelord, ikke lest hele.

## 1. Visjon, tone og følelse

- «hjelper nybegynnere med å planlegge sin neste fottur» – brukeren «skriver rett og slett inn hvor de vil dra, hvor mye tid de har, og hva slags opplevelse de er ute etter». [B] Executive Summary
- Fortrinnet er personalisering og vanlig språk: «en rolig skogstur på et par timer» «i stedet for å filtrere i lister». [B] What Makes This Different
- Ærlig tone: «det ligger ikke i en unik teknisk oppfinnelse», men i hvor godt data og historikk kombineres som «en sammenhengende opplevelse». [B] What Makes This Different
- Tillit og åpenhet: suksess er «et forslag de stoler på og faktisk bruker, som ikke er for krevende». [B] Who This Serves. Tjenesten skal «alltid [vise] hvorfor en tur er foreslått». [B] Vision
- Kjerneidé: «forstå brukeren, ikke bare stedet». [B] Vision
- Faglærer: «vis brukeren hvorfor et forslag passer». [T] Forslag til justering, punkt 2

## 2. Målgruppe og brukssituasjoner

- Primærbruker: nybegynnere i Oslo-området som er «usikre på hva de takler» og mangler erfaring til å vurdere lengde, stigning og vanskelighetsgrad. [B] Who This Serves
- Situasjonen i dag: de vet omtrent sted og tid, men leter i flere kilder eller velger en kjent tur fordi «det er tryggere enn å lete». [B] The Problem
- Mobil: brukerne «sjekker ofte turen på vei ut». [B] Kvalitetskrav – Mobil. [T] ber om å «tenke på mobilbruk ute på tur». [T] 2. Utgangspunkt, kriterium 4
- Utenfor v1: erfarne turgåere, turister og tilflyttere. [B] Who This Serves, Vision
- Demo-persona: en testbruker med ferdig turhistorikk der regel 6–8 synes. [B] Success Criteria 9
- ⚠ PRD: PRD-en har en navngitt persona («Ola») og en gjesteflyt uten innlogging. Det står ikke i briefen.

## 3. Funksjoner og skjermer i briefen

- **Søk/input:** sted, tilgjengelig tid og turtype/opplevelse (topptur, skogstur, utsikt). [B] The Solution, Scope
  - ⚠ PRD: input er varighet + dag, med valgfritt startpunkt, turtype og fritekst.
- **Forslag:** rutelinje på kart, beregnet tidsestimat, bekledningstips fra værvarselet og en kort forklaring på hvorfor turen passer. Minst ett forslag. [B] Success Criteria 1
  - ⚠ PRD: ett forslag om gangen, med «Nytt forslag», turnivå med farge **og** tekst, og ut.no-lenke.
- **Vanskelighetsgrad:** DNT-farger grønn, blå, rød, svart. [B] Success Criteria
- **Konto:** opprette konto, logge inn og slette kontoen med all historikk. [B] Scope
- **Lagre tur og vurdere den:** *for lett / passe / for hard* og *likte / likte ikke*. [B] Success Criteria 4
  - ⚠ PRD: *lett / moderat / vanskelig*, fornøydhet 1–5 og brukt tid. Følg PRD-en.
- **Historikk:** «min turhistorikk» kan utledes som skjerm. [T] 2. Utgangspunkt, kriterium 4
- **Personaliseringsregler som påvirker visningen:** ny bruker får grønn; tre «for lett» gir neste nivå; «for hard» setter tak; «likte ikke» vises ikke igjen. [B] Success Criteria 5–8
- **Tomtilstander og feil** [B] Kvalitetskrav – Feilhåndtering:
  - Ingen tur passer: si fra og foreslå justering (mer tid, annen turtype). «Siden står aldri tom.»
  - Sted utenfor Oslo: si at v1 bare dekker Oslo-området.
  - Værdata mangler: vis turen uten klesråd, med en melding.
  - KI feiler: bruk et regelbasert forslag.
- **UU:** WCAG 2.1 AA – kontrast, tastatur, skjemaetiketter og alt-tekst for kart og bilder. [B] Kvalitetskrav – Universell utforming
- **Personvern:** posisjonen spores ikke. Appen lagrer bare e-post, passord-hash, turer og vurderinger. [B] Kvalitetskrav – Personvern
- **Utenfor v1:** mobilapp, sosiale funksjoner, offline-GPS, push-varsler, føremelding og booking. [B] Scope
- **Språk:** «Støtte for flere språk enn norsk/engelsk» er utenfor. [B] Scope
  - ⚠ PRD: bare norsk i v1.

## 4. Tilbakemeldingen – punkter som påvirker UX

[T] gjelder den eldre engelske briefen. Punkt 1–3 er innarbeidet i [B].

1. KI skal ikke finne på ruter, men velge og forklare blant kjente turer. Det er «potensielt farlig i fjellet». UI-konsekvens: forslaget viser en reell tur fra databasen, med begrunnelse. [T] De viktigste endringene, 1
2. Personaliseringen skal være testbar og synlig: «vis brukeren hvorfor et forslag passer». [T] Forslag til justering, 2
3. Én primærbruker og ett område, slik at «design kan bli gode». [T] De viktigste endringene, 3
4. Kjerneflyten skal være ferdig og stabil først: «beskriv ønsket tur → få et forslag med kart, tid og klesråd → lagre turen og vurder den → få et bedre tilpasset forslag neste gang». [T] Hva vanskelighetsgraden betyr for dere
5. Skjermene kan utledes: søk, forslag med kart og min turhistorikk. Tenk mobil ute på tur. [T] 2. Utgangspunkt, kriterium 4
6. Testmodus for språkmodellen og en testbruker, så sensor kan se personaliseringen. Personaliseringen må være synlig i en demo. [T] 2. Utgangspunkt, kriterium 6
7. Kart med nøkkelfrie tjenester, for eksempel Leaflet med OSM. [T] Gjennomførbarhet, «Egnet for Claude Code»
8. GPX-filer er «mulig, men ikke nødvendig». [T] Vanskelighetsgrad, Filhåndtering

## 5. Fra researchen: data, begrensninger og kreditering

**Datafelt som kan vises** [R] Anbefalinger 5, D1, D2:
- Turnavn. Turrutebasen har delvis navn; mange ruter heter «Ukjent», så gruppen må navngi dem. [R] D1
- Rutelinje på kart (GeoJSON, WGS84 for Leaflet). [R] D2
- Lengde i km (`turf.length`). [R] D2
- Høydemeter fra Kartverkets høyde-API (1 m terrengmodell). [R] D2
- Gradering (egen regel, forslag: grønn ≤5 km og ≤300 hm; blå ≤10 km og ≤600 hm). [R] Anbefaling 2
  - ⚠ PRD: «under 5 km / under 300» etter Merkehåndboka.
- Estimert tid (Naismith eller sveitsisk regel + påslag). [R] D4, Anbefaling 4
- `ruteFølger` (sti, bilvei, gang-/sykkelvei) som en mulig indikator på underlag. [R] D1
- `kilde` og `lisens` per tur. [R] Anbefaling 5

**Begrensninger UI-et må kommunisere:**
- Tidsestimat: vis «pauser ikke inkludert». [R] Anbefaling 4. Formlene bommer med 13,5–15,5 % og undervurderer «trolig» tiden for nybegynnere. [R] D4
- Vanskelighetsgrad er satt av tjenesten, ikke av kilden. Bare 11,7 % av segmentene er graderte, og DNT-hovedrutene er ugraderte. [R] Sammendrag, D1
  - PRD-tekst: «Terreng og føre er ikke vurdert.»
- Høydemeter fra terrengmodell kan bli for høye uten glatting. [R] D2
- Underlagstype mangler i dataene. [R] D1
- Føre og terreng er ikke med. [B] Scope

**Kreditering som må synes** [R] D3, Anbefaling 6:
- «© Kartverket», helst med lenke (CC BY 4.0), for ruter og topografisk kart.
- «© OpenStreetMap contributors» med lenke til openstreetmap.org/copyright, synlig på kartet. Gjelder OSM-fliser og OSM-ruter.
- OSM-ruter: ODbL, færre enn 100 objekter i ett engangsuttrekk.
- ⚠ PRD (NFR-7) legger også til «Data fra MET Norge». Det står ikke i [R].

## 6. Andre apper og nettsider

- **ut.no, AllTrails, Google Maps, turkart, blogger:** steder brukerne leter i i dag. De er «statiske: samme resultat uansett hvem som spør». [B] The Problem, What Makes This Different. [T] Det som er bra, 1
- **ut.no/DNT:** har ikke lenger åpent API. Nasjonal Turbase ser ut til å ha vært ute av drift siden ca. 2020 (middels tillit). Brukes «som inspirasjon ved kurateringen, ikke som datakilde». [R] D1
  - ⚠ PRD: forslaget har en valgfri lenke til turen på ut.no.
- **DNT:** fargeskalaen for vanskelighetsgrad [B] Success Criteria. Fellesturer går i ca. 3 km/t. [R] D4
- **Yr/MET:** værvarsel brukt til klesråd. [B] Scope
- **Waymarked Trails:** GPX mangler ofte høyde. [R] D2
- **geojson.io:** til å tegne turer manuelt ved kurateringen. [R] Sammendrag
- **Leaflet + OpenStreetMap:** foreslått kartbibliotek. [T] Gjennomførbarhet
