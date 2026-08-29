// Turn an existing official render into a short motion clip, via Runway's
// developer API.
//
// Deliberately NOT part of the Netlify build chain. The whole repo rests on
// verify_build_idempotent -- same input, same output, every time -- and a
// generative call is neither deterministic nor free. This is a tool you run
// by hand; it writes an .mp4 into the project's media folder and you commit
// the result. The build then treats it as any other asset.
//
// The prompt is deliberately narrow. This site's position is that it shows
// what is real rather than what the brochure shows, so the only thing being
// generated here is camera movement across the developer's own render.
// Nothing is invented: no new scenery, no people, no weather, no light that
// was not already in the source frame. Every clip is written with a sidecar
// .provenance.json recording the source image, model and prompt, so it is
// always answerable which footage was filmed and which was moved.
//
//   RUNWAYML_API_SECRET=...  node scripts/tools/generate_project_motion.mjs <slug> [--apply]
//
// Without --apply it prints the plan and the cost and calls nothing.

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'node:fs';
import path from 'node:path';

const API = 'https://api.dev.runwayml.com/v1';
const VERSION = '2024-11-06';
const MODEL = 'gen4_turbo';
const DURATION = 5;
const RATIO = '1280:720';
const CREDITS_PER_SECOND = 5;      // gen4_turbo, at $0.01 per credit
const MAX_IMAGE_BYTES = 3_000_000; // data URI ceiling, kept conservative

// Movement only. Anything that could add something the render does not show
// belongs nowhere near this string.
const PROMPT = 'Very slow, steady camera push in. Static subject. Do not add, '
  + 'remove or alter any element of the scene: no new objects, no people, no '
  + 'vehicles, no change to weather, sky, light or reflections.';

const [, , slug, ...flags] = process.argv;
const apply = flags.includes('--apply');

if (!slug) {
  console.error('Usage: node scripts/tools/generate_project_motion.mjs <project-slug> [--apply]');
  process.exit(1);
}

const projectFile = path.join('content', 'liora-projects', slug, 'project.json');
if (!existsSync(projectFile)) {
  console.error(`No such project: ${projectFile}`);
  process.exit(1);
}
const project = JSON.parse(readFileSync(projectFile, 'utf8'));

// The hero render is the one the developer leads with, so it is the one whose
// motion a buyer would recognise. Fall back to the first media item.
const source = project.images?.hero?.src || project.media?.items?.[0]?.src;
if (!source) {
  console.error(`${slug}: no hero image or media item to work from.`);
  process.exit(1);
}
if (!existsSync(source)) {
  console.error(`${slug}: source image missing on disk: ${source}`);
  process.exit(1);
}

const outDir = path.join(path.dirname(source), 'motion');
const outFile = path.join(outDir, `${path.basename(source).replace(/\.[^.]+$/, '')}-motion.mp4`);
const cost = ((DURATION * CREDITS_PER_SECOND) / 100).toFixed(2);

console.log(`  project   ${slug}`);
console.log(`  source    ${source}`);
console.log(`  output    ${outFile}`);
console.log(`  model     ${MODEL}, ${DURATION}s, ${RATIO}`);
console.log(`  cost      $${cost}`);
console.log(`  prompt    ${PROMPT}`);

if (!apply) {
  console.log('\n  Dry run. Re-run with --apply to call the API.');
  process.exit(0);
}

const secret = process.env.RUNWAYML_API_SECRET;
if (!secret) {
  console.error('\n  RUNWAYML_API_SECRET is not set. Set it in your shell; it is never read from a file here.');
  process.exit(1);
}
if (existsSync(outFile)) {
  console.error(`\n  ${outFile} already exists. Delete it first rather than paying to overwrite it.`);
  process.exit(1);
}

const bytes = readFileSync(source);
if (bytes.length > MAX_IMAGE_BYTES) {
  console.error(`\n  Source is ${Math.round(bytes.length / 1024)} kB, over the ${MAX_IMAGE_BYTES / 1024} kB data-URI ceiling.`);
  process.exit(1);
}
const mime = source.endsWith('.png') ? 'image/png' : source.endsWith('.webp') ? 'image/webp' : 'image/jpeg';
const promptImage = `data:${mime};base64,${bytes.toString('base64')}`;

const headers = {
  Authorization: `Bearer ${secret}`,
  'X-Runway-Version': VERSION,
  'Content-Type': 'application/json'
};

const created = await fetch(`${API}/image_to_video`, {
  method: 'POST',
  headers,
  body: JSON.stringify({ model: MODEL, promptImage, promptText: PROMPT, ratio: RATIO, duration: DURATION })
});
if (!created.ok) {
  console.error(`\n  Create failed: ${created.status} ${(await created.text()).slice(0, 300)}`);
  process.exit(1);
}
const { id } = await created.json();
console.log(`\n  task ${id} — polling`);

let task;
for (let attempt = 0; attempt < 120; attempt += 1) {
  await new Promise((resolve) => setTimeout(resolve, 5000));
  const res = await fetch(`${API}/tasks/${id}`, { headers });
  if (!res.ok) {
    console.error(`  Poll failed: ${res.status}`);
    process.exit(1);
  }
  task = await res.json();
  if (['SUCCEEDED', 'FAILED', 'CANCELLED', 'CANCELED'].includes(task.status)) break;
  process.stdout.write('.');
}
console.log('');
if (task.status !== 'SUCCEEDED') {
  console.error(`  Task ${task.status}: ${JSON.stringify(task.failure || task).slice(0, 300)}`);
  process.exit(1);
}

const url = Array.isArray(task.output) ? task.output[0] : task.output;
const video = await fetch(url);
if (!video.ok) {
  console.error(`  Download failed: ${video.status}`);
  process.exit(1);
}
mkdirSync(outDir, { recursive: true });
writeFileSync(outFile, Buffer.from(await video.arrayBuffer()));

// Provenance, so nobody has to guess later which clips were generated.
writeFileSync(`${outFile}.provenance.json`, `${JSON.stringify({
  generated: true,
  tool: 'runway image_to_video',
  model: MODEL,
  sourceImage: source,
  prompt: PROMPT,
  durationSeconds: DURATION,
  ratio: RATIO,
  taskId: id
}, null, 2)}\n`);

console.log(`  written   ${outFile}`);
console.log(`  written   ${outFile}.provenance.json`);
