import { existsSync, readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

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

const navLinks = [
  ['Buying Guides', 'guides.html'],
  ['Why Nueva', 'why-nueva.html'],
  ['Developments', 'developments.html'],
  ['Areas', 'areas.html'],
  ['Advisory', 'advisory.html'],
  ['Contact Us', 'contact.html'],
];

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

function nav() {
  return `<nav class="site-nav">
    <div class="nav-links nav-links-left">
      ${navLinks.slice(0, 3).map(([label, href]) => `<a href="${href}">${label}</a>`).join('\n      ')}
    </div>
    <a class="nav-logo" href="${home}" aria-label="Nueva Living home">
      <img src="assets/liora/brand/nueva-living-hero-logo-transparent.png?v=7" alt="Nueva Living" width="420" height="100">
    </a>
    <div class="nav-links nav-links-right">
      ${navLinks.slice(3).map(([label, href]) => `<a href="${href}">${label}</a>`).join('\n      ')}
    </div>
    <button class="nav-burger" type="button" aria-label="Menu" aria-controls="mobileMenu" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
  </nav>
  <div class="mobile-menu" id="mobileMenu">
    ${navLinks.map(([label, href]) => `<a href="${href}">${label}</a>`).join('\n    ')}
  </div>`;
}

function breadcrumb(currentLabel, parents = []) {
  const parentItems = parents.map(([label, href]) => `<li><a href="${esc(href)}">${esc(label)}</a></li>`).join('\n      ');
  return `<nav class="breadcrumb-bar" aria-label="Breadcrumb">
    <ol class="breadcrumb-list">
      <li><a href="${home}">Home</a></li>${parentItems ? `
      ${parentItems}` : ''}
      <li><span aria-current="page">${esc(currentLabel)}</span></li>
    </ol>
  </nav>`;
}

function footer() {
  return `<footer>
    <div class="footer-grid">
      <div>
        <img class="footer-logo" src="assets/liora/brand/nueva-living-lockup-espresso-transparent.png?v=7" alt="Nueva Living" width="700" height="340" loading="lazy" decoding="async">
        <p class="footer-about">We help international buyers find and compare new-build and off-plan homes across the Costa del Sol.</p>
      </div>
      <div class="footer-col">
        <div class="footer-col-title">Company</div>
        <ul>
          <li><a href="why-nueva.html">Why Nueva Living</a></li>
          <li><a href="about.html">About</a></li>
          <li><a href="advisory.html">Advisory</a></li>
          <li><a href="contact.html">Contact Us</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <div class="footer-col-title">Projects</div>
        <ul>
          <li><a href="developments.html">All Developments</a></li>
          <li><a href="guides.html">Buying Guides</a></li>
          <li><a href="areas.html">Areas Overview</a></li>
          <li><a href="area-marbella.html">Marbella</a></li>
          <li><a href="area-estepona.html">Estepona</a></li>
          <li><a href="area-benahavis.html">Benahav&iacute;s</a></li>
          <li><a href="area-nueva-andalucia.html">Nueva Andaluc&iacute;a</a></li>
          <li><a href="area-mijas-fuengirola.html">Mijas &amp; Fuengirola</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <div class="footer-col-title">Contact</div>
        <ul>
          <li><a href="mailto:contact@nuevaliving.com">contact@nuevaliving.com</a></li>
          <li><a href="tel:+34645446624">+34 645 44 66 24</a></li>
          <li><a href="https://maps.google.com/?q=Avenida+del+Prado+71,+29660+Marbella,+M%C3%A1laga,+Spain" target="_blank" rel="noopener">Avenida del Prado 71, 29660 Marbella, M&aacute;laga, Spain</a></li>
        </ul>
        <div class="footer-col-title" style="margin-top:24px;">Legal</div>
        <ul>
          <li><a href="privacy-policy.html">Privacy Policy</a></li>
          <li><a href="legal-notice.html">Legal Notice</a></li>
          <li><a href="cookie-policy.html">Cookie Policy</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>Information presented on this website is for general marketing purposes only and does not constitute legal, financial or investment advice. Development details, prices, availability and delivery dates are subject to change without notice.</p>
      <span>&copy; 2026 Nueva Living &middot; LIORA LIVING SL. &middot; NIF B88827472</span>
    </div>
  </footer>`;
}

function segmentProjectCardGallery(project) {
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
  const arrows = items.length > 1
    ? `<button type="button" class="project-card-gallery-arrow project-card-gallery-arrow--prev" data-gallery-prev aria-label="Previous image">&#8249;</button>
      <button type="button" class="project-card-gallery-arrow project-card-gallery-arrow--next" data-gallery-next aria-label="Next image">&#8250;</button>`
    : '';

  return `<div class="project-card-gallery" data-project-card-gallery data-card-url="${esc(project.output)}">
      <div class="project-card-gallery-track" data-gallery-track>${slides}
      </div>
      ${arrows}
      ${dots}
    </div>`;
}

function segmentProjectCard(project) {
  const meta = project.card?.meta || [
    ['From', (project.hero?.startingPrice || '').replace(/^From\s+/i, '') || 'On request'],
    ['Type', project.hero?.type || 'Residences'],
    ['Delivery', project.hero?.delivery || 'On request']
  ];
  return `<article class="project-card area-project-card" data-project-card>
    ${segmentProjectCardGallery(project)}
    <div class="project-body">
      <span class="label">${esc(project.card?.label || project.hero?.location || 'New Development')}</span>
      <h3>${esc(project.name)}</h3>
      <p>${esc(project.card?.description || project.description)}</p>
      <div class="meta">${meta.slice(0, 3).map(([label, value]) => `<div><span>${esc(label)}</span><strong>${esc(value)}</strong></div>`).join('')}</div>
      <a class="project-link" href="${esc(project.output)}">Explore Project</a>
    </div>
  </article>`;
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

function renderSegmentPage(segment) {
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
      ${matches.length ? matches.map(segmentProjectCard).join('\n      ') : `<article class="area-project-empty"><span class="label">Private Selection</span><h3>Current opportunities available by request</h3><p>We do not publish a development here until its information is ready to compare. Tell us what you need and we will check current releases directly.</p><a class="project-link" href="contact.html?intent=${encodeURIComponent(segment.title)}#contact-form">Request a Shortlist</a></article>`}
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
      <a class="btn" href="contact.html?intent=${encodeURIComponent(segment.title)}#contact-form">Request a Personal Shortlist</a>
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

  return `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>${esc(segment.title)}</title>
  <meta name="description" content="${esc(segment.description)}">
  <link rel="icon" href="assets/liora/liora-favicon-512.png?v=6" type="image/png" sizes="512x512">
  <link rel="icon" href="assets/liora/favicon-32.png?v=6" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="assets/liora/apple-touch-icon.png?v=6" sizes="180x180">
${fontPreloadBlock}
  <link rel="stylesheet" href="assets/fonts/google/liora-fonts.css">
  <link rel="stylesheet" href="assets/liora/liora-pages.css">
  <script src="assets/liora/liora-card-gallery.js" defer></script>
  <script type="application/ld+json">
${JSON.stringify(schema, null, 2)}
  </script>
</head>
<body class="segment-page">
  ${nav()}
  ${breadcrumb(segment.breadcrumbLabel, [['Developments', 'developments.html'], [segment.areaLabel, segment.areaHref]])}
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
  ${footer()}
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
</body>
</html>`;
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

function renderGuidesPage() {
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
    }
  ];

  return `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>${esc(title)}</title>
  <meta name="description" content="${esc(description)}">
  <link rel="icon" href="assets/liora/liora-favicon-512.png?v=6" type="image/png" sizes="512x512">
  <link rel="icon" href="assets/liora/favicon-32.png?v=6" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="assets/liora/apple-touch-icon.png?v=6" sizes="180x180">
${fontPreloadBlock}
  <link rel="stylesheet" href="assets/fonts/google/liora-fonts.css">
  <link rel="stylesheet" href="assets/liora/liora-pages.css">
  <script src="assets/liora/liora-card-gallery.js" defer></script>
  <script type="application/ld+json">
${JSON.stringify(schema, null, 2)}
  </script>
</head>
<body class="segment-page">
  ${nav()}
  ${breadcrumb('Buying Guides', [['Developments', 'developments.html']])}
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
      <div class="section-head"><span class="label">By Area &amp; Property Type</span><div class="rule"></div><h2 class="section-title">Choose a <em>starting point</em></h2><p class="body-copy">Each guide covers only developments currently matching that area and property type, so the prices and availability shown are real, not indicative.</p></div>
      <div class="cards guides-grid">
        ${SEGMENTS.map(guideCard).join('\n        ')}
      </div>
    </div></section>
  </main>
  ${footer()}
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
</body>
</html>`;
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
    title: 'New-Build Apartments & Penthouses in Nueva Andalucia | Nueva Living',
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

for (const segment of SEGMENTS) {
  const html = renderSegmentPage(segment);
  writeFileSync(segment.output, html);
}

writeFileSync('guides.html', renderGuidesPage());

console.log(JSON.stringify({ written: [...SEGMENTS.map((s) => s.output), 'guides.html'] }, null, 2));
