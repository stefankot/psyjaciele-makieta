#!/usr/bin/env python3
# generated: psyjaciele-podstrony
"""zdjecia_wstaw.py — wstawia wygenerowane zdjęcie na stronę: kadruje do proporcji slotu, zmniejsza, zapisuje JPG w assets/podstrony/<strona>/.

Użycie (z katalogu makiety):
  python3 _generator/narzedzia/zdjecia_wstaw.py <nr 1-45> <plik-źródłowy> [--out KATALOG]   # --out: próba na sucho do innego katalogu
Plan (nr → plik, strona, slot, paleta): _generator/dokumentacja/prompt-chatgpt-brakujace-obrazy/plan-zdjec.json
Surowy plik trafia do _generator/wyniki/_nowe-zdjecia/raw/; stary JPG jest kopiowany do _archiwum/zdjecia-przed-wymiana-2026-10-09/ (tylko jeśli tam go jeszcze nie ma).
Rozmiary: szeroki slot do 1800 px szerokości, pas 21:9 do 2400, pion 4:5 do 1600 px wysokości (bez powiększania).
Filtr „Gocław Film” jest WYŁĄCZONY (właściciel 9.10.2026: „wygląda sztampowo, zdejmij ze wszystkich zdjęć”); włącza go tylko --grade. Opis filtra: matowe, zielono-czarne czernie, kremowe biele, tonowanie cieni w ciemną zieleń,
świateł w kolor sekcji (paleta z planu), −8 % nasycenia, −6 % kontrastu, lekka winieta i drobne ziarno."""
import json
import shutil
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
PLAN = json.loads((ROOT / '_generator/dokumentacja/prompt-chatgpt-brakujace-obrazy/plan-zdjec.json').read_text(encoding='utf-8'))
HIGH = {'SALMON': (255, 226, 205), 'PEACH': (255, 236, 222), 'SAGE': (232, 240, 214), 'MIST': (236, 243, 228), 'IVORY': (255, 247, 236)}


def grade(im, pal, seed):
    a = np.asarray(im).astype(np.float32) / 255.0
    luma = (0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2])[..., None]
    a = luma + (a - luma) * 0.92                                   # -8 % nasycenia
    black = np.array([28, 43, 33], np.float32) / 255
    white = np.array([255, 245, 232], np.float32) / 255
    a = black + a * (white - black)                                # matowe czernie, kremowe biele
    luma = (0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2])[..., None]
    forest = np.array([18, 78, 44], np.float32) / 255
    tint = np.array(HIGH[pal], np.float32) / 255
    sh, hi = (1 - luma) ** 2, luma ** 2
    a = a * (1 - 0.10 * sh) + forest * 0.10 * sh                   # cienie → ciemna zieleń
    a = a * (1 - 0.08 * hi) + tint * 0.08 * hi                     # światła → kolor sekcji
    a = (a - 0.5) * 0.94 + 0.5                                     # −6 % kontrastu
    h, w = a.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    r = ((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2
    a *= (1 - 0.10 * np.clip((r - 0.35) / 1.2, 0, 1))[..., None]   # winieta
    rng = np.random.default_rng(seed)
    small = rng.normal(128, 40, (round(h * 0.8), round(w * 0.8))).clip(0, 255).astype(np.uint8)
    g = np.asarray(Image.fromarray(small).resize((w, h), Image.BILINEAR)).astype(np.float32) / 255 - 0.5
    a += g[..., None] * 0.045 * (0.6 + 0.4 * (1 - luma))           # ziarno (mocniejsze w cieniach)
    return Image.fromarray((a.clip(0, 1) * 255 + 0.5).astype(np.uint8))


CAP = {'21:9': ('w', 2400), '3:2': ('w', 1800), '4:5': ('h', 1600)}


def main():
    n = int(sys.argv[1])
    src = Path(sys.argv[2]).expanduser()
    out_dir = None
    if '--out' in sys.argv:
        out_dir = Path(sys.argv[sys.argv.index('--out') + 1])
    it = next(p for p in PLAN if p['n'] == n)
    im = Image.open(src).convert('RGB')
    W, H = im.size
    r = it['ratio']
    if W / H > r:            # za szeroki → utnij boki
        nw = round(H * r)
        im = im.crop(((W - nw) // 2, 0, (W - nw) // 2 + nw, H))
    else:                    # za wysoki → utnij górę i dół (środek)
        nh = round(W / r)
        top = (H - nh) // 2
        im = im.crop((0, top, W, top + nh))
    axis, cap = CAP[it['aspect']]
    if axis == 'w' and im.width > cap:
        im = im.resize((cap, round(cap / r)), Image.LANCZOS)
    if axis == 'h' and im.height > cap:
        im = im.resize((round(cap * r), cap), Image.LANCZOS)
    if '--grade' in sys.argv:
        im = grade(im, it['pal'], n)
    dest_dir = out_dir or (ROOT / 'assets/podstrony' / it['slug'])
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / it['file']
    if out_dir is None:
        old = dest
        bak = ROOT / '_archiwum/zdjecia-przed-wymiana-2026-10-09' / it['slug'] / it['file']
        if old.exists() and not bak.exists():
            bak.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(old, bak)
        raw = ROOT / '_generator/wyniki/_nowe-zdjecia/raw' / f"{n:02d}-{src.name}"
        raw.parent.mkdir(parents=True, exist_ok=True)
        if not raw.exists() and src.parent.resolve() != raw.parent.resolve():
            shutil.copy2(src, raw)
    im.save(dest, 'JPEG', quality=90, optimize=True, progressive=True)
    print(f"{n:02d} {it['file']}: źródło {W}x{H} → {im.width}x{im.height} ({it['aspect']}, slot {it['w']}x{it['h']}) → {dest}")


if __name__ == '__main__':
    main()
