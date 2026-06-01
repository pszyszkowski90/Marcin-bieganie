# Support Dashboard — dokumentacja logiki i założeń

Zawodnik: **Marcin SZYSZKOWSKI #45**  
Wyścig: **24h Pabianice, 30.05.2026**  
Trasa: pętla 1725 m, asfalt, płaski

---

## Architektura

```
server.py  (Python, localhost:8765)
  │
  ├── GET /                  → support-dashboard.html
  ├── GET /api/results       → proxy do protimer.pl (bez CORS)
  ├── GET /api/log           → odczyt nutrition-log.json
  └── POST /api/log          → zapis nutrition-log.json
```

**Uruchomienie:** `python server.py`, otworzyć `http://localhost:8765`

Serwer czyta HTML z dysku przy każdym żądaniu — zmiana pliku wymaga tylko **odświeżenia przeglądarki**, nie restartu serwera.

---

## Dane live (protimer.pl)

- **URL:** `https://www.protimer.pl/bio/export/results_online/1434/16030`
- **Polling:** co 10 sekund
- **Kolejność proxy:** `/api/results` (serwer lokalny) → `corsproxy.io` → `allorigins.win`

### Parser HTML

Szuka wiersza `<tr>` zawierającego bib `"45"` lub nazwisko `"SZYSZKOWSKI"`. Wyciąga:

| Pole | Format | Źródło |
|------|--------|---------|
| `laps` | liczba całkowita | `lapArr.length` → z tekstu → z dystansu/1725 |
| `lapArr` | tablica sekund | komórki MM:SS (zakres 5–40 min) |
| `elapsed` | sekundy od startu | komórka HH:MM:SS |
| `dist` | km (decimal) | komórka `XX.XXXXX` |
| `rank` | liczba całkowita | jedna z pierwszych 3 komórek (1–200, ≠ 45) |

Gdy `lapArr` jest puste (brak MM:SS w HTML), `laps` jest szacowane z dystansu: `round(dist / 1.725)`.

---

## Predykcja następnego przejścia przez strefę

### Kluczowe założenie: S.startAt jest stały

`S.startAt` = godzina startu wyścigu w ms (ustawiana raz przez użytkownika w polu **Start → OK**).  
**Nigdy nie jest nadpisywana przez fetch** — to zapobiega dryfowi, który wcześniej powodował błąd ~3 min po 5 minutach.

### Formuła

```
lastCrossing = S.startAt + S.elapsed * 1000
nextTs       = lastCrossing + avgLap3 * 1000
```

- `S.elapsed` = `Czas sum.` z protimera = dokładna sekunda od startu kiedy Marcin minął **matę pomiarową**
- `avgLap3` = średnia z ostatnich 3 kółek (lub 590 s = ~9:50 jako domyślna)

### Ważne: mata ≠ strefa supportu

Mata pomiarowa i strefa supportu to **różne miejsca** na trasie. Timing aktualizuje się gdy Marcin mija matę, do strefy dociera ok. kilku minut później. Obserwuj empirycznie ile to zajmuje i uwzględnij w interpretacji countdown.

### Wykrycie nowego kółka

Gdy `d.laps > S.prevLapCount`: karta "Następne przejście" miga na zielono przez 4 sekundy. `S.elapsed` aktualizuje się do nowego `Czas sum.`, countdown zaczyna liczyć od pełnego kółka.

---

## Odżywianie — produkty i wartości odżywcze

Każde kliknięcie przycisku zapisuje wpis `{type, raceS, lap, ts}` do logu.

| Przycisk | Typ | ml | CHO (g) | Na (mg) | Uwagi |
|----------|-----|----|---------|---------|-------|
| 💧 Woda | `water` | 250 | 0 | 0 | |
| 🥤 Izo | `iso` | 250 | 10 | 150 | 250ml, izotonik |
| 🟠 Dzik | `dzik` | 0 | 40 | 200 | saszetka 66g |
| 🔵 SiS | `sis` | 0 | 40 | 12 | żel 60ml |
| 🧂 ALE cap | `ale` | 0 | 0 | ~300 | **szacunek** — sprawdź etykietę! |

`ALE_NA = 300` — stała w kodzie (linia `const ALE_NA = 300`), zmień gdy znasz dokładną wartość.

### Timerki alertów

| Alert | Typ | Interwał | Żółty gdy | Czerwony gdy |
|-------|-----|----------|-----------|--------------|
| 🧂 ALE / elektrolity | `ale` lub `salt` | 60 min | < 10 min | ≤ 0 |
| 🟠 Żel (Dzik/SiS) | `dzik`, `sis`, `gel` | 25 min | < 5 min | ≤ 0 |

Podpowiedź żelowa w karcie "Następne przejście":
- `gelRem ≤ untilNext + 60s` → **🟠 DAJ NA TEJ WIZYCIE (#N)**
- `gelRem ≤ untilNext + avgLap + 60s` → **🟠 NA NASTĘPNEJ WIZYCIE (#N+1)**
- reszta → ✅ nie teraz

---

## Bilans godzinowy

Tabela grupuje wpisy z logu **per godzina biegu** (H1, H2, …).  
Kolumny CHO i Na kolorowane według zakresów:

| Wskaźnik | Zielony | Żółty | Czerwony |
|----------|---------|-------|----------|
| Płyny (ml/h) | 400–700 | 312–400 | < 312 |
| CHO (g/h) | 80–110 | 62–80 | < 62 |
| Na (mg/h) | 500–750 | 390–500 | < 390 |

Pasek u góry logu pokazuje sumy od startu z bieżącym tempem (X ml/h, X g/h, X mg/h).  
⚠️ przy Na oznacza że w logu jest ALE — wartość Na jest szacunkowa.

---

## Historia — pierwsze 5 godzin

Stała `HISTORY` w kodzie (linie ~340–362) zawiera preładowany log z pierwszych ~5h wyścigu wpisany ręcznie przez supportera. Wczytywana automatycznie gdy log jest pusty.

Aby ją zaktualizować: edytuj tablicę `HISTORY` w pliku HTML i odśwież przeglądarkę.

---

## Prognoza końcowego dystansu

Model wykładniczego zaniku tempa:

```
pace(t) = p0 * exp(-k * t)
total   = p0/k * (1 - exp(-k * 24))
```

- `k = 0.025` (stała zaniku, skalibrowana dla dobrze wytrenowanego ultramaratończyka)
- `p0` obliczane z aktualnego tempa i czasu biegu
- Wyniki: 200 km (minimum), 220 km (super), 230 km (optymistyczny)

Prognoza jest orientacyjna — przy k=0.025 niedoszacowuje biegaczy, którzy utrzymują tempo; w pierwszych 3–4h wyścigu ma duży błąd.

---

## Persystencja danych

| Dane | localStorage | nutrition-log.json |
|------|--------------|--------------------|
| Log odżywiania (`nlog`) | ✅ | ✅ (auto-zapis przy każdym kliknięciu) |
| `saltLast`, `gelLast` | ✅ | ✅ |
| `startAt` | ✅ | ✅ |
| `prevLapCount` | ✅ | — |
| Auto-backup | co 5 min | — |

Przy starcie: serwer sprawdza `/api/log` i wczytuje wpisy jeśli ma ich więcej niż localStorage (np. po zmianie urządzenia).

Eksport ręczny: przycisk **💾 Eksport** → plik `support-marcin-YYYY-MM-DDTHH-MM.json`.

---

## Konfiguracja (pasek na dole)

| Pole | Opis | Kiedy ustawiać |
|------|------|----------------|
| **Start** | godzina startu wyścigu (HH:MM) | **raz na początku** — krytyczne dla predykcji! |
| **Kółka / h:mm:ss / km / miejsce** | ręczne dane gdy fetch nie działa | gdy serwer/CORS zawodzi |

---

## Pliki projektu

```
c:\Prywatne\Strava\
  support-dashboard.html   # cały frontend + logika JS
  server.py                # lokalny serwer HTTP (proxy + log)
  nutrition-log.json       # log odżywiania (tworzony przez server.py)
  SUPPORT-DOCS.md          # ten plik
```
