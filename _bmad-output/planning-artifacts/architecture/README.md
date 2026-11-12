# Arkitektur

| Fil eller mappe | Hva det er | Bindende? |
|---|---|---|
| [`architecture-G81-eriksen-2026-11-07/ARCHITECTURE-SPINE.md`](architecture-G81-eriksen-2026-11-07/ARCHITECTURE-SPINE.md) | Arkitekturen for *Your Next Adventure*, med beslutningene AD-1 til AD-14 | **Ja** |
| [`architecture-G81-eriksen-2026-11-07/.memlog.md`](architecture-G81-eriksen-2026-11-07/.memlog.md) | Beslutningsloggen: begrunnelser og alternativer som ble forkastet | Nei, bakgrunn |
| [`architecture-G81-eriksen-2026-11-07/reviews/`](architecture-G81-eriksen-2026-11-07/reviews/) | Gjennomgangene av arkitekturen | Nei, bakgrunn |
| [`technology.md`](technology.md) | Referanse fra faglærer: teknologi og arkitektur for en **annen app** (`pytagoras-website-v2`) | **Nei** |

Forklaringen for sensor står i [`docs/arkitektur.md`](../../../docs/arkitektur.md).

## Om `technology.md`

`technology.md` beskriver ikke denne appen. Ved motstrid gjelder alltid `ARCHITECTURE-SPINE.md`. Stories og kode skal ikke hente stack, tjenester eller nøkler derfra.

Mønstre fra referansen som arkitekturen allerede har:

| Mønster i `technology.md` | Slik er det løst her |
|---|---|
| Mock-fallback: appen virker uten nøkler | KI-variantene ekte, reserve og falsk (AD-10). Appen kjører uten nøkler (AD-12, NFR-1) |
| Demokontoer lastes ved oppstart | Testbrukeren lastes med `lastinn` (AD-3, FR-21) |
| Rate limiting på KI-ruter | Grense per nettleser og per døgn, ikke per IP, fordi v1 bare kjører lokalt (AD-10, NFR-8) |

Valgt bort: flere tjenester, Docker, Postgres, Redis og en egen frontend i Next.js. De bryter én prosess med SQLite (AD-1, AD-4) og kravet om at sensor kan kjøre appen på under 20 minutter (NFR-1). Betaling, e-post og regnskap er utenfor v1.
