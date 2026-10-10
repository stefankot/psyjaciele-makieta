#!/usr/bin/env python3
# generated: psyjaciele-podstrony
"""os_mobilna.py — rysunek do pionowej osi kroków na komórce (poniżej 1001 px): scenka, z której wychodzi kreska przechodząca w oś listy.

Model rysuje scenkę z jedną kreską biegnącą pionowo skrajnie po lewej: w dół do dolnej krawędzi (typ „gora” — rysunek nad listą)
albo od górnej krawędzi (typ „dol” — rysunek pod listą). Skrypt znajduje tę kreskę, przycina kadr tak, by dochodziła do krawędzi,
i zapisuje do _osie.json szerokość wyświetlania oraz przesunięcie, przy którym kreska trafia w oś listy (obramowanie 2 px po lewej).

Użycie (z katalogu makiety; wymaga Pillow i numpy):
  python3 _generator/narzedzia/os_mobilna.py <id z osie.py> <surowy.png>
"""
import json
import subprocess
import sys

import numpy as np
from PIL import Image

import osie
from os_czasu import STAN

S = 0.26        # stała skala wyświetlania: kreska modelu (ok. 8 px) daje ok. 2 px, tyle co oś listy
LINIA = 2       # grubość osi listy w CSS (px)
LEWY = 30       # zapas kadru na lewo od kreski (px obrazu)
MAX_W = 342     # szerokość treści na telefonie 390 px


def main():
    o = next(x for x in osie.OSIE if x['id'] == sys.argv[1])
    typ = o['m']['typ']
    raw = np.array(Image.open(sys.argv[2]).convert('L'))
    raw[raw > 235] = 255
    if typ == 'dol':
        raw = raw[::-1]                                  # liczymy jak dla „gora”, na końcu odwracamy z powrotem
    d = raw < 150
    H, W = d.shape
    cur = np.zeros(W, int)
    best = np.zeros(W, int)
    for y in range(H):
        cur = np.where(d[y], cur + 1, 0)
        best = np.maximum(best, cur)
    xmin = max(0, int(np.where(best >= 150)[0].min()) - 6)   # kreska osi = skrajnie lewa kolumna z długim pionowym odcinkiem
    band = d[:, xmin:xmin + 20]
    rows = np.where(band.any(1))[0]
    y_line = int(rows.max())                             # dokąd dochodzi kreska
    y_other = int(np.where(d[:, xmin + 44:].any(1))[0].max())   # dół reszty scenki
    y_end = y_other + 24
    if y_line < y_end + 3:                               # kreska za krótka: przedłuż ją prosto w dół
        prof = raw[y_line - 14:y_line - 10, xmin:xmin + 20].min(0)
        y_end = min(H - 1, y_end)
        raw[y_line - 10:y_end + 1, xmin:xmin + 20] = prof
        y_line = y_end
    bottom = min(y_line - 2, y_end)
    cols = np.where((raw[bottom - 12:bottom, xmin:xmin + 20] < 150).any(0))[0]
    xc = xmin + (cols.min() + cols.max()) / 2
    kreska = cols.max() - cols.min() + 1
    top = max(0, int(np.where((raw < 150).any(1))[0].min()) - 8)
    right = min(W, int(np.where((raw < 150).any(0))[0].max()) + 9)
    lewy_rys = int(np.where((raw[top:bottom] < 150).any(0))[0].min())          # coś może wystawać na lewo od kreski (np. zawijas)
    left = max(int(round(xc - 84)), min(int(round(xc - LEWY)), lewy_rys - 4))   # najwyżej 84 px obrazu = 22 px strony (margines telefonu)
    crop = raw[top:bottom, max(0, left):right]
    if typ == 'dol':
        crop = crop[::-1]
    h, w = crop.shape
    s = min(S, MAX_W / w)
    png = osie.ROOT / osie.plik_m(o, 'png')
    Image.fromarray(crop).convert('RGB').save(png)
    subprocess.run(['avifenc', '-q', '50', '--qalpha', '90', '-s', '0', '-j', 'all', str(png), str(osie.ROOT / osie.plik_m(o))], check=True, capture_output=True)
    stan = json.loads(STAN.read_text(encoding='utf8')) if STAN.is_file() else {}
    stan.setdefault(o['id'], {})['m'] = {'w': round(w * s, 1), 'ratio': round(w / h, 4), 'shift': round(float(LINIA / 2 - (xc - max(0, left)) * s), 1),
                                         't': round(float(kreska * s), 1)}   # t = grubość narysowanej kreski na stronie (px), dla klina wyrównującego
    STAN.write_text(json.dumps(stan, indent=1, sort_keys=True) + '\n', encoding='utf8')
    print(f'{o["id"]} ({typ}): kadr {w}x{h}px, kreska {kreska}px → {kreska * s:.1f}px, na stronie {w * s:.0f}x{h * s:.0f}px, {stan[o["id"]]["m"]}')


if __name__ == '__main__':
    main()
