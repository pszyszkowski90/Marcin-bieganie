# Plan 24h Pabianice — Taktyka biegu i sprzęt

> Część dokumentacji "Plan 24h Pabianice 30.05.2026" (Marcin, M49, 64 kg). Ten dokument zbiera taktykę biegu (Bossi 2017 + empiria Marcina z Rudy 2023), pacing dla celów 200/220/230 km, EIMD jako główny limiter, protokół Run/Walk z walk-through-aid, podział doby na bloki 4×6h oraz pełny sprzęt: rotacja butów (Saucony Ride 18 + Hoka Clifton 10 Wide, oba 8 mm dropu), skarpety, ubiór warstwowy, czołówki.
>
> Master index: [Plan 24h - Źródło Prawdy.md](Plan%2024h%20-%20%C5%B9r%C3%B3d%C5%82o%20Prawdy.md).

---

## 4. Taktyka biegu — tempo i strategia

### Co mówi najważniejsze badanie (Bossi 2017) — ZWERYFIKOWANE w research

**Bossi AH, Matta GG, Millet GY, et al. „Pacing Strategy During 24-Hour Ultramarathon-Distance Running". Int J Sports Physiol Perform. 2017;12(5):590–596** — 501 zawodników z 5 edycji 24h Rio de Janeiro.

Kluczowy wynik, często mylnie interpretowany w LLM-outputach:

> **„The fastest runners start at LOWER relative intensities and display a more even pacing strategy than slower runners."**

Czyli: **najszybsi startują bliżej tempa średniego, NIE szybciej od słabszych**. [GT] twierdził coś odwrotnego — błąd interpretacji.

Grupy (średnie wyniki): G1 **180,5 km** / G2 **142,4 km** / G3 **122,1 km** / G4 **97,2 km**. Grupa G1 w 1. godzinie leciała ~141% tempa średniego (spadek do 70% w godz. 23 — ~30% spadek). **Im płaska krzywa, tym dalszy wynik** (odwrotna korelacja start pace vs total distance).

### Tempo startowe — rozstrzygnięcie sporu

> **Werdykt**: Bossi 2017 + Decoding Ultramarathon 2024 *Sports Med* — elita startuje 5–8% powyżej średniej tempa docelowego; amatorzy 15–25%. **NIE kopiować procentów Sorokina** (319 km, start 88% średniej) — Marcin nie ma jego VT2.
>
> **Rekomendacja zweryfikowana**:
>
> | Cel | Średnia tempa (brutto) | Optymalne tempo startowe (godz. 0–4) | % średniej prędkości (Vavg) |
> |---|---|---|---|
> | 200 km | 7:12/km (8,33 km/h) | **6:30–6:45/km** (8,89–9,23 km/h) | **107–111% Vavg** (start o 7–11% szybszy) |
> | 220 km | 6:33/km (9,16 km/h) | **6:00–6:15/km** (9,60–10,00 km/h) | **105–109% Vavg** (start o 5–9% szybszy) |
> | 230 km | 6:15/km (9,60 km/h) | **5:50–6:00/km** (10,00–10,29 km/h) | **104–107% Vavg** (start o 4–7% szybszy) |
>
> *Bossi 2017 mierzy "% średniej prędkości" (Vavg = total distance / 24h). G1 elity startowała ~141% Vavg, kończyła ~70% Vavg (~30% spadek). Marcin powinien startować bliżej elity (105–110%) niż amatorów (115–125%).*
>
> **Nie startować na 5:30/km chyba że celujesz 240+ km** (czego Marcin nie ma prawa zakładać bez bazy 24h).

> 🆕 **Empiryczny dowód z Ruda Śląska 2023 — Marcin ma udokumentowaną tendencję do zbyt szybkiego startu**: w biegu 12h poszedł pierwsze 50 km @ ~4:55/km (laps 1–5 ze Stravy) przy średniej całości 5:18/km — ~8% za szybko. Efekt: systematyczny crash od 80. km, tempo spadło do 6:00–6:12/km w 3. tercji, HR opadała 145→115 (central fatigue). Bossi 2017 to teoria — Ruda 2023 to dane Marcina. **Zegarek z alertem tempa (dolnym i górnym) jest obowiązkowy od 1. okrążenia.** Paweł powinien znać docelowe tempo i móc powiedzieć "za szybko" w pierwszej godzinie.
>
> ⚠️ **Uwaga o "konsensusie LLM"**: ta rekomendacja (start 6:30–6:45/km dla 200 km) jest **konserwatywniejsza niż propozycje 3 z 6 LLM-ów**, które sugerowały 5:50–6:00/km dla A-goal. Werdykt został podyktowany **empirią Marcina** (Ruda 2023 + DNF Kaliska 2022 — patrz sekcja 16.12), nie konsensusem teoretycznym. Bossi 2017 wspiera tę decyzję populacyjnie (im płaska krzywa, tym dalszy wynik), ale to dwa case'y własne są decydujące.

### Pacing — co jest pewne (consensus wszystkich 6)

- **Pozytywny split jest nieunikniony i optymalny** — Bossi 2017; Knechtle et al. 2019, *Front Physiol* **[OBSERWACJA]**. Nawet Sorokin zwalnia: według **DUV statistik** (oficjalne IAU) WR Verona/Lupatotissima 17–18.09.2022 = 319,614 km, splity: **100 km @ 6:49:12 (4:05/km), 12h @ 170,953 km (4:13/km średnio), drugie 12h = 148,661 km (4:51/km średnio)**. Spadek tempa średniego między półkami 12h ~15%, między 1. sotką a 2. połową ~19%. **Sam Sorokin w wywiadzie iRunFar („No Limits", 2022) przyznał: „my pacing tactics were bad, I began too fast"** — to mocniejszy argument za konserwatywnym startem niż Bossi. **[EBM/oficjalne]** — [DUV runner=439692](https://statistik.d-u-v.org/getresultperson.php?runner=439692). Nikt nie biega 24h równym tempem.
- **Negatywny split jest nierealistyczny** (wyjątek: Nick Coury 2021, jeden na pokolenie)
- **Cel**: jak najpłaska krzywa pozytywnego splitu. Spadek <20% od godz. 1 do godz. 24 = poziom elity amatorskiej
- **Walk-through-aid** ≠ pit-stop. Walk-through-aid to 15–30 s marszu co okrążenie przy strefie supportu (bidon, żel, łyk bulionu) — **ruch nie ustaje**. Szczegóły w protokole run/walk poniżej. Łącznie ~30–60 min marszu, ale to NIE są postoje.
- **Realne pit-stopy** (zatrzymanie się): planowo **4–8× w 24h**, łącznie ~20–40 min postojów — wliczone w tempo brutto. Scenariusz referencyjny:
  - 2× zmiana butów (godz. 8 i 16), ~3–5 min każda
  - 1–3× toaleta, ~2–3 min każda
  - 1–2× zmiana warstw/przebranie (wieczór, noc), ~3–5 min każda
  - 0–2× interwencja nieprzewidziana (GI, pęcherz, dłuższy odpoczynek), 5–10 min
  - W godz. 18–24h postoje mogą być nieco dłuższe (np. ciepły bulion na stojąco, przebranie), ale **wciąż rzadkie — nie co okrążenie**
  - **Empiria Marcina — Ruda Śląska 2023**: elapsed = moving time = 12:00:00, zero zarejestrowanych postojów w 12h (jedzenie/picie "w locie"). Dla 24h zakładamy realnie 4–8 postojów, bo zmiana butów/warstw jest nieunikniona.
- **Nie siadać** (wyraźnie [GB]: „krzesełko to pułapka"). Siadanie tylko na zmianę butów lub interwencję medyczną

### EIMD — kluczowy limiter w 24h (nowy koncept z research)

**Decoding Ultramarathon 2024, *Sports Medicine*** — muscle damage (EIMD) jest **głównym limiterem w długich ultra**, ważniejszym niż VO2max czy żywienie. Mechanizm:

- Każdy krok = ~2,5× masa ciała ekscentrycznie na jedną stopę
- Przy szybszym tempie: większa amplituda rozciągania, większa siła na lądowanie
- CK (kinaza kreatynowa) rośnie **nieliniowo** z intensywnością — po 8h biegu w 5:30/km Marcin miałby uszkodzenia równoważne 3 maratonom, mając przed sobą jeszcze 16h
- Ortenblad et al. 2013, *J Physiol* — lokalna deplecja glikogenu w **triadach** (sprzężenie wapniowe) następuje PRZED ogólną deplecją → „ściana" w ultra nie jest stopniowa, jest nagła. Szybki start wyczerpuje triad-glycogen szybciej.

**Konsekwencja praktyczna**: każda sekunda wygrana w pierwszych 6h kosztuje 3–5 sekund w godz. 18–24. Ryzyko EIMD → prewencyjne marsze (patrz niżej).

### Strategia Run/Walk — ROZSTRZYGNIĘTA

> **Brak RCT** dla run/walk vs ciągły bieg w 24h. Konsensus rozsądny: **walk-through-aid od 1. okrążenia** — to NIE Galloway 9/1. Praktyczna konieczność dla setupu z niedoświadczonym supportem (Paweł) + reset bioder i wzorca ruchu.
>
> **Protokół rekomendowany**:
> 1. **Od 1. okrążenia**: 15–30 s energicznego marszu przy strefie supportu przy każdym okrążeniu = ~5% czasu w marszu. Jesz/pijesz, podajesz bidon — ruch nie ustaje
> 2. **Po każdym solidnym posiłku** (bułka, pierogi): 2 min marszu → redukuje GI distress (mniej „jostling" żołądka)
> 3. **Co 2h: 1 pełne okrążenie marszem** (~15 min) → reset bioder, łydek, wzorca neuronalnego. **Kluczowe dla M49 — masters mają wyższe ryzyko tendinopatii Achillesa na monotonii pętli**
> 4. **Po godz. 16 biegu**: dodaj 30 s marszu na każdej połowie pętli (~co 5 min biegu)
>
> Sumarycznie: ~10% marszu w 1. połowie, ~20% w drugiej (łącznie ~15% — tłumaczy różnicę między tempem biegowym a brutto).
>
> **NIE Galloway 9/1 ze sztywnym timerem** — Marcin ma profil, w którym ciągły bieg w adekwatnie wolnym tempie jest ekonomiczniejszy (9 min @ 5:50 + 1 min marszu @ 7:00 = ~6:00/km, a on może ciągnąć 6:00 ciągle).

### Przykładowy plan pacingu dla celu 200 km (core) oraz 220 km (A-goal)

**Cel 200 km** — tempo biegowe ~6:35/km, brutto 7:12/km:

| Godzina biegu | Pora dnia | Tempo biegowe | Tempo brutto | Skumulowany dystans |
|---|---|---|---|---|
| 0–6h | 07–13:00 | 6:30/km | 6:45/km | ~53 km |
| 6–12h | 13–19:00 | 6:40/km | 7:00/km | ~105 km |
| 12–18h | 19–01:00 | 7:00/km | 7:30/km | ~153 km |
| 18–24h | 01–07:00 | 7:30/km | 8:00/km | **~198–205 km** |

**Cel 220 km** (A-goal stretch): tempo biegowe ~6:10/km, brutto 6:33/km. Każdy blok 6h o ~15 s/km szybciej niż dla 200 km (parametry w tabeli sekcji 0).

**Reguła dyscypliny**: w godz. 0–2 powinieneś czuć się „irytująco wolno". Wszyscy uciekają — pozwól im. Po 8h większość z nich będzie szła, a Marcin wciąż będzie biegł. **To jest cała tajemnica 24h**.

### Zarządzanie blokami czasowymi

**0–6h (07:00–13:00)**: Euforia startowa, ryzyko „pójścia za szybko". Tempo **6:30–6:45/km** (dla celu 200 km) lub **6:00–6:15/km** (dla celu 220 km). Jedzenie agresywne 90–100 g CHO/h. Walk through aid od 1. okrążenia.

**6–12h (13:00–19:00)**: Cieplejsza pora dnia, możliwy przegrzew, „palate fatigue" (zmęczenie słodkim smakiem). Przejście na realną żywność. Zmiana smaku: słone zamiast słodkiego. Zmiana butów godz. 8.

**12–18h (19:00–01:00)**: „Tu wygrywasz lub przegrywasz". Dominuje ciepłe jedzenie (rosół), zmiana warstw ubrania. **Brak kofeiny** do godz. 16 biegu (~23:00) — patrz sekcja 6.

**18–24h (01:00–07:00) — kryzys biologiczny 02:00–05:00**: Fizjologiczny nadir temperatury ciała i szczyt melatoniny. Besta et al., 2021, *Nutrients* **[EBM]**. Procedura:
1. **Dodatkowa warstwa ubrania** prewencyjnie (nawet jeśli nie zmarzł)
2. **Kofeina mikrodawki** 50 mg co 2–3h
3. **Ciepły bulion** — kubek co 2 okrążenia
4. **Marszobieg**, nie sam marsz — marsz wychłodzi i doprowadzi do DNF (wyraźne ostrzeżenie [GB])
5. **Wschód słońca ~04:35** — psychologiczny reset, blokuje melatoninę, można lekko przyspieszyć

---

## 8. Sprzęt i obuwie

### Buty — consensus wszystkich 4

**2–3 pary, rotacja co 8–10h, para nocna o 0,5–1 rozmiaru większa** (stopy puchną 3–8% w 24h). [GB]: „potężny obrzęk stóp po 12h" **[PRAKTYKA]**.

### 🆕 Rotacja butów Marcina (zaktualizowana 26.04)

**Profil:** drop habitualny 0–5 mm, brak doświadczenia z płytką karbonową, posiada Saucony Ride 18 (160 km przebiegu) + Hoka Clifton 10 Wide (nowe). Detal: sekcje 16.17–16.19.

**Krytyczne reguły:**
- **NIE forsować drop 10–12 mm** — z 0–5 mm habitualnie skok na 10–12 = 86% injury rate (Achilles tendinopathy). Ride 18 + Clifton 10 Wide (oba 8 mm) = bezpieczny konsystentny dobór
- **Rotacja butów OBOWIĄZKOWA** — pętla 1725 m × 24h w jednym kierunku (organizator nie zmienia) = asymetryczne kumulujące się obciążenie ITBS/Achilles. Sekcja 16.20

**Rotacja:**

| Para | Godziny | Model |
|---|---|---|
| #1 dzienne | 0–8h | **Saucony Ride 18** (8 mm, 35/27, 255 g, PWRRUN+) |
| #2 popołudnie/wieczór | 8–16h | **Hoka Clifton 10 Wide** (8 mm, **42/34** max cushion, ~280 g, CMEVA) |
| #3 noc | 16–24h | Powrót do Ride 18 lub Clifton (rotacja co 4–6h), Brooks Hyperion 2 awaryjnie |

**MUST-DO przed startem:** Hoka Clifton 10 Wide ≥30–50 km na treningu (1× medium 10–15 km + 1× long 20+ km). Żadnego biegu w nieprzetestowanych butach na 24h.

Rotacja redukuje mikrourazy — Malisoux 2015 **[EBM]**.

> **Carbon plate — ROZSTRZYGNIĘTE**: Marcin nie biegał w butach z płytką → **absolutnie NIE**. Ryzyko navicular stress fracture u nowicjuszy (PMC 10356879). Muñoz-López 2023 *Sports Med* **[EBM]**: projektowane na max 3h, niszczą łydki i rozcięgno w długim dystansie. **Saucony Ride 18 + max cushion #2/#3 bez płytki.**

### Skarpety (consensus wszystkich 4)

4–5 par, zmiana co ok. 6h lub wcześniej przy mokrości. **Injinji toe socks** (pięciopalczaste) lub **Drymax**. [CB] dodaje: Wrightsock double-layer — Knapik et al., 1996 — redukcja pęcherzy o 85% **[EBM, stare]**. **Nowe skarpety działają jak doping psychologiczny** ([GB]).

### Ubiór warstwowy (consensus)

Prognoza Pabianice koniec maja: dzień 15–22°C, noc 8–13°C, możliwy deszcz.

- Start (07:00): koszulka krótki rękaw + rękawki zapasowe + ultralekka wiatrówka w zapasie
- Dzień (11:00–18:00): koszulka + czapka z daszkiem + okulary + **krem SPF 50**
- Wieczór (18:00–22:00): koszulka + rękawki + buff
- Noc (22:00–05:00): koszulka długi rękaw + cienka kurtka softshell + czapka + **suche rękawiczki**
- Rano (05:00–07:00): zdejmowanie warstw w miarę ocieplania

### Anty-odparzenia (consensus)

**Sudocrem** (tlenek cynku, bariera hydrofobowa) lub **Body Glide** / Squirrel's Nut Butter.
Lokalizacje ([GB]): pachwiny, uda wewnętrzne, sutki, kark, lędźwie, pośladki, przestrzeń między pośladkami, palce u stóp.
Aplikacja przed startem + refresh co 6–8h.

### Czołówka i elektronika (consensus)

- **Główna**: Petzl Nao RL (750 lm, akumulator wymienny) lub Silva Trail Speed 5XT
- **Zapasowa**: Nitecore NU25 UL (400 lm, 80 g) — obowiązkowa
- **Baterie zapasowe**: 2 szt + powerbank 10 000+ mAh

### Kijki (consensus 4/4)

**NIE** na płaskiej pętli asfaltowej — marnują energię w barkach, rozbijają rytm. [GB]: „zostawić w domu". **[PRAKTYKA]**.

---

*Część dokumentacji "Plan 24h Pabianice 30.05.2026". Master index: [Plan 24h - Źródło Prawdy.md](Plan%2024h%20-%20%C5%B9r%C3%B3d%C5%82o%20Prawdy.md). Wersja: 1.0, 2026-04-30.*
