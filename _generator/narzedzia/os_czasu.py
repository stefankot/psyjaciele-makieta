#!/usr/bin/env python3
# generated: psyjaciele-podstrony
"""os_czasu.py — składa rysunek „osi kroków”: oś z N kółkami (wycięta ze wzoru szcz-03-kalendarz.png) + scenka stojąca na osi.

Kadr i geometria są takie same jak we wzorze (1536x1024, kreska osi w wierszach 606–609), więc styl .phase-timeline.has-art
z podstrony.css ustawia każde kółko nad środkiem swojej kolumny, niezależnie od liczby kroków.
Scenka: czarna kreska na białym tle, bez osi. Skrypt przycina ją do rysunku, skaluje stałą skalą (wszystkie scenki mają wtedy
tę samą kreskę i wielkość postaci) i stawia stopami na osi; wyższa scenka dostaje wyższe pole rysunku (_osie.json).

Użycie (z katalogu makiety; wymaga Pillow i numpy):
  python3 _generator/narzedzia/os_czasu.py <id z osie.py> <surowy.png> [--h WYSOKOŚĆ_PX] [--poz POZYCJA]
"""
import json
import subprocess
import sys

import numpy as np
from PIL import Image

import osie

W, H = 1536, 1024
LINE_Y0, LINE_Y1 = 606, 610          # wiersze kreski osi we wzorze
CY = 609.5                           # środek kółek
VIS_W = W / 0.9467                   # szerokość widocznego pola (background-size: 94.67%)
OFF_X = (VIS_W - W) * 0.512          # przesunięcie obrazu w polu (background-position-x: 51.2%)
SKALA = 0.87                         # stała skala scenek: model rysuje je wszystkie w tej samej wielkości i tą samą kreską (ok. 6 px → 5,2 px)
MAX_H = 480                          # najwyższa scenka (px obrazu)
VIS_BOTTOM, VIS_H = 660, 390         # dół widocznego pola i jego wysokość we wzorze (proporcje 4.16:1)
STAN = osie.ROOT / '_generator/narzedzia/_osie.json'   # proporcje pola rysunku dla scenek wyższych niż we wzorze


def centra(n):
    return [VIS_W * (i + .5) / n - OFF_X for i in range(n)]


def _runs(a):
    out = []
    for r in a:
        d = np.diff(np.concatenate(([0], r.astype(np.int8), [0])))
        out.extend(np.where(d == -1)[0] - np.where(d == 1)[0])
    return np.array(out)


def kreska(mask):
    return float(np.median(np.concatenate([_runs(mask), _runs(mask.T)])))


def os_tlo(n):
    ref = np.array(Image.open(osie.ROOT / osie.WZOR).convert('L'))
    out = np.full((H, W), 255, np.uint8)
    cx = centra(n)
    seg = ref[598:618, 1125:1381]                       # czysty odcinek kreski między 4. a 5. kółkiem
    strip = np.concatenate([seg, seg[:, ::-1]] * 4, axis=1)
    x0, x1 = int(round(cx[0])), int(round(cx[-1]))
    out[598:618, x0:x1] = strip[:, :x1 - x0]
    yy, xx = np.mgrid[0:60, 0:60]
    circ = ref[580:640, 1056:1116].copy()               # 4. kółko wzoru (środek 1086, 609.5)
    circ[(xx - 30) ** 2 + (yy - 29.5) ** 2 > 26 ** 2] = 255
    disc = (xx - 30) ** 2 + (yy - 29.5) ** 2 <= 26 ** 2
    for c in cx:
        x = int(round(c)) - 30
        box = out[580:640, x:x + 60]
        box[disc] = circ[disc]
    return out, cx


def main():
    args = sys.argv[1:]
    opt = {}
    for k in ('--h', '--poz'):
        if k in args:
            i = args.index(k)
            opt[k] = float(args[i + 1])
            del args[i:i + 2]
    o = next(x for x in osie.OSIE if x['id'] == args[0])
    raw = np.array(Image.open(args[1]).convert('L'))
    raw[raw > 235] = 255                              # tło bywa złamaną bielą
    if o.get('x0'):
        raw[:, :o['x0']] = 255                        # kadr: tylko część scenki na prawo od x0
    mask = raw < 150
    ys, xs = np.where(mask)
    crop = raw[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    k = kreska(mask[ys.min():ys.max() + 1, xs.min():xs.max() + 1])
    h = opt.get('--h') or o.get('h') or min(MAX_H, crop.shape[0] * SKALA)
    f = h / crop.shape[0]
    w = int(round(crop.shape[1] * f))
    h = int(round(h))
    sc = np.array(Image.fromarray(crop).resize((w, h), Image.LANCZOS))
    canvas, cx = os_tlo(o['n'])
    poz = opt.get('--poz', o['poz'])
    step = cx[1] - cx[0]
    left = max(0, min(W - w, int(round(cx[0] + poz * step - w / 2))))
    top = LINE_Y1 - h
    canvas[top:top + h, left:left + w] = np.minimum(canvas[top:top + h, left:left + w], sc)
    png = osie.ROOT / osie.plik(o, 'png')
    Image.fromarray(canvas).convert('RGB').save(png)
    subprocess.run(['avifenc', '-q', '50', '--qalpha', '90', '-s', '0', '-j', 'all', str(png), str(osie.ROOT / osie.plik(o))], check=True, capture_output=True)
    vis_h = max(VIS_H, VIS_BOTTOM - (top - 14))       # wyższa scenka = wyższe pole rysunku; oś zostaje w tym samym miejscu od dołu
    stan = json.loads(STAN.read_text(encoding='utf8')) if STAN.is_file() else {}
    stan[o['id']] = {'ratio': round(VIS_W / vis_h, 3), 'y': round((vis_h - VIS_BOTTOM) / (vis_h - H) * 100, 2)}
    STAN.write_text(json.dumps(stan, indent=1, sort_keys=True) + '\n', encoding='utf8')
    print(f'{o["id"]}: kreska surowa {k:.1f}px, skala {f:.2f}, scenka {w}x{h}px na pozycji {poz} → {osie.plik(o)}')


if __name__ == '__main__':
    main()
