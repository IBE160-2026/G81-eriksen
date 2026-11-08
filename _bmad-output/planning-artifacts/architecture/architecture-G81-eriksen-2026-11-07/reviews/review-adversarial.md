# Adversarial gjennomgang – ARCHITECTURE-SPINE.md (2026-11-08)

Linse: To enheter ett nivå ned (stories bygget av ulike KI-agenter) følger hver AD ordrett, men bygger likevel noe som ikke passer sammen. Hvert par er et hull. Spinen er ikke endret. Kilder: spine, `.memlog.md`, PRD v1.3 + addendum v1.1, `EXPERIENCE.md`.

## Dom

**Ikke klar som byggekontrakt.** Lagdelingen, lagringen og grensene mot omverdenen er gode, men spinen sier *hvor* ting bor og ikke *hvilken form* delt tilstand har. Fire steder bærer tilstand mellom stories: økten, `turer.geojson`, KI-resultatet og «sist viste nivåtak». Ingen av dem har en fast form eller én eier. Med én nybegynner og én agent per story er det her det går galt. Tre hull er kritiske eller høye og bør lukkes før første story: H1, H2 og H3. Ett funn (H3) er en direkte motsigelse mellom spinen og PRD-en.

| # | Hull | Alvor | Ny/strammet AD |
| --- | --- | --- | --- |
| H1 | Øktens innhold har ingen form og ingen eier | Kritisk | Ny AD-14, strammer AD-5 |
| H2 | «Første søk etter heving» og «sist viste nivåtak» kan skrives på flere måter | Høy | Strammer AD-11 |
| H3 | KI-kallets rekkefølge og resultatform er udefinert, og sekvensdiagrammet motsier FR-12 | Høy | Strammer AD-10 |
| H4 | `turer.geojson` har motstridende feltnavn og enheter og ingen felles datatype | Høy | Ny AD-15, strammer AD-3 |
| H5 | `lastinn` kan være idempotent på en måte som sletter brukernes historikk | Høy | Strammer AD-3.3 |
| H6 | Nivåregler og utvalg har ingen felles resultatform, så FR-8, FR-12, FR-17 og FR-17.1 teller hver for seg | Middels | Strammer AD-11, ny regel i AD-2 |
| H7 | Flere faner deler én økt; registrering og «adressen åpnet direkte» kolliderer | Middels | Strammer AD-5, AD-7 |
| H8 | Værbufferen: uklart hvem som tolker MET-svaret, tidssone og «ingen data»-grunn | Middels | Strammer AD-9 |

---

## H1 – Øktens innhold har ingen form og ingen eier (Kritisk)

**Par som kolliderer.**
- *Story A (søk, FR-4/FR-5)* lagrer `request.session["sok"] = {"dato": date(2026, 11, 7), …}` og `request.session["vist"] = {"granvann-rundt"}`. AD-5 sier bare at økten «lagrer søket, ID-ene til turene som er vist …».
- *Story B (Nytt forslag, FR-7)* gjør `request.session["vist"].append(tur_id)`.
- *Story C (søk på nytt)* leser «Et nytt søk erstatter økten» (AD-5) ordrett og kaller `request.session.flush()` eller `cycle_key()` + `clear()` før det nye søket lagres.

**Hva skjer.**
- Djangos standard `JSONSerializer` kan ikke lagre `datetime.date` eller `set`. Story A krasjer ved lagring (NFR-2).
- Endring på stedet (`.append` på en liste i økten) setter ikke `session.modified`. Story B ser ut til å virke, men listen over viste turer forsvinner ved neste innlasting, og samme tur vises igjen (bryter FR-7).
- Story C logger ut brukeren ved hvert nytt søk, fordi innloggingen også ligger i økten.
- Ingen story eier nøklene, så «Endre søk», «Prøv 3 timer», KI og innlogging leser og skriver hver sine navn.

**Foreslått regel (ny AD-14, og AD-5 strammes).**

> **AD-14 — Øktinnholdet har én form og én eier.**
> **Rule:**
> 1. Alt turforslag-innhold i økten ligger under én nøkkel, `request.session["turforslag"]`. Ingen annen kode leser eller skriver økten direkte, med unntak av Djangos auth og messages.
> 2. Formen er dataklassen `domene.okt.Turforslagsokt` med `til_dict()` og `fra_dict()`. Den har feltene `sok` (`Sok`: `varighet_min: int`, `dato: date`, `startpunkt_id: str | None`, `turtype: str | None`, `fritekst: str`), `vist: list[str]` (tur-ID-er i visningsrekkefølge), `gjeldende: str | None`, `nivaheving: bool` (H2) og `ki: KiResultat | None` (H3). I `til_dict()` lagres datoer som ISO-streng og mengder som sortert liste, slik at JSON-serialiseringen virker.
> 3. Bare `turforslag/okt.py` har `les_okt(request) -> Turforslagsokt | None`, `lagre_okt(request, okt)` og `slett_okt(request)`. `lagre_okt` erstatter alltid hele verdien (aldri endring på stedet), slik at Django merker økten som endret.
> 4. «Et nytt søk erstatter økten» betyr: `lagre_okt` med et nytt `Turforslagsokt`. Ingen kode kaller `session.flush()`, `cycle_key()` eller `clear()` unntatt Djangos `login()` og `logout()`.
> 5. Utlogging og kontosletting fjerner økten gjennom `logout()` (FR-15: brukeren står igjen som gjest uten forslag). Kontosletting gjør rekkefølgen *slett i transaksjon → `logout()` → legg til kvittering → redirect*.

---

## H2 – «Første søk etter heving» og «sist viste nivåtak» (Høy)

AD-11: «Er beregnet nivåtak høyere [enn sist viste], er søket det første etter heving, og verdien oppdateres.» Regelen sier ikke *når* i flyten dette skjer, *hva* som regnes som ett søk, eller *hvor* resultatet huskes.

**Par som kolliderer.**
- *Story A (søk-POST)* sjekker og oppdaterer `bruker.sist_viste_nivatak` i POST og rangerer med nivåheving-prioritet.
- *Story B (Nytt forslag)* rangerer på nytt og spør også `beregnet > sist_viste`. Det er nå usant, så turene rangeres uten nivåheving. Rekkefølgen skifter midt i samme søk: blå tur først, så plutselig grønne turer i en annen rekkefølge. Det bryter FR-5, som sier at prioriteten gjelder hele «det første søket».
- *Story C (personaliseringssetning, FR-12)* må vite om nivåhevingen påvirket valget. Ved innlasting (GET) finnes ikke den informasjonen lenger.

**Flere kanttilfeller som gir ulike svar.**
- Søket gir «ingen treff» eller «bare over nivåtaket» (FR-8). Er hevingen da brukt opp?
- Skjemafeil (FR-4) eller dobbel innsending (NFR-2, uten JS for å sperre knappen, AD-1). Andre POST sletter flagget, og brukeren ser forslaget uten nivåheving.
- Sperre senker nivåtaket under «sist viste». Én agent setter `sist_viste = beregnet` hver gang (også nedover), en annen bare når verdien er høyere. Etter at sperren er opphevet, gir den første tolkningen «heving» igjen, den andre ikke.
- Gjest logger inn midt i et søk. Ble flagget beregnet for gjesten (grønt) eller for brukeren?
- Hva setter `lastinn` som startverdi for testbrukeren (FR-21 skal vise nivåheving)?

**Foreslått regel (AD-11 strammes).**

> **AD-11 (tillegg) — Nivåheving avgjøres én gang per søk og lagres i økten.**
> 1. Bare søk-POST som har bestått skjemavalideringen, avgjør nivåheving: `nivaheving = beregnet_nivatak > bruker.sist_viste_nivatak`. Er den sann, settes `bruker.sist_viste_nivatak = beregnet_nivatak` i samme request. Verdien skrives aldri nedover. Sperre og opphevet sperre endrer den ikke, og opphevet sperre regnes ikke som heving.
> 2. Flagget lagres i `Turforslagsokt.nivaheving` (AD-14) og brukes uendret av «Nytt forslag», «Start fra første forslag igjen», innlasting og personaliseringssetningen. Ingen av dem leser `sist_viste_nivatak`.
> 3. Hevingen regnes som brukt når søket er sendt, også om resultatet blir ingen treff (FR-8).
> 4. Dobbel innsending: er det nye søket likt `okt.sok` og `okt.nivaheving` er sann, arver det nye søket flagget.
> 5. Gjester har ikke `sist_viste_nivatak`, og `nivaheving` er alltid usann. Innlogging midt i et søk endrer ikke flagget. Det nye nivåtaket gjelder fra neste søk (se H3/H6 om omrangering etter innlogging).
> 6. Ny bruker får `sist_viste_nivatak = grønn`. `lastinn` setter testbrukerens verdi til nivået *før* siste heving i den oppdiktede historikken, slik at testbrukerens første søk viser nivåhevingen (FR-21). Nivåtakets rekkefølge lagres som heltall 0–3 (grønn–svart).

---

## H3 – KI-kallets rekkefølge og resultatform (Høy, motsigelse mot PRD)

**Motsigelse.** Sekvensdiagrammet sier «fritekst + treff (bare hvis fritekst og nøkkel)». FR-12 sier «Når KI er tilgjengelig, skriver KI begrunnelsen», og UJ-1 viser at Ola *uten* fritekst får «✦ Skrevet med KI». En agent som følger diagrammet, leverer aldri KI-begrunnelse uten fritekst. En agent som følger FR-12, kaller KI ved hvert søk.

**Par som kolliderer.**
- *Story A (KI-modul)* lager ett kall: tolk fritekst og returner `list[str]` med ID-er (FR-11). Det er dette diagrammet viser, før rangeringen.
- *Story B (begrunnelse, FR-12)* trenger en tekst for *den valgte turen*. Den er først kjent etter rangeringen, som bruker resultatet fra A. B legger inn et nytt kall etter rangeringen.
- *Story C (Nytt forslag)* følger AD-5 («KI-resultatet for det [gjeldende forslaget]») og kaller KI på nytt for den nye turen. Story A lagret ID-listen i økten og forventer at den gjenbrukes.

**Hva er udefinert.**
- Ett eller to kall per søk, og ett kall per forslag eller per søk.
- Gjelder grensen på 5 s per kall eller for hele søket?
- Personaliseringssetningen må være kjent *før* 300-tegnskontrollen (addendum steg 4–5). Den avhenger av valgt tur og nivåheving (H2). Hvem setter sammen hva, og i hvilken rekkefølge?
- Feiler kall 2 etter at kall 1 lyktes: brukes fritekst-rangeringen da fortsatt? Skal «Jeg kunne ikke ta hensyn til ønsket ditt» vises?
- Hva lagres i økten? Rå KI-tekst med plassholdere eller ferdig tekst?
- Innlogging midt i et søk endrer nivåtaket og dermed treffene. KI-ID-ene ble validert mot de gamle treffene.

**Foreslått regel (AD-10 strammes, og sekvensdiagrammet rettes).**

> **AD-10 (tillegg) — Ett KI-kall per søk, fast resultatform.**
> 1. KI kalles én gang per godkjent søk-POST når nøkkelen finnes, med eller uten fritekst. Kallet får søket og de filtrerte treffene og returnerer for hele søket `KiSvar(passer_onsket: list[str], begrunnelser: dict[str, str])`, der hver begrunnelse er tekst med plassholdere per tur-ID. Uten fritekst er `passer_onsket` tom. Grensen på 5 s gjelder hele kallet.
> 2. `domene.ki.valider_svar(svar, treff_ider) -> KiResultat` gir `KiResultat(kilde: "ki" | "reserve", passer_onsket: list[str], begrunnelser: dict[str, str], fritekst_ignorert: bool)`. Er hele svaret ugyldig, gir det `kilde="reserve"`, `passer_onsket=[]` og `fritekst_ignorert = bool(fritekst)`. Resultatet lagres i `Turforslagsokt.ki` (AD-14).
> 3. Begrunnelsen for en vist tur lages av én domenefunksjon, `lag_begrunnelse(tur, sok, ki_resultat, personaliseringssetning) -> Begrunnelse(tekst, kilde)`. Den setter inn plassholderne, legger personaliseringssetningen til og sjekker 300 tegn. Feiler sjekken for denne turen, brukes reservemalen for *denne* turen. Rangeringen endres ikke, og `fritekst_ignorert` endres ikke.
> 4. «Nytt forslag», «Start fra første forslag igjen» og innlasting kaller aldri KI. De bruker `okt.ki`.
> 5. Innlogging midt i et søk endrer ikke det gjeldende forslaget eller `okt.ki`. «Nytt forslag» etter innlogging rangerer med brukerens nivåtak og historikk, men KI-treff gjelder bare ID-er som finnes i `okt.ki.passer_onsket`. Nye treff regnes som «passer ikke ønsket».
>
> Sekvensdiagrammet endres til «søk + treff (hvis nøkkel)».

*Alternativ hvis tokenbruken bekymrer:* begrens `begrunnelser` til de N første treffene i rangeringen, og bruk reservemalen for resten. Regelen må uansett si det.

---

## H4 – `turer.geojson` har ingen felles datatype (Høy)

AD-3.2 sier «feltene i addendumet pluss `kilde` og `lisens`». Addendumet lister `lengde_km`, `gradering` og `estimert_tid`. Konvensjonene sier «lengde i meter», «hele minutter» og domenebegrepet `turniva`.

**Par som kolliderer.**
- *Story A (byggeskript)* følger addendumet ordrett: `lengde_km: 3.5`, `gradering: "grønn"` og `form: "tur-retur"`. For tur-retur lagres lengde og høydemeter for én vei (PRD §3) og `estimert_tid` for hele turen (FR-3).
- *Story B (`lastinn` og modell)* følger konvensjonen: `lengde_m: int` og `turniva` som tekst eller heltall. Feltet `lengde_km` mangler, og B lagrer 0 eller krasjer.
- *Story C (visning, FR-6)* viser «total lengde». C vet ikke at tur-retur må dobles, eller dobler én gang til fordi B allerede doblet ved innlesing.
- Addendumet har ikke feltene `id`, `navn`, `turtyper`, `ut_no_url`, startpunktets koordinat eller ID, `hoydeprofil`-format (avstand og høyde i hvilken enhet, og én vei eller hele turen) og `geometry` med koordinatrekkefølge.
- Startpunkt: ER-diagrammet har STARTPUNKT som entitet, men kurateringslista gir navn og koordinat per tur. To turer fra «Granvannet p-plass» med litt ulike koordinater blir to startpunkter i lista (A) eller ett (B). Værbuffernøkkelen (AD-9) avhenger av koordinaten.

**Foreslått regel (ny AD-15, og AD-3.2 strammes).**

> **AD-15 — Én datatype for tur, brukt av bygging, innlesing og visning.**
> 1. `domene.tur.Tur` (frozen dataklasse) er den eneste beskrivelsen av en tur. Byggeskriptet skriver den med `til_geojson_feature()`, og `lastinn` leser den med `fra_geojson_feature()`. Begge funksjonene ligger i `domene/` og testes med en rundtur-test.
> 2. Feature-felt (`properties`): `id` (stabil streng, `[a-z0-9-]`), `navn`, `startpunkt_id`, `startpunkt_navn`, `startpunkt_lat`, `startpunkt_lon` (4 desimaler), `form` (`"tur_retur"` | `"rundtur"`), `turtyper` (liste av `"marka"` | `"utsikt"` | `"topptur"`), `lengde_m`, `hoydemeter`, `nedstigning` (heltall meter, **én vei for tur_retur**, hele runden for rundtur, som i PRD §3), `hoydeprofil` (liste av `[avstand_m, hoyde_m]` heltall, samme retning som `lengde_m`), `turniva` (`"gronn"` | `"bla"` | `"rod"` | `"svart"`), `estimert_tid_min` (hele turen, ikke avrundet til 5), `ut_no_url` (str eller null), `kilde`, `lisens`. `geometry` er LineString i WGS84 med `[lon, lat]`.
> 3. Totalverdier for visning (total lengde, høydemeter for hele turen, laveste og høyeste punkt) gis bare av `domene.tur`-funksjoner (`total_lengde_m(tur)` osv.), aldri av modell, view eller mal. Avrunding til 5 min skjer bare i formateringen (konvensjon Tid og tall).
> 4. Startpunkt har egen ID i kurateringslista. Koordinaten tilhører startpunktet, ikke turen, og `lastinn` lager én `Startpunkt`-rad per ID.
>
> Addendumets feltnavn (`lengde_km`, `gradering`, `estimert_tid`) erstattes av disse. Endringen føres i addendumet.

---

## H5 – `lastinn` kan være «idempotent» på en måte som sletter historikk (Høy)

AD-3.3: «Kommandoen kan kjøres flere ganger med samme resultat.»

**Par som kolliderer.**
- *Story A (`lastinn`)* oppnår «samme resultat» med `Tur.objects.all().delete()` og deretter `bulk_create`.
- *Story B (registrering, FR-16)* lager `Registrering.tur = ForeignKey(Tur, on_delete=CASCADE)`, som er Djangos vanlige valg.
- Resultat: når turdatabasen bygges på nytt og `lastinn` kjøres igjen, forsvinner alle registreringer, og nivåtakene faller til grønt uten varsel. Med `PROTECT` krasjer i stedet `lastinn`.
- *Story C (testbruker, FR-21)*: Betyr «samme resultat» at testbrukerens historikk og `sist_viste_nivatak` tilbakestilles hver gang? Gjør de det ikke, kan sensor ikke se nivåhevingen to ganger. Gjør de det, slettes testbrukerens registreringer fra demoen.
- Økten (AD-5) kan inneholde tur-ID-er som ikke lenger finnes etter en ny bygging.

**Foreslått regel (AD-3.3 strammes).**

> 3. `lastinn` oppdaterer turer og startpunkter etter ID (`update_or_create`) og sletter aldri en tur som har registreringer. Finnes en tur med registreringer ikke lenger i filen, stopper kommandoen med en tydelig melding og endrer ingenting (én transaksjon). `Registrering.tur` har `on_delete=PROTECT`. Testbrukeren slettes og lages på nytt fra `data/testbruker.*` ved hver kjøring, med registreringer og `sist_viste_nivatak` (AD-11). Det gir samme demo hver gang. Andre brukere røres ikke. Views som leser tur-ID fra økten, behandler en ukjent ID som «forslaget finnes ikke lenger».

---

## H6 – Ingen felles resultatform for nivå og utvalg (Middels)

AD-11 sier at «nivåtak, sperre, fremgang mot neste nivå og foretrukne turtyper beregnes … av rene funksjoner». Flertallsformen inviterer til flere funksjoner som hver går gjennom historikken.

**Par som kolliderer.**
- *Story A (FR-19)* skriver `beregn_nivatak(registreringer)`, som teller lette turer «fra siste nivåendring» og tolker sperre på sin måte.
- *Story B (FR-17.1, fremgang)* skriver `fremgang(registreringer)` og teller på nytt. Teller B lette turer tatt under sperre, mens A ikke gjør det, viser historikken «3 av 3 – neste gang blå», men søket gir fortsatt grønt.
- *Story C (FR-12, personaliseringssetning)* trenger «de tre siste grønne turene var lette» eller sperre-grunnen. C leter i historikken på egen hånd.
- *Story D (FR-8)* trenger å vite om bare turer *over* nivåtaket passer, og om brukeren har historikk. D filtrerer på nytt i view og bryter AD-2. Eller filterfunksjonen returnerer bare en liste, og D gjetter.
- Topptur-erstatning (FR-8): legger filterfunksjonen eller view-et inn utsiktsturer? Gjelder «Nytt forslag» etterpå utsiktslista?

**Foreslått regel (AD-11 og AD-2 strammes).**

> **AD-11 (tillegg):** Én funksjon, `domene.niva.vurder_historikk(registreringer) -> NivaStatus`, går gjennom historikken. Den returnerer `NivaStatus(nivatak, grunnniva, sperre_aktiv, sperre_grunn, lette_mot_neste, siste_heving_grunnlag, foretrukne_turtyper, har_historikk)`. FR-5, FR-8, FR-12 (personaliseringssetning), FR-17 (merknaden over nivåtaket) og FR-17.1 leser bare fra `NivaStatus`. Ingen annen kode går gjennom registreringene.
>
> **AD-2 (tillegg):** `domene.utvalg.velg_turer(turer, sok, niva, ki, nivaheving, gjennomforte) -> Utvalg` returnerer `Utvalg(status, rangert: list[str], melding_nokkel)`, der `status ∈ {TREFF, TOPPTUR_ERSTATTET, BARE_OVER_NIVATAK, INGEN_TREFF}`. Topptur-erstatningen og sjekken «bare over nivåtaket» skjer inne i funksjonen. «Nytt forslag» går videre i `rangert` fra samme kall, og views filtrerer aldri turer selv.

---

## H7 – Flere faner deler én økt; registrering og «adressen åpnet direkte» (Middels)

Djangos økt følger nettleseren, ikke fanen, og innloggingen varer i 2 uker (AD-6). PRD §3 og UX sier at økten varer «til … fanen lukkes» og at «adressen åpnet direkte» gir «Forslaget finnes ikke lenger». UJ-2 forutsetter flere faner.

**Par som kolliderer.**
- *Story A (Registrer gjennomført tur fra turforslaget)* henter turen fra `okt.gjeldende` (AD-5: økten har «gjeldende forslag»). Har brukeren søkt i fane B etterpå, registreres turen fra fane B mens hen står i fane A.
- *Story B (FR-14, gjest → logg inn → rett inn i registreringen)* bruker `?next=/registrer/` uten tur-ID og stoler på økten. Det går galt på samme måte.
- *Story C (tilstanden «adressen åpnet direkte»)* tester at en ny fane mot `/turforslag/` viser meldingen. *Story D (AD-5, innlasting)* viser forslaget fra økten for samme URL. Begge følger reglene, og testene motsier hverandre.

**Foreslått regel (AD-5 og AD-7 strammes).**

> **AD-5 (tillegg):** Det finnes ett aktivt søk per nettleser. Et søk i én fane erstatter forslaget i alle faner, og det er et dokumentert avvik fra «fanen lukkes» i PRD §3. «Forslaget finnes ikke lenger» vises når `les_okt` gir `None` eller når turen ikke finnes (H5). En innlasting viser alltid det som ligger i økten, også i en ny fane.
>
> **AD-7 (tillegg):** Registrering tar turen fra URL-en (`/registrer/<tur_id>/`) og validerer at ID-en finnes i `Tur`. Tur-ID er offentlig katalogdata, ikke søk eller forslag, så AD-5 forbyr ikke dette. Registreringen leser aldri turen fra økten. Krav om innlogging bruker Djangos `next` med den samme URL-en, og `next` godtas bare når `url_has_allowed_host_and_scheme` godkjenner den.
>
> *Alternativ (mer arbeid):* en tilfeldig `sok_id` per søk i URL-en, som slås opp bare i denne økten. Det gir ekte faneisolasjon. Velges bare hvis gruppa vil holde seg til PRD §3 ordrett.

---

## H8 – Værbufferen: tolking, tidssone og «ingen data» (Middels)

AD-9 sier hvor MET kalles og hvordan svaret bufres, men ikke hva tjenesten leverer til domenet.

**Par som kolliderer.**
- *Story A (`tjenester/met.py`)* bufrer rå JSON og returnerer `dict | None`.
- *Story B (`domene/` bekledningstips)* forventer en dataklasse med verdier for kl. 10–16 og tolker «10–16» som UTC-tidene i MET-svaret (MET bruker UTC). Det gir tips for kl. 11–17 eller 12–18 norsk tid.
- FR-10 krever en melding om *hvorfor* det ikke finnes tips. «Ingen data» (AD-9) skiller ikke mellom at MET ikke svarer og at datoen er for langt frem.
- *Story C (forslag-GET ved innlasting)* henter været på nytt. *Story D* forventer det i økten. Ingen av dem er feil etter AD-5.
- To samtidige forespørsler mot et tomt buffer lager to rader med samme nøkkel og krasjer, eller sender to MET-kall. Et 304-svar fra MET må oppdatere `Expires`, ellers spørres MET ved hvert treff.

**Foreslått regel (AD-9 strammes).**

> `tjenester.met.hent_varsel(lat, lon) -> Varsel | None` returnerer en tolket `domene.vaer.Varsel` (tidsserie med tidspunkter i UTC), aldri rå JSON, og `None` bare når MET ikke svarer. `domene.vaer.dagtid(varsel, dato) -> Dagtidsvaer | IngenVarsel(grunn)` velger kl. 10–16 Europe/Oslo og gir `grunn ∈ {"met_svarer_ikke", "for_langt_frem"}`. Bekledningstipsene lages bare fra `Dagtidsvaer`. Bufferen har unik nøkkel `(lat4, lon4)` og skrives med `update_or_create`. Et 304-svar oppdaterer `Expires`. Været lagres ikke i økten: forslag-GET spør proxyen hver gang, og bufferen gjør det billig. Turforslag fra historikken bruker dagens dato (FR-17).

---

## Mindre funn (ikke prioritert)

- **Tur-ID som siste avgjører:** Konvensjonen «uten æ/ø/å» gjelder identifikatorer i koden, ikke tur-ID. Si `[a-z0-9-]` for tur-ID (tatt med i AD-15), så Python-sortering og ORM-`order_by` alltid gir samme rekkefølge.
- **Konfigurasjon:** For at «I dag» skal bli riktig, trengs `TIME_ZONE = "Europe/Oslo"`, `USE_TZ = True` og `timezone.localdate()` som eneste kilde til dagens dato i views. Én linje i konvensjonen Datoer.
- **AD-7 «alle sider med brukerdata krever innlogging»:** Registrering fra Historikk og fra turforslaget bruker samme view (H7), så tilgangskontrollen finnes bare ett sted.
