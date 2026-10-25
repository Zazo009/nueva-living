// Which projects a villa landing page lists, and which of them its figures count.
//
// Read by build_segment_pages.mjs (the page) and build_dist.mjs (the English
// <title>, whose {count} has to be the number the H1 shows). Both import this
// file instead of repeating the rule, because the two copies of the apartment
// rule already have to be kept in step by hand.
//
// A project is listed when its crm.propertyTypes include 'villa' -- the same
// field the apartment pages filter on, so the villa pages and the type pages
// can never disagree about what a villa is. That includes the semi-detached
// houses the developers file as villas.
//
// Some of those projects are mixed: apartments, penthouses or townhouses with
// a few villas among them. They are listed (the card names the full range of
// home types) but they are NOT counted in the page's figures. A mixed
// project's priceMin is its cheapest apartment, and a "villas from EUR 450,000"
// that is really a one-bedroom flat is the kind of number this page exists to
// avoid. Price, bedrooms and availability are computed from the villa-only
// projects, and the page says so.
//
// `areas` lists discovery.area values; null means every area. Marbella takes
// three because the site's area guides split the municipality into Marbella,
// Nueva Andalucia and San Pedro Alcantara, while buyers search "villas in
// Marbella" for all of it.
export const VILLA_SEGMENT_AREAS = {
  'new-build-villas-estepona.html': ['estepona'],
  'new-build-villas-marbella.html': ['marbella', 'nueva-andalucia', 'san-pedro-alcantara'],
  'new-build-villas-costa-del-sol.html': null
};

export const isVillaProject = (project) => (project.crm?.propertyTypes || []).includes('villa');

export const isVillaOnlyProject = (project) => {
  const types = project.crm?.propertyTypes || [];
  return types.length > 0 && types.every((type) => type === 'villa');
};

export function matchVillaProjects(projects, areas) {
  return projects.filter((project) => isVillaProject(project)
    && (areas === null || areas.includes(project.discovery?.area)));
}

export function villaFigures(matches) {
  const villaOnly = matches.filter(isVillaOnlyProject);
  const numbers = (pick) => villaOnly.map(pick).filter((n) => typeof n === 'number');
  const prices = numbers((p) => p.crm?.priceMin);
  const bedroomsMin = numbers((p) => p.crm?.bedroomsMin);
  const bedroomsMax = numbers((p) => p.crm?.bedroomsMax);
  const available = numbers((p) => p.crm?.availableUnits);
  return {
    count: matches.length,
    villaOnlyCount: villaOnly.length,
    mixedCount: matches.length - villaOnly.length,
    priceFrom: prices.length ? Math.min(...prices) : null,
    bedroomsMin: bedroomsMin.length ? Math.min(...bedroomsMin) : null,
    bedroomsMax: bedroomsMax.length ? Math.max(...bedroomsMax) : null,
    availableTotal: available.length ? available.reduce((sum, n) => sum + n, 0) : null
  };
}
