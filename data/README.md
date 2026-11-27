# Turdatabasen

Mappa har kurateringslista og turdatabasen som bygges fra den (AD-3).

- `kurateringsliste.toml`: turene vi har valgt, skrevet for hånd.
- `turer.geojson`: turdatabasen. Den bygges av skriptet og committes. Appen henter aldri turdata mens den kjører.
- `osm-uttrekk.geojson` (finnes ikke ennå): et engangsuttrekk fra OpenStreetMap. Skriptet leser fila bare hvis den finnes, og stopper hvis den har 100 objekter eller flere (AD-3 punkt 3). Det finnes ikke noe OSM-uttrekk (0 objekter), og alle de 15 turene er fra Turrutebasen.

## Bygge turdatabasen

```
python -m skript.bygg_turdatabase
```

Skriptet krever nett. Det henter rutene fra Turrutebasen og høydene fra Kartverkets høyde-API, og regner lengde, høydemeter, nivå og tid i `domene/`. Alt beregnes i minnet før noe skrives. Ved feil stopper skriptet med en norsk melding som sier hvilken tur det gjelder, og `turer.geojson` er da uendret. Samme liste og samme svar gir samme fil byte for byte, så en ny kjøring gir ingen diff så lenge kildene ikke er endret.

Testene (`python manage.py test`) bruker lagrede svar i `tests/fixtures/` og trenger ikke nett.

`python manage.py lastinn` laster `turer.geojson` inn i databasen (lokalt og i byggesteget på Vercel). Den validerer hele fila først, oppretter eller oppdaterer turer og startpunkter etter ID og sletter aldri noe. Turer i databasen som mangler i fila, blir stående med en advarsel, og `--fil <sti>` laster en annen fil.

## Testbrukeren

`testbruker.toml` beskriver testbrukeren og registreringene hennes (FR-21, AR-5). `lastinn` leser fila med `tomllib`, validerer hele fila før noe lagres, og sletter og gjenskaper testbrukeren med registreringene i samme transaksjon som turene. Andre brukere røres ikke. Med `--fil` leses testbrukeren bare når `--testbruker [sti]` er oppgitt.

Vi valgte TOML fordi formatet er standard i Python 3.11+ (ingen ny avhengighet), tillater en kommentar per registrering om hva den viser, og er det samme formatet som kurateringslista.

```toml
epost = "testbruker@example.com"
passord = "Testbruker2026"         # lagres bare som hash; minst 8 tegn etter Djangos passordregler

# Kommentar om hva registreringen viser.
[[registrering]]
tur_id = "vettakollen-fuglemyrhytta"  # må finnes blant turene som lastes
dato = "2026-08-02"                # ISO, ikke frem i tid
brukt_tid_min = 150                # 10 til 1440
vanskelighet = "lett"              # lett, moderat eller vanskelig
fornoydhet = 4                     # 1 til 5
```

Feil i fila (mangler, ugyldig TOML, e-post, passord, ukjent tur-ID, dato frem i tid, ugyldig verdi) gir en norsk melding som peker på registrering og felt, og databasen er uendret. Historikken gir grunnnivå blått, ingen sperre og én heving (`brukt_heving` settes til 0, så første søk viser hevingen).

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

En tur kan også ha `koblinger` rett under `[[tur]]` (før `[tur.rutepunkter]`), se Nordmarksrunden i lista:

```toml
koblinger = [[[60.0, 10.7], [60.00005, 10.7]]]   # [[lat, lon], [lat, lon]] per kobling; plassholder
```

| Felt | Regel |
|---|---|
| `id`, `navn` | Påkrevd tekst. Samme `id` kan ikke stå to ganger. |
| `form` | `tur-retur` eller `rundtur`. |
| `turtyper` | Liste med minst én av `marka`, `utsikt`, `topptur`. |
| `rutenummer` | Liste med rutenummer (`app:rutenummer`) som segmentene hentes for. Segmenter som deles mellom rutenumrene, tas med én gang. |
| `startpunkt` | `id`, `navn`, `lat`, `lon`. Det Ola ser og går fra, for eksempel en holdeplass eller en parkering. Uavhengig av rutepunktene. Samme startpunkt-ID må ha samme navn og koordinat i hele lista. |
| `rutepunkter` | `fra`, valgfri `via` og `til`, alle som `[lat, lon]` i WGS84. |
| `ut_no_url` | Valgfri tekst. Settes når turforslaget på ut.no dekker i hovedsak samme rute, med små forskjeller i start eller mål. |
| `koblinger` | Valgfri liste med par av `[lat, lon]`. Hvert par blir et rett segment i nettverket. Høyst 10 m mellom punktene. |

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

### Koblinger uten rutenummer

Noen steder mangler det et kort stykke uten rutenummer mellom to rutenumre i Turrutebasen, for eksempel ved Ullevålseter. Da kan turen ha `koblinger`: par av punkter som legges inn som rette segmenter før nettverket lages (story 1.7, beslutning 2). Punktene skal være de eksakte segmentendene fra WFS-svaret, så de blir samme node som segmentene (innenfor 1 m). En kobling over **10 m** (`MAKS_KOBLING_M`) stopper skriptet med tur-ID og avstand før noe hentes.

### Rundtur med stilk

En rundtur kan gå samme vei ut og inn på en stilk fra startpunktet til ringen. Skriptet regner ut hvor stor del av lengden som gås to ganger (strekninger mellom to punkter som forekommer mer enn én gang i linja, uten retning). Er det **mer enn halve lengden** (`MAKS_ANDEL_GATT_TO_GANGER`), stopper skriptet med tur-ID og andel, for da er turen i praksis en tur-retur (story 1.7, beslutning 4).

### Festing midt på et segment

Rutepunktene kan fortsatt bare festes til segmentender. Det holdt for alle de 15 turene i story 1.7: alle rutepunktene ligger på en node, og ingen tur trengte å dele et segment eller en lukket ring.

## Høyder og støyfilter

- Høydene hentes fra `https://ws.geonorge.no/hoydedata/v1/punkt` (`koordsys=4258`, punktene som `[lon, lat]`, høyst 50 per kall). Datakilden er terrengmodellen med 1 m oppløsning.
- **Punktavstand 25 m.** Stien deles opp i punkter hvert 25 m, med første og siste punkt. I spiken ga 25 m nesten samme resultat som 10 m (50 mot 51 m nedstigning med terskel 5 m) med 72 i stedet for 177 punkter, altså 2,5 ganger færre kall.
- **Terskel 5 m.** En høydeendring telles bare når den er minst 5 m fra forrige telte høyde (hysterese). Til slutt telles resten fra forrige telte høyde til siste punkt. Uten filter ble stigningen blåst opp med 15–20 m på en sti som går jevnt nedover langs en elv; med 5 m traff summen nettofallet nesten nøyaktig.
- `hoydeprofil` er de samme punktene som høydemeterne regnes fra: `[avstand_m, hoyde_m]`, med hele meter og høyde med én desimal.
- `startpunkt_hoyde_m` hentes fra det samme API-et ved startpunktets koordinat.
- 25 m og 5 m ble satt fra spiken (ett segment langs en elv) og er sjekket mot ut.no i story 1.7. Høydemeterne for `vettakollen-topp`, `frognerseteren-kobberhaughytta` og `noklevann-rundt` avviker −5 %, −12 % og −30 % fra ut.no. Regelen var å endre bare ved over 15 % avvik på minst to av tre, og avviket for Nøklevann kommer av at ut.no-turen starter ved Ulsrud stasjon. Kjørt på ut.no sin egen linje treffer 25 m og 5 m innen 2 % for Vettakollen (221 mot 220), Nøklevann (220 mot 223) og Fuglemyrhytta (226 mot 227), mens 2 m og 10 m bommer med rundt 25 % på Nøklevann. Kobberhaugene bommer med +29 % (555 mot 431), men summen av høydene i ut.no sin egen linje er 537, så tallet 431 kan ikke gjenskapes fra linja og ble ikke lagt vekt på. Verdiene beholdes. Tallene står i `docs/kontroll-turdatabasen.md`.

## Kreditering

- Turruter: Turrutebasen, © Kartverket, CC BY 4.0. Hver tur har `kilde = "turrutebasen"` og `lisens = "CC BY 4.0"`.
- Høyder: Kartverkets høydedata, © Kartverket, CC BY 4.0.
- OSM-uttrekket (når det kommer): © OpenStreetMap contributors, ODbL.

## Turene

De 15 turene i `kurateringsliste.toml` (story 1.7), bygget 2026-11-25. Lengde og høydemeter gjelder én vei ved tur-retur og hele runden ved rundtur. Tiden er estimert tid for hele turen (FR-3), uten pauser. Kontrollen av hver rutelinje står i `docs/kontroll-turdatabasen.md`.

| ID | Navn | Startpunkt | Form | km | Høydemeter opp/ned | Nivå | Tid | Turtyper | ut.no |
|---|---|---|---|---|---|---|---|---|---|
| `frognervassdraget` | Langs Frognervassdraget | Sognsvann | tur-retur | 2,21 | 6/47 | grønn | 1 t 30 min | marka | – |
| `sognsvann-brekke` | Sognsvann–Brekke turvei | Sognsvann | tur-retur | 1,11 | 17/1 | grønn | 45 min | marka | – |
| `frognerseteren-skjennungstua` | Frognerseteren–Skjennungstua | Frognerseteren | tur-retur | 5,16 | 126/120 | blå | 4 t | marka | – |
| `frognerseteren-kobberhaughytta` | Frognerseteren–Kobberhaughytta | Frognerseteren | tur-retur | 8,18 | 172/209 | blå | 6 t 20 min | marka | [1112157534](https://ut.no/turforslag/1112157534) |
| `nordmarksrunden` | Nordmarksrunden: Kobberhaughytta–Bjørnholt–Ullevålseter | Frognerseteren | rundtur | 22,98 | 710/710 | svart | 9 t 40 min | marka | – |
| `vettakollen-topp` | Vettakollen fra Vettakollen stasjon | Vettakollen stasjon | tur-retur | 2,15 | 185/24 | grønn | 2 t 10 min | topptur, utsikt | [114607](https://ut.no/turforslag/114607) |
| `vettakollen-fuglemyrhytta` | Vettakollen stasjon–Fuglemyrhytta | Vettakollen stasjon | tur-retur | 2,74 | 192/35 | grønn | 2 t 35 min | utsikt | [1112154257](https://ut.no/turforslag/1112154257) |
| `vettakollen-rundtur` | Rundtur Vettakollen og Fuglemyrhytta | Vettakollen stasjon | rundtur | 6,08 | 209/209 | blå | 2 t 40 min | topptur, utsikt | – |
| `rundtur-ulsrudvann` | Rundtur Ulsrudvann | Østmarksetra | rundtur | 1,65 | 13/13 | grønn | 30 min | marka | – |
| `noklevann-rundt` | Nøklevann rundt | Østmarksetra | rundtur | 8,23 | 156/156 | blå | 3 t | marka | [1110939](https://ut.no/turforslag/1110939) |
| `ostmarksetra-mariholtet` | Østmarksetra–Mariholtet | Østmarksetra | tur-retur | 3,92 | 146/136 | grønn | 3 t 30 min | marka | – |
| `kolsastoppen` | Kolsåstoppen fra Gjettum | Gjettum | tur-retur | 3,17 | 295/38 | grønn | 3 t 15 min | topptur, utsikt | – |
| `dalivann-rundt` | Dælivann rundt fra Gjettum | Gjettum | rundtur | 4,93 | 54/54 | grønn | 1 t 40 min | marka | – |
| `grorud-badedammen` | Grorud–Badedammen | Grorud stasjon | tur-retur | 1,76 | 74/0 | grønn | 1 t 20 min | marka | – |
| `grorud-grefsenkollen` | Grorud–Grefsenkollen gjennom Lillomarka | Grorud stasjon | tur-retur | 11,81 | 423/232 | rød | 9 t 35 min | utsikt | – |

Startpunktene er holdeplasser eller kjente steder: `sognsvann` og `ostmarksetra` er uendret fra story 1.5, `frognerseteren`, `vettakollen` og `grorud` er tatt fra kandidatlista (holdeplassene i Kartverkets stedsnavn-API), og `gjettum` er Gjettum (gard) fra stedsnavn-API-et. API-et gir tre treff for Gjettum; punktet for «Gjettum stasjon» ligger ca. 640 m fra ruten og ca. 550 m fra der Kolsåsbanen stopper i dag, så gården ble brukt. Holdeplassen Gjettum ligger ca. 300 m sørøst for gården.

`ut_no_url` står der turforslaget på ut.no dekker i hovedsak samme rute, med små forskjeller i start eller mål (for eksempel starter ut.no-turen rundt Nøklevann ved Ulsrud stasjon, og turen til Kobberhaughytta fortsetter opp på Kobberhaugene). Forskjellene står i `docs/kontroll-turdatabasen.md`. Kandidatene hadde flere lenker til turer med annen rute (eller som ikke finnes lenger); de er tatt bort.

## Sammensetning og unntak

`tests/skript/test_sammensetning.py` sjekker reglene i FR-1 mot `turer.geojson`, uten nett. Testen krever minst 15 turer, ikke nøyaktig 15.

| Regel | Krav | Nå |
|---|---|---|
| Grønne eller blå | flertallet | 13 av 15 (9 grønne, 4 blå, 1 rød, 1 svart) |
| Svarte turer | minst 1 | 1 (`nordmarksrunden`) |
| Toppturer | minst 3 | 3 (`vettakollen-topp`, `vettakollen-rundtur`, `kolsastoppen`) |
| Utsiktsturer | minst 5 | 5 (de tre toppturene, `vettakollen-fuglemyrhytta` og `grorud-grefsenkollen`) |
| Turer per startpunkt | minst 2 | Sognsvann 2, Frognerseteren 3, Vettakollen 3, Østmarksetra 3, Gjettum 2, Grorud 2 |
| Grønn tur under 2 t per turtype | hver turtype, unntatt begrunnede unntak | `marka`: 5 (korteste `rundtur-ulsrudvann`, 30 min). `topptur` og `utsikt`: unntak, se under |
| Kilde og lisens | på hver tur | `turrutebasen`, `CC BY 4.0` på alle |

`grorud-grefsenkollen` er ikke merket `topptur`: ruten slutter ved serveringsstedet på Grefsenkollen, ca. 20 m under toppen, og ingen rute i Turrutebasen går helt opp. Det følger regelen om at turtypen skal stemme med ruten (som for Tryvann).

### Unntak på grunn av terrenget

FR-1 krever en grønn tur under 2 t for hver turtype «der terrenget gjør det mulig». To turtyper har ingen slik tur. Unntakene står også i `UNNTAK_GRONN_UNDER_2_T` i `tests/skript/test_sammensetning.py`, og testen feiler hvis en turtype mangler en kort grønn tur uten å stå der, eller står der uten å trenge det.

- `topptur`: blant de 24 kandidatene i `_bmad-output/implementation-artifacts/research-1-7/kandidater.md`, fra de seks startpunktene i lista og tre til (Skullerud, Bogstad og Movann), finnes det ingen grønn topptur som når toppen på under 2 t tur-retur. Den korteste er Vettakollen fra Vettakollen stasjon, som er grønn, men tar 2 t 10 min tur-retur (185 høydemeter opp). Tryvann (35 min fra Frognerseteren) ble vurdert, men ruten slutter ca. 340 m fra Tryvannshøgda og når ikke toppen, så den kan ikke merkes som topptur (beslutning 3, 2026-11-25). Tryvann er derfor ikke med, og `frognerseteren-skjennungstua` er tatt inn i stedet.
- `utsikt`: utsiktspunktene ligger på toppene og åsene over byen, og stigningen dit gir samme tid som toppturene. Den korteste er også Vettakollen (2 t 10 min); Fuglemyrhytta tar 2 t 35 min.

## Testturene fra story 1.5

`frognervassdraget`, `sognsvann-brekke` og `rundtur-ulsrudvann` var testturene i story 1.5. De er med uendret blant de 15, så ingen gamle tur-ID-er blir liggende i databasen på Vercel (beslutning 1). `sognsvann-brekke` tok plassen til kandidaten `sognsvann-ullevalseter`. En fast kopi av den gamle lista og fila ligger i `tests/fixtures/` (`kurateringsliste_testturer.toml` og `turer_lastinn.geojson`), så testene for byggeskriptet og `lastinn` går uten nett og uavhengig av `data/`.
