#!/usr/bin/env python3
# generated: psyjaciele-podstrony
"""checks.py — kontrole statyczne podstron: pokrycie treści (V1), linki (V2), identyfikatory/nagłówki (V4/V5), kolory (V6), obrazy (V13/V14).

Użycie: python3 _generator/narzedzia/checks.py [slug …]  → kod wyjścia ≠ 0 przy błędach.
"""
import json
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import home as H  # noqa: E402
import strony  # noqa: E402

ROOT = HERE.parents[1]


REMOVED = {'zespol': ['ktora-lekarke-wybrac']}


def norm(s):
    s = s.replace('­', '').replace(' ', ' ').replace(' ', ' ')
    s = s.replace('­', '')
    return re.sub(r'\s+', ' ', s).strip()


def texts(soup, sel):
    return [norm(e.get_text(' ')) for e in soup.select(sel)]


def check(slug, pages):
    errs, warns = [], []
    out_path = ROOT / pages.out[slug]
    html = out_path.read_text(encoding='utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    src = BeautifulSoup((ROOT / '_generator' / 'tresci-podstron' / 'czyste' / f'{slug}.html').read_text(encoding='utf-8'), 'html.parser').select_one('div.content')
    main = soup.select_one('main')
    mt = norm(main.get_text(' '))
    mt_nospace = re.sub(r'[^0-9A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]', '', mt)
    # V1 pokrycie: każdy blok tekstu źródła musi wystąpić w main
    miss = []
    # sekcje usunięte na polecenie użytkownika (8.10.2026) — wyłączone z kontroli pokrycia
    skip = set()
    for sid in REMOVED.get(slug, []):
        h = src.find(id=sid)
        if h:
            skip.add(id(h))
            for sib in h.find_next_siblings():
                if sib.name in ('h1', 'h2'):
                    break
                skip.add(id(sib))
                skip.update(id(x) for x in sib.find_all(True))
    for e in src.select('h1,h2,h3,p,li,td,th'):
        if e.find_parent('nav') or id(e) in skip:
            continue
        t = norm(e.get_text(' '))
        if slug == 'zespol' and e.name == 'h2' and t.startswith('lek. wet. '):
            t = 'Lekarka weterynarii ' + t[len('lek. wet. '):]   # skrót rozwinięty na polecenie użytkownika
        if not t:
            continue
        if e.name == 'p' and 'cta-wizyta' in (e.get('class') or []):
            continue   # zdanie „Umów wizytę: …” usunięte na polecenie użytkownika (8.10.2026) — powtarzało przyciski
        key = re.sub(r'[^0-9A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]', '', t)
        if key not in mt_nospace:
            miss.append(t[:80])
    if miss:
        errs.append(f'V1 brak tekstu ({len(miss)}): ' + ' | '.join(miss[:6]))
    # V2 linki
    base = out_path.parent
    for a in soup.select('a[href]'):
        h = a['href']
        if re.match(r'^(https?:|tel:|mailto:|#)', h):
            continue
        p = h.split('#')[0]
        if not p:
            continue
        tgt = (base / p).resolve()
        if p.startswith('/'):
            errs.append(f'V2 link bezwzględny: {h}')
            continue
        if not p.endswith('index.html') and not p.endswith('index-min.html'):
            errs.append(f'V2 link bez index.html: {h}')
        # linki do stron podstron istnieją po zbudowaniu kompletu; tu tylko raportujemy brakujące
        if not tgt.exists():
            warns.append(f'V2 cel nie istnieje (jeszcze): {h}')
    # fragmenty #id istnieją na stronie docelowej własnej strony
    ids = [e['id'] for e in soup.select('[id]')]
    dup = {i for i in ids if ids.count(i) > 1}
    if dup:
        errs.append(f'V4 duplikaty id: {sorted(dup)[:8]}')
    for a in soup.select('a[href^="#"]'):
        f = a['href'][1:]
        if f and f not in ids:
            errs.append(f'V4 fragment bez celu: #{f}')
    # V5 nagłówki
    h1 = soup.select('h1')
    if len(h1) != 1:
        errs.append(f'V5 h1 = {len(h1)}')
    last = 1
    for h in soup.select('main h1,main h2,main h3,main h4,main h5'):
        lv = int(h.name[1])
        if lv > last + 1:
            errs.append(f'V5 przeskok poziomu nagłówka: h{last}→h{lv} „{norm(h.get_text(" "))[:40]}”')
        last = lv
    # V6 kolory w nowych plikach
    # (sprawdzane osobno dla CSS) — tu: brak inline style z kolorem
    for e in soup.select('[style]'):
        st = e['style']
        if re.search(r'#[0-9a-fA-F]{3,8}\b|rgb\(|hsl\(', st):
            errs.append(f'V6 literał koloru w style: {st[:60]}')
    # V13 obrazy
    figs = soup.select('figure.placeholder')
    low = 2 if slug == 'zespol' else 3   # zespół: baner pracy ma już prawdziwy obraz (pies), nie placeholder
    if slug != 'polityka-prywatnosci' and not (low <= len(figs) <= 7):
        errs.append(f'V13 liczba placeholderów = {len(figs)} (wymagane {low}–7)')
    if slug == 'polityka-prywatnosci' and figs:
        errs.append('V13 polityka ma placeholdery')
    # V14: skrypty minimal*
    for s in soup.select('script[src]'):
        if re.search(r'minimal(-nowa)?\.js', s['src']):
            errs.append(f'V14 załadowany {s["src"]}')
    # sekcje: sąsiednie powierzchnie — zapewnia generator
    return errs, warns


def main():
    slugs = sys.argv[1:] or strony.ALL_SLUGS
    all_slugs = [p.stem for p in sorted((ROOT / '_generator' / 'tresci-podstron' / 'czyste').glob('*.html'))]
    pages = H.Pages(all_slugs)
    bad = 0
    for s in slugs:
        if not (ROOT / pages.out[s]).exists():
            print(f'-- {s}: brak pliku')
            continue
        e, w = check(s, pages)
        print(f'{"OK " if not e else "ERR"} {s}  błędy={len(e)} ostrzeżenia={len(w)}')
        for x in e:
            print('    ✗', x)
        for x in w[:4]:
            print('    ~', x)
        bad += len(e)
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
