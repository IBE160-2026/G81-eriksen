# Resultat: brukertest med nybegynnere (SM-1)

Testplan: `docs/brukertest-testplan.md`. Ingen navn, e-post eller opptak står her (NFR-5). Felter merket «ikke notert» mangler i notatene fra testen og må fylles ut av testlederen, ikke gjettes.

**Status:** pågår. 2 av 3–5 testere er gjennomført.

## T1

| Felt | Verdi |
|---|---|
| Kode | T1 |
| Dato | ikke notert |
| Enhet (mobil/PC, nettleser) | PC, Chrome |
| Hvilke turer ble foreslått | Søk 1: ingen tur. Søk 1b (marka): Grorud – Badedammen, grønn. Søk 2: Kolsåstoppen |
| Begrunnelsen viste | ikke notert hvilket merke. Testleder: KI-teksten så fin ut i forhold til hva som dukket opp |
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
| 2 | 4 t, søndag [dato ikke sikker], topptur, startpunkt: alle | Kolsåstoppen | Brukt tid 3 t 50 min, moderat, fornøyd 4 |

Vurderingen i selve registreringen (lett/moderat, fornøyd) telles ikke i SM-C1, fordi den kommer etter turen, ikke på første forslag (testplan §7).

### Funn

- **F1 (T1, søk 1):** Utsikt fra Grorud stasjon med 2,5 t ga ingen tur. Testeren løste det selv ved å bytte turtype til marka. Sjekk at meldingen om at ingen tur passet, gir forslag til hva testeren kan gjøre (FR-8), og om turdatabasen har for få utsiktsturer fra østlige startpunkter.
- **F2:** Datoen i søk 2 er notert som «søndag 29. desember». 29. desember 2026 er en tirsdag, mens 29. november 2026 er en søndag. Trolig skrivefeil. Bekreft datoen.
- **F3:** Startpunktet i søk 2 er notert som «alle startpunkt = Kolsåstoppen». Uklart om testeren valgte «alle startpunkt» og fikk Kolsåstoppen som tur.

Slett konto: gikk fint, uten hjelp (T1 klarte alt uten hjelp).

## T2

| Felt | Verdi |
|---|---|
| Kode | T2 |
| Dato | ikke notert |
| Enhet (mobil/PC, nettleser) | mobil: Safari (iPhone) |
| Hvilke turer ble foreslått | Søk 1: Kolsåstoppen fra Gjettum. Søk 2: Vettakollen |
| Begrunnelsen viste | ikke notert |
| Steg 1–5 og hele kjerneflyten uten hjelp | ja (kjerneflyten gikk fint) |
| Hvor det eventuelt stoppet | ikke notert |
| Spørsmål 1: første forslag relevant? | ikke notert |
| Spørsmål 2: vanskelighet før registrering | ikke notert |
| Fant «Slett konto» selv | ja (gikk veldig fint) |
| Sitater (uten navn) | ingen (ellers ingen kommentarer) |

### Søk og registreringer (slik de ble utført)

| | Søk | Resultat | Registrert tur |
|---|---|---|---|
| 1 | 4 t, fredag 4. desember, topptur, startpunkt: alle | Kolsåstoppen fra Gjettum | Brukt tid 3 t 25 min, lett, fornøyd 4 |
| 2 | 6 t, lørdag 28. november, utsikt, startpunkt: alle | Vettakollen | Brukt tid 3 t, lett, fornøyd 3 |

## Sammendrag

| Tester | Uten hjelp | Første forslag relevant | Vanskelighet (spm. 2) |
|---|---|---|---|
| T1 | ja | ja | lett |
| T2 | ja | ikke notert | ikke notert |

**SM-1:** ikke vurdert ennå (2 testere, ikke ferdig utfylt).
**SM-C1:** ikke vurdert ennå.
