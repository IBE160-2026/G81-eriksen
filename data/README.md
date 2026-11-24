# Turdatabasen

Mappa har kurateringslista og turdatabasen som bygges fra den (AD-3).

- `kurateringsliste.toml`: turene vi har valgt, skrevet for hånd.
- `turer.geojson`: turdatabasen. Den bygges av skriptet og committes. Appen henter aldri turdata mens den kjører.
- `osm-uttrekk.geojson` (finnes ikke ennå): et engangsuttrekk fra OpenStreetMap. Skriptet leser fila bare hvis den finnes, og stopper hvis den har 100 objekter eller flere (AD-3 punkt 3). OSM-turer er ikke med i story 1.5.

## Bygge turdatabasen

```
python -m skript.bygg_turdatabase
```

Skriptet krever nett. Det henter rutene fra Turrutebasen og høydene fra Kartverkets høyde-API, og regner lengde, høydemeter, nivå og tid i `domene/`. Alt beregnes i minnet før noe skrives. Ved feil stopper skriptet med en norsk melding som sier hvilken tur det gjelder, og `turer.geojson` er da uendret. Samme liste og samme svar gir samme fil byte for byte, så en ny kjøring gir ingen diff så lenge kildene ikke er endret.

Testene (`python manage.py test`) bruker lagrede svar i `tests/fixtures/` og trenger ikke nett.

`python manage.py lastinn` laster `turer.geojson` inn i databasen (lokalt og i byggesteget på Vercel). Den validerer hele fila først, oppretter eller oppdaterer turer og startpunkter etter ID og sletter aldri noe. Turer i databasen som mangler i fila, blir stående med en advarsel, og `--fil <sti>` laster en annen fil.

## Formatet på kurateringslista

Hver tur er en `[[tur]]`-tabell:

```toml
[[tur]]
id = "frognervassdraget"            # stabil tur-ID, unik i lista
navn = "Langs Frognervassdraget"    # turnavnet; hentes aldri fra kilden
form = "tur-retur"                  # "tur-retur" eller "rundtur"
turtyper = ["marka"]                # én eller flere av "marka", "utsikt", "topptur"
rutenummer = ["F_01812_03"]         # rutenummer i Turrutebasen, ett eller flere
ut_no_url = ""                      # valgfri; mangler den, blir den ""
startpunkt = { id = "sognsvann", navn = "Sognsvann", lat = 59.96711, lon = 10.73382 }

[tur.rutepunkter]
fra = [59.969076, 10.72659]         # [lat, lon]
til = [59.952655, 10.716583]        # vendepunktet ved tur-retur
# via = [[lat, lon], [lat, lon]]   # valgfri; plassholder, se Rundtur Ulsrudvann i lista for et ekte eksempel
```

| Felt | Regel |
|---|---|
| `id`, `navn` | Påkrevd tekst. Samme `id` kan ikke stå to ganger. |
| `form` | `tur-retur` eller `rundtur`. |
| `turtyper` | Liste med minst én av `marka`, `utsikt`, `topptur`. |
| `rutenummer` | Liste med rutenummer (`app:rutenummer`) som segmentene hentes for. Segmenter som deles mellom rutenumrene, tas med én gang. |
| `startpunkt` | `id`, `navn`, `lat`, `lon`. Det Ola ser og går fra, for eksempel en holdeplass eller en parkering. Uavhengig av rutepunktene. Samme startpunkt-ID må ha samme navn og koordinat i hele lista. |
| `rutepunkter` | `fra`, valgfri `via` og `til`, alle som `[lat, lon]` i WGS84. |
| `ut_no_url` | Valgfri tekst. |

Hele lista sjekkes før noe hentes. Brudd på reglene gir stopp med tur-ID-en (eller startpunkt-ID-en). Ukjente felt i `[[tur]]`, `startpunkt` og `rutepunkter` gir også stopp, så en skrivefeil som `vai` for `via` ikke gir en annen rute.

### Tur-retur og rundtur

- **Tur-retur** krever `til`, som er vendepunktet. Stien går `fra` → `via` … → `til`, og geometri, lengde, høydemeter og nedstigning lagres for **én vei**. Nivået gjelder én vei, og tiden regnes for begge veier (FR-2, FR-3).
- **Rundtur** har ikke `til`. Den slutter i `fra` og krever minst ett `via`. Stien går `fra` → `via` … → `fra`, og hele runden lagres. På en ring trengs ofte to `via`-punkter: med bare ett kan korteste vei tilbake være samme vei som ut.

## Hvordan stien velges

Ett rutenummer i Turrutebasen er ikke én linje, men et nettverk av delte, usorterte segmenter med forgreininger (spiken før story 1.5: `F_01812_03` har 22 segmenter, 2 komponenter og 2 forgreininger). Skriptet gjør derfor dette (`domene/rute.py`):

1. **Nettverk:** segmentene blir kanter, og endepunktene blir noder. Endepunkter **innenfor 1 m** regnes som samme node. I spiken stemte endepunktene eksakt; 5 m smeltet sammen noder som ikke hører sammen og ga falske forgreininger.
2. **Festing:** hvert rutepunkt festes til nærmeste node **innenfor 50 m**. Ligger punktet lenger unna, stopper skriptet med tur-ID og avstand. Rutepunktene bør derfor ligge på en segmentende, ikke midt på et langt segment. Festes to rutepunkter etter hverandre til samme node, stopper skriptet, så et `via`-punkt aldri forsvinner uten varsel.
3. **Korteste sti:** skriptet finner korteste vei gjennom nettverket mellom hvert par av rutepunkter (Dijkstra) og setter segmentene sammen til én linje, snudd der det trengs. Finnes det ingen sti, stopper det med tur-ID og rutenummer.

Lengden er summen av avstandene langs linja (haversine), avrundet til hele meter.

## Høyder og støyfilter

- Høydene hentes fra `https://ws.geonorge.no/hoydedata/v1/punkt` (`koordsys=4258`, punktene som `[lon, lat]`, høyst 50 per kall). Datakilden er terrengmodellen med 1 m oppløsning.
- **Punktavstand 25 m.** Stien deles opp i punkter hvert 25 m, med første og siste punkt. I spiken ga 25 m nesten samme resultat som 10 m (50 mot 51 m nedstigning med terskel 5 m) med 72 i stedet for 177 punkter, altså 2,5 ganger færre kall.
- **Terskel 5 m.** En høydeendring telles bare når den er minst 5 m fra forrige telte høyde (hysterese). Til slutt telles resten fra forrige telte høyde til siste punkt. Uten filter ble stigningen blåst opp med 15–20 m på en sti som går jevnt nedover langs en elv; med 5 m traff summen nettofallet nesten nøyaktig.
- `hoydeprofil` er de samme punktene som høydemeterne regnes fra: `[avstand_m, hoyde_m]`, med hele meter og høyde med én desimal.
- `startpunkt_hoyde_m` hentes fra det samme API-et ved startpunktets koordinat.
- 25 m og 5 m er satt fra spiken (ett segment langs en elv), ikke målt mot publiserte høydeprofiler. De skal sjekkes mot ut.no eller lignende i story 1.7.

## Kreditering

- Turruter: Turrutebasen, © Kartverket, CC BY 4.0. Hver tur har `kilde = "turrutebasen"` og `lisens = "CC BY 4.0"`.
- Høyder: Kartverkets høydedata, © Kartverket, CC BY 4.0.
- OSM-uttrekket (når det kommer): © OpenStreetMap contributors, ODbL.

## Testturene (story 1.5)

Lista har tre testturer. De byttes ut med de 15 kontrollerte turene i story 1.7.

| Tur | Rutenummer | Form | Merknad |
|---|---|---|---|
| Langs Frognervassdraget | `F_01812_03` | tur-retur | Forgreinet nettverk med 2 komponenter. Stien går fra nordenden ved Sognsvann ned til Gaustad. |
| Sognsvann–Brekke turvei | `F_20220203_01` | tur-retur | 2 komponenter med ca. 100 m mellomrom. Turen bruker bare den vestre. |
| Rundtur Ulsrudvann | `F_20200422_1` | rundtur | Ringen rundt vannet, med to `via`-punkter. Rutenummeret har også en komponent langt unna (ved 61,7° N), som ikke nås. |
