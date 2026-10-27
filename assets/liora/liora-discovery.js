(() => {
  const root = document.querySelector('[data-discovery]');
  if (!root) return;

  const grid = root.querySelector('[data-project-grid]');
  const cards = Array.from(root.querySelectorAll('[data-project-card]'));
  const modeButtons = Array.from(root.querySelectorAll('[data-mode]'));
  const panels = Array.from(root.querySelectorAll('[data-filter-panel]'));
  const filterButtons = Array.from(root.querySelectorAll('[data-filter]'));
  const countNodes = Array.from(root.querySelectorAll('[data-result-count-summary]'));
  const clearButtons = Array.from(root.querySelectorAll('[data-clear-filters]'));
  const showButtons = Array.from(root.querySelectorAll('[data-show-results]'));
  const activeNodes = Array.from(root.querySelectorAll('[data-active-filters]'));
  const sortSelect = root.querySelector('[data-sort]');
  const emptyState = root.querySelector('[data-empty-state]');
  const selectInputs = Array.from(root.querySelectorAll('[data-filter-select]'));
  const rangeFields = Array.from(root.querySelectorAll('[data-range-field]'));
  const summary = root.querySelector('.discovery-summary');
  const selected = new Set();
  let aiMatchedSlugs = null;

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

  // A completion is "YYYY-Q" or, on 17 projects, "YYYY-MM": the second number
  // was read as a quarter either way, so "2027-12" became the twelfth quarter
  // (December 2029) and "Within 2 Years" missed projects due in 2027. Anything
  // above 4 is a month and is folded to its quarter.
  const parseCompletion = (value = '') => {
    const [year, second] = String(value).split('-').map(Number);
    if (!year) return null;
    let quarter = second || 4;
    if (quarter > 4) quarter = Math.min(4, Math.ceil(quarter / 3));
    return { year, quarter };
  };

  const completionValue = (value = '') => {
    const parsed = parseCompletion(value);
    if (!parsed) return 999999;
    return parsed.year * 10 + parsed.quarter;
  };

  // Move-in timing buckets are computed against today's date, not stored, so
  // "Within 1 Year" etc. stay accurate as time passes without manual upkeep.
  const completionDate = (value = '') => {
    const parsed = parseCompletion(value);
    if (!parsed) return null;
    const monthIndex = (parsed.quarter - 1) * 3 + 2;
    return new Date(parsed.year, monthIndex, 28);
  };

  // A finished project has no completion date to read -- the card says "Ready to
  // move in" or "Key ready" -- so it never reached any bucket, and "Ready Now"
  // left out every one of the 14 projects that are ready now.
  const timingBucket = (value, status) => {
    if (status === 'completed') return 'ready';
    const date = completionDate(value);
    if (!date) return null;
    const now = new Date();
    const oneYear = new Date(now);
    oneYear.setFullYear(now.getFullYear() + 1);
    const twoYears = new Date(now);
    twoYears.setFullYear(now.getFullYear() + 2);
    if (date <= now) return 'ready';
    if (date <= oneYear) return '1y';
    if (date <= twoYears) return '2y';
    return '2y+';
  };

  const releaseValue = (value = '') => {
    const time = Date.parse(`${value}-01`);
    return Number.isNaN(time) ? 0 : time;
  };

  // Locale pages override these via data-i18n-* attributes on the
  // [data-discovery] section; the English page carries no attributes and
  // falls back to the literals below.
  const i18n = {
    countOne: root.dataset.i18nCountOne || '{count} curated development',
    countMany: root.dataset.i18nCountMany || '{count} curated developments',
    anyPrice: root.dataset.i18nAnyPrice || 'Any price',
    any: root.dataset.i18nAny || 'Any',
    searching: root.dataset.i18nSearching || 'Searching…',
    search: root.dataset.i18nSearch || 'Search',
    aiMatching: root.dataset.i18nAiMatching || 'Showing matching developments.',
    aiNoMatch: root.dataset.i18nAiNoMatch || 'No current development matches that search.',
    aiError: root.dataset.i18nAiError || 'AI search is unavailable right now — try the filters below instead.',
    filters: root.dataset.i18nFilters || 'Filters',
    moreFilters: root.dataset.i18nMoreFilters || 'More filters',
    showOne: root.dataset.i18nShowOne || 'Show 1 development',
    showMany: root.dataset.i18nShowMany || 'Show {n} developments',
    closeFilters: root.dataset.i18nCloseFilters || 'Close filters',
    removeFilter: root.dataset.i18nRemoveFilter || 'Remove filter: {label}',
    // Map view (liora-discovery-map.js reads these through the bridge below).
    map: root.dataset.i18nMap || 'Map',
    list: root.dataset.i18nList || 'List',
    view: root.dataset.i18nView || 'View',
    drawArea: root.dataset.i18nDrawArea || 'Draw your area',
    clearArea: root.dataset.i18nClearArea || 'Clear area',
    areaChip: root.dataset.i18nAreaChip || 'Area',
    drawHint: root.dataset.i18nDrawHint || 'Drag on the map to outline an area.',
    zoomIn: root.dataset.i18nZoomIn || 'Zoom in',
    zoomOut: root.dataset.i18nZoomOut || 'Zoom out',
    mapLabel: root.dataset.i18nMapLabel || 'Map of the developments that match your filters',
    clusterMany: root.dataset.i18nClusterMany || '{n} developments',
    areaCount: root.dataset.i18nAreaCount || '{n} developments in this area',
    areaCountOne: root.dataset.i18nAreaCountOne || '1 development in this area',
    prevProject: root.dataset.i18nPrevProject || 'Previous project',
    nextProject: root.dataset.i18nNextProject || 'Next project',
    closeCard: root.dataset.i18nCloseCard || 'Close',
    unmapped: root.dataset.i18nUnmapped || 'Not shown on the map: {n}',
    backToFilters: root.dataset.i18nBackToFilters || 'Back to filters'
  };

  const countLabel = (count) => (count === 1 ? i18n.countOne : i18n.countMany).replace('{count}', String(count));

  // The line above the page heading says how many developments there are, in the visitor's language.
  const heroCount = document.querySelector('[data-hero-count]');
  if (heroCount && cards.length) heroCount.textContent = countLabel(cards.length);
  const showLabel = (count) => (count === 1 ? i18n.showOne : i18n.showMany).replace('{n}', String(count));

  // Filter-pill labels are translated; the data-filter matching value is not.
  const filterLabel = (value) => {
    const match = filterButtons.find((button) => button.dataset.filter === value);
    return match ? match.textContent.trim() : value;
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
      return curated;
    });
  };

  const svgIcon = (path, size = 12) =>
    `<svg aria-hidden="true" width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">${path}</svg>`;
  const ICON_CLOSE = '<path d="M6 6l12 12M18 6L6 18"/>';
  const ICON_CARET = '<path d="M6 9l6 6 6-6"/>';

  // --- Number formatting ---------------------------------------------------
  // Prices follow the page language (separator and currency placement),
  // Latin digits throughout, including Arabic.

  const lang = (document.documentElement.lang || 'en').toLowerCase();
  let fullFormat = null;
  let compactFormat = null;
  try {
    const tag = `${lang}-u-nu-latn`;
    fullFormat = new Intl.NumberFormat(tag, { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 });
    compactFormat = new Intl.NumberFormat(tag, { style: 'currency', currency: 'EUR', notation: 'compact', maximumFractionDigits: 2 });
  } catch {
    fullFormat = null;
  }

  const clean = (text) => text.replace(/[‎‏؜]/g, '').replace(/ /g, ' ');

  const formatFull = (value, plus) => {
    const text = fullFormat ? clean(fullFormat.format(value)) : `€${Math.round(value).toLocaleString('en-US')}`;
    return plus ? `${text}+` : text;
  };

  const formatCompact = (value, plus) => {
    if (!compactFormat) return formatFull(value, plus);
    const parts = compactFormat.formatToParts(value);
    let at = -1;
    parts.forEach((part, index) => {
      if (part.type === 'compact') at = index;
    });
    if (at < 0) {
      parts.forEach((part, index) => {
        if (part.type === 'integer' || part.type === 'fraction') at = index;
      });
    }
    let text = parts.map((part, index) => {
      let piece = part.value;
      if (lang.startsWith('en') && part.type === 'compact' && piece === 'K') piece = 'k';
      return plus && index === at ? `${piece}+` : piece;
    }).join('');
    text = clean(text);
    return text;
  };

  const formatBedrooms = (value, plus) => (plus ? `${value}+` : String(value));

  // --- Primary selects -------------------------------------------------

  // The polygon drawn on the map, as [[lat, lng], ...] or null. It narrows the
  // list exactly as a filter does: one more condition in update().
  let drawnArea = null;
  const cardPoint = (card) => {
    const lat = parseFloat(card.dataset.lat);
    const lng = parseFloat(card.dataset.lng);
    return Number.isFinite(lat) && Number.isFinite(lng) ? [lat, lng] : null;
  };
  // Ray casting in the lat/lng plane. At the scale of a drawn area on the
  // coast, the distortion against a projected plane is far below a pin.
  const insidePolygon = (point, polygon) => {
    let inside = false;
    for (let i = 0, j = polygon.length - 1; i < polygon.length; j = i, i += 1) {
      const [yi, xi] = polygon[i];
      const [yj, xj] = polygon[j];
      const crosses = (yi > point[0]) !== (yj > point[0])
        && point[1] < ((xj - xi) * (point[0] - yi)) / (yj - yi) + xi;
      if (crosses) inside = !inside;
    }
    return inside;
  };
  const inDrawnArea = (card) => {
    if (!drawnArea) return true;
    const point = cardPoint(card);
    return point ? insidePolygon(point, drawnArea) : false;
  };

  const selectState = { area: '', propertyType: '', status: '', timing: '' };
  const chipGroups = new Map();

  const selectByKey = (key) => selectInputs.find((item) => item.dataset.filterSelect === key);

  const optionLabel = (key) => {
    const select = selectByKey(key);
    const option = select && Array.from(select.options).find((item) => item.value === selectState[key]);
    return option ? option.textContent.trim() : '';
  };

  const setSelect = (key, value) => {
    const select = selectByKey(key);
    if (!select) return;
    if (value && !Array.from(select.options).some((option) => option.value === value)) return;
    selectState[key] = value;
    select.value = value;
    const group = chipGroups.get(key);
    if (group) {
      group.forEach((button) => {
        const on = button.dataset.value === value;
        button.classList.toggle('is-active', on);
        button.setAttribute('aria-pressed', on ? 'true' : 'false');
      });
    }
  };

  let uid = 0;
  selectInputs.forEach((select) => {
    const key = select.dataset.filterSelect;
    select.addEventListener('change', () => {
      aiMatchedSlugs = null;
      setSelect(key, select.value);
      update();
      syncUrl();
    });

    // The same options as single-choice chips. They are the visible control
    // for status and timing, and inside the mobile sheet for the rest; the
    // select stays the source of truth and the audit's authority.
    const group = select.closest('[data-chip-group]');
    const heading = select.closest('label')?.querySelector('span');
    if (!group || !heading) return;
    if (!heading.id) heading.id = `discoveryLabel${(uid += 1)}`;
    const wrap = document.createElement('div');
    wrap.className = 'discovery-chips';
    wrap.setAttribute('role', 'group');
    wrap.setAttribute('aria-labelledby', heading.id);
    const buttons = Array.from(select.options).map((option) => {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'discovery-chip';
      button.dataset.value = option.value;
      button.textContent = option.textContent.trim();
      button.setAttribute('aria-pressed', 'false');
      button.addEventListener('click', () => {
        aiMatchedSlugs = null;
        setSelect(key, option.value);
        update();
        syncUrl();
      });
      wrap.append(button);
      return button;
    });
    chipGroups.set(key, buttons);
    group.append(wrap);
    group.classList.add('is-enhanced');
    setSelect(key, select.value);
  });

  // --- Dual-handle range sliders ---------------------------------------

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
    const label = field.querySelector(':scope > span');
    const isPrice = key === 'price';

    // Scale under the track (decorative: the inputs carry the values).
    const ticks = document.createElement('div');
    ticks.className = 'range-ticks';
    ticks.setAttribute('aria-hidden', 'true');
    if (isPrice) {
      ticks.innerHTML = `<span>${formatCompact(bounds.min)}</span><span>${formatCompact(bounds.max)}</span>`;
    } else {
      for (let n = bounds.min; n <= bounds.max; n += bounds.step) {
        const tick = document.createElement('span');
        tick.textContent = String(n);
        ticks.append(tick);
      }
    }
    field.querySelector('.range-track-wrap')?.after(ticks);

    const labelText = () => {
      const node = label && Array.from(label.childNodes).find((child) => child.nodeType === 3);
      return (node ? node.textContent : '').trim();
    };

    const values = () => {
      let min = Number(minInput.value);
      let max = Number(maxInput.value);
      if (min > max) [min, max] = [max, min];
      return { min, max };
    };

    const isDefault = () => {
      const { min, max } = values();
      return min === bounds.min && max === bounds.max;
    };

    // `always` spells the range out even when it is the whole scale (the
    // popover's readout); the trigger and chips say "Any" instead.
    const text = (compact, always) => {
      const { min, max } = values();
      if (!always && isDefault()) return isPrice ? i18n.anyPrice : i18n.any;
      const atMax = max >= bounds.max;
      if (isPrice) {
        const format = compact ? formatCompact : formatFull;
        return `${format(min)} – ${format(max, atMax)}`;
      }
      return `${formatBedrooms(min)} – ${formatBedrooms(max, atMax)}`;
    };

    const render = () => {
      const { min, max } = values();
      rangeState[key] = { min, max };
      const pctMin = ((min - bounds.min) / (bounds.max - bounds.min)) * 100;
      const pctMax = ((max - bounds.min) / (bounds.max - bounds.min)) * 100;
      if (fill) {
        fill.style.left = `${pctMin}%`;
        fill.style.right = `${100 - pctMax}%`;
      }
      // Both handles parked at the right end: let the lower one be grabbed.
      minInput.style.zIndex = min > (bounds.min + bounds.max) / 2 ? '2' : '1';
      if (readout) readout.textContent = text(false, true);
      if (isPrice) {
        minInput.setAttribute('aria-valuetext', formatFull(min));
        maxInput.setAttribute('aria-valuetext', formatFull(max, max >= bounds.max));
      }
    };

    [minInput, maxInput].forEach((input) => {
      input?.addEventListener('input', () => {
        aiMatchedSlugs = null;
        render();
        update();
      });
      input?.addEventListener('change', syncUrl);
    });

    render();
    return { key, bounds, minInput, maxInput, render, text, isDefault, labelText, field };
  });

  const rangeBy = (key) => rangeControllers.find((item) => item.key === key);

  const setRange = (key, min, max) => {
    const controller = rangeBy(key);
    if (!controller) return;
    if (min !== undefined && controller.minInput) controller.minInput.value = String(min);
    if (max !== undefined && controller.maxInput) controller.maxInput.value = String(max);
    controller.render();
  };

  // --- Popover triggers: Price, Bedrooms, More filters -----------------

  const popFields = Array.from(root.querySelectorAll('[data-pop-field]'));
  const mobileQuery = window.matchMedia('(max-width: 640px)');
  const pops = popFields.map((field) => {
    const trigger = field.querySelector('[data-pop-trigger]');
    const pop = field.querySelector('.discovery-pop');
    const range = rangeBy(field.dataset.popField);
    const label = field.querySelector('[data-pop-label]');
    const value = field.querySelector('[data-pop-value]');
    const text = range ? range.labelText() : i18n.moreFilters;
    if (label) label.textContent = text;
    if (pop) pop.setAttribute('aria-label', text);
    if (field.dataset.popField === 'more') {
      const moreLabel = field.querySelector('[data-more-label]');
      if (moreLabel) moreLabel.textContent = i18n.moreFilters;
    }
    return { field, trigger, pop, range, value, name: field.dataset.popField, text };
  });

  // Short labels on the mobile bar come from the translated markup rather
  // than a second copy of each word.
  const lifestyleLabel = root.querySelector('.discovery-lifestyle-label');
  const texts = {
    filters: i18n.filters,
    type: root.querySelector('[data-chip-group="propertyType"] label > span')?.textContent.trim() || '',
    bedrooms: rangeBy('bedrooms')?.labelText() || '',
    lifestyle: lifestyleLabel ? lifestyleLabel.textContent.replace('✦', '').trim() : ''
  };
  root.querySelectorAll('[data-text]').forEach((node) => {
    node.textContent = texts[node.dataset.text] || '';
  });

  let openPop = null;

  const placePop = (item) => {
    item.pop.classList.remove('is-end');
    const rect = item.pop.getBoundingClientRect();
    const rtl = getComputedStyle(item.pop).direction === 'rtl';
    const overflow = rtl ? rect.left < 8 : rect.right > window.innerWidth - 8;
    if (overflow) item.pop.classList.add('is-end');
  };

  const closePop = (returnFocus) => {
    if (!openPop) return;
    const item = openPop;
    openPop = null;
    item.pop.hidden = true;
    item.trigger.setAttribute('aria-expanded', 'false');
    if (returnFocus) item.trigger.focus();
  };

  const showPop = (item) => {
    if (mobileQuery.matches) return;
    closePop(false);
    openPop = item;
    item.pop.hidden = false;
    item.trigger.setAttribute('aria-expanded', 'true');
    placePop(item);
    const first = item.pop.querySelector('input, button, select');
    if (first) first.focus({ preventScroll: true });
  };

  pops.forEach((item) => {
    item.trigger.addEventListener('click', () => {
      if (openPop === item) closePop(true);
      else showPop(item);
    });
    item.field.addEventListener('focusout', (event) => {
      if (openPop !== item) return;
      const next = event.relatedTarget;
      if (next && !item.field.contains(next)) closePop(false);
    });
  });

  document.addEventListener('pointerdown', (event) => {
    if (openPop && !openPop.field.contains(event.target)) closePop(false);
  });

  // --- Mobile filters sheet ---------------------------------------------

  const sheet = root.querySelector('[data-sheet]');
  const sheetDialog = sheet?.querySelector('[role="dialog"]');
  const sheetBody = sheet?.querySelector('[data-sheet-body]');
  const sheetOpeners = Array.from(root.querySelectorAll('[data-sheet-open]'));
  const sectionNodes = {};
  const movables = [];

  if (sheet && sheetBody) {
    const sheetTitle = sheet.querySelector('[data-sheet-title]');
    if (sheetTitle) sheetTitle.textContent = i18n.filters;
    sheetDialog.setAttribute('aria-label', i18n.filters);
    const closeButton = sheet.querySelector('.discovery-sheet-close');
    if (closeButton) closeButton.setAttribute('aria-label', i18n.closeFilters);

    const sections = {
      area: root.querySelector('[data-chip-group="area"]'),
      price: rangeBy('price')?.field,
      bedrooms: rangeBy('bedrooms')?.field,
      propertyType: root.querySelector('[data-chip-group="propertyType"]'),
      more: root.querySelector('.discovery-pop-body[data-more-body]')
    };
    Object.assign(sectionNodes, sections);
    ['area', 'price', 'bedrooms', 'propertyType', 'more'].forEach((name) => {
      const node = sections[name];
      if (!node) return;
      const marker = document.createComment(name);
      node.before(marker);
      movables.push({ node, marker });
    });
  }

  let sheetOpener = null;

  const inSheet = () => sheet && !sheet.hidden;

  const layoutForViewport = () => {
    if (!sheet) return;
    if (mobileQuery.matches) {
      closePop(false);
      movables.forEach(({ node }) => sheetBody.append(node));
      root.classList.add('is-sheet-layout');
    } else {
      if (inSheet()) closeSheet(false);
      movables.forEach(({ node, marker }) => marker.after(node));
      root.classList.remove('is-sheet-layout');
    }
  };

  const focusables = () =>
    Array.from(sheetDialog.querySelectorAll('button, select, input, a[href], [tabindex]:not([tabindex="-1"])'))
      .filter((node) => !node.disabled && node.getClientRects().length > 0);

  function openSheet(opener, target) {
    if (!sheet || !mobileQuery.matches) return;
    sheetOpener = opener || null;
    sheet.hidden = false;
    document.documentElement.classList.add('discovery-sheet-open');
    sheetOpeners.forEach((button) => button.setAttribute('aria-expanded', 'true'));
    const node = target && (target === 'more' ? root.querySelector('.discovery-lifestyle') : sectionNodes[target]);
    if (node) node.scrollIntoView({ block: 'start' });
    else sheetBody.scrollTop = 0;
    const focusTarget = (node && node.querySelector('button, input, select')) || sheetDialog;
    focusTarget.focus({ preventScroll: true });
  }

  function closeSheet(returnFocus = true) {
    if (!sheet || sheet.hidden) return;
    sheet.hidden = true;
    document.documentElement.classList.remove('discovery-sheet-open');
    sheetOpeners.forEach((button) => button.setAttribute('aria-expanded', 'false'));
    if (returnFocus && sheetOpener) sheetOpener.focus();
  }

  sheetOpeners.forEach((button) => {
    button.setAttribute('aria-haspopup', 'dialog');
    button.setAttribute('aria-expanded', 'false');
    button.addEventListener('click', () => openSheet(button, button.dataset.sheetSection));
  });
  sheet?.querySelectorAll('[data-sheet-close]').forEach((node) => {
    node.addEventListener('click', () => closeSheet(true));
  });
  sheet?.addEventListener('keydown', (event) => {
    if (event.key !== 'Tab') return;
    const nodes = focusables();
    if (!nodes.length) return;
    const first = nodes[0];
    const last = nodes[nodes.length - 1];
    if (event.shiftKey && (document.activeElement === first || document.activeElement === sheetDialog)) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  });

  document.addEventListener('keydown', (event) => {
    if (event.key !== 'Escape') return;
    if (inSheet()) {
      event.preventDefault();
      closeSheet(true);
    } else if (openPop) {
      event.preventDefault();
      closePop(true);
    }
  });

  if (mobileQuery.addEventListener) mobileQuery.addEventListener('change', layoutForViewport);
  else if (mobileQuery.addListener) mobileQuery.addListener(layoutForViewport);

  // "Show n developments": close whatever is open and bring the results
  // into view.
  const showResults = () => {
    closePop(false);
    closeSheet(false);
    // On the map the results are already in view.
    if (viewMode === 'map') return;
    const target = summary || grid;
    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    target.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
  };
  showButtons.forEach((button) => button.addEventListener('click', showResults));

  // --- Active filters (chips) ------------------------------------------

  const activeFilters = () => {
    const list = [];
    [['area', 'area'], ['propertyType', 'propertyType'], ['status', 'status'], ['timing', 'timing']].forEach(([key]) => {
      if (!selectState[key]) return;
      list.push({
        label: optionLabel(key),
        group: key === 'status' || key === 'timing' ? 'more' : key,
        clear: () => setSelect(key, '')
      });
    });
    rangeControllers.forEach((controller) => {
      if (controller.isDefault()) return;
      const prefix = controller.key === 'price' ? '' : `${controller.labelText()}: `;
      list.push({
        label: `${prefix}${controller.text(true)}`,
        group: controller.key,
        clear: () => {
          controller.minInput.value = String(controller.bounds.min);
          controller.maxInput.value = String(controller.bounds.max);
          controller.render();
        }
      });
    });
    [...selected].forEach((value) => {
      list.push({ label: filterLabel(value), group: 'more', clear: () => selected.delete(value) });
    });
    if (drawnArea) {
      list.push({ label: i18n.areaChip, group: 'drawn', clear: () => { drawnArea = null; } });
    }
    return list;
  };

  const renderActive = (list) => {
    activeNodes.forEach((node) => {
      node.replaceChildren(...list.map((item) => {
        const chip = document.createElement('button');
        chip.type = 'button';
        chip.className = 'discovery-active-chip';
        chip.setAttribute('aria-label', i18n.removeFilter.replace('{label}', item.label));
        const text = document.createElement('span');
        text.textContent = item.label;
        chip.append(text);
        chip.insertAdjacentHTML('beforeend', svgIcon(ICON_CLOSE));
        chip.addEventListener('click', () => {
          aiMatchedSlugs = null;
          item.clear();
          update();
          syncUrl();
        });
        return chip;
      }));
    });
  };

  // --- Map view bridge -----------------------------------------------------
  // The map is a second renderer of the same filtered list. It is loaded the
  // first time a visitor asks for it (Leaflet, its tiles and
  // liora-discovery-map.js all stay off the wire until then) and talks to this
  // file only through the object below, so the filter logic has one owner.

  let viewMode = 'list';
  const mapListeners = new Set();
  const bridge = {
    root,
    cards,
    i18n,
    lang,
    visible: [],
    get area() { return drawnArea; },
    cardPoint,
    // Called with a polygon of [lat, lng] pairs, or null to clear.
    setArea(polygon) {
      drawnArea = polygon && polygon.length >= 3 ? polygon : null;
      update();
    },
    price: (card) => numeric(card.dataset.price, 0),
    compactPrice: (value) => formatCompact(value),
    areaLabel: () => (selectState.area ? optionLabel('area') : (selectByKey('area')?.options[0]?.textContent.trim() || '')),
    openFilters: (opener) => { if (mobileQuery.matches) openSheet(opener, 'area'); else selectByKey('area')?.focus(); },
    subscribe(listener) { mapListeners.add(listener); return () => mapListeners.delete(listener); }
  };
  root._discovery = bridge;

  // --- Core filtering -----------------------------------------------------

  function update() {
    const activeTokens = [...selected].map(normalize);
    const price = rangeState.price || { min: 0, max: Infinity };
    const beds = rangeState.bedrooms || { min: 0, max: Infinity };
    const priceBounds = rangeBy('price')?.bounds;
    const bedsBounds = rangeBy('bedrooms')?.bounds;
    // A slider parked at either end means "no limit", not a filter. Only the
    // top end was treated that way, so anything priced below the slider's
    // floor was hidden before the visitor touched a control -- Golf Valley
    // starts at EUR450,000 against a EUR500,000 floor, so the cheapest
    // project on the site never appeared and no slider position could
    // reveal it. Both ends now open up when parked.
    const priceMax = priceBounds && price.max >= priceBounds.max ? Infinity : price.max;
    const priceMin = priceBounds && price.min <= priceBounds.min ? 0 : price.min;
    const bedsMax = bedsBounds && beds.max >= bedsBounds.max ? Infinity : beds.max;
    const bedsMin = bedsBounds && beds.min <= bedsBounds.min ? 0 : beds.min;

    const visible = cards.filter((card) => {
      if (!inDrawnArea(card)) return false;
      if (aiMatchedSlugs) return aiMatchedSlugs.has(card.id);

      const tokens = cardTokens(card);
      if (!activeTokens.every((token) => tokens.has(token))) return false;

      if (selectState.area && card.dataset.area !== selectState.area) return false;
      if (selectState.status && card.dataset.status !== selectState.status) return false;
      if (selectState.timing && timingBucket(card.dataset.completion, card.dataset.status) !== selectState.timing) return false;
      if (selectState.propertyType) {
        const types = listFrom(card.dataset.propertyTypes).map(normalize);
        if (!types.includes(selectState.propertyType)) return false;
      }

      const cardPrice = numeric(card.dataset.price, 0);
      if (cardPrice < priceMin || cardPrice > priceMax) return false;

      const bedroomsMin = numeric(card.dataset.bedroomsMin, 0);
      const bedroomsMax = numeric(card.dataset.bedroomsMax, 999);
      if (bedroomsMax < bedsMin || bedroomsMin > bedsMax) return false;

      return true;
    });

    const sorted = sortCards(cards);

    // Re-appending all of the cards detaches and re-attaches every gallery and image, which on a
    // phone is a visible flash and a lot of decoding. A filter changes which cards show, not the
    // order they sit in, so only move them when the order actually changed (a sort).
    const placed = Array.from(grid.children).filter((el) => el.matches('[data-project-card]'));
    const inOrder = placed.length === sorted.length && sorted.every((card, index) => card === placed[index]);
    const fragment = document.createDocumentFragment();

    sorted.forEach((card) => {
      const isVisible = visible.includes(card);
      card.classList.toggle('is-filtered-out', !isVisible);
      card.setAttribute('aria-hidden', isVisible ? 'false' : 'true');
      if (!inOrder) fragment.append(card);
    });
    if (!inOrder) grid.append(fragment);

    filterButtons.forEach((button) => {
      const active = selected.has(button.dataset.filter);
      button.classList.toggle('is-active', active);
      button.setAttribute('aria-pressed', active ? 'true' : 'false');
    });

    const label = countLabel(visible.length);
    countNodes.forEach((node) => {
      node.textContent = label;
    });
    const cta = showLabel(visible.length);
    showButtons.forEach((button) => {
      button.textContent = cta;
    });

    // List order, so the map's tab order and its "n / total" follow the list.
    bridge.visible = sorted.filter((card) => visible.includes(card));
    mapListeners.forEach((listener) => listener(bridge.visible));

    // On the map the overlay says it; the list's empty state would repeat it
    // above a map that already shows the same message.
    if (emptyState) emptyState.hidden = visible.length > 0 || viewMode === 'map';

    const list = activeFilters();
    renderActive(list);
    root.classList.toggle('has-active-filters', list.length > 0);
    clearButtons.forEach((button) => {
      if (button.hasAttribute('data-clear-when-active')) button.hidden = list.length === 0;
    });
    root.querySelectorAll('[data-filters-count]').forEach((node) => {
      node.textContent = String(list.length);
      node.hidden = list.length === 0;
    });
    const moreCount = list.filter((item) => item.group === 'more').length;
    root.querySelectorAll('[data-more-count]').forEach((node) => {
      node.textContent = String(moreCount);
      node.hidden = moreCount === 0;
    });

    pops.forEach((item) => {
      if (item.range && item.value) item.value.textContent = item.range.text(true);
      const on = item.range ? !item.range.isDefault() : moreCount > 0;
      item.trigger.classList.toggle('is-active', on);
    });
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
      aiMatchedSlugs = null;
      const value = button.dataset.filter;
      if (selected.has(value)) selected.delete(value);
      else selected.add(value);
      update();
      syncUrl();
    });
  });

  clearButtons.forEach((button) => {
    button.addEventListener('click', () => {
      aiMatchedSlugs = null;
      selected.clear();
      drawnArea = null;
      Object.keys(selectState).forEach((key) => setSelect(key, ''));
      rangeControllers.forEach((controller) => {
        controller.minInput.value = String(controller.bounds.min);
        controller.maxInput.value = String(controller.bounds.max);
        controller.render();
      });
      if (sortSelect) sortSelect.value = 'curated';
      update();
      syncUrl();
    });
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
    if (selectState.timing) params.set('timing', selectState.timing);
    const price = rangeState.price;
    const priceBounds = rangeBy('price')?.bounds;
    if (price && priceBounds && (price.min !== priceBounds.min || price.max !== priceBounds.max)) {
      if (price.min !== priceBounds.min) params.set('pmin', String(price.min));
      if (price.max !== priceBounds.max) params.set('pmax', String(price.max));
    }
    const beds = rangeState.bedrooms;
    const bedsBounds = rangeBy('bedrooms')?.bounds;
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

    [['area', 'area'], ['type', 'propertyType'], ['status', 'status'], ['timing', 'timing']].forEach(([param, key]) => {
      const value = params.get(param);
      if (value) setSelect(key, value);
    });

    const pmin = params.get('pmin');
    const pmax = params.get('pmax');
    if (pmin || pmax) setRange('price', pmin ? Number(pmin) : undefined, pmax ? Number(pmax) : undefined);

    const bmin = params.get('bmin');
    const bmax = params.get('bmax');
    if (bmin || bmax) setRange('bedrooms', bmin ? Number(bmin) : undefined, bmax ? Number(bmax) : undefined);

    const sort = params.get('sort');
    if (sort && sortSelect) sortSelect.value = sort;

    Object.entries(TAG_PARAM_KEYS).forEach(([mode, key]) => {
      const raw = params.get(key);
      if (!raw) return;
      raw.split(',').filter(Boolean).forEach((value) => selected.add(value));
      modeButtons.find((button) => button.dataset.mode === mode)?.click();
    });
  }

  restoreFromUrl();
  layoutForViewport();
  update();

  // --- List / Map toggle ------------------------------------------------
  // Two entry points open the map (the button beside Search, the phone pill),
  // and the segmented control switches both ways. Everything the map needs is
  // fetched here, on the first request.

  // The map's own host sits above the grid, inside a stage that only starts
  // laying the two side by side once the map is on.
  const stage = document.createElement('div');
  stage.className = 'discovery-stage';
  const mapView = document.createElement('div');
  mapView.className = 'discovery-map';
  mapView.hidden = true;
  grid.before(stage);
  stage.append(mapView, grid);

  // The two entry points (the List/Map toggle and the phone pill) are static markup, translated like the rest of the page, so
  // they reserve their space before this script runs. The runtime string wins
  // if one is supplied.
  [['.discovery-view-label-list', i18n.list],
    ['.discovery-view-label-map', i18n.map], ['.discovery-map-pill-label', i18n.map]].forEach(([selector, text]) => {
    const node = root.querySelector(selector);
    if (node && text) node.textContent = text;
  });
  root.querySelector('.discovery-view')?.setAttribute('aria-label', i18n.view);

  let mapReady = null;
  let mapOpener = null;

  const absolute = (path) => new URL(path, document.baseURI).href;
  const loadStyle = (href) => new Promise((resolve) => {
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = href;
    // A stylesheet that fails must not strand the visitor on a blank panel.
    link.onload = () => resolve(true);
    link.onerror = () => resolve(false);
    document.head.append(link);
  });
  const loadScript = (src, integrity) => new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.src = src;
    if (integrity) {
      script.integrity = integrity;
      script.crossOrigin = 'anonymous';
    }
    script.onload = resolve;
    script.onerror = () => reject(new Error(`Could not load ${src}`));
    document.head.append(script);
  });

  const ensureMap = () => {
    if (mapReady) return mapReady;
    const css = root.dataset.mapCss;
    const js = root.dataset.mapJs;
    mapReady = Promise.all([css ? loadStyle(absolute(css)) : true, js ? loadScript(absolute(js)) : Promise.reject(new Error('no map script'))])
      .then(() => window.NuevaDiscoveryMap.init(bridge));
    mapReady.catch(() => { mapReady = null; });
    return mapReady;
  };

  const syncViewButtons = () => {
    root.querySelectorAll('[data-view-mode]').forEach((button) => {
      const on = button.dataset.viewMode === viewMode;
      button.setAttribute('aria-pressed', on ? 'true' : 'false');
      button.classList.toggle('is-active', on);
    });
  };

  const setView = (mode, opener) => {
    if (mode === viewMode) return;
    if (mode === 'map') {
      mapOpener = opener || null;
      viewMode = 'map';
      root.classList.add('is-map-view');
      root.setAttribute('aria-busy', 'true');
      syncViewButtons();
      ensureMap().then((api) => {
        if (viewMode !== 'map') return;
        mapView.hidden = false;
        stage.classList.add('is-map');
        document.documentElement.classList.add('discovery-map-open');
        api.show();
        syncViewButtons();
        update();
      }).catch(() => {
        viewMode = 'list';
        root.classList.remove('is-map-view');
        syncViewButtons();
      }).finally(() => root.removeAttribute('aria-busy'));
    } else {
      viewMode = 'list';
      root.classList.remove('is-map-view');
      stage.classList.remove('is-map');
      document.documentElement.classList.remove('discovery-map-open');
      mapView.hidden = true;
      if (mapReady) mapReady.then((api) => api.hide()).catch(() => {});
      syncViewButtons();
      update();
      const back = Array.from(root.querySelectorAll('[data-view-mode="list"]')).find((button) => button.getClientRects().length)
        || mapOpener;
      if (back) back.focus({ preventScroll: true });
    }
  };
  bridge.setView = setView;
  bridge.mapView = mapView;
  bridge.grid = grid;

  root.addEventListener('click', (event) => {
    const opener = event.target.closest('[data-map-open]');
    if (opener) return setView('map', opener);
    const toggle = event.target.closest('[data-view-mode]');
    if (toggle) setView(toggle.dataset.viewMode, toggle);
  });
  syncViewButtons();

  // --- Current / Completed projects view toggle -------------------------

  const viewTabs = Array.from(document.querySelectorAll('[data-view-tab]'));
  const currentViewEls = Array.from(document.querySelectorAll('[data-current-view]'));
  const archivedSection = document.querySelector('[data-archived-section]');
  const archivedGrid = document.querySelector('[data-archived-project-grid]');
  const archivedEmpty = document.querySelector('[data-archived-empty]');
  const archivedTab = document.querySelector('[data-view-tab="archived"]');
  const viewTabsBar = document.querySelector('.developments-view-tabs');
  const hasSoldProjects = archivedGrid?.querySelector('[data-project-card]') != null;

  if (archivedEmpty && archivedGrid) {
    archivedEmpty.hidden = hasSoldProjects;
  }

  // No point showing an "Earlier Sold Projects" tab with nothing in it --
  // hide the whole tab bar until a project is actually marked archived.
  // The bar ships hidden, so a page with nothing to switch to never flashes it before this
  // script runs; it is shown here only when there are sold projects to switch to.
  if (hasSoldProjects && viewTabsBar) viewTabsBar.hidden = false;
  if (!hasSoldProjects) {
    archivedTab?.remove();
    if (viewTabsBar && viewTabsBar.querySelectorAll('[data-view-tab]').length <= 1) {
      viewTabsBar.hidden = true;
    }
  }

  if (viewTabs.length && archivedSection) {
    viewTabs.forEach((tab) => {
      tab.addEventListener('click', () => {
        const showArchived = tab.dataset.viewTab === 'archived';
        viewTabs.forEach((item) => {
          const active = item === tab;
          item.classList.toggle('is-active', active);
          item.setAttribute('aria-selected', active ? 'true' : 'false');
        });
        currentViewEls.forEach((el) => { el.hidden = showArchived; });
        archivedSection.hidden = !showArchived;
      });
    });
  }

  // --- AI-assisted free-text search --------------------------------------
  // Sends the raw query to the AI search function, which reasons over each
  // development's real profile (not just discrete filter fields) and
  // returns matching slugs directly, so results stay accurate for queries
  // that don't map cleanly onto the manual filter set.

  const aiSearchForm = root.querySelector('[data-ai-search-form]');
  const aiSearchInput = root.querySelector('[data-ai-search-input]');
  const aiSearchSubmit = root.querySelector('[data-ai-search-submit]');
  const aiSearchSubmitLabel = root.querySelector('[data-ai-search-submit-label]');
  const aiSearchStatus = root.querySelector('[data-ai-search-status]');
  const aiSearchExamples = Array.from(root.querySelectorAll('[data-ai-search-example]'));
  const aiToggle = root.querySelector('[data-ai-toggle]');
  const aiPanel = root.querySelector('[data-ai-panel]');

  // The assistant sits behind one line of text under the filters: the filters
  // are what most visitors want first, and the field opens on request.
  const setAiOpen = (open) => {
    if (!aiToggle || !aiPanel) return;
    aiPanel.hidden = !open;
    aiToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    if (open) aiSearchInput?.focus({ preventScroll: true });
  };
  aiToggle?.addEventListener('click', () => setAiOpen(aiPanel.hidden));

  const setAiSearchBusy = (busy) => {
    if (aiSearchSubmit) {
      aiSearchSubmit.disabled = busy;
      aiSearchSubmit.setAttribute('aria-busy', busy ? 'true' : 'false');
    }
    if (aiSearchSubmitLabel) aiSearchSubmitLabel.textContent = busy ? i18n.searching : i18n.search;
  };

  const showAiSearchStatus = (text, isError) => {
    if (!aiSearchStatus) return;
    aiSearchStatus.textContent = text;
    aiSearchStatus.hidden = !text;
    aiSearchStatus.classList.toggle('is-error', Boolean(isError));
  };

  const runAiSearch = async (query) => {
    if (!query) return;
    setAiSearchBusy(true);
    showAiSearchStatus('', false);
    try {
      const res = await fetch('/.netlify/functions/nueva-ai-search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query }),
      });
      const data = await res.json().catch(() => null);
      if (!res.ok || !data?.ok) throw new Error(data?.error || 'AI search failed');

      const matchedSlugs = Array.isArray(data.matchedSlugs) ? data.matchedSlugs : [];
      if (matchedSlugs.length) {
        aiMatchedSlugs = new Set(matchedSlugs);
        update();
        syncUrl();
        showAiSearchStatus(data.summary || i18n.aiMatching, false);
      } else {
        showAiSearchStatus(data.summary || i18n.aiNoMatch, false);
      }
    } catch {
      showAiSearchStatus(i18n.aiError, true);
    } finally {
      setAiSearchBusy(false);
    }
  };

  if (aiSearchForm) {
    aiSearchForm.addEventListener('submit', (event) => {
      event.preventDefault();
      runAiSearch(aiSearchInput?.value.trim());
    });
  }

  aiSearchExamples.forEach((chip) => {
    chip.addEventListener('click', () => {
      const text = chip.textContent.trim();
      if (aiSearchInput) aiSearchInput.value = text;
      runAiSearch(text);
    });
  });
})();
