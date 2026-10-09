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
