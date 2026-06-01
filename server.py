#!/usr/bin/env python3
"""
Support server dla Marcin #45 — 24h Pabianice 30.05.2026
Uruchomienie: python server.py
Otworz: http://localhost:8765
"""
import http.server
import socketserver
import urllib.request
import json
import os
import sys
from urllib.parse import urlparse, parse_qs

PORT = 8765
LOG_FILE = os.path.join(os.path.dirname(__file__), 'nutrition-log.json')
RESULTS_URL = 'https://www.protimer.pl/bio/export/results_online/1434/16030'
LAPS_URL    = 'https://www.protimer.pl/bio/export/details/1434/16030/'
PARTICIPANT = '354648'   # Marcin SZYSZKOWSKI #45
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/125.0'}


class Handler(http.server.BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path
        if path == '/api/results':
            self._results()
        elif path == '/api/laps':
            self._laps()
        elif path == '/api/competitor-laps':
            self._competitor_laps()
        elif path == '/api/log':
            self._log_get()
        elif path in ('/', '/support-dashboard.html'):
            self._file('support-dashboard.html', 'text/html; charset=utf-8')
        else:
            self.send_error(404)

    def do_POST(self):
        path = urlparse(self.path).path
        if path == '/api/log':
            self._log_post()
        else:
            self.send_error(404)

    # ── endpoints ────────────────────────────────────────────

    def _results(self):
        try:
            req = urllib.request.Request(RESULTS_URL, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=8) as resp:
                html = resp.read().decode('utf-8', errors='replace')
            self._json({'html': html})
        except Exception as e:
            self._json({'error': str(e)}, status=503)

    def _laps(self):
        try:
            body = f'participant={PARTICIPANT}'.encode()
            req = urllib.request.Request(
                LAPS_URL,
                data=body,
                headers={
                    **HEADERS,
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': '*/*',
                    'Referer': RESULTS_URL,
                },
                method='POST',
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                content = resp.read().decode('utf-8', errors='replace')
            self._json({'content': content})
        except Exception as e:
            self._json({'error': str(e)}, status=503)

    def _competitor_laps(self):
        qs = parse_qs(urlparse(self.path).query)
        pid = qs.get('id', [''])[0]
        if not pid or not pid.isdigit() or not (4 <= len(pid) <= 8):
            self._json({'error': 'invalid participant id'}, status=400)
            return
        try:
            body = f'participant={pid}'.encode()
            req = urllib.request.Request(
                LAPS_URL,
                data=body,
                headers={
                    **HEADERS,
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': '*/*',
                    'Referer': RESULTS_URL,
                },
                method='POST',
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                content = resp.read().decode('utf-8', errors='replace')
            self._json({'content': content})
        except Exception as e:
            self._json({'error': str(e)}, status=503)

    def _log_get(self):
        data = {}
        if os.path.exists(LOG_FILE):
            try:
                with open(LOG_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except Exception:
                pass
        self._json(data)

    def _log_post(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length)
        try:
            data = json.loads(body)
            with open(LOG_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self._json({'ok': True, 'file': LOG_FILE})
        except Exception as e:
            self._json({'error': str(e)}, status=400)

    def _file(self, fname, ctype):
        path = os.path.join(os.path.dirname(__file__), fname)
        try:
            with open(path, 'rb') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-Type', ctype)
            self.send_header('Content-Length', len(content))
            self._cors()
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404)

    # ── helpers ──────────────────────────────────────────────

    def _json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', len(body))
        self._cors()
        self.end_headers()
        self.wfile.write(body)

    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def log_message(self, fmt, *args):
        print(f'  {self.address_string()} — {fmt % args}')


class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    server = ThreadingHTTPServer(('localhost', PORT), Handler)
    print(f'\n🏃  Support server uruchomiony')
    print(f'   Otwórz: http://localhost:{PORT}')
    print(f'   Log:    {LOG_FILE}')
    print(f'   Ctrl+C aby zatrzymać\n')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nSerwer zatrzymany.')
        sys.exit(0)
