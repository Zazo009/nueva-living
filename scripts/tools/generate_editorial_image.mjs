// Editorial hero imagery for the guides, via Runway's text-to-image API.
//
// The guides are general writing about how buying works. Two of them borrowed
// a named development's marketing photo as their hero, which implies an
// association that does not exist and puts one seller's asset behind editorial
// that is supposed to be independent. Two more shared a hero with another
// guide.
//
// The line this tool stays on the right side of: generated imagery is honest
// where it claims nothing. These prompts describe light, material and
// abstraction -- never a recognisable building, never a named place. A
// generated "Puerto Banus" that is not Puerto Banus is the same untruth as a
// generated villa, one level up, which is why area pages are excluded here and
// keep their real photography.
//
//   RUNWAYML_API_SECRET=... node scripts/tools/generate_editorial_image.mjs <key> [--apply]
//
// Without --apply it prints the plan and the cost and calls nothing.

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'node:fs';
import path from 'node:path';

const API = 'https://api.dev.runwayml.com/v1';
const VERSION = '2024-11-06';
const MODEL = 'gen4_image';
const RATIO = '1920:1080';
const CREDITS = 5;  // gen4_image, at $0.01 per credit

const LOOK = 'Editorial photography, natural Mediterranean daylight, muted warm '
  + 'neutrals, shallow depth of field, calm and understated. No text, no logos, '
  + 'no people\'s faces, no recognisable landmark, no identifiable building.';

const BRIEFS = {
  'off-plan-vs-resale': {
    file: 'assets/nueva/editorial/off-plan-vs-resale-1440.jpg',
    prompt: `Two architectural material samples resting side by side on a pale stone surface: `
      + `one a raw concrete and steel offcut, one a finished oak and limestone tile. `
      + `Overhead, close, nothing else in frame. ${LOOK}`,
    replaces: 'a named development\'s aerial photo'
  },
  'purchase-costs': {
    file: 'assets/nueva/editorial/purchase-costs-1440.jpg',
    prompt: `A quiet desk corner in warm daylight: a folded paper document, a pen and a `
      + `pair of glasses on pale stone. Shot from above at an angle, deliberately plain. ${LOOK}`,
    replaces: 'a hero shared with another guide'
  },
  'buying-from-abroad': {
    file: 'assets/nueva/editorial/buying-from-abroad-1440.jpg',
    prompt: `An open notebook and a passport-sized document on a linen surface beside a `
      + `window, soft directional morning light falling across them, blurred greenery `
      + `outside. Nothing legible. ${LOOK}`,
    replaces: 'a hero shared with another guide'
  }
};

const [, , key, ...flags] = process.argv;
const apply = flags.includes('--apply');
const jobs = key === 'all' ? Object.keys(BRIEFS) : [key];

if (!key || (key !== 'all' && !BRIEFS[key])) {
  console.error(`Usage: node scripts/tools/generate_editorial_image.mjs <${Object.keys(BRIEFS).join('|')}|all> [--apply]`);
  process.exit(1);
}

console.log(`  model     ${MODEL}, ${RATIO}`);
console.log(`  cost      $${(jobs.length * CREDITS / 100).toFixed(2)} for ${jobs.length} image(s)\n`);
for (const name of jobs) {
  const b = BRIEFS[name];
  console.log(`  ${name}`);
  console.log(`    output    ${b.file}`);
  console.log(`    replaces  ${b.replaces}`);
  console.log(`    prompt    ${b.prompt.slice(0, 120)}…\n`);
}

if (!apply) {
  console.log('  Dry run. Re-run with --apply to call the API.');
  process.exit(0);
}

const secret = process.env.RUNWAYML_API_SECRET;
if (!secret) {
  console.error('  RUNWAYML_API_SECRET is not set. Set it in your shell; it is never read from a file here.');
  process.exit(1);
}
const headers = {
  Authorization: `Bearer ${secret}`,
  'X-Runway-Version': VERSION,
  'Content-Type': 'application/json'
};

for (const name of jobs) {
  const brief = BRIEFS[name];
  if (existsSync(brief.file)) {
    console.log(`  ${name}: ${brief.file} already exists, skipping rather than paying again.`);
    continue;
  }
  const created = await fetch(`${API}/text_to_image`, {
    method: 'POST',
    headers,
    body: JSON.stringify({ model: MODEL, promptText: brief.prompt, ratio: RATIO })
  });
  if (!created.ok) {
    console.error(`  ${name}: create failed ${created.status} ${(await created.text()).slice(0, 300)}`);
    process.exit(1);
  }
  const { id } = await created.json();
  process.stdout.write(`  ${name}: task ${id} `);

  let task;
  for (let attempt = 0; attempt < 120; attempt += 1) {
    await new Promise((resolve) => setTimeout(resolve, 4000));
    const res = await fetch(`${API}/tasks/${id}`, { headers });
    if (!res.ok) { console.error(`poll failed ${res.status}`); process.exit(1); }
    task = await res.json();
    if (['SUCCEEDED', 'FAILED', 'CANCELLED', 'CANCELED'].includes(task.status)) break;
    process.stdout.write('.');
  }
  console.log('');
  if (task.status !== 'SUCCEEDED') {
    console.error(`  ${name}: ${task.status} ${JSON.stringify(task.failure || {}).slice(0, 200)}`);
    process.exit(1);
  }
  const url = Array.isArray(task.output) ? task.output[0] : task.output;
  const img = await fetch(url);
  if (!img.ok) { console.error(`  ${name}: download failed ${img.status}`); process.exit(1); }
  mkdirSync(path.dirname(brief.file), { recursive: true });
  writeFileSync(brief.file, Buffer.from(await img.arrayBuffer()));
  writeFileSync(`${brief.file}.provenance.json`, `${JSON.stringify({
    generated: true, tool: 'runway text_to_image', model: MODEL,
    prompt: brief.prompt, ratio: RATIO, taskId: id,
    note: 'Editorial abstraction. Depicts no specific property, place or person.'
  }, null, 2)}\n`);
  console.log(`  ${name}: written ${brief.file}`);
}
