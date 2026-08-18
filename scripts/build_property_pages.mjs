import { existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import path from 'node:path';
import propertySync from '../lib/nueva-property-sync.cjs';
import {
  LOCALES,
  DEFAULT_LOCALE,
  localeMeta,
  isRtl,
  t,
  localizeProject,
  hasString,
  localizedPath,
  hreflangLinks,
  rootPrefix,
  baseHrefTag,
  renderLanguageSwitcher,
  LANG_SWITCHER_SCRIPT
} from './lib/i18n.mjs';
import { UNIT_FLOORS } from './lib/unit_floor_translations.mjs';
import { renderUnifiedCard } from './lib/project_card.mjs';
import { realEstateAgentSchema } from './lib/brand.mjs';
// The homepage and developments grids are rendered in English and then
// localized by find/replace entry tables, so the card resolves its strings
// against English here and card_chrome_translations.mjs swaps them later.
const enT = (key, vars) => t(key, 'en', vars);
import { renderProjectCardGallery } from './lib/card_gallery.mjs';
import { hasLiveLocationMap, renderLocationCard, leafletHead } from './lib/location_map.mjs';

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
const fontPreloadBlock = (p = '', locale = 'en') => `  <link rel="preload" href="${p}assets/fonts/google/8vIJ7ww63mVu7gt79mT7PkRXMw.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="${p}assets/fonts/google/JTUSjIg1_i6t8kCHKm459WlhyyTh89Y.woff2" as="font" type="font/woff2" crossorigin>${locale === 'ar' ? `
  <link rel="preload" href="${p}assets/fonts/arabic/SLXVc1nY6HkvangtZmpQdkhzfH5lkSscQyyS4J0.woff2" as="font" type="font/woff2" crossorigin>` : ''}`;
const propertyCssVersion = fileVersion('assets/liora/liora-property.css');
const rtlCssVersion = existsSync('assets/liora/liora-rtl.css') ? fileVersion('assets/liora/liora-rtl.css') : '1';
const propertyJsVersion = fileVersion('assets/liora/liora-property.js');
const locationMapCssVersion = fileVersion('assets/liora/nueva-location-map.css');
const locationMapJsVersion = fileVersion('assets/liora/nueva-location-map.js');
const calculatorJsVersion = fileVersion('assets/liora/liora-calculator.js');

// General buyer-process questions that apply to every development. A
// project's own `faq` array (if set) is appended after these, for
// anything specific to that particular release.
function defaultFaqs(locale = DEFAULT_LOCALE) {
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

function fileVersion(file) {
  return createHash('sha256').update(readFileSync(path.resolve(file))).digest('hex').slice(0, 12);
}

// Availability-table bedroom values are formulaic data strings ("3 bedrooms",
// "Apartment · 2 bed / 2 bath", "5 bed / 6 bath"), not prose -- so they are
// localized by re-formatting the numbers through strings.json templates
// rather than by hand-translating 200+ near-identical data rows. Anything
// that does not match a known shape is returned untouched, so an unusual
// value degrades to English rather than being mangled.
// Unit size values are mostly bare figures ("155 m²") that need no
// translation, but some carry English qualifiers -- "581.72 m² built /
// 985.98 m² plot", "370 m², private pool". Those are re-composed through
// strings.json templates so the numbers stay untouched while the words
// follow the reader's language. Unrecognised shapes pass through as-is.
function localizedUnitSize(value, locale = DEFAULT_LOCALE) {
  if (!value || locale === DEFAULT_LOCALE) return value;
  const raw = String(value).trim();

  const builtPlot = /^([\d.,]+)\s*m²\s*built\s*\/\s*([\d.,]+)\s*m²\s*plot$/i.exec(raw);
  if (builtPlot) return t('unit.builtPlot', locale, { built: builtPlot[1], plot: builtPlot[2] });

  const pool = /^(.+?),\s*private pool$/i.exec(raw);
  if (pool) return t('unit.withPrivatePool', locale, { size: localizedUnitSize(pool[1], locale) });

  return raw;
}

function localizedUnitFloor(value, locale = DEFAULT_LOCALE) {
  if (!value || locale === DEFAULT_LOCALE) return value;
  return UNIT_FLOORS[String(value).trim()]?.[locale] || value;
}

function localizedUnitBedrooms(value, locale = DEFAULT_LOCALE) {
  if (!value || locale === DEFAULT_LOCALE) return value;
  const raw = String(value).trim();

  const typePrefix = /^(Apartment|Villa|Penthouse|Townhouse)\s*·\s*(.+)$/i.exec(raw);
  if (typePrefix) {
    const typeKey = `unit.type${typePrefix[1][0].toUpperCase()}${typePrefix[1].slice(1).toLowerCase()}`;
    const type = t(typeKey, locale);
    const rest = localizedUnitBedrooms(typePrefix[2], locale);
    return `${type === typeKey ? typePrefix[1] : type} · ${rest}`;
  }

  const bedBath = /^(\d+)\s*bed\s*\/\s*(\d+)\s*bath$/i.exec(raw);
  if (bedBath) return t('unit.bedBath', locale, { b: bedBath[1], ba: bedBath[2] });

  const bedroomsBath = /^(\d+)\s*bedrooms?\s*\/\s*(\d+)\s*bathrooms?$/i.exec(raw);
  if (bedroomsBath) return t('unit.bedroomsBathrooms', locale, { n: bedroomsBath[1], m: bedroomsBath[2] });

  const plain = /^(\d+)\s*bedrooms?$/i.exec(raw);
  if (plain) {
    return Number(plain[1]) === 1
      ? t('unit.bedroomCount', locale, { n: plain[1] })
      : t('unit.bedroomsCount', locale, { n: plain[1] });
  }

  return raw;
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

function imageTag(img, className = '', loading = 'lazy', { priority = false } = {}) {
  const style = img.focus ? ` style="object-position: ${esc(img.focus)};"` : '';
  // The LCP image must not be lazy-loaded, and benefits from an explicit
  // priority hint so the browser fetches it ahead of other subresources.
  const loadingAttr = priority ? ' loading="eager" fetchpriority="high"' : (loading ? attr('loading', loading) : '');
  return `<img${className ? ` class="${className}"` : ''} src="${esc(img.src)}" alt="${esc(img.alt || '')}"${attr('width', img.width)}${attr('height', img.height)}${loadingAttr} decoding="async"${style}>`;
}

// Wraps an image in <picture> with WebP sources when the derivatives
// generated by scripts/generate_image_derivatives.py exist on disk. WebP
// runs ~58% smaller than these JPEGs, which matters most for the hero --
// it is the LCP element on every property page. Falls back to the plain
// <img> when a derivative is missing, so nothing breaks if one is absent.
function pictureTag(img, className = '', loading = 'lazy', options = {}) {
  const match = String(img.src || '').match(/^(.*)\.(?:jpe?g)$/i);
  if (!match) return imageTag(img, className, loading, options);
  const base = match[1];
  if (!existsSync(`${base}.webp`)) return imageTag(img, className, loading, options);
  const srcset = [
    [`${base}-640.webp`, 640],
    [`${base}-960.webp`, 960],
    [`${base}.webp`, img.width || 1920]
  ].filter(([file]) => existsSync(file)).map(([file, w]) => `${esc(file)} ${w}w`).join(', ');
  const sizes = options.sizes || '100vw';
  return `<picture>
        <source type="image/webp" srcset="${srcset}" sizes="${esc(sizes)}">
        ${imageTag(img, className, loading, options)}
      </picture>`;
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

// Matterport embeds accept flags that strip their chrome. title=0 removes the
// model title -- which is the developer's own project name, not the name this
// site publishes -- and brand=0 removes Matterport's branding. Both are forced
// on regardless of how the URL was stored, so a pasted share link cannot leak
// the name back onto the page.
function tourEmbedUrl(rawUrl) {
  const url = new URL(String(rawUrl));
  url.searchParams.set('title', '0');
  url.searchParams.set('brand', '0');
  url.searchParams.set('help', '0');
  return url.toString();
}

function localizedCategory(category, locale) {
  const key = `mediaCategory.${category}`;
  return category ? t(key, locale) : category;
}

function renderProjectMedia(project, locale = DEFAULT_LOCALE) {
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
            <button type="button" class="project-media-film-play" data-project-video-play aria-label="${esc(t('media.playFilm', locale))} ${esc(video.title || `${project.name} film`)}">
              <span class="project-media-film-play-icon" aria-hidden="true"></span>
              <span>${t('media.playFilm', locale)}</span>
            </button>
          </div>
          <figcaption>
            <span>${t('media.film', locale)}</span>
            <strong>${esc(video.title || '')}</strong>
            <p>${esc(video.caption || '')}</p>
          </figcaption>
        </figure>` : '';

  /* A 360 tour is a third-party embed weighing several megabytes, so it loads
     only when asked: the poster is a still from the project, and the iframe
     replaces it on click. Matterport's own title bar and branding are switched
     off (title=0&brand=0) because the tour is titled with the developer's
     project name, which this site does not publish. */
  const tour = media.tour;
  const tourBlock = tour?.url ? `<figure class="project-tour reveal-soft" data-project-tour>
          <div class="project-tour-frame">
            <button type="button" class="project-tour-launch" data-tour-launch data-tour-src="${esc(tourEmbedUrl(tour.url))}" aria-label="${esc(t('media.openVirtualTour', locale))}">
              ${tour.poster ? pictureTag({ src: tour.poster, alt: tour.alt || '', width: tour.width || 1600, height: tour.height || 900 }, '', 'lazy', { sizes: MEDIA_TILE_SIZES }) : ''}
              <span class="project-tour-cta">
                <span class="project-tour-cta-icon" aria-hidden="true"></span>
                <span>${t('media.openVirtualTour', locale)}</span>
              </span>
            </button>
          </div>
          <figcaption>
            <span>${t('media.virtualTour', locale)}</span>
            <strong>${esc(tour.title || '')}</strong>
            <p>${esc(tour.caption || t('media.tourLoads', locale))}</p>
          </figcaption>
        </figure>` : '';

  const categories = [...new Set(media.items.map((item) => item.category).filter(Boolean))];
  const cards = categories.map((category) => {
    const categoryItems = media.items.filter((item) => item.category === category);
    const item = categoryItems[0];
    const count = categoryItems.length;
    const categoryLabel = localizedCategory(category, locale);
    const imageLabel = count === 1 ? t('media.imageCountSingular', locale) : t('media.imagesCount', locale, { count });
    return `<button type="button" class="project-media-card project-media-card--category" data-media-category="${esc(category)}" aria-label="${esc(t('media.viewImagesInCategory', locale, { count, category: categoryLabel }))}">
              ${pictureTag(item, '', 'lazy', { sizes: MEDIA_TILE_SIZES })}
              <span class="project-media-caption">
                <small>${esc(categoryLabel)}</small>
                <strong>${esc(item.caption || '')}</strong>
                <span class="project-media-card-cta">${esc(imageLabel)} <span aria-hidden="true">${isRtl(locale) ? '&#8592;' : '&#8594;'}</span></span>
              </span>
            </button>`;
  }).join('\n            ');

  // The gallery dialog was loading the full-size masters -- over 1MB each on
  // some projects, forty of them on Elviria. Hand it the WebP derivative
  // where one exists and keep the master as the fallback.
  const mediaData = JSON.stringify(media.items.map((item) => ({
    src: item.src,
    webp: (() => {
      const match = String(item.src || '').match(/^(.*)\.(?:jpe?g)$/i);
      return match && existsSync(`${match[1]}-960.webp`) ? `${match[1]}-960.webp` : '';
    })(),
    alt: item.alt || '',
    width: item.width || 1600,
    height: item.height || 900,
    caption: item.caption || '',
    category: item.category ? localizedCategory(item.category, locale) : t('media.kicker', locale)
  }))).replace(/</g, '\\u003c');

  const facts = (media.facts || []).map(([value, label]) => `<div class="media-fact"><strong>${esc(value)}</strong><span>${esc(label)}</span></div>`).join('\n          ');

  return {
    section: `<section class="project-section project-media-section" id="media">
      <div class="project-inner">
        <div class="project-media-intro reveal-soft">
          <div>
            <span class="section-kicker">${t('media.kicker', locale)}</span>
            <div class="rule"></div>
            <h2 class="section-headline">${media.headlineHtml}</h2>
          </div>
          <p class="project-lead">${esc(media.copy)}</p>
        </div>
        ${facts ? `<div class="media-facts reveal-soft">${facts}</div>` : ''}
        ${videoBlock}
        ${tourBlock}
        <div class="project-media-grid project-media-grid--categories" data-media-grid>
          ${cards}
        </div>
        <div class="media-gallery-footer">
          <button type="button" class="btn project-btn ghost media-show-all" data-media-show-all>${t('media.viewAllImages', locale, { count: media.items.length })}</button>
          <p class="media-note">${esc(media.note || '')}</p>
        </div>
      </div>
    </section>`,
    dialog: `<dialog class="project-media-dialog" id="projectMediaDialog" aria-label="${esc(project.name)} media viewer">
      <div class="project-media-dialog-shell" data-media-dialog-shell>
        <button type="button" class="media-dialog-close" data-media-close aria-label="${t('media.close', locale)}">${t('media.close', locale)}</button>
        <button type="button" class="media-dialog-nav media-dialog-prev" data-media-prev aria-label="${t('media.previousImage', locale)}">&#8592;</button>
        <figure class="media-dialog-figure">
          <img src="" alt="" width="1600" height="900" decoding="async" data-media-dialog-image>
          <figcaption><span data-media-dialog-count></span><strong data-media-dialog-caption></strong></figcaption>
        </figure>
        <button type="button" class="media-dialog-nav media-dialog-next" data-media-next aria-label="${t('media.nextImage', locale)}">&#8594;</button>
        <div class="media-dialog-stack" data-media-dialog-stack hidden>
          <div class="media-dialog-stack-count" data-media-dialog-stack-count></div>
        </div>
      </div>
    </dialog>
    <script type="application/json" id="projectMediaData">${mediaData}</script>`
  };
}

// The project page used to carry two fact panels: the quick-facts band under
// the hero (starting price, location, type, bedrooms, delivery, status,
// project type, availability) and a second four-card grid beside the
// overview copy (collection, outdoor living, orientation, design). They said
// overlapping things -- on ten of the fourteen projects the overview's
// "Collection: 88 residences" simply restated the band's "Project type:
// Gated resort-style community, 88 residences" -- and cost two blocks of
// page height to do it.
//
// One panel now carries both. A metric is dropped when the band already
// covers it, either by label or because its value is already contained in
// one of the band's values.
function mergedProjectFacts(project, sourceProject = project) {
  const facts = quickFacts(project);
  const metrics = project.overview?.metrics || [];

  // Every duplicate decision is made once, against the untranslated
  // project, and applied by index to each language. Deciding per locale
  // gave the same project a different number of facts in each: German kept
  // a metric English dropped because the translated wording no longer
  // matched, and Arabic dropped all four, because a Latin-only normaliser
  // reduced every Arabic label to an empty string that matched anything.
  const sourceFacts = quickFacts(sourceProject);
  const sourceMetrics = sourceProject.overview?.metrics || [];

  const key = (value) => String(value ?? '').toLowerCase().replace(/[^\p{L}\p{N}]/gu, '');

  // The hero panel already states these four, immediately above the band.
  const heroValues = [
    sourceProject.hero?.location,
    sourceProject.hero?.startingPrice,
    sourceProject.hero?.type,
    sourceProject.hero?.delivery
  ].map(key).filter(Boolean);

  const inHero = (value) => heroValues.includes(key(value));

  const covered = (label, value) => sourceFacts.some(([factLabel, factValue]) => {
    if (key(factLabel) && key(factLabel) === key(label)) return true;
    const needle = key(value);
    // Short values ("Villas", "2-4") collide by accident; only treat a
    // substring match as duplication when there is enough of it to mean
    // something.
    return needle.length > 6 && key(factValue).includes(needle);
  });

  const keepFact = sourceFacts.map(([, value]) => !inHero(value));
  const keepMetric = sourceMetrics.map(([label, value]) => !covered(label, value) && !inHero(value));

  // If a locale overlay has a different number of entries than the source,
  // the indexes no longer line up -- keep them all rather than drop the
  // wrong one.
  const factsAligned = facts.length === sourceFacts.length;
  const metricsAligned = metrics.length === sourceMetrics.length;

  return [
    ...facts.filter((_, index) => (factsAligned ? keepFact[index] : true)),
    ...metrics.filter((_, index) => (metricsAligned ? keepMetric[index] : true))
  ];
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

const MONTH_NAMES = {
  January: { en: 'January', es: 'enero', fr: 'janvier', de: 'Januar', ru: 'января', ar: 'يناير' },
  February: { en: 'February', es: 'febrero', fr: 'février', de: 'Februar', ru: 'февраля', ar: 'فبراير' },
  March: { en: 'March', es: 'marzo', fr: 'mars', de: 'März', ru: 'марта', ar: 'مارس' },
  April: { en: 'April', es: 'abril', fr: 'avril', de: 'April', ru: 'апреля', ar: 'أبريل' },
  May: { en: 'May', es: 'mayo', fr: 'mai', de: 'Mai', ru: 'мая', ar: 'مايو' },
  June: { en: 'June', es: 'junio', fr: 'juin', de: 'Juni', ru: 'июня', ar: 'يونيو' },
  July: { en: 'July', es: 'julio', fr: 'juillet', de: 'Juli', ru: 'июля', ar: 'يوليو' },
  August: { en: 'August', es: 'agosto', fr: 'août', de: 'August', ru: 'августа', ar: 'أغسطس' },
  September: { en: 'September', es: 'septiembre', fr: 'septembre', de: 'September', ru: 'сентября', ar: 'سبتمبر' },
  October: { en: 'October', es: 'octubre', fr: 'octobre', de: 'Oktober', ru: 'октября', ar: 'أكتوبر' },
  November: { en: 'November', es: 'noviembre', fr: 'novembre', de: 'November', ru: 'ноября', ar: 'نوفمبر' },
  December: { en: 'December', es: 'diciembre', fr: 'décembre', de: 'Dezember', ru: 'декабря', ar: 'ديسمبر' }
};

function localizeMonthDate(value, locale) {
  if (!value || locale === DEFAULT_LOCALE) return value;
  const match = /^(?:(\d{1,2})\s+)?([A-Z][a-z]+)\s+(\d{4})$/.exec(value.trim());
  if (!match) return value.replace(/[A-Z][a-z]+/, (month) => MONTH_NAMES[month]?.[locale] || month);
  const [, day, monthName, year] = match;
  const month = MONTH_NAMES[monthName]?.[locale] || monthName;
  if (!day) return `${month} ${year}`;
  if (locale === 'es') return `${day} de ${month} de ${year}`;
  if (locale === 'de') return `${day}. ${month} ${year}`;
  return `${day} ${month} ${year}`;
}

// Bedroom counts are free text and inconsistent across sources: "3 bedrooms",
// "Villa · 4 bed / 4 bath", "5 bed / 6 bath". The first number attached to a
// "bed" word is the bedroom count in every form we hold; the bathroom count
// always follows a "bath" word, so it never matches first.
function unitBedCount(unit) {
  const match = /(\d+)\s*bed/i.exec(String(unit.bedrooms || ''));
  return match ? Number(match[1]) : null;
}

// Prices are display strings ("€1,014,000", "€890,000 + IVA"). Only the
// leading number carries value -- the VAT/IVA suffix has no digits, so
// stripping non-digits is safe.
function unitPriceValue(unit) {
  const digits = String(unit.price || '').replace(/[^\d]/g, '');
  return digits ? Number(digits) : null;
}

// Short, locale-neutral price for band labels: €900k, €1.2M. The table itself
// keeps the exact figure -- these only need to be scannable on a chip.
function compactPrice(value) {
  if (value >= 1_000_000) {
    // Two decimals, trailing zeros trimmed: 2M, 1.5M, 1.75M. Rounding to one
    // decimal would label a €1.75M band boundary "€1.8M" and put units just
    // under the cut in what looks like the wrong band.
    const millions = (value / 1_000_000).toFixed(2).replace(/\.?0+$/, '');
    return `€${millions}M`;
  }
  return `€${Math.round(value / 1000)}k`;
}

// Bands are derived per project rather than fixed site-wide: releases run from
// sub-€400k apartments to €5M villas, so any shared set of thresholds would
// leave most projects with every unit in one band. Split at tertiles, snapped
// to a round step, and drop the whole control if that fails to separate the
// units into at least two groups.
function priceBands(values) {
  const sorted = [...values].sort((a, b) => a - b);
  if (sorted.length < 12) return [];
  const step = sorted[sorted.length - 1] >= 2_000_000 ? 250_000 : 100_000;
  const snap = (value) => Math.round(value / step) * step;
  const cuts = [...new Set([
    snap(sorted[Math.floor(sorted.length / 3)]),
    snap(sorted[Math.floor((sorted.length * 2) / 3)])
  ])].filter((cut) => cut > sorted[0] && cut <= sorted[sorted.length - 1]);
  if (!cuts.length) return [];

  const bands = [];
  let min = 0;
  for (const cut of cuts) {
    bands.push({ min, max: cut });
    min = cut;
  }
  bands.push({ min, max: Infinity });
  // A band nobody falls into is just a dead chip.
  return bands.filter((band) => values.some((v) => v >= band.min && v < band.max)).length === bands.length
    ? bands
    : [];
}

function bandLabel(band, locale) {
  if (band.min === 0) return t('availability.bandUnder', locale, { max: compactPrice(band.max) });
  if (band.max === Infinity) return t('availability.bandOver', locale, { min: compactPrice(band.min) });
  return t('availability.bandBetween', locale, {
    min: compactPrice(band.min),
    max: compactPrice(band.max)
  });
}

// Below this the chips cost more attention than the scrolling they save.
const FILTER_MIN_UNITS = 8;

function renderAvailabilityFilters(units, locale) {
  if (units.length < FILTER_MIN_UNITS) return '';

  const beds = [...new Set(units.map(unitBedCount).filter((n) => n !== null))].sort((a, b) => a - b);
  const prices = units.map(unitPriceValue).filter((n) => n !== null);
  const bands = prices.length === units.length ? priceBands(prices) : [];
  // One bedroom count and no usable bands means there is nothing to filter by.
  if (beds.length < 2 && !bands.length) return '';

  // "€1.75M+" and "€1M – €1.75M" are made of number runs joined by neutral
  // characters. In an RTL paragraph those neutrals take the paragraph
  // direction, so the trailing "+" jumps to the left and the two ends of a
  // range swap. Labels that carry no words are pinned to LTR; ones that do
  // ("أقل من €1M") are left alone so the words stay in reading order.
  const numericOnly = (label) => !/[^\s\d€.,+–\-Mk]/.test(label);
  const chip = (group, value, label, active = false) =>
    `<button type="button" class="availability-chip${active ? ' is-active' : ''}"${numericOnly(label) ? ' dir="ltr"' : ''} data-filter-group="${group}" data-filter-value="${value}" aria-pressed="${active}">${label}</button>`;

  const bedGroup = beds.length < 2 ? '' : `<div class="availability-filter-group">
                <span class="availability-filter-label">${t('availability.bedrooms', locale)}</span>
                <div class="availability-chip-row">
                  ${chip('beds', 'all', t('availability.filterAll', locale), true)}
                  ${beds.map((n) => chip('beds', String(n), t('availability.bedChip', locale, { count: n }))).join('\n                  ')}
                </div>
              </div>`;

  const bandGroup = !bands.length ? '' : `<div class="availability-filter-group">
                <span class="availability-filter-label">${t('availability.price', locale)}</span>
                <div class="availability-chip-row">
                  ${chip('price', 'all', t('availability.filterAll', locale), true)}
                  ${bands.map((band) => chip('price', `${band.min}-${band.max === Infinity ? '' : band.max}`, esc(bandLabel(band, locale)))).join('\n                  ')}
                </div>
              </div>`;

  return `<div class="availability-filters" role="group" aria-label="${t('aria.filterHomes', locale)}"
              data-availability-filters
              data-count-template="${esc(t('availability.filterShowing', locale, { shown: '{shown}', total: '{total}' }))}">
              ${bedGroup}
              ${bandGroup}
              <div class="availability-filter-meta">
                <span class="availability-filter-count" data-availability-count aria-live="polite"></span>
                <button type="button" class="availability-filter-clear" data-availability-clear hidden>${t('availability.filterClear', locale)}</button>
              </div>
            </div>
            <p class="availability-empty" data-availability-empty hidden>${t('availability.filterNone', locale)}</p>`;
}

// A floorplan is worth showing as a picture rather than a link, but most of
// them are PDFs. generate_floorplan_thumbnails renders page one of each to a
// sibling `-thumb.jpg`; where a plan is already an image it is its own thumb.
function floorplanThumb(floorplan) {
  if (!floorplan) return '';
  const asImage = String(floorplan).match(/\.(jpe?g|png)$/i);
  const candidate = asImage ? floorplan : String(floorplan).replace(/\.pdf$/i, '-thumb.jpg');
  return existsSync(candidate) ? candidate : '';
}

// Cards only where the project can actually fill them: a grid of mostly empty
// frames is worse than the table it replaced. A single unit with its own
// floorplan still earns a card -- one populated card reads better than a
// table row for showing off a single resale's layout.
const UNIT_CARD_MIN_COVERAGE = 0.75;

function usesUnitCards(units) {
  if (!units.length) return false;
  const withThumb = units.filter((unit) => floorplanThumb(unit.floorplan)).length;
  return withThumb / units.length >= UNIT_CARD_MIN_COVERAGE;
}

function responsiveThumb(src, alt) {
  const base = String(src).replace(/\.(jpe?g|png)$/i, '');
  const candidates = [[`${base}-640.webp`, 640], [`${base}-960.webp`, 960]]
    .filter(([file]) => existsSync(file))
    .map(([file, width]) => `${esc(file)} ${width}w`);
  const img = `<img src="${esc(src)}" alt="${esc(alt)}" loading="lazy" decoding="async">`;
  if (!candidates.length) return img;
  return `<picture>
                    <source type="image/webp" srcset="${candidates.join(', ')}" sizes="(max-width: 640px) 92vw, (max-width: 1100px) 46vw, 30vw">
                    ${img}
                  </picture>`;
}

function renderUnitCard(unit, project, locale) {
  const beds = unitBedCount(unit);
  const price = unitPriceValue(unit);
  const thumb = floorplanThumb(unit.floorplan);
  const reference = esc(unit.reference);

  const media = thumb
    ? `<a class="unit-card-plan" href="${esc(unit.floorplan)}" target="_blank" rel="noopener" aria-label="${t('availability.floorplanOf', locale, { reference })}">
                  ${responsiveThumb(thumb, t('availability.floorplanOf', locale, { reference }))}
                  <span class="unit-card-plan-hint">${t('availability.viewFloorplan', locale)}</span>
                </a>`
    : '';

  const facts = [
    [t('availability.bedrooms', locale), localizedUnitBedrooms(unit.bedrooms, locale)],
    unit.size ? [t('availability.size', locale), localizedUnitSize(unit.size, locale)] : null,
    unit.floor ? [t('availability.floor', locale), localizedUnitFloor(unit.floor, locale)] : null
  ].filter(Boolean);

  return `<article class="unit-card" data-unit${beds === null ? '' : ` data-beds="${beds}"`}${price === null ? '' : ` data-price="${price}"`}>
                ${media}
                <div class="unit-card-body">
                  <div class="unit-card-head">
                    <strong class="unit-card-ref">${reference}</strong>
                    <span class="availability-status">${t('availability.available', locale)}</span>
                  </div>
                  <dl class="unit-card-facts">
                    ${facts.map(([label, value]) => `<div><dt>${label}</dt><dd>${esc(value)}</dd></div>`).join('\n                    ')}
                  </dl>
                  <p class="unit-card-price">${esc(unit.price)}</p>
                  <a class="unit-card-cta" href="contact.html?intent=${encodeURIComponent(`${project.name} - ${unit.reference}`)}">${t('availability.askAboutUnit', locale, { reference })}</a>
                </div>
              </article>`;
}

function renderAvailabilityRelease(project, locale = DEFAULT_LOCALE) {
  const availability = project.availability || {};
  const units = availability.units || [];
  if (!units.length) return '';

  const hasFloorplans = units.some((unit) => unit.floorplan);
  const hasSize = units.some((unit) => unit.size);
  const hasFloor = units.some((unit) => unit.floor);
  const filters = renderAvailabilityFilters(units, locale);
  const cardGrid = usesUnitCards(units)
    ? `<div class="unit-card-grid" role="list" aria-label="${t('aria.availableUnits', locale)}">
              ${units.map((unit) => renderUnitCard(unit, project, locale)).join('\n              ')}
            </div>`
    : '';

  const rows = units.map((unit) => {
    const beds = unitBedCount(unit);
    const price = unitPriceValue(unit);
    return `<tr${beds === null ? '' : ` data-beds="${beds}"`}${price === null ? '' : ` data-price="${price}"`}>
                <td data-label="${t('availability.reference', locale)}"><strong>${esc(unit.reference)}</strong></td>${hasFloor ? `
                <td data-label="${t('availability.floor', locale)}">${esc(localizedUnitFloor(unit.floor, locale))}</td>` : ''}
                <td data-label="${t('availability.bedrooms', locale)}">${esc(localizedUnitBedrooms(unit.bedrooms, locale))}</td>${hasSize ? `
                <td data-label="${t('availability.size', locale)}">${esc(localizedUnitSize(unit.size, locale))}</td>` : ''}
                <td data-label="${t('availability.price', locale)}"><strong>${esc(unit.price)}</strong></td>
                <td data-label="${t('availability.status', locale)}"><span class="availability-status">${t('availability.available', locale)}</span></td>${hasFloorplans ? `
                <td data-label="${t('availability.floorplan', locale)}">${unit.floorplan ? `<a class="availability-floorplan-link" href="${esc(unit.floorplan)}" target="_blank" rel="noopener">${t('availability.viewPdf', locale)}</a>` : ''}</td>` : ''}
              </tr>`;
  }).join('\n              ');

  return `<div class="availability-release reveal-soft">
          <div class="availability-release-stats" aria-label="${t('aria.currentReleaseSummary', locale)}">
            <div><span>${t('availability.availableHomes', locale)}</span><strong>${units.length}</strong></div>
            <div><span>${t('cinematic.startingPrice', locale)}</span><strong>${esc(availability.startingPrice || project.hero?.startingPrice || '')}</strong></div>
            <div><span>${t('availability.priceRange', locale)}</span><strong>${esc(availability.priceRange || '')}</strong></div>
            <div><span>${t('availability.checked', locale)}</span><strong>${esc(localizeMonthDate(availability.checkedDate, locale) || '')}</strong></div>
          </div>
          <details class="availability-disclosure">
            <summary>
              <span>${t('availability.viewAll', locale, { count: units.length })}</span>
              <span class="availability-summary-icon" aria-hidden="true">+</span>
            </summary>
            ${filters}
            ${cardGrid || `<div class="availability-table-wrap">
              <table class="availability-table">
                <caption class="sr-only">${t('availability.tableCaption', locale, { project: esc(project.name) })}</caption>
                <thead><tr><th scope="col">${t('availability.reference', locale)}</th>${hasFloor ? `<th scope="col">${t('availability.floor', locale)}</th>` : ''}<th scope="col">${t('availability.bedrooms', locale)}</th>${hasSize ? `<th scope="col">${t('availability.size', locale)}</th>` : ''}<th scope="col">${t('availability.price', locale)}</th><th scope="col">${t('availability.status', locale)}</th>${hasFloorplans ? `<th scope="col">${t('availability.floorplan', locale)}</th>` : ''}</tr></thead>
                <tbody>
              ${rows}
                </tbody>
              </table>
            </div>`}
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
  casares: { x: 60, y: 320, label: 'Casares' },
  estepona: { x: 150, y: 295, label: 'Estepona' },
  newGoldenMile: { x: 310, y: 278, label: 'New Golden Mile', key: 'map.newGoldenMile' },
  sanPedro: { x: 420, y: 268, label: 'San Pedro' },
  benahavis: { x: 460, y: 145, label: 'Benahávis' },
  puertoBanus: { x: 560, y: 255, label: 'Puerto Banús' },
  nuevaAndalucia: { x: 600, y: 165, label: 'Nueva Andalucía' },
  goldenMile: { x: 680, y: 233, label: 'Golden Mile', key: 'map.goldenMile' },
  marbellaCentre: { x: 800, y: 218, label: 'Marbella Centre', key: 'map.marbellaCentre' },
  marbellaEast: { x: 950, y: 195, label: 'Marbella East', key: 'map.marbellaEast' },
  malagaAirport: { x: 1080, y: 165, label: 'Málaga Airport', key: 'map.malagaAirport' }
};

function mapLandmarkLabel(point, locale) {
  return point.key ? t(point.key, locale) : point.label;
}

// Context landmarks shown on every map for orientation, unless the
// project's own marker sits on (or very close to) one of them.
const MAP_CONTEXT_ORDER = ['estepona', 'puertoBanus', 'marbellaCentre', 'malagaAirport'];

// Below this pixel distance (in the map's 1200x620 coordinate space) a
// context dot's label would overlap the main project marker's glow and
// label, so it's dropped instead of rendered on top of it.
const MAP_CONTEXT_MIN_DISTANCE = 170;

function mapDistance(a, b) {
  return Math.hypot(a.x - b.x, a.y - b.y);
}

function resolveMapArea(project) {
  const key = project.location?.mapArea;
  if (key && MAP_LANDMARKS[key]) return key;
  return 'marbellaCentre';
}

// The second map label line falls back to hero.location when mapLabelHtml
// carries no <br>. For a project whose label already reads "Area, Town"
// that fallback is the *same* string, which rendered the location twice
// under the marker. Drop the second line when it repeats the first.
function sameMapLine(a, b) {
  const norm = (value) => String(value).toLowerCase().replace(/[\s,._-]+/g, ' ').trim();
  return norm(a) === norm(b);
}

function locationMap(project, locale = DEFAULT_LOCALE) {
  const [mapLineOne = project.name, mapLineTwoRaw = project.hero?.location || 'Costa del Sol'] = mapLabelLines(project.location?.mapLabelHtml);
  const mapLineTwo = sameMapLine(mapLineOne, mapLineTwoRaw) ? '' : mapLineTwoRaw;
  const titleId = `${project.slug}-map-title`;
  const descId = `${project.slug}-map-desc`;

  const areaKey = resolveMapArea(project);
  const marker = MAP_LANDMARKS[areaKey];
  const context = MAP_CONTEXT_ORDER
    .filter((key) => key !== areaKey)
    .filter((key) => mapDistance(MAP_LANDMARKS[key], marker) >= MAP_CONTEXT_MIN_DISTANCE)
    .slice(0, 3);
  const contextNodes = context.map((key, index) => {
    const point = MAP_LANDMARKS[key];
    const muted = index !== 0;
    const anchorEnd = point.x > marker.x;
    return `<g class="map-node${muted ? ' map-node-muted' : ''}" transform="translate(${point.x} ${point.y})">
                <circle r="${muted ? 5 : 6}"/>
                <text x="${anchorEnd ? -12 : 16}" y="${muted ? 4 : -18}"${anchorEnd ? ' text-anchor="end"' : ''}>${esc(mapLandmarkLabel(point, locale))}</text>
              </g>`;
  }).join('\n              ');

  return `<div class="location-map-card">
            <svg class="location-map-svg" viewBox="0 0 1200 620" role="img" aria-labelledby="${esc(titleId)} ${esc(descId)}" focusable="false">
              <title id="${esc(titleId)}">${esc(project.name)} location map</title>
              <desc id="${esc(descId)}">Indicative map showing ${esc(project.name)} in ${esc(project.hero?.location || project.location?.mapLabelHtml || 'Costa del Sol')}, relative to ${context.map((key) => esc(mapLandmarkLabel(MAP_LANDMARKS[key], locale))).join(', ')}.</desc>
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
              <text x="850" y="248" class="map-road-label">${esc(t('map.a7CoastRoad', locale))}</text>
              ${contextNodes}
              <g class="map-marker" transform="translate(${marker.x} ${marker.y})" filter="url(#mapSoftShadow)">
                <circle class="map-marker-glow" r="58"/>
                <circle class="map-marker-disc" r="34"/>
                <circle class="map-marker-dot" r="5"/>
              </g>
              <text class="map-project-label" x="${marker.x}" y="${marker.y + 62}" text-anchor="middle">
                <tspan x="${marker.x}">${esc(mapLineOne)}</tspan>${mapLineTwo ? `
                <tspan x="${marker.x}" dy="18">${esc(mapLineTwo)}</tspan>` : ''}
              </text>
              <text class="map-water-label" x="150" y="502">${esc(t('map.mediterraneanSea', locale))}</text>
              <text class="map-note" x="60" y="52">${esc(t('map.indicativeLocation', locale))}</text>
            </svg>
            <div class="map-legend" aria-hidden="true">
              <span><i class="legend-pin"></i> ${esc(t('map.legendProjectArea', locale))}</span>
              <span><i class="legend-road"></i> ${esc(t('map.legendCoastalAccess', locale))}</span>
              <span><i class="legend-sea"></i> ${esc(t('map.legendMediterranean', locale))}</span>
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

const NEXT_STEPS_ICONS = [
  '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>',
  '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="7" height="16" rx="1"/><rect x="14" y="4" width="7" height="16" rx="1"/></svg>',
  '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7-11-7-11-7z"/><circle cx="12" cy="12" r="3"/></svg>',
  '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11.5 14.5 15.5 9.5"/></svg>',
];

function renderTimelineItems(items = []) {
  return items.map(([step, title, body], index) => `<article class="timeline-item reveal-soft">
            <span class="timeline-hex">${NEXT_STEPS_ICONS[index % NEXT_STEPS_ICONS.length]}</span>
            <span class="timeline-num">${esc(step)}</span>
            <h3>${esc(title)}</h3>
            <p>${esc(body)}</p>
          </article>`).join('\n          ');
}

function nav(project, locale = DEFAULT_LOCALE) {
  const p = rootPrefix(locale);
  const outputPath = project?.output || 'developments.html';
  const switcher = renderLanguageSwitcher(outputPath, locale);
  return `<nav class="site-nav">
    <div class="nav-links nav-links-left">
      <a href="${p}${localizedPath('guides.html', locale)}">${t('nav.buyingGuides', locale)}</a>
      <a href="${p}${localizedPath('why-nueva.html', locale)}">${t('nav.whyNueva', locale)}</a>
      <a href="${p}${localizedPath('developments.html', locale)}">${t('nav.developments', locale)}</a>
    </div>
    <a class="nav-logo" href="${p}${localizedPath('index.html', locale)}" aria-label="${t('nav.home', locale)}">
      <img src="${p}assets/liora/brand/nueva-living-hero-logo-transparent.png?v=7" alt="Nueva Living" width="420" height="100">
    </a>
    <div class="nav-links nav-links-right">
      <a href="${p}${localizedPath('areas.html', locale)}">${t('nav.areas', locale)}</a>
      <a href="${p}${localizedPath('advisory.html', locale)}">${t('nav.advisory', locale)}</a>
      <a href="${p}${localizedPath('contact.html', locale)}">${t('nav.contactUs', locale)}</a>
      ${switcher}
    </div>
    <button class="nav-burger" type="button" aria-label="${t('nav.menu', locale)}" aria-controls="mobileMenu" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
  </nav>

  <div class="mobile-menu" id="mobileMenu">
    <a href="${p}${localizedPath('guides.html', locale)}">${t('nav.buyingGuides', locale)}</a>
    <a href="${p}${localizedPath('why-nueva.html', locale)}">${t('nav.whyNueva', locale)}</a>
    <a href="${p}${localizedPath('developments.html', locale)}">${t('nav.developments', locale)}</a>
    <a href="${p}${localizedPath('areas.html', locale)}">${t('nav.areas', locale)}</a>
    <a href="${p}${localizedPath('advisory.html', locale)}">${t('nav.advisory', locale)}</a>
    <a href="${p}${localizedPath('contact.html', locale)}">${t('nav.contactUs', locale)}</a>
    ${renderLanguageSwitcher(outputPath, locale)}
  </div>`;
}

function projectArea(project, locale = DEFAULT_LOCALE) {
  const location = `${project.hero?.location || ''} ${project.schema?.areaServed || ''}`.toLowerCase();
  if (location.includes('nueva andaluc') || location.includes('nueva andalucía')) {
    return { label: t('area.nuevaAndalucia', locale), href: 'area-nueva-andalucia.html' };
  }
  if (location.includes('benahav')) {
    return { label: t('area.benahavis', locale), href: 'area-benahavis.html' };
  }
  if (location.includes('estepona') || location.includes('new golden mile')) {
    return { label: t('area.estepona', locale), href: 'area-estepona.html' };
  }
  if (location.includes('mijas') || location.includes('fuengirola')) {
    return { label: t('area.mijasFuengirola', locale), href: 'area-mijas-fuengirola.html' };
  }
  // Casares has no area page of its own; it sits west of Estepona and belongs
  // with that page. Without this branch it fell through to the Marbella default
  // and a Casares project was breadcrumbed, titled and schema-tagged as Marbella.
  if (location.includes('casares')) {
    return { label: t('area.casares', locale), href: 'area-estepona.html' };
  }
  if (location.includes('marbella east')) {
    return { label: t('area.marbellaEast', locale), href: 'area-marbella.html' };
  }
  return { label: t('area.marbella', locale), href: 'area-marbella.html' };
}

function breadcrumb(project, locale = DEFAULT_LOCALE) {
  const area = projectArea(project, locale);
  const p = rootPrefix(locale);
  return `<nav class="breadcrumb-bar" aria-label="Breadcrumb">
    <ol class="breadcrumb-list">
      <li><a href="${p}${localizedPath('developments.html', locale)}">${t('breadcrumb.developments', locale)}</a></li>
      <li><a href="${p}${localizedPath(area.href, locale)}">${area.label}</a></li>
      <li><span aria-current="page">${esc(project.shortName || project.name)}</span></li>
    </ol>
  </nav>`;
}

function breadcrumbSchema(project, locale = DEFAULT_LOCALE) {
  const area = projectArea(project, locale);
  const p = localeMeta(locale).urlPrefix ? `${localeMeta(locale).urlPrefix}/` : '';
  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      { '@type': 'ListItem', position: 1, name: t('breadcrumb.developments', locale), item: `${siteUrl}/${p}developments.html` },
      { '@type': 'ListItem', position: 2, name: area.label, item: `${siteUrl}/${p}${area.href}` },
      { '@type': 'ListItem', position: 3, name: project.shortName || project.name, item: `${siteUrl}/${p}${project.output}` }
    ]
  };
}

// Search-facing title/meta lead with property type and area, since those
// are what buyers actually search for -- not the project's own name.
// Search results truncate around 60 characters. The full template ends
// with a " | Nueva Living" brand suffix, which on the longer property
// names -- especially in German and Russian -- pushed the part that
// actually earns the click past the cut. Drop the brand suffix when the
// title would overrun; the descriptive half is worth more than the brand,
// which already appears in the URL and breadcrumb.
const SEO_TITLE_MAX = 60;
const BRAND_SUFFIX = ' | Nueva Living';

function seoTitle(project, locale = DEFAULT_LOCALE) {
  const area = projectArea(project, locale);
  const type = project.hero?.type || 'New Development';
  const build = (t2) => t('seo.titleTemplate', locale, { type: t2, area: area.label, name: project.shortName || project.name });

  const full = build(type);
  if (full.length <= SEO_TITLE_MAX) return full;

  // First give up the brand suffix, which the domain already conveys.
  const withoutBrand = full.endsWith(BRAND_SUFFIX) ? full.slice(0, -BRAND_SUFFIX.length) : full;
  if (withoutBrand.length <= SEO_TITLE_MAX) return withoutBrand;

  // Still long: these run over because the property type is a list --
  // "Wohnungen, Penthäuser & Gartenvillen" is 36 characters before the area
  // and the project name. Keep the first type; the rest is on the page. The
  // separator is whatever the language uses to join a list, so the
  // conjunctions are listed alongside the punctuation.
  const firstType = type.split(/\s*[,&]\s*|\s+(?:&|and|y|et|und|и|و)\s+/i)[0].trim();
  const strip = (value) => (value.endsWith(BRAND_SUFFIX) && value.length > SEO_TITLE_MAX
    ? value.slice(0, -BRAND_SUFFIX.length)
    : value);

  if (firstType && firstType !== type) {
    const trimmed = strip(build(firstType));
    if (trimmed.length <= SEO_TITLE_MAX) return trimmed;
  }

  // Last resort: when the project name already carries the place -- "Marbella
  // West Gardens" in Marbella -- naming the area again buys nothing but
  // characters.
  //
  // The comparison uses the area slug, not the translated label: the project
  // names stay in Latin script, so "Marbella West Gardens" never matches
  // "Марбелья" or "ماربيا" and the Russian and Arabic titles kept overrunning.
  const name = project.shortName || project.name;
  const areaSlug = String(project.discovery?.area || '').split('-')[0];
  const redundant = (areaSlug && name.toLowerCase().includes(areaSlug.toLowerCase()))
    || (area.label && name.toLowerCase().includes(String(area.label).toLowerCase().split(/[\s(]/)[0]));
  if (redundant) {
    const withoutArea = `${firstType || type} — ${name}${BRAND_SUFFIX}`;
    const trimmed = strip(withoutArea);
    if (trimmed.length <= SEO_TITLE_MAX) return trimmed;
  }
  return withoutBrand;
}

function footer(project, locale = DEFAULT_LOCALE) {
  const p = rootPrefix(locale);
  return `<footer>
    <div class="footer-grid">
      <div>
        <img class="footer-logo" src="${p}assets/liora/brand/nueva-living-lockup-espresso-transparent.png?v=7" alt="Nueva Living" width="700" height="340" loading="lazy" decoding="async">
        <p class="footer-about">${t('footer.about.text', locale)}</p>
      </div>
      <div class="footer-col">
        <div class="footer-col-title">${t('footer.companyTitle', locale)}</div>
        <ul>
          <li><a href="${p}${localizedPath('why-nueva.html', locale)}">${t('footer.whyNuevaLiving', locale)}</a></li>
          <li><a href="${p}${localizedPath('about.html', locale)}">${t('footer.about', locale)}</a></li>
          <li><a href="${p}${localizedPath('advisory.html', locale)}">${t('footer.advisory', locale)}</a></li>
          <li><a href="${p}${localizedPath('referrals.html', locale)}">${t('footer.referralProgram', locale)}</a></li>
          <li><a href="${p}${localizedPath('contact.html', locale)}">${t('footer.contactUs', locale)}</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <div class="footer-col-title">${t('footer.projectsTitle', locale)}</div>
        <ul>
          <li><a href="${p}${localizedPath('developments.html', locale)}">${t('footer.allDevelopments', locale)}</a></li>
          <li><a href="${p}${localizedPath(project.output, locale)}">${esc(project.shortName || project.name)}</a></li>
          <li><a href="${p}${localizedPath('guides.html', locale)}">${t('footer.buyingGuides', locale)}</a></li>
          <li><a href="${p}${localizedPath('areas.html', locale)}">${t('footer.areasOverview', locale)}</a></li>
          <li><a href="${p}${localizedPath('area-marbella.html', locale)}">${t('area.marbella', locale)}</a></li>
          <li><a href="${p}${localizedPath('area-estepona.html', locale)}">${t('area.estepona', locale)}</a></li>
          <li><a href="${p}${localizedPath('area-benahavis.html', locale)}">${t('area.benahavis', locale)}</a></li>
          <li><a href="${p}${localizedPath('area-nueva-andalucia.html', locale)}">${t('area.nuevaAndalucia', locale)}</a></li>
          <li><a href="${p}${localizedPath('area-mijas-fuengirola.html', locale)}">${t('area.mijasFuengirola', locale)}</a></li>
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
          <li><a href="${p}${localizedPath('privacy-policy.html', locale)}">${t('footer.privacyPolicy', locale)}</a></li>
          <li><a href="${p}${localizedPath('legal-notice.html', locale)}">${t('footer.legalNotice', locale)}</a></li>
          <li><a href="${p}${localizedPath('cookie-policy.html', locale)}">${t('footer.cookiePolicy', locale)}</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>${t('footer.disclaimer', locale)}</p>
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

function renderConstructionTimeline(project, locale = DEFAULT_LOCALE) {
  const timeline = project.constructionTimeline;
  if (!timeline || !Array.isArray(timeline.points) || !timeline.points.length) return '';

  const points = timeline.points.map((point, index) => `
        <div class="timeline-point${point.milestone ? ' is-milestone' : ''}" style="transition-delay:${(index * 0.09).toFixed(2)}s">
          <span class="timeline-label">${point.milestone && point.label ? esc(point.label) : ''}</span>
          <span class="timeline-marker">${point.milestone ? `<span class="timeline-marker-ring"></span><span class="timeline-marker-core">${TIMELINE_ICONS[point.icon] || TIMELINE_ICONS.leaf}</span>` : ''}</span>
          <span class="timeline-year">${esc(point.year || '')}</span>
        </div>`).join('');

  const paymentTerms = Array.isArray(timeline.paymentTerms) ? timeline.paymentTerms : [];

  let runningPercent = 0;
  const percentTotal = paymentTerms.reduce((sum, [, value]) => {
    const match = /^([\d.]+)%/.exec(String(value).trim());
    return match ? sum + parseFloat(match[1]) : sum;
  }, 0);
  const fixedAmount = paymentTerms.find(([, value]) => !/%/.test(String(value)));

  return `    <section class="project-section construction-timeline-section" id="construction-timeline">
      <div class="project-inner timeline-head reveal-soft">
        <div>
          <span class="section-kicker">${esc(timeline.kicker || t('timeline.timeline', locale))}</span>
          <div class="rule"></div>
          <h2 class="section-headline">${timeline.headlineHtml || `${esc(timeline.kicker || t('timeline.timeline', locale))} of <em>delivery</em>`}</h2>
        </div>
        ${timeline.copy ? `<p class="project-lead timeline-intro">${esc(timeline.copy)}</p>` : ''}
      </div>
      <div class="project-inner timeline-track reveal-soft">${points}
      </div>
${paymentTerms.length ? `      <div class="project-inner timeline-payment-terms reveal-soft">
        <div class="timeline-payment-heading">
          <span class="timeline-payment-kicker">${esc(timeline.paymentTermsLabel || t('timeline.paymentTerms', locale))}</span>
          ${percentTotal ? `<span class="timeline-payment-total">${esc(t(fixedAmount ? 'timeline.paymentSummaryWithReservation' : 'timeline.paymentSummary', locale, {
            amount: fixedAmount ? fixedAmount[1] : '',
            percent: percentTotal % 1 === 0 ? percentTotal : percentTotal.toFixed(1),
            count: paymentTerms.length - (fixedAmount ? 1 : 0)
          }))}</span>` : ''}
        </div>
        <div class="timeline-payment-grid">
          ${paymentTerms.map(([label, value, note], index) => {
            const match = /^([\d.]+)%/.exec(String(value).trim());
            if (match) runningPercent += parseFloat(match[1]);
            const runningLabel = match ? t('timeline.runningTotal', locale, { percent: runningPercent % 1 === 0 ? runningPercent : runningPercent.toFixed(1) }) : '';
            return `<div class="timeline-payment-item">
            <span class="timeline-payment-index">${String(index + 1).padStart(2, '0')}</span>
            <span class="timeline-payment-label">${esc(label)}</span>
            <strong class="timeline-payment-value">${esc(value)}</strong>
            ${note ? `<span class="timeline-payment-note">${esc(note)}</span>` : ''}
            ${runningLabel ? `<span class="timeline-payment-running">${esc(runningLabel)}</span>` : ''}
          </div>`;
          }).join('\n          ')}
        </div>
        ${timeline.paymentTermsNote ? `<p class="timeline-payment-disclaimer">${esc(timeline.paymentTermsNote)}</p>` : ''}
      </div>
` : ''}    </section>

`;
}

function renderProject(sourceProject, locale = DEFAULT_LOCALE) {
  const project = localizeProject(sourceProject, locale);
  const rtl = isRtl(locale);
  const p = rootPrefix(locale);
  const heroImage = image(project, 'hero');
  const architectureImage = image(project, 'architecture');
  const privateImage = image(project, 'privateViewing');
  const lifestyleImage = image(project, 'lifestyle');
  const privateHrefRaw = project.privateViewing?.href || 'index.html?private-viewing=1';
  const privateHref = locale === DEFAULT_LOCALE
    ? privateHrefRaw
    : privateHrefRaw.replace(/^index\.html/, localizedPath('index.html', locale));
  // A project only gets the real map once its plot coordinate has been routed
  // by build_location_maps.mjs. Until then it keeps the stylised SVG map, so
  // this cannot blank out the location section on a project without geo data.
  const liveLocationMap = hasLiveLocationMap(project.slug);
  const privateHeroCta = project.privateViewing?.heroCta || t('cta.cinematicPresentation', locale);
  const privateCta = project.privateViewing?.ctaLabel || t('cta.cinematicPresentation', locale);
  const projectMedia = renderProjectMedia(project, locale);
  const constructionTimeline = renderConstructionTimeline(project, locale);
  const availabilityRelease = renderAvailabilityRelease(project, locale);
  const hasPublishedAvailability = Boolean(project.availability?.units?.length);
  const hasFloorplans = Boolean(project.availability?.units?.some((unit) => unit.floorplan));
  const availabilityBrowseAction = hasPublishedAvailability
    ? actionLink(t('cta.viewAvailableHomes', locale), '#availability')
    : actionLink(t('common.onRequest', locale));
  const availabilityEnquiryAction = actionLink(
    hasPublishedAvailability ? t('cta.askAboutAHome', locale) : t('common.onRequest', locale)
  );
  const facts = [
    [t('common.location', locale), project.hero.location],
    [t('cinematic.startingPrice', locale), project.hero.startingPrice],
    [t('common.propertyType', locale), project.hero.type],
    [t('common.delivery', locale), project.hero.delivery]
  ];
  const quickFactItems = mergedProjectFacts(project, sourceProject);
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
  // Same entity facts as every other page, from lib/brand.mjs. These used
  // to be written out again here and had already lost the address, phone
  // and logo -- Google reads structured data as an assertion about the
  // business, and 84 pages asserting a thinner version of it is worse than
  // one consistent claim.
  const agentSchema = realEstateAgentSchema(siteUrl, { areaServed: 'Costa del Sol' });
  const faqs = [...defaultFaqs(locale), ...(project.faq || [])];
  const faqSchema = {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: faqs.map(([question, answer]) => ({
      '@type': 'Question',
      name: question,
      acceptedAnswer: { '@type': 'Answer', text: answer }
    }))
  };
  const pageTitle = seoTitle(project, locale);
  const localeMetaInfo = localeMeta(locale);
  const canonicalHref = project.canonical
    ? (locale === DEFAULT_LOCALE ? project.canonical : project.canonical.replace('nuevaliving.com/', `nuevaliving.com/${localeMetaInfo.urlPrefix}/`))
    : '';

  return `<!doctype html>
<html lang="${localeMetaInfo.htmlLang}" dir="${localeMetaInfo.dir}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
${baseHrefTag(locale)}  <title>${esc(pageTitle)}</title>
  <meta name="description" content="${esc(project.seoDescription || project.description)}">
  <link rel="canonical" href="${esc(canonicalHref)}">
${hreflangLinks(sourceProject.output, siteUrl)}
  <meta property="og:title" content="${esc(pageTitle)}">
  <meta property="og:description" content="${esc(project.description)}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="${esc(canonicalHref)}">
  <meta property="og:locale" content="${localeMetaInfo.htmlLang}">
  <meta property="og:image" content="${esc(assetUrl(heroImage.src))}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="${esc(pageTitle)}">
  <meta name="twitter:description" content="${esc(project.twitterDescription || project.description)}">
  <meta name="twitter:image" content="${esc(assetUrl(heroImage.src))}">
  <link rel="icon" href="${p}assets/liora/liora-favicon-512.png?v=6" type="image/png" sizes="512x512">
  <link rel="icon" href="${p}assets/liora/favicon-32.png?v=6" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="${p}assets/liora/apple-touch-icon.png?v=6" sizes="180x180">
${fontPreloadBlock(p, locale)}
  <link rel="stylesheet" href="${p}assets/fonts/google/liora-fonts.css">
  <link rel="stylesheet" href="${p}assets/liora/liora-pages.css?v=9">
  <link rel="stylesheet" href="${p}assets/liora/liora-property.css?v=${propertyCssVersion}">${rtl ? `
  <link rel="stylesheet" href="${p}assets/liora/liora-rtl.css?v=${rtlCssVersion}">` : ''}${liveLocationMap ? `
  <link rel="stylesheet" href="${p}assets/liora/nueva-location-map.css?v=${locationMapCssVersion}">
${leafletHead()}
  <script src="${p}assets/liora/nueva-location-map.js?v=${locationMapJsVersion}" defer></script>` : ''}
  <script src="${p}assets/liora/liora-property.js?v=${propertyJsVersion}" defer></script>
  <script src="${p}assets/liora/liora-calculator.js?v=${calculatorJsVersion}" defer></script>
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
${JSON.stringify(breadcrumbSchema(project, locale), null, 2)}
  </script>
</head>
<body
  data-locale="${locale}"
  data-project-name="${esc(project.name)}"
  data-project-message="${esc(project.enquiry.message)}"
  data-project-sent-message="${esc(project.enquiry.sentMessage)}"
>
  ${nav(project, locale)}
  ${breadcrumb(project, locale)}

  <main>
    <section class="project-hero" id="top">
      ${pictureTag(heroImage, 'project-hero-img', '', { priority: true, sizes: '100vw' })}
      <div class="project-hero-inner">
        <div class="hero-copy reveal-soft">
          <span class="project-eyebrow">${esc(project.hero.eyebrow)}</span>
          <h1 class="hero-title">${project.titleHtml}</h1>
          <p class="hero-positioning">${esc(project.description)}</p>
          <div class="hero-actions">
            ${availabilityBrowseAction}
            ${ghostAction(privateHeroCta, privateHref)}
            ${project.media?.items?.length ? ghostAction(t('cta.allImages', locale), '#media') : ''}
          </div>
        </div>
        <aside class="hero-facts reveal-soft" aria-label="${t('aria.projectKeyFacts', locale)}">
          ${facts.map(([label, value]) => `<div class="hero-fact"><span>${esc(label)}</span><strong>${esc(value)}</strong></div>`).join('\n          ')}
        </aside>
      </div>
    </section>

    <nav class="project-nav" aria-label="${t('aria.projectSections', locale)}">
      <div class="project-nav-inner">
        <a href="#overview">${t('navInPage.overview', locale)}</a>
${project.media?.items?.length ? `        <a href="#media">${t('navInPage.media', locale)}</a>\n` : ''}        <a href="#location">${t('navInPage.location', locale)}</a>
${constructionTimeline ? `        <a href="#construction-timeline">${t('timeline.paymentTerms', locale)}</a>\n` : ''}        <a href="#residences">${t('navInPage.residences', locale)}</a>
        <a href="#availability">${t('navInPage.availability', locale)}</a>
        <a href="#calculator">${t('navInPage.affordability', locale)}</a>
        <a href="#why-this-project">${t('navInPage.why', locale)}</a>
        <a href="#architecture">${t('navInPage.architecture', locale)}</a>
        <a href="#project-file">${t('navInPage.projectInfo', locale)}</a>
        <a href="#private-viewing">${t('cta.cinematicPresentation', locale)}</a>
        <a href="#lifestyle">${t('navInPage.lifestyle', locale)}</a>
        <a href="#faq">${t('navInPage.faq', locale)}</a>
        <a href="#enquire">${t('navInPage.enquire', locale)}</a>
      </div>
    </nav>

    <section class="quick-facts-band" aria-label="${t('aria.projectQuickFacts', locale)}">
      <div class="project-inner quick-facts-shell reveal-soft">
        <div class="quick-facts-grid">
          ${quickFactItems.map(([label, value]) => `<div class="quick-fact"><span>${esc(label)}</span><strong>${esc(value)}</strong></div>`).join('\n          ')}
        </div>
        <div class="quick-facts-actions">
${hasPublishedAvailability ? '' : `          ${availabilityBrowseAction}\n`}          ${ghostAction(t('cta.requestProjectMaterial', locale))}
        </div>
      </div>
    </section>

    <section class="project-section" id="overview">
      <div class="project-inner overview-grid overview-grid--prose">
        <div class="reveal-soft">
          <span class="section-kicker">${t('section.overview', locale)}</span>
          <div class="rule"></div>
          <h2 class="section-headline">${project.overview.headlineHtml}</h2>
          ${project.overview.copy.map((item) => `<p class="project-lead">${esc(item)}</p>`).join('\n          ')}
        </div>
      </div>
    </section>

${projectMedia.section ? `    ${projectMedia.section}\n\n` : ''}    <section class="project-section" id="location">
      <div class="project-inner${liveLocationMap ? ' location-stack' : ' location-layout'}">
        <div class="reveal-soft">
          <span class="section-kicker">${t('section.location', locale)}</span>
          <div class="rule"></div>
          <h2 class="section-headline">${project.location.headlineHtml}</h2>
          <p class="project-lead">${esc(project.location.copy)}</p>${liveLocationMap ? '' : `
          <div class="distance-grid" style="margin-top:32px;">
            ${pairs(project.location.distances, 'distance')}
          </div>`}
        </div>${liveLocationMap ? `
        <div class="reveal-soft">${renderLocationCard(project, locale)}
        </div>` : `
        <div class="map-panel reveal-soft" aria-label="${t('aria.indicativeLocationMap', locale, { name: esc(project.name) })}">
          ${locationMap(project, locale)}
        </div>`}
      </div>
    </section>

${constructionTimeline}    <section class="project-section" id="residences">
      <div class="project-inner">
        <div class="reveal-soft">
          <span class="section-kicker">${t('section.residences', locale)}</span>
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
              ? `<a class="btn ghost project-btn" href="#availability">${t('cta.viewFloorplans', locale)}</a>`
              : `<a class="btn ghost project-btn" href="#enquire" data-prefill>${t('cta.requestFloorplans', locale)}</a>`}
          </article>`).join('\n          ')}
        </div>
        <div class="inline-cta-panel reveal-soft">
          <div>
            <span class="fine-label">${t('label.privateMaterial', locale)}</span>
            <p>${t('copy.privateMaterialNote', locale)}</p>
          </div>
          <div class="inline-cta-actions">
${hasPublishedAvailability ? '' : `            ${availabilityBrowseAction}\n`}            ${ghostAction(t('cta.viewFloorplans', locale), hasFloorplans ? '#availability' : '#enquire')}
          </div>
        </div>
      </div>
    </section>

    <section class="project-section" id="availability">
      <div class="project-inner">
        <div class="section-head reveal-soft">
          <span class="section-kicker">${t('section.availability', locale)}</span>
          <div class="rule"></div>
          <h2 class="section-headline">${project.availability.headlineHtml}</h2>
          <p class="project-lead">${esc(project.availability.copy)}</p>
        </div>${project.availability.image ? `
        <figure class="project-plan reveal-soft">
          ${imageTag(project.availability.image)}
          ${project.availability.image.caption ? `<figcaption>${esc(project.availability.image.caption)}</figcaption>` : ''}
        </figure>` : ''}
${availabilityRelease ? `        ${availabilityRelease}\n` : ''}        <div class="availability-panel availability-panel--followup reveal-soft">
          <div class="availability-actions">
            ${availabilityEnquiryAction}
            ${advisorAction(project, t('cta.speakWithAdvisor', locale))}
          </div>
        </div>
      </div>
    </section>

    <section class="project-section calculator-section" id="calculator">
      <div class="project-inner">
        <div class="section-head center reveal-soft">
          <span class="section-kicker">${t('section.affordability', locale)}</span>
          <div class="rule"></div>
          <h2 class="section-headline">${t('calculator.headlineHtml', locale)}</h2>
          <p class="body-copy">${t('calculator.intro', locale)}</p>
        </div>
        <div class="calculator-panel reveal-soft" data-calculator>
          <div class="calculator-inputs">
            <div class="calculator-field calculator-field--dual">
              <div class="calculator-field-label"><span>${t('calculator.purchasePrice', locale)}</span><em data-calc-price-readout>&euro;0</em></div>
              <input type="range" data-calc-price-range min="150000" max="3000000" step="5000" value="${esc(calculatorSeedPrice)}">
              <input type="number" data-calc-price value="${esc(calculatorSeedPrice)}" min="0" step="1000" class="calculator-field-number">
            </div>
            <div class="calculator-field calculator-field--dual">
              <div class="calculator-field-label"><span>${t('calculator.deposit', locale)}</span><em data-calc-deposit-readout>30% &middot; &euro;0</em></div>
              <input type="range" data-calc-deposit min="10" max="100" step="5" value="30">
              <em class="calculator-field-hint">${t('calculator.depositHint', locale)}</em>
            </div>
            <div class="calculator-field calculator-field--dual">
              <div class="calculator-field-label"><span>${t('calculator.mortgageTerm', locale)}</span><em data-calc-term-readout>25 ${t('common.years', locale)}</em></div>
              <input type="range" data-calc-term min="5" max="35" step="1" value="25">
            </div>
            <div class="calculator-field calculator-field--split">
              <label>
                <span>${t('calculator.interestRate', locale)}</span>
                <div class="calculator-input-suffix">
                  <input type="number" data-calc-rate value="3.2" min="0" max="15" step="0.1">
                  <span class="calculator-input-suffix-label">%</span>
                </div>
              </label>
              <div class="calculator-rate-toggle" data-calc-rate-toggle role="group" aria-label="${t('calculator.rateType', locale)}">
                <button type="button" class="is-active" data-rate-type="fixed">${t('calculator.fixed', locale)}</button>
                <button type="button" data-rate-type="variable">${t('calculator.variable', locale)}</button>
              </div>
            </div>
            <label class="calculator-field">
              <span>${t('calculator.taxesAndCosts', locale)}</span>
              <div class="calculator-input-suffix">
                <input type="number" data-calc-costs value="10" min="0" max="20" step="0.5">
                <span class="calculator-input-suffix-label">%</span>
              </div>
              <em class="calculator-field-hint">${t('calculator.taxesHint', locale)}</em>
            </label>
          </div>
          <div class="calculator-results">
            <div class="calculator-result calculator-result--highlight"><span>${t('calculator.estimatedMonthly', locale)}</span><strong data-calc-monthly>&euro;0</strong></div>
            <div class="calculator-result calculator-result--secondary"><span>${t('calculator.cashWithoutMortgage', locale)}</span><strong data-calc-total-property>&euro;0</strong></div>
            <div class="calculator-result calculator-result--secondary"><span>${t('calculator.cashWithMortgage', locale)}</span><strong data-calc-cash-with-mortgage>&euro;0</strong></div>
            <div class="calculator-breakdown-bar" data-calc-bar>
              <span class="calculator-bar-segment calculator-bar-segment--deposit" data-calc-bar-deposit></span>
              <span class="calculator-bar-segment calculator-bar-segment--principal" data-calc-bar-principal></span>
              <span class="calculator-bar-segment calculator-bar-segment--interest" data-calc-bar-interest></span>
            </div>
            <div class="calculator-bar-legend">
              <span><i class="calculator-bar-segment--deposit"></i>${t('calculator.deposit', locale)}</span>
              <span><i class="calculator-bar-segment--principal"></i>${t('calculator.legendPrincipal', locale)}</span>
              <span><i class="calculator-bar-segment--interest"></i>${t('calculator.legendInterest', locale)}</span>
            </div>
            <div class="calculator-result-grid">
              <div class="calculator-result"><span>${t('calculator.deposit', locale)}</span><strong data-calc-deposit-amount>&euro;0</strong></div>
              <div class="calculator-result"><span>${t('calculator.resultLoan', locale)}</span><strong data-calc-loan>&euro;0</strong></div>
              <div class="calculator-result"><span>${t('calculator.resultFinanced', locale)}</span><strong data-calc-financed-pct>0%</strong></div>
              <div class="calculator-result"><span>${t('calculator.resultTotalInterest', locale)}</span><strong data-calc-total-interest>&euro;0</strong></div>
              <div class="calculator-result"><span>${t('calculator.taxesAndCosts', locale)}</span><strong data-calc-costs-amount>&euro;0</strong></div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="project-section project-why" id="why-this-project">
      <div class="project-inner why-grid">
        <div class="reveal-soft">
          <span class="section-kicker">${t('section.why', locale)}</span>
          <div class="rule"></div>
          <h2 class="section-headline">${why.headlineHtml}</h2>
          <p class="project-lead">${esc(why.copy)}</p>
        </div>
        <div class="why-groups">
          <div class="why-group reveal-soft">
            <div class="why-group-head"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/></svg><h3>${t('why.whyItFits', locale)}</h3></div>
            <div class="why-point-grid">
              ${(why.points || []).map(([title, body]) => `<article class="why-point reveal-soft"><h3>${esc(title)}</h3><p>${esc(body)}</p></article>`).join('\n              ')}
            </div>
          </div>
          <div class="why-group reveal-soft">
            <div class="why-group-head"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="3 17 9 11 13 15 21 7"/><polyline points="15 7 21 7 21 13"/></svg><h3>${t('why.investmentCase', locale)}</h3></div>
            <div class="why-point-grid">
              ${(project.investment?.cards || []).map(([title, body]) => `<article class="why-point reveal-soft"><h3>${esc(title)}</h3><p>${esc(body)}</p></article>`).join('\n              ')}
            </div>
          </div>
          <div class="why-group reveal-soft">
            <div class="why-group-head"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11.5 14.5 15.5 9.5"/></svg><h3>${t('why.trustDiligence', locale)}</h3></div>
            <div class="why-point-grid">
              ${(trustDossier.cards || []).map(([title, body]) => `<article class="why-point reveal-soft"><h3>${esc(title)}</h3><p>${esc(body)}</p></article>`).join('\n              ')}
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="project-section dark" id="architecture">
      <div class="project-inner editorial-layout">
        <figure class="editorial-image reveal-soft">
          ${imageTag(architectureImage)}
          <figcaption class="image-caption">${esc(architectureImage.caption || t('architecture.previewFallback', locale))}</figcaption>
        </figure>
        <div class="editorial-copy reveal-soft">
          <span class="section-kicker">${t('section.architecture', locale)}</span>
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
          <span class="section-kicker">${t('section.projectFile', locale)}</span>
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
            <span class="section-kicker">${t('cta.cinematicPresentation', locale)}</span>
            <div class="rule"></div>
            <h2 class="section-headline">${project.privateViewing.headlineHtml}</h2>
            <p>${esc(project.privateViewing.copy)}</p>
            <div class="viewing-insights">
              ${(project.privateViewing.insights || []).map(([title, body]) => `<div><span>${esc(title)}</span><p>${esc(body)}</p></div>`).join('\n              ')}
            </div>
            <div class="cinema-actions">
              ${actionLink(privateCta, privateHref)}
              ${ghostAction(t('cta.requestProjectMaterial', locale))}
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="project-section dark" id="lifestyle">
      <div class="project-inner">
        <div class="cinema-cta reveal-soft">
          ${imageTag(lifestyleImage)}
          <div class="cinema-copy">
            <span class="section-kicker">${t('section.lifestyle', locale)}</span>
            <div class="rule"></div>
            <h2 class="section-headline">${project.lifestyle.headlineHtml}</h2>
            <p>${esc(project.lifestyle.copy)}</p>
          </div>
        </div>
      </div>
    </section>

    <section class="project-section timeline-section" id="timeline">
      <div class="project-inner">
        <div class="section-head center reveal-soft">
          <span class="section-kicker">${t('section.timeline', locale)}</span>
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
          <span class="section-kicker">${t('section.faq', locale)}</span>
          <div class="rule"></div>
          <h2 class="section-headline">${t('faq.headlineHtml', locale)}</h2>
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
          <span class="label">${t('section.enquireLabel', locale)}</span>
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
              <label for="f-first-name">${t('form.firstName', locale)}</label>
              <input id="f-first-name" name="first_name" type="text" autocomplete="given-name" placeholder="${t('form.firstName', locale)}" required>
            </div>
            <div class="field">
              <label for="f-last-name">${t('form.lastName', locale)}</label>
              <input id="f-last-name" name="last_name" type="text" autocomplete="family-name" placeholder="${t('form.lastName', locale)}" required>
            </div>
            <div class="field">
              <label for="f-email">${t('form.email', locale)}</label>
              <input id="f-email" name="email" type="email" autocomplete="email" placeholder="your@email.com" required>
            </div>
            <div class="field">
              <label for="f-phone">${t('form.phone', locale)}</label>
              <input id="f-phone" name="phone" type="tel" autocomplete="tel" placeholder="+34 or international">
            </div>
            <div class="field full">
              <label for="f-msg">${t('form.message', locale)}</label>
              <textarea id="f-msg" name="message">${esc(project.enquiry.message)}</textarea>
            </div>
            <label class="consent-row field full" for="f-consent">
              <input id="f-consent" name="consent" type="checkbox" required>
              <span>${t('form.consentContact', locale)}</span>
            </label>
            <label class="consent-row field full" for="f-marketing-opt-in">
              <input id="f-marketing-opt-in" name="marketing_opt_in" type="checkbox">
              <span>${t('form.consentMarketing', locale)}</span>
            </label>
          </div>
          <div class="form-submit" style="margin-top:26px;">
            <button type="submit" class="btn project-btn">${t('form.submitRequest', locale)}</button>
            <span class="form-note">${esc(project.enquiry.note)}</span>
          </div>
        </form>
      </div>
    </section>
  </main>

${projectMedia.dialog ? `  ${projectMedia.dialog}\n\n` : ''}  <div class="sticky-mobile-cta" aria-label="${t('aria.projectRequestActions', locale)}">
    <a href="#enquire" data-prefill>${hasPublishedAvailability ? t('cta.askAboutAHome', locale) : t('cta.requestAvailability', locale)}</a>
    <a href="${esc(whatsappHref(project))}" target="_blank" rel="noopener" data-whatsapp-advisor data-project="${esc(project.name)}" data-intent="speak with an advisor">${t('cta.speakWithAdvisor', locale)}</a>
  </div>

  ${footer(project, locale)}
  ${LANG_SWITCHER_SCRIPT}
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

export function loadProjects() {
  return projectFiles()
    .map((file) => ({ ...readJson(file), sourceFile: file }))
    .sort((a, b) => {
      const orderA = a.card?.order ?? 999;
      const orderB = b.card?.order ?? 999;
      return orderA === orderB ? a.name.localeCompare(b.name) : orderA - orderB;
    });
}

// Project cards sit one-per-row on phones, two across on tablets and
// three on desktop, so the rendered width never approaches the 1920px
// source.
const CARD_IMAGE_SIZES = '(max-width: 640px) 92vw, (max-width: 1100px) 46vw, 30vw';

// Media-grid tiles sit two-up on phones and four-up on desktop.
const MEDIA_TILE_SIZES = '(max-width: 640px) 46vw, (max-width: 1100px) 30vw, 23vw';

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

  const card = project.card || {};
  const badge = card.badge || titleCase(discovery.status || 'Current Release');
  const priceValue = (meta.find(([label]) => /^from$/i.test(label)) || [])[1]
    || project.hero?.startingPrice?.replace(/^From\s+/i, '')
    || 'On request';
  const dataAttrs = `${attr('data-title', project.name)}${attr('data-price', price)}${attr('data-completion', completion)}${attr('data-release', discovery.releaseDate)}${attr('data-priority', discovery.priority ?? project.card?.order ?? 999)}${attr('data-featured', discovery.featured ? 'true' : 'false')}${attr('data-area', discovery.area)}${discoveryAttr('data-property-types', propertyTypes)}${attr('data-status', crm.constructionStatus)}${attr('data-bedrooms-min', crm.bedroomsMin)}${attr('data-bedrooms-max', crm.bedroomsMax)}${discoveryAttr('data-tags', allTags)}${discoveryAttr('data-lifestyle', lifestyleTags)}${discoveryAttr('data-architecture', architectureTags)}${discoveryAttr('data-location', locationTags)}${discoveryAttr('data-investment', investmentTags)}${discoveryAttr('data-practical', practicalTags)}`;

  return '          ' + renderUnifiedCard({
    project,
    gallery: renderProjectCardGallery(project, { fallback: responsiveCardImageTag(cardImage(project)) }),
    href: project.output,
    name: project.name,
    badge,
    price: priceValue,
    location: card.label || card.locExtended || project.hero?.location || 'New Development',
    description: card.description || project.description,
    type: project.hero?.type || '',
    t: enT,
    id: project.slug,
    attrs: ' data-project-card' + dataAttrs,
    indent: '          '
  });
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
  const loc = card.label || card.locExtended || project.hero?.location || '';
  const picture = renderProjectCardGallery(project, { fallback: responsiveCardImageTag(cardImage(project)) });

  return '      ' + renderUnifiedCard({
    project,
    gallery: picture,
    href: project.output,
    name: project.name,
    badge,
    price: priceValue,
    location: loc,
    description: card.description || project.description,
    type: project.hero?.type || '',
    t: enT,
    className: 'reveal',
    style: `transition-delay:${(0.2 + index * 0.05).toFixed(2)}s`,
    indent: '      '
  });
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
function renderViewingScenesJs(sourceProject, locale = DEFAULT_LOCALE) {
  const project = localizeProject(sourceProject, locale);
  const items = project.media?.items || [];
  if (!items.length) return null;

  const scenes = items.map((item, index) => {
    const num = String(index + 1).padStart(2, '0');
    const isLast = index === items.length - 1;
    const txt = isLast ? 'closing' : (VIEWING_SCENE_CATEGORY_TXT[item.category] || 'exterior');
    const motion = index % 2 === 0
      ? '(p) => ({ s: 1.06 - p * 0.02, x: p * -10, y: p * -2 })'
      : '(p) => ({ s: 1.055 - p * 0.018, x: p * 10, y: 0 })';
    const categoryLabel = item.category ? localizedCategory(item.category, locale) : t('mediaCategory.Residences', locale);
    return `    {
      img: ${JSON.stringify(item.src)},
      pos: "center 50%",
      label: ${JSON.stringify(`${num} — ${categoryLabel}`)},
      hl: ${JSON.stringify(item.caption || project.shortName || project.name)},
      sub: ${JSON.stringify(item.alt || '')},
      gold: ${isLast ? 'true' : 'false'},
      ov: ${JSON.stringify(VIEWING_SCENE_OVERLAY)},
      txt: ${JSON.stringify(txt)},
      motion: ${motion}
    }`;
  });

  return `  ${JSON.stringify(sourceProject.slug)}: [\n${scenes.join(',\n')}\n  ]`;
}

// Cinematic Presentation project metadata (info panel), derived from the same
// project.json fields used everywhere else on the site instead of a
// hand-duplicated copy that can drift out of sync.
function renderViewingProjectEntryJs(sourceProject, locale = DEFAULT_LOCALE) {
  const project = localizeProject(sourceProject, locale);
  const discovery = project.discovery || {};
  const viewing = project.viewing || {};
  const areaDisplay = AREA_DISPLAY_NAMES[discovery.area] || project.card?.label || project.hero?.location || '';
  const highlights = project.architecture?.highlights || [];
  const investmentNotes = (project.investment?.cards || []).map(([, note]) => note).filter(Boolean);
  const availability = viewing.availability || [
    { label: t('availability.status', locale), value: discovery.status || project.hero?.delivery || t('common.onRequest', locale) },
    { label: t('viewing.material', locale), value: t('viewing.materialValue', locale) },
    { label: t('viewing.nextStep', locale), value: t('viewing.nextStepValue', locale, { project: project.shortName || project.name }) }
  ];

  const entry = {
    id: sourceProject.slug,
    name: project.name,
    location: project.hero?.location || '',
    area: areaDisplay,
    price: project.hero?.startingPrice || t('common.onRequest', locale),
    bedrooms: discovery.bedrooms || '',
    builtSize: viewing.builtSize || '',
    terraceSize: viewing.terraceSize || '',
    completion: project.hero?.delivery || t('common.onRequest', locale),
    status: discovery.status || '',
    lifestyle: project.description || '',
    overview: project.overview?.copy?.[0] || project.description || '',
    highlights,
    investmentNotes,
    availability,
    ctaLabel: viewing.ctaLabel || t('cta.requestProjectMaterial', locale),
    ctaMessage: project.enquiry?.message || `I would like to receive the latest information for ${project.name}.`
  };

  return `  ${JSON.stringify(sourceProject.slug)}: ${JSON.stringify(entry, null, 4).replace(/\n/g, '\n  ')}`;
}

// Shared by the initial (English) homepage generation below and by
// build_homepage_locales.mjs, which re-calls this per non-English locale
// to regenerate the cinematic viewer's per-project scene captions/labels
// (translated media.items captions, translated category labels, etc.)
// instead of leaving the English-baked blocks from this pass in place
// untouched on every cloned locale homepage.
export function renderViewingBlocks(projects, locale = DEFAULT_LOCALE) {
  const sorted = [...projects].sort((a, b) => (a.discovery?.priority ?? a.card?.order ?? 999) - (b.discovery?.priority ?? b.card?.order ?? 999));
  const defaultId = sorted[0]?.slug || '';

  const projectsBlock = `/* NUEVA GENERATED VIEWING PROJECTS START */
  const VIEWING_PROJECTS = {
${sorted.map((project) => renderViewingProjectEntryJs(project, locale)).join(',\n')}
  };
  const DEFAULT_VIEWING_PROJECT_ID = ${JSON.stringify(defaultId)};
  /* NUEVA GENERATED VIEWING PROJECTS END */`;

  const scenesBlock = `/* NUEVA GENERATED VIEWING SCENES START */
  const PROJECT_VIEWING_SCENE_SETS = {
${sorted.map((project) => renderViewingScenesJs(project, locale)).filter(Boolean).join(',\n')}
  };
  /* NUEVA GENERATED VIEWING SCENES END */`;

  return { projectsBlock, scenesBlock };
}

function updateHomepageViewingData(projects) {
  if (!existsSync(homepagePage)) return false;

  let html = readFileSync(homepagePage, 'utf8');
  const { projectsBlock, scenesBlock } = renderViewingBlocks(projects, DEFAULT_LOCALE);

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
  // The residence card reads item.name / item.meta / item.features. An array
  // of [label, body] pairs passes every other check and renders as a grid of
  // completely empty cards with only the floorplans button in them.
  for (const item of project.residences?.items || []) {
    if (Array.isArray(item) || typeof item !== 'object' || item === null || !String(item.name || '').trim()) {
      throw new Error(`${label}: every "residences.items" entry must be an object with a non-empty "name" (plus optional "meta" and "features") -- otherwise the residence cards render empty.`);
    }
  }
  // When a residence card is named after a specific released unit ("Villa 01")
  // rather than a type ("Independent Villa"), the availability table is the
  // single source of truth for that unit's price and areas. Nothing else stops
  // the two from drifting apart, or from being swapped between two cards --
  // which reads as a real price on the wrong house.
  const unitsByRef = new Map((project.availability?.units || [])
    .filter((unit) => unit?.reference)
    .map((unit) => [String(unit.reference).trim(), unit]));
  for (const item of project.residences?.items || []) {
    const unit = unitsByRef.get(String(item.name).trim());
    if (!unit) continue;
    const values = (item.meta || []).map(([, value]) => String(value));
    if (unit.price && !values.includes(String(unit.price))) {
      throw new Error(`${label}: residence card "${item.name}" does not carry that unit's availability price ("${unit.price}") -- its "meta" reads ${JSON.stringify(values)}. A residence card named after a unit must agree with the availability table.`);
    }
    for (const area of values.filter((value) => /m²/.test(value))) {
      if (unit.size && !String(unit.size).includes(area.replace(/\s*m²$/, ''))) {
        throw new Error(`${label}: residence card "${item.name}" states an area ("${area}") that does not appear in that unit's availability size ("${unit.size}").`);
      }
    }
  }
  // Locale overlays replace the whole items array, so a translation could
  // reorder the cards and silently attach one villa's figures to the other.
  // Residence *type* names are translated ("Apartment" -> "Apartamento"), so
  // only cards named after a unit reference can be compared by name -- those
  // are identifiers and must read identically in every locale.
  const englishNames = (project.residences?.items || []).map((item) => String(item.name));
  const englishRefs = englishNames.map((name) => (unitsByRef.has(name.trim()) ? name : null));
  for (const [locale, overlay] of Object.entries(project.i18n || {})) {
    const names = (overlay?.residences?.items || []).map((item) => String(item?.name));
    if (!names.length) continue;
    if (names.length !== englishNames.length) {
      throw new Error(`${label}: "i18n.${locale}.residences.items" has ${names.length} cards but English has ${englishNames.length} -- the arrays are positional, so a different length shifts figures onto the wrong residence.`);
    }
    englishRefs.forEach((ref, index) => {
      if (ref && names[index] !== ref) {
        throw new Error(`${label}: "i18n.${locale}.residences.items[${index}].name" is "${names[index]}" but English has the unit reference "${ref}" -- unit references must not be translated or reordered, or the translated figures land on the wrong residence.`);
      }
    });
  }
  // Adding location.site is the whole per-project input for the live map, so a
  // coordinate that has never been routed must not silently fall back to the
  // old SVG map -- the author would reasonably assume the new map was live.
  if (Array.isArray(project.location?.site) && !hasLiveLocationMap(project.slug)) {
    throw new Error(`${label}: "location.site" is set but ${project.slug} has no routed map data. Run: node scripts/build_location_maps.mjs --project=${project.slug}`);
  }
  // A tour URL is embedded in an iframe, so it is the one field on a project
  // that can execute third-party code on the page. Only Matterport's own show
  // URLs are accepted -- not a shortener, not a redirect, not http.
  const tourUrl = project.media?.tour?.url;
  if (tourUrl !== undefined) {
    let parsed = null;
    try { parsed = new URL(String(tourUrl)); } catch { parsed = null; }
    const ok = parsed && parsed.protocol === 'https:'
      && /(^|\.)matterport\.com$/.test(parsed.hostname)
      && parsed.pathname.startsWith('/show')
      && parsed.searchParams.get('m');
    if (!ok) {
      throw new Error(`${label}: "media.tour.url" must be an https Matterport show link with an "m" model id (got ${JSON.stringify(tourUrl)}).`);
    }
  }
  // location.mapArea is a MAP_LANDMARKS key, not prose. resolveMapArea() falls
  // back to marbellaCentre for anything it does not recognise, so a descriptive
  // string ("Cortijo Blanco, San Pedro de Alcantara, Marbella") silently plants
  // the marker in the wrong town rather than failing.
  const mapArea = project.location?.mapArea;
  if (mapArea !== undefined && !Object.prototype.hasOwnProperty.call(MAP_LANDMARKS, mapArea)) {
    throw new Error(`${label}: "location.mapArea" is "${mapArea}", which is not a MAP_LANDMARKS key -- the marker would fall back to marbellaCentre. Use one of: ${Object.keys(MAP_LANDMARKS).join(', ')}.`);
  }
  // privateViewing.href is the destination of both "Cinematic Presentation"
  // buttons (the hero ghost action and the section CTA). It must launch the
  // cinematic player on the homepage; pointing it at an in-page anchor sends a
  // visitor who asked for the presentation to the enquiry form instead.
  const privateHref = project.privateViewing?.href;
  if (privateHref !== undefined) {
    const expected = `index.html?private-viewing=1&project=${project.slug}`;
    if (privateHref !== expected) {
      throw new Error(`${label}: "privateViewing.href" is "${privateHref}" but the Cinematic Presentation buttons must open the player: "${expected}".`);
    }
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
    // Category labels are translated through the strings dictionary, and t()
    // falls back to the key, so a new category with no entry silently renders
    // the literal "mediaCategory.Foo" as the tile label in every locale.
    const undeclared = [...new Set(project.media.items.map((item) => item.category).filter(Boolean))]
      .filter((category) => !hasString(`mediaCategory.${category}`));
    if (undeclared.length) {
      throw new Error(`${label}: media category ${undeclared.map((c) => `"${c}"`).join(', ')} has no "mediaCategory.<name>" entry in content/i18n/strings.json -- the gallery tile would show the raw key as its label.`);
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

  for (const { code: locale } of LOCALES) {
    const outputPath = localizedPath(project.output, locale);
    const html = renderProject(project, locale);
    const fullPath = path.resolve(outputPath);
    mkdirSync(path.dirname(fullPath), { recursive: true });
    writeFileSync(fullPath, html);
    written.push(outputPath);
  }
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
