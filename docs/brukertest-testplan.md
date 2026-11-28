# Testplan: brukertest med nybegynnere (SM-1)

Denne planen er skrevet før første test (story 6.7, AR-21). Utkast til invitasjon til testere: `docs/brukertest-invitasjon.md`. Resultatene føres i `docs/brukertest-resultat.md` etter mal i slutten av dette dokumentet.

## 1. Mål

Mål (SM-1, PRD §8): minst 75 % av testerne klarer kjerneflyten uten hjelp og vurderer det første turforslaget som relevant. Det betyr 3 av 3, 3 av 4 eller 4 av 5 testere.

Motmål (SM-C1): ingen tester vurderer det første turforslaget som *vanskelig*.

Testen validerer søk og turforslag (FR-4 til FR-8), konto (FR-14), registrering av gjennomført tur (FR-16) og nivåreglene (FR-18).

## 2. Testerne

**Antall:** 3–5 testere. Hver får en kode: T1, T2, T3, T4, T5.

**Hvem:** Nybegynnere etter målgruppen i PRD §2: personer som vil på tur i Oslo-området, men ikke er turvante og ikke kjenner marka godt. Ikke egnet: erfarne turgåere, turister og personer som har brukt appen før.

**Krav til hver tester:**
- Er ikke med i prosjektgruppen og har ikke sett eller brukt appen før.
- Har sagt ja etter å ha fått vite hva som noteres (se §3).
- Bruker gjerne mobil. Minst én tester bør bruke mobil og minst én PC, så begge skjermstørrelsene dekkes.

**Personvern (NFR-5):** Navn, e-post og opptak lagres ikke i repoet eller andre steder knyttet til testeren. Bare koden (T1–T5) står i dokumentasjonen. Koblingen mellom kode og person holdes av testlederen utenfor repoet, og kastes etter at resultatet er skrevet.

## 3. Informasjon og samtykke

Testlederen sier dette før testen, og testeren sier ja:

> Du skal teste en nettside som foreslår turer i Oslo-området. Det er siden som testes, ikke deg. Jeg kan ikke hjelpe deg underveis, og det er greit å stoppe når som helst. Jeg skriver ned om du kommer gjennom oppgaven, hvor du eventuelt stopper, to svar du gir, og noen sitater uten navn. Jeg tar ikke opptak og skriver ikke ned navnet eller e-posten din. Kontoen du lager i testen slettes etterpå.

## 4. Forberedelser (testleder)

- Åpne den publiserte siden: https://your-next-adventure.vercel.app/
- Sjekk at siden åpner og at et søk gir turforslag, også i et privat nettleservindu uten Vercel-innlogging. Bruk produksjonsdomenet over, ikke `...-hannah-eriksen.vercel.app` eller adresser til forhåndsvisninger: de krever Vercel-innlogging.
- Lag en liste over test-e-poster, for eksempel `tester1@eksempel.no`, `tester2@eksempel.no`. De trenger ikke være ekte postkasser. Appen sender ikke e-post.
- Velg et enkelt testpassord (minst 8 tegn) som testeren får skrevet ned på lapp. Det slettes sammen med kontoen.
- Ha denne planen og notatskjemaet (§9) klare. Legg telefonen på lydløs.
- Test aldri to testere samtidig på samme test-e-post.

## 5. Oppgaven

Testlederen leser oppgaven høyt og gir den som tekst. Etter dette regnes alt testlederen sier eller viser om appen som hjelp (§6).

> Tenk deg at du vil på en kort tur i Oslo-området i helgen. Du har ca. to timer. Bruk nettsiden til å finne en tur, og gå gjennom dette:
> 1. Søk etter en tur uten å logge inn.
> 2. Se på turforslaget du får.
> 3. Lag en konto. Bruk e-posten og passordet på lappen.
> 4. Tenk deg at du har gått turen. Registrer den som gjennomført, med vurdering.
> 5. Søk etter en ny tur.
> Si høyt hva du tenker underveis.

Når testeren har vært gjennom steg 2, stilles spørsmålene i §7, før steg 4.

## 6. Hva regnes som hjelp

**Regnes som hjelp:**
- Å si eller peke på hva testeren skal trykke på, eller hvor noe står.
- Å forklare hva en tekst, en knapp eller et ord betyr.
- Å si at testeren er på riktig eller feil vei.
- Å gjenta eller omformulere oppgaven etter at den er gitt.
- Alt testlederen sier eller viser om appen etter at oppgaven er gitt.

**Regnes ikke som hjelp:**
- Å lese oppgaven opp igjen ordrett.
- Å svare på spørsmål om selve testen (hvor lang tid det tar, at testeren kan stoppe).
- Å si «hva tenker du nå?» uten å si noe om appen.
- Tekniske problemer som ikke er appens skyld (Wi-Fi faller ut). Notér dem, og start det aktuelle steget på nytt uten å regne det som hjelp.

**Stopp:** Hvis testeren ikke kommer videre i mer enn ca. 2 minutter, eller sier at hen gir opp, regnes steget som ikke gjennomført uten hjelp. Notér hvor det stoppet, og hjelp testeren videre så testen kan fortsette. Resultatet «uten hjelp: nei» står fast.

## 7. Spørsmålene

Stilles når testeren har sett første turforslag, før hen registrerer turen.

1. **Er dette forslaget relevant for det du lette etter?** Ja eller nei.
2. **Hvor vanskelig virker turen for deg?** *Lett*, *moderat* eller *vanskelig*.

Vurderingen testeren gir i selve registreringen (steg 4) telles ikke i SM-C1, fordi testeren ikke har gått turen.

Etter steg 5 stilles disse fritt, og svarene noteres som korte sitater uten navn:
- Hva var enklest?
- Hva var vanskeligst eller forvirrende?
- Stolte du på forslaget? Hvorfor eller hvorfor ikke?

## 8. Etter testen

1. Be testeren velge «Slett konto» og bekrefte. Kvitteringen skal vises på søkesiden. Dette teller ikke som hjelp, men noter om testeren fant det selv.
2. Skriv ned resultatet i notatskjemaet (§9) mens det er friskt.
3. Takk testeren. Slett koblingen mellom kode og person (§2).

## 9. Notatskjema per tester

Kopier til `docs/brukertest-resultat.md` per tester. Ikke skriv navn, e-post eller annet som identifiserer.

| Felt | Verdi |
|---|---|
| Kode | T1 |
| Dato | |
| Enhet (mobil/PC, nettleser) | |
| Hvilke turer ble foreslått (navn, nivå) | |
| Begrunnelsen viste | «✦ Skrevet med KI» / «Begrunnelse fra mal» |
| Steg 1 søk som gjest, uten hjelp | ja / nei |
| Steg 2 turforslag, uten hjelp | ja / nei |
| Steg 3 lage konto, uten hjelp | ja / nei |
| Steg 4 registrere tur, uten hjelp | ja / nei |
| Steg 5 søke på nytt, uten hjelp | ja / nei |
| Hele kjerneflyten uten hjelp | ja / nei |
| Hvor det eventuelt stoppet | |
| Spørsmål 1: relevant? | ja / nei |
| Spørsmål 2: vanskelighet | lett / moderat / vanskelig |
| Fant «Slett konto» selv | ja / nei |
| Sitater (uten navn) | |
| Funn | |

## 10. Oppsummering og konklusjon

Resultatdokumentet har dato, antall testere, tabellen over alle testere, sitater uten navn, funn og konklusjonen.

**En tester har nådd målet** når hen gjennomførte kjerneflyten uten hjelp (alle fem steg) og vurderte første forslag som relevant.

| Antall testere | Må ha nådd målet |
|---|---|
| 3 | 3 |
| 4 | 3 |
| 5 | 4 |

**SM-1:** nådd / ikke nådd.
**SM-C1:** oppfylt når ingen tester svarte *vanskelig* på spørsmål 2.

**Hvis SM-1 ikke er nådd, eller noen svarte *vanskelig*:** Resultatet står slik det ble. Hvert funn blir en issue med tiltak, og rettinger kommer i PR-er som viser til funnet. En ny runde med nye testere dokumenteres på samme måte. Funn om en tekst endres først i Mikrotekst og så i koden (AR-16).

README skal lenke til `docs/brukertest-resultat.md` når den finnes (AR-21).
