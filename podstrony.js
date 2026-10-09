/* generated: psyjaciele-podstrony — podstrony.js
   Zachowania podstron. Przeniesione z minimal-nowa.js (menu, stan nagłówka, pierścienie logo, portrety, kropki rezerwacji,
   halo założycielek) z ochroną przed brakiem elementów + nowe: adresy zmiennych własnych, placeholdery obrazów, szyna rozdziałów,
   kotwice w FAQ, pasek sticky-cta, licznik oddechów. Bez bibliotek, bez zewnętrznych zasobów; każdy moduł w try/catch. */
(function () {
  "use strict";
  var errors = (window.__podstronyErrors = []);
  var rm = window.matchMedia("(prefers-reduced-motion: reduce)");
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function run(name, fn) {
    try { fn(); } catch (e) { errors.push(name + ": " + (e && e.message)); }
  }
  function raf(fn) { return window.requestAnimationFrame(fn); }

  /* 1. ROOT i adresy bezwzględne */
  var ROOT = new URL(document.body.getAttribute("data-root") || "./", location.href);
  function abs(path) { return new URL(path, ROOT).href; }

  /* 2. Adresy w zmiennych własnych (--art, --icon, --blob, --pet-atlas): Chromium rozwiązuje je względem arkusza, nie dokumentu.
        Zapisujemy bezwzględne, żeby zachowanie było takie samo wszędzie. */
  var VAR_URL = /(--(?:art|icon|blob|pet-atlas)\s*:\s*)url\(\s*(['"]?)([^)'"]+)\2\s*\)/g;
  function fixStyle(el) {
    var st = el.getAttribute && el.getAttribute("style");
    if (!st || st.indexOf("url(") < 0) return;
    var next = st.replace(VAR_URL, function (m, pre, q, path) {
      if (!/^assets\//.test(path)) return m;
      return pre + "url(" + abs(path) + ")";
    });
    if (next !== st) el.setAttribute("style", next);
  }
  run("fixCustomPropertyUrls", function () {
    $$('[style*="--art"],[style*="--icon"],[style*="--blob"],[style*="--pet-atlas"]').forEach(fixStyle);
    if ("MutationObserver" in window) {
      new MutationObserver(function (list) {
        list.forEach(function (m) { if (m.target.nodeType === 1) fixStyle(m.target); });
      }).observe(document.body, { attributes: true, attributeFilter: ["style"], subtree: true });
    }
  });

  /* 3. Menu */
  var header = $(".site-header");
  run("initMenu", function () {
    var t = $(".menu-toggle"), m = $("#menu");
    if (!t || !m) return;
    function close() {
      t.setAttribute("aria-expanded", "false");
      m.classList.remove("is-open");
      t.setAttribute("aria-label", "Otwórz menu");
      if (header) header.classList.remove("menu-open");
    }
    t.addEventListener("click", function () {
      var open = t.getAttribute("aria-expanded") !== "true";
      t.setAttribute("aria-expanded", String(open));
      m.classList.toggle("is-open", open);
      if (header) header.classList.toggle("menu-open", open);
      t.setAttribute("aria-label", open ? "Zamknij menu" : "Otwórz menu");
    });
    m.addEventListener("click", function (e) { if (e.target.closest("a")) close(); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && t.getAttribute("aria-expanded") === "true") { close(); t.focus(); }
    });
  });

  /* 4. Stan nagłówka */
  run("initHeaderState", function () {
    if (!header) return;
    var backdrop = $(".header-backdrop");
    var sections = $$("main>section,main>.page-columns>section,body>footer");
    var hero = $(".hero");
    var scheduled = false, lastY = window.scrollY;
    function color(y) {
      var info = header.querySelector(".header-info");
      if (!info || !sections.length) return;
      var r = info.getBoundingClientRect(), probe = r.top + Math.min(r.height, 44) / 2;
      var sec = y <= 16 ? hero : (sections.find(function (s) { var b = s.getBoundingClientRect(); return b.top <= probe && b.bottom > probe; }) || hero);
      if (!sec) return;
      var cs = getComputedStyle(sec);
      var c = (cs.getPropertyValue(sec === hero ? "--ink" : "--small-ink").trim() || cs.getPropertyValue("--ink").trim());
      header.style.setProperty("--nav-ink", c);
    }
    function update() {
      scheduled = false;
      var y = Math.max(0, window.scrollY), d = y - lastY;
      header.classList.toggle("is-compact", y > 16);
      if (backdrop) backdrop.classList.toggle("is-active", y > 16);
      color(y);
      if (y <= 16) { header.classList.remove("is-scrolling-down"); lastY = y; }
      else if (Math.abs(d) > 3) { header.classList.toggle("is-scrolling-down", d > 0); lastY = y; }
    }
    window.addEventListener("scroll", function () { if (!scheduled) { scheduled = true; raf(update); } }, { passive: true });
    window.addEventListener("resize", function () { color(Math.max(0, window.scrollY)); }, { passive: true });
    update();
  });

  /* 5. Pierścienie logo (stopka, obserwuj nas) */
  run("initLogoRings", function () {
    var rings = $$(".social-promo-ring,.footer-logo-ring");
    if (!rings.length) return;
    var visible = new Set(rings), frame = 0, lastT = 0, angle = 0;
    function draw() {
      var a = angle + window.scrollY * 0.12;
      rings.forEach(function (r) { r.style.transform = rm.matches ? "none" : "rotate(" + a + "deg)"; });
    }
    function tick(time) {
      frame = 0;
      if (rm.matches || document.hidden || !visible.size) { lastT = 0; return; }
      if (lastT) angle = (angle + Math.min(time - lastT, 64) * 0.002) % 360;
      lastT = time; draw(); frame = raf(tick);
    }
    function update() {
      draw();
      if (rm.matches || document.hidden || !visible.size) { cancelAnimationFrame(frame); frame = 0; lastT = 0; }
      else if (!frame) frame = raf(tick);
    }
    if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) { e.isIntersecting ? visible.add(e.target) : visible.delete(e.target); });
        update();
      });
      rings.forEach(function (r) { io.observe(r); });
    }
    window.addEventListener("scroll", update, { passive: true });
    document.addEventListener("visibilitychange", update);
    rm.addEventListener("change", update);
    update();
  });

  /* 6. Kąt kształtów portretów */
  run("initBlobAngle", function () {
    var blobs = $$(".portrait-blob");
    if (!blobs.length) return;
    var sched = false;
    function rotate() {
      sched = false;
      blobs.forEach(function (blob, i) {
        var b = blob.parentElement.getBoundingClientRect();
        var p = Math.max(-1, Math.min(1, (innerHeight / 2 - b.top - b.height / 2) / (innerHeight / 2 + b.height / 2)));
        blob.style.setProperty("--blob-angle", (rm.matches ? 0 : p * 6 * (i % 2 ? -1 : 1)) + "deg");
      });
    }
    window.addEventListener("scroll", function () { if (!sched) { sched = true; raf(rotate); } }, { passive: true });
    window.addEventListener("resize", rotate);
    rm.addEventListener("change", rotate);
    rotate();
  });

  /* 7. Kropki rezerwacji (min. 50 px, tryb pionowy ≤ 700 px) */
  run("initBookingPets", function () {
    var section = $(".booking-composition");
    if (!section) return;
    var dots = $$(".booking-pet", section);
    if (!dots.length || !section.querySelector("h2") || !section.querySelector(".booking-bottom")) return;
    var width = 0, height = 0, top = 0, bottom = 0, size = 0, visible = false, frame = 0, elapsed = 0, last = 0, stacked = false, pTop = 0, pBottom = 0, pLeft = 0, pRight = 0;
    var MIN_DOT = 50;
    function measure() {
      var box = section.getBoundingClientRect(), title = section.querySelector("h2").getBoundingClientRect(),
        copy = section.querySelector(".booking-bottom").getBoundingClientRect();
      var pets0 = section.querySelector(".booking-pets"), pb = pets0 ? pets0.getBoundingClientRect() : box;
      width = pb.width; height = pb.height;
      size = Math.max(MIN_DOT, Math.min(80, Math.max(24, width * 0.06), (copy.top - title.bottom) / 3));
      var ph = section.querySelector(".booking-photo");
      /* układ pionowy (tekst nad zdjęciem): na wąskich oknach i w kolumnie artykułu */
      stacked = matchMedia("(max-width:700px)").matches || !!(ph && ph.getBoundingClientRect().top - box.top > box.height * 0.3);
      if (stacked) {
        if (ph) { var pr = ph.getBoundingClientRect(), po = (section.querySelector(".booking-pets") || section).getBoundingClientRect(); pTop = pr.top - po.top; pBottom = pr.bottom - po.top; pLeft = pr.left - po.left; pRight = pr.right - po.left; }
      }
      top = title.bottom - box.top + size * 0.65;
      bottom = copy.top - box.top - size * 0.65;
      dots.forEach(function (d) { d.style.width = size + "px"; d.style.left = "0"; d.style.top = "0"; });
      render();
    }
    function render() {
      dots.forEach(function (dot, i) {
        var right = dot.classList.contains("solid"), n = right ? i - 20 : i, count = right ? 12 : 20;
        var angle = (n * Math.PI * 2) / count + elapsed * (0.065 + ((i * 7) % 13) * 0.009) * (i % 3 === 0 ? -1 : 1);
        var x, y, inset = size * 0.65;
        function travel(a, b, t) { return a + (b - a) * (0.5 + 0.5 * Math.sin(t)); }
        if (right) {
          var t = angle + n * 0.7;
          if (stacked) { x = travel(pLeft + inset, pRight - inset, t); y = travel(pTop + inset, pBottom - inset, t * 0.71 + i); }
          else { x = travel(width / 2 + inset, width - inset, t); y = travel(inset, height - inset, t * 0.71 + i); }
        } else {
          x = travel(inset, width / 2 - inset, angle);
          y = travel(top, bottom, angle * 0.73 + i * 1.9);
        }
        dot.style.transform = "translate(" + (x - size / 2) + "px," + (y - size / 2) + "px) rotate(" + Math.sin(angle) * 12 + "deg)";
      });
    }
    function tick(now) {
      frame = 0;
      if (!visible || rm.matches || document.hidden) { last = 0; return; }
      if (last) elapsed += Math.min(0.05, (now - last) / 1000);
      last = now; render(); frame = raf(tick);
    }
    function start() { if (visible && !rm.matches && !document.hidden && !frame) frame = raf(tick); }
    new IntersectionObserver(function (es) { visible = es[0].isIntersecting; start(); }).observe(section);
    new ResizeObserver(measure).observe(section);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(measure);
    document.addEventListener("visibilitychange", start);
    rm.addEventListener("change", function () { if (rm.matches) { cancelAnimationFrame(frame); frame = 0; last = 0; } else start(); });
    measure();
  });

  /* 8. Halo założycielek (blok „about” na stronie zespołu) */
  run("initFoundersHalo", function () {
    var s = $(".about"), h = $(".portrait-halo"), circle = $(".portrait-circle");
    if (!s || !h || !circle || !window.psyPetPhotos) return;
    var names = ["Luna", "Fafik", "Burek", "Maja", "Reksio", "Kluska", "Mruczek", "Tofik", "Kulka", "Figa", "Azor", "Pieróg", "Pusia", "Max", "Łatek", "Stefan", "Roki", "Misia", "Karmel", "Gucio", "Pestka", "Tosia", "Bąbel", "Filemon", "Nela", "Bigos", "Bela", "Dżeki", "Pączek", "Kicia", "Czarek", "Pixel", "Dusia", "Rysiek", "Frodo", "Nugget", "Koko", "Żurek", "Leo", "Sonia", "Chrupka", "Kapsel", "Mila", "Maniek", "Trufel", "Ziutek", "Ciapek", "Frytka", "Dyzio", "Łobuz", "Bunia", "Precel", "Borys", "Szczypiorek", "Miki", "Gofr", "Zuzia", "Kajtek", "Hultaj", "Chałka", "Mango", "Pimpek", "Klops", "Szarlotka"];
    var D = 0.1 * 1.3, G = 0.035 * 1.3, P = D + G, R = 0.5 + 0.012 + D / 2;
    var rings = [0, 1, 2, 3].map(function (i) {
      var radius = R + i * P, step = 2 * Math.asin(P / (2 * radius)), count = Math.floor(Math.PI / step) + 1;
      if (count % 2 === 0) count--;
      return { radius: radius, step: step, count: count };
    });
    var q = 731;
    function rand() { q = (q * 16807) % 2147483647; return (q - 1) / 2147483646; }
    h.removeAttribute("aria-hidden"); h.setAttribute("role", "group"); h.setAttribute("aria-label", "Zwierzęta naszych psyjaciół");
    var tip = document.createElement("div");
    tip.className = "pet-name-tooltip"; tip.id = "pet-name-tooltip"; tip.setAttribute("role", "tooltip"); tip.hidden = true;
    document.body.appendChild(tip);
    function hideTip() { tip.hidden = true; }
    function showTip(dot) {
      tip.textContent = dot.dataset.petName; tip.hidden = false;
      var r = dot.getBoundingClientRect(), t = tip.getBoundingClientRect();
      tip.style.left = Math.max(8, Math.min(innerWidth - t.width - 8, r.left + r.width / 2 - t.width / 2)) + "px";
      tip.style.top = Math.max(8, r.top - t.height - 8) + "px";
    }
    window.addEventListener("scroll", hideTip, { passive: true });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") hideTip(); });
    var ds = [];
    rings.forEach(function (v, k) {
      for (var i = 0; i < v.count; i++) {
        var A = Math.PI / 2 + (i - (v.count - 1) / 2) * v.step;
        var d = document.createElement("button");
        d.type = "button"; d.className = "halo-dot";
        var pet = window.psyPetPhotos.assign(d, "founders");
        d.dataset.petName = names[pet]; d.setAttribute("aria-label", names[pet]); d.setAttribute("aria-describedby", "pet-name-tooltip");
        d.addEventListener("pointerenter", function (dd) { return function () { showTip(dd); }; }(d));
        d.addEventListener("focus", function (dd) { return function () { showTip(dd); }; }(d));
        d.addEventListener("pointerleave", hideTip); d.addEventListener("blur", hideTip);
        d.addEventListener("click", function (dd) { return function () { showTip(dd); }; }(d));
        d.style.setProperty("--pet-x", ((pet % 8) * 100) / 7 + "%");
        d.style.setProperty("--pet-y", (Math.floor(pet / 8) * 100) / 7 + "%");
        d.style.left = (0.5 - v.radius * Math.cos(A)) * 100 - D * 50 + "%";
        d.style.top = (0.5 - v.radius * Math.sin(A)) * 100 - D * 50 + "%";
        h.appendChild(d); ds.push({ d: d });
      }
    });
    function tangent(p, t) {
      var u = 1 - t;
      return Math.atan2(3 * u * u * (p.c1y - p.y) + 6 * u * t * (p.c2y - p.c1y) - 3 * t * t * p.c2y,
        3 * u * u * (p.c1x - p.x) + 6 * u * t * (p.c2x - p.c1x) - 3 * t * t * p.c2x);
    }
    var paths = ds.map(function (o) {
      var side = rand() > 0.5 ? 1 : -1;
      var p = { d: o.d, side: side, x: side * (1.1 + rand() * 1.1), y: (rand() - 0.5) * 1.8, c1x: side * (0.2 + rand() * 1.4), c1y: (rand() - 0.5) * 2.2,
        c2x: (rand() - 0.5) * 0.7, c2y: -0.08 - rand() * 0.55, start: rand() * 0.38, end: 0.7 + rand() * 0.3, ease: 0.65 + rand() * 1.9,
        mode: Math.floor(rand() * 3), turn: (rand() - 0.5) * 50, angles: [] };
      for (var i = 0; i <= 64; i++) {
        var a = tangent(p, i / 64);
        if (i) { var pr = p.angles[i - 1]; while (a - pr > Math.PI) a -= 2 * Math.PI; while (a - pr < -Math.PI) a += 2 * Math.PI; }
        p.angles.push(a);
      }
      return p;
    });
    var sched = false;
    function move() {
      sched = false;
      var section = s.getBoundingClientRect(), portrait = h.getBoundingClientRect(), photo = circle.getBoundingClientRect();
      var center = photo.top + photo.height / 2, travel = section.height / 2 + innerHeight / 2;
      var progress = Math.max(0, Math.min(1, 1 - (center - innerHeight / 2) / travel));
      paths.forEach(function (p) {
        var raw = rm.matches ? 1 : Math.max(0, Math.min(1, (progress - p.start) / (p.end - p.start)));
        var e = raw * raw * raw * (raw * (raw * 6 - 15) + 10);
        var t = p.mode === 0 ? 1 - Math.pow(1 - e, p.ease) : p.mode === 1 ? Math.pow(e, p.ease) : Math.pow(e, p.ease) / (Math.pow(e, p.ease) + Math.pow(1 - e, p.ease));
        var u = 1 - t, scale = portrait.width;
        var x = (u * u * u * p.x + 3 * u * u * t * p.c1x + 3 * u * t * t * p.c2x) * scale;
        var y = (u * u * u * p.y + 3 * u * u * t * p.c1y + 3 * u * t * t * p.c2y) * scale;
        var idx = Math.min(63, Math.floor(t * 64));
        var ang = ((p.angles[idx] + (p.angles[idx + 1] - p.angles[idx]) * (t * 64 - idx) - p.angles[64]) * 180) / Math.PI;
        p.d.style.transform = "translate(" + x + "px," + y + "px) rotate(" + (ang + p.turn * u) + "deg) scale(" + (0.55 + 0.45 * t) + ")";
        p.d.style.opacity = rm.matches ? 1 : Math.min(1, raw * 6);
      });
    }
    function schedule() { if (!sched) { sched = true; raf(move); } }
    window.addEventListener("scroll", schedule, { passive: true });
    window.addEventListener("resize", schedule);
    rm.addEventListener("change", schedule);
    move();
  });

  /* 9. Szyna rozdziałów (rail-layout) */
  run("initRail", function () {
    $$(".rail-layout").forEach(function (rail) {
      var links = $$(".rail-nav a[href^='#']", rail);
      if (!links.length || !("IntersectionObserver" in window)) return;
      var map = new Map();
      links.forEach(function (a) {
        var t = document.getElementById(decodeURIComponent(a.getAttribute("href").slice(1)));
        if (t) map.set(t, a);
      });
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          if (!e.isIntersecting) return;
          links.forEach(function (a) { a.removeAttribute("aria-current"); });
          map.get(e.target).setAttribute("aria-current", "true");
        });
      }, { rootMargin: "-30% 0px -60% 0px" });
      map.forEach(function (a, t) { io.observe(t); });
    });
  });

  /* 9b. Spis treści jako lewa szpalta (toc-rail): aktywna pozycja (strzałka) + kolor tekstu z sekcji, nad którą szpalta aktualnie stoi */
  run("tocRail", function () {
    var box = document.querySelector(".toc-sticky");
    if (!box) return;
    var rail = box.closest(".toc-rail"), cols = rail.closest(".page-columns");
    var links = $$("a[href^='#']", box), items = [];
    links.forEach(function (a) {
      var t = document.getElementById(decodeURIComponent(a.getAttribute("href").slice(1)));
      if (t) items.push({ a: a, t: t });
    });
    var secs = $$(":scope > section", cols), sched = false;
    /* kreski spisu: szerokość = najdłuższa linia liter (pozycje główne i wcięte podpunkty) */
    function trimRules() {
      var list = $(".toc-list", box); if (!list) return;
      list.style.removeProperty("--toc-w");
      var left = list.getBoundingClientRect().left, max = 0;
      $$(".toc-link, .toc-entry ul a", list).forEach(function (a) {
        var rg = document.createRange(); rg.selectNodeContents(a);
        Array.prototype.forEach.call(rg.getClientRects(), function (r) { if (r.width) max = Math.max(max, r.right - left); });
      });
      if (max > 0) list.style.setProperty("--toc-w", Math.ceil(max) + 1 + "px");
    }
    run("tocTrim", trimRules);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { run("tocTrim", trimRules); });
    window.addEventListener("resize", function () { run("tocTrim", trimRules); });
    function update() {
      sched = false;
      if (getComputedStyle(rail).display === "none") return;
      var line = window.innerHeight * 0.32, cur = null;
      items.forEach(function (it) { if (it.t.getBoundingClientRect().top <= line) cur = it; });
      links.forEach(function (a) { if (cur && a === cur.a) a.setAttribute("aria-current", "true"); else a.removeAttribute("aria-current"); });
      var y = box.getBoundingClientRect().top + 48, hit = null;
      secs.forEach(function (sec) { var r = sec.getBoundingClientRect(); if (r.top <= y && r.bottom > y) hit = sec; });
      if (hit) {
        var cs = getComputedStyle(hit), m = /rgba?\((\d+),\s*(\d+),\s*(\d+)/.exec(cs.backgroundColor);
        var light = m && (0.2126 * +m[1] + 0.7152 * +m[2] + 0.0722 * +m[3]) / 255 > 0.6;
        // sekcja o jasnym tle, ale z jasnym kolorem tekstu (np. rezerwacja z zielonym blokiem w środku) → spis w zieleni marki
        box.style.color = light && /rgba?\((2[0-9]{2})/.test(cs.color) ? "#124e2c" : cs.color;
      }
    }
    function schedule() { if (!sched) { sched = true; raf(update); } }
    window.addEventListener("scroll", schedule, { passive: true });
    window.addEventListener("resize", schedule);
    update();
  });

  /* 10. Kotwice wewnątrz zwiniętego <details> */
  run("initFaqHash", function () {
    function open() {
      var id = decodeURIComponent((location.hash || "").slice(1));
      if (!id) return;
      var t = document.getElementById(id);
      var d = t && t.closest("details");
      if (d && !d.open) { d.open = true; t.scrollIntoView(); }
    }
    window.addEventListener("hashchange", open);
    open();
  });

  /* 11. Placeholdery obrazów: jeśli plik istnieje, podmień ramkę na <img> (cicho) */
  run("initPlaceholders", function () {
    var frames = $$("figure.placeholder[data-src]"), inkN = 0;
    frames.forEach(function (fig) {
      var src = fig.getAttribute("data-src");
      if (!src || fig.classList.contains("has-image")) return;
      var probe = new Image();
      probe.onload = function () {
        var img = document.createElement("img");
        img.src = probe.src; img.alt = fig.getAttribute("data-alt") || "";
        img.width = probe.naturalWidth; img.height = probe.naturalHeight;
        img.loading = "lazy"; img.decoding = "async";
        var kind = fig.getAttribute("data-kind");
        if (kind === "ilustracja" || kind === "diagram" || kind === "wycinek") {
          /* kreska w kolorze --ink sekcji (luminancja → alfa), tło ramki = --accent; filtr per ramka, żeby var(--ink) wziął paletę sekcji */
          var fid = "ink-ph-" + (++inkN), ns = "http://www.w3.org/2000/svg";
          var svg = document.createElementNS(ns, "svg");
          svg.setAttribute("width", "0"); svg.setAttribute("height", "0"); svg.setAttribute("aria-hidden", "true"); svg.style.position = "absolute";
          svg.innerHTML = '<filter id="' + fid + '" color-interpolation-filters="sRGB"><feColorMatrix type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 -.2126 -.7152 -.0722 0 1"/><feComposite in2="SourceGraphic" operator="in" result="lines"/><feFlood flood-color="var(--ink)"/><feComposite in2="lines" operator="in"/></filter>';
          fig.insertBefore(svg, fig.firstChild);
          img.style.filter = "url(#" + fid + ")";
        }
        fig.insertBefore(img, fig.firstChild);
        fig.classList.add("has-image");
      };
      probe.onerror = function () { /* brak pliku: ramka zostaje */ };
      probe.src = abs(src);
    });
  });

  /* 12. Pasek sticky-cta (≤ 700 px): po minięciu page-hero, znika przy kontakcie i stopce */
  run("initStickyCta", function () {
    var bar = $(".sticky-cta"), hero = $(".page-hero");
    if (!bar || !hero || !("IntersectionObserver" in window)) return;
    var heroGone = false, endVisible = false;
    function apply() {
      var show = heroGone && !endVisible;
      bar.classList.toggle("is-visible", show);
      document.body.style.setProperty("--sticky-cta-h", matchMedia("(max-width:700px)").matches ? bar.offsetHeight + "px" : "0px");
    }
    new IntersectionObserver(function (es) { heroGone = !es[0].isIntersecting && es[0].boundingClientRect.top < 0; apply(); }).observe(hero);
    var ends = $$("section.contact, footer");
    var vis = new Set();
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { e.isIntersecting ? vis.add(e.target) : vis.delete(e.target); });
      endVisible = vis.size > 0; apply();
    });
    ends.forEach(function (e) { io.observe(e); });
    window.addEventListener("resize", apply);
    apply();
  });

  /* 13. Licznik oddechów (kardiologia): stoper 60 s i licznik kliknięć; po czasie pokazuje wynik (oddechy na minutę) i krótką wskazówkę:
        do 30 — typowy zakres w spoczynku, powyżej 30 — powtórz pomiar i przy powtarzającym się wyniku skontaktuj się z lekarzem */
  run("initBreathCounter", function () {
    $$(".breath-counter").forEach(function (box) {
      var start = $("[data-breath-start]", box), tap = $("[data-breath-tap]", box), out = $("output", box), res = $("[data-breath-result]", box);
      if (!start || !tap || !out) return;
      var secs = 60, count = 0, timer = 0, running = false, clock = $("[data-breath-time]", box);
      function show() { out.textContent = String(count); if (clock) clock.textContent = String(Math.max(0, secs)); }
      function verdict() {
        var high = count > 30;
        box.setAttribute("data-state", high ? "high" : "ok");
        if (res) res.textContent = count + " oddechów na minutę — " + (high
          ? "powyżej 30. Powtórz pomiar po kilkunastu minutach spokoju; jeśli wynik się powtarza, skontaktuj się z lekarzem."
          : "w typowym zakresie (do 30). Powtórz pomiar w ciągu kilku dni i zapisz wyniki.");
      }
      function stop() { clearInterval(timer); running = false; start.disabled = false; tap.disabled = true; start.textContent = start.getAttribute("data-label-again") || start.textContent; verdict(); }
      start.addEventListener("click", function () {
        count = 0; secs = 60; running = true; tap.disabled = false; start.disabled = true; box.removeAttribute("data-state"); if (res) res.textContent = "Liczę… klikaj „Oddech” przy każdym oddechu."; show();
        timer = setInterval(function () { secs -= 1; show(); if (secs <= 0) stop(); }, 1000);
      });
      tap.addEventListener("click", function () { if (running) { count += 1; show(); } });
      tap.disabled = true;
    });
  });

  /* 14. Ilustracja hero: rysunek przycięty do swojej zawartości (bez białych pól wokół) i przyklejony do lewej-góry, żeby lewy brzeg rysunku
        leżał na lewym brzegu leadu. Zawartość = piksele ciemniejsze od tła; bez dostępu do pikseli (np. file://) zostaje układ wyśrodkowany. */
  run("heroArtAlign", function () {
    $$(".page-hero .poster-grid > .poster-art img, .emergency .section-header > .poster-art img").forEach(function (img) {
      function crop() {
        try {
          var w = img.naturalWidth, h = img.naturalHeight, k = Math.min(1, 320 / Math.max(w, h));
          var c = document.createElement("canvas"); c.width = Math.max(1, Math.round(w * k)); c.height = Math.max(1, Math.round(h * k));
          var x = c.getContext("2d", { willReadFrequently: true }); x.drawImage(img, 0, 0, c.width, c.height);
          var d = x.getImageData(0, 0, c.width, c.height).data, x0 = c.width, y0 = c.height, x1 = -1, y1 = -1;
          for (var i = 0; i < c.height; i++) for (var j = 0; j < c.width; j++) {
            var p = (i * c.width + j) * 4;
            if (d[p + 3] > 20 && (d[p] + d[p + 1] + d[p + 2]) / 3 < 235) { if (j < x0) x0 = j; if (j > x1) x1 = j; if (i < y0) y0 = i; if (i > y1) y1 = i; }
          }
          if (x1 < 0) return;
          var L = (x0 / c.width) * 100, T = (y0 / c.height) * 100, R = (1 - (x1 + 1) / c.width) * 100, B = (1 - (y1 + 1) / c.height) * 100;
          img.style.objectViewBox = "inset(" + T.toFixed(2) + "% " + R.toFixed(2) + "% " + B.toFixed(2) + "% " + L.toFixed(2) + "%)";
          img.style.objectPosition = "left top";
        } catch (e) { /* brak dostępu do pikseli: zostaje układ bez przycięcia */ }
      }
      if (img.complete && img.naturalWidth) crop(); else img.addEventListener("load", crop, { once: true });
    });
  });

  /* 15. Latające kulki w banerze pracy: kilka czarno-białych kulek ze zwierzętami (atlas zdjęć) dryfuje nad szarym psem; bez ruchu przy prefers-reduced-motion */
  run("joinBalls", function () {
    $$(".join-balls").forEach(function (box) {
      var art = box.parentElement, sizes = [64, 88, 72, 96, 60, 80, 68, 84], balls = [], W = 0, H = 0, vis = false, frame = 0;
      sizes.forEach(function (s, i) {
        var b = document.createElement("span"); b.className = "join-ball"; b.style.width = b.style.height = s + "px";
        var fr = 40 + i; b.style.setProperty("--pet-x", (fr % 8 * 100 / 7) + "%"); b.style.setProperty("--pet-y", (Math.floor(fr / 8) * 100 / 7) + "%");
        box.appendChild(b); balls.push({ el: b, s: s, i: i });
      });
      function place(t) {
        balls.forEach(function (o) {
          var a = o.i * 1.7, x = (Math.sin(t * 0.00021 * (1 + (o.i % 3) * 0.4) + a) * 0.5 + 0.5) * Math.max(0, W - o.s),
            y = (Math.sin(t * 0.00027 * (1 + (o.i % 4) * 0.3) + a * 1.3) * 0.5 + 0.5) * Math.max(0, H - o.s);
          o.el.style.transform = "translate(" + x.toFixed(1) + "px," + y.toFixed(1) + "px)";
        });
      }
      function measure() { W = art.clientWidth; H = art.clientHeight; place(rm.matches ? 4000 : performance.now()); }
      function tick(now) { frame = 0; if (!vis || rm.matches || document.hidden) return; place(now); frame = raf(tick); }
      function start() { if (vis && !rm.matches && !document.hidden && !frame) frame = raf(tick); }
      if ("ResizeObserver" in window) new ResizeObserver(measure).observe(art); else window.addEventListener("resize", measure);
      if ("IntersectionObserver" in window) new IntersectionObserver(function (es) { vis = es[0].isIntersecting; start(); }).observe(art);
      document.addEventListener("visibilitychange", start);
      rm.addEventListener("change", function () { measure(); start(); });
      measure();
    });
  });

  // TYMCZASOWE (TEMP-GRID): nakładka siatki 12 kolumn — klawisz G albo ?siatka=1 (?siatka=0 wyłącza); do usunięcia po przeglądzie
  run("siatka", function () {
    var q = /[?&]siatka=([01])/.exec(location.search), b = document.body;
    function set(v) { b.classList.toggle("show-grid", v); try { v ? sessionStorage.setItem("siatka-on", "1") : sessionStorage.removeItem("siatka-on"); } catch (e) {} }
    var on = false;
    try { on = sessionStorage.getItem("siatka-on") === "1"; } catch (e) {}
    if (q) on = q[1] === "1";
    set(on);
    document.addEventListener("keydown", function (e) {
      if ((e.key === "g" || e.key === "G") && !e.metaKey && !e.ctrlKey && !e.altKey && !/^(INPUT|TEXTAREA|SELECT)$/.test((e.target.tagName || ""))) set(!b.classList.contains("show-grid"));
    });
  });

  // inspektor uwag (klawisz „I”, ?uwagi=1): patrz inspektor.js w korzeniu makiety
})();
