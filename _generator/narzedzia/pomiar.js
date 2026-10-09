(opts) => {
  const out = { meta: {}, blocks: [], issues: { overflowX: [], clipped: [], textOut: [], overlap: [], empty: [], broken: [], contrast: [], orphan: [], small: [], anchors: [], dupId: [], imgDist: [], emptyEl: [] } };
  const EPS = 1.5;
  const doc = document.documentElement;
  const vw = doc.clientWidth;
  const sy = window.scrollY;
  const cls = e => (typeof e.className === 'string' ? e.className.trim().split(/\s+/).filter(Boolean).slice(0, 3).join('.') : '');
  const sig = e => e.tagName.toLowerCase() + (e.id ? '#' + e.id : '') + (cls(e) ? '.' + cls(e) : '');
  const R = e => e.getBoundingClientRect();
  const isHidden = e => {
    const cs = getComputedStyle(e);
    if (cs.display === 'none' || cs.visibility === 'hidden') return true;
    if (parseFloat(cs.opacity) < 0.02) return true;
    return false;
  };
  const inClosedDetails = e => {
    const d = e.closest('details:not([open])');
    return d && !e.closest('summary');
  };
  const vis = e => {
    if (e.closest('svg') && e.tagName.toLowerCase() !== 'svg') return false;
    let p = e;
    while (p && p !== document.body) { if (isHidden(p)) return false; p = p.parentElement; }
    if (inClosedDetails(e)) return false;
    const r = R(e);
    if (!(r.width > 0 && r.height > 0)) return false;
    p = e.parentElement;
    while (p && p !== document.body) {
      const pcs = getComputedStyle(p);
      if (pcs.overflowX !== 'visible' || pcs.overflowY !== 'visible' || pcs.clip !== 'auto') {
        const pr = R(p);
        if ((pr.width <= 2 || pr.height <= 2) && (pcs.overflowX !== 'visible' || pcs.overflowY !== 'visible')) return false;
      }
      p = p.parentElement;
    }
    return true;
  };
  const SKIP_CLOSEST = '.visually-hidden, .sr-only, [hidden], .skip, #uwagi-panel, [class*="inspektor"], [class*="paleta-"], .booking-pets, .halo, .halo-dot, .portrait-halo, .scroll-progress, .header-backdrop';
  const nameWhere = e => {
    // najbliższy nagłówek z id (od góry w sekcji) -> link #id
    let s = e.closest('section, footer, header, nav');
    let h = null;
    if (s) { const hs = s.querySelectorAll('h1[id], h2[id], h3[id]'); for (const x of hs) { if (R(x).top + sy <= R(e).top + sy + 2) h = x; } if (!h) h = s.querySelector('[id]'); }
    const sid = s && s.id ? s.id : '';
    return { sec: s ? (s.tagName.toLowerCase() + (s.id ? '#' + s.id : '') + (cls(s) ? '.' + cls(s).split('.')[0] : '')) : '', anchor: sid || (h ? h.id : '') };
  };

  // ---------- siatka ----------
  const cs0 = getComputedStyle(document.body);
  let gap = parseFloat(getComputedStyle(doc).getPropertyValue('--gap'));
  if (!gap) gap = parseFloat(cs0.getPropertyValue('--gap')) || 32;
  const w0 = document.querySelector('main .wrap.section-stack, main .wrap');
  const wr = w0 ? R(w0) : { left: 0, width: vw };
  const wl = wr.left, ww = wr.width;
  const colW = (ww - 11 * gap) / 12;
  out.meta = { vw, scrollW: doc.scrollWidth, bodyScrollW: document.body.scrollWidth, docH: doc.scrollHeight, wl, ww, gap, colW };
  const colL = x => (x - wl) / (colW + gap) + 1;           // 1 = początek kolumny 1
  const colR = x => (x - wl + gap) / (colW + gap);          // 12 = koniec kolumny 12
  const nearInt = v => Math.abs(v - Math.round(v)) * (colW + gap) <= EPS;

  // ---------- bloki (łańcuch bez poziomych wcięć) ----------
  const EXCL_GRID = '.section-illustration, .poster-media, .poster-art, svg, .site-header, .menu, .overlay, .booking-pets, .founder-hover, .portrait-halo, .portrait-circle, .about-photo, .hero-art, .booking-photo, .booking-dog-foreground, .ab-art';
  const blocks = out.blocks;
  const hasInset = cs => (parseFloat(cs.paddingLeft) + parseFloat(cs.paddingRight) + parseFloat(cs.borderLeftWidth) + parseFloat(cs.borderRightWidth)) > 0.5;
  let _id = 0;
  function addBlock(e, depth, chain, pid) {
    const cs = getComputedStyle(e);
    const r = R(e);
    const rec = {
      s: sig(e), d: depth, x0: +(r.left).toFixed(1), x1: +(r.right).toFixed(1), y0: +(r.top + sy).toFixed(1), y1: +(r.bottom + sy).toFixed(1),
      mt: parseFloat(cs.marginTop), mb: parseFloat(cs.marginBottom), pt: parseFloat(cs.paddingTop), pb: parseFloat(cs.paddingBottom),
      pl: parseFloat(cs.paddingLeft), pr: parseFloat(cs.paddingRight),
      lh: cs.lineHeight === 'normal' ? null : parseFloat(cs.lineHeight), fs: parseFloat(cs.fontSize),
      rg: cs.rowGap === 'normal' ? 0 : parseFloat(cs.rowGap), cg: cs.columnGap === 'normal' ? 0 : parseFloat(cs.columnGap),
      disp: cs.display, pos: cs.position, tag: e.tagName.toLowerCase(), img: e.tagName === 'IMG' || !!e.querySelector(':scope > img, :scope > picture'),
      ch: chain, id: ++_id, pid: pid === undefined ? 0 : pid,
      bt: parseFloat(cs.borderTopWidth), bb: parseFloat(cs.borderBottomWidth), bl: parseFloat(cs.borderLeftWidth), br: parseFloat(cs.borderRightWidth),
      txt: ['P','H1','H2','H3','H4','LI','TD','TH','A','SUMMARY','FIGCAPTION','DT','DD','BUTTON','SPAN','EM','BLOCKQUOTE'].includes(e.tagName) ? e.textContent.trim().replace(/\s+/g,' ').slice(0, 28) : ''
    };
    const w = nameWhere(e); rec.sec = w.sec; rec.anc = w.anchor;
    blocks.push(rec);
    return rec;
  }
  function walk(e, depth, chain, pid) {
    for (const c of e.children) {
      const t = c.tagName.toLowerCase();
      if (['script', 'style', 'link', 'meta', 'noscript', 'svg', 'br', 'use', 'path', 'source'].includes(t)) continue;
      const cs = getComputedStyle(c);
      if (cs.display === 'none') continue;
      if (c.matches(SKIP_CLOSEST) || c.closest(SKIP_CLOSEST)) continue;
      if (cs.display === 'contents') { walk(c, depth, chain, pid); continue; }
      if (cs.position === 'absolute' || cs.position === 'fixed') continue;
      if (inClosedDetails(c)) continue;
      const r = R(c);
      if (r.width === 0 && r.height === 0) continue;
      const ex = c.matches(EXCL_GRID) || !!c.closest(EXCL_GRID);
      const rec = addBlock(c, depth, chain + '>' + sig(c).split('.')[0], pid);
      rec.excl = ex;
      if (!ex && !hasInset(cs) && depth < 7 && !['p', 'h1', 'h2', 'h3', 'h4', 'li', 'a', 'span', 'em', 'strong', 'td', 'th', 'img', 'summary', 'figcaption', 'dt', 'dd', 'label', 'button'].includes(t)) walk(c, depth + 1, chain + '>' + sig(c).split('.')[0], rec.id);
      else if (!ex && t === 'li') { /* li: bez zejścia */ }
    }
  }
  document.querySelectorAll('main > section, main > div, main > nav, footer').forEach(sec => {
    // sekcja jako blok najwyższego poziomu
    const r = R(sec);
    if (r.width === 0) return;
    const rec = addBlock(sec, 0, sig(sec), 0); rec.sec = sig(sec); rec.top = true;
    // jeśli to page-columns -> zejdź
    const inner = sec.querySelectorAll(':scope > .wrap, :scope > .toc-rail-wrap, :scope > .wrap > *');
    walk(sec, 1, sig(sec).split('.')[0], rec.id);
  });
  document.querySelectorAll('header.site-header').forEach(h => { const rec = addBlock(h, 0, 'header', 0); rec.top = true; rec.excl = true; });

  // ---------- poziome przewijanie / wystawanie ----------
  const clipAnc = e => {
    let p = e.parentElement;
    while (p && p !== document.documentElement) {
      const cs = getComputedStyle(p);
      if (cs.overflowX !== 'visible' || cs.overflowY !== 'visible' || cs.clipPath !== 'none') {
        if (p === document.body) return null;
        return p;
      }
      p = p.parentElement;
    }
    return null;
  };
  document.querySelectorAll('body *').forEach(e => {
    const t = e.tagName.toLowerCase();
    if (['script', 'style', 'link', 'meta', 'noscript', 'path', 'use', 'source', 'br'].includes(t)) return;
    if (e.closest('svg') && t !== 'svg') return;
    const r = R(e);
    if (r.width === 0 || r.height === 0) return;
    if (e.matches(SKIP_CLOSEST) || e.closest(SKIP_CLOSEST)) return;
    const cs = getComputedStyle(e);
    if (cs.position === 'fixed') return;
    if (isHidden(e)) return;
    if (inClosedDetails(e)) return;
    if (r.right > vw + 1 || r.left < -1) {
      const ca = clipAnc(e);
      let clipped = false;
      if (ca) { const cr = R(ca); if (r.right <= cr.right + 1 && r.left >= cr.left - 1) clipped = true; else clipped = (getComputedStyle(ca).overflowX !== 'visible'); }
      if (!clipped) out.issues.overflowX.push({ s: sig(e), x0: Math.round(r.left), x1: Math.round(r.right), ...nameWhere(e) });
    }
  });

  // ---------- przycięty tekst (overflow != visible) ----------
  document.querySelectorAll('main *, footer *, header *').forEach(e => {
    if (e.closest('svg') || e.matches(SKIP_CLOSEST) || e.closest(SKIP_CLOSEST)) return;
    const cs = getComputedStyle(e);
    if (cs.display === 'none' || cs.display === 'contents') return;
    if (isHidden(e) || inClosedDetails(e)) return;
    const clipX = cs.overflowX !== 'visible', clipY = cs.overflowY !== 'visible';
    if (!clipX && !clipY) return;
    if (e.tagName === 'DETAILS' || e.tagName === 'IMG') return;
    const r = R(e);
    if (r.width === 0) return;
    const sw = e.scrollWidth, cw = e.clientWidth, sh = e.scrollHeight, ch = e.clientHeight;
    const scrollable = (cs.overflowX === 'auto' || cs.overflowX === 'scroll');
    if (clipX && sw > cw + 2) out.issues.clipped.push({ s: sig(e), kind: scrollable ? 'x-scroll' : 'x-clip', sw, cw, ov: cs.overflowX, ...nameWhere(e) });
    if (clipY && sh > ch + 2 && cs.overflowY !== 'auto' && cs.overflowY !== 'scroll') out.issues.clipped.push({ s: sig(e), kind: 'y-clip', sh, ch, ov: cs.overflowY, ...nameWhere(e) });
  });

  // ---------- tekst: wiersze, sierotki, wystawanie ----------
  const TEXT_SEL = 'p, li, h1, h2, h3, h4, h5, td, th, figcaption, summary, dt, dd, blockquote, a, button, label, span, em, strong, cite, address';
  const leafTextEls = [];
  document.querySelectorAll(TEXT_SEL).forEach(e => {
    if (e.closest('svg') || e.matches(SKIP_CLOSEST) || e.closest(SKIP_CLOSEST)) return;
    // tylko elementy mające własny węzeł tekstowy
    let own = false;
    for (const n of e.childNodes) if (n.nodeType === 3 && n.textContent.trim()) { own = true; break; }
    if (!own) return;
    if (!vis(e)) return;
    leafTextEls.push(e);
  });
  const lineInfo = e => {
    // zwraca wiersze: tablica {top,left,right,words:[...]}
    const lines = [];
    const tw = document.createTreeWalker(e, NodeFilter.SHOW_TEXT);
    let n;
    while ((n = tw.nextNode())) {
      const p = n.parentElement;
      if (p.closest('svg, script, style, .visually-hidden')) continue;
      const txt = n.textContent;
      const re = /\S+/g; let m;
      while ((m = re.exec(txt))) {
        const rg = document.createRange(); rg.setStart(n, m.index); rg.setEnd(n, m.index + m[0].length);
        const rs = rg.getClientRects();
        if (!rs.length) continue;
        const rr = rs[0];
        if (rr.width === 0) continue;
        let L = lines.find(l => Math.abs(l.top - rr.top) < rr.height * 0.5);
        if (!L) { L = { top: rr.top, left: rr.left, right: rr.right, bottom: rr.bottom, words: [] }; lines.push(L); }
        L.left = Math.min(L.left, rr.left); L.right = Math.max(L.right, rr.right); L.bottom = Math.max(L.bottom, rr.bottom);
        L.words.push(m[0]);
      }
    }
    lines.sort((a, b) => a.top - b.top);
    return lines;
  };
  const ONE = /^[aiouwzAIOUWZ]$/;
  leafTextEls.forEach(e => {
    const cs = getComputedStyle(e);
    const fs = parseFloat(cs.fontSize);
    const r = R(e);
    if (fs < 15.9) out.issues.small.push({ s: sig(e), fs, t: e.textContent.trim().slice(0, 30), ...nameWhere(e) });
    const t = e.tagName.toLowerCase();
    if (!['span', 'em', 'strong', 'cite', 'a'].includes(t) || e.closest('li, td, th, p, h1, h2, h3, h4, figcaption, summary, button') === null || t === 'a') {
      const lines = lineInfo(e);
      if (lines.length) {
        // wystawanie poza rodzica / okno
        const par = e.closest('p, li, h1, h2, h3, h4, td, th, figcaption, summary, blockquote, button, a') || e.parentElement;
        const pr = R(e.parentElement);
        lines.forEach(l => {
          if (l.right > vw + 1 || l.left < -1) out.issues.textOut.push({ s: sig(e), why: 'poza oknem', l: Math.round(l.left), r: Math.round(l.right), t: l.words.join(' ').slice(0, 30), ...nameWhere(e) });
          else if (l.right > r.right + 1.5 && cs.display !== 'inline' && getComputedStyle(e).whiteSpace !== 'nowrap') out.issues.textOut.push({ s: sig(e), why: 'poza własnym boxem', l: Math.round(l.left), r: Math.round(l.right), box: Math.round(r.right), t: l.words.join(' ').slice(0, 30), ...nameWhere(e) });
        });
        if (['p', 'li', 'h1', 'h2', 'h3', 'h4', 'td', 'th', 'figcaption', 'summary', 'blockquote', 'dd'].includes(t) && lines.length >= 2) {
          const last = lines[lines.length - 1];
          const prev = lines[lines.length - 2];
          const lw = last.words.length;
          const lastTxt = last.words.join(' ');
          if (lw === 1) out.issues.orphan.push({ s: sig(e), kind: 'wdowa-1-slowo', lastLine: lastTxt, nLines: lines.length, ...nameWhere(e) });
          // sierotka: wiersz kończy się jednoliterowym spójnikiem
          for (let i = 0; i < lines.length - 1; i++) {
            const lw2 = lines[i].words[lines[i].words.length - 1];
            if (ONE.test(lw2.replace(/[.,;:]/g, ''))) out.issues.orphan.push({ s: sig(e), kind: 'sierotka-spojnik', word: lw2, line: lines[i].words.slice(-4).join(' '), ...nameWhere(e) });
          }
          // wiersz zaczynający się od znaku interpunkcyjnego
          for (let i = 1; i < lines.length; i++) {
            const fw = lines[i].words[0];
            if (/^[,.;:!?)%»”–—-]$/.test(fw)) out.issues.orphan.push({ s: sig(e), kind: 'interpunkcja-na-poczatku-wiersza', word: fw, ...nameWhere(e) });
          }
        }
      }
    }
  });
  // nagłówek osierocony na końcu sekcji (po nim brak treści w tej samej sekcji, a sekcja ma >1 blok)
  document.querySelectorAll('main h2, main h3, main h4').forEach(h => {
    if (!vis(h) || h.closest(SKIP_CLOSEST)) return;
    const nxt = h.nextElementSibling;
    const par = h.parentElement;
    if (!nxt && par && par.children.length === 1 && !par.matches('header, .section-head, .poster-heading, .title-row, summary')) {
      /* nagłówek jedyny w kontenerze — pomijamy */
    }
  });
  // puste elementy tekstowe / znaczniki
  document.querySelectorAll('main p, main li, main h2, main h3, main h4, main td, main th, main figcaption, main summary, main dt, main dd, main blockquote').forEach(e => {
    if (e.closest('svg') || e.closest(SKIP_CLOSEST)) return;
    if (!e.textContent.trim() && !e.querySelector('img, svg, picture, i, input, canvas, video, a')) {
      const r = R(e);
      out.issues.emptyEl.push({ s: sig(e), w: Math.round(r.width), h: Math.round(r.height), disp: getComputedStyle(e).display, ...nameWhere(e) });
    }
  });

  // ---------- nakładanie się ----------
  const cand = [];
  const CAND_SEL = 'main p, main li, main h1, main h2, main h3, main h4, main figure, main img, main table, main summary, main figcaption, main a, main button, main .callout, main blockquote, main td, main th, header.site-header a, header.site-header button, footer a, footer p, footer h2, footer h3';
  document.querySelectorAll(CAND_SEL).forEach(e => {
    if (e.closest('svg') || e.closest(SKIP_CLOSEST)) return;
    if (!vis(e)) return;
    const cs = getComputedStyle(e);
    if (cs.display === 'inline' || cs.display === 'contents') {
      // inline: sprawdzamy tylko jeśli ma własny tekst (a)
      if (e.tagName !== 'A') return;
    }
    if (cs.position === 'fixed') return;
    const r = R(e);
    if (r.width < 4 || r.height < 4) return;
    if (e.closest('[aria-hidden="true"]') && !e.matches('img')) return;
    cand.push({ e, r });
  });
  const isDesc = (a, b) => a.contains(b) || b.contains(a);
  const ex2 = e => e.closest('.section-illustration, .poster-media, .booking-photo, .booking-composition, .about-photo, .hero-art, .portrait-circle, .founder-hover, .ab-art, .join-art, .join-banner');
  for (let i = 0; i < cand.length; i++) {
    for (let j = i + 1; j < cand.length; j++) {
      const A = cand[i], B = cand[j];
      if (isDesc(A.e, B.e)) continue;
      const ox = Math.min(A.r.right, B.r.right) - Math.max(A.r.left, B.r.left);
      const oy = Math.min(A.r.bottom, B.r.bottom) - Math.max(A.r.top, B.r.top);
      if (ox > 2 && oy > 2) {
        // pomiń oczywiste warstwy: tekst nad tłem figure (np. podpis wewnątrz kadru)
        if (A.e.matches('figure') && B.e.closest('figure') === A.e) continue;
        if (B.e.matches('figure') && A.e.closest('figure') === B.e) continue;
        const pa = getComputedStyle(A.e).position, pb = getComputedStyle(B.e).position;
        out.issues.overlap.push({ a: sig(A.e), b: sig(B.e), ox: Math.round(ox), oy: Math.round(oy), pa, pb, ea: !!ex2(A.e), eb: !!ex2(B.e), ...nameWhere(A.e) });
        if (out.issues.overlap.length > 60) break;
      }
    }
    if (out.issues.overlap.length > 60) break;
  }

  // ---------- obrazy ----------
  document.querySelectorAll('img').forEach(im => {
    if (im.closest(SKIP_CLOSEST)) return;
    const r = R(im);
    const shown = vis(im);
    const nat = { w: im.naturalWidth, h: im.naturalHeight };
    if (im.complete && im.naturalWidth === 0 && (im.currentSrc || im.getAttribute('src'))) out.issues.broken.push({ s: sig(im), src: im.getAttribute('src'), shown, ...nameWhere(im) });
    else if (shown && nat.w) {
      const cs = getComputedStyle(im);
      const fit = cs.objectFit;
      const ar = nat.w / nat.h, dr = r.width / r.height;
      if (fit === 'fill' || fit === '') {
        if (Math.abs(ar - dr) / ar > 0.03 && r.height > 16) out.issues.imgDist.push({ s: sig(im), nat: nat.w + 'x' + nat.h, shown: Math.round(r.width) + 'x' + Math.round(r.height), fit, kind: 'zniekształcenie', ...nameWhere(im) });
      }
      if (r.width > nat.w * 1.15 && r.width > 100) out.issues.imgDist.push({ s: sig(im), nat: nat.w + 'x' + nat.h, shown: Math.round(r.width) + 'x' + Math.round(r.height), kind: 'powiększony>115%', ...nameWhere(im) });
    }
  });

  // ---------- puste ramki ----------
  document.querySelectorAll('main figure, main .placeholder, main .photo-frame, main [class*="frame"], main [class*="art"], main .callout, main .card, main article, main div').forEach(e => {
    if (e.closest('svg') || e.closest(SKIP_CLOSEST) || !vis(e)) return;
    const cs = getComputedStyle(e);
    const r = R(e);
    if (r.width < 24 || r.height < 12) return;
    const borders = ['Top', 'Right', 'Bottom', 'Left'].some(k => parseFloat(cs['border' + k + 'Width']) > 0 && cs['border' + k + 'Style'] !== 'none');
    const bg = cs.backgroundColor && cs.backgroundColor !== 'rgba(0, 0, 0, 0)' && cs.backgroundColor !== 'transparent';
    const bgi = cs.backgroundImage !== 'none';
    const hasContent = e.textContent.trim().length > 0 || e.querySelector('img, svg, picture, video, canvas, iframe, input, table, ul, ol, hr');
    const masked = cs.maskImage !== 'none' && cs.maskImage !== '' || cs.webkitMaskImage !== 'none' && cs.webkitMaskImage !== '' && cs.webkitMaskImage !== undefined;
    const isFig = e.matches('figure, .placeholder, .photo-frame');
    if ((isFig || bg || (borders && r.height > 24)) && !hasContent && !bgi && !masked) out.issues.empty.push({ s: sig(e), w: Math.round(r.width), h: Math.round(r.height), bg: bg ? cs.backgroundColor : '', borders, ...nameWhere(e) });
    if (isFig && e.querySelector('img') && !e.querySelector('img').complete) out.issues.empty.push({ s: sig(e), why: 'img niezaładowany', ...nameWhere(e) });
    if (e.matches('figure.placeholder, .placeholder.photo-frame') && !e.classList.contains('has-image')) out.issues.empty.push({ s: sig(e), why: 'placeholder bez obrazu', w: Math.round(r.width), h: Math.round(r.height), txt: e.textContent.trim().slice(0, 50), ...nameWhere(e) });
  });

  // ---------- kontrast ----------
  const _cv = document.createElement('canvas'); _cv.width = _cv.height = 1;
  const _cx = _cv.getContext('2d', { willReadFrequently: true });
  const parseC = s => {
    if (!s || s === 'transparent') return { r: 0, g: 0, b: 0, a: 0 };
    let m = s.match(/^rgba?\(([^)]+)\)$/);
    if (m) { const p = m[1].split(/[ ,\/]+/).filter(Boolean).map(Number); return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 }; }
    _cx.clearRect(0, 0, 1, 1); _cx.fillStyle = '#000'; _cx.fillStyle = s; _cx.fillRect(0, 0, 1, 1);
    const d = _cx.getImageData(0, 0, 1, 1).data;
    return { r: d[0], g: d[1], b: d[2], a: d[3] / 255 };
  };
  const lum = c => { const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }; return 0.2126 * f(c.r) + 0.7152 * f(c.g) + 0.0722 * f(c.b); };
  const over = (fg, bg) => ({ r: fg.r * fg.a + bg.r * (1 - fg.a), g: fg.g * fg.a + bg.g * (1 - fg.a), b: fg.b * fg.a + bg.b * (1 - fg.a), a: 1 });
  const bgOf = e => {
    const stack = [];
    let unknown = false;
    const er = R(e); const cx = er.left + er.width / 2, cy = er.top + er.height / 2;
    if (e.closest('header.site-header') && !e.closest('a.button, button')) {   // nagłówek leży na hero: tło = pierwsza sekcja main
      const hs = document.querySelector('main > section, main > div'); if (hs) { const c = parseC(getComputedStyle(hs).backgroundColor); if (c && c.a > 0) return { c, unknown: false }; }
    }
    let p = e;
    while (p && p.nodeType === 1) {
      const cs = getComputedStyle(p);
      const pr = R(p);
      const covers = p === e || p === document.body || p === document.documentElement || (cx >= pr.left - 1 && cx <= pr.right + 1 && cy >= pr.top - 1 && cy <= pr.bottom + 1);
      if (covers) {
        const c = parseC(cs.backgroundColor);
        if (cs.backgroundImage !== 'none' && !/^linear-gradient\(\s*(?:rgba?\([^)]*\)|[a-z]+)\s*,\s*(?:rgba?\([^)]*\)|[a-z]+)\s*\)$/.test(cs.backgroundImage)) { unknown = true; }
        if (c && c.a > 0) { stack.push(c); if (c.a >= 0.999) break; }
      }
      p = p.parentElement;
    }
    let base = { r: 255, g: 255, b: 255, a: 1 };
    for (let k = stack.length - 1; k >= 0; k--) base = over(stack[k], base);
    return { c: base, unknown };
  };
  const seenC = new Set();
  leafTextEls.forEach(e => {
    const cs = getComputedStyle(e);
    const fc = parseC(cs.color); if (!fc) return;
    let op = 1; let p = e; while (p && p.nodeType === 1) { op *= parseFloat(getComputedStyle(p).opacity); p = p.parentElement; }
    const { c: bg, unknown } = bgOf(e);
    const fgc = over({ ...fc, a: fc.a * op }, bg);
    const L1 = lum(fgc), L2 = lum(bg);
    const ratio = (Math.max(L1, L2) + 0.05) / (Math.min(L1, L2) + 0.05);
    const fs = parseFloat(cs.fontSize), bold = parseInt(cs.fontWeight) >= 700;
    const large = fs >= 24 || (fs >= 18.66 && bold);
    const need = large ? 3 : 4.5;
    if (ratio < need) {
      const key = sig(e) + '|' + ratio.toFixed(2);
      if (seenC.has(key)) return; seenC.add(key);
      out.issues.contrast.push({ s: sig(e), ratio: +ratio.toFixed(2), need, fs, fg: cs.color, bg: `rgb(${Math.round(bg.r)},${Math.round(bg.g)},${Math.round(bg.b)})`, unknown, t: e.textContent.trim().slice(0, 28), ...nameWhere(e) });
    }
  });

  // ---------- duplikaty id ----------
  const ids = {};
  document.querySelectorAll('[id]').forEach(e => { ids[e.id] = (ids[e.id] || 0) + 1; });
  Object.entries(ids).forEach(([k, v]) => { if (v > 1) out.issues.dupId.push({ id: k, n: v }); });

  // ---------- kotwice (ta sama strona) ----------
  const hdr = document.querySelector('header.site-header');
  const hdrB = hdr && getComputedStyle(hdr).position === 'fixed' ? R(hdr).bottom : 0;
  const hrefs = [];
  document.querySelectorAll('a[href]').forEach(a => {
    const h = a.getAttribute('href');
    hrefs.push({ href: h, abs: a.href, text: a.textContent.trim().slice(0, 30), vis: vis(a) });
    if (h.startsWith('#') && h.length > 1) {
      const id = decodeURIComponent(h.slice(1));
      const t = document.getElementById(id) || document.querySelector(`[name="${CSS.escape(id)}"]`);
      if (!t) out.issues.anchors.push({ href: h, why: 'brak celu', text: a.textContent.trim().slice(0, 30) });
      else {
        const csT = getComputedStyle(t);
        out.issues.anchors.push({ href: h, ok: true, smt: csT.scrollMarginTop, hidden: isHidden(t) || R(t).height === 0, text: a.textContent.trim().slice(0, 30), vis: vis(a) });
      }
    }
  });
  out.hrefs = hrefs;
  out.meta.hdrBottom = hdrB;
  return out;
}
