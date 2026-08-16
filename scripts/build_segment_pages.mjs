import { existsSync, readFileSync, readdirSync, writeFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { createHash } from 'node:crypto';
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
  localizeInternalLinks,
  seoTags
} from './lib/i18n.mjs';
import { renderUnifiedCard } from './lib/project_card.mjs';
import { renderProjectCardGallery } from './lib/card_gallery.mjs';
import { SEGMENT_PAGE_ENTRIES } from './lib/segment_page_translations.mjs';
import { EDITORIAL_ALT_ENTRIES } from './lib/editorial_alt_translations.mjs';
import { PROJECT_CARD_ENTRIES } from './lib/developments_page_translations.mjs';

// Same approach as applyFooterPageTranslations() in build_footer_pages.mjs:
// literal find/replace of translated prose over already-rendered English
// HTML, since segment-page body content (introParagraphs, sub-area
// write-ups, comparison rows, page-specific FAQ) is opaque markup built
// once, not structured per-locale fields. Missing entries for a locale
// leave the English text in place.
// Longest find first, so a short entry can never fire inside a longer
// string before that string's own entry matches. PROJECT_CARD_ENTRIES adds
// the shared project-card meta labels/values and CTA (same set used on
// developments.html); per-project card descriptions come from each
// project.json's own i18n overlay.
const SORTED_SEGMENT_PAGE_ENTRIES = [...SEGMENT_PAGE_ENTRIES, ...PROJECT_CARD_ENTRIES, ...EDITORIAL_ALT_ENTRIES]
  .sort((a, b) => b.find.length - a.find.length);

function cardDescriptionReplacements(locale) {
  const replacements = [];
  for (const project of projects) {
    const en = project.card?.description || project.description;
    const translated = project.i18n?.[locale]?.card?.description;
    if (!en || !translated || en === translated) continue;
    replacements.push([`<p>${en}</p>`, `<p>${translated}</p>`]);
  }
  return replacements;
}

// Project-card gallery alt text. The cards embedded on segment pages come
// from the same English-only card markup as developments.html, so their alt
// attributes are mapped here to each project's translated media items.
function cardImageAltReplacements(locale) {
  const replacements = [];
  for (const project of projects) {
    const english = project.media?.items || [];
    const localized = project.i18n?.[locale]?.media?.items || [];
    if (localized.length !== english.length) continue;
    english.forEach((item, index) => {
      const en = item.alt;
      const translated = localized[index]?.alt;
      if (!en || !translated || en === translated) return;
      replacements.push([`alt="${en}"`, `alt="${translated}"`]);
    });
  }
  return replacements;
}

function applySegmentPageTranslations(html, locale) {
  if (locale === DEFAULT_LOCALE) return html;
  let result = html;
  // Card alts first: some contain area names ("...its wider Marbella East
  // setting...") that the entry table below rewrites, which would stop the
  // full-alt match from ever firing.
  for (const [find, replace] of cardImageAltReplacements(locale)) {
    result = result.split(find).join(replace);
  }
  for (const entry of SORTED_SEGMENT_PAGE_ENTRIES) {
    const replacement = entry[locale];
    if (!replacement) continue;
    result = result.split(entry.find).join(replacement);
  }
  for (const [find, replace] of cardDescriptionReplacements(locale)) {
    result = result.split(find).join(replace);
  }
  return result;
}

function fileVersion(file) {
  return createHash('sha256').update(readFileSync(file)).digest('hex').slice(0, 12);
}

const calculatorJsVersion = fileVersion('assets/liora/liora-calculator.js');

// Property-type x area landing pages. These target what buyers actually
// search for ("apartments for sale in Marbella") rather than a project's
// own name. Editorial copy below is hand-written and evergreen; the stats
// bar and featured-developments grid are computed from whichever projects
// currently match at build time, so this scales automatically as more
// projects are added -- nothing here needs to be touched when inventory
// changes.

const projects = readdirSync('content/liora-projects', { withFileTypes: true })
  .filter((entry) => entry.isDirectory())
  .map((entry) => join('content/liora-projects', entry.name, 'project.json'))
  .filter((file) => existsSync(file))
  .map((file) => JSON.parse(readFileSync(file, 'utf8')))
  .filter((project) => !project.archived);

const home = 'index.html';
const siteUrl = 'https://nuevaliving.com';
const fontPreloadBlock = `  <link rel="preload" href="assets/fonts/google/co3bmX5slCNuHLi8bLeY9MK7whWMhyjYqXtKky2F7g.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="assets/fonts/google/8vIJ7ww63mVu7gt79mT7PkRXMw.woff2" as="font" type="font/woff2" crossorigin>`;

function esc(value) {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function formatEuro(value) {
  return `&euro;${Math.round(value).toLocaleString('en-US')}`;
}

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
  return `<footer>
    <div class="footer-grid">
      <div>
        <img class="footer-logo" src="assets/liora/brand/nueva-living-lockup-espresso-transparent.png?v=7" alt="Nueva Living" width="700" height="340" loading="lazy" decoding="async">
        <p class="footer-about">${t('footer.about.text', locale)}</p>
      </div>
      <div class="footer-col">
        <div class="footer-col-title">${t('footer.companyTitle', locale)}</div>
        <ul>
          <li><a href="why-nueva.html">${t('footer.whyNuevaLiving', locale)}</a></li>
          <li><a href="about.html">${t('footer.about', locale)}</a></li>
          <li><a href="advisory.html">${t('footer.advisory', locale)}</a></li>
          <li><a href="referrals.html">${t('footer.referralProgram', locale)}</a></li>
          <li><a href="contact.html">${t('footer.contactUs', locale)}</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <div class="footer-col-title">${t('footer.projectsTitle', locale)}</div>
        <ul>
          <li><a href="developments.html">${t('footer.allDevelopments', locale)}</a></li>
          <li><a href="guides.html">${t('footer.buyingGuides', locale)}</a></li>
          <li><a href="areas.html">${t('footer.areasOverview', locale)}</a></li>
          <li><a href="area-marbella.html">${t('area.marbella', locale)}</a></li>
          <li><a href="area-estepona.html">${t('area.estepona', locale)}</a></li>
          <li><a href="area-benahavis.html">${t('area.benahavis', locale)}</a></li>
          <li><a href="area-nueva-andalucia.html">${t('area.nuevaAndalucia', locale)}</a></li>
          <li><a href="area-mijas-fuengirola.html">${t('area.mijasFuengirola', locale)}</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <div class="footer-col-title">${t('footer.contactTitle', locale)}</div>
        <ul>
          <li><a href="mailto:contact@nuevaliving.com">contact@nuevaliving.com</a></li>
          <li><a href="tel:+34645446624" dir="ltr">+34 645 44 66 24</a></li>
          <li><a href="https://maps.google.com/?q=Avenida+del+Prado+71,+29660+Marbella,+M%C3%A1laga,+Spain" target="_blank" rel="noopener">Avenida del Prado 71, 29660 Marbella, M&aacute;laga, Spain</a></li>
        </ul>
        <div class="footer-col-title" style="margin-top:24px;">${t('footer.legalTitle', locale)}</div>
        <ul>
          <li><a href="privacy-policy.html">${t('footer.privacyPolicy', locale)}</a></li>
          <li><a href="legal-notice.html">${t('footer.legalNotice', locale)}</a></li>
          <li><a href="cookie-policy.html">${t('footer.cookiePolicy', locale)}</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>${t('footer.disclaimer', locale)}</p>
      <span>&copy; 2026 Nueva Living &middot; LIORA LIVING SL. &middot; NIF B88827472</span>
    </div>
  </footer>`;
}


function segmentProjectCard(project) {
  const meta = project.card?.meta || [
    ['From', (project.hero?.startingPrice || '').replace(/^From\s+/i, '') || 'On request'],
    ['Type', project.hero?.type || 'Residences'],
    ['Delivery', project.hero?.delivery || 'On request']
  ];
  const card = project.card || {};
  const priceValue = (meta.find(([label]) => /^from$/i.test(label)) || [])[1]
    || (project.hero?.startingPrice || '').replace(/^From\s+/i, '')
    || '';
  return renderUnifiedCard({
    project,
    gallery: renderProjectCardGallery(project),
    href: project.output,
    name: project.name,
    badge: card.badge || '',
    price: priceValue,
    location: card.label || card.locExtended || project.hero?.location || 'New Development',
    description: card.description || project.description,
    type: project.hero?.type || '',
    t: (key, vars) => t(key, 'en', vars),
    className: 'area-project-card',
    attrs: ' data-project-card',
    heading: 'h3',
    indent: '    '
  });
}

function matchProjects(segment) {
  return projects.filter((project) => {
    const discovery = project.discovery || {};
    const crm = project.crm || {};
    const areaMatch = discovery.area === segment.area;
    const typeMatch = (crm.propertyTypes || []).some((type) => segment.propertyTypes.includes(type));
    return areaMatch && typeMatch;
  });
}

function computeStats(matches) {
  const prices = matches.map((p) => p.crm?.priceMin).filter((n) => typeof n === 'number');
  const bedroomsMin = matches.map((p) => p.crm?.bedroomsMin).filter((n) => typeof n === 'number');
  const bedroomsMax = matches.map((p) => p.crm?.bedroomsMax).filter((n) => typeof n === 'number');
  const available = matches.map((p) => p.crm?.availableUnits).filter((n) => typeof n === 'number');

  return {
    count: matches.length,
    priceFrom: prices.length ? Math.min(...prices) : null,
    bedroomsMin: bedroomsMin.length ? Math.min(...bedroomsMin) : null,
    bedroomsMax: bedroomsMax.length ? Math.max(...bedroomsMax) : null,
    availableTotal: available.length ? available.reduce((sum, n) => sum + n, 0) : null
  };
}

function collectAmenities(matches) {
  const set = new Set();
  matches.forEach((project) => {
    (project.crm?.amenities || []).forEach((amenity) => set.add(amenity));
  });
  return [...set];
}

function statsBand(stats) {
  const items = [
    ['Developments', String(stats.count)],
    stats.priceFrom ? ['Price From', formatEuro(stats.priceFrom)] : null,
    (stats.bedroomsMin && stats.bedroomsMax) ? ['Bedrooms', `${stats.bedroomsMin}&ndash;${stats.bedroomsMax}`] : null,
    stats.availableTotal ? ['Homes Available Now', String(stats.availableTotal)] : null
  ].filter(Boolean);

  return `<section class="section quiet-band segment-stats-section"><div class="section-inner">
    <div class="area-price-panel segment-stats-panel">
      ${items.map(([label, value]) => `<div class="area-price-item"><span>${esc(label)}</span><strong>${value}</strong></div>`).join('\n      ')}
      <p>Figures reflect currently published developments matching this search and are reconfirmed by Nueva Living before any viewing or reservation.</p>
    </div>
  </div></section>`;
}

function faqSection(faqs) {
  const items = faqs.map(([question, answer], index) => `<details class="segment-faq-item"${index === 0 ? ' open' : ''}>
        <summary>${esc(question)}</summary>
        <p>${esc(answer)}</p>
      </details>`).join('\n      ');

  return `<section class="section segment-faq-section"><div class="section-inner">
    <div class="section-head"><span class="label">Common Questions</span><div class="rule"></div><h2 class="section-title">What buyers usually <em>ask us</em></h2></div>
    <div class="segment-faq-list">
      ${items}
    </div>
  </div></section>`;
}

function segmentSchema(segment, matches) {
  const url = `${siteUrl}/${segment.output}`;
  return [
    {
      '@context': 'https://schema.org',
      '@type': 'CollectionPage',
      name: segment.title,
      url,
      description: segment.description
    },
    {
      '@context': 'https://schema.org',
      '@type': 'ItemList',
      itemListElement: matches.map((project, index) => ({
        '@type': 'ListItem',
        position: index + 1,
        url: `${siteUrl}/${project.output}`,
        name: project.name
      }))
    },
    {
      '@context': 'https://schema.org',
      '@type': 'BreadcrumbList',
      itemListElement: [
        { '@type': 'ListItem', position: 1, name: 'Developments', item: `${siteUrl}/developments.html` },
        { '@type': 'ListItem', position: 2, name: segment.areaLabel, item: `${siteUrl}/${segment.areaHref}` },
        { '@type': 'ListItem', position: 3, name: segment.breadcrumbLabel, item: url }
      ]
    },
    {
      '@context': 'https://schema.org',
      '@type': 'FAQPage',
      mainEntity: segment.faq.map(([question, answer]) => ({
        '@type': 'Question',
        name: question,
        acceptedAnswer: { '@type': 'Answer', text: answer }
      }))
    }
  ];
}

function renderSegmentPage(segment, locale = DEFAULT_LOCALE) {
  const meta = localeMeta(locale);
  const rtl = isRtl(locale);
  const matches = matchProjects(segment);
  const stats = computeStats(matches);
  const amenities = collectAmenities(matches);

  const highlightsSection = `<section class="section segment-subareas"><div class="section-inner">
    <div class="section-head"><span class="label">${esc(segment.areaLabel)} In Detail</span><div class="rule"></div><h2 class="section-title">${segment.subareasHeadlineHtml}</h2></div>
    <div class="cards">
      ${segment.subareas.map(([title, copy], index) => `<article class="card"><div class="card-number">${String(index + 1).padStart(2, '0')}</div><h3>${esc(title)}</h3><p>${esc(copy)}</p></article>`).join('\n      ')}
    </div>
  </div></section>`;

  const developmentsSection = `<section class="section segment-developments"><div class="section-inner">
    <div class="section-head"><span class="label">Current Match</span><div class="rule"></div><h2 class="section-title">${segment.developmentsHeadlineHtml}</h2><p class="body-copy">Only developments currently matching this search are shown below. Price and availability are reconfirmed before a viewing.</p></div>
    <div class="project-grid area-project-grid">
      ${matches.length ? matches.map(segmentProjectCard).join('\n      ') : `<article class="area-project-empty"><span class="label">Private Selection</span><h3>Current opportunities available by request</h3><p>We do not publish a development here until its information is ready to compare. Tell us what you need and we will check current releases directly.</p><a class="project-link" href="contact.html?intent=${encodeURIComponent(`${segment.breadcrumbLabel} in ${segment.areaLabel}`)}#contact-form">Request a Shortlist</a></article>`}
    </div>
  </div></section>`;

  const amenitiesSection = amenities.length ? `<section class="section quiet-band segment-amenities"><div class="section-inner">
    <div class="section-head"><span class="label">What To Expect</span><div class="rule"></div><h2 class="section-title">${segment.amenitiesHeadlineHtml}</h2><p class="body-copy">${esc(segment.amenitiesIntro)}</p></div>
    <ul class="segment-amenity-list">
      ${amenities.map((amenity) => `<li>${esc(amenity.replace(/(^|[\s-])[a-z]/g, (c) => c.toUpperCase()))}</li>`).join('\n      ')}
    </ul>
  </div></section>` : '';

  const comparisonSection = `<section class="section segment-comparison"><div class="section-inner">
    <div class="section-head"><span class="label">Choosing Between Them</span><div class="rule"></div><h2 class="section-title">${segment.comparisonHeadlineHtml}</h2></div>
    <div class="cards two">
      ${segment.comparison.map(([title, copy], index) => `<article class="card"><div class="card-number">${String(index + 1).padStart(2, '0')}</div><h3>${esc(title)}</h3><p>${esc(copy)}</p></article>`).join('\n      ')}
    </div>
  </div></section>`;

  const enquirySection = `<section class="section segment-enquiry"><div class="section-inner">
    <div class="section-head center"><span class="label">Next Step</span><div class="rule"></div><h2 class="section-title">Get a shortlist matching <em>your budget</em></h2><p class="body-copy" style="margin-left:auto;margin-right:auto;">Tell us your budget, preferred sub-area and must-haves. We will reply with current developments and availability that genuinely match.</p></div>
    <div style="display:flex;justify-content:center;">
      <a class="btn" href="contact.html?intent=${encodeURIComponent(`${segment.breadcrumbLabel} in ${segment.areaLabel}`)}#contact-form">Request a Personal Shortlist</a>
    </div>
  </div></section>`;

  const otherSegments = SEGMENTS.filter((s) => s.output !== segment.output);
  const relatedSection = `<section class="section quiet-band segment-related"><div class="section-inner">
    <div class="section-head"><span class="label">Other Areas</span><div class="rule"></div><h2 class="section-title">More buying <em>guides</em></h2></div>
    <ul class="segment-related-list">
      ${otherSegments.map((s) => `<li><a href="${esc(s.output)}">${esc(s.breadcrumbLabel)} in ${esc(s.areaLabel)}</a></li>`).join('\n      ')}
      <li><a href="guides.html">All Buying Guides</a></li>
    </ul>
  </div></section>`;

  const schema = segmentSchema(segment, matches);

  const html = `<!doctype html>
<html lang="${meta.htmlLang}" dir="${meta.dir}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
${baseHrefTag(locale)}  <title>${esc(segment.title)}</title>
  <meta name="description" content="${esc(segment.description)}">
${hreflangLinks(segment.output, siteUrl)}
${seoTags(segment.output, locale, { title: segment.title, description: segment.description, image: `${siteUrl}/${segment.hero.image}` })}
  <link rel="icon" href="assets/liora/liora-favicon-512.png?v=6" type="image/png" sizes="512x512">
  <link rel="icon" href="assets/liora/favicon-32.png?v=6" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="assets/liora/apple-touch-icon.png?v=6" sizes="180x180">
${fontPreloadBlock}
  <link rel="stylesheet" href="assets/fonts/google/liora-fonts.css">
  <link rel="stylesheet" href="assets/liora/liora-pages.css">${rtl ? `
  <link rel="stylesheet" href="assets/liora/liora-rtl.css">` : ''}
  <script src="assets/liora/liora-card-gallery.js" defer></script>
  <script type="application/ld+json">
${JSON.stringify(schema, null, 2)}
  </script>
</head>
<body class="segment-page">
  ${nav(locale, segment.output)}
  ${breadcrumb(segment.breadcrumbLabel, [[t('breadcrumb.developments', locale), 'developments.html'], [segment.areaLabel, segment.areaHref]], locale)}
  <main>
    <section class="page-hero">
      <img src="${esc(segment.hero.image)}" alt="${esc(segment.hero.alt)}" width="${segment.hero.width}" height="${segment.hero.height}"${segment.hero.position ? ` style="object-position:${esc(segment.hero.position)}"` : ''} loading="eager" fetchpriority="high" decoding="async">
      <div class="hero-inner">
        <span class="kicker">${segment.kicker}</span>
        <h1 class="display-title">${segment.heroTitleHtml}</h1>
        <p class="lead">${esc(segment.heroLead)}</p>
      </div>
    </section>
    ${statsBand(stats)}
    <section class="section segment-intro"><div class="section-inner area-intro-layout">
      <div><span class="label">${esc(segment.introLabel)}</span><div class="rule"></div><h2 class="section-title">${segment.introHeadlineHtml}</h2>${segment.introParagraphs.map((p) => `<p class="body-copy">${esc(p)}</p>`).join('\n')}</div>
      <div class="area-highlights">${segment.quickFacts.map(([title, copy], index) => `<article class="area-highlight"><span>${String(index + 1).padStart(2, '0')}</span><h3>${esc(title)}</h3><p>${esc(copy)}</p></article>`).join('')}</div>
    </div></section>
    ${highlightsSection}
    ${developmentsSection}
    ${amenitiesSection}
    ${comparisonSection}
    ${faqSection(segment.faq)}
    ${otherSegments.length ? relatedSection : ''}
    ${enquirySection}
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
  return localizeInternalLinks(applySegmentPageTranslations(html, locale), locale);
}

function lowestPriceAcrossSegments() {
  const prices = SEGMENTS
    .map((segment) => computeStats(matchProjects(segment)).priceFrom)
    .filter((n) => typeof n === 'number');
  return prices.length ? Math.min(...prices) : 500000;
}

function guidesCalculatorSection() {
  const seedPrice = lowestPriceAcrossSegments();
  return `<section class="section quiet-band guides-calculator"><div class="section-inner">
    <div class="section-head center"><span class="label">Affordability</span><div class="rule"></div><h2 class="section-title">How Spanish mortgages <em>work for you</em></h2>
    <p class="body-copy" style="margin-left:auto;margin-right:auto;">Spanish banks lend differently to non-resident buyers than to Spanish residents. Where a resident might get financing up to 80% of a property's value, non-residents are typically capped closer to 70%, and the exact rate, term and how much of your income counts all vary by bank and by your personal financial profile. On top of the mortgage itself, budget for taxes and purchase costs &mdash; transfer tax or VAT, notary, land registry and legal fees &mdash; which typically add another 10-13% on top of the purchase price in Spain.</p>
    <p class="body-copy" style="margin-left:auto;margin-right:auto;">Use the calculator below for a realistic starting estimate of your deposit, monthly payment and total cost of buying, based on typical non-resident lending terms. It is a planning tool, not a mortgage offer &mdash; Nueva Living and your mortgage broker will confirm the real numbers once you have a specific property in mind.</p>
    </div>
    <div class="calculator-panel" data-calculator>
      <div class="calculator-inputs">
        <div class="calculator-field calculator-field--dual">
          <div class="calculator-field-label"><span>Purchase price</span><em data-calc-price-readout>&euro;0</em></div>
          <input type="range" data-calc-price-range min="150000" max="3000000" step="5000" value="${seedPrice}">
          <input type="number" data-calc-price value="${seedPrice}" min="0" step="1000" class="calculator-field-number">
        </div>
        <div class="calculator-field calculator-field--dual">
          <div class="calculator-field-label"><span>Deposit</span><em data-calc-deposit-readout>30% &middot; &euro;0</em></div>
          <input type="range" data-calc-deposit min="10" max="100" step="5" value="30">
          <em class="calculator-field-hint">Set to 30% by default &mdash; as a non-Spanish resident, lenders typically finance up to 70% of the property value. Your own maximum will depend on your bank and financial profile.</em>
        </div>
        <div class="calculator-field calculator-field--dual">
          <div class="calculator-field-label"><span>Mortgage term</span><em data-calc-term-readout>25 years</em></div>
          <input type="range" data-calc-term min="5" max="35" step="1" value="25">
        </div>
        <div class="calculator-field calculator-field--split">
          <label>
            <span>Interest rate</span>
            <div class="calculator-input-suffix">
              <input type="number" data-calc-rate value="3.2" min="0" max="15" step="0.1">
              <span class="calculator-input-suffix-label">%</span>
            </div>
          </label>
          <div class="calculator-rate-toggle" data-calc-rate-toggle role="group" aria-label="Rate type">
            <button type="button" class="is-active" data-rate-type="fixed">Fixed</button>
            <button type="button" data-rate-type="variable">Variable</button>
          </div>
        </div>
        <label class="calculator-field">
          <span>Taxes &amp; purchase costs</span>
          <div class="calculator-input-suffix">
            <input type="number" data-calc-costs value="10" min="0" max="20" step="0.5">
            <span class="calculator-input-suffix-label">%</span>
          </div>
          <em class="calculator-field-hint">Indicative only &mdash; ITP/VAT, notary, registry and legal fees vary by case. Confirm exact costs with your lawyer.</em>
        </label>
      </div>
      <div class="calculator-results">
        <div class="calculator-result calculator-result--highlight"><span>Estimated monthly payment</span><strong data-calc-monthly>&euro;0</strong></div>
        <div class="calculator-result calculator-result--secondary"><span>Cash needed without a mortgage</span><strong data-calc-total-property>&euro;0</strong></div>
        <div class="calculator-result calculator-result--secondary"><span>Cash needed with a mortgage (deposit + costs)</span><strong data-calc-cash-with-mortgage>&euro;0</strong></div>
        <div class="calculator-breakdown-bar" data-calc-bar>
          <span class="calculator-bar-segment calculator-bar-segment--deposit" data-calc-bar-deposit></span>
          <span class="calculator-bar-segment calculator-bar-segment--principal" data-calc-bar-principal></span>
          <span class="calculator-bar-segment calculator-bar-segment--interest" data-calc-bar-interest></span>
        </div>
        <div class="calculator-bar-legend">
          <span><i class="calculator-bar-segment--deposit"></i>Deposit</span>
          <span><i class="calculator-bar-segment--principal"></i>Mortgage principal</span>
          <span><i class="calculator-bar-segment--interest"></i>Total interest</span>
        </div>
        <div class="calculator-result-grid">
          <div class="calculator-result"><span>Deposit</span><strong data-calc-deposit-amount>&euro;0</strong></div>
          <div class="calculator-result"><span>Loan amount</span><strong data-calc-loan>&euro;0</strong></div>
          <div class="calculator-result"><span>Financed</span><strong data-calc-financed-pct>0%</strong></div>
          <div class="calculator-result"><span>Total interest paid</span><strong data-calc-total-interest>&euro;0</strong></div>
          <div class="calculator-result"><span>Taxes &amp; purchase costs</span><strong data-calc-costs-amount>&euro;0</strong></div>
        </div>
      </div>
    </div>
  </div></section>`;
}

const PROCESS_GUIDES = [
  {
    output: 'guide-off-plan-vs-resale.html',
    kicker: 'Buying Guide',
    title: 'Off-Plan vs Resale',
    description: 'How buying off-plan and buying a completed resale home actually compare, across price, risk, payment terms and appreciation.',
    image: 'assets/liora/projects/altos-de-marbella/media/aerial-dusk-pool.jpg',
    alt: 'Aerial dusk view of a new-build Costa del Sol residence and pool terrace'
  },
  {
    output: 'guide-how-buying-works.html',
    kicker: 'Buying Guide',
    title: 'How Buying Works',
    description: 'A step-by-step guide to buying a new-build home on the Costa del Sol, from your first shortlist to collecting the keys.',
    image: 'assets/nueva/journey/reservation-legal-1200.webp',
    alt: 'Buyer signing an agreement with professional guidance'
  }
];

function processGuideCard(guide) {
  return `<a class="card guide-card" href="${esc(guide.output)}">
      <div class="guide-card-image"><img src="${esc(guide.image)}" alt="${esc(guide.alt)}" width="640" height="420" loading="lazy" decoding="async"></div>
      <div class="guide-card-body">
        <span class="label">${esc(guide.kicker)}</span>
        <h3>${esc(guide.title)}</h3>
        <p>${esc(guide.description)}</p>
        <span class="project-link">Read the Guide</span>
      </div>
    </a>`;
}

function guideCard(segment) {
  const matches = matchProjects(segment);
  const stats = computeStats(matches);
  return `<a class="card guide-card" href="${esc(segment.output)}">
      <div class="guide-card-image"><img src="${esc(segment.hero.image)}" alt="${esc(segment.hero.alt)}" width="640" height="420" loading="lazy" decoding="async"></div>
      <div class="guide-card-body">
        <span class="label">${segment.kicker}</span>
        <h3>${esc(segment.breadcrumbLabel)} in ${esc(segment.areaLabel)}</h3>
        <p>${esc(segment.description)}</p>
        <div class="meta">
          <div><span>Developments</span><strong>${stats.count}</strong></div>
          ${stats.priceFrom ? `<div><span>From</span><strong>${formatEuro(stats.priceFrom)}</strong></div>` : ''}
        </div>
        <span class="project-link">Read the Guide</span>
      </div>
    </a>`;
}

function renderGuidesPage(locale = DEFAULT_LOCALE) {
  const meta = localeMeta(locale);
  const rtl = isRtl(locale);
  const title = 'Costa del Sol Buying Guides | Nueva Living';
  const description = 'Compare new-build apartments and penthouses by area across the Costa del Sol, with real prices, availability and local buying guidance from Nueva Living.';
  const schema = [
    {
      '@context': 'https://schema.org',
      '@type': 'CollectionPage',
      name: 'Costa del Sol Buying Guides',
      url: `${siteUrl}/guides.html`,
      description
    },
    {
      '@context': 'https://schema.org',
      '@type': 'ItemList',
      itemListElement: SEGMENTS.map((segment, index) => ({
        '@type': 'ListItem',
        position: index + 1,
        url: `${siteUrl}/${segment.output}`,
        name: segment.title
      }))
    },
    generalFaqSchema()
  ];

  const html = `<!doctype html>
<html lang="${meta.htmlLang}" dir="${meta.dir}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
${baseHrefTag(locale)}  <title>${esc(title)}</title>
  <meta name="description" content="${esc(description)}">
${hreflangLinks('guides.html', siteUrl)}
${seoTags('guides.html', locale, { title, description })}
  <link rel="icon" href="assets/liora/liora-favicon-512.png?v=6" type="image/png" sizes="512x512">
  <link rel="icon" href="assets/liora/favicon-32.png?v=6" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="assets/liora/apple-touch-icon.png?v=6" sizes="180x180">
${fontPreloadBlock}
  <link rel="stylesheet" href="assets/fonts/google/liora-fonts.css">
  <link rel="stylesheet" href="assets/liora/liora-pages.css">${rtl ? `
  <link rel="stylesheet" href="assets/liora/liora-rtl.css">` : ''}
  <script src="assets/liora/liora-card-gallery.js" defer></script>
  <script src="assets/liora/liora-calculator.js?v=${calculatorJsVersion}" defer></script>
  <script type="application/ld+json">
${JSON.stringify(schema, null, 2)}
  </script>
</head>
<body class="segment-page">
  ${nav(locale, 'guides.html')}
  ${breadcrumb(t('nav.buyingGuides', locale), [[t('breadcrumb.developments', locale), 'developments.html']], locale)}
  <main>
    <section class="page-hero">
      <img src="assets/liora/projects/altos-de-marbella/media/aerial-dusk-pool.jpg" alt="Aerial dusk view of a new-build Costa del Sol residence and pool terrace" width="1920" height="1085" loading="eager" fetchpriority="high" decoding="async">
      <div class="hero-inner">
        <span class="kicker">Buying Guides</span>
        <h1 class="display-title">Costa del Sol <em>Buying Guides</em></h1>
        <p class="lead">Compare new-build apartments and penthouses by area, with real prices, availability and the local context you need before you shortlist.</p>
      </div>
    </section>
    <section class="section guides-list"><div class="section-inner">
      <div class="section-head"><span class="label">The Process</span><div class="rule"></div><h2 class="section-title">How buying <em>actually works</em></h2><p class="body-copy">Understand the process before you compare projects.</p></div>
      <div class="cards guides-grid">
        ${PROCESS_GUIDES.map(processGuideCard).join('\n        ')}
      </div>
    </div></section>
    <section class="section quiet-band guides-list"><div class="section-inner">
      <div class="section-head"><span class="label">By Area &amp; Property Type</span><div class="rule"></div><h2 class="section-title">Choose a <em>starting point</em></h2><p class="body-copy">Each guide covers only developments currently matching that area and property type, so the prices and availability shown are real, not indicative.</p></div>
      <div class="cards guides-grid">
        ${SEGMENTS.map(guideCard).join('\n        ')}
      </div>
    </div></section>
    ${guidesCalculatorSection()}
    ${faqSection(GENERAL_FAQS)}
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
  return localizeInternalLinks(applySegmentPageTranslations(html, locale), locale);
}

// Same general buyer-process FAQ used on every property page
// (DEFAULT_FAQS in build_property_pages.mjs), duplicated here since this
// script is a separate, self-contained generator.
const GENERAL_FAQS = [
  ['Can foreigners buy property in Spain?', 'Yes. There are no restrictions on non-Spanish nationals buying property in Spain, whether as a resident or non-resident.'],
  ['What is an NIE number and do I need one?', 'An NIE (Numero de Identificacion de Extranjero) is a tax ID number required for any property purchase in Spain by a non-Spanish national. Nueva Living can guide you through obtaining one before you reserve.'],
  ['What costs should I budget for on top of the purchase price?', 'Buyers typically budget for transfer tax or VAT, notary fees, land registry fees and legal fees on top of the purchase price. Nueva Living provides a full, current cost breakdown for your chosen residence before you reserve.'],
  ['Can I get a mortgage in Spain as a non-resident?', 'Many Spanish banks offer mortgages to non-resident buyers, typically financing a portion of the purchase price. Exact terms depend on the bank and your personal financial profile.'],
  ['What is the difference between off-plan and completed properties?', 'Off-plan means the development is still under construction and is usually sold with staged payments through to completion. A completed property is ready to view and move into now.'],
  ['How does the reservation and payment process work?', 'Reservation and payment structures vary by development and are set out in full before you reserve. Nueva Living reconfirms the current schedule for your chosen residence at every step.'],
  ['Can I rent out the property after purchase?', 'This depends on the individual development and local regulations, which can vary by community and municipality. Nueva Living will confirm the specific rules for a development before you reserve.'],
  ['Do I need a lawyer?', 'Yes, we strongly recommend independent legal representation for any property purchase in Spain. Nueva Living can put you in touch with independent lawyers experienced in Costa del Sol property.']
];

function generalFaqSchema() {
  return {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: GENERAL_FAQS.map(([question, answer]) => ({
      '@type': 'Question',
      name: question,
      acceptedAnswer: { '@type': 'Answer', text: answer }
    }))
  };
}

const SEGMENTS = [
  {
    output: 'new-build-apartments-penthouses-marbella.html',
    area: 'marbella',
    areaLabel: 'Marbella',
    areaHref: 'area-marbella.html',
    propertyTypes: ['apartment', 'penthouse'],
    breadcrumbLabel: 'Apartments & Penthouses',
    title: 'New-Build Apartments & Penthouses in Marbella | Nueva Living',
    description: 'Compare new-build apartments and penthouses across Marbella’s Golf Valley, Elevated Coastline and Marbella West, with real prices, availability and floorplans from Nueva Living.',
    kicker: 'Marbella &middot; Apartments &amp; Penthouses',
    heroTitleHtml: 'New-Build Apartments &amp; Penthouses in <em>Marbella</em>',
    heroLead: 'Compare current apartment and penthouse developments across Marbella, from golf-course settings to elevated sea views, with real prices and availability confirmed before you view.',
    hero: {
      image: 'assets/liora/projects/alisios-residences/hero.jpg',
      alt: 'Aerial view of a new-build apartment and penthouse development framed by the Guadalmina golf course and the Mediterranean, Marbella',
      width: 1920,
      height: 1360,
      position: 'center 55%'
    },
    introLabel: 'Buying In Marbella',
    introHeadlineHtml: 'One municipality, <em>three very different addresses</em>',
    introParagraphs: [
      'Marbella is not one property market. An apartment in Guadalmina Golf, a penthouse on the elevated coastline of Marbella East and a resort-style residence near San Pedro Alcántara are different homes for different buyers, even though all three sit within Marbella.',
      'New-build apartments and penthouses here are typically sold off-plan or under construction, with staged payments through to completion. Nueva Living reconfirms the current price list, floorplans and payment schedule for any development before you shortlist it.'
    ],
    quickFacts: [
      ['Buyer Profile', 'Suits both primary residence and lock-and-leave second-home buyers.'],
      ['Typical Status', 'Most current releases are off-plan or under construction, sold with staged payments.'],
      ['What Varies Most', 'Sub-area, floor level and view (golf, garden or sea) drive price more than the building itself.'],
      ['Before You Reserve', 'Nueva Living confirms current availability, price list and payment terms directly with the developer.']
    ],
    subareasHeadlineHtml: 'Three sub-areas, <em>three different homes</em>',
    subareas: [
      ['Golf Valley & Guadalmina', 'Quieter, golf-course-facing apartments and penthouses close to San Pedro Alcántara and Puerto Banús, popular with buyers who want green space and easy access without being on the beachfront.'],
      ['Marbella East', 'An elevated, more residential coastline with sea-facing homes and a calmer setting than central Marbella, generally suited to buyers prioritising views and privacy over walkability.'],
      ['Marbella West / San Pedro', 'Newer, larger resort-style developments with extensive shared amenities, within walking distance of the beach and San Pedro’s services.']
    ],
    developmentsHeadlineHtml: 'Current apartment &amp; penthouse <em>developments</em>',
    amenitiesHeadlineHtml: 'Amenities to expect',
    amenitiesIntro: 'Specification varies by development, but current Marbella apartment and penthouse releases typically include some combination of the following.',
    comparisonHeadlineHtml: 'Apartment or penthouse <em>in Marbella?</em>',
    comparison: [
      ['Apartment', 'Usually the lower entry price for a given development, with lower service charges than a penthouse in the same building. Ground-floor units in these developments are often sold with a private garden rather than a terrace.'],
      ['Penthouse', 'Typically the largest terrace or roof solarium in the building and the best view, at a meaningful price premium over a mid-floor apartment. Service charges are usually higher, reflecting the larger private outdoor space.']
    ],
    faq: [
      ['Are service charges higher for a penthouse than an apartment in the same development?', 'Usually, yes. Service charges are typically calculated on built size or a fixed per-unit share, and a penthouse’s larger terrace or solarium generally puts it in a higher share than a mid-floor apartment in the same building. Nueva Living confirms the exact community fee structure for any development before you reserve.'],
      ['Do ground-floor apartments come with a private garden?', 'In many of the developments we work with, yes, ground-floor units are sold with a private garden rather than the terrace that upper floors receive, though this varies by development and by building layout. We confirm this unit by unit.'],
      ['Is a golf-view or sea-view unit significantly more expensive than a garden-view unit in the same building?', 'View typically carries a real premium within the same development, though the size of that premium varies by project and by floor. Comparing the current price list across several units in the same building is the most reliable way to see it.'],
      ['Can I still use the pool and gym if I only visit a few months a year?', 'Yes. Community amenities such as pools, gyms and gardens are available to owners year-round regardless of how often you visit, and are covered by the community service charge whether you use them or not.'],
      ['Do these developments allow short-term holiday rental?', 'This depends on the individual development’s community rules and the local municipal licence requirements, which can differ between Marbella’s sub-areas. Nueva Living confirms the specific rental position for a development before you reserve.']
    ]
  },
  {
    output: 'new-build-apartments-penthouses-estepona.html',
    area: 'estepona',
    areaLabel: 'Estepona',
    areaHref: 'area-estepona.html',
    propertyTypes: ['apartment', 'penthouse'],
    breadcrumbLabel: 'Apartments & Penthouses',
    title: 'New-Build Apartments & Penthouses in Estepona | Nueva Living',
    description: 'Compare new-build apartments and penthouses in Estepona, from the New Golden Mile to the town centre, with real prices, availability and floorplans from Nueva Living.',
    kicker: 'Estepona &middot; Apartments &amp; Penthouses',
    heroTitleHtml: 'New-Build Apartments &amp; Penthouses in <em>Estepona</em>',
    heroLead: 'Compare current apartment and penthouse developments across Estepona, from low-rise garden homes on the New Golden Mile to gated communities in the town centre, with real prices and availability confirmed before you view.',
    hero: {
      image: 'assets/liora/projects/jardin-del-mar-residences/hero.jpg',
      alt: 'Exterior view of a new-build apartment and penthouse development with a palm-lined pool terrace, Estepona',
      width: 1920,
      height: 1097,
      position: 'center 50%'
    },
    introLabel: 'Buying In Estepona',
    introHeadlineHtml: 'The Costa del Sol’s <em>fastest-growing market</em>',
    introParagraphs: [
      'Estepona has been the most active new-build market on the Costa del Sol in recent years, and it covers more than one kind of address. A low-rise garden apartment on the New Golden Mile and a gated penthouse in the town centre are both "Estepona", but they suit different buyers.',
      'New-build apartments and penthouses here are typically sold off-plan, with staged payments through to completion. Nueva Living reconfirms the current price list, floorplans and payment schedule for any development before you shortlist it.'
    ],
    quickFacts: [
      ['Buyer Profile', 'Suits both primary residence and lock-and-leave second-home buyers.'],
      ['Typical Status', 'Current releases are off-plan, sold with staged payments through to completion.'],
      ['What Varies Most', 'New Golden Mile developments favour space and resort amenities; central Estepona favours walkability.'],
      ['Before You Reserve', 'Nueva Living confirms current availability, price list and payment terms directly with the developer.']
    ],
    subareasHeadlineHtml: 'Two sub-areas, <em>two different homes</em>',
    subareas: [
      ['Cancelada & New Golden Mile', 'Low-rise garden apartments and penthouses set within a wider resort-style development, with generous private outdoor space and shared amenities such as pools, padel and spa facilities.'],
      ['Central Estepona', 'Gated communities within walking distance of the old town and seafront promenade, generally smaller in scale with a stronger emphasis on wellness amenities and lock-and-leave convenience.']
    ],
    developmentsHeadlineHtml: 'Current apartment &amp; penthouse <em>developments</em>',
    amenitiesHeadlineHtml: 'Amenities to expect',
    amenitiesIntro: 'Specification varies by development, but current Estepona apartment and penthouse releases typically include some combination of the following.',
    comparisonHeadlineHtml: 'Apartment or penthouse <em>in Estepona?</em>',
    comparison: [
      ['Apartment', 'Usually the lower entry price for a given development, with lower service charges than a penthouse in the same building. Ground-floor units in these developments are often sold with a private garden rather than a terrace.'],
      ['Penthouse', 'Typically the largest terrace or roof solarium in the building and the best view, at a meaningful price premium over a mid-floor apartment. Service charges are usually higher, reflecting the larger private outdoor space.']
    ],
    faq: [
      ['What is the difference between buying on the New Golden Mile and in central Estepona?', 'The New Golden Mile generally offers larger, more resort-style developments with more shared amenities and land around each building, while central Estepona offers smaller, more walkable developments closer to the old town and seafront. Both are typically sold off-plan. Nueva Living can talk through which setting suits your priorities.'],
      ['Are service charges higher for a penthouse than an apartment in the same development?', 'Usually, yes. Service charges are typically calculated on built size or a fixed per-unit share, and a penthouse’s larger terrace or solarium generally puts it in a higher share than a mid-floor apartment in the same building. Nueva Living confirms the exact community fee structure for any development before you reserve.'],
      ['Do ground-floor apartments come with a private garden?', 'In many of the developments we work with, yes, ground-floor units are sold with a private garden rather than the terrace that upper floors receive, though this varies by development and by building layout. We confirm this unit by unit.'],
      ['Can I still use the pool, spa and gym if I only visit a few months a year?', 'Yes. Community amenities are available to owners year-round regardless of how often you visit, and are covered by the community service charge whether you use them or not.'],
      ['Do these developments allow short-term holiday rental?', 'This depends on the individual development’s community rules and the local municipal licence requirements. Nueva Living confirms the specific rental position for a development before you reserve.']
    ]
  },
  {
    output: 'new-build-apartments-penthouses-nueva-andalucia.html',
    area: 'nueva-andalucia',
    areaLabel: 'Nueva Andalucía',
    areaHref: 'area-nueva-andalucia.html',
    propertyTypes: ['apartment', 'penthouse'],
    breadcrumbLabel: 'Apartments & Penthouses',
    title: 'New-Build Apartments & Penthouses in Nueva Andalucia',
    description: 'Compare new-build apartments and penthouses in Nueva Andalucia\'s Golf Valley, minutes from Puerto Banus, with real prices, availability and floorplans from Nueva Living.',
    kicker: 'Nueva Andaluc&iacute;a &middot; Apartments &amp; Penthouses',
    heroTitleHtml: 'New-Build Apartments &amp; Penthouses in <em>Nueva Andaluc&iacute;a</em>',
    heroLead: 'Compare current apartment and penthouse developments in Nueva Andalucía’s Golf Valley, minutes from Puerto Banús, with real prices and availability confirmed before you view.',
    hero: {
      image: 'assets/liora/projects/los-olivos-residences/hero.jpg',
      alt: 'Aerial view of a new-build apartment and penthouse development under construction in Nueva Andalucía’s Golf Valley, Marbella, with the coastline beyond',
      width: 1920,
      height: 1078,
      position: 'center 50%'
    },
    introLabel: 'Buying In Nueva Andalucía',
    introHeadlineHtml: 'Golf Valley, <em>minutes from Puerto Banús</em>',
    introParagraphs: [
      'Nueva Andalucía’s Golf Valley is one of the most established gated-community settings on the Costa del Sol: green, quiet and close to golf courses, yet a short drive from Puerto Banús and the beach.',
      'New-build apartments and penthouses here are typically sold off-plan or under construction, with staged payments through to completion. Nueva Living reconfirms the current price list, floorplans and payment schedule for any development before you shortlist it.'
    ],
    quickFacts: [
      ['Buyer Profile', 'Suits both primary residence and lock-and-leave second-home buyers.'],
      ['Typical Status', 'Current releases are under construction, sold with staged payments through to completion.'],
      ['What Varies Most', 'Floor level and outlook (golf course or communal gardens) drive price more than the building itself.'],
      ['Before You Reserve', 'Nueva Living confirms current availability, price list and payment terms directly with the developer.']
    ],
    subareasHeadlineHtml: 'What Golf Valley <em>living means</em>',
    subareas: [
      ['A Golf-Course Setting', 'Developments are built around or alongside golf courses, giving most residences an open, green outlook rather than a dense urban one.'],
      ['Minutes From Puerto Banús', 'Golf Valley sits a short drive from Puerto Banús and the Golden Mile, keeping restaurants, marina life and the beach close without living directly on top of them.'],
      ['Gated & Resort-Style', 'Current developments in this pocket are gated communities with 24-hour security and shared wellness amenities such as pools, spas and social lounges.']
    ],
    developmentsHeadlineHtml: 'Current apartment &amp; penthouse <em>developments</em>',
    amenitiesHeadlineHtml: 'Amenities to expect',
    amenitiesIntro: 'Specification varies by development, but current Nueva Andalucía apartment and penthouse releases typically include some combination of the following.',
    comparisonHeadlineHtml: 'Apartment or penthouse <em>in Nueva Andalucía?</em>',
    comparison: [
      ['Apartment', 'Usually the lower entry price for a given development, with lower service charges than a penthouse in the same building. Ground-floor units in these developments are often sold with a private garden rather than a terrace.'],
      ['Penthouse', 'Typically the largest terrace or roof solarium in the building and the best view, at a meaningful price premium over a mid-floor apartment. Service charges are usually higher, reflecting the larger private outdoor space.']
    ],
    faq: [
      ['How far is Golf Valley from Puerto Banús and the beach?', 'Golf Valley is a short drive from both, typically well under fifteen minutes depending on the exact development and time of day. It is close enough for regular use without the traffic and noise of being directly on the Golden Mile.'],
      ['Are service charges higher for a penthouse than an apartment in the same development?', 'Usually, yes. Service charges are typically calculated on built size or a fixed per-unit share, and a penthouse’s larger terrace or solarium generally puts it in a higher share than a mid-floor apartment in the same building. Nueva Living confirms the exact community fee structure for any development before you reserve.'],
      ['Do ground-floor apartments come with a private garden?', 'In many of the developments we work with, yes, ground-floor units are sold with a private garden rather than the terrace that upper floors receive, though this varies by development and by building layout. We confirm this unit by unit.'],
      ['Is a golf-view unit significantly more expensive than a garden-view unit in the same building?', 'View typically carries a real premium within the same development, though the size of that premium varies by project and by floor. Comparing the current price list across several units in the same building is the most reliable way to see it.'],
      ['Can I still use the pool, spa and gym if I only visit a few months a year?', 'Yes. Community amenities are available to owners year-round regardless of how often you visit, and are covered by the community service charge whether you use them or not.']
    ]
  }
];

const written = [];
for (const segment of SEGMENTS) {
  for (const { code: locale } of LOCALES) {
    const outputPath = localizedPath(segment.output, locale);
    if (outputPath.includes('/')) mkdirSync(outputPath.split('/')[0], { recursive: true });
    writeFileSync(outputPath, renderSegmentPage(segment, locale));
    written.push(outputPath);
  }
}

for (const { code: locale } of LOCALES) {
  const outputPath = localizedPath('guides.html', locale);
  if (outputPath.includes('/')) mkdirSync(outputPath.split('/')[0], { recursive: true });
  writeFileSync(outputPath, renderGuidesPage(locale));
  written.push(outputPath);
}

console.log(JSON.stringify({ written }, null, 2));
