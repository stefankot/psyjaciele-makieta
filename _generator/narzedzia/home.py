# generated: psyjaciele-podstrony
"""home.py — wyciąganie fragmentów ze strony głównej (jedno źródło prawdy) i przepisywanie ścieżek.

Czyta (tylko do odczytu): index.html w korzeniu makiety (strona główna; stałe HOME_FILE i NOWA_FILE),
minimal.css i design-tokens.css (palety).
Fragmenty kopiuje jako surowy tekst (bez parsera), żeby nie zepsuć wielkości liter w SVG.
"""
import json
import os
import posixpath
import re
from pathlib import Path
from urllib.parse import urlsplit

HOME_FILE = 'index.html'                     # §00.1 pkt 4: po podmianie home zmieniasz tylko tę stałą
NOWA_FILE = 'index.html'
DOMENA = 'https://www.psyjacielevet.pl'
ROBOTS = 'noindex,follow'                     # §2.1: jedno miejsce

VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param',
        'source', 'track', 'wbr'}
TAG_RE = re.compile(r'<(/?)([a-zA-Z][a-zA-Z0-9:-]*)((?:[^>"\']|"[^"]*"|\'[^\']*\')*)>')
ATTR_RE = re.compile(r'([\w:-]+)(?:\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|([^\s"\'>]+)))?')
COMMENT_RE = re.compile(r'<!--.*?-->', re.S)
URL_ATTR_RE = re.compile(r'(\s)(href|src|srcset|poster|data-src|data-[\w-]*src)="([^"]*)"')
STYLE_ATTR_RE = re.compile(r'(\sstyle=")([^"]*)(")')
CSS_URL_RE = re.compile(r'url\(\s*([\'"]?)([^)\'"]*)\1\s*\)')


def attrs_of(attr_str):
    out = {}
    for m in ATTR_RE.finditer(attr_str):
        out[m.group(1)] = m.group(2) if m.group(2) is not None else (m.group(3) or m.group(4) or '')
    return out


class Raw:
    """Surowy dokument z funkcjami wycinania zbalansowanych elementów."""

    def __init__(self, html):
        self.html = html
        # wersja do skanowania: komentarze i skrypty zastąpione spacjami (te same pozycje)
        scan = COMMENT_RE.sub(lambda m: ' ' * len(m.group(0)), html)
        scan = re.sub(r'(<script\b[^>]*>)(.*?)(</script>)',
                      lambda m: m.group(1) + ' ' * len(m.group(2)) + m.group(3), scan, flags=re.S)
        self.scan = scan

    def find(self, tag, pred=None, start=0, end=None):
        """Generator (start, end, attrs) elementów <tag> spełniających pred(attrs)."""
        end = end or len(self.scan)
        for m in TAG_RE.finditer(self.scan, start, end):
            if m.group(1) or m.group(2).lower() != tag:
                continue
            a = attrs_of(m.group(3))
            if pred is None or pred(a):
                yield m.start(), self.balanced(m.start()), a

    def balanced(self, start):
        m0 = TAG_RE.match(self.scan, start)
        name = m0.group(2).lower()
        if name in VOID or m0.group(3).rstrip().endswith('/'):
            return m0.end()
        depth = 0
        for m in TAG_RE.finditer(self.scan, start):
            if m.group(2).lower() != name:
                continue
            if m.group(1):
                depth -= 1
                if depth == 0:
                    return m.end()
            elif not m.group(3).rstrip().endswith('/'):
                depth += 1
        raise ValueError('niezbalansowany element ' + name)

    def one(self, tag, pred=None, start=0, end=None):
        for s, e, a in self.find(tag, pred, start, end):
            return self.html[s:e], s, e, a
        return None

    def cls(self, tag, *classes, start=0, end=None):
        want = set(classes)
        return self.one(tag, lambda a: want <= set(a.get('class', '').split()), start, end)

    def by_id(self, tag, ident, start=0, end=None):
        return self.one(tag, lambda a: a.get('id') == ident, start, end)

    def all_cls(self, tag, *classes, start=0, end=None):
        want = set(classes)
        return [(self.html[s:e], a) for s, e, a in
                self.find(tag, lambda a: want <= set(a.get('class', '').split()), start, end)]


def strip_shy(s):
    return s.replace('&shy;', '').replace('­', '')


def text_of(raw):
    t = re.sub(r'<[^>]+>', '', raw)
    import html as _h
    return re.sub(r'\s+', ' ', _h.unescape(strip_shy(t))).strip()


class Pages:
    """Mapa adresów wyjściowych podstron (względem MAKIETA)."""

    def __init__(self, slugs):
        self.out = {'index': '_generator/wyniki/index.html', 'uslugi-weterynaryjne': 'uslugi-weterynaryjne/index.html',
                    'zespol': 'zespol/index.html', 'polityka-prywatnosci': 'polityka-prywatnosci/index.html'}
        for s in slugs:
            if s not in self.out:
                self.out[s] = f'uslugi-weterynaryjne/{s}/index.html'

    def prod(self, slug):
        """Adres produkcyjny (canonical)."""
        if slug == 'index':
            return DOMENA + '/'
        if slug in ('uslugi-weterynaryjne', 'zespol', 'polityka-prywatnosci'):
            return f'{DOMENA}/{slug}/'
        return f'{DOMENA}/uslugi-weterynaryjne/{slug}/'


class Rewriter:
    """Przepisuje ścieżki fragmentów tak, by działały z podanej strony (R5)."""

    def __init__(self, pages: Pages, page_slug):
        self.pages = pages
        self.slug = page_slug
        self.file = pages.out[page_slug]
        self.dir = posixpath.dirname(self.file)
        self.root = '../' * len([p for p in self.dir.split('/') if p])
        self.unmapped = []

    # --- narzędzia -----------------------------------------------------
    def rel_to(self, target):
        """Ścieżka względna z katalogu strony do pliku `target` (względem MAKIETA)."""
        r = posixpath.relpath(target, self.dir or '.')
        return r

    def page_link(self, slug, frag=''):
        return self.rel_to(self.pages.out[slug]) + frag

    def home_link(self, frag=''):
        return self.root + HOME_FILE + frag

    def asset(self, canon):
        return self.root + canon

    # --- adresy z fragmentów home -----------------------------------
    def home_url(self, u, base='.', frag_to_home=False):
        if not u or u.startswith(('http:', 'https:', 'mailto:', 'tel:', 'data:', 'javascript:')):
            return u
        if u.startswith('#'):
            return self.home_link(u) if frag_to_home else u
        sp = urlsplit(u)
        p = posixpath.normpath(posixpath.join(base, sp.path)) if sp.path else ''
        if p.startswith('podstrony/'):      # home może linkować bezpośrednio do podstron (podstrony/…)
            p = p[len('podstrony/'):]
        frag = ('#' + sp.fragment) if sp.fragment else ''
        if p in (NOWA_FILE, HOME_FILE, 'index.html'):
            return self.home_link(frag)
        m = re.match(r'^uslugi-weterynaryjne/([^/]+)/index\.html$', p)
        if m:
            return self.page_link(m.group(1), frag)
        if p == 'uslugi-weterynaryjne/index.html':
            return self.page_link('uslugi-weterynaryjne', frag)
        if p == 'zespol/index.html':
            return self.page_link('zespol', frag)
        if p == 'polityka-prywatnosci/index.html':
            return self.page_link('polityka-prywatnosci', frag)
        return self.asset(p) + (('?' + sp.query) if sp.query else '') + frag

    def fragment(self, raw, base='.', frag_to_home=False):
        def url_attr(m):
            val = m.group(3)
            if m.group(2) == 'srcset':
                parts = []
                for item in val.split(','):
                    bits = item.strip().split(None, 1)
                    bits[0] = self.home_url(bits[0], base, frag_to_home)
                    parts.append(' '.join(bits))
                val = ', '.join(parts)
            else:
                val = self.home_url(val, base, frag_to_home)
            return f'{m.group(1)}{m.group(2)}="{val}"'
        raw = URL_ATTR_RE.sub(url_attr, raw)

        def style_attr(m):
            body = m.group(2)
            # własności własne (--art/--icon/--blob/--pet-atlas): jak na home, bez ROOT (pułapka 4a)
            decls = []
            for d in body.split(';'):
                if ':' not in d:
                    decls.append(d)
                    continue
                name, val = d.split(':', 1)
                is_var = name.strip().startswith('--')

                def css_url(um):
                    u = um.group(2)
                    if u.startswith(('data:', 'http', '#')):
                        return um.group(0)
                    p = posixpath.normpath(posixpath.join(base, u))
                    return f'url({self.asset(p)})'
                decls.append(name + ':' + CSS_URL_RE.sub(css_url, val))
            return m.group(1) + ';'.join(decls) + m.group(3)
        return STYLE_ATTR_RE.sub(style_attr, raw)

    # --- linki z plików treści (adresy produkcyjne) -----------------
    def content_href(self, href):
        if not href or href.startswith(('tel:', 'mailto:', '#')) or re.match(r'^https?://', href):
            if href.startswith(DOMENA):
                return self.content_href(href[len(DOMENA):] or '/')
            return href
        sp = urlsplit(href)
        frag = ('#' + sp.fragment) if sp.fragment else ''
        path = sp.path
        m = re.match(r'^/uslugi-weterynaryjne/([^/]+)/?$', path)
        if m:
            return self.page_link(m.group(1), frag)
        if re.match(r'^/uslugi-weterynaryjne/?$', path):
            return self.page_link('uslugi-weterynaryjne', frag)
        if re.match(r'^/zespol/?$', path):
            return self.page_link('zespol', frag)
        if re.match(r'^/polityka-prywatnosci/?$', path):
            return self.page_link('polityka-prywatnosci', frag)
        if path in ('/', ''):
            return self.home_link(frag)
        self.unmapped.append(href)
        return href


def is_external(href):
    return bool(re.match(r'^https?://', href or '')) and not href.startswith(DOMENA)


class Home:
    def __init__(self, root: Path):
        self.root = Path(root)
        self.nowa_html = (self.root / NOWA_FILE).read_text(encoding='utf-8')
        self.min_html = (self.root / HOME_FILE).read_text(encoding='utf-8')
        self.nowa = Raw(self.nowa_html)
        self.min = Raw(self.min_html)
        self._load()

    # ------------------------------------------------------------------
    def _load(self):
        n = self.nowa
        h = self.nowa_html
        head = h[:h.index('</head>')]
        # kolejność <link>/<script> z head (z ?v=), względem layout-warianty
        self.head_stylesheets = re.findall(r'<link rel="stylesheet" href="([^"]+)"', head)
        self.head_preloads = [m for m in re.findall(r'<link rel="preload"[^>]*>', head) if 'as="font"' in m]
        self.head_sync_script = re.search(r'<script src="([^"]+)"></script>', head).group(1)
        body_scripts = re.findall(r'<script src="([^"]+)"( defer)?></script>', h[h.index('</main>'):])
        self.body_scripts = [(s, bool(d)) for s, d in body_scripts]
        m = re.search(r'<script type="application/ld\+json">(.*?)</script>', head, re.S)
        graph = json.loads(m.group(1))['@graph']
        self.jsonld_vet = next(x for x in graph if x['@type'] == 'VeterinaryCare')
        self.jsonld_website = next(x for x in graph if x['@type'] == 'WebSite')
        self.meta_html = {k: re.search(rf'<meta [^>]*{k}[^>]*>', head).group(0) for k in ('og:site_name',)}

        # nagłówek, tło nagłówka, stopka, filtry <svg>
        self.header_raw = n.cls('header', 'site-header')[0]
        self.footer_raw = n.one('footer')[0]
        body_svg = None
        for s, e, a in n.find('svg', start=n.html.index('</footer>')):
            body_svg = n.html[s:e]
            break
        self.svg_filters_raw = body_svg

        # sekcje
        def sec(i):
            r = n.by_id('section', i)
            return r[0] if r else None
        self.sections = {i: sec(i) for i in ('poczatek', 'onas', 'uslugi', 'zapraszamy', 'przychodnia', 'zespol',
                                             'rekomendacje', 'nagle-przypadki', 'przygotowanie', 'dojazd', 'pytania',
                                             'obserwuj-nas', 'kontakt')}
        # tło sekcji uslugi nie jest <section id=uslugi> w nowa? (jest) — kafle
        usl = self.sections['uslugi']
        ru = Raw(usl)
        self.bento_raw = ru.cls('div', 'bento')[0]
        self.tiles = self._tiles(self.bento_raw)
        # panel po godzinach, instrukcja kroków
        rn = Raw(self.sections['nagle-przypadki'])
        self.after_hours_raw = rn.cls('div', 'after-hours')[0]
        self.emergency_guide_raw = rn.cls('div', 'emergency-guide')[0]
        # opinie
        rr = Raw(self.sections['rekomendacje'])
        self.quotes = [r for r, a in rr.all_cls('div', 'quote')]
        self.review_source_raw = rr.cls('div', 'review-source')[0]
        # zespół
        rz = Raw(self.sections['zespol'])
        self.people_raw = {}
        for r, a in rz.all_cls('article', 'person'):
            mm = re.search(r'person-card-link"[^>]*href="[^"]*#(\w+)"|href="[^"]*#(\w+)"[^>]*class="person-card-link"', r)
            mm2 = re.search(r'class="person-card-link"[^>]*href="[^"]*#(\w+)"', r) or re.search(
                r'href="[^"]*#(\w+)"[^>]*class="person-card-link"', r) or re.search(r'person-card-link[^>]*href="[^"]*#(\w+)"', r)
            key = None
            for mmx in re.finditer(r'<a [^>]*>', r):
                t = mmx.group(0)
                if 'person-card-link' in t:
                    k = re.search(r'#(\w+)"', t)
                    key = k.group(1) if k else None
            self.people_raw[key] = r
        # ilustracje nagłówków sekcji (poster-art) — dla bloków H16/H18
        self.header_arts = {}
        for sid, raw in self.sections.items():
            if not raw:
                continue
            rs = Raw(raw)
            f = rs.cls('figure', 'poster-art')
            if f:
                self.header_arts[sid] = f[0]
        # about
        self.about_raw = self.sections['onas']
        self.booking_raw = self.sections['zapraszamy']
        self.social_raw = self.sections['obserwuj-nas']
        # paleta
        self._palettes()
        # NAP
        v = self.jsonld_vet
        self.nap = {'name': v['name'], 'tel_disp': '537 821 345', 'tel': v['telephone'], 'email': v['email'],
                    'street': v['address']['streetAddress'], 'zip': v['address']['postalCode'],
                    'city': v['address']['addressLocality'], 'map': v['hasMap'],
                    'wettermin': re.search(r'https://www\.wettermin\.pl[^"]+', self.booking_raw).group(0)}

    def _tiles(self, bento):
        tiles = []
        rb = Raw(bento)
        for raw, a in rb.all_cls('article', 'tile'):
            href = re.search(r'<h3><a [^>]*href="([^"]+)"', raw).group(1)
            slug = re.search(r'uslugi-weterynaryjne/([^/]+)/index\.html', href).group(1)
            title_raw = re.search(r'<h3><a [^>]*>(.*?)</a></h3>', raw, re.S).group(1)
            desc = re.search(r'<p class="tile-description"[^>]*>(.*?)</p>', raw, re.S).group(1)
            img = re.search(r'<img class="service-art" src="([^"]+)"', raw).group(1)
            tiles.append({'slug': slug, 'title': strip_shy(title_raw), 'title_shy': title_raw, 'desc_html': desc,
                          'img': posixpath.normpath(img), 'raw': raw})
        return tiles

    # ------------------------------------------------------------------
    def _palettes(self):
        css = (self.root / 'minimal.css').read_text(encoding='utf-8')
        css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
        tokens_css = (self.root / 'design-tokens.css').read_text(encoding='utf-8')
        tok = dict(re.findall(r'(--wp--preset--color--[\w-]+):(#[0-9a-fA-F]{6})', tokens_css))
        self.tokens = tok

        def resolve(v):
            v = v.strip()
            m = re.match(r'var\((--[\w-]+)\)', v)
            if m:
                return tok.get(m.group(1)) or resolve_root(m.group(1))
            return v

        def resolve_root(name):
            m = re.search(re.escape(name) + r':([^;}]+)', css)
            return resolve(m.group(1)) if m else None
        rules = {}
        for m in re.finditer(r'([^{}]+)\{([^{}]*--surface\s*:[^{}]*)\}', css):
            sel = re.sub(r'\s+', ' ', m.group(1).strip())
            body = m.group(2)
            vs = dict(re.findall(r'(--(?:surface|ink|small-ink|accent|hover-ink|hover-accent))\s*:\s*([^;]+)', body))
            rules[sel] = {k: resolve(v) for k, v in vs.items()}
        self.palette_rules = rules
        wanted = {'hero': '.hero', 'about': '.about', 'services': '.services', 'booking': '.booking', 'clinic': '.clinic',
                  'team': '.team', 'reviews': '.reviews', 'emergency': '.emergency',
                  'paper': '.arrival.preparation', 'soft-b': '.arrival:not(.preparation)', 'end': '.contact'}
        self.roles = {}
        for role, sel in wanted.items():
            self.roles[role] = rules[sel]
        self.roles['soft-a'] = rules['.about']
        self.roles['mid-a'] = rules['.services']
        self.roles['mid-b'] = rules['.reviews']
        self.roles['mid-c'] = rules['.team']
        self.roles['top'] = rules['.team']   # hero podstron: łososiowe (zmienne palety .team)
        self.roles['toc'] = rules['.clinic']
        self.roles['alarm'] = rules['.emergency']
        # klasy sekcji dla ról
        self.role_class = {'top': 'hero', 'toc': 'clinic', 'soft-a': 'about', 'soft-b': 'arrival',
                           'mid-a': 'services', 'mid-b': 'reviews', 'mid-c': 'team',
                           'paper': 'arrival preparation', 'alarm': 'emergency', 'booking': 'booking', 'end': 'contact'}
        self.roles['booking'] = rules['.booking']
        # etykiety data-palette z home (pierwsze wystąpienie danej klasy); nie wpływają na CSS
        self.palette_label = {}
        for sid, raw in self.sections.items():
            if not raw:
                continue
            m = re.match(r'<section ([^>]*)>', raw)
            a = attrs_of(m.group(1))
            self.palette_label.setdefault(a.get('class', ''), a.get('data-palette', ''))

    def surface(self, role):
        return self.roles[role]['--surface']

    def label_for(self, cls):
        return self.palette_label.get(cls) or self.palette_label.get(cls.split()[0], '')
