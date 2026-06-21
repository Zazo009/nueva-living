import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();

const pages = [
  'Liora_Living_COLOR_SKETCH_HOME.html',
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
];

const homepage = path.join(root, 'Liora_Living_COLOR_SKETCH_HOME.html');
let homeHtml = fs.readFileSync(homepage, 'utf8');

const replacements = new Map([
  [
    'https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js',
    'assets/vendor/gsap/gsap.min.js',
  ],
  [
    'https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js',
    'assets/vendor/gsap/ScrollTrigger.min.js',
  ],
  [
    'https://images.unsplash.com/photo-1582268611958-ebfd161ef9cf?w=1800&auto=format&fit=crop&q=85',
    'assets/liora/viewing/scene-06.jpg',
  ],
  [
    'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=900&auto=format&fit=crop&q=85',
    'assets/liora/viewing/scene-06.jpg',
  ],
  [
    'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=900&auto=format&fit=crop&q=85',
    'assets/liora/viewing/scene-01.jpg',
  ],
  [
    'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=900&auto=format&fit=crop&q=85',
    'assets/liora/viewing/scene-04.jpg',
  ],
  [
    'https://commons.wikimedia.org/wiki/Special:FilePath/Early_morning_at_a_beach_in_Marbella%2C_Spain_%2829535666316%29.jpg?width=1200',
    'assets/liora/areas/marbella.jpg',
  ],
  [
    'https://commons.wikimedia.org/wiki/Special:FilePath/Playa_en_Estepona.jpg?width=1200',
    'assets/liora/areas/estepona.jpg',
  ],
  [
    'https://commons.wikimedia.org/wiki/Special:FilePath/Benahav%C3%ADs%2C_M%C3%A1laga%2C_Spain_-_panoramio_-_georama.jpg?width=1200',
    'assets/liora/areas/benahavis.jpg',
  ],
  [
    'https://commons.wikimedia.org/wiki/Special:FilePath/Los_Naranjos_Golf_Club.JPG?width=1200',
    'assets/liora/areas/nueva-andalucia.jpg',
  ],
  [
    'https://commons.wikimedia.org/wiki/Special:FilePath/Playa_de_los_Boliches%2C_Fuengirola.jpg?width=1200',
    'assets/liora/areas/fuengirola.jpg',
  ],
  [
    'https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=900&auto=format&fit=crop&q=85',
    'assets/liora/viewing/scene-13.jpg',
  ],
]);

for (const [remote, local] of replacements) {
  homeHtml = homeHtml.replaceAll(remote, local);
}

homeHtml = homeHtml
  .replace(/ title="[^"]*Wikimedia Commons"/g, '')
  .replace(
    /<img src="data:image\/jpeg;base64,[^"]+" alt="Solenne Benahavís new development exterior arrival" loading="lazy" \/>/,
    '<img src="assets/liora/viewing/scene-03.jpg" alt="Solenne Benahavís new development exterior arrival" loading="lazy" decoding="async" width="2048" height="1024" />',
  );

fs.writeFileSync(homepage, homeHtml);

const dimensionCache = new Map();

function getSvgDimensions(filePath) {
  const svg = fs.readFileSync(filePath, 'utf8');
  const width = svg.match(/\bwidth="([\d.]+)"/);
  const height = svg.match(/\bheight="([\d.]+)"/);
  if (width && height) {
    return { width: Math.round(Number(width[1])), height: Math.round(Number(height[1])) };
  }

  const viewBox = svg.match(/\bviewBox="[-\d.]+\s+[-\d.]+\s+([\d.]+)\s+([\d.]+)"/);
  if (viewBox) {
    return { width: Math.round(Number(viewBox[1])), height: Math.round(Number(viewBox[2])) };
  }

  return null;
}

function getRasterDimensions(filePath) {
  const output = execFileSync('sips', ['-g', 'pixelWidth', '-g', 'pixelHeight', filePath], {
    encoding: 'utf8',
  });
  const width = output.match(/pixelWidth:\s+(\d+)/);
  const height = output.match(/pixelHeight:\s+(\d+)/);
  if (!width || !height) return null;
  return { width: Number(width[1]), height: Number(height[1]) };
}

function getDimensions(src) {
  const cleanSrc = src.split(/[?#]/)[0];
  if (!cleanSrc || cleanSrc.startsWith('http') || cleanSrc.startsWith('data:')) return null;
  if (dimensionCache.has(cleanSrc)) return dimensionCache.get(cleanSrc);

  const filePath = path.join(root, cleanSrc);
  if (!fs.existsSync(filePath)) return null;

  const ext = path.extname(filePath).toLowerCase();
  const dimensions = ext === '.svg' ? getSvgDimensions(filePath) : getRasterDimensions(filePath);
  dimensionCache.set(cleanSrc, dimensions);
  return dimensions;
}

for (const page of pages) {
  const filePath = path.join(root, page);
  if (!fs.existsSync(filePath)) continue;

  let html = fs.readFileSync(filePath, 'utf8');
  const updated = html.replace(/<img\b(?=[^>]*\bsrc="([^"]+)")[^>]*>/g, (tag, src) => {
    const dimensions = getDimensions(src);
    if (!dimensions) return tag;

    let next = tag;
    if (!/\bwidth=/.test(next)) {
      next = next.replace(/\s*\/?>$/, ` width="${dimensions.width}"$&`);
    }
    if (!/\bheight=/.test(next)) {
      next = next.replace(/\s*\/?>$/, ` height="${dimensions.height}"$&`);
    }
    return next;
  });

  if (updated !== html) {
    fs.writeFileSync(filePath, updated);
  }
}

console.log(`Hardened ${pages.length} live HTML files.`);
