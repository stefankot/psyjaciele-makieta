#!/usr/bin/env python3
# generated: psyjaciele-podstrony
"""pomiar.py — pomiar wszystkich stron makiety przy kilku szerokościach (Playwright; Chrome z systemu albo Chromium).

Dla każdej strony × szerokości zapisuje _generator/wyniki/_pomiar/<strona>@<szer>.json: położenie bloków względem siatki 12 kolumn,
odstępy i interlinie, wystawanie poza okno, ucięty tekst, nakładanie się, kontrast, sierotki/wdowy, puste ramki, kotwice, 404 i konsola.
Analiza: python3 pomiar_analiza.py [meta|przepelnienia|siatka|rytm|kontrast|sieroty|nakladanie|puste]

Użycie (serwer statyczny w katalogu makiety: python3 -m http.server 8766 --bind 127.0.0.1):
  python3 _generator/narzedzia/pomiar.py [--widths 1710,1440,1280,1000,390] [--only home,zespol] [--base http://127.0.0.1:8766/]
Wymaga: playwright (pip install playwright; używa zainstalowanego Google Chrome albo `playwright install chromium`).
"""
import argparse
import asyncio
import json
from pathlib import Path

from playwright.async_api import async_playwright

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT / '_generator' / 'wyniki' / '_pomiar'
JS = (HERE / 'pomiar.js').read_text(encoding='utf-8')


def strony():
    ps = {'home': 'index.html', 'uslugi': 'uslugi-weterynaryjne/index.html', 'zespol': 'zespol/index.html',
          'polityka': 'polityka-prywatnosci/index.html'}
    for d in sorted((ROOT / 'uslugi-weterynaryjne').iterdir()):
        if d.is_dir():
            ps[d.name] = f'uslugi-weterynaryjne/{d.name}/index.html'
    return ps


async def jedna(ctx, base, name, rel, w, sem, wait):
    async with sem:
        pg = await ctx.new_page()
        await pg.set_viewport_size({'width': w, 'height': 900})
        msgs, bad = [], []
        pg.on('console', lambda m: msgs.append(f'{m.type}: {m.text}') if m.type in ('error', 'warning') else None)
        pg.on('pageerror', lambda e: msgs.append(f'pageerror: {e}'))
        pg.on('response', lambda r: bad.append(f'{r.status} {r.url}') if r.status >= 400 else None)
        pg.on('requestfailed', lambda r: bad.append(f'FAILED {r.url}'))
        await pg.goto(base + rel, wait_until='networkidle')
        H = await pg.evaluate('document.documentElement.scrollHeight')
        y = 0
        while y < H:                                  # przewiń całość: lazy-loading i animacje wejścia
            await pg.evaluate(f'window.scrollTo({{top:{y},behavior:"instant"}})')
            await pg.wait_for_timeout(70)
            y += 450
            H = max(H, await pg.evaluate('document.documentElement.scrollHeight'))
        await pg.evaluate('window.scrollTo({top:0,behavior:"instant"})')
        await pg.wait_for_timeout(wait)
        await pg.add_style_tag(content='*{transition:none!important;caret-color:transparent!important}')
        await pg.mouse.move(2, 2)
        r = await pg.evaluate(JS, {})
        r.update({'console': msgs, 'net': bad, 'page': name, 'w': w})
        (OUT / f'{name}@{w}.json').write_text(json.dumps(r, ensure_ascii=False), encoding='utf-8')
        await pg.close()
        print('ok', name, w, flush=True)


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--widths', default='1710,1440,1280,1000,390')
    ap.add_argument('--only', default='')
    ap.add_argument('--base', default='http://127.0.0.1:8766/')
    ap.add_argument('--wait', type=int, default=3600, help='ms po przewinięciu (animacje startowe Home trwają ok. 3 s)')
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    ps = strony()
    if a.only:
        ps = {k: v for k, v in ps.items() if k in a.only.split(',')}
    sem = asyncio.Semaphore(5)
    async with async_playwright() as p:
        try:
            b = await p.chromium.launch(channel='chrome', headless=True)
        except Exception:
            b = await p.chromium.launch(headless=True)
        ctx = await b.new_context()
        await asyncio.gather(*[jedna(ctx, a.base, n, rel, int(w), sem, a.wait) for n, rel in ps.items() for w in a.widths.split(',')])
        await b.close()


if __name__ == '__main__':
    asyncio.run(main())
