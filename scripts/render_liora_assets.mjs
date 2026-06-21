import path from 'node:path';
import { createRequire } from 'node:module';

const require = createRequire('/Users/sasanraftari/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp/package.json');
const sharp = require('sharp');

const root = path.resolve('assets/liora');

const outputs = [
  {
    input: 'liora-logo-primary.svg',
    output: 'liora-logo-primary-3072.png',
    width: 3072,
    height: 2048,
  },
  {
    input: 'liora-logo-primary.svg',
    output: 'liora-logo-primary-6144.png',
    width: 6144,
    height: 4096,
  },
  {
    input: 'liora-logo-wordmark-light.svg',
    output: 'liora-logo-wordmark-light-3072.png',
    width: 3072,
    height: 2048,
  },
  {
    input: 'liora-logo-wordmark-bronze.svg',
    output: 'liora-logo-wordmark-bronze-3072.png',
    width: 3072,
    height: 2048,
  },
  {
    input: 'liora-monogram.svg',
    output: 'liora-monogram-1024.png',
    width: 1024,
    height: 1024,
  },
];

for (const item of outputs) {
  await sharp(path.join(root, item.input), { density: 288 })
    .resize(item.width, item.height, { fit: 'contain' })
    .png({ compressionLevel: 9, adaptiveFiltering: true })
    .toFile(path.join(root, item.output));

  console.log(`${item.output}: ${item.width}x${item.height}`);
}
