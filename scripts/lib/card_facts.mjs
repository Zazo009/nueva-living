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


// Unit sizes are strings on the unit records ("141 m²", "656 sqm built / 795 sqm plot"), and only
// some projects carry them. The card names which size it means, so the figure is read from the
// units that state that basis only: interior first, then built, then total. A unit that states none
// of them is counted only when no unit does ("size").
const SIZE_BASES = [
  ['interior', /\b(?:interior|usable|useful|living)\b/i],
  ['built', /\bbuilt\b/i],
  ['total', /\btotal\b/i]
];

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

function sizeFact(project) {
  const units = (project.availability?.units || []).filter((unit) => unit && unit.size);
  if (!units.length) return null;
  const read = (unit) => ({ value: parseSize(String(unit.size).split(/[/;]| and /)[0]), text: String(unit.size).split(/[/;]| and /)[0] });
  for (const [basis, pattern] of SIZE_BASES) {
    const values = units.map(read).filter((item) => pattern.test(item.text) && Number.isFinite(item.value) && item.value > 0).map((item) => item.value);
    if (values.length) return { basis, min: Math.round(Math.min(...values)), max: Math.round(Math.max(...values)) };
  }
  const values = units.map(read).map((item) => item.value).filter((value) => Number.isFinite(value) && value > 0);
  if (!values.length) return null;
  return { basis: 'size', min: Math.round(Math.min(...values)), max: Math.round(Math.max(...values)) };
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
