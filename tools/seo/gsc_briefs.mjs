// Turns a Search Console export into a ranked list of content briefs. Run by hand, not from the build:
//
//   node tools/seo/gsc_briefs.mjs <Queries.csv> [<Pages.csv>]
//
// In Search Console: Performance > Search results > set the date range (16 months) > Export > Download
// CSV. The queries file has the columns Query/Clicks/Impressions/CTR/Position (Swedish: Mest populära
// frågor/Klick/Visningar/CTR/Position). The pages file is optional and only used to flag pages that
// already rank for nothing.
//
// What it does: scores every query by the clicks it would gain if the page reached the typical click rate
// for its position, matches the query to the closest existing page, and says what kind of work it is:
// rewrite a title, deepen a page, or write something new. It never writes copy and never publishes.
// Facts for any draft come from content/liora-projects and content/nueva-areas.json, not from here.
import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..', '..');
const [queriesFile, pagesFile] = process.argv.slice(2);
if (!queriesFile) {
  console.error('usage: node tools/seo/gsc_briefs.mjs <Queries.csv> [<Pages.csv>]');
  process.exit(1);
}

// Typical organic click rate by average position (rounded industry curve; only used to rank, not to promise).
const CTR_BY_POSITION = [0, 0.28, 0.15, 0.10, 0.07, 0.05, 0.04, 0.03, 0.025, 0.02, 0.018];
const expectedCtr = (position) => {
  const p = Math.round(position);
  if (p < 1) return CTR_BY_POSITION[1];
  if (p <= 10) return CTR_BY_POSITION[p];
  return Math.max(0.004, 0.018 - (p - 10) * 0.0007);
};

// Search Console writes the delimiter and the decimal mark of the account's locale: "1,4 %" and ";" in Swedish.
function parseCsv(text) {
  const lines = text.replace(/^﻿/, '').split(/\r?\n/).filter((l) => l.trim());
  const delimiter = (lines[0].match(/;/g) || []).length > (lines[0].match(/,/g) || []).length ? ';' : ',';
  const split = (line) => {
    const cells = [];
    let cur = '';
    let quoted = false;
    for (const ch of line) {
      if (ch === '"') quoted = !quoted;
      else if (ch === delimiter && !quoted) { cells.push(cur); cur = ''; }
      else cur += ch;
    }
    cells.push(cur);
    return cells.map((c) => c.trim());
  };
  const header = split(lines[0]);
  return lines.slice(1).map((line) => Object.fromEntries(split(line).map((c, i) => [header[i], c])));
}
const num = (value) => Number(String(value ?? '').replace(/\s|%/g, '').replace(',', '.')) || 0;
const pick = (row, names) => row[Object.keys(row).find((k) => names.includes(k.toLowerCase()))];

const queries = parseCsv(fs.readFileSync(queriesFile, 'utf8')).map((row) => ({
  query: pick(row, ['query', 'top queries', 'mest populära frågor', 'vanligaste frågorna', 'frågor', 'söka efter']),
  clicks: num(pick(row, ['clicks', 'klick'])),
  impressions: num(pick(row, ['impressions', 'visningar', 'exponeringar'])),
  position: num(pick(row, ['position', 'average position', 'genomsnittlig position'])),
})).filter((q) => q.query);

// The site's own pages, by title and file name. Built pages at the repo root are the English set.
const LOCALES = ['es', 'fr', 'de', 'ru', 'ar', 'nl', 'pl', 'sv', 'no'];
const pageFiles = [
  ...fs.readdirSync(root).filter((f) => /\.html$/.test(f) && !/^(404|thank-you)/.test(f)),
  ...LOCALES.flatMap((l) => (fs.existsSync(path.join(root, l)) ? fs.readdirSync(path.join(root, l)).filter((f) => /\.html$/.test(f)).map((f) => `${l}/${f}`) : [])),
];
const hasDist = fs.existsSync(path.join(root, 'dist'));
// Only pages that are really published: a gitignored scratch file at the root is not in dist/.
const published = pageFiles.filter((f) => !hasDist || fs.existsSync(path.join(root, 'dist', f)));
const pages = published.map((file) => {
  const html = fs.readFileSync(path.join(root, file), 'utf8');
  const title = (html.match(/<title>(.*?)<\/title>/s) || [, ''])[1];
  return { file, title, tokens: tokenise(`${file.replace(/\.html$/, '').replace(/[-/]/g, ' ')} ${title}`) };
});
function tokenise(text) {
  return new Set(text.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').split(/[^a-z0-9]+/).filter((t) => t.length > 2));
}
function bestPage(query) {
  const q = tokenise(query);
  let best = null;
  for (const page of pages) {
    const hit = [...q].filter((t) => page.tokens.has(t)).length;
    const score = q.size ? hit / q.size : 0;
    if (!best || score > best.score) best = { ...page, score };
  }
  return best;
}

const brand = /nueva\s?living|nuevaliving/i;
const rows = queries
  .filter((q) => !brand.test(q.query) && q.impressions >= 20)
  .map((q) => {
    const ctr = q.clicks / (q.impressions || 1);
    const gain = Math.max(0, expectedCtr(q.position) - ctr) * q.impressions;
    const page = bestPage(q.query);
    let action;
    if (q.position <= 10) action = 'Rewrite the title and meta description of the page; the ranking is there, the click is not.';
    else if (page && page.score >= 0.5) action = `Deepen ${page.file}: add the missing facts, internal links and a short FAQ for this query.`;
    else action = 'No page answers this: write a new guide or area page from our own project data.';
    return { ...q, ctr, gain, page, action };
  })
  .filter((r) => r.position >= 4 && r.position <= 40)
  .sort((a, b) => b.gain - a.gain)
  .slice(0, 25);

const today = new Date().toISOString().slice(0, 10);
const out = [`# Content briefs from Search Console, ${today}`, '',
  `${queries.length} queries read; ${rows.length} ranked by clicks to gain. Gain assumes the page reaches the usual click rate for its position; it ranks the work, it does not forecast traffic.`, ''];
rows.forEach((r, i) => {
  out.push(`## ${i + 1}. ${r.query}`,
    `- Impressions ${r.impressions}, clicks ${r.clicks}, CTR ${(r.ctr * 100).toFixed(1)}%, average position ${r.position.toFixed(1)}, gain about ${r.gain.toFixed(1)} clicks`,
    `- Closest page: ${r.page ? `${r.page.file} (${Math.round(r.page.score * 100)}% of the words match)` : 'none'}`,
    `- Work: ${r.action}`,
    '- Grounding: write only from content/liora-projects and content/nueva-areas.json; name both figures where two sources disagree; no developer names the site keeps anonymous.', '');
});
if (pagesFile) {
  const ranked = new Set(parseCsv(fs.readFileSync(pagesFile, 'utf8')).map((r) => Object.values(r)[0]));
  out.push(`Pages export read: ${ranked.size} pages have any impressions.`, '');
}
const outDir = path.join(root, 'tools', 'seo', 'out');
fs.mkdirSync(outDir, { recursive: true });
const file = path.join(outDir, `briefs-${today}.md`);
fs.writeFileSync(file, out.join('\n'));
console.log(`${rows.length} briefs written to ${path.relative(root, file)}`);
