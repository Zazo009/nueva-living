// Generates locale variants of developments.html (es/developments.html,
// fr/, de/, ru/, ar/) and adds the language switcher + reciprocal hreflang
// to the English original. Runs AFTER build_property_pages.mjs (which
// regenerates the page's project-card grid) and BEFORE build_dist.mjs
// (which picks any existing <locale>/developments.html up automatically).
//
// Same clone-and-replace approach as build_homepage_locales.mjs: the page
// is hand-authored English HTML plus generated card markup, so each locale
// gets chrome swaps, a literal find/replace pass over the page copy
// (DEVELOPMENTS_PAGE_ENTRIES), a tag-vocabulary pass over filter pills and
// card chips (TAG_LABELS), per-project card descriptions from each
// project.json's own i18n overlay, and data-i18n-* attributes feeding
// liora-discovery.js's runtime strings. Untranslated strings keep English.
import { existsSync, readFileSync, writeFileSync, mkdirSync, readdirSync } from 'node:fs';
import path from 'node:path';
import {
  LOCALES,
  DEFAULT_LOCALE,
  localeMeta,
  isRtl,
  hreflangLinks,
  renderLanguageSwitcher,
  LANG_SWITCHER_SCRIPT
} from './lib/i18n.mjs';
import {
  DEVELOPMENTS_PAGE_ENTRIES,
  TAG_LABELS,
  SHOW_IMAGE_TEMPLATES,
  DISCOVERY_RUNTIME_STRINGS
} from './lib/developments_page_translations.mjs';

const root = process.cwd();
const sourcePath = path.join(root, 'developments.html');
if (!existsSync(sourcePath)) {
  console.log('developments.html not found, skipping developments locale build.');
  process.exit(0);
}

const siteUrl = 'https://nuevaliving.com';

// Idempotency: remove anything this script previously injected into the
// English source so re-running never compounds duplicates.
function stripPriorInjections(html) {
  return html
    .replace(/\s*<details class="lang-switcher" data-lang-switcher>[\s\S]*?<\/details>\n?/g, '\n')
    .replace(/(<link rel="canonical"[^\n]*\n)(?:  <link rel="alternate"[^\n]*\n)*/, '$1')
    .replace(/\s*<script>\n\s*document\.querySelectorAll\('\[data-lang-switcher\]'\)[\s\S]*?<\/script>\n/g, '\n');
}

const source = stripPriorInjections(readFileSync(sourcePath, 'utf8'));

function injectSwitcher(html, locale) {
  const switcher = renderLanguageSwitcher('developments.html', locale);
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

function applyTagLabels(html, locale) {
  let next = html;
  for (const [en, translations] of Object.entries(TAG_LABELS)) {
    const translated = translations[locale];
    if (!translated || translated === en) continue;
    // Filter pills: visible label only; data-filter matching value stays English.
    next = next.split(`data-filter="${en}">${en}</button>`).join(`data-filter="${en}">${translated}</button>`);
  }
  // Card tag chips, scoped to .project-tags divs so <span>...</span>
  // elsewhere (meta labels, etc.) can never be hit.
  next = next.replace(/(<div class="project-tags">)([\s\S]*?)(<\/div>)/g, (whole, open, inner, close) => {
    const mapped = inner.replace(/<span>([\s\S]*?)<\/span>/g, (m, text) => {
      const translated = TAG_LABELS[text]?.[locale];
      return translated ? `<span>${translated}</span>` : m;
    });
    return `${open}${mapped}${close}`;
  });
  return next;
}

function applyCardDescriptions(html, locale) {
  const projectsDir = path.join(root, 'content/liora-projects');
  if (!existsSync(projectsDir)) return html;
  let next = html;
  for (const slug of readdirSync(projectsDir)) {
    const projectPath = path.join(projectsDir, slug, 'project.json');
    if (!existsSync(projectPath)) continue;
    const project = JSON.parse(readFileSync(projectPath, 'utf8'));
    const en = project.card?.description || project.description;
    const translated = project.i18n?.[locale]?.card?.description;
    if (!en || !translated || en === translated) continue;
    next = next.split(`<p>${en}</p>`).join(`<p>${translated}</p>`);
  }
  return next;
}

function applyDiscoveryRuntimeStrings(html, locale) {
  const strings = DISCOVERY_RUNTIME_STRINGS[locale];
  if (!strings) return html;
  const attrs = [
    ['data-i18n-count-one', strings.countOne],
    ['data-i18n-count-many', strings.countMany],
    ['data-i18n-no-filters', strings.noFilters],
    ['data-i18n-any-price', strings.anyPrice],
    ['data-i18n-any', strings.any],
    ['data-i18n-searching', strings.searching],
    ['data-i18n-search', strings.search],
    ['data-i18n-ai-matching', strings.aiMatching],
    ['data-i18n-ai-no-match', strings.aiNoMatch],
    ['data-i18n-ai-error', strings.aiError]
  ].map(([name, value]) => `${name}="${value}"`).join(' ');
  return html.replace(
    'id="development-discovery" data-discovery>',
    `id="development-discovery" data-discovery ${attrs}>`
  );
}

const written = [];

for (const meta of LOCALES) {
  if (meta.code === DEFAULT_LOCALE) continue;
  const locale = meta.code;
  const localeUrl = `${siteUrl}/${meta.urlPrefix}/developments.html`;
  let html = source;

  html = html.replace('<html lang="en">', `<html lang="${meta.htmlLang}" dir="${meta.dir}">`);
  html = html.replace(
    '<meta name="viewport" content="width=device-width, initial-scale=1">',
    '<meta name="viewport" content="width=device-width, initial-scale=1">\n  <base href="../">'
  );
  // Canonical / OG / JSON-LD URLs point at this locale's own page.
  html = html.split(`<link rel="canonical" href="${siteUrl}/developments.html">`)
    .join(`<link rel="canonical" href="${localeUrl}">`);
  html = html.split(`<meta property="og:url" content="${siteUrl}/developments.html">`)
    .join(`<meta property="og:url" content="${localeUrl}">`);
  html = html.split(`"url": "${siteUrl}/developments.html"`).join(`"url": "${localeUrl}"`);
  html = html.replace('<meta property="og:locale" content="en_US">', `<meta property="og:locale" content="${meta.htmlLang}">`);

  // Reciprocal hreflang after the canonical tag.
  html = html.replace(
    `<link rel="canonical" href="${localeUrl}">`,
    `<link rel="canonical" href="${localeUrl}">\n${hreflangLinks('developments.html', siteUrl)}`
  );

  // Language switcher (desktop nav + mobile menu) before text translation,
  // while the English anchors are still literal.
  html = injectSwitcher(html, locale);

  // Page copy, filter UI, cards, footer.
  for (const entry of DEVELOPMENTS_PAGE_ENTRIES) {
    const replacement = entry[locale];
    if (!replacement) continue;
    html = html.split(entry.find).join(replacement);
  }
  html = applyTagLabels(html, locale);
  html = applyCardDescriptions(html, locale);
  html = applyDiscoveryRuntimeStrings(html, locale);

  // Baked-in result count (JS re-renders it on load; this covers no-JS).
  const countMany = DISCOVERY_RUNTIME_STRINGS[locale]?.countMany;
  if (countMany) {
    html = html.replace(/>(\d+) curated developments</g, (m, n) => `>${countMany.replace('{count}', n)}<`);
  }

  // Gallery-dot aria-labels ("Show image 3 of 6").
  const showImage = SHOW_IMAGE_TEMPLATES[locale];
  if (showImage) {
    html = html.replace(/aria-label="Show image (\d+) of (\d+)"/g, (m, n, total) =>
      `aria-label="${showImage.replace('{n}', n).replace('{m}', total)}"`);
  }

  if (isRtl(locale)) {
    html = html.replace(
      '<link rel="stylesheet" href="assets/liora/liora-pages.css">',
      '<link rel="stylesheet" href="assets/liora/liora-pages.css">\n  <link rel="stylesheet" href="assets/liora/liora-rtl.css">'
    );
  }

  const outPath = path.join(root, meta.urlPrefix, 'developments.html');
  mkdirSync(path.dirname(outPath), { recursive: true });
  writeFileSync(outPath, html);
  written.push(`${meta.urlPrefix}/developments.html`);
}

// English original: switcher + reciprocal hreflang, text untouched.
let englishHtml = source;
englishHtml = injectSwitcher(englishHtml, DEFAULT_LOCALE);
englishHtml = englishHtml.replace(
  `<link rel="canonical" href="${siteUrl}/developments.html">`,
  `<link rel="canonical" href="${siteUrl}/developments.html">\n${hreflangLinks('developments.html', siteUrl)}`
);
writeFileSync(sourcePath, englishHtml);
written.push('developments.html (switcher + hreflang added)');

console.log(JSON.stringify({ written }, null, 2));
