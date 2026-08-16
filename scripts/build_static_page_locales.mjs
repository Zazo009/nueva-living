// Generates locale variants of the three hand-authored static pages that
// no render-based build pass covers: compare.html, thank-you.html and
// 404.html. Same clone-and-replace approach as build_developments_locales:
// per-locale chrome + body entries (longest-first), language switcher on
// the English originals, per-locale head metadata and Arabic RTL assets.
// Runs after build_developments_locales.mjs, before build_dist.mjs.
import { existsSync, readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import path from 'node:path';
import {
  LOCALES,
  DEFAULT_LOCALE,
  localeMeta,
  isRtl,
  hreflangLinks,
  renderLanguageSwitcher,
  LANG_SWITCHER_SCRIPT,
  localizeInternalLinks
} from './lib/i18n.mjs';
import { CHROME_ENTRIES } from './lib/developments_page_translations.mjs';
import {
  THANK_YOU_ENTRIES,
  COMPARE_ENTRIES,
  NOT_FOUND_ENTRIES,
  COMPARE_RUNTIME_STRINGS
} from './lib/static_page_translations.mjs';

const root = process.cwd();
const siteUrl = 'https://nuevaliving.com';

// `noindex` matters here: thank-you.html and 404.html carry the tag in
// their own source, but compare.html gets it from build_dist's pageMeta --
// which locale clones bypass. Without it the five locale compare pages
// were indexable, thin, near-duplicate tool pages.
const PAGES = [
  { file: 'thank-you.html', entries: THANK_YOU_ENTRIES },
  { file: 'compare.html', entries: COMPARE_ENTRIES, compareRuntime: true, robots: 'noindex,follow' },
  { file: '404.html', entries: NOT_FOUND_ENTRIES }
];

function stripPriorInjections(html) {
  return html
    .replace(/\s*<details class="lang-switcher" data-lang-switcher>[\s\S]*?<\/details>\n?/g, '\n')
    .replace(/(<link rel="canonical"[^\n]*\n)(?:  <link rel="alternate"[^\n]*\n)*/, '$1')
    .replace(/(<meta name="description"[^\n]*\n)(?:  <link rel="alternate"[^\n]*\n)*/, '$1')
    .replace(/\s*<script>\n\s*document\.querySelectorAll\('\[data-lang-switcher\]'\)[\s\S]*?<\/script>\n/g, '\n');
}

function injectSwitcher(html, file, locale) {
  const switcher = renderLanguageSwitcher(file, locale);
  let next = html.replace(
    '<a href="contact.html">Contact Us</a>\n    </div>',
    `<a href="contact.html">Contact Us</a>\n      ${switcher}\n    </div>`
  );
  next = next.replace(
    '<a href="contact.html">Contact Us</a>\n  </div>',
    `<a href="contact.html">Contact Us</a>\n    ${switcher}\n  </div>`
  );
  return next.replace('</body>', `  ${LANG_SWITCHER_SCRIPT}\n</body>`);
}

// hreflang goes after canonical when the page has one, else after the
// meta description (compare.html carries no canonical).
//
// compare.html is noindex: it is a thin, near-duplicate tool page that only
// makes sense with your own shortlist in it. Annotating a noindex page with
// hreflang sends Google contradictory instructions -- "do not index this"
// alongside "here are its language equivalents" -- so the cluster is simply
// left off. The other two static pages keep theirs.
function injectHreflang(html, file) {
  if (file === 'compare.html') return html;
  const block = hreflangLinks(file, siteUrl);
  const canonical = `<link rel="canonical" href="${siteUrl}/${file}">`;
  if (html.includes(canonical)) {
    return html.replace(canonical, `${canonical}\n${block}`);
  }
  return html.replace(/(<meta name="description"[^\n]*)/, `$1\n${block}`);
}

const written = [];

for (const page of PAGES) {
  const sourcePath = path.join(root, page.file);
  if (!existsSync(sourcePath)) continue;
  const source = stripPriorInjections(readFileSync(sourcePath, 'utf8'));
  const sortedEntries = [...page.entries, ...CHROME_ENTRIES].sort((a, b) => b.find.length - a.find.length);

  for (const meta of LOCALES) {
    if (meta.code === DEFAULT_LOCALE) continue;
    const locale = meta.code;
    const localeUrl = `${siteUrl}/${meta.urlPrefix}/${page.file}`;
    let html = source;

    html = html.replace('<html lang="en">', `<html lang="${meta.htmlLang}" dir="${meta.dir}">`);
    html = html.replace(
      '<meta name="viewport" content="width=device-width, initial-scale=1">',
      '<meta name="viewport" content="width=device-width, initial-scale=1">\n  <base href="../">'
    );
    html = html.split(`<link rel="canonical" href="${siteUrl}/${page.file}">`)
      .join(`<link rel="canonical" href="${localeUrl}">`);
    html = html.split(`<meta property="og:url" content="${siteUrl}/${page.file}">`)
      .join(`<meta property="og:url" content="${localeUrl}">`);

    // hreflang (uses the locale-rewritten canonical as anchor when present).
    // compare.html is left out for the reason given on injectHreflang: it is
    // noindex, and annotating a noindex page with a language cluster gives
    // Google two contradictory instructions.
    const localeCanonical = `<link rel="canonical" href="${localeUrl}">`;
    if (page.file !== 'compare.html') {
      if (html.includes(localeCanonical)) {
        html = html.replace(localeCanonical, `${localeCanonical}\n${hreflangLinks(page.file, siteUrl)}`);
      } else {
        html = html.replace(/(<meta name="description"[^\n]*)/, `$1\n${hreflangLinks(page.file, siteUrl)}`);
      }
    }

    if (page.robots && !/<meta name="robots"/i.test(html)) {
      html = html.replace(
        /(<meta name="description"[^>]*>)/i,
        `$1\n  <meta name="robots" content="${page.robots}">`
      );
    }

    html = injectSwitcher(html, page.file, locale);

    for (const entry of sortedEntries) {
      const replacement = entry[locale];
      if (!replacement) continue;
      html = html.split(entry.find).join(replacement);
    }

    if (page.compareRuntime && COMPARE_RUNTIME_STRINGS[locale]) {
      const json = JSON.stringify(COMPARE_RUNTIME_STRINGS[locale]).replace(/'/g, '&#39;');
      html = html.replace(
        'id="compareRoot" data-compare-root>',
        `id="compareRoot" data-compare-root data-i18n='${json}'>`
      );
    }

    if (isRtl(locale)) {
      html = html.replace(
        '<link rel="stylesheet" href="assets/liora/liora-pages.css">',
        '<link rel="stylesheet" href="assets/liora/liora-pages.css">\n  <link rel="stylesheet" href="assets/liora/liora-rtl.css">'
      );
    }

    const outPath = path.join(root, meta.urlPrefix, page.file);
    mkdirSync(path.dirname(outPath), { recursive: true });
    html = localizeInternalLinks(html, locale);
    writeFileSync(outPath, html);
    written.push(`${meta.urlPrefix}/${page.file}`);
  }

  // English original: switcher + reciprocal hreflang, text untouched.
  let englishHtml = injectSwitcher(source, page.file, DEFAULT_LOCALE);
  englishHtml = injectHreflang(englishHtml, page.file);
  writeFileSync(sourcePath, englishHtml);
  written.push(`${page.file} (switcher + hreflang added)`);
}

console.log(JSON.stringify({ written }, null, 2));
