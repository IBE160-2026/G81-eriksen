# Kontroll av turdatabasen

Kontrolliste for rutelinjene i `data/turer.geojson` og sammenligningen med publiserte høydeprofiler (FR-1, story 1.7). Story 6.2 legger til en rad her for hver ny tur.

## Slik er kontrollen gjort

- **Kart:** hver rutelinje er tegnet på Kartverkets topografiske kart (samme fliser som Norgeskart, `cache.kartverket.no`) i Chrome, med startpunktet, rutens første punkt og laveste og høyeste punkt i høydeprofilen markert. Laveste og høyeste punkt er sammenlignet med høydetall, vannflater og koter på kartet.
- **ut.no:** der det finnes et turforslag med samme start og mål, er linja sammenlignet med turforslaget på ut.no (sidenummeret er tallet i adressen, `ut.no/turforslag/<nummer>`).
- **Sammenheng:** et skript har sjekket at hvert steg i linja er et steg i et segment fra Turrutebasen for turens rutenumre, en kobling fra lista eller et sprang under 1 m mellom to segmentender. Ingen linje har hull.
- **Avstand til startpunktet:** luftlinje fra startpunktets koordinat til rutens første punkt. Over 500 m flagges.
- **Form:** om rundturen slutter der den startet (`i ring`), og hvor stor del av lengden som gås to ganger (`andel_gatt_to_ganger`). Tur-retur går per definisjon samme vei tilbake; tallet gjelder én vei.

Kontrollert 2026-11-25 av Claude. Hannah bekrefter i PR-en.

## Rutelinjene

Høydene er fra `hoydeprofil` (25 m punktavstand). «To ganger» er andelen av lengden som gås to ganger.

| Tur | Dato | Sammenheng | Start → første punkt | Form | Lavest / høyest | Mot kartet | Kontrollert av | Avvik |
|---|---|---|---|---|---|---|---|---|
| `frognervassdraget` | 2026-11-25 | ok | 458 m | tur-retur, 0 % to ganger | 142,6 / 185,1 | Høyest ved nordenden av Sognsvann (vannet 183–181 på kartet), lavest ved Gaustad ned mot Rikshospitalet. | Claude | ingen |
| `sognsvann-brekke` | 2026-11-25 | ok | 437 m | tur-retur, 0 % | 190,3 / 207,9 | Lavest ved Sognsvann (183–181), høyest ved Langmyr. | Claude | ingen |
| `frognerseteren-skjennungstua` | 2026-11-25 | ok | 21 m | tur-retur, 0 % | 377,1 / 489,6 | Lavest i dalen ved Frønsvollen under Rishøgda (411), høyest ved Øvresetertjern like ved Frognerseteren. Ruten tar en bue rundt Nikulpmyrene etter starten, slik de merkede rutene går. | Claude | ingen |
| `frognerseteren-kobberhaughytta` | 2026-11-25 | ok | 21 m | tur-retur, 0 % | 347,1 / 489,6 | Lavest ved utløpet av Blankvann (vannet 354), høyest ved Øvresetertjern. Slutter ved Kobberhaughytta. | Claude | ingen |
| `nordmarksrunden` | 2026-11-25 | ok, med tre koblinger på 2,4, 3,1 og 8,9 m ved Ullevålseter | 21 m | rundtur i ring, 12 % to ganger (stikkveien inn til Kobberhaughytta og stykket nærmest Frognerseteren) | 288,7 / 507,6 | Lavest ved Østre Aurtjern (høydetall 292 og 278 like ved), høyest i lia under Kobberhaugene (518 og 526). | Claude | ingen |
| `vettakollen-topp` | 2026-11-25 | ok | 227 m | tur-retur, 0 % | 244,6 / 419,5 | Lavest ved første punkt i Bånntjernveien (kote 250, høydetall 236,4 like ved), høyest på toppen ved navnet Vettakollen (ut.no 114607 har 416 i samme område). | Claude | ingen |
| `vettakollen-fuglemyrhytta` | 2026-11-25 | ok | 227 m | tur-retur, 0 % | 244,6 / 419,5 | Samme stigning som over, over Vettakollen og videre til Fuglemyrhytta. ut.no 1112154257 har 196–417 fra stasjonen. | Claude | ingen |
| `vettakollen-rundtur` | 2026-11-25 | ok | 227 m | rundtur i ring, 17 % to ganger (stykket fra Bånntjernveien) | 244,6 / 418,7 | Opp vestsiden mot Skådalen, ned over Fuglemyrhytta og Vettakollen. Høyest ved Vettakollen. | Claude | ingen etter rettingen (se under) |
| `rundtur-ulsrudvann` | 2026-11-25 | ok | 132 m | rundtur i ring, 0 % | 185,9 / 198,9 | Lavest ved Ulsrudvannet (185,8 på kartet), høyest ved Bjerke (196–197 like ved). | Claude | ingen |
| `noklevann-rundt` | 2026-11-25 | ok | 132 m | rundtur i ring, 0 % | 152,9 / 212,4 | Lavest ved Rustadsaga nedenfor dammen (Nøklevannet 164–159), høyest ved Østmarksetra. 98 % av linja ligger innenfor 30 m av ut.no 1110939. | Claude | ingen etter rettingen (se under) |
| `ostmarksetra-mariholtet` | 2026-11-25 | ok | 132 m | tur-retur, 0 % | 164,9 / 287,2 | Lavest ved nordenden av Nøklevann (164–159), høyest i lia nord for Sarabråtåsen. Slutter ved Mariholtet. | Claude | ingen |
| `kolsastoppen` | 2026-11-25 | ok | 147 m | tur-retur, 0 % | 91,8 / 379,0 | Lavest ved første punkt ved Toppås, høyest på Nordre Kolsås (høydetall 380 på kartet, 379 moh på ut.no). | Claude | ingen |
| `dalivann-rundt` | 2026-11-25 | ok | 147 m | rundtur i ring, 38 % to ganger (stilken fra Gjettum) | 100,0 / 121,6 | Lavest ved Dælivannet (99 på kartet), høyest ved første punkt ved Toppås like ved Gjettum, i bebyggelsen mellom kotene 120 og 140. | Claude | ingen |
| `grorud-badedammen` | 2026-11-25 | ok | 434 m | tur-retur, 0 % | 169,8 / 243,6 | Lavest ved første punkt sør for Trondheimsveien, høyest ved Badedammen. | Claude | ingen |
| `grorud-grefsenkollen` | 2026-11-25 | ok | 434 m | tur-retur, 0 % | 169,8 / 360,6 | Høyest ved serveringsstedet på Grefsenkollen. Toppen (høydetall 380) ligger ca. 20 m høyere og nås ikke av noen rute i Turrutebasen, så turen er merket `utsikt`, ikke `topptur`. Ruten går nordover gjennom Lillomarka. | Claude | ingen etter rettingen (se under) |

Startpunktene ligger alle under 500 m fra rutens første punkt. `gjettum` er koordinaten til Gjettum (gard) fra Kartverkets stedsnavn-API, ca. 150 m fra rutens første punkt. Stedsnavn-API-et gir tre treff for Gjettum; punktet for «Gjettum stasjon» ligger ca. 640 m fra ruten og ca. 550 m fra der Kolsåsbanen stopper i dag, så det ble ikke brukt.

### Rettet under kontrollen

- `vettakollen-rundtur`: med Vettakollen og Fuglemyrhytta som eneste via-punkter gikk hele runden to ganger (100 %), og den nye sjekken stoppet byggingen. Turen går nå opp vestsiden (rutenummer `F_20171026_02`) og har 17 %.
- `noklevann-rundt`: det østlige via-punktet i kandidatlista lå oppe på åsen (279 moh). Det er flyttet ned til stien langs vannet, så runden følger ut.no-turen.
- `grorud-grefsenkollen`: navnet nevnte Linderudkollen, men ruten går ca. 500 m unna. Navnet er nå «Grorud–Grefsenkollen gjennom Lillomarka», og `topptur` er tatt bort (se tabellen).
- ut.no-lenker som bare delvis gjaldt turen (andre start- eller målpunkter, eller en side som ikke finnes lenger) er tatt bort. `ut_no_url` står bare der ut.no har samme start og mål.

## Sammenligning med publiserte høydeprofiler

Spec 1.7: punktavstanden (25 m) og støyterskelen (5 m) endres bare hvis høydemeterne våre avviker mer enn 15 % fra den publiserte verdien på minst to av tre turer. ut.no oppgir «høydemeter totalt» for hele turen, så for tur-retur er vår verdi `hoydemeter_m + nedstigning_m` og lengden `2 × lengde_m`.

| Tur | ut.no (side) | Lengde vår / ut.no | Høydemeter vår / ut.no | Avvik | Lavest / høyest vår | Lavest / høyest ut.no | Merknad |
|---|---|---|---|---|---|---|---|
| `vettakollen-topp` | [114607](https://ut.no/turforslag/114607) | 4,30 / 3,68 km | 209 / 220 | −5 % | 244,6 / 419,5 | 196 / 416 | ut.no starter ved stasjonen og snur ved utsiktspunktet sør for toppen; vår rute starter i Bånntjernveien og går over toppen. |
| `noklevann-rundt` | [1110939](https://ut.no/turforslag/1110939) | 8,23 / 11,25 km | 156 / 223 | −30 % | 152,9 / 212,4 | 153 / 214 | ut.no starter ved Ulsrud stasjon og har stigningen derfra til Østmarksetra med. Selve runden er den samme (98 % overlapp). |
| `frognerseteren-kobberhaughytta` | [1112157534](https://ut.no/turforslag/1112157534) | 16,37 / 17,55 km | 381 / 431 | −12 % | 347,1 / 489,6 | 347 / 524 | ut.no går videre fra hytta opp på Kobberhaugene (524). |

Én av tre avviker mer enn 15 %, og det skyldes at ut.no-turen er en annen strekning. Kolsåstoppen (reserven) ble ikke brukt: begge ut.no-turene dit (1110204 og 116870) starter et annet sted enn Gjettum.

### Kontroll på ut.no sin egen linje

For å skille punktavstand og terskel fra forskjeller i ruten er beregningen vår (`domene.rute.omsampl` og `hoydemeter_og_nedstigning`, høyder fra Kartverket) kjørt på linja som ut.no publiserer for turen. Tallene er for én vei; for tur-retur er ut.no sin totalverdi opp + ned.

| ut.no | ut.no oppgir | 10 m / 5 m | **25 m / 5 m** | 50 m / 5 m | 25 m / 2 m | 25 m / 10 m |
|---|---|---|---|---|---|---|
| 114607 Vettakollen (t/r) | 220 | +221/−0 | **+221/−0 = 221** | +221/−0 | +225/−4 | +221/−0 |
| 1110939 Nøklevann (rundtur) | 223 | +237 | **+220** | +228 | +282 | +169 |
| 1112154257 Fuglemyrhytta (én vei) | +227/−23 | +233/−28 | **+226/−21** | +229/−24 | +231/−26 | +233/−28 |
| 1112157534 Kobberhaugene (t/r) | 431 | +312/−255 | **+306/−249 = 555** | +312/−255 | +382/−325 | +255/−197 |

Med 25 m og 5 m treffer vi ut.no innen 2 % på Vettakollen, Nøklevann og Fuglemyrhytta. Kobberhaugene avviker (+29 %), men ut.no sin egen linje har bare 64 punkter, og summen av høydene i den gir 537, ikke 431. Tallet på ut.no kan altså ikke gjenskapes fra linja de publiserer. Terskel 2 m blåser opp Nøklevann med 26 %, og 10 m tar bort 24 %, så 5 m ligger riktig.

**Resultat:** 25 m og 5 m beholdes. Ingen konstanter i `domene/rute.py` er endret, og fixturene er ikke laget på nytt.

## Kilder

- Turruter: Turrutebasen, © Kartverket, CC BY 4.0 (WFS `wfs.geonorge.no/skwms1/wfs.turogfriluftsruter`), hentet 2026-11-25.
- Høyder: Kartverkets høydedata (`ws.geonorge.no/hoydedata/v1/punkt`, DTM 1 m), © Kartverket, CC BY 4.0.
- Kart: Kartverkets topografiske kart (`cache.kartverket.no`), © Kartverket.
- Stedsnavn: Kartverkets stedsnavn-API (`api.kartverket.no/stedsnavn/v1`).
- ut.no: turforslagene 114607, 1110939, 1112157534, 1112154257, 1110204 og 116870 (lengde, høydemeter og linja med høyder), lest 2026-11-25.
