# -*- coding: utf-8 -*-
"""Generator typografia/pokaz.html (Etap 4). Uruchom: python3 pokaz_build.py [ścieżka_wyjściowa]
Wymaga: k1.py, k2.py, texts.py (dane punktów z Etapu 3), pokaz.css, pokaz_app.js, pokaz_tekst.html."""
import os, re, sys, json, html
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from texts import plfix
from k1 import K1
from k2 import K2, CDN, HYPH_INIT, FONT_WOFF

ROOT = os.path.dirname(HERE)
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'pokaz.html')
esc = html.escape

# ---- nazwy punktów z klasyfikacji (Etap 2) ------------------------------------------------
kl = open(os.path.join(ROOT, 'klasyfikacja.md'), encoding='utf-8').read()
NAMES = {}
for l in kl.split('\n'):
    m = re.match(r'^\| (P[12]-\d+) \| (.*?) \|', l)
    if m:
        NAMES[m.group(1)] = m.group(2).strip()
assert len(NAMES) == 48, len(NAMES)

def pierwsze_zdanie(s):
    s = re.sub(r'`([^`]+)`', r'\1', s)
    m = re.match(r'^(.{40,220}?[.;])\s', s + ' ')
    return (m.group(1) if m else s[:200]).strip()

def k2apply(pid):
    return next(c for c in K2 if c['id'] == pid)['apply']

# ---- zasady kategorii 2: faza, kolejność, biblioteki, kod -----------------------------------
# faza „tekst”: na odłączonej kopii oryginału; „dom”: na żywej treści (zwraca funkcję sprzątającą); „diag”: tylko raport
REG = {}
def reg(pid, faza, order, libs, code):
    REG[pid] = dict(faza=faza, order=order, libs=libs, code=code)

reg('P2-23', 'tekst', 10, ['typograf'], k2apply('P2-23'))
reg('P2-03', 'tekst', 20, [], k2apply('P2-03'))
reg('P2-04', 'tekst', 30, [], r'''function (el) {
  const ZAKRES = /(?<![\d-])(?!\d{2}-\d{3}(?!\d))(\d+)\s?[-–—]\s?(\d+)(?![\d-])/g;   // dwie liczby; bez kodów pocztowych (00-950)
  mapText(el, s => s.replace(ZAKRES, '$1–$2'));
}''')
reg('P2-05', 'tekst', 40, ['typograf'], k2apply('P2-05'))
reg('P2-06', 'tekst', 50, ['typograf'], k2apply('P2-06'))
reg('P2-07', 'tekst', 60, ['typograf'], k2apply('P2-07'))
reg('P2-02', 'tekst', 70, ['typograf'], k2apply('P2-02'))
reg('P2-08', 'tekst', 80, ['typograf'], k2apply('P2-08'))
reg('P2-09', 'tekst', 90, ['typograf'], k2apply('P2-09'))
reg('P2-01', 'tekst', 100, ['typograf'], k2apply('P2-01'))
reg('P2-11', 'tekst', 110, [], k2apply('P2-11'))
reg('P2-10', 'tekst', 120, [], r'''function (el) {
  const WYJATKI = new Set(['PL', 'UK', 'US']);                       // kody krajów zostają wersalikami
  const SKROT = /(?<!\p{L})\p{Lu}{2,}(?!\p{L})/gu;                   // 2+ wielkie litery obok siebie
  el.querySelectorAll('.glowny p, .lead').forEach(p => {             // nagłówki i podpisy pomijamy
    p.innerHTML = p.innerHTML.replace(/(>|^)([^<]+)/g, (m, g, txt) =>
      g + txt.replace(SKROT, s => WYJATKI.has(s) ? s : '<abbr class="akr">' + s + '</abbr>'));
  });
}''')
reg('P2-12', 'tekst', 130, [], r'''function (el) {
  el.querySelectorAll('.glowny p, .lead').forEach(p => {
    const t = p.lastChild;                                           // tylko gdy akapit kończy się tekstem
    if (t && t.nodeType === 3) t.nodeValue = t.nodeValue.replace(/\s(\S{1,4})\s*$/, '\xA0$1');
  });
}''')
reg('P2-13', 'tekst', 140, ['hyphenopoly'], r'''async function (el) {
  const h = await Hyphenopoly.hyphenators.pl;
  el.querySelectorAll('.glowny p, .lead').forEach(p => {
    const w = document.createTreeWalker(p, NodeFilter.SHOW_TEXT);
    for (let n; (n = w.nextNode()); ) n.nodeValue = h(n.nodeValue, '.hyph');   // wstawia U+00AD w środku wyrazów
  });
}''')

reg('P2-15', 'dom', 200, [], r'''async function (el) {
  await document.fonts.ready;
  const ctx = document.createElement('canvas').getContext('2d');
  const zmiany = [];
  el.querySelectorAll('.glowny p, .lead').forEach(p => {
    const t = p.firstChild;
    const m = t && t.nodeType === 3 && /^[„"«(\[‚]/.exec(t.nodeValue);   // znak otwierający
    if (!m) return;
    const cs = getComputedStyle(p);
    ctx.font = cs.fontStyle + ' ' + cs.fontWeight + ' ' + cs.fontSize + ' ' + cs.fontFamily;
    const s = document.createElement('span');
    s.className = 'wisi';
    s.textContent = m[0];
    s.style.marginInlineStart = -ctx.measureText(m[0]).width + 'px';        // szerokość znaku wystaje w margines
    t.nodeValue = t.nodeValue.slice(1);
    p.prepend(s);
    zmiany.push([p, s, t, m[0]]);
  });
  return () => zmiany.forEach(([p, s, t, z]) => { t.nodeValue = z + t.nodeValue; s.remove(); });
}''')
reg('P2-19', 'dom', 210, [], r'''function (el) {
  const orig = [];
  el.querySelectorAll('td.liczba').forEach(td => {
    orig.push([td, td.innerHTML]);
    const [c, u = ''] = td.textContent.trim().split(',');
    td.innerHTML = '<span class="c">' + c + '</span><span class="u">' + (u ? ',' + u : '') + '</span>';
  });
  const szer = Math.max(0, ...[...el.querySelectorAll('.liczba .u')].map(s => s.getBoundingClientRect().width));
  el.style.setProperty('--ulamek', szer + 'px');                             // wspólna szerokość części ułamkowej
  return () => { el.style.removeProperty('--ulamek'); orig.forEach(([td, h]) => { td.innerHTML = h; }); };
}''')
reg('P2-21', 'dom', 220, [], r'''function (el) {
  const nav = document.createElement('nav');
  nav.className = 'spis';
  nav.setAttribute('aria-label', 'Spis treści');
  const ol = document.createElement('ol');
  const nadane = [];
  [...el.querySelectorAll('.glowny h2, .glowny h3')].forEach((h, i) => {
    if (!h.id) { h.id = 'rozdz-' + (i + 1); nadane.push(h); }
    const li = document.createElement('li');
    li.innerHTML = '<a href="#' + h.id + '">' + h.textContent + '</a>';
    if (h.tagName === 'H3') li.style.marginInlineStart = '1.5em';
    ol.append(li);
  });
  nav.append(ol);
  (el.querySelector('.glowny') || el).prepend(nav);
  return () => { nav.remove(); nadane.forEach(h => h.removeAttribute('id')); };
}''')
reg('P2-18', 'dom', 230, [], r'''function (el) {
  const nr = [];
  el.querySelectorAll('.przypis').forEach((span, i) => {
    const sup = span.previousElementSibling && span.previousElementSibling.classList.contains('odsylacz') ? span.previousElementSibling : null;
    const nota = document.createElement('aside');
    nota.className = 'nota'; nota.id = 'nota-' + (i + 1); nota.setAttribute('role', 'note');
    nota.innerHTML = '<b>' + (i + 1) + '</b> ' + span.innerHTML;
    if (sup) { sup.textContent = i + 1; sup.setAttribute('aria-describedby', nota.id); }   // numeracja i powiązanie dla czytników ekranu
    span.hidden = true;
    el.append(nota);
    nr.push({ sup, nota, span });
  });
  const uloz = () => {
    let dol = 0;
    const baza = el.getBoundingClientRect().top;
    nr.forEach(({ sup, nota }) => {
      if (getComputedStyle(nota).position !== 'absolute') { nota.style.removeProperty('top'); return; }
      const gora = Math.max(sup ? sup.getBoundingClientRect().top - baza : 0, dol + 8);   // nie zachodzi na poprzednią
      nota.style.top = gora + 'px';
      dol = gora + nota.offsetHeight;
    });
  };
  uloz();
  const ro = new ResizeObserver(uloz);
  ro.observe(el);
  return () => { ro.disconnect(); nr.forEach(({ nota, span }) => { nota.remove(); span.hidden = false; }); };
}''')
reg('P2-14', 'dom', 240, ['hyphenopoly', 'texlinebreak'], r'''async function (el) {
  await document.fonts.ready;
  const h = await Hyphenopoly.hyphenators.pl;
  const hyphenate = w => h(w, '.hyph').split('\xAD');                        // sylaby dla tex-linebreak
  const ps = [...el.querySelectorAll('.glowny p')].filter(p => !p.children.length);   // bez złożonego inline
  const { justifyContent, unjustifyContent } = texLineBreak_lib;
  justifyContent(ps, hyphenate);
  let szer = el.clientWidth;
  const ro = new ResizeObserver(() => {
    if (el.clientWidth === szer) return;
    szer = el.clientWidth;
    ps.forEach(unjustifyContent);
    justifyContent(ps, hyphenate);
  });
  ro.observe(el);
  return () => { ro.disconnect(); ps.forEach(unjustifyContent); };
}''')
reg('P2-17', 'dom', 250, [], r'''function (el, ui) {
  const U = 8;                                                              // moduł siatki bazowej
  const dopasuj = () => {
    el.querySelectorAll('figure.obr').forEach(f => {
      f.style.marginBlockEnd = '0px';
      const h = f.getBoundingClientRect().height;
      f.style.marginBlockEnd = (Math.ceil(h / U) * U - h) + 'px';           // dopełnienie do wielokrotności U
    });
    const baza = el.getBoundingClientRect().top;
    const dp = [...el.querySelectorAll('figure.obr + p')].map(p => Math.round((p.getBoundingClientRect().top - baza) % U));
    ui.say('przesunięcie akapitów po obrazach względem siatki ' + U + ' px: ' + dp.join(' px, ') + ' px');
  };
  dopasuj();
  let szer = el.clientWidth;
  const ro = new ResizeObserver(() => { if (el.clientWidth !== szer) { szer = el.clientWidth; dopasuj(); } });
  ro.observe(el);
  return () => { ro.disconnect(); el.querySelectorAll('figure.obr').forEach(f => f.style.removeProperty('margin-block-end')); };
}''')
reg('P2-20', 'dom', 260, [], r'''function (el) {
  const zywa = document.createElement('div');
  zywa.className = 'zywa';
  zywa.setAttribute('aria-hidden', 'true');                                 // duplikat treści nagłówka
  el.prepend(zywa);
  const h = [...el.querySelectorAll('.glowny h2')];
  let rAF = 0;
  const ustaw = () => {
    rAF = 0;
    let i = 0;
    h.forEach((x, k) => { if (x.getBoundingClientRect().top <= 96) i = k; });   // ostatni nagłówek nad górną krawędzią okna
    zywa.textContent = '§ ' + (i + 1) + ' · ' + h[i].textContent;
  };
  const przy = () => { if (!rAF) rAF = requestAnimationFrame(ustaw); };
  ustaw();
  addEventListener('scroll', przy, { passive: true });
  return () => { removeEventListener('scroll', przy); cancelAnimationFrame(rAF); zywa.remove(); };
}''')
reg('P2-16', 'dom', 270, [], r'''function (el, ui) {
  const W = ui.layer;
  const rysuj = () => {
    W.querySelectorAll('.cnt').forEach(n => n.remove());
    const baza = W.getBoundingClientRect();
    const liczby = [];
    el.querySelectorAll('.glowny p, .lead').forEach(p => {
      const lh = parseFloat(getComputedStyle(p).lineHeight) || 24;
      const wiersze = [];                                                   // { y, x, n }: pozycja pionowa, prawy brzeg, liczba znaków
      const w = document.createTreeWalker(p, NodeFilter.SHOW_TEXT);
      const r = document.createRange();
      for (let t; (t = w.nextNode()); ) {
        for (let i = 0; i < t.length; i++) {
          r.setStart(t, i); r.setEnd(t, i + 1);
          const b = r.getClientRects()[0];
          if (!b || b.height > lh * 1.6) continue;                          // pomijamy inicjał (kilka wierszy wysokości)
          const o = wiersze[wiersze.length - 1];
          const mid = b.top + b.height / 2;
          if (o && Math.abs(o.mid - mid) < 10) { o.n++; o.x = Math.max(o.x, b.right); } else wiersze.push({ y: b.top, mid, x: b.right, n: 1 });   // indeksy górne zostają w swoim wierszu
        }
      }
      wiersze.forEach((o, i) => {
        const s = document.createElement('span');
        s.className = 'cnt'; s.textContent = o.n;
        s.style.top = (o.y - baza.top) + 'px'; s.style.left = (el.getBoundingClientRect().left - baza.left - 34) + 'px';   // w lewym marginesie, nie koliduje z przypisami
        W.append(s);
        if (i < wiersze.length - 1) liczby.push(o.n);                       // ostatni wiersz akapitu pomijamy
      });
    });
    if (liczby.length) ui.say('znaków w wierszu: średnio ' + Math.round(liczby.reduce((a, b) => a + b, 0) / liczby.length) + ', zakres ' + Math.min(...liczby) + '–' + Math.max(...liczby));
  };
  rysuj();
  const ro = new ResizeObserver(rysuj);
  ro.observe(el);
  return () => { ro.disconnect(); W.querySelectorAll('.cnt').forEach(n => n.remove()); };
}''')
reg('P2-22', 'dom', 280, [], r'''function (el, ui) {
  const W = ui.layer;
  const skanuj = () => {
    W.querySelectorAll('.kr').forEach(n => n.remove());
    const b0 = W.getBoundingClientRect();
    let kliny = 0;
    el.querySelectorAll('.glowny p').forEach(p => {
      const r = document.createRange();
      r.selectNodeContents(p);
      const wiersze = [];                                                   // jeden wpis na wiersz: góra, wysokość i prawy brzeg
      const lh = parseFloat(getComputedStyle(p).lineHeight) || 24;
      [...r.getClientRects()].forEach(b => {
        if (b.height > lh * 1.6) return;                                    // pomijamy inicjał
        const mid = b.top + b.height / 2;
        const w = wiersze.find(x => Math.abs(x.mid - mid) < 10);
        if (w) w.right = Math.max(w.right, b.right); else wiersze.push({ top: b.top, mid, h: b.height, right: b.right });
      });
      const d = wiersze.map(x => x.right).slice(0, -1);                     // ostatni wiersz akapitu pomijamy
      for (let i = 0, bieg = 1, znak = 0; i < d.length; i++) {
        const z = i ? Math.sign(Math.round(d[i] - d[i - 1])) : 0;
        if (z && z === znak) bieg++; else { bieg = z ? 2 : 1; znak = z; }
        if (bieg >= 4 && (i + 1 === d.length || Math.sign(Math.round(d[i + 1] - d[i])) !== znak)) {
          kliny++;                                                          // klin: ≥ 4 kolejne wiersze w jednym kierunku
          for (let k = i - bieg + 1; k <= i; k++) {
            const m = document.createElement('i');
            m.className = 'kr';
            m.style.top = (wiersze[k].top - b0.top) + 'px'; m.style.height = wiersze[k].h + 'px';
            m.style.left = (wiersze[k].right - b0.left + 4) + 'px';
            W.append(m);
          }
        }
      }
    });
    ui.say('wykryte kliny (≥ 4 wiersze o monotonicznej długości): ' + kliny);
  };
  skanuj();
  const ro = new ResizeObserver(skanuj);
  ro.observe(el);
  return () => { ro.disconnect(); W.querySelectorAll('.kr').forEach(n => n.remove()); };
}''')
reg('P2-24', 'diag', 290, ['opentype'], r'''async function (el, ui) {
  const buf = await (await fetch('%s')).arrayBuffer();
  const font = opentype.parse(buf);                                         // Source Serif 4 Regular, WOFF
  const znaki = [...new Set(el.textContent.replace(/\s/g, ''))];
  const brak = znaki.filter(c => font.charToGlyphIndex(c) === 0);
  ui.say('znaków w dokumencie: ' + znaki.length + ', brakuje w foncie: ' + brak.length + (brak.length ? ' (' + brak.join(' ') + ')' : ''));
}''' % FONT_WOFF)
assert len(REG) == 24, len(REG)

# ---- tablica danych dla panelu -------------------------------------------------------------
reg_js = []
for c in sorted(K1, key=lambda c: c['id']):
    reg_js.append('  { id: %s, n: %s, lvl: %s, cat: 1, attr: %s, opis: %s, on: null, off: null }' % (
        json.dumps(c['id']), json.dumps(plfix(NAMES[c['id']]), ensure_ascii=False), json.dumps(c['lvl'], ensure_ascii=False),
        json.dumps(c['id']), json.dumps(plfix(pierwsze_zdanie(c['why'])), ensure_ascii=False)))
for c in sorted(K2, key=lambda c: c['id']):
    r = REG[c['id']]
    reg_js.append('  { id: %s, n: %s, lvl: %s, cat: 2, attr: %s, opis: %s, faza: %s, order: %d, libs: %s,\n    on: %s, off: null }' % (
        json.dumps(c['id']), json.dumps(plfix(NAMES[c['id']]), ensure_ascii=False), json.dumps(c['lvl'], ensure_ascii=False),
        json.dumps(c['id']), json.dumps(plfix(pierwsze_zdanie(c['why'])), ensure_ascii=False),
        json.dumps(r['faza']), r['order'], json.dumps(r['libs']), r['code']))
RULES_JS = 'const RULES = [\n' + ',\n'.join(reg_js) + '\n];'

LIB_JS = ('const LIB = {\n'
          '  typograf: { src: ["%s"] },\n'
          '  hyphenopoly: { src: ["%s"], init: function () {\n%s\n  } },\n'
          '  texlinebreak: { src: ["%s"] },\n'
          '  opentype: { src: ["%s"] },\n};' % (CDN['typograf'], CDN['hyphenopoly'], HYPH_INIT, CDN['texlinebreak'], CDN['opentype']))

css = open(os.path.join(HERE, 'pokaz.css'), encoding='utf-8').read()
app = open(os.path.join(HERE, 'pokaz_app.js'), encoding='utf-8').read()
tekst = open(os.path.join(HERE, 'pokaz_tekst.html'), encoding='utf-8').read()

PANEL = '''<button class="p-toggle" id="p-przycisk" type="button" aria-expanded="true" aria-controls="panel" aria-keyshortcuts="P">Zasady <span>0/48</span></button>
<aside class="p-panel" id="panel" aria-label="Panel zasad typografii" hidden>
<header class="p-nagl"><h2>Zasady typografii (<span id="p-licznik">0 / 48</span>)</h2><button class="p-zwin" type="button" aria-keyshortcuts="Escape">Zwiń</button></header>
<div class="p-akcje">
<button type="button" data-akcja="wszystkie">Włącz wszystkie</button>
<button type="button" data-akcja="zadne">Wyłącz wszystkie</button>
<button type="button" data-akcja="url">Zapisz stan w URL</button>
</div>
<p class="p-url"><input id="p-url" type="text" readonly hidden aria-label="Adres strony ze stanem przełączników"></p>
<p class="p-status" id="p-status" role="status" aria-live="polite"></p>
<ul class="p-diag" id="p-diag" aria-label="Wyniki narzędzi pomiarowych"></ul>
<div id="p-grupy"></div>
<p class="p-stopka">Stan wyłączony to celowo surowy skład: kerning, ligatury i inne funkcje fontu są w nim jawnie wyłączone, żeby przełączniki były widoczne. Skróty: P otwiera i zamyka panel, Esc zwija. „karta” prowadzi do punktu w zasady.html.</p>
</aside>'''

HTML = '''<!doctype html>
<html lang="pl" data-z="" data-n="">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Pokaz zasad typografii</title>
<meta name="description" content="Tekst demonstracyjny z panelem, w którym każdą zasadę typografii z katalogu włączasz i wyłączasz na żywo.">
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="preload" as="font" type="font/woff2" crossorigin href="https://cdn.jsdelivr.net/gh/adobe-fonts/source-serif@4.005R/WOFF2/VAR/SourceSerif4Variable-Roman.ttf.woff2">
<style>
%(css)s
</style>
</head>
<body>
<a class="skip" href="#dokument">Przejdź do treści</a>
<div class="strona">
<article class="dokument" id="dokument" lang="pl">
<div class="pole" id="pole">
%(tekst)s
</div>
<div class="nakladki" id="nakladki" aria-hidden="true"></div>
</article>
</div>
%(panel)s
<noscript><p style="font-family:sans-serif;padding:16px">Panel zasad wymaga JavaScriptu. Tekst poniżej pokazano w stanie surowym.</p></noscript>
<script>
%(lib)s
%(rules)s
%(app)s
</script>
</body>
</html>
'''
out = HTML % dict(css=css, tekst=tekst, panel=plfix(PANEL) if False else PANEL, lib=LIB_JS, rules=RULES_JS, app=app)
open(OUT, 'w', encoding='utf-8').write(out)
print('zapisano', OUT, len(out), 'znaków;', 'zasad:', len(K1) + len(K2))
