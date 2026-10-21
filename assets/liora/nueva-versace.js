// Behaviour for the versace layout of the signature template: sections come in, the
// hero settles, the chapter bar marks where you are, the catalogue of Versace touches
// turns, and the walk through the rooms pages one view at a time. Nothing here is
// needed to read the page: every rule that hides content is scoped to .vs-js, which
// this file adds, and reduced motion gets the final state at once.
(() => {
  const root = document.documentElement;
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const items = document.querySelectorAll('[data-vs-in]');

  // ---- Reveal on scroll -------------------------------------------------------
  // Decided from the layout box on each paint: a framed item starts clipped, and an
  // IntersectionObserver would not see a clipped target.
  let pending = [...items];
  const reveal = () => {
    if (!pending.length) return;
    const line = window.innerHeight * 0.92;
    pending = pending.filter((item) => {
      const box = item.getBoundingClientRect();
      if (box.bottom < 0 || box.top > line) return true;
      item.classList.add('is-in');
      return false;
    });
  };
  if (reduced) {
    items.forEach((item) => item.classList.add('is-in'));
    pending = [];
  } else {
    root.classList.add('vs-js');
    const hero = document.querySelector('.vs-hero');
    if (hero) requestAnimationFrame(() => requestAnimationFrame(() => hero.classList.add('is-ready')));
  }
  // The viewer and the catalogue need their hiding rules even when motion is reduced.
  root.classList.add('vs-js');

  // ---- Chapter bar ----------------------------------------------------------------
  const links = [...document.querySelectorAll('[data-chapter]')];
  const targets = links.map((link) => document.getElementById(link.dataset.chapter)).filter(Boolean);
  if (links.length && 'IntersectionObserver' in window) {
    const active = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        links.forEach((link) => link.classList.toggle('is-active', link.dataset.chapter === entry.target.id));
        // Centre the active link inside the bar itself; scrollIntoView would move the page too.
        const link = links.find((item) => item.dataset.chapter === entry.target.id);
        const strip = link?.parentElement;
        if (strip && strip.scrollWidth > strip.clientWidth) {
          strip.scrollTo({ left: link.offsetLeft - (strip.clientWidth - link.offsetWidth) / 2, behavior: reduced ? 'auto' : 'smooth' });
        }
      });
    }, { rootMargin: '-30% 0px -60% 0px' });
    targets.forEach((target) => active.observe(target));
  }

  const progress = document.querySelector('[data-vs-progress]');
  const layers = [...document.querySelectorAll('[data-vs-parallax]')];
  let waiting = false;
  const paint = () => {
    waiting = false;
    reveal();
    const height = window.innerHeight;
    if (progress) {
      const room = document.documentElement.scrollHeight - height;
      progress.style.transform = `scaleX(${room > 0 ? Math.min(1, window.scrollY / room).toFixed(4) : 0})`;
    }
    if (reduced) return;
    layers.forEach((layer) => {
      const box = layer.parentElement.getBoundingClientRect();
      if (box.bottom < 0 || box.top > height) return;
      layer.style.transform = `translate3d(0, ${(window.scrollY * 0.12).toFixed(1)}px, 0)`;
    });
  };
  window.addEventListener('scroll', () => {
    if (waiting) return;
    waiting = true;
    requestAnimationFrame(paint);
  }, { passive: true });
  window.addEventListener('resize', reveal);
  paint();

  // ---- The house's hand: a catalogue ------------------------------------------------
  const touches = [...document.querySelectorAll('[data-vs-touch]')];
  const touchImages = [...document.querySelectorAll('[data-vs-touch-img]')];
  const showTouch = (index) => {
    touches.forEach((button) => {
      const on = button.dataset.vsTouch === String(index);
      button.classList.toggle('is-active', on);
      button.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
    touchImages.forEach((image) => image.classList.toggle('is-active', image.dataset.vsTouchImg === String(index)));
  };
  touches.forEach((button) => {
    button.addEventListener('click', () => showTouch(button.dataset.vsTouch));
    button.addEventListener('mouseenter', () => { if (window.matchMedia('(hover: hover)').matches) showTouch(button.dataset.vsTouch); });
  });

  // ---- The rooms: one view at a time -------------------------------------------------
  const viewer = document.querySelector('[data-vs-viewer]');
  if (viewer) {
    const slides = [...viewer.querySelectorAll('[data-vs-slide]')];
    const thumbs = [...viewer.querySelectorAll('[data-vs-thumb]')];
    let current = 0;
    const show = (index, fromThumb) => {
      current = (index + slides.length) % slides.length;
      slides.forEach((slide, position) => {
        const on = position === current;
        slide.classList.toggle('is-active', on);
        slide.setAttribute('aria-hidden', on ? 'false' : 'true');
      });
      thumbs.forEach((thumb, position) => {
        const on = position === current;
        thumb.classList.toggle('is-active', on);
        thumb.setAttribute('aria-pressed', on ? 'true' : 'false');
      });
      const strip = viewer.querySelector('[data-vs-thumbs]');
      const thumb = thumbs[current];
      if (strip && thumb && !fromThumb) {
        strip.scrollTo({ left: thumb.offsetLeft - (strip.clientWidth - thumb.offsetWidth) / 2, behavior: reduced ? 'auto' : 'smooth' });
      }
    };
    const rtl = (root.getAttribute('dir') || '').toLowerCase() === 'rtl';
    viewer.querySelector('[data-vs-prev]')?.addEventListener('click', () => show(current - 1));
    viewer.querySelector('[data-vs-next]')?.addEventListener('click', () => show(current + 1));
    thumbs.forEach((thumb, position) => thumb.addEventListener('click', () => show(position, true)));
    viewer.setAttribute('tabindex', '0');
    viewer.addEventListener('keydown', (event) => {
      if (event.key === 'ArrowRight') { event.preventDefault(); show(current + (rtl ? -1 : 1)); }
      if (event.key === 'ArrowLeft') { event.preventDefault(); show(current + (rtl ? 1 : -1)); }
    });
  }
})();
