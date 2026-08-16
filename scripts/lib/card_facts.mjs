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

/**
 * The delivery string duplicates the status badge on 6 of 14 projects: the
 * badge reads "Off-Plan" and hero.delivery reads "Off-plan". Printing both
 * reintroduces exactly the repetition the redesign removes, so the column
 * is dropped when it says the same thing as the badge.
 */
function duplicatesBadge(delivery, badge) {
  const normalise = (value) => String(value ?? '')
    .toLowerCase()
    .replace(/[\s\-–—,.]/g, '');
  const a = normalise(delivery);
  const b = normalise(badge);
  if (!a || !b) return false;
  return a === b || b.includes(a) || a.includes(b);
}

// Unit sizes are strings on the unit records ("141 m²"), and only 8 of the
// 14 projects carry them. Pull the numbers out and keep the range.
function sizeRange(project) {
  const sizes = (project.availability?.units || [])
    .map((unit) => parseFloat(String(unit.size ?? '').replace(/[^\d.,]/g, '').replace(',', '.')))
    .filter((value) => Number.isFinite(value) && value > 0);
  if (!sizes.length) return '';
  const min = Math.round(Math.min(...sizes));
  const max = Math.round(Math.max(...sizes));
  return min === max ? `${min} m²` : `${min}–${max} m²`;
}

/**
 * @param {object} project   the (already localized) project
 * @param {object} options
 * @param {string} options.badge      status badge text, to detect duplication
 * @param {function} options.t        (key, vars) => localized string
 * @returns {{label: string, value: string, sub: string, tone?: string}[]}
 *          between 0 and 3 columns, in display order
 */
export function cardFacts(project, { badge, t }) {
  const crm = project.crm || {};
  const columns = [];

  const delivery = project.hero?.delivery;
  if (delivery && !duplicatesBadge(delivery, badge)) {
    columns.push({ label: t('card.delivery'), value: delivery, sub: '' });
  }

  const min = crm.bedroomsMin;
  const max = crm.bedroomsMax;
  if (Number.isFinite(min) || Number.isFinite(max)) {
    const lo = Number.isFinite(min) ? min : max;
    const hi = Number.isFinite(max) ? max : min;
    columns.push({
      label: t('card.homes'),
      value: lo === hi ? t('card.bedSingle', { n: lo }) : t('card.bedRange', { min: lo, max: hi }),
      sub: sizeRange(project)
    });
  }

  // availableUnits is missing on one project but its units[] list is the
  // available list, so its length is the same number.
  const available = Number.isFinite(crm.availableUnits)
    ? crm.availableUnits
    : (project.availability?.units || []).length;
  const total = crm.totalUnits;
  if (available > 0 && Number.isFinite(total) && total > 0) {
    columns.push({
      label: t('card.available'),
      value: t('card.unitsOf', { available, total }),
      sub: project.availability?.phase || '',
      tone: 'gold'
    });
  }

  return columns;
}
