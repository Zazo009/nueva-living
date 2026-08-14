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
export function hreflangLinks(outputPath, siteUrl) {
  const links = LOCALES.map((meta) => {
    const href = `${siteUrl}/${localizedPath(outputPath, meta.code)}`;
    return `  <link rel="alternate" hreflang="${meta.hreflang}" href="${href}">`;
  });
  links.push(`  <link rel="alternate" hreflang="x-default" href="${siteUrl}/${outputPath}">`);
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

// Renders the on-brand language switcher: a native <details>/<summary>
// primitive (accessible, keyboard-operable, zero JS dependency by default)
// styled entirely through the site's own design tokens rather than a
// generic UI-library dropdown. `outputPath` is the current page's English
// output filename (e.g. "developments.html"), used to compute each
// locale's equivalent URL so switching language preserves the current page.
export function renderLanguageSwitcher(outputPath, locale) {
  const current = localeMeta(locale);
  const options = LOCALES.map((meta) => {
    // Absolute path (leading "/"), not a bare relative filename resolved
    // via <base href>: Netlify's link post-processing does not understand
    // <base>, and it silently mis-rewrote the English option's relative
    // "index.html" (or "developments.html", etc.) into the current page's
    // own directory (e.g. "/ar/") since that's the only locale whose
    // localizedPath() has no directory prefix to anchor it. An absolute
    // path needs no resolution by anything, so it can't be mis-rewritten.
    const href = `/${localizedPath(outputPath, meta.code)}`;
    const active = meta.code === locale;
    return `<a class="lang-switcher-option${active ? ' is-active' : ''}" href="${href}" lang="${meta.htmlLang}" ${active ? 'aria-current="true"' : ''}>${meta.nativeLabel}</a>`;
  }).join('\n            ');

  return `<details class="lang-switcher" data-lang-switcher>
      <summary class="lang-switcher-toggle" aria-label="${t('lang.switcherLabel', locale)}">
        <span class="lang-switcher-code">${current.code.toUpperCase()}</span>
        <svg class="lang-switcher-caret" viewBox="0 0 12 8" aria-hidden="true"><path d="M1 1.5 6 6.5 11 1.5" stroke-width="1.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </summary>
      <div class="lang-switcher-panel" role="menu">
            ${options}
      </div>
    </details>`;
}

// Shared close-on-outside-click / close-on-route-change behaviour for the
// <details> based switcher -- kept tiny and dependency-free so it can be
// safely inlined on every page type (property, footer, segment), including
// pages that don't load the larger liora-property.js bundle.
export const LANG_SWITCHER_SCRIPT = `<script>
  document.querySelectorAll('[data-lang-switcher]').forEach((el) => {
    document.addEventListener('click', (event) => {
      if (!el.open) return;
      if (el.contains(event.target)) return;
      el.open = false;
    });
    el.addEventListener('toggle', () => {
      if (!el.open) return;
      document.querySelectorAll('[data-lang-switcher][open]').forEach((other) => {
        if (other !== el) other.open = false;
      });
    });
  });
</script>`;
