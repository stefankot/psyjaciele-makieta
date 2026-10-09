// Keep the static first frame until the illustration is visible.
(() => {
  const images = [...document.querySelectorAll('img[data-animated-src]')];
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const visible = new Set();
  const started = new Set();
  const heroImages = images.filter(image => image.closest('.hero'));
  const heroLoads = new Map();
  function prepareHero(image) {
    if (reducedMotion.matches || heroLoads.has(image)) return;
    // Fetch bytes immediately, without decoding/playing the animation early.
    const load = fetch(image.dataset.animatedSrc)
      .then(response => {
        if (!response.ok) throw new Error('Illustration could not be loaded');
        return response.blob();
      });
    heroLoads.set(image, load);
    Promise.all([
      load,
      new Promise(resolve => setTimeout(resolve, Math.max(0, 3000 - performance.now())))
    ]).then(([blob]) => {
      if (reducedMotion.matches || started.has(image)) return;
      const still = image.src;
      const url = URL.createObjectURL(blob);
      started.add(image);
      image.addEventListener('error', () => {
        image.src = still;
        URL.revokeObjectURL(url);
      }, { once: true });
      image.src = url;
      image.dataset.animationStartedAt = String(performance.now());
    }).catch(() => { heroLoads.delete(image); });
  }
  function start(image) {
    if (reducedMotion.matches || started.has(image) || !visible.has(image)) return;
    if (image.closest('.hero')) return;
    started.add(image);
    const still = image.src;
    image.addEventListener('error', () => { image.src = still; }, { once: true });
    image.loading = 'eager';
    image.fetchPriority = 'low';
    image.src = image.dataset.animatedSrc;
  }
  heroImages.forEach(prepareHero);
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
    if (!reducedMotion.matches) {
      heroLoads.clear();
      heroImages.forEach(prepareHero);
      images.forEach(start);
    }
  });
})();
