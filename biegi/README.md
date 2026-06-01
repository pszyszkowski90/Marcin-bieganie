# Biegi — historia startów

Jeden katalog per bieg. Struktura każdego katalogu:

```
NAZWA-BIEGU-ROK/
├── README.md           wyniki, krótkie podsumowanie
├── plan/               dokumenty planistyczne (taktyka, żywienie, trening)
├── kontekst/           dane o biegu: trasa, regulamin, timeline
├── decyzje/            ADR — decision records (DEC-NNN)
├── wyniki/             dane po biegu: analiza, CSV, skrypty
└── support-raceday/    materiały na dzień wyścigu (do wydrukowania, dashboard)
```

---

## Historia startów

| Rok | Bieg | Format | Dystans | Miejsce | Uwagi |
|-----|------|--------|---------|---------|-------|
| 2026 | **PZLA MP 24h Pabianice** | 24h pętla 1725 m, asfalt | **212.7 km** | #8 open / **#5 M40** | Plan 200 km, wykonanie bliżej 220 km w 1. połowie |

> Wcześniejsze starty (przed tym repo): zob. [marcin/Historia startów.md](../marcin/Historia%20startów.md)

---

## Następny bieg

_(do uzupełnienia)_

---

## Jak dodać nowy bieg

```bash
mkdir biegi/NAZWA-BIEGU-ROK
# Skopiuj strukturę z poprzedniego biegu
cp -r biegi/PZLA-MP-24h-Pabianice-2026/decyzje biegi/NAZWA-BIEGU-ROK/
# Stwórz README.md dla nowego biegu
```

Następnie:
1. Wypełnij `kontekst/` — dane o trasie i regulaminie
2. Zaplanuj `plan/` referując do `wiedza/` i `marcin/`
3. Zapisz kluczowe decyzje w `decyzje/DEC-NNN`
