# Psycopg blokkert av Smart App Control

## 2026-11-26 kl. 09:36 — Hannah Eriksen

### Oppgave
Hannah meldte at PR #32 var merget, og ba meg gjennomføre den anbefalte løsningen for blokkeringen. To tester i `tests.web.test_vercel` feilet lokalt fordi psycopg-DLL-en ble blokkert.

### Plan
- Les Code Integrity-loggen i Windows for å finne hva som blokkeres.
- Prøv anbefalingen: installer `psycopg-binary==3.3.9` på nytt i `venv/`.
- Det hjalp ikke. Hannah valgte deretter å hoppe over de to testene lokalt når psycopg ikke kan lastes.

### Resultat
- **Årsak:** Smart App Control er på (`VerifiedAndReputablePolicyState = 1`). Code Integrity-hendelse 3033/3077 viser at `psycopg_binary.libs/libpq-….dll` og `pq.cp314-win_amd64.pyd` blokkeres fordi de ikke er signert. Smart App Control gikk trolig over fra evaluering til «på» natt til 2026-11-26.
- **Ny installasjon:** hjalp ikke. Filene er identiske og usignerte.
- **Commit `022e395`** (`tests/web/test_vercel.py`): `test_check_deploy_er_ren` og `test_innstillingene_pa_vercel` hoppes over med en melding når `import psycopg` feiler. Den tredje testen i klassen kjører fortsatt.
- **Tester:** 301 kjørt, OK, med 2 hoppet over. Ruff er rent.
- Byggingen på Vercel sjekker fortsatt Postgres ved hver deploy (`migrate` og `lastinn` mot Neon).

### Åpne punkter
- Postgres-sjekken kjører ikke lokalt på denne PC-en så lenge Smart App Control er på. Byggeloggen på Vercel er kontrollen.
