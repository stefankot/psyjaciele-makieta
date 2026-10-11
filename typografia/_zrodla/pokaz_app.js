/* ---------- pokaz.html: silnik panelu ----------
   Dane zasad (tablica RULES) i konfiguracja bibliotek (LIB) są wstawiane przez pokaz_build.py.
   Zasada kategorii 1 to tylko token w data-z na <html> (CSS w @layer reguly).
   Zasada kategorii 2 ma funkcję on(el, ctx): faza „tekst” działa na odłączonej kopii oryginału,
   faza „dom” na żywej treści i zwraca funkcję sprzątającą (off), faza „diag” tylko raportuje.
   Wyłączenie dowolnej zasady = przebudowa treści z oryginału z pozostałymi włączonymi. */
(() => {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const root = document.documentElement;
  const pole = $('#pole');
  const dok = $('#dokument');
  const warstwa = $('#nakladki');
  const ORIG = pole.innerHTML;

  const KONFLIKTY = [
    { ids: ['P1-19', 'P1-20', 'P1-23'], why: 'jeden układ strony naraz (kanon 2:3, kanon ISO albo rozkładówka).' },
    { ids: ['P1-21', 'P1-22', 'P1-23'], why: 'jeden układ treści naraz (siatka, kolumny albo rozkładówka).' },
    { ids: ['P1-12', 'P2-13', 'P2-14'], why: 'jeden mechanizm dzielenia wyrazów naraz.' },
    { ids: ['P1-13', 'P2-14'], why: 'justowanie CSS i algorytm Knutha–Plassa wykluczają się.' },
    { ids: ['P1-14', 'P2-15'], why: 'wiszące znaki w CSS i w skrypcie wykluczają się.' },
    { ids: ['P1-22', 'P2-18'], why: 'przypisy boczne w CSS i w skrypcie wykluczają się.' },
  ];
  const WYMAGA = { 'P2-17': ['P1-03'] };
  const NARZEDZIA = [
    { id: 'baza', n: 'Siatka bazowa 8 px' },
    { id: 'kolumny', n: 'Siatka 12 kolumn', wymaga: ['P1-21'] },
    { id: 'pole', n: 'Konstrukcja kanonu: przekątne i pole składu', wymagaJedna: ['P1-19', 'P1-20', 'P1-23'] },
    { id: 'nbsp', n: 'Podświetl spacje niełamliwe i cienkie' },
  ];

  const on = new Set();
  const tools = new Set();
  const diag = new Map();
  let otwarty = matchMedia('(min-width:1200px)').matches;
  let czysty = true;

  /* ---------- pomocnicze (używane przez zasady) ---------- */
  window.mapText = (el, fn) => {
    const w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
    for (let n; (n = w.nextNode()); ) n.nodeValue = fn(n.nodeValue);
  };
  const markSpaces = h => h.replace(/(<[^>]*>)|(&nbsp;|[   ])/g, (m, tag, sp) => tag ? tag : '<span class="nb">' + sp + '</span>');

  /* ---------- konflikty i zależności ---------- */
  function blokada(id) {
    for (const k of KONFLIKTY) {
      if (!k.ids.includes(id)) continue;
      const inny = k.ids.find(x => x !== id && on.has(x));
      if (inny) return 'Koliduje z ' + inny + ' (włączone): ' + k.why;
    }
    const w = WYMAGA[id];
    if (w) { const brak = w.find(x => !on.has(x)); if (brak) return 'Wymaga włączenia ' + brak + '.'; }
    return '';
  }
  function blokadaNarz(t) {
    if (t.wymaga) { const brak = t.wymaga.find(x => !on.has(x)); if (brak) return 'Wymaga włączenia ' + brak + '.'; }
    if (t.wymagaJedna && !t.wymagaJedna.some(x => on.has(x))) return 'Wymaga jednej z reguł: ' + t.wymagaJedna.join(', ') + '.';
    return '';
  }
  function kaskada() {
    let zmiana = true;
    while (zmiana) {
      zmiana = false;
      for (const [k, w] of Object.entries(WYMAGA)) {
        if (on.has(k) && w.some(x => !on.has(x))) { on.delete(k); komunikat(k + ' wyłączona, bo wymaga ' + w.join(', ') + '.'); zmiana = true; }
      }
      for (const t of NARZEDZIA) {
        if (tools.has(t.id) && blokadaNarz(t)) { tools.delete(t.id); komunikat('Nakładka „' + t.n + '” wyłączona: ' + blokadaNarz(t)); zmiana = true; }
      }
    }
  }

  /* ---------- stan i panel ---------- */
  const panel = $('#panel');
  const przycisk = $('#p-przycisk');
  const status = $('#p-status');
  const listaDiag = $('#p-diag');
  const wejscia = new Map();

  function komunikat(t) { status.textContent = t; }

  function ustaw(id, v) {
    if (v) {
      const b = blokada(id);
      if (b) { komunikat(id + ': ' + b); return false; }
      on.add(id);
    } else {
      on.delete(id);
    }
    return true;
  }

  function odswiez() {
    kaskada();
    root.dataset.z = [...on].join(' ');
    root.dataset.n = [...tools].join(' ');
    for (const r of RULES) {
      const w = wejscia.get(r.id);
      const b = on.has(r.id) ? '' : blokada(r.id);
      w.input.checked = on.has(r.id);
      w.input.disabled = !!b;
      w.blok.textContent = b;
      w.blok.hidden = !b;
      w.input.toggleAttribute('aria-describedby', false);
      if (b) w.input.setAttribute('aria-describedby', w.blok.id);
    }
    for (const t of NARZEDZIA) {
      const w = wejscia.get('n:' + t.id);
      const b = tools.has(t.id) ? '' : blokadaNarz(t);
      w.input.checked = tools.has(t.id);
      w.input.disabled = !!b;
      w.blok.textContent = b;
      w.blok.hidden = !b;
    }
    $('#p-licznik').textContent = on.size + ' / ' + RULES.length;
    przycisk.querySelector('span').textContent = on.size + '/' + RULES.length;
    zapisz();
    zaplanuj();
  }

  function budujPanel() {
    const tresc = $('#p-grupy');
    const poziomy = [['mikro', 'Mikro'], ['makro', 'Makro'], ['własne', 'Własne']];
    for (const [lv, nazwa] of poziomy) {
      const rs = RULES.filter(r => r.lvl === lv);
      const fs = document.createElement('fieldset');
      fs.className = 'p-grupa';
      fs.innerHTML = '<legend>' + nazwa + ' (' + rs.length + ')</legend><ul></ul>';
      const ul = $('ul', fs);
      for (const r of rs) ul.append(wiersz(r.id, r.id + '', r.n, r.opis, 'zasady.html#' + r.id, r.cat, (v) => { if (ustaw(r.id, v)) odswiez(); else odswiez(); }, r.id));
      tresc.append(fs);
    }
    const fn = document.createElement('fieldset');
    fn.className = 'p-grupa';
    fn.innerHTML = '<legend>Nakładki i narzędzia</legend><ul></ul>';
    for (const t of NARZEDZIA) {
      $('ul', fn).append(wiersz('n:' + t.id, 'nakładka', t.n, '', '', 0, (v) => { if (v) { if (!blokadaNarz(t)) tools.add(t.id); } else tools.delete(t.id); odswiez(); }, 'n-' + t.id));
    }
    tresc.append(fn);
  }
  function wiersz(klucz, etykietaId, nazwa, opis, href, cat, zmiana, idHtml) {
    const li = document.createElement('li');
    li.className = 'p-regula';
    const input = document.createElement('input');
    input.type = 'checkbox';
    input.id = 'cb-' + idHtml;
    const label = document.createElement('label');
    label.htmlFor = input.id;
    label.innerHTML = '<span class="pid">' + etykietaId + '</span>';
    label.append(document.createTextNode(nazwa));
    if (opis) label.title = opis;
    li.append(input, label);
    if (href) {
      const a = document.createElement('a');
      a.href = href; a.target = '_blank'; a.rel = 'noopener';
      a.textContent = 'karta';
      a.setAttribute('aria-label', 'Karta punktu ' + etykietaId + ' w zasady.html');
      li.append(a);
    } else li.append(document.createElement('span'));
    const blok = document.createElement('p');
    blok.className = 'blok';
    blok.id = 'bl-' + idHtml;
    blok.hidden = true;
    li.append(blok);
    input.addEventListener('change', () => { komunikat(''); zmiana(input.checked); });
    wejscia.set(klucz, { input, blok });
    return li;
  }

  /* ---------- zapis stanu: localStorage i URL ---------- */
  const KLUCZ = 'pokaz-typografia-v1';
  function zapisz() {
    const dane = { z: [...on], n: [...tools] };
    if (matchMedia('(min-width:1200px)').matches) dane.panel = otwarty;       // na wąskim ekranie panel zawsze startuje zwinięty
    try { localStorage.setItem(KLUCZ, JSON.stringify(dane)); } catch (e) { /* tryb prywatny lub zablokowany magazyn */ }
  }
  function adresZeStanem() {
    const p = new URLSearchParams();
    if (on.size) p.set('z', [...on].join('.'));
    if (tools.size) p.set('n', [...tools].join('.'));
    const q = p.toString();
    return location.origin + location.pathname + (q ? '?' + q.replace(/%2C/g, ',') : '');
  }
  function wczytaj() {
    const q = new URLSearchParams(location.search);
    if (q.has('z') || q.has('n')) {
      return { z: (q.get('z') || '').split('.').filter(Boolean), n: (q.get('n') || '').split('.').filter(Boolean), zUrl: true };
    }
    try { const s = JSON.parse(localStorage.getItem(KLUCZ)); if (s && Array.isArray(s.z)) return s; } catch (e) { /* brak magazynu */ }
    return null;
  }
  function zastosujStan(s) {
    const znane = new Set(RULES.map(r => r.id));
    const pominiete = [];
    for (const id of s.z || []) { if (znane.has(id) && !ustaw(id, true)) pominiete.push(id); }
    for (const id of s.n || []) { const t = NARZEDZIA.find(x => x.id === id); if (t && !blokadaNarz(t)) tools.add(id); }
    if (pominiete.length) komunikat('Pominięto z powodu kolizji lub zależności: ' + pominiete.join(', ') + '.');
  }

  /* ---------- przyciski zbiorcze ---------- */
  function wlaczWszystkie() {
    on.clear();
    const pominiete = [];
    for (const r of RULES) { if (!ustaw(r.id, true)) pominiete.push(r.id); }
    odswiez();
    komunikat('Włączono ' + on.size + ' z ' + RULES.length + '. Pominięto ' + pominiete.length + ' (kolizje): ' + pominiete.join(', ') + '.');
  }
  function wylaczWszystkie() { on.clear(); tools.clear(); odswiez(); komunikat('Wyłączono wszystkie zasady i nakładki.'); }
  async function zapiszUrl() {
    const url = adresZeStanem();
    history.replaceState(null, '', url);
    const poleUrl = $('#p-url');
    poleUrl.value = url;
    poleUrl.hidden = false;
    let skopiowano = false;
    try { await navigator.clipboard.writeText(url); skopiowano = true; } catch (e) { poleUrl.select(); }
    komunikat('Stan zapisany w adresie strony' + (skopiowano ? ' i skopiowany do schowka.' : '; skopiuj adres z pola poniżej.'));
  }

  /* ---------- otwieranie panelu ---------- */
  function ustawPanel(v, fokus) {
    otwarty = v;
    panel.hidden = !v;
    przycisk.setAttribute('aria-expanded', String(v));
    zapisz();
    if (fokus) { (v ? $('.p-zwin', panel) : przycisk).focus(); }
  }

  /* ---------- biblioteki ---------- */
  const zaladowane = {};
  const wczytajSkrypt = src => new Promise((res, rej) => {
    const s = document.createElement('script');
    s.src = src; s.async = true; s.onload = res;
    s.onerror = () => rej(new Error('nie udało się załadować ' + src));
    document.head.append(s);
  });
  const ensureLib = name => zaladowane[name] || (zaladowane[name] = (async () => {
    for (const src of LIB[name].src) await wczytajSkrypt(src);
    if (LIB[name].init) await LIB[name].init();
  })().catch(e => { delete zaladowane[name]; throw e; }));

  /* ---------- przebudowa treści ---------- */
  let seq = 0;
  let planowane = false;
  const sprzatanie = [];
  const kolejnosc = (a, b) => a.order - b.order;
  function zaplanuj() {
    if (planowane) return;
    planowane = true;
    requestAnimationFrame(() => { planowane = false; render(); });
  }
  function odswiezDiag() {
    listaDiag.replaceChildren(...[...diag].map(([id, t]) => { const li = document.createElement('li'); li.textContent = id + ': ' + t; return li; }));
  }
  const kontekst = r => ({ id: r.id, layer: warstwa, say: t => { diag.set(r.id, t); odswiezDiag(); } });

  async function render() {
    const moj = ++seq;
    while (sprzatanie.length) { try { sprzatanie.pop()(); } catch (e) { /* sprzątanie best effort */ } }
    $$('.cnt,.kr', warstwa).forEach(n => n.remove());
    diag.clear(); odswiezDiag();
    const aktywne = RULES.filter(r => r.cat === 2 && on.has(r.id));
    const tekst = aktywne.filter(r => r.faza === 'tekst').sort(kolejnosc);
    const dom = aktywne.filter(r => r.faza === 'dom').sort(kolejnosc);
    const diagnostyczne = aktywne.filter(r => r.faza === 'diag').sort(kolejnosc);
    const przeksztalca = tekst.length || dom.length || tools.has('nbsp');
    try {
      const libs = [...new Set(aktywne.flatMap(r => r.libs || []))];
      if (libs.length && libs.some(l => !zaladowane[l])) komunikat('Ładowanie bibliotek z CDN: ' + libs.join(', ') + '…');
      await Promise.all(libs.map(ensureLib));
      if (status.textContent.startsWith('Ładowanie')) komunikat('');
      if (moj !== seq) return;
      if (przeksztalca || !czysty) {
        const kopia = document.createElement('div');
        kopia.innerHTML = ORIG;
        for (const r of tekst) { await r.on(kopia, kontekst(r)); if (moj !== seq) return; }
        if (tools.has('nbsp')) kopia.innerHTML = markSpaces(kopia.innerHTML);
        pole.replaceChildren(...kopia.childNodes);
        czysty = !przeksztalca;
      }
      if (document.fonts) await document.fonts.ready;
      if (moj !== seq) return;
      for (const r of dom) {
        const d = await r.on(pole, kontekst(r));
        if (moj !== seq) { if (typeof d === 'function') d(); return; }
        if (typeof d === 'function') sprzatanie.push(d);
      }
      for (const r of diagnostyczne) {
        const d = await r.on(pole, kontekst(r));
        if (moj !== seq) { if (typeof d === 'function') d(); return; }
        if (typeof d === 'function') sprzatanie.push(d);
      }
    } catch (e) {
      komunikat('Błąd: ' + e.message + '. Zasady wymagające tej biblioteki zostały wyłączone.');
      const nazwy = Object.keys(LIB).filter(l => !zaladowane[l]);
      for (const r of RULES) { if (on.has(r.id) && (r.libs || []).some(l => nazwy.includes(l))) on.delete(r.id); }
      odswiez();
      return;
    }
    rysujNakladki();
  }

  /* ---------- nakładki ---------- */
  function rysujNakladki() {
    $$('.ov', warstwa).forEach(n => n.remove());
    const baza = warstwa.getBoundingClientRect();
    if (tools.has('kolumny') && on.has('P1-21')) {
      const cs = getComputedStyle(pole);
      const r = pole.getBoundingClientRect();
      const tory = cs.gridTemplateColumns.split(' ').map(parseFloat).filter(x => !isNaN(x));
      const odstep = parseFloat(cs.columnGap) || 0;
      let x = r.left - baza.left + parseFloat(cs.paddingLeft || 0);
      for (const w of tory) {
        const d = document.createElement('div');
        d.className = 'ov ov-kol';
        d.style.cssText = 'left:' + x + 'px;top:' + (r.top - baza.top) + 'px;width:' + w + 'px;height:' + r.height + 'px';
        warstwa.append(d);
        x += w + odstep;
      }
    }
    if (tools.has('pole')) {
      // konstrukcja pierwszej „strony” kanonu: przekątne strony i pole składu z marginesów .pole (dokument jest dłuższy niż jedna strona)
      const csd = getComputedStyle(dok), csp = getComputedStyle(pole);
      const W = dok.clientWidth;
      const ar = csd.aspectRatio.split('/').map(parseFloat);
      const Hp = W * (ar.length === 2 && ar[0] && ar[1] ? ar[1] / ar[0] : 1.5);
      const x0 = parseFloat(csp.marginLeft) || 0, y0 = parseFloat(csp.marginTop) || 0;
      const x1 = W - (parseFloat(csp.marginRight) || 0), y1 = Hp - (parseFloat(csp.marginBottom) || 0);
      const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      svg.setAttribute('class', 'ov ov-kanon');
      svg.setAttribute('viewBox', '0 0 ' + W + ' ' + Hp);
      svg.style.cssText = 'left:0;top:0;width:' + W + 'px;height:' + Hp + 'px';
      const p1 = document.createElementNS(svg.namespaceURI, 'path');
      p1.setAttribute('d', 'M0 0L' + W + ' ' + Hp + 'M' + W + ' 0L0 ' + Hp);
      const p2 = document.createElementNS(svg.namespaceURI, 'path');
      p2.setAttribute('d', 'M' + x0 + ' ' + y0 + 'H' + x1 + 'V' + y1 + 'H' + x0 + 'Z M' + x0 + ' ' + y0 + 'L' + x1 + ' ' + y1 + 'M' + x1 + ' ' + y0 + 'L' + x0 + ' ' + y1);
      svg.append(p1, p2);
      warstwa.append(svg);
    }
  }
  new ResizeObserver(() => rysujNakladki()).observe(dok);

  /* ---------- start ---------- */
  budujPanel();
  $('.p-zwin', panel).addEventListener('click', () => ustawPanel(false, true));
  przycisk.addEventListener('click', () => ustawPanel(true, true));
  $('[data-akcja="wszystkie"]').addEventListener('click', wlaczWszystkie);
  $('[data-akcja="zadne"]').addEventListener('click', wylaczWszystkie);
  $('[data-akcja="url"]').addEventListener('click', zapiszUrl);
  document.addEventListener('keydown', e => {
    if (e.defaultPrevented || e.ctrlKey || e.metaKey || e.altKey) return;
    if (e.key === 'Escape' && otwarty && panel.contains(document.activeElement)) { ustawPanel(false, true); return; }
    const t = e.target;
    const pisze = t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName) && t.type !== 'checkbox');
    if ((e.key === 'p' || e.key === 'P') && !pisze) { ustawPanel(!otwarty, true); }
  });

  const zapamietany = wczytaj();
  if (zapamietany) {
    if (!zapamietany.zUrl && typeof zapamietany.panel === 'boolean' && matchMedia('(min-width:1200px)').matches) otwarty = zapamietany.panel;
    zastosujStan(zapamietany);
  }
  ustawPanel(otwarty, false);
  odswiez();
  window.__pokaz = { on, tools, RULES, ustaw, odswiez, render, wlaczWszystkie, wylaczWszystkie, adresZeStanem, zastosujStan, KONFLIKTY, WYMAGA, diag, ORIG };
})();
