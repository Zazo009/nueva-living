import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const fontsDir = path.join(root, 'assets/fonts/google');
const remoteCssPath = path.join(fontsDir, 'liora-fonts.remote.css');
const localCssPath = path.join(fontsDir, 'liora-fonts.css');

const pages = [
  'nueva-living-home.html',
  'liora-about.html',
  'liora-access.html',
  'liora-advisory.html',
  'liora-approach.html',
  'liora-areas.html',
  'liora-cookie-policy.html',
  'liora-developments.html',
  'liora-legal-notice.html',
  'liora-privacy-policy.html',
  'property-altos-de-marbella.html',
];

if (!fs.existsSync(remoteCssPath)) {
  throw new Error(`Missing ${remoteCssPath}. Fetch the Google Fonts CSS first.`);
}

fs.mkdirSync(fontsDir, { recursive: true });

let css = fs.readFileSync(remoteCssPath, 'utf8');
const urls = [...new Set([...css.matchAll(/https:\/\/fonts\.gstatic\.com\/[^)]+\.woff2/g)].map((match) => match[0]))];

for (const url of urls) {
  const filename = path.basename(new URL(url).pathname);
  const target = path.join(fontsDir, filename);

  if (!fs.existsSync(target) || fs.statSync(target).size === 0) {
    execFileSync('curl', ['-L', url, '-o', target], { stdio: 'inherit' });
  }

  css = css.replaceAll(url, `./${filename}`);
}

css = `/* Self-hosted Nueva Living font package.
   Source families: Cinzel, Cormorant Garamond, Montserrat.
   Regenerate with scripts/self_host_fonts.mjs after refreshing liora-fonts.remote.css. */

${css}`;

fs.writeFileSync(localCssPath, css);

const googleFontsBlock = /\n\s*<link rel="preconnect" href="https:\/\/fonts\.googleapis\.com"\s*\/?>\n\s*<link rel="preconnect" href="https:\/\/fonts\.gstatic\.com" crossorigin\s*\/?>\n\s*<link href="https:\/\/fonts\.googleapis\.com\/css2\?family=Cinzel:wght@400;500;600&family=Cormorant\+Garamond:wght@300;400;500&family=Montserrat:wght@300;400;500&display=swap" rel="stylesheet"\s*\/?>/g;
const localFontsLink = '\n  <link rel="stylesheet" href="assets/fonts/google/liora-fonts.css">';

for (const page of pages) {
  const filePath = path.join(root, page);
  if (!fs.existsSync(filePath)) continue;

  const html = fs.readFileSync(filePath, 'utf8');
  const updated = html.replace(googleFontsBlock, localFontsLink);

  if (updated !== html) {
    fs.writeFileSync(filePath, updated);
  }
}

console.log(`Self-hosted ${urls.length} font files and updated ${pages.length} HTML files.`);
