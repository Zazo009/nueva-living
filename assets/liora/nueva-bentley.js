// Behaviour for the bentley layout of the signature template: things come in as they are scrolled to,
// the chapter bar marks where you are, the switch between the two residences, and the theatre where the
// picture stays and the words go past it. Nothing here is needed to read the page: every rule that hides
// content is scoped to .bn-js, which this file adds, and reduced motion gets the final state at once.
(() => {
  const root = document.documentElement;
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const items = document.querySelectorAll('[data-bn-in]');
  const rtl = (root.getAttribute('dir') || '').toLowerCase() === 'rtl';

  // ---- Reveal on scroll (from the layout box, which clip-path leaves alone) ---------
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
  // The viewer and the theatre need their hiding rules even when motion is reduced.
  root.classList.add('bn-js');
  if (reduced) {
    items.forEach((item) => item.classList.add('is-in'));
    pending = [];
  } else {
    const hero = document.querySelector('.bn-hero');
    if (hero) requestAnimationFrame(() => requestAnimationFrame(() => hero.classList.add('is-ready')));
  }

  // ---- Chapter bar ------------------------------------------------------------------
  const links = [...document.querySelectorAll('[data-chapter]')];
  const targets = links.map((link) => document.getElementById(link.dataset.chapter)).filter(Boolean);
  if (links.length && 'IntersectionObserver' in window) {
    const active = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        links.forEach((link) => link.classList.toggle('is-active', link.dataset.chapter === entry.target.id));
        const link = links.find((item) => item.dataset.chapter === entry.target.id);
        const strip = link?.parentElement;
        if (strip && strip.scrollWidth > strip.clientWidth) {
          strip.scrollTo({ left: link.offsetLeft - (strip.clientWidth - link.offsetWidth) / 2, behavior: reduced ? 'auto' : 'smooth' });
        }
      });
    }, { rootMargin: '-30% 0px -60% 0px' });
    targets.forEach((target) => active.observe(target));
  }

  const progress = document.querySelector('[data-bn-progress]');
  let waiting = false;
  const paint = () => {
    waiting = false;
    reveal();
    if (progress) {
      const room = document.documentElement.scrollHeight - window.innerHeight;
      progress.style.transform = `scaleX(${room > 0 ? Math.min(1, window.scrollY / room).toFixed(4) : 0})`;
    }
  };
  window.addEventListener('scroll', () => {
    if (waiting) return;
    waiting = true;
    requestAnimationFrame(paint);
  }, { passive: true });
  window.addEventListener('resize', reveal);
  paint();

  // ---- The two residences, one switch ---------------------------------------------------
  const tabs = [...document.querySelectorAll('[data-bn-type]')];
  const panels = [...document.querySelectorAll('[data-bn-type-panel]')];
  const choose = (index) => {
    tabs.forEach((tab) => {
      const on = tab.dataset.bnType === String(index);
      tab.classList.toggle('is-active', on);
      tab.setAttribute('aria-selected', on ? 'true' : 'false');
    });
    panels.forEach((panel) => {
      const on = panel.dataset.bnTypePanel === String(index);
      panel.hidden = !on;
      panel.classList.toggle('is-active', on);
    });
  };
  tabs.forEach((tab) => {
    tab.addEventListener('click', () => choose(tab.dataset.bnType));
    tab.addEventListener('keydown', (event) => {
      if (event.key !== 'ArrowRight' && event.key !== 'ArrowLeft') return;
      event.preventDefault();
      const step = (event.key === 'ArrowRight' ? 1 : -1) * (rtl ? -1 : 1);
      const next = tabs[(tabs.indexOf(tab) + step + tabs.length) % tabs.length];
      next.focus();
      choose(next.dataset.bnType);
    });
  });

  // ---- The theatre: the picture follows whichever room is in the middle of the screen ------
  const theatre = document.querySelector('[data-bn-theatre]');
  if (theatre && 'IntersectionObserver' in window) {
    const stages = [...theatre.querySelectorAll('[data-bn-stage]')];
    const steps = [...theatre.querySelectorAll('[data-bn-step]')];
    const show = (index) => {
      stages.forEach((stage) => stage.classList.toggle('is-active', stage.dataset.bnStage === String(index)));
      steps.forEach((step) => step.classList.toggle('is-active', step.dataset.bnStep === String(index)));
    };
    const watch = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) show(entry.target.dataset.bnStep);
      });
    }, { rootMargin: '-45% 0px -45% 0px' });
    steps.forEach((step) => watch.observe(step));
  }
})();
