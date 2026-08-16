// The project card gallery -- the swipeable image block at the top of every
// listing card.
//
// This used to exist as three near-identical copies, one in each builder
// (build_property_pages, build_footer_pages, build_segment_pages). They had
// drifted: only the property-pages copy had the WebP <picture> markup, so the
// area and segment pages were still shipping 1920px JPEGs into 330px slots,
// and when share/fullscreen buttons were added only that copy got them --
// leaving 19 of the site's 43 card galleries without them, in every language.
//
// One copy, imported by all three builders. Add a feature here and every card
// on the site has it.

import { existsSync } from 'node:fs';

export const CARD_IMAGE_SIZES = '(max-width: 640px) 92vw, (max-width: 1100px) 46vw, 30vw';

function esc(value) {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function attr(name, value) {
  return value === undefined || value === null || value === '' ? '' : ` ${name}="${esc(value)}"`;
}

// Card slides render around 350 CSS px wide but the source files are 1920px --
// roughly 430KB each, six per card. <picture> is `display: contents` in CSS,
// so the <img> stays the flex item of the scroll track and every gallery rule
// applies unchanged: smaller files, identical layout.
function slideTag(item, projectName) {
  const img = `<img src="${esc(item.src)}" alt="${esc(item.alt || projectName)}" loading="lazy" decoding="async">`;
  const match = String(item.src || '').match(/^(.*)\.(?:jpe?g)$/i);
  if (!match) return `\n              ${img}`;
  const base = match[1];
  const candidates = [[`${base}-640.webp`, 640], [`${base}-960.webp`, 960]]
    .filter(([file]) => existsSync(file))
    .map(([file, width]) => `${esc(file)} ${width}w`);
  if (!candidates.length) return `\n              ${img}`;
  return `
              <picture>
                <source type="image/webp" srcset="${candidates.join(', ')}" sizes="${CARD_IMAGE_SIZES}">
                ${img}
              </picture>`;
}

/**
 * @param {object} project        the (already localized) project
 * @param {object} [options]
 * @param {string} [options.fallback]  markup to use when there is no gallery
 */
export function renderProjectCardGallery(project, options = {}) {
  const items = (project.media?.items || []).slice(0, 6);
  if (!items.length) {
    if (options.fallback) return options.fallback;
    const image = project.images?.hero || {};
    return `<img src="${esc(image.src)}" alt="${esc(image.alt || project.name)}" width="${image.width || 1600}" height="${image.height || 900}" loading="lazy" decoding="async">`;
  }

  const slides = items.map((item) => slideTag(item, project.name)).join('');

  const dots = items.length > 1
    ? `<div class="project-card-gallery-dots" data-gallery-dots>${items.map((_, index) => `<button type="button" class="project-card-gallery-dot${index === 0 ? ' is-active' : ''}" data-gallery-dot="${index}" aria-label="Show image ${index + 1} of ${items.length}"></button>`).join('')}</div>`
    : '';

  const arrows = items.length > 1
    ? `<button type="button" class="project-card-gallery-arrow project-card-gallery-arrow--prev" data-gallery-prev aria-label="Previous image">&#8249;</button>
              <button type="button" class="project-card-gallery-arrow project-card-gallery-arrow--next" data-gallery-next aria-label="Next image">&#8250;</button>`
    : '';

  // The card carries six slides, but the fullscreen viewer opens the whole
  // project -- 41 images on Elviria. The list ships as a <template> of real
  // <img alt="..."> rather than JSON because the locale builds translate
  // captions by rewriting `alt="<english>"` across the rendered page; inside a
  // JSON blob every caption would have stayed English on non-English pages.
  // Template content is inert and the URL sits on data-src, so nothing here is
  // fetched until the viewer opens.
  const allImages = (project.media?.items || []).filter((item) => item.src && !item.video);
  const manifest = allImages.length > 1
    ? `\n              <template data-card-images>${allImages
        .map((item) => {
          const match = String(item.src).match(/^(.*)\.(?:jpe?g)$/i);
          // A 2560px master per image is far too much for a phone scrolling
          // forty of them; point at the WebP derivative where one exists.
          const webp = match && existsSync(`${match[1]}-960.webp`) ? ` data-webp="${esc(`${match[1]}-960.webp`)}"` : '';
          return `<img data-src="${esc(item.src)}"${webp} alt="${esc(item.alt || item.caption || project.name)}">`;
        })
        .join('')}</template>`
    : '';

  // Share and fullscreen sit with the shortlist heart in one corner cluster;
  // nueva-shortlist.js drops the heart in at the top of this container.
  //
  // The labels are written here in English and replaced at runtime with the
  // reader's language by the gallery script's own dictionary. Emitting them
  // rather than leaving the naming entirely to JS means the buttons are never
  // anonymous to a screen reader, including before the script runs.
  const actions = `
              <div class="project-card-actions" data-card-actions>
                <button type="button" class="project-card-action" data-card-share aria-label="Share this project" title="Share this project">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="18" cy="5" r="3"></circle><circle cx="6" cy="12" r="3"></circle><circle cx="18" cy="19" r="3"></circle><path d="M8.6 13.5l6.8 4M15.4 6.5l-6.8 4"></path></svg>
                </button>${allImages.length > 1 ? `
                <button type="button" class="project-card-action" data-card-expand aria-label="View all photos" title="View all photos">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 4H4v5M15 4h5v5M15 20h5v-5M9 20H4v-5"></path></svg>
                </button>` : ''}
              </div>`;

  return `<div class="project-card-gallery" data-project-card-gallery data-card-url="${esc(project.output)}"${attr('data-card-name', project.name)}>
              <div class="project-card-gallery-track" data-gallery-track>${slides}
              </div>
              ${arrows}
              ${dots}${actions}${manifest}
            </div>`;
}
