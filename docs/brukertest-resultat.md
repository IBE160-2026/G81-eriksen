# Resultat: brukertest med nybegynnere (SM-1)

Testplan: `docs/brukertest-testplan.md`. Ingen navn, e-post eller opptak står her (NFR-5). Felter merket «ikke notert» mangler i notatene fra testen og må fylles ut av testlederen, ikke gjettes.

**Status:** pågår. 3 av 3–5 testere er gjennomført.

## T1

| Felt | Verdi |
|---|---|
| Kode | T1 |
| Dato | 2026-11-28 |
| Enhet (mobil/PC, nettleser) | PC, Chrome |
| Hvilke turer ble foreslått | Søk 1: ingen tur. Søk 1b (marka): Grorud – Badedammen, grønn. Søk 2: Kolsåstoppen (turene som dukket opp) |
| Begrunnelsen viste | ikke notert om merket var KI eller mal. Testleder: KI-merket og teksten så fine ut i forhold til turen som dukket opp |
| Steg 1 søk som gjest, uten hjelp | ja |
| Steg 2 turforslag, uten hjelp | ja |
| Steg 3 lage konto, uten hjelp | ja |
| Steg 4 registrere tur, uten hjelp | ja |
| Steg 5 søke på nytt, uten hjelp | ja |
| Hele kjerneflyten uten hjelp | ja |
| Hvor det eventuelt stoppet | Søk 1 ga «Jeg fant ingen tur som passer søket ditt». Testeren prøvde marka i stedet og kom videre |
| Spørsmål 1: første forslag relevant? | ja |
| Spørsmål 2: vanskelighet før registrering | lett |
| Fant «Slett konto» selv | ja (gikk fint) |
| Sitater (uten navn) | ingen |

### Søk og registreringer (slik de ble utført)

| | Søk | Resultat | Registrert tur |
|---|---|---|---|
| 1 | 2,5 t, søndag 29. november, utsikt, startpunkt Grorud stasjon | Ingen tur som passer søket | – |
| 1b | Samme, men turtype marka | Grorud – Badedammen, grønn | Brukt tid 1 t 15 min, lett, fornøyd 3 |
| 2 | 4 t, søndag 29. november, topptur, startpunkt: alle (turen som kom opp: Kolsåstoppen) | Kolsåstoppen | Brukt tid 3 t 50 min, moderat, fornøyd 4 |

Vurderingen i selve registreringen (lett/moderat, fornøyd) telles ikke i SM-C1, fordi den kommer etter turen, ikke på første forslag (testplan §7).

### Funn

- **F1 (T1, søk 1):** Utsikt fra Grorud stasjon med 2,5 t ga ingen tur. Testeren løste det selv ved å bytte turtype til marka. Sjekk at meldingen om at ingen tur passet, gir forslag til hva testeren kan gjøre (FR-8), og om turdatabasen har for få utsiktsturer fra østlige startpunkter.

Slett konto: gikk fint, uten hjelp (T1 klarte alt uten hjelp).

## T2

| Felt | Verdi |
|---|---|
| Kode | T2 |
| Dato | 2026-11-28 |
| Enhet (mobil/PC, nettleser) | mobil: Safari (iPhone) |
| Hvilke turer ble foreslått | Søk 1: Kolsåstoppen fra Gjettum. Søk 2: Vettakollen (turene som dukket opp) |
| Begrunnelsen viste | ikke notert |
| Steg 1–5 og hele kjerneflyten uten hjelp | ja (kjerneflyten gikk fint) |
| Hvor det eventuelt stoppet | ikke notert |
| Spørsmål 1: første forslag relevant? | ja |
| Spørsmål 2: vanskelighet før registrering | lett |
| Fant «Slett konto» selv | ja (gikk veldig fint) |
| Sitater (uten navn) | ingen (ellers ingen kommentarer) |

### Søk og registreringer (slik de ble utført)

| | Søk | Resultat | Registrert tur |
|---|---|---|---|
| 1 | 4 t, fredag 4. desember, topptur, startpunkt: alle | Kolsåstoppen fra Gjettum | Brukt tid 3 t 25 min, lett, fornøyd 4 |
| 2 | 6 t, lørdag 28. november, utsikt, startpunkt: alle | Vettakollen | Brukt tid 3 t, lett, fornøyd 3 |

## T3

| Felt | Verdi |
|---|---|
| Kode | T3 |
| Dato | 2026-11-28 |
| Enhet (mobil/PC, nettleser) | mobil: Android (nettleser ikke notert) |
| Hvilke turer ble foreslått | Søk 1: Dælivann. Søk 2: Kolsåstoppen fra Gjettum (turene som dukket opp) |
| Begrunnelsen viste | ikke notert |
| Steg 1–5 og hele kjerneflyten uten hjelp | ikke notert («det gikk fint å bruke») |
| Hvor det eventuelt stoppet | ikke notert |
| Spørsmål 1: første forslag relevant? | ikke notert |
| Spørsmål 2: vanskelighet før registrering | ikke sikkert: «lett» er notert ved Dælivann, men det er uklart om det var svaret på spørsmål 2 eller turens nivå |
| Fant «Slett konto» selv | ja (gikk fint) |
| Sitater (uten navn) | «Det gikk fint å bruke.» (kommentar fra testen) |

### Søk og registreringer (slik de ble utført)

| | Søk | Resultat | Registrert tur |
|---|---|---|---|
| 1 | 2 t, 29. november, marka, startpunkt: alle | Dælivann (notert «lett») | Brukt tid 1 t 35 min, lett, fornøyd 1 |
| 2 | 5 t, [29. desember eller 29. november, bekreft], utsikt, startpunkt: alle | Kolsåstoppen fra Gjettum | Brukt tid 1 t 20 min, moderat, fornøyd 4 |

## Sammendrag

| Tester | Uten hjelp | Første forslag relevant | Vanskelighet (spm. 2) |
|---|---|---|---|
| T1 | ja | ja | lett |
| T2 | ja | ja | lett |
| T3 | ikke notert | ikke notert | ikke sikkert |

**SM-1:** T1 og T2 har nådd målet (uten hjelp og første forslag relevant). T3 kan ikke avgjøres før «uten hjelp», relevans og vanskelighet er notert. Med 3 testere må alle 3 nå målet.
**SM-C1:** så langt oppfylt: ingen av T1 og T2 svarte «vanskelig» (begge «lett»). Avgjøres når alle testerne er ferdige.
