// The search preview on ai.html: three buyer briefs, each with two refinements, answered from the
// same catalogue the assistant connector serves (buildMcpCatalog, the source of
// netlify/functions/data/mcp-catalog.json). It runs in the visitor's browser with no assistant and
// no network call: every answer is worked out here, at build time, and printed into the page.
//
// Honesty rules, because a preview that over-promises is worse than none:
// - Budget is judged home by home on the price list, as the connector does. A project whose range
//   overlaps the budget but whose remaining homes do not is left out.
// - Type is judged home by home too. In a project that mixes apartments and villas, only the homes
//   whose price-list line names them a villa count as villas, so Selwo's €464,000 apartment never
//   stands behind "a villa under €2 million"; its semi-detached villas from €1,468,000 do.
// - "Private pool" is only claimed for projects whose homes are all villas and whose page names a
//   private pool. Each of those was read on 2026-11-18 and says every villa has its own pool. In a
//   mixed project the pool belongs to some homes only, so such a project never matches it.
// - "Key-ready" is the construction stage "completed", which applies to every home in the project.
// - "In Mijas" is the project's own location line naming Mijas; El Higuerón is in Fuengirola.
// - The price shown is the lowest price among the homes that match, not the project's floor.
// The build stops if any of these cannot be applied, rather than print a card that might not match.
import { buildMcpCatalog } from './mcp_catalog.mjs';
import { PRICE_FORMAT } from './prices.mjs';
import { existsSync } from 'node:fs';

const BRIEFS = [
  {
    key: 'E',
    lead: 'atalaya-pool-villas',
    label: 'A villa in Estepona',
    type: 'villa',
    match: (p) => p.area === 'estepona',
    refinements: [
      { key: 1, label: 'Under &euro;2 million', budgetMax: 2000000 },
      { key: 2, label: 'Private pool', privatePool: true },
    ],
    questions: [
      'I&rsquo;m looking for a villa in Estepona.',
      'I&rsquo;m looking for a villa in Estepona under &euro;2 million.',
      'I&rsquo;m looking for a villa in Estepona with a private pool.',
      'I&rsquo;m looking for a villa in Estepona under &euro;2 million with a private pool.',
    ],
  },
  {
    key: 'M',
    lead: 'mijas-golf-park-residences',
    label: 'An apartment in Mijas',
    type: 'apartment',
    match: (p) => p.area === 'mijas-fuengirola' && /mijas/i.test(p.locales.en.location || ''),
    refinements: [
      { key: 1, label: 'Key-ready', keyReady: true },
      { key: 2, label: 'Under &euro;500,000', budgetMax: 500000 },
    ],
    questions: [
      'I&rsquo;m looking for a new apartment in Mijas.',
      'I&rsquo;m looking for a new, key-ready apartment in Mijas.',
      'I&rsquo;m looking for a new apartment in Mijas under &euro;500,000.',
      'I&rsquo;m looking for a new, key-ready apartment in Mijas under &euro;500,000.',
    ],
  },
  {
    key: 'N',
    lead: 'vega-verde-residences',
    label: 'New in Nueva Andaluc&iacute;a',
    type: null,
    match: (p) => p.area === 'nueva-andalucia',
    refinements: [
      { key: 1, label: 'Key-ready', keyReady: true },
      { key: 2, label: 'Under &euro;1.5 million', budgetMax: 1500000 },
    ],
    questions: [
      'I&rsquo;m looking for a new home in Nueva Andaluc&iacute;a.',
      'I&rsquo;m looking for a new, key-ready home in Nueva Andaluc&iacute;a.',
      'I&rsquo;m looking for a new home in Nueva Andaluc&iacute;a under &euro;1.5 million.',
      'I&rsquo;m looking for a new, key-ready home in Nueva Andaluc&iacute;a under &euro;1.5 million.',
    ],
  },
];

const eur = (value) => {
  const m = /(?:EUR|€)\s*([\d,.]+)/.exec(String(value || ''));
  if (!m) return null;
  const n = Number(m[1].replace(/[.,](?=\d{3}\b)/g, ''));
  return Number.isFinite(n) && n > 10000 ? n : null;
};
const VILLA_LINE = /villa/i;
const HOUSE_LINE = /villa|townhouse|town house|house|adosad/i;

// The homes of one project that are of the brief's type, with their prices (null: on request).
function homesOfType(raw, catalogEntry, type) {
  const units = raw.availability?.units || [];
  const types = catalogEntry.propertyTypes || [];
  if (!type) return units.map((u) => eur(u.price));
  if (!types.includes(type)) return [];
  if (type === 'villa') {
    const onlyVillas = types.every((t) => t === 'villa');
    return units.filter((u) => onlyVillas || VILLA_LINE.test(u.floor || '')).map((u) => eur(u.price));
  }
  // apartment: apartments and penthouses; houses and villas in a mixed project are left out.
  const onlyFlats = types.every((t) => t === 'apartment' || t === 'penthouse');
  return units.filter((u) => onlyFlats || !HOUSE_LINE.test(u.floor || '')).map((u) => eur(u.price));
}

function answer(brief, active, catalog, rawBySlug) {
  const refinements = brief.refinements.filter((r) => active.includes(r.key));
  const budgetMax = Math.min(...refinements.map((r) => r.budgetMax || Infinity));
  const out = [];
  for (const p of catalog.projects) {
    if (!brief.match(p)) continue;
    const raw = rawBySlug.get(p.slug);
    if (!raw) continue;
    if (refinements.some((r) => r.keyReady) && p.status !== 'completed') continue;
    if (refinements.some((r) => r.privatePool)
      && !(p.features.includes('private_pool') && p.propertyTypes.every((t) => t === 'villa'))) continue;
    const homes = homesOfType(raw, p, brief.type);
    if (!homes.length) continue;
    const priced = homes.filter((n) => n != null);
    let fitting = priced;
    if (budgetMax !== Infinity) {
      fitting = priced.filter((n) => n <= budgetMax);
      // Homes "on request" with a published floor: judged by the floor, as the connector does.
      if (!fitting.length && !priced.length && p.priceMin != null && p.priceMin <= budgetMax
        && p.propertyTypes.length === 1) fitting = [p.priceMin];
      if (!fitting.length) continue;
    }
    out.push({ slug: p.slug, from: fitting.length ? Math.min(...fitting) : null, order: raw.card?.order ?? 999 });
  }
  // The brief's lead project (chosen as a representative first answer) goes first when it matches;
  // the rest follow the site's own card order.
  const rank = (x) => (x.slug === brief.lead ? -1 : x.order);
  return out.sort((a, b) => rank(a) - rank(b) || a.slug.localeCompare(b.slug));
}

// The catalogue's localized "From EUR 464,000" with the matching homes' lowest price put in place
// of the project's own floor, in the locale's spelling.
function fromLabel(entry, catalogEntry, value, locale) {
  const label = entry.from;
  if (!label || value == null || value === catalogEntry.priceMin) return label;
  const digits = (n) => n.toLocaleString('en-US');
  const fmt = PRICE_FORMAT[locale];
  const oldText = fmt ? fmt(digits(catalogEntry.priceMin)) : digits(catalogEntry.priceMin);
  const newText = fmt ? fmt(digits(value)) : digits(value);
  if (!label.includes(oldText)) {
    throw new Error(`ai.html preview: cannot place ${value} in "${label}" (${catalogEntry.slug}, ${locale})`);
  }
  return label.replace(oldText, newText);
}

function picture(src, alt, eager) {
  const local = src.replace(/^https:\/\/nuevaliving\.com\//, '');
  const stem = local.replace(/\.(jpe?g|png)$/i, '');
  const sizes = [[640, `${stem}-640.webp`], [960, `${stem}-960.webp`], [1920, `${stem}.webp`]]
    .filter(([, f]) => existsSync(f));
  const source = sizes.length
    ? `<source type="image/webp" srcset="${sizes.map(([w, f]) => `${f} ${w}w`).join(', ')}" sizes="(max-width: 860px) calc(100vw - 40px), 640px">`
    : '';
  return `<picture>${source}<img src="${local}" alt="${alt.replace(/"/g, '&quot;')}" width="1920" height="1080" ${eager ? 'fetchpriority="high"' : 'loading="lazy"'} decoding="async"></picture>`;
}

const esc = (s) => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

export function aiSearchPreview(projects, locale) {
  const catalog = buildMcpCatalog(projects);
  const rawBySlug = new Map(projects.map((p) => [p.slug, p]));
  const bySlug = new Map(catalog.projects.map((p) => [p.slug, p]));
  const areaName = (slug) => catalog.areas.find((a) => a.slug === slug)?.names?.[locale] || slug;

  const bank = [];
  const cards = new Map();
  const cardFor = (slug, value) => {
    const key = `${slug}:${value ?? ''}`;
    if (cards.has(key)) return cards.get(key).id;
    const p = bySlug.get(slug);
    const l = p.locales[locale] || p.locales.en;
    const img = (l.images || []).find((i) => i.url === p.image) || (l.images || [])[0] || { url: p.image, alt: l.name };
    const id = `r${cards.size}`;
    cards.set(key, { id, html: `<article class="ai-result" data-card="${id}"${cards.size ? ' hidden' : ''}>
          <a class="ai-result-media" href="property-${slug}.html" tabindex="-1" aria-hidden="true">${picture(p.image || img.url, img.alt || l.name, cards.size === 0)}</a>
          <div class="ai-result-body">
            <p class="ai-result-place">${esc(l.location)} &middot; ${esc(l.type)}</p>
            <h3 class="ai-result-name"><a href="property-${slug}.html">${esc(l.name)}</a></h3>
            <p class="ai-result-price">${esc(fromLabel(l, p, value, locale))}</p>
            ${l.delivery ? `<p class="ai-result-delivery"><span class="ai-result-key">Delivery</span> ${esc(l.delivery)}</p>` : ''}
            <a class="ai-result-link" href="property-${slug}.html">See the development</a>
          </div>
        </article>` });
    return id;
  };

  for (const brief of BRIEFS) {
    for (let mask = 0; mask < 4; mask += 1) {
      const active = [1, 2].filter((k) => mask & k);
      const found = answer(brief, active, catalog, rawBySlug);
      // A refinement that changes nothing would be a control that lies about doing something.
      const ids = found.map((f) => cardFor(f.slug, f.from));
      bank.push(`<span data-q="${brief.key}${mask}" data-cards="${ids.join(' ')}">${brief.questions[mask]}</span>`);
    }
  }
  // The first card printed is the initial answer, so it must be the first match for E0.
  const first = bank[0].match(/data-cards="([^" ]+)/);
  if (!first || first[1] !== 'r0') throw new Error('ai.html preview: the first brief has no match');

  const briefButtons = BRIEFS.map((b, i) => `<button type="button" class="ai-brief" data-brief="${b.key}" aria-pressed="${i === 0}">${b.label}</button>`).join('');
  const refineGroups = BRIEFS.map((b, i) => `<div class="ai-refine-set" data-for="${b.key}"${i ? ' hidden' : ''}>${b.refinements.map((r) => `<button type="button" class="ai-chip" data-r="${r.key}" aria-pressed="false"><span class="ai-chip-mark" aria-hidden="true"></span>${r.label}</button>`).join('')}</div>`).join('');

  return `<section class="section ai-try" id="try"><div class="section-inner">
    <div class="section-head"><span class="label">Try a Search</span><div class="rule"></div><h2 class="section-title">Pick a search, <em>then narrow it</em></h2></div>
    <div class="ai-try-grid">
      <div class="ai-try-ask">
        <div class="ai-controls ai-c-brief" data-js-only hidden>
          <p class="ai-control-label" id="ai-start-label">Start from</p>
          <div class="ai-briefs" role="group" aria-labelledby="ai-start-label">${briefButtons}</div>
        </div>
        <div class="ai-question">
          <p class="ai-control-label">Your question</p>
          <p class="ai-question-text" data-question aria-live="polite">${BRIEFS[0].questions[0]}</p>
        </div>
        <div class="ai-controls ai-c-refine" data-js-only hidden>
          <p class="ai-control-label" id="ai-refine-label">Narrow it</p>
          <div class="ai-refine" role="group" aria-labelledby="ai-refine-label">${refineGroups}</div>
        </div>
        <div class="ai-use">
          <a class="btn" href="#setup" data-use="chatgpt">Use this search in ChatGPT</a>
          <a class="btn ghost" href="#setup" data-use="claude">Use this search in Claude</a>
        </div>
        <p class="ai-note">A guided preview built from our project pages, not a live assistant. In ChatGPT or Claude, the answer comes from the same pages.</p>
      </div>
      <div class="ai-try-result">
        <div class="ai-stage" data-stage>${[...cards.values()].map((c) => c.html).join('')}
          <div class="ai-empty" data-empty hidden><p>Nothing on our pages matches all of that yet.</p><button type="button" class="ai-chip" data-broaden>Remove the last filter</button></div>
        </div>
        <div class="ai-result-nav" data-js-only hidden>
          <button type="button" class="ai-nav-btn" data-step="-1" aria-label="Previous match"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M15 5l-7 7 7 7"/></svg></button>
          <span class="ai-count" data-count dir="ltr">1 / 1</span>
          <button type="button" class="ai-nav-btn" data-step="1" aria-label="Next match"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M9 5l7 7-7 7"/></svg></button>
        </div>
        <p class="ai-qual">List prices before VAT and purchase costs, confirmed before any reservation. Images are mostly renders.</p>
      </div>
    </div>
    <div class="ai-bank" hidden>${bank.join('')}</div>
  </div></section>`;
}
