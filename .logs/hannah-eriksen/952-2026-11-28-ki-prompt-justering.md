# KI: tenking av og prompt-justering

## 2026-11-28 — Hannah Eriksen

### Oppgave
Kjøre `docs/ki-testplan.md` mot ekte KI (claude-haiku-5-5) og rette det som viste seg.

### Resultat
- Lokal kjøring (SQLite): 10 KI-kall, 7 godkjent, 3 forkastet (2 `ugyldig`: tomt og avkuttet, 1 `tallord`: engelsk resonnement i svaret). Loggen hadde ingen personopplysninger.
- Årsak målt med direkte kall: modellen lager en «thinking»-blokk som spiser `max_tokens` (stop_reason `max_tokens`, 300 tokens), særlig for topptur-søk. Med `thinking: disabled` ga 5 av 5 gyldig tekst på ~70 tokens; med tenking på trengtes 350–490 tokens.
- Fix: `thinking={"type": "disabled"}` og `MAKS_TOKENS = 400` i `tjenester/ki/ekte.py`; prompten ber om ingen tenking/engelsk og at modellen ikke regner selv; test sjekker `thinking` i forespørselen.
- Kontroll etter fix: 12 av 12 ekte kall ga tekst med `{varighet}` og 100–190 tegn. 854 tester OK, ruff rent.

### Åpne punkter
- Kjør hele testplanen på nytt (vurder forkastelsesrate, UI-klikk i Nytt forslag, «Topptur erstattet» med 2 t som ga ingen tur) og fyll ut resultattabellene i `docs/ki-testplan.md`.
- Produksjon: sjekk etter deploy at KI-kall går innenfor 5 s timeout.
