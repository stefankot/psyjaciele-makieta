/* ---------- zasady.html: obsługa strony (filtry, narzędzia, pomiary, uruchamianie przykładów kategorii 2) ---------- */
(() => {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const pl = n => String(n).replace('.', ',');

  /* filtry poziomu */
  $$('.filters').forEach(f => {
    const list = document.getElementById(f.dataset.target);
    const counter = document.querySelector('[data-counter="' + f.dataset.target + '"]');
    f.addEventListener('click', e => {
      const b = e.target.closest('button');
      if (!b) return;
      $$('button', f).forEach(x => x.setAttribute('aria-pressed', x === b ? 'true' : 'false'));
      let n = 0;
      $$('.pt, .grp', list).forEach(c => {
        const show = b.dataset.lvl === 'all' || c.dataset.lvl === b.dataset.lvl;
        c.hidden = !show;
        if (show && c.classList.contains('pt')) n++;
      });
      if (counter) $('[data-visible]', counter).textContent = n;
    });
  });

  /* narzędzia: przełączniki klas i suwaki zmiennych CSS */
  document.addEventListener('change', e => {
    const t = e.target;
    if (t.matches('[data-toggle-class]')) t.closest('.pt').classList.toggle(t.dataset.toggleClass, t.checked);
  });
  const setRange = t => {
    const card = t.closest('.pt');
    card.style.setProperty(t.dataset.var, t.value + t.dataset.unit);
    const o = t.parentElement.querySelector('output');
    if (o) o.textContent = t.value + ' ' + t.dataset.unit;
  };
  document.addEventListener('input', e => {
    if (e.target.matches('input[type=range][data-var]')) { setRange(e.target); measureCard(e.target.closest('.pt')); }
  });
  $$('input[type=range][data-var]').forEach(setRange);

  /* ---------- pomiary linii ---------- */
  function lineRows(el) {
    const r = document.createRange();
    r.selectNodeContents(el);
    const rows = [];
    [...r.getClientRects()].forEach(b => {
      if (!b.width || !b.height) return;
      const mid = b.top + b.height / 2;
      const row = rows.find(x => Math.abs(mid - x.mid) < x.h / 2);
      if (row) { row.left = Math.min(row.left, b.left); row.right = Math.max(row.right, b.right); }
      else rows.push({ mid, h: b.height, left: b.left, right: b.right });
    });
    return rows.sort((a, b) => a.mid - b.mid);
  }
  function lineTexts(p) {                        // teksty kolejnych wierszy akapitu (po znakach)
    const out = [];
    let y = null;
    const w = document.createTreeWalker(p, NodeFilter.SHOW_TEXT);
    const r = document.createRange();
    for (let t; (t = w.nextNode()); ) {
      for (let i = 0; i < t.length; i++) {
        r.setStart(t, i); r.setEnd(t, i + 1);
        const b = r.getClientRects()[0];
        if (!b) { if (out.length) out[out.length - 1] += t.data[i]; continue; }
        if (y === null || Math.abs(b.top - y) > 4) { out.push(''); y = b.top; }
        out[out.length - 1] += t.data[i];
      }
    }
    return out;
  }
  const blocks = t => $$(':scope > h3, :scope > h4, :scope > h5, :scope > p', t);

  const STAT = {
    chars(t) {
      const p = $('p', t);
      if (!p) return '';
      const c = lineTexts(p).map(s => s.replace(/\s+$/, '').length);
      if (c.length < 2) return '';
      const body = c.slice(0, -1);
      return 'znaków w wierszu: śr. ' + Math.round(body.reduce((a, b) => a + b, 0) / body.length) + ', maks. ' + Math.max(...body);
    },
    lines(t) { return 'wierszy: ' + blocks(t).reduce((n, b) => n + lineRows(b).length, 0); },
    lastline(t) {
      const v = blocks(t).map(b => {
        const rows = lineRows(b);
        if (rows.length < 2) return null;
        const w = b.getBoundingClientRect().width;
        const l = rows[rows.length - 1];
        return Math.round(100 * (l.right - l.left) / w) + ' %';
      }).filter(Boolean);
      return v.length ? 'ostatni wiersz: ' + v.join(', ') + ' szerokości' : '';
    },
    lh(t) {
      const p = $('p', t);
      const cs = getComputedStyle(p);
      const lh = parseFloat(cs.lineHeight), fs = parseFloat(cs.fontSize);
      return 'interlinia: ' + pl(+lh.toFixed(1)) + ' px (×' + pl((lh / fs).toFixed(2)) + ')';
    },
    h8(t) {
      const h = t.getBoundingClientRect().height;
      const q = h / 8;
      const ok = Math.abs(q - Math.round(q)) < 0.01;
      return 'wysokość: ' + pl(+h.toFixed(1)) + ' px = ' + pl(+q.toFixed(2)) + ' × 8 px' + (ok ? ' (całkowita)' : ' (ułamek)');
    },
    hang(t, pane) {
      if (pane === 'before') return '';
      return CSS.supports('hanging-punctuation', 'first') ? 'wiszące znaki: natywnie' : 'wiszące znaki: zamiennik (text-indent)';
    },
    hyph(t, pane, card) {
      if (pane === 'before') return '';
      const rows = lineRows($('p', t)).length;
      const b = card.querySelector('.before .tekst p');
      return 'wierszy: ' + rows + (b ? ' (przed: ' + lineRows(b).length + ')' : '');
    },
  };

  function measureCard(card) {
    $$('.pane', card).forEach(pane => {
      const t = $('.tekst', pane);
      if (!t) return;
      const kind = pane.classList.contains('after') ? 'after' : 'before';
      $$('.stat[data-stat]', pane).forEach(s => {
        const fn = STAT[s.dataset.stat];
        if (!fn) return;
        try { s.textContent = fn(t, kind === 'after' ? 'after' : 'before', card); } catch (e) { s.textContent = ''; }
      });
    });
  }

  function hyphProbe() {
    const d = document.createElement('div');
    d.lang = 'pl';
    d.style.cssText = 'position:absolute;visibility:hidden;left:-9999px;top:0;inline-size:4.5em;font:16px/24px var(--serif);hyphens:auto;overflow-wrap:normal;word-break:normal;text-align:left';
    d.textContent = 'nieprzejednany przedstawiciel';
    document.body.append(d);
    const res = d.scrollWidth <= d.clientWidth + 1;
    d.remove();
    return res;
  }
  function statusP1() {
    const a = $('[data-status-for="P1-12"]');
    if (a) {
      const ok = hyphProbe();
      a.textContent = 'Test w tej przeglądarce (lang="pl", wyraz „nieprzejednany”): hyphens: auto ' +
        (ok ? 'dzieli polskie wyrazy (słownik dostępny).' : 'nie dzieli polskich wyrazów (brak słownika). Użyj Hyphenopoly (P2-13) albo miękkich łączników w tekście.');
    }
    const b = $('[data-status-for="P1-14"]');
    if (b) b.textContent = 'Test w tej przeglądarce: hanging-punctuation: first ' +
      (CSS.supports('hanging-punctuation', 'first') ? 'jest obsługiwane natywnie.' : 'nie jest obsługiwane; okno „Po” używa ujemnego wcięcia (zamiennik).');
  }

  const k1cards = $$('.pt[data-cat="1"]');
  const ro1 = new ResizeObserver(es => {
    const seen = new Set();
    es.forEach(e => { const c = e.target.closest('.pt'); if (!seen.has(c)) { seen.add(c); requestAnimationFrame(() => measureCard(c)); } });
  });
  k1cards.forEach(c => $$('.sample', c).forEach(s => ro1.observe(s)));
  const measureAll = () => { k1cards.forEach(measureCard); statusP1(); };
  measureAll();
  if (document.fonts) document.fonts.ready.then(measureAll);

  /* ---------- kategoria 2: ładowanie bibliotek i uruchamianie reguł ---------- */
  const loaded = {};
  const loadScript = src => new Promise((res, rej) => {
    const s = document.createElement('script');
    s.src = src; s.async = true;
    s.onload = res;
    s.onerror = () => rej(new Error('nie udało się załadować ' + src));
    document.head.append(s);
  });
  const ensureLib = name => loaded[name] || (loaded[name] = (async () => {
    for (const src of LIB[name].src) await loadScript(src);
    if (LIB[name].init) await LIB[name].init();
  })());

  const INV = [[' ', '⍽ nbsp'], [' ', 'wąska nbsp'], [' ', 'cienka spacja'], ['­', 'miękki łącznik'], ['–', 'półpauza –'], ['—', 'pauza —'],
    ['„', '„'], ['”', '”'], ['«', '«'], ['»', '»'], ['’', '’'], ['…', '…'], ['×', '×'], ['−', '−'], ['±', '±'], ['≠', '≠'], ['°', '°'],
    ['©', '©'], ['™', '™'], ['®', '®'], ['′', '′'], ['″', '″'], ['½', '½'], ['¼', '¼'], ['¾', '¾']];
  const count = txt => { const o = {}; for (const ch of txt) o[ch] = (o[ch] || 0) + 1; return o; };
  function deltaText(a, b, la, lb) {
    const parts = [];
    INV.forEach(([ch, label]) => { const d = (b[ch] || 0) - (a[ch] || 0); if (d) parts.push(label + ' ' + (d > 0 ? '+' : '') + d); });
    if (la !== lb) parts.push('długość ' + la + ' → ' + lb);
    return parts.length ? 'zmiany: ' + parts.join(', ') : 'bez zmian znaków';
  }
  const markSpaces = h => h.replace(/(<[^>]*>)|(&nbsp;|[   ])/g, (m, tag, sp) => tag ? tag : '<span class="nb">' + sp + '</span>');
  const oneWordLast = root => $$('p', root).filter(p => { const l = lineTexts(p); return l.length > 1 && !/\s/.test(l[l.length - 1].trim()); }).length;

  const state = new WeakMap();
  function render(card) {
    const S = state.get(card);
    const st = $('[data-k2-status]', card);
    st.textContent = S.msg || '';
    const btn = $('[data-act="toggle"]', card);
    btn.textContent = S.applied ? 'Przywróć oryginał' : 'Zastosuj regułę';
    btn.setAttribute('aria-pressed', S.applied ? 'true' : 'false');
    btn.disabled = S.busy;
  }
  async function applyCard(card) {
    const S = state.get(card);
    if (S.busy || S.applied) return;
    const def = KP[card.id];
    S.busy = true;
    S.msg = def.libs.length ? 'Ładowanie biblioteki z CDN…' : 'Stosowanie reguły…';
    render(card);
    try {
      for (const l of def.libs) await ensureLib(l);
      if (document.fonts) await document.fonts.ready;
      S.extra = '';
      const ui = { say: t => { S.extra = t; } };
      const a = count(S.el.textContent), la = S.el.textContent.length;
      const d = await def.apply(S.el, ui);
      S.dispose = typeof d === 'function' ? d : null;
      S.applied = true;
      S.html = S.el.innerHTML;
      const parts = [];
      if (!def.noinv) {
        const txt = deltaText(a, count(S.el.textContent), la, S.el.textContent.length);
        $('[data-stat="k2delta"]', card).textContent = txt;
      }
      if (card.id === 'P2-12') parts.push('wdowy wyrazowe (ostatni wiersz z jednym wyrazem): przed ' + oneWordLast(S.beforeEl) + ', po ' + oneWordLast(S.el));
      if (S.extra) parts.push(S.extra);
      S.msg = parts.length ? parts.join(' · ') : 'Reguła zastosowana.';
      if (def.marks && $('[data-act="marks"]', card).checked) S.el.innerHTML = markSpaces(S.html);
    } catch (e) {
      S.msg = 'Błąd: ' + e.message + '. Okno „Po” pozostaje w stanie oryginalnym.';
      S.el.innerHTML = S.orig;
      S.applied = false;
    }
    S.busy = false;
    render(card);
  }
  function restoreCard(card) {
    const S = state.get(card);
    if (S.busy || !S.applied) return;
    if (S.dispose) S.dispose();
    S.dispose = null;
    S.el.innerHTML = S.orig;
    S.applied = false;
    S.msg = 'Przywrócono oryginał (DOM i obserwatory sprzątnięte).';
    $('[data-stat="k2delta"]', card).textContent = '';
    render(card);
  }

  const k2cards = $$('.pt.k2');
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) { io.unobserve(e.target); applyCard(e.target); }
  }), { rootMargin: '400px 0px' });
  k2cards.forEach(card => {
    const el = $('.pane.after .tekst', card);
    state.set(card, { el, beforeEl: $('.pane.before .tekst', card), orig: el.innerHTML, applied: false, busy: false, dispose: null, msg: $('[data-k2-status]', card).textContent, html: '' });
    $('[data-act="toggle"]', card).addEventListener('click', () => {
      const S = state.get(card);
      S.applied ? restoreCard(card) : applyCard(card);
    });
    const m = $('[data-act="marks"]', card);
    if (m) m.addEventListener('change', () => {
      const S = state.get(card);
      if (!S.applied) return;
      S.el.innerHTML = m.checked ? markSpaces(S.html) : S.html;
    });
    io.observe(card);
  });
  window.__zasady = { applyCard, restoreCard, state, ensureLib };   // do testów ręcznych w konsoli
})();
