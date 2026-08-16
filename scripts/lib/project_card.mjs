// The listing card -- one definition, used by every grid on the site.
//
// There used to be two visually different cards. The homepage rendered a
// `.dev-card`: status badge over the image, "From EUR x" burned into the
// bottom corner, location / name / tagline / meta / CTA. The developments,
// area and segment pages rendered a `.project-card`: no badge, no price on
// the image, a tag row instead of a type chip. Same projects, same data --
// two looks, so a visitor moving from the homepage to /developments saw the
// same thirteen properties presented as if they came from different sites.
//
// This renders the richer homepage card everywhere. The outer element keeps
// the `project-card` class and the `data-project-card` filter attributes so
// discovery filtering, the shortlist heart and the dark-band overrides all
// keep working untouched; the inner structure is the homepage's.
//
// The class names on the chrome (`dev-badge`, `dev-price-overlay`, `lbl`,
// `val`) are deliberately unchanged: the locale builds translate those
// strings with find/replace entries keyed on exactly those class prefixes
// (see lib/card_chrome_translations.mjs), so keeping the names means the
// badge and price prefix arrive already translated on every page that now
// shows them for the first time.

// The price sits in the bottom corner of the photo with the status badge in
// the opposite corner. "From EUR 2,400,000" fits; "From EUR 2,400,000 + VAT"
// runs into the badge on a phone. The suffix is dropped from the overlay
// only -- the meta row directly below still carries the full price, so
// nothing is hidden from the buyer.
//
// Area and segment pages render the already-translated price, so every
// language's form of the suffix has to be recognised here.
const TAX_SUFFIX = /\s*(?:\+\s*(?:VAT|IVA|TVA|НДС|ضريبة)\.?|zzgl\.\s*MwSt\.?)\s*$/iu;

function esc(value) {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

/**
 * @param {object}   card
 * @param {string}   card.gallery     rendered gallery/image markup
 * @param {string}   card.href        project URL
 * @param {string}   card.name        project name
 * @param {string}   card.badge       status chip over the image
 * @param {string}   card.price       price shown bottom-right, without the "From"
 * @param {string}   card.pricePrefix localized "From" (default English)
 * @param {string}   card.location    eyebrow above the name
 * @param {string}   card.description tagline
 * @param {[string,string][]} card.meta   label/value pairs (max 3 shown)
 * @param {string}   card.cta         CTA text
 * @param {string}   [card.id]        element id
 * @param {string}   [card.className] extra classes on the article
 * @param {string}   [card.style]     inline style (reveal transition delay)
 * @param {string}   [card.attrs]     pre-escaped data-* attribute string
 * @param {string}   [card.heading]   'h2' | 'h3' (default h2)
 * @param {string}   [card.indent]    leading whitespace for the markup
 */
export function renderUnifiedCard(card) {
  const {
    gallery, href, name, badge, price, pricePrefix = 'From', location, description,
    meta = [], cta = 'Explore Project', id, className = '', style = '',
    attrs = '', heading = 'h2', indent = ''
  } = card;

  const classes = ['project-card', 'dev-card', className].filter(Boolean).join(' ');
  const badgeMarkup = badge ? `<span class="dev-badge">${esc(badge)}</span>\n        ` : '';
  const priceMarkup = price
    ? `\n          <div class="dev-price-overlay">${esc(pricePrefix)} ${esc(String(price).replace(TAX_SUFFIX, ''))}</div>`
    : '';
  const metaMarkup = meta.slice(0, 3)
    .map(([label, value]) => `<div class="dev-meta-item"><span class="lbl">${esc(label)}</span><span class="val">${esc(value)}</span></div>`)
    .join('');

  return `<article class="${classes}"${id ? ` id="${esc(id)}"` : ''}${style ? ` style="${style}"` : ''} data-card-url="${esc(href)}"${attrs}>
        <div class="dev-img-wrap">
          ${badgeMarkup}${gallery}
          <div class="dev-img-overlay"></div>${priceMarkup}
        </div>
        <div class="dev-body">
          <div class="dev-loc">${esc(location)}</div>
          <${heading} class="dev-name">${esc(name)}</${heading}>
          <p class="dev-tagline">${esc(description)}</p>
          <div class="dev-meta">${metaMarkup}</div>
          <div class="dev-footer">
            <a class="dev-cta-link" href="${esc(href)}">${esc(cta)}</a>
          </div>
        </div>
      </article>`.replace(/\n/g, `\n${indent}`);
}
