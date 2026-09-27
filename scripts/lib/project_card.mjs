// The listing card -- one definition, used by every grid on the site.
//
// v2 (dev-card--v2): nothing sits over the photo. Status badge in a bar above
// the image, gallery controls in a bar below it, price + units in a band at the
// ruled row under the name. Styles: the 'Listing card v2' block at the end of
// assets/liora/nueva-system.css.
//
// There used to be two visually different cards, one on the homepage and one
// on every other grid. They were consolidated into this partial; this is the
// redesign of that single card.
//
// WHAT OTHER CODE DEPENDS ON  (changing any of these breaks live behaviour)
//
//   .dev-card, [data-project-card]   nueva-shortlist, liora-discovery,
//                                    nueva-tracking, liora-conversion
//   .dev-img-wrap                    nueva-shortlist (heart placement)
//   .dev-loc                         nueva-shortlist (saved location)
//   .dev-name                        nueva-shortlist, tracking, conversion
//   .dev-cta-link[href*=property-]   nueva-shortlist, conversion
//   [data-card-actions]              nueva-shortlist injects the heart here
//   .project-card-actions            liora-card-gallery (click passthrough)
//   data-card-url                    liora-card-gallery, nueva-shortlist
//   data-card-price / data-card-type nueva-shortlist reads these instead of
//                                    counting fact columns positionally
//
// The old design carried a FROM / TYPE / STATUS grid and nueva-shortlist
// read it by index -- metaValues[0] as the price, metaValues[1] as the type.
// The redesign replaces that grid with Delivery / Homes / Available, so the
// indexes would have silently started saving a delivery date as the price
// and sending it to the CRM. The two data attributes above replace the
// positional read; nueva-shortlist prefers them and falls back to the old
// selectors, so nothing regresses on pages built before this change.

import { cardFacts } from './card_facts.mjs';

// CRM numbers arrive as numbers on thirteen projects and as strings on one
// ("4", "15"). Number.isFinite rejects a string, so that project silently
// lost its Homes and Available columns and its unit badge -- no error, just
// a card with one fact instead of three. Coerce rather than trust the type.
function toNumber(value) {
  const n = typeof value === 'string' ? Number(value.trim()) : value;
  return Number.isFinite(n) ? n : undefined;
}

function esc(value) {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

// The price sits over the photo. "From EUR 2,400,000 + VAT" collides with
// the badge on a phone, so the tax suffix is dropped here only -- the full
// price stays on the project page. Every language's form is listed because
// the area and segment pages render an already-translated price.
const TAX_SUFFIX = /\s*(?:\+\s*(?:VAT|IVA|TVA|НДС|ضريبة|skatt|mva)\.?|zzgl\.\s*MwSt\.?)\s*$/iu;

const ARROW = '<svg class="dev-cta-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 12h15M13 6l6 6-6 6"></path></svg>';

// Quick contact on every card. Same number as the mobile menu, and the same
// label key: spelled out, "WhatsApp" is identical in nine languages and the
// untranslated-text guard reads that as a missing translation -- and Arabic
// does have its own spelling for it.
const WHATSAPP_NUMBER = '46707576709';
const WA_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"></path></svg>';

/**
 * @param {object}   card
 * @param {object}   card.project     the (already localized) project, for facts
 * @param {string}   card.gallery     rendered gallery markup
 * @param {string}   card.href        project URL
 * @param {string}   card.name        project name
 * @param {string}   card.badge       status badge over the image
 * @param {string}   card.price       price, without the "From"
 * @param {string}   card.location    eyebrow above the price
 * @param {string}   card.description tagline, clamped to 3 lines in CSS
 * @param {string}   card.type        property type -- not displayed, carried
 *                                    on data-card-type for the shortlist
 * @param {function} card.t           (key, vars) => localized string
 * @param {string}   [card.id]
 * @param {string}   [card.className]
 * @param {string}   [card.style]
 * @param {string}   [card.attrs]     pre-escaped data-* attribute string
 * @param {string}   [card.heading]   'h2' | 'h3'
 * @param {string}   [card.indent]
 */
export function renderUnifiedCard(card) {
  const {
    project = {}, gallery, href, name, badge, price, location, description, type = '',
    t, id, className = '', style = '', attrs = '', heading = 'h2', indent = ''
  } = card;

  const classes = ['project-card', 'dev-card', 'dev-card--v2', className].filter(Boolean).join(' ');
  const cleanPrice = String(price ?? '').replace(TAX_SUFFIX, '');
  // "From" only makes sense in front of a figure. A villa quoted on request
  // read "From Price on request" on its card.
  const showsFromLabel = /\d/.test(cleanPrice);
  // Shown with the € sign ("€305,000") instead of "EUR 305,000". Translated
  // pages then get their own spelling from localizeCardPrices() in prices.mjs,
  // which already accepts both forms. data-card-price keeps the raw value for
  // the shortlist/CRM.
  const displayPrice = cleanPrice.replace(/^EUR\s*(?=\d)/, '€');

  // Badge row: status, plus the unit count when the project has one.
  const crm = project.crm || {};
  const available = toNumber(crm.availableUnits) ?? (project.availability?.units || []).length;
  const total = toNumber(crm.totalUnits);
  // "25 of 25 left" claims that nothing in the scheme has sold, which is a
  // claim about the whole development, not about the release list we actually
  // read. Casares Costa said it because its total was set from the length of
  // its own availability table. A ratio is only worth printing when the two
  // numbers differ; otherwise the count stands on its own.
  const hasUnits = available > 0 && total !== undefined && total > available;
  const badges = [
    badge ? `<span class="dev-badge">${esc(badge)}</span>` : '',
    hasUnits ? `<span class="dev-badge-units">${esc(t('card.unitsLeft', { available, total }))}</span>` : ''
  ].filter(Boolean).join('');

  const facts = cardFacts(project, { badge, t });
  const factsMarkup = facts.length
    ? `<div class="dev-facts" data-fact-count="${facts.length}">${facts.map((fact) => `
            <div class="dev-fact${fact.tone === 'gold' ? ' dev-fact--gold' : ''}">
              <span class="dev-fact-label">${esc(fact.label)}</span>
              <span class="dev-fact-value">${esc(fact.value)}</span>${fact.sub ? `
              <span class="dev-fact-sub">${esc(fact.sub)}</span>` : ''}
            </div>`).join('')}
          </div>`
    : '';

  const priceMarkup = cleanPrice
    ? `<div class="dev-price">${showsFromLabel ? `<span class="dev-price-label">${esc(t('card.from'))}</span>` : ''}<span class="dev-price-amount">${esc(displayPrice)}</span></div>`
    : '';
  const statusBadge = badge ? `<span class="dev-badge">${esc(badge)}</span>` : '';
  const unitsBadge = hasUnits ? `<span class="dev-badge-units">${esc(t('card.unitsLeft', { available, total }))}</span>` : '';
  const waHref = `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(name || '')}`;

  return `<article class="${classes}"${id ? ` id="${esc(id)}"` : ''}${style ? ` style="${style}"` : ''} data-card-url="${esc(href)}"${attrs}${price ? ` data-card-price="${esc(cleanPrice)}"` : ''}${type ? ` data-card-type="${esc(type)}"` : ''}>
        <div class="dev-img-wrap">
          ${gallery}
          <div class="dev-scrim" aria-hidden="true"></div>
          <div class="dev-overlay" aria-hidden="true"></div>
          ${statusBadge ? `<div class="dev-v2-badges"><div class="dev-badges">${statusBadge}</div></div>` : ''}
        </div>
        <div class="dev-body">
          ${location ? `<div class="dev-loc">${esc(location)}</div>` : ''}
          <${heading} class="dev-name">${esc(name)}</${heading}>
          ${priceMarkup || unitsBadge ? `<div class="dev-v2-priceline">${priceMarkup}${unitsBadge}</div>` : ''}
          <p class="dev-tagline">${esc(description)}</p>
          ${factsMarkup}
          <div class="dev-v2-cta">
            <a class="dev-cta-link" href="${esc(href)}"><span class="dev-cta-label">${esc(t('cta.exploreProject'))}</span>${ARROW}</a>
            <a class="dev-v2-whatsapp" href="${esc(waHref)}" target="_blank" rel="noopener">${WA_ICON}<span>${esc(t('cta.whatsappUs'))}</span></a>
          </div>
        </div>
      </article>`.replace(/\n/g, `\n${indent}`);
}
