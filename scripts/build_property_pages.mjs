import { existsSync, readdirSync, readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';

const projectsDir = path.resolve('content/liora-projects');
const conventionalImageDir = 'assets/liora/projects';
const developmentsPage = path.resolve('developments.html');
const generatedProjectsStart = '<!-- NUEVA GENERATED PROJECTS START -->';
const generatedProjectsEnd = '<!-- NUEVA GENERATED PROJECTS END -->';
const siteUrl = 'https://nueva-living.com';
const fontPreloadBlock = `  <link rel="preload" href="assets/fonts/google/co3bmX5slCNuHLi8bLeY9MK7whWMhyjYqXtKky2F7g.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="assets/fonts/google/8vIJ7ww63mVu7gt79mT7PkRXMw.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="assets/fonts/google/JTUSjIg1_i6t8kCHKm459WlhyyTh89Y.woff2" as="font" type="font/woff2" crossorigin>`;

function esc(value = '') {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function attr(name, value) {
  return value === undefined || value === null || value === '' ? '' : ` ${name}="${esc(value)}"`;
}

function readJson(file) {
  return JSON.parse(readFileSync(file, 'utf8'));
}

function conventionalImage(slug, key) {
  const names = key === 'privateViewing' ? ['privateViewing', 'private-viewing'] : [key];
  const candidate = names
    .flatMap((name) => ['jpg', 'jpeg', 'png', 'webp'].map((ext) => path.join(conventionalImageDir, slug, `${name}.${ext}`)))
    .find((item) => existsSync(item));
  return candidate || '';
}

function image(project, key, fallback = {}) {
  const img = project.images?.[key] || {};
  return {
    ...fallback,
    ...img,
    src: img.src || conventionalImage(project.slug, key) || fallback.src || ''
  };
}

function imageTag(img, className = '', loading = 'lazy') {
  return `<img${className ? ` class="${className}"` : ''} src="${esc(img.src)}" alt="${esc(img.alt || '')}"${attr('width', img.width)}${attr('height', img.height)}${loading ? attr('loading', loading) : ''} decoding="async">`;
}

function assetUrl(src = '') {
  if (/^https?:\/\//i.test(src)) return src;
  return `${siteUrl}/${String(src).replace(/^\/+/, '')}`;
}

function cardImage(project) {
  const hero = image(project, 'hero');
  const card = project.card?.image || {};
  return {
    ...hero,
    ...card,
    src: card.src || conventionalImage(project.slug, 'card') || hero.src
  };
}

function pairs(items = [], className = '') {
  return items.map(([label, value]) => `<div${className ? ` class="${className}"` : ''}><span>${esc(label)}</span><strong>${esc(value)}</strong></div>`).join('\n');
}

function paragraphs(items = []) {
  return items.map((item) => `<p>${esc(item)}</p>`).join('\n');
}

function featureList(items = []) {
  return `<ul class="feature-list">\n${items.map((item) => `            <li>${esc(item)}</li>`).join('\n')}\n          </ul>`;
}

function quickFacts(project) {
  return project.quickFacts || [
    ['Starting price', project.hero?.startingPrice || 'On request'],
    ['Location', project.hero?.location || 'Costa del Sol'],
    ['Property type', project.hero?.type || 'New development residences'],
    ['Delivery', project.hero?.delivery || 'On request']
  ];
}

function actionLink(label, href = '#enquire', extra = '') {
  const prefill = href.startsWith('#enquire') ? ' data-prefill' : '';
  return `<a class="btn project-btn${extra ? ` ${extra}` : ''}" href="${esc(href)}"${prefill}>${esc(label)}</a>`;
}

function ghostAction(label, href = '#enquire') {
  return actionLink(label, href, 'ghost');
}

function mapLabelLines(html = 'Project<br>Area') {
  return String(html)
    .split(/<br\s*\/?>/i)
    .map((part) => part.replace(/<[^>]*>/g, '').trim())
    .filter(Boolean)
    .slice(0, 2);
}

function locationMap(project) {
  const [mapLineOne = project.name, mapLineTwo = project.hero?.location || 'Costa del Sol'] = mapLabelLines(project.location?.mapLabelHtml);
  const titleId = `${project.slug}-map-title`;
  const descId = `${project.slug}-map-desc`;
  return `<div class="location-map-card">
            <svg class="location-map-svg" viewBox="0 0 760 520" role="img" aria-labelledby="${esc(titleId)} ${esc(descId)}" focusable="false">
              <title id="${esc(titleId)}">${esc(project.name)} location map</title>
              <desc id="${esc(descId)}">Indicative map showing ${esc(project.name)} in ${esc(project.hero?.location || project.location?.mapLabelHtml || 'Costa del Sol')}, close to the coast, Marbella Centre, Puerto Banús, golf and Málaga Airport.</desc>
              <defs>
                <linearGradient id="mapSeaGradient" x1="0" x2="1" y1="0" y2="1">
                  <stop offset="0" stop-color="#dfe9e3"/>
                  <stop offset="1" stop-color="#cbd8d2"/>
                </linearGradient>
                <radialGradient id="mapProjectGlow" cx="50%" cy="50%" r="50%">
                  <stop offset="0" stop-color="#b89564" stop-opacity="0.34"/>
                  <stop offset="0.58" stop-color="#b89564" stop-opacity="0.12"/>
                  <stop offset="1" stop-color="#b89564" stop-opacity="0"/>
                </radialGradient>
                <filter id="mapSoftShadow" x="-30%" y="-30%" width="160%" height="160%">
                  <feDropShadow dx="0" dy="16" stdDeviation="18" flood-color="#2b271f" flood-opacity="0.14"/>
                </filter>
              </defs>
              <rect class="map-paper" x="1" y="1" width="758" height="518"/>
              <path class="map-hills" d="M0 118 C90 82 158 132 246 100 C336 66 430 104 520 72 C618 38 696 56 760 30 L760 0 L0 0 Z"/>
              <path class="map-sea" d="M0 358 C92 332 174 356 272 342 C376 326 464 346 570 324 C654 306 716 318 760 286 L760 520 L0 520 Z"/>
              <path class="map-coast" d="M0 358 C92 332 174 356 272 342 C376 326 464 346 570 324 C654 306 716 318 760 286"/>
              <path class="map-road map-road-secondary" d="M50 188 C150 164 238 178 350 154 C482 126 592 140 714 112"/>
              <path class="map-road map-road-main" d="M42 292 C142 270 256 292 376 270 C492 248 606 248 720 218"/>
              <path class="map-road map-local" d="M502 224 C488 252 478 286 468 322"/>
              <path class="map-route" d="M356 265 C398 250 448 242 500 226"/>
              <g class="map-node map-node-muted" transform="translate(198 282)">
                <circle r="5"/>
                <text x="-6" y="-17" text-anchor="end">Puerto Banús</text>
              </g>
              <g class="map-node" transform="translate(356 266)">
                <circle r="6"/>
                <text x="-12" y="-20" text-anchor="end">Marbella Centre</text>
              </g>
              <g class="map-node map-node-muted" transform="translate(646 164)">
                <circle r="5"/>
                <text x="16" y="4">Málaga Airport</text>
              </g>
              <g class="map-node map-node-muted" transform="translate(492 334)">
                <circle r="5"/>
                <text x="16" y="4">Beach access</text>
              </g>
              <g class="map-node map-node-muted" transform="translate(458 184)">
                <circle r="5"/>
                <text x="-14" y="4" text-anchor="end">Golf</text>
              </g>
              <g class="map-marker" transform="translate(502 224)" filter="url(#mapSoftShadow)">
                <circle class="map-marker-glow" r="58"/>
                <circle class="map-marker-disc" r="34"/>
                <circle class="map-marker-dot" r="5"/>
              </g>
              <text class="map-project-label" x="502" y="286" text-anchor="middle">
                <tspan x="502">${esc(mapLineOne)}</tspan>
                <tspan x="502" dy="18">${esc(mapLineTwo)}</tspan>
              </text>
              <text class="map-water-label" x="92" y="430">Mediterranean Sea</text>
              <text class="map-road-label" x="86" y="178">AP-7</text>
              <text class="map-road-label" x="84" y="286">A-7 Coast Road</text>
              <text class="map-note" x="40" y="52">Indicative location</text>
            </svg>
            <div class="map-legend" aria-hidden="true">
              <span><i class="legend-pin"></i> Project area</span>
              <span><i class="legend-road"></i> Coastal access</span>
              <span><i class="legend-sea"></i> Mediterranean</span>
            </div>
          </div>`;
}

function whatsappHref(project) {
  const rawNumber = project.contact?.whatsappNumber || '34600000000';
  const number = String(rawNumber).replace(/[^\d]/g, '');
  const message = project.contact?.whatsappMessage || `Hello Nueva Living, I would like to speak with an advisor about ${project.name}.`;
  return `https://wa.me/${number}?text=${encodeURIComponent(message)}`;
}

function advisorAction(project, label = 'Speak With Advisor') {
  return `<a class="btn project-btn ghost" href="${esc(whatsappHref(project))}" target="_blank" rel="noopener" data-whatsapp-advisor data-project="${esc(project.name)}" data-intent="speak with an advisor">${esc(label)}</a>`;
}

function normaliseCardList(items = []) {
  return Array.isArray(items) ? items.filter(Boolean).map(String) : [];
}

function discoveryAttr(name, items = []) {
  const value = normaliseCardList(items).join('|');
  return value ? attr(name, value) : '';
}

function priceNumber(value = '') {
  const numeric = String(value).replace(/[^\d]/g, '');
  return numeric ? Number(numeric) : '';
}

function completionRank(value = '') {
  const str = String(value);
  const quarter = str.match(/Q([1-4])\s*(20\d{2})/i);
  if (quarter) return `${quarter[2]}-${quarter[1]}`;
  const year = str.match(/20\d{2}/);
  return year ? `${year[0]}-4` : '';
}

function renderDiscoveryTags(tags = []) {
  return normaliseCardList(tags).slice(0, 5).map((tag) => `<span>${esc(tag)}</span>`).join('');
}

function renderDocumentRows(items = []) {
  return items.map(([title, body, action], index) => `<article class="document-row reveal-soft">
            <div class="document-index">${String(index + 1).padStart(2, '0')}</div>
            <div>
              <h3>${esc(title)}</h3>
              <p>${esc(body)}</p>
            </div>
            <a href="#enquire" data-prefill>${esc(action || 'Request')}</a>
          </article>`).join('\n          ');
}

function renderTimelineItems(items = []) {
  return items.map(([step, title, body]) => `<article class="timeline-item reveal-soft">
            <span>${esc(step)}</span>
            <h3>${esc(title)}</h3>
            <p>${esc(body)}</p>
          </article>`).join('\n          ');
}

function nav() {
  return `<nav class="site-nav">
    <a class="nav-logo" href="index.html" aria-label="Nueva Living home">
      <img src="assets/liora/brand/nueva-living-hero-logo-transparent.png?v=7" alt="Nueva Living" width="420" height="100">
    </a>
    <div class="nav-links">
      <a href="approach.html">Approach</a>
      <a href="developments.html">Developments</a>
      <a href="areas.html">Areas</a>
      <a href="advisory.html">Advisory</a>
      <a href="contact.html">Contact Us</a>
    </div>
    <button class="nav-burger" type="button" aria-label="Menu" aria-controls="mobileMenu" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
  </nav>

  <div class="mobile-menu" id="mobileMenu">
    <a href="approach.html">Approach</a>
    <a href="developments.html">Developments</a>
    <a href="areas.html">Areas</a>
    <a href="advisory.html">Advisory</a>
    <a href="contact.html">Contact Us</a>
  </div>`;
}

function footer(project) {
  return `<footer>
    <div class="footer-grid">
      <div>
        <img class="footer-logo" src="assets/liora/brand/nueva-living-lockup-espresso-transparent.png?v=7" alt="Nueva Living" width="700" height="340" loading="lazy" decoding="async">
        <p class="footer-about">A specialist advisory firm focused exclusively on new-build and off-plan property across the Costa del Sol. Serving international buyers with clarity and confidence.</p>
      </div>
      <div class="footer-col">
        <div class="footer-col-title">Company</div>
        <ul>
          <li><a href="approach.html">Our Approach</a></li>
          <li><a href="about.html">About</a></li>
          <li><a href="advisory.html">Advisory</a></li>
          <li><a href="contact.html">Request Access</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <div class="footer-col-title">Projects</div>
        <ul>
          <li><a href="developments.html">All Developments</a></li>
          <li><a href="${esc(project.output)}">${esc(project.shortName || project.name)}</a></li>
          <li><a href="areas.html">Areas Overview</a></li>
          <li><a href="areas.html#marbella">Marbella</a></li>
          <li><a href="areas.html#estepona">Estepona</a></li>
          <li><a href="areas.html#benahavis">Benahavís</a></li>
          <li><a href="areas.html#nueva-andalucia">Nueva Andalucía</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <div class="footer-col-title">Contact</div>
        <ul>
          <li><a href="mailto:contact@nueva-living.com">contact@nueva-living.com</a></li>
          <li><a href="areas.html#marbella">Marbella, Spain</a></li>
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
      <span>&copy; 2026 Nueva Living</span>
    </div>
  </footer>`;
}

function renderProject(project) {
  const heroImage = image(project, 'hero');
  const architectureImage = image(project, 'architecture');
  const privateImage = image(project, 'privateViewing');
  const privateHref = project.privateViewing?.href || 'index.html?private-viewing=1';
  const privateHeroCta = project.privateViewing?.heroCta || 'Book Private Viewing';
  const privateCta = project.privateViewing?.ctaLabel || 'Enter Private Viewing';
  const facts = [
    ['Location', project.hero.location],
    ['Starting Price', project.hero.startingPrice],
    ['Type', project.hero.type],
    ['Delivery', project.hero.delivery]
  ];
  const quickFactItems = quickFacts(project);
  const why = project.why || {
    headlineHtml: `Why ${esc(project.shortName || project.name)} <em>matters</em>`,
    copy: project.description,
    points: []
  };
  const projectFile = project.projectFile || {
    headlineHtml: 'Request the private <em>project file</em>',
    copy: 'Current project material is available by private request.',
    documents: [
      ['Project brochure', 'Project overview and lifestyle positioning', 'Request Brochure'],
      ['Floorplans', 'Current layouts by residence type', 'Request Floorplans'],
      ['Price availability sheet', 'Latest released units and guide pricing', 'Request Availability']
    ]
  };
  const trustDossier = project.trustDossier || {
    headlineHtml: 'Private project <em>dossier</em>',
    copy: 'Project clarity is reviewed privately before a viewing or reservation.',
    cards: []
  };
  const timeline = project.timeline || {
    headlineHtml: 'Indicative buyer <em>sequence</em>',
    items: []
  };
  const schemaUrl = project.canonical || `https://nueva-living.com/${project.output}`;
  const productSchema = {
    '@context': 'https://schema.org',
    '@type': 'Product',
    name: project.name,
    description: project.description,
    category: project.schema?.category || 'New development residences',
    brand: { '@type': 'Brand', name: 'Nueva Living' },
    offers: {
      '@type': 'Offer',
      priceCurrency: project.schema?.priceCurrency || 'EUR',
      price: project.schema?.price || '',
      availability: 'https://schema.org/InStock',
      url: schemaUrl
    },
    areaServed: { '@type': 'Place', name: project.schema?.areaServed || project.hero.location }
  };
  const agentSchema = {
    '@context': 'https://schema.org',
    '@type': 'RealEstateAgent',
    name: 'Nueva Living',
    url: `${siteUrl}/`,
    email: 'contact@nueva-living.com',
    areaServed: 'Costa del Sol'
  };

  return `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>${esc(project.name)} | Nueva Living</title>
  <meta name="description" content="${esc(project.seoDescription || project.description)}">
  <link rel="canonical" href="${esc(project.canonical || '')}">
  <meta property="og:title" content="${esc(project.name)} | Nueva Living">
  <meta property="og:description" content="${esc(project.description)}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="${esc(project.canonical || '')}">
  <meta property="og:image" content="${esc(assetUrl(heroImage.src))}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="${esc(project.name)} | Nueva Living">
  <meta name="twitter:description" content="${esc(project.twitterDescription || project.description)}">
  <meta name="twitter:image" content="${esc(assetUrl(heroImage.src))}">
  <link rel="icon" href="assets/liora/liora-favicon-512.png?v=6" type="image/png" sizes="512x512">
  <link rel="icon" href="assets/liora/favicon-32.png?v=6" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="assets/liora/apple-touch-icon.png?v=6" sizes="180x180">
${fontPreloadBlock}
  <link rel="stylesheet" href="assets/fonts/google/liora-fonts.css">
  <link rel="stylesheet" href="assets/liora/liora-pages.css">
  <link rel="stylesheet" href="assets/liora/liora-property.css">
  <script src="assets/liora/liora-property.js" defer></script>
  <script type="application/ld+json">
${JSON.stringify(productSchema, null, 2)}
  </script>
  <script type="application/ld+json">
${JSON.stringify(agentSchema, null, 2)}
  </script>
</head>
<body
  data-project-name="${esc(project.name)}"
  data-project-message="${esc(project.enquiry.message)}"
  data-project-sent-message="${esc(project.enquiry.sentMessage)}"
>
  ${nav()}

  <main>
    <section class="project-hero" id="top">
      ${imageTag(heroImage, 'project-hero-img', '')}
      <div class="project-hero-inner">
        <div class="hero-copy reveal-soft">
          <span class="project-eyebrow">${esc(project.hero.eyebrow)}</span>
          <h1 class="hero-title">${project.titleHtml}</h1>
          <p class="hero-positioning">${esc(project.description)}</p>
          <div class="hero-actions">
            ${actionLink('Request Availability')}
            ${ghostAction(privateHeroCta, privateHref)}
          </div>
        </div>
        <aside class="hero-facts reveal-soft" aria-label="Project key facts">
          ${facts.map(([label, value]) => `<div class="hero-fact"><span>${esc(label)}</span><strong>${esc(value)}</strong></div>`).join('\n          ')}
        </aside>
      </div>
    </section>

    <nav class="project-nav" aria-label="Project sections">
      <div class="project-nav-inner">
        <a href="#overview">Overview</a>
        <a href="#why-this-project">Why</a>
        <a href="#architecture">Architecture</a>
        <a href="#residences">Residences</a>
        <a href="#project-file">Project File</a>
        <a href="#private-viewing">Private Viewing</a>
        <a href="#lifestyle">Lifestyle</a>
        <a href="#location">Location</a>
        <a href="#investment">Investment</a>
        <a href="#project-dossier">Clarity</a>
        <a href="#availability">Availability</a>
        <a href="#enquire">Enquire</a>
      </div>
    </nav>

    <section class="quick-facts-band" aria-label="Project quick facts">
      <div class="project-inner quick-facts-shell reveal-soft">
        <div class="quick-facts-grid">
          ${quickFactItems.map(([label, value]) => `<div class="quick-fact"><span>${esc(label)}</span><strong>${esc(value)}</strong></div>`).join('\n          ')}
        </div>
        <div class="quick-facts-actions">
          ${actionLink('Request Availability')}
          ${ghostAction('Request Project Material')}
        </div>
      </div>
    </section>

    <section class="project-section" id="overview">
      <div class="project-inner overview-grid">
        <div class="reveal-soft">
          <span class="section-kicker">Overview</span>
          <div class="rule"></div>
          <h2 class="section-headline">${project.overview.headlineHtml}</h2>
          ${project.overview.copy.map((item) => `<p class="project-lead">${esc(item)}</p>`).join('\n          ')}
        </div>
        <div class="metrics-grid reveal-soft">
          ${pairs(project.overview.metrics, 'metric')}
        </div>
      </div>
    </section>

    <section class="project-section project-why" id="why-this-project">
      <div class="project-inner why-grid">
        <div class="reveal-soft">
          <span class="section-kicker">Why This Project</span>
          <div class="rule"></div>
          <h2 class="section-headline">${why.headlineHtml}</h2>
          <p class="project-lead">${esc(why.copy)}</p>
        </div>
        <div class="why-point-grid">
          ${(why.points || []).map(([title, body]) => `<article class="why-point reveal-soft"><h3>${esc(title)}</h3><p>${esc(body)}</p></article>`).join('\n          ')}
        </div>
      </div>
    </section>

    <section class="project-section dark" id="architecture">
      <div class="project-inner editorial-layout">
        <figure class="editorial-image reveal-soft">
          ${imageTag(architectureImage)}
          <figcaption class="image-caption">${esc(architectureImage.caption || 'Architecture preview')}</figcaption>
        </figure>
        <div class="editorial-copy reveal-soft">
          <span class="section-kicker">Architecture</span>
          <div class="rule"></div>
          <h2 class="section-headline">${project.architecture.headlineHtml}</h2>
          ${paragraphs(project.architecture.copy)}
          ${featureList(project.architecture.highlights)}
        </div>
      </div>
    </section>

    <section class="project-section" id="residences">
      <div class="project-inner">
        <div class="reveal-soft">
          <span class="section-kicker">Residences</span>
          <div class="rule"></div>
          <h2 class="section-headline">${project.residences.headlineHtml}</h2>
          <p class="project-lead">${esc(project.residences.copy)}</p>
        </div>
        <div class="residence-grid">
          ${project.residences.items.map((item) => `<article class="residence-card reveal-soft">
            <h3>${esc(item.name)}</h3>
            <div class="res-meta">
              ${pairs(item.meta)}
            </div>
            ${featureList(item.features)}
            <a class="btn ghost project-btn" href="#enquire" data-prefill>Request Floorplans</a>
          </article>`).join('\n          ')}
        </div>
        <div class="inline-cta-panel reveal-soft">
          <div>
            <span class="fine-label">Private Material</span>
            <p>Current layouts, view positions and unit availability should be reviewed against the latest developer file before shortlisting.</p>
          </div>
          <div class="inline-cta-actions">
            ${actionLink('Request Availability')}
            ${ghostAction('View Floorplans')}
          </div>
        </div>
      </div>
    </section>

    <section class="project-section project-file-section" id="project-file">
      <div class="project-inner">
        <div class="section-head reveal-soft">
          <span class="section-kicker">Project File</span>
          <div class="rule"></div>
          <h2 class="section-headline">${projectFile.headlineHtml}</h2>
          <p class="project-lead">${esc(projectFile.copy)}</p>
        </div>
        <div class="document-center">
          ${renderDocumentRows(projectFile.documents)}
        </div>
      </div>
    </section>

    <section class="project-section dark" id="private-viewing">
      <div class="project-inner">
        <div class="cinema-cta reveal-soft">
          ${imageTag(privateImage)}
          <div class="cinema-copy">
            <span class="section-kicker">Private Viewing</span>
            <div class="rule"></div>
            <h2 class="section-headline">${project.privateViewing.headlineHtml}</h2>
            <p>${esc(project.privateViewing.copy)}</p>
            <div class="viewing-insights">
              ${(project.privateViewing.insights || []).map(([title, body]) => `<div><span>${esc(title)}</span><p>${esc(body)}</p></div>`).join('\n              ')}
            </div>
            <div class="cinema-actions">
              ${actionLink(privateCta, privateHref)}
              ${ghostAction('Request Project Material')}
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="project-section dark" id="lifestyle">
      <div class="project-inner lifestyle-layout">
        <div class="editorial-copy reveal-soft">
          <span class="section-kicker">Lifestyle</span>
          <div class="rule"></div>
          <h2 class="section-headline">${project.lifestyle.headlineHtml}</h2>
          <p>${esc(project.lifestyle.copy)}</p>
        </div>
        <div class="lifestyle-panels reveal-soft">
          ${project.lifestyle.panels.map(([title, body]) => `<article class="lifestyle-panel"><h3>${esc(title)}</h3><p>${esc(body)}</p></article>`).join('\n          ')}
        </div>
      </div>
    </section>

    <section class="project-section" id="location">
      <div class="project-inner location-layout">
        <div class="reveal-soft">
          <span class="section-kicker">Location</span>
          <div class="rule"></div>
          <h2 class="section-headline">${project.location.headlineHtml}</h2>
          <p class="project-lead">${esc(project.location.copy)}</p>
          <div class="distance-grid" style="margin-top:32px;">
            ${pairs(project.location.distances, 'distance')}
          </div>
        </div>
        <div class="map-panel reveal-soft" aria-label="Indicative location map for ${esc(project.name)}">
          ${locationMap(project)}
        </div>
      </div>
    </section>

    <section class="project-section" id="investment">
      <div class="project-inner">
        <div class="reveal-soft">
          <span class="section-kicker">Investment Context</span>
          <div class="rule"></div>
          <h2 class="section-headline">${project.investment.headlineHtml}</h2>
          <p class="project-lead">${esc(project.investment.copy)}</p>
        </div>
        <div class="investment-grid">
          ${project.investment.cards.map(([title, body]) => `<article class="investment-card reveal-soft"><h3>${esc(title)}</h3><p>${esc(body)}</p></article>`).join('\n          ')}
        </div>
      </div>
    </section>

    <section class="project-section dossier-section" id="project-dossier">
      <div class="project-inner dossier-layout">
        <div class="reveal-soft">
          <span class="section-kicker">Project Clarity</span>
          <div class="rule"></div>
          <h2 class="section-headline">${trustDossier.headlineHtml}</h2>
          <p class="project-lead">${esc(trustDossier.copy)}</p>
        </div>
        <div class="dossier-grid">
          ${(trustDossier.cards || []).map(([title, body]) => `<article class="dossier-card reveal-soft"><h3>${esc(title)}</h3><p>${esc(body)}</p></article>`).join('\n          ')}
        </div>
      </div>
    </section>

    <section class="project-section timeline-section" id="timeline">
      <div class="project-inner">
        <div class="section-head center reveal-soft">
          <span class="section-kicker">Buyer Sequence</span>
          <div class="rule"></div>
          <h2 class="section-headline">${timeline.headlineHtml}</h2>
        </div>
        <div class="project-timeline">
          ${renderTimelineItems(timeline.items)}
        </div>
      </div>
    </section>

    <section class="project-section" id="availability">
      <div class="project-inner">
        <div class="availability-panel reveal-soft">
          <div>
            <span class="section-kicker">Availability</span>
            <div class="rule"></div>
            <h2 class="section-headline">${project.availability.headlineHtml}</h2>
            <p>${esc(project.availability.copy)}</p>
          </div>
          <div class="availability-actions">
            ${actionLink('Request Availability')}
            ${advisorAction(project)}
          </div>
        </div>
      </div>
    </section>

    <section class="project-section" id="enquire">
      <div class="project-inner">
        <div class="section-head center reveal-soft">
          <span class="label">Enquire</span>
          <div class="rule"></div>
          <h2 class="section-title">${project.enquiry.headlineHtml}</h2>
          <p class="body-copy">${esc(project.enquiry.copy)}</p>
        </div>
        <form class="enquiry-card reveal-soft" id="projectForm" name="project-material-request" method="POST" data-netlify="true" netlify-honeypot="bot-field" action="/thank-you.html">
          <input type="hidden" name="form-name" value="project-material-request">
          <p style="display:none"><label>Do not fill this out <input name="bot-field"></label></p>
          <input type="hidden" id="f-project" name="project" value="${esc(project.name)}">
          <input type="hidden" name="preferred_area" value="${esc(project.hero?.location || '')}">
          <input type="hidden" name="property_type_interest" value="${esc(project.hero?.type || '')}">
          <input type="hidden" name="budget_range" value="${esc(project.hero?.startingPrice || '')}">
          <div class="form-grid">
            <div class="field">
              <label for="f-name">Name</label>
              <input id="f-name" name="name" type="text" autocomplete="name" placeholder="Your name" required>
            </div>
            <div class="field">
              <label for="f-email">Email</label>
              <input id="f-email" name="email" type="email" autocomplete="email" placeholder="your@email.com" required>
            </div>
            <div class="field full">
              <label for="f-phone">Phone / WhatsApp</label>
              <input id="f-phone" name="phone" type="tel" autocomplete="tel" placeholder="+34 or international">
            </div>
            <div class="field full">
              <label for="f-msg">Message</label>
              <textarea id="f-msg" name="message">${esc(project.enquiry.message)}</textarea>
            </div>
            <label class="consent-row field full" for="f-consent">
              <input id="f-consent" name="consent" type="checkbox" required>
              <span>I consent to Nueva Living contacting me about this project request. Information is handled with discretion.</span>
            </label>
          </div>
          <div class="form-submit" style="margin-top:26px;">
            <button type="submit" class="btn project-btn">Submit Request</button>
            <span class="form-note">${esc(project.enquiry.note)}</span>
          </div>
        </form>
      </div>
    </section>
  </main>

  <div class="sticky-mobile-cta" aria-label="Project request actions">
    <a href="#enquire" data-prefill>Request Availability</a>
    <a href="${esc(whatsappHref(project))}" target="_blank" rel="noopener" data-whatsapp-advisor data-project="${esc(project.name)}" data-intent="speak with an advisor">Speak With Advisor</a>
  </div>

  ${footer(project)}
</body>
</html>
`;
}

function projectFiles() {
  if (!existsSync(projectsDir)) return [];
  return readdirSync(projectsDir, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => path.join(projectsDir, entry.name, 'project.json'))
    .filter((file) => existsSync(file));
}

function loadProjects() {
  return projectFiles()
    .map((file) => ({ ...readJson(file), sourceFile: file }))
    .sort((a, b) => {
      const orderA = a.card?.order ?? 999;
      const orderB = b.card?.order ?? 999;
      return orderA === orderB ? a.name.localeCompare(b.name) : orderA - orderB;
    });
}

function renderProjectCard(project) {
  const img = cardImage(project);
  const meta = project.card?.meta || [
    ['From', project.hero?.startingPrice?.replace(/^From\s+/i, '') || 'On request'],
    ['Type', project.hero?.type || 'Residences'],
    ['Delivery', project.hero?.delivery || 'On request']
  ];
  const discovery = project.discovery || {};
  const price = discovery.price || project.schema?.price || priceNumber(project.hero?.startingPrice);
  const completion = discovery.completionSort || completionRank(project.hero?.delivery);
  const lifestyleTags = normaliseCardList(discovery.lifestyleTags);
  const architectureTags = normaliseCardList(discovery.architectureTags);
  const locationTags = normaliseCardList(discovery.locationTags);
  const investmentTags = [
    ...normaliseCardList(discovery.investmentTags),
    ...normaliseCardList(discovery.buyerIntentTags)
  ];
  const practicalTags = normaliseCardList(discovery.practicalTags || [
    ...(discovery.propertyTypes || []),
    discovery.bedrooms,
    discovery.status,
    discovery.availability
  ]);
  const allTags = [
    ...lifestyleTags,
    ...architectureTags,
    ...locationTags,
    ...investmentTags,
    ...practicalTags
  ];
  const cardTags = discovery.cardTags || allTags.slice(0, 4);

  return `          <article class="project-card" id="${esc(project.slug)}" data-project-card${attr('data-title', project.name)}${attr('data-price', price)}${attr('data-completion', completion)}${attr('data-release', discovery.releaseDate)}${attr('data-priority', discovery.priority ?? project.card?.order ?? 999)}${attr('data-featured', discovery.featured ? 'true' : 'false')}${discoveryAttr('data-tags', allTags)}${discoveryAttr('data-lifestyle', lifestyleTags)}${discoveryAttr('data-architecture', architectureTags)}${discoveryAttr('data-location', locationTags)}${discoveryAttr('data-investment', investmentTags)}${discoveryAttr('data-practical', practicalTags)}>
            ${imageTag(img)}
            <div class="project-body">
              <span class="label">${esc(project.card?.label || project.hero?.location || 'Curated Project')}</span>
              <h3>${esc(project.name)}</h3>
              <p>${esc(project.card?.description || project.description)}</p>
              ${discovery.advisoryBadge ? `<div class="advisory-badge">${esc(discovery.advisoryBadge)}</div>` : ''}
              <div class="meta">${meta.map(([label, value]) => `<div><span>${esc(label)}</span><strong>${esc(value)}</strong></div>`).join('')}</div>
              ${cardTags.length ? `<div class="project-tags">${renderDiscoveryTags(cardTags)}</div>` : ''}
              <a class="project-link" href="${esc(project.output)}">Explore Project</a>
            </div>
          </article>`;
}

function updateDevelopmentsPage(projects) {
  if (!existsSync(developmentsPage)) return false;

  const html = readFileSync(developmentsPage, 'utf8');
  const gridOpen = '<div class="project-grid" data-project-grid>';
  const gridStart = html.indexOf(gridOpen);
  const start = html.indexOf(generatedProjectsStart);
  const end = html.indexOf(generatedProjectsEnd);

  if (gridStart === -1) {
    throw new Error('developments.html is missing the project grid container.');
  }

  if (start === -1 || end === -1 || end < start) {
    throw new Error('developments.html is missing NUEVA GENERATED PROJECTS markers.');
  }

  const gridContentStart = gridStart + gridOpen.length;
  const lineStart = html.lastIndexOf('\n', gridStart) + 1;
  const gridIndent = html.slice(lineStart, gridStart);
  const cardIndent = `${gridIndent}  `;
  const cards = projects.map(renderProjectCard).join('\n');
  const generatedBlock = `\n${cardIndent}${generatedProjectsStart}\n${cards}\n${cardIndent}${generatedProjectsEnd}`;
  const next = `${html.slice(0, gridContentStart)}${generatedBlock}${html.slice(end + generatedProjectsEnd.length)}`;
  writeFileSync(developmentsPage, next);
  return true;
}

const written = [];
const projects = loadProjects();
for (const project of projects) {
  if (!project.slug || !project.output) {
    throw new Error(`${path.relative(process.cwd(), project.sourceFile)} must include slug and output.`);
  }

  const html = renderProject(project);
  writeFileSync(path.resolve(project.output), html);
  written.push(project.output);
}

const developmentsUpdated = updateDevelopmentsPage(projects);

console.log(JSON.stringify({ written, developmentsUpdated }, null, 2));
