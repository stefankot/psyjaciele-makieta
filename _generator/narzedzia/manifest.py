# generated: psyjaciele-podstrony
"""manifest.py — _obrazy.json (źródło prawdy), _obrazy.md, OBRAZY-PROMPTY.md.

Wejście: wyniki build.py (placeholdery użyte na stronach: sekcja/rola) + rejestr obrazy.OBRAZY (opisy, prompty).
Zapisuje wyłącznie w podstrony/. Pliki .json nie mogą nieść znacznika HTML, więc znacznik jest polem "_generated".
"""
import json
from collections import OrderedDict

import obrazy

ROD = {'foto': 'zdjęcie', 'pas': 'pas (zdjęcie panoramiczne)', 'wycinek': 'wycinek z przezroczystością',
       'ilustracja': 'ilustracja liniowa', 'diagram': 'diagram', 'ikona': 'ikona'}


def collect(results):
    """results: {slug: {'placeholders': [...]}} → lista wpisów manifestu w kolejności stron i występowania."""
    rows = []
    seen = set()
    for slug, r in results.items():
        for ph in r['placeholders']:
            pid = ph['id']
            if pid in seen:
                raise SystemExit(f'DUPLIKAT data-ph: {pid}')
            seen.add(pid)
            sp = obrazy.OBRAZY[pid]
            rows.append(OrderedDict([
                ('id', pid), ('strona', sp['strona']), ('sekcja', ph.get('sekcja', '')), ('rola', ph.get('rola', '')),
                ('rodzaj', sp['kind']), ('ratio', ph['ratio'].replace('/', ':')), ('plik', ph['file']),
                ('min_px', sp['min_px']), ('opis_pl', sp['opis_pl']), ('czego_unikać', sp['czego_unikac_pl']),
                ('alt_pl', sp['alt']), ('podpis_pl', sp['title']), ('prompt_en', sp['prompt_en']),
                ('obróbka', sp['obrobka']), ('źródło', sp['zrodlo'])]))
    unused = sorted(set(obrazy.OBRAZY) - seen)
    return rows, unused


def to_json(rows):
    return json.dumps({'_generated': 'psyjaciele-podstrony', 'liczba': len(rows), 'obrazy': rows}, ensure_ascii=False, indent=1) + '\n'


def to_md(rows):
    out = ['<!-- generated: psyjaciele-podstrony -->', '# Obrazy do wgrania (manifest)', '',
           f'Liczba placeholderów: **{len(rows)}**. Źródło prawdy: `_obrazy.json`. Wgraj plik pod ścieżką z kolumny „Plik” '
           '(względem katalogu makiety) i odśwież stronę — ramka podmieni się sama (`podstrony.js`).', '']
    by = OrderedDict()
    for r in rows:
        by.setdefault(r['strona'], []).append(r)
    for strona, lst in by.items():
        out += [f'## {strona}', '', '| ID | Sekcja | Rodzaj | Proporcje | Min. px | Plik | Opis | Źródło |', '|---|---|---|---|---|---|---|---|']
        for r in lst:
            out.append(f"| `{r['id']}` | {r['sekcja'] or '—'} | {ROD[r['rodzaj']]} | {r['ratio']} | {r['min_px']} | "
                       f"`{r['plik']}` | {r['opis_pl']} | {r['źródło']} |")
        out.append('')
        for r in lst:
            out.append(f"- **{r['id']}** — alt: „{r['alt_pl']}”; podpis: „{r['podpis_pl']}”; unikać: {r['czego_unikać']}; obróbka: {r['obróbka']}.")
        out.append('')
    return '\n'.join(out) + '\n'


def to_prompts(rows):
    out = ['<!-- generated: psyjaciele-podstrony -->', '# Prompty do generowania obrazów (EN)', '',
           'Jeden blok na obraz; nazwa pliku w drugim wierszu każdego bloku. Obrazy z kolumny „źródło” oznaczone jako '
           '*prawdziwe zdjęcie* najlepiej zastąpić zdjęciem z przychodni (za zgodą opiekunów) — prompt jest wtedy tylko zapasowy.', '']
    for r in rows:
        out += [f"## {r['id']}", '', '```text', r['prompt_en'].rstrip(), '```', '']
    return '\n'.join(out) + '\n'
