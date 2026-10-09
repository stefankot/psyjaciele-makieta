# generated: psyjaciele-podstrony
"""strony.py — szkielet budowy stron: PageBuilder (PB), algorytm palet (§10A.1), dane meta (okruszki, powiązania).

Plany konkretnych stron (kolejność bloków, fakty, podziały tytułów) są w plany.py — tu nie ma ani jednego zdania treści.
"""
import re
from pathlib import Path

import bloki as B
from home import Rewriter
from zrodlo import Src

SLUGS_USLUGI = [
    'choroby-wewnetrzne-u-psow-i-kotow', 'diagnostyka-laboratoryjna-weterynaryjna',
    'szczepienia-oraz-profilaktyka-przeciwpasozytnicza', 'chirurgia-weterynaryjna-tkanek-miekkich',
    'kardiologia-weterynaryjna', 'diagnostyka-obrazowa-psow-i-kotow', 'okulistyka-weterynaryjna',
    'dermatologia-weterynaryjna', 'stomatologia-weterynaryjna', 'nefrologia-weterynaryjna',
    'urologia-weterynaryjna', 'pomiar-cisnienia-psow-i-kotow', 'wystawianie-paszportow-psom-i-kotom',
    'czipowanie-psow-i-kotow']
ALL_SLUGS = ['uslugi-weterynaryjne'] + SLUGS_USLUGI + ['zespol', 'polityka-prywatnosci']

# nazwy bazowe ilustracji hero (service-<nazwa>.png); slug → plik po stronie assets
HERO_ART = {
    'uslugi-weterynaryjne': 'assets/illustrations/sekcja-uslugi-c.png',
    'zespol': 'assets/illustrations/zespol-header-first-frame.png',
}

# mapa powiązań „Zobacz też” (maks. 4; tytuł i opis z kafla home)
RELATED = {
    'choroby-wewnetrzne-u-psow-i-kotow': ['diagnostyka-laboratoryjna-weterynaryjna', 'diagnostyka-obrazowa-psow-i-kotow', 'nefrologia-weterynaryjna', 'kardiologia-weterynaryjna'],
    'diagnostyka-laboratoryjna-weterynaryjna': ['choroby-wewnetrzne-u-psow-i-kotow', 'diagnostyka-obrazowa-psow-i-kotow', 'szczepienia-oraz-profilaktyka-przeciwpasozytnicza', 'nefrologia-weterynaryjna'],
    'szczepienia-oraz-profilaktyka-przeciwpasozytnicza': ['czipowanie-psow-i-kotow', 'wystawianie-paszportow-psom-i-kotom', 'choroby-wewnetrzne-u-psow-i-kotow'],
    'chirurgia-weterynaryjna-tkanek-miekkich': ['diagnostyka-obrazowa-psow-i-kotow', 'diagnostyka-laboratoryjna-weterynaryjna', 'stomatologia-weterynaryjna', 'choroby-wewnetrzne-u-psow-i-kotow'],
    'kardiologia-weterynaryjna': ['pomiar-cisnienia-psow-i-kotow', 'diagnostyka-obrazowa-psow-i-kotow', 'choroby-wewnetrzne-u-psow-i-kotow', 'nefrologia-weterynaryjna'],
    'diagnostyka-obrazowa-psow-i-kotow': ['choroby-wewnetrzne-u-psow-i-kotow', 'kardiologia-weterynaryjna', 'urologia-weterynaryjna', 'chirurgia-weterynaryjna-tkanek-miekkich'],
    'okulistyka-weterynaryjna': ['dermatologia-weterynaryjna', 'choroby-wewnetrzne-u-psow-i-kotow', 'pomiar-cisnienia-psow-i-kotow'],
    'dermatologia-weterynaryjna': ['choroby-wewnetrzne-u-psow-i-kotow', 'diagnostyka-laboratoryjna-weterynaryjna', 'okulistyka-weterynaryjna'],
    'stomatologia-weterynaryjna': ['chirurgia-weterynaryjna-tkanek-miekkich', 'choroby-wewnetrzne-u-psow-i-kotow', 'szczepienia-oraz-profilaktyka-przeciwpasozytnicza'],
    'nefrologia-weterynaryjna': ['urologia-weterynaryjna', 'pomiar-cisnienia-psow-i-kotow', 'diagnostyka-laboratoryjna-weterynaryjna', 'choroby-wewnetrzne-u-psow-i-kotow'],
    'urologia-weterynaryjna': ['nefrologia-weterynaryjna', 'diagnostyka-obrazowa-psow-i-kotow', 'diagnostyka-laboratoryjna-weterynaryjna', 'choroby-wewnetrzne-u-psow-i-kotow'],
    'pomiar-cisnienia-psow-i-kotow': ['kardiologia-weterynaryjna', 'nefrologia-weterynaryjna', 'choroby-wewnetrzne-u-psow-i-kotow'],
    'wystawianie-paszportow-psom-i-kotom': ['czipowanie-psow-i-kotow', 'szczepienia-oraz-profilaktyka-przeciwpasozytnicza'],
    'czipowanie-psow-i-kotow': ['szczepienia-oraz-profilaktyka-przeciwpasozytnicza', 'wystawianie-paszportow-psom-i-kotom'],
}

CYCLE = ['soft-a', 'mid-a', 'mid-c', 'mid-b', 'paper', 'soft-b']
GREEN_ROLES = ('alarm', 'booking')


class Item:
    def __init__(self, role, inner=None, html=None, sid=None, aria=None, cls=None, kind='chapter', tag=''):
        self.role, self.inner, self.html = role, inner, html
        self.sid, self.aria, self.cls, self.kind, self.tag = sid, aria, cls, kind, tag


class PB:
    def __init__(self, home, pages, slug, root):
        self.home, self.pages, self.slug, self.root = home, pages, slug, Path(root)
        self.rw = Rewriter(pages, slug)
        self.src = Src(slug, self.root, self.rw)
        from plany import TITLE_SPLIT
        self.ctx = B.Ctx(home, self.rw, self.src, slug, TITLE_SPLIT.get(slug, {}))
        self.ctx.cur_sec = ''
        self.items = []
        self.h1_id = 'tytul-strony'
        self.crumb_label = self.label_for_slug(slug)
        self.faq_data = None
        self._flip = False
        self.toc_ids = [e['id'] for e in self.src.toc]

    # ------------------------------------------------------------------
    def label_for_slug(self, slug):
        t = {x['slug']: x['title'] for x in self.home.tiles}
        return t.get(slug) or {'uslugi-weterynaryjne': 'Usługi', 'zespol': 'Zespół', 'polityka-prywatnosci': 'Polityka prywatności'}[slug]

    def S(self, key):
        """Sekcja/podsekcja źródła po prefiksie id (musi być jednoznaczny)."""
        c = [k for k in self.src.by_id if k == key] or [k for k in self.src.by_id if k.startswith(key)]
        assert len(c) == 1, f'{self.slug}: klucz „{key}” → {c}'
        return self.src.by_id[c[0]]

    def num(self, sec):
        try:
            return self.toc_ids.index(sec.id) + 1
        except ValueError:
            return None

    def mark(self, *secs):
        for s in secs:
            for n in s.all_nodes():
                self.ctx.used_nodes.add(id(n))
            self.ctx.used_nodes.add(('sec', s.id))

    def flip(self):
        self._flip = not self._flip
        return self._flip

    # --- sekcje --------------------------------------------------------
    def add(self, role, inner=None, **kw):
        it = Item(role, inner=inner, **kw)
        self.items.append(it)
        return it

    def begin(self, sec):
        self.ctx.cur_sec = sec.id if sec else ''
        self.ctx.cur_title = B.plain(sec.title) if sec else ''

    def head(self, sec, lead=False, level=2, forced=None):
        lead_html = None
        if lead and sec.nodes and sec.nodes[0].name == 'p' and len(sec.nodes[0].get_text()) <= 240:
            lead_html = sec.nodes[0].decode_contents()
            self._lead_taken = sec.nodes[0]
        else:
            self._lead_taken = None
        return B.section_head(self.ctx, self.num(sec), sec, lead_html, level, forced)

    def chapter(self, sec, body, aside='', reverse=None, role=None, lead_head=False, tag='', sticky=True, cls_extra=''):
        """N6: aside = nagłówek rozdziału (+ opcjonalnie obraz), body = treść."""
        self.begin(sec)
        r = self.flip() if reverse is None else reverse
        head = self.head(sec, lead=lead_head)
        inner = B.split_feature(self.ctx, head + aside, body, reverse=r, cls=cls_extra)
        return self.add(role, inner, aria=sec.id, tag=tag)

    def wide(self, sec, body, role=None, lead_head=False, tag='', before=''):
        self.begin(sec)
        head = self.head(sec, lead=lead_head)
        inner = f'{head}{before}{body}'
        return self.add(role, inner, aria=sec.id, tag=tag)

    def body_nodes(self, nodes, skip=None):
        """Domyślne renderowanie węzłów (p/ul/ol/table)."""
        return ''.join(B._node_html(self.ctx, n) for n in nodes if n is not skip)

    # --- standardowe sekcje --------------------------------------------
    def hero(self, facts, kick='Usługa', no_art=False, art=None, hid=None, mask=False):
        ctx, src = self.ctx, self.src
        rw = self.rw
        if self.slug in ('uslugi-weterynaryjne', 'zespol', 'polityka-prywatnosci'):
            crumbs = [('Strona główna', rw.home_link()), (self.crumb_label, None)]
        else:
            crumbs = [('Strona główna', rw.home_link()), ('Usługi', rw.page_link('uslugi-weterynaryjne')), (self.crumb_label, None)]
        # bez okruszków i etykiety nad tytułem; zamiast nich strzałka powrotu po lewej stronie tytułu
        crumbs, kick = None, None
        back = (rw.home_link(), 'Wróć na stronę główną')   # strzałka zawsze prowadzi na stronę główną (polecenie właściciela)
        art_html = ''
        if not no_art:
            from obrazy import HERO_ID, OBRAZY
            ctx.cur_sec = 'poczatek'
            tile = next((x for x in self.home.tiles if x['slug'] == self.slug), None)
            if tile:   # strony usług: ilustracja z kafla usługi na stronie głównej (polecenie użytkownika)
                art_html = B.art_figure(ctx, tile['img'], ratio='1', alt='', eager=True, w=800, h=800)
            else:
                hero_file = OBRAZY[HERO_ID[self.slug]]['plik']
                if (self.root / hero_file).exists():   # gotowa ilustracja hero: kreska --ink na tle sekcji, jak na stronach usług
                    art_html = B.art_figure(ctx, hero_file, ratio='1', alt='', eager=True, w=1024, h=1024)
                else:
                    art_html = f'<div class="poster-art hero-placeholder">{B.photo_frame(ctx, HERO_ID[self.slug], ratio="1/1", role="hero")}</div>'
        fs = ''   # pasek faktów usunięty na polecenie użytkownika (8.10.2026)
        h1 = src.h1.decode_contents()
        html = B.page_hero(ctx, crumbs, kick, h1, src.lead, src.cta, art_html, fs, hid=self.h1_id,
                           forced=ctx.title_split('h1'), no_art=no_art, back=back)
        self.items.append(Item('top', html=html, kind='hero'))
        if src.intro_extra:
            self.ctx.pending_intro = src.intro_extra

    def hero_art_path(self):
        import posixpath
        if self.slug in HERO_ART:
            return HERO_ART[self.slug]
        t = next(x for x in self.home.tiles if x['slug'] == self.slug)
        base = re.sub(r'-[abc]\.png$', '.png', t['img'])
        return base if (self.root / base).exists() else t['img']

    def toc(self):
        html = B.toc_index(self.ctx, self.src.toc)
        it = self.add('toc', html, aria='toc-title', kind='toc')
        return it

    def faq(self, sec=None, mode=None):
        sec = sec or self.src.faq()
        self.begin(sec)
        n = len(sec.subs)
        mode = mode or ('columns' if B.faq_is_columns(sec) else 'accordion')
        head = B.section_head(self.ctx, self.num(sec), sec, None, 2, self.ctx.title_split(sec.id))
        if mode == 'columns':
            body = B.faq_columns(self.ctx, sec)
        else:
            body = B.faq_accordion(self.ctx, sec)
        self.faq_data = [(s.id, B.plain(s.title), ''.join(str(x) for x in s.nodes)) for s in sec.subs]
        inner = f'{head}{body}'
        if mode == 'accordion' and self.slug in SLUGS_USLUGI:
            # baner „Praca w Psyjaciołach” na końcu sekcji: 8 kolumn, zdjęcie u góry
            jobs = Src('zespol', self.root, self.rw).by_id['praca-w-psyjaciolach']
            banner = B.join_banner(self.ctx, jobs.title, jobs.nodes, B.join_art_shared(self.ctx), 'mailto:kontakt@psyjacielevet.pl',
                                   hid='praca-w-psyjaciolach')
            inner = f'{head}{body}{banner}'
        self.add('paper', inner, aria=sec.id, cls='arrival preparation faq', kind='faq')

    def related(self):
        rel = RELATED.get(self.slug)
        if not rel:
            return
        self.ctx.cur_sec = 'zobacz-tez'
        self.ctx.use('related-tiles')
        inner = (f'<header class="section-head">'
                 f'<h2 id="zobacz-tez"><em>Kolejne usługi</em></h2></header>{B.related_tiles(self.ctx, rel)}')
        self.add(None, inner, aria='zobacz-tez', kind='related')

    def booking(self):
        self.items.append(Item('booking', html=B.booking_section(self.ctx), kind='booking'))

    def contact(self, sec=None):
        sec = sec or self.src.contact()
        self.begin(sec)
        self.items.append(Item('end', html=B.contact_section(self.ctx, sec), kind='contact'))

    # --- palety ------------------------------------------------------------
    def surface(self, role):
        r = self.home.roles
        if role == 'social':
            return r['mid-c']['--surface']
        return r[role]['--surface']

    def finish(self):
        items = self.items
        # „Poza godzinami pracy” pod sekcją „Jak umówić …”, w kolumnie artykułu (spis treści nie jest przerywany)
        ah = [it for it in items if it.kind == 'after-hours']
        ct = [it for it in items if it.kind == 'contact']
        if ah and ct:
            items.remove(ah[0])
            items.insert(items.index(ct[0]) + 1, ah[0])
            ah[0].role = None
        ptr = 0
        for i, it in enumerate(items):
            if it.role is not None:
                continue
            prev = self.surface(items[i - 1].role) if i else None
            nxt = self.surface(items[i + 1].role) if i + 1 < len(items) and items[i + 1].role else None
            for k in range(len(CYCLE)):
                cand = CYCLE[(ptr + k) % len(CYCLE)]
                s = self.surface(cand)
                if s != prev and s != nxt:
                    it.role = cand
                    ptr = (ptr + k + 1) % len(CYCLE)
                    break
            else:
                raise RuntimeError(f'{self.slug}: brak palety dla sekcji {i}')
        for a, b in zip(items, items[1:]):
            assert self.surface(a.role) != self.surface(b.role), f'{self.slug}: sąsiednie sekcje o tej samej powierzchni ({a.role}/{b.role})'
        # spis treści: wpis „Opinie opiekunów” po „Najczęstsze pytania” (sekcja jest w kolumnie artykułu)
        if any(it.kind in ('reviews', 'after-hours') for it in items) and any(it.kind == 'toc' for it in items):
            toc2 = []
            for e in self.src.toc:
                toc2.append(e)
                if (any(it.kind == 'reviews' for it in items) and re.search(r'najczęstsze pytania', e['text'], re.I)
                        and not any(x['id'] == 'section-title-6' for x in self.src.toc)):
                    toc2.append({'id': 'section-title-6', 'text': 'Opinie opiekunów', 'subs': []})
            if any(it.kind == 'after-hours' for it in items) and not any(x['id'] == 'after-hours-title' for x in toc2):
                toc2.append({'id': 'after-hours-title', 'text': 'Poza godzinami pracy', 'subs': []})
            if len(toc2) > len(self.src.toc):
                self.src.toc = toc2
                for it in items:
                    if it.kind == 'toc':
                        it.html = None
                        it.inner = B.toc_index(self.ctx, toc2)
        green = sum(1 for it in items if it.role in GREEN_ROLES)
        self.green_count = green
        out = []
        for it in items:
            if it.html is not None:
                out.append((it, it.html))
                continue
            cls = it.cls or self.home.role_class[it.role]
            if it.kind == 'toc':
                cls += ' toc-mobile'   # wersja dla wąskich okien; od 1001 px spis jest lewą szpaltą (toc-rail)
            out.append((it, B.section(self.ctx, cls, it.inner, sid=it.sid, aria=it.aria, label=self.home.label_for(cls))))
        # artykuły: kolumna po prawej (kol. 5–12), po lewej przyklejony spis treści (kol. 1–4); sekcje „home” i pasma pełnej szerokości poza kolumną
        full = {'hero', 'toc', 'social', 'rail', 'about'}   # „doctors” (Kto przyjmuje) w kolumnie 8 kol., spis treści idzie do końca   # „reviews” (Opinie opiekunów) w kolumnie 8 kol. i w spisie treści
        toc_html = B.toc_rail(self.ctx, self.src.toc) if any(it.kind == 'toc' for it, _ in out) else ''
        res, cur = [], []
        def flush():
            nonlocal cur, toc_html
            if cur:
                rail, toc_html = toc_html, ''
                res.append(f'<div class="page-columns">{rail}{"".join(cur)}</div>')
                cur = []
        for it, html in out:
            if it.kind in full:
                flush()
                res.append(html)
            else:
                cur.append(html)
        flush()
        # na desktopie (toc ukryty) pierwsza sekcja po hero nie może mieć tej samej powierzchni co hero
        vis = [it for it in items if it.kind != 'toc']
        for a, b in zip(vis, vis[1:]):
            assert self.surface(a.role) != self.surface(b.role), f'{self.slug}: po ukryciu spisu sąsiednie sekcje o tej samej powierzchni ({a.role}/{b.role})'
        out = res
        self.roles_used = [it.role for it in items]
        return '\n'.join(out)
