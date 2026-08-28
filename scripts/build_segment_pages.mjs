import { existsSync, readFileSync, readdirSync, writeFileSync, mkdirSync } from 'node:fs';
import { organizationSchema } from './lib/brand.mjs';
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
  renderGuidesMenu,
  renderAreasMenu,
  guidesMobileLinks,
  renderDrawerActions,
  LANG_SWITCHER_SCRIPT,
  localizeInternalLinks,
  seoTags
} from './lib/i18n.mjs';
import { renderUnifiedCard } from './lib/project_card.mjs';
import { renderProjectCardGallery } from './lib/card_gallery.mjs';
import { SEGMENT_PAGE_ENTRIES } from './lib/segment_page_translations.mjs';
import { SEGMENT_CLUSTER_ENTRIES } from './lib/segment_page_translations_clusters.mjs';
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
const SORTED_SEGMENT_PAGE_ENTRIES = [...SEGMENT_PAGE_ENTRIES, ...SEGMENT_CLUSTER_ENTRIES, ...PROJECT_CARD_ENTRIES, ...EDITORIAL_ALT_ENTRIES]
  .sort((a, b) => b.find.length - a.find.length);

function cardDescriptionReplacements(locale) {
  const replacements = [];
  for (const project of projects) {
    const en = project.card?.description || project.description;
    const translated = project.i18n?.[locale]?.card?.description;
    if (!en || !translated || en === translated) continue;
    // Both markup shapes: the card's paragraph carries a class now, and a
    // bare-<p> key silently stopped matching when it gained one.
    replacements.push([`<p class="dev-tagline">${en}</p>`, `<p class="dev-tagline">${translated}</p>`]);
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

// The breadcrumb and its BreadcrumbList both named the area in English on
// every locale, because the label is plain segment data rather than a string
// key. Falls back to the English label so a new segment without a key still
// builds.
// The breadcrumb's own label was raw English too -- "Elviria" sat under a
// Russian trail, while its sibling segments happened to read correctly only
// because "Apartments & Penthouses" has a translation-table entry.
// Amenities were Title-Cased for display and then looked up in a dictionary
// keyed in sentence case, so the lookup never matched and every locale showed
// "Wellness Room With Sauna And Hammam" in English. Translating first fixes
// the match; Title Case then has to stop at English, because it is wrong
// typography in Spanish, French and the rest -- German capitalises its nouns
// through the translation itself.
const AMENITY_DICTIONARY = JSON.parse(
  readFileSync(join(process.cwd(), 'content', 'i18n', 'amenities.json'), 'utf8')
);

function localizedAmenity(amenity, locale) {
  const titleCase = (value) => value.replace(/(^|[\s-])[a-z]/g, (c) => c.toUpperCase());
  if (locale === DEFAULT_LOCALE) return titleCase(amenity);
  const translated = AMENITY_DICTIONARY[amenity]?.[locale];
  return translated || titleCase(amenity);
}

function localizedBreadcrumbLabel(segment, locale) {
  return segment.breadcrumbLabelKey ? t(segment.breadcrumbLabelKey, locale) : segment.breadcrumbLabel;
}

function localizedAreaLabel(segment, locale) {
  return segment.areaLabelKey ? t(segment.areaLabelKey, locale) : segment.areaLabel;
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
    // The same sentence appears twice on these pages: once in the visible
    // markup with "&amp;", once inside the JSON-LD with a raw "&". Entries
    // are written against the markup, so the structured data was never
    // touched -- six segment pages per locale served Google an English
    // schema.org name under a fully translated <h1>.
    if (entry.find.includes('&amp;')) {
      result = result.split(entry.find.split('&amp;').join('&'))
        .join(replacement.split('&amp;').join('&'));
    }
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
    [t('nav.developments', locale), 'developments.html'],
    [t('nav.about', locale), 'about.html'],
    [t('nav.advisory', locale), 'advisory.html'],
    [t('nav.contactUs', locale), 'contact.html'],
  ];
}

function nav(locale = DEFAULT_LOCALE, currentOutputPath = 'index.html') {
  const links = navLinks(locale);
  const link = (index) => {
    const [label, href] = links[index];
    return `<a href="${href}">${label}</a>`;
  };
  const switcher = renderLanguageSwitcher(currentOutputPath, locale);
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
          <li><a href="advisory.html">${t('nav.advisory', locale)}</a></li>
          <li><a href="referrals.html">${t('nav.referralAmbassador', locale)}</a></li>
          <li><a href="contact.html">${t('footer.contactUs', locale)}</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <div class="footer-col-title">${t('footer.projectsTitle', locale)}</div>
        <ul>
          <li><a href="developments.html">${t('nav.developments', locale)}</a></li>
          <li><a href="guides.html">${t('nav.buyingGuides', locale)}</a></li>
          <li><a href="areas.html">${t('nav.allAreas', locale)}</a></li>
          <li><a href="area-marbella.html">${t('area.marbella', locale)}</a></li>
          <li><a href="area-estepona.html">${t('area.estepona', locale)}</a></li>
          <li><a href="area-casares.html">${t('area.casares', locale)}</a></li>
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
          <li><a href="https://maps.google.com/?q=Avenida+del+Prado+71,+29660+Marbella,+M%C3%A1laga,+Spain" target="_blank" rel="noopener">Avenida del Prado 71, 29660 Marbella, M&aacute;laga, ${t('common.spain', locale)}</a></li>
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

// The audit asks for a live inventory count in the title and H1 -- the
// pattern every ranking competitor uses -- but only when it flatters. A
// hardcoded number goes stale the moment a unit sells, so it is resolved
// from the same availability data the page already displays.
//
// Rule from the audit: show the count only at 10 or above. "2 apartments for
// sale in Estepona" reads as an empty shop and costs the click, so below the
// threshold the sentence falls back to its countless form.
// Same treatment as the footer page template: the hero is the LCP element on
// these pages and was shipping as a 487-636KB JPEG with no modern format.
// Variant widths are discovered on disk, so a hero without them degrades to
// the original rather than emitting a broken srcset.
function heroPicture(hero) {
  const src = hero.image;
  const stem = src.replace(/\.[a-z]+$/i, '');
  const dir = stem.slice(0, stem.lastIndexOf('/'));
  const base = stem.slice(stem.lastIndexOf('/') + 1);
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
  const img = `<img src="${esc(src)}" alt="${esc(hero.alt)}" width="${hero.width}" height="${hero.height}"`
    + `${hero.position ? ` style="object-position:${esc(hero.position)}"` : ''} loading="eager" fetchpriority="high" decoding="async">`;
  if (!avif && !webp) return img;
  return `<picture>`
    + (avif ? `<source type="image/avif" srcset="${avif}" sizes="100vw">` : '')
    + (webp ? `<source type="image/webp" srcset="${webp}" sizes="100vw">` : '')
    + img + `</picture>`;
}

const COUNT_DISPLAY_MIN = 10;

function resolveCount(text, stats) {
  if (!text) return text;
  if (!text.includes('{count}')) return text;
  const n = stats?.availableTotal;
  if (typeof n === 'number' && n >= COUNT_DISPLAY_MIN) {
    return text.replace('{count}', String(n));
  }
  return text.replace(/\{count\}\s*/, '');
}

// Most segments are an area crossed with a property type. A cluster segment
// instead names its projects outright, because the thing it targets is a
// sub-area with no discovery.area of its own -- "New Golden Mile" is a real
// search term spanning several Estepona addresses, and nothing in the data
// models it. Listing slugs keeps that explicit and reviewable rather than
// inventing a second area taxonomy.
function matchProjects(segment) {
  if (segment.slugs) {
    return segment.slugs.map((slug) => {
      const project = projects.find((candidate) => candidate.slug === slug);
      if (!project) {
        throw new Error(`${segment.output}: lists slug "${slug}", which is not an active project. `
          + 'Remove it or fix the slug -- a cluster page silently missing a project is the bug '
          + 'this check exists to prevent.');
      }
      return project;
    });
  }
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

function segmentSchema(segment, matches, locale) {
  const url = `${siteUrl}/${segment.output}`;
  // The {count} placeholder has to be resolved here too. The <title> and the
  // H1 both run through resolveCount(); the JSON-LD did not, so structured
  // data was advertising a literal "{count} New-Build Apartments..." to
  // search engines on every segment page and on the guides hub.
  const stats = computeStats(matches);
  const name = resolveCount(segment.title, stats);
  return [
    // Who publishes this. Locale segment pages carried a CollectionPage and
    // nothing identifying the company behind it.
    organizationSchema(siteUrl, { description: t('org.description', locale) }),
    {
      '@context': 'https://schema.org',
      '@type': 'CollectionPage',
      name,
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
        { '@type': 'ListItem', position: 2, name: localizedAreaLabel(segment, locale), item: `${siteUrl}/${segment.areaHref}` },
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
    <div class="section-head"><span class="label">${esc(t('segment.inDetail', locale, { area: localizedAreaLabel(segment, locale) }))}</span><div class="rule"></div><h2 class="section-title">${segment.subareasHeadlineHtml}</h2></div>
    <div class="cards">
      ${segment.subareas.map(([title, copy], index) => `<article class="card"><div class="card-number">${String(index + 1).padStart(2, '0')}</div><h3>${esc(title)}</h3><p>${esc(copy)}</p></article>`).join('\n      ')}
    </div>
  </div></section>`;

  const developmentsSection = `<section class="section segment-developments"><div class="section-inner">
    <div class="section-head"><span class="label">Current Match</span><div class="rule"></div><h2 class="section-title">${segment.developmentsHeadlineHtml}</h2><p class="body-copy">Only developments currently matching this search are shown below. Price and availability are reconfirmed before a viewing.</p></div>
    <div class="project-grid area-project-grid">
      ${matches.length ? matches.map(segmentProjectCard).join('\n      ') : `<article class="area-project-empty"><span class="label">Private Selection</span><h3>Current opportunities available by request</h3><p>We do not publish a development here until its information is ready to compare. Tell us what you need and we will check current releases directly.</p><a class="project-link" href="contact.html#contact-form&intent=${encodeURIComponent(`${segment.breadcrumbLabel} in ${segment.areaLabel}`)}">Request a Shortlist</a></article>`}
    </div>
  </div></section>`;

  const amenitiesSection = amenities.length ? `<section class="section quiet-band segment-amenities"><div class="section-inner">
    <div class="section-head"><span class="label">What To Expect</span><div class="rule"></div><h2 class="section-title">${segment.amenitiesHeadlineHtml}</h2><p class="body-copy">${esc(segment.amenitiesIntro)}</p></div>
    <ul class="segment-amenity-list">
      ${amenities.map((amenity) => `<li>${esc(localizedAmenity(amenity, locale))}</li>`).join('\n      ')}
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
      <a class="btn" href="contact.html#contact-form&intent=${encodeURIComponent(`${segment.breadcrumbLabel} in ${segment.areaLabel}`)}">Request a Personal Shortlist</a>
    </div>
  </div></section>`;

  const otherSegments = SEGMENTS.filter((s) => s.output !== segment.output);
  const relatedSection = `<section class="section quiet-band segment-related"><div class="section-inner">
    <div class="section-head"><span class="label">Other Areas</span><div class="rule"></div><h2 class="section-title">More buying <em>guides</em></h2></div>
    <ul class="segment-related-list">
      ${otherSegments.map((s) => `<li><a href="${esc(s.output)}">${s.cardHeading ? esc(s.cardHeading) : `${esc(s.breadcrumbLabel)} in ${esc(s.areaLabel)}`}</a></li>`).join('\n      ')}
      <li><a href="guides.html">All Buying Guides</a></li>
    </ul>
  </div></section>`;

  const schema = segmentSchema(segment, matches, locale);

  const html = `<!doctype html>
<html lang="${meta.htmlLang}" dir="${meta.dir}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
${baseHrefTag(locale)}  <title>${esc(resolveCount(segment.title, stats))}</title>
  <meta name="description" content="${esc(segment.description)}">
${hreflangLinks(segment.output, siteUrl)}
${seoTags(segment.output, locale, { title: resolveCount(segment.title, stats), description: segment.description, image: `${siteUrl}/${segment.hero.image}` })}
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
  ${breadcrumb(localizedBreadcrumbLabel(segment, locale), [[t('breadcrumb.developments', locale), 'developments.html'], [localizedAreaLabel(segment, locale), segment.areaHref]], locale)}
  <main>
    <section class="page-hero">
      ${heroPicture(segment.hero)}
      <div class="hero-inner">
        <span class="kicker">${segment.kicker}</span>
        <h1 class="display-title">${resolveCount(segment.heroTitleHtml, stats)}</h1>
        <p class="lead">${esc(segment.heroLead)}</p>
      </div>
    </section>
    ${statsBand(stats)}
    <section class="section segment-intro"><div class="section-inner area-intro-layout">
      <div><span class="label">${esc(segment.introLabel)}</span><div class="rule"></div><h2 class="section-title">${segment.introHeadlineHtml}</h2>${segment.introParagraphs.map((p) => `<p class="body-copy">${esc(p)}</p>`).join('\n')}${segment.areaLinkHtml ? `\n<p class="body-copy">${segment.areaLinkHtml}</p>` : ''}</div>
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
  return `<section class="section quiet-band guides-calculator" id="mortgage-calculator"><div class="section-inner">
    <div class="section-head center"><span class="label">Affordability</span><div class="rule"></div><h2 class="section-title">How Spanish mortgages <em>work for you</em></h2>
    <p class="body-copy" style="margin-left:auto;margin-right:auto;">Spanish banks lend differently to non-resident buyers than to Spanish residents. Where a resident might get financing up to 80% of a property's value, non-residents are typically capped closer to 70%, and the exact rate, term and how much of your income counts all vary by bank and by your personal financial profile. On top of the mortgage itself, budget for taxes and purchase costs &mdash; transfer tax or VAT, notary, land registry and legal fees &mdash; which typically add another 10-13% on top of the purchase price in Spain.</p>
    <p class="body-copy" style="margin-left:auto;margin-right:auto;">Use the calculator below for a realistic starting estimate of your deposit, monthly payment and total cost of buying, based on typical non-resident lending terms. It is a planning tool, not a mortgage offer &mdash; Nueva Living and your mortgage broker will confirm the real numbers once you have a specific property in mind.</p>
    </div>
    <div class="calculator-panel" data-calculator>
      <div class="calculator-inputs">
        <div class="calculator-field calculator-field--dual">
          <div class="calculator-field-label"><span id="calc-price-label">Purchase price</span><em data-calc-price-readout>&euro;0</em></div>
          <input type="range" data-calc-price-range aria-labelledby="calc-price-label" min="150000" max="3000000" step="5000" value="${seedPrice}">
          <input type="number" data-calc-price aria-labelledby="calc-price-label" value="${seedPrice}" min="0" step="1000" class="calculator-field-number">
        </div>
        <div class="calculator-field calculator-field--dual">
          <div class="calculator-field-label"><span id="calc-deposit-label">Deposit</span><em data-calc-deposit-readout>30% &middot; &euro;0</em></div>
          <input type="range" data-calc-deposit aria-labelledby="calc-deposit-label" min="10" max="100" step="5" value="30">
          <em class="calculator-field-hint">Set to 30% by default &mdash; as a non-Spanish resident, lenders typically finance up to 70% of the property value. Your own maximum will depend on your bank and financial profile.</em>
        </div>
        <div class="calculator-field calculator-field--dual">
          <div class="calculator-field-label"><span id="calc-term-label">Mortgage term</span><em data-calc-term-readout>25 years</em></div>
          <input type="range" data-calc-term aria-labelledby="calc-term-label" min="5" max="35" step="1" value="25">
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
    output: 'guide-buying-from-abroad-spain.html',
    kicker: 'Buying Guide',
    title: 'Buying from Abroad',
    description: 'What a purchase actually needs you present for: when the NIE is required, what a power of attorney covers, and how the money reaches the developer.',
    image: 'assets/nueva/journey/project-review-v2-1200.webp',
    alt: 'Buyer reviewing project documents remotely'
  },
  {
    output: 'guide-bank-guarantee-off-plan-spain.html',
    kicker: 'Buying Guide',
    title: 'Bank Guarantees Explained',
    description: 'What actually protects an off-plan deposit under Spanish law, and the point in the timeline at which the statutory guarantee has not started yet.',
    image: 'assets/nueva/journey/reservation-legal-1200.webp',
    alt: 'Buyer reviewing purchase contract documents with legal guidance'
  },
  {
    output: 'guide-off-plan-payment-schedules.html',
    kicker: 'Buying Guide',
    title: 'Off-Plan Payment Schedules',
    description: 'The staged payment structures the developers on this site have supplied in writing, from reservation through to the balance at deed.',
    image: 'assets/nueva/journey/project-review-v2-1200.webp',
    alt: 'Reviewing a development payment schedule and floorplans'
  },
  {
    output: 'guide-new-build-warranties-snagging.html',
    kicker: 'Buying Guide',
    title: 'Warranties and Snagging',
    description: 'The ten, three and one-year guarantees on a Spanish new-build, who is liable under each, and why the handover inspection starts the clock.',
    image: 'assets/nueva/journey/completion-aftercare-1200.webp',
    alt: 'Handover inspection of a completed new-build residence'
  },
  {
    output: 'guide-purchase-costs-andalucia.html',
    kicker: 'Buying Guide',
    title: 'New-Build Purchase Costs',
    description: 'What a new-build in Andalucia costs on top of the price: IVA at 10%, AJD at 1.2%, and the notary, registry and legal fees around them.',
    image: 'assets/liora/viewing/scene-13.jpg',
    alt: 'Costa del Sol new-build residence viewed from its terrace'
  },
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
        <h3>${segment.cardHeading ? esc(segment.cardHeading) : `${esc(segment.breadcrumbLabel)} in ${esc(segment.areaLabel)}`}</h3>
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
    organizationSchema(siteUrl, { description: t('org.description', locale) }),
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
        name: resolveCount(segment.title, computeStats(matchProjects(segment)))
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
      ${heroPicture({ image: 'assets/liora/projects/altos-de-marbella/media/aerial-dusk-pool.jpg', alt: 'Aerial dusk view of a new-build Costa del Sol residence and pool terrace', width: 1920, height: 1085 })}
      <div class="hero-inner">
        <span class="kicker">Buying Guides</span>
        <h1 class="display-title">Costa del Sol <em>Buying Guides</em></h1>
        <p class="lead">Compare new-build apartments and penthouses by area, with real prices, availability and the local context you need before you shortlist.</p>
      </div>
    </section>
    <section class="section guides-list"><div class="section-inner">
      <div class="section-head"><span class="label">The Process</span><div class="rule"></div><h2 class="section-title">How buying <em>actually works</em></h2><p class="body-copy">Understand the process before you compare projects.</p></div>
      <div class="cards guides-grid">
        ${PROCESS_GUIDES.filter((guide) => !guide.englishOnly || locale === DEFAULT_LOCALE).map(processGuideCard).join('\n        ')}
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
    output: 'new-build-homes-san-pedro-guadalmina.html',
    area: 'marbella',
    slugs: ['marbella-west-garden-residences', 'nueva-alcantara-residences', 'alisios-residences', 'cortijo-blanco-villa-collection'],
    areaLabel: 'San Pedro & Guadalmina',
    areaLabelKey: 'area.sanPedroGuadalmina',
    areaHref: 'area-marbella.html',
    propertyTypes: ['apartment', 'penthouse', 'villa'],
    breadcrumbLabel: 'San Pedro & Guadalmina',
    breadcrumbLabelKey: 'segment.newBuildHomes',
    cardHeading: 'New-Build Homes in San Pedro & Guadalmina',
    title: '{count} New-Build Homes in San Pedro & Guadalmina, Marbella',
    description: 'New-build apartments, penthouses and villas in San Pedro Alcantara and Guadalmina, western Marbella, from EUR 527,500. Real availability and delivery dates.',
    kicker: 'Marbella West &middot; San Pedro &amp; Guadalmina',
    heroTitleHtml: '{count} New-Build Homes for Sale in <em>San Pedro &amp; Guadalmina</em>',
    heroLead: 'Western Marbella between the town and Puerto Banús: a working Spanish high street on one side, four golf courses on the other, and the beach within walking distance of both.',
    hero: {
      image: 'assets/liora/projects/marbella-west-garden-residences/hero.jpg',
      alt: 'New-build residences with gardens in western Marbella between San Pedro Alcantara and Puerto Banús',
      width: 1920,
      height: 1280,
      position: 'center 55%'
    },
    introLabel: 'Buying In San Pedro & Guadalmina',
    introHeadlineHtml: 'A town that <em>works in February</em>',
    areaLinkHtml: 'Comparing across the municipality? Our guide to <a href="area-marbella.html">where to buy in Marbella, area by area</a> sets this stretch against Marbella East and the Golden Mile.',
    introParagraphs: [
      'San Pedro Alc\u00e1ntara is the part of Marbella that does not empty out in winter. It has its own high street, a plaza people actually use, schools, health centres and a boulevard down to the beach -- the things a resort address usually sends you elsewhere for. Guadalmina sits immediately west of it, quieter and built around the golf.',
      'The two together cover an unusually wide range: apartments from EUR 527,500 through to villas above EUR 4,000,000, within a few minutes of each other. Puerto Banús is five minutes east, which is close enough to use and far enough not to live in.'
    ],
    quickFacts: [
      ['Buyer Profile', 'Suits year-round residents, families using the international schools, and buyers who want Puerto Banús nearby without living beside it.'],
      ['Typical Status', 'Current releases are off-plan or under construction, sold with staged payments through to completion.'],
      ['What Varies Most', 'Format, more than location. The same few streets hold a EUR 527,500 apartment and a EUR 4,000,000 villa.'],
      ['Before You Reserve', 'Nueva Living confirms current availability, price list and payment terms directly with the developer.']
    ],
    subareasHeadlineHtml: 'Two neighbourhoods, <em>one stretch of coast</em>',
    subareas: [
      ['San Pedro Alc\u00e1ntara', 'A real town rather than a development: high street, market, schools and a boulevard to the beach. Walkable, level, and busy all year. The apartment stock sits here.'],
      ['Guadalmina', 'West of San Pedro and built around Guadalmina Golf, lower density and quieter. Established rather than growing, and where the golf-side apartments and villas are.'],
      ['Cortijo Blanco', 'The pocket between San Pedro and Puerto Banús, a few streets back from the promenade. Level, established, and within walking distance of both.']
    ],
    developmentsHeadlineHtml: 'Current <em>developments</em>',
    amenitiesHeadlineHtml: 'Amenities to expect',
    amenitiesIntro: 'Specification varies by development, but current releases on this stretch typically include some combination of the following.',
    comparisonHeadlineHtml: 'San Pedro or <em>Puerto Ban&uacute;s?</em>',
    comparison: [
      ['San Pedro & Guadalmina', 'More space for the money, a neighbourhood that functions year-round, and parking you can find. Five minutes from Puerto Banús by car. The trade is that the marina glamour is somewhere you visit rather than live in.'],
      ['Puerto Banús itself', 'The address, the marina and the walk-out nightlife, at a clear premium and with far less new-build stock. Better suited to short stays than to a household that needs a school run.']
    ],
    faq: [
      ['How far is San Pedro from Puerto Banús?', 'About five minutes by car, or a walk along the promenade from the eastern edge of San Pedro. Close enough to use the marina without living with its noise or its parking.'],
      ['Is San Pedro a real town or a resort?', 'A real town. It has a high street, a weekly market, schools, health centres and a resident population that stays through the winter -- which is not true of every address in Marbella. That is the main reason buyers choose it over the Golden Mile.'],
      ['What is the difference between San Pedro and Guadalmina?', 'San Pedro is the town: walkable, level, busy. Guadalmina is immediately west, lower density and organised around the golf course, with larger plots and less foot traffic. Prices in Guadalmina are generally higher for the same built area.'],
      ['Are the international schools nearby?', 'Yes. Several of the Costa del Sol\u2019s international schools sit in and around San Pedro and Guadalmina, which is a large part of why the area holds its year-round population. We can confirm distances for a specific development.'],
      ['Can I walk to the beach?', 'From most of San Pedro, yes -- the boulevard runs from the town centre down to the promenade. From the Guadalmina golf-side addresses it is a short drive. We confirm the actual walking distance for a development rather than relying on a brochure claim.']
    ]
  },
  {
    output: 'new-build-homes-elviria-marbella.html',
    area: 'marbella',
    slugs: ['elviria-hills-residences', 'laurel-hill-residences', 'elviria-woodland-residences'],
    areaLabel: 'Elviria',
    areaLabelKey: 'area.elviria',
    areaHref: 'area-marbella.html',
    propertyTypes: ['apartment', 'penthouse', 'villa', 'townhouse'],
    breadcrumbLabel: 'Elviria',
    breadcrumbLabelKey: 'segment.newBuildHomes',
    cardHeading: 'New-Build Homes in Elviria',
    title: '{count} New-Build Homes in Elviria, Marbella East',
    description: 'New-build apartments, townhouses and villas in Elviria on Marbella East, from EUR 690,000. Real availability, floorplans and delivery dates.',
    kicker: 'Marbella East &middot; Elviria',
    heroTitleHtml: '{count} New-Build Homes for Sale in <em>Elviria</em>',
    heroLead: 'The pine-covered hillside east of Marbella, where the beach clubs sit below and three golf courses sit behind, and where most of Marbella East\u2019s current new-build stock is concentrated.',
    hero: {
      image: 'assets/liora/projects/elviria-hills-residences/hero.jpg',
      alt: 'Elevated new-build residences among pines above the Elviria coastline, Marbella East',
      width: 1920,
      height: 1280,
      position: 'center 55%'
    },
    introLabel: 'Buying In Elviria',
    introHeadlineHtml: 'Marbella East, <em>at Marbella East prices</em>',
    areaLinkHtml: 'Comparing across the municipality? Our guide to <a href="area-marbella.html">where to buy in Marbella, area by area</a> sets Elviria against the Golden Mile and Marbella West.',
    introParagraphs: [
      'Elviria is the stretch of Marbella East between the A-7 and the pine hills behind it, about twenty minutes from the old town and the same again from the airport. It is residential rather than resort: a supermarket you actually use, international schools, and beach clubs that stay open through the winter.',
      'It also holds the largest concentration of new-build stock on this side of Marbella. The three current releases here run from EUR 690,000, which is roughly where Marbella starts, and they cover apartments, townhouses and villas rather than one format. All are under construction or off-plan with staged payments.'
    ],
    quickFacts: [
      ['Buyer Profile', 'Suits year-round residents and families as much as second-home buyers, helped by the schools and the everyday services.'],
      ['Typical Status', 'Every current release is under construction or off-plan, sold with staged payments through to completion.'],
      ['What Varies Most', 'Height. Elviria runs from the beach up into the hills, and the elevated plots carry both the sea views and the premium.'],
      ['Before You Reserve', 'Nueva Living confirms current availability, price list and payment terms directly with the developer.']
    ],
    subareasHeadlineHtml: 'One name, <em>three distinct heights</em>',
    subareas: [
      ['Elviria West', 'The growing edge closest to Marbella, elevated enough for sea views, with the golf courses and the beach clubs both within a short drive. Where most of the current apartment stock sits.'],
      ['Elviria Sur', 'The lower, flatter part nearer the coast, around three kilometres from Nikki Beach. The most walkable to the sand and the strongest for rental demand.'],
      ['The pine hills', 'Behind and above the rest, backing onto Santa Maria and Cabopino golf. Quieter and more private, and where the villa and woodland plots are.']
    ],
    developmentsHeadlineHtml: 'Current <em>developments</em>',
    amenitiesHeadlineHtml: 'Amenities to expect',
    amenitiesIntro: 'Specification varies by development, but current releases in Elviria typically include some combination of the following.',
    comparisonHeadlineHtml: 'Elviria or <em>central Marbella?</em>',
    comparison: [
      ['Elviria', 'More built area for the money, greener surroundings, and a genuine year-round neighbourhood with schools and services. The trade is that you drive to the old town and to Puerto Banús rather than walking.'],
      ['Central Marbella', 'Walkable to the old town and the promenade, and a shorter hop to Puerto Banús, at a clear premium per square metre. Better for short stays and for buyers who want the address more than the floor area.']
    ],
    faq: [
      ['How far is Elviria from Marbella old town?', 'Around fifteen to twenty minutes by car along the A-7, depending on where in Elviria you are and the time of year. The airport is a similar distance in the other direction, which is unusual on this coast -- most of Marbella is materially further from both.'],
      ['Is Elviria walkable, or do I need a car?', 'It depends on the height. Elviria Sur, nearer the coast, is walkable to the beach and to everyday shops. The elevated plots in Elviria West and the pine hills assume a car, which is also what buys the views and the quiet.'],
      ['What golf is nearby?', 'Santa Maria Golf and Cabopino Golf both sit directly behind Elviria, with Rio Real a short drive west. The woodland plots back onto the courses; the apartment releases are a few minutes away.'],
      ['Is Elviria good for letting?', 'Rental demand here is helped by the beach clubs and the schools, which pull both holiday and longer lets. Whether a specific development permits short-term letting depends on its community rules and the municipal licence position. Nueva Living confirms this for a development before you reserve.'],
      ['Why is Elviria cheaper than the Golden Mile?', 'Distance from central Marbella, and nothing else that matters. The build standard on the current releases is the same, and the plots are larger. Elviria starts around EUR 690,000 where the Golden Mile starts several times higher.']
    ]
  },
  {
    output: 'new-build-homes-new-golden-mile.html',
    area: 'estepona',
    slugs: [
      'vista-alta-suites',
      'jardin-del-mar-residences',
      'cancelada-park',
      'meridian-golf-villas',
      'fairway-grove-villas',
      'el-campanario-golf-villa',
      'bel-air-villa-collection'
    ],
    areaLabel: 'the New Golden Mile',
    areaLabelKey: 'area.newGoldenMile',
    areaHref: 'area-estepona.html',
    propertyTypes: ['apartment', 'penthouse', 'villa'],
    breadcrumbLabel: 'New Golden Mile',
    breadcrumbLabelKey: 'segment.newBuildHomes',
    // "New Golden Mile in the New Golden Mile" is what the default card
    // heading produces for a cluster whose label already names the place.
    cardHeading: 'New-Build Homes on the New Golden Mile',
    title: '{count} New-Build Homes on the New Golden Mile',
    description: 'New-build apartments, penthouses and villas on the New Golden Mile between Estepona and Puerto Banús, from EUR 695,000. Real availability and delivery dates.',
    kicker: 'Estepona &middot; New Golden Mile',
    heroTitleHtml: '{count} New-Build Homes for Sale on the <em>New Golden Mile</em>',
    heroLead: 'The stretch between Estepona and Puerto Banús, where beachside apartments and golf-side villas sit within a few minutes of each other.',
    hero: {
      image: 'assets/liora/projects/jardin-del-mar-residences/hero.jpg',
      alt: 'New-build residence with pool and gardens on the New Golden Mile between Estepona and Puerto Banús',
      width: 1920,
      height: 1280,
      position: 'center 55%'
    },
    introLabel: 'Buying On The New Golden Mile',
    introHeadlineHtml: 'Not Estepona, <em>not quite Marbella</em>',
    areaLinkHtml: 'Looking more widely? Our guide to <a href="area-estepona.html">where to buy in Estepona, area by area</a> sets the New Golden Mile against the town itself and the coast further west.',
    introParagraphs: [
      'The New Golden Mile is the coastal strip running from the eastern edge of Estepona up to Puerto Banús. It is its own market rather than a part of either: buyers who start in Marbella come here for space and newer stock, and buyers who start in Estepona come here for proximity to Puerto Banús.',
      'It is also unusually mixed. Within a few minutes of each other you will find beachside apartment releases from EUR 695,000 and golf-side villa collections up to EUR 3,500,000, which is why this page covers both rather than splitting them. Every current release here is off-plan or under construction with staged payments.'
    ],
    quickFacts: [
      ['Buyer Profile', 'Suits buyers who want Puerto Banús within reach without Marbella pricing, and families who need more built area than the Golden Mile offers.'],
      ['Typical Status', 'All current releases are off-plan or under construction, sold with staged payments through to completion.'],
      ['What Varies Most', 'Distance to the beach against distance to the golf. The apartment releases sit beachside; the villa collections sit inland around El Campanario.'],
      ['Before You Reserve', 'Nueva Living confirms current availability, price list and payment terms directly with the developer.']
    ],
    subareasHeadlineHtml: 'One strip, <em>three distinct pockets</em>',
    subareas: [
      ['Cancelada &amp; beachside', 'The most walkable part of the strip, with apartment and penthouse releases close to the beach and everyday services. The lower entry point on the New Golden Mile and the easiest to let.'],
      ['El Campanario', 'Inland and golf-facing, built around the golf and country club. Almost all of the villa stock on this stretch sits here, on larger plots than anything beachside.'],
      ['Bel Air', 'An established, low-density address at the Marbella end of the strip, closest to Puerto Banús, where new villa releases are small and infrequent.']
    ],
    developmentsHeadlineHtml: 'Current <em>developments</em>',
    amenitiesHeadlineHtml: 'Amenities to expect',
    amenitiesIntro: 'Specification varies by development, but current releases on this stretch typically include some combination of the following.',
    comparisonHeadlineHtml: 'Apartment or villa <em>on this stretch?</em>',
    comparison: [
      ['Apartment or penthouse', 'Beachside, walkable and from EUR 695,000. Community pools and gardens are maintained for you, which suits owners who are not here year-round. The practical choice if you want to be able to leave and lock the door.'],
      ['Villa', 'Golf-side around El Campanario, from EUR 1,550,000, on private plots with a private pool. More space and more privacy, and more to maintain: budget for a gardener and pool service whether you are here or not.']
    ],
    faq: [
      ['Where exactly is the New Golden Mile?', 'It is the coastal strip between the eastern edge of Estepona and Puerto Banús, taking in Cancelada, El Campanario and Bel Air. It is not an administrative area, which is why it does not appear on municipal maps, but it is how the stretch is bought and sold locally.'],
      ['Is it in Estepona or Marbella?', 'Almost all of it falls within the municipality of Estepona, with the Bel Air end closest to the Marbella boundary. For practical purposes -- taxes, licences, town hall -- treat it as Estepona.'],
      ['Why is it cheaper than the Golden Mile in Marbella?', 'It is further from central Marbella and it is newer, with more land still being built on. That is what keeps entry prices near EUR 695,000 here against Marbella pricing a few kilometres east. It is a location difference, not a build-quality one.'],
      ['Can I walk to the beach from these developments?', 'From the beachside apartment releases around Cancelada, generally yes. The villa collections around El Campanario are inland and golf-facing, so a car is assumed there. We confirm the actual walking distance for a specific development rather than relying on a brochure claim.'],
      ['Is there much difference in service charges between an apartment and a villa here?', 'They are different in kind rather than degree. An apartment carries a community charge covering shared pools, gardens and lighting. A villa usually carries a smaller community charge but takes on its own pool and garden maintenance directly, which often costs more in total once you add it up.']
    ]
  },
  {
    output: 'new-build-apartments-penthouses-mijas-fuengirola.html',
    area: 'mijas-fuengirola',
    areaLabel: 'Mijas & Fuengirola',
    areaLabelKey: 'area.mijasFuengirola',
    areaHref: 'area-mijas-fuengirola.html',
    propertyTypes: ['apartment', 'penthouse'],
    breadcrumbLabel: 'Apartments & Penthouses',
    title: '{count} New-Build Apartments & Penthouses in Mijas & Fuengirola',
    description: 'New-build apartments and penthouses in Mijas, Fuengirola and Benalmadena from EUR 390,000. Real availability, floorplans and delivery dates.',
    kicker: 'Mijas &amp; Fuengirola &middot; Apartments &amp; Penthouses',
    heroTitleHtml: '{count} New-Build Apartments &amp; Penthouses for Sale in <em>Mijas &amp; Fuengirola</em>',
    heroLead: 'The eastern stretch of the coast, where the same budget buys more floor area than it does in Marbella, with current releases in Mijas, Las Lagunas and Torremuelle.',
    hero: {
      image: 'assets/liora/projects/cerrado-vista-residences/media/sunset-terrace-coastal-view.jpg',
      alt: 'Penthouse terrace at sunset with panoramic views over the Mijas and Fuengirola coastline',
      width: 1920,
      height: 1127,
      position: 'center 55%'
    },
    introLabel: 'Buying In Mijas & Fuengirola',
    introHeadlineHtml: 'The same coast, <em>at a different price</em>',
    areaLinkHtml: 'Weighing up the towns? Our guide to <a href="area-mijas-fuengirola.html">where to buy in Mijas and Fuengirola</a> compares them on price, character and who each one suits.',
    introParagraphs: [
      'This is the part of the Costa del Sol where the arithmetic changes. Entry prices here start around EUR 390,000, against EUR 527,500 in Marbella for the same kind of home, and the gap widens once you compare built size rather than headline price.',
      'What you trade is prestige, not access. Malaga airport is closer from here than it is from Marbella, the train line runs to Fuengirola, and the golf courses at Mijas sit minutes inland. Current releases here are under construction or off-plan with staged payments, and Nueva Living reconfirms the price list, floorplans and payment schedule before you shortlist anything.'
    ],
    quickFacts: [
      ['Buyer Profile', 'Suits buyers who want coastal access and floor area over a Marbella address, and investors working to a yield rather than a trophy.'],
      ['Typical Status', 'Every current release is under construction or off-plan, sold with staged payments through to completion.'],
      ['What Varies Most', 'Position relative to the sea and the golf courses. Las Lagunas is inland and connected; Torremuelle sits above the water.'],
      ['Before You Reserve', 'Nueva Living confirms current availability, price list and payment terms directly with the developer.']
    ],
    subareasHeadlineHtml: 'Three settings, <em>three different trade-offs</em>',
    subareas: [
      ['Mijas', 'Inland and elevated, next to the golf courses, with the widest spread of prices on this stretch. Suits buyers who want space and green surroundings within a short drive of the beach rather than on it.'],
      ['Las Lagunas', 'Between Fuengirola and Mijas, the most connected of the three: everyday services, schools and the train line within reach. The practical choice for year-round living rather than seasonal use.'],
      ['Torremuelle, Benalmadena', 'A quieter pocket above the coastline east of Fuengirola, closer to Malaga than to Marbella, with sea-facing positions and a smaller, more private scale of development.']
    ],
    developmentsHeadlineHtml: 'Current apartment &amp; penthouse <em>developments</em>',
    amenitiesHeadlineHtml: 'Amenities to expect',
    amenitiesIntro: 'Specification varies by development, but current releases on this stretch typically include some combination of the following.',
    comparisonHeadlineHtml: 'Apartment or penthouse <em>on this stretch?</em>',
    comparison: [
      ['Apartment', 'The lower entry price in any given development, and where the value argument for this area is strongest: the price per built square metre here is materially below the equivalent in Marbella. Ground-floor units are often sold with a private garden.'],
      ['Penthouse', 'The largest terrace or solarium in the building and the best of the sea or golf view, at a premium over a mid-floor unit. On this coast a penthouse still frequently lands under what a mid-floor apartment costs further west.']
    ],
    faq: [
      ['Why are new-build prices lower here than in Marbella?', 'Land costs less on this stretch than it does between Marbella and Estepona, and that carries through to the finished price rather than reflecting a difference in build quality. Current releases here run from around EUR 390,000, against EUR 527,500 for the equivalent in Marbella.'],
      ['How far is Malaga airport?', 'Closer than it is from Marbella. Fuengirola, Mijas Costa and Benalmadena all sit on the airport side of the coast, which shortens the transfer at both ends of a trip and matters more than it sounds if you plan to visit often or rent the property out.'],
      ['Is there a train to this part of the coast?', 'Yes. The Cercanias line runs from Malaga and the airport to Fuengirola, which is unusual on this coast: Marbella and Estepona have no rail connection at all. It makes year-round living and car-free visits genuinely practical here.'],
      ['Are these developments suitable for holiday rental?', 'Rental demand on this stretch is strong and year-round rather than purely seasonal, helped by the airport proximity and the train. Whether a specific development permits short-term letting depends on its community rules and the municipal licence position, which differs between Mijas, Fuengirola and Benalmadena. Nueva Living confirms this for a development before you reserve.'],
      ['Is Benalmadena the same market as Mijas and Fuengirola?', 'It is a separate municipality with its own character, though it sits on the same stretch and buyers usually shop across all three. Torremuelle, where our current Benalmadena release sits, is a quieter residential pocket above the coastline rather than part of the busier Benalmadena Costa.']
    ]
  },
  {
    output: 'new-build-apartments-penthouses-marbella.html',
    area: 'marbella',
    areaLabel: 'Marbella',
    areaLabelKey: 'area.marbella',
    areaHref: 'area-marbella.html',
    propertyTypes: ['apartment', 'penthouse'],
    breadcrumbLabel: 'Apartments & Penthouses',
    title: '{count} New-Build Apartments & Penthouses in Marbella',
    description: 'New-build apartments and penthouses across Golf Valley, Marbella East and Marbella West, from €527,500. Real availability, floorplans and delivery dates.',
    kicker: 'Marbella &middot; Apartments &amp; Penthouses',
    heroTitleHtml: '{count} New-Build Apartments &amp; Penthouses for Sale in <em>Marbella</em>',
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
    areaLinkHtml: 'Still deciding on a neighbourhood? Our guide to <a href="area-marbella.html">where to buy in Marbella, area by area</a> compares the Golden Mile, Marbella East and Marbella West on price, character and who each one suits.',
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
    areaLabelKey: 'area.estepona',
    areaHref: 'area-estepona.html',
    propertyTypes: ['apartment', 'penthouse'],
    breadcrumbLabel: 'Apartments & Penthouses',
    title: 'New-Build Apartments & Penthouses in Estepona',
    description: 'New-build apartments and penthouses in Estepona, from the New Golden Mile to the town centre. From €720,000, with floorplans and delivery dates.',
    kicker: 'Estepona &middot; Apartments &amp; Penthouses',
    heroTitleHtml: '{count} New-Build Apartments &amp; Penthouses for Sale in <em>Estepona</em>',
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
    areaLinkHtml: 'If you are weighing up locations first, <a href="area-estepona.html">where to buy in Estepona</a> sets out the New Golden Mile, the town centre and Bahía Dorada side by side, with local asking prices.',
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
    areaLabelKey: 'area.nuevaAndalucia',
    areaHref: 'area-nueva-andalucia.html',
    propertyTypes: ['apartment', 'penthouse'],
    breadcrumbLabel: 'Apartments & Penthouses',
    title: 'New-Build Apartments & Penthouses in Nueva Andalucia',
    description: 'New-build apartments and penthouses in Nueva Andalucia\'s Golf Valley, minutes from Puerto Banús. From €450,000, with floorplans and delivery dates.',
    kicker: 'Nueva Andaluc&iacute;a &middot; Apartments &amp; Penthouses',
    heroTitleHtml: '{count} New-Build Apartments &amp; Penthouses for Sale in <em>Nueva Andaluc&iacute;a</em>',
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
    areaLinkHtml: 'For the wider picture, <a href="area-nueva-andalucia.html">where to buy in Nueva Andalucía</a> covers Las Brisas, Los Naranjos and Aloha, and how close each sits to Puerto Banús.',
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
