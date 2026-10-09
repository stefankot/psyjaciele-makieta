#!/usr/bin/env python3
# generated: psyjaciele-podstrony
"""pomiar_analiza.py — zestawienia z _generator/wyniki/_pomiar/*.json (po pomiar.py).

Użycie: python3 pomiar_analiza.py <temat> [szerokości]
  meta          przewijanie poziome, błędy konsoli, 404
  przepelnienia elementy poza oknem, uciety tekst, tekst poza własnym boxem
  siatka        bloki poza 12 kolumnami (tolerancja 1,6 px; wykluczone: ilustracje, pełnoszerokie tła sekcji, stopka, przyciski)
  rytm          odstępy i interlinie niebędące wielokrotnością 8 px
  kontrast      tekst poniżej 4,5∶1 (3∶1 dla dużego)
  sieroty       jednoliterowe spójniki na końcu wiersza, jednowyrazowe ostatnie wiersze, pauza na początku wiersza
  nakladanie    nachodzące na siebie elementy
  puste         puste ramki i placeholdery bez obrazu
"""
import collections
import glob
import json
import re
import sys
from pathlib import Path

D = Path(__file__).resolve().parents[1] / 'wyniki' / '_pomiar'
TOPIC = sys.argv[1] if len(sys.argv) > 1 else 'meta'
WIDTHS = [int(x) for x in sys.argv[2].split(',')] if len(sys.argv) > 2 else None
DATA = {}
for f in sorted(glob.glob(str(D / '*@*.json'))):
    d = json.load(open(f, encoding='utf-8'))
    if WIDTHS is None or d['w'] in WIDTHS:
        DATA[(d['page'], d['w'])] = d


def grupuj(kind, key, val, limit=40):
    g = collections.defaultdict(lambda: collections.defaultdict(list))
    for (p, w), d in DATA.items():
        for it in d['issues'][kind]:
            g[key(it)][p].append((w, val(it)))
    for k, pp in sorted(g.items(), key=lambda kv: -sum(len(v) for v in kv[1].values()))[:limit]:
        ws = sorted({w for v in pp.values() for w, _ in v})
        print(f'  {k} | stron={len(pp)} szer={ws} | np. {list(pp)[:3]} {next(iter(pp.values()))[0][1]}')


def meta():
    for (p, w), d in sorted(DATA.items()):
        m, fl = d['meta'], []
        if m['scrollW'] > m['vw']:
            fl.append(f"przewijanie poziome {m['scrollW']}>{m['vw']}")
        if d['console']:
            fl.append('konsola: ' + ' | '.join(sorted({c[:100] for c in d['console']})))
        if d['net']:
            fl.append('sieć: ' + ' | '.join(sorted({n[:90] for n in d['net']})))
        if fl:
            print(p, w, fl)
    print('(brak wpisów = brak przewijania, błędów konsoli i 404)')


def siatka():
    EPS = 1.6
    TEXT = {'p', 'h1', 'h2', 'h3', 'h4', 'li', 'a', 'span', 'em', 'strong', 'dt', 'dd', 'td', 'th', 'summary', 'figcaption', 'button', 'label', 'cite', 'address', 'blockquote', 'tr', 'thead', 'tbody'}
    agg = collections.defaultdict(lambda: collections.defaultdict(list))
    for (p, w), d in DATA.items():
        m = d['meta']
        step = m['colW'] + m['gap']
        for b in d['blocks']:
            if b.get('excl') or b.get('top') or b['x1'] - b['x0'] < 20:
                continue
            ch = b['ch']
            if ch.startswith('footer') or b['s'].startswith('section') or b['s'].startswith('div.wrap.booking') or re.search(r'social-promo|booking|about-photo|hero-art|hero-links|hero-actions|hero-btn|hero-status|\.button|icon is-rated', b['s']):
                continue
            lc = (b['x0'] - m['wl']) / step + 1
            rc = (b['x1'] - m['wl'] + m['gap']) / step
            bad = abs(lc - round(lc)) * step > EPS or (abs(rc - round(rc)) * step > EPS and b['tag'] not in TEXT)
            key = (w, re.sub(r'#[^.]+', '', b['s'])[:50], b['d'])
            agg[key]['n'].append(1)
            if bad:
                agg[key]['bad'].append((p[:12], round(lc, 2), round(rc, 2), round(b['x0']), round(b['x1']), b['anc']))
    n = 0
    for (w, sg, dep), v in sorted(agg.items(), key=lambda kv: (kv[0][0], -len(kv[1]['bad']))):
        if v['bad']:
            n += 1
            print(w, f'{sg:50} d{dep} n={len(v["n"])} poza={len(v["bad"])} np. {v["bad"][0]}')
    if not n:
        print('(wszystko na siatce)')


def rytm():
    m8 = lambda v: abs(v / 8 - round(v / 8)) < 0.07
    agg = collections.defaultdict(set)
    for (p, w), d in DATA.items():
        for b in d['blocks']:
            if b.get('excl') or b['pos'] in ('absolute', 'fixed') or b['ch'].startswith('footer>div>div>div>div>div'):
                continue
            for prop in ('mt', 'mb', 'pt', 'pb', 'pl', 'pr', 'rg', 'cg'):
                v = b[prop]
                if v and not m8(v) and abs(v) < 400:
                    agg[(re.sub(r'#[^.]+', '', b['s'])[:44], prop, round(v, 1))].add((p[:12], w))
            if b['lh'] and b['txt'] and not m8(b['lh']):
                agg[(re.sub(r'#[^.]+', '', b['s'])[:44], 'line-height', round(b['lh'], 1))].add((p[:12], w))
    for k, v in sorted(agg.items(), key=lambda kv: -len(kv[1]))[:60]:
        print(k, sorted(v)[:3])
    print('(brak wpisów = wszystkie odstępy i interlinie są wielokrotnościami 8 px)')


T = {'meta': meta, 'siatka': siatka, 'rytm': rytm,
     'przepelnienia': lambda: [grupuj('overflowX', lambda i: i['s'], lambda i: f"x0={i['x0']} x1={i['x1']}"),
                               grupuj('clipped', lambda i: (i['s'], i['kind']), lambda i: ''),
                               grupuj('textOut', lambda i: (i['s'], i['why']), lambda i: i.get('t'))],
     'kontrast': lambda: grupuj('contrast', lambda i: (i['s'], i['fg'], i['bg']), lambda i: f"{i['ratio']}∶1 «{i['t']}»"),
     'sieroty': lambda: grupuj('orphan', lambda i: (i['kind'],), lambda i: i['s'], 60),
     'nakladanie': lambda: grupuj('overlap', lambda i: (i['a'], i['b']), lambda i: f"{i['ox']}×{i['oy']}"),
     'puste': lambda: [grupuj('empty', lambda i: (i['s'], i.get('why', '')), lambda i: ''), grupuj('emptyEl', lambda i: (i['s'],), lambda i: '')]}

if __name__ == '__main__':
    if not DATA:
        sys.exit('Brak danych: uruchom najpierw pomiar.py')
    T[TOPIC]()
