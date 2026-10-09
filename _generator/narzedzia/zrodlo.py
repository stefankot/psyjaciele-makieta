# generated: psyjaciele-podstrony
"""zrodlo.py — rozbiór plików treści (D1): _generator/tresci-podstron/czyste/<slug>.html.

Tekst nigdy nie jest przepisywany ręcznie: węzły bs4 są serializowane z poprawionymi linkami (R5).
"""
import re
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Tag

from home import is_external


def slugify_pl(s):
    tr = str.maketrans('ąćęłńóśźżĄĆĘŁŃÓŚŹŻ', 'acelnoszzACELNOSZZ')
    s = s.translate(tr).lower()
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    return s


class Sec:
    def __init__(self, tag):
        self.tag = tag
        self.id = tag.get('id') or ''
        self.title = tag.decode_contents()
        self.text = tag.get_text(' ', strip=True)
        self.level = int(tag.name[1])
        self.nodes = []      # węzły (Tag) przed pierwszym h3
        self.subs = []       # podsekcje h3 (Sec)

    def all_nodes(self):
        for n in self.nodes:
            yield n
        for s in self.subs:
            for n in s.all_nodes():
                yield n

    def find(self, kind):
        return [n for n in self.nodes if n.name == kind]

    def words(self):
        return len(' '.join(n.get_text(' ') for n in self.all_nodes()).split())


class Src:
    def __init__(self, slug, root: Path, rw):
        self.slug = slug
        self.rw = rw
        raw = (root / '_generator' / 'tresci-podstron' / 'czyste' / f'{slug}.html').read_text(encoding='utf-8')
        self.raw = raw
        self.title = re.search(r'<!--\s*title:\s*(.*?)\s*-->', raw).group(1)
        m = re.search(r'<!--\s*meta description:\s*(.*?)\s*-->', raw)
        self.desc = m.group(1) if m else ''
        soup = BeautifulSoup(raw, 'html.parser')
        self.soup = soup
        content = soup.select_one('div.content')
        self._fix_links(content)
        kids = [c for c in content.children if isinstance(c, Tag)]
        self.h1 = next(k for k in kids if k.name == 'h1')
        self.cta = None
        self.lead = []        # akapity wstępu (przed spisem/pierwszym h2)
        self.intro_extra = []  # inne elementy wstępu (tabela itp.)
        self.nav = None
        i = kids.index(self.h1) + 1
        while i < len(kids) and kids[i].name != 'h2':
            k = kids[i]
            if k.name == 'nav':
                self.nav = k
            elif k.name == 'p' and 'cta-wizyta' in (k.get('class') or []):
                self.cta = k
            elif k.name == 'p' and not self.intro_extra:
                self.lead.append(k)
            else:
                self.intro_extra.append(k)
            i += 1
        # sekcje
        self.secs = []
        cur2 = cur3 = None
        for k in kids[i:]:
            if k.name == 'h2':
                cur2 = Sec(k)
                cur3 = None
                self.secs.append(cur2)
            elif k.name == 'h3':
                cur3 = Sec(k)
                cur2.subs.append(cur3)
            else:
                (cur3 or cur2).nodes.append(k)
        self.by_id = {}
        for s in self.secs:
            self.by_id[s.id] = s
            for t in s.subs:
                self.by_id[t.id] = t
        self.toc = self._toc()

    # -------------------------------------------------------------
    def _fix_links(self, root):
        for a in root.find_all('a'):
            h = a.get('href')
            if not h:
                continue
            if h.startswith('#'):
                continue
            a['href'] = self.rw.content_href(h)
            if is_external(h):
                a['rel'] = 'noopener'

    def _toc(self):
        out = []
        if self.nav is None:
            return [{'id': s.id, 'text': s.title, 'subs': [{'id': t.id, 'text': t.title} for t in s.subs]} for s in self.secs]
        ol = self.nav.find('ol')
        for li in ol.find_all('li', recursive=False):
            a = li.find('a', recursive=False)
            subs = []
            ul = li.find('ul')
            if ul:
                for sli in ul.find_all('li', recursive=False):
                    sa = sli.find('a')
                    subs.append({'id': sa['href'][1:], 'text': sa.decode_contents()})
            out.append({'id': a['href'][1:], 'text': a.decode_contents(), 'subs': subs})
        return out

    # -------------------------------------------------------------
    def sec(self, sid):
        return self.by_id[sid]

    def faq(self):
        for s in self.secs:
            if re.search(r'pytani', s.text, re.I) and s.subs:
                return s
        return None

    def contact(self):
        s = self.secs[-1]
        if re.match(r'Jak umówi', s.text):
            return s
        return None

    def plain_text(self):
        return re.sub(r'\s+', ' ', self.content_text()).strip()

    def content_text(self):
        return self.soup.select_one('div.content').get_text(' ')


def inner(tag):
    """Wewnętrzny HTML węzła (z poprawionymi linkami)."""
    return tag.decode_contents()


def outer(tag):
    return str(tag)


def runin(li):
    """Etykieta run-in: <strong>Etykieta.</strong> reszta → (label_html, rest_html) albo (None, html)."""
    first = None
    for c in li.children:
        if isinstance(c, NavigableString) and not c.strip():
            continue
        first = c
        break
    if isinstance(first, Tag) and first.name == 'strong':
        lab = first.decode_contents()
        t = first.get_text()
        if re.search(r'[.:]\s*$', t) and len(t.split()) <= 6:
            rest = ''.join(str(x) for x in list(first.next_siblings))
            lab_clean = re.sub(r'[.:]\s*$', '', lab)
            return lab_clean, rest.lstrip()
    return None, li.decode_contents()


def table_rows(tbl):
    head = [th.decode_contents() for th in tbl.select('thead th')]
    rows = []
    for tr in tbl.select('tbody tr'):
        rows.append([c.decode_contents() for c in tr.find_all(['td', 'th'])])
    return head, rows
