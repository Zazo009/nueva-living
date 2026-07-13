import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const dist = path.join(root, 'dist');
const projectsDir = path.join(root, 'content/liora-projects');

const baseHtmlFiles = [
  '404.html',
  'about.html',
  'contact.html',
  'advisory.html',
  'approach.html',
  'areas.html',
  'cookie-policy.html',
  'developments.html',
  'legal-notice.html',
  'privacy-policy.html',
  'thank-you.html',
];

const siteUrl = 'https://nueva-living.com';
const socialImage = `${siteUrl}/assets/liora/viewing/scene-08.jpg`;
const fontPreloadBlock = [
  '  <link rel="preload" href="assets/fonts/google/co3bmX5slCNuHLi8bLeY9MK7whWMhyjYqXtKky2F7g.woff2" as="font" type="font/woff2" crossorigin>',
  '  <link rel="preload" href="assets/fonts/google/8vIJ7ww63mVu7gt79mT7PkRXMw.woff2" as="font" type="font/woff2" crossorigin>',
  '  <link rel="preload" href="assets/fonts/google/JTUSjIg1_i6t8kCHKm459WlhyyTh89Y.woff2" as="font" type="font/woff2" crossorigin>'
].join('\n');
const basePageMeta = {
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
  'developments.html': {
    title: 'Costa del Sol New Developments | Nueva Living',
    description: 'Explore curated Costa del Sol new developments selected for architecture, lifestyle, location logic and long-term value.',
    path: '/developments.html',
    type: 'website',
    schema: {
      '@context': 'https://schema.org',
      '@type': 'CollectionPage',
      name: 'Costa del Sol New Developments',
      url: `${siteUrl}/developments.html`,
      description: 'Curated new-development projects across the Costa del Sol.'
    }
  },
  'areas.html': {
    title: 'Costa del Sol Area Guide | Nueva Living',
    description: 'A refined Costa del Sol area guide for new-development buyers comparing Marbella, Estepona, Benahavis, Nueva Andalucia and surrounding areas.',
    path: '/areas.html',
    type: 'article'
  },
  'approach.html': {
    title: 'New Development Advisory Approach | Nueva Living',
    description: 'How Nueva Living structures a clearer, more selective advisory process for Costa del Sol new-development buyers.',
    path: '/approach.html',
    type: 'article'
  },
  'advisory.html': {
    title: 'Costa del Sol Buyer Advisory | Nueva Living',
    description: 'Buyer-focused advisory for evaluating Costa del Sol new developments, developer context, reservation strategy and long-term lifestyle logic.',
    path: '/advisory.html',
    type: 'article'
  },
  'about.html': {
    title: 'About Nueva Living | Costa del Sol New Development Advisory',
    description: 'Nueva Living is a Costa del Sol new-development advisory brand focused on curated access, discretion and clear buyer guidance.',
    path: '/about.html',
    type: 'website'
  },
  'contact.html': {
    title: 'Request Private Access | Nueva Living',
    description: 'Request a private shortlist of curated Costa del Sol new-development opportunities matched to your brief, area preferences and ownership goals.',
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
  '404.html': {
    title: 'Page Not Found | Nueva Living',
    description: 'The requested Nueva Living page could not be found.',
    path: '/404.html',
    robots: 'noindex,follow',
    type: 'website'
  }
};

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
      title: `${project.name} | Nueva Living`,
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
  'assets/liora/cards',
  'assets/liora/hero',
  'assets/liora/video',
  'assets/liora/viewing',
  'content',
];

function copyFile(source, target) {
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.writeFileSync(target, fs.readFileSync(source));
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

function injectFontPreloads(html) {
  if (!html.includes('assets/fonts/google/liora-fonts.css')) return html;
  if (html.includes('co3bmX5slCNuHLi8bLeY9MK7whWMhyjYqXtKky2F7g.woff2')) return html;
  return html.replace(
    /\n\s*<link rel="stylesheet" href="assets\/fonts\/google\/liora-fonts\.css">/i,
    `\n${fontPreloadBlock}\n  <link rel="stylesheet" href="assets/fonts/google/liora-fonts.css">`
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
    const priority = file === 'index.html' ? '1.0' : file === 'developments.html' ? '0.9' : file.startsWith('property-') ? '0.85' : '0.7';
    return [
      '  <url>',
      `<loc>${siteUrl}${meta.path}</loc>`,
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
  '/liora-approach.html /approach.html 301',
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
