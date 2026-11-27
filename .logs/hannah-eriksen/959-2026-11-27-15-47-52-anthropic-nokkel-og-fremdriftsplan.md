# Anthropic-nøkkel og fremdriftsplan

## 2026-11-27 kl. 15:47 — Hannah Eriksen

### Oppgave
Ny fremdriftsplan mot fristen 15. desember (to ganger, med 2.3 og 3.3 i arbeid), forklaring av KI-nøkkel og kostnadstak, og innlegging av `ANTHROPIC_API_KEY` lokalt og hos Vercel før Epic 4.

### Plan
- Fremdrift ut fra `sprint-status.yaml`, byggerekkefølgen i `epics.md` og tempoet i git-loggen.
- Kostnadstak i to lag: appens grense (story 4.4, AR-12: 20 kall per nettleser per 60 min, 200 per døgn) og forhåndsbetalt kreditt uten auto-reload hos Anthropic.
- Nøkkelen skulle aldri vises i chat eller terminal: Hannah limer den inn i `.env`, og den sendes videre med pipe.

### Resultat
- Plan (27. nov ettermiddag): 3.3–3.4 i dag, 4.1–4.5 28.–29. nov, P2 30. nov–4. des (6.2 tur for tur), P2-stopp 4. des, 6.6 5. des, 6.7 7.–9. des, 6.8 10. des, buffer 11.–14. des, lever senest 14. des.
- Nøkkel laget i Anthropic-konsollen (Default workspace, uten Admin API). Den havnet først i en feil fil, `IBE160G81-eriksen.env`, fordi `code C:\…\.env` kjørt i Git Bash mistet skråstrekene. Den ble flyttet til `.env`, og feilfilen ble slettet. Den ble aldri committet.
- Kontrollert: én `ANTHROPIC_API_KEY`-linje i `.env`, `.env` git-ignorert, `.env.example` uendret, ingen nøkler i git-historikken og ingen andre filer med nøkkelen. `GET /v1/models` ga 200 og viser `claude-haiku-5-5`, og Django-settings leser nøkkelen.
- Vercel (`your-next-adventure`): `ANTHROPIC_API_KEY` lagt inn som Sensitive, **bare i Production** (AR-24). Preview har ingen nøkkel.
- Ingen kodeendringer.

### Åpne punkter
- Bekreft i Anthropic-konsollen at auto-reload er av (eventuelt utgiftsgrense på workspacet), så kreditten er et hardt kostnadstak.
- Når 4.5 er merget: sjekk at produksjonen viser KI-begrunnelse, og at forhåndsvisningene fortsatt bruker reservemalen.
- Avtal med 3–5 nybegynnere til brukertesten i 6.7 (ca. 7.–9. des).
