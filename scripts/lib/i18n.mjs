// Central i18n helper for the static-site build scripts.
//
// This is a build-time system, not a runtime framework: each locale gets its
// own fully-rendered set of static HTML files (English stays at the site
// root to preserve existing URLs; other locales are emitted under
// /<locale>/...). There is no client-side language switch -- switching
// language is a normal navigation to the equivalent page in that locale's
// directory, which keeps the cinematic presentation, animations and
// hydration-free architecture completely unaffected.
import { readFileSync } from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const localesConfig = JSON.parse(readFileSync(path.join(root, 'content/i18n/locales.json'), 'utf8'));
const strings = JSON.parse(readFileSync(path.join(root, 'content/i18n/strings.json'), 'utf8'));

export const LOCALES = localesConfig.locales;
export const DEFAULT_LOCALE = localesConfig.default;
export const LOCALE_CODES = LOCALES.map((l) => l.code);

export function localeMeta(code) {
  return LOCALES.find((l) => l.code === code) || LOCALES.find((l) => l.code === DEFAULT_LOCALE);
}

export function isRtl(code) {
  return localeMeta(code).dir === 'rtl';
}

// t(key, locale, vars?) -- looks up a shared UI string, falling back to
// English when a translation is missing, and finally to the key itself
// (visibly wrapped) only in local/dev builds so a gap is never silently
// invisible during review, but never ships untranslated to production.
export function t(key, locale = DEFAULT_LOCALE, vars = {}) {
  const entry = strings[key];
  let value;
  if (!entry) {
    value = undefined;
  } else {
    value = entry[locale] || entry[DEFAULT_LOCALE];
  }
  if (value === undefined) {
    if (process.env.NODE_ENV !== 'production') {
      console.warn(`[i18n] Missing string key "${key}" for locale "${locale}"`);
    }
    value = key;
  }
  return Object.entries(vars).reduce(
    (acc, [name, val]) => acc.replaceAll(`{${name}}`, String(val)),
    value
  );
}

function isPlainObject(value) {
  return value !== null && typeof value === 'object' && !Array.isArray(value);
}

// Merges a locale-specific content overlay onto the English source object.
// Top-level keys are merged one level deep when both sides are plain
// objects (e.g. overlay.availability = {headlineHtml, copy, sourceNote} onto
// English availability = {..., units: [...]}), so a translator can override
// just the prose fields of a section without having to also restate
// factual/structural data like `availability.units`, `privateViewing.href`
// or image dimensions -- those silently keep falling back to English.
// Arrays (quickFacts, media.items, why.points, ...) and primitives are
// replaced wholesale when present, since a translated array must stand on
// its own (partial-array merging has no sane semantics here).
// Whether a string key exists in the dictionary. Used by build-time guards:
// t() falls back to returning the key itself, so a missing entry renders as
// literal "mediaCategory.Solarium" on the page rather than failing loudly.
// True when strings.json actually defines this key. Callers that build a key
// from content (e.g. `mediaCategory.${category}`) must check this first: a
// project's i18n overlay may already have localized that content, in which
// case there is no key to find and t() would return the literal key text.
export function hasString(key) {
  return Object.prototype.hasOwnProperty.call(strings, key);
}

export function localizeProject(project, locale) {
  if (locale === DEFAULT_LOCALE) return project;
  const overlay = project.i18n?.[locale];
  if (!overlay) return project;
  const merged = { ...project };
  for (const [key, value] of Object.entries(overlay)) {
    const englishValue = project[key];
    merged[key] = (isPlainObject(value) && isPlainObject(englishValue))
      ? { ...englishValue, ...value }
      : value;
  }
  return merged;
}

// Path helper: English keeps the existing flat URL (e.g. "developments.html");
// every other locale is prefixed with its directory (e.g. "es/developments.html").
export function localizedPath(outputPath, locale) {
  const meta = localeMeta(locale);
  if (!meta.urlPrefix) return outputPath;
  return `${meta.urlPrefix}/${outputPath}`;
}

// Builds the reciprocal hreflang link tags for a given page across every
// locale that has a rendered equivalent, plus x-default pointing at English.
// `locales` lets a caller advertise only the locales it actually generated.
// A page we can only stand behind in English (statutory content that has not
// been through native-language review) must not claim nine translations that
// do not exist -- an hreflang pointing at a missing or English-bodied URL is
// worse than no hreflang at all.
export function hreflangLinks(outputPath, siteUrl, locales = LOCALES) {
  const links = locales.map((meta) => {
    const href = pageUrl(outputPath, meta.code, siteUrl);
    return `  <link rel="alternate" hreflang="${meta.hreflang}" href="${href}">`;
  });
  links.push(`  <link rel="alternate" hreflang="x-default" href="${pageUrl(outputPath, DEFAULT_LOCALE, siteUrl)}">`);
  return links.join('\n');
}

// Locale pages live one directory deeper (es/developments.html) than
// English (developments.html). Rather than hand-prefixing every one of the
// hundreds of relative asset/image/link references scattered through the
// large page-render functions (fragile and easy to miss one), every
// non-English page emits a single `<base href="../">` tag in <head> and all
// existing relative paths resolve correctly unmodified -- this function is
// kept only for call sites that explicitly opt out of relying on <base>.
export function rootPrefix() {
  return '';
}

export function baseHrefTag(locale) {
  return localeMeta(locale).urlPrefix ? '  <base href="../">\n' : '';
}

// The public URL for a page in a given locale.
//
// Homepages are served from their directory, so the canonical form is
// https://nuevaliving.com/ and https://nuevaliving.com/es/ -- never
// /es/index.html. Both resolve, and advertising two forms of the same page
// across canonical, hreflang and sitemap is exactly the kind of ambiguity
// those tags exist to remove. English already used the clean form; this
// makes every locale match.
export function pageUrl(outputPath, locale, siteUrl = 'https://nuevaliving.com') {
  const prefix = localeMeta(locale).urlPrefix;
  const dir = prefix ? `${prefix}/` : '';
  if (outputPath === 'index.html') return `${siteUrl}/${dir}`;
  return `${siteUrl}/${dir}${outputPath}`;
}

// WebPage + BreadcrumbList JSON-LD for a page that has no schema of its
// own. The footer, area and guides pages shipped with no structured data
// in any language (90 indexable pages), which is what breadcrumb rich
// results in search are built from. `trail` is [[label, outputPath], ...]
// from the page's own visible breadcrumb, so the two always agree.
export function pageSchema({ outputPath, locale, title, description, trail = [], siteUrl = 'https://nuevaliving.com' }) {
  const items = [
    { name: 'Nueva Living', path: 'index.html' },
    ...trail.map(([name, path]) => ({ name, path })),
    { name: title, path: outputPath }
  ];
  const schema = [
    {
      '@context': 'https://schema.org',
      '@type': 'WebPage',
      name: title,
      description,
      url: pageUrl(outputPath, locale, siteUrl),
      inLanguage: localeMeta(locale).htmlLang,
      isPartOf: { '@type': 'WebSite', name: 'Nueva Living', url: siteUrl }
    },
    {
      '@context': 'https://schema.org',
      '@type': 'BreadcrumbList',
      itemListElement: items.map((item, index) => ({
        '@type': 'ListItem',
        position: index + 1,
        name: item.name,
        item: pageUrl(item.path, locale, siteUrl)
      }))
    }
  ];
  return `  <script type="application/ld+json">\n${JSON.stringify(schema, null, 2)}\n  </script>`;
}

// Self-referencing canonical + social tags for a locale page.
//
// build_dist.mjs's injectSeo() only covers pages that have a pageMeta
// entry, which in practice means the English originals -- it deliberately
// skips locale pages on the assumption they author their own tags at
// render time. Footer and segment pages only emitted hreflang and
// og:locale, so 110 indexable locale pages shipped with no canonical and
// no Open Graph at all. With six near-identical language versions a
// self-referencing canonical is what keeps them from reading as duplicates.
export function seoTags(outputPath, locale, { title, description, siteUrl = 'https://nuevaliving.com', image, type = 'website' } = {}) {
  const meta = localeMeta(locale);
  const url = pageUrl(outputPath, locale, siteUrl);
  const shareImage = image || `${siteUrl}/assets/liora/viewing/scene-08.jpg`;
  const esc = (value) => String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
  return [
    `<link rel="canonical" href="${esc(url)}">`,
    `<meta property="og:site_name" content="Nueva Living">`,
    `<meta property="og:locale" content="${esc(meta.htmlLang)}">`,
    `<meta property="og:type" content="${esc(type)}">`,
    `<meta property="og:title" content="${esc(title)}">`,
    `<meta property="og:description" content="${esc(description)}">`,
    `<meta property="og:url" content="${esc(url)}">`,
    `<meta property="og:image" content="${esc(shareImage)}">`,
    `<meta name="twitter:card" content="summary_large_image">`,
    `<meta name="twitter:title" content="${esc(title)}">`,
    `<meta name="twitter:description" content="${esc(description)}">`,
    `<meta name="twitter:image" content="${esc(shareImage)}">`
  ].map((line) => `  ${line}`).join('\n');
}

// `<base href="../">` makes relative ASSET paths resolve correctly from one
// directory deeper -- but it does the same thing to relative PAGE links, so
// a bare href="guides.html" on es/about.html resolves to the ENGLISH
// /guides.html. That silently dropped the reader back into English from
// every nav link, footer link, breadcrumb and logo on every locale page.
//
// This rewrites internal page links to sit inside the locale directory
// (guides.html -> es/guides.html, which `<base>` then resolves to
// /es/guides.html). Applied to already-rendered HTML so it covers links
// wherever they were written, rather than relying on every one of the
// hundreds of call sites remembering to localize itself.
//
// Left alone: absolute paths (the language switcher deliberately uses
// those to move BETWEEN locales), external URLs, anchors, mailto/tel,
// asset paths, and anything already carrying the locale prefix.
export function localizeInternalLinks(html, locale) {
  const meta = localeMeta(locale);
  if (!meta.urlPrefix) return html;
  const prefix = meta.urlPrefix;

  // data-card-url is rewritten alongside href because it is a page link in
  // every sense that matters -- the card gallery navigates to it when the
  // photo is clicked, and the shortlist stores it as the saved project's
  // URL. Left unlocalized it sent an Arabic or Spanish reader to the
  // English project page, but only when they clicked the image rather than
  // the button, which is why it went unnoticed: the visible link was right.
  return html.replace(/(href|data-card-url)="([^"]+)"/g, (whole, attribute, url) => {
    if (/^(?:[a-z][a-z0-9+.-]*:|\/\/|\/|#)/i.test(url)) return whole;
    if (url.startsWith(`${prefix}/`)) return whole;
    // Only page links: must be an .html file at the top level, optionally
    // followed by a query string and/or fragment. Asset paths (which live
    // under assets/…) never match because of the leading-directory check.
    if (!/^[A-Za-z0-9._-]+\.html(?:[?#].*)?$/.test(url)) return whole;
    return `${attribute}="${prefix}/${url}"`;
  });
}

// Renders the on-brand language switcher: a native <details>/<summary>
// primitive (accessible, keyboard-operable, zero JS dependency by default)
// styled entirely through the site's own design tokens rather than a
// generic UI-library dropdown. `outputPath` is the current page's English
// output filename (e.g. "developments.html"), used to compute each
// locale's equivalent URL so switching language preserves the current page.
export const LANG_CHECK_ICON = '<svg class="lang-switcher-check" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke-width="2.4" aria-hidden="true"><path d="M4 12.5l5 5L20 6.5"></path></svg>';
export const LANG_CHECK_SPACER = '<span class="lang-switcher-check-spacer" aria-hidden="true"></span>';

// `fallbackPath` is for pages that exist in English only (verified statutory
// content we will not publish machine-translated). Without it the switcher
// would offer nine languages that all 404, so instead each non-English option
// points at the nearest page that does exist in that language -- normally the
// guides hub -- and the English option still points at this page.
export function renderLanguageSwitcher(outputPath, locale, fallbackPath = null) {
  const current = localeMeta(locale);
  const options = LOCALES.map((meta) => {
    // Absolute path (leading "/"), not a bare relative filename resolved
    // via <base href>: Netlify's link post-processing does not understand
    // <base>, and it silently mis-rewrote the English option's relative
    // "index.html" (or "developments.html", etc.) into the current page's
    // own directory (e.g. "/ar/") since that's the only locale whose
    // localizedPath() has no directory prefix to anchor it. An absolute
    // path needs no resolution by anything, so it can't be mis-rewritten.
    const target = fallbackPath && meta.code !== DEFAULT_LOCALE ? fallbackPath : outputPath;
    const href = `/${localizedPath(target, meta.code)}`;
    const active = meta.code === locale;
    return `<a class="lang-switcher-option${active ? ' is-active' : ''}" href="${href}" lang="${meta.htmlLang}" ${active ? 'aria-current="true"' : ''}>${active ? LANG_CHECK_ICON : LANG_CHECK_SPACER}${meta.nativeLabel}</a>`;
  }).join('\n            ');

  return `<details class="lang-switcher" data-lang-switcher>
      <summary class="lang-switcher-toggle" aria-label="${t('lang.switcherLabel', locale)}">
        <span class="lang-switcher-code">${current.code.toUpperCase()}</span>
        <svg class="lang-switcher-caret" viewBox="0 0 12 8" aria-hidden="true"><path d="M1 1.5 6 6.5 11 1.5" stroke-width="1.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </summary>
      <div class="lang-switcher-panel" role="menu">
        <span class="lang-switcher-panel-label">${t('lang.switcherLabel', locale)}</span>
        <div class="lang-switcher-panel-options">
            ${options}
        </div>
      </div>
    </details>`;
}

// The Guides nav item and its submenu, rendered once here so all five
// nav-generating builders share one implementation rather than each
// keeping its own copy (which is how the nav groupings drifted before).
// Same <details> mechanism as the language switcher above: keyboard
// accessible and functional with no JS, with the shared script below
// adding click-outside dismissal.
//
// `prefix` is the builder's own root prefix (property pages sit one
// directory deeper); pass '' where pages are written to the site root.
function guidesMenuItems(locale) {
  return [
    [t('nav.buyingGuides', locale), localizedPath('guides.html', locale)],
    [t('nav.mortgageCalculator', locale), `${localizedPath('guides.html', locale)}#mortgage-calculator`],
    [t('nav.referralAmbassador', locale), localizedPath('referrals.html', locale)]
  ];
}

// The burger menu uses the same disclosure component; only the CSS
// differs, so the panel sits inline in the drawer rather than floating.
export function guidesMobileLinks(locale, prefix = '') {
  return renderGuidesMenu(locale, prefix);
}

export function areasMobileLinks(locale, prefix = '') {
  return renderAreasMenu(locale, prefix);
}

// The burger drawer's two contact actions, sitting directly under the nav
// list. WhatsApp is the primary (filled) action, email the secondary
// (outlined) -- keep that hierarchy. Numbers match the general business
// contacts already used in the footer.
export function renderDrawerActions(locale) {
  return `<div class="mobile-menu-actions">
      <a class="mobile-menu-action mobile-menu-action--primary" href="https://wa.me/46707576709" target="_blank" rel="noopener">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1-.2.2-.6.8-.8 1-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4 0-.5.2-.7l.4-.5c.1-.2.1-.3 0-.5l-.8-1.9c-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.5.1-.7.3-.2.3-.9.9-.9 2.2s.9 2.5 1.1 2.7c.1.2 1.8 2.8 4.4 3.9.6.3 1.1.4 1.5.6.6.2 1.2.1 1.6.1.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.2-.3-.2-.5-.4z"></path></svg>
        <span>${t('cta.whatsappUs', locale)}</span>
      </a>
      <a class="mobile-menu-action mobile-menu-action--secondary" href="mailto:contact@nuevaliving.com">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><rect x="3" y="5" width="18" height="14"></rect><path d="M3 7l9 6 9-6"></path></svg>
        <span>${t('cta.emailUs', locale)}</span>
      </a>
    </div>`;
}

function areasMenuItems(locale) {
  return [
    [t('nav.allAreas', locale), localizedPath('areas.html', locale)],
    [t('area.marbella', locale), localizedPath('area-marbella.html', locale)],
    [t('area.nuevaAndalucia', locale), localizedPath('area-nueva-andalucia.html', locale)],
    [t('area.benahavis', locale), localizedPath('area-benahavis.html', locale)],
    [t('area.estepona', locale), localizedPath('area-estepona.html', locale)],
    [t('area.casares', locale), localizedPath('area-casares.html', locale)],
    [t('area.mijasFuengirola', locale), localizedPath('area-mijas-fuengirola.html', locale)]
  ];
}

// Guides and Areas are the same component with a different list. Writing the
// markup out twice is how the two would drift -- one gaining a caret or an
// aria attribute the other never got -- so there is one renderer.
function renderNavDisclosure(label, items, prefix) {
  const options = items
    .map(([text, href]) => `<a class="nav-dropdown-option" href="${prefix}${href}">${text}</a>`)
    .join('\n          ');

  return `<details class="nav-dropdown" data-nav-dropdown>
      <summary class="nav-dropdown-toggle">
        <span>${label}</span>
        <svg class="nav-dropdown-caret" viewBox="0 0 12 8" aria-hidden="true"><path d="M1 1.5 6 6.5 11 1.5" stroke-width="1.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </summary>
      <div class="nav-dropdown-panel" role="menu">
          ${options}
      </div>
    </details>`;
}

export function renderGuidesMenu(locale, prefix = '') {
  return renderNavDisclosure(t('nav.guides', locale), guidesMenuItems(locale), prefix);
}

export function renderAreasMenu(locale, prefix = '') {
  return renderNavDisclosure(t('nav.areas', locale), areasMenuItems(locale), prefix);
}

// Shared close-on-outside-click / close-on-route-change behaviour for the
// <details> based switcher -- kept tiny and dependency-free so it can be
// safely inlined on every page type (property, footer, segment), including
// pages that don't load the larger liora-property.js bundle.
export const LANG_SWITCHER_SCRIPT = `<script>
  // Guides submenu: same dismissal behaviour as the language switcher,
  // plus Esc to close. Opening one closes the other so the two panels
  // can never overlap in the bar.
  document.querySelectorAll('[data-nav-dropdown]').forEach((el) => {
    document.addEventListener('click', (event) => {
      if (!el.open) return;
      if (el.contains(event.target)) return;
      el.open = false;
    });
    el.addEventListener('toggle', () => {
      if (!el.open) return;
      document.querySelectorAll('[data-nav-dropdown][open], [data-lang-switcher][open]').forEach((other) => {
        if (other !== el) other.open = false;
      });
    });
  });

  document.addEventListener('keydown', (event) => {
    if (event.key !== 'Escape') return;
    document.querySelectorAll('[data-nav-dropdown][open], [data-lang-switcher][open]').forEach((el) => {
      el.open = false;
    });
  });

  document.querySelectorAll('[data-lang-switcher]').forEach((el) => {
    document.addEventListener('click', (event) => {
      if (!el.open) return;
      if (el.contains(event.target)) return;
      el.open = false;
    });
    el.addEventListener('toggle', () => {
      if (!el.open) return;
      document.querySelectorAll('[data-lang-switcher][open], [data-nav-dropdown][open]').forEach((other) => {
        if (other !== el) other.open = false;
      });

      // The panel's CSS anchors it to whichever edge of the toggle its
      // language convention favors (right on LTR, left on RTL). That
      // anchor is fine on desktop, but on a narrow phone the toggle can
      // sit anywhere in the top bar (it gets moved next to the burger
      // button below 1120px), so a fixed-width panel opening from it can
      // run off either side of the screen. Clamp it back into view after
      // layout settles, in viewport coordinates, so it works regardless
      // of which edge it opened from.
      var panel = el.querySelector('.lang-switcher-panel');
      if (!panel) return;
      requestAnimationFrame(() => {
        panel.style.left = '';
        panel.style.right = '';
        var margin = 12;
        var elRect = el.getBoundingClientRect();
        var panelRect = panel.getBoundingClientRect();
        var overflowRight = panelRect.right - (window.innerWidth - margin);
        var overflowLeft = margin - panelRect.left;
        if (overflowRight > 0) {
          panel.style.right = 'auto';
          panel.style.left = (panelRect.left - elRect.left - overflowRight) + 'px';
        } else if (overflowLeft > 0) {
          panel.style.right = 'auto';
          panel.style.left = (panelRect.left - elRect.left + overflowLeft) + 'px';
        }
      });
    });
  });

  // On narrow screens the nav links collapse into the burger menu, which
  // used to take the language switcher with them -- buried under the menu,
  // and styled flat so its open panel read as a dark block. Lift it into
  // the top bar instead, next to the shortlist heart, so it looks and
  // behaves exactly as it does on desktop. The switcher already inside the
  // mobile menu is removed so there is only ever one.
  (function () {
    var nav = document.querySelector('.site-nav, #nav');
    var menu = document.querySelector('.mobile-menu');
    if (!nav) return;
    var inBar = nav.querySelector('[data-lang-switcher]');
    var inMenu = menu ? menu.querySelector('[data-lang-switcher]') : null;
    if (!inBar && !inMenu) return;

    // Prefer the nav-bar copy; if the page only has the menu one, promote it.
    var switcher = inBar || inMenu;
    if (switcher === inMenu) nav.appendChild(switcher);
    else if (inMenu && inMenu.parentNode) inMenu.parentNode.removeChild(inMenu);

    var burger = nav.querySelector('.nav-burger, #burgerBtn');
    var mq = window.matchMedia('(max-width: 1120px)');
    var home = switcher.parentNode;
    var homeNext = switcher.nextSibling;

    function place() {
      if (mq.matches) {
        // Sit immediately before the burger, after the heart.
        if (burger && switcher.nextElementSibling !== burger) nav.insertBefore(switcher, burger);
        switcher.setAttribute('data-lang-switcher-compact', '');
      } else {
        if (switcher.parentNode !== home) home.insertBefore(switcher, homeNext);
        switcher.removeAttribute('data-lang-switcher-compact');
      }
    }
    place();
    if (mq.addEventListener) mq.addEventListener('change', place);
    else if (mq.addListener) mq.addListener(place);
  })();
</script>`;

// Google truncates meta descriptions around 160 characters, so anything past
// that is invisible -- and worse, it usually cuts mid-word. Trim to the last
// sentence that fits; if a single sentence is already too long, fall back to
// the last word boundary and mark the cut.
export const SEO_DESCRIPTION_MAX = 160;

export function clampDescription(text, max = SEO_DESCRIPTION_MAX) {
  const value = String(text || '').replace(/\s+/g, ' ').trim();
  if (value.length <= max) return value;

  const sentenceEnd = /[.!?…](?=\s|$)/g;
  let cut = 0;
  let match;
  while ((match = sentenceEnd.exec(value)) !== null) {
    if (match.index + 1 > max) break;
    cut = match.index + 1;
  }
  if (cut >= max * 0.6) return value.slice(0, cut).trim();

  const slice = value.slice(0, max - 1);
  const lastSpace = slice.lastIndexOf(' ');
  return `${slice.slice(0, lastSpace > 0 ? lastSpace : slice.length).replace(/[,;:]$/, '')}…`;
}
