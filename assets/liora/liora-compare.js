(() => {
  const root = document.querySelector('[data-compare-root]');
  if (!root) return;

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

  function formatPrice(min, max) {
    const fmt = (value) => `€${Math.round(value).toLocaleString('en-US')}`;
    if (min && max && min !== max) return `${fmt(min)} - ${fmt(max)}`;
    if (min) return `From ${fmt(min)}`;
    return 'On request';
  }

  function formatBedrooms(min, max) {
    if (!min && !max) return 'On request';
    if (min && max && min !== max) return `${min}-${max} bedrooms`;
    return `${min || max} bedrooms`;
  }

  function formatStatus(value) {
    if (!value) return 'On request';
    return value.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
  }

  function formatDelivery(value) {
    if (!value) return 'To be confirmed';
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return value;
    return date.toLocaleDateString('en-GB', { year: 'numeric', month: 'short' });
  }

  function emptyState(message) {
    root.innerHTML = `<div class="compare-empty">
      <p class="body-copy">${message}</p>
      <a class="btn" href="developments.html">Browse Developments</a>
    </div>`;
  }

  const ROWS = [
    ['Price', (p) => formatPrice(p.priceMin, p.priceMax)],
    ['Bedrooms', (p) => formatBedrooms(p.bedroomsMin, p.bedroomsMax)],
    ['Property types', (p) => (p.propertyTypes || []).map((t) => t.charAt(0).toUpperCase() + t.slice(1)).join(', ') || 'On request'],
    ['Status', (p) => formatStatus(p.constructionStatus)],
    ['Delivery', (p) => formatDelivery(p.deliveryDate)],
    ['Total units', (p) => p.totalUnits ?? 'On request'],
    ['Available units', (p) => p.availableUnits ?? 'On request'],
    ['Area', (p) => p.area ? p.area.replace(/-/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase()) : 'On request'],
    ['Amenities', (p) => (p.amenities || []).slice(0, 6).map((a) => a.charAt(0).toUpperCase() + a.slice(1)).join(', ') || 'On request']
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
    <p class="compare-note">Prices, availability and delivery dates are indicative and reconfirmed by Nueva Living before any reservation.</p>`;
  }

  const shortlist = readShortlist();
  if (!shortlist.length) {
    emptyState('You have not saved any developments yet. Save a project from its page or card to compare it here.');
    return;
  }

  fetch('assets/liora/data/projects-catalog.json')
    .then((res) => res.json())
    .then((catalog) => {
      const byId = new Map(catalog.map((p) => [p.slug, p]));
      const matched = shortlist.map((item) => byId.get(item.id)).filter(Boolean);
      if (!matched.length) {
        emptyState('We could not find your saved developments. They may have been updated -- try browsing again.');
        return;
      }
      render(matched);
    })
    .catch(() => {
      emptyState('Comparison data is unavailable right now. Please try again shortly.');
    });
})();
