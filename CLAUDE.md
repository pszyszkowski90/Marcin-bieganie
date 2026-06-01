# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Purpose

Personal running repository for **Marcin Szyszkowski** (M49, 64 kg, marathon PB 2:57).  
Not a code project — hosts training plans, race documentation, analytics, and a knowledge base for ultra running.  
Managed jointly by Paweł (brother, supporter) and Claude Code.

## Repository structure

```
marcin/          Athlete knowledge base — profile, race history, equipment
wiedza/          Reusable science — training theory, nutrition, tactics, risk
biegi/           Per-race directories — one subfolder per race
prompts/         Reusable LLM prompt templates
logs/            Training logs placeholder
```

**Key navigation:**
- Athlete profile: [marcin/README.md](marcin/README.md)
- Knowledge base: [wiedza/README.md](wiedza/README.md)
- Race history: [biegi/README.md](biegi/README.md)
- Last race: [biegi/PZLA-MP-24h-Pabianice-2026/](biegi/PZLA-MP-24h-Pabianice-2026/)

## Athlete profile (fixed anchor)

M49, 168 cm, 64 kg, ~10 yr running, 14 ultras (6× 100 km+).  
Marathon PB **2:57** Gdańsk 19.04.2026. Half 1:23. VDOT ~65.  
Last race: PZLA MP 24h Pabianice 30.05.2026 — **212.7 km, #8 open**.

## MCP servers

`.mcp.json` wires up: `mcp__strava__*`, `mcp__notion__*`, `mcp__hackmd__*`.  
On Strava auth errors call `connect-strava`. Never commit `.mcp.json`.

## Working conventions

- **Language**: Polish for all plans, notes, analyses. Technical terms in English.
- **Evidence tags**: `[EBM]`, `[OBSERWACJA]`, `[EKSTRAPOLACJA]`, `[PRAKTYKA]`, `[DO WERYFIKACJI]`
- **Source codes**: `[CB]`/`[CD]` Claude basic/details, `[GB]`/`[GD]` Gemini, `[R]` research
- **Date anchor**: Race day was 30.05.2026. Compute weeks/training labels from current harness date.
- **Distance goals** (Pabianice 2026): A 200–215 km, B 180–195 km, stretch 220–230 km — achieved 212.7 km.
- Never modify `.mcp.json`, `.env`, `*.secret` — they're gitignored.

## Race analytics scripts

`biegi/PZLA-MP-24h-Pabianice-2026/wyniki/dane/`:
- `pobierz_dane.py` — scrapes ProTimer (race 1434/edition 16030), outputs CSV
- `analizuj.py` — computes pacing metrics from CSV, generates `top10_analiza.md`

Run with: `python pobierz_dane.py` / `python analizuj.py` from the `dane/` directory.
