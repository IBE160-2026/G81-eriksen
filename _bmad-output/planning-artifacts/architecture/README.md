# Arkitektur

| Fil eller mappe | Hva det er | Bindende? |
|---|---|---|
| [`architecture-G81-eriksen-2026-11-07/ARCHITECTURE-SPINE.md`](architecture-G81-eriksen-2026-11-07/ARCHITECTURE-SPINE.md) | Arkitekturen for *Your Next Adventure*, med beslutningene AD-1 til AD-15 | **Ja** |
| [`architecture-G81-eriksen-2026-11-07/.memlog.md`](architecture-G81-eriksen-2026-11-07/.memlog.md) | Beslutningsloggen: begrunnelser og alternativer som ble forkastet | Nei, bakgrunn |
| [`architecture-G81-eriksen-2026-11-07/reviews/`](architecture-G81-eriksen-2026-11-07/reviews/) | Gjennomgangene av arkitekturen | Nei, bakgrunn |
| [`technology.md`](technology.md) | Referanse fra faglærer: teknologi og arkitektur for en **annen app** (`pytagoras-website-v2`) | **Nei** |
| [`verifisering-technology.md`](verifisering-technology.md) | Sjekk av hvert valg i `technology.md` mot PRD, UX og spinen, med fem hull (H-1 til H-5) | Nei, bakgrunn |

Forklaringen for sensor står i [`docs/arkitektur.md`](../../../docs/arkitektur.md).

## Om `technology.md`

`technology.md` beskriver ikke denne appen. Ved motstrid gjelder alltid `ARCHITECTURE-SPINE.md`. Stories og kode skal ikke hente stack, tjenester eller nøkler derfra.

Mønstre fra referansen som arkitekturen allerede har:

| Mønster i `technology.md` | Slik er det løst her |
|---|---|
| Mock-fallback: appen virker uten nøkler | KI-variantene ekte, reserve og falsk (AD-10). Appen kjører uten nøkler (AD-12, NFR-1) |
| Demokontoer lastes ved oppstart | Testbrukeren lastes med `lastinn` (AD-3, FR-21) |
| Rate limiting på KI-ruter | Grense per nettleser og per døgn, ikke per IP (AD-10, NFR-8). Grensen per nettleser kan omgås ved å slette cookies, men totalgrensen per døgn holder kostnaden nede også på Vercel |
| Rate limiting på innlogging | Grense for mislykkede forsøk per e-post (AD-7, NFR-8) |
| Railway og Supabase for publisering | Vercel og Neon, som faglærer tilbyr (AD-15, NFR-10). Lokal kjøring virker uten noen av dem (NFR-1) |

Valgt bort: flere tjenester, Docker, Redis og en egen frontend i Next.js. De bryter én prosess (AD-1) og kravet om at sensor kan kjøre appen på under 20 minutter (NFR-1). Postgres brukes bare på Vercel, der SQLite ikke kan lagre data varig. Lokalt brukes fortsatt SQLite (AD-4). Betaling, e-post og regnskap er utenfor v1.
