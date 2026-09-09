// Which area guide a project belongs to, and what to call that area.
//
// This lived twice: projectArea() in build_property_pages.mjs titled the nine
// locale pages, projectAreaLabel() in build_dist.mjs titled the English one.
// Adding a branch to one and not the other gave a project two different areas
// -- a Benalmadena development read "Marbella" on the English page and
// "Benalmadena" on the other nine for exactly that reason, and both files
// carried a comment warning the next person about it. One ordered table now,
// and audit_site_consistency checks that neither file has grown its own copy.
//
// The rules are ordered and the first match wins. Most read the project's
// location text, which is prose and can say anything; sanPedro reads the
// mapArea key instead, which is validated against MAP_LANDMARKS and cannot
// quietly drift. "Cortijo Blanco, Marbella" and "Guadalmina Golf, Marbella"
// name neither San Pedro nor anything a text rule would catch, so the five
// projects there had all been falling through to the Marbella default.
//
// `englishLabel` is what the English build prints. It is unaccented for three
// areas because that is what those pages have always said; changing it would
// rewrite live titles and schema for a cosmetic reason.
export const PROJECT_AREA_RULES = [
  { key: 'nuevaAndalucia', englishLabel: 'Nueva Andalucia', slug: 'nueva-andalucia', href: 'area-nueva-andalucia.html',
    match: (text) => text.includes('nueva andaluc') },
  { key: 'benahavis', englishLabel: 'Benahavis', slug: 'benahavis', href: 'area-benahavis.html',
    match: (text) => text.includes('benahav') },
  { key: 'estepona', englishLabel: 'Estepona', slug: 'estepona', href: 'area-estepona.html',
    match: (text) => text.includes('estepona') || text.includes('new golden mile') },
  { key: 'mijasFuengirola', englishLabel: 'Mijas & Fuengirola', slug: 'mijas-fuengirola', href: 'area-mijas-fuengirola.html',
    match: (text) => text.includes('mijas') || text.includes('fuengirola') },
  // Benalmadena has no guide of its own and sits between Fuengirola and
  // Torremolinos, so it borrows the Mijas & Fuengirola page. The label still
  // names the real town: calling it "Mijas & Fuengirola" put a factual error
  // in the title tag, the breadcrumb and the schema.
  { key: 'benalmadena', englishLabel: 'Benalmadena', slug: 'mijas-fuengirola', href: 'area-mijas-fuengirola.html',
    match: (text) => text.includes('benalmad') },
  { key: 'casares', englishLabel: 'Casares', slug: 'casares', href: 'area-casares.html',
    match: (text) => text.includes('casares') },
  { key: 'sanPedroAlcantara', englishLabel: 'San Pedro de Alcantara', slug: 'san-pedro-alcantara', href: 'area-san-pedro-alcantara.html',
    match: (text, mapArea) => mapArea === 'sanPedro' },
  // Elviria is in Marbella East, but only one of the three projects there
  // happened to write "Marbella East" into its location line, so the other two
  // fell through to plain Marbella and the three were breadcrumbed, titled and
  // filed in the CRM three different ways. The place name settles it.
  { key: 'marbellaEast', englishLabel: 'Marbella East', slug: 'marbella', href: 'area-marbella.html',
    match: (text) => text.includes('marbella east') || text.includes('elviria') },
];

export const DEFAULT_PROJECT_AREA = { key: 'marbella', englishLabel: 'Marbella', slug: 'marbella', href: 'area-marbella.html' };

export function projectAreaRule(project) {
  const text = `${project?.hero?.location || ''} ${project?.schema?.areaServed || ''}`.toLowerCase();
  const mapArea = project?.location?.mapArea;
  return PROJECT_AREA_RULES.find((rule) => rule.match(text, mapArea)) || DEFAULT_PROJECT_AREA;
}
