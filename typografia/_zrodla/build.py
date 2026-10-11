# -*- coding: utf-8 -*-
"""Generator typografia/zasady.html (Etap 3). Uruchom: python3 build.py [ścieżka_wyjściowa]"""
import re, sys, html, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from texts import plfix_html, plfix
from k1 import K1
from k2 import K2, CDN, HYPH_INIT, HELPERS, FONT_WOFF

ROOT = os.path.dirname(HERE)          # katalog typografia/
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'zasady.html')
esc = html.escape

# ------------------------------------------------------------------ dane z katalogu i klasyfikacji
RULES = {}
for l in open(os.path.join(ROOT, 'katalog.md'), encoding='utf-8'):
    m = re.match(r'^\| ([MAW]-\d+) \|', l)
    if not m:
        continue
    c = [x.strip() for x in l.strip().strip('|').split('|')]
    RULES[c[0]] = dict(id=c[0], lvl=c[1], group=c[2], text=' | '.join(c[3:-2]), src=c[-2], note=c[-1])
assert len(RULES) == 288, len(RULES)

kl = open(os.path.join(ROOT, 'klasyfikacja.md'), encoding='utf-8').read()
def table_rows(prefix):
    rows = []
    for l in kl.split('\n'):
        if l.startswith('| ' + prefix):
            rows.append([x.strip() for x in l.strip().strip('|').split(' | ')] if False else [x.strip() for x in l.strip().strip('|').split('|')])
    return rows
P1T, P2T, K3T = {}, {}, []
for c in table_rows('P1-'):
    P1T[c[0]] = dict(name=c[1], rules=c[2], tech=' | '.join(c[3:-3]), sup=c[-3], fb=c[-2], unote=c[-1])
for c in table_rows('P2-'):
    P2T[c[0]] = dict(name=c[1], rules=c[2], tech=' | '.join(c[3:-4]), waga=c[-4], cost=c[-3], risk=c[-2], when=c[-1])
sec8 = kl.split('## 8.')[1].split('## 9.')[0]
for l in sec8.split('\n'):
    m = re.match(r'^\| ([MAW]-\d+) \| (.*?) \| (.*) \|$', l)
    if m:
        K3T.append((m.group(1), m.group(3)))
assert len(P1T) == 24 and len(P2T) == 24, (len(P1T), len(P2T))
R1 = []
sec9 = kl.split('## 9.')[1].split('## 10.')[0]
for l in sec9.split('\n'):
    if l.startswith('| R1-'):
        c = [x.strip() for x in l.strip().strip('|').split('|')]
        R1.append(dict(id=c[0], name=c[1], rules=c[2], tech=c[3], sup=c[4], note=c[5]))
assert len(R1) == 17

def rule_ids(s):
    head = s.split('poza pokazem')[0]
    return re.findall(r'[MAW]-\d+', head)

def sources(ids):
    """Źródła z wierszy katalogu; strony tej samej książki i rozdziału scalone (B 2.1.2, s. 26–27)."""
    def expand(txt):
        pg = set()
        for part in [x.strip() for x in txt.split(',') if x.strip()]:
            if '–' in part:
                a, b = part.split('–')
                pg.update(range(int(a), int(b) + 1))
            else:
                pg.add(int(part))
        return pg
    def compress(pg):
        pg = sorted(pg); runs = []
        for p in pg:
            if runs and p == runs[-1][1] + 1:
                runs[-1][1] = p
            else:
                runs.append([p, p])
        return ', '.join(str(a) if a == b else '%d–%d' % (a, b) for a, b in runs)
    order, pages, raw = [], {}, []
    for i in ids:
        cell = RULES[i]['src'].strip()
        for s in [x.strip() for x in cell.split(';') if x.strip()]:
            if re.match(r'^\d+(?:\.\d+)*, s\.', s):
                s = 'B ' + s                                   # „8.1, s. 143” po „B 8.3.1, s. 160;” dotyczy tej samej książki
            m = re.match(r'^(B \d+(?:\.\d+)*(?:, \d+(?:\.\d+)*)*),? s\. ([\d–, ]+)$', s) or re.match(r'^(L(?:·\w+)?) s\. ([\d–, ]+)$', s)
            if m:
                key = m.group(1)
                if key not in pages:
                    pages[key] = set(); order.append(key)
                pages[key] |= expand(m.group(2))
            elif s not in raw:
                raw.append(s)
    out = [('%s, s. %s' % (k, compress(pages[k]))) if k.startswith('B') else ('%s s. %s' % (k, compress(pages[k]))) for k in order]
    return out + raw

def tag_html(s):
    return plfix(esc(s))

def rich(s):
    return re.sub(r'`([^`]+)`', r'<code>\1</code>', tag_html(s))

def code_html(src):
    return esc(src)

# ------------------------------------------------------------------ CSS demonstracyjny (okna „Przed” i „Po”)
def scoped(card, pane, css):
    """CSS z karty trafia do okna przez zagnieżdżony selektor; instrukcje @layer a, b; wynosimy na wierzch."""
    top, body = [], []
    for line in css.split('\n'):
        if re.match(r'^@layer [\w\s,-]+;\s*$', line):
            top.append(line)
        else:
            body.append(line)
    out = '\n'.join(top)
    b = '\n'.join(body).strip()
    if b:
        out += '\n#%s .%s {\n%s\n}\n' % (card, pane, b)
    return out

def demo_css(card):
    parts = []
    if card.get('base'):
        parts.append('/* %s: wspólne */\n%s' % (card['id'], scoped(card['id'], 'pane', card['base'])))
    if card.get('before'):
        parts.append(scoped(card['id'], 'before', card['before']))
    if card.get('css'):
        parts.append(scoped(card['id'], 'after', card['css']))
    return '\n'.join(parts)

# ------------------------------------------------------------------ karty
SUP_LABEL = {'pelne': 'wsparcie pełne', 'czesciowe': 'wsparcie częściowe', 'ograniczone': 'wsparcie ograniczone'}
COST_LABEL = {'niski': 'koszt niski', 'średni': 'koszt średni', 'wysoki': 'koszt wysoki'}
COST_CLASS = {'niski': 'niski', 'średni': 'sredni', 'wysoki': 'wysoki'}

def rules_details(ids):
    rows = ''.join('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
        r, esc(RULES[r]['lvl']), tag_html(RULES[r]['text']), tag_html(RULES[r]['src'])) for r in ids)
    return ('<details class="kod"><summary>Zasady z katalogu (%d)</summary><div class="tablewrap"><table class="k3 rules">'
            '<thead><tr><th>ID</th><th>Poziom</th><th>Zasada</th><th>Źródło</th></tr></thead><tbody>%s</tbody></table></div></details>' % (len(ids), rows))

def stat_span(kind):
    return '<span class="stat" data-stat="%s" aria-live="polite"></span>' % kind

def tools_html(tools):
    out = []
    for t in tools:
        if t['type'] == 'toggle':
            out.append('<label><input type="checkbox" data-toggle-class="%s"> %s</label>' % (t['cls'], esc(t['label'])))
        elif t['type'] == 'range':
            out.append('<label>%s <input type="range" min="%s" max="%s" value="%s" data-var="%s" data-unit="%s"> <output>%s %s</output></label>' % (
                esc(t['label']), t['min'], t['max'], t['value'], t['var'], t['unit'], t['value'], t['unit']))
    return '<div class="tools">%s</div>' % ''.join(out) if out else ''

def sample_html(inner, sample_cls, own_tekst=False, cols=False):
    ov = '<div class="overlay" aria-hidden="true">%s</div>' % ('<i></i>' * 12) if cols else ''
    body = inner if own_tekst else '<div class="tekst">%s</div>' % inner
    return '<div class="sample %s">%s%s</div>' % (sample_cls, body, ov)

def k1_card(c):
    t = P1T[c['id']]
    ids = rule_ids(t['rules'])
    srcs = sources(ids)
    inner_a = plfix_html(c.get('after_html') or c['html'])
    inner_b = plfix_html(c.get('before_html') or c['html'])
    own = c['id'] in ('P1-13', 'P1-22')
    cols = c['id'] == 'P1-21'
    sample_cls = c.get('sample', '')
    stat_b = ''.join(stat_span(s) for s in c['stats'] if s != 'hyph') if c['stats'] else ''
    stat_a = ''.join(stat_span(s) for s in c['stats'])
    code_after = (('/* wspólne dla obu okien */\n' + c['base'] + '\n\n') if c['base'] else '') + c['css']
    code_before = (('/* wspólne dla obu okien */\n' + c['base'] + '\n\n') if c['base'] else '') + c['before'] if c['before'] else ''
    codes = '<div class="codes"><figure><figcaption>Kod okna „Po” (ten sam, który działa poniżej)</figcaption><pre class="code"><code>%s</code></pre></figure></div>' % code_html(code_after)
    before_code = ''
    if c['before']:
        before_code = ('<details class="kod"><summary>Kod okna „Przed”</summary><pre class="code"><code>%s</code></pre></details>' % code_html(c['before']))
    stack = ' stack' if c['wide'] else ''
    sup = c['sup']
    badges = '<span class="tag">%s</span><span class="tag">kategoria 1</span><span class="badge %s">%s</span>' % (c['lvl'], sup, SUP_LABEL[sup])
    meta = (
        '<dl class="meta">'
        '<div class="full"><dt>Uzasadnienie</dt><dd>%s</dd></div>'
        '<div><dt>Zasady z katalogu</dt><dd>%s</dd></div>'
        '<div><dt>Źródło</dt><dd>%s</dd></div>'
        '<div><dt>Technika</dt><dd>%s</dd></div>'
        '<div><dt>Wsparcie (Chrome / Safari / Firefox)</dt><dd>%s</dd></div>'
        '<div class="full"><dt>Fallback</dt><dd>%s</dd></div>'
        '</dl>' % (rich(c['why']), esc(', '.join(ids)), tag_html('; '.join(srcs)),
                   rich(t['tech']), tag_html(t['sup']), rich(t['fb'])))
    toggle_in = ''
    demo = (
        '<div class="demo%s">'
        '<figure class="pane before"><figcaption><span>Przed</span>%s</figcaption>%s</figure>'
        '<figure class="pane after"><figcaption><span>Po</span>%s</figcaption>%s</figure></div>' % (
            stack, stat_b, sample_html(inner_b, sample_cls, own, cols), stat_a, sample_html(inner_a, sample_cls, own, cols)))
    note = '<p class="note">%s</p>' % plfix(re.sub(r'`([^`]+)`', r'<code>\1</code>', esc(c['note']))) if c['note'] else ''
    status = '<p class="status" data-status-for="%s" aria-live="polite"></p>' % c['id'] if c['id'] in ('P1-12', 'P1-14') else ''
    return ('<article class="pt" id="%s" data-lvl="%s" data-cat="1"><header><span class="id">%s</span><h4>%s</h4><p class="badges">%s</p></header>%s%s%s%s%s%s%s%s</article>' % (
        c['id'], c['lvl'], c['id'], tag_html(t['name']), badges, meta, rules_details(ids), codes, before_code, tools_html(c['tools']),
        demo, status, note))

def k2_card(c):
    t = P2T[c['id']]
    ids = rule_ids(t['rules'])
    srcs = sources(ids)
    cost = t['cost'].strip()
    libs = c['libs']
    code = c['apply']
    head = ''
    if libs:
        head += '/* biblioteki z CDN (wersje przypięte):\n' + ''.join(' * %s\n' % CDN[l] for l in libs) + ' */\n'
    if 'hyphenopoly' in libs:
        head += '/* inicjalizacja Hyphenopoly po załadowaniu loadera */\n' + HYPH_INIT + '\n\n'
    if c.get('uses_helper'):
        head += '/* funkcja pomocnicza (patrz „Wspólne” na początku sekcji) */\n'
    code_show = head + '/* reguła */\nconst regula = ' + code + ';'
    badges = '<span class="tag">%s</span><span class="tag">kategoria 2</span><span class="badge %s">%s</span>' % (
        c['lvl'], COST_CLASS[cost], COST_LABEL[cost])
    meta = (
        '<dl class="meta">'
        '<div class="full"><dt>Uzasadnienie</dt><dd>%s</dd></div>'
        '<div><dt>Zasady z katalogu</dt><dd>%s</dd></div>'
        '<div><dt>Źródło</dt><dd>%s</dd></div>'
        '<div><dt>Rozwiązanie i wymagania</dt><dd>%s</dd></div>'
        '<div><dt>Waga</dt><dd>%s</dd></div>'
        '<div><dt>Koszt i ryzyka</dt><dd>%s</dd></div>'
        '<div><dt>Kiedy się opłaca</dt><dd>%s</dd></div>'
        '</dl>' % (rich(c['why']), esc(', '.join(ids)), tag_html('; '.join(srcs)),
                   rich(t['tech']), rich(t['waga']), rich(t['risk']), rich(t['when'])))
    controls = ['<button type="button" data-act="toggle" aria-pressed="false">Zastosuj regułę</button>']
    if c['marks']:
        controls.append('<label><input type="checkbox" data-act="marks"> Pokaż znaki niełamliwe</label>')
    for tl in c['tools']:
        if tl['type'] == 'toggle':
            controls.append('<label><input type="checkbox" data-toggle-class="%s"> %s</label>' % (tl['cls'], esc(tl['label'])))
    controls_html = '<div class="tools">%s</div>' % ''.join(controls)
    stack = ' stack' if c['wide'] else ''
    sample_cls = c.get('sample', '')
    raw = c['raw']
    demo = (
        '<div class="demo%s">'
        '<figure class="pane before"><figcaption><span>Przed</span></figcaption>%s</figure>'
        '<figure class="pane after"><figcaption><span>Po</span><span class="stat" data-stat="k2delta" aria-live="polite"></span></figcaption>%s</figure></div>' % (
            stack, sample_html(raw, sample_cls), sample_html(raw, sample_cls)))
    if c['id'] == 'P2-16':
        pass
    status = '<p class="status" data-k2-status aria-live="polite">Reguła zostanie zastosowana automatycznie po przewinięciu do tej karty.</p>'
    note = '<p class="note">%s</p>' % plfix(re.sub(r'`([^`]+)`', r'<code>\1</code>', esc(c['note']))) if c['note'] else ''
    css_code = ''
    if c['base'] or c['css']:
        css_all = (('/* wspólne dla obu okien */\n' + c['base'] + '\n\n') if c['base'] else '') + c['css']
        css_code = '<figure><figcaption>CSS okna „Po”</figcaption><pre class="code"><code>%s</code></pre></figure>' % code_html(css_all.strip())
    codes = ('<div class="codes%s"><figure><figcaption>Kod (ten sam, który wykonuje przycisk)</figcaption><pre class="code"><code>%s</code></pre></figure>%s</div>' % (
        ' two' if css_code else '', code_html(code_show), css_code))
    return ('<article class="pt k2" id="%s" data-lvl="%s" data-cat="2"><header><span class="id">%s</span><h4>%s</h4><p class="badges">%s</p></header>%s%s%s%s%s%s%s</article>' % (
        c['id'], c['lvl'], c['id'], tag_html(P2T[c['id']]['name']), badges, meta, rules_details(ids), codes, controls_html, demo, status, note))

def filters(target, items):
    n = {'mikro': 0, 'makro': 0, 'własne': 0}
    for c in items:
        n[c['lvl']] += 1
    btns = ['<button type="button" data-lvl="all" aria-pressed="true">Wszystkie (%d)</button>' % len(items)]
    for l in ('mikro', 'makro', 'własne'):
        btns.append('<button type="button" data-lvl="%s" aria-pressed="false">%s (%d)</button>' % (l, l.capitalize(), n[l]))
    return n, '<div class="filters" role="group" aria-label="Filtr poziomu" data-target="%s">%s</div>' % (target, ''.join(btns))

# ------------------------------------------------------------------ K3 i „poza katalogiem”
def k3_table():
    rows = []
    for i, why in K3T:
        r = RULES[i]
        rows.append('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (i, esc(r['lvl']), tag_html(r['text']), tag_html(why)))
    return ('<div class="tablewrap" tabindex="0" role="region" aria-label="Tabela zasad niemożliwych w sieci"><table class="k3">'
            '<thead><tr><th>ID</th><th>Poziom</th><th>Zasada</th><th>Dlaczego niemożliwe i najbliższe przybliżenie</th></tr></thead><tbody>%s</tbody></table></div>' % ''.join(rows))

POZA = [
    ('Zasady nadrzędne i postawy', 'B 1.1–1.3, 2.4.11, 8.8.1, 9.6, 10.2',
     'Typografia ma służyć treści, tekst czyta się przed projektowaniem, a każdą zasadę, która nie służy tekstowi, należy porzucić. To pewniki bez kryterium, które da się sprawdzić na stronie; nie ma ich jak przełączyć ani zmierzyć.'),
    ('Historia stylów i technologii składu', 'B rozdz. 7 (poza listą cech stylów); L s. 10–35',
     'Opisuje, jak powstawały kroje i style w czasie; wiedza kulturowa, nie reguła. Z rozdziału 7 przeniesiono tylko cechy stylów, które wpływają na dobór kroju.'),
    ('Przegląd krojów, odlewnie, projektanci, tablice znaków', 'B rozdz. 11 i dodatki A, C–E',
     'Katalog krojów i ich twórców jest materiałem informacyjnym. Dobór kroju jest decyzją projektanta (w tym demo: Source Serif 4), a nie przełączanym parametrem.'),
    ('Lettering, logotypy i projektowanie fontów', 'L s. 64–71, 76–79',
     'Dotyczy rysowania liter, nie składu tekstu. Strona używa gotowego fontu; kreślenie liter byłoby osobnym zadaniem.'),
    ('Nowe ortografie i alfabety', 'B 6.7',
     'Zachowano jako pojedynczy wiersz (M-153, kategoria 3). Nie dotyczy polskiego pisma.'),
    ('Proces redakcyjny i korekta', 'L s. 212–217',
     'Przebieg redakcji, symbole korektorskie i dostarczanie tekstu autorom to organizacja pracy, nie wygląd strony. Zachowano tylko oczyszczanie tekstu przed składem (P2-23).'),
    ('Eseje o tekście, autorstwie i liniowości', 'L s. 87–101, 106–107, 118–119, 144–147, 202–203, 206',
     'Rozważania teoretyczne i ćwiczenia. Zachowano wyłącznie wnioski o ekranie, które weszły do zasad „własnych”.'),
]

REASONS = [
    (30, 'Nadwyżka kategorii 1 ponad X = 24', 'wymieniono w rezerwie R1 (poniżej); można włączyć na życzenie'),
    (24, 'Dotyczy kodu, builda lub prawa', 'np. subsetting fontów, licencje, struktura dokumentu; nie wpływa na wygląd samego tekstu'),
    (22, 'Niemożliwe w sieci (kategoria 3)', 'przybliżenia w sekcji „Niemożliwe w sieci”'),
    (18, 'Decyzja o doborze kroju lub cecha fontu', 'wybór kroju i jego rysunek należą do projektanta, nie do przełącznika'),
    (12, 'Dubluje inny punkt lub wynika z niego', 'ta sama reguła jest już w punkcie pokazu'),
    (12, 'Poza zakresem demo', 'inny język, rzadki kontekst, niski zysk, brak algorytmu'),
    (11, 'Metoda, postawa lub informacja', 'nie jest pojedynczą regułą do przełączenia'),
    (6, 'Odrzucone lub rozstrzygnięte w konflikcie', 'zob. rozstrzygnięcia K-01 – K-09 w klasyfikacja.md'),
]

def poza_html():
    li = ''.join('<li><b>%s</b><p><span class="src">%s</span><br>%s</p></li>' % (tag_html(a), tag_html(b), tag_html(c)) for a, b, c in POZA)
    reasons = ''.join('<tr><td>%d</td><td>%s</td><td>%s</td></tr>' % (n, tag_html(a), tag_html(b)) for n, a, b in REASONS)
    r1 = ''.join('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (r['id'], rich(r['name']), rich(r['tech']), rich(r['note'])) for r in R1)
    return (
        '<h3 class="sub">Czego książki dotyczą, a co nie zmienia się w regułę</h3><ul class="poza-list">%s</ul>'
        '<h3 class="sub">Zasady katalogu, które nie weszły do pokazu</h3><p class="what">W katalogu jest 288 zasad; do punktów pokazu weszło 153, a 135 zostało poza nim z powodami poniżej. '
        'Szczegóły każdej zasady są w tabeli klasyfikacji (klasyfikacja.md, sekcja 5).</p>'
        '<div class="tablewrap"><table class="k3"><thead><tr><th>Zasad</th><th>Powód</th><th>Co to znaczy</th></tr></thead><tbody>%s</tbody></table></div>'
        '<h3 class="sub">Rezerwa kategorii 1 (R1-01 – R1-17)</h3><p class="what">Punkty, które da się zrobić samym CSS, ale nie zmieściły się w limicie 24; do włączenia na życzenie.</p>'
        '<div class="tablewrap"><table class="k3"><thead><tr><th>ID</th><th>Punkt</th><th>Technika</th><th>Uwagi</th></tr></thead><tbody>%s</tbody></table></div>' % (li, reasons, r1))

# ------------------------------------------------------------------ złożenie strony
n1, f1 = filters('k1-lista', K1)
n2, f2 = filters('k2-lista', K2)
LV = ['mikro', 'makro', 'własne']
def grouped(items, card, n):
    out = []
    for lv in LV:
        sel = sorted([c for c in items if c['lvl'] == lv], key=lambda c: c['id'])
        if not sel:
            continue
        out.append('<h3 class="grp" data-lvl="%s">%s <span>(%d)</span></h3>' % (lv, lv.capitalize(), len(sel)))
        out.extend(card(c) for c in sel)
    return '\n'.join(out)
k1_html = grouped(K1, k1_card, n1)
k2_html = grouped(K2, k2_card, n2)
css_demo = '\n'.join(demo_css(c) for c in K1) + '\n' + '\n'.join(demo_css(c) for c in K2 if c['base'] or c['css'])
page_css = open(os.path.join(HERE, 'page.css'), encoding='utf-8').read()

def k2_registry():
    out = ['const KP = {};']
    for c in K2:
        out.append('KP[%s] = { libs: %s, marks: %s, noinv: %s, apply: %s };' % (
            json.dumps(c['id']), json.dumps(c['libs']), 'true' if c['marks'] else 'false',
            'true' if int(c['id'][3:]) in (14, 15, 16, 17, 18, 19, 20, 21, 22, 24) else 'false', c['apply']))
    return '\n'.join(out)

LIB_JS = ('const LIB = {\n'
          '  typograf: { src: ["%s"] },\n'
          '  hyphenopoly: { src: ["%s"], init: function () {\n%s\n  } },\n'
          '  texlinebreak: { src: ["%s"] },\n'
          '  opentype: { src: ["%s"] },\n};' % (CDN['typograf'], CDN['hyphenopoly'], HYPH_INIT, CDN['texlinebreak'], CDN['opentype']))

app_js = open(os.path.join(HERE, 'app.js'), encoding='utf-8').read()

INTRO = ('Katalog zasad z dwóch książek (Ellen Lupton, „Thinking with Type”, wyd. 2, oraz Robert Bringhurst, „The Elements of Typographic Style”, wyd. 3) '
         'przełożony na praktykę stron internetowych. Każdy punkt ma działający przykład na własnym, wymyślonym tekście: okno „Przed” pokazuje stan domyślny, '
         'okno „Po” stan z regułą. Kod pod tytułem punktu jest tym samym kodem, który steruje oknem „Po”.')

LEGEND = [
    ('Poziomy', ['<b>mikro</b>: znak, wyraz, wiersz, akapit.', '<b>makro</b>: strona, siatka, układ, hierarchia.', '<b>własne</b>: reguły dopisane z kontekstu sieci (tabele, listy, render).']),
    ('Kategoria 1: CSS i HTML – wsparcie', ['<b>pełne</b>: działa w bieżących Chrome, Safari i Firefox.', '<b>częściowe</b>: brakuje jednej przeglądarki albo zależy od słownika.',
                                           '<b>ograniczone</b>: działa tylko w jednej przeglądarce; podano fallback.',
                                           'Wersje pochodzą z MDN browser-compat-data 8.1.5 (8.10.2026). Sprawdziłem tylko Chromium 156; Safari i Firefoksa nie testowałem.']),
    ('Kategoria 2: JavaScript, biblioteki, build – koszt', ['<b>niski</b>: kilkaset bajtów własnego kodu, mała szansa na regresję.', '<b>średni</b>: biblioteka lub kilkaset bajtów z ryzykiem wyjątków i dostępności.',
                                                          '<b>wysoki</b>: ciężka logika, przeliczanie przy zmianie rozmiaru, ryzyko kolizji z innym kodem.',
                                                          'Wagi „własnego kodu” są szacunkami z projektu, nie pomiarami.']),
    ('Kategoria 3: niemożliwe w sieci', ['Zasady związane z papierem, stroną, rozkładówką i ręczną korektą optyczną. Dla każdej podano najbliższe przybliżenie albo jego brak.']),
]

legend_html = ''.join('<div><h2>%s</h2>%s</div>' % (tag_html(h), ''.join('<p>%s</p>' % plfix_html(x) for x in ps)) for h, ps in LEGEND)

HTML = '''<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Zasady typografii w sieci</title>
<meta name="description" content="Zasady typografii z książek Lupton i Bringhursta przełożone na CSS, JavaScript i biblioteki, z żywymi przykładami przed i po.">
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="preload" as="font" type="font/woff2" crossorigin href="https://cdn.jsdelivr.net/gh/adobe-fonts/source-serif@4.005R/WOFF2/VAR/SourceSerif4Variable-Roman.ttf.woff2">
<style>
@layer page;
%(page_css)s
</style>
<style id="demo-css">
%(css_demo)s
</style>
</head>
<body>
<a class="skip" href="#glowna">Przejdź do treści</a>
<header class="top"><div class="wrap">
<p class="brand">Typografia w sieci · etap 3 z 4</p>
<h1>Zasady typografii w sieci</h1>
<p class="lead">%(intro)s</p>
<nav aria-label="Sekcje strony"><ul>
<li><a href="#k1"><b>%(n1)d</b><span>Kategoria 1: CSS i HTML</span></a></li>
<li><a href="#k2"><b>%(n2)d</b><span>Kategoria 2: JavaScript, biblioteki, build</span></a></li>
<li><a href="#k3"><b>%(n3)d</b><span>Kategoria 3: niemożliwe w sieci</span></a></li>
<li><a href="#poza"><b>Poza</b><span>Poza katalogiem i poza pokazem</span></a></li>
</ul></nav>
<div class="legend">%(legend)s</div>
</div></header>
<main id="glowna">
<section class="block" id="k1" aria-labelledby="k1-h"><div class="wrap">
<header><h2 id="k1-h">Kategoria 1: sam CSS i HTML</h2>
<p class="what">Reguły, które daje się wdrożyć bez JavaScriptu. Przy każdym podano wsparcie przeglądarek i fallback.</p>
<p class="counter" data-counter="k1-lista"><strong><span data-total>%(n1)d</span> punktów</strong><span>mikro %(n1a)d</span><span>makro %(n1b)d</span><span>własne %(n1c)d</span><span>widocznych: <b data-visible>%(n1)d</b></span></p>
%(f1)s</header>
<div id="k1-lista">
%(k1)s
</div></div></section>
<section class="block" id="k2" aria-labelledby="k2-h"><div class="wrap">
<header><h2 id="k2-h">Kategoria 2: JavaScript, biblioteki, build</h2>
<p class="what">Reguły wymagające własnego kodu, biblioteki z CDN albo przetwarzania tekstu. Przykłady uruchamiają się po przewinięciu do karty (biblioteki ładowane są wtedy z CDN, wersje przypięte); przycisk „Przywróć” cofa zmiany w DOM.</p>
<p class="counter" data-counter="k2-lista"><strong><span data-total>%(n2)d</span> punktów</strong><span>mikro %(n2a)d</span><span>makro %(n2b)d</span><span>własne %(n2c)d</span><span>widocznych: <b data-visible>%(n2)d</b></span></p>
%(f2)s
<details class="kod"><summary>Wspólne: funkcja pomocnicza używana w kilku punktach</summary><pre class="code"><code>%(helpers)s</code></pre></details>
</header>
<div id="k2-lista">
%(k2)s
</div></div></section>
<section class="block" id="k3" aria-labelledby="k3-h"><div class="wrap">
<header><h2 id="k3-h">Kategoria 3: niemożliwe w sieci</h2>
<p class="what">Zasady, których nie da się wdrożyć, bo sieć nie jest drukiem: nie ma stałego formatu, papieru, grzbietu, rozkładówki ani kontroli nad podziałem na strony. Przy każdej podano najbliższe przybliżenie.</p>
<p class="counter"><strong>%(n3)d zasad</strong><span>w tym 25 w pełni niemożliwych, 5 zasad mieszanych (część w kategorii 1)</span></p></header>
%(k3)s
</div></section>
<section class="block poza" id="poza" aria-labelledby="poza-h"><div class="wrap">
<header><h2 id="poza-h">Poza katalogiem i poza pokazem</h2>
<p class="what">Co książki mówią, a nie mieści się w żadnej zasadzie przekładalnej na stronę, oraz jakie zasady katalogu nie weszły do punktów pokazu.</p></header>
%(poza)s
</div></section>
</main>
<footer class="site"><div class="wrap">
<p><b>Stan przeglądarek i testów.</b> Dane o wsparciu: MDN browser-compat-data 8.1.5 z 8.10.2026 (bieżące wersje stabilne w zbiorze: Chrome 155, Safari 27, Firefox 157). Strona została sprawdzona w Chromium 156; Safari i Firefoksa nie testowałem, więc ich zachowanie opisano wyłącznie według MDN.</p>
<p><b>Biblioteki z CDN (jsDelivr, wersje przypięte).</b> Typograf 7.8.0, Hyphenopoly 6.1.0 (wzorce pl), tex-linebreak 0.9.0, opentype.js 2.0.0. Font: Source Serif 4 (Adobe, licencja OFL), wersja 4.005R.</p>
<p><b>Źródła.</b> Katalog zasad (katalog.md, 288 zasad), rekonstrukcja tabel Bringhursta (bringhurst-tabele.md) i klasyfikacja (klasyfikacja.md). Teksty przykładów są własne, zasady są parafrazami z podaniem miejsca w książce.</p>
</div></footer>
<script>
%(lib)s
%(registry)s
%(helper_js)s
%(app)s
</script>
</body>
</html>
'''

out = HTML % dict(
    page_css=page_css, css_demo=css_demo, intro=tag_html(INTRO), legend=legend_html,
    n1=len(K1), n2=len(K2), n3=len(K3T), n1a=n1['mikro'], n1b=n1['makro'], n1c=n1['własne'],
    n2a=n2['mikro'], n2b=n2['makro'], n2c=n2['własne'], f1=f1, f2=f2, k1=k1_html, k2=k2_html, k3=k3_table(),
    poza=poza_html(), helpers=esc(HELPERS), lib=LIB_JS, registry=k2_registry(), helper_js=HELPERS, app=app_js)
open(OUT, 'w', encoding='utf-8').write(out)
print('zapisano', OUT, len(out), 'bajtów')
