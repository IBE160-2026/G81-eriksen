# Manuell testplan for KI-begrunnelsen (story 4.5)

Automatiske tester bruker bare falsk KI og falsk HTTP-transport. Denne planen sjekker begrunnelsen mot ekte KI, med tur- og søkedata fra appen. Den krever en Anthropic-konto og en nøkkel i `.env`, og kan gjøres etter merge. Storyen kan merges uten at tabellene under er fylt ut.

**Regler:** Nøkkelen står bare i `.env` lokalt og som `ANTHROPIC_API_KEY` for Production hos Vercel. Skriv aldri nøkkelen i denne filen, i chat, i en logg eller i en commit.

## Forberedelser

1. Legg nøkkelen i `.env` (`ANTHROPIC_API_KEY=...`). Kjør `venv/Scripts/python.exe manage.py lastinn` og `venv/Scripts/python.exe manage.py runserver`.
2. Slett `logs/ki.log` hvis den finnes, så du bare ser denne økten.
3. Bruk ett nettleservindu, uten innlogging. Grensen er 20 kall per nettleser siste time, så del planen i to økter ved behov. Hvert søk sender ett kall (første tur). «Nytt forslag» sender ett kall til.

## Søkene

Kjør minst 10 søk. Skriv i tabellen hva du så på første tur.

| # | Varighet | Turtype | Startpunkt | Merke (✦ Skrevet med KI / Begrunnelse fra mal) | Nevnte begrunnelsen varigheten? | Nevnte den turtypen? | Ser teksten naturlig ut? |
|---|----------|---------|------------|-----------------------------------------------|--------------------------------|----------------------|--------------------------|
| 1 | 1 time | ingen | ingen | | | | |
| 2 | 1,5 timer | Marka | ingen | | | | |
| 3 | 2 timer | Utsikt | ingen | | | | |
| 4 | 2,5 timer | ingen | velg ett | | | | |
| 5 | 3 timer | Marka | ingen | | | | |
| 6 | 3 timer | Utsikt | velg ett | | | | |
| 7 | 4 timer | ingen | ingen | | | | |
| 8 | 5 timer | Marka | ingen | | | | |
| 9 | 6 timer | Utsikt | ingen | | | | |
| 10 | 3 timer | Topptur (gruppe: se under) | ingen | | | | |
| 11 | 4 timer | Topptur | ingen | | | | |
| 12 | 2 timer | Topptur | ingen | | | | |
| 13 | 3 timer | ingen | ingen, **innlogget bruker med historikk** (testbrukeren) | | | | |

**Gruppen med topptur (rad 10–12):** Be om topptur med varigheter som ikke har noen topptur, så status blir «topptur erstattet» og turen er en utsiktstur. Begrunnelsen skal da si at turen er en utsiktstur og ikke kalle den topptur. Svar som mangler «utsikt», forkastes med årsaken `turtype`. Skriv ned hva du fikk.

Kontroller også per søk:

- Merket står rett over overskriften «Begrunnelse», og ✦ leses ikke opp av skjermleser.
- Last siden på nytt og trykk «Nytt forslag», og gå så tilbake med «Start fra første forslag igjen». Teksten og merket skal være uendret, og `logs/ki.log` skal ikke få nye linjer.
- Teksten har ingen sifre, tallord eller nivåord utenom det systemet har satt inn. Teksten er under 300 tegn.
- For rad 13: begrunnelsen er under 300 tegn også med setningen om nivå eller turtype fra historikken (systemet legger den til etter KI-teksten), og `logs/ki.log` har ingen e-post eller bruker-ID.
- Teksten nevner ikke startpunktet (KI får bare en ID).

## Resultat

Fyll ut etter alle søkene.

| Mål | Antall |
|-----|--------|
| Søk gjort | |
| Turer vist første gang (kall sendt) | |
| «✦ Skrevet med KI» | |
| «Begrunnelse fra mal» | |
| Forkastede svar (linjer i `logs/ki.log`) | |

Forkastelser per årsak i `logs/ki.log` (kalltype `begrunnelse`):

| Årsak | Antall | Eksempel på svaret (kort) |
|-------|--------|---------------------------|
| `tom` | | |
| `ugyldig` | | |
| `siffer` | | |
| `tallord` | | |
| `nivaord` | | |
| `turtype` | | |
| `for_lang` | | |
| `tidsavbrudd` | | |
| `feil` | | |

Vurdering: Hvor mange av begrunnelsene nevnte varigheten og turtypen når den var valgt? Er det noe i prompten (`tjenester/ki/prompt.py`) som bør justeres? Prompten kan justeres uten å endre kriteriene i `domene/ki_validering.py`.

## Slik leser du loggen

`logs/ki.log` har én linje per forkastet svar eller feil, skilt med tabulator: `tidspunkt`, `kalltype`, `årsak`, `svar`. Linjeskift i svaret står som `\n`.

- Vis alle: `cat logs/ki.log` (Git Bash) eller `Get-Content logs/ki.log` (PowerShell).
- Tell per årsak: `cut -f3 logs/ki.log | sort | uniq -c`.
- Linjer med kalltype `begrunnelse` er det denne planen gjelder. Linjer med tom kalltype og årsak `totalgrense` betyr at døgngrensen på 200 kall er nådd.
- Ingen linje skal ha e-post, bruker-ID eller søke-ID. Sjekk med `grep -c "@" logs/ki.log`, som skal gi 0.
- Filer eldre enn 30 dager slettes automatisk. Hos Vercel går loggen til standard ut og slettes etter 1 time, så kvalitetssikringen gjøres lokalt.

## Sjekk av nøkkelen hos Vercel

1. Kjør `vercel env ls`.
2. `ANTHROPIC_API_KEY` skal stå bare for Production, ikke for Preview eller Development.
3. Åpne en forhåndsvisning av en pull request og søk. Alle begrunnelser skal være «Begrunnelse fra mal», og siden skal virke som vanlig.
4. Uten nøkkel (tom `.env`) skal hele kjerneflyten virke som før med «Begrunnelse fra mal».

## Fritekstønsket (fylles ut i story 4.7)

Fritekstfeltet er ikke på plass før story 4.6 og 4.7. Raden under fylles ut da.

| # | Søk og fritekst | Tolkingen traff turene du ventet? | Nevnte begrunnelsen ønsket? | Merke | Merknad |
|---|-----------------|-----------------------------------|-----------------------------|-------|---------|
| F1 | (fylles ut i 4.7) | | | | |
