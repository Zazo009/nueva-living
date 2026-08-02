(() => {
  const root = document.querySelector('[data-discovery]');
  if (!root) return;

  const grid = root.querySelector('[data-project-grid]');
  const cards = Array.from(root.querySelectorAll('[data-project-card]'));
  const modeButtons = Array.from(root.querySelectorAll('[data-mode]'));
  const panels = Array.from(root.querySelectorAll('[data-filter-panel]'));
  const filterButtons = Array.from(root.querySelectorAll('[data-filter]'));
  const selectedFiltersNode = root.querySelector('[data-selected-filters]');
  const countNodes = Array.from(root.querySelectorAll('[data-result-count], [data-result-count-summary]'));
  const clearButton = root.querySelector('[data-clear-filters]');
  const sortSelect = root.querySelector('[data-sort]');
  const emptyState = root.querySelector('[data-empty-state]');
  const selectInputs = Array.from(root.querySelectorAll('[data-filter-select]'));
  const rangeFields = Array.from(root.querySelectorAll('[data-range-field]'));
  const lifestyleToggle = root.querySelector('[data-lifestyle-toggle]');
  const lifestylePanel = root.querySelector('[data-lifestyle-panel]');
  const selected = new Set();

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

  const countLabel = (count) => `${count} curated ${count === 1 ? 'development' : 'developments'}`;

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
      return curated;
    });
  };

  const renderSelectedFilters = () => {
    if (!selectedFiltersNode) return;
    selectedFiltersNode.replaceChildren();

    if (!selected.size) {
      const empty = document.createElement('span');
      empty.textContent = 'No lifestyle filters selected';
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
        syncUrl();
      });
      selectedFiltersNode.append(chip);
    });
  };

  // --- Primary selects -------------------------------------------------

  const selectState = { area: '', propertyType: '', status: '' };
  selectInputs.forEach((select) => {
    const key = select.dataset.filterSelect;
    select.addEventListener('change', () => {
      selectState[key] = select.value;
      update();
      syncUrl();
    });
  });

  // --- Dual-handle range sliders ---------------------------------------

  const formatPrice = (value, bounds, isMax) => {
    if (isMax && value >= bounds.max) return `${formatPriceValue(value)}+`;
    return formatPriceValue(value);
  };

  const formatPriceValue = (value) => {
    if (value >= 1000000) {
      const millions = value / 1000000;
      return `€${millions % 1 === 0 ? millions.toFixed(0) : millions.toFixed(1)}M`;
    }
    return `€${Math.round(value).toLocaleString('en-US')}`;
  };

  const formatBedrooms = (value, bounds, isMax) => (isMax && value >= bounds.max ? `${value}+` : `${value}`);

  const rangeState = {};

  const rangeControllers = rangeFields.map((field) => {
    const key = field.dataset.rangeField;
    const bounds = {
      min: Number(field.dataset.rangeMin),
      max: Number(field.dataset.rangeMax),
      step: Number(field.dataset.rangeStep)
    };
    const minInput = field.querySelector('[data-range-input="min"]');
    const maxInput = field.querySelector('[data-range-input="max"]');
    const fill = field.querySelector('[data-range-fill]');
    const readout = field.querySelector('[data-range-readout]');
    const formatter = key === 'price' ? formatPrice : formatBedrooms;

    rangeState[key] = { min: bounds.min, max: bounds.max };

    const render = () => {
      let min = Number(minInput.value);
      let max = Number(maxInput.value);
      if (min > max) {
        [min, max] = [max, min];
      }
      rangeState[key] = { min, max };
      const pctMin = ((min - bounds.min) / (bounds.max - bounds.min)) * 100;
      const pctMax = ((max - bounds.min) / (bounds.max - bounds.min)) * 100;
      if (fill) {
        fill.style.left = `${pctMin}%`;
        fill.style.right = `${100 - pctMax}%`;
      }
      if (readout) {
        readout.textContent = min === bounds.min && max === bounds.max
          ? (key === 'price' ? 'Any price' : 'Any')
          : `${formatter(min, bounds, false)} – ${formatter(max, bounds, true)}`;
      }
    };

    [minInput, maxInput].forEach((input) => {
      input?.addEventListener('input', () => {
        render();
        update();
      });
      input?.addEventListener('change', syncUrl);
    });

    render();
    return { key, bounds, minInput, maxInput, render };
  });

  const setRange = (key, min, max) => {
    const controller = rangeControllers.find((item) => item.key === key);
    if (!controller) return;
    if (min !== undefined && controller.minInput) controller.minInput.value = String(min);
    if (max !== undefined && controller.maxInput) controller.maxInput.value = String(max);
    controller.render();
  };

  // --- Lifestyle panel toggle -------------------------------------------

  const setLifestyleOpen = (open) => {
    if (!lifestylePanel || !lifestyleToggle) return;
    lifestylePanel.hidden = !open;
    lifestyleToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    root.classList.toggle('is-lifestyle-open', open);
  };

  lifestyleToggle?.addEventListener('click', () => {
    setLifestyleOpen(lifestylePanel?.hidden !== false);
  });

  // --- Core filtering -----------------------------------------------------

  function update() {
    const activeTokens = [...selected].map(normalize);
    const price = rangeState.price || { min: 0, max: Infinity };
    const beds = rangeState.bedrooms || { min: 0, max: Infinity };
    const priceBounds = rangeControllers.find((item) => item.key === 'price')?.bounds;
    const bedsBounds = rangeControllers.find((item) => item.key === 'bedrooms')?.bounds;
    const priceMax = priceBounds && price.max >= priceBounds.max ? Infinity : price.max;
    const bedsMax = bedsBounds && beds.max >= bedsBounds.max ? Infinity : beds.max;

    const visible = cards.filter((card) => {
      const tokens = cardTokens(card);
      if (!activeTokens.every((token) => tokens.has(token))) return false;

      if (selectState.area && card.dataset.area !== selectState.area) return false;
      if (selectState.status && card.dataset.status !== selectState.status) return false;
      if (selectState.propertyType) {
        const types = listFrom(card.dataset.propertyTypes).map(normalize);
        if (!types.includes(selectState.propertyType)) return false;
      }

      const cardPrice = numeric(card.dataset.price, 0);
      if (cardPrice < price.min || cardPrice > priceMax) return false;

      const bedroomsMin = numeric(card.dataset.bedroomsMin, 0);
      const bedroomsMax = numeric(card.dataset.bedroomsMax, 999);
      if (bedroomsMax < beds.min || bedroomsMin > bedsMax) return false;

      return true;
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
      syncUrl();
    });
  });

  clearButton?.addEventListener('click', () => {
    selected.clear();
    selectState.area = '';
    selectState.propertyType = '';
    selectState.status = '';
    selectInputs.forEach((select) => { select.value = ''; });
    rangeControllers.forEach((controller) => {
      controller.minInput.value = String(controller.bounds.min);
      controller.maxInput.value = String(controller.bounds.max);
      controller.render();
    });
    if (sortSelect) sortSelect.value = 'curated';
    update();
    syncUrl();
  });

  sortSelect?.addEventListener('change', () => {
    update();
    syncUrl();
  });

  // --- URL sync -------------------------------------------------------

  const TAG_PARAM_KEYS = {
    lifestyle: 'lifestyle',
    architecture: 'architecture',
    location: 'setting',
    investment: 'investment'
  };

  function syncUrl() {
    const params = new URLSearchParams();
    if (selectState.area) params.set('area', selectState.area);
    if (selectState.propertyType) params.set('type', selectState.propertyType);
    if (selectState.status) params.set('status', selectState.status);
    const price = rangeState.price;
    const priceBounds = rangeControllers.find((item) => item.key === 'price')?.bounds;
    if (price && priceBounds && (price.min !== priceBounds.min || price.max !== priceBounds.max)) {
      if (price.min !== priceBounds.min) params.set('pmin', String(price.min));
      if (price.max !== priceBounds.max) params.set('pmax', String(price.max));
    }
    const beds = rangeState.bedrooms;
    const bedsBounds = rangeControllers.find((item) => item.key === 'bedrooms')?.bounds;
    if (beds && bedsBounds && (beds.min !== bedsBounds.min || beds.max !== bedsBounds.max)) {
      if (beds.min !== bedsBounds.min) params.set('bmin', String(beds.min));
      if (beds.max !== bedsBounds.max) params.set('bmax', String(beds.max));
    }
    if (sortSelect && sortSelect.value !== 'curated') params.set('sort', sortSelect.value);

    panels.forEach((panel) => {
      const mode = panel.dataset.filterPanel;
      const key = TAG_PARAM_KEYS[mode];
      if (!key) return;
      const values = Array.from(panel.querySelectorAll('[data-filter]'))
        .filter((button) => selected.has(button.dataset.filter))
        .map((button) => button.dataset.filter);
      if (values.length) params.set(key, values.join(','));
    });

    const query = params.toString();
    const url = `${window.location.pathname}${query ? `?${query}` : ''}`;
    window.history.replaceState(null, '', url);
  }

  function restoreFromUrl() {
    const params = new URLSearchParams(window.location.search);
    if (!params.toString()) return;

    const area = params.get('area');
    if (area) {
      const select = selectInputs.find((item) => item.dataset.filterSelect === 'area');
      if (select) { select.value = area; selectState.area = area; }
    }
    const type = params.get('type');
    if (type) {
      const select = selectInputs.find((item) => item.dataset.filterSelect === 'propertyType');
      if (select) { select.value = type; selectState.propertyType = type; }
    }
    const status = params.get('status');
    if (status) {
      const select = selectInputs.find((item) => item.dataset.filterSelect === 'status');
      if (select) { select.value = status; selectState.status = status; }
    }

    const pmin = params.get('pmin');
    const pmax = params.get('pmax');
    if (pmin || pmax) setRange('price', pmin ? Number(pmin) : undefined, pmax ? Number(pmax) : undefined);

    const bmin = params.get('bmin');
    const bmax = params.get('bmax');
    if (bmin || bmax) setRange('bedrooms', bmin ? Number(bmin) : undefined, bmax ? Number(bmax) : undefined);

    const sort = params.get('sort');
    if (sort && sortSelect) sortSelect.value = sort;

    let hasTagFilters = false;
    Object.entries(TAG_PARAM_KEYS).forEach(([mode, key]) => {
      const raw = params.get(key);
      if (!raw) return;
      raw.split(',').filter(Boolean).forEach((value) => {
        selected.add(value);
        hasTagFilters = true;
      });
      if (hasTagFilters) {
        const modeButton = modeButtons.find((button) => button.dataset.mode === mode);
        modeButton?.click();
      }
    });

    if (hasTagFilters) setLifestyleOpen(true);
  }

  restoreFromUrl();
  update();

  // --- Card image galleries -------------------------------------------

  root.querySelectorAll('[data-project-card-gallery]').forEach((gallery) => {
    const track = gallery.querySelector('[data-gallery-track]');
    const dots = Array.from(gallery.querySelectorAll('[data-gallery-dot]'));
    if (!track) return;

    const setActiveDot = () => {
      if (!dots.length || !track.clientWidth) return;
      const index = Math.round(track.scrollLeft / track.clientWidth);
      dots.forEach((dot, i) => dot.classList.toggle('is-active', i === index));
    };

    let scrollTimer = null;
    track.addEventListener('scroll', () => {
      clearTimeout(scrollTimer);
      scrollTimer = setTimeout(setActiveDot, 80);
    }, { passive: true });

    dots.forEach((dot, index) => {
      dot.addEventListener('click', (event) => {
        event.stopPropagation();
        track.scrollTo({ left: index * track.clientWidth, behavior: 'smooth' });
      });
    });

    gallery.addEventListener('click', (event) => {
      if (event.target.closest('[data-gallery-dot]')) return;
      const url = gallery.getAttribute('data-card-url');
      if (url) window.location.href = url;
    });
  });
})();
