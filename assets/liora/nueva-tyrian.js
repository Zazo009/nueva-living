// Behaviour for the tyrian layout of the signature template: things come in as
// slabs, the hero settles, the terrace curves drift against the scroll, the chapter
// bar marks where you are, the residences rail pages sideways, and the price list
// drawn as a building answers to a tap. Nothing here is needed to read the page:
// every rule that hides content is scoped to .ty-js, which this file adds, and
// reduced motion gets the final state at once.
(() => {
  const root = document.documentElement;
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const rtl = (root.getAttribute('dir') || '').toLowerCase() === 'rtl';
  const items = document.querySelectorAll('[data-ty-in]');

  // ---- Slabs and rises on scroll -------------------------------------------
  // A slab starts clipped to nothing, and an IntersectionObserver treats a fully
  // clipped target as never visible, so the reveal is decided from the layout box
  // (which clip-path leaves alone) each time the page paints.
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
    root.classList.add('ty-js');
    const hero = document.querySelector('.ty-hero');
    if (hero) requestAnimationFrame(() => requestAnimationFrame(() => hero.classList.add('is-ready')));
  }

  // ---- Chapter bar ----------------------------------------------------------
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

  const progress = document.querySelector('[data-ty-progress]');
  const drifting = [...document.querySelectorAll('[data-ty-drift]')];
  const layers = [...document.querySelectorAll('[data-ty-parallax]')];
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
    // The curves slide a little with the scroll, the nearer one more than the far one.
    drifting.forEach((path) => {
      const rate = Number(path.dataset.tyDrift) || 0;
      path.style.transform = `translate3d(${((rtl ? 1 : -1) * window.scrollY * rate * 0.06).toFixed(1)}px, 0, 0)`;
    });
    layers.forEach((layer) => {
      const box = layer.parentElement.getBoundingClientRect();
      if (box.bottom < 0 || box.top > height) return;
      const offset = (box.top + box.height / 2 - height / 2) / height;
      layer.style.transform = `translate3d(0, ${(-offset * 44).toFixed(1)}px, 0)`;
    });
  };
  window.addEventListener('scroll', () => {
    if (waiting) return;
    waiting = true;
    requestAnimationFrame(paint);
  }, { passive: true });
  paint();
  window.addEventListener('resize', reveal);

  // ---- The building ---------------------------------------------------------
  const elevation = document.querySelector('[data-ty-elevation]');
  const detail = document.querySelector('[data-ty-detail]');
  if (elevation && detail) {
    const cells = [...elevation.querySelectorAll('[data-ty-home]')];
    const tabs = [...elevation.querySelectorAll('[data-ty-floor]')];
    const field = (name) => detail.querySelector(`[data-ty-d-${name}]`);
    const statusWords = {};
    // The words for the three statuses sit in the legend, in the page's own language.
    document.querySelectorAll('.ty-legend i[data-status]').forEach((mark) => {
      statusWords[mark.dataset.status] = mark.parentElement.textContent.split('·')[0].trim();
    });
    const show = (cell) => {
      cells.forEach((other) => other.setAttribute('aria-pressed', other === cell ? 'true' : 'false'));
      field('number').textContent = cell.dataset.number;
      const status = field('status');
      status.dataset.status = cell.dataset.status;
      status.textContent = statusWords[cell.dataset.status] || cell.dataset.status;
      field('type').textContent = cell.dataset.type || '';
      field('price').textContent = cell.dataset.price || '';
      const link = field('link');
      if (link) {
        if (cell.dataset.unit) {
          link.hidden = false;
          link.setAttribute('href', `#unit-${cell.dataset.unit}`);
        } else {
          link.hidden = true;
        }
      }
    };
    cells.forEach((cell) => cell.addEventListener('click', () => show(cell)));
    tabs.forEach((tab) => tab.addEventListener('click', () => {
      const index = tab.dataset.tyFloor;
      const already = elevation.dataset.focus === index;
      if (already) {
        delete elevation.dataset.focus;
        tabs.forEach((other) => other.setAttribute('aria-pressed', 'false'));
        return;
      }
      elevation.dataset.focus = index;
      tabs.forEach((other) => other.setAttribute('aria-pressed', other === tab ? 'true' : 'false'));
      // On a floor, the first priced residence is the one worth looking at.
      const onFloor = cells.filter((cell) => cell.dataset.floor === index);
      const first = onFloor.find((cell) => cell.dataset.status === 'available') || onFloor[0];
      if (first) show(first);
    }));
  }

  // ---- Residences rail: page sideways ---------------------------------------
  const rail = document.querySelector('[data-ty-rail]');
  if (rail) {
    const step = (direction) => {
      const cards = rail.querySelectorAll('.ty-unit');
      const width = cards.length > 1 ? Math.abs(cards[1].offsetLeft - cards[0].offsetLeft) : rail.clientWidth * 0.8;
      rail.scrollBy({ left: direction * (rtl ? -1 : 1) * width, behavior: reduced ? 'auto' : 'smooth' });
    };
    document.querySelector('[data-ty-prev]')?.addEventListener('click', () => step(-1));
    document.querySelector('[data-ty-next]')?.addEventListener('click', () => step(1));
    rail.addEventListener('keydown', (event) => {
      if (event.key === 'ArrowRight') { event.preventDefault(); step(1); }
      if (event.key === 'ArrowLeft') { event.preventDefault(); step(-1); }
    });
    // A link from the building to a residence: bring the card into the rail.
    document.querySelectorAll('[data-ty-d-link]').forEach((link) => {
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
})();
