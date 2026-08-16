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

  const projectVideo = document.querySelector('[data-project-video]');
  const projectVideoShell = document.querySelector('[data-project-video-shell]');
  const projectVideoPlay = document.querySelector('[data-project-video-play]');

  if (projectVideo && projectVideoShell && projectVideoPlay) {
    const mobileVideo = window.matchMedia('(max-width: 640px) and (orientation: portrait)');
    const selectedVideoSource = () => (
      mobileVideo.matches
        ? projectVideo.dataset.videoMobile
        : projectVideo.dataset.videoDesktop
    );

    const selectedPoster = () => (
      mobileVideo.matches
        ? projectVideo.dataset.posterMobile
        : projectVideo.dataset.posterDesktop
    );

    const updatePoster = () => {
      if (projectVideo.currentSrc || projectVideo.src) return;
      projectVideo.poster = selectedPoster() || '';
    };

    const playProjectVideo = async () => {
      // Keep the sizeable film entirely out of the request chain until the visitor chooses to play it.
      if (!projectVideo.src) {
        projectVideo.src = selectedVideoSource() || '';
        projectVideo.load();
      }

      projectVideo.controls = true;
      projectVideoShell.classList.add('is-loading');
      try {
        await projectVideo.play();
      } catch (error) {
        projectVideoShell.classList.remove('is-loading');
        projectVideoShell.classList.add('has-video-error');
        console.warn('The project film could not be started.', error);
      }
    };

    projectVideoPlay.addEventListener('click', playProjectVideo);
    projectVideo.addEventListener('playing', () => {
      projectVideoShell.classList.remove('is-loading', 'has-video-error');
      projectVideoShell.classList.add('is-playing');
    });
    projectVideo.addEventListener('error', () => {
      projectVideoShell.classList.remove('is-loading');
      projectVideoShell.classList.add('has-video-error');
    });
    mobileVideo.addEventListener?.('change', updatePoster);
    updatePoster();
  }

  const mediaDialog = document.getElementById('projectMediaDialog');
  const mediaGrid = document.querySelector('[data-media-grid]');

  if (mediaDialog && mediaGrid) {
    const mediaCards = [...mediaGrid.querySelectorAll('[data-media-category]')];
    const showAllButton = document.querySelector('[data-media-show-all]');
    const dialogShell = mediaDialog.querySelector('[data-media-dialog-shell]');
    const dialogImage = mediaDialog.querySelector('[data-media-dialog-image]');
    const dialogCaption = mediaDialog.querySelector('[data-media-dialog-caption]');
    const dialogCount = mediaDialog.querySelector('[data-media-dialog-count]');
    const dialogStack = mediaDialog.querySelector('[data-media-dialog-stack]');
    const dialogStackCount = mediaDialog.querySelector('[data-media-dialog-stack-count]');
    const mediaData = document.getElementById('projectMediaData');
    let mediaItems = [];
    let activeMediaItems = [];
    let activeMediaIndex = 0;
    let swipeStartX = 0;
    let stackObserver = null;

    try {
      mediaItems = JSON.parse(mediaData?.textContent || '[]');
    } catch (error) {
      console.warn('Project media data could not be read.', error);
    }

    const stackQuery = window.matchMedia ? window.matchMedia('(max-width: 640px)') : null;
    const useStack = () => Boolean(stackQuery?.matches);

    function showMediaAt(index) {
      if (!activeMediaItems.length || !dialogImage) return;
      activeMediaIndex = (index + activeMediaItems.length) % activeMediaItems.length;
      const item = activeMediaItems[activeMediaIndex];
      dialogImage.src = item.webp || item.src;
      if (item.webp) dialogImage.addEventListener('error', () => { dialogImage.src = item.src; }, { once: true });
      dialogImage.alt = item.alt || '';
      dialogImage.width = Number(item.width) || 1600;
      dialogImage.height = Number(item.height) || 900;
      if (dialogCaption) dialogCaption.textContent = item.caption || '';
      if (dialogCount) dialogCount.textContent = `${String(activeMediaIndex + 1).padStart(2, '0')} / ${String(activeMediaItems.length).padStart(2, '0')}`;
    }

    function updateStackCount(index) {
      if (!dialogStackCount) return;
      dialogStackCount.textContent = `${String(index + 1).padStart(2, '0')} / ${String(activeMediaItems.length).padStart(2, '0')}`;
    }

    function buildStack() {
      if (!dialogStack) return;
      stackObserver?.disconnect();
      dialogStack.querySelectorAll('.media-dialog-stack-item').forEach((el) => el.remove());

      activeMediaItems.forEach((item, index) => {
        const figure = document.createElement('figure');
        figure.className = 'media-dialog-stack-item';
        figure.dataset.stackIndex = String(index);

        const img = document.createElement('img');
        img.src = item.webp || item.src;
        if (item.webp) img.addEventListener('error', () => { img.src = item.src; }, { once: true });
        img.alt = item.alt || '';
        img.width = Number(item.width) || 1600;
        img.height = Number(item.height) || 900;
        img.loading = 'lazy';
        img.decoding = 'async';
        figure.appendChild(img);

        if (item.caption) {
          const caption = document.createElement('figcaption');
          caption.textContent = item.caption;
          figure.appendChild(caption);
        }

        dialogStack.appendChild(figure);
      });

      updateStackCount(0);

      if ('IntersectionObserver' in window) {
        stackObserver = new IntersectionObserver((entries) => {
          const visible = entries.filter((entry) => entry.isIntersecting);
          if (!visible.length) return;
          visible.sort((a, b) => b.intersectionRatio - a.intersectionRatio);
          const index = Number(visible[0].target.dataset.stackIndex || 0);
          activeMediaIndex = index;
          updateStackCount(index);
        }, { root: dialogStack, threshold: [0.5, 0.75] });

        dialogStack.querySelectorAll('.media-dialog-stack-item').forEach((el) => stackObserver.observe(el));
      }
    }

    function openMedia(category = 'All') {
      activeMediaItems = category === 'All'
        ? mediaItems
        : mediaItems.filter((item) => item.category === category);
      if (!activeMediaItems.length) return;

      if (useStack()) {
        dialogShell?.classList.add('is-stack-mode');
        if (dialogStack) dialogStack.hidden = false;
        dialogStack.scrollTop = 0;
        buildStack();
      } else {
        dialogShell?.classList.remove('is-stack-mode');
        if (dialogStack) dialogStack.hidden = true;
        showMediaAt(0);
      }

      if (typeof mediaDialog.showModal === 'function') mediaDialog.showModal();
      else mediaDialog.setAttribute('open', '');
      document.body.classList.add('media-dialog-open');
    }

    function closeMedia() {
      if (typeof mediaDialog.close === 'function') mediaDialog.close();
      else mediaDialog.removeAttribute('open');
      document.body.classList.remove('media-dialog-open');
      stackObserver?.disconnect();
    }

    mediaCards.forEach((card) => {
      card.addEventListener('click', () => openMedia(card.dataset.mediaCategory || 'All'));
    });

    showAllButton?.addEventListener('click', () => openMedia('All'));

    mediaDialog.querySelector('[data-media-close]')?.addEventListener('click', closeMedia);
    mediaDialog.querySelector('[data-media-prev]')?.addEventListener('click', () => showMediaAt(activeMediaIndex - 1));
    mediaDialog.querySelector('[data-media-next]')?.addEventListener('click', () => showMediaAt(activeMediaIndex + 1));
    mediaDialog.addEventListener('cancel', (event) => {
      event.preventDefault();
      closeMedia();
    });
    mediaDialog.addEventListener('click', (event) => {
      if (event.target === mediaDialog) closeMedia();
    });
    mediaDialog.addEventListener('keydown', (event) => {
      if (useStack()) return;
      if (event.key === 'ArrowLeft') showMediaAt(activeMediaIndex - 1);
      if (event.key === 'ArrowRight') showMediaAt(activeMediaIndex + 1);
    });
    mediaDialog.addEventListener('pointerdown', (event) => {
      if (useStack()) return;
      swipeStartX = event.clientX;
    }, { passive: true });
    mediaDialog.addEventListener('pointerup', (event) => {
      if (useStack()) return;
      const distance = event.clientX - swipeStartX;
      if (Math.abs(distance) < 48) return;
      showMediaAt(activeMediaIndex + (distance < 0 ? 1 : -1));
    }, { passive: true });

    mediaDialog.addEventListener('close', () => {
      document.body.classList.remove('media-dialog-open');
      stackObserver?.disconnect();
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

// ---------- Availability filtering ----------
// The release table can run to sixty rows. Bedroom and price-band chips are
// emitted at build time (with the units' parsed values on each <tr>), so all
// this has to do is show and hide rows. Everything stays in the DOM, so the
// table is complete for search engines and for anyone without JS.
(function () {
  document.querySelectorAll('[data-availability-filters]').forEach((panel) => {
    const release = panel.closest('.availability-release');
    const table = release?.querySelector('.availability-table');
    const empty = release?.querySelector('[data-availability-empty]');
    const countEl = panel.querySelector('[data-availability-count]');
    const clearBtn = panel.querySelector('[data-availability-clear]');
    if (!table) return;

    const rows = Array.from(table.querySelectorAll('tbody tr'));
    const template = panel.getAttribute('data-count-template') || '';
    const active = { beds: 'all', price: 'all' };

    const matches = (row) => {
      if (active.beds !== 'all' && row.dataset.beds !== active.beds) return false;
      if (active.price !== 'all') {
        const price = Number(row.dataset.price);
        if (!Number.isFinite(price)) return false;
        const [min, max] = active.price.split('-');
        if (price < Number(min)) return false;
        if (max !== '' && price >= Number(max)) return false;
      }
      return true;
    };

    const apply = () => {
      let shown = 0;
      rows.forEach((row) => {
        const visible = matches(row);
        row.hidden = !visible;
        if (visible) shown += 1;
      });

      const filtered = active.beds !== 'all' || active.price !== 'all';
      if (countEl) {
        countEl.textContent = filtered
          ? template.replace('{shown}', String(shown)).replace('{total}', String(rows.length))
          : '';
      }
      if (clearBtn) clearBtn.hidden = !filtered;
      if (empty) empty.hidden = shown > 0;
      // A header over nothing reads as a broken table.
      table.hidden = shown === 0;
    };

    panel.querySelectorAll('[data-filter-group]').forEach((button) => {
      button.addEventListener('click', () => {
        const group = button.getAttribute('data-filter-group');
        active[group] = button.getAttribute('data-filter-value');
        panel.querySelectorAll(`[data-filter-group="${group}"]`).forEach((peer) => {
          const on = peer === button;
          peer.classList.toggle('is-active', on);
          peer.setAttribute('aria-pressed', String(on));
        });
        apply();
      });
    });

    clearBtn?.addEventListener('click', () => {
      active.beds = 'all';
      active.price = 'all';
      panel.querySelectorAll('[data-filter-group]').forEach((peer) => {
        const on = peer.getAttribute('data-filter-value') === 'all';
        peer.classList.toggle('is-active', on);
        peer.setAttribute('aria-pressed', String(on));
      });
      apply();
    });

    apply();
  });
})();
