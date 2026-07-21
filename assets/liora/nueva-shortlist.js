(() => {
  const storageKey = 'nueva-living-shortlist-v1';
  const projectPathPattern = /property-[a-z0-9-]+\.html/i;
  let savedProjects = readShortlist();
  let previousFocus = null;
  let toastTimer = 0;

  function clean(value) {
    return String(value || '').replace(/\s+/g, ' ').trim();
  }

  function escapeHtml(value) {
    return String(value || '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  function normalizedProjectUrl(value) {
    const match = clean(value).match(projectPathPattern);
    return match ? match[0] : '';
  }

  function projectIdFromUrl(value) {
    return normalizedProjectUrl(value)
      .replace(/^property-/, '')
      .replace(/\.html$/i, '');
  }

  function safeProject(project) {
    const url = normalizedProjectUrl(project?.url);
    const id = clean(project?.id) || projectIdFromUrl(url);
    const name = clean(project?.name);
    if (!id || !url || !name) return null;

    return {
      id,
      name,
      url,
      location: clean(project?.location),
      image: clean(project?.image),
      price: clean(project?.price),
      type: clean(project?.type)
    };
  }

  function readShortlist() {
    try {
      const value = JSON.parse(localStorage.getItem(storageKey) || '[]');
      if (!Array.isArray(value)) return [];
      return value.map(safeProject).filter(Boolean).slice(0, 24);
    } catch {
      return [];
    }
  }

  function writeShortlist() {
    try {
      localStorage.setItem(storageKey, JSON.stringify(savedProjects));
    } catch {
      // The shortlist remains usable for this page even if storage is unavailable.
    }
  }

  function heartIcon() {
    return '<svg class="nueva-heart-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78L12 21.23l8.84-8.84a5.5 5.5 0 0 0 0-7.78Z"/></svg>';
  }

  function projectFromCard(card) {
    const link = card.querySelector('.project-link[href*="property-"], .dev-cta-link[href*="property-"]');
    const url = normalizedProjectUrl(link?.getAttribute('href') || card.dataset.cardUrl);
    const image = card.querySelector('img');
    const metaValues = [...card.querySelectorAll('.meta strong, .dev-meta-item .val')].map((node) => clean(node.textContent));
    return safeProject({
      id: card.id || projectIdFromUrl(url),
      name: card.dataset.title || card.querySelector('.dev-name, h3, [data-project-name]')?.textContent,
      url,
      location: card.querySelector('.dev-loc, .project-body > .label')?.textContent,
      image: image?.getAttribute('src'),
      price: metaValues[0],
      type: metaValues[1]
    });
  }

  function projectFromPage() {
    const name = clean(document.body?.dataset?.projectName);
    const url = normalizedProjectUrl(window.location.pathname);
    if (!name || !url) return null;

    const facts = [...document.querySelectorAll('.hero-fact')];
    const factValue = (label) => facts.find((fact) => clean(fact.querySelector('span')?.textContent).toLowerCase().includes(label))
      ?.querySelector('strong')?.textContent;

    return safeProject({
      id: projectIdFromUrl(url),
      name,
      url,
      location: factValue('location'),
      price: factValue('price'),
      type: factValue('type'),
      image: document.querySelector('.project-hero-img')?.getAttribute('src')
    });
  }

  function isSaved(id) {
    return savedProjects.some((project) => project.id === id);
  }

  function track(eventName, project) {
    window.lioraTrack?.(eventName, {
      shortlist_count: savedProjects.length,
      project: project?.name,
      project_id: project?.id
    });
  }

  function showToast(message) {
    const toast = document.querySelector('[data-shortlist-toast]');
    if (!toast) return;
    toast.textContent = message;
    toast.classList.add('is-visible');
    window.clearTimeout(toastTimer);
    toastTimer = window.setTimeout(() => toast.classList.remove('is-visible'), 2400);
  }

  function toggleProject(project) {
    const existingIndex = savedProjects.findIndex((item) => item.id === project.id);
    const added = existingIndex === -1;

    if (added) savedProjects.push(project);
    else savedProjects.splice(existingIndex, 1);

    writeShortlist();
    render();
    showToast(added ? `${project.name} added to your shortlist.` : `${project.name} removed from your shortlist.`);
    track(added ? 'shortlist_add' : 'shortlist_remove', project);
  }

  function favoriteButton(project, extraClass = '') {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = `nueva-favorite-button ${extraClass}`.trim();
    button.dataset.shortlistId = project.id;
    button.innerHTML = `${heartIcon()}${extraClass ? '<span data-save-project-label>Save Project</span>' : ''}`;
    button.addEventListener('pointerdown', (event) => event.stopPropagation());
    button.addEventListener('click', (event) => {
      event.preventDefault();
      event.stopPropagation();
      toggleProject(project);
    });
    return button;
  }

  function enhanceProjectCards() {
    document.querySelectorAll('[data-project-card], .dev-card[data-card-url]').forEach((card) => {
      if (card.dataset.shortlistReady === 'true') return;
      const project = projectFromCard(card);
      if (!project) return;

      const target = card.matches('.dev-card') ? card.querySelector('.dev-img-wrap') : card;
      if (!target) return;
      target.appendChild(favoriteButton(project));
      card.dataset.shortlistReady = 'true';
    });
  }

  function enhanceProjectPage() {
    const project = projectFromPage();
    const actions = document.querySelector('.project-hero .hero-actions');
    if (!project || !actions || actions.querySelector('[data-shortlist-id]')) return;
    actions.appendChild(favoriteButton(project, 'nueva-save-project'));
  }

  function triggerMarkup(className, label) {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = `nueva-shortlist-trigger ${className}`;
    button.setAttribute('aria-haspopup', 'dialog');
    button.setAttribute('aria-controls', 'nuevaShortlistDrawer');
    button.innerHTML = `${heartIcon()}${label ? '<span>Shortlist</span>' : ''}<span class="nueva-shortlist-count" data-shortlist-count>0</span>`;
    button.addEventListener('click', openDrawer);
    return button;
  }

  function enhanceNavigation() {
    const nav = document.querySelector('.site-nav, #nav');
    if (!nav || nav.dataset.shortlistReady === 'true') return;

    const rightLinks = nav.querySelector('.nav-links-right');
    if (rightLinks) {
      const desktopTrigger = triggerMarkup('nueva-shortlist-nav-trigger', true);
      if (rightLinks.tagName === 'UL') {
        const item = document.createElement('li');
        item.className = 'nueva-shortlist-nav-item';
        item.appendChild(desktopTrigger);
        rightLinks.appendChild(item);
      } else {
        rightLinks.appendChild(desktopTrigger);
      }
    }

    const burger = nav.querySelector('.nav-burger, #burgerBtn');
    const mobileTrigger = triggerMarkup('nueva-shortlist-mobile-trigger', false);
    if (burger) nav.insertBefore(mobileTrigger, burger);
    else nav.appendChild(mobileTrigger);

    nav.dataset.shortlistReady = 'true';
  }

  function drawerTemplate() {
    const scrim = document.createElement('button');
    scrim.type = 'button';
    scrim.className = 'nueva-shortlist-scrim';
    scrim.dataset.shortlistScrim = '';
    scrim.setAttribute('aria-label', 'Close shortlist');
    scrim.addEventListener('click', closeDrawer);

    const drawer = document.createElement('aside');
    drawer.className = 'nueva-shortlist-drawer';
    drawer.id = 'nuevaShortlistDrawer';
    drawer.setAttribute('role', 'dialog');
    drawer.setAttribute('aria-modal', 'true');
    drawer.setAttribute('aria-labelledby', 'nuevaShortlistTitle');
    drawer.setAttribute('aria-hidden', 'true');
    drawer.innerHTML = `
      <header class="nueva-shortlist-head">
        <div>
          <span class="nueva-shortlist-eyebrow">Your Shortlist</span>
          <h2 class="nueva-shortlist-title" id="nuevaShortlistTitle">Saved Projects</h2>
        </div>
        <button class="nueva-shortlist-close" type="button" data-shortlist-close aria-label="Close shortlist">&times;</button>
      </header>
      <div class="nueva-shortlist-body" data-shortlist-body></div>`;
    drawer.querySelector('[data-shortlist-close]').addEventListener('click', closeDrawer);
    drawer.addEventListener('keydown', trapFocus);

    const toast = document.createElement('div');
    toast.className = 'nueva-shortlist-toast';
    toast.dataset.shortlistToast = '';
    toast.setAttribute('role', 'status');
    toast.setAttribute('aria-live', 'polite');

    document.body.append(scrim, drawer, toast);
  }

  function shortlistMessage() {
    const lines = savedProjects.map((project, index) => {
      const details = [project.location, project.price].filter(Boolean).join(' | ');
      return `${index + 1}. ${project.name}${details ? ` - ${details}` : ''}`;
    });
    return `I would like to discuss my Nueva Living shortlist:\n\n${lines.join('\n')}`;
  }

  function itemMarkup(project) {
    return `
      <li class="nueva-shortlist-item">
        ${project.image
          ? `<img class="nueva-shortlist-item-image" src="${escapeHtml(project.image)}" alt="" width="216" height="162" loading="lazy" decoding="async">`
          : '<span class="nueva-shortlist-item-image" aria-hidden="true"></span>'}
        <div class="nueva-shortlist-item-copy">
          <span>${escapeHtml(project.location || project.type || 'Nueva Living selection')}</span>
          <strong>${escapeHtml(project.name)}</strong>
          <a href="${escapeHtml(project.url)}">View Project</a>
        </div>
        <button class="nueva-shortlist-remove" type="button" data-remove-shortlist="${escapeHtml(project.id)}" aria-label="Remove ${escapeHtml(project.name)} from shortlist">
          ${heartIcon()}
        </button>
      </li>`;
  }

  function emptyMarkup() {
    return `
      <div class="nueva-shortlist-empty">
        <span class="nueva-shortlist-empty-icon">${heartIcon()}</span>
        <p>Tap the heart on any project to build a private shortlist you can keep, compare and send to us.</p>
        <a class="nueva-shortlist-browse" href="developments.html">Browse Developments</a>
      </div>`;
  }

  function formMarkup() {
    const names = savedProjects.map((project) => project.name).join(', ');
    return `
      <div class="nueva-shortlist-form-shell">
        <h3>Send Your Shortlist</h3>
        <p>Share the projects you saved and we will come back with current availability, useful comparisons and the right next step.</p>
        <form class="nueva-shortlist-form" name="nueva-shortlist" method="POST" data-crm-lead action="/.netlify/functions/nueva-lead">
          <input type="hidden" name="request_context" value="Nueva Living shortlist: ${escapeHtml(names)}">
          <input type="hidden" name="project" value="${escapeHtml(names)}">
          <div class="nueva-shortlist-field">
            <label for="shortlistFirstName">First Name</label>
            <input id="shortlistFirstName" name="first_name" type="text" autocomplete="given-name" required>
          </div>
          <div class="nueva-shortlist-field">
            <label for="shortlistLastName">Last Name</label>
            <input id="shortlistLastName" name="last_name" type="text" autocomplete="family-name" required>
          </div>
          <div class="nueva-shortlist-field">
            <label for="shortlistEmail">Email</label>
            <input id="shortlistEmail" name="email" type="email" autocomplete="email" required>
          </div>
          <div class="nueva-shortlist-field">
            <label for="shortlistPhone">Phone / WhatsApp</label>
            <input id="shortlistPhone" name="phone" type="tel" autocomplete="tel">
          </div>
          <div class="nueva-shortlist-field">
            <label for="shortlistMessage">Anything We Should Know?</label>
            <textarea id="shortlistMessage" name="message">${escapeHtml(shortlistMessage())}</textarea>
          </div>
          <label class="nueva-shortlist-consent">
            <input name="consent" type="checkbox" required>
            <span>I agree to be contacted and for my data to be stored.</span>
          </label>
          <button class="nueva-shortlist-submit" type="submit">Send Shortlist</button>
          <span class="form-response" role="status" aria-live="polite"></span>
        </form>
      </div>`;
  }

  function renderDrawer() {
    const body = document.querySelector('[data-shortlist-body]');
    if (!body) return;

    body.innerHTML = savedProjects.length
      ? `<ol class="nueva-shortlist-items">${savedProjects.map(itemMarkup).join('')}</ol>${formMarkup()}`
      : emptyMarkup();

    body.querySelectorAll('[data-remove-shortlist]').forEach((button) => {
      button.addEventListener('click', () => {
        const project = savedProjects.find((item) => item.id === button.dataset.removeShortlist);
        if (project) toggleProject(project);
      });
    });

    const form = body.querySelector('form[data-crm-lead]');
    if (form) {
      window.nuevaRegisterLeadForms?.(body);
      form.addEventListener('submit', () => track('shortlist_send', { name: 'Shortlist' }), { capture: true });
    }
  }

  function updateControls() {
    const count = savedProjects.length;
    document.querySelectorAll('[data-shortlist-count]').forEach((node) => {
      node.textContent = String(count);
      node.setAttribute('aria-label', `${count} saved ${count === 1 ? 'project' : 'projects'}`);
    });

    document.querySelectorAll('[data-shortlist-id]').forEach((button) => {
      const saved = isSaved(button.dataset.shortlistId);
      const projectName = projectFromPage()?.name || projectFromCard(button.closest('[data-project-card], .dev-card'))?.name || 'project';
      button.classList.toggle('is-saved', saved);
      button.setAttribute('aria-pressed', String(saved));
      button.setAttribute('aria-label', saved ? `Remove ${projectName} from shortlist` : `Save ${projectName} to shortlist`);
      button.title = saved ? 'Remove from shortlist' : 'Save to shortlist';
      const label = button.querySelector('[data-save-project-label]');
      if (label) label.textContent = saved ? 'Saved to Shortlist' : 'Save Project';
    });
  }

  function render() {
    updateControls();
    renderDrawer();
  }

  function openDrawer() {
    const drawer = document.getElementById('nuevaShortlistDrawer');
    const scrim = document.querySelector('[data-shortlist-scrim]');
    if (!drawer || !scrim) return;

    previousFocus = document.activeElement;
    renderDrawer();
    drawer.classList.add('is-open');
    scrim.classList.add('is-open');
    drawer.setAttribute('aria-hidden', 'false');
    document.body.classList.add('nueva-shortlist-open');
    drawer.querySelector('[data-shortlist-close]')?.focus({ preventScroll: true });
    track('shortlist_open');
  }

  function closeDrawer() {
    const drawer = document.getElementById('nuevaShortlistDrawer');
    const scrim = document.querySelector('[data-shortlist-scrim]');
    if (!drawer || !scrim) return;

    drawer.classList.remove('is-open');
    scrim.classList.remove('is-open');
    drawer.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('nueva-shortlist-open');
    previousFocus?.focus?.({ preventScroll: true });
  }

  function trapFocus(event) {
    if (event.key === 'Escape') {
      event.preventDefault();
      closeDrawer();
      return;
    }
    if (event.key !== 'Tab') return;

    const focusable = [...event.currentTarget.querySelectorAll('a[href], button:not([disabled]), input:not([disabled]), textarea:not([disabled])')]
      .filter((node) => node.offsetParent !== null);
    if (!focusable.length) return;
    const first = focusable[0];
    const last = focusable.at(-1);

    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  }

  function initialize() {
    drawerTemplate();
    enhanceNavigation();
    enhanceProjectCards();
    enhanceProjectPage();
    render();

    window.addEventListener('storage', (event) => {
      if (event.key !== storageKey) return;
      savedProjects = readShortlist();
      render();
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initialize, { once: true });
  else initialize();
})();
