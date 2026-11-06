# Avstemming: teknisk research (turdata Oslomarka) mot spines

Kilde: `research/technical-turdata-oslomarka-2026-10-29/research.md`.
Spines: **E** = EXPERIENCE.md, **D** = DESIGN.md. Researchen er i hovedsak teknisk; bare UX-relevante funn er vurdert.

## 1. Dekket

- Nivå settes av tjenesten etter fast regel, ikke av kilden (Sammendrag 3, D1) → E Mikrotekst nivåforklaring «Beregnet av tjenesten … Terreng og føre er ikke vurdert», E «Nivåmerke».
- Tidsestimat deterministisk, KI gjetter ikke tid (D4) → E KI-åpenhet 4, «Faktarute».
- «vis ‹pauser ikke inkludert›» (Anbefaling 4) → E Faste formater, D Typography-regler.
- Kreditering «© Kartverket», «© OpenStreetMap contributors» med lenke til openstreetmap.org/copyright, synlig på kartet (D3, Anbefaling 6) → E «Kreditering», D «Kreditering».
- ut.no som inspirasjon, ikke datakilde (D1) → E Inspiration «Hentet fra UT.no», kun lenke.
- Høydemeter fra terrengmodell er usikre (D2) → tall vises med «ca.» (E Key Flows).
- Rutelinje på kart → E «Kart».

## 2. Avvik

- **Kartbibliotek/flis-kilde:** Researchen forutsetter Leaflet (EPSG:4326) og drøfter både OSM-fliser og Kartverkets WMTS. E Foundation sier at UI-/kartbibliotek ikke er et UX-vedtak. Ingen memlog-beslutning; se Konflikter 2.
- **Ingen bilder fra ut.no** – memlog (decision) Illustrasjoner, l. 22. Researchen nevner ikke bilder, men ut.no som inspirasjonskilde er i tråd med dette.

## 3. Mistet

1. **Underlag som hint til nybegynnere.** D1: «**Nyttig felt:** `ruteFølger` (ST = sti, BV = bilvei, GS = gang-/sykkelvei osv.) sier noe om underlaget og kan brukes som en indikator på vanskelighetsgrad». Hverken spines eller PRD viser underlag (sti vs. vei), selv om nivåforklaringen sier at terreng ikke er vurdert.
2. **Ærlighet om usikkerheten i tidsestimatet.** D4: formlene «bommer med 13,5–15,5 %» og «undervurderer trolig tiden for nybegynnere». Spines skriver «ca.» og «pauser ikke inkludert», men «Slik lager jeg forslaget» sier bare «faste formler»; at et nybegynnerpåslag er lagt inn og at tiden kan avvike, blir ikke sagt.
3. **Zoomgrenser på kartet.** D3: Kartverkets topografiske kart – «Bruk ut over ‹normal bruk› av detaljerte kartdata (zoom 12–20, Geovekst) krever tillatelse». E «Kart» lar brukeren zoome fritt med + / − uten grenser.
4. **Navnekonvensjon for turer.** D1: 41 av 186 ruter heter «Ukjent», og gruppen må navngi turene selv. Spines har ingen regel for turnavn (eksempelet «Granåsen rundt» er oppdiktet), selv om turnavnet er overskriften på turforslaget.

## 4. Konflikter (ikke loggført)

1. **Spines trenger data som ikke er i lagringsformatet.** Anbefaling 5: «Lagre turene som statisk GeoJSON med feltene `kilde`, `lisens`, `lengde_km`, `hoydemeter`, `gradering`, `estimert_tid`». Turillustrasjon (høydeprofil, «utsikt etter ca. … km»), utsiktsmarkøren på kartet og Kartbeskrivelse krever lagret høydeprofil, utsiktspunkt og beskrivelsestekst per tur. Høydeprofilen må tas vare på ved importen (D2), ikke bare summen.
2. **Kartfliser er låst i D, men åpne i E.** D «Kart»: «Kartverket-fliser (lyse i begge moduser)», og D/E sin Kreditering forutsetter Kartverket + OSM. E Foundation: kartbibliotek er «ikke et UX-vedtak». Researchen gir Kartverkets WMTS bare «middels tillit» og ber om å «Kontroller gjeldende adresse før bruk». Valget av fliser er ikke ført i memlog.
3. **`map-route` er ikke verifisert mot de flisene som faktisk velges.** D Kontrastmål: «3,4 mot plassholder, ikke verifisert mot ekte fliser». Hvis arkitekturen velger OSM-fliser (Leaflet-standard, D3), gjelder verken målingen eller antakelsen om lyse Kartverket-fliser. Delvis kjent (E Åpne punkter), men koblingen til flisvalget er ikke ført.
