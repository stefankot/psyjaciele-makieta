# generated: psyjaciele-podstrony
"""bloki.py — czyste funkcje renderujące bloki (H* z home, N* nowe). Wejście: dane ze źródła, wyjście: HTML.

Nic tu nie wpisuje zdań treści: wszystkie teksty pochodzą ze źródła (węzły bs4) albo z białej listy UI (R4.3).
"""
import html as _html
import re

from bs4 import BeautifulSoup, Tag, NavigableString

from home import Raw, strip_shy, text_of, DOMENA
from zrodlo import runin, table_rows

NB = ' '
ARROW_IN = '<span class="type-arrow ico ico-arrow-right" aria-hidden="true"></span>'
ARROW_OUT = '<span class="type-arrow ico ico-arrow-up-right" aria-hidden="true"></span>'


# ----------------------------------------------------------------------------
# typografia, tytuły
# ----------------------------------------------------------------------------
def nbsp_html(s):
    """Spacja niełamliwa po jednoliterowych wyrazach i skrótach (poza znacznikami) — R4.7."""
    parts = re.split(r'(<[^>]+>)', s)
    out = []
    for p in parts:
        if p.startswith('<'):
            out.append(p)
            continue
        p = re.sub(r'(?<![\w])([aiouwzAIOUWZ]) ', r'\1' + NB, p)
        p = re.sub(r'\b(lek\.) (wet\.)', r'\1' + NB + r'\2', p)
        p = re.sub(r'\b(lek\. wet\.|ul\.|lok\.) ', lambda m: m.group(1) + NB, p)
        p = re.sub(r'(\d) (zł|min|godz|kg|mg|ml|r\.)\b', r'\1' + NB + r'\2', p)
        out.append(p)
    return ''.join(out)


def plain(s):
    return re.sub(r'\s+', ' ', _html.unescape(re.sub(r'<[^>]+>', '', strip_shy(s)))).strip()


def esc(s):
    return _html.escape(s, quote=True)


_STOP = {'o', 'w', 'z', 'i', 'u', 'a', 'do', 'na', 'po', 'od', 'za', 'ze', 'we', 'że', 'to', 'co', 'czy', 'jak'}


def split_title(text, forced=None):
    """Zwraca (roman, hidden, em) albo None (→ wzorzec (a): całość w <em>)."""
    t = plain(text)
    words = t.split()
    if forced:
        r, e = forced.split('|')
        sep = ''
        m = re.search(re.escape(r) + r'(\s*[—–:,]\s*|\s+)' + re.escape(e), t)
        if m and m.group(1).strip():
            sep = m.group(1)
        return r, sep, e
    if len(words) <= 3 or len(t) <= 28:
        return None
    for sepc in (' — ', ' – '):
        if sepc in t:
            a, b = t.split(sepc, 1)
            return a, sepc, b
    m = re.match(r'^([^:]{6,}?):\s+(.+)$', t)
    if m:
        return m.group(1), ': ', m.group(2)
    m = re.match(r'^([^,]{4,}?),\s+(.+)$', t)
    if m and len(m.group(1).split()) <= 4:
        return m.group(1), ', ', m.group(2)
    n = len(words)
    k = 2 if n <= 5 else n // 2
    while k < n - 1 and words[k - 1].lower() in _STOP:
        k += 1
    if k >= n:
        return None
    return ' '.join(words[:k]), ' ', ' '.join(words[k:])


def title_inner(text_html, forced=None, nbsp=True):
    """Wnętrze h1/h2: zawsze jeden napis (Satoshi, jeden rozmiar) — tytułów się nie rozbija na człony (polecenie użytkownika 8.10.2026).
    Słowa nigdy nie są zmieniane; `forced` zachowany tylko dla zgodności wywołań."""
    return nbsp_html(text_html) if nbsp else text_html


def heading(level, text_html, hid=None, forced=None, cls=None):
    idattr = f' id="{hid}"' if hid else ''
    c = f' class="{cls}"' if cls else ''
    return f'<h{level}{idattr}{c}>{title_inner(text_html, forced)}</h{level}>'


def kicker(text):
    return f'<span class="kicker">{text}</span>'


class Ctx:
    """Stan jednej strony podczas renderowania."""

    def __init__(self, home, rw, src, slug, label_forced=None):
        self.home = home
        self.rw = rw
        self.src = src
        self.slug = slug
        self.ink_n = 0
        self.ids = set()
        self.placeholders = []
        self.sections = []          # (role, class_str, id, html, aria)
        self.forced_titles = label_forced or {}
        self.used_nodes = set()
        self.uses = set()           # typy bloków użytych na stronie (V12)
        self.svg_needed = False

    def use(self, *names):
        self.uses.update(names)

    def uid(self, base):
        b = base
        n = 2
        while b in self.ids:
            b = f'{base}-{n}'
            n += 1
        self.ids.add(b)
        return b

    def ink_filter(self):
        self.ink_n += 1
        fid = f'ink-{self.slug[:18]}-{self.ink_n}'
        svg = (f'<svg width="0" height="0" aria-hidden="true" style="position:absolute"><filter id="{fid}" '
               'color-interpolation-filters="sRGB"><feColorMatrix type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 '
               '-.2126 -.7152 -.0722 0 1"/><feComposite in2="SourceGraphic" operator="in" result="lines"/>'
               '<feFlood flood-color="var(--ink)"/><feComposite in2="lines" operator="in"/></filter></svg>')
        return fid, svg

    def title_split(self, sid):
        return self.forced_titles.get(sid)


# ----------------------------------------------------------------------------
# szkielet sekcji
# ----------------------------------------------------------------------------
def section(ctx, cls, inner, sid=None, aria=None, label=None, extra=''):
    lab = label if label is not None else ctx.home.label_for(cls)
    a = [f'class="{cls}"']
    if lab:
        a.append(f'data-palette="{lab}"')
    else:
        a.append('data-palette')
    if sid:
        a.insert(0, f'id="{sid}"')
    if aria:
        a.append(f'aria-labelledby="{aria}"')
    return f'<section {" ".join(a)}{extra}><div class="wrap section-stack">{inner}</div></section>'


# ----------------------------------------------------------------------------
# N2 breadcrumb, N3 fact-strip, N1 page-hero
# ----------------------------------------------------------------------------
def breadcrumb(ctx, items):
    """items: [(label, href|None)] — ostatnia pozycja bez linku."""
    ctx.use('breadcrumb')
    lis = []
    for i, (lab, href) in enumerate(items):
        if i == len(items) - 1:
            lis.append(f'<li aria-current="page">{lab}</li>')
        else:
            lis.append(f'<li><a href="{href}">{lab}</a></li>')
    return f'<nav class="breadcrumb" aria-label="Okruszki"><ol>{"".join(lis)}</ol></nav>'


def fact_strip(ctx, pairs, page_text):
    ctx.use('fact-strip')
    norm = lambda s: re.sub(r'\s+', ' ', s.replace(NB, ' ')).strip()
    t = norm(page_text)
    cells = []
    for dt, dd in pairs:
        assert norm(dd) in t, f'fact-strip: „{dd}” nie jest podciągiem tekstu strony ({ctx.slug})'
        cells.append(f'<div><dt>{dt}</dt><dd>{dd}</dd></div>')
    return f'<dl class="fact-strip">{"".join(cells)}</dl>'


def hero_actions(ctx, cta):
    """Przyciski wyprowadzone z linków akapitu cta-wizyta (§00.6, N1)."""
    nap = ctx.home.nap
    wet = None
    tel = None
    if cta is not None:
        for a in cta.find_all('a'):
            h = a.get('href', '')
            if 'wettermin' in h:
                wet = h
            if h.startswith('tel:'):
                tel = h
    tel = tel or ('tel:' + nap['tel'])
    tel_txt = f'Zadzwoń: {nap["tel_disp"].replace(" ", NB)}'
    parts = []
    if wet:
        parts.append(f'<a class="hero-btn hero-btn--solid" href="{wet}" rel="noopener">Umów wizytę{NB}<span class="ico ico-arrow-up-right" aria-hidden="true"></span></a>')
        parts.append(f'<a class="hero-btn hero-btn--ghost" href="{tel}">{tel_txt}</a>')
    else:
        parts.append(f'<a class="hero-btn hero-btn--solid" href="{tel}">{tel_txt}</a>')
    parts.append('<a class="hero-status" data-hero-status href="#kontakt" hidden></a>')
    return f'<div class="hero-actions">{"".join(parts)}</div>'


_ROOT = __import__('pathlib').Path(__file__).resolve().parents[2]


def prefer_avif(img):
    """Jeśli obok pliku (png/jpg/webp) leży wersja .avif, użyj jej (konwersja: avif.py)."""
    a = re.sub(r'\.(png|jpe?g|webp)$', '.avif', img, flags=re.I)
    return a if a != img and (_ROOT / a).exists() else img


def art_figure(ctx, img, ratio='1', alt='', mask=False, eager=False, w=None, h=None):
    """T1 (filtr barwiący atramentem sekcji) albo T2 (maska) — hero i kafle."""
    rw = ctx.rw
    img = prefer_avif(img)
    if mask:
        return (f'<figure class="section-illustration poster-art" style="--art-ratio:{ratio}">'
                f'<span class="art" aria-hidden="true" style="--art:url({img})"></span></figure>')
    fid, svg = ctx.ink_filter()
    wh = f' width="{w}" height="{h}"' if w else ''
    lazy = '' if eager else ' loading="lazy"'
    return (f'<figure class="section-illustration poster-art" style="--art-ratio:{ratio}">{svg}'
            f'<img src="{rw.asset(img)}" alt="{esc(alt)}"{wh}{lazy} decoding="async" '
            f'style="width:100%;height:100%;object-fit:contain;filter:url(#{fid})"></figure>')


def back_link(href, label):
    return (f'<a class="back-link" href="{href}" aria-label="{esc(label)}"><svg viewBox="0 0 24 24" width="48" height="48" aria-hidden="true" focusable="false">'
            '<path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z"/><path d="M16 12H8M8 12L11.5 15.5M8 12L11.5 8.5"/></svg></a>')


def page_hero(ctx, crumbs, kick, h1, lead_nodes, cta, art, facts, hid='h1-strony', forced=None, no_art=False, back=None):
    """Hero w układzie Off→Grid: tytuł (kol. 1–6) i przyciski pod nim, lead w kol. 7–12, ilustracja pod przyciskami (kol. 1–6).
    Zdanie „Umów wizytę: …” usunięte (powtarzało przyciski)."""
    ctx.use('page-hero', 'poster-grid')
    h1html = f'<h1 id="{hid}">{title_inner(h1, forced)}</h1>'
    leads = ''.join(f'<p>{n.decode_contents()}</p>' for n in lead_nodes)
    actions = hero_actions(ctx, cta)
    fs = facts or ''
    ctx.use('back-link')
    title = f'<div class="title-row">{back_link(*back)}{h1html}</div>' if back else h1html
    heading_html = (f'<div class="poster-heading">{breadcrumb(ctx, crumbs) if crumbs else ""}{kicker(kick) if kick else ""}{title}</div>')
    artf = '' if no_art else art
    copy = f'<div class="poster-copy">{leads}</div>' if leads else ''
    cls = 'hero page-hero' + (' is-plain' if no_art else '')
    inner = f'<div class="poster-grid">{heading_html}{copy}{actions}{artf}</div>{fs}'
    return section(ctx, cls, inner, sid='poczatek', aria=hid, label=ctx.home.label_for('hero'))


# ----------------------------------------------------------------------------
# N4 toc-index
# ----------------------------------------------------------------------------
def toc_index(ctx, toc):
    """N4: spis treści bez numeracji; podpunkty tylko dla rozdziałów nie-FAQ (pytania są w samej sekcji FAQ)."""
    ctx.use('toc-index')
    entries = []
    for e in toc:
        subs = ''
        if e['subs'] and not re.search(r'najczęstsze pytania', e['text'], re.I):
            subs = '<ul>' + ''.join(f'<li><a href="#{s["id"]}">{s["text"]}</a></li>' for s in e['subs']) + '</ul>'
        entries.append(f'<div class="toc-entry"><a class="toc-link" href="#{e["id"]}">{e["text"]}</a>{subs}</div>')
    return (f'<nav class="toc-index" aria-labelledby="toc-title"><p class="kicker" id="toc-title">Spis treści</p>'
            f'<div class="toc-grid">{"".join(entries)}</div></nav>')


def toc_rail(ctx, toc):
    """Spis treści jako lewa, przyklejona szpalta (4 kolumny): wiersze oddzielone kreskami, podpunkty z kreskami i wcięciem,
    strzałka po lewej przy aktywnej pozycji (moduł „toc-rail” w podstrony.js). Pokazywana od 1001 px; poniżej działa toc_index."""
    ctx.use('toc-rail')
    entries = []
    for e in toc:
        subs = ''
        if e['subs'] and not re.search(r'najczęstsze pytania', e['text'], re.I):
            subs = '<ul>' + ''.join(f'<li><a href="#{s["id"]}">{s["text"]}</a></li>' for s in e['subs']) + '</ul>'
        entries.append(f'<li class="toc-entry"><a class="toc-link" href="#{e["id"]}">{e["text"]}</a>{subs}</li>')
    return ('<nav class="toc-rail" aria-labelledby="toc-rail-title"><div class="toc-rail-wrap"><div class="toc-sticky">'
            '<p class="kicker" id="toc-rail-title">Spis treści</p>'
            f'<ol class="toc-list">{"".join(entries)}</ol></div></div></nav>')


# ----------------------------------------------------------------------------
# N5 section-head, N6 split-feature, N7 rail-layout
# ----------------------------------------------------------------------------
def section_head(ctx, num, sec, lead_html=None, level=2, forced=None):
    ctx.use('section-head')
    k = None if isinstance(num, int) else num   # numery rozdziałów usunięte (ozdobnik, mylący)
    lead = f'<p class="section-lead">{lead_html}</p>' if lead_html else ''
    kk = f'<span class="kicker">{k}</span>' if k else ''
    f = forced or ctx.title_split(sec.id)
    return f'<header class="section-head">{kk}{heading(level, sec.title, sec.id, f)}{lead}</header>'


def _short_pair(body):
    """Czy tekst, który stałby obok zdjęcia (callout albo akapit po pierwszym elemencie), jest krótki (< 320 znaków)?"""
    kids = [c for c in BeautifulSoup(body, 'html.parser').contents if getattr(c, 'name', None)]
    if not kids:
        return False
    pair = kids[0] if 'callout' in (kids[0].get('class') or []) else (kids[1] if len(kids) > 1 and (kids[1].name == 'p' or 'sub-chapter' in (kids[1].get('class') or [])) else None)
    return pair is not None and len(pair.get_text().strip()) < 320


def split_feature(ctx, aside, body, reverse=False, cls=''):
    ctx.use('split-feature')
    if 'photo-frame' not in aside or _short_pair(body):   # bez zdjęcia obok nie ma pary 4+4; mało tekstu: zdjęcie poziome, tekst pod nim   # mało tekstu: zdjęcie poziome na 8 kolumn, tekst pod nim (nie obok pionowego zdjęcia)
        cls = (cls + ' is-short').strip()
    r = ' is-reversed' if reverse else ''
    return (f'<div class="split-feature{r}{(" " + cls) if cls else ""}"><div class="split-aside">{aside}</div>'
            f'<div class="split-body">{body}</div></div>')


def rail_layout(ctx, items, body, label='Rozdziały'):
    """items: [(id, html_text)] — szyna nawigacji; body: HTML."""
    ctx.use('rail-layout')
    lis = ''.join(f'<li><a href="#{i}">{t}</a></li>' for i, t in items)
    return (f'<div class="rail-layout"><nav class="rail-nav" aria-label="{label}"><p class="kicker">{label}</p>'
            f'<ol>{lis}</ol></nav><div class="rail-body">{body}</div></div>')


# ----------------------------------------------------------------------------
# listy N8, N10, N14, N21
# ----------------------------------------------------------------------------
def ruled_list(ctx, ul, variant='', ordered=None):
    ctx.use('ruled-list')
    is_ol = (ordered if ordered is not None else ul.name == 'ol')
    tag = 'ol' if is_ol else 'ul'
    items = ul.find_all('li', recursive=False)
    v = variant.split() if variant else []
    if is_ol and 'is-numbered' not in v and 'is-checklist' not in v:
        v.append('is-numbered')
    if len(items) >= 8 and 'is-columns' not in v and sum(len(li.get_text().split()) for li in items) / len(items) <= 7:
        v.append('is-columns')
    cls = ' '.join(['ruled-list'] + v)
    lis = ''.join(f'<li>{li.decode_contents()}</li>' for li in items)
    return f'<{tag} class="{cls}">{lis}</{tag}>'


def step_list(ctx, ol, titles=True, steps=None, cls='', h=3):
    ctx.use('step-list')
    items = ol.find_all('li', recursive=False)
    n = len(items)
    st = steps or (n if n <= 4 else 3)
    lis = []
    for li in items:
        lab, rest = runin(li) if titles else (None, li.decode_contents())
        if lab:
            lis.append(f'<li><h{h} class="step-title">{lab}</h{h}><p>{rest}</p></li>')
        else:
            lis.append(f'<li><p>{rest}</p></li>')
    return f'<ol class="step-list{(" " + cls) if cls else ""}" style="--steps:{st}">{"".join(lis)}</ol>'


def key_values(ctx, ul):
    ctx.use('key-values')
    rows = []
    for li in ul.find_all('li', recursive=False):
        lab, rest = runin(li)
        if lab:
            rows.append(f'<div><dt>{lab}</dt><dd>{rest}</dd></div>')
        else:
            rows.append(f'<div><dt></dt><dd>{li.decode_contents()}</dd></div>')
    return f'<dl class="key-values">{"".join(rows)}</dl>'


def chooser(ctx, ul):
    """N21: zdanie ze źródła zostaje; myślnik rozdzielający warunek i rekomendację → strzałka."""
    ctx.use('chooser')
    lis = []
    for li in ul.find_all('li', recursive=False):
        h = li.decode_contents()
        m = re.search(r'\s[—–]\s', h)
        if m:
            h = f'<span>{h[:m.start()]}</span> {ARROW_IN} <span>{h[m.end():]}</span>'
        else:
            h = f'<span>{h}</span>'
        lis.append(f'<li><p>{h}</p></li>')
    return f'<ul class="chooser">{"".join(lis)}</ul>'


# ----------------------------------------------------------------------------
# tabele N9, N11, N12, N13
# ----------------------------------------------------------------------------
def _label(ctx, label):
    return esc(plain(label)) if label else 'Tabela'


def ruled_table(ctx, tbl, label, kind=''):
    ctx.use('ruled-table')
    head, rows = table_rows(tbl)
    ncol = max(len(head), max((len(r) for r in rows), default=0))
    ths = ''.join(f'<th scope="col">{h}</th>' for h in head)
    if kind == 'is-directory':
        ths += '<th scope="col"><span class="visually-hidden">Przejdź</span></th>'
    body = []
    for r in rows:
        cells = []
        for i, c in enumerate(r):
            if i == 0:
                cells.append(f'<th scope="row">{c}</th>')
            else:
                lab = esc(plain(head[i])) if i < len(head) else ''
                cells.append(f'<td data-label="{lab}">{c}</td>')
        if kind == 'is-directory':
            cells.append(f'<td class="row-go" aria-hidden="true">{ARROW_IN}</td>')
        body.append(f'<tr>{"".join(cells)}</tr>')
    k = f' {kind}' if kind else ''
    if len(head) == 2 and head[0] == '':
        pass
    return (f'<div class="ruled-table{k}" role="region" tabindex="0" aria-label="{_label(ctx, label)}">'
            f'<table><thead><tr>{ths}</tr></thead><tbody>{"".join(body)}</tbody></table></div>')


def triage_table(ctx, tbl, label):
    ctx.use('ruled-table')
    head, rows = table_rows(tbl)
    ths = ''.join(f'<th scope="col">{h}</th>' for h in head)
    body = []
    for r in rows:
        cells = [f'<th scope="row">{r[0]}</th>']
        for i, c in enumerate(r[1:], 1):
            lab = esc(plain(head[i]))
            cells.append(f'<td data-label="{lab}"><strong>{c}</strong></td>')
        body.append(f'<tr>{"".join(cells)}</tr>')
    return (f'<div class="ruled-table is-triage" role="region" tabindex="0" aria-label="{_label(ctx, label)}">'
            f'<table><thead><tr>{ths}</tr></thead><tbody>{"".join(body)}</tbody></table></div>')


def phase_timeline(ctx, tbl):
    ctx.use('phase-timeline')
    head, rows = table_rows(tbl)
    lis = []
    for r in rows:
        lis.append(f'<li><h4><span class="visually-hidden">{head[0]}: </span>{r[0]}</h4>'
                   f'<p class="phase-when"><span class="visually-hidden">{head[1]}: </span>{r[1]}</p>'
                   f'<p><span class="visually-hidden">{head[2]}: </span>{r[2]}</p></li>')
    return f'<ol class="phase-timeline" style="--phases:{len(rows)}">{"".join(lis)}</ol>'


def duo_cols(ctx, tbl, label, labelled=None):
    """Kolumny tabeli = dwie strony (psy/koty, AKI/PChN). Pierwsza kolumna jest etykietą wiersza, gdy jest ich 3."""
    ctx.use('duo')
    head, rows = table_rows(tbl)
    has_label = len(head) == 3 if labelled is None else labelled
    sides = head[1:] if has_label else head
    hid = f'<span class="visually-hidden">{head[0]}</span>' if has_label and head[0] else ''
    out = [f'<div class="duo" role="group" aria-label="{_label(ctx, label)}">{hid}',
           f'<div class="duo-head">{sides[0]}</div><span class="duo-vs" aria-hidden="true"><em>vs</em></span>'
           f'<div class="duo-head">{sides[1]}</div>']
    for r in rows:
        cells = r[1:] if has_label else r
        lab = f'<p class="duo-label">{r[0]}</p>' if has_label else ''
        out.append(f'<div class="duo-row">{lab}'
                   f'<div class="duo-cell" data-side="{esc(plain(sides[0]))}">{cells[0]}</div>'
                   f'<div class="duo-cell" data-side="{esc(plain(sides[1]))}">{cells[1]}</div></div>')
    out.append('</div>')
    return ''.join(out)


def duo_rows(ctx, tbl, label):
    """Wiersze tabeli = dwie strony (tabela „Gdzie | Badania”): każda strona to wiersz."""
    ctx.use('duo')
    head, rows = table_rows(tbl)
    a, b = rows[0], rows[1]
    hv = f'<span class="visually-hidden">{head[0]}: </span>'
    cv = f'<span class="visually-hidden">{head[1]}: </span>'
    return (f'<div class="duo is-rows" role="group" aria-label="{_label(ctx, label)}">'
            f'<div class="duo-head">{hv}{a[0]}</div><span class="duo-vs" aria-hidden="true"><em>vs</em></span>'
            f'<div class="duo-head">{hv}{b[0]}</div>'
            f'<div class="duo-row"><div class="duo-cell" data-side="{esc(plain(head[1]))}">{cv}{a[1]}</div>'
            f'<div class="duo-cell" data-side="{esc(plain(head[1]))}">{cv}{b[1]}</div></div></div>')


def range_scale(ctx, tbl, label):
    """N13: wizualizacja tabeli ze źródła; pełna tabela dla czytników ekranu pozostaje w DOM (visually-hidden)."""
    ctx.use('range-scale')
    head, rows = table_rows(tbl)
    lis = []
    for r in rows:
        extra = ''.join(f'<span class="range-cell" data-label="{esc(plain(head[i]))}">{c}</span>' for i, c in enumerate(r[1:], 1))
        lis.append(f'<li><span class="range-value">{r[0]}</span>{extra}</li>')
    hidden = ruled_table(ctx, tbl, label).replace('class="ruled-table"', 'class="ruled-table visually-hidden"').replace(
        ' role="region" tabindex="0"', '')
    return (f'<ol class="range-scale" aria-hidden="true" style="--cols-n:{len(rows)}">{"".join(lis)}</ol>{hidden}')


# ----------------------------------------------------------------------------
# sygnały N16, N17, N18, N19
# ----------------------------------------------------------------------------
def alert_band(ctx, h_level, h_text, h_id, inner, kick='Pilne', inverted=True, phone=True, cls=''):
    ctx.use('alert-band')
    nap = ctx.home.nap
    c = 'alert-band' + (' is-inverted' if inverted else '') + (f' {cls}' if cls else '')
    btn = (f'<a class="button" href="tel:{nap["tel"]}">Zadzwoń: {nap["tel_disp"].replace(" ", NB)}</a>') if phone else ''
    return (f'<div class="{c}" role="note"><span class="kicker">{kick}</span>'
            f'<h{h_level}{f" id={chr(34)}{h_id}{chr(34)}" if h_id else ""} class="alert-title">{h_text}</h{h_level}>{inner}{btn}</div>')


def callout(ctx, kick, p_nodes):
    ctx.use('callout')
    ps = ''.join(f'<p>{p.decode_contents() if isinstance(p, Tag) else p}</p>' for p in p_nodes)
    kk = f'<span class="kicker">{kick}</span>' if kick == 'Pilne' else ''   # etykiety zostają tylko kryzysowe (polecenie użytkownika)
    return f'<aside class="callout">{kk}{ps}</aside>'


def cta_band(ctx, cta, extra_html=''):
    ctx.use('cta-band')
    return (f'<div class="cta-band">{hero_actions(ctx, cta)}{extra_html}</div>')   # zdanie „Umów wizytę: …” usunięte — powtarzało przyciski


def sticky_cta(ctx):
    ctx.use('sticky-cta')
    nap = ctx.home.nap
    return (f'<div class="sticky-cta" aria-label="Szybki kontakt"><a class="button" href="{nap["wettermin"]}" rel="noopener">'
            f'Umów wizytę {ARROW_OUT}</a><a class="button" href="tel:{nap["tel"]}">Zadzwoń</a></div>')


# ----------------------------------------------------------------------------
# FAQ H5 / N20
# ----------------------------------------------------------------------------
def faq_items(sec):
    """Zwraca [(h3_id, h3_html, [węzły odpowiedzi])]."""
    return [(s.id, s.title, s.nodes) for s in sec.subs]


def faq_is_columns(sec):
    items = faq_items(sec)
    n = len(items)
    if n == 0 or n % 3:
        return False
    for _, _, nodes in items:
        if any(x.name != 'p' for x in nodes):
            return False
        if sum(len(x.get_text()) for x in nodes) > 380:
            return False
    return True


def faq_columns(ctx, sec):
    ctx.use('detail-columns')
    cols = []
    for sid, title, nodes in faq_items(sec):
        ps = ''.join(f'<p>{n.decode_contents()}</p>' for n in nodes)
        cols.append(f'<div><h3 id="{sid}">{title}</h3><div class="detail-body">{ps}</div></div>')
    return f'<div class="arrival-details detail-columns ruled-columns">{"".join(cols)}</div>'


def faq_accordion(ctx, sec, open_first=None):
    ctx.use('faq-accordion')
    items = faq_items(sec)
    op = (len(items) >= 6) if open_first is None else open_first
    out = []
    for i, (sid, title, nodes) in enumerate(items):
        body = ''.join(_node_html(ctx, n) for n in nodes)
        o = ' open' if (op and i == 0) else ''
        out.append(f'<details class="faq-item"{o}><summary><h3 id="{sid}">{title}</h3></summary>'
                   f'<div class="faq-answer book-prose">{body}</div></details>')
    return f'<div class="faq-accordion">{"".join(out)}</div>'


_CALLOUT_RE = re.compile(r'^(Ważne|Uwaga|Pamiętaj|Zapamiętaj)\b')


def _node_html(ctx, n):
    """Prosty węzeł bloku (p/ul/ol/table) jako HTML zbliżony do źródła."""
    if n.name == 'p':
        if _CALLOUT_RE.match(n.get_text(' ', strip=True)):
            return callout(ctx, 'Ważne', [n])
        return f'<p>{n.decode_contents()}</p>'
    if n.name in ('ul', 'ol'):
        return ruled_list(ctx, n)
    if n.name == 'table':
        return ruled_table(ctx, n, getattr(ctx, 'cur_title', ''))
    return str(n)


# ----------------------------------------------------------------------------
# placeholdery N24, N25, N26
# ----------------------------------------------------------------------------
EXT = {'foto': 'jpg', 'pas': 'jpg', 'wycinek': 'png', 'ilustracja': 'png', 'diagram': 'png', 'ikona': 'svg'}


# ustawienie kadru zdjęcia w ramce 8 kolumn (object-position), gdy domyślne 50% 40% ucina główny motyw
PH_POS = {'chir-03-opieka-po': '50% 54%'}


def photo_frame(ctx, ph_id, variant='', ratio=None, role=''):
    from obrazy import OBRAZY
    spec = OBRAZY[ph_id]
    kind = spec['kind']
    ratio = ratio or spec['ratio']
    ext = EXT[kind]
    fn = f'assets/podstrony/{ctx.slug}/{ph_id}.{ext}'
    ctx.placeholders.append({'id': ph_id, 'kind': kind, 'ratio': ratio, 'file': fn, 'page': ctx.slug,
                             'sekcja': getattr(ctx, 'cur_sec', ''), 'rola': role})
    ctx.use('photo-frame')
    cls = 'placeholder photo-frame' + (f' {variant}' if variant else '')
    r = ratio.replace(':', '/')
    wide = ''
    try:
        rw_, rh_ = (float(x) for x in ratio.replace('/', ':').split(':'))
        if rw_ <= rh_:
            cls += ' is-narrow'   # portret i kwadrat: połowa szerokości kolumny artykułu
            wide = f'{rw_ * 2:g}/{rh_:g}'   # ta sama wysokość, ramka 8 kolumn (gdy obok nie ma tekstu)
    except ValueError:
        pass
    arr = {'foto': 'Zdjęcie', 'pas': 'Pas', 'wycinek': 'Wycinek', 'ilustracja': 'Ilustracja', 'diagram': 'Diagram', 'ikona': 'Ikona'}[kind]
    bw = 'kolor, retro' if kind in ('foto', 'pas') else ('liniowa' if kind in ('diagram', 'ilustracja') else 'czarna kreska na białym tle')
    return (f'<figure class="{cls}" data-ph="{ph_id}" data-kind="{kind}" data-src="{fn}" '
            f'data-alt="{esc(spec["alt"])}" style="--ph-ratio:{r}' + (f';--ph-ratio-wide:{wide}' if wide else '') + (f';--ph-pos:{PH_POS[ph_id]}' if ph_id in PH_POS else '') + '">'
            f'<figcaption><strong>{esc(spec["title"])}</strong><span>{arr} {ratio.replace("/", "∶")} · {bw}</span></figcaption></figure>'
            f'<!-- Podmiana: wgraj plik {fn} i odśwież stronę — podstrony.js podmieni ramkę bez edycji HTML. -->')


def figure_band(ctx, ph_id, callout_html=''):
    ctx.use('figure-band')
    return f'<div class="figure-band">{photo_frame(ctx, ph_id, ratio="21/9")}{callout_html}</div>'


def figure_mosaic(ctx, ids, reverse=False):
    ctx.use('figure-mosaic')
    r = ' is-reversed' if reverse else ''
    inner = ''.join(photo_frame(ctx, i) for i in ids)
    return f'<div class="figure-mosaic{r}">{inner}</div>'


# ----------------------------------------------------------------------------
# bloki kopiowane z home (H*)
# ----------------------------------------------------------------------------
def home_header_raw(ctx, sid, new_h2_id=None):
    """header.poster-grid.section-header z sekcji home (przepisane ścieżki)."""
    raw = ctx.home.sections[sid]
    r = Raw(raw).cls('header', 'poster-grid', 'section-header')[0]
    return ctx.rw.fragment(r)


def related_tiles(ctx, slugs):
    """N22: kafle bez ilustracji (odrzucone pliki usunięte); tytuł i opis z kafla home."""
    ctx.use('related-tiles')
    tiles = {t['slug']: t for t in ctx.home.tiles}
    arts = []
    for s in slugs:
        t = tiles[s]
        href = ctx.rw.page_link(s)
        arts.append(f'<article><h3><a href="{href}">{t["title"]}</a></h3><p>{t["desc_html"]}</p></article>')
    return f'<div class="related-tiles ruled-columns">{"".join(arts)}</div>'


def people_cards(ctx, keys):
    ctx.use('people')
    cards = ''.join(ctx.rw.fragment(ctx.home.people_raw[k]) for k in keys)
    return f'<div class="grid people ruled-columns">{cards}</div>'


def after_hours(ctx):
    ctx.use('after-hours')
    return ctx.rw.fragment(ctx.home.after_hours_raw)


def quotes_block(ctx, idx):
    ctx.use('quotes')
    qs = ''.join(ctx.rw.fragment(ctx.home.quotes[i]) for i in idx)
    return f'<div class="grid quotes ruled-columns">{qs}</div>'


def emergency_guide(ctx, ol, gid, title_html, untitled=False, source_p=None):
    """H11. Przy untitled: bez h3, aria-labelledby wskazuje nagłówek sekcji (gid)."""
    ctx.use('emergency-guide')
    items = ol.find_all('li', recursive=False)
    lis = []
    for li in items:
        lab, rest = runin(li)
        if lab and not untitled:
            lis.append(f'<li><h4>{lab}</h4><p>{rest}</p></li>')
        else:
            lis.append(f'<li><p>{li.decode_contents()}</p></li>')
    src = f'<p class="emergency-guide-source">{source_p}</p>' if source_p else ''
    cls = 'emergency-guide' + (' is-untitled' if untitled else '')
    h = f'<h3 id="{gid}">{title_html}</h3>' if (title_html and not untitled) else ''
    lab = f' aria-labelledby="{gid}"' if gid else ''
    return f'<div class="{cls}"{lab}>{h}<ol class="emergency-steps">{"".join(lis)}</ol>{src}</div>'


def bento(ctx):
    ctx.use('bento')
    ctx.svg_needed = True
    raw = ctx.home.bento_raw
    return ctx.rw.fragment(raw)


def photo_pets_note():
    return ''


# ----------------------------------------------------------------------------
# sekcje kopiowane z home (H13, H14, H15) i zamknięcie (H16)
# ----------------------------------------------------------------------------
def booking_section(ctx):
    """H13: sekcja #zapraszamy z home (tekst lekarek, bez FB/IG — to już wersja „nowa”)."""
    ctx.use('booking')
    html = ctx.rw.fragment(ctx.home.booking_raw)
    # szary pies z kulkami jest tylko na stronie głównej i w banerze pracy — na podstronach rezerwacja bez zdjęcia (polecenie właściciela)
    html = re.sub(r'<div class="booking-photo[^"]*"[^>]*></div>', '', html)
    html = re.sub(r'<figure class="booking-dog-foreground">.*?</figure>', '', html, flags=re.S)
    html = re.sub(r'<div class="booking-pets[^"]*"[^>]*>.*?</div>', '', html, flags=re.S)
    return html


def social_section(ctx):
    ctx.use('social-promo')
    return ctx.rw.fragment(ctx.home.social_raw)


def about_section(ctx):
    ctx.use('about')
    return ctx.rw.fragment(ctx.home.about_raw)


def contact_section(ctx, sec):
    """H16: plakat + H7 z wierszy listy „Jak umówić…” (<strong> → h3)."""
    ctx.use('contact', 'poster-grid', 'contact-columns')
    ul = next(n for n in sec.nodes if n.name == 'ul')
    rest = [n for n in sec.nodes if n is not ul]
    cols = []
    for li in ul.find_all('li', recursive=False):
        lab, body = runin(li)
        assert lab, f'contact: brak etykiety w wierszu {li.get_text()[:40]}'
        cols.append(f'<div class="contact-column"><h3>{lab}</h3><p>{body}</p></div>')
    art = ctx.rw.fragment(ctx.home.header_arts['kontakt'])
    after = ''.join(f'<p class="contact-note">{n.decode_contents()}</p>' for n in rest if n.name == 'p')
    hid = sec.id
    forced = ctx.title_split(sec.id)
    head = (f'<header class="poster-grid section-header"><div class="poster-copy"><div class="poster-heading">'
            f'<h2 id="{hid}">{title_inner(sec.title, forced)}</h2></div></div>{art}</header>')
    inner = f'{head}<div class="contact-columns detail-columns ruled-columns">{"".join(cols)}</div>{after}'
    return (f'<section class="contact" data-palette="{ctx.home.label_for("contact")}" id="kontakt" aria-labelledby="{hid}">'
            f'<div class="wrap section-stack">{inner}</div></section>')


# ----------------------------------------------------------------------------
# H5/H6 z elementów źródła
# ----------------------------------------------------------------------------
def equipment_grid(ctx, subs, numbered=True, cols=3):
    """H6: równoległe krótkie wpisy z h3 → kolumny z liniami (h3 zachowuje id i poziom)."""
    ctx.use('equipment-grid')
    cells = []
    for s in subs:
        body = ''.join(_node_html(ctx, n) for n in s.nodes)
        cells.append(f'<div><h3 id="{s.id}">{s.title}</h3>{body}</div>')
    cls = 'equipment-grid detail-columns ruled-columns' + (' is-numbered' if numbered else '')
    return f'<div class="{cls}" style="--grid-cols:{cols}">{"".join(cells)}</div>'


def detail_columns_from_subs(ctx, subs):
    ctx.use('detail-columns')
    cells = []
    for s in subs:
        body = ''.join(_node_html(ctx, n) for n in s.nodes)
        cells.append(f'<div><h3 id="{s.id}">{s.title}</h3><div class="detail-body">{body}</div></div>')
    return f'<div class="arrival-details detail-columns ruled-columns">{"".join(cells)}</div>'


def sub_chapter(ctx, sub, body_html=None, level=3):
    """Podrozdział (h3 + węzły) wewnątrz split-body."""
    body = body_html if body_html is not None else ''.join(_node_html(ctx, n) for n in sub.nodes)
    return f'<div class="sub-chapter"><h{level} id="{sub.id}">{sub.title}</h{level}>{body}</div>'


def prose(ctx, nodes):
    """Akapity i proste węzły jako .book-prose."""
    inner = ''.join(_node_html(ctx, n) for n in nodes)
    return f'<div class="book-prose">{inner}</div>' if inner else ''


def person_link_text(ctx, anchor):
    return ctx.home.people_raw[anchor]


# ----------------------------------------------------------------------------
# nagłówek plakatowy sekcji (H4) z własnym h2 i ilustracją z home
# ----------------------------------------------------------------------------
def poster_header(ctx, art_key, sec=None, title_html=None, hid=None, kick=None, lead_html=None, forced=None, extra_bottom=''):
    ctx.use('poster-grid')
    if sec is not None:
        title_html, hid = sec.title, sec.id
        forced = forced or ctx.title_split(sec.id)
    art = ctx.rw.fragment(ctx.home.header_arts[art_key])
    k = f'<span class="kicker">{kick}</span>' if kick else ''
    h2 = title_inner(title_html, forced)
    pre = ''
    if kick:   # etykieta kryzysowa („Pilne”) scalona z tytułem w jednym napisie z myślnikiem
        pre = f' data-pre="{kick} — "'
        k = ''
    bottom = ''
    if lead_html or extra_bottom:
        lp = f'<p>{lead_html}</p>' if lead_html else ''
        bottom = f'<div class="poster-bottom">{lp}{extra_bottom}</div>'
    return (f'<header class="poster-grid section-header"><div class="poster-copy"><div class="poster-heading">{k}'
            f'<h2 id="{hid}"{pre}>{h2}</h2></div>{bottom}</div>{art}</header>')


def prose_nodes(ctx, nodes):
    """Węzły prawnicze: p / ol / ul / tabela bez ozdobników (N15)."""
    out = []
    for n in nodes:
        if n.name == 'p':
            out.append(f'<p>{n.decode_contents()}</p>')
        elif n.name in ('ol', 'ul'):
            out.append(ruled_list(ctx, n, ordered=(n.name == 'ol')))
        elif n.name == 'table':
            out.append(ruled_table(ctx, n, getattr(ctx, 'cur_title', '')))
        else:
            out.append(str(n))
    return ''.join(out)


def join_art_dog(ctx):
    """Obraz banera „Praca w Psyjaciołach”: siatka 8×8 kolorowych zdjęć pacjentów (psy i koty), komórki 80×80 px, całość 640×640 px."""
    ctx.use('join-banner')
    s1 = ctx.rw.asset('assets/join-pacjenci-640.avif')
    s2 = ctx.rw.asset('assets/join-pacjenci-1254.avif')
    return (f'<img class="join-grid" src="{s1}" srcset="{s1} 640w, {s2} 1254w" sizes="(min-width: 1001px) 843px, 100vw" '
            'alt="Pacjenci przychodni Psyjaciele — psy i koty" width="640" height="640" loading="lazy" decoding="async">')


def join_art_shared(ctx):
    """Wspólny obraz banera na podstronach usług i na stronie Zespół: szary pies z latającymi kulkami."""
    return join_art_dog(ctx)


def join_banner(ctx, title, nodes, img_html, mail_href, hid=None, side=False, forced=None):
    """Baner „Praca w Psyjaciołach”: cały baner jest jednym linkiem mailto; u góry szary pies z latającymi kulkami (300 px),
    pod nim apla w kolorze kulek: tytuł u góry apli, krótki tekst (adres e-mail tylko raz) ze strzałką na dole."""
    ctx.use('join-banner')
    parts = [re.sub(r'</?a\b[^>]*>', '', n.decode_contents()).strip() for n in nodes]
    parts = [x for x in parts if x]
    arrow = '<span class="join-arrow" aria-hidden="true"></span>'
    if parts:
        parts[-1] = f'{parts[-1]} {arrow}'
        ps = ''.join(f'<p>{x}</p>' for x in parts)
    else:
        ps = f'<p>{arrow}</p>'
    h = f'<h2 id="{hid}" aria-label="{plain(title)}">Praca</h2>' if hid else '<h2 aria-label="Praca w Psyjaciołach">Praca</h2>'   # na banerze widać samo „Praca”
    return (f'<a class="join-banner" href="{mail_href}"><div class="join-art">{img_html}</div>'
            f'<div class="join-copy"><div class="join-text">{h}</div>{ps}</div></a>')
