/*
  nowa-header.js — kolor podkładu paska/rozmycia dopasowany do sekcji pod spodem.
  --header-bg ustawiamy na <html>, bo tło rozmycia (.header-backdrop) nie jest potomkiem <header>.
  Kolor tekstu (--nav-ink) nadal ustawia minimal.js; tu wymuszamy go tylko tam, gdzie sekcja
  ma tło dzielone na pół (rezerwacja, obserwuj nas): papier + zieleń.
*/
(() => {
  const root = document.documentElement;
  const header = document.querySelector('.site-header');
  if (!header) return;
  const hero = document.querySelector('.hero');
  const sections = [...document.querySelectorAll('main > section, main > .page-columns > section, body > footer')];
  const PAPER = '#f7f3ee';
  const GREEN = '#124e2c';
  const flat = ['booking', 'social-promo-section'];
  let ticking = false;

  function solidBg(el) {
    const c = getComputedStyle(el).backgroundColor;
    return !c || c === 'transparent' || c === 'rgba(0, 0, 0, 0)' ? null : c;
  }

  function update() {
    ticking = false;
    const y = window.scrollY;
    const probe = Math.min(header.getBoundingClientRect().height, 96) / 2;
    const section = y <= 16
      ? hero
      : sections.find(s => { const r = s.getBoundingClientRect(); return r.top <= probe && r.bottom > probe; }) || hero;
    let bg = section ? solidBg(section) : null;
    if (!bg || (section && flat.some(c => section.classList.contains(c)))) {
      bg = PAPER;
      header.style.setProperty('--nav-ink', GREEN);
    }
    root.style.setProperty('--header-bg', bg);
  }

  function schedule() {
    if (!ticking) { ticking = true; requestAnimationFrame(update); }
  }

  window.addEventListener('scroll', schedule, { passive: true });
  window.addEventListener('resize', schedule, { passive: true });
  update();
})();

/*
  Znacznik „tu jesteś” w rozwiniętej nawigacji: strzałka w prawo (aria-current) przy pozycji odpowiadającej bieżącej stronie
  (dokładne dopasowanie ścieżki; link z # tylko gdy zgadza się z adresem) oraz, na stronie głównej, przy sekcji widocznej pod nagłówkiem.
*/
(() => {
  const nav = document.querySelector('.site-nav');
  if (!nav) return;
  const norm = p => p.replace(/index\.html$/, '').replace(/\/+$/, '');
  const here = norm(location.pathname);
  const links = [...nav.querySelectorAll('a[href]')].filter(a => a.protocol === location.protocol && a.host === location.host);
  links.forEach(a => a.removeAttribute('aria-current'));
  const sectionLinks = [];
  links.forEach(a => {
    if (norm(a.pathname) !== here) return;
    if (!a.hash) { a.setAttribute('aria-current', 'page'); return; }
    if (a.hash === location.hash && !document.querySelector(a.hash)) { a.setAttribute('aria-current', 'location'); return; }
    if (document.querySelector(a.hash)) sectionLinks.push(a);
  });
  if (!sectionLinks.length) return;
  const header = document.querySelector('.site-header');
  let ticking = false;
  function mark() {
    ticking = false;
    const probe = (header ? header.getBoundingClientRect().height : 80) + 24;
    let active = null;
    if (window.scrollY > 16) {
      sectionLinks.forEach(a => {
        const el = document.querySelector(a.hash);
        const r = el.getBoundingClientRect();
        if (r.top <= probe && r.bottom > probe) active = a.hash;
      });
    }
    sectionLinks.forEach(a => { if (active && a.hash === active) a.setAttribute('aria-current', 'location'); else a.removeAttribute('aria-current'); });
  }
  const schedule = () => { if (!ticking) { ticking = true; requestAnimationFrame(mark); } };
  window.addEventListener('scroll', schedule, { passive: true });
  window.addEventListener('resize', schedule, { passive: true });
  window.addEventListener('hashchange', schedule);
  mark();
})();

/* Logo w nagłówku: grubość linii wyrównywana do wzorca z największego stanu (wysokość 100 px), ale tylko w 40 % różnicy —
   pełne wyrównanie zalewało drobne detale małego logo na telefonie (czytelność), a brak wyrównania dawał zbyt cienką linię.
   Rysunek ma linię ok. 6,1 jednostki viewBox (210 wysokości); ścieżki mają vector-effect: non-scaling-stroke, więc obrys jest w px. */
(function () {
  var logo = document.querySelector(".site-header .brand .nav-logo");
  if (!logo || !window.ResizeObserver) return;
  var LINE = 6.1 / 210, REF = 2.9, SHARE = 0.4;
  function update() {
    var h = logo.getBoundingClientRect().height;
    if (!h) return;
    logo.style.setProperty("stroke-width", Math.max(0, (REF - LINE * h) * SHARE).toFixed(2) + "px", "important");
  }
  new ResizeObserver(update).observe(logo);
  update();
})();

/* Stopka na telefonie (≤ 700 px): „Na stronie” (domyślnie rozwinięte), „Usługi” i „Zespół” (domyślnie zwinięte) są zwijane przyciskiem przy tytule;
   „Śledź nas” zostaje na końcu nawigacji. Na szerszych ekranach przyciski są ukryte w CSS, a listy zawsze widoczne. */
(function () {
  var groups = [
    ["footer .foot-links.footer-nav-strona > div:first-child", "strona", true],
    ["footer .foot-links.footer-nav-uslugi > div", "uslugi", false],
    ["footer .foot-links.footer-nav-zespol > div", "zespol", false]
  ];
  groups.forEach(function (g) {
    var box = document.querySelector(g[0]);
    if (!box) return;
    var h2 = box.querySelector("h2"), nav = box.querySelector("nav");
    if (!h2 || !nav) return;
    var id = "foot-nav-" + g[1], open = g[2];
    nav.id = id;
    var label = (h2.textContent || "").trim();
    var btn = document.createElement("button");
    btn.type = "button"; btn.className = "foot-toggle"; btn.setAttribute("aria-controls", id);
    btn.innerHTML = '<span class="ico ico-nav-arrow-right" aria-hidden="true"></span>';
    function sync() {
      box.classList.toggle("is-open", open);
      btn.setAttribute("aria-expanded", open ? "true" : "false");
      btn.setAttribute("aria-label", (open ? "Zwiń: " : "Rozwiń: ") + label);
    }
    btn.addEventListener("click", function () { open = !open; sync(); });
    h2.appendChild(btn);
    box.classList.add("foot-group", "is-collapsible");
    sync();
  });
})();

/* Interlinia po mierze: im mniej znaków w wierszu, tym krótsza interlinia (<= 24 znaki: 1,30; 38: 1,50; 55: 1,60; 72: 1,68; więcej: 1,75).
   Liczba znaków w wierszu = szerokość bloku / średnia szerokość znaku (pomiar canvas w kroju i rozmiarze bloku); wynik zaokrąglany
   do siatki (8 px; na telefonie 7 px = 8 × 0,875). Obejmuje bloki z listy SEL; reszta tekstu zostaje na stałej interlinii z CSS. */
(function () {
  var SEL = ".hero-links";
  var ctx = document.createElement("canvas").getContext("2d");
  var SAMPLE = "Przychodnia dla psów i kotów, wizyty także w weekendy, zapisz się";
  function ratio(c) {
    if (c <= 24) return 1.3;
    if (c <= 38) return 1.3 + (c - 24) / 14 * 0.2;
    if (c <= 55) return 1.5 + (c - 38) / 17 * 0.1;
    if (c <= 72) return 1.6 + (c - 55) / 17 * 0.08;
    return 1.75;
  }
  function apply() {
    var step = innerWidth <= 700 ? 7 : 8;
    document.querySelectorAll(SEL).forEach(function (el) {
      var cs = getComputedStyle(el), fs = parseFloat(cs.fontSize);
      if (!fs || !el.clientWidth) return;
      ctx.font = cs.fontWeight + " " + cs.fontSize + " " + cs.fontFamily;
      var avg = ctx.measureText(SAMPLE).width / SAMPLE.length;
      var inner = el.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
      var lh = Math.max(step * 2, Math.round(fs * ratio(inner / avg) / step) * step);
      el.style.setProperty("line-height", lh + "px", "important");
    });
  }
  var t;
  function later() { clearTimeout(t); t = setTimeout(apply, 60); }
  addEventListener("resize", later, { passive: true });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(apply);
  apply();
})();

/* God mode (Shift+G): przełącza wygląd aureoli w sekcji Zespół — z promienistego wieńca kresek (domyślnie) na owalny pierścień nad głową. Pamięta wybór w sessionStorage. */
(function () {
  var root = document.documentElement;
  try { if (sessionStorage.getItem("god-mode") === "1") root.classList.add("god"); } catch (e) {}
  document.addEventListener("keydown", function (e) {
    if (!e.shiftKey || (e.key !== "G" && e.key !== "g") || e.metaKey || e.ctrlKey || e.altKey) return;
    if (/^(INPUT|TEXTAREA|SELECT)$/.test((e.target.tagName || "")) || e.target.isContentEditable) return;
    var on = root.classList.toggle("god");
    try { on ? sessionStorage.setItem("god-mode", "1") : sessionStorage.removeItem("god-mode"); } catch (err) {}
    var t = document.createElement("div");
    t.textContent = on ? "God mode: wł." : "God mode: wył.";
    t.setAttribute("role", "status");
    t.style.cssText = "position:fixed;left:24px;bottom:24px;z-index:9999;padding:8px 16px;background:#124e2c;color:#fbd9c6;font:700 16px/24px Satoshi,Arial,sans-serif";
    document.body.appendChild(t); setTimeout(function () { t.remove(); }, 1400);
  });
})();
