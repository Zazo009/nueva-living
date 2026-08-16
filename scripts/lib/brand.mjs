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
  streetAddress: 'Avenida del Prado 71',
  postalCode: '29660',
  addressLocality: 'Marbella',
  addressRegion: 'Malaga',
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
    ...IDENTITY,
    url: siteUrl,
    logo: `${siteUrl}/assets/liora/brand/nueva-living-lockup-espresso-transparent.png`,
    address: ADDRESS,
    ...(SAME_AS.length ? { sameAs: SAME_AS } : {}),
    ...extra
  };
}
