# NotebookLM — prompty do Twojego notebooka z 14 źródłami naukowymi

Notebook zawiera 14 papierów / meta-analiz (2017–2026) z następujących obszarów: **running economy (RE)**, **durability RE**, **strength/resistance training dla biegaczy**, **trening polaryzowany (POL) i rozkład intensywności (TID)**, **dawka biegu**, oraz kilka prac o biegach uphill/downhill (mało relewantne dla płaskiej pętli asfaltowej — warto to zaznaczyć w prompcie, żeby model nie forsował tych źródeł).

---

## Kontekst zawodnika (wstawić na początek każdego prompta)

> Marcin, 49 lat (rocznik 1977), 168 cm, 64 kg, BMI 22,7. Staż biegowy ~10 lat. 13 ukończonych ultra (2016–2026), w tym 6× 100 km+ oraz **160 km w 22 h 44 m** (Rumia 2021). Świeży sub-3 maraton: **2:57 Gdańsk 19.04.2026** (PB karierowy, wcześniej 2:59 sprzed lat). Półmaraton 1:23, 3000 m 10:31. Objętość ostatnio ~60 km/tydz.
>
> Cel: **minimum 200 km w 24 h na PZLA MP w Pabianicach 30.05.2026**, płaska asfaltowa pętla 1725 m. Do startu **38 dni** licząc od 22.04.2026 (3 dni po maratonie PB). Pierwsze 7–10 dni musi być regeneracją pomaratońską.

---

## Prompt 1 (główny, one-shot) — do wklejenia do NotebookLM

```
Zawodnik: 49 lat, 168 cm / 64 kg, staż 10 lat, 13 ukończonych ultra (6× 100 km+, rekord 160 km w 22:44). Świeży PB maratonu 2:57 (3 dni temu). Cel: 200 km w 24 h na płaskiej asfaltowej pętli 1725 m. Do startu 38 dni. Pierwsze 7–10 dni = regeneracja po maratonie.

Na podstawie ZAŁĄCZONYCH ŹRÓDEŁ w tym notebooku przygotuj raport w 5 sekcjach. Odpowiadaj TYLKO na podstawie tych źródeł, z cytowaniami do konkretnych dokumentów. Tam, gdzie źródło nie odpowiada wprost — powiedz to zamiast ekstrapolować. Prace o uphill/downhill w większości nie dotyczą tego celu (płaska pętla); używaj ich tylko jeśli jakiś wynik generalizuje się na bieg płaski.

SEKCJE RAPORTU:

1. RUNNING ECONOMY + DURABILITY (priorytet)
Co źródła (Llanos-Lagos 2024×2, Zanini 2025, Rodriguez-Barbero 2025) mówią o:
- ile poprawy RE można realistycznie osiągnąć w 5–8 tygodniach u doświadczonego biegacza,
- jak RE degraduje się w trakcie wielogodzinnego wysiłku (durability) i które interwencje to ograniczają,
- jakie konkretne bodźce treningowe (pliometria, ciężary, sprinty, intervally) najsilniej podbijają RE i durability.

2. STRENGTH / RESISTANCE TRAINING
Van Hooren 2024, Karp 2024: jaki protokół siłowy stosować 5 tyg. przed celem 24 h? Konkretnie: rodzaj obciążeń, objętość, częstotliwość, kiedy przerwać przed startem. Co robić, a czego unikać w taperze siłowym u biegacza 49 lat.

3. TRENING — TID / POLARIZED / DAWKA
Rivera-Kofler 2025, Muniz-Pumares 2025, Frandsen 2025: jaki rozkład intensywności (POL vs pyramidal vs threshold) optymalnie działa dla biegacza ultra przed kluczowym startem? Jaka tygodniowa objętość jest "wystarczająca" (punkty malejącej stopy zwrotu)? Jak to pogodzić z regeneracją po maratonie w T-6.

4. SPECYFIKA 24 H NA PĘTLI
Czy którekolwiek z tych źródeł daje implikacje dla 24-godzinnego wysiłku stałotempowego (nie trail)? Jeśli tak — jakie. Jeśli nie — powiedz wprost, że te źródła nie pokrywają tego obszaru i wypisz listę pytań, na które trzeba odpowiedzieć z innych źródeł.

5. KONKRETNE WNIOSKI NA 5 TYGODNI
Sklej z sekcji 1–4 krótki plan (5–10 punktów) "co robić, czego unikać" w oknie 38 dni, zakotwiczony w cytatach.

Format: krótkie akapity lub bullety. Każda teza z cytatem do źródła w formacie (Autor Rok). Bez ogólników "trenerzy zalecają".
```

---

## Prompt 1b (wersja skrócona, gdyby główny był za długi)

```
Zawodnik ultra 49 lat, 64 kg, staż 10 lat, 6× 100 km+, rekord 160 km / 22:44 h. PB maratonu 2:57 (3 dni temu). Cel: 200 km w 24 h na płaskiej pętli asfaltowej za 38 dni.

Wyłącznie na podstawie załączonych źródeł odpowiedz w 4 sekcjach:

1. Running economy + durability (Llanos-Lagos, Zanini, Rodriguez-Barbero): ile poprawy w 5–8 tyg., które bodźce działają, jak ograniczyć spadek RE w długim wysiłku.
2. Strength training w taperze (Van Hooren, Karp): protokół 5 tyg. przed celem, kiedy przerwać.
3. Rozkład intensywności i dawka (Rivera-Kofler, Muniz-Pumares, Frandsen): POL vs pyramidal vs threshold, optymalna objętość tygodniowa.
4. Wnioski "co robić / czego unikać" w oknie 38 dni po świeżym PB maratonu.

Każda teza z cytatem (Autor Rok). Prace uphill/downhill pomiń, chyba że wynik uogólnia się na bieg płaski.
```

---

## Prompty dodatkowe (węższe, jeśli chcesz drążyć poszczególne tematy)

### Prompt 2 — durability RE
```
Na podstawie Zanini 2025 i Rodriguez-Barbero 2025 (oraz innych źródeł z notebooka): jak zmienia się ekonomia biegu w trakcie wielogodzinnego wysiłku u doświadczonego biegacza? Jakie konkretne interwencje treningowe (typy jednostek, objętość, tempo) najskuteczniej tę degradację ograniczają? Jakie markery/testy pozwalają ją monitorować? Odpowiedz w 5–8 punktach z cytatami.
```

### Prompt 3 — strength w taperze
```
Na podstawie Van Hooren 2024 i Karp 2024: jak dokładnie powinien wyglądać protokół treningu siłowego w ostatnich 5 tygodniach przed kluczowym długodystansowym startem (cel 24 h, zawodnik 49 lat, 64 kg)? Podaj konkretnie: ćwiczenia (typ), obciążenie (%1RM lub RPE), serie × powtórzenia, częstotliwość w tygodniu, kiedy zrobić ostatnią ciężką sesję, kiedy przerwać pliometrię. Jeśli źródła nie odpowiadają na część pytań — zaznacz to.
```

### Prompt 4 — TID po maratonie
```
Na podstawie Rivera-Kofler 2025, Muniz-Pumares 2025 i Frandsen 2025: jaki model rozkładu intensywności (polarized, pyramidal, threshold) jest optymalny dla doświadczonego biegacza ultra w 5-tygodniowym oknie między maratonem PB (sub-3) a głównym startem 24 h? Jak dokładnie rozłożyć Zone 1/2/3 (w % czasu tygodniowego) w tych 5 tygodniach? Kiedy włączać intensywność po maratonie i w jakich dawkach? Odpowiedz z cytatami.
```

### Prompt 5 — dawka u weterana
```
Na podstawie Frandsen 2025 (How Much Running): jaka jest optymalna tygodniowa objętość biegowa dla doświadczonego biegacza ultra (49 lat, 10 lat stażu), uwzględniając punkty malejącej stopy zwrotu i ryzyko kontuzji? Jak ten wynik zmienia się dla celu 200 km w 24 h vs celu maratonowego? Cytaty.
```

---

## Jak tego użyć

1. Otwórz swój NotebookLM z tymi 14 źródłami.
2. Wklej **Prompt 1**. Jeśli odpowiedź jest ucięta/ogólnikowa — użyj **Prompt 1b**.
3. Potem odpal **Prompt 2–5** osobno, żeby pogłębić konkretne tematy.
4. Zapisz odpowiedzi obok w `prompts/odpowiedzi/notebooklm-<temat>.md`.
5. Kiedy zbierzesz odpowiedzi z NotebookLM + Claude + ChatGPT + Perplexity → merge w `plan-24h.md`.

## Uwaga o cytowaniach

NotebookLM **z definicji** cytuje do konkretnych fragmentów źródeł (klikalne numery przy tezach). To gigantyczny plus tej sesji vs. ogólny LLM — masz natychmiastowy ślad od rekomendacji do zdania w papierze. W merge warto przepisywać ten ślad (np. "[Zanini 2025, sekcja 3.2]"), żeby finałowy plan był weryfikowalny.

## Czego NIE zrobi NotebookLM

NotebookLM odpowie TYLKO z załączonych źródeł. Nie będzie miał wiedzy o:
- dawkowaniu węglowodanów w ultra (to nie jest w tych źródłach),
- protokołach żywieniowych, ładowaniu węgli, suplementacji,
- specyfice 24 h na pętli, pacingu, strategii mentalnej,
- supporcie, sprzęcie, butach.

Te tematy zostawiamy dla głównego promptu `bieg-24h-przygotowanie.md` (Claude / ChatGPT / Perplexity).
