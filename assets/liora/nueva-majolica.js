// Behaviour for the majolica layout of the signature template: things slide in
// from a side as they reach the viewport, the hero settles, the block tabs swap
// their panel with a slide, the residences rail pages sideways, and the chapter
// bar marks where you are. Nothing here is needed to read the page: every rule
// that hides content is scoped to .mj-js, which this file adds last, and
// reduced motion gets the final state at once.
(() => {
  const root = document.documentElement;
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const rtl = (root.getAttribute('dir') || '').toLowerCase() === 'rtl';
  const items = document.querySelectorAll('[data-mj-in]');

  // ---- Slide-in on scroll --------------------------------------------------
  if (!('IntersectionObserver' in window) || reduced) {
    items.forEach((item) => item.classList.add('is-in'));
  } else {
    root.classList.add('mj-js');
    const reveal = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-in');
        reveal.unobserve(entry.target);
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
    items.forEach((item) => reveal.observe(item));
    // The hero has no scroll to wait for: let the first frame paint, then slide.
    const hero = document.querySelector('.mj-hero');
    if (hero) requestAnimationFrame(() => requestAnimationFrame(() => hero.classList.add('is-ready')));
  }

  // ---- Chapter bar: mark the chapter crossing the upper third --------------
  const links = [...document.querySelectorAll('[data-chapter]')];
  const targets = links.map((link) => document.getElementById(link.dataset.chapter)).filter(Boolean);
  if (links.length && 'IntersectionObserver' in window) {
    const active = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        links.forEach((link) => link.classList.toggle('is-active', link.dataset.chapter === entry.target.id));
        links.find((link) => link.dataset.chapter === entry.target.id)?.scrollIntoView({ block: 'nearest', inline: 'center' });
      });
    }, { rootMargin: '-30% 0px -60% 0px' });
    targets.forEach((target) => active.observe(target));
  }

  // ---- Block tabs: one panel at a time, sliding in ------------------------
  const tabs = [...document.querySelectorAll('[data-mj-tab]')];
  const panels = [...document.querySelectorAll('[data-mj-panel]')];
  if (tabs.length && panels.length) {
    const show = (number, focus) => {
      tabs.forEach((tab) => {
        const on = tab.dataset.mjTab === String(number);
        tab.setAttribute('aria-selected', on ? 'true' : 'false');
        tab.tabIndex = on ? 0 : -1;
        if (on && focus) tab.focus();
      });
      panels.forEach((panel) => {
        const on = panel.dataset.mjPanel === String(number);
        panel.hidden = !on;
        panel.classList.toggle('is-entering', on && !reduced);
      });
    };
    tabs.forEach((tab) => {
      tab.addEventListener('click', () => show(tab.dataset.mjTab, false));
      tab.addEventListener('keydown', (event) => {
        const index = tabs.indexOf(tab);
        const step = { ArrowRight: rtl ? -1 : 1, ArrowLeft: rtl ? 1 : -1 }[event.key];
        if (!step) return;
        event.preventDefault();
        const next = tabs[(index + step + tabs.length) % tabs.length];
        show(next.dataset.mjTab, true);
      });
    });
    // Without script every panel stays visible, one under the other.
    show(1, false);
  }

  // ---- Residences rail: page sideways --------------------------------------
  const rail = document.querySelector('[data-mj-rail]');
  if (rail) {
    const step = (direction) => {
      const card = rail.querySelector('.mj-unit');
      const width = card ? card.getBoundingClientRect().width + 20 : rail.clientWidth * 0.8;
      rail.scrollBy({ left: direction * (rtl ? -1 : 1) * width, behavior: reduced ? 'auto' : 'smooth' });
    };
    document.querySelector('[data-mj-prev]')?.addEventListener('click', () => step(-1));
    document.querySelector('[data-mj-next]')?.addEventListener('click', () => step(1));
    rail.addEventListener('keydown', (event) => {
      if (event.key === 'ArrowRight') { event.preventDefault(); step(1); }
      if (event.key === 'ArrowLeft') { event.preventDefault(); step(-1); }
    });
    // A link from a block panel to a residence: bring the card into the rail.
    document.querySelectorAll('.mj-block-units a[href^="#unit-"]').forEach((link) => {
      link.addEventListener('click', (event) => {
        const card = document.querySelector(link.getAttribute('href'));
        if (!card) return;
        event.preventDefault();
        document.getElementById('residences')?.scrollIntoView({ behavior: reduced ? 'auto' : 'smooth', block: 'start' });
        const offset = rtl ? card.offsetLeft - rail.clientWidth + card.offsetWidth : card.offsetLeft;
        rail.scrollTo({ left: offset - 24, behavior: reduced ? 'auto' : 'smooth' });
      });
    });
  }

  // ---- Reading progress, along the foot of the chapter bar -----------------
  const progress = document.querySelector('[data-mj-progress]');
  if (progress) {
    let waiting = false;
    const paint = () => {
      waiting = false;
      const room = document.documentElement.scrollHeight - window.innerHeight;
      progress.style.transform = `scaleX(${room > 0 ? Math.min(1, window.scrollY / room).toFixed(4) : 0})`;
    };
    window.addEventListener('scroll', () => {
      if (waiting) return;
      waiting = true;
      requestAnimationFrame(paint);
    }, { passive: true });
  }

  // ---- Parallax: a few pixels against the scroll ---------------------------
  const layers = [...document.querySelectorAll('[data-mj-parallax]')];
  if (layers.length && !reduced) {
    let queued = false;
    const update = () => {
      queued = false;
      const height = window.innerHeight;
      layers.forEach((layer) => {
        const box = layer.parentElement.getBoundingClientRect();
        if (box.bottom < 0 || box.top > height) return;
        const progress = (box.top + box.height / 2 - height / 2) / height;
        layer.style.transform = `translate3d(0, ${(-progress * 40).toFixed(1)}px, 0)`;
      });
    };
    window.addEventListener('scroll', () => {
      if (queued) return;
      queued = true;
      requestAnimationFrame(update);
    }, { passive: true });
  }
})();
