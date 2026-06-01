# Marcin — bieganie

Repozytorium przygotowań biegowych Marcina Szyszkowskiego.  
Prowadzone przez Pawła (brat, supporter) wspólnie z Claude Code.

---

## Struktura

```
marcin/          Baza wiedzy o zawodniku — profil, historia startów, sprzęt
wiedza/          Baza wiedzy ogólna — teoria biegów ultra, żywienie, taktyka, ryzyko
biegi/           Katalog biegów — jeden podkatalog na każdy start
prompts/         Szablony promptów do przyszłego planowania z LLM
logs/            Dzienniki treningowe
```

---

## Biegi

| Rok | Bieg | Format | Dystans | Miejsce | Link |
|-----|------|--------|---------|---------|------|
| 2026 | PZLA MP 24h Pabianice | 24h, pętla 1725 m | 212.7 km | #8 open / #5 M40 | [biegi/PZLA-MP-24h-Pabianice-2026](biegi/PZLA-MP-24h-Pabianice-2026/) |

---

## Nawigacja po bazie wiedzy

**Zawodnik**: [marcin/README.md](marcin/README.md)  
**Wiedza ogólna**: [wiedza/README.md](wiedza/README.md)

---

## Jak używać tego repo przy planowaniu nowego biegu

1. Zapoznaj się z aktualnym profilem zawodnika → `marcin/`
2. Dobierz wiedzę tematyczną do formatu biegu → `wiedza/`
3. Utwórz nowy katalog w `biegi/NAZWA-BIEGU-ROK/`
4. Jako bazę użyj struktury z `biegi/PZLA-MP-24h-Pabianice-2026/` (plan/, kontekst/, decyzje/, wyniki/)
5. Zapisuj decyzje treningowe jako pliki DEC-NNN w `decyzje/`

---

## MCP / narzędzia

`.mcp.json` łączy z: Strava API, Notion, HackMD.  
Tokeny i sekrety są w `.gitignore` — nigdy nie commituj `.mcp.json`.
