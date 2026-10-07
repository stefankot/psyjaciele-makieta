/* Psyjaciele — warstwa ruchu, wersja 3 (para z animacje.css). Dołącz po minimal.js.
   API: window.PsyjacieleRuch.enable() / .disable(). */
(function(){
  var root = document.documentElement;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  var observers = [], cleanups = [], enabled = false;

  function onScreen(el){ var r = el.getBoundingClientRect(); return r.top < innerHeight && r.bottom > 0; }
  function once(els, cb, opts){
    if(!('IntersectionObserver' in window)){ els.forEach(cb); return; }
    var io = new IntersectionObserver(function(entries){ entries.forEach(function(e){ if(e.isIntersecting){ io.unobserve(e.target); cb(e.target); } }); }, opts);
    els.forEach(function(el){ io.observe(el); }); observers.push(io);
  }

  /* ── stałe poprawki i informacje (działają też bez ruchu) ── */
  function arrows(){
    document.querySelectorAll('.type-arrow').forEach(function(a){
      a.classList.toggle('is-diagonal', /[↗↘↖↙]/.test(a.textContent));
      if(a.querySelector('.type-arrow-glyph')) return;
      var g = document.createElement('span'); g.className = 'type-arrow-glyph'; g.textContent = a.textContent; a.textContent = ''; a.appendChild(g);
    });
  }
  function openNow(){
    var rows = document.querySelectorAll('.site-header .header-hours > div'); if(rows.length < 2) return;
    var parts = new Intl.DateTimeFormat('en-GB', {timeZone:'Europe/Warsaw', weekday:'short', hour:'2-digit', minute:'2-digit', hour12:false}).formatToParts(new Date());
    var get = function(t){ return (parts.find(function(p){ return p.type === t; }) || {}).value; };
    var weekend = /Sat|Sun/.test(get('weekday')); var row = rows[weekend ? 1 : 0];
    var range = (row.querySelector('dd').textContent.match(/(\d{1,2})[:.](\d{2})\D+(\d{1,2})[:.](\d{2})/) || []).map(Number);
    if(range.length < 5) return;
    var now = (+get('hour')) * 60 + (+get('minute')), close = range[3]*60 + range[4], open = now >= range[1]*60 + range[2] && now < close;
    var closing = open && close - now <= 60;
    rows.forEach(function(r){ r.classList.remove('is-today','is-open','is-closing'); r.removeAttribute('title'); });
    row.classList.add('is-today'); row.classList.toggle('is-open', open); row.classList.toggle('is-closing', closing);
    row.title = (closing ? 'Zamykamy za mniej niż godzinę' : open ? 'Teraz otwarte' : 'Teraz zamknięte') + ' (według stałych godzin)';
  }
  function rating(animated){
    var icon = document.querySelector('.reviews .review-source .icon'); if(!icon) return;
    var m = icon.parentElement.textContent.match(/(\d)[,.](\d)\s*na podstawie/); if(!m) return;
    var value = Math.min(5, parseFloat(m[1] + '.' + m[2]));
    var url = (getComputedStyle(icon).getPropertyValue('--icon').match(/url\(["']?([^"')]+)/) || [])[1]; if(!url) return;
    function apply(ratio){
      var w = icon.clientWidth, h = icon.clientHeight, drawn = Math.min(w, h * ratio);
      icon.style.setProperty('--rating-cut', (w - drawn * value / 5).toFixed(1) + 'px');
      icon.style.setProperty('--stars-none', w + 'px'); icon.style.setProperty('--stars-all', (w - drawn).toFixed(1) + 'px');
      if(!animated || onScreen(icon) || !('IntersectionObserver' in window)){ icon.classList.add('is-rated'); return; }
      icon.classList.add('will-rate');
      // start dopiero, gdy gwiazdki są wyraźnie w oknie (nie przy samej dolnej krawędzi)
      var io = new IntersectionObserver(function(entries){
        if(!entries[0].isIntersecting) return; io.disconnect();
        function settle(){ icon.classList.add('is-rated'); icon.classList.remove('is-rating','will-rate'); }
        if(!enabled){ settle(); return; }
        icon.classList.add('is-rating'); icon.classList.remove('will-rate');
        icon.addEventListener('animationend', settle, {once:true}); setTimeout(settle, 2200);
      }, {threshold:.6, rootMargin:'0px 0px -22% 0px'});
      io.observe(icon.parentElement);
    }
    // proporcje ikony z viewBox (naturalWidth zaokrągla wymiary SVG do pikseli)
    fetch(url).then(function(r){ return r.text(); }).then(function(svg){
      var vb = (svg.match(/viewBox="([^"]+)"/) || [])[1]; var p = vb ? vb.trim().split(/[\s,]+/).map(Number) : null;
      if(p && p[2] > 0 && p[3] > 0) apply(p[2] / p[3]); else throw 0;
    }).catch(function(){ var img = new Image(); img.onload = function(){ apply(img.naturalWidth / img.naturalHeight); }; img.src = url; });
  }

  /* ── ruch ── */
  var small = window.matchMedia('(max-width: 700px)');
  var AMP = {big: 2, service: 1.5, phone: .6};          // przesunięcie kreski w px; na telefonach × 0,6
  function saving(){ var c = navigator.connection; return !!(c && c.saveData); }
  function boilScale(){
    var k = small.matches ? AMP.phone : 1;
    document.querySelectorAll('#boil-filters feDisplacementMap').forEach(function(m){
      m.setAttribute('scale', ((m.parentNode.id.indexOf('boil-s') === 0 ? AMP.service : AMP.big) * k).toFixed(2));
    });
  }
  function boil(){
    if(saving()) return;                                  // oszczędzanie danych: ilustracje stoją
    if(!document.getElementById('boil-1')){
      var svg = document.createElementNS('http://www.w3.org/2000/svg','svg');
      svg.setAttribute('width','0'); svg.setAttribute('height','0'); svg.setAttribute('aria-hidden','true'); svg.id = 'boil-filters';
      function set(prefix, freq){ return [3, 11, 23, 37].map(function(seed, i){
        return '<filter id="' + prefix + (i+1) + '" x="-4%" y="-4%" width="108%" height="108%"><feTurbulence type="fractalNoise" baseFrequency="' + freq + '" numOctaves="1" seed="' + seed + '"/><feDisplacementMap in="SourceGraphic" scale="1" xChannelSelector="R" yChannelSelector="G"/></filter>'; }).join(''); }
      svg.innerHTML = set('boil-', 0.028) + set('boil-s', 0.045);   // duże ilustracje / małe rysunki usług
      document.body.appendChild(svg);
    }
    boilScale(); small.addEventListener('change', boilScale);
    var els = [].slice.call(document.querySelectorAll('figure.section-illustration, img.service-art')), paused = false, io = null;
    function resumeVisible(){ els.forEach(function(el){ el.classList.toggle('is-boiling', enabled && !paused && !document.hidden && (io ? el.dataset.inView === '1' : true)); }); }
    document.addEventListener('visibilitychange', resumeVisible);
    cleanups.push(function(){ document.removeEventListener('visibilitychange', resumeVisible); });
    els.forEach(function(el){ el.style.animationDelay = '-' + Math.round(Math.random() * 720) + 'ms'; });
    function setAll(on){ els.forEach(function(el){ el.classList.toggle('is-boiling', on); }); }
    if(!('IntersectionObserver' in window)) setAll(true);
    else {
      io = new IntersectionObserver(function(entries){ entries.forEach(function(e){ e.target.dataset.inView = e.isIntersecting ? '1' : ''; e.target.classList.toggle('is-boiling', e.isIntersecting && !paused && !document.hidden); }); }, {rootMargin:'40px 0px'});
      els.forEach(function(el){ io.observe(el); }); observers.push(io);
    }
    // słaba bateria bez ładowania: pętla staje, po podłączeniu wraca
    if(navigator.getBattery) navigator.getBattery().then(function(bt){
      if(!enabled) return;
      function check(){ paused = !bt.charging && bt.level <= .2; resumeVisible(); }
      bt.addEventListener('levelchange', check); bt.addEventListener('chargingchange', check); check();
      cleanups.push(function(){ bt.removeEventListener('levelchange', check); bt.removeEventListener('chargingchange', check); });
    }).catch(function(){});
    cleanups.push(function(){ small.removeEventListener('change', boilScale); els.forEach(function(el){ el.classList.remove('is-boiling'); el.style.animationDelay = ''; delete el.dataset.inView; }); });
  }
  function rules(){
    var els = [].filter.call(document.querySelectorAll('.ruled-columns > div, .ruled-columns > article, .equipment-grid > div'), function(el){
      return !onScreen(el) && parseFloat(getComputedStyle(el).borderTopWidth) > 0;
    });
    els.forEach(function(el){ el.classList.add('rule-wait'); el.style.setProperty('--i', [].indexOf.call(el.parentElement.children, el) % 3); });
    once(els, function(el){
      el.classList.add('rule-draw'); el.classList.remove('rule-wait');
      el.addEventListener('animationend', function done(e){ if(e.animationName !== 'rule-draw') return; el.removeEventListener('animationend', done); el.classList.remove('rule-draw'); });
    }, {threshold:0, rootMargin:'0px 0px -24% 0px'});     // linia musi wejść na ok. 1/4 wysokości okna od dołu
    cleanups.push(function(){ document.querySelectorAll('.rule-wait,.rule-draw').forEach(function(el){ el.classList.remove('rule-wait','rule-draw'); }); });
  }
  function landing(){
    function whenScrollStops(cb){
      var done = false, last = scrollY, still = 0, timer;
      function finish(){ if(done) return; done = true; clearInterval(timer); removeEventListener('scrollend', finish); setTimeout(cb, 180); }
      if('onscrollend' in window) addEventListener('scrollend', finish, {once:true});
      timer = setInterval(function(){ if(scrollY === last){ if(++still >= 4) finish(); } else { still = 0; last = scrollY; } }, 60);
      setTimeout(finish, 4000);
    }
    function onClick(e){
      var a = e.target.closest('a[href^="#"]'); if(!a || a.getAttribute('href').length < 2) return;
      var target = document.getElementById(decodeURIComponent(a.getAttribute('href').slice(1))); if(!target) return;
      var heading = target.matches('h1,h2,h3') ? target : target.querySelector('h2,h3'); if(!heading) return;
      var mark = heading.querySelector('em') || heading;
      setTimeout(function(){ whenScrollStops(function(){
        if(!enabled) return;
        mark.classList.remove('is-landed'); void mark.offsetWidth; mark.classList.add('is-landed');
        mark.addEventListener('animationend', function(){ mark.classList.remove('is-landed'); }, {once:true});
      }); }, 80);
    }
    document.addEventListener('click', onClick);
    cleanups.push(function(){ document.removeEventListener('click', onClick); });
  }
  function pets(){
    var list = [].slice.call(document.querySelectorAll('.hero-links .hero-inline-pet')); if(!list.length) return;
    var hero = document.querySelector('.hero'), visible = true, turn = 0, timer, popped;
    function frameOf(p){ return p.dataset.frame; }
    function show(pet, animate){
      var used = list.map(frameOf), n;
      do { n = Math.floor(Math.random() * 64); } while(used.indexOf(String(n)) > -1);
      pet.dataset.frame = n;
      pet.style.setProperty('--pet-x', (n % 8 * 100 / 7) + '%'); pet.style.setProperty('--pet-y', (Math.floor(n / 8) * 100 / 7) + '%');
      if(!animate) return;
      pet.classList.remove('is-swapping'); void pet.offsetWidth; pet.classList.add('is-swapping');
      setTimeout(function(){ pet.classList.remove('is-swapping'); }, 400);
    }
    popped = setTimeout(function(){ list.forEach(function(p){ p.classList.add('is-popped'); }); }, 1600);
    timer = setInterval(function(){ if(!visible || document.hidden || saving()) return; show(list[turn % list.length], true); turn++; }, 2800);   // jedno zdjęcie na raz, po kolei
    function over(e){ var pet = e.target.closest && e.target.closest('.hero-inline-pet'); if(pet && pet.classList.contains('is-popped')) show(pet, true); }
    document.addEventListener('pointerover', over);
    if(hero && 'IntersectionObserver' in window){ var io = new IntersectionObserver(function(en){ visible = en[0].isIntersecting; }); io.observe(hero); observers.push(io); }
    cleanups.push(function(){ clearInterval(timer); clearTimeout(popped); document.removeEventListener('pointerover', over); list.forEach(function(p){ p.classList.remove('is-swapping','is-popped'); }); });
  }
  function progress(){
    var bar = document.createElement('div'); bar.className = 'scroll-progress'; bar.setAttribute('aria-hidden','true'); document.body.appendChild(bar);
    var ticking = false;
    function update(){ ticking = false; var max = root.scrollHeight - innerHeight; bar.style.setProperty('--progress', max > 0 ? Math.min(1, scrollY / max).toFixed(4) : 0); }
    function onScroll(){ if(!ticking){ ticking = true; requestAnimationFrame(update); } }
    addEventListener('scroll', onScroll, {passive:true}); addEventListener('resize', onScroll); update();
    cleanups.push(function(){ removeEventListener('scroll', onScroll); removeEventListener('resize', onScroll); bar.remove(); });
  }

  function enable(){
    if(enabled || reduce.matches) return; enabled = true;
    root.classList.add('motion'); boil(); rules(); landing(); pets(); progress();
  }
  function disable(){
    if(!enabled) return; enabled = false;
    observers.forEach(function(io){ io.disconnect(); }); observers = [];
    cleanups.forEach(function(fn){ fn(); }); cleanups = [];
    root.classList.remove('motion');
  }
  function init(){
    arrows(); openNow(); setInterval(openNow, 60000);
    var auto = !root.hasAttribute('data-ruch-off');
    rating(!reduce.matches);
    if(auto) enable();
    reduce.addEventListener('change', function(){ if(reduce.matches) disable(); else if(auto) enable(); });
  }
  window.PsyjacieleRuch = {enable: enable, disable: disable};
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
