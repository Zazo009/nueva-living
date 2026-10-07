// Writes src/published.json: the videos and PDFs the build publishes, and so the
// only ones the worker will serve from R2.
//
// The list is read from dist/ rather than from the bucket or from git, because
// dist/ is what Netlify actually ships. The bucket holds everything that was ever
// uploaded and git holds files the build leaves out on purpose -- two hero videos
// are kept only as a revert path, and uploading "everything tracked" made them
// public for a few minutes. Publishing is a decision the build already makes;
// this follows it rather than keeping a second opinion.
//
// Run after build_dist.mjs:  node infra/media-worker/make-allowlist.mjs
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const dist = path.resolve(here, '..', '..', 'dist');
if (!fs.existsSync(path.join(dist, 'assets'))) {
  console.error('dist/assets not found -- run the build first.');
  process.exit(1);
}

const keys = [];
(function walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full);
    else if (/\.(mp4|pdf)$/i.test(entry.name)) keys.push(path.relative(dist, full).split(path.sep).join('/'));
  }
})(path.join(dist, 'assets'));

keys.sort();
fs.writeFileSync(path.join(here, 'src', 'published.json'), JSON.stringify(keys, null, 1) + '\n');
console.log(`${keys.length} published videos and PDFs written to src/published.json`);
