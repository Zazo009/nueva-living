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
  LANG_SWITCHER_SCRIPT,
  localizeProject,
  localizeInternalLinks
} from './lib/i18n.mjs';
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

function navLinks(locale) {
  return [
    [t('nav.buyingGuides', locale), 'guides.html'],
    [t('nav.whyNueva', locale), 'why-nueva.html'],
    [t('nav.developments', locale), 'developments.html'],
    [t('nav.areas', locale), 'areas.html'],
    [t('nav.advisory', locale), 'advisory.html'],
    [t('nav.contactUs', locale), 'contact.html'],
  ];
}

function footerLinks(locale) {
  return {
    company: [
      [t('footer.whyNuevaLiving', locale), 'why-nueva.html'],
      [t('footer.about', locale), 'about.html'],
      [t('footer.advisory', locale), 'advisory.html'],
      [t('footer.referralProgram', locale), 'referrals.html'],
      [t('footer.contactUs', locale), 'contact.html'],
    ],
    projects: [
      [t('footer.allDevelopments', locale), 'developments.html'],
      [t('footer.buyingGuides', locale), 'guides.html'],
      [t('footer.areasOverview', locale), 'areas.html'],
      [t('area.marbella', locale), 'area-marbella.html'],
      [t('area.estepona', locale), 'area-estepona.html'],
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

function nav(locale = DEFAULT_LOCALE, currentOutputPath = 'index.html') {
  const links = navLinks(locale);
  const switcher = renderLanguageSwitcher(currentOutputPath, locale);
  return `<nav class="site-nav">
    <div class="nav-links nav-links-left">
      ${links.slice(0, 3).map(([label, href]) => `<a href="${href}">${label}</a>`).join('\n      ')}
    </div>
    <a class="nav-logo" href="${home}" aria-label="${t('nav.home', locale)}">
      <img src="assets/liora/brand/nueva-living-hero-logo-transparent.png?v=7" alt="Nueva Living" width="420" height="100">
    </a>
    <div class="nav-links nav-links-right">
      ${links.slice(3).map(([label, href]) => `<a href="${href}">${label}</a>`).join('\n      ')}
      ${switcher}
    </div>
    <button class="nav-burger" type="button" aria-label="${t('nav.menu', locale)}" aria-controls="mobileMenu" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
  </nav>
  <div class="mobile-menu" id="mobileMenu">
    ${links.map(([label, href]) => `<a href="${href}">${label}</a>`).join('\n    ')}
    ${renderLanguageSwitcher(currentOutputPath, locale)}
  </div>`;
}

function breadcrumb(currentLabel, parents = [], locale = DEFAULT_LOCALE) {
  const parentItems = parents.map(([label, href]) => `<li><a href="${esc(href)}">${esc(label)}</a></li>`).join('\n      ');
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

function page({ file, title, breadcrumbTitle, breadcrumbs, description, heroImage, heroAlt = '', heroWidth, heroHeight, heroPosition, heroKicker, heroTitle, heroLead, body, bodyClass = '' }, locale = DEFAULT_LOCALE) {
  const meta = localeMeta(locale);
  const rtl = isRtl(locale);
  const html = `<!doctype html>
<html lang="${meta.htmlLang}" dir="${meta.dir}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
${baseHrefTag(locale)}  <title>${esc(title)} | Nueva Living</title>
  <meta name="description" content="${esc(description)}">
${hreflangLinks(file, 'https://nuevaliving.com')}
  <meta property="og:locale" content="${meta.htmlLang}">
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
  ${nav(locale, file)}
  ${breadcrumb(breadcrumbTitle || title, breadcrumbs, locale)}
  <main>
    <section class="page-hero">
      <img src="${esc(heroImage)}" alt="${esc(heroAlt)}"${heroWidth ? ` width="${heroWidth}"` : ''}${heroHeight ? ` height="${heroHeight}"` : ''}${heroPosition ? ` style="object-position:${esc(heroPosition)}"` : ''} loading="eager" fetchpriority="high" decoding="async">
      <div class="hero-inner">
        <span class="kicker">${esc(heroKicker)}</span>
        <h1 class="display-title">${heroTitle}</h1>
        <p class="lead">${esc(heroLead)}</p>
      </div>
    </section>
    ${body}
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

function areaProjectCardGallery(project) {
  const items = (project.media?.items || []).slice(0, 6);
  if (!items.length) {
    const image = project.images?.hero || {};
    return `<img src="${esc(image.src)}" alt="${esc(image.alt || project.name)}" width="${image.width || 1600}" height="${image.height || 900}" loading="lazy" decoding="async">`;
  }

  const slides = items.map((item) => `
      <img src="${esc(item.src)}" alt="${esc(item.alt || project.name)}" loading="lazy" decoding="async">`).join('');
  const dots = items.length > 1
    ? `<div class="project-card-gallery-dots" data-gallery-dots>${items.map((_, index) => `<button type="button" class="project-card-gallery-dot${index === 0 ? ' is-active' : ''}" data-gallery-dot="${index}" aria-label="Show image ${index + 1} of ${items.length}"></button>`).join('')}</div>`
    : '';

  return `<div class="project-card-gallery" data-project-card-gallery data-card-url="${esc(project.output)}">
      <div class="project-card-gallery-track" data-gallery-track>${slides}
      </div>
      ${dots}
    </div>`;
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
  const projectType = project.hero?.type || project.quickFacts?.find(([label]) => label === 'Property type')?.[1] || t('common.newDevelopment', locale);
  return `<article class="project-card area-project-card" data-project-card>
    ${areaProjectCardGallery(project)}
    <div class="project-body">
      <span class="label">${esc(project.card?.label || project.hero?.location || t('common.newDevelopment', locale))}</span>
      <h3>${esc(project.name)}</h3>
      <p>${esc(project.card?.description || project.description)}</p>
      <div class="meta">${meta.slice(0, 3).map(([label, value]) => `<div><span>${esc(label)}</span><strong>${esc(value)}</strong></div>`).join('')}</div>
      <div class="project-tags"><span>${esc(projectType)}</span><span>${t('common.currentAvailability', locale)}</span></div>
      <a class="project-link" href="${esc(project.output)}">${t('cta.exploreProject', locale)}</a>
    </div>
  </article>`;
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

  return `<form class="form-panel area-form" name="nueva-${esc(area.slug)}-enquiry" method="POST" data-crm-lead action="/.netlify/functions/nueva-lead">
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
  const priceItems = area.prices.map((price) => `<div class="area-price-item"><span>${esc(price.label)}</span><strong>${esc(price.value)}</strong></div>`).join('');
  const highlights = area.highlights.map(([title, copy], index) => `<article class="area-highlight"><span>${String(index + 1).padStart(2, '0')}</span><h3>${esc(title)}</h3><p>${esc(copy)}</p></article>`).join('');
  const paragraphs = area.intro.paragraphs.map((paragraph) => `<p class="body-copy">${esc(paragraph)}</p>`).join('');
  const spotlightSection = area.spotlight ? `
    <section class="section area-spotlight"><div class="section-inner"><div class="section-head"><span class="label">${t('area.localKnowledge', locale)}</span><div class="rule"></div><h2 class="section-title">${area.spotlight.headlineHtml}</h2><p class="body-copy">${esc(area.spotlight.intro)}</p></div><div class="cards spotlight-cards">${area.spotlight.items.map(([title, copy, image], index) => `<article class="card spotlight-card">${image ? `<div class="spotlight-card-image"><img src="${esc(image.src)}" alt="${esc(image.alt || title)}" width="${image.width || 800}" height="${image.height || 600}" loading="lazy" decoding="async"></div>` : ''}<div class="spotlight-card-body"><div class="card-number">${String(index + 1).padStart(2, '0')}</div><h3>${esc(title)}</h3><p>${esc(copy)}</p></div></article>`).join('')}</div>${area.spotlight.photoCredits ? `<p class="spotlight-photo-credits">${esc(area.spotlight.photoCredits)}</p>` : ''}</div></section>` : '';

  return {
    file: area.output,
    title: t('area.areaGuide', locale, { name: area.name }),
    breadcrumbTitle: area.name,
    breadcrumbs: [[t('nav.areas', locale), 'areas.html']],
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
    <section class="section quiet-band"><div class="section-inner"><div class="section-head center"><span class="label">Know Someone Looking?</span><div class="rule"></div><h2 class="section-title">Introduce someone, <em>get rewarded</em></h2><p class="body-copy" style="margin-left:auto;margin-right:auto;">If someone in your life is thinking about a home on the Costa del Sol, our <a href="referrals.html">Referral &amp; Ambassador Program</a> lets you introduce them and receive a share of our commission when their purchase completes.</p></div></div></section>
    <section class="cta-band"><div class="cta-inner"><div><span class="label">Ready When You Are</span><h2 class="cta-title">Bring us your wish list. We will bring back the options worth your time.</h2></div><a class="btn" href="contact.html#contact-form">Start Your Search</a></div></section>`,
  },
  {
    file: 'areas.html',
    title: 'Areas',
    description: 'Costa del Sol area guide for new development buyers.',
    heroImage: 'assets/liora/viewing/scene-01.jpg',
    heroKicker: 'Locations',
    heroTitle: 'The Costa del Sol, <em>area by area</em>',
    heroLead: 'Every area feels different. We help you compare daily life, travel times, views, prices and future resale demand.',
    body: `<section class="section"><div class="section-inner"><div class="section-head"><span class="label">Area Guide</span><div class="rule"></div><h2 class="section-title">Find the area that <em>fits you</em></h2><p class="body-copy">We look at what it is actually like to live there, how easy it is to get around and what supports long-term demand.</p></div><div class="area-stack">
      <a class="area-row" id="marbella" href="area-marbella.html" aria-label="Explore the Marbella area guide"><img src="assets/liora/areas/marbella.jpg" alt="Marbella coastline at sunrise with La Concha mountain" width="1920" height="2880" loading="lazy" decoding="async"><div class="area-copy"><span class="label">Marbella</span><h3>The coast's best-known address</h3><p>Marbella combines beaches, restaurants, international schools and established neighbourhoods, from the Golden Mile to Sierra Blanca.</p><span class="area-explore">Explore Marbella</span></div></a>
      <a class="area-row" id="estepona" href="area-estepona.html" aria-label="Explore the Estepona area guide"><img src="assets/liora/areas/estepona.jpg" alt="Estepona old town street with white houses and flower pots" width="1920" height="1278" loading="lazy" decoding="async"><div class="area-copy"><span class="label">Estepona</span><h3>A growing coastal town</h3><p>Estepona has seen major improvements in recent years, with a lively old town, good beach access and plenty of new projects.</p><span class="area-explore">Explore Estepona</span></div></a>
      <a class="area-row" id="benahavis" href="area-benahavis.html" aria-label="Explore the Benahavis area guide"><img src="assets/liora/areas/benahavis.jpg" alt="Benahavis mountain village and elevated hillside landscape" width="1920" height="1280" loading="lazy" decoding="async"><div class="area-copy"><span class="label">Benahavis</span><h3>Privacy, hills and open views</h3><p>Set above Marbella, Benahavis is known for gated communities, golf, villas and a quieter pace of life.</p><span class="area-explore">Explore Benahavis</span></div></a>
      <a class="area-row" id="nueva-andalucia" href="area-nueva-andalucia.html" aria-label="Explore the Nueva Andalucia area guide"><img src="assets/liora/areas/nueva-andalucia.jpg" alt="Puerto Banus marina and La Concha near Nueva Andalucia" width="1920" height="1280" loading="lazy" decoding="async"><div class="area-copy"><span class="label">Nueva Andalucia</span><h3>Golf Valley living</h3><p>Close to Puerto Banus and surrounded by golf courses, Nueva Andalucia works well for buyers who want restaurants, services and year-round activity nearby.</p><span class="area-explore">Explore Nueva Andalucia</span></div></a>
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
    heroTitle: 'Know what you are buying <em>before you decide</em>',
    heroLead: 'We help you check the location, developer, finishes, payment plan and future resale appeal before you choose a home.',
    body: `<section class="section"><div class="section-inner split"><div><span class="label">An Independent View</span><div class="rule"></div><h2 class="section-title">Clear advice for <em>the buyer</em></h2><p class="body-copy">A developer brochure shows the project at its best. We help you look beyond it and understand what is genuinely strong, what is fairly standard and what needs a closer check.</p></div><div class="image-panel"><img src="assets/liora/viewing/scene-13.jpg" alt="Interior detail"></div></div></section>
    <section class="section quiet-band"><div class="section-inner"><div class="section-head"><span class="label">How We Help</span><div class="rule"></div><h2 class="section-title">The details we help you <em>compare</em></h2></div><div class="cards"><article class="card"><h3>Compare Projects</h3><p>We compare prices, orientation, amenities, completion dates and nearby alternatives side by side.</p></article><article class="card"><h3>Plan the Purchase</h3><p>We talk through how you will use the home, rental plans, financing and what you may want later.</p></article><article class="card"><h3>Reserve with Clarity</h3><p>We organise project documents, viewings, reservation details and an introduction to an independent lawyer.</p></article></div></div></section>
    <section class="section"><div class="section-inner"><div class="section-head center"><span class="label">Our Promise</span><div class="rule"></div><h2 class="section-title">Straight answers, <em>no pressure</em></h2></div><div class="cards two"><article class="card"><h3>A Shorter, Better List</h3><p>We would rather show you three suitable projects than thirty generic options.</p></article><article class="card"><h3>Real Urgency Only</h3><p>We only flag urgency when availability, pricing or a reservation deadline genuinely changes.</p></article></div></div></section>
    ${generalFaqSection()}
    <section class="cta-band"><div class="cta-inner"><h2 class="cta-title">Talk through the options before you reserve.</h2><a class="btn" href="contact.html">Talk to an Advisor</a></div></section>`,
  },
  {
    file: 'guide-how-buying-works.html',
    title: 'How Buying Works',
    description: 'A step-by-step guide to buying a new-build home on the Costa del Sol, from your first shortlist to collecting the keys.',
    heroImage: 'assets/liora/viewing/scene-13.jpg',
    heroKicker: 'Buying Guide',
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
            <p>Spanish building law generally provides for a structural warranty, a shorter warranty on installations, and a one-year warranty on finishes. After completion, budgeting for ongoing costs such as community fees and annual property tax (IBI) becomes part of owning the home.</p>
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
    file: 'guide-off-plan-vs-resale.html',
    title: 'Off-Plan vs Resale',
    description: 'How buying off-plan and buying a completed resale home actually compare on the Costa del Sol, across price, risk, payment terms and appreciation.',
    heroImage: 'assets/liora/projects/altos-de-marbella/media/aerial-dusk-pool.jpg',
    heroKicker: 'Buying Guide',
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
        <h4>Does the bank guarantee cover everything I pay?</h4>
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
    <div class="section-inner"><p class="guide-disclaimer g-reveal">This guide is general information to help you compare off-plan and resale purchases on the Costa del Sol. It is not legal, tax or financial advice, and does not replace independent professional advice tailored to your situation.</p></div>
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
    <section class="section ambassador-reveal" id="referral-form"><div class="section-inner"><div class="section-head center"><span class="label">Introduce Someone</span><div class="rule"></div><h2 class="section-title">Introduce them <em>today</em></h2><p class="body-copy" style="margin-left:auto;margin-right:auto;">Share your details and theirs. We will take it from there.</p></div><form class="form-panel" id="referral-form-panel" name="nueva-referral-request" method="POST" data-crm-lead action="/.netlify/functions/nueva-lead"><input type="hidden" name="subject" data-remove-prefix value="New Nueva Living referral submission"><input type="hidden" id="referral-request-context" name="request_context" value="Referral &amp; Ambassador Program"><input type="hidden" name="message" id="referral-message"><div class="form-grid"><div class="field"><label for="ref-first-name">Your First Name</label><input id="ref-first-name" name="first_name" autocomplete="given-name" placeholder="First name" required></div><div class="field"><label for="ref-last-name">Your Last Name</label><input id="ref-last-name" name="last_name" autocomplete="family-name" placeholder="Last name" required></div><div class="field"><label for="ref-email">Your Email Address</label><input id="ref-email" name="email" type="email" autocomplete="email" placeholder="your@email.com" required></div><div class="field"><label for="ref-phone">Your Phone Number</label><input id="ref-phone" name="phone" type="tel" autocomplete="tel" placeholder="+34 or international"></div><div class="field"><label for="friend-name">Their Name</label><input id="friend-name" name="friend_name" placeholder="Who are you introducing?" required></div><div class="field"><label for="friend-contact">Their Email or Phone</label><input id="friend-contact" name="friend_contact" placeholder="How can we reach them?" required></div><div class="field full"><label for="friend-notes">What Are They Looking For?</label><textarea id="friend-notes" name="friend_notes" placeholder="Budget, area, property type, timing -- whatever you know."></textarea></div><label class="consent-row field full" for="ref-consent"><input id="ref-consent" name="consent" type="checkbox" required><span>I agree to be contacted and for my data to be stored.</span></label></div><div class="form-actions"><button class="btn" type="submit">Submit Referral</button><span class="form-response"></span></div></form></div></section>
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
    heroTitle: 'We focus on <em>new developments</em>',
    heroLead: 'Nueva Living was created for buyers who want straightforward help in the Costa del Sol new-build market.',
    body: `<section class="section"><div class="section-inner split"><div class="image-panel logo-panel"><img src="assets/liora/brand/nueva-living-lockup-sand-transparent.png?v=7" alt="Nueva Living logo" width="700" height="340"></div><div><span class="label">About Nueva Living</span><div class="rule"></div><h2 class="section-title">New builds are <em>what we know</em></h2><p class="body-copy">Because we only work with new and off-plan homes, we know the developers, the projects and the questions buyers should ask.</p><p class="body-copy">Our job is simple: show you what is available, explain what is good and help you leave the wrong options behind.</p></div></div></section>
    <section class="section founder-section" id="founder"><div class="section-inner split founder-layout"><figure class="founder-portrait"><img src="assets/liora/team/sasan-raftari-founder.jpg?v=20260727" srcset="assets/liora/team/sasan-raftari-founder-compact.jpg?v=20260727 646w, assets/liora/team/sasan-raftari-founder.jpg?v=20260727 1064w" sizes="(max-width: 980px) calc(100vw - 40px), 46vw" alt="Sasan Raftari, founder of Nueva Living" width="1064" height="1479" loading="lazy" decoding="async"></figure><div class="founder-copy"><span class="label">Founder</span><div class="rule"></div><h2 class="section-title">Sasan <em>Raftari</em></h2><p class="founder-role">Founder, Nueva Living</p><p class="body-copy">Sasan founded Nueva Living to make the search for a new home on the Costa del Sol clearer and more focused.</p><p class="body-copy">Contact him directly to discuss your search, ask about a project or build a shortlist around what matters to you.</p><div class="founder-contact" aria-label="Contact Sasan Raftari"><a href="mailto:sasan@nuevaliving.com"><span>Email</span><strong>sasan@nuevaliving.com</strong></a><a href="https://wa.me/46707576709" target="_blank" rel="noopener" data-whatsapp-advisor data-context="Sasan Raftari, Founder" data-intent="contact founder"><span>Phone / WhatsApp</span><strong>+46 707 57 67 09</strong></a></div></div></div></section>
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
    heroTitle: 'Tell us what you are <em>looking for</em>',
    heroLead: 'Share a few details and we will come back with relevant projects, current availability and a clear next step.',
    body: `<section class="section"><div class="section-inner"><div class="section-head center"><span class="label">Your Search</span><div class="rule"></div><h2 class="section-title">Let us help you <em>narrow it down</em></h2><p class="body-copy" style="margin-left:auto;margin-right:auto;">Tell us what matters to you. We will reply with the projects and information that best fit your search.</p></div><div class="contact-nap" style="max-width:640px;margin:0 auto 40px;text-align:center;">
      <span class="footer-col-title" style="display:block;margin-bottom:10px;">Visit Us</span>
      <p class="body-copy" style="margin:0;">
        <a href="https://maps.google.com/?q=Avenida+del+Prado+71,+29660+Marbella,+M%C3%A1laga,+Spain" target="_blank" rel="noopener">Avenida del Prado 71, 29660 Marbella, M&aacute;laga, Spain</a>
      </p>
    </div><form class="form-panel" id="contact-form" name="liora-access-request" method="POST" data-crm-lead action="/.netlify/functions/nueva-lead"><input type="hidden" name="subject" data-remove-prefix value="New Nueva Living contact enquiry"><input type="hidden" id="request-context" name="request_context" value="General contact request"><div class="form-grid"><div class="field"><label for="first-name">First Name</label><input id="first-name" name="first_name" autocomplete="given-name" placeholder="First name" required></div><div class="field"><label for="last-name">Last Name</label><input id="last-name" name="last_name" autocomplete="family-name" placeholder="Last name" required></div><div class="field"><label for="email">Email Address</label><input id="email" name="email" type="email" autocomplete="email" placeholder="your@email.com" required></div><div class="field"><label for="phone">Phone Number</label><input id="phone" name="phone" type="tel" autocomplete="tel" placeholder="+34 or international"></div><div class="field"><label for="area">Preferred Area</label><select id="area" name="preferred_area"><option value="">Select area...</option><option>Marbella</option><option>Estepona</option><option>Benahavis</option><option>Nueva Andalucia</option><option>Open to all areas</option></select></div><div class="field"><label for="property-type">Property Type</label><select id="property-type" name="property_type_interest"><option value="">Select type...</option><option>Apartments</option><option>Penthouses</option><option>Villas</option><option>Townhouses</option><option>Mixed / Open</option></select></div><div class="field"><label for="budget">Budget Range</label><select id="budget" name="budget_range"><option value="">Select budget...</option><option>&euro;300,000 - &euro;500,000</option><option>&euro;500,000 - &euro;900,000</option><option>&euro;900,000 - &euro;1,500,000</option><option>&euro;1,500,000+</option></select></div><div class="field"><label for="purpose">How Will You Use It?</label><select id="purpose" name="purchase_purpose"><option value="">Select purpose...</option><option>Primary Residence</option><option>Holiday Home</option><option>Investment / Rental</option><option>Combination</option></select></div><div class="field full"><label for="message">Message</label><textarea id="message" name="message" placeholder="Tell us what you are looking for..."></textarea></div><label class="consent-row field full" for="consent"><input id="consent" name="consent" type="checkbox" required><span>I agree to be contacted and for my data to be stored.</span></label><label class="consent-row field full" for="marketing-opt-in"><input id="marketing-opt-in" name="marketing_opt_in" type="checkbox"><span>I would also like to receive occasional project updates from Nueva Living.</span></label></div><div class="form-actions"><button class="btn" type="submit">Send Enquiry</button><span class="form-response"></span></div></form></div></section>`,
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
  for (const { code: locale } of LOCALES) {
    const resolvedItem = item.__area ? areaDetailPage(item.__area, locale) : item;
    const outputPath = localizedPath(item.file, locale);
    const fullPath = outputPath;
    if (outputPath.includes('/')) mkdirSync(outputPath.split('/')[0], { recursive: true });
    writeFileSync(fullPath, page(resolvedItem, locale));
    written.push(outputPath);
  }
}

console.log(JSON.stringify({ pages: written }, null, 2));
