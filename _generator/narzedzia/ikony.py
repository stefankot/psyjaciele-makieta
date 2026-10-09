#!/usr/bin/env python3
"""ikony.py — generuje ikony.css z wybranych ikon Iconoir (MIT, assets/icons/iconoir/*.svg; https://iconoir.com).
Każda ikona to maska CSS (kolor = currentColor). Grubość linii: ikona w ramce 1,25 em ma kreskę 2,5 jedn. siatki 24 (= 0,13 em, jak
pochylone pismo Satoshi 700). Większe ramki dostają cieńszą kreskę (warianty poniżej), tak by kreska na ekranie równała się kresce tekstu obok.
Użycie (z katalogu makiety):  python3 _generator/narzedzia/ikony.py"""
import re, urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'assets' / 'icons' / 'iconoir'
BASE_SW = 2.5
# nazwa pliku → [(przyrostek, grubość w jedn. siatki 24)] — warianty dla dużych ramek
VARIANTS = {
    'info-circle': [('lg', 1.05)],          # 48 px obok tekstu 16 px (kreska ≈ 2,1 px)
    'warning-triangle': [('lg', 0.8)],      # 64 px (callout)
    'plus-circle': [('faq', 2.3)],          # 32 px obok pytania 24 px (kreska ≈ 3,1 px)
    'minus-circle': [('faq', 2.3)],
}


def data_uri(svg: str, sw: float) -> str:
    svg = re.sub(r'\s*stroke-width="[^"]*"', '', svg)
    svg = svg.replace('<svg ', f'<svg stroke-width="{sw:g}" ', 1)
    svg = svg.replace('currentColor', '#000')
    svg = re.sub(r'\s+', ' ', svg).strip()
    return 'url("data:image/svg+xml,' + urllib.parse.quote(svg, safe=" /:=\"'-.,;()") .replace('"', "'") + '")'

# Reguły ogólne (Home i podstrony): rozmiar, położenie i ruch ikon w miejscach dawnych glifów.
EXTRA = r"""
html body.book-type .type-arrow.ico{font-size:1em!important;margin-left:.25em;inline-size:1.25em;block-size:1.25em;vertical-align:-.28em;line-height:1;font-weight:inherit}
html body.book-type .site-header .site-nav a .type-arrow.ico,html body.book-type .foot-links a .type-arrow.ico{margin:0}
html body.book-type .hero-btn .ico{margin-left:.25em}
html.motion .type-arrow.ico{transition:translate .2s ease-out}
html.motion :is(a,button):is(:hover,:focus-visible) .type-arrow.ico-arrow-right{translate:4px 0}
html.motion :is(a,button):is(:hover,:focus-visible) .type-arrow.ico-arrow-up-right{translate:3px -3px}
html body.book-type .header-call .ico{inline-size:24px;block-size:24px;margin:0;vertical-align:middle}
html:not(.bar) body.book-type .site-header .header-call{display:none}
html body.book-type .services .tile h3::after{content:"";inline-size:1.1em;block-size:1.1em;font-size:inherit;font-weight:inherit;background:currentColor;-webkit-mask:var(--ico-arrow-up-right) center/contain no-repeat;mask:var(--ico-arrow-up-right) center/contain no-repeat;opacity:.65}
/* ikony pomocnicze nad tytułami kolumn (dojazd, przygotowanie, kontakt) — 32 px, kreska jak w tytule 24 px */
html body.book-type :is(#dojazd,#przygotowanie,#kontakt) .detail-columns > div > h3::before{content:"";display:block;inline-size:32px;block-size:32px;margin-block-end:var(--s2,13px);background:currentColor;-webkit-mask:var(--ic) center/contain no-repeat;mask:var(--ic) center/contain no-repeat}
html body.book-type #dojazd .detail-columns > div:nth-child(1){--ic:var(--ico-walking-l)}
html body.book-type #dojazd .detail-columns > div:nth-child(2){--ic:var(--ico-bus-l)}
html body.book-type #dojazd .detail-columns > div:nth-child(3){--ic:var(--ico-car-l)}
html body.book-type #kontakt .detail-columns > div:nth-child(1){--ic:var(--ico-map-pin-l)}
html body.book-type #kontakt .detail-columns > div:nth-child(2){--ic:var(--ico-phone-l)}
html body.book-type #kontakt .detail-columns > div:nth-child(3){--ic:var(--ico-clock-l)}
html body.book-type #przygotowanie .detail-columns > div:nth-child(1){--ic:var(--ico-page-l)}
html body.book-type #przygotowanie .detail-columns > div:nth-child(2){--ic:var(--ico-stats-report-l)}
html body.book-type #przygotowanie .detail-columns > div:nth-child(3){--ic:var(--ico-list-l)}
html body.book-type #przygotowanie .detail-columns > div:nth-child(4){--ic:var(--ico-chat-bubble-question-l)}
html body.book-type #przygotowanie .detail-columns > div:nth-child(5){--ic:var(--ico-shield-check-l)}
/* menu rozwijane: adres, godziny, telefon, e-mail */
html body.book-type .site-nav :is(.nav-address,.nav-hours){position:relative;padding-inline-start:32px}
html body.book-type .site-nav :is(.nav-address,.nav-hours)::before{content:"";display:inline-block;background:currentColor;-webkit-mask:var(--ic) center/contain no-repeat;mask:var(--ic) center/contain no-repeat}
html body.book-type .site-nav :is(.nav-address,.nav-hours)::before{position:absolute;inset-inline-start:0;inset-block-start:2px;inline-size:20px;block-size:20px}
html body.book-type .site-nav .nav-address{--ic:var(--ico-map-pin)}
html body.book-type .site-nav .nav-hours{--ic:var(--ico-clock)}
/* przyciski telefonu */
html body.book-type .hero-btn--ghost::before,html body.book-type a.booking-phone::before{content:"";display:inline-block;inline-size:1.25em;block-size:1.25em;margin-inline-end:.5em;vertical-align:-.28em;background:currentColor;-webkit-mask:var(--ico-phone) center/contain no-repeat;mask:var(--ico-phone) center/contain no-repeat}
"""


def main():
    out = ['/* ikony.css — GENEROWANY przez _generator/narzedzia/ikony.py z ikon Iconoir (MIT, assets/icons/iconoir/LICENSE-iconoir.txt). Nie edytuj ręcznie. */',
           '.ico{display:inline-block;flex:none;inline-size:1.25em;block-size:1.25em;vertical-align:-.28em;background:currentColor;'
           '-webkit-mask:var(--ico) center/contain no-repeat;mask:var(--ico) center/contain no-repeat}', ':root{']
    classes = []
    for f in sorted(SRC.glob('*.svg')):
        n = f.stem
        svg = f.read_text()
        out.append(f'--ico-{n}:{data_uri(svg, BASE_SW)};')
        classes.append(f'.ico-{n}{{--ico:var(--ico-{n})}}')
        out.append(f'--ico-{n}-l:{data_uri(svg, 2.3)};')
        for suf, sw in VARIANTS.get(n, []):
            out.append(f'--ico-{n}-{suf}:{data_uri(svg, sw)};')
    out.append('}')
    out += classes
    out.append(EXTRA.strip())
    (ROOT / 'ikony.css').write_text('\n'.join(out) + '\n')
    print(f'ikony.css: {len(classes)} ikon, {(ROOT / "ikony.css").stat().st_size // 1024} KB')


if __name__ == '__main__':
    main()
