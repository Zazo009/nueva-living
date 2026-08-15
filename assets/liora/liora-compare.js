(() => {
  const root = document.querySelector('[data-compare-root]');
  if (!root) return;

  // Locale pages carry a data-i18n JSON blob on [data-compare-root];
  // English pages carry none and use the literal fallbacks below.
  let i18n = {};
  try { i18n = JSON.parse(root.dataset.i18n || '{}'); } catch { i18n = {}; }
  const tt = (key, fallback) => i18n[key] || fallback;

  // Locale pages carry <base href="../">, so a bare "developments.html"
  // written from JS would resolve to the ENGLISH page and drop the reader
  // out of their language. See the matching helper in nueva-shortlist.js.
  const LOCALE_DIRS = ['es', 'fr', 'de', 'ru', 'ar'];
  const localeDir = LOCALE_DIRS.find((dir) => location.pathname.startsWith('/' + dir + '/')) || '';
  const localeHref = (page) => (localeDir ? localeDir + '/' + page : page);

  const storageKey = 'nueva-living-shortlist-v1';

  function readShortlist() {
    try {
      const value = JSON.parse(localStorage.getItem(storageKey) || '[]');
      return Array.isArray(value) ? value : [];
    } catch {
      return [];
    }
  }

  function escapeHtml(value) {
    return String(value || '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  const onRequest = () => tt('onRequest', 'On request');

  function formatPrice(min, max) {
    const fmt = (value) => `€${Math.round(value).toLocaleString('en-US')}`;
    if (min && max && min !== max) return `${fmt(min)} - ${fmt(max)}`;
    if (min) return tt('priceFrom', 'From {price}').replace('{price}', fmt(min));
    return onRequest();
  }

  function formatBedrooms(min, max) {
    if (!min && !max) return onRequest();
    if (min && max && min !== max) return tt('bedroomsRange', '{min}-{max} bedrooms').replace('{min}', min).replace('{max}', max);
    return tt('bedroomsOne', '{n} bedrooms').replace('{n}', min || max);
  }

  function formatStatus(value) {
    if (!value) return onRequest();
    const mapped = (i18n.statusMap || {})[value];
    if (mapped) return mapped;
    return value.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
  }

  function formatDelivery(value) {
    if (!value) return tt('toBeConfirmed', 'To be confirmed');
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return value;
    return date.toLocaleDateString(tt('dateLocale', 'en-GB'), { year: 'numeric', month: 'short' });
  }

  function localizedType(value) {
    const mapped = (i18n.typeMap || {})[value];
    return mapped || value.charAt(0).toUpperCase() + value.slice(1);
  }

  function emptyState(message) {
    root.innerHTML = `<div class="compare-empty">
      <p class="body-copy">${message}</p>
      <a class="btn" href="${localeHref('developments.html')}">${tt('browse', 'Browse Developments')}</a>
    </div>`;
  }

  const ROWS = [
    [tt('rowPrice', 'Price'), (p) => formatPrice(p.priceMin, p.priceMax)],
    [tt('rowBedrooms', 'Bedrooms'), (p) => formatBedrooms(p.bedroomsMin, p.bedroomsMax)],
    [tt('rowPropertyTypes', 'Property types'), (p) => (p.propertyTypes || []).map(localizedType).join(', ') || onRequest()],
    [tt('rowStatus', 'Status'), (p) => formatStatus(p.constructionStatus)],
    [tt('rowDelivery', 'Delivery'), (p) => formatDelivery(p.deliveryDate)],
    [tt('rowTotalUnits', 'Total units'), (p) => p.totalUnits ?? onRequest()],
    [tt('rowAvailableUnits', 'Available units'), (p) => p.availableUnits ?? onRequest()],
    [tt('rowArea', 'Area'), (p) => p.area ? p.area.replace(/-/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase()) : onRequest()],
    [tt('rowAmenities', 'Amenities'), (p) => (p.amenities || []).slice(0, 6).map((a) => (i18n.amenityMap || {})[a] || a.charAt(0).toUpperCase() + a.slice(1)).join(', ') || onRequest()]
  ];

  function render(projects) {
    const head = `<tr><th scope="col">
        </th>${projects.map((p) => `<th scope="col">
          <a class="compare-card-link" href="${escapeHtml(p.url)}">
            ${p.image ? `<img src="${escapeHtml(p.image)}" alt="" width="200" height="150" loading="lazy" decoding="async">` : ''}
            <span>${escapeHtml(p.name)}</span>
          </a>
        </th>`).join('')}</tr>`;

    const body = ROWS.map(([label, getValue]) => `<tr>
        <th scope="row">${escapeHtml(label)}</th>
        ${projects.map((p) => `<td>${escapeHtml(getValue(p))}</td>`).join('')}
      </tr>`).join('\n      ');

    root.innerHTML = `<div class="compare-table-wrap">
      <table class="compare-table">
        <thead>${head}</thead>
        <tbody>
          ${body}
        </tbody>
      </table>
    </div>
    <p class="compare-note">${tt('note', 'Prices, availability and delivery dates are indicative and reconfirmed by Nueva Living before any reservation.')}</p>`;
  }

  const shortlist = readShortlist();
  if (!shortlist.length) {
    emptyState(tt('emptyNotSaved', 'You have not saved any developments yet. Save a project from its page or card to compare it here.'));
    return;
  }

  fetch('assets/liora/data/projects-catalog.json')
    .then((res) => res.json())
    .then((catalog) => {
      const byId = new Map(catalog.map((p) => [p.slug, p]));
      const matched = shortlist.map((item) => byId.get(item.id)).filter(Boolean);
      if (!matched.length) {
        emptyState(tt('emptyNotFound', 'We could not find your saved developments. They may have been updated -- try browsing again.'));
        return;
      }
      render(matched);
    })
    .catch(() => {
      emptyState(tt('emptyError', 'Comparison data is unavailable right now. Please try again shortly.'));
    });
})();
