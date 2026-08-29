// Assemble a vertical social cut from a project's real photography.
//
// Every frame is a photograph of a completed property. Nothing is generated:
// the movement is an ffmpeg pan and scale over the actual pixels, which is
// faithful by construction rather than by prompt. That matters more in an ad
// than anywhere else on the site, because an ad is a commercial claim.
//
// Runway's part in this campaign is the voice, added afterwards, in ten
// languages. It never touches the picture.
//
// Outside the build chain, like the rest of scripts/tools.
//
//   node scripts/tools/build_social_cut.mjs la-morelia-de-marbella

import { readFileSync, existsSync, mkdirSync, writeFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import path from 'node:path';

const W = 1080, H = 1920, FPS = 30;

// Shot list: file, seconds, and how the frame moves. Ordered as a story --
// the view first because it is the hook, the rooms after it, the setting last.
const SHOTS = {
  'la-morelia-de-marbella': [
    ['terrace-plunge-pool-view.jpg', 4.0, 'in'],
    ['covered-terrace-dining-lounge.jpg', 3.0, 'left'],
    ['living-dining-kitchen-open-plan.jpg', 3.0, 'in'],
    ['kitchen.jpg', 2.5, 'right'],
    ['bedroom-terrace-access.jpg', 3.0, 'in'],
    ['second-bedroom.jpg', 2.5, 'left'],
    ['communal-infinity-pools.jpg', 3.5, 'out'],
    ['communal-gardens-loungers.jpg', 3.5, 'in']
  ]
};

const slug = process.argv[2];
const shots = SHOTS[slug];
if (!shots) {
  console.error(`Usage: node scripts/tools/build_social_cut.mjs <${Object.keys(SHOTS).join('|')}>`);
  process.exit(1);
}

const mediaDir = path.join('assets', 'liora', 'projects', slug, 'media');
const outDir = path.join('dist-social', slug);
mkdirSync(outDir, { recursive: true });

// Pan expressions. Each moves across the source rather than inventing beyond it.
const move = (kind, frames) => {
  const z = { in: `min(1+0.0009*on,1.14)`, out: `max(1.14-0.0009*on,1)` }[kind] || '1.10';
  const x = kind === 'left' ? `(iw-iw/zoom)*(1-on/${frames})`
    : kind === 'right' ? `(iw-iw/zoom)*(on/${frames})`
    : `iw/2-(iw/zoom/2)`;
  return `zoompan=z='${z}':d=${frames}:x='${x}':y='ih/2-(ih/zoom/2)':s=${W}x${H}:fps=${FPS}`;
};

const parts = [];
shots.forEach(([file, seconds, kind], i) => {
  const src = path.join(mediaDir, file);
  if (!existsSync(src)) {
    console.error(`  missing: ${src}`);
    process.exit(1);
  }
  const frames = Math.round(seconds * FPS);
  const clip = path.join(outDir, `clip-${String(i).padStart(2, '0')}.mp4`);
  execFileSync('ffmpeg', ['-v', 'error', '-loop', '1', '-i', src, '-t', String(seconds), '-r', String(FPS),
    '-vf', `scale=${W * 3}:-1,crop=iw:ih*0.62:0:ih*0.19,${move(kind, frames)},format=yuv420p`,
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-y', clip]);
  parts.push(clip);
  console.log(`  ${String(seconds).padStart(4)}s  ${kind.padEnd(5)}  ${file}`);
});

const list = path.join(outDir, 'concat.txt');
writeFileSync(list, `${parts.map((p) => `file '${path.basename(p)}'`).join('\n')}\n`);
const out = path.join(outDir, `${slug}-social-silent.mp4`);
execFileSync('ffmpeg', ['-v', 'error', '-f', 'concat', '-safe', '0', '-i', list,
  '-c:v', 'libx264', '-preset', 'slow', '-crf', '20', '-pix_fmt', 'yuv420p',
  '-movflags', '+faststart', '-y', out]);

const total = shots.reduce((sum, s) => sum + s[1], 0);
console.log(`\n  ${out}  —  ${total}s, ${W}x${H}, no audio yet`);
