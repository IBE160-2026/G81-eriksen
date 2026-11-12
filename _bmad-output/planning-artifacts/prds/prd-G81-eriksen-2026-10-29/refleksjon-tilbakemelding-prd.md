# Refleksjon: tilbakemelding på PRD

| | |
|---|---|
| **Gruppe** | G81 – G81-eriksen |
| **Svar på** | `tilbakemelding-prd.md` §7 Refleksjonsspørsmål |
| **Dato** | 2026-11-12 |
| **Status** | Utkast – skal leses og skrives om med egne ord før det leveres |

## 1. Hvordan sjekker jeg at en KI-assistent har forstått «sperre» og «heving» likt?

Arbeidet med tilbakemeldingen viste at problemet er reelt. FR-19 sa at en tur vurdert *vanskelig* senker nivåtaket «til turnivået for den turen». Teksten i `EXPERIENCE.md` og eksempelet i tilbakemeldingen forutsatte derimot at en blå tur på blått tak gir grønt tak. To lesere hadde altså forstått samme setning ulikt, og det oppdaget jeg først da jeg prøvde å skrive kanttilfellene som konkrete eksempler.

Derfor sjekker jeg forståelsen med eksempler, ikke med prosa:

- **Eksemplene er fasiten.** FR-19 har nå 12 eksempler med tilstand før, registrering og tilstand etter (PRD v1.4). SM-2 sier at hvert eksempel er et testtilfelle. Testene skrives fra tabellen *før* jeg ber KI skrive selve regelen, og i en egen økt, slik at KI ikke skriver både kode og test ut fra samme misforståelse.
- **Eksemplene skiller tolkningene.** Eksempel 4 og 5 feiler hvis sperren settes til turens nivå, eller hvis bare *moderat* opphever sperren. Jeg kan sjekke det ved å be KI lage en bevisst feil variant (den gamle tolkningen) og se at minst én test feiler.
- **Én funksjon eier reglene.** Arkitekturen (AD-11) sier at bare `vurder_historikk` går gjennom registreringene. Søk, fremgang og begrunnelse leser resultatet. Da kan ikke to stories tolke reglene hver for seg.
- **KI forklarer tilbake.** Før koden skrives, ber jeg KI beskrive reglene med egne ord og fylle ut tabellen for noen nye tilfeller. Svarene sammenligner jeg med PRD-en.
- **Testbrukeren viser det i praksis.** Testbrukeren (FR-21) viser heving og sperre i appen, så jeg ser at det testene sier, også stemmer med det brukeren ser.

## 2. Hvilke forslag fra gjennomgangene valgte jeg bort, og hvorfor?

PRD-en har vært gjennom rubrikk-, struktur- og språkgjennomganger for v1.0 og v1.1, og avstemming mot brief, research, sensorveiledning og UX. De fleste forslagene er brukt. Disse valgte jeg bort:

| Forslag | Fra | Hvorfor valgt bort |
|---|---|---|
| Flytte §7 Scope rett etter §2 (pyramidemodellen) | Strukturgjennomgang v1.0 | §-numrene er brukt i PRD, `EXPERIENCE.md`, arkitektur og logger. Flyttingen ville gitt mange henvisninger å rette for liten gevinst |
| Bytte overskriften «Scope» til «Omfang» | Språkgjennomgang v1.0 (1 av 41 funn) | «Scope» er et fast BMAD-begrep. De andre 40 språkfunnene ble brukt |
| Kutte setningen i UJ-2 om at Ola kunne ha bedt om en lett tur | Strukturgjennomgang v1.1 | Setningen viser at brukeren fortsatt kan få grønne turer etter en heving. Det er viktig for motmålet SM-C1 (ikke presse nybegynnere) |
| La KI oppdage steder uten turer i friteksten og gi en egen melding | Arkitekturarbeidet (alternativ B) | Det øker KI-omfanget og virker ikke uten nøkkel. En fast hjelpetekst under startpunktlista dekker det samme (PRD v1.3) |
| Endre eller angre en registrering | UX-arbeidet (åpent punkt i `EXPERIENCE.md`) | Utsatt til senere fase (§7.2) for å holde omfanget nede |
| Grense på KI-kall «per økt» | Tilbakemeldingen på PRD-en (4.3) | «Økt» betyr ett søk i én fane (§3), så grensen ville vært lett å omgå. Grensen gjelder i stedet per nettleser per time, med en totalgrense per døgn (NFR-8) |

Ett forslag ga ikke den effekten tilbakemeldingen ventet: å flytte ordlyden til `EXPERIENCE.md` (4.5) gjorde ikke PRD-en kortere, fordi budskapet fortsatt må beskrives. Gevinsten ble én kilde for ordlyd.

Mønsteret er at jeg har valgt bort forslag som bare gir finere form, men som koster mange følgeendringer, og forslag som ville gjort KI-delen større eller svekket SM-C1.
