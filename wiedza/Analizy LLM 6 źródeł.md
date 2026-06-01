---
tags: [źródła, LLM, mapa, analizy, kody-źródeł]
aliases: ["LLM mapa", "6 źródeł", "Analizy LLM"]
created: 2026-04-28
type: meta
---

# Analizy LLM — mapa 6 źródeł

> Plan został zsyntetyzowany z **6 niezależnych analiz LLM** + research weryfikacyjny [R]. Każde źródło ma swój kod używany w cytowaniach (np. „[GB] dodaje" w planie).

## Tabela kodów

| Kod | Model | Format | Plik |
|-----|-------|--------|------|
| **[CB]** | Claude basic | Pierwsza analiza ogólna | `LLM Output/ogólne/Claude basic.txt` |
| **[CD]** | Claude details | Pogłębiona analiza ogólna | `LLM Output/ogólne/Claude details.md` |
| **[GB]** | Gemini basic | Pierwsza analiza ogólna | `LLM Output/ogólne/Gemini basic.txt` |
| **[GD]** | Gemini details | Pogłębiona analiza ogólna | `LLM Output/ogólne/Gemini details.md` |
| **[CT]** | Claude tempo | Analiza specjalistyczna — tempo | `LLM Output/tempo/Claude tempo details.md` |
| **[GT]** | Gemini tempo | Analiza specjalistyczna — tempo | `LLM Output/tempo/Gemini tempo details.md` |
| **[CŻ]** | Claude żywienie | Analiza specjalistyczna — żywienie | `LLM Output/żywienie/Claude żywienie details.md` |
| **[GŻ]** | Gemini żywienie | Analiza specjalistyczna — żywienie | `LLM Output/żywienie/Gemini żywienie details.md` |
| **[R]** | Research weryfikacyjny | Web search + literatura | Wpisany bezpośrednio w plan |

## Lokalizacja

Wszystkie surowe analizy LLM są w `LLM Output/` w katalogu projektu:
- [LLM Output/ogólne/](../../LLM%20Output/og%C3%B3lne/) — pierwsza warstwa
- [LLM Output/tempo/](../../LLM%20Output/tempo/) — druga warstwa, specjalistyczna
- [LLM Output/żywienie/](../../LLM%20Output/%C5%BCywienie/) — druga warstwa, specjalistyczna
- [LLM Output/komentarze/](../../LLM%20Output/komentarze/) — trzecia warstwa, refleksje
- [LLM Output/research-uzupełniający-2026-04-23.md](../../LLM%20Output/research-uzupe%C5%82niaj%C4%85cy-2026-04-23.md) — research [R]

## Promty

Promty użyte do generowania analiz są w `prompts/`:
- [prompts/bieg-24h-przygotowanie.md](../../prompts/bieg-24h-przygotowanie.md) — główny prompt z parametrami
- [prompts/marcin-historia-wyscigow.md](../../prompts/marcin-historia-wyscigow.md) — historia Marcina
- [prompts/pabianice-bieg-24h-fakty.md](../../prompts/pabianice-bieg-24h-fakty.md) — fakty o biegu
- [prompts/pabianice-regulamin-2026.txt](../../prompts/pabianice-regulamin-2026.txt) — regulamin
- [prompts/notebooklm-prompt.md](../../prompts/notebooklm-prompt.md) — prompt dla NotebookLM (14 papierów naukowych)

## Kluczowe rozbieżności (gdzie LLM nie były zgodne)

### Spór 1 — Tempo startowe
- **3/6 (CT, GD, GT):** 5:50–6:00/km dla A-goal 200 km
- **3/6 (CB, CD, GB):** ostrożniejsze
- **Werdykt:** [[../80-Decyzje/DEC-002 Tempo startowe konserwatywne|6:30–6:45/km]] (empiria Marcina decydująca)

### Spór 2 — Kreatyna
- **3/4 (Ja, ChatGPT, Claude B):** odstawienie obronione
- **1/4 (Gemini):** PRZECIW odstawieniu
- **Werdykt:** [[../80-Decyzje/DEC-004 Kreatyna 3 opcje|3 opcje, decyzja Marcina]]

### Spór 3 — Tempo long runa
- **Ja + ChatGPT:** easy + bloki w tempie 24h
- **Claude B:** easy + ostatnie 10–15 km szybsze niż 24h
- **Gemini:** tylko naturalne 5:00–5:30/km
- **Werdykt:** [[../80-Decyzje/DEC-008 Long run dwufazowy|Dwufazowy z race-fueling]]

### Spór 4 — Sód
- **GB, GT:** 300–600 mg/h
- **CB, CD, GD:** 500–800 mg/h
- **Werdykt:** [[../30-Żywienie/Nawodnienie i sód|500–700 mg/h baseline, 700–1000 mg/h ciepło/salty sweater]]

### Spór 5 — Kofeina dawka
- **Większość:** 600 mg/24h
- **Claude B:** 800–900 mg/24h (oparte o Kamimori 2005 SUSOPS)
- **Werdykt:** [[../80-Decyzje/DEC-003 Kofeina bez wash-out|600–650 mg/24h, bez wash-outu]]

### Spór 6 — Kawa pre-race
- **Większość:** 200 mg ~60 min przed
- **GB:** „mit do odrzucenia" — kawa rano wywinduje tętno
- **Werdykt:** kawa OK dla habitualnego consumera (Carvalho 2022 obala mit)

## Co LLM-y zgadzały się jednomyślnie

- **NLPZ — bezwzględny zakaz** (4/4)
- **Old protocol Astrand carbo-loading — odrzucony** (4/4)
- **Pić ad libitum, nie na siłę** (4/4)
- **G:F 1:0,8 dla CHO >60 g/h** (4/4)
- **Sleep banking T-1 ważniejszy niż piątkowy sen** (4/4)
- **Gut training jako priorytet #1** (6/6)

## Mocne strony per źródło

| Kod | Mocna strona |
|-----|--------------|
| **[CB] Claude basic** | Solidne fundamenty, syntetyczne |
| **[CD] Claude details** | Pogłębione mechanizmy, ekstrapolacje |
| **[GB] Gemini basic** | Praktyczne, ostre cytaty (np. „krzesełko to pułapka") |
| **[GD] Gemini details** | Liczby + cytowania, dyscyplina źródłowa |
| **[CT] Claude tempo** | Tabele tempa, kalkulacje |
| **[GT] Gemini tempo** | Procenty Vavg, ale **błąd interpretacji Bossi** |
| **[CŻ] Claude żywienie** | Costa 2017, mechanizmy SGLT1/GLUT5 |
| **[GŻ] Gemini żywienie** | Western States data, GI symptoms |
| **[R] Research** | Korekty błędów, weryfikacja Stravy |

## Słabe strony / błędy do uwagi

- **[GT]** błąd interpretacji Bossi 2017 — myślał, że szybsi startują szybciej (jest odwrotnie)
- **[GŻ]** błędna atrybucja Costa 2020 (powinno być Costa 2017 + Stuempfle 2015)
- **[CD] historycznie** błąd Knechtle predykcja 158–180 (poprawne 206)

## Powiązania

- **Notacja dowodów** → [[Notacja dowodów]]
- **Literatura cytowana** → [[Literatura kluczowa]]
- **Plan operacyjny (cytuje kody)** → [[../../Plan 24h - Źródło Prawdy.md|Plan 24h - Źródło Prawdy]]
