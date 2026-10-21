// Data and renderer for guide-new-build-prices-costa-del-sol.html.
//
// Every figure on that page is computed here from content/liora-projects/*/project.json, at build
// time, and nowhere else. Only PUBLIC fields are read (name, slug, output, archived, discovery.*,
// hero.*, card.meta, availability.*). Nothing under `crm` is read: the real name and developer
// live there, and the page names projects by their public name only.
//
// The grouping follows the developments filter so this page cannot disagree with it:
//   area     discovery.area                        (the filter's data-area)
//   price    discovery.price                       (the filter's data-price and the card's amount)
//   delivery discovery.completionSort || the year/quarter in hero.delivery, a month folded to its
//            quarter and a bare year folded to Q4 -- the same fold as parseCompletion() in
//            assets/liora/liora-discovery.js and completionRank() in build_property_pages.mjs
//   ready    discovery.status says key ready / completed / resale (the filter's 'completed')
//
// Prices are formatted with PRICE_FORMAT from prices.mjs, the table the project pages use.
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { t, localizedPath, DEFAULT_LOCALE } from './i18n.mjs';
import { PRICE_FORMAT } from './prices.mjs';
import { MONTH_NAMES, localizeMonthDate } from './dates.mjs';
import { GUIDE_PRICES_COPY } from './guide_prices_translations.mjs';

export const PRICES_GUIDE_FILE = 'guide-new-build-prices-costa-del-sol.html';

const TYPE_ORDER = ['apartment', 'penthouse', 'villa', 'townhouse'];
const TYPE_TAG = { apartment: 'Apartments', penthouse: 'Penthouses', villa: 'Villas', townhouse: 'Townhouses' };
const AREA_KEY = {
  marbella: 'marbella', estepona: 'estepona', casares: 'casares', benahavis: 'benahavis',
  'nueva-andalucia': 'nuevaAndalucia', 'san-pedro-alcantara': 'sanPedroAlcantara',
  'mijas-fuengirola': 'mijasFuengirola', benalmadena: 'benalmadena', torremolinos: 'torremolinos'
};
const READY = /key ready|completed|resale/i;

const esc = (value) => String(value ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

// discovery.propertyTypes is free text ("Apartments/Penthouses", "Duplex Penthouse", "Villa").
// A duplex is counted with the apartments and a duplex penthouse with the penthouses.
export function normaliseTypes(list = []) {
  const found = new Set();
  for (const entry of list) {
    for (const part of String(entry).toLowerCase().split('/')) {
      if (/townhouse/.test(part)) found.add('townhouse');
      else if (/villa/.test(part)) found.add('villa');
      else if (/penthouse/.test(part)) found.add('penthouse');
      else if (/apartment|duplex/.test(part)) found.add('apartment');
    }
  }
  return TYPE_ORDER.filter((type) => found.has(type));
}

export function completionOf(project) {
  const discovery = project.discovery || {};
  if (READY.test(discovery.status || '')) return { kind: 'ready' };
  let year; let quarter; let precise = false;
  if (discovery.completionSort) {
    const [y, second] = String(discovery.completionSort).split('-').map(Number);
    if (y) {
      year = y;
      let q = second || 4;
      if (q > 4) q = Math.min(4, Math.ceil(q / 3));
      quarter = q;
      precise = Boolean(second);
    }
  } else {
    const text = String(project.hero?.delivery || '');
    const q = text.match(/Q([1-4])\s*(20\d{2})/i);
    if (q) { year = Number(q[2]); quarter = Number(q[1]); precise = true; }
    else {
      const y = text.match(/20\d{2}/);
      if (y) { year = Number(y[0]); quarter = 4; }
    }
  }
  return year ? { kind: 'dated', year, quarter, precise } : { kind: 'unconfirmed' };
}

// What the developer says about tax on the listed price: 'net' (excluded), 'gross' (included) or
// 'unstated'. Read conservatively from the price strings and the availability notes: a sentence
// that hedges ("may exclude") or reports a gap ("does not say whether") counts as nothing.
export function taxBasis(project) {
  const price = [project.card?.meta?.find((m) => m[0] === 'From')?.[1], project.hero?.startingPrice,
    project.availability?.startingPrice, project.availability?.priceRange].join(' ');
  if (/\+\s*(?:VAT|IVA)\b|\+\s*\d+%\s*ITP/i.test(price)) return 'net';
  const text = `${project.availability?.sourceNote || ''} ${project.availability?.copy || ''}`;
  let net = false; let gross = false;
  for (const sentence of text.split(/(?<=[.;])\s+/)) {
    if (!/\b(?:VAT|IVA|taxes|tax|ITP)\b/i.test(sentence)) continue;
    if (/not say|not state|not give|whether|may exclude|may change/i.test(sentence) && !/\bexclud/i.test(sentence.split(/may change/i)[0])) continue;
    if (/\bnet\b|exclud|without VAT|not include|plus (?:the )?(?:\d+% )?(?:VAT|IVA)|must be increased/i.test(sentence)) net = true;
    else if (/(?:prices?|price list|list)\s+(?:are\s+)?(?:include|inclusive)/i.test(sentence)) gross = true;
  }
  if (net && !gross) return 'net';
  if (gross && !net) return 'gross';
  return 'unstated';
}

function monthIndex(text) {
  const match = /([A-Z][a-z]+)\s+(\d{4})/.exec(String(text || ''));
  if (!match) return null;
  const month = Object.keys(MONTH_NAMES).indexOf(match[1]);
  return month < 0 ? null : { year: Number(match[2]), month, name: match[1], value: Number(match[2]) * 12 + month };
}

export function loadPriceProjects(rootDir = '.') {
  const dir = join(rootDir, 'content', 'liora-projects');
  const projects = [];
  const skipped = [];
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    if (!entry.isDirectory()) continue;
    const file = join(dir, entry.name, 'project.json');
    if (!existsSync(file)) continue;
    const p = JSON.parse(readFileSync(file, 'utf8'));
    const price = Number(p.discovery?.price);
    const area = p.discovery?.area;
    if (p.archived || !p.output || !Number.isFinite(price) || price <= 0 || !AREA_KEY[area]) {
      skipped.push(p.slug || entry.name);
      continue;
    }
    projects.push({
      slug: p.slug, name: p.name, output: p.output, area, price,
      types: normaliseTypes(p.discovery?.propertyTypes),
      completion: completionOf(p), tax: taxBasis(p), checked: monthIndex(p.availability?.checkedDate)
    });
  }
  projects.sort((a, b) => a.slug.localeCompare(b.slug));
  return { projects, skipped };
}

export function median(values) {
  const sorted = [...values].sort((a, b) => a - b);
  const mid = Math.floor(sorted.length / 2);
  return sorted.length % 2 ? sorted[mid] : Math.round((sorted[mid - 1] + sorted[mid]) / 2);
}

function priceStats(list) {
  const prices = list.map((p) => p.price);
  const low = list.reduce((a, b) => (b.price < a.price ? b : a));
  const high = list.reduce((a, b) => (b.price > a.price ? b : a));
  return { count: list.length, min: Math.min(...prices), median: median(prices), max: Math.max(...prices), lowProject: low, highProject: high };
}

const sortValue = (c) => c.year * 10 + c.quarter;

export function computePriceStats(projects) {
  const byArea = new Map();
  for (const p of projects) { if (!byArea.has(p.area)) byArea.set(p.area, []); byArea.get(p.area).push(p); }
  const areas = [...byArea.entries()]
    .map(([slug, list]) => {
      const dated = list.filter((p) => p.completion.kind === 'dated').map((p) => p.completion).sort((a, b) => sortValue(a) - sortValue(b));
      return {
        slug, list, ...priceStats(list),
        types: TYPE_ORDER.filter((type) => list.some((p) => p.types.includes(type))),
        ready: list.filter((p) => p.completion.kind === 'ready').length,
        first: dated[0], last: dated[dated.length - 1]
      };
    })
    .sort((a, b) => b.count - a.count || a.slug.localeCompare(b.slug));

  const groupKey = (p) => {
    const set = p.types;
    if (set.length && set.every((type) => type === 'apartment' || type === 'penthouse')) return set.join('+');
    if (set.length === 1) return set[0];
    return 'mixed';
  };
  const groupOrder = ['apartment', 'apartment+penthouse', 'penthouse', 'villa', 'townhouse', 'mixed'];
  const byGroup = new Map();
  for (const p of projects) { const key = groupKey(p); if (!byGroup.has(key)) byGroup.set(key, []); byGroup.get(key).push(p); }
  const groups = groupOrder.filter((key) => byGroup.has(key)).map((key) => ({ key, types: key === 'mixed' ? [] : key.split('+'), ...priceStats(byGroup.get(key)) }));
  const offered = TYPE_ORDER.map((type) => ({ type, count: projects.filter((p) => p.types.includes(type)).length })).filter((row) => row.count);

  const years = [...new Set(projects.filter((p) => p.completion.kind === 'dated').map((p) => p.completion.year))].sort();
  const delivery = [];
  const ready = projects.filter((p) => p.completion.kind === 'ready');
  if (ready.length) delivery.push({ key: 'ready', ...priceStats(ready) });
  for (const year of years) delivery.push({ key: String(year), year, ...priceStats(projects.filter((p) => p.completion.kind === 'dated' && p.completion.year === year)) });
  const unconfirmed = projects.filter((p) => p.completion.kind === 'unconfirmed');
  if (unconfirmed.length) delivery.push({ key: 'unconfirmed', ...priceStats(unconfirmed) });

  const checks = projects.map((p) => p.checked).filter(Boolean).sort((a, b) => a.value - b.value);
  return {
    total: projects.length, overall: priceStats(projects), areas, groups, offered, delivery,
    tax: { net: projects.filter((p) => p.tax === 'net').length, gross: projects.filter((p) => p.tax === 'gross').length, unstated: projects.filter((p) => p.tax === 'unstated').length },
    oldest: checks[0], newest: checks[checks.length - 1]
  };
}

// ---------------------------------------------------------------------------------------------
// Rendering
// ---------------------------------------------------------------------------------------------
const tags = JSON.parse(readFileSync(join(process.cwd(), 'content/i18n/tags.json'), 'utf8'));

function typeWord(type, locale, first) {
  const tag = TYPE_TAG[type];
  const word = locale === DEFAULT_LOCALE ? tag : tags[tag][locale];
  if (locale === 'de') return word;
  return first ? word : word.charAt(0).toLocaleLowerCase(locale) + word.slice(1);
}

function joinTypes(types, locale, copy) {
  const words = types.map((type, index) => typeWord(type, locale, index === 0));
  if (words.length < 2) return words.join('');
  if (words.length === 2) return locale === 'ar' ? `${words[0]} ${copy.and}${words[1]}` : `${words[0]} ${copy.and} ${words[1]}`;
  const head = words.slice(0, -1).join(copy.comma);
  const last = words[words.length - 1];
  return locale === 'ar' ? `${head} ${copy.and}${last}` : `${head} ${copy.and} ${last}`;
}

const money = (n, locale) => {
  const grouped = Number(n).toLocaleString('en-US');
  const text = locale === DEFAULT_LOCALE ? `€${grouped}` : PRICE_FORMAT[locale](grouped);
  return locale === 'ar' ? `<span dir="ltr">${text}</span>` : text;
};

const ROMAN = ['I', 'II', 'III', 'IV'];
const AR_ORDINAL = ['الأول', 'الثاني', 'الثالث', 'الرابع'];
function quarterLabel(c, locale) {
  if (!c.precise) return String(c.year);
  const q = c.quarter;
  switch (locale) {
    case 'es': case 'fr': return `T${q} ${c.year}`;
    case 'nl': case 'sv': case 'no': return `K${q} ${c.year}`;
    case 'ru': return `${q} кв. ${c.year}`;
    case 'pl': return `${ROMAN[q - 1]} kw. ${c.year}`;
    case 'ar': return `الربع ${AR_ORDINAL[q - 1]} ${c.year}`;
    default: return `Q${q} ${c.year}`;
  }
}

function areaName(slug, locale) { return esc(t(`area.${AREA_KEY[slug]}`, locale)); }
// The name is written as a token and put back by restoreProjectNames() after the translation pass,
// so no find/replace entry can rewrite part of it.
const projectLink = (p) => `<a href="${esc(p.output)}">§${p.slug}§</a>`;
// The page's own table styles go into <head> here, too: inside <main> a <style> block is a text node
// that is identical in all ten languages, which the untranslated-text guard reads as a missing
// translation.
export function restoreProjectNames(html, projects) {
  const byslug = new Map(projects.map((p) => [p.slug, p.name]));
  return html
    .replace(/§([a-z0-9-]+)§/g, (whole, slug) => (byslug.has(slug) ? esc(byslug.get(slug)) : whole))
    .replace('</head>', `  ${PRICES_STYLE}\n</head>`);
}
const fill = (text, vars) => Object.entries(vars).reduce((acc, [k, v]) => acc.replaceAll(`{${k}}`, v), text);
const monthText = (m, locale) => localizeMonthDate(`${m.name} ${m.year}`, locale);

function windowText(area, copy, locale) {
  const parts = [];
  if (area.first) {
    const a = quarterLabel(area.first, locale); const b = quarterLabel(area.last, locale);
    parts.push(a === b ? a : `${a} – ${b}`);
  }
  if (area.ready) parts.unshift(copy.readyNow);
  return parts.length ? parts.join(' · ') : copy.none;
}

export const PRICES_STYLE = `<style>
.np-wrap{overflow-x:auto;border-top:1px solid var(--line);margin:26px auto 0;max-width:1180px}
.np-table{width:100%;border-collapse:collapse;font-family:var(--ui-font,"Montserrat",Arial,sans-serif);font-size:13.5px;line-height:1.5;color:var(--ink)}
.np-table caption{caption-side:top;text-align:start;padding:12px 14px 0;font-size:11.5px;color:var(--muted)}
.np-table th,.np-table td{padding:13px 14px;border-bottom:1px solid var(--line);text-align:start;vertical-align:top}
.np-table thead th{font-size:10px;font-weight:500;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.np-table tbody th{font-weight:600}
.np-table td.n{font-variant-numeric:tabular-nums;white-space:nowrap}
.np-table td.n strong{font-weight:600;color:var(--bronze)}
.np-table small{display:block;margin-top:2px;font-size:11px;color:var(--muted);white-space:normal}
.np-table a{color:inherit;text-underline-offset:3px}
.np-note{max-width:900px;margin:16px auto 0;font-size:12px;line-height:1.6;color:var(--muted);text-align:center}
[lang="ar"] .np-table thead th{letter-spacing:0;text-transform:none}
</style>`;

function table({ caption, head, rows }) {
  return `<div class="np-wrap g-reveal"><table class="np-table"><caption>${esc(caption)}</caption><thead><tr>${head.map((h, i) => `<th scope="col">${esc(h)}</th>`).join('')}</tr></thead><tbody>
${rows.join('\n')}
</tbody></table></div>`;
}

const priceCell = (n, project, locale) => `<td class="n"><strong>${money(n, locale)}</strong><small>${projectLink(project)}</small></td>`;
const plainPrice = (n, locale) => `<td class="n">${money(n, locale)}</td>`;

function section(label, title, intro, inner, band = false) {
  return `<section class="section${band ? ' quiet-band' : ''}"><div class="section-inner">
    <div class="section-head center g-reveal"><span class="label">${label}</span><div class="rule"></div><h2 class="section-title">${title}</h2></div>
    ${intro ? `<p class="body-copy g-reveal">${intro}</p>` : ''}
    ${inner}
  </div></section>`;
}

export function renderPricesBody(locale, projects, stats = computePriceStats(projects)) {
  const copy = GUIDE_PRICES_COPY[locale] || GUIDE_PRICES_COPY[DEFAULT_LOCALE];
  const dash = ' – ';
  const typeLabel = (types) => joinTypes(types, locale, copy);

  // 1. how to read, key figures
  const o = stats.overall;
  const facts = `<div class="cards g-reveal">
      <article class="card"><h3>${stats.total}</h3><p>${esc(copy.factProjects)}</p></article>
      <article class="card"><h3>${money(o.median, locale)}</h3><p>${esc(copy.factMedian)}</p></article>
      <article class="card"><h3>${money(o.min, locale)}${dash}${money(o.max, locale)}</h3><p>${esc(copy.factRange)}</p></article>
    </div>`;
  const intro = `<section class="section"><div class="section-inner">
      <div class="guide-intro g-reveal">
        <div class="section-head center"><span class="label">${esc(copy.howLabel)}</span><div class="rule"></div><h2 class="section-title">${copy.howTitle}</h2></div>
        <p class="body-copy">${esc(copy.howP1)}</p>
        <p class="body-copy">${esc(copy.howP2)}</p>
      </div>
      ${facts}
      <div class="guide-cta-row" style="display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin-top:26px;">
        <a class="btn" href="contact.html#contact-form">${esc(copy.ctaAsk)}</a>
        <a class="btn ghost" href="developments.html">${esc(copy.ctaBrowse)}</a>
      </div>
    </div></section>`;

  // 2. by area
  const areaRows = stats.areas.map((a) => `<tr><th scope="row"><a href="${esc(`area-${a.slug}.html`)}">${areaName(a.slug, locale)}</a></th><td class="n">${a.count}</td>${priceCell(a.min, a.lowProject, locale)}${plainPrice(a.median, locale)}${priceCell(a.max, a.highProject, locale)}<td>${esc(typeLabel(a.types))}</td><td class="n">${esc(windowText(a, copy, locale))}</td></tr>`);
  const areaTable = table({ caption: copy.areaCaption, head: [copy.thArea, copy.thProjects, copy.thLowest, copy.thMedian, copy.thHighest, copy.thTypes, copy.thWindow], rows: areaRows })
    + `<p class="np-note g-reveal">${esc(copy.areaNote)}</p>`;
  const byArea = section(esc(copy.areaLabel), copy.areaTitle, esc(copy.areaIntro), areaTable);

  // 3. by type of home
  const typeRows = stats.groups.map((g) => `<tr><th scope="row">${esc(g.key === 'mixed' ? copy.mixed : typeLabel(g.types))}</th><td class="n">${g.count}</td>${priceCell(g.min, g.lowProject, locale)}${plainPrice(g.median, locale)}${priceCell(g.max, g.highProject, locale)}</tr>`);
  const offered = stats.offered.map((row) => `${esc(typeWord(row.type, locale, true))} ${row.count}`).join(' · ');
  const typeTable = table({ caption: copy.typeCaption, head: [copy.thType, copy.thProjects, copy.thLowest, copy.thMedian, copy.thHighest], rows: typeRows })
    + `<p class="np-note g-reveal">${esc(copy.typeOffered)}: ${offered}</p>`;
  const byType = section(esc(copy.typeLabel), copy.typeTitle, esc(copy.typeIntro), typeTable);

  // 4. by delivery year
  const yearRows = stats.delivery.map((d) => {
    const label = d.key === 'ready' ? copy.readyNow : d.key === 'unconfirmed' ? copy.unconfirmed : String(d.year);
    return `<tr><th scope="row">${esc(label)}</th><td class="n">${d.count}</td>${priceCell(d.min, d.lowProject, locale)}${plainPrice(d.median, locale)}</tr>`;
  });
  const byYear = section(esc(copy.yearLabel), copy.yearTitle, esc(copy.yearIntro),
    table({ caption: copy.yearCaption, head: [copy.thDelivery, copy.thProjects, copy.thLowest, copy.thMedian], rows: yearRows }));

  // 5. every project
  const areaOrder = new Map(stats.areas.map((a, i) => [a.slug, i]));
  const listed = [...projects].sort((a, b) => areaOrder.get(a.area) - areaOrder.get(b.area) || a.price - b.price || a.slug.localeCompare(b.slug));
  const taxLabel = { net: copy.taxNet, gross: copy.taxGross, unstated: copy.taxNone };
  const listRows = listed.map((p) => {
    const c = p.completion;
    const when = c.kind === 'ready' ? copy.readyNow : c.kind === 'dated' ? quarterLabel(c, locale) : copy.none;
    return `<tr><th scope="row">${projectLink(p)}</th><td>${areaName(p.area, locale)}</td>${plainPrice(p.price, locale)}<td>${esc(taxLabel[p.tax])}</td><td>${esc(typeLabel(p.types))}</td><td class="n">${esc(when)}</td></tr>`;
  });
  const list = section(esc(copy.listLabel), copy.listTitle, esc(copy.listIntro),
    table({ caption: copy.listCaption, head: [copy.thProject, copy.thArea, copy.thFrom, copy.thTax, copy.thTypes, copy.thDelivery], rows: listRows }));

  // 6. method
  const vars = {
    net: String(stats.tax.net), gross: String(stats.tax.gross), none: String(stats.tax.unstated),
    oldest: stats.oldest ? monthText(stats.oldest, locale) : '', newest: stats.newest ? monthText(stats.newest, locale) : ''
  };
  const method = ['m1', 'm2', 'm3', 'm4', 'm5', 'm6', 'm7'].map((key) => {
    const extra = key === 'm3' ? `<p><a href="guide-purchase-costs-andalucia.html">${esc(copy.costsLink)}</a></p>` : '';
    return `<div class="guide-compare-row"><div class="guide-compare-label">${esc(copy[`${key}l`])}</div><div><p>${esc(fill(copy[`${key}t`], vars))}</p>${extra}</div></div>`;
  }).join('\n        ');
  const methodSection = section(esc(copy.methodLabel), copy.methodTitle, '', `<div class="guide-compare-grid g-reveal">
        ${method}
      </div>`);

  // 7. FAQ
  const villa = stats.groups.find((g) => g.key === 'villa');
  const apartment = stats.groups.find((g) => g.key === 'apartment');
  const a2 = villa && apartment && villa.count >= 3 && apartment.count >= 3
    ? fill(esc(copy.a2), { villa: money(villa.median, locale), apt: money(apartment.median, locale) })
    : esc(copy.a2fb);
  const answers = [esc(copy.a1), a2, esc(copy.a3), esc(fill(copy.a4, vars))];
  const faq = [1, 2, 3, 4].map((n, i) => `<details class="segment-faq-item"${i === 0 ? ' open' : ''}>
        <summary>${esc(copy[`q${n}`])}</summary>
        <p>${answers[i]}</p>
      </details>`).join('\n      ');
  const faqSection = `<section class="section segment-faq-section"><div class="section-inner">
    <div class="section-head"><span class="label">Common Questions</span><div class="rule"></div><h2 class="section-title">${copy.faqTitle}</h2></div>
    <div class="segment-faq-list">
      ${faq}
    </div>
  </div></section>`;

  return [intro, byArea, byType, byYear, list, methodSection, faqSection].join('\n  ');
}

// schema.org Dataset for the tables, written after the translation pass so no token in it can be
// rewritten (see the note on withFaqSchema in build_footer_pages.mjs).
export function datasetSchemaJson({ locale, name, description, url, stats }) {
  return JSON.stringify({
    '@context': 'https://schema.org',
    '@type': 'Dataset',
    '@id': `${url}#dataset`,
    name,
    description,
    url,
    inLanguage: locale === 'ar' ? 'ar' : locale,
    isAccessibleForFree: true,
    keywords: ['Costa del Sol', 'new-build', 'off-plan', 'prices'],
    spatialCoverage: { '@type': 'Place', name: 'Costa del Sol, Spain' },
    creator: { '@id': 'https://nuevaliving.com/#organization' },
    publisher: { '@id': 'https://nuevaliving.com/#organization' },
    variableMeasured: ['Number of current projects', 'Lowest from price (EUR)', 'Median from price (EUR)', 'Highest from price (EUR)', 'Home types', 'Delivery quarter or year'],
    size: `${stats.total} projects`
  }, null, 2);
}
