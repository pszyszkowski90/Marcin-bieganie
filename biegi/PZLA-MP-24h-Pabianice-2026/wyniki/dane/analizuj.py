#!/usr/bin/env python3
"""
Oblicz metryki pacing dla top 10 z danych CSV i wygeneruj raport.
Wymaga: dane/okrazenia_top10.csv (wygenerowanego przez pobierz_dane.py)

Użycie:
  python analizuj.py
"""

import csv
import os
import math
import re
from collections import defaultdict

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
DANE_DIR    = os.path.join(SCRIPT_DIR, 'dane')
ANALIZA_DIR = os.path.join(SCRIPT_DIR, 'analiza')

LAPS_FILE    = os.path.join(DANE_DIR, 'okrazenia_top10.csv')
RESULTS_FILE = os.path.join(DANE_DIR, 'top10_wyniki.csv')
METRICS_FILE = os.path.join(DANE_DIR, 'metryki_top10.csv')
ANALIZA_FILE = os.path.join(ANALIZA_DIR, 'top10_analiza.md')

LOOP_M = 1725  # m / okrążenie
RACE_HOURS = 24

# ── Benchmarki naukowe (literatura) ──────────────────────────────────────────
BENCHMARK = {
    'cv_elite_max':  23.0,   # % — granica elity
    'cv_rec_min':    35.0,   # % — początek rekreacyjnego
    'fade_elite_min': 0.80,  # współczynnik zaniku: elita ≥ 0.80
    'fade_rec_max':  0.70,   # współczynnik zaniku: rekreacyjny < 0.70
    'ssr_threshold': 3.5,    # km/h — SSR = Substantial Speed Reduction w ciągu 1h
    'dist_1st_12h':  60.0,   # % całości dystansu w pierwszych 12h — elita
}

# ── Ładowanie danych ──────────────────────────────────────────────────────────

def load_laps():
    """Zwraca {imie_nazwisko: [{'pozycja', 'nr', 'czas_okr_s', 'czas_kum_s',
                                'predkosc_kmh', 'tempo_min_km', 'godzina_biegu'}, ...]}"""
    if not os.path.exists(LAPS_FILE):
        print(f'[BŁĄD] Brak pliku: {LAPS_FILE}')
        print('Uruchom najpierw: python pobierz_dane.py')
        raise SystemExit(1)

    athletes = defaultdict(list)
    with open(LAPS_FILE, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            name = row['zawodnik']
            try:
                lap = {
                    'pozycja':       int(row['pozycja']),
                    'nr':            int(row['nr_okrazenia']),
                    'czas_okr_s':    int(row['czas_okr_s']),
                    'czas_kum_s':    int(row['czas_kum_s']),
                    'predkosc_kmh':  float(row['predkosc_kmh']),
                    'tempo_min_km':  float(row['tempo_min_km']),
                    'godzina_biegu': float(row['godzina_biegu']),
                }
                athletes[name].append(lap)
            except (ValueError, KeyError):
                continue
    return dict(athletes)


def load_results():
    """Zwraca {imie_nazwisko: {'pozycja', 'dystans_km', 'czas_sumy', ...}}"""
    results = {}
    if not os.path.exists(RESULTS_FILE):
        return results
    with open(RESULTS_FILE, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            results[row['imie_nazwisko']] = row
    return results

# ── Statystyki ────────────────────────────────────────────────────────────────

def mean(vals):
    return sum(vals) / len(vals) if vals else 0.0

def stdev(vals):
    if len(vals) < 2:
        return 0.0
    m = mean(vals)
    return math.sqrt(sum((x - m) ** 2 for x in vals) / (len(vals) - 1))

def laps_in_window(laps, h_start, h_end):
    """Okrążenia których czas kumulatywny mieści się w [h_start, h_end) godzin."""
    return [l for l in laps if h_start <= l['godzina_biegu'] < h_end]

def dist_km_in_window(laps, h_start, h_end):
    return len(laps_in_window(laps, h_start, h_end)) * LOOP_M / 1000

def avg_speed_in_window(laps, h_start, h_end):
    window = laps_in_window(laps, h_start, h_end)
    speeds = [l['predkosc_kmh'] for l in window if l['predkosc_kmh'] > 0]
    return mean(speeds)

# ── Metryki ───────────────────────────────────────────────────────────────────

def compute_metrics(name, laps, result_row):
    """Oblicza wszystkie metryki pacing dla jednego zawodnika."""
    if not laps:
        return None

    laps_sorted = sorted(laps, key=lambda x: x['nr'])
    speeds = [l['predkosc_kmh'] for l in laps_sorted if l['predkosc_kmh'] > 0]
    if not speeds:
        return None

    total_laps = len(laps_sorted)
    total_dist_km = total_laps * LOOP_M / 1000
    pozycja = laps_sorted[0]['pozycja']

    # Prędkości w kwartałach
    s_0_6h   = avg_speed_in_window(laps_sorted, 0, 6)
    s_6_12h  = avg_speed_in_window(laps_sorted, 6, 12)
    s_12_18h = avg_speed_in_window(laps_sorted, 12, 18)
    s_18_24h = avg_speed_in_window(laps_sorted, 18, 24)

    d_0_6h   = dist_km_in_window(laps_sorted, 0, 6)
    d_6_12h  = dist_km_in_window(laps_sorted, 6, 12)
    d_12_18h = dist_km_in_window(laps_sorted, 12, 18)
    d_18_24h = dist_km_in_window(laps_sorted, 18, 24)

    # Pierwsza połowa vs druga połowa
    dist_1st_half = dist_km_in_window(laps_sorted, 0, 12)
    pct_1st_half  = (dist_1st_half / total_dist_km * 100) if total_dist_km > 0 else 0

    # Wskaźnik zaniku = prędkość 18–24h / prędkość 0–6h
    fade_ratio = (s_18_24h / s_0_6h) if s_0_6h > 0 else 0

    # CV tempa (per okrążenie) = odch.std / średnia * 100%
    cv_tempa = (stdev(speeds) / mean(speeds) * 100) if mean(speeds) > 0 else 0

    # Tempo startu (pierwsze 10 okrążeń)
    start_laps = laps_sorted[:10]
    start_speed = mean([l['predkosc_kmh'] for l in start_laps if l['predkosc_kmh'] > 0])

    # Najszybsze / najwolniejsze okrążenie
    best_speed  = max(speeds)
    worst_speed = min(speeds)

    # SSR — Substantial Speed Reductions: liczba godzin z nagłym spadkiem > 3.5 km/h
    hourly_speeds = []
    for h in range(RACE_HOURS):
        ws = avg_speed_in_window(laps_sorted, h, h + 1)
        if ws > 0:
            hourly_speeds.append(ws)
    ssr_count = 0
    for i in range(1, len(hourly_speeds)):
        drop = hourly_speeds[i - 1] - hourly_speeds[i]
        if drop > BENCHMARK['ssr_threshold']:
            ssr_count += 1

    # Klasyfikacja względem benchmarków
    if cv_tempa <= BENCHMARK['cv_elite_max']:
        cv_klasa = 'elita'
    elif cv_tempa <= BENCHMARK['cv_rec_min']:
        cv_klasa = 'sub-elita'
    else:
        cv_klasa = 'rekreacyjny'

    if fade_ratio >= BENCHMARK['fade_elite_min']:
        fade_klasa = 'elita'
    elif fade_ratio >= BENCHMARK['fade_rec_max']:
        fade_klasa = 'sub-elita'
    else:
        fade_klasa = 'zbyt duży zanik'

    return {
        'zawodnik':        name,
        'pozycja':         pozycja,
        'dystans_km':      round(total_dist_km, 2),
        'okrazenia':       total_laps,
        'srednia_predkosc': round(mean(speeds), 2),
        'tempo_start_kmh': round(start_speed, 2),
        'predkosc_0_6h':   round(s_0_6h, 2),
        'predkosc_6_12h':  round(s_6_12h, 2),
        'predkosc_12_18h': round(s_12_18h, 2),
        'predkosc_18_24h': round(s_18_24h, 2),
        'dystans_0_6h':    round(d_0_6h, 1),
        'dystans_6_12h':   round(d_6_12h, 1),
        'dystans_12_18h':  round(d_12_18h, 1),
        'dystans_18_24h':  round(d_18_24h, 1),
        'pct_dystans_1pol': round(pct_1st_half, 1),
        'wskaznik_zaniku':  round(fade_ratio, 3),
        'cv_tempa_proc':    round(cv_tempa, 1),
        'ssr_zdarzenia':    ssr_count,
        'najszybsze_kmh':   round(best_speed, 2),
        'najwolniejsze_kmh': round(worst_speed, 2),
        'cv_klasa':         cv_klasa,
        'fade_klasa':       fade_klasa,
    }


# ── Zapis metryk CSV ──────────────────────────────────────────────────────────

METRICS_FIELDS = [
    'zawodnik', 'pozycja', 'dystans_km', 'okrazenia', 'srednia_predkosc',
    'tempo_start_kmh',
    'predkosc_0_6h', 'predkosc_6_12h', 'predkosc_12_18h', 'predkosc_18_24h',
    'dystans_0_6h', 'dystans_6_12h', 'dystans_12_18h', 'dystans_18_24h',
    'pct_dystans_1pol',
    'wskaznik_zaniku', 'cv_tempa_proc', 'ssr_zdarzenia',
    'najszybsze_kmh', 'najwolniejsze_kmh',
    'cv_klasa', 'fade_klasa',
]


def save_metrics_csv(metrics_list):
    with open(METRICS_FILE, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=METRICS_FIELDS)
        w.writeheader()
        w.writerows(metrics_list)
    print(f'  Zapisano {METRICS_FILE}')


# ── Generowanie raportu MD ────────────────────────────────────────────────────

def fmt_speed(v):
    return f'{v:.2f}' if v else '–'

def fmt_pct(v):
    return f'{v:.1f}%' if v else '–'

def classification_emoji(klasa):
    return {'elita': '★', 'sub-elita': '◑', 'rekreacyjny': '○', 'zbyt duży zanik': '↓'}.get(klasa, '')

def speed_to_tempo(kmh):
    """km/h → min:ss / km"""
    if not kmh or kmh <= 0:
        return '–'
    s = 3600 / kmh
    m = int(s // 60)
    ss = int(s % 60)
    return f'{m}:{ss:02d}'

def tempo_diff_str(actual_kmh, plan_kmh):
    """Zwraca opis różnicy tempa: '5:58 /km (+1:46/km szybciej niż plan)'"""
    actual_s = 3600 / actual_kmh if actual_kmh > 0 else 0
    plan_s   = 3600 / plan_kmh   if plan_kmh   > 0 else 0
    diff_s   = plan_s - actual_s  # >0 = actual szybszy (niższe tempo)
    diff_abs = int(abs(diff_s))
    diff_m, diff_ss = diff_abs // 60, diff_abs % 60
    diff_str = f'{diff_m}:{diff_ss:02d}'
    tempo_str = speed_to_tempo(actual_kmh)
    if abs(diff_s) < 10:
        return f'{tempo_str} /km (~zgodnie z planem)'
    elif diff_s > 0:
        return f'{tempo_str} /km (**{diff_str}/km szybciej** niż plan)'
    else:
        return f'{tempo_str} /km ({diff_str}/km wolniej niż plan)'


def generate_report(metrics_list, laps_by_athlete, results):
    marcin_m = next((m for m in metrics_list if 'SZYSZKOWSKI' in m['zawodnik']), None)

    lines = []
    lines.append('# Analiza tempa TOP 10 — PZLA MP 24h Pabianice, 30.05.2026')
    lines.append('')
    lines.append('> Dane: ProTimer (protimer.pl) | Loop: 1725 m (asfalt, płaski)')
    lines.append('> Analiza: CV tempa, wskaźnik zaniku, tempo kwartalne, SSR')
    lines.append('')

    # ── Wyniki ogólne ─────────────────────────────────────────────────────────
    lines.append('## 1. Wyniki ogólne — TOP 10')
    lines.append('')
    lines.append('| # | Zawodnik | Kat | Dystans | Okrążenia | Śr. tempo |')
    lines.append('|---|----------|-----|---------|-----------|-----------|')
    for m in metrics_list:
        res = results.get(m['zawodnik'], {})
        kat = res.get('kategoria', '')
        row = (f"| {m['pozycja']} | **{m['zawodnik']}** | {kat} "
               f"| {m['dystans_km']:.1f} km | {m['okrazenia']} "
               f"| {speed_to_tempo(m['srednia_predkosc'])} /km |")
        lines.append(row)
    lines.append('')

    # ── Metryki pacing ────────────────────────────────────────────────────────
    lines.append('## 2. Metryki pacing')
    lines.append('')
    lines.append('**Legenda klasyfikacji:** ★ elita (wg literatury naukowej) · ◑ sub-elita · ○ rekreacyjny · ↓ zbyt duży zanik tempa')
    lines.append('')
    lines.append('> **CV tempa** (współczynnik zmienności per okrążenie): elita <23%, rekreacyjny >35%  ')
    lines.append('> **Wskaźnik zaniku** (tempo 0–6h / tempo 18–24h): elita 0.80–0.95, rekreacyjny <0.70')
    lines.append('')
    lines.append('| # | Zawodnik | CV tempa | Klasa CV | Wsk. zaniku | Klasa zaniku | SSR zd. |')
    lines.append('|---|----------|----------|----------|-------------|--------------|---------|')
    for m in metrics_list:
        row = (f"| {m['pozycja']} | {m['zawodnik']} "
               f"| {fmt_pct(m['cv_tempa_proc'])} {classification_emoji(m['cv_klasa'])} "
               f"| {m['cv_klasa']} "
               f"| {m['wskaznik_zaniku']:.3f} {classification_emoji(m['fade_klasa'])} "
               f"| {m['fade_klasa']} "
               f"| {m['ssr_zdarzenia']} |")
        lines.append(row)
    lines.append('')

    # ── Tempo kwartalne ───────────────────────────────────────────────────────
    lines.append('## 3. Tempo kwartalne (min:ss /km)')
    lines.append('')
    lines.append('Szybsze tempo = mniejsza liczba (np. 5:26 /km jest szybsze niż 6:36 /km).')
    lines.append('')
    header = '| # | Zawodnik | 0–6h | 6–12h | 12–18h | 18–24h | Zanik |'
    sep    = '|---|----------|------|-------|--------|--------|-------|'
    lines.append(header)
    lines.append(sep)

    for m in metrics_list:
        prefix = '**' if 'SZYSZKOWSKI' in m['zawodnik'] else ''
        suffix = '**' if prefix else ''
        row = (f"| {m['pozycja']} | {prefix}{m['zawodnik']}{suffix} "
               f"| {speed_to_tempo(m['predkosc_0_6h'])} "
               f"| {speed_to_tempo(m['predkosc_6_12h'])} "
               f"| {speed_to_tempo(m['predkosc_12_18h'])} "
               f"| {speed_to_tempo(m['predkosc_18_24h'])} "
               f"| {m['wskaznik_zaniku']:.2f} |")
        lines.append(row)

    # Wiersz ze średnią TOP10 (jako tempo)
    s06   = mean([m['predkosc_0_6h']   for m in metrics_list if m['predkosc_0_6h']])
    s612  = mean([m['predkosc_6_12h']  for m in metrics_list if m['predkosc_6_12h']])
    s1218 = mean([m['predkosc_12_18h'] for m in metrics_list if m['predkosc_12_18h']])
    s1824 = mean([m['predkosc_18_24h'] for m in metrics_list if m['predkosc_18_24h']])
    fade_avg = mean([m['wskaznik_zaniku'] for m in metrics_list if m['wskaznik_zaniku']])
    lines.append(f'| – | *Średnia TOP10* | *{speed_to_tempo(s06)}* | *{speed_to_tempo(s612)}* | '
                 f'*{speed_to_tempo(s1218)}* | *{speed_to_tempo(s1824)}* | *{fade_avg:.2f}* |')
    lines.append('')

    # ── Dystans w kwartałach ──────────────────────────────────────────────────
    lines.append('## 4. Dystans w kwartałach (km)')
    lines.append('')
    lines.append('| # | Zawodnik | 0–6h | 6–12h | 12–18h | 18–24h | 1. połowa % |')
    lines.append('|---|----------|------|-------|--------|--------|-------------|')
    for m in metrics_list:
        prefix = '**' if 'SZYSZKOWSKI' in m['zawodnik'] else ''
        suffix = '**' if prefix else ''
        row = (f"| {m['pozycja']} | {prefix}{m['zawodnik']}{suffix} "
               f"| {m['dystans_0_6h']:.1f} "
               f"| {m['dystans_6_12h']:.1f} "
               f"| {m['dystans_12_18h']:.1f} "
               f"| {m['dystans_18_24h']:.1f} "
               f"| {m['pct_dystans_1pol']:.1f}% |")
        lines.append(row)
    lines.append('')

    # ── Analiza Marcina ───────────────────────────────────────────────────────
    lines.append('## 5. Marcin Szyszkowski (#8) — analiza szczegółowa')
    lines.append('')
    if marcin_m:
        lines.append(f'- **Dystans**: {marcin_m["dystans_km"]:.1f} km ({marcin_m["okrazenia"]} okrążeń)')
        lines.append(f'- **Średnie tempo**: {speed_to_tempo(marcin_m["srednia_predkosc"])} /km')
        lines.append(f'- **Tempo startu** (pierwsze 10 okrążeń): '
                     f'{speed_to_tempo(marcin_m["tempo_start_kmh"])} /km')
        lines.append(f'- **CV tempa**: {marcin_m["cv_tempa_proc"]:.1f}% → **{marcin_m["cv_klasa"]}** '
                     f'(benchmark: elita <23%, rekreacyjny >35%)')
        lines.append(f'- **Wskaźnik zaniku**: {marcin_m["wskaznik_zaniku"]:.3f} → **{marcin_m["fade_klasa"]}** '
                     f'(benchmark: elita ≥0.80)')
        lines.append(f'- **SSR zdarzenia** (nagłe spowolnienia >3.5 km/h w ciągu 1h): {marcin_m["ssr_zdarzenia"]}')
        lines.append('')
        lines.append('### Plan vs rzeczywistość')
        lines.append('> Plan (z dokumentu Taktyka): tempo **brutto** (obejmuje walk-through-aid).')
        lines.append('> Plan 220 km: każdy kwartał ~15 s/km szybciej niż plan 200 km.')
        lines.append('')

        # Plany brutto z dokumentu "Plan 24h - Taktyka i sprzęt.md"
        # Cel 200 km brutto: 6:45 / 7:00 / 7:30 / 8:00  (min:ss /km → km/h)
        # Cel 220 km brutto: 6:30 / 6:45 / 7:15 / 7:45
        def pace_to_kmh(mins, secs):
            return 3600 / (mins * 60 + secs)

        plan200 = [pace_to_kmh(6,45), pace_to_kmh(7, 0), pace_to_kmh(7,30), pace_to_kmh(8, 0)]
        plan220 = [pace_to_kmh(6,30), pace_to_kmh(6,45), pace_to_kmh(7,15), pace_to_kmh(7,45)]
        actual  = [marcin_m['predkosc_0_6h'], marcin_m['predkosc_6_12h'],
                   marcin_m['predkosc_12_18h'], marcin_m['predkosc_18_24h']]
        periods = ['0–6h', '6–12h', '12–18h', '18–24h']

        lines.append('| Blok | Plan 200 km | Plan 220 km | Rzeczywistość | vs 200 km | vs 220 km |')
        lines.append('|------|------------|-------------|---------------|-----------|-----------|')

        for i, period in enumerate(periods):
            p200 = speed_to_tempo(plan200[i])
            p220 = speed_to_tempo(plan220[i])
            act  = speed_to_tempo(actual[i])

            # Różnica vs plan200 (w sekundach na km); ujemna = szybszy
            diff200_s = 3600 / actual[i] - 3600 / plan200[i]   # >0 = wolniejszy niż plan
            diff220_s = 3600 / actual[i] - 3600 / plan220[i]

            def fmt_diff(ds):
                abs_s = abs(int(ds))
                m2, s2 = abs_s // 60, abs_s % 60
                if abs(ds) < 8:
                    return '≈ plan'
                elif ds < 0:
                    return f'**{m2}:{s2:02d}/km szybciej**'
                else:
                    return f'{m2}:{s2:02d}/km wolniej'

            lines.append(f'| {period} | {p200} | {p220} | **{act}** | {fmt_diff(diff200_s)} | {fmt_diff(diff220_s)} |')

        lines.append('')
        lines.append('> Marcin biegł pierwsze dwa kwartały bliżej tempa 220 km, '
                     'w nocy (12–18h) i nad ranem (18–24h) wrócił do tempa 200 km.')
        lines.append('')
    else:
        lines.append('_Brak danych dla Marcina Szyszkowskiego._')
        lines.append('')

    # ── Porównanie Marcin vs TOP10 ─────────────────────────────────────────────
    lines.append('## 6. Marcin vs reszta TOP 10 — porównanie kwartalne')
    lines.append('')
    lines.append('Tempo w kwartałach (min:ss /km) — **Marcin** pogrubiony, ostatnia kolumna = mediana TOP9:')
    lines.append('')

    quarters = [
        ('0–6h',   'predkosc_0_6h'),
        ('6–12h',  'predkosc_6_12h'),
        ('12–18h', 'predkosc_12_18h'),
        ('18–24h', 'predkosc_18_24h'),
    ]

    col_names = [m['zawodnik'].split()[-1] for m in metrics_list]
    header_cols = ' | '.join(f'{n[:10]:10s}' for n in col_names)
    lines.append(f'| Okres      | {header_cols} | Med. TOP9 |')
    sep_cols = ' | '.join('-----------' for _ in col_names)
    lines.append(f'|------------|{sep_cols}|-----------|')

    for period_name, field in quarters:
        others = [m[field] for m in metrics_list if 'SZYSZKOWSKI' not in m['zawodnik'] and m[field] > 0]
        med_speed = sorted(others)[len(others) // 2] if others else 0

        row_vals = []
        for m in metrics_list:
            t = speed_to_tempo(m[field])
            if 'SZYSZKOWSKI' in m['zawodnik']:
                row_vals.append(f'**{t}**    ')
            else:
                row_vals.append(f'{t}       ')
        row_cols = ' | '.join(row_vals)
        lines.append(f'| {period_name:10s} | {row_cols} | {speed_to_tempo(med_speed)}       |')

    # Wiersz zaniku
    fade_vals = []
    for m in metrics_list:
        if 'SZYSZKOWSKI' in m['zawodnik']:
            fade_vals.append(f'**{m["wskaznik_zaniku"]:.2f}**  ')
        else:
            fade_vals.append(f'{m["wskaznik_zaniku"]:.2f}     ')
    others_fade = [m['wskaznik_zaniku'] for m in metrics_list
                   if 'SZYSZKOWSKI' not in m['zawodnik'] and m['wskaznik_zaniku'] > 0]
    med_fade = sorted(others_fade)[len(others_fade) // 2] if others_fade else 0
    lines.append(f'| {"Zanik":10s} | {" | ".join(fade_vals)} | {med_fade:.2f}       |')
    lines.append('')

    # Wnioski dla Marcina vs reszta
    lines.append('### Wnioski porównawcze')
    lines.append('')
    if marcin_m:
        others_06 = [m['predkosc_0_6h'] for m in metrics_list
                     if 'SZYSZKOWSKI' not in m['zawodnik'] and m['predkosc_0_6h'] > 0]
        med_06 = sorted(others_06)[len(others_06) // 2] if others_06 else 0
        # Dla tempa: mniejsze km/h = wolniejsze (wyższe tempo min:ss)
        diff_06 = marcin_m['predkosc_0_6h'] - med_06  # <0 = Marcin wolniejszy

        m_t = speed_to_tempo(marcin_m['predkosc_0_6h'])
        med_t = speed_to_tempo(med_06)
        diff_s = abs(3600 / marcin_m['predkosc_0_6h'] - 3600 / med_06) if med_06 > 0 else 0
        diff_m2, diff_ss2 = int(diff_s) // 60, int(diff_s) % 60

        if diff_06 > 0.3:
            lines.append(f'- **Start (0–6h)**: Marcin biegł **szybciej** od mediany '
                         f'({m_t} vs {med_t} /km, różnica {diff_m2}:{diff_ss2:02d}/km)')
        elif diff_06 < -0.3:
            lines.append(f'- **Start (0–6h)**: Marcin biegł **wolniej** od mediany '
                         f'({m_t} vs {med_t} /km, różnica {diff_m2}:{diff_ss2:02d}/km)')
        else:
            lines.append(f'- **Start (0–6h)**: Marcin biegł podobnie do mediany ({m_t} vs {med_t} /km)')

        others_cv = sorted(m['cv_tempa_proc'] for m in metrics_list
                           if 'SZYSZKOWSKI' not in m['zawodnik'] and m['cv_tempa_proc'] > 0)
        marcin_rank_cv = sum(1 for v in others_cv if v < marcin_m['cv_tempa_proc']) + 1
        lines.append(f'- **Równomierność tempa (CV)**: {marcin_m["cv_tempa_proc"]:.1f}% — '
                     f'{"bardziej równomierne" if marcin_rank_cv <= 5 else "mniej równomierne"} niż '
                     f'{len(others_cv) - marcin_rank_cv + 1} z 9 pozostałych zawodników')

        others_fade2 = [m['wskaznik_zaniku'] for m in metrics_list
                        if 'SZYSZKOWSKI' not in m['zawodnik'] and m['wskaznik_zaniku'] > 0]
        med_fade2 = sorted(others_fade2)[len(others_fade2) // 2] if others_fade2 else 0

        m_last  = speed_to_tempo(marcin_m['predkosc_18_24h'])
        m_first = speed_to_tempo(marcin_m['predkosc_0_6h'])
        if marcin_m['wskaznik_zaniku'] >= med_fade2:
            lines.append(f'- **Utrzymanie tempa**: Marcin spowolnił mniej niż mediana grupy '
                         f'(wskaźnik zaniku {marcin_m["wskaznik_zaniku"]:.3f} vs {med_fade2:.3f}); '
                         f'tempo {m_first} /km na starcie → {m_last} /km na finiszu')
        else:
            lines.append(f'- **Utrzymanie tempa**: Marcin spowolnił bardziej niż mediana grupy '
                         f'(wskaźnik zaniku {marcin_m["wskaznik_zaniku"]:.3f} vs {med_fade2:.3f}); '
                         f'tempo {m_first} /km na starcie → {m_last} /km na finiszu')
    lines.append('')

    # ── Ranking równomierności ────────────────────────────────────────────────
    lines.append('## 7. Ranking równomierności pacing')
    lines.append('')
    lines.append('> Mniejszy CV = bardziej równomierne tempo = strategia bliższa elitarnej')
    lines.append('')
    sorted_by_cv = sorted(metrics_list, key=lambda m: m['cv_tempa_proc'])
    lines.append('| Rank | Zawodnik | CV tempa | Śr. tempo | Wsk. zaniku | Klasa |')
    lines.append('|------|----------|----------|-----------|-------------|-------|')
    for i, m in enumerate(sorted_by_cv, 1):
        prefix = '**' if 'SZYSZKOWSKI' in m['zawodnik'] else ''
        suffix = '**' if prefix else ''
        row = (f'| {i} | {prefix}{m["zawodnik"]}{suffix} '
               f'| {m["cv_tempa_proc"]:.1f}% '
               f'| {speed_to_tempo(m["srednia_predkosc"])} /km '
               f'| {m["wskaznik_zaniku"]:.3f} '
               f'| {classification_emoji(m["cv_klasa"])} {m["cv_klasa"]} |')
        lines.append(row)
    lines.append('')

    # ── Metodologia ───────────────────────────────────────────────────────────
    lines.append('---')
    lines.append('')
    lines.append('## Metodologia')
    lines.append('')
    lines.append('- **CV tempa**: odchylenie standardowe / średnia prędkości per okrążenie × 100%')
    lines.append('- **Wskaźnik zaniku**: średnia prędkość 18–24h / średnia prędkość 0–6h')
    lines.append('- **SSR zdarzenia**: liczba godzin, w których prędkość godzinowa spadła '
                 'o >3.5 km/h względem poprzedniej godziny')
    lines.append('- **Dystans okrążenia**: 1725 m (oficjalna pętla Pabianice)')
    lines.append('')
    lines.append('**Źródła benchmarków:**')
    lines.append('- Knechtle et al. (2021): *Pacing Strategy During 24-Hour Ultramarathon Running* '
                 '— IJSPP (PMC 7739753)')
    lines.append('- Cejka et al. (2022): *The Relationship between 24h Ultramarathon Performance '
                 'and the "Big Three" Strategies* (PMC 9609733)')
    lines.append('- Hunter et al. (2016): *24-Hour Ultra-Marathon Running Narrative Review* (PMC 12996520)')
    lines.append('')

    return '\n'.join(lines)


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    os.makedirs(ANALIZA_DIR, exist_ok=True)

    print('=' * 60)
    print('Analiza pacing TOP 10 — PZLA MP 24h Pabianice 2026')
    print('=' * 60)

    print('\n[1] Ładowanie danych...')
    laps_by_athlete = load_laps()
    results = load_results()
    print(f'  Zawodnicy z danymi: {len(laps_by_athlete)}')
    for name, laps in laps_by_athlete.items():
        print(f'    {name}: {len(laps)} okrążeń')

    print('\n[2] Obliczanie metryk...')
    metrics_list = []
    for name, laps in laps_by_athlete.items():
        if not laps:
            print(f'  {name}: brak danych, pomijam')
            continue
        m = compute_metrics(name, laps, results.get(name, {}))
        if m:
            metrics_list.append(m)
            print(f'  #{m["pozycja"]:2d} {name}: CV={m["cv_tempa_proc"]:.1f}% '
                  f'zanik={m["wskaznik_zaniku"]:.3f} SSR={m["ssr_zdarzenia"]}')

    if not metrics_list:
        print('[BŁĄD] Brak metryk do analizy.')
        raise SystemExit(1)

    metrics_list.sort(key=lambda m: m['pozycja'])

    print('\n[3] Zapisywanie metryki_top10.csv...')
    save_metrics_csv(metrics_list)

    print('\n[4] Generowanie raportu...')
    report = generate_report(metrics_list, laps_by_athlete, results)
    with open(ANALIZA_FILE, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f'  Zapisano {ANALIZA_FILE}')

    print(f'\n[OK] Gotowe.')
    print(f'  Metryki: {METRICS_FILE}')
    print(f'  Raport:  {ANALIZA_FILE}')


if __name__ == '__main__':
    main()
