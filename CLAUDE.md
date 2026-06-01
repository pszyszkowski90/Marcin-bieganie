# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

Personal workspace for preparing user **Marcin (M49, 64 kg)** for the **PZLA MP 24h ultramarathon, Pabianice, 30.05.2026** (1725 m flat asphalt loop, target 200+ km). It is **not a code project** — it hosts:

1. The synthesized training/pacing/nutrition plan ([Plan 24h - Źródło Prawdy.md](Plan%2024h%20-%20%C5%B9r%C3%B3d%C5%82o%20Prawdy.md)).
2. Raw LLM outputs from independent analyses ([LLM Output/](LLM%20Output/)).
3. Prompts and source material used to generate those analyses ([prompts/](prompts/)).
4. MCP server configuration ([.mcp.json](.mcp.json)) for Strava, Notion, and HackMD.

Most work is reading/editing Markdown, pulling Strava activity data via the MCP, and reconciling conflicting recommendations between sources.

## Repository layout

- **`Plan 24h - Źródło Prawdy.md`** — the canonical "source of truth" plan. Everything else feeds into it. When the user asks to update the plan, edit this file. It uses:
  - **Evidence tags**: `[EBM]` (RCT/meta-analysis), `[OBSERWACJA]`, `[EKSTRAPOLACJA]`, `[PRAKTYKA]`, `[DO WERYFIKACJI]`.
  - **Source codes**: `[CB]`/`[CD]` Claude basic/details, `[GB]`/`[GD]` Gemini basic/details, `[CT]`/`[GT]` tempo, `[CŻ]`/`[GŻ]` żywienie, `[R]` weryfikacyjny research.
  - **`> ⚠️ SPORNA KWESTIA`** callouts where the six analyses disagree — preserve them; don't collapse to a single recommendation unless the user has decided.
  Preserve this notation when editing.
- **`LLM Output/`** — raw analyses, organized by topic (`ogólne/`, `tempo/`, `żywienie/`). Read-only inputs to the source-of-truth doc unless the user explicitly asks to add a new analysis.
- **`prompts/`** — prompts used to generate the LLM outputs, plus race regulations, athlete history, and the NotebookLM prompt for the 14-paper science notebook.
- **`logs/`** — empty placeholder for run/training logs.
- **`docs/`** — Obsidian-style knowledge base with atomic notes and `[[wikilinks]]`. Captures **why** decisions were made (uzasadnienia), not **what** to do (that's in `Plan 24h - Źródło Prawdy.md`). Entry point: [docs/README.md](docs/README.md) (MOC). Folders are numbered to keep ordering: `00-Kontekst`, `10-Cele`, `20-Trening`, `30-Żywienie`, `40-Taktyka`, `50-Sprzęt`, `60-Support`, `70-Ryzyko`, `80-Decyzje` (ADR-style decision log), `90-Źródła`. **When updating the plan, also update or create the matching note in `docs/`** so future conversations have the rationale. New significant decisions go in `docs/80-Decyzje/` as a new `DEC-NNN ...` ADR.

## MCP servers

`.mcp.json` wires up three MCPs. **Always prefer these tools over hand-rolled HTTP calls.**

- **`mcp__strava__*`** — Strava data: activities (`get-recent-activities`, `get-all-activities`, `get-activity-details`, `get-activity-streams`, `get-activity-laps`), athlete (`get-athlete-profile`, `get-athlete-stats`, `get-athlete-zones`), segments, route export (`gpx`/`tcx`), connection helpers. Access tokens are short-lived; on auth errors call `connect-strava` rather than editing `.mcp.json` by hand.
- **`mcp__notion__*`** — Notion API (the user may store training logs there).
- **`mcp__hackmd__*`** — HackMD notes (collaborative markdown).

## Working conventions

- **Language**: the plan, prompts, and most LLM outputs are in **Polish**. Match the user's language and the document's existing language when editing. Technical terms (RE, EBM, taper, B2B, gut training, durability) are kept in English by convention — do not translate them.
- **Athlete profile is fixed** and referenced throughout: 49 y, 168 cm, 64 kg, ~10 yr running, 13 ultras (6× 100 km+), 160 km in 22:44 (Rumia 2021, trail), marathon PB **2:57 Gdańsk 19.04.2026**, half 1:23, 3000 m 10:31, ~60 km/wk recent volume. Don't paraphrase these numbers loosely — they anchor every prediction in the plan.
- **Race day is anchored**: 30.05.2026. Use the date set by the harness when computing weeks-to-race or training week labels (T-6, T-5, …, T-1). Race format: solo, supported by brother Paweł (no support experience), forecast 15–22 °C day / 8–13 °C night, possible rain.
- **Distance goals**: A 200–215 km, B 180–195 km, stretch 220–230 km. Predictive models (Knechtle 2011, ekstrapolacje z Pabianic 2020 i Rumia 2021, DUV M45–50) all live in section 0 of the plan — reference them rather than inventing new targets.
- **Evidence-first edits**: when adding a claim to `Plan 24h - Źródło Prawdy.md`, attach an evidence tag and (if non-trivial) a source code. Do not silently introduce recommendations without a source.
- **Token / secrets hygiene**: `.mcp.json`, `.env`, and `*.secret` are gitignored. Never commit them and never paste their contents into chat or generated docs.
