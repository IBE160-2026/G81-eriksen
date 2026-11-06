# Avstemming: tilbakemelding på product brief mot spines

Kilde: `docs/tilbakemelding-product-brief.md` (faglærer, 2026-10-06; gjelder den engelske briefen, commit `65465e9`).
Spines: **E** = EXPERIENCE.md, **D** = DESIGN.md. Tilbakemeldingen er innarbeidet i PRD-en; her vurderes bare det som påvirker UX.

## 1. Dekket

- KI finner ikke på ruter, men velger og forklarer blant kjente turer (De viktigste endringene 1) → E KI-åpenhet («Ruten, tiden og nivået kommer fra Kartverkets turdata … ikke fra KI»).
- «vis brukeren hvorfor et forslag passer» (Forslag til justering 2) → E «Begrunnelse», personaliseringsregel i klartekst (UJ-2).
- Én primærbruker og ett område, så «design kan bli gode» → D Brand & Style, E Foundation.
- Kjerneflyten «beskriv ønsket tur → få et forslag … → lagre turen og vurder den → få et bedre tilpasset forslag» → E UJ-1 og UJ-2.
- Skjermbilder og flyter skissert (§2 kriterium 4) → wireframes/ia og flow-ola, mockups.
- Testmodus for språkmodellen (§2 kriterium 6) → E «KI-merke»: «Begrunnelse fra mal» også i testmodus uten nøkkel.
- Testbruker for sensor → E IA («Testbrukeren … logger inn via vanlig innlogging»).
- Prioritering: E/D merker mørk modus som det som kuttes først, og P2-kutt av bekledningstips gir ingen tomrom (E «Bekledningstips»).

## 2. Avvik

- **«Tenk på mobilbruk ute på tur, selv om v1 er en nettside»** (§2 kriterium 4, Design og brukeropplevelse) → v1 er desktop. Memlog (override) Plattform, l. 18. Overstyringen begrunnes bare mot PRD NFR-3/UJ-1, ikke mot denne vurderingskommentaren (se Konflikter 1).
- **«Leaflet med OpenStreetMap»** (Gjennomførbarhet, «Egnet for Claude Code») → E Foundation: «ikke et UX-vedtak».

## 3. Mistet

1. **Personaliseringen skal kunne *ses* i en demo.** §2 kriterium 6: testbruker «slik at sensor kan se personaliseringen uten å bruke appen i flere uker». Spines viser personalisering bare i begrunnelsen når en regel slo inn. Det finnes ingen visning av nivåtak, sperre eller turtypepreferanse, og ingen fremgang mot neste nivå. Sperre og preferanse (FR-19/FR-20) har heller ingen eksempeltekst, så testbrukerens historikk viser seg ikke tydelig.
2. **Personvern nevnt for brukeren.** Vanskelighetsgrad-tabellen: «Innlogging og turhistorikk (hvor brukeren har vært) er personopplysninger». Ingen personverntekst ved registrering eller på Konto.
3. **GPX som mulighet.** Filhåndtering: «GPX-filer for ruter er en mulig, men ikke nødvendig del». Spines tar ikke stilling (ingen «Last ned rute»). Merk at addendum sier at turdatabasen ikke tilbys som nedlastbar fil (ODbL), så eventuell GPX må begrenses til Kartverket-turer.
4. **Mobil «ute på tur» som brukssituasjon.** Utover selve layouten mangler spines det kommentaren peker på: brukeren som sjekker turen underveis (finne startpunktet, se ruten). Utsatt med mobilen, men ikke ført som noe senere fase må dekke.

## 4. Konflikter (ikke loggført)

1. **Desktop-overstyringen mot et vurderingskriterium.** §2 kriterium 4 (Design og brukeropplevelse, 10 % av del 1) ber eksplisitt om å tenke på mobilbruk. Memlog l. 18 og E Avvik fra PRD nevner bare PRD-kravene. Risikoen for vurderingen er ikke ført, og ingen begrunnelse er skrevet som sensor kan lese.
2. **Omfangsadvarsel mot nye UX-tillegg.** Tilbakemeldingen: «Seks v1-punkter med fire integrasjoner er mye for en gruppe på én person» og «Pass på at kjerneflyten blir ferdig og stabil før dere legger til mer». Spines legger til illustrasjoner tegnet fra høydedata, mørk modus, KI-forklaringspanel og UJ-3. Mørk modus har en kuttregel, men Turillustrasjon bærer klimakset i UJ-1 (memlog l. 28) og har verken prioritet eller reserve hvis den må kuttes.
3. **Kartvalg.** Faglærer foreslår Leaflet + OSM. D «Kart» låser «Kartverket-fliser», mens E sier at kartvalget ikke er et UX-vedtak. Ingen memlog-beslutning (samme funn som reconcile-research, Konflikter 2).
