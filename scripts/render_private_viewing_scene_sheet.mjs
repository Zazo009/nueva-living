import path from 'node:path';
import { copyFileSync, existsSync, mkdirSync, writeFileSync, readFileSync } from 'node:fs';

const html = readFileSync('Liora_Living_SOLENNE_POLISHED.html', 'utf8');
const outDir = path.resolve('artifacts/liora/private-viewing-scenes');
mkdirSync(outDir, { recursive: true });

function unescapeJsString(value) {
  return JSON.parse(`"${value.replace(/"/g, '\\"')}"`);
}

function getField(block, key) {
  const match = block.match(new RegExp(`\\b${key}:\\s*"((?:\\\\.|[^"\\\\])*)"`));
  return match ? unescapeJsString(match[1]) : '';
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

const sceneRe = /\{\s*img:\s*"((?:\\.|[^"\\])*)"([\s\S]*?)motion:/g;
const scenes = [];
let match;

while ((match = sceneRe.exec(html))) {
  const [, rawImg, block] = match;
  const index = scenes.length + 1;
  const src = unescapeJsString(rawImg);
  const filename = `scene-${String(index).padStart(2, '0')}.jpg`;
  const outPath = path.join(outDir, filename);

  if (src.startsWith('data:image/jpeg;base64,')) {
    writeFileSync(outPath, Buffer.from(src.slice('data:image/jpeg;base64,'.length), 'base64'));
  } else {
    const srcPath = path.resolve(src);
    if (!existsSync(srcPath)) {
      throw new Error(`Missing scene ${index} asset: ${src}`);
    }
    copyFileSync(srcPath, outPath);
  }

  scenes.push({
    index,
    filename,
    label: getField(block, 'label'),
    headline: getField(block, 'hl').replace(/<br>/g, ' / '),
    sub: getField(block, 'sub'),
  });
}

if (scenes.length !== 20) {
  throw new Error(`Expected 20 private viewing scenes, found ${scenes.length}.`);
}

const sheet = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Liora Private Viewing Scene Audit</title>
<style>
  body {
    margin: 0;
    padding: 28px;
    background: #f5f0e7;
    color: #282a25;
    font-family: Arial, sans-serif;
  }
  h1 {
    margin: 0 0 22px;
    font-size: 24px;
    letter-spacing: 0.04em;
  }
  .grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 18px;
  }
  figure {
    margin: 0;
    background: #fffaf1;
    border: 1px solid rgba(80, 65, 45, 0.18);
  }
  img {
    display: block;
    width: 100%;
    aspect-ratio: 16 / 9;
    object-fit: cover;
    background: #111;
  }
  figcaption {
    min-height: 110px;
    padding: 12px 14px 14px;
  }
  .label {
    font-weight: 700;
    font-size: 13px;
    letter-spacing: 0.08em;
    color: #7b6334;
    text-transform: uppercase;
  }
  .headline {
    margin-top: 7px;
    font-size: 17px;
    line-height: 1.25;
  }
  .sub {
    margin-top: 7px;
    color: #6b665d;
    font-size: 12px;
    line-height: 1.45;
  }
</style>
</head>
<body>
<h1>Liora Private Viewing Scene Audit</h1>
<div class="grid">
${scenes.map((scene) => `
  <figure>
    <img src="${scene.filename}" alt="Scene ${scene.index}">
    <figcaption>
      <div class="label">${escapeHtml(scene.label)}</div>
      <div class="headline">${escapeHtml(scene.headline)}</div>
      <div class="sub">${escapeHtml(scene.sub)}</div>
    </figcaption>
  </figure>`).join('\n')}
</div>
</body>
</html>`;

writeFileSync(path.join(outDir, 'scene-contact-sheet.html'), sheet);
writeFileSync(path.join(outDir, 'scene-copy-current.json'), JSON.stringify(scenes, null, 2));

console.log(JSON.stringify({
  scenes: scenes.length,
  sheet: path.relative(process.cwd(), path.join(outDir, 'scene-contact-sheet.html')),
  dir: path.relative(process.cwd(), outDir),
}, null, 2));
