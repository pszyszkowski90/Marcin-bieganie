---
tags: [decyzje, ADR, decision-log, index]
aliases: ["Decision Log", "ADR index"]
created: 2026-04-28
type: index
---

# Decision Log — index decyzji projektowych

> **Konwencja ADR (Architecture Decision Record):** każda decyzja sporna, kontrowersyjna lub wymagająca uzasadnienia ma osobny plik. **Format:** Status / Kontekst / Opcje / Decyzja / Konsekwencje / Dowody.

## Po co Decision Log

W tym projekcie 6 niezależnych analiz LLM dało **wiele rozbieżnych rekomendacji**. Każdy ADR dokumentuje:
- **Co** zdecydowaliśmy
- **Dlaczego** (alternatywy odrzucone)
- **Na podstawie czego** (literatura, empiria, ryzyko)
- **Kiedy zmienić** (warunki rewizji)

To pozwala w przyszłości **wracać do decyzji** ze świadomym kontekstem zamiast zaczynać od zera.

## Lista decyzji (chronologicznie)

| ID | Tytuł | Data | Status |
|----|-------|------|--------|
| **DEC-001** | [[DEC-001 Cel A 200-215\|Cel dystansowy A: 200–215 km]] | 24.04.2026 | ✅ Przyjęta |
| **DEC-002** | [[DEC-002 Tempo startowe konserwatywne\|Tempo startowe konserwatywne (6:30–6:45/km dla 200 km)]] | 27.04.2026 | ✅ Przyjęta |
| **DEC-003** | [[DEC-003 Kofeina bez wash-out\|Kofeina bez wash-outu pre-race]] | 24.04.2026 | ✅ Przyjęta |
| **DEC-004** | [[DEC-004 Kreatyna 3 opcje\|Kreatyna — 3 opcje, decyzja Marcina]] | 24.04.2026 | 🟡 Otwarta (decyzja Marcina) |
| **DEC-005** | [[DEC-005 Brak płytki karbonowej\|Brak płytki karbonowej]] | 24.04.2026 | ✅ Przyjęta |
| **DEC-006** | [[DEC-006 Pętla bez zmiany kierunku\|Pętla bez zmiany kierunku → rotacja butów obowiązkowa]] | 26.04.2026 | ✅ Przyjęta |
| **DEC-007** | [[DEC-007 Plan low-mileage\|Plan treningowy low-mileage (75–85 km szczyt)]] | 26.04.2026 | ✅ Przyjęta |
| **DEC-008** | [[DEC-008 Long run dwufazowy\|Long run T-4 dwufazowy z race-fueling test]] | 23.04.2026 | ✅ Przyjęta |
| **DEC-009** | [[DEC-009 Run-Walk od 1 okrążenia\|Run-Walk: walk-through-aid od 1. okrążenia (NIE Galloway)]] | 23.04.2026 | ✅ Przyjęta |
| **DEC-010** | [[DEC-010 Probiotyki Sanprobi\|Probiotyki Sanprobi Barrier — wdrożyć]] | 23.04.2026 | ✅ Przyjęta |
| **DEC-011** | [[DEC-011 Sok z buraka opcjonalny\|Sok z buraka — opcjonalny, dawka terapeutyczna]] | 23.04.2026 | 🟡 Opcjonalna |

## Statusy

- ✅ **Przyjęta** — decyzja zamknięta, wpisana w plan operacyjny
- 🟡 **Otwarta** — wymaga inputu Marcina/zewnętrznego (np. test, lekarz, organizator)
- 🟡 **Opcjonalna** — ekonomia decyzji, można wybrać alternatywę bez zmiany planu głównego
- ❌ **Odrzucona** — analizowana, ale wybrano alternatywę
- 🔄 **Do rewizji** — warunki zmieniły się, zmienia się decyzja

## Kategorie tematyczne

### Pacing i taktyka biegu
- [[DEC-001 Cel A 200-215]]
- [[DEC-002 Tempo startowe konserwatywne]]
- [[DEC-009 Run-Walk od 1 okrążenia]]

### Żywienie i suplementacja
- [[DEC-003 Kofeina bez wash-out]]
- [[DEC-004 Kreatyna 3 opcje]]
- [[DEC-010 Probiotyki Sanprobi]]
- [[DEC-011 Sok z buraka opcjonalny]]

### Sprzęt
- [[DEC-005 Brak płytki karbonowej]]
- [[DEC-006 Pętla bez zmiany kierunku]]

### Trening
- [[DEC-007 Plan low-mileage]]
- [[DEC-008 Long run dwufazowy]]

## Kiedy dodać nowy ADR

**Dodaj nowy ADR gdy:**
- Decyzja ma ≥2 obronione alternatywy
- Decyzja zmienia coś istotnego w planie operacyjnym
- Konsensus źródeł jest podzielony (np. 3/4 LLM jedno, 1/4 drugie)
- Empiria własna (np. Stravy) zmieniła rekomendację z literatury

**NIE dodawaj ADR gdy:**
- Konsensus 100% (np. „NLPZ zakazane" — to nie jest sporna decyzja)
- Decyzja trywialna (np. „kupić banany do strefy")
- Refinement istniejącej decyzji bez zmiany meritum

## Format ADR

Każdy plik ma strukturę:

```markdown
---
tags: [decyzja, ...]
type: decision
status: ✅/🟡/❌
date: YYYY-MM-DD
---

# DEC-NNN — Tytuł

## Status
✅/🟡/❌ — opis statusu

## Kontekst
Co działo się przed decyzją? Jakie pytanie?

## Opcje rozważone
A, B, C — z plusami/minusami

## Decyzja
Co wybraliśmy.

## Uzasadnienie
Dlaczego — dowody, źródła, empiria.

## Konsekwencje
Co się zmienia w planie operacyjnym.

## Warunki rewizji
Kiedy ta decyzja powinna być przegłosowana.

## Powiązania
Linki do notatek tematycznych.
```

## Powiązania

- **Plan operacyjny** → [[../../Plan 24h - Źródło Prawdy.md|Plan 24h - Źródło Prawdy]]
- **Główny MOC** → [[../README]]
- **Notacja dowodów** → [[../90-Źródła/Notacja dowodów]]
