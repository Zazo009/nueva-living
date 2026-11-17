// What the site itself says, as plain text, for the chat on the site (netlify/functions/nueva-chat.js).
//
// The chat answers questions about projects from the connector's catalogue (mcp-catalog.json) and
// everything else -- buying costs, the bank guarantee, areas, how the advisory works -- from the
// pages listed here. It reads only what is already published: the English page's <main>, with
// headings kept so the model can quote the right section, plus the page's address in each of the
// ten languages from its own hreflang links. Project pages are left out on purpose; the catalogue
// carries their facts in a shape the search can filter.
//
// build_dist.mjs writes the result to netlify/functions/data/site-knowledge.json, and the audit
// checks that file for every real project name and developer, as it checks the catalogue.
import fs from 'node:fs';
import path from 'node:path';

// Pages that answer nothing a buyer would ask, or whose content is the project list itself.
const SKIP = new Set([
  '404.html', 'thank-you.html', 'compare.html', 'developments.html', 'ai.html', 'cookie-policy.html',
  'nueva-living-home.html', 'index.html',
]);

const ENTITIES = {
  amp: '&', lt: '<', gt: '>', quot: '"', apos: "'", nbsp: ' ', euro: '€', middot: '·', ndash: '–',
  mdash: '—', rsquo: '’', lsquo: '‘', rdquo: '”', ldquo: '“', hellip: '…', times: '×', sup2: '²',
  deg: '°', aacute: 'á', eacute: 'é', iacute: 'í', oacute: 'ó', uacute: 'ú', ntilde: 'ñ', Aacute: 'Á',
  Eacute: 'É', Iacute: 'Í', Oacute: 'Ó', Uacute: 'Ú', Ntilde: 'Ñ', uuml: 'ü', ouml: 'ö', auml: 'ä',
  aring: 'å', oslash: 'ø', aelig: 'æ', ccedil: 'ç', egrave: 'è', agrave: 'à', rarr: '→', larr: '←',
  bull: '•', pound: '£', shy: '',
};

function decode(text) {
  return text
    .replace(/&#x([0-9a-f]+);/gi, (_, hex) => String.fromCodePoint(parseInt(hex, 16)))
    .replace(/&#(\d+);/g, (_, dec) => String.fromCodePoint(Number(dec)))
    .replace(/&([a-z0-9]+);/gi, (whole, name) => (name in ENTITIES ? ENTITIES[name] : whole));
}

function attr(tag, name) {
  const match = new RegExp(`${name}="([^"]*)"`, 'i').exec(tag);
  return match ? decode(match[1]) : '';
}

// <main> as text: headings on their own lines ("## "), blocks separated by line breaks.
function mainText(html) {
  const main = /<main[^>]*>([\s\S]*?)<\/main>/i.exec(html);
  if (!main) return '';
  return decode(main[1]
    .replace(/<(script|style|svg|noscript|template|form|button|select)[^>]*>[\s\S]*?<\/\1>/gi, ' ')
    .replace(/<h([1-4])[^>]*>/gi, (_, level) => `\n${'#'.repeat(Math.max(2, Number(level)))} `)
    .replace(/<\/h[1-4]>/gi, '\n')
    .replace(/<li[^>]*>/gi, '\n- ')
    .replace(/<(br|\/p|\/div|\/li|\/tr|\/article|\/section|\/dd|\/dt|\/summary|\/details)[^>]*>/gi, '\n')
    .replace(/<\/t[dh]>/gi, ' | ')
    .replace(/<[^>]+>/g, ' '))
    .replace(/[ \t ]+/g, ' ')
    .replace(/ *\n */g, '\n')
    .replace(/\n{2,}/g, '\n')
    .trim();
}

export function buildSiteKnowledge(root) {
  const pages = [];
  for (const file of fs.readdirSync(root).filter((name) => name.endsWith('.html')).sort()) {
    if (SKIP.has(file) || file.startsWith('property-')) continue;
    const html = fs.readFileSync(path.join(root, file), 'utf8');
    const urls = {};
    for (const tag of html.match(/<link[^>]+rel="alternate"[^>]*>/gi) || []) {
      const lang = attr(tag, 'hreflang');
      if (lang && lang !== 'x-default') urls[lang] = attr(tag, 'href');
    }
    // Only pages published in the site's languages: drafts and exports at the root have no hreflang.
    if (!urls.en) continue;
    const text = mainText(html);
    if (text.length < 400) continue;
    const title = decode((/<title>([\s\S]*?)<\/title>/i.exec(html) || [])[1] || '').replace(/\s+/g, ' ').trim();
    const description = attr((/<meta[^>]+name="description"[^>]*>/i.exec(html) || [''])[0], 'content');
    pages.push({ id: file.replace(/\.html$/, ''), title, description, urls, text });
  }
  return { pages };
}
