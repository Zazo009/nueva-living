// Fails if running the build twice changes anything.
//
// Why this exists: five files in the repo root are both a source and a build
// output -- the builders read them, inject nav/hreflang/scripts, and write them
// back. That only works while every injection strips its own previous output
// first. One strip regex silently stopped matching when a Guides block was
// added above the selector it was anchored on, and from then on each build
// appended another copy of the same 4.4KB script. Twenty-five copies had
// accumulated in 404, compare, thank-you and developments -- 105KB of the
// 125KB of thank-you.html -- and shipped to production, because nothing about
// the rendered page looked wrong.
//
// Run after the build chain. A non-empty report means an injection is no
// longer removing its predecessor.
import { execFileSync } from 'node:child_process';
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { createHash } from 'node:crypto';
import path from 'node:path';

const root = process.cwd();
const BUILDERS = [
  'build_footer_pages', 'build_property_pages', 'build_segment_pages',
  'build_homepage_locales', 'build_developments_locales', 'build_static_page_locales'
];

function htmlFiles(dir, depth = 0) {
  const out = [];
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    if (entry.name === 'dist' || entry.name === 'node_modules' || entry.name.startsWith('.')) continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory() && depth < 1) out.push(...htmlFiles(full, depth + 1));
    else if (entry.isFile() && entry.name.endsWith('.html')) out.push(full);
  }
  return out;
}

const digest = () => Object.fromEntries(
  htmlFiles(root).map((f) => [path.relative(root, f), createHash('md5').update(readFileSync(f)).digest('hex')])
);

const before = digest();
for (const b of BUILDERS) execFileSync('node', [`scripts/${b}.mjs`], { stdio: 'ignore' });
const after = digest();

const changed = Object.keys(before).filter((f) => before[f] !== after[f]);
if (changed.length) {
  console.error(`Build is not idempotent: ${changed.length} file(s) changed on a repeat build.`);
  console.error('An injection is appending without stripping its previous output.\n');
  for (const f of changed.slice(0, 20)) console.error(`  ${f}`);
  if (changed.length > 20) console.error(`  ... and ${changed.length - 20} more`);
  process.exit(1);
}
console.log(`Build is idempotent: ${Object.keys(before).length} HTML files unchanged on a repeat build.`);
