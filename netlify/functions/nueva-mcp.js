// Nueva Living inside Claude and ChatGPT: a Model Context Protocol server at https://nuevaliving.com/mcp.
//
// A person adds the address as a connector (Claude: Customize > Connectors > Add custom connector;
// ChatGPT: an app in developer mode) and can then search the projects in their own words. The
// assistant calls the three tools below and answers from what they return.
//
// Transport: MCP "Streamable HTTP", stateless. Every request is one JSON-RPC message in a POST and
// gets one JSON answer; no session, no server-sent events, no state between calls. That is all the
// protocol requires of a server that never pushes anything, and it is what a Netlify function can
// do. The protocol is small enough to speak by hand, which keeps this function free of
// dependencies, like every other function here.
//
// What it may say: data/mcp-catalog.json, built by build_property_pages from the fields the project
// pages already print, in the ten site languages. Never the crm block. The audit checks each entry
// for its own project's real name and developer, as it does the pages.
//
// Leads: request_details hands the enquiry to nueva-lead.js, the same forwarder the site's forms
// use, so it reaches the CRM with the same spam rules and the same field mapping.
const crypto = require('crypto');
const catalog = require('./data/mcp-catalog.json');
const lead = require('./nueva-lead');
const { WIDGET_HTML } = require('./lib/mcp-widget');

const SERVER_INFO = { name: 'nueva-living', title: 'Nueva Living', version: '1.0.0' };
const PROTOCOL_VERSIONS = ['2025-06-18', '2025-03-26', '2024-11-05'];
const LANGUAGES = ['en', 'es', 'fr', 'de', 'ru', 'ar', 'nl', 'pl', 'sv', 'no'];
const PROPERTY_TYPES = ['apartment', 'penthouse', 'villa', 'townhouse', 'duplex'];
const STAGES = ['off_plan', 'under_construction', 'completed'];
const MAX_RESULTS = 6;
const FEATURES = ['sea_view', 'beach', 'golf', 'private_pool', 'communal_pool', 'indoor_pool', 'garden', 'rooftop',
  'gated', 'gym', 'spa', 'lift', 'smart_home', 'coworking', 'ev_charging', 'mountain_view'];
const ADVISOR = { email: 'contact@nuevaliving.com', whatsapp: '+46 70 757 67 09', contact: 'https://nuevaliving.com/contact.html' };

// The view a host draws for the results (MCP Apps: Claude and ChatGPT). Its address carries a hash
// of its own bytes, so a host that caches views fetches a changed one instead of an old copy.
const WIDGET_URI = `ui://nueva-living/view-${crypto.createHash('sha256').update(WIDGET_HTML).digest('hex').slice(0, 10)}.html`;
const WIDGET_DOMAINS = ['https://nuevaliving.com', 'https://fonts.googleapis.com', 'https://fonts.gstatic.com'];
// The base map is read with range requests from this site's own archive (CORS headers in netlify.toml).
const WIDGET_CONNECT = ['https://nuevaliving.com'];
const WIDGET_DESCRIPTION = 'Nueva Living development cards with photos, list prices, delivery and a map, filters that narrow the search, a detail view with the homes on the price list, and a form to ask an advisor.';
const WIDGET_META = {
  ui: { prefersBorder: true, csp: { resourceDomains: WIDGET_DOMAINS, connectDomains: WIDGET_CONNECT } },
  'openai/widgetCSP': { resource_domains: WIDGET_DOMAINS, connect_domains: WIDGET_CONNECT },
  'openai/widgetPrefersBorder': true,
  'openai/widgetDescription': WIDGET_DESCRIPTION,
};
function toolMeta(invoking, invoked) {
  return {
    ui: { resourceUri: WIDGET_URI },
    'ui/resourceUri': WIDGET_URI,
    'openai/outputTemplate': WIDGET_URI,
    'openai/widgetAccessible': true,
    'openai/toolInvocation/invoking': invoking,
    'openai/toolInvocation/invoked': invoked,
  };
}

// What the server is, its tools and the caveats on its data. Facts only: the Claude directory review
// (November 2026) asked for no directives aimed at the assistant and no contact channels here.
const INSTRUCTIONS = [
  'Nueva Living is an independent advisory for new-build and off-plan homes on the Costa del Sol, Spain, from Torremolinos to Casares.',
  'Tools: search_developments returns up to six developments that fit a brief, with suggestions that narrow it; get_development returns one development\'s details and the homes on its price list; request_details returns Nueva Living\'s enquiry form for chosen developments, which the person fills in and sends themselves. No tool sends personal details.',
  'Prices are the developers\' list prices in EUR before Spanish VAT (IVA) and purchase costs unless the price note says otherwise, and are reconfirmed by Nueva Living before any reservation.',
  'Images are mostly computer-generated renders from the developer, not photographs of the finished building. Map positions are approximate.',
  'Sizes are the developer\'s own figures: built area where given, otherwise interior; each result\'s size.basis says which ("mixed" when the price list uses both). Size searches allow 10% either side, as developers measure differently.',
  'The language parameter returns names, prices and dates in English, Spanish, French, German, Russian, Arabic, Dutch, Polish, Swedish or Norwegian. features takes requirements such as sea_view or private_pool; wishes takes free text in any language.',
  'Where the client supports MCP Apps, results are also shown as cards with photos, a map and the enquiry form.',
].join(' ');

// --- small helpers ---------------------------------------------------------------------------

function fold(value) {
  return String(value || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase()
    .replace(/[^a-z0-9Ѐ-ӿ؀-ۿ]+/g, ' ').trim();
}

function words(value) {
  return fold(value).split(' ').filter((w) => w.length > 2);
}

function lang(value) {
  return LANGUAGES.includes(value) ? value : 'en';
}

function areaName(slug, language) {
  const area = catalog.areas.find((a) => a.slug === slug);
  return area ? (area.names[language] || area.names.en) : slug;
}

// Wishes arrive in the person's language, so every language's own wording is searched: "havsutsikt"
// finds what the Swedish page says, "vue mer" what the French one does.
function haystack(project) {
  const parts = [project.area, project.tags.join(' ')];
  for (const l of Object.values(project.locales)) {
    parts.push(l.name, l.location, l.type, l.summary, l.description, l.locationNote, l.why);
  }
  for (const a of catalog.areas.filter((x) => x.slug === project.area)) parts.push(...Object.values(a.names));
  return fold(parts.join(' '));
}

const HAYSTACKS = new Map(catalog.projects.map((p) => [p.slug, haystack(p)]));

// Wishes that name a feature, in the ten site languages (folded: no accents, lower case). An
// assistant should put these in `features`, but a person's own words often arrive in `wishes`
// ("egen pool", "vistas al mar"); a project with the feature then ranks first. Words every project
// shares ("pool", "golf" in Estepona) would otherwise decide the order on their own.
const WISH_FEATURES = {
  private_pool: ['egen pool', 'privat pool', 'private pool', 'own pool', 'piscina privada', 'piscine privee', 'privatpool', 'eigener pool', 'eigenem pool', 'prive zwembad', 'privezwembad', 'eigen zwembad', 'prywatny basen', 'prywatnym basenem', 'частныи бассеин', 'собственныи бассеин', 'مسبح خاص', 'privat basseng', 'eget basseng'],
  sea_view: ['havsutsikt', 'havutsikt', 'sea view', 'ocean view', 'vistas al mar', 'vista al mar', 'vue mer', 'vue sur la mer', 'meerblick', 'zeezicht', 'uitzicht op zee', 'widok na morze', 'вид на море', 'اطلالة على البحر'],
  beach: ['nara stranden', 'vid stranden', 'near the beach', 'beachfront', 'walk to the beach', 'cerca de la playa', 'primera linea', 'pres de la plage', 'strandnah', 'am strand', 'nabij het strand', 'aan het strand', 'blisko plazy', 'у пляжа', 'рядом с пляжем', 'قرب الشاطئ', 'naer stranden', 'nær stranden'],
  golf: ['golf', 'гольф', 'غولف'],
  gated: ['inhagnat', 'gated', 'urbanizacion cerrada', 'residence fermee', 'bewachte', 'afgesloten', 'osiedle zamkniete', 'закрыт', 'inngjerdet', 'مسور'],
  gym: ['gym', 'gimnasio', 'salle de sport', 'fitness', 'silownia', 'спортзал', 'treningsrom', 'صالة رياضية'],
  spa: ['spa', 'sauna', 'спа'],
  garden: ['tradgard', 'garden', 'jardin', 'garten', 'tuin', 'ogrod', 'сад', 'hage', 'حديقة'],
  rooftop: ['takterrass', 'rooftop', 'roof terrace', 'solarium', 'dachterrasse', 'dakterras', 'toit-terrasse', 'toit terrasse', 'taras na dachu', 'терраса на крыше', 'takterrasse'],
  lift: ['hiss', 'elevator', 'ascensor', 'ascenseur', 'aufzug', 'winda', 'лифт', 'مصعد', 'heis'],
  indoor_pool: ['inomhuspool', 'indoor pool', 'piscina cubierta', 'piscine interieure', 'innenpool', 'hallenbad', 'binnenzwembad', 'kryty basen', 'крытыи бассеин', 'مسبح داخلي', 'innendors basseng'],
  mountain_view: ['bergsutsikt', 'mountain view', 'vistas a la montana', 'vue montagne', 'bergblick', 'bergzicht', 'widok na gory', 'вид на горы', 'fjellutsikt'],
};
const WISH_PHRASES = Object.entries(WISH_FEATURES).map(([feature, phrases]) => [feature, phrases.map(fold)]);

function wishedFeatures(wishes) {
  const text = ` ${fold(wishes)} `;
  if (!text.trim()) return [];
  return WISH_PHRASES.filter(([, phrases]) => phrases.some((p) => text.includes(` ${p} `) || text.includes(` ${p}`))).map(([f]) => f);
}

// How much a wish word says: one most projects contain ranks almost nothing.
function wordWeight(word) {
  let n = 0;
  for (const hay of HAYSTACKS.values()) if (hay.includes(word)) n += 1;
  return n / HAYSTACKS.size > 0.4 ? 0.1 : 1;
}

// A place the person names: an area slug or name in any language, or a place mentioned on a
// project's own page (Nueva Andalucía, New Golden Mile, La Cala de Mijas...).
// Several places in one request ("Estepona or Marbella", "Mijas, Fuengirola") match any of them.
function locationParts(location) {
  return String(location || '')
    .split(/[,;/|]|\s(?:or|and|o|y|ou|et|oder|und|of|en|eller|och|lub|i|или|и|أو|و)\s/i)
    .map((part) => part.trim())
    .filter(Boolean);
}

function matchesLocation(project, location) {
  const parts = locationParts(location);
  if (parts.length > 1) return parts.some((part) => matchesPlace(project, part));
  return matchesPlace(project, location);
}

function matchesPlace(project, location) {
  const wanted = fold(location);
  if (!wanted || /^(costa del sol|spain|espana|andalucia|malaga)$/.test(wanted)) return true;
  const area = catalog.areas.find((a) => a.slug === project.area);
  if (area && Object.values(area.names).some((n) => fold(n) === wanted || fold(n).includes(wanted))) return true;
  if (fold(project.area).includes(wanted)) return true;
  const en = project.locales.en;
  return fold(`${en.location} ${en.name} ${project.tags.join(' ')}`).includes(wanted);
}

function overlapsBudget(project, min, max) {
  const low = project.priceMin;
  const high = project.priceMax || project.priceMin;
  if (low == null) return !max && !min;
  if (max && low > max) return false;
  if (min && high < min) return false;
  return true;
}

function card(project, language, matching) {
  const l = project.locales[language] || project.locales.en;
  return {
    slug: project.slug,
    name: l.name,
    area: areaName(project.area, language),
    location: l.location,
    type: l.type,
    from: l.from,
    priceRange: l.priceRange || null,
    priceMinEur: project.priceMin,
    priceMaxEur: project.priceMax,
    bedrooms: project.bedroomsMin == null ? null
      : project.bedroomsMin === project.bedroomsMax || project.bedroomsMax == null
        ? `${project.bedroomsMin}` : `${project.bedroomsMin}-${project.bedroomsMax}`,
    stage: project.status,
    delivery: l.delivery || null,
    summary: l.summary,
    features: project.features,
    size: sizeSummary(project),
    homesListed: project.homes.length,
    homesMatching: matching ? matching.count : null,
    fromMatchingEur: matching ? matching.from : null,
    image: project.image,
    map: project.coordinates ? { lat: project.coordinates[0], lng: project.coordinates[1], approximate: true } : null,
    url: l.url,
  };
}

// The homes on a project's price list that fit the budget and bedrooms, when the list prices them.
// A project whose list prices nothing ("on request") is judged by its range instead.
// Size is the developer's figure (built where given, otherwise interior) and developers measure
// differently, so a size range is widened by SIZE_MARGIN either side, as on the website's filter.
const SIZE_MARGIN = 0.1;
function sizeFits(sqm, args) {
  if (!args.size_min && !args.size_max) return true;
  if (sqm == null) return false;
  if (args.size_min && sqm < args.size_min * (1 - SIZE_MARGIN)) return false;
  if (args.size_max && sqm > args.size_max * (1 + SIZE_MARGIN)) return false;
  return true;
}

// The homes on a project's price list that fit the budget, bedrooms and size, when the list prices them.
// A project whose list prices nothing ("on request") is judged by its range instead.
function homesMatching(project, args) {
  const sized = Boolean(args.size_min || args.size_max);
  const priced = project.homes.filter((h) => h.priceEur != null || (sized && h.sqm != null));
  if (!priced.length || !(args.budget_min || args.budget_max || args.bedrooms_min || sized)) return null;
  const fit = priced.filter((h) => (!args.budget_max || (h.priceEur != null && h.priceEur <= args.budget_max))
    && (!args.budget_min || (h.priceEur != null && h.priceEur >= args.budget_min))
    && (!args.bedrooms_min || h.bedrooms == null || h.bedrooms >= args.bedrooms_min)
    && sizeFits(h.sqm, args));
  const prices = fit.map((h) => h.priceEur).filter((n) => n != null);
  return { count: fit.length, from: prices.length ? Math.min(...prices) : null };
}

// "78-106 m²" and whether that is built area, interior, or a mix of the two across the list.
function sizeSummary(project) {
  const sized = project.homes.filter((h) => h.sqm != null);
  if (!sized.length) return null;
  const sizes = sized.map((h) => h.sqm);
  const low = Math.min(...sizes);
  const high = Math.max(...sizes);
  const bases = new Set(sized.map((h) => h.sizeBasis));
  return { range: low === high ? `${low} m²` : `${low}-${high} m²`, basis: bases.size > 1 ? 'mixed' : [...bases][0] };
}

function suggestions(pool, args) {
  const out = [];
  const areas = [...new Set(pool.map((p) => p.area))];
  if (!args.location && areas.length > 1) out.push({ narrow_by: 'location', options: areas.slice(0, 6).map((a) => areaName(a, lang(args.language))) });
  const types = [...new Set(pool.flatMap((p) => p.propertyTypes))];
  if (!args.property_type && types.length > 1) out.push({ narrow_by: 'property_type', options: types });
  if (!args.budget_max) {
    const prices = pool.map((p) => p.priceMin).filter(Boolean).sort((a, b) => a - b);
    if (prices.length > 3) out.push({ narrow_by: 'budget_max', options: [prices[Math.floor(prices.length / 3)], prices[Math.floor((2 * prices.length) / 3)]].map((n) => Math.ceil(n / 100000) * 100000) });
  }
  if (!args.stage) {
    const stages = [...new Set(pool.map((p) => p.status).filter(Boolean))];
    if (stages.length > 1) out.push({ narrow_by: 'stage', options: stages });
  }
  return out;
}

// --- tools -----------------------------------------------------------------------------------

const TOOLS = [
  {
    name: 'search_developments',
    title: 'Search Nueva Living developments',
    description: 'Searches the new-build developments Nueva Living advises on along the Costa del Sol (Marbella, Estepona, Benahavís, Casares, Mijas and nearby). Returns up to six best matches with name, area, type, list price from, bedrooms, construction stage, expected delivery, a photo and the page link, whether more matches exist, and suggestions that narrow the search. Prices are EUR list prices before VAT and purchase costs.',
    inputSchema: {
      type: 'object',
      properties: {
        location: { type: 'string', maxLength: 120, description: 'Town, area or neighbourhood in the person\'s words, e.g. "Marbella", "Estepona", "Nueva Andalucía", "New Golden Mile", "Benahavís". Several places separated by commas match any of them: "Estepona, Marbella".' },
        budget_min: { type: 'integer', minimum: 0, description: 'EUR, total purchase price.' },
        budget_max: { type: 'integer', minimum: 0, description: 'EUR, total purchase price, inclusive.' },
        bedrooms_min: { type: 'integer', minimum: 0, maximum: 10 },
        size_min: { type: 'integer', minimum: 20, maximum: 5000, description: 'Square metres. The developer\'s own figure is used (built area where given, otherwise interior) with a 10% margin, as developers measure differently.' },
        size_max: { type: 'integer', minimum: 20, maximum: 5000, description: 'Square metres, as size_min.' },
        property_type: { type: 'string', enum: PROPERTY_TYPES },
        stage: { type: 'string', enum: STAGES, description: 'off_plan = sold before or at the start of construction; under_construction; completed = key ready.' },
        features: { type: 'array', maxItems: 8, items: { type: 'string', enum: FEATURES }, description: 'Required features; every one listed must be named on the development\'s page. beach = beachfront or walking distance to the beach.' },
        wishes: { type: 'string', maxLength: 300, description: 'Anything else that ranks the results, in the person\'s own words and language: "quiet", "family", "investment", "walk to restaurants".' },
        language: { type: 'string', enum: LANGUAGES, description: 'Language of the person. Names, prices and dates come back in it. Default en.' },
      },
      additionalProperties: false,
    },
    annotations: { title: 'Search Nueva Living developments', readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false },
    _meta: toolMeta('Searching Nueva Living developments…', 'Found the best matches'),
  },
  {
    name: 'get_development',
    title: 'Get development details',
    description: 'Full details of one development by its slug from a search result: description, location and drive times, delivery, price range and the note on what the prices include, the homes on the price list with bedrooms, size, price and the floor plan link where the page has one, up to eight images, approximate map position, which documents the page offers (floor plans, video, virtual tour, quality specifications) and the page link and its enquiry form.',
    inputSchema: {
      type: 'object',
      properties: {
        slug: { type: 'string', minLength: 2, maxLength: 80, description: 'Development slug from search_developments, e.g. "valle-romano-crest-villas".' },
        language: { type: 'string', enum: LANGUAGES },
      },
      required: ['slug'],
      additionalProperties: false,
    },
    annotations: { title: 'Get development details', readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false },
    _meta: toolMeta('Opening the development…', 'Development details ready'),
  },
  {
    name: 'request_details',
    title: 'Ask a Nueva Living advisor to get in touch',
    // Sends nothing. It opens Nueva Living's enquiry form for the chosen developments; the person
    // types their own name and e-mail and presses Send, which posts straight to this server's
    // enquiry route without passing through the model (Claude directory review, November 2026:
    // a confirmation the model cannot set). Without MCP Apps the person gets the page link instead.
    description: 'Opens Nueva Living\'s enquiry form for the developments the person chose. The person types their own name and e-mail and sends the form themselves; this tool sends no personal details. Returns the form for the host to show and the development page where the same form is available.',
    inputSchema: {
      type: 'object',
      properties: {
        slugs: { type: 'array', minItems: 1, maxItems: 6, items: { type: 'string' }, description: 'Developments the person is asking about, as slugs from search_developments.' },
        language: { type: 'string', enum: LANGUAGES },
      },
      required: ['slugs'],
      additionalProperties: false,
    },
    annotations: { title: 'Ask a Nueva Living advisor to get in touch', readOnlyHint: false, destructiveHint: true, idempotentHint: false, openWorldHint: true },
    _meta: toolMeta('Opening the enquiry form…', 'Enquiry form ready'),
  },
];

function searchDevelopments(args) {
  const language = lang(args.language);
  const features = (Array.isArray(args.features) ? args.features : []).filter((f) => FEATURES.includes(f));
  let pool = catalog.projects.filter((p) => p.priceMin != null || p.locales.en.from);
  if (args.location) pool = pool.filter((p) => matchesLocation(p, args.location));
  const locationFound = pool.length > 0;
  if (args.property_type) pool = pool.filter((p) => p.propertyTypes.includes(args.property_type));
  if (args.stage) pool = pool.filter((p) => p.status === args.stage);
  if (features.length) pool = pool.filter((p) => features.every((f) => p.features.includes(f)));
  if (args.bedrooms_min) pool = pool.filter((p) => (p.bedroomsMax ?? p.bedroomsMin ?? 0) >= args.bedrooms_min);

  // Budget and bedrooms are judged home by home where the price list prices its homes, so a project
  // whose range overlaps the budget but whose remaining homes do not is left out.
  const matches = new Map();
  pool = pool.filter((p) => {
    const m = homesMatching(p, args);
    if (m) { matches.set(p.slug, m); return m.count > 0; }
    if (args.size_min || args.size_max) return false;
    return !(args.budget_min || args.budget_max) || overlapsBudget(p, args.budget_min, args.budget_max);
  });

  const wishes = words(args.wishes).map((w) => [w, wordWeight(w)]);
  const wished = wishedFeatures(args.wishes).filter((f) => !features.includes(f));
  const scored = pool.map((p) => {
    const hay = HAYSTACKS.get(p.slug);
    const score = wished.reduce((sum, f) => sum + (p.features.includes(f) ? 5 : 0), 0)
      + wishes.reduce((sum, [w, weight]) => sum + (hay.includes(w) ? weight : 0), 0);
    return { p, score };
  }).sort((a, b) => b.score - a.score || (a.p.priceMin || 9e12) - (b.p.priceMin || 9e12));

  // The price list does not say which type each home is, so in a project that mixes types a count
  // of homes in budget would include the wrong ones when a type is asked for. It is left off there.
  const shown = (p) => (args.property_type && p.propertyTypes.length > 1 ? null : matches.get(p.slug));
  const results = scored.slice(0, MAX_RESULTS).map(({ p }) => card(p, language, shown(p)));
  const out = {
    kind: 'search',
    language,
    query: { ...args, features, language },
    understood_wishes: wished,
    results,
    total: scored.length,
    more_matches: scored.length > MAX_RESULTS,
    refine: scored.length > MAX_RESULTS ? suggestions(scored.map((s) => s.p), args) : [],
    note: 'List prices in EUR before VAT and purchase costs; availability and prices are reconfirmed by Nueva Living before reservation. Images are mostly renders; map positions are approximate.',
  };
  if (!results.length) {
    out.message = !locationFound
      ? `Nueva Living does not currently advise on a development in "${args.location}". Areas covered: ${catalog.areas.map((a) => a.names[language] || a.names.en).join(', ')}.`
      : 'No development fits every criterion together; each of budget, bedrooms, type, stage and features narrows the results.';
  }
  // No record of what was asked: the Claude directory policy (1E) rules out keeping conversation
  // data even for logging, so only the fact of a call is counted.
  console.log('mcp search');
  return out;
}

function getDevelopment(args) {
  const language = lang(args.language);
  const project = catalog.projects.find((p) => p.slug === String(args.slug || '').trim());
  if (!args.slug) return { error: 'slug is required: the slug of a development as given in search_developments results.' };
  if (!project) return { error: `No development has the slug "${args.slug}". Slugs are the ones given in search_developments results.` };
  const l = project.locales[language] || project.locales.en;
  console.log('mcp details');
  return {
    kind: 'development',
    language,
    ...card(project, language),
    description: l.description,
    why: l.why,
    availability: l.availability,
    price_note: l.priceNote,
    checked: l.checked,
    homes: l.units,
    location_note: l.locationNote,
    distances: l.distances,
    images: l.images,
    images_note: l.mediaNote,
    documents: l.documents,
    tags: project.tags,
    enquire: l.url,
    contact: { enquiry_form: l.url, email: ADVISOR.email },
  };
}

// The tool the model can call: no personal details in, none sent. The form it opens is sent by the
// person, through the route in the handler below.
function enquiryForm(args) {
  const language = lang(args.language);
  const projects = (Array.isArray(args.slugs) ? args.slugs : []).map((slug) => catalog.projects.find((p) => p.slug === slug)).filter(Boolean);
  if (!projects.length) return { error: 'No development has those slugs. Slugs are the ones given in search_developments results.' };
  const first = projects[0];
  const l = first.locales[language] || first.locales.en;
  console.log('mcp form');
  return {
    kind: 'enquiry_form',
    language,
    sent: false,
    slug: first.slug,
    slugs: projects.map((p) => p.slug),
    name: l.name,
    developments: projects.map((p) => (p.locales[language] || p.locales.en).name),
    enquire: l.url,
  };
}

// Leads are the one write. A function instance lives for minutes to hours, so this counter is a
// brake on a loop inside one conversation, not a defence against a determined sender; the CRM's
// own spam rules (lib/lead-spam.js, via nueva-lead) still apply to everything that passes.
const recent = new Map();
function tooMany(key) {
  const now = Date.now();
  const hits = (recent.get(key) || []).filter((t) => now - t < 3600e3);
  hits.push(now);
  recent.set(key, hits);
  return hits.length > 5;
}

// Where an enquiry came from, as the CRM records it. The chat on the site (nueva-chat.js) passes its own.
const MCP_CHANNEL = { label: 'an AI assistant (MCP connector)', page: '/mcp', consentPlace: 'an AI assistant conversation', utm: 'ai-assistant' };
const WIDGET_CHANNEL = { label: 'the enquiry form in an AI assistant (MCP connector)', page: '/mcp', consentPlace: 'the Nueva Living enquiry form shown in an AI assistant', utm: 'ai-assistant' };

async function requestDetails(args, event, channel = MCP_CHANNEL) {
  if (args.consent !== true) {
    return { sent: false, error: 'Not sent: the consent box was not ticked.' };
  }
  const email = String(args.email || '').trim();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return { sent: false, error: 'That e-mail address is not valid.' };
  const ip = event.headers['x-nf-client-connection-ip'] || event.headers['x-forwarded-for'] || 'unknown';
  if (tooMany(`${ip}|${email.toLowerCase()}`)) return { sent: false, error: 'Not sent: several enquiries were sent from here in the last hour.' };

  const projects = (args.slugs || [])
    .map((slug) => catalog.projects.find((p) => p.slug === slug))
    .filter(Boolean);
  const names = projects.map((p) => p.locales.en.name);
  const message = [
    String(args.message || '').trim(),
    names.length ? `Developments: ${names.join(', ')}` : '',
    `Sent from ${channel.label}, language ${lang(args.language)}.`,
  ].filter(Boolean).join(' ');

  const result = await lead.handler({
    httpMethod: 'POST',
    headers: { 'content-type': 'application/json', 'user-agent': event.headers['user-agent'] || '', 'x-nf-client-connection-ip': ip },
    body: JSON.stringify({
      first_name: args.first_name,
      last_name: args.last_name,
      email,
      phone: args.phone || '',
      message,
      project: names[0] || '',
      budget_max: args.budget_max || '',
      preferred_areas: [...new Set(projects.map((p) => p.area))],
      property_types: [...new Set(projects.flatMap((p) => p.propertyTypes))],
      consent: true,
      consent_text: `Agreed in ${channel.consentPlace} to be contacted by Nueva Living and for these details to be stored for that purpose`,
      source_page: channel.page,
      utm_source: channel.utm,
    }),
  });
  if (result.statusCode >= 400) {
    console.error('MCP lead not accepted', { status: result.statusCode, body: String(result.body).slice(0, 200) });
    return { sent: false, error: 'Not sent: the enquiry could not be delivered just now. The same form is on the development page.' };
  }
  console.log('mcp lead');
  return { kind: 'request', sent: true, message: 'Sent. A Nueva Living advisor will reply by e-mail, normally within one working day.' };
}

// --- JSON-RPC over HTTP ------------------------------------------------------------------------

const HEADERS = {
  'Content-Type': 'application/json',
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'Content-Type, Accept, Authorization, Mcp-Session-Id, Mcp-Protocol-Version',
  'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
  'Cache-Control': 'no-store',
};

function reply(statusCode, body) {
  return { statusCode, headers: HEADERS, body: body === undefined ? '' : JSON.stringify(body) };
}

function rpcResult(id, result) {
  return reply(200, { jsonrpc: '2.0', id, result });
}

function rpcError(id, code, message) {
  return reply(200, { jsonrpc: '2.0', id: id ?? null, error: { code, message } });
}

function toolResult(data) {
  const isError = Boolean(data.error);
  return { content: [{ type: 'text', text: JSON.stringify(data) }], structuredContent: data, isError };
}

// The chat on the site runs the same three tools with the same rules (nueva-chat.js).
exports.shared = { TOOLS, INSTRUCTIONS, ADVISOR, LANGUAGES, catalog, searchDevelopments, getDevelopment, requestDetails };

exports.handler = async (event) => {
  if (event.httpMethod === 'OPTIONS') return reply(204);
  if (event.httpMethod === 'GET') {
    // No server-to-client stream: the spec's answer is 405. A browser landing here gets a pointer.
    return { statusCode: 405, headers: { ...HEADERS, Allow: 'POST', 'Content-Type': 'text/plain; charset=utf-8' }, body: 'Nueva Living MCP server. Add https://nuevaliving.com/mcp as a connector in Claude or ChatGPT.\n' };
  }
  if (event.httpMethod !== 'POST') return reply(405, { error: 'Method not allowed' });

  let message;
  try {
    message = JSON.parse(event.isBase64Encoded ? Buffer.from(event.body || '', 'base64').toString('utf8') : event.body || '');
  } catch {
    return rpcError(null, -32700, 'Parse error');
  }
  // The enquiry form's Send button, pressed by the person in the card view. It is not JSON-RPC and
  // not a tool: a model calling tools cannot reach it, so an enquiry needs the person's own click.
  if (message && message.kind === 'enquiry' && message.jsonrpc === undefined) {
    const result = await requestDetails(message, event, WIDGET_CHANNEL);
    return reply(result.sent ? 200 : 400, result);
  }
  if (Array.isArray(message)) return rpcError(null, -32600, 'Batches are not supported');
  if (!message || message.jsonrpc !== '2.0' || typeof message.method !== 'string') return rpcError(message?.id, -32600, 'Invalid request');

  const { id, method, params = {} } = message;
  // Notifications (initialized, cancelled...) carry no id and get no body.
  if (id === undefined || id === null) return reply(202);

  try {
    switch (method) {
      case 'initialize': {
        const asked = params.protocolVersion;
        return rpcResult(id, {
          protocolVersion: PROTOCOL_VERSIONS.includes(asked) ? asked : PROTOCOL_VERSIONS[0],
          capabilities: { tools: { listChanged: false }, resources: { listChanged: false } },
          serverInfo: SERVER_INFO,
          instructions: INSTRUCTIONS,
        });
      }
      case 'ping':
        return rpcResult(id, {});
      case 'tools/list':
        return rpcResult(id, { tools: TOOLS });
      case 'resources/list':
        return rpcResult(id, { resources: [{ uri: WIDGET_URI, name: 'Nueva Living view', title: 'Nueva Living view', description: WIDGET_DESCRIPTION, mimeType: 'text/html;profile=mcp-app', _meta: WIDGET_META }] });
      case 'resources/read':
        if (!/^ui:\/\/nueva-living\/view(-[0-9a-f]+)?\.html$/.test(params.uri || '')) return rpcError(id, -32002, 'Resource not found');
        return rpcResult(id, { contents: [{ uri: params.uri, mimeType: 'text/html;profile=mcp-app', text: WIDGET_HTML, _meta: WIDGET_META }] });
      case 'resources/templates/list':
        return rpcResult(id, { resourceTemplates: [] });
      case 'prompts/list':
        return rpcResult(id, { prompts: [] });
      case 'tools/call': {
        const args = params.arguments || {};
        if (params.name === 'search_developments') return rpcResult(id, toolResult(searchDevelopments(args)));
        if (params.name === 'get_development') return rpcResult(id, toolResult(getDevelopment(args)));
        if (params.name === 'request_details') return rpcResult(id, toolResult(enquiryForm(args)));
        return rpcError(id, -32602, `Unknown tool: ${params.name}`);
      }
      default:
        return rpcError(id, -32601, `Method not found: ${method}`);
    }
  } catch (error) {
    console.error('MCP request failed', { method, message: error.message });
    return rpcError(id, -32603, 'Internal error');
  }
};
