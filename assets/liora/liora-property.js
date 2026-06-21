(() => {
  const page = document.body;
  const projectContext = {
    name: page.dataset.projectName || '',
    materialMessage: page.dataset.projectMessage || '',
    sentMessage: page.dataset.projectSentMessage || 'Thank you. Your request has been noted for private follow-up.'
  };

  const burger = document.querySelector('.nav-burger');
  const menu = document.getElementById('mobileMenu');

  function closeMobileMenu() {
    if (!burger || !menu) return;
    menu.classList.remove('open');
    burger.setAttribute('aria-expanded', 'false');
    document.body.classList.remove('menu-open');
  }

  if (burger && menu) {
    burger.addEventListener('pointerdown', (event) => event.stopPropagation());
    burger.addEventListener('click', (event) => {
      event.preventDefault();
      event.stopPropagation();
      const open = menu.classList.toggle('open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      document.body.classList.toggle('menu-open', open);
    });

    menu.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', closeMobileMenu);
    });
  }

  function prefillProjectForm() {
    const msg = document.getElementById('f-msg');
    const project = document.getElementById('f-project');
    if (project && projectContext.name) project.value = projectContext.name;
    if (msg && projectContext.materialMessage) msg.value = projectContext.materialMessage;
  }

  document.querySelectorAll('[data-prefill]').forEach((cta) => {
    cta.addEventListener('click', () => prefillProjectForm());
  });

  const projectNav = document.querySelector('.project-nav');
  const projectNavInner = document.querySelector('.project-nav-inner');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function updateProjectNavOverflow() {
    if (!projectNav || !projectNavInner) return;
    const maxScroll = projectNavInner.scrollWidth - projectNavInner.clientWidth;
    const hasRight = maxScroll > 4 && projectNavInner.scrollLeft < maxScroll - 4;
    projectNav.classList.toggle('has-scroll-right', hasRight);
  }

  if (projectNav && projectNavInner) {
    projectNavInner.addEventListener('scroll', updateProjectNavOverflow, { passive: true });
    window.addEventListener('resize', updateProjectNavOverflow, { passive: true });
    window.addEventListener('load', updateProjectNavOverflow, { once: true });
    requestAnimationFrame(updateProjectNavOverflow);
  }

  function stickyOffset() {
    const siteNav = document.querySelector('.site-nav');
    const siteHeight = siteNav?.getBoundingClientRect().height || 0;
    const projectHeight = projectNav?.getBoundingClientRect().height || 0;
    return Math.round(siteHeight + projectHeight + 16);
  }

  if (projectNav && projectNavInner) {
    const navLinks = [...projectNavInner.querySelectorAll('a[href^="#"]')];
    const navEntries = navLinks
      .map((link) => {
        const id = decodeURIComponent(link.getAttribute('href').slice(1));
        const section = document.getElementById(id);
        return section ? { id, link, section } : null;
      })
      .filter(Boolean);

    function keepActiveLinkInView(link) {
      const left = link.offsetLeft - ((projectNavInner.clientWidth - link.offsetWidth) / 2);
      projectNavInner.scrollTo({
        left: Math.max(0, left),
        behavior: reducedMotion ? 'auto' : 'smooth'
      });
    }

    function setActiveSection(id, shouldReveal = true) {
      navEntries.forEach(({ id: entryId, link }) => {
        const active = entryId === id;
        link.classList.toggle('is-active', active);
        if (active) link.setAttribute('aria-current', 'true');
        else link.removeAttribute('aria-current');
      });

      const activeEntry = navEntries.find((entry) => entry.id === id);
      if (activeEntry && shouldReveal) keepActiveLinkInView(activeEntry.link);
    }

    function sectionFromScrollPosition() {
      const marker = window.scrollY + stickyOffset() + 24;
      let current = navEntries[0];
      for (const entry of navEntries) {
        if (entry.section.offsetTop <= marker) current = entry;
        else break;
      }
      return current;
    }

    function scrollToSection(id, shouldWriteHash = false) {
      const entry = navEntries.find((item) => item.id === id);
      if (!entry) return;

      setActiveSection(id);
      window.scrollTo({
        top: Math.max(0, entry.section.getBoundingClientRect().top + window.scrollY - stickyOffset()),
        behavior: reducedMotion ? 'auto' : 'smooth'
      });

      if (shouldWriteHash) window.history.replaceState(null, '', `#${id}`);
    }

    let scrollTicking = false;
    function updateActiveFromScroll() {
      scrollTicking = false;
      const current = sectionFromScrollPosition();
      if (current) setActiveSection(current.id);
    }

    function requestActiveUpdate() {
      if (scrollTicking) return;
      scrollTicking = true;
      requestAnimationFrame(updateActiveFromScroll);
    }

    navLinks.forEach((link) => {
      link.addEventListener('click', (event) => {
        const id = decodeURIComponent(link.getAttribute('href').slice(1));
        if (!navEntries.some((entry) => entry.id === id)) return;

        event.preventDefault();
        scrollToSection(id, true);
      });
    });

    if ('IntersectionObserver' in window) {
      const observerRoot = () => `-${stickyOffset() + 8}px 0px -62% 0px`;
      let sectionObserver = new IntersectionObserver((entries) => {
        const visible = entries
          .filter((entry) => entry.isIntersecting)
          .sort((a, b) => Math.abs(a.boundingClientRect.top) - Math.abs(b.boundingClientRect.top));
        if (visible[0]) setActiveSection(visible[0].target.id);
      }, { rootMargin: observerRoot(), threshold: [0, 0.12, 0.24] });

      navEntries.forEach(({ section }) => sectionObserver.observe(section));

      window.addEventListener('resize', () => {
        sectionObserver.disconnect();
        sectionObserver = new IntersectionObserver((entries) => {
          const visible = entries
            .filter((entry) => entry.isIntersecting)
            .sort((a, b) => Math.abs(a.boundingClientRect.top) - Math.abs(b.boundingClientRect.top));
          if (visible[0]) setActiveSection(visible[0].target.id);
        }, { rootMargin: observerRoot(), threshold: [0, 0.12, 0.24] });
        navEntries.forEach(({ section }) => sectionObserver.observe(section));
        requestActiveUpdate();
      }, { passive: true });
    } else {
      window.addEventListener('scroll', requestActiveUpdate, { passive: true });
      window.addEventListener('resize', requestActiveUpdate, { passive: true });
    }

    window.addEventListener('load', () => {
      const hashId = decodeURIComponent(window.location.hash.replace(/^#/, ''));
      if (hashId && navEntries.some((entry) => entry.id === hashId)) {
        requestAnimationFrame(() => requestAnimationFrame(() => scrollToSection(hashId)));
      } else {
        requestActiveUpdate();
      }
    }, { once: true });
    requestActiveUpdate();
  }

  const form = document.getElementById('projectForm');
  function isLocalFormPreview() {
    return window.location.protocol === 'file:' || ['127.0.0.1', 'localhost'].includes(window.location.hostname);
  }

  if (form) {
    form.addEventListener('submit', (event) => {
      prefillProjectForm();
      if (!isLocalFormPreview()) return;

      event.preventDefault();
      const note = form.querySelector('.form-note');
      const submit = form.querySelector('button[type="submit"]');
      if (note) {
        note.textContent = projectContext.sentMessage;
        note.classList.add('is-sent');
      }
      if (submit) submit.textContent = 'Request Noted';
    });
  }

  const revealItems = document.querySelectorAll('.reveal-soft');

  if ('IntersectionObserver' in window && !reducedMotion) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('in');
        observer.unobserve(entry.target);
      });
    }, { threshold: 0.14 });

    revealItems.forEach((item) => observer.observe(item));
  } else {
    revealItems.forEach((item) => item.classList.add('in'));
  }
})();
