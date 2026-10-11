#!/usr/bin/env python3
"""Skala typografii telefonu: baza 16 px -> 14 px (współczynnik 0,875), wszystkie pozostałe rozmiary proporcjonalnie.

Dla każdej reguły CSS ze strony (kolejność jak w <link>), która ustawia font-size, line-height w px albo zmienną rozmiaru tekstu
(--*size*, --*-lh, --leading-*, --hero-title, --type-*), generuje kopię ze skalowanymi wartościami (px i vw ×0,875) w bloku
@media (max-width: 700px), z zachowaniem kontekstu @media/@supports i !important. Plik dołączany jako ostatni arkusz — kopie
wygrywają z oryginałami tak samo jak oryginały między sobą (ta sama specyficzność, ta sama kolejność).
Wyniki: mobile-skala.css (strona główna) i mobile-skala-podstrony.css (podstrony; z podstrony.css).
Uruchamiane z build.py; samodzielnie: python3 mobile_skala.py
"""
import re, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
F = 0.875
MOBILE = 700
VAR_RE = re.compile(r'^--(?:.*size.*|.*-lh|leading-.*|hero-title|type-.*)$')
SKIP_AT = ('@font-face', '@keyframes', '@-webkit-keyframes', '@page', '@property', '@counter-style', '@font-feature-values')


def strip_comments(css):
    return re.sub(r'/\*.*?\*/', '', css, flags=re.S)


def find_close(s, i):
    """i = indeks po '{'; zwraca indeks pasującego '}'."""
    depth, q, par = 1, None, 0
    n = len(s)
    while i < n:
        c = s[i]
        if q:
            if c == '\\': i += 1
            elif c == q: q = None
        elif c in '"\'': q = c
        elif c == '(': par += 1
        elif c == ')': par -= 1
        elif par <= 0:
            if c == '{': depth += 1
            elif c == '}':
                depth -= 1
                if depth == 0: return i
        i += 1
    raise ValueError('niezamknięty blok')


def split_top(s, sep=';'):
    """Dzieli ciało reguły na deklaracje i zagnieżdżone reguły (CSS nesting): koniec elementu = ';' albo '}' zamykające blok na poziomie 0."""
    out, cur, q, par, br = [], [], None, 0, 0
    for c in s:
        if q:
            cur.append(c)
            if c == q: q = None
            continue
        if c in '"\'': q = c
        elif c == '(': par += 1
        elif c == ')': par -= 1
        elif c == '{': br += 1
        elif c == '}': br -= 1
        cur.append(c)
        if par <= 0 and not q and ((c == sep and br == 0) or (c == '}' and br == 0)):
            out.append(''.join(cur).rstrip(';')); cur = []
    if ''.join(cur).strip(): out.append(''.join(cur))
    return out


def expand(sel, body):
    """Zwraca listę (selektor, deklaracje do skalowania) dla reguły i jej zagnieżdżonych reguł (spłaszczone: & → selektor rodzica)."""
    res, decls = [], []
    for piece in split_top(body):
        piece = piece.strip()
        if not piece: continue
        if '{' in piece:
            i = piece.index('{'); nsel = piece[:i].strip(); nbody = piece[i + 1:piece.rindex('}')]
            if nsel.startswith('@'): continue
            parts = [x.strip() for x in nsel.split(',')]
            psel = [x.strip() for x in sel.split(',')]
            joined = ','.join((n.replace('&', p) if '&' in n else f'{p} {n}') for n in parts for p in psel)
            res += expand(joined, nbody)
        elif ':' in piece:
            prop, val = piece.split(':', 1)
            if relevant(prop): decls.append(f'{prop.strip()}:{scale_val(val.strip())}')
    if decls: res.insert(0, (sel, ';'.join(decls)))
    return res


def walk(css, ctx, out):
    i, n = 0, len(css)
    while i < n:
        # prelude do '{' lub ';' na poziomie 0
        j, q, par = i, None, 0
        while j < n:
            c = css[j]
            if q:
                if c == '\\': j += 1
                elif c == q: q = None
            elif c in '"\'': q = c
            elif c == '(': par += 1
            elif c == ')': par -= 1
            elif par <= 0 and c in '{;': break
            j += 1
        if j >= n: break
        prelude = css[i:j].strip()
        if css[j] == ';':
            i = j + 1; continue
        k = find_close(css, j + 1)
        body = css[j + 1:k]
        i = k + 1
        if prelude.startswith('@'):
            if prelude.lower().startswith(SKIP_AT): continue
            if prelude.lower().startswith(('@media', '@supports', '@layer', '@container')):
                walk(body, ctx + [prelude], out)
            continue
        out.append((ctx, prelude, body))


def scale_val(v):
    def px(m):
        x = float(m.group(1)) * F
        return f'{round(x * 2) / 2:g}px'
    def vw(m):
        return f'{round(float(m.group(1)) * F, 3):g}vw'
    v = re.sub(r'(?<![\w.-])(-?\d*\.?\d+)px', px, v)
    return re.sub(r'(?<![\w.-])(-?\d*\.?\d+)vw', vw, v)


def relevant(prop):
    p = prop.strip().lower()
    return p in ('font-size', 'line-height') or bool(VAR_RE.match(p))


def ctx_ok(ctx):
    for c in ctx:
        cl = c.lower()
        if 'print' in cl: return False
        for m in re.finditer(r'min-width:\s*(\d+(?:\.\d+)?)px', cl):
            if float(m.group(1)) > MOBILE: return False
    return True


def generate_sheet(css_files):
    parts = []
    for f in css_files:
        p = ROOT / f
        if not p.exists(): continue
        rules = []
        walk(strip_comments(p.read_text(encoding='utf-8')), [], rules)
        for ctx, sel, body in rules:
            if not ctx_ok(ctx): continue
            exp = expand(sel, body)
            if not exp: continue
            for esel, edecl in exp:
                txt = f'{esel}{{{edecl}}}'
                for c in reversed(ctx): txt = f'{c}{{{txt}}}'
                parts.append(txt)
    head = (f'/* GENEROWANE przez _generator/narzedzia/mobile_skala.py — nie edytuj ręcznie. Telefon (≤{MOBILE} px): baza 14 px = 16 px × {F}, '
            f'wszystkie rozmiary i interlinie w px/vw skalowane ×{F}. */\n')
    return head + f'@media (max-width:{MOBILE}px){{\n' + '\n'.join(parts) + '\n}\n', len(parts)


def home_sheets():
    html = (ROOT / 'index.html').read_text(encoding='utf-8')
    hrefs = re.findall(r'<link rel="stylesheet" href="([^"?]+)', html)
    return [h for h in hrefs if not h.startswith(('http', '//')) and not h.startswith('mobile-skala')]


def generate():
    sheets = home_sheets()
    a, na = generate_sheet(sheets)
    (ROOT / 'mobile-skala.css').write_text(a, encoding='utf-8')
    b, nb = generate_sheet(sheets + ['podstrony.css'])
    (ROOT / 'mobile-skala-podstrony.css').write_text(b, encoding='utf-8')
    print(f'mobile-skala.css: {na} reguł; mobile-skala-podstrony.css: {nb} reguł')


if __name__ == '__main__':
    generate()
