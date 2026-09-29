// Record that a project's images have been looked at.
//
//   node scripts/review_project_images.mjs --project=<slug>
//       lists the images that still need a review, and does nothing else.
//
//   node scripts/review_project_images.mjs --project=<slug> --confirm
//       records them, and is only run by whoever has just opened them.
//
//   node scripts/review_project_images.mjs --seed
//       one-off: accepts every image already live at the time the manifest
//       was introduced.
//
// What to look for, because the text guards cannot: the developer's own name
// or logo rendered inside the image -- on a gate, a wall, a hoarding, a pool
// floor, a letterbox, a screen -- and any other identifying mark such as a
// neighbouring business's signage. Names live in crm.realName and
// crm.realDeveloper; this prints them alongside so they are in front of you
// while you look.
import fs from 'node:fs';
import path from 'node:path';
import {
  imageHash, readManifest, writeManifest, projectImagePaths,
} from './lib/image_review.mjs';

const root = process.cwd();
const args = process.argv.slice(2);
const slug = args.find((a) => a.startsWith('--project='))?.slice('--project='.length);
const confirm = args.includes('--confirm');
const seed = args.includes('--seed');

if (!slug && !seed) {
  console.error('Usage: --project=<slug> [--confirm]   or   --seed');
  process.exit(1);
}

const projectsDir = path.join(root, 'content', 'liora-projects');
// A directory listing picks up .DS_Store and anything else the filesystem
// leaves behind, so take only the entries that are actually projects.
const slugs = seed
  ? fs.readdirSync(projectsDir).filter((name) => fs.existsSync(path.join(projectsDir, name, 'project.json')))
  : [slug];
const manifest = readManifest(root);
const today = new Date().toISOString().slice(0, 10);

let pending = 0;
let recorded = 0;

for (const current of slugs) {
  const file = path.join(projectsDir, current, 'project.json');
  if (!fs.existsSync(file)) {
    console.error(`${current}: no project.json`);
    process.exit(1);
  }
  const project = JSON.parse(fs.readFileSync(file, 'utf8'));
  const names = [project.crm?.realName, project.crm?.realDeveloper].filter(Boolean);
  const unreviewed = [];

  for (const rel of projectImagePaths(project)) {
    const abs = path.join(root, rel);
    if (!fs.existsSync(abs)) {
      console.error(`${current}: ${rel} is in the record but not on disk`);
      process.exit(1);
    }
    const hash = imageHash(abs);
    if (manifest[rel]?.sha === hash) continue;
    unreviewed.push({ rel, hash });
  }

  if (!unreviewed.length) continue;

  if (!seed) {
    console.log(`\n${current} — ${unreviewed.length} image(s) not yet reviewed`);
    if (names.length) console.log(`  watch for: ${names.join(', ')}`);
    for (const { rel } of unreviewed) console.log(`  ${rel}`);
  }

  if (confirm || seed) {
    for (const { rel, hash } of unreviewed) {
      manifest[rel] = { sha: hash, reviewed: seed ? 'pre-existing' : today };
      recorded += 1;
    }
  } else {
    pending += unreviewed.length;
  }
}

if (confirm || seed) {
  writeManifest(manifest, root);
  console.log(`\nRecorded ${recorded} image(s) as reviewed.`);
} else if (pending) {
  console.log(`\n${pending} image(s) awaiting review. Open them, then re-run with --confirm.`);
} else {
  console.log('Every image in this project has been reviewed.');
}
