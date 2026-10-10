#!/usr/bin/env python3
# generated: psyjaciele-podstrony
"""build.py — generator podstron Psyjaciół (idempotentny; zapisuje strony usług, zespołu i polityki w korzeniu makiety, a pliki pomocnicze w _generator/wyniki/).

Użycie (z dowolnego katalogu):
  python3 _generator/narzedzia/build.py [--only slug[,slug…]] [--bake] [--check] [--dry-run] [--root MAKIETA]
"""
import argparse
import html as _html
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import infografiki  # noqa: E402
import nbsp  # noqa: E402
import psy  # noqa: E402

import bloki as B  # noqa: E402
import home as H  # noqa: E402
import obrazy  # noqa: E402
import manifest  # noqa: E402
import plany  # noqa: E402
import mobile_skala  # noqa: E402
import strony  # noqa: E402

MARK = '<!-- generated: psyjaciele-podstrony -->'
CSS_V = '155'
JS_V = '28'


def esc(s):
    return _html.escape(s, quote=True)


# ---------------------------------------------------------------------------
# JSON-LD
# ---------------------------------------------------------------------------
def jsonld(home, pages, P, crumbs, faq):
    D = H.DOMENA
    url = pages.prod(P.slug)
    vet = home.jsonld_vet
    vet_id = vet['@id']
    site_id = home.jsonld_website['@id']
    graph = [dict(vet), dict(home.jsonld_website)]
    bl = {'@type': 'BreadcrumbList', '@id': url + '#breadcrumb',
          'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n, **({'item': u} if u else {})}
                              for i, (n, u) in enumerate(crumbs)]}
    wp = {'@type': 'WebPage', '@id': url + '#webpage', 'url': url, 'name': P.src.title, 'inLanguage': 'pl-PL',
          'isPartOf': {'@id': site_id}, 'about': {'@id': vet_id}, 'breadcrumb': {'@id': bl['@id']}}
    if P.src.desc:
        wp['description'] = P.src.desc
    graph += [wp, bl]
    if P.slug in strony.SLUGS_USLUGI:
        graph.append({'@type': 'Service', '@id': url + '#usluga', 'name': P.crumb_label, 'serviceType': P.crumb_label,
                      'provider': {'@id': vet_id}, 'areaServed': vet['areaServed'], 'url': url})
    if faq and len(faq) >= 3:
        ents = []
        for _id, q, a_html in faq:
            a = B.plain(a_html)
            ents.append({'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}})
        graph.append({'@type': 'FAQPage', '@id': url + '#faq', 'mainEntity': ents})
    return json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, indent=1)


# ---------------------------------------------------------------------------
# dokument
# ---------------------------------------------------------------------------
def head_html(home, pages, P, ld):
    rw = P.rw
    R = rw.root
    s = P.src
    url = pages.prod(P.slug)
    title = esc(re.sub(r'\s+', ' ', s.title))
    desc = esc(s.desc)
    parts = [MARK, '<meta charset="utf-8">', '<meta name="viewport" content="width=device-width, initial-scale=1">',
             '<link rel="icon" href="data:,">',  # makieta bez faviconu: puste „data:,” oszczędza żądania /favicon.ico (404 w konsoli)
             f'<title>{title}</title>']
    if desc:
        parts.append(f'<meta name="description" content="{desc}">')
    parts.append(f'<meta name="robots" content="{H.ROBOTS}">')
    parts.append(f'<script src="{R}{home.head_sync_script}"></script>')
    parts.append(f'<link rel="canonical" href="{url}">')
    parts += ['<meta property="og:type" content="website">', '<meta property="og:locale" content="pl_PL">',
              '<meta property="og:site_name" content="Psyjaciele">', f'<meta property="og:title" content="{title}">']
    if desc:
        parts.append(f'<meta property="og:description" content="{desc}">')
    parts += [f'<meta property="og:url" content="{url}">', '<meta name="twitter:card" content="summary">',
              f'<meta name="twitter:title" content="{title}">']
    if desc:
        parts.append(f'<meta name="twitter:description" content="{desc}">')
    for pl in home.head_preloads:
        parts.append(rw.fragment(pl))
    for href in home.head_stylesheets:
        if href.startswith('mobile-skala'):
            continue
        parts.append(f'<link rel="stylesheet" href="{rw.home_url(href)}">')
    parts.append(f'<link rel="stylesheet" href="{R}podstrony.css?v={CSS_V}">')
    parts.append(f'<link rel="stylesheet" href="{R}mobile-skala-podstrony.css?v={CSS_V}">')
    parts.append(f'<script type="application/ld+json">{ld}</script>')
    return '\n'.join(parts)


def header_html(home, P):
    rw = P.rw
    h = rw.fragment(home.header_raw, frag_to_home=True)
    hub = rw.page_link('uslugi-weterynaryjne')
    team = rw.page_link('zespol')
    cur_u = ''
    cur_z = ''
    if P.slug == 'uslugi-weterynaryjne':
        cur_u = ' aria-current="page"'
    elif P.slug in strony.SLUGS_USLUGI:
        cur_u = ' aria-current="true"'
    if P.slug == 'zespol':
        cur_z = ' aria-current="page"'
    h = re.sub(r'<a href="[^"]*#uslugi">Usługi</a>', f'<a href="{hub}"{cur_u}>Usługi</a>', h)
    h = re.sub(r'<a href="[^"]*#zespol">Zespół</a>', f'<a href="{team}"{cur_z}>Zespół</a>', h)
    return h


def body_scripts(home, rw):
    R = rw.root
    out = []
    for src, _d in home.body_scripts:
        name = src.split('?')[0].split('/')[-1]
        if name in ('minimal-nowa.js', 'minimal.js'):
            continue
        if name == 'pet-photos.js':
            q = src.split('?', 1)[1] if '?' in src else ''
            out.append(f'<script src="{R}pet-photos.js{"?" + q if q else ""}" defer></script>')
            continue
        out.append(f'<script src="{rw.home_url(src)}" defer></script>')
    out.append(f'<script src="{R}podstrony.js?v={JS_V}" defer></script>')
    return '\n'.join(out)


def render(home, pages, slug, root):
    P = strony.PB(home, pages, slug, root)
    plany.PLANS[slug](P)
    main = P.finish()
    rw = P.rw
    if 'id="kontakt"' not in main:
        main = main.replace('href="#kontakt"', f'href="{rw.home_link()}#kontakt"')
    ctx = P.ctx
    crumbs = [('Strona główna', H.DOMENA + '/')]
    if slug in strony.SLUGS_USLUGI:
        crumbs.append(('Usługi', pages.prod('uslugi-weterynaryjne')))
    crumbs.append((P.crumb_label, None))
    ld = jsonld(home, pages, P, crumbs, P.faq_data)
    svg = rw.fragment(home.svg_filters_raw) if ctx.svg_needed else ''
    sticky = B.sticky_cta(ctx) if slug != 'polityka-prywatnosci' else ''
    doc = f'''<!doctype html>
<html lang="pl"><head>
{head_html(home, pages, P, ld)}
</head>
<body class="book-type subpage" data-root="{rw.root}" data-page="{slug}">
<a class="skip" href="#main">Przejdź do treści</a>
<div class="header-backdrop" aria-hidden="true"></div>{header_html(home, P)}
<main id="main">
{main}
</main>
{rw.fragment(home.footer_raw, frag_to_home=True)}
{svg}
{sticky}
{body_scripts(home, rw)}
</body></html>
'''
    return doc, P


def simple_head(home, rw, title, desc):
    R = rw.root
    parts = [MARK, '<meta charset="utf-8">', '<meta name="viewport" content="width=device-width, initial-scale=1">', '<link rel="icon" href="data:,">',
             f'<title>{esc(title)}</title>', f'<meta name="description" content="{esc(desc)}">',
             f'<meta name="robots" content="{H.ROBOTS}">', f'<script src="{R}{home.head_sync_script}"></script>']
    for pl in home.head_preloads:
        parts.append(rw.fragment(pl))
    for href in home.head_stylesheets:
        if href.startswith('mobile-skala'):
            continue
        parts.append(f'<link rel="stylesheet" href="{rw.home_url(href)}">')
    parts.append(f'<link rel="stylesheet" href="{R}podstrony.css?v={CSS_V}">')
    parts.append(f'<link rel="stylesheet" href="{R}mobile-skala-podstrony.css?v={CSS_V}">')
    return '\n'.join(parts)


class _Dummy:
    def __init__(self, slug, rw):
        self.slug, self.rw = slug, rw


def render_overview(home, pages, rows):
    """podstrony/index.html — przegląd wygenerowanych stron i plików pomocniczych (noindex)."""
    rw = H.Rewriter(pages, 'index')
    P = _Dummy('index', rw)
    lab = home.label_for
    trs = []
    for slug, label, kind in rows:
        href = rw.page_link(slug)
        trs.append(f'<tr><th scope="row"><a href="{href}">{esc(label)}</a></th><td data-label="Rodzaj">{kind}</td>'
                   f'<td data-label="Adres"><span>{href}</span></td><td class="row-go" aria-hidden="true">→</td></tr>')
    tools = [('_bloki.html', 'Katalog bloków N1–N27 w czterech paletach'), ('_obrazy.md', 'Lista obrazów do wgrania (czytelna)'),
             ('OBRAZY-PROMPTY.md', 'Prompty EN do generowania obrazów'), ('_obrazy.json', 'Manifest obrazów (źródło prawdy)'),
             ('_raport.md', 'Raport z weryfikacji i lista rzeczy niesprawdzonych')]
    lis = ''.join(f'<li><a href="{f}">{f}</a> — {d}</li>' for f, d in tools)
    main = (f'<section id="poczatek" class="hero page-hero is-plain" data-palette="{lab("hero")}" aria-labelledby="tytul-strony">'
            '<div class="wrap section-stack"><div class="poster-grid"><div class="poster-heading"><span class="kicker">Makieta · noindex</span>'
            '<h1 id="tytul-strony"><em>Podstrony Psyjaciół</em></h1></div>'
            '<div class="poster-copy"><p>Przegląd wygenerowanych podstron makiety oraz plików pomocniczych. Strona techniczna, nie do indeksowania.</p></div></div></div></section>'
            f'<section class="services" data-palette="{lab("services")}" aria-labelledby="strony"><div class="wrap section-stack">'
            '<header class="section-head"><h2 id="strony"><em>Strony</em></h2></header>'
            '<div class="ruled-table is-directory" role="region" tabindex="0" aria-label="Lista podstron"><table><thead><tr>'
            '<th scope="col">Strona</th><th scope="col">Rodzaj</th><th scope="col">Adres</th><th scope="col"><span class="visually-hidden">Przejdź</span></th></tr></thead>'
            f'<tbody>{"".join(trs)}</tbody></table></div></div></section>'
            f'<section class="arrival" data-palette="{lab("arrival")}" aria-labelledby="pliki"><div class="wrap section-stack">'
            '<header class="section-head"><h2 id="pliki"><em>Pliki pomocnicze</em></h2></header>'
            f'<ul class="ruled-list">{lis}</ul></div></section>')
    head = simple_head(home, rw, 'Podstrony Psyjaciół — przegląd', 'Przegląd wygenerowanych podstron makiety.')
    return f"""<!doctype html>
<html lang="pl"><head>
{head}
</head>
<body class="book-type subpage" data-root="{rw.root}" data-page="index">
<a class="skip" href="#main">Przejdź do treści</a>
<div class="header-backdrop" aria-hidden="true"></div>{header_html(home, P)}
<main id="main">
{main}
</main>
{rw.fragment(home.footer_raw, frag_to_home=True)}
{body_scripts(home, rw)}
</body></html>
"""


def write(path: Path, content: str, dry=False):
    if path.suffix == '.html':
        content = infografiki.inject(path.parent.name, content)   # infografiki po nagłówkach wskazanych sekcji
        content = psy.wrap(content)   # słowo „Psyjaciele” zawsze krojem Rialto (.psy)
        content = nbsp.fix(content)   # twarda spacja po a/i/o/u/w/z i przed pauzą (bez „sierotek” na końcu wiersza)
    if path.exists():
        old = path.read_text(encoding='utf-8')
        if 'generated: psyjaciele-podstrony' not in old[:400] and '"_generated": "psyjaciele-podstrony"' not in old[:400]:
            alt = path.parents[len(path.parents) - 1]
            raise SystemExit(f'ODMOWA: {path} istnieje i nie ma znacznika generatora (R11)')
        if old == content:
            return False
    if not dry:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
    return True


def main():
    mobile_skala.generate()
    ap = argparse.ArgumentParser()
    ap.add_argument('--only')
    ap.add_argument('--root', default=str(HERE.parents[1]))
    ap.add_argument('--bake', action='store_true')
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    root = Path(a.root)
    home = H.Home(root)
    slugs = a.only.split(',') if a.only else [s for s in strony.ALL_SLUGS if s in plany.PLANS]
    all_slugs = [p.stem for p in sorted((root / '_generator' / 'tresci-podstron' / 'czyste').glob('*.html'))]
    pages = H.Pages(all_slugs)
    _unused_manifest = {}
    results = {}
    titles = {}
    for s in slugs:
        doc, P = render(home, pages, s, root)
        titles[s] = P.crumb_label
        out = root / pages.out[s]
        changed = write(out, doc, a.dry_run)
        results[s] = {'file': pages.out[s], 'changed': changed, 'roles': P.roles_used, 'uses': sorted(P.ctx.uses),
                      'placeholders': P.ctx.placeholders, 'green': P.green_count}
        print(f'{"zapisano" if changed else "bez zmian"}  {pages.out[s]}  [{len(doc)//1024} KB, ph={len(P.ctx.placeholders)}, palety={len(set(P.roles_used))}]')
    if not a.only:
        out_dir = root / '_generator' / 'wyniki'
        rows, unused = manifest.collect(results)
        for name, body in (('_obrazy.json', manifest.to_json(rows)), ('_obrazy.md', manifest.to_md(rows)),
                           ('OBRAZY-PROMPTY.md', manifest.to_prompts(rows))):
            ch = write(out_dir / name, body, a.dry_run)
            print(f'{"zapisano" if ch else "bez zmian"}  _generator/wyniki/{name}  [{len(rows)} obrazów]')
        if unused:
            print('UWAGA: wpisy rejestru bez użycia na stronach:', ', '.join(unused))
        lst = [('index', 'Przegląd', 'przegląd')]
        for s in slugs:
            lst.append((s, titles[s], 'hub' if s == 'uslugi-weterynaryjne' else ('usługa' if s in strony.SLUGS_USLUGI else 'strona')))
        ch = write(root / pages.out['index'], render_overview(home, pages, lst[1:]), a.dry_run)
        print(f'{"zapisano" if ch else "bez zmian"}  {pages.out["index"]}')
        import bloki_demo
        ch = write(out_dir / '_bloki.html', bloki_demo.render(home, pages, root, sys.modules[__name__]), a.dry_run)
        print(f'{"zapisano" if ch else "bez zmian"}  _generator/wyniki/_bloki.html')
    if a.bake:
        print('--bake: nie zaimplementowano; podmiana obrazów działa w przeglądarce (podstrony.js).')
    (HERE / '_stan.json').write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding='utf-8')


if __name__ == '__main__':
    main()
