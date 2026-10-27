// The three fact columns on the listing card: Delivery, Homes, Available.
//
// Everything here is derived from data that already exists on the project --
// no new content fields, no CRM changes. What each column can actually show,
// measured across all 14 projects:
//
//   Delivery   hero.delivery          14/14, but free prose, not quarters:
//                                     "Q4 2027", "Off-plan", "To be
//                                     confirmed", "18 months from contract".
//                                     Already translated via the i18n
//                                     overlay, so it is passed through as-is
//                                     rather than rebuilt from a pattern.
//   Homes      crm.bedroomsMin/Max    14/14
//              + size range           8/14 (parsed from availability.units)
//   Available  crm.availableUnits     14/14
//              / crm.totalUnits
//
// The phase sub-line under Available reads `availability.phase`. That field
// now exists on every project but is empty -- the values are real facts
// about real releases ("Phase 2"), so they have to be filled in from the
// developer's material, not invented here. Fill any of them in and the line
// appears on that card with no further code change; leave it empty and the
// line stays absent.
//
// A column with no data is dropped entirely and the survivors split the
// width -- never an empty column, never a dash.

// CRM numbers arrive as numbers on thirteen projects and as strings on one
// ("4", "15"). Number.isFinite rejects a string, so that project silently
// lost its Homes and Available columns and its unit badge -- no error, just
// a card with one fact instead of three. Coerce rather than trust the type.
function toNumber(value) {
  const n = typeof value === 'string' ? Number(value.trim()) : value;
  return Number.isFinite(n) ? n : undefined;
}


// Unit sizes are strings on the unit records, and most of them list several measures at once:
// "260.83 sqm built, 151.77 sqm interior, 16.62 sqm terrace". Each measure is read on its own and
// put in a class, so the card can say which one it shows and never reads the built area as the
// interior one:
//   interior  "interior", "usable", "useful", "built interior", "built inside"
//   built     "built", "total built"
//   total     "total" on its own
//   size      a bare figure with no word after it
// Terraces, gardens, solariums, pools, basements and plots are not the home's size and are skipped.
const SIZE_BASES = ['interior', 'built', 'total', 'size'];
const NOT_LIVING = /plot|terrace|garden|solarium|porch|basement|pool|outside|rooftop/;

// "1,260.53" is one thousand two hundred and sixty, not 1.26: a comma followed by exactly three
// digits is a thousands separator. Anything else with a comma is a decimal comma ("98,5").
function parseSize(text) {
  const raw = (String(text ?? '').match(/\d[\d.,]*/) || [''])[0].replace(/[.,]+$/, '');
  if (!raw) return NaN;
  const cleaned = /^\d{1,3}(,\d{3})+(\.\d+)?$/.test(raw)
    ? raw.replace(/,/g, '')
    : /^\d+,\d{1,2}$/.test(raw) ? raw.replace(',', '.') : raw.replace(/,/g, '');
  return parseFloat(cleaned);
}

function classifyMeasure(part) {
  const text = part.toLowerCase();
  if (!/\d/.test(text) || NOT_LIVING.test(text)) return null;
  if (/interior|usable|useful|inside|living/.test(text)) return 'interior';
  if (/built/.test(text)) return 'built';
  if (/\btotal\b/.test(text)) return 'total';
  return /^[\s\d.,]*(?:sqm|m\u00b2|m2)?\s*$/.test(text) ? 'size' : null;
}

// One unit's string -> { interior: 151.77, built: 260.83, ... }
function measuresOf(sizeText) {
  const found = {};
  for (const part of String(sizeText).split(/[;/]|,(?!\d{3}(?:\D|$))/)) {
    const basis = classifyMeasure(part);
    const value = parseSize(part);
    if (basis && Number.isFinite(value) && value > 0 && !(basis in found)) found[basis] = value;
  }
  return found;
}

function sizeFact(project) {
  const units = (project.availability?.units || []).filter((unit) => unit && unit.size).map((unit) => measuresOf(unit.size));
  // The basis most units state wins, so the range is the one a buyer can compare across the
  // homes; interior beats built beats total when they cover the same number.
  let best = null;
  for (const basis of SIZE_BASES) {
    const values = units.map((measures) => measures[basis]).filter(Boolean);
    if (values.length && (!best || values.length > best.values.length)) best = { basis, values };
  }
  // A bare figure takes the basis the project's documents state for it, when they state one.
  if (best && best.basis === 'size' && ['interior', 'built', 'total'].includes(project.availability?.sizeBasis)) best.basis = project.availability.sizeBasis;
  if (best) return { basis: best.basis, min: Math.round(Math.min(...best.values)), max: Math.round(Math.max(...best.values)), covered: best.values.length, units: units.length };

  // No unit states a size (the project lists types, not homes): read it from the type cards.
  const readType = (matcher) => {
    const numbers = [];
    for (const item of project.residences?.items || []) {
      for (const pair of item.meta || []) {
        if (Array.isArray(pair) && matcher.test(String(pair[0]))) {
          String(pair[1]).replace(/\d[\d.,]*/g, (m) => { const n = parseSize(m); if (Number.isFinite(n) && n > 0) numbers.push(n); return m; });
        }
      }
    }
    return numbers;
  };
  for (const [basis, matcher] of [['interior', /^interior(?! built)|interior built|usable|useful/i], ['built', /^built|total built/i]]) {
    const numbers = readType(matcher);
    if (numbers.length) return { basis, min: Math.round(Math.min(...numbers)), max: Math.round(Math.max(...numbers)), covered: 0, units: 0 };
  }
  return null;
}

/**
 * @param {object} project   the (already localized) project
 * @param {object} options
 * @param {function} options.t        (key, vars) => localized string
 * @returns {{label: string, value: string, sub: string, tone?: string}[]}
 *          between 0 and 3 columns, in display order
 */
export function cardFacts(project, { t }) {
  const crm = project.crm || {};
  const columns = [];

  // Delivery shows on every card, even when it echoes the status badge
  // above it ("Completed" under "Completed, Ready To Move In"). A column
  // that appears on twelve cards and silently vanishes on two reads as a
  // gap in the data rather than as tidiness, and a buyer scanning the grid
  // is comparing the same three facts across every project.
  const delivery = project.hero?.delivery;
  if (delivery) {
    columns.push({ label: t('card.delivery'), value: delivery, sub: '' });
  }

  const min = toNumber(crm.bedroomsMin);
  const max = toNumber(crm.bedroomsMax);
  const bedroomColumn = (min !== undefined || max !== undefined)
    ? (() => {
        const lo = min !== undefined ? min : max;
        const hi = max !== undefined ? max : min;
        return { label: t('card.bedrooms'), value: lo === hi ? String(lo) : `${lo}\u2013${hi}`, sub: '', numeric: true };
      })()
    : null;
  if (bedroomColumn) columns.unshift(bedroomColumn);

  const size = sizeFact(project);
  if (size) {
    const labelKey = { interior: 'card.sizeInterior', built: 'card.sizeBuilt', total: 'card.sizeTotal', size: 'card.size' }[size.basis];
    columns.splice(bedroomColumn ? 1 : 0, 0, {
      label: t(labelKey),
      value: size.min === size.max ? `${size.min}` : `${size.min}\u2013${size.max}`,
      unit: 'm\u00b2',
      sub: '',
      numeric: true
    });
  }

  return columns;
}
