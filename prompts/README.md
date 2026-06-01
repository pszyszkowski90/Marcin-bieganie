# Prompts — szablony do planowania z LLM

Szablony promptów wielokrotnego użytku przy planowaniu kolejnych biegów.

| Plik | Użycie |
|---|---|
| [bieg-24h-przygotowanie.md](bieg-24h-przygotowanie.md) | Bazowy prompt do analizy przygotowania do biegu 24h |
| [notebooklm-prompt.md](notebooklm-prompt.md) | Prompt do NotebookLM — synteza literatury naukowej |
| [marcin-historia-wyscigow.md](../marcin/historia-startow-prompt.md) | Dane historyczne Marcina do wstrzyknięcia w prompt |

## Jak używać przy nowym biegu

1. Pobierz dane o biegu → uzupełnij `biegi/NOWY-BIEG/kontekst/`
2. Weź prompt z `bieg-24h-przygotowanie.md` (lub stwórz analogiczny dla innego formatu)
3. Wstrzyknij profil zawodnika z `marcin/README.md`
4. Wstrzyknij dane o historii startów z `marcin/Historia startów.md`
5. Uruchom przez Claude / Gemini / ChatGPT
6. Zachowaj wyniki w `biegi/NOWY-BIEG/llm-analizy/`
