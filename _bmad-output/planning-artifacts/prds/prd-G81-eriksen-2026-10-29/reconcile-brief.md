---
title: "Input-avstemming: brief, tilbakemelding og endringsplan mot PRD"
created: 2026-11-06
step: Finalize – input reconciliation
---

# Input-avstemming: brief, tilbakemelding og endringsplan mot PRD

**Inputs som er sjekket:**
- `docs/product-brief-your-next-adventure-no.md` (kanonisk brief, forkortet «Brief»)
- `docs/tilbakemelding-product-brief.md` (faglærer, forkortet «TB»)
- `notater/endringsplan-product-brief.md` (forkortet «EP»)
- `docs/product-brief-your-next-adventure-en.md` (utdatert v1, bare skumlest: ingenting nytt utover det som ble rettet i den norske briefen)

**Metode:** Hvert punkt i inputene ble sjekket mot `prd.md`, `addendum.md`, PRD §9 og `.memlog.md`. Avvik som er loggført i memlog eller i §9, er **ikke** regnet som gap. De står i en egen liste nederst. Noen av dem er likevel tatt med som gap når beslutningen bare står i memlog og PRD-en samtidig sier noe annet.

**Alvorlighetsgrad:** høy = motsier input eller faglærers krav og påvirker vurderingen eller implementeringen. Middels = mangler i sporbarhet eller UX som bør rettes før arkitekturen. Lav = kosmetisk, eller hører hjemme i en senere fase.

---

## Gap-liste

### G1. Begrunnelsen forklarer ikke personaliseringen (høy)
- **Kilde:** TB, «Forslag til justering» pkt. 2: «Gjør personaliseringen regelbasert i v1 … **og vis brukeren hvorfor et forslag passer**». EP A, «Andre forslag»: «brukeren får se hvorfor et forslag passer». Brief, Vision: «samtidig som tjenesten alltid viser hvorfor en tur er foreslått».
- **PRD:** §6 lover at tjenesten «forklarer alltid hvorfor en tur blir foreslått», men FR-12 krever bare at begrunnelsen viser til *søkeverdier* (varighet, turtype, ønske). Ingen FR krever at nivåheving (FR-19), sperre etter *vanskelig* (FR-19), at turen ikke er gått før (FR-5), eller turtypepreferansen (FR-20) forklares for brukeren. Malen i addendum («Turen tar ca. 2 t og har utsikt, som du ba om») har heller ingen slik del.
- **Hvorfor det betyr noe:** Gjennomsiktig personalisering er selve fortrinnet, og den er det faglærer eksplisitt ba om. Uten et krav blir den ikke bygget eller testet (SM-2), og UJ-2 («etter tre grønne turer vurdert lett får han en blå tur først») blir usynlig for brukeren.
- **Forslag:** Utvid FR-12, eller legg til et nytt FR: «Når en personaliseringsregel har påvirket forslaget, viser begrunnelsen hvilken regel det var, med en fast tekst, for eksempel: ‹Du har vurdert tre grønne turer som lette, så nå foreslår vi en blå tur› / ‹Vi holder oss på blått nivå fordi forrige tur føltes vanskelig›.» Teksten lages av regler, ikke av KI, så den fungerer også i reserveløsningen. Legg dette inn i akseptkriteriene for testbrukeren (FR-21).

### G2. Fritekstønsket ignoreres i det stille når KI feiler (middels/høy)
- **Kilde:** Brief, What Makes This Different: «Vi skal være ærlige om hva fortrinnet er». EP B1: briefen må ikke love noe koden ikke gjør (varseltegnet «planleggingsdokumentene beskriver en annen app enn den som er levert»). TB: «håndtering av usikre svar».
- **PRD:** I FR-13 står det: «fritekstønsket ignoreres … Brukeren merker bare at begrunnelsen er enklere.» Har brukeren skrevet «helst ved vann», blir ønsket altså droppet uten at hen får vite det. Når KI mangler, kan heller ingenting hindre at malteksten antyder at ønsket ble oppfylt.
- **Hvorfor det betyr noe:** Dette bryter med ærligheten om KI og med tonen i §6 («oversalger ikke KI»). Det gir også dårligere tillit (§2.1, emosjonell jobb: «stole på forslaget»).
- **Forslag:** Endre FR-13: «Hvis brukeren skrev et fritekstønske og reserveløsningen brukes, viser forslaget en kort melding om at ønsket ikke ble tatt med denne gangen, for eksempel ‹Vi kunne ikke tolke ønsket ditt nå, så forslaget bygger bare på skjemaet›. Malteksten viser aldri til fritekstønsket.» Vurder også å merke KI-skrevne begrunnelser diskré (åpenhet om KI).

### G3. Briefens SC 8 («likte ikke» → ikke foreslått igjen) er endret uten å stå i §9, og §4.8 sier feil (middels)
- **Kilde:** Brief SC 8: «En tur brukeren har vurdert som *likte ikke*, blir ikke foreslått igjen.»
- **PRD:** FR-5 sier at turer med fornøydhet 1–2 «kommer sist» og «aldri blir helt utelukket». Beslutningen er loggført i memlog («Bekreftet: fornøydhet 1-2 = 'likte ikke' -> prioriteres lavere, ikke utelukket»), men den står **ikke** i §9. I tillegg sier §4.8 at «Reglene er de samme som i briefen (SC 5–8)», og det stemmer ikke for SC 8. Også «aldri helt utelukket» for alle gjennomførte turer er nytt sammenlignet med briefen.
- **Hvorfor det betyr noe:** Det er nettopp sporbarheten fra brief til PRD som sensor sjekker (kriterium 1, 30 %). En stille endring av en testbar regel er et varseltegn (EP, «Varseltegn»).
- **Forslag:** Legg til en rad i §9: «‹Likte ikke› (fornøydhet 1–2) gir lavest prioritet i stedet for utelukkelse | Siden er aldri tom med få turer. Brukeren kan bruke historikken til å gå turen igjen.» Endre §4.8 til «Reglene bygger på briefen (SC 5–8), med disse endringene: … (se §9)».

### G4. Briefen blir ikke oppdatert, og PRD-en sier ikke at den overstyrer briefen (middels)
- **Kilde:** EP B, «Varseltegn»: «Planleggingsdokumentene beskriver en annen app enn den som er levert → Hold briefen oppdatert når planen endrer seg». TB §3: «Oppdater product brief i repoet når dere har gjort endringene». EP C pkt. 3: endringslogg eller beslutningsfil.
- **PRD:** Briefen og PRD-en er nå uenige om gjestetilgang, vurderingsskala, SC 8, antall forslag, stedsinput og brukertestmålet. §9 lister forskjellene, men det står ingen steder hvilket dokument som gjelder. Briefen har heller ingen henvisning til PRD-en.
- **Forslag:** Legg inn én setning i §0: «Der PRD-en avviker fra briefen, gjelder PRD-en. Alle avvik står i §9.» Vurder i tillegg en kort note eller endringslogglinje i briefen som viser til PRD-en, slik at historikken viser utviklingen.

### G5. Ingen prioritering eller kuttlinje i scope til tross for faglærers advarsel om omfang (middels)
- **Kilde:** TB, Gjennomførbarhet: «Tid og omfang – Risiko. Seks v1-punkter med fire integrasjoner er mye for en gruppe på én person.» TB, Middels: «Pass på at kjerneflyten blir ferdig og stabil før dere legger til mer».
- **PRD:** §7.1 har 21 FR uten prioritet. Flere ting er nye sammenlignet med briefen: gjestemodus, «Nytt forslag» med økt-minne, datovalg frem i tid, historikkvisning med gjenåpning (FR-17), ut.no-lenke og topptur-reserve. Bare personlig tidsestimat og glemt passord er flyttet ut med begrunnelse i omfanget.
- **Forslag:** Merk FR-ene som *kjerne* (det SM-1-flyten krever) og *tillegg*, eller legg til en rekkefølge i §7.1, for eksempel: kjerne = FR-1 til FR-6, FR-9, FR-13, FR-14, FR-16, FR-18, FR-19 og FR-21; tillegg = FR-7, FR-11, FR-12 (KI-delen), FR-15, FR-17 og FR-20. Det viser at advarselen er tatt på alvor.

### G6. Overgangen fra gjest til konto i kjerneflyten er ikke spesifisert (middels)
- **Kilde:** Brief SC 10 og TB: kjerneflyten «beskrive tur → få forslag → **lagre** → vurdere». Brief SC 4: «lagre en gjennomført tur».
- **PRD:** SM-1-flyten er «søke som gjest → få forslag → registrere seg → vurdere turen». FR-14 sier bare at gjesten «blir bedt om å logge inn». Ingen FR sier at turforslaget gjesten så, blir tatt vare på gjennom registreringen. FR-16 sier heller ikke *hvor* brukeren registrerer turen som gjennomført (fra forslaget? fra en liste?). Briefens «lagre» som eget steg er borte uten at det er nevnt i §9.
- **Forslag:** Legg til i FR-14 eller FR-16: «Når en gjest registrerer seg eller logger inn fra et turforslag, vises det samme forslaget etterpå, og turen kan registreres som gjennomført derfra.» Si i FR-16 at registreringen starter fra turforslaget.

### G7. Briefens «Vision» og den videre retningen er tatt helt ut (lav/middels)
- **Kilde:** Brief, Vision (læring, flere regioner, flere brukergrupper og aktiviteter, «alltid viser hvorfor»). TB/EP: «Mer avansert ‹læring› kan stå i Vision.»
- **PRD:** §1 sier «I v1 skjer tilpasningen etter enkle, faste regler», men hvor produktet skal på sikt, står ingen steder. §7.2 «Senere fase» har bare tre tekniske punkter. Faglærer ga Vision-delen status OK og pekte på den som riktig sted for mer avansert læring.
- **Forslag:** Legg til to–tre setninger i §1 (eller under §7.2 «Senere fase»): fra faste regler til en tjeneste som lærer, flere regioner og aktiviteter, og at forslagene alltid skal forklares. Bruk ordlyd som ikke oversalger (EP B1: ikke «stoler blindt på»).

### G8. Forbeholdet om gradering og sikkerhet vises ikke for brukeren (lav/middels)
- **Kilde:** TB pkt. 1: KI-oppdiktede stier er «potensielt farlig i fjellet». Brief: nybegynnere «mangler erfaring til å vurdere lengde, stigning og vanskelighetsgrad selv». Brief, Scope: terrengstatus og føre er utenfor v1 fordi det er «for upresist til å love».
- **PRD:** FR-2 sier at forbeholdet (bare lengde og høydemeter, ikke terreng eller føre) er «dokumentert», men ikke at **brukeren** ser det. Nybegynnere kan tolke grønt nivå som en garanti.
- **Forslag:** Legg til i FR-6: «Turnivået vises med en kort forklaring på hva fargen bygger på (lengde og høydemeter), og at føre og terreng ikke er vurdert.» Det styrker også den ærlige og trygge tonen i §6.

### G9. «Siden står aldri tom» er beskrivelse, ikke krav (lav)
- **Kilde:** Brief, Kvalitetskrav: «Siden står aldri tom.» EP B2.
- **PRD:** Setningen står i beskrivelsen til §4.3, og FR-8, FR-10 og FR-13 dekker hvert sitt tilfelle. Kombinasjonen er derimot ikke dekket: KI feiler, MET feiler og det er bare ett treff, samtidig som gjentatte «Nytt forslag» tømmer listen (FR-7 → FR-8). FR-8 foreslår «lengre varighet eller et annet startpunkt», men ikke briefens «en annen turtype».
- **Forslag:** Løft prinsippet til et kort NFR eller et punkt i NFR-2 («Alle tilstander viser enten et turforslag eller en forklaring med neste steg»). Legg til «annen turtype» i FR-8. Si også hva som skjer når «Nytt forslag» er brukt opp: start på nytt fra toppen, eller vis FR-8-meldingen.

### G10. Mobilbruk ute er bare dekket som «responsiv» (lav)
- **Kilde:** TB, kriterium 4: «Tenk på mobilbruk ute på tur». Brief: «brukerne ofte sjekker turen på vei ut».
- **PRD:** NFR-3 sier bare «responsiv og fungerer på mobilskjerm». Konteksten i §2.1 («på mobilen på vei ut») er nevnt, men gir ingen krav.
- **Forslag:** Utvid NFR-3 litt: det viktigste (kart, tid, nivå, klesråd) synes uten mye scrolling, og knappene er store nok til å trykke på. Detaljene kan tas i UX-fasen.

### G11. «Praktiske tips» er snevret inn til bekledningstips uten at det er nevnt (lav)
- **Kilde:** Brief, Executive Summary: «rute på kart, tidsbruk og praktiske tips». Brief, Solution: «relevante tips for turen, inkludert bekledningstips».
- **PRD:** Bare bekledningstips (FR-9). Andre tips, for eksempel om drikke, hodelykt eller kollektivtransport til startpunktet, er verken med eller nevnt i §9.
- **Forslag:** Enten en linje i §9 («Tips er avgrenset til bekledningstips i v1») eller et valgfritt tekstfelt per tur i turdatabasen (FR-1).

### G12. Mindre avvik som er loggført i memlog, men ikke i §9 (lav)
- Språk: briefen ekskluderer «flere språk enn norsk/engelsk», mens PRD-en bare har norsk. Dette står i memlog («UI-språk v1: kun norsk»), men ikke i §9.
- Turtype: briefens eksempler var *skogstur*, *topptur* og *utsikt*, mens PRD-en har *marka*, *utsikt* og *topptur*. Dette står i memlog, men ikke i §9.
- Kobling mellom farge og vurderingsord fra memlog (grønn=lett, blå og rød=moderat, svart=vanskelig) er ikke brukt eller nevnt i PRD-en. Avklar om den fortsatt gjelder, eller marker den som erstattet.
- **Forslag:** Legg til de to første som rader i §9. Avklar den tredje i memlog-auditen.

### G13. Faglærers repo- og testmodus-punkter (lav, hører hjemme i arkitekturen)
- **Kilde:** TB, kriterium 6 og 7: testmodus med forhåndslagrede svar eller regelbasert reserve, egne mapper for turdatabase og testdata, valg av språkmodell og plan for kostnad.
- **PRD:** Reserveløsningen (FR-13) og `.env.example` (NFR-1) dekker kjernen. Mappestruktur, valg av modell og kostnad er riktig å utsette, men det står ikke at de er utsatt.
- **Forslag:** En linje i §0 eller i addendum: «Valg av språkmodell, kostnad og repostruktur (turdatabase og testdata i egne mapper) avgjøres i arkitekturen (TB, kriterium 5–7).»

---

## Ikke gap: loggførte, bevisste endringer (for ordens skyld)

- Konto er valgfri, og gjest kan søke (§9 og memlog)
- Skjema med valgfri fritekst i stedet for bare fritekst (§9, addendum og memlog)
- Vurderingsskalaen *lett / moderat / vanskelig* + fornøydhet 1–5 + brukt tid (§9 og memlog)
- Ett forslag om gangen + «Nytt forslag» (§9; motsier briefens «minst ett forslag» med vilje)
- Startpunkt fra liste, og meldingen om sted utenfor Oslo-området er fjernet (§9)
- Brukertestmålet er 75 % (§9)
- Terskler og tidsformel (§9, research-gradering.md og addendum)
- Personlig tidsestimat, kartklikk og glemt passord er flyttet til en senere fase (§7.2 og memlog)
- 20–30 turer i Oslo-området i stedet for faglærers eksempel Molde (briefen hadde allerede valgt Oslo, og faglærer ba bare om ett område)
- Ordbruken «lærer / smartere» er fjernet (EP B1), og dette er dekket i §1 og §6
- Personvern (NFR-5), UU (NFR-4), testbruker med oppdiktede data (FR-21) og slette konto (FR-15) er dekket
