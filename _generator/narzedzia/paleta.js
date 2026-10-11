/* paleta.js — nakładka do zmiany palet kolorów (klawisz K, ładowana przez inspektor.js).
   1) ZESTAW PALET całej strony (u góry panelu): szlachetna (domyślna) / poprzednia / Feminist Art Coalition. Zestaw to atrybut
      html[data-paleta] (definicje: palety-zestawy.css), pamiętany w localStorage „psyjaciele-paleta” i ustawiany też przez ?paleta=… w adresie.
      Podglądy zestawów i palety sekcji aktywnego zestawu są czytane z CSS (bez własnej kopii kolorów).
   2) PALETA JEDNEJ SEKCJI: najedź i kliknij sekcję → panel z paletami aktywnego zestawu + 12 klasycznych zestawień + własne kolory + „Odwróć”.
   Zmiany to zmienne CSS sekcji (--surface, --ink, --small-ink, --accent, --hover-ink, --hover-accent) ustawione inline,
   więc nie dotykają plików; „Kopiuj zmiany” daje Markdown do wklejenia w rozmowie. Esc / K zamyka nakładkę (zmiany zostają do odświeżenia). */
(function () {
  "use strict";
  if (window.__paleta) return;

  // Klasyczne zestawienia z mody i wnętrz (dwanaście; kolejność = rzędy po trzy: jasna/ciemna na przemian). Te same kolory są tokenami w theme.json.
  // Zieleń Psyjaciół (#124e36, tło hero) jest stała — pierwsza paleta ma ją jako tło. Kontrast tekst/tło ≥ 5,7:1, tekst/akcent ≥ 4,5:1 (pomiar WCAG 2.x).
  // [nazwa, surface = tło, ink = tekst/rysunek, small = tekst mały (ink 14 % w stronę czerni/bieli; panel i tak liczy to sam),
  //  accent = tło uzupełniające (karty, kształty), hover = kolor po najechaniu (panel używa small)]
  var PRESETS = [
    ["Szmaragd i szampan",       "#124e36", "#f0e4cc", "#f2e8d3", "#1d6a4b", "#f2e8d3"],
    ["Ecru i zieleń",            "#f3ecdc", "#124e36", "#0f432e", "#e5dac1", "#0f432e"],
    ["Wielbłąd i czekolada",  "#d8bc94", "#3a2216", "#321d13", "#c8a87a", "#321d13"],
    ["Burgund i róż",         "#5a1828", "#f4dad2", "#f6dfd8", "#74293b", "#f6dfd8"],
    ["Róż pudrowy i burgund", "#f1dcd4", "#5a1828", "#4d1522", "#e6c5bc", "#4d1522"],
    ["Terakota i krem",       "#9c4326", "#fcf0e2", "#fcf2e6", "#af5434", "#fcf2e6"],
    ["Granat i wielbłąd",     "#14213d", "#e2c79c", "#e6cfaa", "#1f3358", "#e6cfaa"],
    ["Błękit i granat",          "#c9d6e3", "#14213d", "#111c34", "#b6c7d8", "#111c34"],
    ["Oliwka i kość słoniowa","#51542b", "#f5f0e0", "#f6f2e4", "#626637", "#f6f2e4"],
    ["Czerń i kość słoniowa", "#181513", "#f1eadb", "#f3ede0", "#2b2724", "#f3ede0"],
    ["Greige i czerń",        "#d6ccbe", "#1e1a17", "#1a1614", "#c6baaa", "#1a1614"],
    ["Bakłażan i róż",        "#3b1f40", "#ebd5d8", "#eedbdd", "#512f58", "#eedbdd"]
  ];
  var VARS = ["--surface", "--ink", "--small-ink", "--accent", "--hover-ink", "--hover-accent"];
  // Zestawy palet całej strony. id = wartość html[data-paleta] (szlachetna = brak atrybutu); kolory są w palety-zestawy.css i style sekcji.
  var SETS = [
    { id: "szlachetna", name: "Szlachetna", desc: "szmaragd, ecru, terakota, granat — klasyka z mody (domyślna)" },
    { id: "poprzednia", name: "Poprzednia", desc: "zielone ściany, brzoskwinia, szałwia, kobalt" },
    { id: "fac", name: "Feminist Art Coalition", desc: "krem, głęboka zieleń, mięta, koral" }
  ];
  var SET_KEY = "psyjaciele-paleta";
  // Role sekcji, z których składa się zestaw: [etykieta, klasy, znacznik]. Klasy dają te same reguły palet co prawdziwe sekcje.
  var ROLES = [["Hero", "hero"], ["Usługi", "services"], ["Zaproszenie", "booking"], ["O nas", "about"], ["Przychodnia", "clinic"], ["Zespół", "team"],
    ["Opinie", "reviews"], ["Nagłe przypadki", "emergency"], ["Przed wizytą", "arrival preparation"], ["Dojazd", "arrival"], ["Pytania", "arrival preparation faq"],
    ["Kontakt", "contact"], ["Stopka", "", "footer"]];
  var STRIP = [0, 1, 2, 3, 5, 11, 12];   // role pokazane w podglądzie zestawu: hero, usługi, zaproszenie, o nas, zespół, kontakt, stopka
  var LABELS = ["Tło", "Tekst", "Tekst mały", "Akcent (karty, kształty)"];

  var on = false, sel = null, hot = null, changes = [], box, label, panel;

  function css() {
    var s = document.createElement("style");
    s.id = "paleta-css";
    s.textContent =
      ".pl-box{position:fixed;z-index:2147483000;pointer-events:none;border:3px dashed #ff2d95;box-sizing:border-box;display:none}" +
      ".pl-box.is-sel{border-style:solid;border-color:#00b7ff}" +
      ".pl-tag{position:fixed;z-index:2147483001;pointer-events:none;background:#ff2d95;color:#fff;font:600 12px/1 system-ui,sans-serif;padding:5px 8px;display:none}" +
      ".pl-panel{position:fixed;z-index:2147483002;left:16px;bottom:16px;width:340px;max-height:calc(100vh - 32px);overflow:auto;background:#111;color:#fff;font:13px/1.35 system-ui,sans-serif;padding:14px;box-shadow:0 8px 32px rgba(0,0,0,.4)}" +
      ".pl-panel *{box-sizing:border-box}.pl-panel h4{margin:0 0 8px;font-size:14px;color:#fff}.pl-panel p{margin:0 0 10px;color:#bbb}" +
      ".pl-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin-bottom:10px}" +
      ".pl-sw{border:2px solid #444;background:none;color:#fff;cursor:pointer;padding:0;text-align:left;font:inherit}.pl-sw:hover,.pl-sw:focus-visible{border-color:#fff;outline:0}" +
      ".pl-sw i{display:block;height:34px;position:relative}.pl-sw i b{position:absolute;left:8px;top:8px;width:18px;height:18px;border-radius:50%}.pl-sw i u{position:absolute;right:8px;bottom:6px;width:14px;height:14px}" +
      ".pl-sw span{display:block;padding:4px 6px;font-size:11px}" +
      ".pl-row{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-bottom:10px}.pl-row label{display:grid;gap:3px;font-size:11px;color:#bbb}" +
      ".pl-row input{width:100%;height:30px;padding:0;border:2px solid #444;background:none;cursor:pointer}" +
      ".pl-btns{display:flex;flex-wrap:wrap;gap:6px}.pl-btns button{background:#2a2a2a;color:#fff;border:0;padding:7px 10px;cursor:pointer;font:inherit}.pl-btns button:hover{background:#444}" +
      ".pl-panel [hidden]{display:none!important}" +
      ".pl-h{margin:10px 0 6px;font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:#888}.pl-h:first-of-type{margin-top:0}" +
      ".pl-sets{display:grid;gap:6px;margin-bottom:4px}" +
      ".pl-set{display:grid;grid-template-columns:auto 1fr;gap:10px;align-items:center;border:2px solid #444;background:none;color:#fff;cursor:pointer;padding:6px;text-align:left;font:inherit}.pl-set:hover,.pl-set:focus-visible{border-color:#fff;outline:0}.pl-set.is-on{border-color:#00b7ff}" +
      ".pl-chips{display:flex}.pl-chips i{display:block;width:13px;height:32px}" +
      ".pl-set b{display:block;font-size:12px}.pl-set small{display:block;color:#aaa;font-size:11px;line-height:1.3}" +
      ".pl-msg{margin-top:8px;color:#7ee787;min-height:16px}";
    document.head.appendChild(s);
  }

  function sectionOf(el) {
    if (!el || !el.closest) return null;
    if (panel && panel.contains(el)) return null;
    return el.closest("section, footer");
  }
  function nameOf(sec) {
    var h = sec.querySelector("h1,h2");
    var t = h ? (h.innerText || h.textContent).trim().replace(/\s+/g, " ").slice(0, 48) : "";
    return (sec.id ? "#" + sec.id : sec.tagName.toLowerCase() + "." + (sec.className || "").toString().split(" ")[0]) + (t ? " „" + t + "”" : "");
  }
  function selectorOf(sec) {
    if (sec.id) return "#" + sec.id;
    var all = Array.prototype.slice.call(document.querySelectorAll(sec.tagName.toLowerCase()));
    return sec.tagName.toLowerCase() + (sec.className ? "." + sec.className.toString().trim().split(/\s+/).join(".") : "") + " (nr " + (all.indexOf(sec) + 1) + ")";
  }
  function place(el, tag, sec) {
    if (!sec) { el.style.display = "none"; if (tag) tag.style.display = "none"; return; }
    var r = sec.getBoundingClientRect();
    el.style.cssText = "display:block;left:" + r.left + "px;top:" + r.top + "px;width:" + r.width + "px;height:" + r.height + "px";
  }
  function draw() {
    place(box, label, sel || hot);
    box.classList.toggle("is-sel", !!sel);
    var s = sel || hot;
    if (s) {
      var r = s.getBoundingClientRect();
      label.textContent = nameOf(s) + (sel ? " — wybrana" : " — kliknij");
      label.style.cssText = "display:block;left:" + Math.max(0, r.left) + "px;top:" + Math.max(0, r.top) + "px";
    } else label.style.display = "none";
  }

  // pochodne: „tekst mały” = tekst odrobinę dalej od tła (ciemniejszy na jasnym, jaśniejszy na ciemnym); „akcent” = tło lekko w stronę tekstu (linie, elementy graficzne)
  function rgb(h) { h = toHex(h); return [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)]; }
  function hex(a) { return "#" + a.map(function (n) { return ("0" + Math.max(0, Math.min(255, Math.round(n))).toString(16)).slice(-2); }).join(""); }
  function lum(a) { var f = function (v) { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }; return 0.2126 * f(a[0]) + 0.7152 * f(a[1]) + 0.0722 * f(a[2]); }
  function mix(a, b, t) { return a.map(function (v, i) { return v + (b[i] - v) * t; }); }
  function deriveSmall(surface, ink) { var s = rgb(surface), i = rgb(ink); return hex(mix(i, lum(s) > lum(i) ? [0, 0, 0] : [255, 255, 255], 0.14)); }
  function deriveAccent(surface, ink) { return hex(mix(rgb(surface), rgb(ink), 0.16)); }
  var touched = [];

  function cur(sec, v) { return (getComputedStyle(sec).getPropertyValue(v) || "").trim(); }
  function toHex(c) {
    if (!c) return "#000000";
    if (c.charAt(0) === "#") return c.length === 4 ? "#" + c[1] + c[1] + c[2] + c[2] + c[3] + c[3] : c.slice(0, 7);
    var m = /rgba?\((\d+),\s*(\d+),\s*(\d+)/.exec(c);
    if (!m) return "#000000";
    return "#" + [m[1], m[2], m[3]].map(function (n) { return ("0" + (+n).toString(16)).slice(-2); }).join("");
  }
  function record(sec) {
    for (var i = 0; i < changes.length; i++) if (changes[i].el === sec) return changes[i];
    var r = { el: sec, orig: {} };
    VARS.forEach(function (v) { r.orig[v] = sec.style.getPropertyValue(v); });
    changes.push(r);
    return r;
  }
  function set(sec, vals) {
    record(sec);
    VARS.forEach(function (v, i) { if (vals[i]) sec.style.setProperty(v, vals[i]); });
    refreshInputs();
    window.dispatchEvent(new Event("scroll"));
  }
  function apply(p) { if (sel) { touched[2] = touched[3] = null; var sm = deriveSmall(p[1], p[2]); set(sel, [p[1], p[2], sm, p[4], sm, p[1]]); } }
  function invert() { if (!sel) return; set(sel, [cur(sel, "--ink"), cur(sel, "--surface"), cur(sel, "--surface"), cur(sel, "--accent"), cur(sel, "--hover-ink"), cur(sel, "--ink")]); }
  function resetOne() {
    if (!sel) return;
    changes = changes.filter(function (r) { if (r.el !== sel) return true; VARS.forEach(function (v) { r.orig[v] ? sel.style.setProperty(v, r.orig[v]) : sel.style.removeProperty(v); }); return false; });
    refreshInputs();
  }
  function resetAll() {
    changes.forEach(function (r) { VARS.forEach(function (v) { r.orig[v] ? r.el.style.setProperty(v, r.orig[v]) : r.el.style.removeProperty(v); }); });
    changes = []; refreshInputs();
  }
  function copyAll() {
    var out = ["# Zmiany palet", "", "zestaw palet: **" + setName(curSet()) + "** (`?paleta=" + curSet() + "`)", ""];
    changes.forEach(function (r, i) {
      out.push((i + 1) + ". **" + selectorOf(r.el) + "** (" + nameOf(r.el) + ")");
      VARS.forEach(function (v) { var x = r.el.style.getPropertyValue(v); if (x) out.push("   - `" + v + ": " + x + "`"); });
    });
    out.push("", "adres: " + location.href.replace(/[?&]uwagi=1/, ""));
    var txt = out.join("\n");
    var ok = function () { msg("Skopiowano " + changes.length + " zmian(y)."); };
    if (navigator.clipboard) navigator.clipboard.writeText(txt).then(ok, function () { window.prompt("Skopiuj:", txt); });
    else window.prompt("Skopiuj:", txt);
  }
  function msg(t) { var m = panel.querySelector(".pl-msg"); if (m) m.textContent = t; }

  // ── zestawy palet ──────────────────────────────────────────────────────────────
  var tmp;
  function hexOf(v) {   // dowolny zapis koloru z CSS → #rrggbb
    v = (v || "").trim(); if (!v) return "#000000";
    if (v.charAt(0) === "#") return toHex(v);
    if (!tmp) { tmp = document.createElement("i"); tmp.style.cssText = "position:absolute;left:-9999px;visibility:hidden"; }
    document.body.appendChild(tmp); tmp.style.color = ""; tmp.style.color = v;
    var c = getComputedStyle(tmp).color; document.body.removeChild(tmp);
    return toHex(c);
  }
  function curSet() { return document.documentElement.getAttribute("data-paleta") || "szlachetna"; }
  function setName(id) { for (var i = 0; i < SETS.length; i++) if (SETS[i].id === id) return SETS[i].name; return id; }
  function writeAttr(id) { var r = document.documentElement; id === "szlachetna" ? r.removeAttribute("data-paleta") : r.setAttribute("data-paleta", id); }
  // Palety wszystkich ról danego zestawu: atrybut jest ustawiany, kolory czytane z niewidocznych próbek i atrybut wraca — w jednym kroku, bez przemalowania.
  function probe(id) {
    var prev = curSet(); writeAttr(id);
    var host = document.createElement("div");
    host.style.cssText = "position:absolute;left:-9999px;top:0;width:10px;height:10px;visibility:hidden;pointer-events:none";
    document.body.appendChild(host);
    var out = ROLES.map(function (r) {
      var el = document.createElement(r[2] || "section"); el.className = r[1]; host.appendChild(el);
      var cs = getComputedStyle(el);
      return [r[0], hexOf(cs.getPropertyValue("--surface")), hexOf(cs.getPropertyValue("--ink")), hexOf(cs.getPropertyValue("--accent"))];
    });
    document.body.removeChild(host); writeAttr(prev);
    return out;
  }
  var setPresets = [];
  function renderSets() {
    if (!panel) return;
    var now = curSet();
    panel.querySelector(".pl-sets").innerHTML = SETS.map(function (st) {
      var chips = probe(st.id), strip = STRIP.map(function (i) { return '<i style="background:' + chips[i][1] + '"></i>'; }).join("");
      return '<button type="button" class="pl-set' + (st.id === now ? " is-on" : "") + '" data-set="' + st.id + '" aria-pressed="' + (st.id === now) + '"><span class="pl-chips">' + strip + "</span><span><b>" + st.name + (st.id === now ? " ✓" : "") + "</b><small>" + st.desc + "</small></span></button>";
    }).join("");
    // palety sekcji aktywnego zestawu (dla domyślnego pomijamy — to te same kolory co w klasycznych dwunastu)
    var box2 = panel.querySelector(".pl-setgrid"), head = panel.querySelector(".pl-sethead");
    setPresets = [];
    if (now !== "szlachetna") {
      var seen = {};
      probe(now).forEach(function (r) { var k = r[1] + r[2]; if (!seen[k]) { seen[k] = 1; setPresets.push([r[0], r[1], r[2], "", r[3]]); } });
    }
    head.hidden = box2.hidden = !setPresets.length;
    head.textContent = "Palety sekcji — zestaw „" + setName(now) + "”";
    box2.innerHTML = setPresets.map(function (p, i) {
      return '<button type="button" class="pl-sw" data-sp="' + i + '" title="' + p[0] + '"><i style="background:' + p[1] + '"><b style="background:' + p[2] + '"></b><u style="background:' + p[4] + '"></u></i><span>' + p[0] + "</span></button>";
    }).join("");
  }
  function setSet(id) {
    if (curSet() === id) return;
    resetAll();   // zmiany ręczne dotyczyły poprzedniego zestawu
    writeAttr(id);
    try { id === "szlachetna" ? localStorage.removeItem(SET_KEY) : localStorage.setItem(SET_KEY, id); } catch (e) {}
    renderSets(); refreshInputs();
    window.dispatchEvent(new Event("scroll")); window.dispatchEvent(new Event("resize"));   // nagłówek i dolny pasek liczą kolory od nowa
    msg("Zestaw: " + setName(id) + ".");
  }

  function buildPanel() {
    panel = document.createElement("div");
    panel.className = "pl-panel";
    var sw = PRESETS.map(function (p, i) {
      return '<button type="button" class="pl-sw" data-i="' + i + '" title="' + p[0] + '"><i style="background:' + p[1] + '"><b style="background:' + p[2] + '"></b><u style="background:' + p[4] + '"></u></i><span>' + p[0] + "</span></button>";
    }).join("");
    var inputs = LABELS.map(function (l, i) { return '<label>' + l + '<input type="color" data-v="' + i + '"></label>'; }).join("");
    panel.innerHTML = '<h4>Palety <small style="color:#888">(K)</small></h4>' +
      '<div class="pl-h">Zestaw palet całej strony</div><div class="pl-sets"></div>' +
      '<div class="pl-h">Wybrana sekcja</div><p class="pl-name">Najedź na sekcję i kliknij, żeby ją wybrać.</p>' +
      '<div class="pl-h pl-sethead" hidden></div><div class="pl-grid pl-setgrid" hidden></div>' +
      '<div class="pl-h">Klasyczne zestawienia</div><div class="pl-grid">' + sw + '</div><div class="pl-row">' + inputs + '</div>' +
      '<div class="pl-btns"><button type="button" data-a="invert">Odwróć</button><button type="button" data-a="one">Przywróć sekcję</button><button type="button" data-a="all">Przywróć wszystko</button><button type="button" data-a="copy">Kopiuj zmiany</button><button type="button" data-a="close">Zamknij (K)</button></div><div class="pl-msg"></div>';
    document.body.appendChild(panel);
    panel.addEventListener("click", function (e) {
      var b = e.target.closest("button"); if (!b) return;
      if (b.hasAttribute("data-set")) setSet(b.getAttribute("data-set"));
      else if (b.hasAttribute("data-sp")) apply(setPresets[+b.getAttribute("data-sp")]);
      else if (b.hasAttribute("data-i")) apply(PRESETS[+b.getAttribute("data-i")]);
      else { var a = b.getAttribute("data-a"); if (a === "invert") invert(); else if (a === "one") resetOne(); else if (a === "all") resetAll(); else if (a === "copy") copyAll(); else if (a === "close") api.destroy(); }
    });
    panel.addEventListener("input", function (e) {
      var i = e.target.getAttribute && e.target.getAttribute("data-v"); if (i == null || !sel) return;
      var map = ["--surface", "--ink", "--small-ink", "--accent"]; record(sel);
      sel.style.setProperty(map[+i], e.target.value);
      if (+i === 0) sel.style.setProperty("--hover-accent", e.target.value);
      if (+i === 2 || +i === 3) touched[+i] = sel;
      if (+i < 2) {   // tło/tekst → pochodne (tekst mały, akcent), o ile ich ręcznie nie ustawiono
        var su = toHex(cur(sel, "--surface")), ik = toHex(cur(sel, "--ink"));
        if (touched[2] !== sel) { var sm = deriveSmall(su, ik); sel.style.setProperty("--small-ink", sm); sel.style.setProperty("--hover-ink", sm); }
        if (touched[3] !== sel) sel.style.setProperty("--accent", deriveAccent(su, ik));
        refreshInputs();
      }
    });
  }
  function refreshInputs() {
    if (!panel) return;
    var n = panel.querySelector(".pl-name");
    n.textContent = sel ? nameOf(sel) : "Najedź na sekcję i kliknij, żeby ją wybrać.";
    ["--surface", "--ink", "--small-ink", "--accent"].forEach(function (v, i) {
      var inp = panel.querySelector('[data-v="' + i + '"]'); if (inp) { inp.disabled = !sel; if (sel) inp.value = toHex(cur(sel, v)); }
    });
  }

  function onMove(e) { if (panel.contains(e.target)) { hot = null; draw(); return; } hot = sectionOf(e.target); draw(); }
  function onClick(e) {
    if (panel.contains(e.target)) return;
    var s = sectionOf(e.target); if (!s) return;
    e.preventDefault(); e.stopPropagation();
    sel = s; refreshInputs(); draw();
  }
  function onKey(e) { if (e.key === "Escape") api.destroy(); }
  function onScroll() { draw(); }

  var api = {
    start: function () {
      if (on) return; on = true;
      if (window.__uwagi && window.__uwagi.destroy) window.__uwagi.destroy();
      css();
      box = document.createElement("div"); box.className = "pl-box"; label = document.createElement("div"); label.className = "pl-tag";
      document.body.appendChild(box); document.body.appendChild(label);
      buildPanel(); renderSets(); refreshInputs();
      document.addEventListener("mousemove", onMove, true);
      document.addEventListener("click", onClick, true);
      document.addEventListener("keydown", onKey, true);
      window.addEventListener("scroll", onScroll, { passive: true });
      window.addEventListener("resize", onScroll);
    },
    destroy: function () {
      if (!on) return; on = false;
      document.removeEventListener("mousemove", onMove, true);
      document.removeEventListener("click", onClick, true);
      document.removeEventListener("keydown", onKey, true);
      window.removeEventListener("scroll", onScroll);
      window.removeEventListener("resize", onScroll);
      [box, label, panel, document.getElementById("paleta-css")].forEach(function (n) { if (n && n.parentNode) n.parentNode.removeChild(n); });
      sel = hot = null;
    },
    toggle: function () { on ? api.destroy() : api.start(); },
    setSet: setSet,
    isOn: function () { return on; }
  };
  window.__paleta = api;
})();
