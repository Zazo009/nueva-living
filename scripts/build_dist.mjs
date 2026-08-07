import fs from 'node:fs';
import path from 'node:path';
import { createHash } from 'node:crypto';
import vm from 'node:vm';

const root = process.cwd();
const dist = path.join(root, 'dist');
const projectsDir = path.join(root, 'content/liora-projects');
const areas = JSON.parse(fs.readFileSync(path.join(root, 'content/nueva-areas.json'), 'utf8'));
const fontCss = fs.readFileSync(path.join(root, 'assets/fonts/google/liora-fonts.css'), 'utf8');
function contentVersion(relativePath) {
  return createHash('sha256')
    .update(fs.readFileSync(path.join(root, relativePath)))
    .digest('hex')
    .slice(0, 12);
}

const conversionScriptPath = 'assets/liora/liora-conversion.js';
const discoveryScriptPath = 'assets/liora/liora-discovery.js';
const cardGalleryScriptPath = 'assets/liora/liora-card-gallery.js';
const trackingScriptPath = 'assets/liora/nueva-tracking.js';
const shortlistScriptPath = 'assets/liora/nueva-shortlist.js';
const shortlistStylesheetPath = 'assets/liora/nueva-shortlist.css';
const compareScriptPath = 'assets/liora/liora-compare.js';
const compareStylesheetPath = 'assets/liora/liora-compare.css';
const navInteractionsStylesheetPath = 'assets/liora/nueva-nav-interactions.css';
const newsletterStylesheetPath = 'assets/liora/nueva-newsletter.css';
const systemStylesheetPath = 'assets/liora/nueva-system.css';
const pagesStylesheetPath = 'assets/liora/liora-pages.css';
const propertyStylesheetPath = 'assets/liora/liora-property.css';
const conversionScriptVersion = contentVersion(conversionScriptPath);
const discoveryScriptVersion = contentVersion(discoveryScriptPath);
const cardGalleryScriptVersion = contentVersion(cardGalleryScriptPath);
const trackingScriptVersion = contentVersion(trackingScriptPath);
const shortlistScriptVersion = contentVersion(shortlistScriptPath);
const shortlistStylesheetVersion = contentVersion(shortlistStylesheetPath);
const compareScriptVersion = contentVersion(compareScriptPath);
const compareStylesheetVersion = contentVersion(compareStylesheetPath);
const navInteractionsStylesheetVersion = contentVersion(navInteractionsStylesheetPath);
const newsletterStylesheetVersion = contentVersion(newsletterStylesheetPath);
const systemStylesheetVersion = contentVersion(systemStylesheetPath);
const pagesStylesheetVersion = contentVersion(pagesStylesheetPath);
const propertyStylesheetVersion = contentVersion(propertyStylesheetPath);

const baseHtmlFiles = [
  '404.html',
  'about.html',
  'contact.html',
  'advisory.html',
  'why-nueva.html',
  'areas.html',
  ...areas.map((area) => area.output),
  'compare.html',
  'cookie-policy.html',
  'developments.html',
  'guides.html',
  'legal-notice.html',
  'new-build-apartments-penthouses-marbella.html',
  'new-build-apartments-penthouses-estepona.html',
  'new-build-apartments-penthouses-nueva-andalucia.html',
  'privacy-policy.html',
  'referrals.html',
  'thank-you.html',
];

const siteUrl = 'https://nuevaliving.com';
const socialImage = `${siteUrl}/assets/liora/viewing/scene-08.jpg`;
const fontPreloadBlock = [
  '  <link rel="preload" href="assets/fonts/google/8vIJ7ww63mVu7gt79mT7PkRXMw.woff2" as="font" type="font/woff2" crossorigin>',
  '  <link rel="preload" href="assets/fonts/google/JTUSjIg1_i6t8kCHKm459WlhyyTh89Y.woff2" as="font" type="font/woff2" crossorigin>'
].join('\n');
const basePageMeta = {
  'index.html': {
    title: 'Nueva Living | Costa del Sol New Developments',
    description: 'Find and compare new-build homes across Marbella, Estepona, Benahavis and the wider Costa del Sol with personal buyer support.',
    path: '/',
    type: 'website',
    schema: [
      {
        '@context': 'https://schema.org',
        '@type': 'RealEstateAgent',
        name: 'Nueva Living',
        legalName: 'LIORA LIVING SL.',
        taxID: 'B88827472',
        url: siteUrl,
        email: 'contact@nuevaliving.com',
        areaServed: ['Marbella', 'Estepona', 'Benahavis', 'Costa del Sol'],
        knowsAbout: ['New developments', 'Off-plan property', 'Luxury real estate advisory']
      },
      {
        '@context': 'https://schema.org',
        '@type': 'Organization',
        name: 'Nueva Living',
        legalName: 'LIORA LIVING SL.',
        url: siteUrl,
        logo: `${siteUrl}/assets/liora/brand/nueva-living-lockup-espresso-transparent.png`,
        email: 'contact@nuevaliving.com',
        telephone: '+34645446624',
        address: {
          '@type': 'PostalAddress',
          streetAddress: 'Avenida del Prado 71',
          postalCode: '29660',
          addressLocality: 'Marbella',
          addressRegion: 'Malaga',
          addressCountry: 'ES'
        }
      },
      {
        '@context': 'https://schema.org',
        '@type': 'WebSite',
        name: 'Nueva Living',
        url: siteUrl
      }
    ]
  },
  'developments.html': {
    title: 'Costa del Sol New Developments | Nueva Living',
    description: 'Explore new developments across the Costa del Sol, chosen for their design, location and everyday appeal.',
    path: '/developments.html',
    type: 'website'
    // No `schema` here: developments.html already carries its own inline
    // CollectionPage JSON-LD, and seoBlock() does not strip existing
    // <script type="application/ld+json"> tags, so adding one here would
    // duplicate it in the built output.
  },
  'guides.html': {
    title: 'Costa del Sol Buying Guides | Nueva Living',
    description: 'Compare new-build apartments and penthouses by area across the Costa del Sol, with real prices, availability and local buying guidance from Nueva Living.',
    path: '/guides.html',
    type: 'website'
  },
  'new-build-apartments-penthouses-marbella.html': {
    title: 'New-Build Apartments & Penthouses in Marbella | Nueva Living',
    description: 'Compare new-build apartments and penthouses across Marbella’s Golf Valley, Elevated Coastline and Marbella West, with real prices, availability and floorplans from Nueva Living.',
    path: '/new-build-apartments-penthouses-marbella.html',
    type: 'website'
    // No `schema` here either: build_segment_pages.mjs already writes the
    // full CollectionPage/ItemList/BreadcrumbList/FAQPage JSON-LD inline.
  },
  'new-build-apartments-penthouses-estepona.html': {
    title: 'New-Build Apartments & Penthouses in Estepona | Nueva Living',
    description: 'Compare new-build apartments and penthouses in Estepona, from the New Golden Mile to the town centre, with real prices, availability and floorplans from Nueva Living.',
    path: '/new-build-apartments-penthouses-estepona.html',
    type: 'website'
  },
  'new-build-apartments-penthouses-nueva-andalucia.html': {
    title: 'New-Build Apartments & Penthouses in Nueva Andalucia | Nueva Living',
    description: 'Compare new-build apartments and penthouses in Nueva Andalucia\'s Golf Valley, minutes from Puerto Banus, with real prices, availability and floorplans from Nueva Living.',
    path: '/new-build-apartments-penthouses-nueva-andalucia.html',
    type: 'website'
  },
  'areas.html': {
    title: 'Costa del Sol Area Guide | Nueva Living',
    description: 'Compare Marbella, Estepona, Benahavis, Nueva Andalucia and nearby Costa del Sol areas before choosing a new-build home.',
    path: '/areas.html',
    type: 'article'
  },
  'why-nueva.html': {
    title: 'Why Choose Nueva Living | Costa del Sol Buyer Support',
    description: 'Local Costa del Sol insight, honest advice and a clear step-by-step process, from the first conversation through to handover.',
    path: '/why-nueva.html',
    type: 'website',
    schema: {
      '@context': 'https://schema.org',
      '@type': 'AboutPage',
      name: 'Why Choose Nueva Living',
      url: `${siteUrl}/why-nueva.html`,
      description: 'How Nueva Living supports international buyers comparing new developments on the Costa del Sol.'
    }
  },
  'advisory.html': {
    title: 'Costa del Sol Buyer Advisory | Nueva Living',
    description: 'Practical buyer support for comparing Costa del Sol new developments, developers, purchase steps and long-term suitability.',
    path: '/advisory.html',
    type: 'article',
    schema: {
      '@context': 'https://schema.org',
      '@type': 'FAQPage',
      mainEntity: [
        ['Can foreigners buy property in Spain?', 'Yes. There are no restrictions on non-Spanish nationals buying property in Spain, whether as a resident or non-resident.'],
        ['What is an NIE number and do I need one?', 'An NIE (Numero de Identificacion de Extranjero) is a tax ID number required for any property purchase in Spain by a non-Spanish national. Nueva Living can guide you through obtaining one before you reserve.'],
        ['What costs should I budget for on top of the purchase price?', 'Buyers typically budget for transfer tax or VAT, notary fees, land registry fees and legal fees on top of the purchase price. Nueva Living provides a full, current cost breakdown for your chosen residence before you reserve.'],
        ['Can I get a mortgage in Spain as a non-resident?', 'Many Spanish banks offer mortgages to non-resident buyers, typically financing a portion of the purchase price. Exact terms depend on the bank and your personal financial profile.'],
        ['What is the difference between off-plan and completed properties?', 'Off-plan means the development is still under construction and is usually sold with staged payments through to completion. A completed property is ready to view and move into now.'],
        ['How does the reservation and payment process work?', 'Reservation and payment structures vary by development and are set out in full before you reserve. Nueva Living reconfirms the current schedule for your chosen residence at every step.'],
        ['Can I rent out the property after purchase?', 'This depends on the individual development and local regulations, which can vary by community and municipality. Nueva Living will confirm the specific rules for a development before you reserve.'],
        ['Do I need a lawyer?', 'Yes, we strongly recommend independent legal representation for any property purchase in Spain. Nueva Living can put you in touch with independent lawyers experienced in Costa del Sol property.']
      ].map(([question, answer]) => ({
        '@type': 'Question',
        name: question,
        acceptedAnswer: { '@type': 'Answer', text: answer }
      }))
    }
  },
  'referrals.html': {
    title: 'Referral & Ambassador Program | Nueva Living',
    description: 'Introduce a friend to Nueva Living and receive a share of our commission when their Costa del Sol purchase completes.',
    path: '/referrals.html',
    type: 'article'
  },
  'about.html': {
    title: 'About Nueva Living | Costa del Sol New Development Advisory',
    description: 'Nueva Living helps international buyers find, compare and understand new developments across the Costa del Sol.',
    path: '/about.html',
    type: 'website'
  },
  'contact.html': {
    title: 'Contact Nueva Living | Costa del Sol New Developments',
    description: 'Tell us what you are looking for and receive a personal shortlist of Costa del Sol new developments that match your needs.',
    path: '/contact.html',
    type: 'website'
  },
  'privacy-policy.html': {
    title: 'Privacy Policy | Nueva Living',
    description: 'Privacy policy information for Nueva Living enquiries, buyer communication and website contact forms.',
    path: '/privacy-policy.html',
    robots: 'noindex,follow',
    type: 'website'
  },
  'legal-notice.html': {
    title: 'Legal Notice | Nueva Living',
    description: 'Legal notice and website-use information for Nueva Living.',
    path: '/legal-notice.html',
    robots: 'noindex,follow',
    type: 'website'
  },
  'cookie-policy.html': {
    title: 'Cookie Policy | Nueva Living',
    description: 'Cookie policy information for the Nueva Living website.',
    path: '/cookie-policy.html',
    robots: 'noindex,follow',
    type: 'website'
  },
  'thank-you.html': {
    title: 'Request Received | Nueva Living',
    description: 'Thank you for contacting Nueva Living. Your private new-development request has been received.',
    path: '/thank-you.html',
    robots: 'noindex,follow',
    type: 'website'
  },
  'compare.html': {
    title: 'Compare Your Shortlist | Nueva Living',
    description: 'Compare the Costa del Sol developments you have saved to your shortlist, side by side.',
    path: '/compare.html',
    robots: 'noindex,follow',
    type: 'website'
  },
  '404.html': {
    title: 'Page Not Found | Nueva Living',
    description: 'The requested Nueva Living page could not be found.',
    path: '/404.html',
    robots: 'noindex,follow',
    type: 'website'
  }
};

for (const area of areas) {
  basePageMeta[area.output] = {
    title: area.seo.title,
    description: area.seo.description,
    path: `/${area.output}`,
    type: 'article',
    image: `${siteUrl}/${area.hero.image}`,
    schema: {
      '@context': 'https://schema.org',
      '@type': 'CollectionPage',
      name: area.seo.title.replace(/ \| Nueva Living$/, ''),
      url: `${siteUrl}/${area.output}`,
      description: area.seo.description,
      about: {
        '@type': 'Place',
        name: area.name,
        containedInPlace: {
          '@type': 'AdministrativeArea',
          name: 'Costa del Sol, Malaga, Spain'
        }
      }
    }
  };
}

function loadProjectPages() {
  if (!fs.existsSync(projectsDir)) return [];

  return fs.readdirSync(projectsDir, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => path.join(projectsDir, entry.name, 'project.json'))
    .filter((file) => fs.existsSync(file))
    .map((file) => JSON.parse(fs.readFileSync(file, 'utf8')))
    .filter((project) => project.output && fs.existsSync(path.join(root, project.output)))
    .sort((a, b) => (a.card?.order ?? 999) - (b.card?.order ?? 999));
}

function projectAreaLabel(project) {
  const location = `${project.hero?.location || ''} ${project.schema?.areaServed || ''}`.toLowerCase();
  if (location.includes('nueva andaluc') || location.includes('nueva andalucía')) return 'Nueva Andalucia';
  if (location.includes('benahav')) return 'Benahavis';
  if (location.includes('estepona') || location.includes('new golden mile')) return 'Estepona';
  if (location.includes('mijas') || location.includes('fuengirola')) return 'Mijas & Fuengirola';
  if (location.includes('marbella east')) return 'Marbella East';
  return 'Marbella';
}

// Mirrors seoTitle() in build_property_pages.mjs -- leads with property
// type and area, since that is what buyers actually search for, not the
// project's own (often anonymized) name.
function projectSeoTitle(project) {
  const area = projectAreaLabel(project);
  const type = project.hero?.type || 'New Development';
  return `${type} in ${area} — ${project.shortName || project.name} | Nueva Living`;
}

const projectPages = loadProjectPages();
const htmlFiles = [
  ...baseHtmlFiles,
  ...projectPages.map((project) => project.output)
];

const pageMeta = {
  ...basePageMeta,
  ...Object.fromEntries(projectPages.map((project) => [
    project.output,
    {
      title: projectSeoTitle(project),
      description: project.seoDescription || project.description || `${project.name} new development preview by Nueva Living.`,
      path: `/${project.output}`,
      type: 'website'
    }
  ]))
};

const assetFiles = [
  'assets/liora/advisory-property.jpg',
  'assets/liora/apple-touch-icon.png',
  'assets/liora/favicon-16.png',
  'assets/liora/favicon-32.png',
  'assets/liora/liora-discovery.js',
  'assets/liora/liora-card-gallery.js',
  'assets/liora/liora-conversion.js',
  'assets/liora/nueva-tracking.js',
  'assets/liora/liora-favicon-512.png',
  'assets/liora/liora-pages.css',
  'assets/liora/liora-property.css',
  'assets/liora/liora-property.js',
  'assets/liora/nueva-newsletter.css',
  'assets/liora/nueva-nav-interactions.css',
  'assets/liora/nueva-shortlist.css',
  'assets/liora/nueva-shortlist.js',
  'assets/liora/liora-compare.css',
  'assets/liora/liora-compare.js',
  'assets/liora/nueva-system.css',
  'assets/liora/brand/nueva-living-hero-logo.png',
  'assets/liora/brand/nueva-living-hero-logo-sand.png',
  'assets/liora/brand/nueva-living-lockup-espresso.png',
  'assets/liora/brand/nueva-living-lockup-sand.png',
  'assets/liora/brand/nueva-living-hero-logo-transparent.png',
  'assets/liora/brand/nueva-living-hero-logo-sand-transparent.png',
  'assets/liora/brand/nueva-living-lockup-espresso-transparent.png',
  'assets/liora/brand/nueva-living-lockup-sand-transparent.png',
  'assets/liora/video/hero-desktop-v2.mp4',
  'assets/liora/video/hero-mobile-v2.mp4',
  'assets/vendor/gsap/gsap.min.js',
  'assets/vendor/gsap/ScrollTrigger.min.js',
];

const assetDirectories = [
  'assets/fonts/google',
  'assets/liora/areas',
  'assets/liora/cards',
  'assets/liora/data',
  'assets/liora/hero',
  'assets/liora/projects',
  'assets/liora/team',
  'assets/liora/viewing',
  'assets/nueva/advantages',
  'assets/nueva/journey',
  'content',
];

function copyFile(source, target) {
  fs.mkdirSync(path.dirname(target), { recursive: true });

  if (/\.(?:js|css)$/i.test(source)) {
    let lastError = null;

    for (let attempt = 0; attempt < 18; attempt += 1) {
      try {
        const firstRead = fs.readFileSync(source);
        Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, 90);
        const stableRead = fs.readFileSync(source);

        if (!firstRead.equals(stableRead)) {
          throw new Error(`Asset changed while being read: ${source}`);
        }
        if (/\.js$/i.test(source)) {
          new vm.Script(stableRead.toString('utf8'), { filename: source });
        }

        fs.writeFileSync(target, stableRead);
        const written = fs.readFileSync(target);
        if (!written.equals(stableRead)) {
          throw new Error(`Incomplete asset copy: ${source}`);
        }
        return;
      } catch (error) {
        lastError = error;
        Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, 120 * (attempt + 1));
      }
    }

    throw lastError || new Error(`Unable to copy stable asset: ${source}`);
  }

  const expectedSize = fs.statSync(source).size;
  let lastError = null;

  for (let attempt = 0; attempt < 3; attempt += 1) {
    try {
      fs.copyFileSync(source, target);
      if (fs.statSync(target).size === expectedSize) return;
      lastError = new Error(`Incomplete asset copy: ${source}`);
    } catch (error) {
      lastError = error;
    }

    // APFS/iCloud-backed folders can briefly cancel large synchronous copies.
    Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, 60 * (attempt + 1));
  }

  throw lastError || new Error(`Unable to copy asset: ${source}`);
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function absoluteUrl(file) {
  const meta = pageMeta[file];
  return `${siteUrl}${meta?.path || `/${file}`}`;
}

function seoBlock(file) {
  const meta = pageMeta[file];
  if (!meta) return '';
  const url = absoluteUrl(file);
  const shareImage = meta.image || socialImage;
  const lines = [
    `<link rel="canonical" href="${escapeHtml(url)}">`,
    meta.robots ? `<meta name="robots" content="${escapeHtml(meta.robots)}">` : '',
    `<meta property="og:site_name" content="Nueva Living">`,
    `<meta property="og:locale" content="en_US">`,
    `<meta property="og:type" content="${escapeHtml(meta.type || 'website')}">`,
    `<meta property="og:title" content="${escapeHtml(meta.title)}">`,
    `<meta property="og:description" content="${escapeHtml(meta.description)}">`,
    `<meta property="og:url" content="${escapeHtml(url)}">`,
    `<meta property="og:image" content="${escapeHtml(shareImage)}">`,
    `<meta name="twitter:card" content="summary_large_image">`,
    `<meta name="twitter:title" content="${escapeHtml(meta.title)}">`,
    `<meta name="twitter:description" content="${escapeHtml(meta.description)}">`,
    `<meta name="twitter:image" content="${escapeHtml(shareImage)}">`,
    meta.schema ? `<script type="application/ld+json">\n${JSON.stringify(meta.schema, null, 2)}\n  </script>` : ''
  ].filter(Boolean);
  return lines.map((line) => `  ${line}`).join('\n');
}

function stripSeo(html) {
  return html
    .replace(/\n\s*<link rel="canonical"[^>]*>/gi, '')
    .replace(/\n\s*<meta name="robots"[^>]*>/gi, '')
    .replace(/\n\s*<meta property="og:[^>]*>/gi, '')
    .replace(/\n\s*<meta name="twitter:[^>]*>/gi, '')
    .replace(/\n\s*<link rel="preconnect" href="https:\/\/fonts\.(?:googleapis|gstatic)\.com"[^>]*>/gi, '')
    .replace(/\n\s*<link href="https:\/\/fonts\.googleapis\.com[^>]*>/gi, '');
}

function injectFontPreloads(html) {
  if (!html.includes('assets/fonts/google/liora-fonts.css')) return html;
  const withoutLegacyPreloads = html.replace(
    /\n\s*<link rel="preload" href="assets\/fonts\/google\/(?:co3bmX5slCNuHLi8bLeY9MK7whWMhyjYqXtKky2F7g|8vIJ7ww63mVu7gt79mT7PkRXMw|JTUSjIg1_i6t8kCHKm459WlhyyTh89Y)\.woff2" as="font" type="font\/woff2" crossorigin>/gi,
    ''
  );
  return withoutLegacyPreloads.replace(
    /\n\s*<link rel="stylesheet" href="assets\/fonts\/google\/liora-fonts\.css">/i,
    `\n${fontPreloadBlock}\n  <link rel="stylesheet" href="assets/fonts/google/liora-fonts.css">`
  );
}

function inlineFontStyles(html) {
  if (!html.includes('assets/fonts/google/liora-fonts.css')) return html;
  const inlined = fontCss.replace(/url\(\.\//g, 'url(assets/fonts/google/');
  return html.replace(
    /<link rel="stylesheet" href="assets\/fonts\/google\/liora-fonts\.css">/i,
    `<style data-nueva-fonts>${inlined}</style>`
  );
}

function minifyCss(css) {
  let output = '';
  let quote = '';

  for (let index = 0; index < css.length; index += 1) {
    const char = css[index];
    const next = css[index + 1];

    if (quote) {
      output += char;
      if (char === '\\') {
        output += next || '';
        index += 1;
      } else if (char === quote) {
        quote = '';
      }
      continue;
    }

    if (char === '"' || char === "'") {
      quote = char;
      output += char;
      continue;
    }

    if (char === '/' && next === '*') {
      const end = css.indexOf('*/', index + 2);
      index = end === -1 ? css.length : end + 1;
      continue;
    }

    if (/\s/.test(char)) {
      let cursor = index + 1;
      while (cursor < css.length && /\s/.test(css[cursor])) cursor += 1;
      const before = output.at(-1) || '';
      const after = css[cursor] || '';
      if (before && after && !/[{}:;,]/.test(before) && !/[{}:;,]/.test(after)) output += ' ';
      index = cursor - 1;
      continue;
    }

    output += char;
  }

  return output.replace(/;}/g, '}').trim();
}

function minifyInlineStyles(html) {
  return html.replace(/<style([^>]*)>([\s\S]*?)<\/style>/gi, (_, attributes, css) => (
    `<style${attributes}>${minifyCss(css)}</style>`
  ));
}

function optimizeHtml(html) {
  return minifyInlineStyles(inlineFontStyles(html))
    // Assets are immutable in production, so content hashes ensure every CSS
    // and form-handler revision reaches both new and returning visitors.
    .replace(
      /assets\/liora\/liora-pages\.css(?:\?v=[a-z0-9]+)?/gi,
      `${pagesStylesheetPath}?v=${pagesStylesheetVersion}`
    )
    .replace(
      /assets\/liora\/liora-property\.css(?:\?v=[a-z0-9]+)?/gi,
      `${propertyStylesheetPath}?v=${propertyStylesheetVersion}`
    )
    .replace(
      /assets\/liora\/liora-compare\.css(?:\?v=[a-z0-9]+)?/gi,
      `${compareStylesheetPath}?v=${compareStylesheetVersion}`
    )
    .replace(
      /assets\/liora\/liora-compare\.js(?:\?v=[a-z0-9]+)?/gi,
      `${compareScriptPath}?v=${compareScriptVersion}`
    )
    .replace(
      /assets\/liora\/nueva-system\.css(?:\?v=[a-z0-9]+)?/gi,
      `${systemStylesheetPath}?v=${systemStylesheetVersion}`
    )
    .replace(
      /assets\/liora\/liora-conversion\.js(?:\?v=[a-z0-9]+)?/gi,
      `${conversionScriptPath}?v=${conversionScriptVersion}`
    )
    .replace(
      /assets\/liora\/liora-discovery\.js(?:\?v=[a-z0-9]+)?/gi,
      `${discoveryScriptPath}?v=${discoveryScriptVersion}`
    )
    .replace(
      /assets\/liora\/liora-card-gallery\.js(?:\?v=[a-z0-9]+)?/gi,
      `${cardGalleryScriptPath}?v=${cardGalleryScriptVersion}`
    );
}

function injectSeo(html, file) {
  const meta = pageMeta[file];
  if (!meta) return html;

  let next = stripSeo(html)
    .replace(/<title>[\s\S]*?<\/title>/i, `<title>${escapeHtml(meta.title)}</title>`)
    .replace(/<meta name="description" content="[^"]*"\s*\/?>/i, `<meta name="description" content="${escapeHtml(meta.description)}">`)
    .replace(/nueva-living-home\.html/g, 'index.html');

  if (!next.includes('assets/fonts/google/liora-fonts.css')) {
    next = next.replace(
      /(\n\s*<link rel="stylesheet" href="assets\/liora\/liora-pages\.css">)/,
      `\n${fontPreloadBlock}\n  <link rel="stylesheet" href="assets/fonts/google/liora-fonts.css">$1`
    );
  }
  next = injectFontPreloads(next);

  const block = seoBlock(file);
  if (block) {
    next = next.replace(/(<meta name="description" content="[^"]*"\s*\/?>)/i, `$1\n${block}`);
  }
  return next;
}

function injectConversion(html) {
  if (html.includes('assets/liora/liora-conversion.js')) return html;
  return html.replace(
    /\n<\/body>/i,
    '\n  <script src="assets/liora/liora-conversion.js" defer></script>\n</body>'
  );
}

function injectTracking(html) {
  if (html.includes(trackingScriptPath)) return html;
  return html.replace(
    /\n<\/head>/i,
    `\n  <script src="${trackingScriptPath}?v=${trackingScriptVersion}" defer></script>\n</head>`
  );
}

function injectShortlist(html) {
  let next = html;
  if (!next.includes(shortlistStylesheetPath)) {
    next = next.replace(
      /\n<\/head>/i,
      `\n  <link rel="stylesheet" href="${shortlistStylesheetPath}?v=${shortlistStylesheetVersion}" media="print" onload="this.media='all'">\n  <noscript><link rel="stylesheet" href="${shortlistStylesheetPath}?v=${shortlistStylesheetVersion}"></noscript>\n</head>`
    );
  }
  if (!next.includes(shortlistScriptPath)) {
    next = next.replace(
      /\n<\/body>/i,
      `\n  <script src="${shortlistScriptPath}?v=${shortlistScriptVersion}" defer></script>\n</body>`
    );
  }
  return next;
}

function injectNavInteractions(html) {
  if (html.includes(navInteractionsStylesheetPath)) return html;
  return html.replace(
    /\n<\/head>/i,
    `\n  <link rel="stylesheet" href="${navInteractionsStylesheetPath}?v=${navInteractionsStylesheetVersion}" media="print" onload="this.media='all'">\n  <noscript><link rel="stylesheet" href="${navInteractionsStylesheetPath}?v=${navInteractionsStylesheetVersion}"></noscript>\n</head>`
  );
}

function injectSystemStyles(html) {
  if (html.includes(systemStylesheetPath)) return html;
  return html.replace(
    /\n<\/head>/i,
    `\n  <link rel="stylesheet" href="${systemStylesheetPath}?v=${systemStylesheetVersion}">\n</head>`
  );
}

const newsletterMarkup = `    <section class="footer-newsletter" aria-labelledby="footer-newsletter-title">
      <div class="footer-newsletter-copy">
        <span class="footer-newsletter-kicker">Private Updates</span>
        <h2 id="footer-newsletter-title">The coast, carefully edited.</h2>
        <p>Occasional notes on new releases, meaningful availability and the developments worth knowing about.</p>
      </div>
      <form class="footer-newsletter-form" name="nueva-newsletter" method="POST" action="/.netlify/functions/nueva-lead" data-crm-lead data-newsletter-form data-submitting-label="Subscribing..." data-success-label="Subscribed" data-submitting-message="Adding you to Nueva Living updates..." data-success-message="You are on the list. We will only send updates worth opening." data-error-message="We could not subscribe you just now. Please email contact@nuevaliving.com.">
        <input type="hidden" name="request_context" value="Newsletter signup">
        <input type="hidden" name="message" value="Newsletter subscription request">
        <input type="hidden" name="consent" value="true">
        <input type="hidden" name="consent_text" value="I agree to receive occasional Nueva Living project updates and for my data to be stored">
        <label class="footer-newsletter-honeypot" aria-hidden="true">Website<input name="website" tabindex="-1" autocomplete="off"></label>
        <div class="footer-newsletter-fields">
          <label class="footer-newsletter-field">
            <span>First name</span>
            <input name="first_name" type="text" autocomplete="given-name" placeholder="First name" required>
          </label>
          <label class="footer-newsletter-field">
            <span>Last name</span>
            <input name="last_name" type="text" autocomplete="family-name" placeholder="Last name" required>
          </label>
          <label class="footer-newsletter-field footer-newsletter-field--email">
            <span>Email address</span>
            <input name="email" type="email" autocomplete="email" inputmode="email" placeholder="you@email.com" required>
          </label>
          <button class="footer-newsletter-submit" type="submit">Subscribe</button>
        </div>
        <div class="footer-newsletter-meta">
          <label class="footer-newsletter-consent">
            <input name="marketing_opt_in" type="checkbox" required>
            <span>I agree to receive occasional Nueva Living updates. Unsubscribe at any time. See our <a href="privacy-policy.html">Privacy Policy</a>.</span>
          </label>
          <span class="form-response" aria-live="polite"></span>
        </div>
      </form>
    </section>`;

function injectNewsletter(html) {
  let next = html;
  if (!next.includes(newsletterStylesheetPath)) {
    next = next.replace(
      /\n<\/head>/i,
      `\n  <link rel="stylesheet" href="${newsletterStylesheetPath}?v=${newsletterStylesheetVersion}" media="print" onload="this.media='all'">\n  <noscript><link rel="stylesheet" href="${newsletterStylesheetPath}?v=${newsletterStylesheetVersion}"></noscript>\n</head>`
    );
  }
  if (!next.includes('data-newsletter-form') && /<footer(?:\s[^>]*)?>/i.test(next)) {
    // The last footer is the page footer; earlier matches may be semantic
    // attribution elements inside testimonials.
    const footerMatches = [...next.matchAll(/<footer(?:\s[^>]*)?>/gi)];
    const siteFooter = footerMatches.at(-1);
    if (siteFooter) {
      const insertAt = siteFooter.index + siteFooter[0].length;
      next = `${next.slice(0, insertAt)}\n${newsletterMarkup}${next.slice(insertAt)}`;
    }
  }
  return next;
}

// Conservative, dependency-free JS minifier: strips comments and collapses
// whitespace while tracking string/template-literal state so nothing inside
// quotes is ever touched. Does not attempt regex-literal detection -- safe
// for this codebase today (verified no regex literals in the homepage
// controller), but a future edit that adds one should re-check this.
function minifyJs(js) {
  let output = '';
  let quote = '';
  let lineHasContent = false;

  for (let index = 0; index < js.length; index += 1) {
    const char = js[index];
    const next = js[index + 1];

    if (quote) {
      output += char;
      if (char === '\\') {
        output += next || '';
        index += 1;
      } else if (char === quote) {
        quote = '';
      }
      continue;
    }

    if (char === '"' || char === "'" || char === '`') {
      quote = char;
      output += char;
      lineHasContent = true;
      continue;
    }

    if (char === '/' && next === '/') {
      const end = js.indexOf('\n', index + 2);
      index = end === -1 ? js.length : end - 1;
      continue;
    }

    if (char === '/' && next === '*') {
      const end = js.indexOf('*/', index + 2);
      index = end === -1 ? js.length : end + 1;
      continue;
    }

    if (char === '\n') {
      if (lineHasContent) output += '\n';
      lineHasContent = false;
      continue;
    }

    if (char === ' ' || char === '\t') {
      let cursor = index + 1;
      while (cursor < js.length && (js[cursor] === ' ' || js[cursor] === '\t')) cursor += 1;
      if (lineHasContent && cursor < js.length && js[cursor] !== '\n') output += ' ';
      index = cursor - 1;
      continue;
    }

    output += char;
    lineHasContent = true;
  }

  return output.trim();
}

function externalizeHomepageController(html, publicName) {
  if (publicName !== 'index.html') return html;

  const controllerPattern = /<script>\s*(document\.addEventListener\('DOMContentLoaded',[\s\S]*?)\s*<\/script>/;
  const match = html.match(controllerPattern);
  if (!match) throw new Error('Homepage controller script was not found');

  const controller = `${minifyJs(match[1].trim())}\n`;
  const controllerVersion = createHash('sha256')
    .update(controller)
    .digest('hex')
    .slice(0, 12);
  const target = path.join(dist, 'assets/liora/nueva-homepage.js');
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.writeFileSync(target, controller);

  return html.replace(
    controllerPattern,
    `<script src="assets/liora/nueva-homepage.js?v=${controllerVersion}" defer></script>`
  );
}

function writeHtml(source, target, publicName) {
  const html = fs.readFileSync(source, 'utf8');
  fs.mkdirSync(path.dirname(target), { recursive: true });
  const productionHtml = externalizeHomepageController(
    injectSystemStyles(injectNavInteractions(injectShortlist(injectNewsletter(injectConversion(injectTracking(injectSeo(html, publicName))))))),
    publicName
  );
  fs.writeFileSync(target, optimizeHtml(productionHtml));
}

function copyDirectory(source, target) {
  if (!fs.existsSync(source)) return;

  for (const entry of fs.readdirSync(source, { withFileTypes: true })) {
    if (entry.name === '.DS_Store') continue;
    if (entry.name.endsWith('.remote.css')) continue;

    const sourcePath = path.join(source, entry.name);
    const targetPath = path.join(target, entry.name);

    if (entry.isDirectory()) {
      copyDirectory(sourcePath, targetPath);
      continue;
    }

    copyFile(sourcePath, targetPath);
  }
}

fs.rmSync(dist, { recursive: true, force: true });
fs.mkdirSync(dist, { recursive: true });

console.log('Building HTML pages...');
for (const file of htmlFiles) {
  writeHtml(path.join(root, file), path.join(dist, file), file);
}

writeHtml(
  path.join(root, 'nueva-living-home.html'),
  path.join(dist, 'index.html'),
  'index.html',
);

console.log('Copying core assets...');
for (const file of assetFiles) {
  console.log(`- ${file}`);
  copyFile(path.join(root, file), path.join(dist, file));
}

console.log('Copying asset directories...');
for (const directory of assetDirectories) {
  console.log(`- ${directory}`);
  copyDirectory(path.join(root, directory), path.join(dist, directory));
}

console.log('Cleaning duplicate artifacts...');
for (const entry of fs.readdirSync(dist, { withFileTypes: true })) {
  if (/\s[23](?:\..*)?$/.test(entry.name)) {
    fs.rmSync(path.join(dist, entry.name), { recursive: true, force: true });
  }
}

console.log('Writing deploy metadata...');
const metadata = `# Nueva Living deploy package

Generated: ${new Date().toISOString()}

For a simple static preview, deploy the contents of this dist folder.

For production lead capture with Marbella CRM, deploy the repository with netlify.toml so Netlify also deploys:
- netlify/functions/nueva-lead.js
- netlify/functions/nueva-track.js

Entry point:
- index.html

Included:
- current live HTML pages
- assets/
- content/

Excluded:
- old preview folders
- handoff zips
- artifacts
- legacy logo previews
- local working notes
`;

fs.writeFileSync(path.join(dist, 'README.md'), metadata);

const sitemapLastmod = new Date().toISOString().slice(0, 10);

const sitemapEntries = Object.entries(pageMeta)
  .filter(([, meta]) => meta.robots !== 'noindex,follow')
  .map(([file, meta]) => {
    const priority = file === 'index.html' ? '1.0' : file === 'developments.html' ? '0.9' : file.startsWith('property-') ? '0.85' : file.startsWith('new-build-') ? '0.8' : '0.7';
    return [
      '  <url>',
      `<loc>${siteUrl}${meta.path}</loc>`,
      `<lastmod>${sitemapLastmod}</lastmod>`,
      '<changefreq>weekly</changefreq>',
      `<priority>${priority}</priority>`,
      '</url>'
    ].join('');
  })
  .join('\n');

fs.writeFileSync(
  path.join(dist, 'sitemap.xml'),
  [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    sitemapEntries,
    '</urlset>',
    ''
  ].join('\n')
);

fs.writeFileSync(path.join(dist, 'robots.txt'), `User-agent: *\nAllow: /\nSitemap: ${siteUrl}/sitemap.xml\n`);

const legacyRedirects = [
  '/liora-approach.html /why-nueva.html 301',
  '/approach.html /why-nueva.html 301',
  '/liora-developments.html /developments.html 301',
  '/liora-areas.html /areas.html 301',
  '/liora-advisory.html /advisory.html 301',
  '/liora-about.html /about.html 301',
  '/liora-access.html /contact.html 301',
  '/liora-privacy-policy.html /privacy-policy.html 301',
  '/liora-legal-notice.html /legal-notice.html 301',
  '/liora-cookie-policy.html /cookie-policy.html 301',
];

fs.writeFileSync(path.join(dist, '_redirects'), `${legacyRedirects.join('\n')}\n/* /404.html 404\n`);

fs.writeFileSync(path.join(dist, '_headers'), `/*.html
  Cache-Control: public, max-age=0, must-revalidate

/assets/*
  Cache-Control: public, max-age=31536000, immutable

/sitemap.xml
  Cache-Control: public, max-age=3600

/robots.txt
  Cache-Control: public, max-age=3600
`);

console.log(`Created clean deploy folder: ${dist}`);
