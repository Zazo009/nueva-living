// The two live figures the developments index quotes: how many projects it
// lists and the lowest guide price among them.
//
// They used to be resolved in build_dist.mjs for the English description only,
// so the nine translations of that sentence either carried no figure at all
// or -- in Arabic -- carried one typed in by hand ("30 projects, from
// 305,000") that went stale while the English beside it kept counting. Both
// builders now read the same list through the same function, and a
// translation quotes the figures the same way the English does: with the
// {count} and {minPrice} placeholders.
//
// {minPrice} resolves to the English spelling ("213,000"). A translation
// writes it after a euro sign ("€{minPrice}"), and the locale's own price
// convention is applied afterwards by localizeCardPrices() in prices.mjs, the
// pass every locale page already goes through -- so there is one table of
// price formats on the site, not a second one here.
import fs from 'node:fs';
import path from 'node:path';

// A project is published once its English page exists. This is the filter
// build_dist.mjs has always applied to the project list; it lives here so the
// locale builder cannot drift from it.
export function loadPublishedProjects(root) {
  const projectsDir = path.join(root, 'content/liora-projects');
  if (!fs.existsSync(projectsDir)) return [];
  return fs.readdirSync(projectsDir, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => path.join(projectsDir, entry.name, 'project.json'))
    .filter((file) => fs.existsSync(file))
    .map((file) => JSON.parse(fs.readFileSync(file, 'utf8')))
    .filter((project) => project.output && fs.existsSync(path.join(root, project.output)));
}

export function developmentsFacts(projects) {
  const prices = projects
    .map((project) => Number(project.discovery?.price))
    .filter((value) => Number.isFinite(value) && value > 0);
  return {
    count: projects.length,
    minPrice: prices.length ? Math.min(...prices) : null
  };
}

export function fillDevelopmentsFacts(text, { count, minPrice }) {
  return text
    .replace(/\{count\}/g, String(count))
    .replace(/\{minPrice\}/g, minPrice ? minPrice.toLocaleString('en-US') : '');
}
