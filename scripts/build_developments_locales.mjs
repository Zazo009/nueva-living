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
  LANG_SWITCHER_SCRIPT,
  localizeInternalLinks
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
const SORTED_ENTRIES = [...DEVELOPMENTS_PAGE_ENTRIES].sort((a, b) => b.find.length - a.find.length);

// Idempotency: remove anything this script previously injected into the
// English source so re-running never compounds duplicates.
function stripPriorInjections(html) {
  return html
    .replace(/\s*<details class="lang-switcher" data-lang-switcher>[\s\S]*?<\/details>\n?/g, '\n')
    .replace(/(<link rel="canonical"[^\n]*\n)(?:  <link rel="alternate"[^\n]*\n)*/, '$1')
    // Matches ANY <script> that mentions [data-lang-switcher], rather than one
    // that begins with it. The block used to start with that selector; a
    // Guides-dropdown section was later added above it, this anchor stopped
    // matching, and the script was appended again on every single build --
    // 25 copies of the same 4.4KB block had accumulated in these pages before
    // anyone noticed, because nothing about the page looked wrong.
    .replace(/\s*<script>((?:(?!<\/script>)[\s\S])*?\[data-lang-switcher\](?:(?!<\/script>)[\s\S])*?)<\/script>\n/g, '\n');
}

const source = stripPriorInjections(readFileSync(sourcePath, 'utf8'));

// The desktop switcher is anchored on the nav divider, which exists only
// to precede it, rather than on the Contact link: that link's label has
// been renamed and a divider was inserted after it since this was
// written, and each time the anchor stopped matching the switcher was
// silently dropped from the desktop header with no build error.
function injectSwitcher(html, locale) {
  const switcher = renderLanguageSwitcher('developments.html', locale);
  const divider = '<span class="nav-divider" aria-hidden="true"></span>';
  let next = html.replace(divider, `${divider}\n      ${switcher}`);
  // The drawer switcher goes last, after the WhatsApp/Email actions block.
  // Anchor on the email action rather than the Contact link: the actions
  // block now sits between them, and a stale anchor here fails silently.
  next = next.replace(
    /(<a class="mobile-menu-action mobile-menu-action--secondary"[\s\S]*?<\/a>\n    <\/div>)\n  <\/div>/,
    `$1\n    ${switcher}\n  </div>`
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
  const missed = [];
  for (const slug of readdirSync(projectsDir)) {
    const projectPath = path.join(projectsDir, slug, 'project.json');
    if (!existsSync(projectPath)) continue;
    const project = JSON.parse(readFileSync(projectPath, 'utf8'));
    const en = project.card?.description || project.description;
    const translated = project.i18n?.[locale]?.card?.description;
    if (!en || !translated || en === translated) continue;
    // Keyed on the card's tagline class rather than a bare <p>. The bare
    // form silently stopped matching the moment the card gained a class on
    // that paragraph, and the only symptom was English descriptions on five
    // translated pages -- no error, no failed build. Both forms are handled
    // so neither markup shape can break it again, and a miss is reported
    // rather than passing quietly.
    const before = next;
    next = next
      .split(`<p class="dev-tagline">${en}</p>`).join(`<p class="dev-tagline">${translated}</p>`)
      .split(`<p>${en}</p>`).join(`<p>${translated}</p>`);
    if (before === next && next.includes(en)) {
      missed.push(`${slug}: card description present but not replaced for ${locale}`);
    }
  }
  if (missed.length) {
    throw new Error(`Card description translation failed:\n  ${missed.join('\n  ')}`);
  }
  return next;
}

// Project-card gallery image alt text. The cards are generated once, in
// English, by build_property_pages.mjs (renderProjectCard has no locale
// argument -- it writes into the shared developments.html markers), so the
// alt attributes arrive here as English regardless of locale. Each project's
// media items are already translated in project.json, so this maps each
// English alt to its localized counterpart by index.
function applyCardImageAlts(html, locale) {
  const projectsDir = path.join(root, 'content/liora-projects');
  if (!existsSync(projectsDir)) return html;
  let next = html;
  for (const slug of readdirSync(projectsDir)) {
    const projectPath = path.join(projectsDir, slug, 'project.json');
    if (!existsSync(projectPath)) continue;
    const project = JSON.parse(readFileSync(projectPath, 'utf8'));
    const english = project.media?.items || [];
    const localized = project.i18n?.[locale]?.media?.items || [];
    if (localized.length !== english.length) continue;
    english.forEach((item, index) => {
      const en = item.alt;
      const translated = localized[index]?.alt;
      if (!en || !translated || en === translated) return;
      next = next.split(`alt="${en}"`).join(`alt="${translated}"`);
    });
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

  // Page copy, filter UI, cards, footer. Longest find first so a short
  // entry can never corrupt a longer string before its own entry matches.
  // Card alts before the entry table: some alts contain area names that the
  // table rewrites, which would break the full-alt match.
  html = applyCardImageAlts(html, locale);
  for (const entry of SORTED_ENTRIES) {
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
  html = localizeInternalLinks(html, locale);
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
