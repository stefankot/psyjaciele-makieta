/*
  layout-header.js — tło stałego paska (header) dopasowane do sekcji pod spodem.
  Kolor tekstu (--nav-ink) nadal ustawia minimal.js; tu ustawiamy tylko --header-bg
  i dla sekcji o dzielonym tle (rezerwacja, obserwuj nas) wymuszamy papier + zieleń.
*/
(() => {
  const header = document.querySelector('.site-header');
  if (!header) return;
  const hero = document.querySelector('.hero');
  const sections = [...document.querySelectorAll('main > section, body > footer')];
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
    const probe = header.getBoundingClientRect().height / 2;
    const section = y <= 16
      ? hero
      : sections.find(s => { const r = s.getBoundingClientRect(); return r.top <= probe && r.bottom > probe; }) || hero;
    let bg = section ? solidBg(section) : null;
    if (!bg || (section && flat.some(c => section.classList.contains(c)))) {
      bg = PAPER;
      header.style.setProperty('--nav-ink', GREEN);
    }
    header.style.setProperty('--header-bg', bg);
  }

  function schedule() {
    if (!ticking) { ticking = true; requestAnimationFrame(update); }
  }

  window.addEventListener('scroll', schedule, { passive: true });
  window.addEventListener('resize', schedule, { passive: true });
  update();
})();
