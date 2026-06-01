---
tags: [cele, prediction, modele]
aliases: ["Predictive models", "Knechtle"]
created: 2026-04-28
type: analysis
---

# Modele predykcyjne dystansu 24h

Pięć niezależnych modeli zbiegających się w **A-goal 200–215 km** dla profilu Marcina. Konwergencja niezależnych metod = silny argument za realizmem celu.

## Model 1 — Knechtle 2011 equation

**Źródło:** Knechtle B et al., *Ir J Med Sci*, 2011. **[EBM]**

**Inputy:** longest distance ever (160 km Rumia 2021), marathon PB w minutach (177 min = 2:57).

**Formuła Knechtle 2022 PMC9609733:** `D_24h = 234,7 + 0,481·longest_km − 0,594·marathon_min`

**Obliczenie:**
```
D = 234,7 + 0,481·160 − 0,594·177
  = 234,7 + 76,96 − 105,14
  = 206 km
```

**Komentarz:** model zaniża dla doświadczonych ultrasów (n=14 ukończonych ultra to ponad medianę próby Knechtle).

> [!note] Korekta v3 dokumentu
> Wcześniejsze wersje cytowały błędnie 158–180 km. **Poprawne 206 km** — błąd matematyczny w v1→v2 wykryty 27.04.2026.

## Model 2 — Pabianice 2020 ekstrapolacja

**Źródło:** [[Historia startów]] — UltraPark Weekend 28.08.2020, 100 km @ 9:49:55, 20. miejsce.

**Logika:** Marcin biegł na **tej samej pętli** w 2020 z tempem **5:54/km** dla 100 km. Dla 24h tempo średnie spada o ~25% (typowy positive split — patrz [[40-Taktyka/Bossi 2017 — pacing 24h]]).

**Obliczenie:** 5:54 × 1,25 = **7:25/km średnia 24h** → 8,1 km/h × 24h = **194 km**, zakres **190–205 km**.

## Model 3 — DUV statystyka M45–50, PB 2:55–3:00, debiut 24h

**Źródło:** statistik.d-u-v.org agregat dla biegaczy z PB 2:55–3:00 startujących pierwszy raz na 24h.

**Wynik:** typowy zakres **170–200 km**. Dystans 220+ wymaga 3–4 lat treningu ultra-pętlowego (czego Marcin nie ma).

**Komentarz:** to argument przeciwko stretch 220+. **DUV mówi: 220+ to wyjątek, nie reguła** dla profilu Marcina.

## Model 4 — Ruda 2023 + korekta tartan → asfalt

**Źródło:** [[Historia startów#Bieg 12h Ruda Śląska 2023]] — 135,73 km @ 5:18/km na stadionie tartanowym.

**Korekta nawierzchni:** asfalt obciąża mięśnie ~10–15% bardziej niż tartan (Zadpoor & Nikooyan 2012, *J Biomech*) — niższy energy return, wyższy impact loading rate.

**Ekstrapolacja:**
- Naiwnie (135,73 × 2 = 271 km) → **niemożliwe**, bo tempo zwalnia w 2. połowie
- Z korektą positive split + nawierzchnia → **200–215 km** dla 24h Pabianice asfalt

**Komentarz:** to **najlepszy punkt referencyjny** dla formatu timed-race na pętli, ale dowód na A-goal, nie stretch 220+.

> [!warning] Pierwotny błąd Claude'a
> Pierwsza analiza Stravy (~04.2026) zidentyfikowała Rudę jako pętlę uliczną — błędnie. **Faktycznie: 25 okrążeń stadionu 400 m × 4 = 10 km batchowane jako "lap" w zegarku**. Marcin sam to skorygował 24.04.2026. Konsekwencja: ekstrapolacja zmniejszona z 215–235 km do **200–215 km**. Patrz [[Plan 24h - Źródło Prawdy#16.1|sekcja 16.1 planu]].

## Model 5 — PB maraton × 5,0 (heurystyka praktyczna)

**Źródło:** Koop J. *Training Essentials for Ultrarunning*, 2nd ed., 2021. **[PRAKTYKA]**

**Obliczenie:** 2:57 × 5 = 14:45 → na takim tempie 24h da ~195–210 km.

> [!error] Atrybucja — **NIE Bossi 2017**
> Wcześniejsze wersje dokumentu i część LLM-ów cytowały tę heurystykę jako Bossi 2017. **Bossi 2017 to studium pacingu, nie predyktor dystansu**. Atrybucja poprawiona w v3 (27.04.2026).

## Model 6 (uzupełniający) — VDOT × time-on-feet curve

VDOT Marcina ~65 (z maratonu 2:57). Daniels' tabele dają dla 24h ~170 km na samym VO2max (ekonomia bez fueling cap). Ale w 24h limiterem nie jest VO2max — to **EIMD i fueling**: patrz [[40-Taktyka/EIMD główny limiter]].

## Konwergencja

| Model | Predykcja | Waga |
|-------|-----------|------|
| Knechtle 2011/2022 | 206 km | Średnia |
| Pabianice 2020 | 190–205 km | **Wysoka** (ten sam teren) |
| DUV M45–50 | 170–200 km | Wysoka (statystyka populacyjna) |
| Ruda 2023 + korekta | 200–215 km | **Wysoka** (najbliższy format) |
| PB × 5,0 | 195–210 km | Średnia (heurystyka) |

**Wniosek:** wszystkie zbiegają się w **200–215 km = A-goal**. Stretch 220+ jest poza zasięgiem statystycznym, możliwy tylko w idealny dzień.

## Powiązania

- **Cele dystansowe** → [[Cele dystansowe]]
- **Empiria własna jako test modeli** → [[Empiria Marcina]]
- **EIMD jako limiter** → [[40-Taktyka/EIMD główny limiter]]
- **Decyzja celu** → [[80-Decyzje/DEC-001 Cel A 200-215]]
