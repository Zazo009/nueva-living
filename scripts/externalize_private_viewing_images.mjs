import path from 'node:path';
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';

const htmlPath = path.resolve('Liora_Living_SOLENNE_POLISHED.html');
const outDir = path.resolve('assets/liora/viewing');
mkdirSync(outDir, { recursive: true });

const html = readFileSync(htmlPath, 'utf8');
let index = 0;

const rewritten = html.replace(/img:\s*"data:image\/jpeg;base64,([^"]+)"/g, (match, base64) => {
  index += 1;
  const filename = `scene-${String(index).padStart(2, '0')}.jpg`;
  writeFileSync(path.join(outDir, filename), Buffer.from(base64, 'base64'));
  return `img: "assets/liora/viewing/${filename}"`;
});

if (index === 0) {
  console.log(JSON.stringify({ changed: false, reason: 'No inline private viewing images found.' }, null, 2));
} else {
  writeFileSync(htmlPath, rewritten);
  console.log(JSON.stringify({ changed: true, scenes: index, outDir: path.relative(process.cwd(), outDir) }, null, 2));
}
