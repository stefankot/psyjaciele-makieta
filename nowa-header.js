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
  const GREEN = '#124e36';
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
    t.style.cssText = "position:fixed;left:24px;bottom:24px;z-index:9999;padding:8px 16px;background:#124e36;color:#f0e4cc;font:700 16px/24px Satoshi,Arial,sans-serif";
    document.body.appendChild(t); setTimeout(function () { t.remove(); }, 1400);
  });
})();

/* Telefon: dolny pasek z przyciskami (header-actions) dostaje tło i kolor wg tego, co leży pod nim — ten sam wygląd co górny pasek,
   ale liczony osobno, bo na dole jest zwykle inna sekcja niż na górze. */
(function () {
  var header = document.querySelector(".site-header"), bar = header && header.querySelector(".header-actions");
  if (!bar) return;
  var mq = matchMedia("(max-width: 700px)"), ticking = false;
  function lum(rgb) { var m = /rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?/.exec(rgb); if (!m || (m[4] !== undefined && +m[4] === 0)) return null; return (0.2126 * +m[1] + 0.7152 * +m[2] + 0.0722 * +m[3]) / 255; }
  function update() {
    ticking = false;
    if (!mq.matches) { ["--header-bg", "--nav-ink"].forEach(function (k) { bar.style.removeProperty(k); }); return; }
    var y = innerHeight - 4, hits = document.elementsFromPoint(innerWidth / 2, y), bgEl = null, bgLum = null;
    for (var i = 0; i < hits.length && bgLum === null; i++) {
      if (header.contains(hits[i])) continue;
      for (var e = hits[i]; e && bgLum === null; e = e.parentElement) { var l = lum(getComputedStyle(e).backgroundColor); if (l !== null) { bgLum = l; bgEl = e; } }
    }
    if (bgLum === null) return;
    var bg = getComputedStyle(bgEl).backgroundColor, ink;
    if (bgLum > 0.55) ink = "#124e36";
    else { var tl = lum(getComputedStyle(bgEl).color); ink = tl !== null && tl > 0.5 ? getComputedStyle(bgEl).color : "#f7f3ee"; }
    bar.style.setProperty("--header-bg", bg); bar.style.setProperty("--nav-ink", ink); bar.style.setProperty("color", ink);
    /* przyciski dolnego paska zawsze w kolorach innych niż sekcja pod spodem: „Umów wizytę” pomarańczowy (jak w menu), „Dzwoń” zielony na jasnym tle albo papierowy na ciemnym */
    var light = bgLum > 0.55;
    bar.style.setProperty("--call-bg", light ? "#124e36" : "#f7f3ee");
    bar.style.setProperty("--call-ink", light ? "#f0e4cc" : "#124e36");
  }
  function schedule() { if (!ticking) { ticking = true; requestAnimationFrame(update); } }
  addEventListener("scroll", schedule, { passive: true }); addEventListener("resize", schedule); addEventListener("load", schedule);
  mq.addEventListener && mq.addEventListener("change", schedule);
  update();
})();

/* Hero (desktop): odstęp nad siatką (padding sekcji + siatki) = o tyle ilustracja jest podciągnięta w górę, żeby stała na środku całego hero. */
(function () {
  var hero = document.querySelector(".hero"), grid = hero && hero.querySelector(".wrap.grid");
  if (!grid) return;
  function lift() {
    var v = innerWidth > 700 ? parseFloat(getComputedStyle(hero).paddingTop) + parseFloat(getComputedStyle(grid).paddingTop) : 0;
    hero.style.setProperty("--hero-lift", v + "px");
  }
  addEventListener("resize", lift, { passive: true }); addEventListener("load", lift);
  lift();
})();

/* Rezerwacja (Wettermin) zawsze w nowej karcie: strona przychodni zostaje otwarta w tle (telefon, godziny, dojazd). */
(function () {
  document.querySelectorAll('a[href*="wettermin.pl"]').forEach(function (a) {
    a.target = "_blank";
    var rel = (a.getAttribute("rel") || "").split(/\s+/).filter(Boolean);
    if (rel.indexOf("noopener") < 0) rel.push("noopener");
    a.setAttribute("rel", rel.join(" "));
  });
})();

/* Po kliknięciu rezerwacji (Wettermin otwiera się w nowej karcie) na tej stronie pojawia się krótkie potwierdzenie z numerem telefonu — użytkownik wie, że rezerwacja
   jest otwarta w drugiej karcie, a jeśli się zawaha, może od razu zadzwonić. Znika samo po 9 s albo po kliknięciu „×”. */
(function () {
  var timer = null, box = null;
  function hide() { if (box) { box.remove(); box = null; } clearTimeout(timer); }
  function show() {
    hide();
    box = document.createElement("div");
    box.className = "booking-toast"; box.setAttribute("role", "status");
    box.innerHTML = '<span>Rezerwacja otwarta w&nbsp;nowej karcie. Wolisz zadzwonić? <a href="tel:+48537821345">537&nbsp;821&nbsp;345</a></span><button type="button" aria-label="Zamknij komunikat">×</button>';
    box.querySelector("button").addEventListener("click", hide);
    document.body.appendChild(box);
    timer = setTimeout(hide, 9000);
  }
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest('a[href*="wettermin.pl"]');
    if (a) setTimeout(show, 300);
  });
})();

/* Ciasteczka i statystyki: zabawny piktogram ciasteczka w prawym dolnym rogu otwiera mały panel zgody. Google Analytics 4 (darmowy) ładuje się dopiero po akceptacji;
   bez zgody nie powstaje żadne ciasteczko ani zapytanie do Google. Zgoda jest zapamiętana w localStorage. Zdarzenia: kliknięcie rezerwacji i telefonu z miejscem na stronie.
   USTAW identyfikator pomiaru GA4 poniżej (np. "G-ABC123XYZ"); dopóki jest pusty, nic się nie ładuje (zgoda i piktogram działają, ale nie ma dokąd wysyłać danych). */
(function () {
  var GA_ID = "";                       /* ← tu wpisz identyfikator pomiaru GA4 */
  var KEY = "psyjaciele-zgoda", loaded = false;
  function get() { try { return localStorage.getItem(KEY) || "tak"; } catch (e) { return "tak"; } }   /* zgoda domyślnie włączona; „Odrzucam” zapisuje wybór i wyłącza statystyki */
  function set(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }
  function load() {
    if (loaded || !GA_ID) return; loaded = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    gtag("js", new Date()); gtag("config", GA_ID, { anonymize_ip: true });
    var s = document.createElement("script"); s.async = true; s.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(GA_ID); document.head.appendChild(s);
  }
  function where(a) {
    if (a.closest(".header-actions")) return window.innerWidth <= 700 ? "dolny-pasek" : "naglowek";
    if (a.closest(".site-nav")) return "menu";
    if (a.closest(".site-header")) return "naglowek";
    if (a.closest("footer")) return "stopka";
    var sec = a.closest("section"); return sec && sec.id ? sec.id : "tresc";
  }
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("a[href]"); if (!a || get() !== "tak" || !window.gtag) return;
    var h = a.getAttribute("href") || "";
    if (/wettermin\.pl/.test(h)) gtag("event", "klik_rezerwacja", { miejsce: where(a) });
    else if (/^tel:/.test(h)) gtag("event", "klik_telefon", { miejsce: where(a) });
  });
  var policy = document.querySelector('footer a[href$="polityka-prywatnosci/index.html"]'), policyHref = policy ? policy.getAttribute("href") : "";
  var btn = document.createElement("button"), panel = document.createElement("div");
  btn.type = "button"; btn.className = "cookie-btn"; btn.setAttribute("aria-expanded", "false"); btn.setAttribute("aria-label", "Ciasteczka i statystyki");
  btn.innerHTML = '<svg viewBox="0 0 64 64" aria-hidden="true"><path class="ck-body" d="M32 4a28 28 0 1 0 28 28c-6 1-10-3-10-8-6 0-10-4-10-10-5 1-8-3-8-10z"/><circle class="ck-chip" cx="22" cy="24" r="3.4"/><circle class="ck-chip" cx="40" cy="38" r="3.4"/><circle class="ck-chip" cx="24" cy="44" r="3"/><circle class="ck-chip" cx="44" cy="52" r="2.6"/><path class="ck-smile" d="M26 34q4 5 9 0"/><circle class="ck-eye" cx="26" cy="31" r="1.6"/><circle class="ck-eye" cx="35" cy="31" r="1.6"/></svg>';
  panel.className = "cookie-panel"; panel.hidden = true; panel.setAttribute("role", "dialog"); panel.setAttribute("aria-label", "Ciasteczka i statystyki");
  panel.innerHTML = '<p><strong>Ciasteczka włączone.</strong> Używamy darmowych statystyk Google Analytics, żeby sprawdzać, które przyciski są klikane. Możesz je wyłączyć — strona działa tak samo.' + (policyHref ? ' <a href="' + policyHref + '">Polityka prywatności</a>' : '') + '</p><div><button type="button" data-z="tak">Zostaw włączone</button><button type="button" data-z="nie">Wyłącz</button></div>';
  function state(v) { document.documentElement.dataset.zgoda = v || "brak"; }
  function close() { panel.hidden = true; btn.setAttribute("aria-expanded", "false"); }
  btn.addEventListener("click", function () { var o = panel.hidden; panel.hidden = !o; btn.setAttribute("aria-expanded", String(o)); });
  panel.addEventListener("click", function (e) {
    var z = e.target.getAttribute && e.target.getAttribute("data-z"); if (!z) return;
    set(z); state(z); close(); if (z === "tak") load();
  });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !panel.hidden) { close(); btn.focus(); } });
  document.body.appendChild(panel); document.body.appendChild(btn);
  state(get()); if (get() === "tak") load();
})();

/* Sekcja Zespół: filtr specjalizacji — klik w pastylkę przygasza osoby bez tej specjalizacji (ponowny klik albo „wszystkie” czyści filtr). */
(function () {
  var box = document.querySelector(".team-specs"); if (!box) return;
  var items = document.querySelectorAll(".team-arch .ta-col li");
  function norm(t) { return t.replace(/\s+/g, " ").trim().toLowerCase(); }
  function apply(spec) {
    box.querySelectorAll("button").forEach(function (b) { b.setAttribute("aria-pressed", String(!!spec && b.dataset.spec === spec)); });
    items.forEach(function (li) {
      var has = !spec || Array.prototype.some.call(li.querySelectorAll(".ta-spec span"), function (s) { return norm(s.textContent) === spec; });
      li.classList.toggle("is-dim", !has);
    });
  }
  var cur = null;
  box.addEventListener("click", function (e) {
    var b = e.target.closest("button"); if (!b) return;
    cur = cur === b.dataset.spec ? null : b.dataset.spec; apply(cur);
  });
})();
