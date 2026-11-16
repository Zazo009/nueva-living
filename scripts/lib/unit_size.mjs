// The size of one home, read from the size line of the developer's price list.
//
// Developers do not measure alike. Most give the built area (construida), about a quarter give only
// the interior, and what "built" includes differs from one developer to the next: across the 253
// homes on the site that give both, built runs from 1.1 to 1.6 times the interior. No conversion
// recovers one from the other with any accuracy, so none is attempted. The size filter reads the
// figure the developer gives -- built where there is one, otherwise interior -- and says which it
// is, and the filter itself allows a margin (SIZE_MARGIN) for the difference in method.
//
// Used by the developments cards (data-sizes) and by the assistant connector's catalogue, so the
// site and the assistant read a home's size the same way.

export const SIZE_MARGIN = 0.1;

// "1.102 sqm" and "1,102 sqm" are a thousand and a hundred and two square metres, not one.
function number(raw) {
  const value = String(raw).replace(/\s/g, '');
  if (/^\d{1,3}[.,]\d{3}$/.test(value)) return Number(value.replace(/[.,]/, ''));
  return Number(value.replace(',', '.'));
}

const UNIT = '(?:sqm|sq\\.?\\s?m|m²|m2)';
const BUILT = new RegExp(`([\\d][\\d.,]*)\\s*${UNIT}\\s*(?:built|constructed)(?!\\s*outside)`, 'i');
const INTERIOR = new RegExp(`([\\d][\\d.,]*)\\s*${UNIT}\\s*(?:interior|internal|useful|living)`, 'i');
const ANY = new RegExp(`([\\d][\\d.,]*)\\s*${UNIT}`, 'i');

// { sqm, basis } with basis 'built' or 'interior', or null when the line gives no size. A line
// that names neither ("103 m²", "370 m², private pool") is taken as built: that is what a bare
// figure means on a Spanish price list.
export function unitSize(text) {
  const line = String(text || '');
  for (const [re, basis] of [[BUILT, 'built'], [INTERIOR, 'interior'], [ANY, 'built']]) {
    const match = re.exec(line);
    if (!match) continue;
    const sqm = Math.round(number(match[1]));
    if (Number.isFinite(sqm) && sqm >= 20 && sqm <= 5000) return { sqm, basis };
  }
  return null;
}

// Every distinct size in a project's price list, smallest first.
export function projectSizes(project) {
  const sizes = new Set();
  for (const unit of project.availability?.units || []) {
    const size = unitSize(unit.size);
    if (size) sizes.add(size.sqm);
  }
  return [...sizes].sort((a, b) => a - b);
}
