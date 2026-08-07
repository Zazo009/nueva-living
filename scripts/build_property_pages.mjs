import { existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import path from 'node:path';
import propertySync from '../lib/nueva-property-sync.cjs';

const {
  DEFAULT_PROPERTY_WEBHOOK_URL,
  cleanEnvironmentValue,
  projectToPropertyPayload,
  sendPropertyToCrm,
  validatePropertyPayload
} = propertySync;

const projectsDir = path.resolve('content/liora-projects');
const conventionalImageDir = 'assets/liora/projects';
const developmentsPage = path.resolve('developments.html');
const generatedProjectsStart = '<!-- NUEVA GENERATED PROJECTS START -->';
const generatedProjectsEnd = '<!-- NUEVA GENERATED PROJECTS END -->';
const generatedArchivedProjectsStart = '<!-- NUEVA GENERATED ARCHIVED PROJECTS START -->';
const generatedArchivedProjectsEnd = '<!-- NUEVA GENERATED ARCHIVED PROJECTS END -->';
const homepagePage = path.resolve('nueva-living-home.html');
const generatedHomeCardsStart = '<!-- NUEVA GENERATED HOME PROJECTS START -->';
const generatedHomeCardsEnd = '<!-- NUEVA GENERATED HOME PROJECTS END -->';
const siteUrl = 'https://nuevaliving.com';
const fontPreloadBlock = `  <link rel="preload" href="assets/fonts/google/8vIJ7ww63mVu7gt79mT7PkRXMw.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="assets/fonts/google/JTUSjIg1_i6t8kCHKm459WlhyyTh89Y.woff2" as="font" type="font/woff2" crossorigin>`;
const propertyCssVersion = fileVersion('assets/liora/liora-property.css');
const propertyJsVersion = fileVersion('assets/liora/liora-property.js');

// General buyer-process questions that apply to every development. A
// project's own `faq` array (if set) is appended after these, for
// anything specific to that particular release.
const DEFAULT_FAQS = [
  ['Can foreigners buy property in Spain?', 'Yes. There are no restrictions on non-Spanish nationals buying property in Spain, whether as a resident or non-resident.'],
  ['What is an NIE number and do I need one?', 'An NIE (Numero de Identificacion de Extranjero) is a tax ID number required for any property purchase in Spain by a non-Spanish national. Nueva Living can guide you through obtaining one before you reserve.'],
  ['What costs should I budget for on top of the purchase price?', 'Buyers typically budget for transfer tax or VAT, notary fees, land registry fees and legal fees on top of the purchase price. Nueva Living provides a full, current cost breakdown for your chosen residence before you reserve.'],
  ['Can I get a mortgage in Spain as a non-resident?', 'Many Spanish banks offer mortgages to non-resident buyers, typically financing a portion of the purchase price. Exact terms depend on the bank and your personal financial profile.'],
  ['What is the difference between off-plan and completed properties?', 'Off-plan means the development is still under construction and is usually sold with staged payments through to completion. A completed property is ready to view and move into now.'],
  ['How does the reservation and payment process work?', 'Reservation and payment structures vary by development and are set out in full before you reserve. Nueva Living reconfirms the current schedule for your chosen residence at every step.'],
  ['Can I rent out the property after purchase?', 'This depends on the individual development and local regulations, which can vary by community and municipality. Nueva Living will confirm the specific rules for a development before you reserve.'],
  ['Do I need a lawyer?', 'Yes, we strongly recommend independent legal representation for any property purchase in Spain. Nueva Living can put you in touch with independent lawyers experienced in Costa del Sol property.']
];

function fileVersion(file) {
  return createHash('sha256').update(readFileSync(path.resolve(file))).digest('hex').slice(0, 12);
}

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
  const style = img.focus ? ` style="object-position: ${esc(img.focus)};"` : '';
  return `<img${className ? ` class="${className}"` : ''} src="${esc(img.src)}" alt="${esc(img.alt || '')}"${attr('width', img.width)}${attr('height', img.height)}${loading ? attr('loading', loading) : ''} decoding="async"${style}>`;
}

function responsiveCardImageTag(img) {
  const match = String(img.src || '').match(/^(.*)\.(?:jpe?g)$/i);
  if (!match || !match[1].includes('/cards/')) return imageTag(img);
  const base = match[1];
  const sizes = '(max-width: 760px) calc(100vw - 50px), (max-width: 1100px) 50vw, 33vw';
  return `<picture class="project-card-picture">
              <source type="image/avif" srcset="${esc(base)}-640.avif 640w, ${esc(base)}-900.avif 900w" sizes="${sizes}">
              <source type="image/webp" srcset="${esc(base)}-640.webp 640w, ${esc(base)}-900.webp 900w" sizes="${sizes}">
              ${imageTag(img)}
            </picture>`;
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

function renderProjectMedia(project) {
  const media = project.media;
  if (!media?.items?.length) return { section: '', dialog: '' };

  const video = media.video;
  const videoBlock = video?.desktopSrc ? `<figure class="project-media-film reveal-soft" data-project-video-shell>
          <div class="project-media-film-frame">
            <video
              playsinline
              preload="none"
              poster="${esc(video.poster || '')}"
              data-project-video
              data-video-desktop="${esc(video.desktopSrc)}"
              data-video-mobile="${esc(video.mobileSrc || video.desktopSrc)}"
              data-poster-desktop="${esc(video.poster || '')}"
              data-poster-mobile="${esc(video.mobilePoster || video.poster || '')}"
              aria-label="${esc(video.alt || `${project.name} film`)}"
            ></video>
            <button type="button" class="project-media-film-play" data-project-video-play aria-label="Play ${esc(video.title || `${project.name} film`)}">
              <span class="project-media-film-play-icon" aria-hidden="true"></span>
              <span>Play film</span>
            </button>
          </div>
          <figcaption>
            <span>Film</span>
            <strong>${esc(video.title || '')}</strong>
            <p>${esc(video.caption || '')}</p>
          </figcaption>
        </figure>` : '';

  const categories = [...new Set(media.items.map((item) => item.category).filter(Boolean))];
  const cards = categories.map((category) => {
    const categoryItems = media.items.filter((item) => item.category === category);
    const item = categoryItems[0];
    const count = categoryItems.length;
    const imageLabel = `${count} ${count === 1 ? 'image' : 'images'}`;
    return `<button type="button" class="project-media-card project-media-card--category" data-media-category="${esc(category)}" aria-label="View ${imageLabel} in ${esc(category)}">
              ${imageTag(item, '', 'lazy')}
              <span class="project-media-caption">
                <small>${esc(category)}</small>
                <strong>${esc(item.caption || '')}</strong>
                <span class="project-media-card-cta">View ${imageLabel} <span aria-hidden="true">&#8594;</span></span>
              </span>
            </button>`;
  }).join('\n            ');

  const mediaData = JSON.stringify(media.items.map((item) => ({
    src: item.src,
    alt: item.alt || '',
    width: item.width || 1600,
    height: item.height || 900,
    caption: item.caption || '',
    category: item.category || 'Media'
  }))).replace(/</g, '\\u003c');

  const facts = (media.facts || []).map(([value, label]) => `<div class="media-fact"><strong>${esc(value)}</strong><span>${esc(label)}</span></div>`).join('\n          ');

  return {
    section: `<section class="project-section project-media-section" id="media">
      <div class="project-inner">
        <div class="project-media-intro reveal-soft">
          <div>
            <span class="section-kicker">Media</span>
            <div class="rule"></div>
            <h2 class="section-headline">${media.headlineHtml}</h2>
          </div>
          <p class="project-lead">${esc(media.copy)}</p>
        </div>
        ${facts ? `<div class="media-facts reveal-soft">${facts}</div>` : ''}
        ${videoBlock}
        <div class="project-media-grid project-media-grid--categories" data-media-grid>
          ${cards}
        </div>
        <div class="media-gallery-footer">
          <button type="button" class="btn project-btn ghost media-show-all" data-media-show-all>View all ${media.items.length} images</button>
          <p class="media-note">${esc(media.note || '')}</p>
        </div>
      </div>
    </section>`,
    dialog: `<dialog class="project-media-dialog" id="projectMediaDialog" aria-label="${esc(project.name)} media viewer">
      <div class="project-media-dialog-shell" data-media-dialog-shell>
        <button type="button" class="media-dialog-close" data-media-close aria-label="Close media viewer">Close</button>
        <button type="button" class="media-dialog-nav media-dialog-prev" data-media-prev aria-label="Previous image">&#8592;</button>
        <figure class="media-dialog-figure">
          <img src="" alt="" width="1600" height="900" decoding="async" data-media-dialog-image>
          <figcaption><span data-media-dialog-count></span><strong data-media-dialog-caption></strong></figcaption>
        </figure>
        <button type="button" class="media-dialog-nav media-dialog-next" data-media-next aria-label="Next image">&#8594;</button>
        <div class="media-dialog-stack" data-media-dialog-stack hidden>
          <div class="media-dialog-stack-count" data-media-dialog-stack-count></div>
        </div>
      </div>
    </dialog>
    <script type="application/json" id="projectMediaData">${mediaData}</script>`
  };
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

function renderAvailabilityRelease(project) {
  const availability = project.availability || {};
  const units = availability.units || [];
  if (!units.length) return '';

  const hasFloorplans = units.some((unit) => unit.floorplan);
  const hasSize = units.some((unit) => unit.size);
  const hasFloor = units.some((unit) => unit.floor);

  const rows = units.map((unit) => `<tr>
                <td data-label="Reference"><strong>${esc(unit.reference)}</strong></td>${hasFloor ? `
                <td data-label="Floor">${esc(unit.floor)}</td>` : ''}
                <td data-label="Bedrooms">${esc(unit.bedrooms)}</td>${hasSize ? `
                <td data-label="Size">${esc(unit.size)}</td>` : ''}
                <td data-label="Price"><strong>${esc(unit.price)}</strong></td>
                <td data-label="Status"><span class="availability-status">Available</span></td>${hasFloorplans ? `
                <td data-label="Floorplan">${unit.floorplan ? `<a class="availability-floorplan-link" href="${esc(unit.floorplan)}" target="_blank" rel="noopener">View PDF</a>` : ''}</td>` : ''}
              </tr>`).join('\n              ');

  return `<div class="availability-release reveal-soft">
          <div class="availability-release-stats" aria-label="Current release summary">
            <div><span>Available homes</span><strong>${units.length}</strong></div>
            <div><span>Starting price</span><strong>${esc(availability.startingPrice || project.hero?.startingPrice || '')}</strong></div>
            <div><span>Price range</span><strong>${esc(availability.priceRange || '')}</strong></div>
            <div><span>Checked</span><strong>${esc(availability.checkedDate || '')}</strong></div>
          </div>
          <details class="availability-disclosure">
            <summary>
              <span>View all ${units.length} available homes</span>
              <span class="availability-summary-icon" aria-hidden="true">+</span>
            </summary>
            <div class="availability-table-wrap">
              <table class="availability-table">
                <caption class="sr-only">Available homes at ${esc(project.name)}</caption>
                <thead><tr><th scope="col">Reference</th>${hasFloor ? '<th scope="col">Floor</th>' : ''}<th scope="col">Bedrooms</th>${hasSize ? '<th scope="col">Size</th>' : ''}<th scope="col">Price</th><th scope="col">Status</th>${hasFloorplans ? '<th scope="col">Floorplan</th>' : ''}</tr></thead>
                <tbody>
              ${rows}
                </tbody>
              </table>
            </div>
          </details>
          <p class="availability-source-note">${esc(availability.sourceNote || '')}</p>
        </div>`;
}

function mapLabelLines(html = 'Project<br>Area') {
  return String(html)
    .split(/<br\s*\/?>/i)
    .map((part) => part.replace(/<[^>]*>/g, '').trim())
    .filter(Boolean)
    .slice(0, 2);
}

// Indicative Costa del Sol positions, west to east, tuned against the
// coast/road paths below (which already span the full canvas). Not
// geodetically precise -- this is a stylised orientation map, not a
// survey -- but the relative order and spacing is real, so a project's
// marker actually lands on the correct side of its neighbours instead of
// every project sharing one hardcoded position (see history of this file
// for the Cancelada Park bug this replaces).
const MAP_LANDMARKS = {
  estepona: { x: 150, y: 295, label: 'Estepona' },
  newGoldenMile: { x: 310, y: 278, label: 'New Golden Mile' },
  sanPedro: { x: 420, y: 268, label: 'San Pedro' },
  benahavis: { x: 460, y: 145, label: 'Benahávis' },
  puertoBanus: { x: 560, y: 255, label: 'Puerto Banús' },
  nuevaAndalucia: { x: 600, y: 165, label: 'Nueva Andalucía' },
  goldenMile: { x: 680, y: 233, label: 'Golden Mile' },
  marbellaCentre: { x: 800, y: 218, label: 'Marbella Centre' },
  marbellaEast: { x: 950, y: 195, label: 'Marbella East' },
  malagaAirport: { x: 1080, y: 165, label: 'Málaga Airport' }
};

// Context landmarks shown on every map for orientation, unless the
// project's own marker sits on (or very close to) one of them.
const MAP_CONTEXT_ORDER = ['estepona', 'puertoBanus', 'marbellaCentre', 'malagaAirport'];

function resolveMapArea(project) {
  const key = project.location?.mapArea;
  if (key && MAP_LANDMARKS[key]) return key;
  return 'marbellaCentre';
}

function locationMap(project) {
  const [mapLineOne = project.name, mapLineTwo = project.hero?.location || 'Costa del Sol'] = mapLabelLines(project.location?.mapLabelHtml);
  const titleId = `${project.slug}-map-title`;
  const descId = `${project.slug}-map-desc`;

  const areaKey = resolveMapArea(project);
  const marker = MAP_LANDMARKS[areaKey];
  const context = MAP_CONTEXT_ORDER.filter((key) => key !== areaKey).slice(0, 3);
  const contextNodes = context.map((key, index) => {
    const point = MAP_LANDMARKS[key];
    const muted = index !== 0;
    const anchorEnd = point.x > marker.x;
    return `<g class="map-node${muted ? ' map-node-muted' : ''}" transform="translate(${point.x} ${point.y})">
                <circle r="${muted ? 5 : 6}"/>
                <text x="${anchorEnd ? -12 : 16}" y="${muted ? 4 : -18}"${anchorEnd ? ' text-anchor="end"' : ''}>${esc(point.label)}</text>
              </g>`;
  }).join('\n              ');

  return `<div class="location-map-card">
            <svg class="location-map-svg" viewBox="0 0 1200 620" role="img" aria-labelledby="${esc(titleId)} ${esc(descId)}" focusable="false">
              <title id="${esc(titleId)}">${esc(project.name)} location map</title>
              <desc id="${esc(descId)}">Indicative map showing ${esc(project.name)} in ${esc(project.hero?.location || project.location?.mapLabelHtml || 'Costa del Sol')}, relative to ${context.map((key) => esc(MAP_LANDMARKS[key].label)).join(', ')}.</desc>
              <defs>
                <linearGradient id="mapSeaGradient" x1="0" x2="1" y1="0" y2="1">
                  <stop offset="0" stop-color="#BFDCE0"/>
                  <stop offset="1" stop-color="#5C8E98"/>
                </linearGradient>
                <radialGradient id="mapProjectGlow" cx="50%" cy="50%" r="50%">
                  <stop offset="0" stop-color="#A8834A" stop-opacity="0.34"/>
                  <stop offset="0.58" stop-color="#A8834A" stop-opacity="0.12"/>
                  <stop offset="1" stop-color="#A8834A" stop-opacity="0"/>
                </radialGradient>
                <filter id="mapSoftShadow" x="-30%" y="-30%" width="160%" height="160%">
                  <feDropShadow dx="0" dy="16" stdDeviation="18" flood-color="#2F2417" flood-opacity="0.14"/>
                </filter>
              </defs>
              <rect class="map-paper" width="1200" height="620"/>
              <path class="map-hills" d="M0 400 C180 372 330 394 470 366 C650 332 810 348 1010 296 C1090 276 1150 256 1200 232 L1200 0 L0 0 Z"/>
              <path class="map-sea" d="M0 400 C180 372 330 394 470 366 C650 332 810 348 1010 296 C1090 276 1150 256 1200 232 L1200 620 L0 620 Z"/>
              <path class="map-coast" d="M0 400 C180 372 330 394 470 366 C650 332 810 348 1010 296 C1090 276 1150 256 1200 232"/>
              <path class="map-road map-road-secondary" d="M100 210 C270 176 425 182 585 156 C775 126 940 114 1115 74"/>
              <text x="140" y="188" class="map-road-label">AP-7</text>
              <path class="map-road map-road-main" d="M95 300 C245 272 390 282 535 258 C695 232 845 214 1098 168"/>
              <text x="850" y="248" class="map-road-label">A-7 Coast Road</text>
              ${contextNodes}
              <g class="map-marker" transform="translate(${marker.x} ${marker.y})" filter="url(#mapSoftShadow)">
                <circle class="map-marker-glow" r="58"/>
                <circle class="map-marker-disc" r="34"/>
                <circle class="map-marker-dot" r="5"/>
              </g>
              <text class="map-project-label" x="${marker.x}" y="${marker.y + 62}" text-anchor="middle">
                <tspan x="${marker.x}">${esc(mapLineOne)}</tspan>
                <tspan x="${marker.x}" dy="18">${esc(mapLineTwo)}</tspan>
              </text>
              <text class="map-water-label" x="150" y="502">Mediterranean Sea</text>
              <text class="map-note" x="60" y="52">Indicative location</text>
            </svg>
            <div class="map-legend" aria-hidden="true">
              <span><i class="legend-pin"></i> Project area</span>
              <span><i class="legend-road"></i> Coastal access</span>
              <span><i class="legend-sea"></i> Mediterranean</span>
            </div>
          </div>`;
}

function whatsappHref(project) {
  const rawNumber = project.contact?.whatsappNumber || '46707576709';
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

function renderDocumentRows(items = [], hasPublishedAvailability = false, hasFloorplans = false) {
  return items.map(([title, body, action], index) => `<article class="document-row reveal-soft">
            <div class="document-index">${String(index + 1).padStart(2, '0')}</div>
            <div>
              <h3>${esc(title)}</h3>
              <p>${esc(body)}</p>
            </div>
            ${hasPublishedAvailability && /availability/i.test(action || '')
              ? '<a href="#availability">Open Current Release</a>'
              : hasFloorplans && /floorplan/i.test(action || '')
              ? '<a href="#availability">View Floorplans</a>'
              : `<a href="#enquire" data-prefill>${esc(action || 'Request')}</a>`}
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
    <div class="nav-links nav-links-left">
      <a href="approach.html">Approach</a>
      <a href="why-nueva.html">Why Nueva</a>
      <a href="developments.html">Developments</a>
    </div>
    <a class="nav-logo" href="index.html" aria-label="Nueva Living home">
      <img src="assets/liora/brand/nueva-living-hero-logo-transparent.png?v=7" alt="Nueva Living" width="420" height="100">
    </a>
    <div class="nav-links nav-links-right">
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
    <a href="why-nueva.html">Why Nueva</a>
    <a href="developments.html">Developments</a>
    <a href="areas.html">Areas</a>
    <a href="advisory.html">Advisory</a>
    <a href="contact.html">Contact Us</a>
  </div>`;
}

function projectArea(project) {
  const location = `${project.hero?.location || ''} ${project.schema?.areaServed || ''}`.toLowerCase();
  if (location.includes('nueva andaluc') || location.includes('nueva andalucía')) {
    return { label: 'Nueva Andalucía', href: 'area-nueva-andalucia.html' };
  }
  if (location.includes('benahav')) {
    return { label: 'Benahavís', href: 'area-benahavis.html' };
  }
  if (location.includes('estepona') || location.includes('new golden mile')) {
    return { label: 'Estepona', href: 'area-estepona.html' };
  }
  if (location.includes('mijas') || location.includes('fuengirola')) {
    return { label: 'Mijas & Fuengirola', href: 'area-mijas-fuengirola.html' };
  }
  if (location.includes('marbella east')) {
    return { label: 'Marbella East', href: 'area-marbella.html' };
  }
  return { label: 'Marbella', href: 'area-marbella.html' };
}

function breadcrumb(project) {
  const area = projectArea(project);
  return `<nav class="breadcrumb-bar" aria-label="Breadcrumb">
    <ol class="breadcrumb-list">
      <li><a href="developments.html">Developments</a></li>
      <li><a href="${area.href}">${area.label}</a></li>
      <li><span aria-current="page">${esc(project.shortName || project.name)}</span></li>
    </ol>
  </nav>`;
}

function breadcrumbSchema(project) {
  const area = projectArea(project);
  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      { '@type': 'ListItem', position: 1, name: 'Developments', item: `${siteUrl}/developments.html` },
      { '@type': 'ListItem', position: 2, name: area.label, item: `${siteUrl}/${area.href}` },
      { '@type': 'ListItem', position: 3, name: project.shortName || project.name, item: `${siteUrl}/${project.output}` }
    ]
  };
}

// Search-facing title/meta lead with property type and area, since those
// are what buyers actually search for -- not the project's own name.
function seoTitle(project) {
  const area = projectArea(project);
  const type = project.hero?.type || 'New Development';
  return `${type} in ${area.label} — ${project.shortName || project.name} | Nueva Living`;
}

function footer(project) {
  return `<footer>
    <div class="footer-grid">
      <div>
        <img class="footer-logo" src="assets/liora/brand/nueva-living-lockup-espresso-transparent.png?v=7" alt="Nueva Living" width="700" height="340" loading="lazy" decoding="async">
        <p class="footer-about">We help international buyers find and compare new-build and off-plan homes across the Costa del Sol.</p>
      </div>
      <div class="footer-col">
        <div class="footer-col-title">Company</div>
        <ul>
          <li><a href="approach.html">Our Approach</a></li>
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
          <li><a href="${esc(project.output)}">${esc(project.shortName || project.name)}</a></li>
          <li><a href="areas.html">Areas Overview</a></li>
          <li><a href="area-marbella.html">Marbella</a></li>
          <li><a href="area-estepona.html">Estepona</a></li>
          <li><a href="area-benahavis.html">Benahavís</a></li>
          <li><a href="area-nueva-andalucia.html">Nueva Andalucía</a></li>
          <li><a href="area-mijas-fuengirola.html">Mijas &amp; Fuengirola</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <div class="footer-col-title">Contact</div>
        <ul>
          <li><a href="mailto:contact@nuevaliving.com">contact@nuevaliving.com</a></li>
          <li><a href="area-marbella.html">Marbella, Spain</a></li>
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

const TIMELINE_ICONS = {
  leaf: '<svg class="timeline-leaf" viewBox="0 0 28 28" aria-hidden="true"><path d="M6 22C7 13 13 7 22 6c-1 9-7 15-16 16Z"/><path d="M7.5 20.5 20 8" /></svg>',
  start: '<svg class="timeline-icon" viewBox="0 0 28 28" aria-hidden="true"><path d="M9 4v20" stroke-linecap="round"/><path d="M9 5 21 9.5 9 14Z" stroke-linejoin="round"/></svg>',
  construction: '<svg class="timeline-icon" viewBox="0 0 28 28" aria-hidden="true"><path d="M8 24V6" stroke-linecap="round"/><path d="M8 6 22 8" stroke-linecap="round"/><path d="M20 8v6" stroke-linecap="round"/><path d="M4 24h10" stroke-linecap="round"/></svg>',
  finish: '<svg class="timeline-icon" viewBox="0 0 28 28" aria-hidden="true"><circle cx="9" cy="14" r="4.5"/><path d="M13 14h11" stroke-linecap="round"/><path d="M19 14v4" stroke-linecap="round"/><path d="M24 14v3" stroke-linecap="round"/></svg>'
};

function renderConstructionTimeline(project) {
  const timeline = project.constructionTimeline;
  if (!timeline || !Array.isArray(timeline.points) || !timeline.points.length) return '';

  const points = timeline.points.map((point, index) => `
        <div class="timeline-point${point.milestone ? ' is-milestone' : ''}" style="transition-delay:${(index * 0.09).toFixed(2)}s">
          <span class="timeline-label">${point.milestone && point.label ? esc(point.label) : ''}</span>
          <span class="timeline-marker">${point.milestone ? `<span class="timeline-marker-ring"></span><span class="timeline-marker-core">${TIMELINE_ICONS[point.icon] || TIMELINE_ICONS.leaf}</span>` : ''}</span>
          <span class="timeline-year">${esc(point.year || '')}</span>
        </div>`).join('');

  const paymentTerms = Array.isArray(timeline.paymentTerms) ? timeline.paymentTerms : [];

  return `    <section class="project-section construction-timeline-section" id="construction-timeline">
      <div class="project-inner timeline-head reveal-soft">
        <div>
          <span class="section-kicker">${esc(timeline.kicker || 'Timeline')}</span>
          <div class="rule"></div>
          <h2 class="section-headline">${timeline.headlineHtml || `${esc(timeline.kicker || 'Timeline')} of <em>delivery</em>`}</h2>
        </div>
        ${timeline.copy ? `<p class="project-lead timeline-intro">${esc(timeline.copy)}</p>` : ''}
      </div>
      <div class="project-inner timeline-track reveal-soft">${points}
      </div>
${paymentTerms.length ? `      <div class="project-inner timeline-payment-terms reveal-soft">
        <span class="timeline-payment-kicker">${esc(timeline.paymentTermsLabel || 'Payment Terms')}</span>
        <div class="timeline-payment-grid">
          ${paymentTerms.map(([label, value], index) => `<div class="timeline-payment-item">
            <span class="timeline-payment-index">${String(index + 1).padStart(2, '0')}</span>
            <span class="timeline-payment-label">${esc(label)}</span>
            <strong class="timeline-payment-value">${esc(value)}</strong>
          </div>`).join('\n          ')}
        </div>
      </div>
` : ''}    </section>

`;
}

function renderProject(project) {
  const heroImage = image(project, 'hero');
  const architectureImage = image(project, 'architecture');
  const privateImage = image(project, 'privateViewing');
  const privateHref = project.privateViewing?.href || 'index.html?private-viewing=1';
  const privateHeroCta = project.privateViewing?.heroCta || 'Cinematic Presentation';
  const privateCta = project.privateViewing?.ctaLabel || 'Cinematic Presentation';
  const projectMedia = renderProjectMedia(project);
  const constructionTimeline = renderConstructionTimeline(project);
  const availabilityRelease = renderAvailabilityRelease(project);
  const hasPublishedAvailability = Boolean(project.availability?.units?.length);
  const hasFloorplans = Boolean(project.availability?.units?.some((unit) => unit.floorplan));
  const availabilityBrowseAction = hasPublishedAvailability
    ? actionLink('View Available Homes', '#availability')
    : actionLink('Request Availability');
  const availabilityEnquiryAction = actionLink(
    hasPublishedAvailability ? 'Ask About a Residence' : 'Request Availability'
  );
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
    copy: 'Ask us for the latest project information and availability.',
    documents: [
      ['Project brochure', 'Project overview and lifestyle positioning', 'Request Brochure'],
      ['Floorplans', 'Current layouts by residence type', 'Request Floorplans'],
      ['Price availability sheet', 'Latest released units and guide pricing', 'Request Availability']
    ]
  };
  const trustDossier = project.trustDossier || {
    headlineHtml: 'What to know <em>before you view</em>',
    copy: 'We check the important project details before a viewing or reservation.',
    cards: []
  };
  const timeline = project.timeline || {
    headlineHtml: 'What happens <em>next</em>',
    items: []
  };
  const schemaUrl = project.canonical || `https://nuevaliving.com/${project.output}`;
  const schemaPrice = project.schema?.price;
  const calculatorSeedPrice = project.crm?.priceMin ?? project.discovery?.price ?? schemaPrice ?? 500000;
  const productSchema = {
    '@context': 'https://schema.org',
    '@type': 'Product',
    name: project.name,
    description: project.description,
    image: assetUrl(heroImage.src),
    category: project.schema?.category || 'New development residences',
    brand: { '@type': 'Brand', name: 'Nueva Living' },
    ...(schemaPrice ? {
      offers: {
        '@type': 'Offer',
        priceCurrency: project.schema?.priceCurrency || 'EUR',
        price: schemaPrice,
        availability: 'https://schema.org/InStock',
        url: schemaUrl
      }
    } : {}),
    areaServed: { '@type': 'Place', name: project.schema?.areaServed || project.hero.location }
  };
  const agentSchema = {
    '@context': 'https://schema.org',
    '@type': 'RealEstateAgent',
    name: 'Nueva Living',
    legalName: 'LIORA LIVING SL.',
    taxID: 'B88827472',
    url: `${siteUrl}/`,
    email: 'contact@nuevaliving.com',
    areaServed: 'Costa del Sol'
  };
  const faqs = [...DEFAULT_FAQS, ...(project.faq || [])];
  const faqSchema = {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: faqs.map(([question, answer]) => ({
      '@type': 'Question',
      name: question,
      acceptedAnswer: { '@type': 'Answer', text: answer }
    }))
  };
  const pageTitle = seoTitle(project);

  return `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>${esc(pageTitle)}</title>
  <meta name="description" content="${esc(project.seoDescription || project.description)}">
  <link rel="canonical" href="${esc(project.canonical || '')}">
  <meta property="og:title" content="${esc(pageTitle)}">
  <meta property="og:description" content="${esc(project.description)}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="${esc(project.canonical || '')}">
  <meta property="og:image" content="${esc(assetUrl(heroImage.src))}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="${esc(pageTitle)}">
  <meta name="twitter:description" content="${esc(project.twitterDescription || project.description)}">
  <meta name="twitter:image" content="${esc(assetUrl(heroImage.src))}">
  <link rel="icon" href="assets/liora/liora-favicon-512.png?v=6" type="image/png" sizes="512x512">
  <link rel="icon" href="assets/liora/favicon-32.png?v=6" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="assets/liora/apple-touch-icon.png?v=6" sizes="180x180">
${fontPreloadBlock}
  <link rel="stylesheet" href="assets/fonts/google/liora-fonts.css">
  <link rel="stylesheet" href="assets/liora/liora-pages.css?v=9">
  <link rel="stylesheet" href="assets/liora/liora-property.css?v=${propertyCssVersion}">
  <script src="assets/liora/liora-property.js?v=${propertyJsVersion}" defer></script>
  <script type="application/ld+json">
${JSON.stringify(productSchema, null, 2)}
  </script>
  <script type="application/ld+json">
${JSON.stringify(agentSchema, null, 2)}
  </script>
  <script type="application/ld+json">
${JSON.stringify(faqSchema, null, 2)}
  </script>
  <script type="application/ld+json">
${JSON.stringify(breadcrumbSchema(project), null, 2)}
  </script>
</head>
<body
  data-project-name="${esc(project.name)}"
  data-project-message="${esc(project.enquiry.message)}"
  data-project-sent-message="${esc(project.enquiry.sentMessage)}"
>
  ${nav()}
  ${breadcrumb(project)}

  <main>
    <section class="project-hero" id="top">
      ${imageTag(heroImage, 'project-hero-img', '')}
      <div class="project-hero-inner">
        <div class="hero-copy reveal-soft">
          <span class="project-eyebrow">${esc(project.hero.eyebrow)}</span>
          <h1 class="hero-title">${project.titleHtml}</h1>
          <p class="hero-positioning">${esc(project.description)}</p>
          <div class="hero-actions">
            ${availabilityBrowseAction}
            ${ghostAction(privateHeroCta, privateHref)}
            ${project.media?.items?.length ? ghostAction('All Photos', '#media') : ''}
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
${project.media?.items?.length ? '        <a href="#media">Media</a>\n' : ''}        <a href="#residences">Residences</a>
        <a href="#availability">Availability</a>
        <a href="#calculator">Affordability</a>
        <a href="#location">Location</a>
        <a href="#why-this-project">Why</a>
        <a href="#architecture">Architecture</a>
        <a href="#project-file">Project Info</a>
        <a href="#private-viewing">Cinematic Presentation</a>
        <a href="#lifestyle">Lifestyle</a>
        <a href="#faq">FAQ</a>
        <a href="#enquire">Enquire</a>
      </div>
    </nav>

    <section class="quick-facts-band" aria-label="Project quick facts">
      <div class="project-inner quick-facts-shell reveal-soft">
        <div class="quick-facts-grid">
          ${quickFactItems.map(([label, value]) => `<div class="quick-fact"><span>${esc(label)}</span><strong>${esc(value)}</strong></div>`).join('\n          ')}
        </div>
        <div class="quick-facts-actions">
${hasPublishedAvailability ? '' : `          ${availabilityBrowseAction}\n`}          ${ghostAction('Request Project Material')}
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

${constructionTimeline}${projectMedia.section ? `    ${projectMedia.section}\n\n` : ''}    <section class="project-section" id="residences">
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
            ${hasFloorplans
              ? '<a class="btn ghost project-btn" href="#availability">View Floorplans</a>'
              : '<a class="btn ghost project-btn" href="#enquire" data-prefill>Request Floorplans</a>'}
          </article>`).join('\n          ')}
        </div>
        <div class="inline-cta-panel reveal-soft">
          <div>
            <span class="fine-label">Private Material</span>
            <p>Current layouts, view positions and unit availability should be reviewed against the latest developer file before shortlisting.</p>
          </div>
          <div class="inline-cta-actions">
${hasPublishedAvailability ? '' : `            ${availabilityBrowseAction}\n`}            ${ghostAction('View Floorplans', hasFloorplans ? '#availability' : '#enquire')}
          </div>
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
            ${availabilityEnquiryAction}
            ${advisorAction(project)}
          </div>
        </div>
${availabilityRelease ? `        ${availabilityRelease}\n` : ''}      </div>
    </section>

    <section class="project-section calculator-section" id="calculator">
      <div class="project-inner">
        <div class="section-head center reveal-soft">
          <span class="section-kicker">Affordability</span>
          <div class="rule"></div>
          <h2 class="section-headline">Estimate your <em>monthly payment</em></h2>
          <p class="body-copy">A quick indicative estimate only. Confirm exact terms with your lender before making any decision.</p>
        </div>
        <div class="calculator-panel reveal-soft" data-calculator>
          <div class="calculator-inputs">
            <div class="calculator-field calculator-field--dual">
              <div class="calculator-field-label"><span>Purchase price</span><em data-calc-price-readout>&euro;0</em></div>
              <input type="range" data-calc-price-range min="150000" max="3000000" step="5000" value="${esc(calculatorSeedPrice)}">
              <input type="number" data-calc-price value="${esc(calculatorSeedPrice)}" min="0" step="1000" class="calculator-field-number">
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
                <input type="number" data-calc-rate value="3.5" min="0" max="15" step="0.1">
              </label>
              <div class="calculator-rate-toggle" data-calc-rate-toggle role="group" aria-label="Rate type">
                <button type="button" class="is-active" data-rate-type="fixed">Fixed</button>
                <button type="button" data-rate-type="variable">Variable</button>
              </div>
            </div>
            <label class="calculator-field">
              <span>Taxes &amp; purchase costs</span>
              <input type="number" data-calc-costs value="10" min="0" max="20" step="0.5">
              <em class="calculator-field-hint">Indicative only &mdash; ITP/VAT, notary, registry and legal fees vary by case. Confirm exact costs with your lawyer.</em>
            </label>
          </div>
          <div class="calculator-results">
            <div class="calculator-result calculator-result--highlight"><span>Estimated monthly payment</span><strong data-calc-monthly>&euro;0</strong></div>
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
              <div class="calculator-result"><span>Total cost of property</span><strong data-calc-total-property>&euro;0</strong></div>
            </div>
          </div>
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

    <section class="project-section project-why" id="why-this-project">
      <div class="project-inner why-grid">
        <div class="reveal-soft">
          <span class="section-kicker">Why This Project</span>
          <div class="rule"></div>
          <h2 class="section-headline">${why.headlineHtml}</h2>
          <p class="project-lead">${esc(why.copy)}</p>
        </div>
        <div class="why-point-grid why-point-grid--merged">
          ${[
            ...(why.points || []),
            ...(project.investment?.cards || []),
            ...(trustDossier.cards || [])
          ].map(([title, body]) => `<article class="why-point reveal-soft"><h3>${esc(title)}</h3><p>${esc(body)}</p></article>`).join('\n          ')}
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

    <section class="project-section project-file-section" id="project-file">
      <div class="project-inner">
        <div class="section-head reveal-soft">
          <span class="section-kicker">Project Information</span>
          <div class="rule"></div>
          <h2 class="section-headline">${projectFile.headlineHtml}</h2>
          <p class="project-lead">${esc(projectFile.copy)}</p>
        </div>${projectFile.image ? `
        <figure class="project-plan reveal-soft">
          ${imageTag(projectFile.image)}
          ${projectFile.image.caption ? `<figcaption>${esc(projectFile.image.caption)}</figcaption>` : ''}
        </figure>` : ''}
        <div class="document-center">
          ${renderDocumentRows(projectFile.documents, hasPublishedAvailability, hasFloorplans)}
        </div>
      </div>
    </section>

    <section class="project-section dark" id="private-viewing">
      <div class="project-inner">
        <div class="cinema-cta reveal-soft">
          ${imageTag(privateImage)}
          <div class="cinema-copy">
            <span class="section-kicker">Cinematic Presentation</span>
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

    <section class="project-section timeline-section" id="timeline">
      <div class="project-inner">
        <div class="section-head center reveal-soft">
          <span class="section-kicker">Next Steps</span>
          <div class="rule"></div>
          <h2 class="section-headline">${timeline.headlineHtml}</h2>
        </div>
        <div class="project-timeline">
          ${renderTimelineItems(timeline.items)}
        </div>
      </div>
    </section>

    <section class="project-section faq-section" id="faq">
      <div class="project-inner">
        <div class="section-head center reveal-soft">
          <span class="section-kicker">FAQ</span>
          <div class="rule"></div>
          <h2 class="section-headline">Common <em>buyer questions</em></h2>
        </div>
        <div class="faq-list">
          ${faqs.map(([question, answer], index) => `<details class="faq-item reveal-soft"${index === 0 ? ' open' : ''}>
            <summary>${esc(question)}<span class="faq-toggle-icon" aria-hidden="true"></span></summary>
            <p>${esc(answer)}</p>
          </details>`).join('\n          ')}
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
        <form class="enquiry-card reveal-soft" id="projectForm" name="project-material-request" method="POST" data-crm-lead action="/.netlify/functions/nueva-lead">

          <input type="hidden" name="subject" data-remove-prefix value="Nueva Living enquiry - ${esc(project.name)}">

          <input type="hidden" id="f-project" name="project" value="${esc(project.name)}">
          <input type="hidden" name="preferred_area" value="${esc(project.hero?.location || '')}">
          <input type="hidden" name="property_type_interest" value="${esc(project.hero?.type || '')}">
          <input type="hidden" name="budget_range" value="${esc(project.hero?.startingPrice || '')}">
          <div class="form-grid">
            <div class="field">
              <label for="f-first-name">First Name</label>
              <input id="f-first-name" name="first_name" type="text" autocomplete="given-name" placeholder="First name" required>
            </div>
            <div class="field">
              <label for="f-last-name">Last Name</label>
              <input id="f-last-name" name="last_name" type="text" autocomplete="family-name" placeholder="Last name" required>
            </div>
            <div class="field">
              <label for="f-email">Email</label>
              <input id="f-email" name="email" type="email" autocomplete="email" placeholder="your@email.com" required>
            </div>
            <div class="field">
              <label for="f-phone">Phone / WhatsApp</label>
              <input id="f-phone" name="phone" type="tel" autocomplete="tel" placeholder="+34 or international">
            </div>
            <div class="field full">
              <label for="f-msg">Message</label>
              <textarea id="f-msg" name="message">${esc(project.enquiry.message)}</textarea>
            </div>
            <label class="consent-row field full" for="f-consent">
              <input id="f-consent" name="consent" type="checkbox" required>
              <span>I agree to be contacted and for my data to be stored.</span>
            </label>
            <label class="consent-row field full" for="f-marketing-opt-in">
              <input id="f-marketing-opt-in" name="marketing_opt_in" type="checkbox">
              <span>I would also like to receive occasional project updates from Nueva Living.</span>
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

${projectMedia.dialog ? `  ${projectMedia.dialog}\n\n` : ''}  <div class="sticky-mobile-cta" aria-label="Project request actions">
    <a href="#enquire" data-prefill>${hasPublishedAvailability ? 'Ask About a Home' : 'Request Availability'}</a>
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

function buildCompareCatalog(projects) {
  return projects
    .filter((project) => !project.archived)
    .map((project) => {
      const discovery = project.discovery || {};
      const crm = project.crm || {};
      return {
        slug: project.slug,
        name: project.name,
        url: project.output,
        image: assetUrl(cardImage(project).src),
        area: discovery.area || crm.area || null,
        propertyTypes: crm.propertyTypes || discovery.propertyTypes || [],
        priceMin: crm.priceMin ?? discovery.price ?? null,
        priceMax: crm.priceMax ?? null,
        bedroomsMin: crm.bedroomsMin ?? null,
        bedroomsMax: crm.bedroomsMax ?? null,
        totalUnits: crm.totalUnits ?? null,
        availableUnits: crm.availableUnits ?? null,
        constructionStatus: crm.constructionStatus || null,
        deliveryDate: crm.deliveryDate || null,
        amenities: crm.amenities || []
      };
    });
}

function buildSearchCatalog(projects) {
  return projects
    .filter((project) => !project.archived)
    .map((project) => {
      const discovery = project.discovery || {};
      const crm = project.crm || {};
      const tags = [
        ...(discovery.lifestyleTags || []),
        ...(discovery.architectureTags || []),
        ...(discovery.locationTags || []),
        ...(discovery.investmentTags || [])
      ];
      return {
        slug: project.slug,
        name: project.name,
        area: discovery.area || crm.area || null,
        propertyTypes: crm.propertyTypes || discovery.propertyTypes || [],
        priceMin: crm.priceMin ?? discovery.price ?? null,
        priceMax: crm.priceMax ?? null,
        bedroomsMin: crm.bedroomsMin ?? null,
        bedroomsMax: crm.bedroomsMax ?? null,
        constructionStatus: crm.constructionStatus || null,
        tags: [...new Set(tags)],
        description: project.description || '',
        overview: (project.overview?.copy || []).join(' '),
        why: project.why?.copy || '',
        location: project.location?.copy || '',
        distances: project.location?.distances || []
      };
    });
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

function renderProjectCardGallery(project) {
  const items = (project.media?.items || []).slice(0, 6);
  if (!items.length) return responsiveCardImageTag(cardImage(project));

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

function renderProjectCard(project) {
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
  const crm = project.crm || {};
  const propertyTypes = normaliseCardList(crm.propertyTypes);

  return `          <article class="project-card" id="${esc(project.slug)}" data-project-card${attr('data-title', project.name)}${attr('data-price', price)}${attr('data-completion', completion)}${attr('data-release', discovery.releaseDate)}${attr('data-priority', discovery.priority ?? project.card?.order ?? 999)}${attr('data-featured', discovery.featured ? 'true' : 'false')}${attr('data-area', discovery.area)}${discoveryAttr('data-property-types', propertyTypes)}${attr('data-status', crm.constructionStatus)}${attr('data-bedrooms-min', crm.bedroomsMin)}${attr('data-bedrooms-max', crm.bedroomsMax)}${discoveryAttr('data-tags', allTags)}${discoveryAttr('data-lifestyle', lifestyleTags)}${discoveryAttr('data-architecture', architectureTags)}${discoveryAttr('data-location', locationTags)}${discoveryAttr('data-investment', investmentTags)}${discoveryAttr('data-practical', practicalTags)}>
            ${renderProjectCardGallery(project)}
            <div class="project-body">
              <span class="label">${esc(project.card?.label || project.hero?.location || 'New Development')}</span>
              <h3>${esc(project.name)}</h3>
              <p>${esc(project.card?.description || project.description)}</p>
              <div class="meta">${meta.map(([label, value]) => `<div><span>${esc(label)}</span><strong>${esc(value)}</strong></div>`).join('')}</div>
              ${cardTags.length ? `<div class="project-tags">${renderDiscoveryTags(cardTags)}</div>` : ''}
              <a class="project-link" href="${esc(project.output)}">Explore Project</a>
            </div>
          </article>`;
}

function titleCase(value = '') {
  return String(value).replace(/\w\S*/g, (word) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase());
}

function renderHomeCard(project, index) {
  const card = project.card || {};
  const discovery = project.discovery || {};
  const meta = card.meta || [
    ['From', project.hero?.startingPrice?.replace(/^From\s+/i, '') || 'On request'],
    ['Type', project.hero?.type || 'Residences'],
    ['Delivery', project.hero?.delivery || 'On request']
  ];
  const priceValue = (meta.find(([label]) => /^from$/i.test(label)) || [])[1]
    || project.hero?.startingPrice?.replace(/^From\s+/i, '')
    || 'On request';
  const badge = card.badge || titleCase(discovery.status || 'Current Release');
  const loc = card.locExtended || card.label || project.hero?.location || '';
  const typeTag = card.typeTag || (discovery.locationTags || [])[0] || card.label || '';
  const picture = renderProjectCardGallery(project);

  return `      <div class="dev-card reveal" style="transition-delay:${(0.2 + index * 0.05).toFixed(2)}s" data-card-url="${esc(project.output)}">
        <div class="dev-img-wrap">
          <span class="dev-badge">${esc(badge)}</span>
          ${picture}
          <div class="dev-img-overlay"></div>
          <div class="dev-price-overlay">From ${esc(priceValue)}</div>
        </div>
        <div class="dev-body">
          <div class="dev-loc">${esc(loc)}</div>
          <div class="dev-name">${esc(project.name)}</div>
          <p class="dev-tagline">${esc(card.description || project.description)}</p>
          <div class="dev-meta">
            ${meta.map(([label, value]) => `<div class="dev-meta-item"><span class="lbl">${esc(label)}</span><span class="val">${esc(value)}</span></div>`).join('\n            ')}
          </div>
          <div class="dev-footer">
            <a class="dev-cta-link" href="${esc(project.output)}">Discover Project</a>
            <span class="dev-type-tag">${esc(typeTag)}</span>
          </div>
        </div>
      </div>`;
}

const AREA_DISPLAY_NAMES = {
  marbella: 'Marbella',
  estepona: 'Estepona',
  benahavis: 'Benahavís',
  'nueva-andalucia': 'Nueva Andalucía',
  'mijas-fuengirola': 'Mijas & Fuengirola'
};

const VIEWING_SCENE_CATEGORY_TXT = {
  Exteriors: 'exterior',
  Location: 'exterior',
  Residences: 'interior',
  Resort: 'amenity'
};

const VIEWING_SCENE_OVERLAY = 'linear-gradient(to right, rgba(10,9,8,0.42), rgba(10,9,8,0.15), rgba(10,9,8,0.06))';

// Cinematic Presentation scenes, auto-derived from the project's own curated
// media gallery so every project gets its own real photos by default --
// never a stand-in fallback belonging to a different project.
function renderViewingScenesJs(project) {
  const items = project.media?.items || [];
  if (!items.length) return null;

  const scenes = items.map((item, index) => {
    const num = String(index + 1).padStart(2, '0');
    const isLast = index === items.length - 1;
    const txt = isLast ? 'closing' : (VIEWING_SCENE_CATEGORY_TXT[item.category] || 'exterior');
    const motion = index % 2 === 0
      ? '(p) => ({ s: 1.06 - p * 0.02, x: p * -10, y: p * -2 })'
      : '(p) => ({ s: 1.055 - p * 0.018, x: p * 10, y: 0 })';
    return `    {
      img: ${JSON.stringify(item.src)},
      pos: "center 50%",
      label: ${JSON.stringify(`${num} — ${item.category || 'Residence'}`)},
      hl: ${JSON.stringify(item.caption || project.shortName || project.name)},
      sub: ${JSON.stringify(item.alt || '')},
      gold: ${isLast ? 'true' : 'false'},
      ov: ${JSON.stringify(VIEWING_SCENE_OVERLAY)},
      txt: ${JSON.stringify(txt)},
      motion: ${motion}
    }`;
  });

  return `  ${JSON.stringify(project.slug)}: [\n${scenes.join(',\n')}\n  ]`;
}

// Cinematic Presentation project metadata (info panel), derived from the same
// project.json fields used everywhere else on the site instead of a
// hand-duplicated copy that can drift out of sync.
function renderViewingProjectEntryJs(project) {
  const discovery = project.discovery || {};
  const viewing = project.viewing || {};
  const areaDisplay = AREA_DISPLAY_NAMES[discovery.area] || project.card?.label || project.hero?.location || '';
  const highlights = project.architecture?.highlights || [];
  const investmentNotes = (project.investment?.cards || []).map(([, note]) => note).filter(Boolean);
  const availability = viewing.availability || [
    { label: 'Status', value: discovery.status || project.hero?.delivery || 'On request' },
    { label: 'Material', value: 'Brochure, floorplans and current price list' },
    { label: 'Next Step', value: `Ask for the latest ${project.shortName || project.name} information` }
  ];

  const entry = {
    id: project.slug,
    name: project.name,
    location: project.hero?.location || '',
    area: areaDisplay,
    price: project.hero?.startingPrice || 'On request',
    bedrooms: discovery.bedrooms || '',
    builtSize: viewing.builtSize || 'Residence-specific',
    terraceSize: viewing.terraceSize || 'Residence-specific',
    completion: project.hero?.delivery || 'On request',
    status: discovery.status || '',
    lifestyle: project.description || '',
    overview: project.overview?.copy?.[0] || project.description || '',
    highlights,
    investmentNotes,
    availability,
    ctaLabel: viewing.ctaLabel || 'Get Project Information',
    ctaMessage: project.enquiry?.message || `I would like to receive the latest information for ${project.name}.`
  };

  return `  ${JSON.stringify(project.slug)}: ${JSON.stringify(entry, null, 4).replace(/\n/g, '\n  ')}`;
}

function updateHomepageViewingData(projects) {
  if (!existsSync(homepagePage)) return false;

  let html = readFileSync(homepagePage, 'utf8');
  const sorted = [...projects].sort((a, b) => (a.discovery?.priority ?? a.card?.order ?? 999) - (b.discovery?.priority ?? b.card?.order ?? 999));
  const defaultId = sorted[0]?.slug || '';

  const projectsBlock = `/* NUEVA GENERATED VIEWING PROJECTS START */
  const VIEWING_PROJECTS = {
${sorted.map(renderViewingProjectEntryJs).join(',\n')}
  };
  const DEFAULT_VIEWING_PROJECT_ID = ${JSON.stringify(defaultId)};
  /* NUEVA GENERATED VIEWING PROJECTS END */`;

  const scenesBlock = `/* NUEVA GENERATED VIEWING SCENES START */
  const PROJECT_VIEWING_SCENE_SETS = {
${sorted.map(renderViewingScenesJs).filter(Boolean).join(',\n')}
  };
  /* NUEVA GENERATED VIEWING SCENES END */`;

  const projectsStart = html.indexOf('/* NUEVA GENERATED VIEWING PROJECTS START */');
  const projectsEnd = html.indexOf('/* NUEVA GENERATED VIEWING PROJECTS END */');
  const scenesStart = html.indexOf('/* NUEVA GENERATED VIEWING SCENES START */');
  const scenesEnd = html.indexOf('/* NUEVA GENERATED VIEWING SCENES END */');

  if (projectsStart === -1 || projectsEnd === -1 || scenesStart === -1 || scenesEnd === -1) {
    throw new Error('nueva-living-home.html is missing NUEVA GENERATED VIEWING markers.');
  }

  const projectsEndTag = '/* NUEVA GENERATED VIEWING PROJECTS END */';
  const scenesEndTag = '/* NUEVA GENERATED VIEWING SCENES END */';

  html = scenesStart < projectsStart
    ? html.slice(0, scenesStart) + scenesBlock + html.slice(scenesEnd + scenesEndTag.length, projectsStart) + projectsBlock + html.slice(projectsEnd + projectsEndTag.length)
    : html.slice(0, projectsStart) + projectsBlock + html.slice(projectsEnd + projectsEndTag.length, scenesStart) + scenesBlock + html.slice(scenesEnd + scenesEndTag.length);

  writeFileSync(homepagePage, html);
  return true;
}

function updateHomepageProjectCards(projects) {
  if (!existsSync(homepagePage)) return false;

  const html = readFileSync(homepagePage, 'utf8');
  const start = html.indexOf(generatedHomeCardsStart);
  const end = html.indexOf(generatedHomeCardsEnd);

  if (start === -1 || end === -1 || end < start) {
    throw new Error('nueva-living-home.html is missing NUEVA GENERATED HOME PROJECTS markers.');
  }

  const featured = projects
    .filter((project) => project.discovery?.featured && !project.archived)
    .sort((a, b) => (a.discovery?.priority ?? a.card?.order ?? 999) - (b.discovery?.priority ?? b.card?.order ?? 999));

  const cards = featured.map(renderHomeCard).join('\n\n');
  const before = html.slice(0, start + generatedHomeCardsStart.length);
  const after = html.slice(end);
  const next = `${before}\n${cards}\n      ${after}`;
  writeFileSync(homepagePage, next);
  return true;
}

function writeGeneratedGrid(html, { gridMarkerAttr, startMarker, endMarker, cards, label }) {
  const attrIndex = html.indexOf(gridMarkerAttr);
  const start = html.indexOf(startMarker);
  const end = html.indexOf(endMarker);

  if (attrIndex === -1) {
    throw new Error(`developments.html is missing the ${label} grid container.`);
  }
  if (start === -1 || end === -1 || end < start) {
    throw new Error(`developments.html is missing ${label} markers.`);
  }

  const tagClose = html.indexOf('>', attrIndex);
  const gridStart = html.lastIndexOf('<div', attrIndex);
  const gridContentStart = tagClose + 1;
  const lineStart = html.lastIndexOf('\n', gridStart) + 1;
  const gridIndent = html.slice(lineStart, gridStart);
  const cardIndent = `${gridIndent}  `;
  const generatedBlock = `\n${cardIndent}${startMarker}\n${cards}\n${cardIndent}${endMarker}`;
  return `${html.slice(0, gridContentStart)}${generatedBlock}${html.slice(end + endMarker.length)}`;
}

function updateDevelopmentsPage(projects) {
  if (!existsSync(developmentsPage)) return false;

  const activeProjects = projects.filter((project) => !project.archived);
  // "Earlier Sold Projects" is a track-record tab: developments that have
  // sold out and are no longer part of the active marketing set. Set
  // `"archived": true` on a project's project.json to move it here.
  const soldProjects = projects.filter((project) => project.archived);

  let html = readFileSync(developmentsPage, 'utf8');
  html = writeGeneratedGrid(html, {
    gridMarkerAttr: 'data-project-grid',
    startMarker: generatedProjectsStart,
    endMarker: generatedProjectsEnd,
    cards: activeProjects.map(renderProjectCard).join('\n'),
    label: 'NUEVA GENERATED PROJECTS'
  });

  if (html.includes('data-archived-project-grid')) {
    html = writeGeneratedGrid(html, {
      gridMarkerAttr: 'data-archived-project-grid',
      startMarker: generatedArchivedProjectsStart,
      endMarker: generatedArchivedProjectsEnd,
      cards: soldProjects.map(renderProjectCard).join('\n'),
      label: 'NUEVA GENERATED ARCHIVED PROJECTS'
    });
  }

  writeFileSync(developmentsPage, html);
  return true;
}

async function syncProjectsToCrm(projects) {
  const secret = cleanEnvironmentValue(process.env.CRM_WEBHOOK_SECRET);
  if (!secret) {
    return {
      enabled: false,
      reason: 'CRM_WEBHOOK_SECRET is not available in the build environment'
    };
  }

  const webhookUrl = cleanEnvironmentValue(process.env.CRM_PROPERTY_WEBHOOK_URL)
    || DEFAULT_PROPERTY_WEBHOOK_URL;
  const strict = cleanEnvironmentValue(process.env.CRM_PROPERTY_SYNC_STRICT).toLowerCase() === 'true';
  const results = [];

  for (const project of projects) {
    const payload = projectToPropertyPayload(project, { siteUrl });
    const errors = validatePropertyPayload(payload, payload);

    if (errors.length) {
      const message = `${project.name || project.slug}: ${errors.join('; ')}`;
      results.push({ name: project.name || project.slug, success: false, error: message });
      if (strict) throw new Error(`CRM property sync validation failed: ${message}`);
      console.warn(`CRM property sync skipped: ${message}`);
      continue;
    }

    try {
      const result = await sendPropertyToCrm(payload, { secret, webhookUrl });
      results.push({
        name: payload.name,
        success: true,
        property_id: result.property_id,
        action: result.action
      });
    } catch (error) {
      const message = error.message || 'Unknown CRM property sync error';
      results.push({ name: payload.name, success: false, error: message });
      if (strict) throw error;
      console.warn(`CRM property sync failed for ${payload.name}: ${message}`);
    }
  }

  return {
    enabled: true,
    synced: results.filter((item) => item.success).length,
    failed: results.filter((item) => !item.success).length,
    results
  };
}

// Required sections whose headlineHtml (and, for a couple, copy) is
// interpolated directly into the page with no fallback -- an omitted
// field would otherwise render as the literal string "undefined" on a
// live page instead of failing the build. `media` is only required
// when the project actually has media.items.
const REQUIRED_SECTIONS = [
  'overview', 'residences', 'availability', 'location', 'why',
  'architecture', 'projectFile', 'privateViewing', 'lifestyle', 'timeline', 'enquiry'
];

function validateProject(project) {
  const label = path.relative(process.cwd(), project.sourceFile);
  for (const key of REQUIRED_SECTIONS) {
    const section = project[key];
    if (!section || typeof section.headlineHtml !== 'string' || !section.headlineHtml.trim()) {
      throw new Error(`${label}: "${key}.headlineHtml" is missing -- it renders directly into the page with no fallback.`);
    }
  }
  // investment.cards and trustDossier.cards feed the merged "Why This
  // Project" grid alongside why.points -- their own headlineHtml/copy no
  // longer render anywhere, but the cards themselves still need to exist.
  if (!project.investment?.cards?.length) {
    throw new Error(`${label}: "investment.cards" is missing or empty -- it feeds the merged Why This Project grid.`);
  }
  if (!project.trustDossier?.cards?.length) {
    throw new Error(`${label}: "trustDossier.cards" is missing or empty -- it feeds the merged Why This Project grid.`);
  }
  if (project.media?.items?.length) {
    if (typeof project.media.headlineHtml !== 'string' || !project.media.headlineHtml.trim()) {
      throw new Error(`${label}: "media.headlineHtml" is missing -- required whenever media.items is set.`);
    }
    if (typeof project.media.copy !== 'string' || !project.media.copy.trim()) {
      throw new Error(`${label}: "media.copy" is missing -- required whenever media.items is set.`);
    }
    if (!project.media.items.some((item) => item.category)) {
      throw new Error(`${label}: no media.items have a "category" -- the preview grid groups by category, so without one it renders as an empty gap above the "View all" button.`);
    }
  }
}

const written = [];
const projects = loadProjects();
for (const project of projects) {
  if (!project.slug || !project.output) {
    throw new Error(`${path.relative(process.cwd(), project.sourceFile)} must include slug and output.`);
  }
  validateProject(project);

  const html = renderProject(project);
  writeFileSync(path.resolve(project.output), html);
  written.push(project.output);
}

const developmentsUpdated = updateDevelopmentsPage(projects);
const homepageUpdated = updateHomepageProjectCards(projects);
const viewingUpdated = updateHomepageViewingData(projects);
const crmSync = await syncProjectsToCrm(projects);

const searchCatalogDir = path.resolve('netlify/functions/data');
mkdirSync(searchCatalogDir, { recursive: true });
writeFileSync(path.join(searchCatalogDir, 'projects-catalog.json'), JSON.stringify(buildSearchCatalog(projects), null, 2));

const compareCatalogDir = path.resolve('assets/liora/data');
mkdirSync(compareCatalogDir, { recursive: true });
writeFileSync(path.join(compareCatalogDir, 'projects-catalog.json'), JSON.stringify(buildCompareCatalog(projects), null, 2));

console.log(JSON.stringify({ written, developmentsUpdated, homepageUpdated, viewingUpdated, crmSync }, null, 2));
