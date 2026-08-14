// Generates locale variants of the homepage (nueva-living-home.html -> a
// real, functioning es/index.html, fr/index.html, de/index.html,
// ru/index.html, ar/index.html) so the language switcher and the property
// pages' "Cinematic Presentation" links -- which already point at
// "<locale>/index.html" -- resolve to a real page instead of 404ing.
//
// Scope (documented, not silently partial): this script fully localizes
// the homepage's shared chrome -- nav, mobile menu, footer, language
// switcher, <html lang/dir>, hreflang, and (for Arabic) the RTL stylesheet
// and self-hosted Arabic font. It does NOT translate the homepage's own
// hero copy, repeating content blocks, or the embedded cinematic
// presentation's UI-chrome strings ("Guided", "Project Details", field
// labels) -- those live deep inside ~700 lines of hand-authored JS in this
// file and are called out explicitly as the top follow-up item in
// docs/i18n.md. Every non-default-locale homepage is a real, complete page
// (not a placeholder): the untranslated sections simply render their
// existing English content, which is honest fallback behaviour, not a
// broken or empty route.
import { existsSync, readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import path from 'node:path';
import { LOCALES, DEFAULT_LOCALE, localeMeta, t, isRtl, rootPrefix } from './lib/i18n.mjs';

const root = process.cwd();
const sourcePath = path.join(root, 'nueva-living-home.html');
if (!existsSync(sourcePath)) {
  console.log('nueva-living-home.html not found, skipping homepage locale build.');
  process.exit(0);
}

// Strip any switcher/hreflang/base-tag/RTL-link this script injected on a
// previous run, so re-running the build (e.g. a second local build, or a
// CI re-run) always starts from a clean English baseline instead of
// compounding duplicate injections into the source file it reads from.
function stripPriorInjections(html) {
  return html
    .replace(/<base href="\.\.\/">\n/g, '')
    .replace(/(<title>[^<]*<\/title>\n)(?:  <link rel="alternate"[^\n]*\n)*/, '$1')
    .replace(/<li><details class="lang-switcher" data-lang-switcher>[\s\S]*?<\/details><\/li>\n\s*/g, '')
    .replace(/\s*<details class="lang-switcher" data-lang-switcher>[\s\S]*?<\/details>\n(?=\s*<\/div>)/g, '\n')
    .replace(/\n\s*#nav \.lang-switcher, \.mobile-menu \.lang-switcher[\s\S]*?\.mobile-menu \.lang-switcher-option \{ color: inherit; \}\n/g, '\n')
    .replace(/\n\s*<link rel="stylesheet" href="\.\.\/assets\/liora\/liora-rtl\.css\?v=[^"]*">\n/g, '\n')
    .replace(/\s*<script>\n\s*document\.querySelectorAll\('\[data-lang-switcher\]'\)[\s\S]*?<\/script>\n/g, '\n');
}

const source = stripPriorInjections(readFileSync(sourcePath, 'utf8'));
const rtlCssVersion = existsSync(path.join(root, 'assets/liora/liora-rtl.css')) ? '1' : '1';

// Exact-string replacements for the homepage's own hand-authored nav/
// footer copy (verified against the current markup). Applied globally so
// both the desktop nav and the duplicated mobile-menu list pick up the
// same translation from one entry.
function navFooterReplacements(locale) {
  return [
    ['>Buying Guides<', `>${t('nav.buyingGuides', locale)}<`],
    ['>Why Nueva<', `>${t('nav.whyNueva', locale)}<`],
    ['>Developments<', `>${t('nav.developments', locale)}<`],
    ['>Areas<', `>${t('nav.areas', locale)}<`],
    ['>Advisory<', `>${t('nav.advisory', locale)}<`],
    ['>Contact Us<', `>${t('nav.contactUs', locale)}<`],
    ['aria-label="Nueva Living — Home"', `aria-label="${t('nav.home', locale)}"`],
    ['aria-label="Menu"', `aria-label="${t('nav.menu', locale)}"`],
    ['New Development Advice', t('footer.about.tagline', locale)],
    ['We help international buyers find and compare new-build and off-plan homes across the Costa del Sol.', t('footer.about.text', locale)],
    ['>Company<', `>${t('footer.companyTitle', locale)}<`],
    ['>Why Nueva Living<', `>${t('footer.whyNuevaLiving', locale)}<`],
    ['>About<', `>${t('footer.about', locale)}<`],
    ['>Privacy Policy<', `>${t('footer.privacyPolicy', locale)}<`],
    ['>Legal Notice<', `>${t('footer.legalNotice', locale)}<`],
    ['>Cookie Policy<', `>${t('footer.cookiePolicy', locale)}<`],
    ['>Projects<', `>${t('footer.projectsTitle', locale)}<`],
    ['>All Developments<', `>${t('footer.allDevelopments', locale)}<`],
    ['>Areas Overview<', `>${t('footer.areasOverview', locale)}<`],
    ['Information on this website is for general marketing purposes only and does not constitute legal, financial or investment advice. Details, prices and delivery dates are subject to change.', t('footer.disclaimer', locale)]
  ];
}

const switcherCss = `
    #nav .lang-switcher, .mobile-menu .lang-switcher { position: relative; }
    #nav .lang-switcher-toggle, .mobile-menu .lang-switcher-toggle {
      display: inline-flex; align-items: center; gap: 6px; cursor: pointer; list-style: none;
      color: #f4ead9; font-family: 'Montserrat', Arial, sans-serif; font-size: clamp(13px, 0.95vw, 14px);
      font-weight: 600; letter-spacing: 0.10em; padding: 12px 0;
    }
    #nav .lang-switcher-toggle::-webkit-details-marker { display: none; }
    #nav .lang-switcher-caret { width: 10px; height: 7px; }
    #nav .lang-switcher-caret path, .mobile-menu .lang-switcher-caret path { stroke: currentColor; }
    #nav .lang-switcher-panel {
      position: absolute; top: 100%; right: 0; margin-top: 10px; min-width: 160px;
      background: #2f2417; border: 1px solid rgba(201,163,95,0.28); box-shadow: 0 18px 50px rgba(0,0,0,0.35);
      display: flex; flex-direction: column; padding: 8px; z-index: 40;
    }
    #nav .lang-switcher-option {
      display: block; padding: 9px 12px; color: #f4ead9; font-size: 13px; font-weight: 500;
      letter-spacing: 0.02em; text-decoration: none; white-space: nowrap;
    }
    #nav .lang-switcher-option:hover, #nav .lang-switcher-option.is-active { background: rgba(201,163,95,0.16); color: #c9a35f; }
    .mobile-menu .lang-switcher-panel { position: static; margin-top: 8px; border: none; background: transparent; box-shadow: none; padding-left: 12px; }
    .mobile-menu .lang-switcher-option { color: inherit; }
`;

function renderSwitcherHtml(locale, forMobile) {
  const current = localeMeta(locale);
  const p = rootPrefix(locale);
  const options = LOCALES.map((meta) => {
    const href = `${p}${meta.urlPrefix ? `${meta.urlPrefix}/` : ''}index.html`;
    const active = meta.code === locale;
    return `<a class="lang-switcher-option${active ? ' is-active' : ''}" href="${href}" lang="${meta.htmlLang}" ${active ? 'aria-current="true"' : ''}>${meta.nativeLabel}</a>`;
  }).join('\n              ');
  const inner = `<details class="lang-switcher" data-lang-switcher>
      <summary class="lang-switcher-toggle" aria-label="${t('lang.switcherLabel', locale)}">
        <span class="lang-switcher-code">${current.code.toUpperCase()}</span>
        <svg class="lang-switcher-caret" viewBox="0 0 12 8" aria-hidden="true"><path d="M1 1.5 6 6.5 11 1.5" stroke-width="1.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </summary>
      <div class="lang-switcher-panel" role="menu">
              ${options}
      </div>
    </details>`;
  return forMobile ? inner : `<li>${inner}</li>`;
}

const LANG_SWITCHER_SCRIPT = `<script>
  document.querySelectorAll('[data-lang-switcher]').forEach((el) => {
    document.addEventListener('click', (event) => {
      if (!el.open) return;
      if (el.contains(event.target)) return;
      el.open = false;
    });
  });
</script>`;

const siteUrl = 'https://nuevaliving.com';
function hreflangBlock() {
  const lines = LOCALES.map((m) => `  <link rel="alternate" hreflang="${m.hreflang}" href="${siteUrl}/${m.urlPrefix ? `${m.urlPrefix}/` : ''}index.html">`);
  lines.push(`  <link rel="alternate" hreflang="x-default" href="${siteUrl}/index.html">`);
  return lines.join('\n');
}

const written = [];

for (const meta of LOCALES) {
  if (meta.code === DEFAULT_LOCALE) continue;
  const locale = meta.code;
  let html = source;

  // <html lang/dir>
  html = html.replace('<html lang="en">', `<html lang="${meta.htmlLang}" dir="${meta.dir}">`);

  // <base> so every existing relative asset/page reference resolves
  // correctly from one directory deeper, exactly as on the property pages.
  html = html.replace(
    '<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />',
    '<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />\n  <base href="../">'
  );

  // Language switcher is inserted first, while the surrounding English
  // text is still literal and easy to anchor on; nav/footer text
  // translation runs after so it also picks up the switcher's own labels
  // (harmless no-op for those) in one consistent pass.
  html = html.replace(
    '</ul>\n    <button class="nav-burger"',
    `${renderSwitcherHtml(locale, false)}\n    </ul>\n    <button class="nav-burger"`
  );
  html = html.replace(
    '<a href="contact.html" onclick="closeMobile()">Contact Us</a>\n  </div>',
    `<a href="contact.html" onclick="closeMobile()">Contact Us</a>\n    ${renderSwitcherHtml(locale, true)}\n  </div>`
  );

  // Nav / footer chrome
  for (const [find, replace] of navFooterReplacements(locale)) {
    html = html.split(find).join(replace);
  }

  // Reciprocal hreflang, right after <title> (a stable, unique anchor).
  html = html.replace(
    /(<title>[^<]*<\/title>)/,
    `$1\n${hreflangBlock()}`
  );

  // Switcher styling + close-on-outside-click script + RTL/Arabic assets
  html = html.replace('</style>\n</head>', `${switcherCss}\n  </style>\n</head>`);
  if (isRtl(locale)) {
    html = html.replace(
      '</head>',
      `  <link rel="stylesheet" href="../assets/liora/liora-rtl.css?v=${rtlCssVersion}">\n</head>`
    );
  }
  html = html.replace('</body>', `  ${LANG_SWITCHER_SCRIPT}\n</body>`);

  const outPath = path.join(root, meta.urlPrefix, 'index.html');
  mkdirSync(path.dirname(outPath), { recursive: true });
  writeFileSync(outPath, html);
  written.push(`${meta.urlPrefix}/index.html`);
}

// The English homepage also gets the switcher (so users can navigate INTO
// a locale, not just back out of one) and the reciprocal hreflang set.
// Text stays English; no <base>, no RTL assets, no lang/dir change needed.
let englishHtml = source;
if (!englishHtml.includes('data-lang-switcher')) {
  englishHtml = englishHtml.replace(
    '</ul>\n    <button class="nav-burger"',
    `${renderSwitcherHtml(DEFAULT_LOCALE, false)}\n    </ul>\n    <button class="nav-burger"`
  );
  englishHtml = englishHtml.replace(
    '<a href="contact.html" onclick="closeMobile()">Contact Us</a>\n  </div>',
    `<a href="contact.html" onclick="closeMobile()">Contact Us</a>\n    ${renderSwitcherHtml(DEFAULT_LOCALE, true)}\n  </div>`
  );
  englishHtml = englishHtml.replace('</style>\n</head>', `${switcherCss}\n  </style>\n</head>`);
  englishHtml = englishHtml.replace(
    /(<title>[^<]*<\/title>)/,
    `$1\n${hreflangBlock()}`
  );
  englishHtml = englishHtml.replace('</body>', `  ${LANG_SWITCHER_SCRIPT}\n</body>`);
  writeFileSync(sourcePath, englishHtml);
  written.push('nueva-living-home.html (switcher + hreflang added)');
}

console.log(JSON.stringify({ written }, null, 2));
