/*
  layout-status.js — wskaźnik „otwarte / zamknięte” (czas Warszawy; godziny jak w nagłówku: Pn–Pt 9:00–20:00, Sob–Nd 10:00–14:00).
  1. „Otwarte teraz” w hero ([data-hero-status]); poza godzinami chip prowadzi do kontaktu i lecznic całodobowych.
  2. Krótki wskaźnik (kropka + słowo) przy każdym numerze telefonu przychodni, który stoi sam, czyli poza przyciskami hero
     (te mają własny status), z wyjątkiem paska sticky-cta: nagłówek, rezerwacja, kontakt, stopka. Pełna kropka = otwarte, pusta = zamknięte.
*/
(() => {
  const PHONE = 'a[href="tel:+48537821345"]';
  const HOURS = { weekday: [9, 20], weekend: [10, 14] };

  function warsawNow() {
    const parts = new Intl.DateTimeFormat('en-GB', {
      timeZone: 'Europe/Warsaw', weekday: 'short', hour: '2-digit', minute: '2-digit', hour12: false
    }).formatToParts(new Date());
    const get = t => parts.find(p => p.type === t).value;
    const map = { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 };
    return { day: map[get('weekday')], minutes: (+get('hour') % 24) * 60 + +get('minute') };
  }
  const hoursFor = d => (d === 0 || d === 6 ? HOURS.weekend : HOURS.weekday);
  const fmt = h => `${h}:00`;

  function current() {
    const { day, minutes } = warsawNow();
    const [open, close] = hoursFor(day);
    if (minutes >= open * 60 && minutes < close * 60) {
      const left = close * 60 - minutes;
      return { state: left <= 60 ? 'closing' : 'open', close, day, minutes };
    }
    let d = day, label = 'dziś';
    if (minutes >= close * 60) { d = (day + 1) % 7; label = 'jutro'; }
    return { state: 'closed', label, from: hoursFor(d)[0], day, minutes };
  }

  // Wskaźnik tylko tam, gdzie numer stoi sam; numer w ciągłym tekście (akapit, element listy) go nie dostaje.
  function inRunningText(a) {
    const p = a.parentElement;
    return !!p && /^(P|LI)$/.test(p.tagName) && (p.textContent.length - a.textContent.length) > 30;
  }

  const hero = document.querySelector('[data-hero-status]');
  const phones = Array.from(document.querySelectorAll(PHONE)).filter(a => !a.closest('.hero-actions, .sticky-cta') && !a.matches('.header-call') && !inRunningText(a));
  const tags = phones.map(a => {
    const s = document.createElement('span');
    s.className = 'phone-status';
    a.appendChild(s);
    return s;
  });

  function render() {
    const st = current();
    if (hero) {
      let text;
      if (st.state === 'closed') text = `Zamknięte — ${st.label} od ${fmt(st.from)}. Nagły przypadek?`;
      else text = st.state === 'closing' ? `Otwarte jeszcze do ${fmt(st.close)}` : `Otwarte teraz — do ${fmt(st.close)}`;
      hero.textContent = text;
      hero.dataset.state = st.state;
      hero.setAttribute('href', st.state === 'closed' ? '#after-hours-title' : (document.getElementById('zapraszamy') ? '#zapraszamy' : '#kontakt'));
      hero.hidden = false;
    }
    const word = st.state === 'closed' ? `zamknięte — ${st.label} od ${fmt(st.from)}` : (st.state === 'closing' ? `otwarte jeszcze do ${fmt(st.close)}` : `otwarte do ${fmt(st.close)}`);
    const title = st.state === 'closed' ? `Przychodnia zamknięta — ${st.label} od ${fmt(st.from)}` : `Przychodnia otwarta do ${fmt(st.close)}`;
    tags.forEach(t => { t.textContent = word; t.dataset.state = st.state === 'closed' ? 'closed' : 'open'; t.title = title; });
  }
  render();
  setInterval(render, 60000);
})();
