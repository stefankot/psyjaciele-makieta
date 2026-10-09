/* inspektor.js — skrót klawiszowy „I” włącza/wyłącza inspektor uwag (narzędzie do zaznaczania elementów i zbierania poprawek).
   Klik w element zapisuje uwagę z selektorem CSS, wymiarami w siatce, stylem i fragmentem HTML; „Kopiuj wszystko” daje Markdown
   do wklejenia w rozmowie z Claude. Działa na localhost, 127.0.0.1 i file://; na stronie publicznej tylko po dopisaniu ?uwagi=1.
   Ładuje _generator/narzedzia/uwagi.js dopiero przy pierwszym użyciu. */
(function () {
  "use strict";
  var self = document.currentScript && document.currentScript.src;
  if (!self) return;
  var LOCAL = /^(localhost|127\.0\.0\.1|\[::1\]|)$/.test(location.hostname) || location.protocol === "file:";
  var flag = false;   // inspektor zawsze startuje zamknięty; otwiera go dopiero klawisz I (lub ?uwagi=1 w adresie)
  try { sessionStorage.removeItem("uwagi-on"); } catch (e) {}
  var q = /[?&]uwagi=([01])/.exec(location.search);
  flag = !!(q && q[1] === "1");
  var loading = false;

  function load(done) {
    if (window.__uwagi) { done(window.__uwagi); return; }
    if (loading) return;
    loading = true;
    var s = document.createElement("script");
    s.src = new URL("_generator/narzedzia/uwagi.js", self).href + "?v=" + Date.now();
    s.onload = function () { loading = false; if (done) done(window.__uwagi); };
    s.onerror = function () { loading = false; console.warn("inspektor: nie znaleziono _generator/narzedzia/uwagi.js"); };
    document.body.appendChild(s);
  }
  function toggle() {
    if (window.__uwagi) { window.__uwagi.destroy(); return; }
    load(function (api) { if (api && api.pick) api.pick(true); });
  }
  document.addEventListener("keydown", function (e) {
    if ((e.key !== "i" && e.key !== "I") || e.metaKey || e.ctrlKey || e.altKey) return;
    if (/^(INPUT|TEXTAREA|SELECT)$/.test((e.target.tagName || "")) || e.target.isContentEditable) return;
    if (!LOCAL && !flag) return;
    e.preventDefault();
    toggle();
  });
  if (flag) load(function (api) { if (api && api.pick) api.pick(true); });
})();
