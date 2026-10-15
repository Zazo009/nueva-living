// Behaviour for the signature project template: reveal on scroll, the chapter
// bar's active state, a slow parallax on the two full-bleed images, and the
// count-up on the masterplan figures. Nothing here is needed to read the page:
// every rule that hides content is scoped to .js-sig, which this file adds
// last, and reduced motion gets the final state at once.
(() => {
  const root = document.documentElement;
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const items = document.querySelectorAll('[data-sig-appear]');

  if (!('IntersectionObserver' in window) || reduced) {
    items.forEach((item) => item.classList.add('is-in'));
  } else {
    root.classList.add('js-sig');
    const reveal = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-in');
        reveal.unobserve(entry.target);
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
    items.forEach((item) => reveal.observe(item));
  }

  // Chapter bar: mark the chapter whose section is crossing the upper third.
  const links = [...document.querySelectorAll('[data-chapter]')];
  const targets = links.map((link) => document.getElementById(link.dataset.chapter)).filter(Boolean);
  if (links.length && 'IntersectionObserver' in window) {
    const active = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        links.forEach((link) => link.classList.toggle('is-active', link.dataset.chapter === entry.target.id));
        const current = links.find((link) => link.dataset.chapter === entry.target.id);
        current?.scrollIntoView({ block: 'nearest', inline: 'center' });
      });
    }, { rootMargin: '-30% 0px -60% 0px' });
    targets.forEach((target) => active.observe(target));
  }

  // Parallax: translate the image a few percent against the scroll.
  const layers = [...document.querySelectorAll('[data-sig-parallax]')];
  if (layers.length && !reduced) {
    let queued = false;
    const update = () => {
      queued = false;
      const height = window.innerHeight;
      layers.forEach((layer) => {
        const box = layer.parentElement.getBoundingClientRect();
        if (box.bottom < 0 || box.top > height) return;
        const progress = (box.top + box.height / 2 - height / 2) / height;
        layer.style.transform = `translate3d(0, ${(-progress * 36).toFixed(1)}px, 0)`;
      });
    };
    window.addEventListener('scroll', () => {
      if (queued) return;
      queued = true;
      requestAnimationFrame(update);
    }, { passive: true });
    update();
  }

  // Count-up: only for a figure made of digits and separators, so "50,000"
  // counts and anything with letters in it is left exactly as written.
  const counters = [...document.querySelectorAll('[data-sig-count]')];
  if (counters.length && 'IntersectionObserver' in window && !reduced) {
    const count = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        count.unobserve(entry.target);
        const node = entry.target;
        const text = node.textContent.trim();
        if (!/^[\d.,  \s]+$/.test(text)) return;
        const digits = Number(text.replace(/\D/g, ''));
        if (!digits) return;
        const start = performance.now();
        const run = (now) => {
          const t = Math.min(1, (now - start) / 1400);
          const value = Math.round(digits * (1 - Math.pow(1 - t, 3)));
          node.textContent = text.replace(/\d[\d.,  \s]*/, () => {
            const raw = String(value);
            const separator = text.match(/[.,  ]/)?.[0];
            return separator && digits >= 1000 ? raw.replace(/\B(?=(\d{3})+(?!\d))/g, separator) : raw;
          });
          if (t < 1) requestAnimationFrame(run);
          else node.textContent = text;
        };
        requestAnimationFrame(run);
      });
    }, { threshold: 0.6 });
    counters.forEach((node) => count.observe(node));
  }
})();
