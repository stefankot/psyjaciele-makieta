#!/usr/bin/env python3
# generated: psyjaciele-podstrony
"""audit.py — audyt przeglądarkowy (Playwright/Chromium): konsola, błędy JS, przepełnienie poziome, najmniejsza czcionka, osie siatki, Rialto, zrzuty.

Użycie: python3 audit.py [--widths 1440,1024,768,390] [--shots] [slug …]   (serwer statyczny na :8765 w katalogu MAKIETA)
Wynik: _generator/wyniki/_audyt.json (+ zrzuty JPEG w _generator/wyniki/_zrzuty/ przy --shots)
"""
import argparse
import asyncio
import json
import sys
from pathlib import Path

from playwright.async_api import async_playwright

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import strony  # noqa: E402

ROOT = HERE.parents[1]
BASE = 'http://127.0.0.1:8765/'
OUT = {'uslugi-weterynaryjne': 'uslugi-weterynaryjne/index.html', 'zespol': 'zespol/index.html',
       'polityka-prywatnosci': 'polityka-prywatnosci/index.html'}

JS = r'''() => {
  const vw = document.documentElement.clientWidth;
  const over = [];
  for (const e of document.querySelectorAll('body *')) {
    const r = e.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;
    const cs = getComputedStyle(e);
    if (cs.position === 'fixed') continue;
    if (r.right > vw + 1 && !e.closest('.ruled-table, .visually-hidden, [aria-hidden=true], .booking-pets, .halo, .halo-dot, .reviews-illustration, .poster-media, svg, .footer-logo, .social-promo')) {
      over.push((e.tagName + '.' + (e.className && e.className.baseVal === undefined ? e.className : '')).slice(0, 60) + ' r=' + Math.round(r.right));
      if (over.length > 5) break;
    }
  }
  let small = [];
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let n;
  while ((n = walker.nextNode())) {
    const t = n.textContent.trim();
    if (!t) continue;
    const p = n.parentElement;
    if (!p || p.closest('script,style,noscript,.visually-hidden,svg')) continue;
    const cs = getComputedStyle(p);
    if (cs.display === 'none' || cs.visibility === 'hidden') continue;
    const fs = parseFloat(cs.fontSize);
    if (fs < 15.99) small.push(fs.toFixed(1) + ' ' + p.tagName + '.' + (typeof p.className === 'string' ? p.className : '') + ' «' + t.slice(0, 24) + '»');
  }
  return { scrollW: document.documentElement.scrollWidth, vw, over, small: small.slice(0, 8), nSmall: small.length,
           errs: window.__podstronyErrors || null, h1: document.querySelectorAll('h1').length, h: document.documentElement.scrollHeight };
}'''

AXES_JS = r'''() => {
  // siatka: 12 kolumn, rynna --gap; osie: kol. 1, kol. 5 (artykuł), kol. 7 (hero: lead); zdjęcia w artykule 4 albo 8 kolumn
  const bad = [];
  const rootCS = getComputedStyle(document.body);
  const g = parseFloat(rootCS.getPropertyValue('--gap')) || 32;
  const w0 = document.querySelector('main .wrap');
  if (!w0) return { bad, rialto: 0 };
  const wr = w0.getBoundingClientRect();
  const c = (wr.width - 11 * g) / 12;
  const colStart = n => wr.left + (n - 1) * (c + g);
  const span = n => n * c + (n - 1) * g;
  const near = (a, b) => Math.abs(a - b) <= 1.5;
  const name = e => (e.tagName + '.' + (typeof e.className === 'string' ? e.className.split(' ')[0] : '')).slice(0, 40);
  const hero = document.querySelector('#poczatek .poster-grid');
  if (hero) {
    const h = hero.querySelector('.poster-heading'), cp = hero.querySelector('.poster-copy'), art = hero.querySelector('.poster-art');
    if (h && !near(h.getBoundingClientRect().left, colStart(1))) bad.push('hero tytuł nie na osi 1');
    if (cp && !near(cp.getBoundingClientRect().left, colStart(7))) bad.push('hero lead nie na osi 7');
    if (art && !near(art.getBoundingClientRect().left, colStart(7))) bad.push('hero ilustracja nie na osi 7');
    if (art && !near(art.getBoundingClientRect().width, span(6))) bad.push('hero ilustracja nie ma 6 kolumn: ' + Math.round(art.getBoundingClientRect().width));
  }
  document.querySelectorAll('.page-columns > section > .wrap > *').forEach(e => {
    const r = e.getBoundingClientRect();
    if (r.width === 0 || e.matches('.visually-hidden, .ruled-table.visually-hidden')) return;
    if (!near(r.left, colStart(5))) bad.push('artykuł nie na osi 5: ' + name(e) + ' x=' + Math.round(r.left));
    if (!e.matches('p, .book-prose, .contact-note, .callout, .legal-prose') && !near(r.right, wr.right)) bad.push('artykuł nie kończy się na prawym brzegu: ' + name(e) + ' r=' + Math.round(r.right));
  });
  document.querySelectorAll('.page-columns .photo-frame, .page-columns .section-header > .poster-art').forEach(e => {
    const r = e.getBoundingClientRect();
    if (r.width === 0 || e.closest('.ab-art')) return;   // kafel baneru: 2 × połowa 8 kolumn, granica na środku rynny
    if (!(near(r.width, span(4)) || near(r.width, span(8)))) bad.push('obraz nie ma 4 ani 8 kolumn: ' + name(e) + ' w=' + Math.round(r.width));
  });
  document.querySelectorAll('.page-columns :is(h2, .toc-rail)').forEach(e => { /* tytuły: lewy brzeg = oś 5 */
    const r = e.getBoundingClientRect(); if (e.matches('.toc-rail') || r.width === 0) return;
    if (!near(r.left, colStart(5)) && !e.closest('.profile, .rail-body, .join-banner')) bad.push('tytuł nie na osi 5: ' + e.textContent.trim().slice(0, 30) + ' x=' + Math.round(r.left));
  });
  const ts = document.querySelector('.toc-sticky');
  if (ts && ts.getBoundingClientRect().width > 0 && !near(ts.getBoundingClientRect().left, colStart(1))) bad.push('spis treści nie na osi 1');
  // Rialto: ma nie występować w tekście widocznym
  let rialto = 0;
  const wk = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n;
  while ((n = wk.nextNode())) { const t = n.textContent.trim(); if (!t) continue; const p = n.parentElement; if (!p || p.closest('script,style,noscript,.visually-hidden,svg')) continue;
    const cs = getComputedStyle(p); if (cs.display === 'none') continue; if (!p.closest('.psy') && /rialto/i.test(cs.fontFamily)) rialto++; }
  return { bad: bad.slice(0, 12), rialto };
}'''


async def one(ctx, slug, w, shots, sem, res):
    async with sem:
        pg = await ctx.new_page()
        await pg.set_viewport_size({'width': w, 'height': 900})
        msgs = []
        pg.on('console', lambda m: msgs.append(f'{m.type}: {m.text}') if m.type in ('error', 'warning') else None)
        pg.on('pageerror', lambda e: msgs.append(f'pageerror: {e}'))
        bad = []
        pg.on('response', lambda r: bad.append(f'{r.status} {r.url}') if r.status >= 400 else None)
        rel = OUT.get(slug) or f'uslugi-weterynaryjne/{slug}/index.html'
        await pg.goto(BASE + rel, wait_until='networkidle')
        H = await pg.evaluate('document.documentElement.scrollHeight')
        y = 0
        while y < H:
            await pg.evaluate(f'window.scrollTo(0,{y})')
            await pg.wait_for_timeout(60)
            y += 600
        await pg.evaluate('window.scrollTo(0,0)')
        await pg.wait_for_timeout(500)
        r = await pg.evaluate(JS)
        ax = await pg.evaluate(AXES_JS) if w >= 1001 else {'bad': [], 'rialto': await pg.evaluate("()=>{let k=0;const wk=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while((n=wk.nextNode())){const t=n.textContent.trim();if(!t)continue;const p=n.parentElement;if(!p||p.closest('script,style,noscript,.visually-hidden,svg'))continue;const cs=getComputedStyle(p);if(cs.display==='none')continue;if(/rialto/i.test(cs.fontFamily))k++}return k}")}
        r['axes'] = ax['bad']
        r['rialto'] = ax['rialto']
        r['console'] = [m for m in msgs if 'Failed to load resource' not in m]
        r['http_bad'] = [b for b in bad if '/assets/podstrony/' not in b]
        r['ph_404'] = len([b for b in bad if '/assets/podstrony/' in b])
        if shots:
            d = ROOT / '_generator' / 'wyniki' / '_zrzuty'
            d.mkdir(exist_ok=True)
            await pg.screenshot(path=str(d / f'{slug}-{w}.jpg'), full_page=True, type='jpeg', quality=55)
        res[f'{slug}@{w}'] = r
        await pg.close()


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('slugs', nargs='*')
    ap.add_argument('--widths', default='1440,1280,1024,768,390')
    ap.add_argument('--shots', action='store_true')
    a = ap.parse_args()
    slugs = a.slugs or strony.ALL_SLUGS
    res = {}
    sem = asyncio.Semaphore(4)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context()
        await asyncio.gather(*[one(ctx, s, int(w), a.shots, sem, res) for s in slugs for w in a.widths.split(',')])
        await b.close()
    (ROOT / '_generator' / 'wyniki' / '_audyt.json').write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
    for k in sorted(res):
        r = res[k]
        flags = []
        if r['scrollW'] > r['vw'] + 1:
            flags.append(f'OVERFLOW {r["scrollW"]}>{r["vw"]}')
        if r['over']:
            flags.append('over:' + '; '.join(r['over'][:3]))
        if r['console']:
            flags.append('console:' + ' | '.join(r['console'][:2]))
        if r['http_bad']:
            flags.append('http:' + ' | '.join(r['http_bad'][:2]))
        if r['errs']:
            flags.append('js:' + ' | '.join(r['errs']))
        if r['h1'] != 1:
            flags.append(f'h1={r["h1"]}')
        if r['nSmall']:
            flags.append(f'small16={r["nSmall"]}')
        if r.get('axes'):
            flags.append('axes:' + ' | '.join(r['axes'][:4]))
        if r.get('rialto'):
            flags.append(f'rialto={r["rialto"]}')
        print(('!! ' if flags else 'ok ') + k, ' ; '.join(flags))


asyncio.run(main())
