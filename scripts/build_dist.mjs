import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const dist = path.join(root, 'dist');

const htmlFiles = [
  '404.html',
  'liora-about.html',
  'liora-access.html',
  'liora-advisory.html',
  'liora-approach.html',
  'liora-areas.html',
  'liora-cookie-policy.html',
  'liora-developments.html',
  'liora-legal-notice.html',
  'liora-privacy-policy.html',
  'property-altos-de-marbella.html',
  'thank-you.html',
];

const siteUrl = 'https://nueva-living.com';
const socialImage = `${siteUrl}/assets/liora/viewing/scene-08.jpg`;
const pageMeta = {
  'index.html': {
    title: 'Nueva Living | Curated Costa del Sol New Developments',
    description: 'Private new-development advisory for design-led residences across Marbella, Estepona, Benahavis and the wider Costa del Sol.',
    path: '/',
    type: 'website',
    schema: {
      '@context': 'https://schema.org',
      '@type': 'RealEstateAgent',
      name: 'Nueva Living',
      url: siteUrl,
      email: 'contact@nueva-living.com',
      areaServed: ['Marbella', 'Estepona', 'Benahavis', 'Costa del Sol'],
      knowsAbout: ['New developments', 'Off-plan property', 'Luxury real estate advisory']
    }
  },
  'liora-developments.html': {
    title: 'Costa del Sol New Developments | Nueva Living',
    description: 'Explore curated Costa del Sol new developments selected for architecture, lifestyle, location logic and long-term value.',
    path: '/liora-developments.html',
    type: 'website',
    schema: {
      '@context': 'https://schema.org',
      '@type': 'CollectionPage',
      name: 'Costa del Sol New Developments',
      url: `${siteUrl}/liora-developments.html`,
      description: 'Curated new-development projects across the Costa del Sol.'
    }
  },
  'property-altos-de-marbella.html': {
    title: 'Altos de Marbella Residences | Marbella East New Development',
    description: 'Altos de Marbella Residences is a curated Marbella East new-development preview with elevated sea-facing homes from EUR 1,250,000.',
    path: '/property-altos-de-marbella.html',
    type: 'website'
  },
  'liora-areas.html': {
    title: 'Costa del Sol Area Guide | Nueva Living',
    description: 'A refined Costa del Sol area guide for new-development buyers comparing Marbella, Estepona, Benahavis, Nueva Andalucia and surrounding areas.',
    path: '/liora-areas.html',
    type: 'article'
  },
  'liora-approach.html': {
    title: 'New Development Advisory Approach | Nueva Living',
    description: 'How Nueva Living structures a clearer, more selective advisory process for Costa del Sol new-development buyers.',
    path: '/liora-approach.html',
    type: 'article'
  },
  'liora-advisory.html': {
    title: 'Costa del Sol Buyer Advisory | Nueva Living',
    description: 'Buyer-focused advisory for evaluating Costa del Sol new developments, developer context, reservation strategy and long-term lifestyle logic.',
    path: '/liora-advisory.html',
    type: 'article'
  },
  'liora-about.html': {
    title: 'About Nueva Living | Costa del Sol New Development Advisory',
    description: 'Nueva Living is a Costa del Sol new-development advisory brand focused on curated access, discretion and clear buyer guidance.',
    path: '/liora-about.html',
    type: 'website'
  },
  'liora-access.html': {
    title: 'Request Private Access | Nueva Living',
    description: 'Request a private shortlist of curated Costa del Sol new-development opportunities matched to your brief, area preferences and ownership goals.',
    path: '/liora-access.html',
    type: 'website'
  },
  'liora-privacy-policy.html': {
    title: 'Privacy Policy | Nueva Living',
    description: 'Privacy policy information for Nueva Living enquiries, buyer communication and website contact forms.',
    path: '/liora-privacy-policy.html',
    robots: 'noindex,follow',
    type: 'website'
  },
  'liora-legal-notice.html': {
    title: 'Legal Notice | Nueva Living',
    description: 'Legal notice and website-use information for Nueva Living.',
    path: '/liora-legal-notice.html',
    robots: 'noindex,follow',
    type: 'website'
  },
  'liora-cookie-policy.html': {
    title: 'Cookie Policy | Nueva Living',
    description: 'Cookie policy information for the Nueva Living website.',
    path: '/liora-cookie-policy.html',
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
  '404.html': {
    title: 'Page Not Found | Nueva Living',
    description: 'The requested Nueva Living page could not be found.',
    path: '/404.html',
    robots: 'noindex,follow',
    type: 'website'
  }
};

const assetFiles = [
  'assets/liora/advisory-property.jpg',
  'assets/liora/apple-touch-icon.png',
  'assets/liora/favicon-16.png',
  'assets/liora/favicon-32.png',
  'assets/liora/liora-discovery.js',
  'assets/liora/liora-conversion.js',
  'assets/liora/liora-favicon-512.png',
  'assets/liora/liora-pages.css',
  'assets/liora/liora-property.css',
  'assets/liora/liora-property.js',
  'assets/liora/brand/nueva-living-hero-logo.png',
  'assets/liora/brand/nueva-living-hero-logo-sand.png',
  'assets/liora/brand/nueva-living-lockup-espresso.png',
  'assets/liora/brand/nueva-living-lockup-sand.png',
  'assets/liora/brand/nueva-living-hero-logo-transparent.png',
  'assets/liora/brand/nueva-living-hero-logo-sand-transparent.png',
  'assets/liora/brand/nueva-living-lockup-espresso-transparent.png',
  'assets/liora/brand/nueva-living-lockup-sand-transparent.png',
  'assets/vendor/gsap/gsap.min.js',
  'assets/vendor/gsap/ScrollTrigger.min.js',
];

const assetDirectories = [
  'assets/fonts/google',
  'assets/liora/areas',
  'assets/liora/video',
  'assets/liora/viewing',
  'content',
];

function copyFile(source, target) {
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.copyFileSync(source, target);
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
  const lines = [
    `<link rel="canonical" href="${escapeHtml(url)}">`,
    meta.robots ? `<meta name="robots" content="${escapeHtml(meta.robots)}">` : '',
    `<meta property="og:site_name" content="Nueva Living">`,
    `<meta property="og:locale" content="en_US">`,
    `<meta property="og:type" content="${escapeHtml(meta.type || 'website')}">`,
    `<meta property="og:title" content="${escapeHtml(meta.title)}">`,
    `<meta property="og:description" content="${escapeHtml(meta.description)}">`,
    `<meta property="og:url" content="${escapeHtml(url)}">`,
    `<meta property="og:image" content="${escapeHtml(socialImage)}">`,
    `<meta name="twitter:card" content="summary_large_image">`,
    `<meta name="twitter:title" content="${escapeHtml(meta.title)}">`,
    `<meta name="twitter:description" content="${escapeHtml(meta.description)}">`,
    `<meta name="twitter:image" content="${escapeHtml(socialImage)}">`,
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
      '\n  <link rel="stylesheet" href="assets/fonts/google/liora-fonts.css">$1'
    );
  }

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

function writeHtml(source, target, publicName) {
  const html = fs.readFileSync(source, 'utf8');
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.writeFileSync(target, injectConversion(injectSeo(html, publicName)));
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

for (const file of htmlFiles) {
  writeHtml(path.join(root, file), path.join(dist, file), file);
}

writeHtml(
  path.join(root, 'nueva-living-home.html'),
  path.join(dist, 'index.html'),
  'index.html',
);

for (const file of assetFiles) {
  copyFile(path.join(root, file), path.join(dist, file));
}

for (const directory of assetDirectories) {
  copyDirectory(path.join(root, directory), path.join(dist, directory));
}

for (const entry of fs.readdirSync(dist, { withFileTypes: true })) {
  if (/\s[23](?:\..*)?$/.test(entry.name)) {
    fs.rmSync(path.join(dist, entry.name), { recursive: true, force: true });
  }
}

const metadata = `# Nueva Living deploy package

Generated: ${new Date().toISOString()}

For a simple static preview, deploy the contents of this dist folder.

For production lead capture with Marbella CRM, deploy the repository with netlify.toml so Netlify also deploys:
- netlify/functions/liora-lead.js

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

const sitemapEntries = Object.entries(pageMeta)
  .filter(([, meta]) => meta.robots !== 'noindex,follow')
  .map(([file, meta]) => {
    const priority = file === 'index.html' ? '1.0' : file === 'liora-developments.html' ? '0.9' : file.startsWith('property-') ? '0.85' : '0.7';
    return `  <url><loc>${siteUrl}${meta.path}</loc><changefreq>weekly</changefreq><priority>${priority}</priority></url>`;
  })
  .join('\n');

fs.writeFileSync(path.join(dist, 'sitemap.xml'), `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${sitemapEntries}\n</urlset>\n`);

fs.writeFileSync(path.join(dist, 'robots.txt'), `User-agent: *\nAllow: /\nSitemap: ${siteUrl}/sitemap.xml\n`);

fs.writeFileSync(path.join(dist, '_redirects'), `/* /404.html 404\n`);

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
