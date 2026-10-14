// Files and hints that let AI assistants and answer engines find and quote the site
// correctly: llms.txt and llms-full.txt, the robots.txt groups for assistant crawlers,
// and the IndexNow key. All of it is generated from the same public data as the pages
// (the public catalogue, each project's public description and the area guides), never
// from the `crm` block, so the developer's own name cannot reach it. A guard in
// audit_site_consistency.mjs checks that.
import fs from 'node:fs';
import path from 'node:path';

// IndexNow asks the site to prove it owns the URLs it submits: a file named after
// the key, at the site root, containing the key. The key is not a secret.
export const INDEXNOW_KEY = '5e0b8a3f7c4d42f19a6e2d1b0c9f8a37';

// Crawlers that fetch pages for assistants and answer engines, and the ones that
// collect text to train models. Naming them states the intent explicitly: the site
// wants to be found and quoted.
const ASSISTANT_AGENTS = [
  'OAI-SearchBot', 'ChatGPT-User', 'GPTBot',
  'Claude-SearchBot', 'Claude-User', 'ClaudeBot',
  'PerplexityBot', 'Perplexity-User',
  'Google-Extended', 'Applebot-Extended', 'Applebot', 'Bingbot', 'CCBot'
];

export function robotsTxt(siteUrl) {
  const groups = ASSISTANT_AGENTS.map((agent) => `User-agent: ${agent}\nAllow: /\n`).join('\n');
  return `User-agent: *\nAllow: /\n\n${groups}\nSitemap: ${siteUrl}/sitemap.xml\n`;
}

const clean = (value) => String(value ?? '').replace(/\s+/g, ' ').trim();

const AREA_LABELS = {
  marbella: 'Marbella',
  estepona: 'Estepona',
  casares: 'Casares',
  benahavis: 'Benahavís',
  'nueva-andalucia': 'Nueva Andalucía',
  'san-pedro-alcantara': 'San Pedro de Alcántara',
  'mijas-fuengirola': 'Mijas & Fuengirola',
  benalmadena: 'Benalmádena',
  torremolinos: 'Torremolinos'
};

const STATUS_LABELS = {
  off_plan: 'off-plan',
  under_construction: 'under construction',
  completed: 'completed'
};

function money(value) {
  return value ? `EUR ${Number(value).toLocaleString('en-GB')}` : '';
}

function priceRange(p) {
  if (!p.priceMin) return 'price on request';
  return p.priceMax && p.priceMax !== p.priceMin
    ? `from ${money(p.priceMin)} to ${money(p.priceMax)}`
    : `from ${money(p.priceMin)}`;
}

function bedrooms(p) {
  if (!p.bedroomsMin) return '';
  return p.bedroomsMax && p.bedroomsMax !== p.bedroomsMin
    ? `${p.bedroomsMin} to ${p.bedroomsMax} bedrooms`
    : `${p.bedroomsMin} bedrooms`;
}

function titleOf(file) {
  const html = fs.readFileSync(file, 'utf8');
  const match = /<title>([^<]*)<\/title>/.exec(html);
  return clean(match?.[1]).replace(/\s*\|\s*Nueva Living$/i, '');
}

// projects: the public catalogue (assets/liora/data/projects-catalog.json), each entry
// joined with the public `description` of its project.json.
export function buildLlms({ siteUrl, dist, projects, areas }) {
  const url = (rel) => `${siteUrl}/${String(rel).replace(/^\//, '')}`;
  const guides = fs.readdirSync(dist)
    .filter((name) => /^guide-.*\.html$/.test(name))
    .sort()
    .map((name) => ({ name, title: titleOf(path.join(dist, name)) }));
  const areaPages = areas
    .map((area) => ({ slug: area.slug, name: AREA_LABELS[area.slug] || area.name, output: area.output }))
    .filter((area) => fs.existsSync(path.join(dist, area.output)));
  const byArea = new Map();
  for (const project of projects) {
    const key = project.area || 'other';
    if (!byArea.has(key)) byArea.set(key, []);
    byArea.get(key).push(project);
  }

  const summary = 'Nueva Living is a private new-build and off-plan property advisory based in Marbella, Spain. '
    + 'It works only with new developments on the Costa del Sol, from Torremolinos to Casares, and helps international buyers '
    + 'compare projects, understand prices and payment terms, and shortlist homes. The site is published in English, Spanish, '
    + 'French, German, Russian, Arabic, Dutch, Polish, Norwegian and Swedish.';

  const head = [
    '# Nueva Living',
    '',
    `> ${summary}`,
    '',
    `Prices and availability on this site are the developers' own list prices at the date shown on each page. Each page says what the price includes, and prices should be confirmed with the developer before any reservation. Images of unbuilt homes are computer-generated illustrations.`,
    '',
    '## About',
    '',
    `- [About Nueva Living](${url('about.html')}): who runs it, what it does and how to get in touch`,
    `- [Advisory](${url('advisory.html')}): how Nueva Living helps a buyer from first search to completion`,
    `- [Contact](${url('contact.html')}): email, phone and WhatsApp`,
    '',
    '## Search',
    '',
    `- [All developments](${url('developments.html')}): ${projects.length} current projects with filters for location, price, bedrooms, status and lifestyle, and a map view`,
    `- [Areas](${url('areas.html')}): the Costa del Sol areas covered, with local price levels and what each area is like`,
    ''
  ];

  const areaLines = ['## Areas', ''];
  for (const area of areaPages) {
    const count = (byArea.get(area.slug) || []).length;
    areaLines.push(`- [${area.name}](${url(area.output)}): area guide${count ? `; ${count} current developments` : ''}`);
  }
  areaLines.push('');

  const guideLines = ['## Buying guides', ''];
  for (const guide of guides) guideLines.push(`- [${guide.title}](${url(guide.name)})`);
  guideLines.push('');

  const projectLines = ['## Developments', ''];
  for (const [slug, list] of [...byArea.entries()].sort((a, b) => (AREA_LABELS[a[0]] || a[0]).localeCompare(AREA_LABELS[b[0]] || b[0]))) {
    projectLines.push(`### ${AREA_LABELS[slug] || slug}`, '');
    for (const p of list.sort((a, b) => a.name.localeCompare(b.name))) {
      const facts = [bedrooms(p), priceRange(p), STATUS_LABELS[p.constructionStatus], p.deliveryDate ? `delivery ${p.deliveryDate}` : ''].filter(Boolean).join('; ');
      projectLines.push(`- [${p.name}](${url(p.url)}): ${clean(p.location)}. ${facts}.`);
    }
    projectLines.push('');
  }

  const optional = [
    '## Optional',
    '',
    `- [Full catalogue in one file](${url('llms-full.txt')}): every development with its facts and description`,
    `- [Sitemap](${url('sitemap.xml')})`,
    ''
  ];
  const llms = [...head, ...areaLines, ...guideLines, ...projectLines, ...optional].join('\n');

  const full = [
    '# Nueva Living: full catalogue',
    '',
    `> ${summary}`,
    '',
    `This file lists every current development on ${siteUrl} with the facts a buyer asks first. Each page carries the details, floorplans, payment terms and an enquiry form. Figures are the developers' list prices at the date shown on the page.`,
    ''
  ];
  for (const [slug, list] of [...byArea.entries()].sort((a, b) => (AREA_LABELS[a[0]] || a[0]).localeCompare(AREA_LABELS[b[0]] || b[0]))) {
    full.push(`## ${AREA_LABELS[slug] || slug}`, '');
    for (const p of list.sort((a, b) => a.name.localeCompare(b.name))) {
      full.push(`### ${p.name}`, '');
      full.push(`- Page: ${url(p.url)}`);
      full.push(`- Location: ${clean(p.location)}`);
      if (p.propertyTypes?.length) full.push(`- Types: ${p.propertyTypes.join(', ')}`);
      if (bedrooms(p)) full.push(`- Bedrooms: ${bedrooms(p)}`);
      full.push(`- Price: ${priceRange(p)}`);
      if (p.totalUnits) full.push(`- Homes: ${p.availableUnits ?? 'n/a'} listed of ${p.totalUnits}`);
      if (p.constructionStatus) full.push(`- Status: ${STATUS_LABELS[p.constructionStatus] || p.constructionStatus}`);
      if (p.deliveryDate) full.push(`- Delivery: ${p.deliveryDate}`);
      if (p.amenities?.length) full.push(`- Amenities: ${p.amenities.join(', ')}`);
      if (p.description) full.push('', clean(p.description));
      full.push('');
    }
  }
  return { llms, full: `${full.join('\n')}\n` };
}
