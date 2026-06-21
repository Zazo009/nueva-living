(() => {
  const root = document.querySelector('[data-discovery]');
  if (!root) return;

  const grid = root.querySelector('[data-project-grid]');
  const cards = Array.from(root.querySelectorAll('[data-project-card]'));
  const modeButtons = Array.from(root.querySelectorAll('[data-mode]'));
  const panels = Array.from(root.querySelectorAll('[data-filter-panel]'));
  const filterButtons = Array.from(root.querySelectorAll('[data-filter]'));
  const selectedFiltersNode = root.querySelector('[data-selected-filters]');
  const countNodes = Array.from(root.querySelectorAll('[data-result-count], [data-mobile-result-count]'));
  const clearButton = root.querySelector('[data-clear-filters]');
  const sortSelect = root.querySelector('[data-sort]');
  const emptyState = root.querySelector('[data-empty-state]');
  const openButton = root.querySelector('[data-discovery-open]');
  const closeButtons = Array.from(root.querySelectorAll('[data-discovery-close]'));
  const selected = new Set();
  const mobilePanelQuery = window.matchMedia('(max-width: 640px)');

  const normalize = (value = '') =>
    String(value)
      .toLowerCase()
      .replace(/&/g, 'and')
      .replace(/\s+/g, ' ')
      .trim();

  const listFrom = (value = '') =>
    String(value)
      .split('|')
      .map((item) => item.trim())
      .filter(Boolean);

  const cardTokens = (card) => {
    if (card._lioraTokens) return card._lioraTokens;
    const values = [
      card.dataset.tags,
      card.dataset.lifestyle,
      card.dataset.architecture,
      card.dataset.location,
      card.dataset.investment,
      card.dataset.practical,
      card.dataset.title
    ];
    card._lioraTokens = new Set(values.flatMap(listFrom).map(normalize));
    return card._lioraTokens;
  };

  const numeric = (value, fallback = 99999999) => {
    const parsed = Number(value);
    return Number.isFinite(parsed) ? parsed : fallback;
  };

  const completionValue = (value = '') => {
    const [year, quarter] = String(value).split('-').map(Number);
    if (!year) return 999999;
    return year * 10 + (quarter || 4);
  };

  const releaseValue = (value = '') => {
    const time = Date.parse(`${value}-01`);
    return Number.isNaN(time) ? 0 : time;
  };

  const countLabel = (count) => `${count} curated ${count === 1 ? 'project' : 'projects'}`;

  const setPanelOpen = (open) => {
    const mobilePanel = mobilePanelQuery.matches;
    root.classList.toggle('is-discovery-collapsed', !open);
    document.body.classList.toggle('discovery-panel-open', mobilePanel && open);
    if (openButton) openButton.setAttribute('aria-expanded', open ? 'true' : 'false');
  };

  const sortCards = (items) => {
    const mode = sortSelect?.value || 'curated';
    return [...items].sort((a, b) => {
      const priorityA = numeric(a.dataset.priority, 999);
      const priorityB = numeric(b.dataset.priority, 999);
      const curated = priorityA - priorityB || String(a.dataset.title || '').localeCompare(b.dataset.title || '');

      if (mode === 'newest') return releaseValue(b.dataset.release) - releaseValue(a.dataset.release) || curated;
      if (mode === 'price-asc') return numeric(a.dataset.price) - numeric(b.dataset.price) || curated;
      if (mode === 'price-desc') return numeric(b.dataset.price, 0) - numeric(a.dataset.price, 0) || curated;
      if (mode === 'completion') return completionValue(a.dataset.completion) - completionValue(b.dataset.completion) || curated;
      if (mode === 'featured') {
        const featuredA = a.dataset.featured === 'true' ? 0 : 1;
        const featuredB = b.dataset.featured === 'true' ? 0 : 1;
        return featuredA - featuredB || curated;
      }
      return curated;
    });
  };

  const renderSelectedFilters = () => {
    if (!selectedFiltersNode) return;
    selectedFiltersNode.replaceChildren();

    if (!selected.size) {
      const empty = document.createElement('span');
      empty.textContent = 'No filters selected';
      selectedFiltersNode.append(empty);
      return;
    }

    [...selected].forEach((value) => {
      const chip = document.createElement('button');
      chip.className = 'selected-chip';
      chip.type = 'button';
      chip.textContent = value;
      chip.addEventListener('click', () => {
        selected.delete(value);
        update();
      });
      selectedFiltersNode.append(chip);
    });
  };

  function update() {
    const activeTokens = [...selected].map(normalize);
    const visible = cards.filter((card) => {
      const tokens = cardTokens(card);
      return activeTokens.every((token) => tokens.has(token));
    });
    const sorted = sortCards(cards);
    const fragment = document.createDocumentFragment();

    sorted.forEach((card) => {
      const isVisible = visible.includes(card);
      card.classList.toggle('is-filtered-out', !isVisible);
      card.setAttribute('aria-hidden', isVisible ? 'false' : 'true');
      fragment.append(card);
    });
    grid.append(fragment);

    filterButtons.forEach((button) => {
      const active = selected.has(button.dataset.filter);
      button.classList.toggle('is-active', active);
      button.setAttribute('aria-pressed', active ? 'true' : 'false');
    });

    const label = countLabel(visible.length);
    countNodes.forEach((node) => {
      node.textContent = label;
    });

    if (emptyState) emptyState.hidden = visible.length > 0;
    renderSelectedFilters();
  }

  modeButtons.forEach((button) => {
    button.addEventListener('click', () => {
      const mode = button.dataset.mode;
      modeButtons.forEach((item) => {
        const active = item === button;
        item.classList.toggle('is-active', active);
        item.setAttribute('aria-selected', active ? 'true' : 'false');
      });
      panels.forEach((panel) => {
        panel.classList.toggle('is-active', panel.dataset.filterPanel === mode);
      });
    });
  });

  filterButtons.forEach((button) => {
    button.setAttribute('aria-pressed', 'false');
    button.addEventListener('click', () => {
      const value = button.dataset.filter;
      if (selected.has(value)) selected.delete(value);
      else selected.add(value);
      update();
    });
  });

  clearButton?.addEventListener('click', () => {
    selected.clear();
    update();
  });

  sortSelect?.addEventListener('change', update);
  openButton?.addEventListener('click', () => setPanelOpen(true));
  closeButtons.forEach((button) => button.addEventListener('click', () => setPanelOpen(false)));
  mobilePanelQuery.addEventListener?.('change', () => {
    if (!mobilePanelQuery.matches) document.body.classList.remove('discovery-panel-open');
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') setPanelOpen(false);
  });

  update();
})();
