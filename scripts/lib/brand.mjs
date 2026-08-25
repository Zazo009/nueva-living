// Who the company is, in one place.
//
// These facts were written out twice -- once in build_dist.mjs for the
// static pages and again in build_property_pages.mjs for the 84 property
// pages -- and the two had already drifted: the property pages' agent
// schema carried no address, phone or logo. Structured data is exactly
// where drift hurts, because Google reads it as an assertion about the
// business and inconsistent assertions are worth less than none.

export const SAME_AS = [
  // Profiles that corroborate this is the same company. `sameAs` is the
  // property Google uses to tell an entity apart from one with a nearly
  // identical name -- which is the practical problem here, with another
  // firm called "Nuva Living" ranking for the brand query.
  //
  // Anything left out is simply not claimed; add URLs as they exist.
  'https://www.instagram.com/nuevaliving',
  // Google Business Profile, the officially issued share link. For a local
  // business this is the strongest claim here: Instagram corroborates the
  // name, this corroborates the name, the Marbella address and the phone
  // together -- the same address asserted below.
  'https://maps.app.goo.gl/AVKXU8m9sL7LA5uK6'
  // Still unclaimed:
  //   'https://www.linkedin.com/company/<slug>/',
  //   'https://www.facebook.com/<page>/'
];

export const ADDRESS = {
  '@type': 'PostalAddress',
  // Matched word for word to the Google Business Profile, which reads
  // "Av. del Prado, 71, Nueva Andalucía, 29660 Marbella, Málaga". The district
  // was missing here, and NAP consistency across the profile, the schema and
  // any directory listing is what lets Google treat them as one business
  // rather than two similar ones -- the whole point of the brand-SERP work.
  streetAddress: 'Avenida del Prado 71, Nueva Andalucía',
  postalCode: '29660',
  addressLocality: 'Marbella',
  addressRegion: 'Málaga',
  addressCountry: 'ES'
};

const IDENTITY = {
  name: 'Nueva Living',
  legalName: 'LIORA LIVING SL.',
  taxID: 'B88827472',
  email: 'contact@nuevaliving.com',
  telephone: '+34645446624'
};

/**
 * @param {string} siteUrl  e.g. https://nuevaliving.com
 * @param {object} [extra]  type-specific properties (areaServed, knowsAbout…)
 */
export function realEstateAgentSchema(siteUrl, extra = {}) {
  return {
    '@context': 'https://schema.org',
    '@type': 'RealEstateAgent',
    '@id': organizationId(siteUrl),
    ...IDENTITY,
    url: `${siteUrl}/`,
    logo: `${siteUrl}/assets/liora/brand/nueva-living-lockup-espresso-transparent.png`,
    address: ADDRESS,
    ...(SAME_AS.length ? { sameAs: SAME_AS } : {}),
    ...extra
  };
}

export function organizationSchema(siteUrl, extra = {}) {
  return {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    '@id': organizationId(siteUrl),
    ...IDENTITY,
    url: siteUrl,
    logo: `${siteUrl}/assets/liora/brand/nueva-living-lockup-espresso-transparent.png`,
    address: ADDRESS,
    ...(SAME_AS.length ? { sameAs: SAME_AS } : {}),
    ...extra
  };
}

// The two founders, for Person schema on /about. Every field here is stated
// on that page in visible copy -- name, role, email and phone -- so the
// structured data asserts nothing the page does not already say. That is the
// point of it: the audit found the site does not rank for its own brand
// name, with two similarly named firms occupying the space, and named people
// tied to the organisation are one of the signals that separates one entity
// from another.
// `slug` gives each founder a stable @id on /about.html, so every page that
// names them points at one entity instead of minting a fresh Person each
// time. Google treats repeated un-@id'd Person blocks as separate people,
// which splits exactly the reputation signal these are here to build.
//
// `photo` is the real headshot already on the page -- E-E-A-T asks who is
// behind advice about a purchase this size, and an image in the markup that
// the structured data never mentions answers that only to a human reader.
//
// `sameAs` stays empty until real profile URLs exist. An unclaimed profile is
// better than a wrong one: sameAs is a claim of identity, and a guess that
// resolves to someone else is worse than saying nothing.
export const FOUNDERS = [
  {
    slug: 'sasan-raftari',
    name: 'Sasan Raftari',
    jobTitle: 'Founder',
    email: 'sasan@nuevaliving.com',
    telephone: '+46707576709',
    photo: 'assets/liora/team/sasan-raftari-founder.jpg',
    // The specifics matter more than the adjectives here: "17 years" and the
    // named roles are checkable claims, which is what E-E-A-T asks of the
    // person signing pages about tax rates and guarantee law.
    description: 'Founder of Nueva Living. Seventeen years in sales, around ten of them in digital as a product manager, ecommerce manager and head of digital, now applied to new-build property on the Costa del Sol.',
    knowsAbout: [
      'New-build property on the Costa del Sol',
      'Off-plan purchase process',
      'Ecommerce and digital product management',
      'Property search technology'
    ],
    sameAs: []
  },
  {
    slug: 'sami-altun',
    name: 'Sami Altun',
    jobTitle: 'Co-Founder',
    email: 'sami@nuevaliving.com',
    telephone: '+34645446624',
    photo: 'assets/liora/team/sami-altun-co-founder.jpg',
    knowsAbout: [
      'New-build property on the Costa del Sol',
      'Business development',
      'Property investment appraisal'
    ],
    sameAs: []
  }
];

// One canonical node id for the company. Every schema block that refers to
// Nueva Living points here rather than restating the facts, so the graph
// describes one organisation instead of a dozen similar ones.
// Who signs the buying guides. These pages state tax rates, statutory
// guarantee periods and warranty law -- the class of content Google's raters
// are told to check for a named, accountable author. An unsigned page asserts
// the same facts with nobody behind them.
export const GUIDE_AUTHOR = FOUNDERS[0];

export function organizationId(siteUrl) {
  return `${siteUrl}/#organization`;
}

export function personId(siteUrl, person) {
  return `${siteUrl}/about.html#${person.slug}`;
}

export function personSchemas(siteUrl) {
  return FOUNDERS.map((person) => ({
    '@context': 'https://schema.org',
    '@type': 'Person',
    '@id': personId(siteUrl, person),
    name: person.name,
    jobTitle: person.jobTitle,
    email: person.email,
    telephone: person.telephone,
    image: `${siteUrl}/${person.photo}`,
    ...(person.description ? { description: person.description } : {}),
    ...(person.knowsAbout?.length ? { knowsAbout: person.knowsAbout } : {}),
    ...(person.sameAs?.length ? { sameAs: person.sameAs } : {}),
    workLocation: ADDRESS,
    worksFor: { '@id': organizationId(siteUrl) },
    url: `${siteUrl}/about.html`,
    mainEntityOfPage: `${siteUrl}/about.html`
  }));
}

// Names the site itself, distinct from the company. Without it the homepage
// asserted the business but never the website as an entity.
export function webSiteSchema(siteUrl) {
  return {
    '@context': 'https://schema.org',
    '@type': 'WebSite',
    name: IDENTITY.name,
    url: `${siteUrl}/`,
    publisher: { '@type': 'Organization', name: IDENTITY.name, url: siteUrl }
  };
}
