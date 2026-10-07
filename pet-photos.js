// Each photo belongs to one section and one circle, including animated hero swaps.
(() => {
  const ranges = { founders: [0, 64], booking: [64, 84], hero: [84, 128] };
  const assigned = new Map();
  const used = new Set();
  function available(group) {
    const [start, end] = ranges[group];
    return Array.from({ length: end - start }, (_, i) => start + i).filter(id => !used.has(id));
  }
  function apply(element, id) {
    const frame = id % 64;
    element.dataset.petPhoto = String(id);
    element.dataset.frame = String(id);
    element.style.setProperty('--pet-atlas', `url(assets/${id < 64 ? 'pets-phone-atlas.png' : 'pets-phone-atlas-unique-v2.png'})`);
    element.style.setProperty('--pet-x', `${frame % 8 * 100 / 7}%`);
    element.style.setProperty('--pet-y', `${Math.floor(frame / 8) * 100 / 7}%`);
  }
  function assign(element, group) {
    if (assigned.has(element)) return assigned.get(element).id;
    const id = available(group)[0];
    if (id === undefined) throw new Error(`No unique pet photos remaining for ${group}`);
    used.add(id);
    assigned.set(element, { id, group });
    apply(element, id);
    return id;
  }
  function swap(element) {
    const previous = assigned.get(element);
    if (!previous) return;
    const pool = available(previous.group);
    if (!pool.length) return;
    const id = pool[Math.floor(Math.random() * pool.length)];
    used.delete(previous.id);
    used.add(id);
    assigned.set(element, { id, group: previous.group });
    apply(element, id);
  }
  window.psyPetPhotos = { assign, swap };
  document.querySelectorAll('.hero-inline-pet').forEach(element => assign(element, 'hero'));
  document.querySelectorAll('.booking-pet:not(.solid)').forEach(element => assign(element, 'booking'));
})();
