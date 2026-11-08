---
title: Your Next Adventure — EXPERIENCE
status: final
created: 2026-11-06
updated: 2026-11-08
name: Your Next Adventure
description: Hvordan nettsiden virker — skjermer, tilstander, flyter, tilgjengelighet og tekster — for en rolig turkompis som gir nybegynnere ett turforslag om gangen i Oslo-området.
sources:
  - _bmad-output/planning-artifacts/prds/prd-G81-eriksen-2026-10-29/prd.md
  - _bmad-output/planning-artifacts/prds/prd-G81-eriksen-2026-10-29/addendum.md
  - _bmad-output/planning-artifacts/research/technical-turdata-oslomarka-2026-10-29/research.md
  - docs/product-brief-your-next-adventure-no.md
  - docs/tilbakemelding-product-brief.md
---

# Your Next Adventure — Experience Spine

## Foundation

- **Form:** en nettside på norsk (`<html lang="nb">`). **PC først** (referanseskjerm 1280 × 800) **med en enkel, stablet mobilutgave i v1** (se Responsive & Platform). PRD NFR-3 (44 × 44 px knapper, mobil uten sidelengs rulling) og WCAG 2.1 AA (NFR-4) gjelder fullt ut. Utenfor v1: app, GPS-posisjon og offline.
- **UI-system:** Ingen UI- eller kartbibliotek er valgt. Valget tas i arkitekturen.
- **Visuell identitet:** `DESIGN.md` eier hvordan det ser ut (tokens, komponenter, kontrast). Denne filen eier hvordan det virker. Tokens refereres som `{colors.primary}` og så videre.
- **Mørk modus:** med i v1 (PRD NFR-9, P2). Den følger innstillingen for lys eller mørk modus på enheten (`prefers-color-scheme`), og det finnes ingen egen bryter. Kartflisene og alt oppå dem forblir lyse.
- **Kuttrekkefølge** hvis tiden blir knapp (PRD §7.1, alle P2): (1) fremgang mot neste nivå i Historikk (FR-17.1), (2) mørk modus (NFR-9), (3) Fritekstønske (FR-11): feltet skjules helt, og Forklaringspanel mister setningen om at KI tolker ønsket, (4) Bekledningstips (FR-9 og FR-10): seksjonen forsvinner uten tomrom, (5) turtypepreferanse (FR-20): ingen egen visning forsvinner.
- **Turforslagets levetid:** Et turforslag lever bare i økten, det vil si fra et søk sendes til et nytt søk sendes eller fanen lukkes (PRD §3 og FR-7). Ny innlasting av samme fane beholder forslaget og listen over turer som er vist. Planlagte turer lagres ikke (PRD §9). Det finnes ingen delbar lenke til et turforslag.
- Ett turforslag om gangen. Konto er valgfri.

### Visuelle referanser

**Ved konflikt vinner DESIGN.md og EXPERIENCE.md over mocker og wireframes.**

| Fil | Viser | Status og kjente avvik |
|---|---|---|
| [mockups/key-sok.html](mockups/key-sok.html) | Søk, utfylt og med feil | Nøkkelskjerm. |
| [mockups/key-turforslag.html](mockups/key-turforslag.html) | Turforslag på desktop og mobil, med folden | Nøkkelskjerm. Nivåforklaringen og KI-begrunnelsen har eldre ordlyd. Mikrotekst gjelder. |
| [mockups/key-historikk.html](mockups/key-historikk.html) | Historikk etter registrering | Nøkkelskjerm. Fremgangslinjen har eldre ordlyd og to rader («2 av 3»), mens UJ-2 steg 3 gir den tredje registreringen og teksten for «målet nådd». |
| [wireframes/ia-2026-11-06.excalidraw](wireframes/ia-2026-11-06.excalidraw) | Skjermer, ruter og tilgang | Wireframe. |
| [wireframes/flow-ola-2026-11-06.excalidraw](wireframes/flow-ola-2026-11-06.excalidraw) | UJ-1, UJ-2, kjerneflyten (skjerm 1–6) og kanttilstandene A–G | Wireframe. Viser fornøydhet «4 av 5» der brukerreisen sier 5. |
| [mockups/direction-stille-kart.html](mockups/direction-stille-kart.html) | Retningen Stille kart, også tilstanden Uten værvarsel | Eldre referanse. Eldre Granskog-palett, eksemplet 4,2 km / 230 hm, «Finn tur» og «Historikk» i gjestemenyen, en utsiktsmarkør på kartet, tre turtypekort og bare desktop. |
| [mockups/direction-turkort.html](mockups/direction-turkort.html) | Retningen Turkort, også tilstanden Alle forslag er vist | Eldre referanse. Eldre Granskog-palett, eksemplet 4,2 km / 230 hm, søkeoverskriften «Når vil du på tur, og hvor lenge?», tre turtypekort og bare desktop. |
| [mockups/color-themes-2.html](mockups/color-themes-2.html) | Palettvariantene som ble vurdert | Eldre referanse. Fargene i DESIGN.md gjelder. |

Logg inn / Lag konto, Registrer gjennomført tur, Konto og Bekreft sletting har ingen mock. Skjermer uten mock bygges fra DESIGN.md, denne filen og wireframene.

## Information Architecture

Kart over skjermer, ruter og tilgang: [wireframes/ia-2026-11-06.excalidraw](wireframes/ia-2026-11-06.excalidraw). Alle sidetitler slutter på « – Your Next Adventure» (utelatt i tabellen).

| Skjerm | Tilgang | Nås fra | Formål | `h1` | Sidetittel (`<title>`) |
|---|---|---|---|---|---|
| Søk (forside) | Alle | Logo, «Finn tur», «Finn en ny tur», «Endre søk» (forhåndsutfylt) | Skjemaet møter brukeren direkte, uten intro-side. Mock: [mockups/key-sok.html](mockups/key-sok.html) (utfylt og med feil). | «Hvor lang tid har du?» | «Finn tur» |
| Turforslag | Alle | «Finn en tur», «Åpne som turforslag» i Historikk | Egen visning etter søk med Stille kart-oppsettet. Ett forslag om gangen. Mock: [mockups/key-turforslag.html](mockups/key-turforslag.html) (desktop og mobil). | Turnavnet, eller overskriften i Tilstandspanel | «{Turnavn} – Turforslag». Under lasting «Finner tur …». Med Tilstandspanel: panelets overskrift. |
| Logg inn / Lag konto | Alle (inngang til kontofunksjoner) | «Logg inn» i toppmenyen, eller en kontofunksjon brukt som gjest | Logg inn eller lag konto med e-post og passord. Turforslaget beholdes (FR-14). | «Logg inn» eller «Lag konto» | «Logg inn» / «Lag konto» |
| Registrer gjennomført tur | Kun innlogget | «Registrer gjennomført tur» fra Turforslag eller Historikk | Egen side, ikke dialog. Etter lagring: Historikk med suksessmelding. | «Registrer gjennomført tur» | «Registrer gjennomført tur: {Turnavn}» |
| Historikk | Kun innlogget | «Historikk» i toppmenyen | Tur, dato og vurdering. Brukt tid står sammen med estimert tid. Mock: [mockups/key-historikk.html](mockups/key-historikk.html) (etter registrering). | «Historikk» | «Historikk» |
| Konto | Kun innlogget | «Konto» i toppmenyen | E-post, personverntekst, «Logg ut» og «Slett konto». | «Konto» | «Konto» |
| Bekreft sletting | Kun innlogget | «Slett konto» på Konto | Egen side med nøktern bekreftelse, bekreftelsesknapp og Avbryt (FR-15). | «Vil du slette kontoen?» | «Slett konto» |

**Toppmeny:** Gjest ser logo og «Logg inn». Innlogget ser logo, «Finn tur», «Historikk» og «Konto». «Logg ut» står på Konto, ikke i menyen. Logoen fører alltid til Søk.

**Logg inn / Lag konto** er én rute med to visninger [ASSUMPTION]: «Logg inn» (standard) med lenken «Har du ikke konto? Lag konto», og «Lag konto» med lenken tilbake. Hver visning har én primærknapp: «Logg inn» eller «Lag konto og fortsett». Kontoopprettelse heter «Lag konto» i grensesnittet, så den ikke forveksles med «Registrer gjennomført tur» [ASSUMPTION].

**Ruter som krever konto:**

- En gjest som trykker «Registrer gjennomført tur», sendes til Logg inn / Lag konto og deretter **rett inn i registreringen av den turen**.
- En gjest som logger inn av andre grunner, kommer tilbake dit hen var, og turforslaget beholdes.
- Går en gjest direkte til Historikk eller Konto, sendes hen til innlogging og tilbake etterpå [ASSUMPTION].

Testbrukeren (FR-21) logger inn via vanlig innlogging og har ingen egen skjerm.

## Voice and Tone

Stemmen og den estetiske holdningen står i `DESIGN.md` under Brand & Style. Her står mikroteksten.

- **Personlig turkompis.** Tjenesten snakker i jeg-form og tiltaler brukeren med du. Den er varm, konkret og kort. **PRD-tekster i vi-form vises i jeg-form** i grensesnittet. Originalen står i kolonnen Kilde i Mikrotekst.
- **Sparsomt** med emoji og utropstegn. De eneste faste tegnene er ✦ i KI-merket, ↗ på lenker til andre nettsteder og 🎉 i fremgangslinjen når målet er nådd. Alle tre er `aria-hidden`. Lenker til andre nettsteder har i tillegg skjult tekst om hvor de går.
- **Nøktern i alvorlige øyeblikk.** Ved feilmeldinger, innlogging, personvern og sletting av konto er tonen rolig og saklig, uten emoji og uten spøk.
- **KI skal synes, men ikke overselges** (PRD §6). Reglene står i Component Patterns under KI-merke og Forklaringspanel. Tall (tid, lengde, nivå) settes alltid inn av systemet.
- **Personalisering forklares med konkrete regler**, for eksempel «Når du har gått tre grønne turer som føltes lette, foreslår jeg blå turer først neste gang du søker.» Teksten må aldri antyde at KI lærer, så «Neste tur blir enda mer din» er ikke lov.
- **Domeneord ordrett fra PRD:** Tur, Turforslag, Begrunnelse, Bekledningstips, Gjennomført tur, Historikk, Nivåtak, Sperre, Gjest, Bruker. Handlingen heter «registrere gjennomført tur», ikke «lagre». Turtypene er *marka*, *utsikt* og *topptur*, aldri «skogstur».
- **Faste formater:** «Grønn – lett», «ca. 1 t 35 min» med «pauser ikke inkludert» og «3,5 km totalt». Tur-retur og rundtur merkes alltid.
- **Bevisste navneforskjeller:** «Finn tur» er menypunktet, «Finn en tur» sender søket, og «Finn en ny tur» er handlingen på et turforslag fra historikken. Alle tre fører til Søk. «Slett konto» åpner bekreftelsen, og «Slett kontoen» sletter. «Registrer gjennomført tur» er både lenken til siden og sendeknappen på siden (PRD).

### Mikrotekst

Tabellen er hjemmet for all tekst i grensesnittet. Kolonnen Kilde sier hvor teksten kommer fra:

- «PRD»: teksten står ordrett i PRD-en.
- «PRD, jeg-form»: PRD-teksten er skrevet om etter stemmen, og originalen står i samme celle.
- «Godkjent (wireframe)», «Godkjent (mock)» og «Godkjent (memlog)»: teksten kommer fra en godkjent wireframe, mock eller memlog (beslutningsloggen fra UX-arbeidet). «Godkjent (mock, Turkort)» viser til den eldre retningsmocken Turkort.
- [ASSUMPTION]: teksten er en plassholder.

Har en rad flere tekster med ulik kilde, står kilden per tekst.

| Situasjon | Tekst i grensesnittet | Kilde |
|---|---|---|
| Overskrift på Søk | «Hvor lang tid har du?» | Godkjent (wireframe) |
| Ingress på Søk | «Fyll inn varighet og dato, så får du ett turforslag om gangen.» | Godkjent (wireframe) |
| Feltetiketter | «Varighet», «Dato», «Turtype», «Startpunkt (valgfritt)», «Fritekstønske (valgfritt)» | PRD (feltnavn) |
| Turtypevalg | «Alle turtyper» (forvalgt), «Marka», «Utsikt», «Topptur» | Godkjent (memlog) |
| Hjelpetekst | «1–8 timer», «Fra i dag til 30 dager frem», «0 / 200 tegn» | Godkjent (mock) |
| Plassholder i fritekst | «For eksempel "rundt 5 km" eller "forbi et vann"» | Godkjent (mock) |
| Hjelpetekst i fritekst | «Jeg prøver å ta hensyn til ønsket ditt.» | Godkjent (mock) |
| Startpunkt, standardvalg | «Alle startpunkt» | Godkjent (mock) |
| Hjelpetekst under Startpunkt | «Jeg har foreløpig bare turer i Oslo-området.» | PRD, jeg-form (FR-4: «turene dekker foreløpig bare Oslo-området») |
| Søkeknapp | «Finn en tur» | Godkjent (mock) |
| Søkeoppsummering | «Lørdag 7. nov. · 2 t · Utsikt» og «Endre søk» | Godkjent (mock) |
| Turforslag fra historikken | «Fra historikken din» | PRD (FR-17) |
| Turforslag fra historikken, over nivåtaket | «Denne turen er over nivået jeg foreslår for deg nå.» | PRD (FR-17) |
| Lasting | «Finner en tur med utsikt som passer 2 timer …», «Kart lastes …» | [ASSUMPTION] |
| Lasting, nytt forslag | «Finner et nytt forslag …» | [ASSUMPTION] |
| Startpunkt i Infokolonne | «Start: Granvannet p-plass» | Godkjent (memlog) |
| Turtype-treff | «{Turtype} – som du ba om», for eksempel «Utsikt – som du ba om» | Godkjent (mock) |
| Nivåforklaring | «Jeg har beregnet nivået etter Merkehåndbokas mal ut fra lengde og høydemeter. Terreng og føre er ikke vurdert.» | PRD (FR-6, jeg-form fra v1.1) |
| Estimert tid | «ca. 1 t 35 min (pauser ikke inkludert)» | PRD (formatet) |
| Knapper på turforslaget | «Nytt forslag», «Registrer gjennomført tur» | PRD |
| Knapp, turforslag fra historikken | «Finn en ny tur» | PRD (FR-17) |
| ut.no-lenke | «Se turen på ut.no ↗», skjult tillegg «(åpnes på ut.no)» | Godkjent (mock) |
| Begrunnelse (reservemalen) | «Turen tar ca. 2 t og har utsikt, som du ba om» | PRD (addendum, eksempel på reservemalen, FR-13) |
| Begrunnelse (KI, eksempel fra UJ-1) | KI skriver «Turen tar {tid}, så den passer innenfor {varighet}. Den har utsikt, som du ba om, og er {nivå}, som passer når du er ny.» Systemet setter inn tallene og nivået, så brukeren ser «Turen tar ca. 1 t 35 min, så den passer innenfor 2 timer. Den har utsikt, som du ba om, og er grønn, som passer når du er ny.» | Godkjent (mock), rettet etter PRD FR-12: plassholderne `{tid}`, `{varighet}`, `{lengde}` og `{nivå}` settes inn av systemet |
| Begrunnelse (personalisering) | «Du får en blå tur fordi de tre siste grønne turene var lette for deg.» (personaliseringssetning fra setningsmalen, lagt til av systemet) | PRD (FR-12) |
| Begrunnelse (sperre) | «Du får en grønn tur igjen fordi den siste blå turen føltes vanskelig.» | [ASSUMPTION] |
| Begrunnelse, turforslag fra historikken | «Du gikk denne turen 12. oktober og ga den 5 av 5.» | PRD (FR-17) |
| KI-merke / malmerke | «✦ Skrevet med KI» / «Begrunnelse fra mal» | PRD (FR-12) |
| Forklaringspanel | Utløser «Slik lager jeg forslaget». Innholdet står under Forklaringspanel i Component Patterns. | Utløser: PRD (FR-12). Ordlyden i innholdet: Godkjent (memlog) |
| Fritekst ignorert | «Jeg kunne ikke ta hensyn til ønsket ditt denne gangen» | PRD (FR-13, jeg-form fra v1.1) |
| Topptur passer ikke | «Toppturer krever mer tid enn du har oppgitt» | PRD |
| Topptur passer ikke, merke | «Utsikt i stedet for topptur» | [ASSUMPTION] |
| Nivåtak, tittel | «Ingen grønne turer passer søket» | [ASSUMPTION] |
| Nivåtak (gjest) | «Som ny bruker får du grønne turer. Lag konto og vurder turene dine, så tilpasser jeg forslagene etter hvordan turene kjentes for deg.» | PRD |
| Nivåtak (innlogget uten historikk) | «Som ny bruker får du grønne turer. Registrer og vurder turene du går, så tilpasser jeg forslagene etter hvordan turene kjentes for deg.» | [ASSUMPTION]. Budskapet står i PRD FR-8, og ordlyden er foreløpig (PRD §10). |
| Nivåtak (bruker med historikk) | «Akkurat nå foreslår jeg turer opp til grønt nivå, og ingen av dem passer søket.» | [ASSUMPTION] |
| Ingen treff | «Jeg fant ingen tur som passer søket ditt», «Prøv å endre søket:» | [ASSUMPTION] |
| Alle forslag er vist | «Du har sett alle turene som passer søket» | PRD |
| Alle forslag er vist, ingress | «Det var fire turer med utsikt som passer 2 timer.» / «Vil du prøve noe annet?» | Første: Godkjent (mock, Turkort). Andre: [ASSUMPTION] |
| Endringsforslag | «Prøv 3 timer», «Velg startpunkt», «Prøv marka», «Start fra første forslag igjen» | Godkjent (mock, Turkort) |
| Bekledningstips | De seks tipsene i FR-9, ordrett, for eksempel «Gode sko og litt mat og drikke» | PRD |
| Grunnlag for tips | «Etter værvarselet for startpunktet kl. 10–16.» | Godkjent (mock) |
| Uten værvarsel, for langt frem | «Jeg har ikke værvarsel for lørdag 28. november ennå, så jeg kan ikke gi bekledningstips. Varselet kommer omtrent 9–10 dager før.» | [ASSUMPTION] |
| Uten værvarsel, MET svarer ikke | «Jeg får ikke hentet værvarselet akkurat nå, så jeg kan ikke gi bekledningstips.» | [ASSUMPTION] |
| Kartfliser feiler | «Kartet kunne ikke lastes. Ruten er beskrevet i "Kartet i tekst".» og «Prøv igjen» | [ASSUMPTION] |
| Kart på berøringsskjerm | «Bruk to fingre for å flytte kartet» | [ASSUMPTION] |
| Kartknapper og lenke på kartet | «Zoom inn», «Zoom ut» (synlig som + og −), «Vis hele ruten», lenken «Kartet i tekst» | Godkjent (mock) |
| Uventet feil | «Noe gikk galt, og jeg fikk ikke hentet et forslag. Prøv igjen.» og «Prøv igjen» / «Endre søk» | [ASSUMPTION] |
| Forslaget finnes ikke lenger | «Turforslaget er ikke lenger tilgjengelig. Søk på nytt for å få et forslag.» | [ASSUMPTION] |
| Feil i søket | «Velg varighet» | Godkjent (mock) |
| Feil i søket, andre felt | «Velg en dato fra i dag til {dato om 30 dager}», «Ønsket kan ha høyst 200 tegn. Nå har det {n}.» | [ASSUMPTION] |
| Krav om konto | «Logg inn for å registrere», «Turforslaget er tatt vare på.», lenken «Tilbake til turforslaget» | [ASSUMPTION] |
| Knapper i Logg inn / Lag konto | «Logg inn», «Lag konto og fortsett» | «Logg inn»: Godkjent (memlog). «Lag konto og fortsett»: [ASSUMPTION] |
| Passordhjelp | «Minst 8 tegn», bryter «Vis passord» | «Minst 8 tegn»: Godkjent (wireframe). «Vis passord»: [ASSUMPTION] |
| Feil innlogging | «Feil e-post eller passord» | PRD |
| E-posten finnes fra før | «Kunne ikke lage konto – prøv å logge inn» | PRD (FR-14) |
| Feil i kontofelt | «Skriv inn e-postadressen din», «E-postadressen må ha med @, for eksempel ola@eksempel.no», «Passordet må ha minst 8 tegn» | [ASSUMPTION] |
| Innlogging utløpt | «Du er logget ut fordi det har gått lang tid. Logg inn igjen, så tar jeg vare på det du har fylt inn.» | [ASSUMPTION] |
| Registreringsskjema | «Alle fire felt er påkrevd.», «I dag eller tidligere», «10 min–24 t» | Godkjent (wireframe) |
| Fornøydhet, forklaring | «1 = ikke fornøyd, 5 = svært fornøyd» | [ASSUMPTION] |
| Feil ved registrering | «Velg datoen du gikk turen», «Datoen kan ikke være frem i tid», «Brukt tid må være mellom 10 minutter og 24 timer», «Velg hvor vanskelig turen føltes», «Velg hvor fornøyd du var» | [ASSUMPTION] |
| Registreringsknapper | «Registrer gjennomført tur», «Avbryt» | «Registrer gjennomført tur»: PRD. «Avbryt»: [ASSUMPTION] |
| Etter registrering | «Turen er registrert i historikken din.» (tittel i Melding (suksess), uten brødtekst) | Godkjent (mock) |
| Historikk, handlinger | «Åpne som turforslag», «Registrer gjennomført tur» | PRD |
| Historikk, under tabellen | «Nye søk prioriterer turer du ikke har gått.» | Godkjent (mock) |
| Historikktabell, kolonner | «Tur», «Dato», «Brukt tid», «Opplevd vanskelighet», «Fornøydhet» og skjult «Handlinger» | Godkjent (mock) |
| Historikktabell, formater | Dato «7. nov.», brukt tid «1 t 50 min» med «estimert ca. 1 t 35 min» under, vanskelighet «Lett» / «Moderat» / «Vanskelig», fornøydhet «5 av 5» | Godkjent (mock) |
| Fremgang (valgfri), underveis | «Du har gått 2 av 3 grønne turer som føltes lette. Etter én til foreslår jeg blå turer først neste gang du søker.» (tallet følger historikken) | Godkjent (memlog). Krav: PRD FR-17.1 |
| Fremgang (valgfri), målet nådd | «Tre grønne turer som føltes lette – godt gått! 🎉 Neste gang kan du få blå turer.» | Godkjent (memlog). Krav: PRD FR-17.1 |
| Tom historikk | «Du har ikke registrert noen turer ennå.» og «Finn tur» | [ASSUMPTION] |
| Personvern på Konto | «Jeg lagrer bare e-postadressen din, passordet ditt i sikret form og turene du registrerer. Jeg sporer ikke hvor du er, og KI-tjenesten får ingen personopplysninger om deg.» | Innhold: Godkjent (memlog). Ordlyd: [ASSUMPTION] |
| Logget ut | «Du er logget ut.» | [ASSUMPTION] |
| Bekreft sletting | Overskrift «Vil du slette kontoen?», tekst «All historikken din slettes for godt, og det kan ikke angres.» | Godkjent (memlog) |
| Sletteknapper | «Slett kontoen», «Avbryt» | [ASSUMPTION] |
| Kvittering etter sletting | «Kontoen din er slettet.» | [ASSUMPTION] |
| Kreditering | «© Kartverket · © OpenStreetMap contributors · Data fra MET Norge» | PRD (NFR-7). MET-formen: Godkjent (memlog) |

## Component Patterns

Her står hvordan komponentene oppfører seg. Det visuelle står i `DESIGN.md` under Components, med de samme navnene.

| Komponent | Brukes på | Regler for oppførsel |
|---|---|---|
| Toppmeny | Alle skjermer | Innholdet avhenger av om brukeren er gjest eller innlogget (se IA). `header` med `nav`. Det aktive punktet har `aria-current="page"`. Logoen fører til Søk. Menypunktene brytes til en ny linje når plassen ikke strekker til. Ingen hamburgermeny. |
| Primærknapp | Alle skjermer | Én per visning. Under innsending får den `aria-disabled="true"`, beholder fokus og ignorerer nye klikk, så dobbel innsending ikke gir dobbel handling (NFR-2). Enter i et skjema utløser den. |
| Sekundærknapp | Turforslag, Registrer gjennomført tur, Bekreft sletting | Alternativ handling. På turforslaget er «Nytt forslag» primær og «Registrer gjennomført tur» sekundær. |
| Fokusring | Alle skjermer | Vises ved tastaturfokus (`:focus-visible`) på alt man kan fokusere på, og fjernes aldri. På kartet brukes kartvarianten. |
| Skjemafelt | Søk, Logg inn / Lag konto, Registrer gjennomført tur | Etiketten er alltid synlig. Feltene valideres ved innsending og på serveren. Feilmeldingen står rett under feltet og over hjelpeteksten. Feilmelding og hjelpetekst kobles begge med `aria-describedby`, i den rekkefølgen (feil først), og feltet får `aria-invalid="true"`. Feilteksten sier hvordan feilen rettes (se Mikrotekst). Fokus flyttes til det første feltet med feil. Søk har **ingen feiloppsummering** øverst: feil ved feltet og fokusflyttingen er nok ([mockups/key-sok.html](mockups/key-sok.html), feiltilstanden). Kontrolltypene står i tabellen under. |
| Turtypekort | Søk | Ekte radiogruppe med fire valg: «Alle turtyper» (forvalgt), Marka, Utsikt og Topptur. Piltastene flytter valget, og alle valg kan nås med tastatur. Ordet «Valgt» har `aria-hidden="true"`, fordi tilstanden kommer fra radioknappen. |
| Valggruppe | Registrer gjennomført tur | Én radiogruppe for opplevd vanskelighet (lett / moderat / vanskelig) og én for fornøydhet (1–5). Begge har `fieldset` og `legend` og er påkrevd. Fornøydhet har forklaringen fra Mikrotekst («Fornøydhet, forklaring») koblet til gruppen, og 1 og 5 har synlig ankertekst. |
| Søkeoppsummering | Laster, Turforslag, tilstander | Viser søket som en linje, også under lasting. «Endre søk» går til Søk med skjemaet forhåndsutfylt. Ved turforslag fra historikken viser den «Fra historikken din» i stedet, uten «Endre søk». |
| Kart | Turforslag | Se Kart – oppførsel under tabellen. |
| Kreditering | Turforslag (på kartet) | Alltid synlig på kartet. Lenkene er understreket: Kartverket til Kartverkets lisensside, «OpenStreetMap contributors» (`lang="en"`) til openstreetmap.org/copyright og «Data fra MET Norge» til MET Norge. |
| Kartbeskrivelse | Turforslag | Overskrift «Kartet i tekst» (`h2`). Teksten **genereres fra turdata** og ikke av KI, med minst startpunktets navn, form, total lengde, høydemeter og laveste og høyeste punkt fra høydeprofilen. Eksempel med den oppdiktede eksempelturen: «Rundtur på 3,5 km totalt fra Granvannet p-plass. Ruten stiger ca. 130 høydemeter, fra 180 til 310 moh.» |
| Infokolonne | Turforslag | Den visuelle høyrekolonnen. Rekkefølgen står under Turforslag – rekkefølge og er lik på alle bredder. Meldinger om forslaget (topptur erstattet, fritekst ignorert) står rett etter turnavnet og Turtype-treff, så de leses rett etter `h1`. «Nytt forslag» er beskrevet under Interaction Primitives. |
| Turillustrasjon | Turforslag, Søk, Turoppsummering | Tegnes fra rutelinjen og høydeprofilen. Høydeprofilen beregnes fra høydedata når turdatabasen bygges. Ikke interaktiv. På turforslaget er den en `figure` med `figcaption` (for eksempel «Rundtur. Laveste punkt 180 moh, høyeste 310 moh.»), og SVG-en er `aria-hidden` fordi bildeteksten er komplett. På Søk er den bare pynt (`aria-hidden`) og har ingen bildetekst. |
| Nivåmerke | Turforslag, Turoppsummering, Historikktabell | Alltid farge og tekst. Den faste nivåforklaringen står ved siden av på turforslaget. Nivået beregnes av tjenesten, aldri av KI. |
| Turtype-treff | Turforslag | Vises bare når brukeren har valgt en bestemt turtype og turen har den. Treffet nevnes også i begrunnelsen. Når en topptur blir erstattet av en utsiktstur, står merket fra Mikrotekst («Topptur passer ikke, merke») i stedet. |
| Formmerke | Turforslag | «Rundtur» eller «Tur-retur». Vises alltid, sammen med linjen «Start: {startpunkt}». |
| Faktarute | Turforslag | Total lengde, høydemeter og estimert tid med «pauser ikke inkludert». Tallene kommer fra systemet, aldri fra KI. |
| Begrunnelse | Turforslag | Overskrift `h2` «Begrunnelse». Maks 300 tegn. Grensen gjelder hele begrunnelsen slik brukeren ser den, etter innsetting av verdier og med personaliseringssetningen. Overskrides grensen, brukes reservemalen (PRD FR-12, FR-13). Nevner varigheten, og turtypen og fritekstønsket hvis de er oppgitt. Reservemalen nevner aldri fritekstønsket. Har en personaliseringsregel påvirket valget, legger systemet til en personaliseringssetning fra setningsmalen (se Mikrotekst). Eksempelet fra UJ-1 i Mikrotekst er ikke fast tekst, men viser tonen og hva en KI-skrevet begrunnelse skal nevne. KI skriver aldri tall eller nivå. De står som plassholdere (`{tid}`, `{varighet}`, `{lengde}` og `{nivå}`) som systemet fyller inn (PRD FR-12). |
| KI-merke | Turforslag | Rett over Begrunnelse. Viser «✦ Skrevet med KI» når KI har skrevet begrunnelsen. Ved reserveløsning (FR-13), i testmodus uten API-nøkkel til KI-tjenesten og ved turforslag fra historikken viser det «Begrunnelse fra mal» i stedet. |
| Forklaringspanel | Turforslag | Utfellbar `<details>`/`<summary>` med utløseren «Slik lager jeg forslaget», lukket som standard. Innholdet sier i jeg-form: (1) Ruten, tiden og nivået kommer fra Kartverkets turdata og faste formler, ikke fra KI. (2) Tiden kan bomme med rundt 15 prosent, og nybegynnere bruker ofte lenger tid enn beregnet. (3) KI tolker ønsket ditt og skriver begrunnelsen, og den kan ta feil. |
| Bekledningstips | Turforslag | Overskrift `h2` «Bekledningstips for {dag}», grunnlaget i én linje og ett eller flere tips etter FR-9, ordrett. «Gode sko og litt mat og drikke» vises alltid. Mangler værvarsel, byttes listen ut med en Melding (info) under samme overskrift. Kuttes seksjonen, se kuttrekkefølgen i Foundation. |
| Melding | Alle skjermer | Info, advarsel, feil og suksess, alltid med ikon og tekst. En suksessmelding kan være bare en tittel når den sier alt (se Mikrotekst, «Etter registrering»). Den står der saken gjelder, aldri som en toast som forsvinner. Meldinger på samme side leses opp med `role="status"` / `role="alert"`. Meldinger som følger med en navigering, får fokus (se Accessibility Floor). |
| Tilstandspanel | Turforslag (ingen treff, nivåtak, alle vist) | Erstatter turinnholdet. Overskriften er `h1`. Det gir alltid neste steg: konkrete endringsforslag, «Endre søk», og ved «alle vist» også «Start fra første forslag igjen». «Prøv 3 timer» og «Prøv marka» kjører søket på nytt med én endring. «Velg startpunkt» går til det forhåndsutfylte skjemaet med fokus på Startpunkt. |
| Lasteindikator | Laster | Viser Søkeoppsummering med en gang, flaten der kartet kommer og en tekstlinje. Opplesing og `aria-busy`: se Accessibility Floor › Sidetitler og fokus. Ingen animasjon når `prefers-reduced-motion` er på. |
| Turoppsummering | Registrer gjennomført tur, Logg inn / Lag konto (ved krav om konto) | Viser hvilken tur det gjelder: navn, illustrasjon, nivå, form, lengde og estimert tid. Ikke interaktiv. |
| Historikktabell | Historikk | Ekte `<table>`, nyeste først, med én rad per registrering, også når samme tur er gått flere ganger (FR-19). Turnavnet er `<th scope="row">`. Handlingskolonnen har skjult overskrift «Handlinger», og handlingene har skjulte tillegg («– Granåsen rundt, 7. nov.»). Under bruddpunktet ruller tabellen sidelengs i egen beholder (`role="region"`, `aria-label="Historikk"`, `tabindex="0"`), aldri hele siden. Kolonner og formater: se Mikrotekst. Rekkefølgen på siden: DESIGN.md › Layout & Spacing › Historikk. → [mockups/key-historikk.html](mockups/key-historikk.html) |
| Slettebekreftelse | Bekreft sletting | Egen side. Bare en eksplisitt bekreftelsesknapp, ingen inntasting av e-post. «Slett kontoen» står ikke på samme sted som «Slett konto» på Konto, så et dobbeltklikk ikke sletter. «Avbryt» går tilbake til Konto. |

**Skjemafelt – kontrolltyper.** Native kontroller der det går.

| Felt | Kontroll | Tastatur og regler |
|---|---|---|
| Varighet | `<select>` med «Velg» og 1–8 t i halvtimessteg | Vanlig tastaturoppførsel for nedtrekksliste. Tom ved start (wireframe). |
| Dato (Søk) | `<select>` med de 31 aktuelle dagene, for eksempel «Lørdag 7. november» [ASSUMPTION] | I dag er forvalgt. Ingen egen kalenderwidget. |
| Turtype | Radiogruppe (Turtypekort) | Piltaster. «Alle turtyper» er forvalgt. |
| Startpunkt | `<select>` med «Alle startpunkt» først [ASSUMPTION] | Vanlig tastaturoppførsel for nedtrekksliste. |
| Fritekstønske | `<textarea>` med teller | Feltet stopper ikke inntastingen ved 200 tegn. Telleren viser «{n} / 200 tegn», og over 200 gir feil ved innsending. At grensen er passert, meldes én gang i en live-region med `aria-live="polite"`, ikke for hvert tastetrykk. Kuttes FR-11, se kuttrekkefølgen i Foundation. |
| Dato (registrering) | `<input type="date">` med `max` = i dag [ASSUMPTION] | I dag er forvalgt. |
| Brukt tid | `fieldset` «Brukt tid» med to tallfelt, «Timer» og «Minutter» (`inputmode="numeric"`) [ASSUMPTION] | Hjelpetekst «10 min–24 t». |
| Opplevd vanskelighet, Fornøydhet | Radiogrupper (Valggruppe) | Piltaster. |
| E-post | `type="email"`, `autocomplete="email"` | |
| Passord | `type="password"`, `autocomplete="current-password"` ved innlogging og `new-password` ved ny konto | Bryteren «Vis passord» [ASSUMPTION]. |

**Kart – oppførsel.**

| Inndata | Kartet | Siden |
|---|---|---|
| Tab | Tab-stopp i plasseringsrekkefølge: «Kartet i tekst», «Vis hele ruten», «Zoom inn», «Zoom ut» og lenkene i Kreditering. Kartflaten er også et tab-stopp (`tabindex="0"`). | Tab går videre ut av kartet. |
| Piltaster, + og − (kartflaten har fokus) | Piltastene flytter kartet, + og − zoomer. | – |
| Rullehjul | – | Ruller. |
| Ctrl (eller Cmd) + rullehjul | Zoomer. | – |
| Én finger på berøringsskjerm | Viser hintet fra Mikrotekst («Kart på berøringsskjerm»). | Ruller. |
| To fingre på berøringsskjerm | Flytter og zoomer. | – |
| Nytt forslag | Flyttes til den nye ruten, uten animasjon når `prefers-reduced-motion` er på. | – |

- Kartet er `role="region"` med `aria-label="Kart over {turnavn}"`. Den synlige lenken «Kartet i tekst» oppe til venstre på kartet hopper til Kartbeskrivelse. «Vis hele ruten» står til venstre for zoomknappene oppe til høyre ([mockups/key-turforslag.html](mockups/key-turforslag.html)).
- Kartbibliotekets engelske standardtekster byttes til norsk, og biblioteket får ingen egne fokusstopp eller reklamelenker.
- Markørene er pynt og kan ikke få fokus. Kartbeskrivelse gir den samme informasjonen.
- **Kartet holder aldri på tastaturfokus.**
- **Kartet fanger aldri siderullingen.**

**Turforslag – rekkefølge.** DOM-rekkefølgen er den samme på alle bredder, så Tab, skjermleser og mobil følger den. På desktop plasseres Kart i venstre kolonne med CSS grid. Mocken viser mobil (375 px) og desktop (1280 px) side om side, med denne rekkefølgen: [mockups/key-turforslag.html](mockups/key-turforslag.html).

1. Søkeoppsummering (eller «Fra historikken din»)
2. Turnavn (`h1`), Nivåmerke med forklaring og Turtype-treff
3. Meldinger om forslaget (topptur erstattet, fritekst ignorert)
4. Nøkkeltall: Formmerke, «Start: …», Faktarute og ut.no-lenke
5. Turillustrasjon
6. Kart med Kreditering
7. KI-merke, Begrunnelse og Forklaringspanel
8. Bekledningstips
9. Knappene «Nytt forslag» og «Registrer gjennomført tur» (full bredde på mobil)
10. Kartbeskrivelse («Kartet i tekst»)

## State Patterns

Alle tilstandene fra PRD §6 er dekket. Hver tilstand viser enten et turforslag eller en forklaring med neste steg (NFR-2). Kolonnen «Skisse» viser til skjerm 1–6 og kanttilstand A–G i [wireframes/flow-ola-2026-11-06.excalidraw](wireframes/flow-ola-2026-11-06.excalidraw). Mockene står i Foundation › Visuelle referanser. Tekstene står i Mikrotekst.

**Søk**

| Tilstand | Skisse | Behandling |
|---|---|---|
| Første visning | 1 | Dato er i dag, Varighet er tom («Velg»), «Alle turtyper» er valgt og Startpunkt er «Alle startpunkt». |
| Forhåndsutfylt | – | Etter «Endre søk» er alle feltene fylt ut fra forrige søk. |
| Feil i skjemaet (FR-4) | A | Søket sendes ikke. Feilen står rett under feltet med «!» og tekst, over hjelpeteksten, og fokus går til det første feilfeltet. Ingen feiloppsummering øverst. |
| Logget ut (som gjest) | – | Melding (suksess) fra Mikrotekst («Logget ut») får fokus. Toppmenyen viser bare «Logg inn». |
| Konto slettet (som gjest) | – | Brukeren er logget ut. Melding (suksess) fra Mikrotekst («Kvittering etter sletting») får fokus. |

**Turforslag**

| Tilstand | Skisse | Behandling |
|---|---|---|
| Laster (§6) | 2 | Lasteindikator: Søkeoppsummering, tom kartflate og lastetekst. |
| Turforslag vist | 3 | Stille kart-oppsettet. Foldmålet (det som skal synes uten rulling) står i DESIGN.md under Layout & Spacing. |
| Henter nytt forslag (FR-7) | – | Det gamle forslaget står dempet, og «Nytt forslag» beholder fokus. Opplesing: se Accessibility Floor › Sidetitler og fokus. |
| Alle turtyper | – | Turtype-treff vises ikke. Begrunnelsen nevner varigheten. |
| Uten ut.no-lenke | – | Lenken skjules. |
| Personalisering påvirket valget | – | Systemet legger til personaliseringssetningen fra setningsmalen, som nevner regelen konkret (FR-12). Teksten ved sperre er foreløpig (se Åpne punkter). |
| Topptur passer ikke (FR-8) | G | En utsiktstur vises med merket fra Mikrotekst og Melding (advarsel) rett etter turnavnet. Passer heller ingen utsiktstur, gjelder Ingen treff. |
| Bare turer over nivåtaket (FR-8) | C | Tilstandspanel uten tur. Tre tekstvarianter: gjest (PRD-teksten med lenken «Lag konto»), innlogget uten historikk (uten «Lag konto») og bruker med historikk. Neste steg er «Endre søk». |
| Ingen treff (FR-8) | B | Tilstandspanel med konkrete endringsforslag: lengre varighet, et annet startpunkt og en annen turtype. |
| Alle forslag er vist (FR-7) | D | Tilstandspanel med antall turer som fantes, konkrete endringsforslag, «Start fra første forslag igjen» og «Endre søk». Ingen tur vises to ganger i samme økt, med mindre brukeren velger «Start fra første forslag igjen». |
| Uten værvarsel (FR-10) | E | Forslaget vises, men Bekledningstips er byttet ut med en Melding (info). To varianter: datoen er for langt frem, eller MET svarer ikke. |
| Reserveløsning (FR-13) | F | Begrunnelsen lages fra reservemalen, og KI-merket viser «Begrunnelse fra mal». Har brukeren skrevet et fritekstønske, står Melding (info) om det rett etter turnavnet. Testmodus uten nøkkel ser lik ut. |
| Turforslag fra historikken (FR-17) | – | «Fra historikken din» i stedet for Søkeoppsummering. Kart, illustrasjon og tall som vanlig. Ingen Turtype-treff, fordi det ikke finnes et søk med valgt turtype (FR-6). Bekledningstips for i dag. Begrunnelsen er en fast mal uten KI og trenger ikke nevne varigheten, og KI-merket viser «Begrunnelse fra mal». Økten endres ikke (FR-7). «Nytt forslag» er byttet ut med «Finn en ny tur», som går til Søk. Er turen over det nåværende nivåtaket, vises den likevel, med Melding (info) fra Mikrotekst («Turforslag fra historikken, over nivåtaket») rett etter turnavnet (PRD FR-17). |
| Ny innlasting av fanen | – | Samme forslag og samme liste over viste turer. Økten varer til et nytt søk sendes eller fanen lukkes (PRD §3). |
| Fanen er lukket, eller adressen er åpnet direkte | – | Det finnes ikke noe forslag. Søk vises med Melding (info) fra Mikrotekst («Forslaget finnes ikke lenger»). |
| Kartfliser lastes ikke | – | Kartflaten viser Melding (info) med «Prøv igjen» og lenke til Kartbeskrivelse. Turillustrasjon, Faktarute og Kartbeskrivelse vises uansett. |

**Logg inn / Lag konto**

| Tilstand | Skisse | Behandling |
|---|---|---|
| Gjest møter krav om konto (FR-14) | 4 | Turoppsummering og tekstene fra Mikrotekst («Krav om konto»). Etterpå går gjesten rett inn i registreringen av turen. |
| Første visning | 4 | Visningen «Logg inn» med e-post, passord, primærknappen «Logg inn» og lenken «Lag konto». |
| Feil innlogging | – | Melding (feil). Den sier ikke hvilket felt som er feil. |
| E-posten finnes fra før | – | Melding (feil) med PRD-teksten. |
| Passord for kort | – | Feilmelding ved feltet. Hjelpeteksten «Minst 8 tegn» vises alltid. |
| Innlogging utløpt (sider som krever konto) | – | Brukeren sendes til Logg inn og tilbake til samme side etterpå. Utfylte felt beholdes [ASSUMPTION]. |

**Registrer gjennomført tur**

| Tilstand | Skisse | Behandling |
|---|---|---|
| Første visning | 5 | Turoppsummering øverst. Dato er i dag, og de andre feltene er tomme. «Alle fire felt er påkrevd.» vises. |
| Feil i skjemaet (FR-16) | – | Feilen står ved feltet, og ingenting lagres. |

**Historikk**

| Tilstand | Skisse | Behandling |
|---|---|---|
| Registrert | 6 | Melding (suksess) står først rett under `h1` og får fokus. Den kan være bare tittelen. Så kommer fremgangslinjen (hvis den finnes) og tabellen. Den nye raden står øverst. |
| Fremgang mot neste nivå (FR-17.1, valgfri) | – | Én linje under `h1`, eller under suksessmeldingen når den vises, om hvor brukeren står mot neste nivå. To varianter, underveis og målet nådd (se Mikrotekst). Linjen er vanlig tekst og leses ikke opp av seg selv. Står først i kuttrekkefølgen (Foundation). |
| Tom historikk | – | Tilstandspanel-mønsteret med forklaring og «Finn tur». |
| Laster / feil ved lasting (også Konto) | – | Samme rolige lastemønster som Turforslag. Ved feil: Melding (feil) med «Prøv igjen». |

**Konto og Bekreft sletting**

| Tilstand | Skisse | Behandling |
|---|---|---|
| Standard (Konto) | – | E-post, personverntekst, «Logg ut» og «Slett konto». |
| Bekreft sletting (FR-15) | – | Egen side med teksten fra Mikrotekst, «Slett kontoen» og «Avbryt». |
| Sletting feiler | – | Melding (feil) med «Prøv igjen». Kontoen er urørt. |

**Alle skjermer**

| Tilstand | Skisse | Behandling |
|---|---|---|
| Sender | – | Se Primærknapp. |
| Uventet feil eller nettverksbrudd (NFR-2) | – | Melding (feil) i nøktern tone med neste steg («Prøv igjen» eller «Endre søk»). Utfylte felt beholdes. |

## Interaction Primitives

- **Mus, tastatur og berøring er like gode.** Hele kjerneflyten kan gjøres med tastatur: søk, se forslaget, «Nytt forslag», logg inn eller lag konto, registrer gjennomført tur, Historikk, logg ut og slett konto.
- **Tab** følger DOM-rekkefølgen, som er lik på alle bredder (se Turforslag – rekkefølge). På desktop gir det ett bevisst hopp inn i kartet til venstre og tilbake til Infokolonne.
- **Enter** sender skjemaer. **Piltastene** flytter mellom valgene i Turtypekort og Valggruppe. **Mellomrom** og **Enter** åpner og lukker Forklaringspanel.
- **Ett forslag om gangen.** «Nytt forslag» bytter innholdet på stedet uten å laste siden på nytt. Fokus og opplesing står i Accessibility Floor › Sidetitler og fokus. Ingen lister med mange turer, ingen karuseller og ingen uendelig rulling.
- **Sider fremfor dialoger.** Registrer gjennomført tur og Bekreft sletting er egne sider. Det finnes ingen modale dialoger i kjerneflyten.
- **Ingen bekreftelse unntatt ved sletting.** Bare sletting av konto spør «er du sikker?».
- **Nettleserens tilbakeknapp** virker mellom alle visninger (fokus: se Accessibility Floor). «Endre søk» gir det samme som Tilbake fra Turforslag [ASSUMPTION].
- **Bevegelse** er rolig og kort. Alt slås av ved `prefers-reduced-motion`.
- **Ikke lov:** informasjon som bare finnes ved hover, fokusfeller eller rullefeller i kartet, toasts som forsvinner før de er lest, og automatiske omdirigeringer med tidsur.

## Accessibility Floor

Her står kravene til oppførsel. Listen er sjekklisten for SM-4. Kontrastmålene står i `DESIGN.md` under Colors.

- **WCAG 2.1 AA** er målet (NFR-4). Det verifiseres med et automatisk verktøy, en manuell sjekkliste og en manuell test av mobilvisningen (SM-4).
- **Reflow:** Alt innhold virker uten sidelengs rulling ved 320 CSS px bredde (400 % zoom på 1280 px). Bare kartet og Historikktabell kan rulle i egen beholder.
- **Tekst:** 200 % tekstzoom og tekstavstand etter WCAG 1.4.12 klipper eller overlapper ingenting. Det finnes ingen fast foldhøyde.
- **Tastatur:** se Interaction Primitives og Kart – oppførsel. **Fokusring** er alltid synlig, og kartet har en tekstbeskrivelse (**Kartbeskrivelse**, FR-6).
- **Berøring:** Alt man kan trykke på utenfor løpende tekst, er minst 44 × 44 px (NFR-3).
- **Feil:** Feilmeldinger er koblet til feltet (`aria-describedby`), leses opp og sier hvordan feilen rettes.
- **Aldri bare farge:** Nivå har alltid tekst. Status har ikon og tekst. Lenker i løpende tekst er understreket. Valgt Turtypekort viser «Valgt», og valgt segment i Valggruppe har en hake.
- **Skjema:** Alle felt har synlige etiketter (FR-4). Grupper bruker `fieldset` og `legend`. E-post og passord har `autocomplete`. Plassholdere står i `{colors.text-muted}`.
- **Sidetitler og fokus:** Ved hver visningsendring (også «Nytt forslag» og Tilstandspanel) settes `document.title` etter IA-tabellen, og fokus flyttes til visningens `h1` (`tabindex="-1"`). Nettleserens tilbakeknapp gir fokus til elementet som startet overgangen, eller til `h1`. Mens et forslag hentes, har visningen `aria-busy="true"`, og lastemeldingen leses opp i en live-region med `aria-live="polite"` **utenfor** den beholderen. Selve byttet meldes ikke i noen live-region, så skjermlesere får én kanal.
- **Meldinger etter navigering:** Når en navigering har en melding med seg (registrert, logget ut, konto slettet, turforslaget ikke lenger tilgjengelig), står meldingen rett under `h1` og får fokus i stedet for `h1` (`tabindex="-1"`). Meldingen leses ikke i tillegg opp i en live-region.
- **Bevegelse:** `prefers-reduced-motion` respekteres, også i kartet.
- **Andre steder:** språk (`lang`) står i Foundation og Kreditering, glyfer og lenker til andre nettsteder i Voice and Tone, og Turillustrasjon i Component Patterns.

**Overskrifter og landemerker.** Hver visning har `header` med `nav` (Toppmeny) og én `main` som rommer hele visningen, også kart og Infokolonne. Turforslaget er ikke `aside`. Kartet er `region`. `h1` per skjerm står i IA-tabellen. `h2` finnes bare på Turforslag («Begrunnelse», «Bekledningstips for {dag}», «Kartet i tekst») og Konto («Personvern» [ASSUMPTION]).

## Key Flows

Wireframe av UJ-1 og UJ-2 med kanttilstander: [wireframes/flow-ola-2026-11-06.excalidraw](wireframes/flow-ola-2026-11-06.excalidraw). Eksempelturen «Granåsen rundt» med start på «Granvannet p-plass» er oppdiktet: rundtur, 3,5 km totalt, ca. 130 høydemeter, ca. 1 t 35 min, «Grønn – lett».

### UJ-1. Ola tar en spontan tur en fin dag, uten konto (desktop-tilpasset)

*Ola sitter i sofaen på PC-en og vil på tur til helgen. Han er ikke turvant, kjenner ikke marka godt og vil ha en enkel måte å få forslag på. Han er gjest.*

1. Ola åpner nettsiden. Søkeskjemaet møter ham med en gang under «Hvor lang tid har du?».
2. Han velger Varighet «2 timer» og Dato «Lørdag 7. november». Under Turtype flytter han valget fra «Alle turtyper» til **Utsikt**, som viser «Valgt». Startpunkt og Fritekstønske hopper han over. Steg 1–2: [mockups/key-sok.html](mockups/key-sok.html).
3. Han trykker «Finn en tur». Lastevisningen viser «Lørdag 7. nov. · 2 t · Utsikt» med en gang.
4. Turforslaget kommer: «Granåsen rundt», «Grønn – lett» med forklaringen, «Utsikt – som du ba om», «Rundtur», «Start: Granvannet p-plass», «3,5 km totalt», «ca. 130 høydemeter» og «ca. 1 t 35 min (pauser ikke inkludert)».
5. **Klimaks:** Uten å rulle ser Ola tre ting samtidig: den lille tegningen av runden og høydeprofilen, kartet og merket «Utsikt – som du ba om». Begrunnelsen under «✦ Skrevet med KI» sier det samme med egne ord, for eksempel «Turen tar ca. 1 t 35 min, så den passer innenfor 2 timer. Den har utsikt, som du ba om, og er grønn, som passer når du er ny.» Tiden, varigheten og nivået er satt inn av systemet (Mikrotekst, «Begrunnelse (KI, eksempel fra UJ-1)»). Kombinasjonen gjør at han tenker: *«Ja, den tar jeg.»* Steg 4–5, med folden: [mockups/key-turforslag.html](mockups/key-turforslag.html).
6. Han leser bekledningstipsene for lørdag og ser at «Se turen på ut.no» finnes hvis han vil vite mer.
7. Han vil kunne registrere turen etterpå, så han trykker «Logg inn», velger «Lag konto» og lager konto med e-post og passord. Han kommer tilbake til det samme turforslaget (FR-14), og toppmenyen viser nå «Finn tur», «Historikk» og «Konto». Fanen lar han stå åpen.

**Kanttilfelle (PRD):** Hadde Ola bedt om topptur, og ingen topptur passet innenfor varigheten, ville han fått en utsiktstur og meldingen «Toppturer krever mer tid enn du har oppgitt».

**Feilveier:**

- Han glemmer Varighet. «Velg varighet» står under feltet, fokus går dit, og søket sendes ikke ([mockups/key-sok.html](mockups/key-sok.html), feiltilstanden).
- Ingen tur passer. Han får tre konkrete endringsforslag.
- Bare blå turer eller vanskeligere passer. Han får nivåtakmeldingen for gjester.
- Han har bladd gjennom alle turene. Han får «Du har sett alle turene som passer søket» med konkrete endringsforslag.
- Datoen er mer enn 9–10 dager frem. Forslaget vises uten bekledningstips og med en forklaring.
- KI er nede, eller nøkkelen mangler. Han får «Begrunnelse fra mal».
- E-posten er allerede registrert. Han får «Kunne ikke lage konto – prøv å logge inn» og logger inn i stedet.

#### Delflyt: Nytt forslag (FR-7)

1. Ola trykker «Nytt forslag». Knappen beholder fokus, og «Finner et nytt forslag …» leses opp mens det gamle forslaget står dempet.
2. Det nye forslaget erstatter innholdet på stedet. Sidetittelen oppdateres, fokus går til det nye turnavnet, og kartet viser den nye ruten.
3. Etter det siste forslaget kommer Tilstandspanel «Du har sett alle turene som passer søket», og fokus går til overskriften.
4. «Start fra første forslag igjen» viser det første forslaget igjen.

### UJ-2. Ola kommer tilbake og får bedre forslag (desktop-tilpasset)

*Lørdag ettermiddag, rett etter turen, hjemme på PC-en. Ola laget konto i UJ-1 og har registrert to lette grønne turer fra før. Fanen med turforslaget er fortsatt åpen.*

1. Ola trykker «Registrer gjennomført tur» på turforslaget for Granåsen rundt.
2. Han kommer rett inn i Registrer gjennomført tur. Der oppgir han dato (i dag), brukt tid «1 t 50 min», opplevd vanskelighet «lett» og fornøydhet 5, og trykker «Registrer gjennomført tur».
3. Han lander i Historikk. Fokus står på suksessmeldingen «Turen er registrert i historikken din.», så den leses opp. Under den står fremgangslinjen. Dette er hans tredje grønne tur som føltes lett, så linjen viser «Tre grønne turer som føltes lette – godt gått! 🎉 Neste gang kan du få blå turer.» Den nye raden står øverst: «Granåsen rundt» med «Grønn – lett» under, «7. nov.», «1 t 50 min» med «estimert ca. 1 t 35 min» under, «Lett» og «5 av 5». Oppsettet: [mockups/key-historikk.html](mockups/key-historikk.html) (mocken viser underveis-varianten).
4. Han trykker «Finn tur» og søker igjen. Nivåtaket er nettopp hevet, så blå turer kommer først i dette søket (PRD FR-5). Forslaget er «Blå – moderat», og begrunnelsen sier: «Du får en blå tur fordi de tre siste grønne turene var lette for deg.» Hadde han heller villet ha en lett tur, kunne han skrevet «helst en lett tur» i Fritekstønske eller trykket «Nytt forslag», som også gir grønne turer.
5. **Klimaks:** Ola ser at siden tar hensyn til ham, og han vet nøyaktig hvorfor. Regelen står i klartekst og er ikke et vagt løfte om «læring».
6. Senere åpner han favoritturen fra Historikk med «Åpne som turforslag». Den vises som turforslag fra historikken under «Fra historikken din» med begrunnelsen «Du gikk denne turen 12. oktober og ga den 5 av 5.» og bekledningstips for i dag.

**Feilveier:**

- Han har lukket fanen. Forslaget er borte, så han søker på nytt med samme søk og blar til Granåsen rundt.
- Han er logget ut. Han logger inn og kommer tilbake. Feil passord gir «Feil e-post eller passord».
- Han setter brukt tid til 5 min eller velger en dato frem i tid. Feilen står ved feltet, og ingenting lagres.
- Han dobbeltklikker «Registrer gjennomført tur». Det blir bare én registrering.

### UJ-3. Ola sletter kontoen (lagt til i UX)

*Ola vil ikke lenger bruke tjenesten.*

1. Han er innlogget og går til «Konto» i toppmenyen.
2. Han trykker «Slett konto».
3. Siden Bekreft sletting viser i nøktern tone «Vil du slette kontoen?» og «All historikken din slettes for godt, og det kan ikke angres.» Under står «Slett kontoen» og «Avbryt». Han skriver ikke inn e-posten.
4. Han bekrefter.
5. **Klimaks:** Han er logget ut og står på Søk som gjest. Kvitteringen «Kontoen din er slettet.» har fokus og leses opp. Toppmenyen viser bare «Logg inn». Han ser tydelig at alt er borte.

**Feilveier:**

- Han angrer og trykker «Avbryt». Han kommer tilbake til Konto, og ingenting er endret.
- Slettingen feiler på serveren. Han får Melding (feil) med neste steg, og kontoen er urørt.

V1 har bare full kontosletting (FR-15). Enkeltturer kan ikke slettes.

## Inspiration & Anti-patterns

- **Hentet fra UT.no:** ryddig oppsett og fine illustrasjoner av turene, forenklet og ikke kopiert. Vi tegner egne illustrasjoner fra data og bruker ingen fotografier eller bilder fra UT.no.
- **Hentet fra et godt turkart (Stille kart):** kartet først, en rolig Infokolonne og ett tydelig valg.
- **Hentet fra en turbok (Turkort):** serif-overskrifter, illustrerte turtypekort og tilstander som foreslår hva du kan endre.
- **Forkastet: retningen «Rolig oversikt»**, med søket i en sidestolpe og et tett oppsett.
- **Forkastet: filtrering i lister og mange treff samtidig** (slik som på ut.no, AllTrails og Google Maps). Produktet gir ett forslag om gangen med en begrunnelse.
- **Forkastet: utsiktsmarkør på kartet og skrevet rutebeskrivelse per tur**, fordi turdataene ikke har utsiktspunkter eller beskrivelser.

## Responsive & Platform

PC først, med en enkel, stablet mobilutgave i v1. Bredder og flytende regler står i DESIGN.md under Layout & Spacing.

| Bredde | Oppførsel |
|---|---|
| ≥ 1280 px (referanse) | Turforslaget har to kolonner: kart til venstre og Infokolonne til høyre. Foldmålet gjelder. |
| ca. 720–1279 px | To kolonner. Kartet krymper først, deretter Infokolonne. |
| < ca. 720 px (mobil, og 200–400 % zoom) | Én kolonne. Søk, Tilstandspanel og alle skjemaer stables. Knappene på turforslaget fyller hele bredden. |

**Smal skjerm og berøring.** På mobil står kartet innenfor sidemargen, ca. 60 % av skjermhøyden, så siden kan rulles med én finger ved siden av kartet. Øvrige regler: trykkflater og reflow i Accessibility Floor, kart i Kart – oppførsel, Toppmeny og Historikktabell i Component Patterns, Søk-oppsettet i DESIGN.md › Layout & Spacing.

## Avvik fra PRD

Disse avvikene fra PRD v1.0 ble tatt inn i PRD v1.1 (2026-11-07). Listen står igjen som sporing, og hvert punkt viser hvor i PRD-en det står nå. Et punkt som ikke er løst i PRD-en, er merket «Åpent».

1. **UJ-1: Grønn-nivået stemmer ikke.** UJ-1 viser «tur-retur, 7,2 km totalt … Grønn – lett», men FR-2 sier at Grønn er under 5 km. Eksemplet må rettes. *Tatt inn i PRD v1.1 (UJ-1: rundtur, 3,5 km totalt).*
2. **UJ-1 og UJ-2 er skrevet om.** Ola planlegger på PC i sofaen (2 t, lørdag, utsikt) i stedet for på mobilen på vei ut. Han lager konto på slutten av UJ-1, registrerer turen rett etter at han har gått den, og søker på nytt hvis fanen er lukket. *Tatt inn i PRD v1.1 (UJ-1, UJ-2, feilveiene i §2.3).*
3. **UJ-2 komprimerer «etter noen turer».** Etter FR-19 krever en blå tur tre registrerte grønne turer vurdert lett. Brukerreisen forutsetter at to av dem var registrert fra før, så registreringen i UJ-2 steg 2 er den tredje. *Tatt inn i PRD v1.1 (UJ-2, FR-19).*
4. **UJ-3 (slett konto) er ny.** Den fantes ikke i PRD-en. *Tatt inn i PRD v1.1 (UJ-3, FR-15).*
5. **PRD-tekster i jeg-form.** Tekster i vi-form vises i jeg-form (originalene står i kolonnen Kilde i Mikrotekst). PRD-en bør få jeg-formen, eller en regel om at stemmen er jeg-form. *Tatt inn i PRD v1.1 (§6 Stemme og tone, jeg-form i FR-6, FR-13 og FR-17).*
6. **Skjermnavn.** PRD §6 kaller skjermen «logg inn / registrer». Her heter den Logg inn / Lag konto, så kontoopprettelse ikke forveksles med «Registrer gjennomført tur». *Tatt inn i PRD v1.1 (§6).*
7. **«Åpne som turforslag» fra Historikk (FR-17)** avviker fra FR-7, FR-9 og FR-12, blant annet nevner begrunnelsen ikke varigheten. Se State Patterns › Turforslag fra historikken. *Tatt inn i PRD v1.1 (§3 Turforslag fra historikken, FR-17).*
8. **Turforslaget lever bare i økten.** Økten varer til fanen lukkes, ikke «til siden lastes på nytt» (§3). Se Foundation. *Tatt inn i PRD v1.1 (§3 Økt, FR-7).*
9. **«Alle turtyper»** er et eget, forvalgt valg i Turtype (FR-4), så brukeren kan gå tilbake til alle turtyper med tastatur (en radiogruppe kan ellers ikke nullstilles). *Tatt inn i PRD v1.1 (FR-4).*
10. **Startpunktets navn** står i Infokolonne («Start: …»). Det er et tillegg til FR-6. *Tatt inn i PRD v1.1 (FR-6).*
11. **Personverntekst på Konto** gjør NFR-5 synlig (se Mikrotekst). *Tatt inn i PRD v1.1 (NFR-5).*
12. **Nivåtak (FR-8):** Innloggede uten historikk og brukere med historikk får egne tekster (se Mikrotekst). FR-8 ga samme tekst til gjester og brukere uten historikk. *Tatt inn i PRD v1.1 (FR-8). Ordlyden er foreløpig (PRD §10).*
13. **Turdata:** Høydeprofilen må beregnes fra høydedata og lagres når turdatabasen bygges, og startpunktets navn må lagres. Addendum-feltene (`kilde`, `lisens`, `lengde_km` …) har bare totalverdier, ikke høydeprofil. Utsiktspunkt og skrevet rutebeskrivelse trengs ikke. *Tatt inn i PRD v1.1 (§3 Tur, FR-1 og addendum: `hoydeprofil`, `startpunkt`).*
14. **Tillegg som ikke sto i PRD-en:** mørk modus, KI-merke, Forklaringspanel med usikkerhetssetningen om tid og valgfri fremgang mot neste nivå i Historikk. Kuttrekkefølgen, også for FR-11, står i Foundation. *Tatt inn i PRD v1.1 (NFR-9, FR-12, FR-17.1 og kuttrekkefølgen i §7.1).*
15. **Tekster PRD-en ikke gir:** uten værvarsel, bekreftelse ved sletting, nivåtak, lasting, feilmeldinger med forslag til retting, tom historikk og innlogging utløpt (se Mikrotekst). *Tatt inn i PRD v1.1 (§0 og §6: Mikrotekst eier ordlyden, bekreftelsessiden i FR-15). Ordlyden som er merket som antakelse, er foreløpig (PRD §10).*
16. **Wireframes i §6:** PRD §6 skal vise til `wireframes/ia-2026-11-06.excalidraw` og `wireframes/flow-ola-2026-11-06.excalidraw`. *Tatt inn i PRD v1.1 (§6).*

## Åpne punkter

| Punkt | Avklares i | Blokkerer |
|---|---|---|
| **Kartfliser og målinger.** Flis-kilden (Kartverket topo eller OSM) velges i arkitekturen. Før valget godkjennes, må `{colors.map-route}`, `{colors.map-marker-start}` og `{colors.map-focus-ring}` måles mot ekte fliser i skog, myr, vann og bebyggelse. Zoomgrensene for Kartverkets detaljerte kartdata (zoom 12–20) må også avklares. **Delvis løst 2026-11-08:** flisene er Kartverket topo, zoom høyst 18 (AD-8). Fargemålingen mot topo-flisene gjenstår. | Arkitektur: [ARCHITECTURE-SPINE.md](../../architecture/architecture-G81-eriksen-2026-11-07/ARCHITECTURE-SPINE.md) | Kartfargene i DESIGN.md |
| **Nettleserstøtte.** **Løst 2026-11-08:** de to nyeste versjonene av Chrome, Edge, Firefox og Safari, også mobil. | Arkitektur: [ARCHITECTURE-SPINE.md](../../architecture/architecture-G81-eriksen-2026-11-07/ARCHITECTURE-SPINE.md) | – |
| **Innloggingsøktens lengde** (WCAG 2.2.1) og om utfylte felt kan beholdes gjennom ny innlogging. **Delvis løst 2026-11-08:** innloggingen varer i to uker uten inaktivitetsgrense, og utløpt innlogging sender til Logg inn og tilbake (AD-6). Om utfylte felt beholdes, avgjøres i kontostoryen. | Arkitektur: [ARCHITECTURE-SPINE.md](../../architecture/architecture-G81-eriksen-2026-11-07/ARCHITECTURE-SPINE.md) | Tilstanden Innlogging utløpt |
| **Neste steg ved feil innlogging.** Glemt passord er utsatt til senere fase (PRD v1.1 §7.2), men NFR-2 krever likevel et neste steg i tilstanden Feil innlogging. | UX | Tilstanden Feil innlogging |
| **Sperre og turtypepreferanse (FR-19, FR-20).** Teksten ved sperre er foreløpig. Preferansen har ingen tekst. | PRD og UX | Tekstene ved sperre og preferanse |
| **«Låse opp lengre turer».** FR-8-teksten og turkompis-eksemplet sier «lengre», mens FR-19 hever nivået (lengde eller høydemeter). Ordlyden bør sjekkes mot SM-C1 (ikke presse nybegynnere). **Løst 2026-11-07:** ny ordlyd i PRD v1.2 FR-8 og Mikrotekst. | PRD | – |
| **Turens turtyper** vises bare som treff. Med «Alle turtyper» får brukeren ikke vite at turen har utsikt. | UX | – |
| **Hjelp til å tolke tall** («passer for nybegynnere», «slak stigning»), underlag (sti eller vei fra `ruteFølger`) og nedstigning i Faktarute. | UX | – |
| **Finne igjen favoritter** i Historikk (sortering eller markering etter fornøydhet). | UX | – |
| **Navn på turer.** 41 av 186 ruter heter «Ukjent» i kildedataene, og vi trenger en regel for turnavn. **Løst 2026-11-08:** turnavnet skrives for hånd i kurateringslista og hentes aldri fra kilden (AD-3). | Arkitektur: [ARCHITECTURE-SPINE.md](../../architecture/architecture-G81-eriksen-2026-11-07/ARCHITECTURE-SPINE.md) | – |
| **Turillustrasjon uten reserve.** Den bærer klimakset i UJ-1. Hva vises hvis den må kuttes? | UX | Kuttrekkefølgen |
| **Tekster merket [ASSUMPTION]** i Mikrotekst må godkjennes, særlig nivåtak, sperre, personvern, feilmeldinger og tilstandene uten værvarsel. | UX | Ferdig mikrotekst |
| **Mykere statusflater** for Melding, og **ikonstil** for turtypekort, bekledningstips, meldinger og Nivåmerke. | UX (DESIGN.md) | – |
