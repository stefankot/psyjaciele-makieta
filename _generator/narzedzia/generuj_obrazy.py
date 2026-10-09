#!/usr/bin/env python3
# generated: psyjaciele-podstrony
"""generuj_obrazy.py — generuje obrazy z _obrazy.json przez OpenAI Images (gpt-image-1) albo Gemini (NanoBanana).

[NIEZWERYFIKOWANE] Skrypt nie był uruchomiony: z środowiska, w którym powstał, api.openai.com i generativelanguage.googleapis.com
są nieosiągalne (brak ruchu wychodzącego). Formaty żądań pochodzą z pamięci modelu — sprawdź w dokumentacji dostawców.

Klucze: zmienne środowiskowe OPENAI_API_KEY / GEMINI_API_KEY albo plik _narzedzia/.env (linie KLUCZ=wartość; nie commituj).
Użycie (z katalogu makiety):
  python3 podstrony/_narzedzia/generuj_obrazy.py --engine openai --ids kard-00-hero,oko-00-hero [--ref plik.png ...]
  python3 podstrony/_narzedzia/generuj_obrazy.py --engine gemini --kind ilustracja --out podstrony/_wygenerowane
Wynik trafia do --out (domyślnie podstrony/_wygenerowane/<id>.png) — przejrzyj ręcznie i dopiero wtedy skopiuj pod ścieżkę „plik” z manifestu.
Referencje stylu: domyślnie 4 zaakceptowane ilustracje z home (assets/illustrations/services/service-*-a/b.png); zawsze podawaj ≥3.
"""
import argparse
import base64
import json
import mimetypes
import os
import sys
import urllib.request
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DEFAULT_REFS = ['assets/illustrations/services/service-internal-a.png', 'assets/illustrations/services/service-cardiology-b.png',
                'assets/illustrations/services/service-eyes-a.png', 'assets/illustrations/services/service-dentistry-a.png']


def key(name):
    if os.environ.get(name):
        return os.environ[name]
    env = HERE / '.env'
    if env.exists():
        for line in env.read_text().splitlines():
            if line.startswith(name + '='):
                return line.split('=', 1)[1].strip().strip('"\'')
    sys.exit(f'Brak klucza {name} (zmienna środowiskowa lub _narzedzia/.env)')


def openai_edit(prompt, refs, size):
    k = key('OPENAI_API_KEY')
    b = uuid.uuid4().hex
    parts = []

    def field(n, v):
        parts.append(f'--{b}\r\nContent-Disposition: form-data; name="{n}"\r\n\r\n{v}\r\n'.encode())

    field('model', 'gpt-image-1')
    field('prompt', prompt)
    field('size', size)
    field('background', 'transparent')
    field('output_format', 'png')
    for r in refs:
        p = Path(r)
        mt = mimetypes.guess_type(p.name)[0] or 'image/png'
        parts.append((f'--{b}\r\nContent-Disposition: form-data; name="image[]"; filename="{p.name}"\r\nContent-Type: {mt}\r\n\r\n').encode()
                     + p.read_bytes() + b'\r\n')
    parts.append(f'--{b}--\r\n'.encode())
    req = urllib.request.Request('https://api.openai.com/v1/images/edits', data=b''.join(parts),
                                 headers={'Authorization': f'Bearer {k}', 'Content-Type': f'multipart/form-data; boundary={b}'})
    with urllib.request.urlopen(req, timeout=300) as r:
        return base64.b64decode(json.load(r)['data'][0]['b64_json'])


def gemini(prompt, refs):
    k = key('GEMINI_API_KEY')
    parts = [{'text': prompt}]
    for r in refs:
        p = Path(r)
        parts.append({'inline_data': {'mime_type': mimetypes.guess_type(p.name)[0] or 'image/png', 'data': base64.b64encode(p.read_bytes()).decode()}})
    body = json.dumps({'contents': [{'parts': parts}]}).encode()
    req = urllib.request.Request('https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent',
                                 data=body, headers={'x-goog-api-key': k, 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=300) as r:
        for part in json.load(r)['candidates'][0]['content']['parts']:
            d = part.get('inline_data') or part.get('inlineData')
            if d:
                return base64.b64decode(d['data'])
    raise SystemExit('Gemini nie zwrócił obrazu')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--engine', choices=['openai', 'gemini'], required=True)
    ap.add_argument('--ids', help='lista id po przecinku')
    ap.add_argument('--kind', help='np. ilustracja — wszystkie obrazy tego rodzaju')
    ap.add_argument('--ref', action='append', help='plik referencji stylu (można wiele)')
    ap.add_argument('--out', default=str(ROOT / 'podstrony' / '_wygenerowane'))
    a = ap.parse_args()
    refs = [str(ROOT / r) if not Path(r).is_absolute() else r for r in (a.ref or DEFAULT_REFS)]
    if len(refs) < 3:
        sys.exit('Podaj co najmniej 3 referencje stylu (--ref).')
    rows = json.loads((ROOT / 'podstrony' / '_obrazy.json').read_text(encoding='utf-8'))['obrazy']
    ids = set(a.ids.split(',')) if a.ids else None
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for r in rows:
        if (ids and r['id'] not in ids) or (a.kind and r['rodzaj'] != a.kind) or (not ids and not a.kind):
            continue
        size = '1024x1024' if r['ratio'] == '1:1' else ('1536x1024' if r['ratio'] in ('3:2', '4:3', '21:9') else '1024x1536')
        img = openai_edit(r['prompt_en'], refs, size) if a.engine == 'openai' else gemini(r['prompt_en'], refs)
        (out / f"{r['id']}.png").write_bytes(img)
        print('zapisano', out / f"{r['id']}.png")


if __name__ == '__main__':
    main()
