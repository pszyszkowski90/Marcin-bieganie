#!/usr/bin/env python3
"""
Pobierz dane okrążeń top 10 z PZLA MP 24h Pabianice 2026.
Zapis do dane/

Użycie:
  python pobierz_dane.py          # pobierz dane i zapisz CSV
  python pobierz_dane.py --debug  # + zapisz raw HTML do dane/_debug_*.html
"""

import urllib.request
import urllib.parse
import re
import csv
import os
import sys
import time
from html.parser import HTMLParser

# ── Konfiguracja ────────────────────────────────────────────────────────────

RACE_ID  = '1434'
EDITION  = '16030'
BASE_URL = 'https://www.protimer.pl'
RESULTS_URL = f'{BASE_URL}/bio/export/results_online/{RACE_ID}/{EDITION}'
LAPS_URL    = f'{BASE_URL}/bio/export/details/{RACE_ID}/{EDITION}/'

HTTP_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Accept-Language': 'pl-PL,pl;q=0.9,en-US;q=0.8',
}

# Znany participant ID — anchor point do weryfikacji
MARCIN_PARTICIPANT_ID = 354648
MARCIN_USER_ID        = 18826

# Znane user IDs z profili ProTimer (do odkrycia participant IDs przez stronę profilu)
KNOWN_USER_IDS = {
    'Piotrowski Marek':    13945,
    'Napiórkowski Mariusz': 9267,
    'Skrobała Dariusz':    18829,
    'Szyszkowski Marcin':  18826,
}

LOOP_M = 1725  # metry na okrążenie

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DANE_DIR   = os.path.join(SCRIPT_DIR, 'dane')
DEBUG      = '--debug' in sys.argv

# ── HTTP ─────────────────────────────────────────────────────────────────────

def fetch_get(url):
    req = urllib.request.Request(url, headers={**HTTP_HEADERS, 'Accept': 'text/html'})
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.read().decode('utf-8', errors='replace')


def fetch_laps_post(participant_id):
    data = f'participant={participant_id}'.encode()
    headers = {
        **HTTP_HEADERS,
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': RESULTS_URL,
        'Accept': '*/*',
    }
    req = urllib.request.Request(LAPS_URL, data=data, headers=headers, method='POST')
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.read().decode('utf-8', errors='replace')


def save_debug_html(name, html):
    if DEBUG:
        path = os.path.join(DANE_DIR, f'_debug_{name}.html')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'  [debug] Zapisano {path}')

# ── HTML parser ───────────────────────────────────────────────────────────────

class TableParser(HTMLParser):
    """Parsuje wszystkie <table> z HTML — zwraca listę tabel jako listy wierszy."""

    def __init__(self):
        super().__init__()
        self.tables    = []   # [{'headers': [], 'rows': [[cell,...]], 'row_attrs': [{},...]}]
        self._tbl      = None
        self._row      = None
        self._cell     = None
        self._in_th    = False
        self._row_a    = {}

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'table':
            self._tbl = {'headers': [], 'rows': [], 'row_attrs': []}
            self.tables.append(self._tbl)
        elif tag == 'tr' and self._tbl is not None:
            self._row  = []
            self._row_a = a
        elif tag in ('th', 'td') and self._tbl is not None:
            self._cell  = {'text': '', 'href': None, 'attrs': a}
            self._in_th = (tag == 'th')
        elif tag == 'a' and self._cell is not None:
            href = a.get('href', '')
            if href:
                self._cell['href'] = href

    def handle_endtag(self, tag):
        if tag in ('th', 'td') and self._cell is not None and self._tbl is not None:
            if self._in_th:
                self._tbl['headers'].append(self._cell['text'].strip())
            elif self._row is not None:
                self._row.append(self._cell)
            self._cell  = None
            self._in_th = False
        elif tag == 'tr' and self._tbl is not None and self._row:
            self._tbl['rows'].append(self._row)
            self._tbl['row_attrs'].append(self._row_a)
            self._row = None

    def handle_data(self, data):
        if self._cell is not None:
            self._cell['text'] += data


# ── Parsowanie wyników ────────────────────────────────────────────────────────

def extract_participant_ids_from_html(html):
    """
    Szuka participant IDs osadzonych w HTML wyników na kilka różnych sposobów.
    Zwraca dict {participant_id: kontekst} i listę {imię/nazwisko: pid} jeśli uda się dopasować.
    """
    ids_found = {}

    # Wzorzec 1: data-participant="354648"
    for m in re.finditer(r'data-participant=["\'](\d{4,8})["\']', html, re.I):
        ids_found[int(m.group(1))] = 'data-participant'

    # Wzorzec 2: onclick z ID np. onclick="getDetails(354648)"
    for m in re.finditer(r'onclick=["\'][^"\']*?(\d{5,7})[^"\']*?["\']', html, re.I):
        pid = int(m.group(1))
        if pid not in (int(RACE_ID), int(EDITION)):
            ids_found[pid] = 'onclick'

    # Wzorzec 3: href z participant= lub /details/RACE/EDITION/ID
    for m in re.finditer(r'participant=(\d{4,8})', html, re.I):
        ids_found[int(m.group(1))] = 'href-param'

    for m in re.finditer(
        rf'/bio/export/details/{RACE_ID}/{EDITION}/(\d{{4,8}})', html, re.I
    ):
        ids_found[int(m.group(1))] = 'href-path'

    # Wzorzec 4: value= w ukrytym input blisko tabeli wyników
    for m in re.finditer(r'<input[^>]+name=["\']participant["\'][^>]+value=["\'](\d+)["\']',
                         html, re.I):
        ids_found[int(m.group(1))] = 'input-value'

    return ids_found


def parse_results_page(html):
    """
    Parsuje stronę wyników regex-based — niezawodne przy formatach "6 / 1" w pozycji
    i data-participant osadzonym na <a> w komórce (nie na <tr>).
    """
    athletes = []
    found_positions = set()

    # Podziel na bloki <tr>...</tr>
    trs = re.findall(r'<tr>(.*?)</tr>', html, re.DOTALL)

    for tr in trs:
        # Tylko wiersze zawodników — muszą mieć data-participant
        pid_m = re.search(r'data-participant="(\d+)"', tr)
        if not pid_m:
            continue
        pid = int(pid_m.group(1))

        # Pozycja — po </a> następuje "N" lub "N / K"
        # Obsługuje: "1", "6 / 1", "9 / 3" itp.
        pos_m = re.search(r'</a>\s*(\d+)\s*(?:/\s*\d+\s*)?</td>', tr)
        if not pos_m:
            continue
        pos = int(pos_m.group(1))

        if pos in found_positions:
            continue  # duplikat — pomiń
        if pos > 10:
            if found_positions and max(found_positions) >= 10:
                break   # mamy już top 10, reszta nieistotna
            continue

        found_positions.add(pos)

        # User ID (tylko dla zawodników z profilem ProTimer)
        uid_m = re.search(r'data-user="(\d+)"', tr)
        uid = int(uid_m.group(1)) if uid_m else None

        # Zawartość komórek — strip tagów HTML
        cells_raw = re.findall(r'<td[^>]*>(.*?)</td>', tr, re.DOTALL)
        cells = [re.sub(r'<[^>]+>', '', c).strip() for c in cells_raw]
        # Normalizuj białe znaki
        cells = [re.sub(r'\s+', ' ', c) for c in cells]

        name = cells[2] if len(cells) > 2 else f'Zawodnik#{pos}'
        # Kategoria: skróć do np. "M40" (usuń opis słowny po spacji)
        kat_raw = cells[7] if len(cells) > 7 else ''
        kat_m = re.match(r'(M\d+|F\d+|K\d+|[MFW]\d+)', kat_raw)
        kat = kat_m.group(1) if kat_m else kat_raw[:10]

        athletes.append({
            'pozycja':        pos,
            'imie_nazwisko':  name,
            'kategoria':      kat,
            'klub':           cells[5] if len(cells) > 5 else '',
            'okrazenia':      cells[8] if len(cells) > 8 else '',
            'dystans_km':     cells[10] if len(cells) > 10 else '',
            'czas_sumy':      cells[9] if len(cells) > 9 else '',
            'participant_id': pid,
            'user_id':        uid,
        })

    athletes.sort(key=lambda a: a['pozycja'])

    if DEBUG:
        print(f'  [debug] Sparsowano {len(athletes)} wierszy (szukano top 10)')

    return athletes


def find_pid_from_profile(user_id, athlete_name):
    """
    Próbuje wyciągnąć participant ID dla tego wyścigu ze strony profilu zawodnika.
    """
    url = f'{BASE_URL}/bio/user/results/{user_id}/'
    try:
        html = fetch_get(url)
        save_debug_html(f'profile_{user_id}', html)
        time.sleep(0.3)

        # Szukaj participant ID w kontekście tego wyścigu
        # Wzorzec: link lub onclick blisko wzmianki o RACE_ID lub EDITION
        snippets = []
        for m in re.finditer(rf'(?:{RACE_ID}|{EDITION})', html):
            start = max(0, m.start() - 300)
            end   = min(len(html), m.end() + 300)
            snippets.append(html[start:end])

        for snippet in snippets:
            # Szukaj 6-cyfrowego ID które nie jest race/edition
            for m in re.finditer(r'\b(\d{5,7})\b', snippet):
                candidate = int(m.group(1))
                if candidate not in (int(RACE_ID), int(EDITION)) and 100000 <= candidate <= 999999:
                    if DEBUG:
                        print(f'  [debug] Kandydat PID {candidate} ze strony profilu {user_id} '
                              f'({athlete_name})')
                    return candidate

        # Wzorzec 2: szukaj jawnie "participant=X"
        for m in re.finditer(r'participant=(\d+)', html):
            return int(m.group(1))

    except Exception as e:
        print(f'  [warn] Profil {user_id} ({athlete_name}): {e}')
    return None


# ── Parsowanie okrążeń ────────────────────────────────────────────────────────

def time_to_s(t):
    """HH:MM:SS lub MM:SS → sekundy. None jeśli niepoprawne."""
    t = t.strip()
    parts = t.split(':')
    try:
        if len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        if len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1])
    except (ValueError, IndexError):
        pass
    return None


def parse_laps(html, athlete_name, pozycja):
    """
    Parsuje HTML z okrążeniami ProTimer.
    Format tabeli: każdy <tr> ma <th>Okrążenie N</th> + 2x <td>.
    Kolumna 1: "HH:MM:SS (opcjonalnie: + domiar) / pozycja"
    Kolumna 2: absolutny czas zegara "HH:MM:SS.mmm"
    Wiersz "Gunshot" zawiera czas startu wyścigu.
    """
    # Znajdź tabelę z okrążeniami — szukamy tej która zawiera "Gunshot" i "Okrążenie"
    tables_html = re.findall(r'<table[^>]*>(.*?)</table>', html, re.DOTALL)

    laps_table_html = None
    for t in tables_html:
        t_lower = t.lower()
        if 'gunshot' in t_lower or ('okr' in t_lower and len(re.findall(r'<tr', t)) > 50):
            laps_table_html = t
            break

    if laps_table_html is None:
        # Fallback: największa tabela
        if tables_html:
            laps_table_html = max(tables_html, key=len)
        else:
            print(f'  [warn] Brak tabel HTML dla {athlete_name}')
            return []

    rows_html = re.findall(r'<tr[^>]*>(.*?)</tr>', laps_table_html, re.DOTALL)

    if DEBUG:
        print(f'  [debug] Tabela okrazenia {athlete_name}: {len(rows_html)} wierszy')

    gunshot_abs_s = None
    laps = []

    for row_html in rows_html:
        # Label z <th>
        label_m = re.search(r'<th[^>]*>(.*?)</th>', row_html, re.DOTALL)
        label   = re.sub(r'<[^>]+>', '', label_m.group(1)).strip() if label_m else ''

        # Dane z <td>
        td_vals = re.findall(r'<td[^>]*>(.*?)</td>', row_html, re.DOTALL)
        cells   = [re.sub(r'<[^>]+>', '', td).strip() for td in td_vals]

        if not label and not cells:
            continue

        label_lower = label.lower()

        # Wiersz startu (Gunshot)
        if 'gunshot' in label_lower or (not label and not any(cells)):
            if len(cells) >= 2:
                abs_m = re.match(r'(\d+):(\d+):(\d+(?:\.\d+)?)', cells[1])
                if abs_m:
                    h, m, s = int(abs_m.group(1)), int(abs_m.group(2)), float(abs_m.group(3))
                    gunshot_abs_s = h * 3600 + m * 60 + s
            continue

        # Wiersz okrążenia: "Okrążenie N" lub "Okr. N"
        lap_num_m = re.search(r'(\d+)', label)
        if not lap_num_m or not cells:
            continue
        lap_num = int(lap_num_m.group(1))

        # Czas okrążenia z komórki 0: "00:10:05 (+ 0,426km) / 39"
        lap_time_m = re.match(r'(\d+):(\d+):(\d+)', cells[0])
        if not lap_time_m:
            continue
        lap_s = int(lap_time_m.group(1)) * 3600 + int(lap_time_m.group(2)) * 60 + int(lap_time_m.group(3))
        if lap_s <= 0:
            continue

        # Czas kumulatywny z absolutnego czasu zegara (kolumna 1)
        cum_s = None
        if len(cells) >= 2 and gunshot_abs_s is not None:
            abs_m2 = re.match(r'(\d+):(\d+):(\d+(?:\.\d+)?)', cells[1])
            if abs_m2:
                h, m, s = int(abs_m2.group(1)), int(abs_m2.group(2)), float(abs_m2.group(3))
                abs_s = h * 3600 + m * 60 + s
                # Obsługa przejścia przez północ (wyścig trwa >12h po starcie)
                if abs_s < gunshot_abs_s:
                    abs_s += 86400
                cum_s = abs_s - gunshot_abs_s

        if cum_s is None:
            # Fallback: zsumuj czasy okrążeń
            cum_s = sum(l['czas_okr_s'] for l in laps) + lap_s

        speed = (LOOP_M / lap_s * 3.6) if lap_s > 0 else 0.0
        pace  = (lap_s / (LOOP_M / 1000) / 60) if lap_s > 0 else 0.0

        laps.append({
            'zawodnik':      athlete_name,
            'pozycja':       pozycja,
            'nr_okrazenia':  lap_num,
            'czas_okr_s':    lap_s,
            'czas_kum_s':    int(round(cum_s)),
            'dystans_m':     LOOP_M,
            'predkosc_kmh':  round(speed, 3),
            'tempo_min_km':  round(pace, 3),
            'godzina_biegu': round(cum_s / 3600, 4),
        })

    return laps


# ── Zapis CSV ─────────────────────────────────────────────────────────────────

LAP_FIELDS = [
    'zawodnik', 'pozycja', 'nr_okrazenia', 'czas_okr_s', 'czas_kum_s',
    'dystans_m', 'predkosc_kmh', 'tempo_min_km', 'godzina_biegu',
]

ATHLETE_FIELDS = [
    'pozycja', 'imie_nazwisko', 'kategoria', 'klub',
    'okrazenia', 'dystans_km', 'czas_sumy', 'participant_id', 'user_id',
]


def save_csvs(athletes, all_laps_by_athlete):
    os.makedirs(DANE_DIR, exist_ok=True)

    # top10_wyniki.csv
    with open(os.path.join(DANE_DIR, 'top10_wyniki.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=ATHLETE_FIELDS)
        w.writeheader()
        for a in athletes:
            w.writerow({k: a.get(k, '') for k in ATHLETE_FIELDS})
    print(f'  Zapisano top10_wyniki.csv ({len(athletes)} zawodników)')

    # okrazenia_top10.csv (wszystkie razem)
    all_laps = []
    for laps in all_laps_by_athlete.values():
        all_laps.extend(laps)
    all_laps.sort(key=lambda x: (x['pozycja'], x['nr_okrazenia']))

    with open(os.path.join(DANE_DIR, 'okrazenia_top10.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=LAP_FIELDS)
        w.writeheader()
        w.writerows(all_laps)
    print(f'  Zapisano okrazenia_top10.csv ({len(all_laps)} okrążeń)')

    # per zawodnik
    for name, laps in all_laps_by_athlete.items():
        if not laps:
            continue
        safe = re.sub(r'[^\w\- ]', '', name).strip().replace(' ', '_').lower()
        path = os.path.join(DANE_DIR, f'okrazenia_{safe}.csv')
        with open(path, 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=LAP_FIELDS)
            w.writeheader()
            w.writerows(laps)
        print(f'  Zapisano okrazenia_{safe}.csv ({len(laps)} okrążeń)')


# ── Główny flow ───────────────────────────────────────────────────────────────

def main():
    print('=' * 60)
    print('Pobieranie danych: PZLA MP 24h Pabianice 2026')
    print(f'URL: {RESULTS_URL}')
    print('=' * 60)

    # 1. Pobierz stronę wyników
    print('\n[1] Pobieranie strony wyników...')
    try:
        results_html = fetch_get(RESULTS_URL)
    except Exception as e:
        print(f'[BŁĄD] Nie można pobrać wyników: {e}')
        sys.exit(1)
    save_debug_html('results', results_html)
    print(f'  OK — {len(results_html):,} znaków')

    # 2. Szukaj participant IDs w HTML wyników
    print('\n[2] Szukanie participant IDs w HTML...')
    ids_in_html = extract_participant_ids_from_html(results_html)
    if ids_in_html:
        print(f'  Znalezione IDs: {sorted(ids_in_html.keys())}')
    else:
        print('  Nie znaleziono participant IDs w głównym HTML.')

    # 3. Parsuj top 10
    print('\n[3] Parsowanie top 10...')
    athletes = parse_results_page(results_html)
    if not athletes:
        print('[BŁĄD] Nie sparsowano żadnego zawodnika.')
        sys.exit(1)
    print(f'  Sparsowano {len(athletes)} zawodników:')
    for a in athletes:
        print(f'    #{a["pozycja"]:2d}  {a["imie_nazwisko"]:<30s}  '
              f'{a["dystans_km"]:>6s} km  PID={a["participant_id"]}  UID={a["user_id"]}')

    # 4. Weryfikacja participant IDs (nowy parser wyciąga je bezpośrednio z HTML)
    print('\n[4] Weryfikacja participant IDs...')
    for a in athletes:
        # Fallback: wpisz znany PID dla Marcina jeśli brakuje
        if a['participant_id'] is None and 'Szyszkowski' in a['imie_nazwisko']:
            a['participant_id'] = MARCIN_PARTICIPANT_ID
            print(f'  Fallback: wstawiono PID {MARCIN_PARTICIPANT_ID} dla Marcina')
        # Uzupełnij known user IDs
        if a['user_id'] is None:
            for known_name, uid in KNOWN_USER_IDS.items():
                parts = known_name.split()
                if all(p in a['imie_nazwisko'] for p in parts):
                    a['user_id'] = uid

    found = sum(1 for a in athletes if a['participant_id'] is not None)
    print(f'  Participant IDs: {found}/{len(athletes)}')
    for a in athletes:
        status = f'PID={a["participant_id"]}' if a['participant_id'] else 'BRAK PID'
        print(f'    #{a["pozycja"]:2d}  {a["imie_nazwisko"]:<30s}  {status}')

    # 5. Pobierz okrążenia
    print('\n[5] Pobieranie okrążeń...')
    all_laps = {}

    for a in athletes:
        name = a['imie_nazwisko']
        pid  = a['participant_id']

        if pid is None:
            print(f'  #{a["pozycja"]:2d} {name}: pominięto (brak participant ID)')
            all_laps[name] = []
            continue

        print(f'  #{a["pozycja"]:2d} {name} (PID={pid})...', end=' ', flush=True)
        try:
            laps_html = fetch_laps_post(pid)
            save_debug_html(f'laps_{pid}', laps_html)
            laps = parse_laps(laps_html, name, a['pozycja'])
            all_laps[name] = laps
            total_dist = len(laps) * LOOP_M / 1000
            if laps:
                print(f'OK — {len(laps)} okr, ~{total_dist:.1f} km')
            else:
                print('OK ale brak okrążeń (możliwy błąd parsowania)')
        except Exception as e:
            print(f'BŁĄD: {e}')
            all_laps[name] = []
        time.sleep(0.5)  # delikatne throttling

    # 6. Zapisz CSV
    print('\n[6] Zapisywanie CSV...')
    save_csvs(athletes, all_laps)

    # 7. Podsumowanie
    total_laps = sum(len(v) for v in all_laps.values())
    with_data  = sum(1 for v in all_laps.values() if v)
    print(f'\n[OK] Gotowe. {with_data}/{len(athletes)} zawodnikow z danymi, '
          f'{total_laps} okrazen lacznie.')
    if with_data < len(athletes):
        missing = [a['imie_nazwisko'] for a in athletes
                   if not all_laps.get(a['imie_nazwisko'])]
        print(f'  Brak danych: {missing}')
        print('  Wskazówka: uruchom z --debug i sprawdź dane/_debug_results.html')


if __name__ == '__main__':
    main()
