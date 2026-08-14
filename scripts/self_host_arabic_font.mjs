// Regenerates assets/fonts/arabic/liora-arabic-fonts.css and its woff2 file
// from Google Fonts, following the same self-hosting pattern as
// self_host_fonts.mjs (Cinzel/Montserrat). Cairo is a single variable font
// (wght 200-1000) covering the site's 400/500/600/700 weight range in one
// ~36KB file, restricted to the Arabic unicode-range subset so it never
// pulls in Latin/Cyrillic glyph data the brand fonts already cover.
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const fontsDir = path.join(root, 'assets/fonts/arabic');
fs.mkdirSync(fontsDir, { recursive: true });

const remoteCssUrl = 'https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700&display=swap';
const remoteCss = execFileSync('curl', [
  '-sL',
  '-A', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
  remoteCssUrl
]).toString();

const blocks = remoteCss.split(/(?=\/\* \w[\w-]* \*\/\n@font-face)/);
const arabicBlocks = blocks.filter((b) => b.trim().startsWith('/* arabic */'));
if (!arabicBlocks.length) {
  throw new Error('No arabic-subset @font-face blocks found in the Google Fonts response.');
}

let css = arabicBlocks.join('\n');
const urls = [...new Set([...css.matchAll(/https:\/\/fonts\.gstatic\.com\/[^)]+\.woff2/g)].map((m) => m[0]))];

for (const url of urls) {
  const filename = path.basename(url);
  const target = path.join(fontsDir, filename);
  if (!fs.existsSync(target) || fs.statSync(target).size === 0) {
    execFileSync('curl', ['-sL', url, '-o', target], { stdio: 'inherit' });
  }
  css = css.replaceAll(url, `./${filename}`);
}

css = css.replace(/font-display:\s*swap;/g, 'font-display: block;');
const header = `/* Self-hosted Arabic typeface for Nueva Living -- Cairo.
   Applied to :lang(ar) content only via liora-rtl.css, so it never loads
   for LTR locales. Chosen for a refined, contemporary geometric character
   that pairs with Montserrat's own geometric-sans structure (shared visual
   weight and letterform logic) while providing genuine Arabic shaping
   quality across the weight range the brand already uses (400-700).
   Regenerate with scripts/self_host_arabic_font.mjs. */

`;

fs.writeFileSync(path.join(fontsDir, 'liora-arabic-fonts.css'), header + css);
console.log(`Wrote liora-arabic-fonts.css referencing ${urls.length} font file(s).`);
