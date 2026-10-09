/* generated: psyjaciele-podstrony
 * uwagi.js — narzędzie do zaznaczania elementów i komentowania ich (tylko do przeglądu makiety).
 * Uruchomienie: dopisz ?uwagi=1 do adresu strony w podstrony/ albo użyj zakładki (bookmarklet) z podstrony/_narzedzia/UWAGI.md.
 * Uwagi zapisują się w przeglądarce (localStorage) i można je skopiować jako Markdown jednym przyciskiem.
 */
(function () {
  if (window.__uwagi) { window.__uwagi.toggle(); return; }
  var KEY = 'psyjaciele-uwagi:v1';
  var state = { on: true, picking: false, hover: null, open: null };
  var notes = load();

  function load() { try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch (e) { return []; } }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(notes)); } catch (e) { /* brak storage */ } }
  function el(tag, attrs, html) {
    var n = document.createElement(tag);
    for (var k in (attrs || {})) n.setAttribute(k, attrs[k]);
    if (html != null) n.innerHTML = html;
    return n;
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  // ---- styl (inline, żeby nie dotykać CSS strony) ----
  var css = el('style', { 'data-uwagi': '' }, [
    '.uw-ui,.uw-ui *{box-sizing:border-box;font:16px/24px system-ui,sans-serif;letter-spacing:0;text-transform:none}',
    '.uw-panel{position:fixed;right:16px;bottom:16px;z-index:2147483646;width:320px;max-width:calc(100vw - 32px);background:#fff;color:#111;border:2px solid #111;border-radius:8px;box-shadow:0 8px 32px rgba(0,0,0,.35);padding:16px}',
    '.uw-panel h2{margin:0 0 8px;font-weight:700}',
    '.uw-panel button{cursor:pointer;border:2px solid #111;background:#fff;color:#111;border-radius:4px;padding:8px 16px;margin:0 8px 8px 0}',
    '.uw-panel button.uw-primary{background:#111;color:#fff}',
    '.uw-panel button.uw-active{background:#ffd400}',
    '.uw-count{margin:0 0 8px}',
    '.uw-hover{outline:3px solid #ff2d95!important;outline-offset:2px!important;cursor:crosshair!important}',
    '.uw-marked{outline:2px dashed #ff2d95!important;outline-offset:2px!important}',
    '.uw-pin{position:absolute;z-index:2147483645;width:32px;height:32px;border-radius:50%;background:#ff2d95;color:#fff;border:2px solid #fff;display:flex;align-items:center;justify-content:center;font-weight:700;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,.4)}',
    '.uw-pop{position:absolute;z-index:2147483647;width:320px;max-width:calc(100vw - 32px);background:#fff;color:#111;border:2px solid #ff2d95;border-radius:8px;padding:16px;box-shadow:0 8px 32px rgba(0,0,0,.4)}',
    '.uw-pop textarea{width:100%;height:96px;border:2px solid #111;border-radius:4px;padding:8px;resize:vertical;display:block;margin:8px 0}',
    '.uw-pop button{cursor:pointer;border:2px solid #111;background:#fff;color:#111;border-radius:4px;padding:8px 16px;margin:0 8px 0 0}',
    '.uw-pop button.uw-primary{background:#111;color:#fff}',
    '.uw-pop code{display:block;word-break:break-all;background:#f1f1f1;padding:4px 8px;border-radius:4px;margin-top:4px}'
  ].join(''));
  document.head.appendChild(css);

  // ---- selektor CSS elementu ----
  function selector(e) {
    var parts = [];
    while (e && e.nodeType === 1 && e !== document.body && e !== document.documentElement) {
      if (e.id && document.querySelectorAll('#' + CSS.escape(e.id)).length === 1) { parts.unshift('#' + CSS.escape(e.id)); break; }
      var t = e.tagName.toLowerCase();
      var cls = (e.className && typeof e.className === 'string') ? e.className.trim().split(/\s+/).filter(function (c) { return c && c.indexOf('uw-') !== 0; }).slice(0, 2) : [];
      var s = t + cls.map(function (c) { return '.' + CSS.escape(c); }).join('');
      var p = e.parentElement;
      if (p) {
        var same = Array.prototype.filter.call(p.children, function (x) { return x.tagName === e.tagName; });
        if (same.length > 1) s += ':nth-of-type(' + (same.indexOf(e) + 1) + ')';
      }
      parts.unshift(s);
      e = p;
    }
    return parts.join(' > ');
  }
  function section(e) {
    var s = e.closest('section,header,footer,article,nav,aside');
    if (!s) return '';
    var h = s.querySelector('h1,h2,h3');
    return (s.id ? '#' + s.id : '') + (h ? ' „' + (h.innerText || h.textContent).trim().replace(/\s+/g, ' ').slice(0, 60) + '”' : '');
  }
  function here() { return location.pathname + (location.search.replace(/[?&]uwagi=1/, '') || ''); }
  function mine() { return notes.filter(function (n) { return n.page === here(); }); }
  function find(sel) { try { return document.querySelector(sel); } catch (e) { return null; } }

  // ---- panel ----
  var panel = el('div', { 'class': 'uw-ui uw-panel', role: 'region', 'aria-label': 'Uwagi do strony' });
  document.body.appendChild(panel);
  function renderPanel() {
    panel.innerHTML = '<h2>Uwagi do strony</h2><p class="uw-count">Na tej stronie: <b>' + mine().length + '</b> · razem: <b>' + notes.length + '</b></p>' +
      '<button type="button" data-a="pick" class="uw-primary' + (state.picking ? ' uw-active' : '') + '">' + (state.picking ? 'Klikaj elementy… (Esc)' : 'Zaznacz element') + '</button>' +
      '<button type="button" data-a="copy">Kopiuj wszystko</button>' +
      '<button type="button" data-a="clear">Wyczyść</button>' +
      '<button type="button" data-a="hide">Zamknij</button>' +
      '<div class="uw-msg" aria-live="polite"></div>';
  }
  panel.addEventListener('click', function (ev) {
    var a = ev.target.getAttribute && ev.target.getAttribute('data-a');
    if (a === 'pick') { state.picking = !state.picking; closePop(); renderPanel(); }
    if (a === 'copy') copyAll();
    if (a === 'clear') { if (confirm('Usunąć wszystkie uwagi (ze wszystkich stron)?')) { notes = []; save(); closePop(); draw(); renderPanel(); } }
    if (a === 'hide') api.destroy();
  });

  function msg(t) { var m = panel.querySelector('.uw-msg'); if (m) m.textContent = t; }
  function copyAll() {
    var out = ['# Uwagi do makiety', ''];
    var by = {};
    notes.forEach(function (n) { (by[n.page] = by[n.page] || []).push(n); });
    Object.keys(by).forEach(function (p) {
      out.push('## ' + p, '');
      by[p].forEach(function (n, i) {
        out.push((i + 1) + '. **' + n.comment.replace(/\n+/g, ' ') + '**');
        out.push('   - element: `' + n.sel + '` (' + n.tag + ')');
        if (n.sec) out.push('   - sekcja: ' + n.sec);
        if (n.text) out.push('   - tekst: „' + n.text + '”');
        out.push('   - szerokość okna: ' + n.vw + ' px');
      });
      out.push('');
    });
    var txt = out.join('\n');
    var done = function () { msg('Skopiowano ' + notes.length + ' uwag(i). Wklej je do rozmowy.'); };
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(txt).then(done, fallback); else fallback();
    function fallback() {
      var ta = el('textarea'); ta.value = txt; ta.style.cssText = 'position:fixed;left:-9999px'; document.body.appendChild(ta); ta.select();
      try { document.execCommand('copy'); done(); } catch (e) { msg('Nie udało się skopiować — zaznacz tekst ręcznie.'); window.prompt('Skopiuj (Ctrl/Cmd+C):', txt); }
      ta.remove();
    }
  }

  // ---- wybieranie elementów ----
  function isUi(t) { return t.closest && (t.closest('.uw-ui') || t.closest('.uw-pin') || t.closest('.uw-pop')); }
  document.addEventListener('mouseover', onOver, true);
  document.addEventListener('mouseout', onOut, true);
  document.addEventListener('click', onClick, true);
  document.addEventListener('keydown', onKey, true);
  function onOver(ev) { if (!state.picking || isUi(ev.target)) return; clearHover(); state.hover = ev.target; ev.target.classList.add('uw-hover'); }
  function onOut() { clearHover(); }
  function clearHover() { if (state.hover) { state.hover.classList.remove('uw-hover'); state.hover = null; } }
  function onClick(ev) {
    if (!state.picking || isUi(ev.target)) return;
    ev.preventDefault(); ev.stopPropagation();
    var t = ev.target; clearHover();
    openPop({ el: t, x: ev.pageX, y: ev.pageY });
  }
  function onKey(ev) {
    if (ev.key === 'Escape') { if (state.open) closePop(); else if (state.picking) { state.picking = false; renderPanel(); } }
  }

  // ---- okienko komentarza ----
  function closePop() { if (state.open) { state.open.node.remove(); state.open = null; } }
  function openPop(o) {
    closePop();
    var e = o.el, existing = o.note;
    var node = el('div', { 'class': 'uw-ui uw-pop' });
    var left = Math.min(Math.max(8, o.x), Math.max(8, document.documentElement.scrollWidth - 336));
    node.style.left = left + 'px'; node.style.top = (o.y + 12) + 'px';
    var sel = existing ? existing.sel : selector(e);
    node.innerHTML = '<b>' + (existing ? 'Uwaga ' + (notes.indexOf(existing) + 1) : 'Nowa uwaga') + '</b><code>' + esc(sel) + '</code>' +
      '<textarea aria-label="Komentarz" placeholder="Co poprawić?"></textarea>' +
      '<button type="button" class="uw-primary" data-a="ok">Zapisz</button><button type="button" data-a="cancel">Anuluj</button>' +
      (existing ? '<button type="button" data-a="del">Usuń</button>' : '');
    document.body.appendChild(node);
    var ta = node.querySelector('textarea'); if (existing) ta.value = existing.comment; ta.focus();
    state.open = { node: node };
    node.addEventListener('click', function (ev) {
      var a = ev.target.getAttribute('data-a');
      if (a === 'cancel') closePop();
      if (a === 'del') { notes.splice(notes.indexOf(existing), 1); save(); closePop(); draw(); renderPanel(); }
      if (a === 'ok') {
        var c = ta.value.trim(); if (!c) { ta.focus(); return; }
        if (existing) existing.comment = c;
        else notes.push({ page: here(), sel: sel, tag: e.tagName.toLowerCase(), sec: section(e), text: (e.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 80), comment: c, vw: window.innerWidth });
        save(); closePop(); draw(); renderPanel();
      }
    });
  }

  // ---- znaczniki (pinezki) ----
  function draw() {
    Array.prototype.forEach.call(document.querySelectorAll('.uw-pin'), function (p) { p.remove(); });
    Array.prototype.forEach.call(document.querySelectorAll('.uw-marked'), function (m) { m.classList.remove('uw-marked'); });
    mine().forEach(function (n) {
      var t = find(n.sel); if (!t) return;
      t.classList.add('uw-marked');
      var r = t.getBoundingClientRect();
      var pin = el('button', { 'class': 'uw-ui uw-pin', type: 'button', 'aria-label': 'Uwaga ' + (notes.indexOf(n) + 1) }, String(notes.indexOf(n) + 1));
      pin.style.left = Math.max(0, r.left + window.scrollX - 12) + 'px';
      pin.style.top = Math.max(0, r.top + window.scrollY - 12) + 'px';
      pin.addEventListener('click', function (ev) { ev.preventDefault(); ev.stopPropagation(); openPop({ el: t, note: n, x: r.left + window.scrollX, y: r.top + window.scrollY }); });
      document.body.appendChild(pin);
    });
  }
  var rt; window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(draw, 150); });
  window.addEventListener('scroll', function () { clearTimeout(rt); rt = setTimeout(draw, 400); }, { passive: true });

  var api = {
    toggle: function () { panel.style.display = panel.style.display === 'none' ? '' : 'none'; },
    destroy: function () {
      document.removeEventListener('mouseover', onOver, true); document.removeEventListener('mouseout', onOut, true);
      document.removeEventListener('click', onClick, true); document.removeEventListener('keydown', onKey, true);
      clearHover(); closePop();
      Array.prototype.forEach.call(document.querySelectorAll('.uw-pin,.uw-ui'), function (n) { n.remove(); });
      Array.prototype.forEach.call(document.querySelectorAll('.uw-marked'), function (m) { m.classList.remove('uw-marked'); });
      css.remove(); delete window.__uwagi;
    }
  };
  window.__uwagi = api;
  renderPanel(); draw();
  setTimeout(draw, 1200); // po animacjach układu / podmianie obrazów
})();
