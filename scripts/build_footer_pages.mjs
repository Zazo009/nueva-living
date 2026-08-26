import { existsSync, readFileSync, readdirSync, writeFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';
import {
  LOCALES,
  DEFAULT_LOCALE,
  localeMeta,
  isRtl,
  t,
  localizedPath,
  hreflangLinks,
  baseHrefTag,
  renderLanguageSwitcher,
  renderGuidesMenu,
  renderAreasMenu,
  guidesMobileLinks,
  renderDrawerActions,
  LANG_SWITCHER_SCRIPT,
  localizeProject,
  localizeInternalLinks,
  seoTags,
  pageSchema
} from './lib/i18n.mjs';
import { MONTH_NAMES, localizeMonthDate } from './lib/dates.mjs';
import { GUIDE_AUTHOR, organizationSchema, personSchemas, organizationId, personId } from './lib/brand.mjs';
import { renderUnifiedCard } from './lib/project_card.mjs';
import { renderProjectCardGallery } from './lib/card_gallery.mjs';
import { FOOTER_PAGE_ENTRIES } from './lib/footer_page_translations.mjs';
import { EDITORIAL_ALT_ENTRIES } from './lib/editorial_alt_translations.mjs';

// Applies FOOTER_PAGE_ENTRIES (translated body prose for footer pages) as
// literal string replacement over already-rendered HTML -- the `pages`
// array below is built once with fixed English `body` HTML, so rather
// than restructure every page's render into a locale-aware function
// (a much bigger refactor for content that's opaque markup, not
// structured fields), each entry's exact English text is swapped for its
// translation post-render, the same proven approach used for the
// homepage's HOMEPAGE_CONTENT_ENTRIES. Untranslated entries (or entries
// with no match for a given locale) simply leave the English text in
// place -- safe, honest fallback, not a broken page.
// Longest find first: a short entry ("Areas" -> "Zonas") must never fire
// inside a longer string ("Areas We Cover") before that string's own
// entry has had its chance to match.
const SORTED_FOOTER_PAGE_ENTRIES = [...FOOTER_PAGE_ENTRIES, ...EDITORIAL_ALT_ENTRIES].sort((a, b) => b.find.length - a.find.length);

function applyFooterPageTranslations(html, locale) {
  if (locale === DEFAULT_LOCALE) return html;
  let result = html;
  for (const entry of SORTED_FOOTER_PAGE_ENTRIES) {
    const replacement = entry[locale];
    if (!replacement) continue;
    result = result.split(entry.find).join(replacement);
  }
  return result;
}

// Same general buyer-process FAQ used on every property page (defaultFaqs()
// in build_property_pages.mjs) -- sourced from the same translated
// content/i18n/strings.json faq.* keys rather than a hardcoded English
// duplicate, so this already has full es/fr/de/ru/ar coverage.
function generalFaqs(locale = DEFAULT_LOCALE) {
  return [
    [t('faq.foreigners.q', locale), t('faq.foreigners.a', locale)],
    [t('faq.nie.q', locale), t('faq.nie.a', locale)],
    [t('faq.costs.q', locale), t('faq.costs.a', locale)],
    [t('faq.mortgage.q', locale), t('faq.mortgage.a', locale)],
    [t('faq.offplan.q', locale), t('faq.offplan.a', locale)],
    [t('faq.reservation.q', locale), t('faq.reservation.a', locale)],
    [t('faq.rental.q', locale), t('faq.rental.a', locale)],
    [t('faq.lawyer.q', locale), t('faq.lawyer.a', locale)]
  ];
}

function generalFaqSection(locale = DEFAULT_LOCALE) {
  const items = generalFaqs(locale).map(([question, answer], index) => `<details class="segment-faq-item"${index === 0 ? ' open' : ''}>
        <summary>${question}</summary>
        <p>${answer}</p>
      </details>`).join('\n      ');

  return `<section class="section segment-faq-section"><div class="section-inner">
    <div class="section-head"><span class="label">${t('section.faq', locale)}</span><div class="rule"></div><h2 class="section-title">${t('faq.headlineHtml', locale)}</h2></div>
    <div class="segment-faq-list">
      ${items}
    </div>
  </div></section>`;
}

const areas = JSON.parse(readFileSync('content/nueva-areas.json', 'utf8'));
const projects = readdirSync('content/liora-projects', { withFileTypes: true })
  .filter((entry) => entry.isDirectory())
  .map((entry) => join('content/liora-projects', entry.name, 'project.json'))
  .filter((file) => existsSync(file))
  .map((file) => JSON.parse(readFileSync(file, 'utf8')));

const home = 'index.html';
const fontPreloadBlock = `  <link rel="preload" href="assets/fonts/google/co3bmX5slCNuHLi8bLeY9MK7whWMhyjYqXtKky2F7g.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="assets/fonts/google/8vIJ7ww63mVu7gt79mT7PkRXMw.woff2" as="font" type="font/woff2" crossorigin>`;

// Areas and Guides are disclosures rather than flat links, so they are not in
// this list -- nav() places them by name. Slicing this array by index is what
// broke when Areas moved out of it, so the positions are written out instead.
function navLinks(locale) {
  return [
    [t('nav.developments', locale), 'developments.html'],
    [t('nav.about', locale), 'about.html'],
    [t('nav.advisory', locale), 'advisory.html'],
    [t('nav.contactUs', locale), 'contact.html'],
  ];
}

function footerLinks(locale) {
  return {
    company: [
      [t('footer.whyNuevaLiving', locale), 'why-nueva.html'],
      [t('footer.about', locale), 'about.html'],
      [t('nav.advisory', locale), 'advisory.html'],
      [t('nav.referralAmbassador', locale), 'referrals.html'],
      [t('footer.contactUs', locale), 'contact.html'],
    ],
    projects: [
      [t('nav.developments', locale), 'developments.html'],
      [t('nav.buyingGuides', locale), 'guides.html'],
      [t('nav.allAreas', locale), 'areas.html'],
      [t('area.marbella', locale), 'area-marbella.html'],
      [t('area.estepona', locale), 'area-estepona.html'],
      [t('area.casares', locale), 'area-casares.html'],
      [t('area.benahavis', locale), 'area-benahavis.html'],
      [t('area.nuevaAndalucia', locale), 'area-nueva-andalucia.html'],
      [t('area.mijasFuengirola', locale), 'area-mijas-fuengirola.html'],
    ],
    legal: [
      [t('footer.privacyPolicy', locale), 'privacy-policy.html'],
      [t('footer.legalNotice', locale), 'legal-notice.html'],
      [t('footer.cookiePolicy', locale), 'cookie-policy.html'],
    ],
  };
}

function nav(locale = DEFAULT_LOCALE, currentOutputPath = 'index.html', langFallback = null) {
  const links = navLinks(locale);
  const link = (index) => {
    const [label, href] = links[index];
    return `<a href="${href}">${label}</a>`;
  };
  const switcher = renderLanguageSwitcher(currentOutputPath, locale, langFallback);
  return `<nav class="site-nav">
    <div class="nav-links nav-links-left">
      ${link(0)}
      ${renderAreasMenu(locale)}
      ${link(1)}
    </div>
    <a class="nav-logo" href="${home}" aria-label="${t('nav.home', locale)}">
      <img class="nav-wordmark" src="assets/liora/brand/nueva-living-hero-logo-transparent.png?v=7" alt="Nueva Living" width="420" height="100">
      <span class="nav-wordmark-text" aria-hidden="true">Nueva Living</span>
    </a>
    <div class="nav-links nav-links-right">
      ${link(2)}
      ${renderGuidesMenu(locale)}
      ${link(3)}
      <span class="nav-divider" aria-hidden="true"></span>
      ${switcher}
    </div>
    <button class="nav-burger" type="button" aria-label="${t('nav.menu', locale)}" aria-controls="mobileMenu" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
  </nav>
  <div class="mobile-menu" id="mobileMenu">
    ${link(0)}
    ${renderAreasMenu(locale)}
    ${link(1)}
    ${link(2)}
    ${guidesMobileLinks(locale)}
    ${link(3)}
    ${renderDrawerActions(locale)}
    ${renderLanguageSwitcher(currentOutputPath, locale, langFallback)}
  </div>`;
}

// A breadcrumb parent is the same destination the nav and footer link to, so
// it must carry the same label. These were literal English strings in the page
// definitions, which meant every locale's guide pages showed a breadcrumb
// reading "Guides" while the menu two lines above said "Köpguider".
const BREADCRUMB_PARENT_KEYS = {
  'guides.html': 'nav.buyingGuides',
  'developments.html': 'nav.developments',
  'areas.html': 'nav.allAreas'
};

function breadcrumb(currentLabel, parents = [], locale = DEFAULT_LOCALE) {
  const parentItems = parents.map(([label, href]) => {
    const key = BREADCRUMB_PARENT_KEYS[href];
    return `<li><a href="${esc(href)}">${esc(key ? t(key, locale) : label)}</a></li>`;
  }).join('\n      ');
  return `<nav class="breadcrumb-bar" aria-label="Breadcrumb">
    <ol class="breadcrumb-list">
      <li><a href="${home}">${t('breadcrumb.home', locale)}</a></li>${parentItems ? `
      ${parentItems}` : ''}
      <li><span aria-current="page">${esc(currentLabel)}</span></li>
    </ol>
  </nav>`;
}

function footer(locale = DEFAULT_LOCALE) {
  const links = footerLinks(locale);
  const list = (items) => items.map(([label, href]) => `<li><a href="${href}">${label}</a></li>`).join('\n          ');
  return `<footer>
    <div class="footer-grid">
      <div>
        <img class="footer-logo" src="assets/liora/brand/nueva-living-lockup-espresso-transparent.png?v=7" alt="Nueva Living" width="700" height="340">
        <p class="footer-about">${t('footer.about.text', locale)}</p>
      </div>
      <div class="footer-col">
        <div class="footer-col-title">${t('footer.companyTitle', locale)}</div>
        <ul>
          ${list(links.company)}
        </ul>
      </div>
      <div class="footer-col">
        <div class="footer-col-title">${t('footer.projectsTitle', locale)}</div>
        <ul>
          ${list(links.projects)}
        </ul>
      </div>
      <div class="footer-col">
        <div class="footer-col-title">${t('footer.contactTitle', locale)}</div>
        <ul>
          <li><a href="mailto:contact@nuevaliving.com">contact@nuevaliving.com</a></li>
          <li><a href="tel:+34645446624" dir="ltr">+34 645 44 66 24</a></li>
          <li><a href="https://maps.google.com/?q=Avenida+del+Prado+71,+29660+Marbella,+M%C3%A1laga,+Spain" target="_blank" rel="noopener">Avenida del Prado 71, 29660 Marbella</a></li>
        </ul>
        <div class="footer-col-title" style="margin-top:24px;">${t('footer.legalTitle', locale)}</div>
        <ul>
          ${list(links.legal)}
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>${t('footer.disclaimer', locale)}</p>
      <span>&copy; 2026 Nueva Living &middot; LIORA LIVING SL. &middot; NIF B88827472</span>
    </div>
  </footer>`;
}

// seoContext replaces the decorative kicker with a line that actually carries
// the page's search terms, and it now sits inside the <h1> rather than above
// it. The editorial display line is untouched -- the audit's finding was that
// these H1s were beautiful and said nothing a search engine could use, not
// that they were bad writing. Falls back to the kicker where no context is
// supplied, so locale pages and any page not covered by the audit are
// unaffected.
// Hero images were shipping as bare JPEGs -- 203KB to 956KB each, no srcset,
// no modern format -- and on every page the hero is the LCP element. AVIF at
// the same visual quality runs 60-90% smaller here.
//
// The widths are probed rather than assumed: only variants that actually exist
// on disk are offered, so a hero without generated variants degrades to the
// original JPEG instead of emitting a 404 into the srcset.
function heroPicture(src, alt = '', width, height, position) {
  const stem = src.replace(/\.[a-z]+$/i, '');
  const dir = stem.slice(0, stem.lastIndexOf('/'));
  const base = stem.slice(stem.lastIndexOf('/') + 1);
  // Discovered from disk rather than assumed: variants are named for the
  // width they actually are, so a 2047px source yields -2047, not -2048.
  const siblings = existsSync(dir) ? readdirSync(dir) : [];
  const srcsetFor = (ext) => siblings
    .map((name) => name.match(new RegExp(`^${base}-(\\d+)\\.${ext}$`)))
    .filter(Boolean)
    .map((m) => ({ w: Number(m[1]), file: `${dir}/${m[0]}` }))
    .filter(({ w }) => w >= 1200)
    .sort((a, b) => a.w - b.w)
    .map(({ w, file }) => `${file} ${w}w`)
    .join(', ');
  const avif = srcsetFor('avif');
  const webp = srcsetFor('webp');
  const attrs = `alt="${esc(alt)}"${width ? ` width="${width}"` : ''}${height ? ` height="${height}"` : ''}`
    + `${position ? ` style="object-position:${esc(position)}"` : ''} loading="eager" fetchpriority="high" decoding="async"`;
  if (!avif && !webp) return `<img src="${esc(src)}" ${attrs}>`;
  const sizes = '100vw';
  return `<picture>`
    + (avif ? `<source type="image/avif" srcset="${avif}" sizes="${sizes}">` : '')
    + (webp ? `<source type="image/webp" srcset="${webp}" sizes="${sizes}">` : '')
    + `<img src="${esc(src)}" ${attrs}></picture>`;
}

// The byline shows a date a reader can read; the datetime attribute keeps the
// machine-readable form. Writing the ISO string at the reader is what this
// replaced.
function humanDate(iso, locale) {
  const [year, month, day] = String(iso).split('-');
  const monthName = Object.keys(MONTH_NAMES)[Number(month) - 1];
  return localizeMonthDate(`${Number(day)} ${monthName} ${year}`, locale);
}

const siteUrl = 'https://nuevaliving.com';

// A buying guide states tax rates, statutory guarantee periods and warranty
// law. Google's raters are told to look for a named, accountable author on
// exactly this kind of page, and these carried only WebPage + BreadcrumbList:
// the same assertions with nobody behind them.
//
// The Person and Organization nodes ship alongside the Article rather than
// being referenced into thin air, so the author reference resolves on the page
// that makes the claim. Both reuse the @ids minted on /about.html, so this is
// the same Sasan Raftari the about page describes and not a second one.
//
// dateModified starts equal to datePublished and is rewritten by build_dist
// from the content hash, so it moves when the guide's text actually changes
// rather than on every deploy.
function guideArticleSchema({ file, title, description, heroImage, datePublished, locale }) {
  const author = { '@id': personId(siteUrl, GUIDE_AUTHOR) };
  return [
    organizationSchema(siteUrl),
    ...personSchemas(siteUrl).filter((person) => person['@id'] === author['@id']),
    {
      '@context': 'https://schema.org',
      '@type': 'Article',
      '@id': `${siteUrl}/${localizedPath(file, locale)}#article`,
      headline: title,
      description,
      inLanguage: localeMeta(locale).htmlLang,
      image: `${siteUrl}/${heroImage}`,
      author,
      publisher: { '@id': organizationId(siteUrl) },
      datePublished,
      dateModified: datePublished,
      mainEntityOfPage: `${siteUrl}/${localizedPath(file, locale)}`
    }
  ];
}

function page({ file, title, breadcrumbTitle, breadcrumbs, description, heroImage, heroAlt = '', heroWidth, heroHeight, heroPosition, heroKicker, seoContext, heroTitle, heroLead, body, bodyClass = '', englishOnly = false, datePublished }, locale = DEFAULT_LOCALE) {
  const meta = localeMeta(locale);
  const rtl = isRtl(locale);
  const html = `<!doctype html>
<html lang="${meta.htmlLang}" dir="${meta.dir}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
${baseHrefTag(locale)}  <title>${esc(title)} | Nueva Living</title>
  <meta name="description" content="${esc(description)}">
${hreflangLinks(file, 'https://nuevaliving.com', englishOnly ? [LOCALES[0]] : LOCALES)}
${seoTags(file, locale, { title: `${title} | Nueva Living`, description, image: heroImage ? `https://nuevaliving.com/${heroImage}` : undefined })}
${pageSchema({ outputPath: file, locale, title: breadcrumbTitle || title, description, trail: breadcrumbs || [] })}${datePublished ? `
  <script type="application/ld+json">
${JSON.stringify(guideArticleSchema({ file, title, description, heroImage, datePublished, locale }), null, 2)}
  </script>` : ''}
  <link rel="icon" href="assets/liora/liora-favicon-512.png?v=6" type="image/png" sizes="512x512">
  <link rel="icon" href="assets/liora/favicon-32.png?v=6" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="assets/liora/apple-touch-icon.png?v=6" sizes="180x180">
${fontPreloadBlock}
  <link rel="stylesheet" href="assets/fonts/google/liora-fonts.css">
  <link rel="stylesheet" href="assets/liora/liora-pages.css">${rtl ? `
  <link rel="stylesheet" href="assets/liora/liora-rtl.css">` : ''}
  <script src="assets/liora/liora-card-gallery.js" defer></script>
</head>
<body${bodyClass ? ` class="${bodyClass}"` : ''}>
  ${nav(locale, file, englishOnly ? 'guides.html' : null)}
  ${breadcrumb(breadcrumbTitle || title, breadcrumbs, locale)}
  <main>
    <section class="page-hero">
      ${heroPicture(heroImage, heroAlt, heroWidth, heroHeight, heroPosition)}
      <div class="hero-inner">
        <h1 class="display-title">
          <span class="kicker">${esc(seoContext || heroKicker)}</span>
          <span class="display-title-line">${heroTitle}</span>
        </h1>
        <p class="lead">${esc(heroLead)}</p>
${datePublished ? `        <p class="guide-byline"><span>${t('guide.writtenBy', locale)} <a href="about.html" rel="author">${esc(GUIDE_AUTHOR.name)}</a></span><span class="guide-byline-sep" aria-hidden="true">&middot;</span><span>${t('guide.updated', locale)} <time data-guide-updated datetime="${datePublished}">${esc(humanDate(datePublished, locale))}</time></span></p>` : ''}
      </div>
    </section>
    ${typeof body === 'function' ? body(locale) : body}
  </main>
  ${footer(locale)}
  <script>
    const burger = document.querySelector('.nav-burger');
    const menu = document.getElementById('mobileMenu');
    if (burger && menu) {
      burger.addEventListener('pointerdown', (event) => event.stopPropagation());
      burger.addEventListener('click', (event) => {
        event.preventDefault();
        event.stopPropagation();
        const open = menu.classList.toggle('open');
        burger.setAttribute('aria-expanded', open ? 'true' : 'false');
        document.body.classList.toggle('menu-open', open);
      });
      menu.querySelectorAll('a').forEach((link) => {
        link.addEventListener('click', () => {
          menu.classList.remove('open');
          burger.setAttribute('aria-expanded', 'false');
          document.body.classList.remove('menu-open');
        });
      });
    }
  </script>
  ${LANG_SWITCHER_SCRIPT}
</body>
</html>`;
  return localizeInternalLinks(applyFooterPageTranslations(html, locale), locale);
}

function esc(value) {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

const META_LABEL_KEYS = { From: 'common.from', Type: 'common.type', Status: 'common.status', Delivery: 'common.delivery' };

// card.meta is raw [label, value] data on the English project object, never
// translated directly (see the docs on the project.i18n overlay pattern --
// only prose fields are translated, not this kind of paired data). Labels
// are a small closed vocabulary so they're translated via t(); the "Type"
// value specifically is swapped for the already-localized hero.type
// (falling back to the raw meta value for any other label, e.g. price or
// delivery-quarter strings that are locale-agnostic anyway).
function localizedMeta(project, meta, locale) {
  return meta.map(([label, value]) => {
    const localizedLabel = META_LABEL_KEYS[label] ? t(META_LABEL_KEYS[label], locale) : label;
    const localizedValue = label === 'Type' && project.hero?.type ? project.hero.type : value;
    return [localizedLabel, localizedValue];
  });
}

function areaProjectCard(sourceProject, locale = DEFAULT_LOCALE) {
  const project = localizeProject(sourceProject, locale);
  const meta = localizedMeta(project, project.card?.meta || [], locale);
  const card = project.card || {};
  const priceValue = (meta.find(([label]) => /^(from|desde|à partir de|ab|от|ابتداءً من)$/i.test(label)) || [])[1]
    || (project.hero?.startingPrice || '').replace(/^From\s+/i, '')
    || '';
  return renderUnifiedCard({
    project,
    gallery: renderProjectCardGallery(project),
    href: project.output,
    name: project.name,
    badge: card.badge || '',
    price: priceValue,
    location: card.label || card.locExtended || project.hero?.location || t('common.newDevelopment', locale),
    description: card.description || project.description,
    type: project.hero?.type || '',
    t: (key, vars) => t(key, locale, vars),
    className: 'area-project-card',
    attrs: ' data-project-card',
    heading: 'h3',
    indent: '    '
  });
}

function areaProjects(area, locale = DEFAULT_LOCALE) {
  const selected = area.featuredProjects
    .map((projectSlug) => projects.find((project) => project.slug === projectSlug))
    .filter(Boolean);

  if (selected.length) return selected.map((project) => areaProjectCard(project, locale)).join('\n');

  return `<article class="area-project-empty">
    <span class="label">${t('area.privateSelection', locale)}</span>
    <h3>${t('area.currentOpportunities', locale)}</h3>
    <p>${t('area.noPublishedProjectNote', locale)}</p>
    <a class="project-link" href="#area-enquiry">${t('area.requestShortlist', locale)}</a>
  </article>`;
}

function areaPriceSources(area, locale = DEFAULT_LOCALE) {
  const sources = area.priceSources || [{ label: t('area.viewMarketReference', locale), url: area.priceSource }];
  return sources
    .filter((source) => source.url)
    .map((source) => `<a href="${esc(source.url)}" target="_blank" rel="noopener noreferrer">${esc(source.label)}</a>`)
    .join('');
}

function areaForm(area, locale = DEFAULT_LOCALE) {
  const areaOptions = areas.map((option) => (
    `<option value="${esc(option.formArea)}"${option.slug === area.slug ? ' selected' : ''}>${esc(option.name)}</option>`
  )).join('');

  return `<form class="form-panel area-form" name="nueva-${esc(area.slug)}-enquiry" method="POST" data-crm-lead action="/.netlify/functions/nueva-lead"><input type="text" name="honeypot" tabindex="-1" autocomplete="off" aria-hidden="true" style="display:none">
    <input type="hidden" name="subject" data-remove-prefix value="New Nueva Living ${esc(area.name)} enquiry">
    <input type="hidden" name="request_context" value="${esc(area.name)} area enquiry">
    <div class="form-grid">
      <div class="field"><label for="${esc(area.slug)}-first-name">${t('form.firstName', locale)}</label><input id="${esc(area.slug)}-first-name" name="first_name" autocomplete="given-name" placeholder="${t('form.firstNamePlaceholder', locale)}" required></div>
      <div class="field"><label for="${esc(area.slug)}-last-name">${t('form.lastName', locale)}</label><input id="${esc(area.slug)}-last-name" name="last_name" autocomplete="family-name" placeholder="${t('form.lastNamePlaceholder', locale)}" required></div>
      <div class="field"><label for="${esc(area.slug)}-email">${t('form.email', locale)}</label><input id="${esc(area.slug)}-email" name="email" type="email" autocomplete="email" placeholder="your@email.com" required></div>
      <div class="field"><label for="${esc(area.slug)}-phone">${t('form.phone', locale)}</label><input id="${esc(area.slug)}-phone" name="phone" type="tel" autocomplete="tel" placeholder="${t('form.phonePlaceholder', locale)}"></div>
      <div class="field"><label for="${esc(area.slug)}-area">${t('form.preferredArea', locale)}</label><select id="${esc(area.slug)}-area" name="preferred_area">${areaOptions}<option value="Open to all areas">${t('form.openToAllAreas', locale)}</option></select></div>
      <div class="field"><label for="${esc(area.slug)}-property-type">${t('form.propertyType', locale)}</label><select id="${esc(area.slug)}-property-type" name="property_type_interest"><option value="">${t('form.selectType', locale)}</option><option value="Apartments">${t('form.apartments', locale)}</option><option value="Penthouses">${t('form.penthouses', locale)}</option><option value="Villas">${t('form.villas', locale)}</option><option value="Townhouses">${t('form.townhouses', locale)}</option><option value="Mixed / Open">${t('form.mixedOpen', locale)}</option></select></div>
      <div class="field"><label for="${esc(area.slug)}-budget">${t('form.budgetRange', locale)}</label><select id="${esc(area.slug)}-budget" name="budget_range"><option value="">${t('form.selectBudget', locale)}</option><option>&euro;300,000 - &euro;500,000</option><option>&euro;500,000 - &euro;900,000</option><option>&euro;900,000 - &euro;1,500,000</option><option>&euro;1,500,000+</option></select></div>
      <div class="field"><label for="${esc(area.slug)}-bedrooms">${t('area.minimumBedrooms', locale)}</label><select id="${esc(area.slug)}-bedrooms" name="bedrooms_min"><option value="">${t('form.any', locale)}</option><option value="1">1+</option><option value="2">2+</option><option value="3">3+</option><option value="4">4+</option></select></div>
      <div class="field full"><label for="${esc(area.slug)}-message">${t('form.message', locale)}</label><textarea id="${esc(area.slug)}-message" name="message">${esc(area.formMessage)}</textarea></div>
      <label class="consent-row field full" for="${esc(area.slug)}-consent"><input id="${esc(area.slug)}-consent" name="consent" type="checkbox" required><span>${t('form.consentContact', locale)}</span></label>
      <label class="consent-row field full" for="${esc(area.slug)}-marketing"><input id="${esc(area.slug)}-marketing" name="marketing_opt_in" type="checkbox"><span>${t('form.consentMarketing', locale)}</span></label>
    </div>
    <div class="form-actions"><button class="btn" type="submit">${t('form.sendEnquiry', locale)}</button><span class="form-response"></span></div>
  </form>`;
}

const SEGMENT_LINKS = {
  marbella: { href: 'new-build-apartments-penthouses-marbella.html', area: 'Marbella' },
  estepona: { href: 'new-build-apartments-penthouses-estepona.html', area: 'Estepona' },
  'nueva-andalucia': { href: 'new-build-apartments-penthouses-nueva-andalucia.html', area: 'Nueva Andaluc&iacute;a' },
};

function areaDetailPage(sourceArea, locale = DEFAULT_LOCALE) {
  const area = localizeProject(sourceArea, locale);
  // "Marbella average asking price" is a place name plus a phrase. Translating
  // the phrase and keeping the name means the six areas need no per-area
  // overlay for it -- they had none, in any of the nine locales.
  const priceLabel = (label) => {
    const match = /^(.+?)\s+average asking price$/i.exec(String(label || '').trim());
    return match ? t('area.averageAskingPrice', locale, { name: match[1] }) : label;
  };
  const priceItems = area.prices.map((price) => `<div class="area-price-item"><span>${esc(priceLabel(price.label))}</span><strong>${esc(price.value)}</strong></div>`).join('');
  const highlights = area.highlights.map(([title, copy], index) => `<article class="area-highlight"><span>${String(index + 1).padStart(2, '0')}</span><h3>${esc(title)}</h3><p>${esc(copy)}</p></article>`).join('');
  const paragraphs = area.intro.paragraphs.map((paragraph) => `<p class="body-copy">${esc(paragraph)}</p>`).join('');
  const spotlightSection = area.spotlight ? `
    <section class="section area-spotlight"><div class="section-inner"><div class="section-head"><span class="label">${t('area.localKnowledge', locale)}</span><div class="rule"></div><h2 class="section-title">${area.spotlight.headlineHtml}</h2><p class="body-copy">${esc(area.spotlight.intro)}</p></div><div class="cards spotlight-cards">${area.spotlight.items.map(([title, copy, image], index) => `<article class="card spotlight-card">${image ? `<div class="spotlight-card-image"><img src="${esc(image.src)}" alt="${esc(image.alt || title)}" width="${image.width || 800}" height="${image.height || 600}" loading="lazy" decoding="async"></div>` : ''}<div class="spotlight-card-body"><div class="card-number">${String(index + 1).padStart(2, '0')}</div><h3>${esc(title)}</h3><p>${esc(copy)}</p></div></article>`).join('')}</div>${area.spotlight.photoCredits ? `<p class="spotlight-photo-credits">${esc(area.spotlight.photoCredits)}</p>` : ''}</div></section>` : '';

  return {
    file: area.output,
    // The localized seo.title if the area overlay carries one, otherwise the
    // generic template. Without this the locale pages all read "Områdesguide
    // Marbella" / "Przewodnik po okolicy Marbella" -- a label, not something
    // anyone searches for -- while the English page got the real title from
    // build_dist. The description was already localized; the title was not.
    // <title> appends " | Nueva Living" below, and the older locale overlays
    // already carry it, so strip it here rather than shipping it twice.
    title: (area.seo?.title || t('area.areaGuide', locale, { name: area.name }))
      .replace(/\s*\|\s*Nueva Living\s*$/, ''),
    breadcrumbTitle: area.name,
    breadcrumbs: [[t('nav.allAreas', locale), 'areas.html']],
    description: area.seo.description,
    heroImage: area.hero.image,
    heroAlt: area.hero.alt,
    heroWidth: area.hero.width,
    heroHeight: area.hero.height,
    heroPosition: area.hero.position,
    heroKicker: area.hero.kicker,
    heroTitle: area.hero.titleHtml,
    heroLead: area.hero.lead,
    bodyClass: 'area-detail-page',
    body: `<section class="section area-introduction"><div class="section-inner area-intro-layout"><div><span class="label">${t('area.livingIn', locale, { name: esc(area.name) })}</span><div class="rule"></div><h2 class="section-title">${area.intro.headlineHtml}</h2>${paragraphs}</div><div class="area-highlights">${highlights}</div></div></section>${spotlightSection}
    <section class="section quiet-band area-market"><div class="section-inner area-market-layout"><div><span class="label">${t('area.priceContext', locale)}</span><div class="rule"></div><h2 class="section-title">${t('area.currentAskingPriceReference', locale)}</h2><p class="body-copy">${t('area.priceContextIntro', locale)}</p></div><div class="area-price-panel">${priceItems}<p>${esc(area.priceNote)}</p><div class="area-price-sources">${areaPriceSources(area, locale)}</div></div></div></section>
    <section class="section area-developments"><div class="section-inner"><div class="section-head"><span class="label">${t('area.currentMatch', locale)}</span><div class="rule"></div><h2 class="section-title">${t('area.projectsIn', locale, { name: esc(area.name) })}</h2><p class="body-copy">${t('area.projectsMatchingNote', locale)}</p>${SEGMENT_LINKS[area.slug] ? `<a class="project-link area-guide-link" href="${SEGMENT_LINKS[area.slug].href}">${t('area.readFullGuide', locale, { area: SEGMENT_LINKS[area.slug].area })}</a>` : ''}</div><div class="project-grid area-project-grid">${areaProjects(area, locale)}</div></div></section>
    <section class="section area-enquiry-section" id="area-enquiry"><div class="section-inner"><div class="section-head center"><span class="label">${t('area.askAbout', locale, { name: esc(area.name) })}</span><div class="rule"></div><h2 class="section-title">${t('area.requestRelevantShortlist', locale)}</h2><p class="body-copy" style="margin-left:auto;margin-right:auto;">${t('area.shortlistNote', locale)}</p></div>${areaForm(area, locale)}</div></section>`,
  };
}

const pages = [
  {
    file: 'why-nueva.html',
    title: 'Why Choose Nueva Living',
    description: 'Why international buyers choose Nueva Living for local insight, honest advice and a smoother Costa del Sol property search.',
    heroImage: 'assets/liora/advisory-property.jpg',
    heroAlt: 'Contemporary Costa del Sol home surrounded by Mediterranean planting',
    heroKicker: 'Why Nueva Living',
    seoContext: 'An Independent Buyer\u2019s Agent for Costa del Sol New Builds',
    heroTitle: 'Finding a home should feel <em>exciting, not exhausting</em>',
    heroLead: 'We know the coast, ask the questions that glossy brochures leave out and stay close from the first conversation to the day you get the keys.',
    body: `<section class="section"><div class="section-inner split"><div><span class="label">What Sets Us Apart</span><div class="rule"></div><h2 class="section-title">Beautiful brochures are easy. <em>Good decisions take more.</em></h2><p class="body-copy">A sea-view render can make almost any development look perfect. We look past the presentation: the exact setting, the developer, the payment terms, the compromises and whether the property will still suit you years from now.</p></div><div class="image-panel"><img src="assets/liora/viewing/scene-13.jpg" alt="Refined interior detail in a Costa del Sol residence" width="2048" height="1365" loading="lazy" decoding="async"></div></div></section>
    <section class="section quiet-band"><div class="section-inner"><div class="section-head"><span class="label">Why Buyers Choose Us</span><div class="rule"></div><h2 class="section-title">Useful at the moments <em>that matter</em></h2></div><div class="cards why-cards">
      <article class="card"><div class="card-number">01</div><h3>Local, Down to Street Level</h3><p>Years on the Costa del Sol mean we understand how neighbouring communities can differ in access, atmosphere and long-term appeal.</p></article>
      <article class="card"><div class="card-number">02</div><h3>Beyond the Public Listings</h3><p>When private releases or off-market availability open up, we can bring the relevant opportunities into your search.</p></article>
      <article class="card"><div class="card-number">03</div><h3>One Thread, Start to Finish</h3><p>From your brief and viewings to negotiation and handover, we keep the moving parts together and coordinate with your independent lawyer.</p></article>
      <article class="card"><div class="card-number">04</div><h3>Three Languages, One Conversation</h3><p>Speak with us in English, Spanish or Swedish. The details stay clear, whichever language feels most natural.</p></article>
      <article class="card"><div class="card-number">05</div><h3>Honest About the Trade-offs</h3><p>If a location is noisy, a terrace is overlooked or the price feels ambitious, we say so. A good decision matters more than a quick one.</p></article>
      <article class="card"><div class="card-number">06</div><h3>Still Here After the Keys</h3><p>Handover is not the end of the relationship. We remain available and connect you with trusted local services when needed.</p></article>
    </div></div></section>
    <section class="section"><div class="section-inner"><div class="section-head center"><span class="label">Process</span><div class="rule"></div><h2 class="section-title">From first enquiry to <em>reservation</em></h2><p class="body-copy" style="margin-left:auto;margin-right:auto;">A simple step-by-step process, with no pressure.</p></div><div class="cards">
      <article class="card"><div class="card-number">1</div><h3>Tell Us What You Need</h3><p>We talk through your budget, timing, preferred areas and must-haves.</p></article>
      <article class="card"><div class="card-number">2</div><h3>Receive Your Shortlist</h3><p>You get a focused selection with current prices and availability.</p></article>
      <article class="card"><div class="card-number">3</div><h3>View and Decide</h3><p>We arrange viewings, share the project documents and explain the reservation process.</p></article>
    </div></div></section>
    <section class="section quiet-band"><div class="section-inner"><div class="section-head center"><span class="label">Know Someone Looking?</span><div class="rule"></div><h2 class="section-title">Introduce someone, <em>get rewarded</em></h2><p class="body-copy" style="margin-left:auto;margin-right:auto;">If someone in your life is thinking about a home on the Costa del Sol, our <a href="referrals.html">Referral &amp; Ambassador Program</a> lets you introduce them and receive a share of our commission when their purchase completes.</p><a class="btn ghost" href="referrals.html">Introduce Someone</a></div></div></section>
    <section class="section"><div class="section-inner"><div class="section-head center"><span class="label">Who We Are</span><div class="rule"></div><h2 class="section-title">The people <em>behind the advice</em></h2><p class="body-copy" style="margin-left:auto;margin-right:auto;">We work only with new and off-plan homes on the Costa del Sol, which is why we know the developers, the projects and the questions worth asking.</p><a class="btn ghost" href="about.html">About Nueva Living</a></div></div></section>
    <section class="cta-band"><div class="cta-inner"><div><span class="label">Ready When You Are</span><h2 class="cta-title">Bring us your wish list. We will bring back the options worth your time.</h2></div><a class="btn" href="contact.html#contact-form">Start Your Search</a></div></section>`,
  },
  {
    file: 'areas.html',
    title: 'Areas',
    description: 'Costa del Sol area guide for new development buyers.',
    heroImage: 'assets/liora/viewing/scene-01.jpg',
    heroKicker: 'Locations',
    seoContext: 'Where to Buy on the Costa del Sol \u00b7 Area Guide 2026',
    heroTitle: 'The Costa del Sol, <em>area by area</em>',
    heroLead: 'Every area feels different. We help you compare daily life, travel times, views, prices and future resale demand.',
    body: `<section class="section"><div class="section-inner"><div class="section-head"><span class="label">Area Guide</span><div class="rule"></div><h2 class="section-title">Find the area that <em>fits you</em></h2><p class="body-copy">We look at what it is actually like to live there, how easy it is to get around and what supports long-term demand.</p></div><div class="area-stack">
      <a class="area-row" id="marbella" href="area-marbella.html" aria-label="Explore the Marbella area guide"><img src="assets/liora/areas/marbella.jpg" alt="Marbella coastline at sunrise with La Concha mountain" width="1920" height="2880" loading="lazy" decoding="async"><div class="area-copy"><span class="label">Marbella</span><h3>The coast's best-known address</h3><p>Marbella combines beaches, restaurants, international schools and established neighbourhoods, from the Golden Mile to Sierra Blanca.</p><span class="area-explore">Explore Marbella</span></div></a>
      <a class="area-row" id="estepona" href="area-estepona.html" aria-label="Explore the Estepona area guide"><img src="assets/liora/areas/estepona.jpg" alt="Estepona old town street with white houses and flower pots" width="1920" height="1278" loading="lazy" decoding="async"><div class="area-copy"><span class="label">Estepona</span><h3>A growing coastal town</h3><p>Estepona has seen major improvements in recent years, with a lively old town, good beach access and plenty of new projects.</p><span class="area-explore">Explore Estepona</span></div></a>
      <a class="area-row" id="casares" href="area-casares.html" aria-label="Explore the Casares area guide"><img src="assets/liora/projects/sierra-bermeja-residences/media/development-sea-view.jpg" alt="New-build apartment blocks on the Casares hillside, with the Mediterranean and the mountains beyond" width="1400" height="787" loading="lazy" decoding="async"><div class="area-copy"><span class="label">Casares</span><h3>Lower prices, one municipality west</h3><p>A hilltop white village, a golf valley and a low-rise coast, priced below neighbouring Estepona. Car-dependent, and the three zones differ sharply.</p><span class="area-explore">Explore Casares</span></div></a>
      <a class="area-row" id="benahavis" href="area-benahavis.html" aria-label="Explore the Benahavis area guide"><img src="assets/liora/areas/benahavis.jpg" alt="Benahavis mountain village and elevated hillside landscape" width="1920" height="1280" loading="lazy" decoding="async"><div class="area-copy"><span class="label">Benahavis</span><h3>Privacy, hills and open views</h3><p>Set above Marbella, Benahavis is known for gated communities, golf, villas and a quieter pace of life.</p><span class="area-explore">Explore Benahavis</span></div></a>
      <a class="area-row" id="nueva-andalucia" href="area-nueva-andalucia.html" aria-label="Explore the Nueva Andalucia area guide"><img src="assets/liora/areas/nueva-andalucia.jpg" alt="Puerto Banús marina and La Concha near Nueva Andalucia" width="1920" height="1280" loading="lazy" decoding="async"><div class="area-copy"><span class="label">Nueva Andalucia</span><h3>Golf Valley living</h3><p>Close to Puerto Banús and surrounded by golf courses, Nueva Andalucia works well for buyers who want restaurants, services and year-round activity nearby.</p><span class="area-explore">Explore Nueva Andalucia</span></div></a>
      <a class="area-row" id="mijas-fuengirola" href="area-mijas-fuengirola.html" aria-label="Explore the Mijas and Fuengirola area guide"><img src="assets/liora/areas/fuengirola.jpg" alt="Fuengirola seafront sign with palms and Mediterranean water" width="1920" height="2560" loading="lazy" decoding="async"><div class="area-copy"><span class="label">Mijas &amp; Fuengirola</span><h3>Easy access and more choice</h3><p>This part of the coast offers good services, easy links to Malaga and a wider range of prices.</p><span class="area-explore">Explore Mijas &amp; Fuengirola</span></div></a>
    </div></div></section>
    <section class="cta-band"><div class="cta-inner"><h2 class="cta-title">Not sure where to start? Tell us what matters to you.</h2><a class="btn" href="contact.html">Ask About Areas</a></div></section>`,
  },
  {
    file: 'advisory.html',
    title: 'Advisory',
    description: 'Buyer-focused advisory for Costa del Sol new development purchases.',
    heroImage: 'assets/liora/advisory-property.jpg',
    heroKicker: 'Advisory',
    seoContext: 'Off-Plan Buyer Advisory, Costa del Sol',
    heroTitle: 'Know what you are buying <em>before you decide</em>',
    heroLead: 'We help you check the location, developer, finishes, payment plan and future resale appeal before you choose a home.',
    body: (locale) => `<section class="section"><div class="section-inner split"><div><span class="label">An Independent View</span><div class="rule"></div><h2 class="section-title">Clear advice for <em>the buyer</em></h2><p class="body-copy">A developer brochure shows the project at its best. We help you look beyond it and understand what is genuinely strong, what is fairly standard and what needs a closer check.</p></div><div class="image-panel"><img src="assets/liora/viewing/scene-13.jpg" alt="Interior detail"></div></div></section>
    <section class="section quiet-band"><div class="section-inner"><div class="section-head"><span class="label">How We Help</span><div class="rule"></div><h2 class="section-title">The details we help you <em>compare</em></h2></div><div class="cards"><article class="card"><h3>Compare Projects</h3><p>We compare prices, orientation, amenities, completion dates and nearby alternatives side by side.</p></article><article class="card"><h3>Plan the Purchase</h3><p>We talk through how you will use the home, rental plans, financing and what you may want later.</p></article><article class="card"><h3>Reserve with Clarity</h3><p>We organise project documents, viewings, reservation details and an introduction to an independent lawyer.</p></article></div></div></section>
    <section class="section"><div class="section-inner"><div class="section-head center"><span class="label">Our Promise</span><div class="rule"></div><h2 class="section-title">Straight answers, <em>no pressure</em></h2></div><div class="cards two"><article class="card"><h3>A Shorter, Better List</h3><p>We would rather show you three suitable projects than thirty generic options.</p></article><article class="card"><h3>Real Urgency Only</h3><p>We only flag urgency when availability, pricing or a reservation deadline genuinely changes.</p></article></div></div></section>
    ${generalFaqSection()}
    ${locale === DEFAULT_LOCALE ? `<section class="section quiet-band"><div class="section-inner"><div class="section-head center"><span class="label">The Mechanics</span><div class="rule" style="margin-left:auto;margin-right:auto;"></div><h2 class="section-title">How an off-plan purchase <em>actually works</em></h2><p class="body-copy" style="margin-left:auto;margin-right:auto;">Three guides on the parts of the process buyers ask about most, each written against the statute or against the schedules our developers have supplied in writing.</p></div><div class="cards"><article class="card"><h3><a href="guide-bank-guarantee-off-plan-spain.html">Bank Guarantees</a></h3><p>What protects your deposit under Ley 38/1999, and the point before the building licence at which it does not yet apply.</p></article><article class="card"><h3><a href="guide-off-plan-payment-schedules.html">Payment Schedules</a></h3><p>Reservation, contract, construction milestones and the balance at deed, using real figures from the projects on this site.</p></article><article class="card"><h3><a href="guide-new-build-warranties-snagging.html">Warranties and Snagging</a></h3><p>The ten, three and one-year guarantees, who is liable under each, and why handover starts the clock.</p></article></div></div></section>` : ''}
    <section class="section"><div class="section-inner"><div class="section-head center"><span class="label">Who We Are</span><div class="rule"></div><h2 class="section-title">The people <em>behind the advice</em></h2><p class="body-copy" style="margin-left:auto;margin-right:auto;">We work only with new and off-plan homes on the Costa del Sol, which is why we know the developers, the projects and the questions worth asking.</p><a class="btn ghost" href="about.html">About Nueva Living</a></div></div></section>
    <section class="cta-band"><div class="cta-inner"><h2 class="cta-title">Talk through the options before you reserve.</h2><a class="btn" href="contact.html">Talk to an Advisor</a></div></section>`,
  },
  {
    file: 'guide-how-buying-works.html',
    datePublished: '2026-08-12',
    title: 'How Buying Works',
    description: 'A step-by-step guide to buying a new-build home on the Costa del Sol, from your first shortlist to collecting the keys.',
    heroImage: 'assets/liora/viewing/scene-13.jpg',
    heroKicker: 'Buying Guide',
    seoContext: 'How to Buy a New-Build on the Costa del Sol \u00b7 7 Steps for 2026',
    heroTitle: 'Buying a new-build home, <em>step by step</em>',
    heroLead: 'Off-plan and new-build purchases work differently from buying a resale home. Here is exactly how the process runs, from your first shortlist to collecting the keys.',
    bodyClass: 'guide-article-page',
    body: `<section class="section"><div class="section-inner">
      <div class="guide-intro g-reveal">
        <p class="body-copy">New-build and off-plan purchases follow a different sequence from a resale purchase: staged payments, a private purchase contract, and a developer's construction timeline rather than an immediate move-in date. Seven steps, start to finish.</p>
        <div class="guide-cta-row" style="display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin-top:22px;">
          <a class="btn" href="#journey">See the Full Journey</a>
          <a class="btn ghost" href="contact.html#contact-form">Speak With an Advisor</a>
        </div>
      </div>
      <div class="guide-overview g-reveal" style="--reveal-delay:80ms">
        <div class="guide-overview-item"><strong>7</strong><span>Steps, Reservation to Keys</span></div>
        <div class="guide-overview-item"><strong>3</strong><span>People Involved: You, Nueva Living, Your Lawyer</span></div>
        <div class="guide-overview-item"><strong>NIE</strong><span>Needed Before You Sign</span></div>
        <div class="guide-overview-item"><strong>2&ndash;4</strong><span>Weeks, Reservation to Contract</span></div>
      </div>
    </div></section>
    <section class="section" id="journey"><div class="section-inner">
      <div class="section-head center g-reveal"><span class="label">The Buying Journey</span><div class="rule" style="margin-left:auto;margin-right:auto;"></div><h2 class="section-title">Seven steps, <em>start to finish</em></h2></div>
      <div class="guide-journey">
        <article class="guide-step g-reveal">
          <div class="guide-step-head">
            <span class="guide-step-index">01</span>
            <div class="guide-step-body">
              <h3>Work Out What You Actually Want</h3>
              <p>Be clear on budget, area, property type and timing before looking at a single project. Off-plan homes can be sold years before delivery, so timing matters here more than for a resale purchase.</p>
            </div>
          </div>
          <div class="guide-step-roles">
            <div class="guide-role"><span>What You Do</span><p>Decide your budget, preferred areas, property type and rough timing.</p></div>
            <div class="guide-role"><span>What Nueva Living Does</span><p>Helps you weigh off-plan against a completed, move-in-ready home for your situation.</p></div>
          </div>
          <details class="guide-step-more">
            <summary>Good to know: off-plan or completed?</summary>
            <p>Off-plan usually means a lower entry price and payments staged over the build period, at the cost of waiting. A completed home costs more upfront but you can see and move into it now. See our <a href="guide-off-plan-vs-resale.html">full off-plan vs resale comparison</a> for the detail.</p>
          </details>
        </article>
        <article class="guide-step g-reveal">
          <div class="guide-step-head">
            <span class="guide-step-index">02</span>
            <div class="guide-step-body">
              <h3>Build a Real Shortlist</h3>
              <p>Property portals tend to show broad price ranges and renders rather than confirmed, current availability. A useful shortlist compares a small number of genuinely suitable projects on the details that matter.</p>
            </div>
          </div>
          <div class="guide-step-roles">
            <div class="guide-role"><span>What You Do</span><p>Share your budget, areas and requirements.</p></div>
            <div class="guide-role"><span>What Nueva Living Does</span><p>Compares confirmed current pricing, availability and developer track record across projects for you.</p></div>
          </div>
          <details class="guide-step-more">
            <summary>Good to know: do I need to be in Spain to start?</summary>
            <p>No. Most of this stage -- comparing projects, reviewing floorplans and pricing, even a private cinematic presentation of a project -- can be done remotely before you commit to a viewing trip.</p>
          </details>
        </article>
        <article class="guide-step g-reveal">
          <div class="guide-step-head">
            <span class="guide-step-index">03</span>
            <div class="guide-step-body">
              <h3>View the Projects</h3>
              <p>For off-plan projects this usually means visiting the site and a show apartment if one exists. For completed developments, you view the actual residence you would be buying.</p>
            </div>
          </div>
          <div class="guide-step-roles">
            <div class="guide-role"><span>What You Do</span><p>Plan and attend the viewing trip, or a remote presentation first.</p></div>
            <div class="guide-role"><span>What Nueva Living Does</span><p>Arranges viewings and show apartments, ideally two or three projects on one trip for real comparison.</p></div>
          </div>
        </article>
        <article class="guide-step g-reveal">
          <div class="guide-step-head">
            <span class="guide-step-index">04</span>
            <div class="guide-step-body">
              <h3>Reserve Your Chosen Residence</h3>
              <p>A reservation takes the specific residence off the market while your private purchase contract is prepared, typically within two to four weeks.</p>
            </div>
          </div>
          <div class="guide-step-roles">
            <div class="guide-role"><span>What You Do</span><p>Pay the reservation amount, which is later credited against the purchase price.</p></div>
            <div class="guide-role"><span>What Nueva Living Does</span><p>Confirms the reservation terms and what happens to the amount if you do not proceed.</p></div>
          </div>
          <details class="guide-step-more">
            <summary>Good to know: how much is the reservation?</summary>
            <p>It varies by developer and project, from a few thousand euros up to around 1% of the price on some developments. A reservation is not the point of no return, but it is a real commitment -- confirm the terms before you pay it.</p>
          </details>
        </article>
        <article class="guide-step g-reveal">
          <div class="guide-step-head">
            <span class="guide-step-index">05</span>
            <div class="guide-step-body">
              <h3>Sign the Private Purchase Contract</h3>
              <p>The binding agreement setting out price, payment schedule, specification and delivery terms. You will need an NIE before or shortly after this stage.</p>
            </div>
          </div>
          <div class="guide-step-roles">
            <div class="guide-role"><span>What You Do</span><p>Obtain your NIE if you do not already have one, and review the contract.</p></div>
            <div class="guide-role"><span>What Nueva Living Does</span><p>Coordinates the paperwork and timeline with the developer.</p></div>
            <div class="guide-role"><span>What Your Lawyer Does</span><p>Reviews the contract terms and confirms the bank guarantee before you sign.</p></div>
          </div>
          <details class="guide-step-more">
            <summary>Good to know: what if the developer does not finish the project?</summary>
            <p>For off-plan purchases, payments from this point are usually staged across construction milestones. Spanish law requires developers to bank-guarantee off-plan payments made before completion, so staged payments are protected if the development is not delivered -- confirming that guarantee is in place is one of the checks your lawyer carries out.</p>
          </details>
        </article>
        <article class="guide-step g-reveal">
          <div class="guide-step-head">
            <span class="guide-step-index">06</span>
            <div class="guide-step-body">
              <h3>Legal Checks and Independent Representation</h3>
              <p>We strongly recommend independent legal representation -- a lawyer acting for you, not the developer or the selling agency.</p>
            </div>
          </div>
          <div class="guide-step-roles">
            <div class="guide-role"><span>What You Do</span><p>Instruct an independent lawyer before signing anything binding.</p></div>
            <div class="guide-role"><span>What Nueva Living Does</span><p>Can introduce you to independent lawyers experienced in Costa del Sol property.</p></div>
            <div class="guide-role"><span>What Your Lawyer Does</span><p>Checks the developer's registration and track record, the building licence, land registry status and the bank guarantee.</p></div>
          </div>
          <details class="guide-step-more">
            <summary>Good to know: financing</summary>
            <p>Many non-resident buyers arrange a mortgage at this stage. Spanish banks do lend to non-residents, usually financing a portion of the price, though exact terms depend on the bank and your financial profile.</p>
          </details>
        </article>
        <article class="guide-step g-reveal">
          <div class="guide-step-head">
            <span class="guide-step-index">07</span>
            <div class="guide-step-body">
              <h3>Completion and Handover</h3>
              <p>Completion happens at the notary, where the final balance is paid and the deed of sale is signed and registered in your name.</p>
            </div>
          </div>
          <div class="guide-step-roles">
            <div class="guide-role"><span>What You Do</span><p>Pay the final balance and sign at the notary.</p></div>
            <div class="guide-role"><span>What Nueva Living Does</span><p>Coordinates handover and helps you inspect the property against the agreed specification.</p></div>
            <div class="guide-role"><span>What Your Lawyer Does</span><p>Confirms the deed of sale and its registration.</p></div>
          </div>
          <details class="guide-step-more">
            <summary>Good to know: warranties and ongoing costs</summary>
            <p>Spanish building law generally provides for a structural warranty, a shorter warranty on installations, and a one-year warranty on finishes. After completion, budgeting for ongoing costs such as community fees and annual property tax (IBI) becomes part of owning the home. For the one-off taxes and fees due at purchase, see our <a href="guide-purchase-costs-andalucia.html">breakdown of new-build purchase costs in Andalucia</a>.</p>
          </details>
        </article>
      </div>
    </div></section>
    <section class="section quiet-band"><div class="section-inner">
      <div class="section-head center g-reveal"><span class="label">Before You Start</span><div class="rule" style="margin-left:auto;margin-right:auto;"></div><h2 class="section-title">A quick <em>checklist</em></h2></div>
      <div class="guide-checklist g-reveal" data-guide-checklist data-checklist-id="how-buying-works">
        <div class="guide-checklist-progress">
          <div class="guide-checklist-progress-track"><div class="guide-checklist-progress-fill" data-checklist-fill></div></div>
          <span class="guide-checklist-count" data-checklist-count>0 of 7</span>
        </div>
        <div class="guide-checklist-list">
          <label class="guide-check-item"><input type="checkbox" data-checklist-item="budget"><span>Define your budget</span></label>
          <label class="guide-check-item"><input type="checkbox" data-checklist-item="offplan"><span>Decide off-plan or completed</span></label>
          <label class="guide-check-item"><input type="checkbox" data-checklist-item="nie"><span>Apply for your NIE</span></label>
          <label class="guide-check-item"><input type="checkbox" data-checklist-item="lawyer"><span>Select an independent lawyer</span></label>
          <label class="guide-check-item"><input type="checkbox" data-checklist-item="bank"><span>Consider a Spanish bank account</span></label>
          <label class="guide-check-item"><input type="checkbox" data-checklist-item="funds"><span>Prepare proof of funds</span></label>
          <label class="guide-check-item"><input type="checkbox" data-checklist-item="use"><span>Clarify how you will use the property</span></label>
        </div>
        <button type="button" class="guide-checklist-reset" data-checklist-reset>Reset Checklist</button>
      </div>
    </div></section>
    <section class="section"><div class="section-inner">
      <div class="section-head center g-reveal"><span class="label">Key Terms</span><div class="rule" style="margin-left:auto;margin-right:auto;"></div><h2 class="section-title">A short <em>glossary</em></h2></div>
      <div class="guide-glossary g-reveal">
        <details class="guide-glossary-item"><summary>NIE</summary><p>Numero de Identificacion de Extranjero -- a Spanish tax ID number required for any property purchase by a non-Spanish national.</p></details>
        <details class="guide-glossary-item"><summary>Reservation Agreement</summary><p>The document and payment that takes a specific residence off the market while your private purchase contract is prepared.</p></details>
        <details class="guide-glossary-item"><summary>Private Purchase Contract</summary><p>Contrato de compraventa -- the binding agreement setting out price, payment schedule, specification and delivery terms.</p></details>
        <details class="guide-glossary-item"><summary>Bank Guarantee</summary><p>Legally required protection for off-plan payments made before completion, covering you if the development is not delivered.</p></details>
        <details class="guide-glossary-item"><summary>Notary</summary><p>The public official before whom the final deed of sale is signed at completion.</p></details>
        <details class="guide-glossary-item"><summary>Escritura</summary><p>The deed of sale signed at the notary and registered in your name at completion.</p></details>
        <details class="guide-glossary-item"><summary>Land Registry</summary><p>The official record of property ownership and charges, checked by your lawyer before you sign.</p></details>
      </div>
    </div></section>
    ${generalFaqSection()}
    <div class="section-inner"><p class="guide-disclaimer g-reveal">This guide is general information about the typical off-plan buying process on the Costa del Sol. It is not legal, tax or financial advice, and does not replace independent professional advice tailored to your situation.</p></div>
    <section class="cta-band"><div class="cta-inner"><div><span class="label">Ready to Start</span><h2 class="cta-title">Let's find your fit.</h2></div><a class="btn" href="contact.html#contact-form">Start Your Search</a></div></section>
    <script>
      (() => {
        const items = document.querySelectorAll('.g-reveal');
        if (!items.length) return;
        const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        if (reducedMotion || !('IntersectionObserver' in window)) {
          items.forEach((item) => item.classList.add('in'));
          return;
        }
        const observer = new IntersectionObserver((entries) => {
          entries.forEach((entry) => {
            if (!entry.isIntersecting) return;
            entry.target.classList.add('in');
            observer.unobserve(entry.target);
          });
        }, { threshold: 0.12 });
        items.forEach((item) => observer.observe(item));
      })();
      (() => {
        document.querySelectorAll('[data-guide-checklist]').forEach((panel) => {
          const id = panel.dataset.checklistId || 'default';
          const storageKey = \`nueva-guide-checklist-\${id}\`;
          const checkboxes = [...panel.querySelectorAll('[data-checklist-item]')];
          const fill = panel.querySelector('[data-checklist-fill]');
          const count = panel.querySelector('[data-checklist-count]');
          const resetBtn = panel.querySelector('[data-checklist-reset]');

          function readState() {
            try {
              return JSON.parse(window.localStorage.getItem(storageKey) || '{}');
            } catch (err) {
              return {};
            }
          }

          function writeState(state) {
            try {
              window.localStorage.setItem(storageKey, JSON.stringify(state));
            } catch (err) {
              /* localStorage unavailable; checklist still works for this session */
            }
          }

          function render() {
            const checked = checkboxes.filter((box) => box.checked).length;
            const pct = checkboxes.length ? Math.round((checked / checkboxes.length) * 100) : 0;
            if (fill) fill.style.width = \`\${pct}%\`;
            if (count) count.textContent = \`\${checked} of \${checkboxes.length}\`;
          }

          const saved = readState();
          checkboxes.forEach((box) => {
            const key = box.dataset.checklistItem;
            if (saved[key]) box.checked = true;
            box.addEventListener('change', () => {
              const state = readState();
              state[box.dataset.checklistItem] = box.checked;
              writeState(state);
              render();
            });
          });

          if (resetBtn) {
            resetBtn.addEventListener('click', () => {
              checkboxes.forEach((box) => { box.checked = false; });
              writeState({});
              render();
            });
          }

          render();
        });
      })();
    </script>`,
  },
  {
    file: 'guide-bank-guarantee-off-plan-spain.html',
    datePublished: '2026-08-24',
    title: 'Bank Guarantees on Off-Plan Property in Spain',
    description: 'How Spanish law protects off-plan deposits: the segregated account, the aval or seguro de caucion, and why cover starts at the building licence.',
    heroImage: 'assets/nueva/journey/reservation-legal-1200.webp',
    heroKicker: 'Buying Guide',
    seoContext: 'Bank Guarantees on Off-Plan Property \u00b7 2026 Guide',
    heroTitle: 'What actually protects <em>your deposit</em>',
    heroLead: 'Spanish law guarantees the money you pay during construction. It does not guarantee all of it, from the moment you pay it, and the gap is where buyers get caught.',
    breadcrumbs: [['Guides', 'guides.html']],
    bodyClass: 'guide-article-page',
    // English only: statutory content we have verified against the
    // consolidated text of the law. We do not publish translations of it
    // that have not been through native-language legal review.
    body: `<section class="section"><div class="section-inner">
      <div class="guide-intro g-reveal">
        <p class="body-copy">When you buy off-plan you pay for a home that does not exist yet. Spanish law answers that with a specific mechanism: the money you hand over during construction has to be guaranteed, held apart from the developer's own funds, and returned with interest if the home is never delivered. Knowing exactly how that protection works -- and the one point at which it does not yet apply -- is the difference between an informed off-plan purchase and a hopeful one.</p>
        <div class="guide-cta-row" style="display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin-top:22px;">
          <a class="btn" href="#gap">The Pre-Licence Gap</a>
          <a class="btn ghost" href="contact.html#contact-form">Ask About a Specific Project</a>
        </div>
      </div>
    </div></section>

    <section class="section"><div class="section-inner">
      <div class="section-head center g-reveal"><span class="label">The Law As It Stands</span><div class="rule" style="margin-left:auto;margin-right:auto;"></div><h2 class="section-title">Ley 38/1999, <em>not Ley 57/1968</em></h2></div>
      <p class="body-copy g-reveal">A great deal of English-language material about Spanish off-plan purchases still cites Ley 57/1968 as the source of your protection. That law was repealed with effect from 1 January 2016. Its regime was carried over, with changes, into the first additional provision of Ley 38/1999 (the Ley de Ordenaci&oacute;n de la Edificaci&oacute;n), in the wording given to it by Ley 20/2015. If a page tells you Ley 57/1968 protects your deposit today, it has not been updated in a decade -- and the changes are not cosmetic.</p>
    </div></section>

    <section class="section"><div class="section-inner">
      <div class="section-head center g-reveal"><span class="label">What The Developer Must Do</span><div class="rule" style="margin-left:auto;margin-right:auto;"></div><h2 class="section-title">Four obligations, <em>not one</em></h2></div>
      <div class="guide-compare-grid g-reveal">
        <div class="guide-compare-row"><div class="guide-compare-label">A segregated account</div><div><p>Advance payments must be received through a credit institution and deposited in a special account, kept separate from any other class of funds. Money may only leave that account for costs arising directly from the construction of those homes. It is not the developer's working capital.</p></div></div>
        <div class="guide-compare-row"><div class="guide-compare-label">A guarantee</div><div><p>Repayment must be guaranteed, either by a <em>seguro de cauci&oacute;n</em> with an insurer authorised to operate in Spain, or by an <em>aval solidario</em> issued by an authorised credit institution. Both are acceptable; what matters is that one of them exists and names you.</p></div></div>
        <div class="guide-compare-row"><div class="guide-compare-label">Disclosure in the contract</div><div><p>The purchase contract itself must state the developer's obligation to repay, identify the insurer or guarantor, and identify the credit institution and the account. At signing you should also be handed the document evidencing the guarantee attached to your particular payments.</p></div></div>
        <div class="guide-compare-row"><div class="guide-compare-label">Consequences of skipping it</div><div><p>Failing to put the guarantee in place is treated as a consumer-protection infringement, carrying a penalty of up to 25% of the amounts that should have been secured, on top of anything the regional building rules impose.</p></div></div>
      </div>
    </div></section>

    <section class="section" id="gap"><div class="section-inner">
      <div class="section-head center g-reveal"><span class="label">The Part Most Guides Omit</span><div class="rule" style="margin-left:auto;margin-right:auto;"></div><h2 class="section-title">The guarantee starts at <em>the building licence</em></h2></div>
      <p class="body-copy g-reveal">The obligation to guarantee repayment runs from the point the building licence is obtained -- not from the moment you first pay. This is one of the substantive differences between the current regime and the 1968 law it replaced, and it is the single most practical thing to understand before you reserve.</p>
      <p class="body-copy g-reveal">In plain terms: if you pay a reservation fee on a project whose licence has not yet been granted, that money is not sitting behind the statutory guarantee. It may well be protected by what your contract says instead -- many reservation agreements make the fee refundable during a due-diligence window, and that is a contractual protection, not a legal one. The two are not interchangeable, and only one of them is the same at every developer.</p>
      <p class="body-copy g-reveal">This is not a reason to avoid pre-licence projects. It is a reason to know which category a project is in before you transfer anything, and to have your lawyer read the reservation terms rather than assume the statute covers you. Every project on this site states its licence status in its own trust dossier, in those words, because the distinction changes what your money is standing on.</p>
    </div></section>

    <section class="section"><div class="section-inner">
      <div class="section-head center g-reveal"><span class="label">If It Goes Wrong</span><div class="rule" style="margin-left:auto;margin-right:auto;"></div><h2 class="section-title">What you can <em>actually recover</em></h2></div>
      <p class="body-copy g-reveal">If construction does not begin, is not finished within the agreed period, or the habitation certificate is not obtained, you may claim back the amounts paid on account -- including the taxes applied to them -- plus statutory interest. You can either terminate the contract or grant the developer an extension, which is recorded as an additional clause setting the new delivery date.</p>
      <p class="body-copy g-reveal">The practical lesson is that the guarantee is only as useful as the paperwork behind it. Ask for the guarantee document at signing, check it names you and your specific payments, and keep it. A guarantee that exists in principle but was never issued to you is the failure mode this provision was written to prevent.</p>
    </div></section>

    <section class="section"><div class="section-inner">
      <div class="section-head center g-reveal"><span class="label">Before You Rely On This</span><div class="rule" style="margin-left:auto;margin-right:auto;"></div><h2 class="section-title">Sourced from the <em>consolidated statute</em></h2></div>
      <p class="body-copy g-reveal">The obligations described on this page are taken from the first additional provision of Ley 38/1999 as consolidated after Ley 20/2015, and are current as of August 2026. This is general information about how the protection is structured; it is not legal advice, and how it applies to a particular contract is a question for your own lawyer. Nueva Living confirms licence status and guarantee arrangements in writing for a specific project on request.</p>
      <div class="guide-cta-row" style="display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin-top:22px;">
        <a class="btn" href="contact.html#contact-form">Check a Project's Licence Status</a>
        <a class="btn ghost" href="guide-off-plan-payment-schedules.html">How Payments Are Staged</a>
      </div>
    </div></section>`,
  },
  {
    file: 'guide-off-plan-payment-schedules.html',
    datePublished: '2026-08-24',
    title: 'Off-Plan Payment Schedules on the Costa del Sol',
    description: 'Real staged payment schedules from Costa del Sol developers: reservation fees, the 30% contract stage, construction milestones and the balance at deed.',
    heroImage: 'assets/nueva/journey/project-review-v2-1200.webp',
    heroKicker: 'Buying Guide',
    seoContext: 'Off-Plan Payment Schedules \u00b7 2026 Guide',
    heroTitle: 'How off-plan payments <em>are actually staged</em>',
    heroLead: 'Not an averaged range borrowed from elsewhere: the schedules the developers of the projects on this site have supplied in writing.',
    breadcrumbs: [['Guides', 'guides.html']],
    bodyClass: 'guide-article-page',
    // English only: statutory content we have verified against the
    // consolidated text of the law. We do not publish translations of it
    // that have not been through native-language legal review.
    body: `<section class="section"><div class="section-inner">
      <div class="guide-intro g-reveal">
        <p class="body-copy">Off-plan purchases are paid in stages, and the stages are not standardised. The figures below are not a market average taken from elsewhere -- they are the actual schedules supplied by the developers of the projects listed on this site, which is why the ranges are narrower and less tidy than the ones you will read in a generic guide.</p>
        <div class="guide-cta-row" style="display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin-top:22px;">
          <a class="btn" href="#stages">The Four Stages</a>
          <a class="btn ghost" href="developments.html">See the Developments</a>
        </div>
      </div>
    </div></section>

    <section class="section" id="stages"><div class="section-inner">
      <div class="section-head center g-reveal"><span class="label">What We Actually See</span><div class="rule" style="margin-left:auto;margin-right:auto;"></div><h2 class="section-title">Reservation, contract, <em>build, deed</em></h2></div>
      <p class="body-copy g-reveal">Across the projects on this site where the developer has supplied a written schedule, the shape is consistent even though the numbers move.</p>
      <div class="guide-compare-grid g-reveal">
        <div class="guide-compare-row"><div class="guide-compare-label">Reservation</div><div><p>Either a fixed sum or a percentage. We see fixed reservations from &euro;6,000 to &euro;10,000, and percentage reservations from 1% to 5%. This takes the unit off the market for an agreed period while contracts are prepared.</p></div></div>
        <div class="guide-compare-row"><div class="guide-compare-label">Private purchase contract</div><div><p>Typically bringing the total paid to 30%, with the reservation usually counted towards it. Some developers stage this as 25% at contract with the balance spread across the build. Signing windows are short -- 15 to 30 days from reservation is normal.</p></div></div>
        <div class="guide-compare-row"><div class="guide-compare-label">During construction</div><div><p>Highly variable. Some projects take nothing between contract and completion; others take 10% at a fixed date, or tie payments to certified milestones such as completion of the foundation and of the structure. One project on this site spreads 50% across fifteen monthly payments from the start of works.</p></div></div>
        <div class="guide-compare-row"><div class="guide-compare-label">Completion</div><div><p>The balance at the deed of sale, most often 50% to 70%. This is also where the bulk of the tax falls due.</p></div></div>
      </div>
      <p class="body-copy g-reveal">Note that stage payments are quoted plus VAT in most schedules, so the cash required at each stage is higher than the headline percentage. See <a href="guide-purchase-costs-andalucia.html">what a new-build costs on top of the price</a> for how IVA and AJD land across the timeline.</p>
    </div></section>

    <section class="section"><div class="section-inner">
      <div class="section-head center g-reveal"><span class="label">Reservation Agreements</span><div class="rule" style="margin-left:auto;margin-right:auto;"></div><h2 class="section-title">Market practice, <em>not statute</em></h2></div>
      <p class="body-copy g-reveal">This is worth stating plainly, because it is often blurred: there is no Spanish statute governing reservation agreements. What your reservation fee does, whether it is refundable, and for how long, is whatever your particular reservation document says. It is a contract, and its terms vary between developers.</p>
      <p class="body-copy g-reveal">That matters more than it sounds, because the statutory guarantee over advance payments only begins once the building licence has been obtained. A reservation paid before that point rests on the contract wording alone. Some agreements make the fee refundable for a defined due-diligence window; others do not. Read it, or have your lawyer read it, before transferring anything -- and see <a href="guide-bank-guarantee-off-plan-spain.html">how the bank guarantee works</a> for what changes once the licence is in place.</p>
    </div></section>

    <section class="section"><div class="section-inner">
      <div class="section-head center g-reveal"><span class="label">Where The Money Sits</span><div class="rule" style="margin-left:auto;margin-right:auto;"></div><h2 class="section-title">Not the developer's <em>working capital</em></h2></div>
      <p class="body-copy g-reveal">Once the guarantee regime applies, amounts you pay on account must be received through a credit institution and held in a special account, separate from any other class of funds, and may only be drawn for costs arising directly from building those homes. If a developer proposes any other arrangement for staged payments, that is the point to stop and take advice.</p>
    </div></section>

    <section class="section"><div class="section-inner">
      <div class="section-head center g-reveal"><span class="label">Before You Rely On This</span><div class="rule" style="margin-left:auto;margin-right:auto;"></div><h2 class="section-title">Schedules change <em>per project</em></h2></div>
      <p class="body-copy g-reveal">The ranges above describe the written schedules held for the projects listed on this site as of August 2026. They are not a rule, and they are not an offer -- an individual developer can and does structure payments differently, and terms change between releases. Nueva Living reconfirms the current payment structure in writing for a specific residence before any reservation. This page is general information, not legal, tax or financial advice.</p>
      <div class="guide-cta-row" style="display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin-top:22px;">
        <a class="btn" href="contact.html#contact-form">Request a Payment Structure</a>
        <a class="btn ghost" href="guide-how-buying-works.html">How Buying a New-Build Works</a>
      </div>
    </div></section>`,
  },
  {
    file: 'guide-new-build-warranties-snagging.html',
    datePublished: '2026-08-24',
    title: 'New-Build Warranties and Snagging in Spain',
    description: 'The ten, three and one-year guarantees on a Spanish new-build: who is liable under each, which one is insured by law, and when the clock starts.',
    heroImage: 'assets/nueva/journey/completion-aftercare-1200.webp',
    heroKicker: 'Buying Guide',
    seoContext: 'New-Build Warranties and Snagging \u00b7 2026 Guide',
    heroTitle: 'Three warranties, <em>three different clocks</em>',
    heroLead: 'A Spanish new-build carries ten, three and one-year cover against defects. They start on the same day, point at different parties, and only one of them is insured by law.',
    breadcrumbs: [['Guides', 'guides.html']],
    bodyClass: 'guide-article-page',
    // English only: statutory content we have verified against the
    // consolidated text of the law. We do not publish translations of it
    // that have not been through native-language legal review.
    englishOnly: true,
    body: `<section class="section"><div class="section-inner">
      <div class="guide-intro g-reveal">
        <p class="body-copy">A new-build comes with statutory cover against defects, and it is not one warranty but three, each running for a different length of time and each pointing at a different party. Knowing which clock applies to a given problem is what turns a snagging list from a favour the developer might do into a claim with a legal basis.</p>
        <div class="guide-cta-row" style="display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin-top:22px;">
          <a class="btn" href="#periods">The Three Periods</a>
          <a class="btn ghost" href="contact.html#contact-form">Ask About a Specific Project</a>
        </div>
      </div>
    </div></section>

    <section class="section" id="periods"><div class="section-inner">
      <div class="section-head center g-reveal"><span class="label">Article 17, Ley 38/1999</span><div class="rule" style="margin-left:auto;margin-right:auto;"></div><h2 class="section-title">Ten years, three years, <em>one year</em></h2></div>
      <p class="body-copy g-reveal">All three periods run from the date the works are formally received without reservations -- or, where reservations were made, from the date those are put right. Not from when you move in, and not from the deed.</p>
      <div class="guide-compare-grid g-reveal">
        <div class="guide-compare-row"><div class="guide-compare-label">10 years &middot; structural</div><div><p>Damage caused by defects affecting the foundations, supports, beams, floor slabs, load-bearing walls or other structural elements. The building agents are liable.</p></div></div>
        <div class="guide-compare-row"><div class="guide-compare-label">3 years &middot; habitability</div><div><p>Damage from defects in construction elements or installations that cause the building to fail the habitability requirements -- damp penetration, insulation, water, heating and similar.</p></div></div>
        <div class="guide-compare-row"><div class="guide-compare-label">1 year &middot; finishes</div><div><p>Defects of execution affecting elements of finish or trim. Here the constructor alone is liable, which is a narrower answer than the other two periods give you.</p></div></div>
      </div>
    </div></section>

    <section class="section"><div class="section-inner">
      <div class="section-head center g-reveal"><span class="label">Insurance</span><div class="rule" style="margin-left:auto;margin-right:auto;"></div><h2 class="section-title">Only one of the three <em>is insured by law</em></h2></div>
      <p class="body-copy g-reveal">Liability and insurance are not the same thing, and this is where expectations often run ahead of the statute. For buildings whose main use is housing, only the ten-year structural cover is compulsory insurance. The one-year and three-year guarantees remain liabilities of the parties rather than insurances that must be in place, pending implementing regulation that has not arrived.</p>
      <p class="body-copy g-reveal">In practice this means a structural problem has an insurer standing behind it, while a three-year habitability defect is a claim against the agents involved. Both are real; they are not equally easy to enforce, and it is worth knowing which one you are in before a dispute rather than during it.</p>
    </div></section>

    <section class="section"><div class="section-inner">
      <div class="section-head center g-reveal"><span class="label">At Handover</span><div class="rule" style="margin-left:auto;margin-right:auto;"></div><h2 class="section-title">The snagging list <em>is the clock-starter</em></h2></div>
      <p class="body-copy g-reveal">Because the periods run from reception of the works, and because reservations noted at reception shift the start date until they are put right, the handover inspection is not a formality. Recording defects in writing at that point is what fixes the date and creates the record you would later rely on.</p>
      <p class="body-copy g-reveal">Snagging inspections themselves are market practice rather than a statutory step -- there is no law requiring one, and no prescribed format. What the law does is define the periods and the liabilities that an inspection lets you use. A written, dated list, delivered to the developer, is the practical bridge between the two.</p>
    </div></section>

    <section class="section"><div class="section-inner">
      <div class="section-head center g-reveal"><span class="label">Before You Rely On This</span><div class="rule" style="margin-left:auto;margin-right:auto;"></div><h2 class="section-title">Sourced from the <em>consolidated statute</em></h2></div>
      <p class="body-copy g-reveal">The periods and liabilities described here are taken from articles 17 and 19 of Ley 38/1999 and its second additional provision, as consolidated, and are current as of August 2026. This page is general information about how the cover is structured, not legal advice. Whether a particular defect falls in a particular period is a question of fact for your lawyer and, usually, a surveyor. Nueva Living can provide the warranty and insurance documentation held for a specific project on request.</p>
      <div class="guide-cta-row" style="display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin-top:22px;">
        <a class="btn" href="contact.html#contact-form">Request Warranty Documentation</a>
        <a class="btn ghost" href="guide-bank-guarantee-off-plan-spain.html">How the Bank Guarantee Works</a>
      </div>
    </div></section>`,
  },
  {
    file: 'guide-purchase-costs-andalucia.html',
    datePublished: '2026-08-24',
    title: 'New-Build Purchase Costs in Andalucia',
    description: 'New-build in Andalucia in 2026: IVA at 10%, AJD at 1.2%, plus notary, land registry and legal fees, and the reduced stamp-duty rates that can apply.',
    heroImage: 'assets/liora/viewing/scene-13.jpg',
    heroKicker: 'Buying Guide',
    seoContext: 'New-Build Purchase Costs in Andalucia \u00b7 2026 Guide',
    heroTitle: 'What a new-build costs <em>on top of the price</em>',
    heroLead: 'Every competitor writes a Spain-wide cost guide quoting 8 to 13 per cent. New-build in Andalucia is a specific number, and it is knowable before you offer.',
    breadcrumbs: [['Guides', 'guides.html']],
    bodyClass: 'guide-article-page',
    body: `<section class="section"><div class="section-inner">
      <div class="guide-intro g-reveal">
        <p class="body-copy">Most cost guides for Spain quote a single national range, usually somewhere between 8 and 13 per cent. That range exists because it is averaging two different purchases across seventeen regions. For a new-build in Andaluc&iacute;a the tax side is not a range at all -- it is two fixed rates, and you can work out the number exactly.</p>
        <div class="guide-cta-row" style="display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin-top:22px;">
          <a class="btn" href="#taxes">See the Breakdown</a>
          <a class="btn ghost" href="contact.html#contact-form">Ask About a Specific Project</a>
        </div>
      </div>
    </div></section>

    <section class="section" id="taxes"><div class="section-inner">
      <div class="section-head center g-reveal"><span class="label">The Two Taxes</span><div class="rule" style="margin-left:auto;margin-right:auto;"></div><h2 class="section-title">IVA and AJD, <em>not transfer tax</em></h2></div>
      <p class="body-copy g-reveal">A new-build bought from the developer is a first transmission, so it carries VAT rather than the transfer tax that applies to a resale. In Andaluc&iacute;a that means two separate taxes on the same purchase.</p>
      <div class="guide-compare-grid g-reveal">
        <div class="guide-compare-row"><div class="guide-compare-label">IVA (VAT)</div><div><p><strong>10% of the purchase price.</strong> The national rate for new residential property. It drops to 4% for officially protected housing (VPO de r&eacute;gimen especial), which does not apply to the developments on this site.</p></div></div>
        <div class="guide-compare-row"><div class="guide-compare-label">AJD (stamp duty)</div><div><p><strong>1.2% of the purchase price</strong> in Andaluc&iacute;a. This is the regional rate, set at 1.2% since April 2021 and made permanent by the region's Ley 5/2021. Older guides still quote 1.5%, which was the rate before that change.</p></div></div>
        <div class="guide-compare-row"><div class="guide-compare-label">Total tax</div><div><p><strong>11.2%</strong> on a new-build. For comparison, a resale in Andaluc&iacute;a carries ITP at 7% and no AJD -- so the tax on a new home is roughly four points higher than on an equivalent resale.</p></div></div>
      </div>
    </div></section>

    <section class="section"><div class="section-inner">
      <div class="section-head center g-reveal"><span class="label">Reduced Rates</span><div class="rule" style="margin-left:auto;margin-right:auto;"></div><h2 class="section-title">When AJD is <em>lower than 1.2%</em></h2></div>
      <p class="body-copy g-reveal">Andaluc&iacute;a applies reduced AJD rates in specific circumstances. They are worth checking before you assume the general rate, though most purchases on this coast fall outside them.</p>
      <div class="cards g-reveal">
        <article class="card"><h3>1%</h3><p>Where the property value does not exceed &euro;150,000 and it will be the buyer's habitual residence.</p></article>
        <article class="card"><h3>0.3%</h3><p>Where the buyer is under 35 and the property will be their habitual residence.</p></article>
        <article class="card"><h3>0.1%</h3><p>For large families (familia numerosa) and for buyers with a recognised disability, subject to the region's conditions.</p></article>
      </div>
    </div></section>

    <section class="section"><div class="section-inner">
      <div class="section-head center g-reveal"><span class="label">On Top of Tax</span><div class="rule" style="margin-left:auto;margin-right:auto;"></div><h2 class="section-title">Notary, registry <em>and legal fees</em></h2></div>
      <p class="body-copy g-reveal">Notary and Land Registry fees are set by national tariff, so they do not vary between providers. Legal fees do.</p>
      <div class="guide-compare-grid g-reveal">
        <div class="guide-compare-row"><div class="guide-compare-label">Notary</div><div><p>Roughly &euro;600 to &euro;1,200 on a typical residential purchase, scaling with the price and the length of the deed. Regulated, so shopping around does not change it.</p></div></div>
        <div class="guide-compare-row"><div class="guide-compare-label">Land Registry</div><div><p>Roughly &euro;400 to &euro;700. Also regulated.</p></div></div>
        <div class="guide-compare-row"><div class="guide-compare-label">Legal</div><div><p>Typically 1% of the price plus 21% IVA on the fee, or a fixed quote in the &euro;1,500 to &euro;3,000 range for a straightforward purchase. This one is negotiable, and it is the line worth comparing quotes on.</p></div></div>
      </div>
    </div></section>

    <section class="section"><div class="section-inner">
      <div class="section-head center g-reveal"><span class="label">Worked Example</span><div class="rule" style="margin-left:auto;margin-right:auto;"></div><h2 class="section-title">A &euro;450,000 <em>new-build</em></h2></div>
      <div class="guide-compare-grid g-reveal">
        <div class="guide-compare-row"><div class="guide-compare-label">IVA at 10%</div><div><p>&euro;45,000</p></div></div>
        <div class="guide-compare-row"><div class="guide-compare-label">AJD at 1.2%</div><div><p>&euro;5,400</p></div></div>
        <div class="guide-compare-row"><div class="guide-compare-label">Notary and registry</div><div><p>Roughly &euro;1,000 to &euro;1,900</p></div></div>
        <div class="guide-compare-row"><div class="guide-compare-label">Legal</div><div><p>Roughly &euro;4,500 plus IVA at 1%, or a fixed quote</p></div></div>
        <div class="guide-compare-row"><div class="guide-compare-label">Budget for</div><div><p><strong>Around &euro;57,000, or about 12.5% over the price.</strong> Taxes are the fixed &euro;50,400 of that; the rest moves with who you instruct.</p></div></div>
      </div>
      <p class="body-copy g-reveal">That is the acquisition cost. It does not include mortgage arrangement and valuation fees if you are borrowing, furnishing, or the running costs that start after completion -- IBI, community fees and utilities.</p>
    </div></section>

    <section class="section"><div class="section-inner">
      <div class="section-head center g-reveal"><span class="label">Before You Rely On This</span><div class="rule" style="margin-left:auto;margin-right:auto;"></div><h2 class="section-title">Figures current at <em>August 2026</em></h2></div>
      <p class="body-copy g-reveal">The IVA rate is national and the AJD rate is set by Andaluc&iacute;a; both can change, and the reduced rates carry conditions that depend on your circumstances. This page is general information about how the costs are structured, not tax or legal advice. Confirm the figures for your own purchase with your lawyer or tax adviser before you commit to anything. Nueva Living provides a written cost breakdown for a specific residence on request.</p>
      <div class="guide-cta-row" style="display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin-top:22px;">
        <a class="btn" href="contact.html#contact-form">Request a Cost Breakdown</a>
        <a class="btn ghost" href="guide-how-buying-works.html">How Buying a New-Build Works</a>
      </div>
    </div></section>`,
  },
  {
    file: 'guide-off-plan-vs-resale.html',
    datePublished: '2026-08-12',
    title: 'Off-Plan vs Resale',
    description: 'How buying off-plan and buying a completed resale home actually compare on the Costa del Sol, across price, risk, payment terms and appreciation.',
    heroImage: 'assets/liora/projects/altos-de-marbella/media/aerial-dusk-pool.jpg',
    heroKicker: 'Buying Guide',
    seoContext: 'Off-Plan vs Resale on the Costa del Sol \u00b7 2026 Guide',
    heroTitle: 'Off-plan vs resale: <em>which fits your plan</em>',
    heroLead: 'Both are legitimate ways to buy on the Costa del Sol. The right one depends on your timeline, your appetite for construction risk, and what you actually want the property to do for you.',
    bodyClass: 'guide-article-page',
    body: `<section class="section"><div class="section-inner">
      <div class="guide-intro g-reveal">
        <p class="body-copy">Neither is inherently the better investment -- they suit different buyers, timelines and risk tolerances. Compare them below on the points that actually affect your decision.</p>
        <div class="guide-cta-row" style="display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin-top:22px;">
          <a class="btn" href="#compare">Compare Now</a>
          <a class="btn ghost" href="contact.html#contact-form">Speak With an Advisor</a>
        </div>
      </div>
    </div></section>
    <section class="section" id="compare"><div class="section-inner">
      <div class="section-head center g-reveal"><span class="label">Side by Side</span><div class="rule" style="margin-left:auto;margin-right:auto;"></div><h2 class="section-title">Off-plan <em>or completed</em></h2></div>
      <div class="guide-tabs g-reveal" data-guide-tabs>
        <div class="guide-tablist" role="tablist" aria-label="Off-plan vs resale comparison">
          <button type="button" class="guide-tab" id="tab-offplan" role="tab" aria-selected="true" aria-controls="panel-offplan" data-tab-target="panel-offplan">Off-Plan / New Development</button>
          <button type="button" class="guide-tab" id="tab-resale" role="tab" aria-selected="false" aria-controls="panel-resale" data-tab-target="panel-resale" tabindex="-1">Completed / Resale</button>
        </div>
        <div class="guide-tabpanel is-active" id="panel-offplan" role="tabpanel" aria-labelledby="tab-offplan">
          <div class="guide-compare-grid">
            <div class="guide-compare-row"><div class="guide-compare-label">Price</div><div><p>Usually priced below a comparable finished home, since you are committing years ahead of delivery and taking on construction timeline risk. That gap narrows, or closes, as a project moves toward its final released units.</p></div></div>
            <div class="guide-compare-row"><div class="guide-compare-label">Payment</div><div><p>Staged: a reservation, a larger payment on signing the private purchase contract, further payments at construction milestones, and the balance on completion.</p></div></div>
            <div class="guide-compare-row"><div class="guide-compare-label">Risk</div><div><p>Construction and delivery risk: the project could be delayed or, worst case, not completed. Payments made before completion are required by law to be bank-guaranteed.</p></div></div>
            <div class="guide-compare-row"><div class="guide-compare-label">Specification</div><div><p>Buying early sometimes means a genuine say in finishes -- flooring, kitchen options, occasionally layout -- depending how far along construction is. That window closes near completion.</p></div></div>
            <div class="guide-compare-row"><div class="guide-compare-label">Timing</div><div><p>Waiting, sometimes years, for delivery. The developer's track record for hitting its delivery date deserves real scrutiny.</p></div></div>
            <div class="guide-compare-row"><div class="guide-compare-label">Appreciation</div><div><p>The case is buying below completed-market price and the value closing that gap by delivery. This depends on the specific project and area performing as expected -- it is not a guarantee.</p></div></div>
            <div class="guide-compare-row"><div class="guide-compare-label">Snagging</div><div><p>A formal snagging inspection happens before or at handover, with defects listed for the developer to fix under the build warranty. You are working from the developer's finish standard, not judging an existing property.</p></div></div>
            <div class="guide-compare-row"><div class="guide-compare-label">Documentation</div><div><p>Completion depends on the developer obtaining the first occupation license and certificate of completion before the deed can be signed at the notary. Your lawyer confirms these are in place before you complete.</p></div></div>
            <div class="guide-compare-row"><div class="guide-compare-label">Completion</div><div><p>Happens once the building is finished and licensed, on a date the developer estimates rather than guarantees. Delays of a few months against the original estimate are not unusual.</p></div></div>
          </div>
        </div>
        <div class="guide-tabpanel" id="panel-resale" role="tabpanel" aria-labelledby="tab-resale" hidden>
          <div class="guide-compare-grid">
            <div class="guide-compare-row"><div class="guide-compare-label">Price</div><div><p>Costs more upfront, but you are paying for a known quantity: the actual finish, the actual view, the actual noise level, none of which you can fully judge from a floorplan and a render.</p></div></div>
            <div class="guide-compare-row"><div class="guide-compare-label">Payment</div><div><p>Simpler: reserve, sign, pay the balance, usually within 30 to 60 days. No construction-linked schedule, and no way to spread the cost over time.</p></div></div>
            <div class="guide-compare-row"><div class="guide-compare-label">Risk</div><div><p>Removed entirely. What you see is what you get, and you can inspect the actual property before committing to anything.</p></div></div>
            <div class="guide-compare-row"><div class="guide-compare-label">Specification</div><div><p>Fixed. A limitation if you wanted something different, an advantage if you would rather judge real materials and workmanship than a specification sheet.</p></div></div>
            <div class="guide-compare-row"><div class="guide-compare-label">Timing</div><div><p>Can generate rental income or be lived in immediately after completion, with no construction timeline in the way.</p></div></div>
            <div class="guide-compare-row"><div class="guide-compare-label">Appreciation</div><div><p>Easier to benchmark against genuinely comparable recent sales in the same building or area -- real, current data rather than a projection.</p></div></div>
            <div class="guide-compare-row"><div class="guide-compare-label">Snagging</div><div><p>Not applicable in the same way. Any defects are whatever the current owner has or has not addressed, so a professional survey before you commit matters more here than a developer warranty.</p></div></div>
            <div class="guide-compare-row"><div class="guide-compare-label">Documentation</div><div><p>Already issued and checkable: your lawyer verifies the existing title, license history and any charges on the property at the Land Registry before you sign.</p></div></div>
            <div class="guide-compare-row"><div class="guide-compare-label">Completion</div><div><p>Set by you and the seller, typically 30 to 60 days after signing, with no construction or licensing timeline to depend on.</p></div></div>
          </div>
        </div>
      </div>
      <div class="guide-callout g-reveal" style="max-width:820px;margin-left:auto;margin-right:auto;">
        <h3>Does the bank guarantee cover everything I pay?</h3>
        <p>It covers payments made ahead of completion specifically. The exact scope and validity of the guarantee for a given project is something to confirm in writing before signing, not something to assume.</p>
      </div>
    </div></section>
    <section class="section quiet-band"><div class="section-inner">
      <div class="guide-section g-reveal" style="max-width:720px;margin:0 auto;padding-top:0;">
        <div class="guide-section-head" style="justify-content:center;"><h2>Which one <em>actually fits you</em></h2></div>
        <p>Off-plan tends to suit buyers who do not need the property immediately, want to spread payments over time, and are comfortable with construction-stage risk in exchange for a lower entry price and, in some cases, a say in the finish.</p>
        <p>A completed home tends to suit buyers who want to move in, rent out, or simply see exactly what they are buying without waiting or without taking on delivery risk -- often at a higher upfront cost for that certainty.</p>
        <p>Most buyers are not purely one or the other. The honest way to decide is to compare specific projects against your own budget, timeline and risk tolerance, rather than deciding on off-plan versus resale as an abstract category first. For the full step-by-step process once you have decided, see <a href="guide-how-buying-works.html">how buying works</a>.</p>
      </div>
    </div></section>
    <section class="section"><div class="section-inner">
      <div class="section-head center g-reveal"><span class="label">Key Terms</span><div class="rule" style="margin-left:auto;margin-right:auto;"></div><h2 class="section-title">A short <em>glossary</em></h2></div>
      <div class="guide-glossary g-reveal">
        <details class="guide-glossary-item"><summary>Private Purchase Contract</summary><p>Contrato de compraventa -- the binding agreement setting out price, payment schedule, specification and delivery terms, signed after reservation.</p></details>
        <details class="guide-glossary-item"><summary>Bank Guarantee</summary><p>Legally required protection for off-plan payments made before completion, covering you if the development is not delivered.</p></details>
        <details class="guide-glossary-item"><summary>Snagging</summary><p>A formal inspection before or at handover to list defects for the developer to fix under the build warranty.</p></details>
        <details class="guide-glossary-item"><summary>First Occupation License</summary><p>Licencia de primera ocupacion -- the official confirmation a newly built home is fit to be lived in, required before completion.</p></details>
        <details class="guide-glossary-item"><summary>Comunidad de Propietarios</summary><p>The community of owners that manages and charges for shared areas and services in a development, whether off-plan or resale.</p></details>
        <details class="guide-glossary-item"><summary>Escritura</summary><p>The deed of sale signed at the notary and registered in your name at completion.</p></details>
      </div>
    </div></section>
    <div class="section-inner"><p class="body-copy g-reveal" style="text-align:center;">The two routes are also taxed differently: new-build carries IVA and AJD, resale carries ITP. See <a href="guide-purchase-costs-andalucia.html">what a new-build actually costs in Andalucia</a> for the figures.</p><p class="guide-disclaimer g-reveal">This guide is general information to help you compare off-plan and resale purchases on the Costa del Sol. It is not legal, tax or financial advice, and does not replace independent professional advice tailored to your situation.</p></div>
    <section class="cta-band"><div class="cta-inner"><div><span class="label">Compare Real Options</span><h2 class="cta-title">Not sure which fits? Let's talk.</h2></div><a class="btn" href="contact.html#contact-form">Start Your Search</a></div></section>
    <script>
      (() => {
        const items = document.querySelectorAll('.g-reveal');
        if (!items.length) return;
        const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        if (reducedMotion || !('IntersectionObserver' in window)) {
          items.forEach((item) => item.classList.add('in'));
          return;
        }
        const observer = new IntersectionObserver((entries) => {
          entries.forEach((entry) => {
            if (!entry.isIntersecting) return;
            entry.target.classList.add('in');
            observer.unobserve(entry.target);
          });
        }, { threshold: 0.12 });
        items.forEach((item) => observer.observe(item));
      })();
      (() => {
        document.querySelectorAll('[data-guide-tabs]').forEach((wrap) => {
          const tabs = [...wrap.querySelectorAll('[role="tab"]')];
          tabs.forEach((tab) => {
            tab.addEventListener('click', () => activate(tab));
            tab.addEventListener('keydown', (event) => {
              const index = tabs.indexOf(tab);
              if (event.key === 'ArrowRight') activate(tabs[(index + 1) % tabs.length], true);
              if (event.key === 'ArrowLeft') activate(tabs[(index - 1 + tabs.length) % tabs.length], true);
            });
          });

          function activate(tab, focus) {
            tabs.forEach((item) => {
              const selected = item === tab;
              item.setAttribute('aria-selected', selected ? 'true' : 'false');
              item.tabIndex = selected ? 0 : -1;
              const panel = document.getElementById(item.dataset.tabTarget);
              if (panel) {
                panel.classList.toggle('is-active', selected);
                panel.hidden = !selected;
              }
            });
            if (focus) tab.focus();
          }
        });
      })();
    </script>`,
  },
  {
    file: 'referrals.html',
    title: 'Referral & Ambassador Program',
    description: 'Introduce someone to Nueva Living and receive a share of our commission when their Costa del Sol purchase completes.',
    heroImage: 'assets/liora/projects/vega-verde-residences/media/terrace-sunset.jpg',
    heroAlt: 'Rooftop terrace lounge and dining area overlooking the Costa del Sol coastline',
    heroWidth: 1920,
    heroHeight: 1029,
    heroPosition: 'center 55%',
    heroKicker: 'Referral & Ambassador Program',
    seoContext: 'Refer a Costa del Sol Buyer, Share the Commission',
    heroTitle: 'Your introduction deserves <em>more than a thank you</em>',
    heroLead: 'The people you introduce to Nueva Living get the same private, unhurried search every client receives. When their search ends in a home, yours ends in a genuine reward.',
    bodyClass: 'ambassador-page',
    body: `<section class="section ambassador-reveal"><div class="section-inner"><div class="section-head center"><span class="label">How It Works</span><div class="rule" style="margin-left:auto;margin-right:auto;"></div><h2 class="section-title">A simple way to <em>say thank you</em></h2></div>
      <div class="ambassador-hexline">
        <div class="ambassador-hex-step ambassador-reveal" style="--reveal-delay:0ms">
          <div class="ambassador-hex"><svg viewBox="0 0 24 24" width="30" height="30" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg></div>
          <span class="ambassador-hex-num">01</span>
          <h3>Tell Us Who</h3>
          <p>Share their details in the form below.</p>
        </div>
        <div class="ambassador-hex-step ambassador-hex-step--down ambassador-reveal" style="--reveal-delay:90ms">
          <div class="ambassador-hex"><svg viewBox="0 0 24 24" width="30" height="30" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11.5 14.5 15.5 9.5"/></svg></div>
          <span class="ambassador-hex-num">02</span>
          <h3>We Confirm It&rsquo;s Genuine</h3>
          <p>We check honestly, either way.</p>
        </div>
        <div class="ambassador-hex-step ambassador-reveal" style="--reveal-delay:180ms">
          <div class="ambassador-hex"><svg viewBox="0 0 24 24" width="30" height="30" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg></div>
          <span class="ambassador-hex-num">03</span>
          <h3>We Look After Them</h3>
          <p>The same private process, every client.</p>
        </div>
        <div class="ambassador-hex-step ambassador-hex-step--down ambassador-reveal" style="--reveal-delay:270ms">
          <div class="ambassador-hex"><svg viewBox="0 0 24 24" width="30" height="30" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="20 12 20 22 4 22 4 12"/><rect x="2" y="7" width="20" height="5"/><line x1="12" y1="22" x2="12" y2="7"/><path d="M12 7H7.5a2.5 2.5 0 0 1 0-5C11 2 12 7 12 7z"/><path d="M12 7h4.5a2.5 2.5 0 0 0 0-5C13 2 12 7 12 7z"/></svg></div>
          <span class="ambassador-hex-num">04</span>
          <h3>You Get Rewarded</h3>
          <p>A share of our commission, in writing.</p>
        </div>
      </div>
    </div></section>
    <section class="ambassador-image-break ambassador-reveal">
      <img src="assets/liora/projects/jardin-del-mar-residences/media/exterior-pool-night.jpg" alt="Night view of a Costa del Sol residence and palm-lined pool terrace" width="1920" height="1095" loading="lazy" decoding="async">
      <div class="ambassador-image-break-caption">Introductions built on trust tend to find homes built to last.</div>
    </section>
    <section class="section quiet-band ambassador-reveal"><div class="section-inner"><div class="section-head center"><span class="label">The Reward</span><div class="rule" style="margin-left:auto;margin-right:auto;"></div><h2 class="section-title">Simple, honest <em>terms</em></h2></div>
      <div class="ambassador-facts">
        <div class="ambassador-fact"><svg class="ambassador-fact-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="19" y1="5" x2="5" y2="19"/><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/></svg><p>A genuine share of our commission, not a flat finder's fee.</p></div>
        <div class="ambassador-fact"><svg class="ambassador-fact-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><polyline points="8 15 10.5 17.5 15.5 12.5"/></svg><p>Paid once their purchase legally completes.</p></div>
        <div class="ambassador-fact"><svg class="ambassador-fact-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18.178 8c5.096 0 5.096 8 0 8-5.095 0-7.133-8-12.739-8-4.585 0-4.585 8 0 8 5.606 0 7.644-8 12.74-8z"/></svg><p>No limit &mdash; refer as many people as you like.</p></div>
        <div class="ambassador-fact"><svg class="ambassador-fact-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><line x1="3" y1="12" x2="21" y2="12"/><path d="M12 3a13.7 13.7 0 0 1 3.5 9A13.7 13.7 0 0 1 12 21a13.7 13.7 0 0 1-3.5-9A13.7 13.7 0 0 1 12 3z"/></svg><p>Works wherever they live, in Spain or abroad.</p></div>
      </div>
    </div></section>
    <section class="section ambassador-faq ambassador-reveal"><div class="section-inner"><div class="section-head center"><span class="label">Common Questions</span><div class="rule" style="margin-left:auto;margin-right:auto;"></div><h2 class="section-title">What ambassadors usually <em>ask us</em></h2></div>
      <div class="segment-faq-list">
        <details class="segment-faq-item" open><summary>How is my referral tracked once I submit it?</summary><p>The moment you submit the form below, we record the introduction against your details before reaching out to them.</p></details>
        <details class="segment-faq-item"><summary>What if the person I introduce already has a Nueva Living project in mind?</summary><p>We will still help them. The reward specifically recognises bringing us a genuinely new client, not someone already in touch with us.</p></details>
        <details class="segment-faq-item"><summary>What if they contact Nueva Living directly first?</summary><p>Submitting the introduction yourself, before they reach out independently, is what establishes it as your referral.</p></details>
        <details class="segment-faq-item"><summary>How will I know if my referral leads to a sale?</summary><p>We keep you updated on progress, within the bounds of their privacy, and confirm directly once a reward is due.</p></details>
      </div>
    </div></section>
    <section class="section ambassador-reveal" id="referral-form"><div class="section-inner"><div class="section-head center"><span class="label">Introduce Someone</span><div class="rule"></div><h2 class="section-title">Introduce them <em>today</em></h2><p class="body-copy" style="margin-left:auto;margin-right:auto;">Share your details and theirs. We will take it from there.</p></div><form class="form-panel" id="referral-form-panel" name="nueva-referral-request" method="POST" data-crm-lead action="/.netlify/functions/nueva-lead"><input type="text" name="honeypot" tabindex="-1" autocomplete="off" aria-hidden="true" style="display:none"><input type="hidden" name="subject" data-remove-prefix value="New Nueva Living referral submission"><input type="hidden" id="referral-request-context" name="request_context" value="Referral &amp; Ambassador Program"><input type="hidden" name="message" id="referral-message"><div class="form-grid"><div class="field"><label for="ref-first-name">Your First Name</label><input id="ref-first-name" name="first_name" autocomplete="given-name" placeholder="First name" required></div><div class="field"><label for="ref-last-name">Your Last Name</label><input id="ref-last-name" name="last_name" autocomplete="family-name" placeholder="Last name" required></div><div class="field"><label for="ref-email">Your Email Address</label><input id="ref-email" name="email" type="email" autocomplete="email" placeholder="your@email.com" required></div><div class="field"><label for="ref-phone">Your Phone Number</label><input id="ref-phone" name="phone" type="tel" autocomplete="tel" placeholder="+34 or international"></div><div class="field"><label for="friend-name">Their Name</label><input id="friend-name" name="friend_name" placeholder="Who are you introducing?" required></div><div class="field"><label for="friend-contact">Their Email or Phone</label><input id="friend-contact" name="friend_contact" placeholder="How can we reach them?" required></div><div class="field full"><label for="friend-notes">What Are They Looking For?</label><textarea id="friend-notes" name="friend_notes" placeholder="Budget, area, property type, timing -- whatever you know."></textarea></div><label class="consent-row field full" for="ref-consent"><input id="ref-consent" name="consent" type="checkbox" required><span>I agree to be contacted and for my data to be stored.</span></label></div><div class="form-actions"><button class="btn" type="submit">Submit Referral</button><span class="form-response"></span></div></form></div></section>
    <script>
      (() => {
        const nameField = document.getElementById('friend-name');
        const contactField = document.getElementById('friend-contact');
        const notesField = document.getElementById('friend-notes');
        const messageField = document.getElementById('referral-message');
        if (!nameField || !contactField || !notesField || !messageField) return;
        function composeMessage() {
          const parts = ['Referral: ' + (nameField.value || '(name not given)') + ' -- ' + (contactField.value || '(no contact given)')];
          if (notesField.value.trim()) parts.push(notesField.value.trim());
          messageField.value = parts.join('. ');
        }
        [nameField, contactField, notesField].forEach((field) => {
          field.addEventListener('input', composeMessage);
        });
        composeMessage();
      })();
      (() => {
        const items = document.querySelectorAll('.ambassador-reveal');
        if (!items.length) return;
        const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        if (reducedMotion || !('IntersectionObserver' in window)) {
          items.forEach((item) => item.classList.add('in'));
          return;
        }
        const observer = new IntersectionObserver((entries) => {
          entries.forEach((entry) => {
            if (!entry.isIntersecting) return;
            entry.target.classList.add('in');
            observer.unobserve(entry.target);
          });
        }, { threshold: 0.14 });
        items.forEach((item) => observer.observe(item));
      })();
    </script>`,
  },
  {
    file: 'about.html',
    title: 'About',
    description: 'About Nueva Living, a Costa del Sol new development advisory firm.',
    heroImage: 'assets/liora/viewing/scene-19.jpg',
    heroKicker: 'About Nueva Living',
    seoContext: 'Nueva Living: New-Build Specialists on the Costa del Sol',
    heroTitle: 'We focus on <em>new developments</em>',
    heroLead: 'Nueva Living was created for buyers who want straightforward help in the Costa del Sol new-build market.',
    body: `<section class="section"><div class="section-inner split"><div class="image-panel logo-panel"><img src="assets/liora/brand/nueva-living-lockup-sand-transparent.png?v=7" alt="Nueva Living logo" width="700" height="340"></div><div><span class="label">About Nueva Living</span><div class="rule"></div><h2 class="section-title">New builds are <em>what we know</em></h2><p class="body-copy">Because we only work with new and off-plan homes, we know the developers, the projects and the questions buyers should ask.</p><p class="body-copy">Our job is simple: show you what is available, explain what is good and help you leave the wrong options behind.</p></div></div></section>
    <section class="section founder-section" id="founder"><div class="section-inner split founder-layout"><figure class="founder-portrait"><img src="assets/liora/team/sasan-raftari-founder.jpg?v=20260727" srcset="assets/liora/team/sasan-raftari-founder-compact.jpg?v=20260727 646w, assets/liora/team/sasan-raftari-founder.jpg?v=20260727 1064w" sizes="(max-width: 980px) calc(100vw - 40px), 46vw" alt="Sasan Raftari, founder of Nueva Living" width="1064" height="1479" loading="lazy" decoding="async"></figure><div class="founder-copy"><span class="label">Founder</span><div class="rule"></div><h2 class="section-title">Sasan <em>Raftari</em></h2><p class="founder-role">Founder, Nueva Living</p><p class="body-copy">Sasan founded Nueva Living to make the search for a new home on the Costa del Sol clearer and more focused.</p><p class="body-copy">Sasan has spent 17 years in sales, around ten of them in digital as a product manager, ecommerce manager and head of digital. He combines the two to build the Costa del Sol's most user-friendly and advanced portal for new-build property.</p><p class="body-copy">Contact him directly to discuss your search, ask about a project or build a shortlist around what matters to you.</p><div class="founder-contact" aria-label="Contact Sasan Raftari"><a href="mailto:sasan@nuevaliving.com"><span>Email</span><strong>sasan@nuevaliving.com</strong></a><a href="https://wa.me/46707576709" target="_blank" rel="noopener" data-whatsapp-advisor data-context="Sasan Raftari, Founder" data-intent="contact founder"><span>Phone / WhatsApp</span><strong>+46 707 57 67 09</strong></a></div></div></div></section>
    <section class="section founder-section" id="sami-altun"><div class="section-inner split founder-layout founder-layout-reverse"><figure class="founder-portrait"><img src="assets/liora/team/sami-altun-co-founder.jpg?v=20260727" srcset="assets/liora/team/sami-altun-co-founder-compact.jpg?v=20260727 560w, assets/liora/team/sami-altun-co-founder.jpg?v=20260727 1024w" sizes="(max-width: 980px) calc(100vw - 40px), 46vw" alt="Sami Altun, co-founder of Nueva Living" width="1024" height="1535" loading="lazy" decoding="async"></figure><div class="founder-copy"><span class="label">Co-Founder</span><div class="rule"></div><h2 class="section-title">Sami <em>Altun</em></h2><p class="founder-role">Co-Founder, Nueva Living</p><p class="body-copy">Sami brings a background in business development and economics, with a practical focus on evaluating opportunities, structuring decisions and building long-term relationships.</p><p class="body-copy">At Nueva Living, he connects commercial insight with each buyer's priorities, helping keep project selection and the purchasing process clear, considered and grounded.</p><div class="founder-contact" aria-label="Contact Sami Altun"><a href="mailto:sami@nuevaliving.com"><span>Email</span><strong>sami@nuevaliving.com</strong></a><a href="https://wa.me/34645446624" target="_blank" rel="noopener" data-whatsapp-advisor data-whatsapp-number="34645446624" data-context="Sami Altun, Co-Founder" data-intent="contact co-founder"><span>Phone / WhatsApp</span><strong>+34 645 44 66 24</strong></a></div></div></div></section>
    <section class="section quiet-band"><div class="section-inner"><div class="cards"><article class="card"><div class="card-number">40+</div><h3>Developers We Work With</h3><p>Direct conversations and project access across the main Costa del Sol areas.</p></article><article class="card"><div class="card-number">7</div><h3>Areas We Cover</h3><p>From Marbella and Benahavis to Estepona, Nueva Andalucia, Mijas and Fuengirola.</p></article><article class="card"><div class="card-number">100%</div><h3>Focused on New Builds</h3><p>One clear focus keeps our advice useful and up to date.</p></article></div></div></section>
    <section class="section"><div class="section-inner"><div class="section-head"><span class="label">What Matters to Us</span><div class="rule"></div><h2 class="section-title">Access, privacy and <em>clear advice</em></h2></div><div class="cards"><article class="card"><h3>Privacy</h3><p>We handle your requirements carefully and only share details when needed for your request.</p></article><article class="card"><h3>Fewer, Better Options</h3><p>We focus on the projects worth considering rather than sending you a long catalogue.</p></article><article class="card"><h3>The Full Picture</h3><p>Every recommendation includes the area, developer, timing and what may support future value.</p></article></div></div></section>
    <section class="cta-band"><div class="cta-inner"><h2 class="cta-title">Tell us what you are looking for and we will help with the next step.</h2><a class="btn" href="contact.html">Contact Us</a></div></section>`,
  },
  {
    file: 'contact.html',
    title: 'Contact Us',
    breadcrumbTitle: 'Contact Us',
    description: 'Tell Nueva Living what kind of new home you are looking for on the Costa del Sol.',
    heroImage: 'assets/liora/viewing/scene-08.jpg',
    heroKicker: 'Contact Nueva Living',
    seoContext: 'Get Your Costa del Sol New-Build Shortlist',
    heroTitle: 'Tell us what you are <em>looking for</em>',
    heroLead: 'Share a few details and we will come back with relevant projects, current availability and a clear next step.',
    body: `<section class="section"><div class="section-inner"><div class="section-head center"><span class="label">Your Search</span><div class="rule"></div><h2 class="section-title">Let us help you <em>narrow it down</em></h2><p class="body-copy" style="margin-left:auto;margin-right:auto;">Tell us what matters to you. We will reply with the projects and information that best fit your search.</p></div><div class="contact-nap" style="max-width:640px;margin:0 auto 40px;text-align:center;">
      <span class="footer-col-title" style="display:block;margin-bottom:10px;">Visit Us</span>
      <p class="body-copy" style="margin:0;">
        <a href="https://maps.google.com/?q=Avenida+del+Prado+71,+29660+Marbella,+M%C3%A1laga,+Spain" target="_blank" rel="noopener">Avenida del Prado 71, 29660 Marbella, M&aacute;laga, Spain</a>
      </p>
      <p class="body-copy" style="margin:10px 0 0;">
        <a href="https://wa.me/46707576709" target="_blank" rel="noopener" data-whatsapp-advisor data-whatsapp-number="46707576709" data-context="my property search" data-intent="ask a question" dir="ltr">WhatsApp +46 70 757 67 09</a>
      </p>
    </div><form class="form-panel" id="contact-form" name="liora-access-request" method="POST" data-crm-lead action="/.netlify/functions/nueva-lead"><input type="text" name="honeypot" tabindex="-1" autocomplete="off" aria-hidden="true" style="display:none"><input type="hidden" name="subject" data-remove-prefix value="New Nueva Living contact enquiry"><input type="hidden" id="request-context" name="request_context" value="General contact request"><div class="form-grid"><div class="field"><label for="first-name">First Name</label><input id="first-name" name="first_name" autocomplete="given-name" placeholder="First name" required></div><div class="field"><label for="last-name">Last Name</label><input id="last-name" name="last_name" autocomplete="family-name" placeholder="Last name" required></div><div class="field"><label for="email">Email Address</label><input id="email" name="email" type="email" autocomplete="email" placeholder="your@email.com" required></div><div class="field"><label for="phone">Phone Number</label><input id="phone" name="phone" type="tel" autocomplete="tel" placeholder="+34 or international"></div><div class="field"><label for="area">Preferred Area</label><select id="area" name="preferred_area"><option value="">Select area...</option><option>Marbella</option><option>Estepona</option><option>Benahavis</option><option>Nueva Andalucia</option><option>Open to all areas</option></select></div><div class="field"><label for="property-type">Property Type</label><select id="property-type" name="property_type_interest"><option value="">Select type...</option><option>Apartments</option><option>Penthouses</option><option>Villas</option><option>Townhouses</option><option>Mixed / Open</option></select></div><div class="field"><label for="budget">Budget Range</label><select id="budget" name="budget_range"><option value="">Select budget...</option><option>&euro;300,000 - &euro;500,000</option><option>&euro;500,000 - &euro;900,000</option><option>&euro;900,000 - &euro;1,500,000</option><option>&euro;1,500,000+</option></select></div><div class="field"><label for="purpose">How Will You Use It?</label><select id="purpose" name="purchase_purpose"><option value="">Select purpose...</option><option>Primary Residence</option><option>Holiday Home</option><option>Investment / Rental</option><option>Combination</option></select></div><div class="field full"><label for="message">Message</label><textarea id="message" name="message" placeholder="Tell us what you are looking for..."></textarea></div><label class="consent-row field full" for="consent"><input id="consent" name="consent" type="checkbox" required><span>I agree to be contacted and for my data to be stored.</span></label><label class="consent-row field full" for="marketing-opt-in"><input id="marketing-opt-in" name="marketing_opt_in" type="checkbox"><span>I would also like to receive occasional project updates from Nueva Living.</span></label></div><div class="form-actions"><button class="btn" type="submit">Send Enquiry</button><span class="form-response"></span></div></form></div></section>`,
  },
  {
    file: 'privacy-policy.html',
    title: 'Privacy Policy',
    description: 'Privacy policy draft for Nueva Living.',
    heroImage: 'assets/liora/viewing/scene-11.jpg',
    heroKicker: 'Legal',
    heroTitle: 'Privacy <em>Policy</em>',
    heroLead: 'How we collect, use and protect the information you share with us.',
    body: legalBody('Privacy Policy', [
      ['Overview', 'LIORA LIVING SL. (NIF B88827472), operating under the Nueva Living brand, is responsible for personal information submitted through enquiry forms, email or direct communication.'],
      ['Information We May Collect', 'Name, contact details, preferred area, budget range, purchase purpose and any details voluntarily included in a message. Website measurement may also collect page visits, temporary session identifiers, device and browser type, general interaction events, referral or campaign information and performance or error data. Analytics does not read or store the values entered into form fields.'],
      ['How Information Is Used', 'Information is used to respond to enquiries, prepare relevant project suggestions, coordinate viewings and maintain appropriate records of client communication. Aggregated website measurement is used to understand which pages and features are useful, identify technical problems and improve website performance.'],
      ['Sharing', 'Enquiry details may be processed in Nueva Living\'s customer relationship management system and shared with developers, legal advisers or other service providers only where necessary for a requested enquiry, viewing, reservation or service step. Website measurement events may be processed by Nueva Living\'s CRM and hosting providers for analytics and technical operation.'],
      ['Retention &amp; Rights', 'Personal data should be retained only for as long as needed for the enquiry or client relationship. Visitors may request access, correction or deletion by contacting contact@nuevaliving.com.'],
    ]),
  },
  {
    file: 'legal-notice.html',
    title: 'Legal Notice',
    description: 'Legal notice draft for Nueva Living.',
    heroImage: 'assets/liora/viewing/scene-15.jpg',
    heroKicker: 'Legal',
    heroTitle: 'Legal <em>Notice</em>',
    heroLead: 'Who operates this website, what the information is for and the terms that apply.',
    body: legalBody('Legal Notice', [
      ['Website Owner', 'This website is presented under the Nueva Living brand and operated by LIORA LIVING SL., Tax ID (NIF) B88827472.'],
      ['Purpose Of The Website', 'The site provides general marketing information about new-build and off-plan property opportunities across the Costa del Sol. Content is indicative and subject to change.'],
      ['No Legal Or Financial Advice', 'Information on this website does not constitute legal, financial, tax or investment advice. Buyers should seek independent professional advice before making any property decision.'],
      ['Property Information', 'Prices, availability, plans, delivery dates and specifications are provided for general orientation and may change without notice. Final details must be confirmed directly through official developer documentation.'],
      ['Intellectual Property', 'Branding, layout, written content and original materials on this website may not be copied or reused without permission. Third-party images remain subject to their respective rights.'],
    ]),
  },
  {
    file: 'cookie-policy.html',
    title: 'Cookie Policy',
    description: 'Cookie policy draft for Nueva Living.',
    heroImage: 'assets/liora/viewing/scene-10.jpg',
    heroKicker: 'Legal',
    heroTitle: 'Cookie <em>Policy</em>',
    heroLead: 'What cookies and third-party tools may be used on this website.',
    body: legalBody('Cookie Policy', [
      ['Current Setup', 'This website does not use advertising cookies. It uses first-party browser storage to keep a temporary website-measurement session active for up to 30 minutes and to support features such as saved project shortlists.'],
      ['Essential Cookies', 'Essential cookies or equivalent browser storage may be used to support basic website function, security, form handling or preference storage where required.'],
      ['Website Measurement', 'Website measurement records page visits, scroll milestones, general clicks, media interactions, form submission status, technical errors and performance metrics. It also records basic device, browser, referral and campaign information. It does not collect the values typed into form fields.'],
      ['Third-Party Services', 'The site may load maps, video embeds or form and CRM services from third-party providers. These providers may process technical data according to their own policies.'],
      ['Managing Preferences', 'Visitors can remove website storage through browser settings and may contact contact@nuevaliving.com with a privacy request. Consent requirements for non-essential measurement should be reviewed for each market in which the website is offered.'],
    ]),
  },
];

pages.push(...areas.map((area) => ({ __area: area, file: area.output })));

function legalBody(title, sections) {
  return `<section class="section"><div class="section-inner legal-layout"><aside class="legal-nav">${sections.map(([heading]) => `<a href="#${slug(heading)}">${heading}</a>`).join('')}</aside><div class="legal-stack"><div class="section-head"><span class="label">Important Information</span><div class="rule"></div><h2 class="section-title">${title}</h2><p class="body-copy">This page explains the main terms in plain language. It should be reviewed by qualified legal counsel before any future material change.</p></div>${sections.map(([heading, text]) => `<article class="legal-card" id="${slug(heading)}"><h3>${heading}</h3><p>${text}</p></article>`).join('')}</div></div></section><section class="cta-band"><div class="cta-inner"><h2 class="cta-title">Have a question about a project?</h2><a class="btn" href="contact.html">Contact Us</a></div></section>`;
}

function slug(value) {
  return value.toLowerCase().replace(/&amp;/g, 'and').replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
}

const written = [];
for (const item of pages) {
  // englishOnly pages are generated in English alone: see the note on
  // hreflangLinks(). Nothing downstream needs changing -- build_dist derives
  // its sitemap alternates from what actually exists on disk.
  const localesForItem = item.englishOnly ? [LOCALES[0]] : LOCALES;
  for (const { code: locale } of localesForItem) {
    const resolvedItem = item.__area ? areaDetailPage(item.__area, locale) : item;
    const outputPath = localizedPath(item.file, locale);
    const fullPath = outputPath;
    if (outputPath.includes('/')) mkdirSync(outputPath.split('/')[0], { recursive: true });
    writeFileSync(fullPath, page(resolvedItem, locale));
    written.push(outputPath);
  }
}

console.log(JSON.stringify({ pages: written }, null, 2));
