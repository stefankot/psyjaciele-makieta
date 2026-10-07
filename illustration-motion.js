// Keep the static first frame until the illustration is visible.
(() => {
  const images = [...document.querySelectorAll('img[data-animated-src]')];
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const visible = new Set();
  const started = new Set();
  let heroReady = false;
  function start(image) {
    if (reducedMotion.matches || started.has(image) || !visible.has(image)) return;
    if (image.closest('.hero') && !heroReady) return;
    started.add(image);
    const still = image.src;
    image.addEventListener('error', () => { image.src = still; }, { once: true });
    image.loading = 'eager';
    image.fetchPriority = 'low';
    image.src = image.dataset.animatedSrc;
  }
  function afterPageLoad() {
    setTimeout(() => {
      heroReady = true;
      images.forEach(start);
    }, 3000);
  }
  if (document.readyState === 'complete') afterPageLoad();
  else window.addEventListener('load', afterPageLoad, { once: true });
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          visible.add(entry.target);
          start(entry.target);
        } else visible.delete(entry.target);
      });
    }, { threshold: .12 });
    images.forEach(image => observer.observe(image));
  } else {
    images.forEach(image => { visible.add(image); start(image); });
  }
  reducedMotion.addEventListener('change', () => {
    if (!reducedMotion.matches) images.forEach(start);
  });
})();
