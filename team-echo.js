/* team-echo.js — hover kart zespołu (Home i „Kto przyjmuje”): obrys sylwetki powielany na zewnątrz w zapętlonej animacji.

   Jak działa: z kanału alfa zdjęcia (wycięta sylwetka) liczony jest raz dokładny rozkład odległości od sylwetki (EDT, Felzenszwalb–Huttenlocher).
   W każdej klatce rysowane są pierścienie o stałej grubości i stałym odstępie (odstęp S), przesuwane o t·v: wzór jest okresowy w (d − t·v),
   więc ruch na zewnątrz zapętla się bez szwu. Pierścień wyłania się z krawędzi sylwetki i zanika przy brzegu komórki.
   Kolor = `color` canvasu z CSS (--team-overlay-ink, domyślnie --accent karty), czytany przy każdym starcie, więc zmiana palety (K) działa.

   Zasady: tylko gdy kursor/fokus jest na karcie (pętla rAF zatrzymuje się po zniknięciu), nie przy prefers-reduced-motion, nie na urządzeniach dotykowych.
   Brak canvasu/obrazu → karta bez linii (klasa has-echo dodawana dopiero po udanym przygotowaniu).
   Parametry (px CSS): STROKE_PX grubość linii, GAP_PX odstęp między liniami (oś do osi), SPEED_PX prędkość ruchu na zewnątrz [px/s], FADE_IN_PX odcinek, na którym
   linia wyłania się z krawędzi sylwetki. */
(() => {
  'use strict';
  const STROKE_PX = 3, GAP_PX = 15, SPEED_PX = 11, FADE_IN_PX = 16, ALPHA_THRESHOLD = 128, FADE_OUT_MS = 380;
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  const cards = [...document.querySelectorAll('.team .people .person')];
  if (!cards.length || !window.HTMLCanvasElement) return;
  const INF = 1e20;

  /* --- dokładna transformata odległości (kwadraty odległości), 1-D i 2-D --- */
  function edt1d(f, d, v, z, n) {
    let k = 0;
    v[0] = 0; z[0] = -INF; z[1] = INF;
    for (let q = 1; q < n; q++) {
      let s;
      for (;;) {
        const p = v[k];
        s = ((f[q] + q * q) - (f[p] + p * p)) / (2 * q - 2 * p);
        if (s <= z[k]) k--; else break;
      }
      k++; v[k] = q; z[k] = s; z[k + 1] = INF;
    }
    k = 0;
    for (let q = 0; q < n; q++) {
      while (z[k + 1] < q) k++;
      const dq = q - v[k];
      d[q] = dq * dq + f[v[k]];
    }
  }
  function edt2d(grid, w, h) {
    const n = Math.max(w, h), f = new Float32Array(n), d = new Float32Array(n), v = new Int32Array(n), z = new Float32Array(n + 1);
    for (let x = 0; x < w; x++) {
      for (let y = 0; y < h; y++) f[y] = grid[y * w + x];
      edt1d(f, d, v, z, h);
      for (let y = 0; y < h; y++) grid[y * w + x] = d[y];
    }
    for (let y = 0; y < h; y++) {
      for (let x = 0; x < w; x++) f[x] = grid[y * w + x];
      edt1d(f, d, v, z, w);
      for (let x = 0; x < w; x++) grid[y * w + x] = d[x];
    }
  }

  const colorCtx = document.createElement('canvas').getContext('2d', { willReadFrequently: true });
  function parseColor(css) {
    colorCtx.canvas.width = colorCtx.canvas.height = 1;
    colorCtx.clearRect(0, 0, 1, 1);
    colorCtx.fillStyle = '#000';
    colorCtx.fillStyle = css;
    colorCtx.fillRect(0, 0, 1, 1);
    const p = colorCtx.getImageData(0, 0, 1, 1).data;
    return [p[0], p[1], p[2]];
  }

  const smooth = (a, b, x) => { const t = Math.min(1, Math.max(0, (x - a) / (b - a))); return t * t * (3 - 2 * t); };

  function whenReady(img) {
    if (img.complete && img.naturalWidth) return Promise.resolve();
    return new Promise((res, rej) => { img.addEventListener('load', res, { once: true }); img.addEventListener('error', rej, { once: true }); });
  }

  /* --- przygotowanie karty: canvas + rozkład odległości --- */
  async function prepare(card) {
    const figure = card.querySelector('figure'), img = card.querySelector('.portrait-blob img');
    if (!figure || !img) throw new Error('brak figure/img');
    await whenReady(img);
    const fr = figure.getBoundingClientRect();
    if (!fr.width) throw new Error('figure ukryte');
    const scale = Math.min(window.devicePixelRatio || 1, 1.5);
    const W = Math.round(fr.width * scale), H = Math.round(fr.height * scale);

    /* narysuj zdjęcie dokładnie tak, jak jest pokazane: object-fit: contain, object-position: center bottom */
    const ir = img.getBoundingClientRect();
    const bx = (ir.left - fr.left) * scale, by = (ir.top - fr.top) * scale, bw = ir.width * scale, bh = ir.height * scale;
    const k = Math.min(bw / img.naturalWidth, bh / img.naturalHeight);
    const dw = img.naturalWidth * k, dh = img.naturalHeight * k;
    const off = document.createElement('canvas');
    off.width = W; off.height = H;
    const octx = off.getContext('2d', { willReadFrequently: true });
    octx.drawImage(img, bx + (bw - dw) / 2, by + (bh - dh), dw, dh);
    const px = octx.getImageData(0, 0, W, H).data;

    const grid = new Float32Array(W * H);
    let inside = 0;
    for (let i = 0; i < W * H; i++) {
      if (px[i * 4 + 3] >= ALPHA_THRESHOLD) { grid[i] = 0; inside++; } else grid[i] = INF;
    }
    if (inside < 50) throw new Error('pusta sylwetka');
    edt2d(grid, W, H);

    /* tylko piksele na zewnątrz sylwetki, w zasięgu animacji */
    const dMax = Math.max(W, H) * 1.05;
    let n = 0;
    for (let i = 0; i < W * H; i++) { const d = Math.sqrt(grid[i]); grid[i] = d; if (d > 0 && d < dMax) n++; }
    const idx = new Uint32Array(n), dist = new Float32Array(n);
    for (let i = 0, j = 0; i < W * H; i++) { const d = grid[i]; if (d > 0 && d < dMax) { idx[j] = i; dist[j] = d; j++; } }

    const canvas = document.createElement('canvas');
    canvas.className = 'person-echo';
    canvas.width = W; canvas.height = H;
    canvas.setAttribute('aria-hidden', 'true');
    figure.insertBefore(canvas, figure.firstChild);
    const ctx = canvas.getContext('2d');
    const frame = ctx.createImageData(W, H);
    return { figure, canvas, ctx, frame, idx, dist, W, H, scale, key: W + 'x' + H };
  }

  const states = new WeakMap();
  function ensure(card) {
    let st = states.get(card);
    if (!st) { st = { promise: null, data: null, raf: 0, hold: 0, running: false, t0: 0 }; states.set(card, st); }
    const figure = card.querySelector('figure');
    const key = figure ? Math.round(figure.getBoundingClientRect().width) : 0;
    if (st.data && st.sizeKey !== key) {              /* rozmiar komórki się zmienił → przygotuj od nowa */
      st.data.canvas.remove(); st.data = null; st.promise = null; card.classList.remove('has-echo');
    }
    if (!st.promise) {
      st.sizeKey = key;
      st.promise = prepare(card).then(d => { st.data = d; card.classList.add('has-echo'); return d; }).catch(() => { st.failed = true; return null; });
    }
    return st;
  }

  function draw(card, st, now) {
    const d = st.data;
    if (!d) return;
    const { W, H, idx, dist, frame } = d;
    const k = d.scale, S = GAP_PX * k, half = STROKE_PX * k / 2, speed = SPEED_PX * k;
    const off = ((now - st.t0) / 1000 * speed) % S;
    const fadeIn = FADE_IN_PX * k, fadeFrom = 0.5 * W, fadeTo = 0.95 * W;
    const a = frame.data;
    for (let i = 0; i < idx.length; i++) {
      const dd = dist[i];
      let x = (dd - off) % S; if (x < 0) x += S;
      let al = half - Math.abs(x - S / 2) + 0.5;      /* grubość linii z wygładzeniem 1 px */
      if (al <= 0) { a[idx[i] * 4 + 3] = 0; continue; }
      if (al > 1) al = 1;
      if (dd < fadeIn) al *= dd / fadeIn;               /* pierścień wyłania się z krawędzi sylwetki */
      if (dd > fadeFrom) al *= 1 - smooth(fadeFrom, fadeTo, dd);
      a[idx[i] * 4 + 3] = (al * 255) | 0;
    }
    d.ctx.putImageData(frame, 0, 0);
  }

  function setColor(card, st) {
    const d = st.data; if (!d) return;
    const css = getComputedStyle(d.canvas).color;
    const [r, g, b] = parseColor(css || 'rgb(0,0,0)');
    const a = d.frame.data;
    for (let i = 0; i < d.idx.length; i++) { const o = d.idx[i] * 4; a[o] = r; a[o + 1] = g; a[o + 2] = b; }
  }

  function loop(card, st) {
    if (!st.running) return;
    draw(card, st, performance.now());
    st.raf = requestAnimationFrame(() => loop(card, st));
  }

  async function start(card) {
    if (reduce.matches) return;
    const st = ensure(card);
    clearTimeout(st.hold);
    await st.promise;
    if (!st.data || st.failed) return;
    if (!card.matches(':hover, :focus-within')) return;   /* kursor mógł już zjechać */
    setColor(card, st);
    if (!st.running) { st.running = true; st.t0 = performance.now(); loop(card, st); }
  }
  function stop(card) {
    const st = states.get(card); if (!st) return;
    clearTimeout(st.hold);
    st.hold = setTimeout(() => {
      if (card.matches(':hover, :focus-within')) return;
      st.running = false; cancelAnimationFrame(st.raf);
    }, FADE_OUT_MS);
  }

  cards.forEach(card => {
    card.addEventListener('pointerenter', e => { if (e.pointerType === 'mouse' || e.pointerType === 'pen') start(card); });
    card.addEventListener('pointerleave', () => stop(card));
    card.addEventListener('focusin', () => start(card));
    card.addEventListener('focusout', () => stop(card));
  });

  /* przygotuj karty z wyprzedzeniem, gdy sekcja zbliża się do okna (bez blokowania ładowania) */
  const warm = list => list.forEach((c, i) => setTimeout(() => ensure(c), 120 * i));
  const section = cards[0].closest('.people');
  if (reduce.matches) return;
  if ('IntersectionObserver' in window && section) {
    const io = new IntersectionObserver(es => { if (es.some(e => e.isIntersecting)) { io.disconnect(); warm(cards); } }, { rootMargin: '400px 0px' });
    io.observe(section);
  }
})();
