// One spelling of a price per language.
//
// A project overlay may pre-format its own prices; whatever it leaves alone is
// rendered here. The two used to disagree -- twenty-four of the thirty-six
// projects carried both "470 250 EUR" and "470 250 €" -- so the table lives in
// one module now and the audit checks the overlays against it.
//
// The project cards are generated in English and the locale pages are built by
// cloning them, which left the card price in English grouping ("€3,990,000")
// on every translated page while the "From" label beside it was translated.
// localizeCardPrices() is the pass that fixes that, and it has to run on every
// page type that carries a card.
export const PRICE_FORMAT = {
  es: (n) => `${n.replace(/,/g, '.')} €`,
  fr: (n) => `${n.replace(/,/g, ' ')} €`,
  de: (n) => `${n.replace(/,/g, '.')} €`,
  ru: (n) => `${n.replace(/,/g, ' ')} €`,
  ar: (n) => `${n} €`,
  nl: (n) => `€ ${n.replace(/,/g, '.')}`,
  pl: (n) => `${n.replace(/,/g, ' ')} €`,
  sv: (n) => `${n.replace(/,/g, ' ')} €`,
  no: (n) => `${n.replace(/,/g, ' ')} €`
};

// "€3,990,000" or "EUR 3,990,000" -> the locale's own spelling. Anything else
// ("On request", a range, an already-localised figure) is returned untouched.
export function formatLocalePrice(value, locale) {
  const format = PRICE_FORMAT[locale];
  if (!format || !value) return value;
  const match = /^(?:EUR|€)\s*([\d,]+)$/.exec(String(value).trim());
  return match ? format(match[1]) : value;
}

const CARD_PRICE_ATTR = /(data-card-price=")([^"]*)(")/g;
const CARD_PRICE_TEXT = /(<span class="dev-price-amount">)([^<]*)(<\/span>)/g;

// English grouping with a leading symbol -- "€3,990,000" -- is never correct on
// a translated page, wherever it sits: a card, a budget dropdown, a sentence.
// The card attribute and span are rewritten by name first (they may hold a
// bare "EUR 3,990,000"), then anything left over outside <script> blocks, so
// JSON-LD keeps its machine values.
const ENGLISH_PRICE = /€\s?\d{1,3}(?:,\d{3})+/g;
const SCRIPT_BLOCK = /(<script[\s\S]*?<\/script>)/g;

export function localizeCardPrices(html, locale) {
  if (!PRICE_FORMAT[locale]) return html;
  const withCards = html
    .replace(CARD_PRICE_ATTR, (m, open, value, close) => open + formatLocalePrice(value, locale) + close)
    .replace(CARD_PRICE_TEXT, (m, open, value, close) => open + formatLocalePrice(value, locale) + close);
  return withCards
    .split(SCRIPT_BLOCK)
    .map((part) => (part.startsWith('<script')
      ? part
      : part.replace(ENGLISH_PRICE, (price) => formatLocalePrice(price, locale))))
    .join('');
}
