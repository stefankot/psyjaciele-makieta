/*
  nowa-readability.js — wybór nawigacji (ładowany synchronicznie w <head>, żeby nie było „mrugnięcia”).
  html.bar        → nowy stały pasek (telefon ≤ 700 px ORAZ tryb większej czytelności)
  html.is-large-ui → przeglądarka ustawiona na większą czytelność:
                     domyślny rozmiar czcionki przeglądarki ≥ 18 px albo systemowe „większy kontrast”
                     (powiększenie strony zoomem NIE jest wykrywane — okno podglądu dawało fałszywe alarmy)
  W pozostałych przypadkach (desktop, tablet) działa nawigacja jak w oryginale.
  Wymuszenie do testów: ?bar=1 (nowy pasek) lub ?bar=0 (nawigacja jak w oryginale).
*/
(() => {
  const root = document.documentElement;
  const force = new URLSearchParams(location.search).get('bar');
  const narrow = matchMedia('(max-width: 700px)');
  const contrast = matchMedia('(prefers-contrast: more)');

  function largeUi() {
    if (force === '1') return true;
    if (force === '0') return false;
    const fontSize = parseFloat(getComputedStyle(root).fontSize) || 16;
    return fontSize >= 18 || contrast.matches;
  }

  function apply() {
    const large = largeUi();
    root.classList.toggle('is-large-ui', large);
    root.classList.toggle('bar', large || narrow.matches);
  }

  apply();
  narrow.addEventListener('change', apply);
  contrast.addEventListener('change', apply);
  window.addEventListener('resize', apply, { passive: true });
})();

/*
  Zestaw palet (nakładka K → „Zestaw palet całej strony”): ?paleta=poprzednia | fac | szlachetna w adresie albo wartość zapamiętana w localStorage
  → html[data-paleta]. Brak atrybutu = zestaw domyślny (szlachetna). Ustawiane tu, synchronicznie w <head>, żeby kolory nie „mrugały”.
  Definicje zestawów: palety-zestawy.css.
*/
(() => {
  const KEY = 'psyjaciele-paleta';
  try {
    const q = new URLSearchParams(location.search).get('paleta');
    if (q !== null) { q === '' || q === 'szlachetna' ? localStorage.removeItem(KEY) : localStorage.setItem(KEY, q); }
    const v = q !== null ? q : localStorage.getItem(KEY);
    if (v && v !== 'szlachetna' && /^[a-z0-9-]{2,24}$/.test(v)) document.documentElement.setAttribute('data-paleta', v);
  } catch (e) { /* localStorage zablokowany: zestaw domyślny */ }
})();
