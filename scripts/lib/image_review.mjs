// Every image that ships has been looked at by a person.
//
// The anonymisation guard reads project.json and the built pages, so it
// catches the developer's own name in prose, alt text, a caption or a
// filename. It cannot read pixels. Two of the renders delivered for
// playa-del-angel-residences carried the developer's name inside the image --
// one engraved on the entrance gate, one set in letters on the spa wall --
// and both would have gone live with every text check green.
//
// Optical character recognition would be the direct answer and is the wrong
// tool here: it means a system dependency inside the Netlify build, run over
// 1,677 images, to catch a case that appears a few times a year. What is
// cheap and total is recording the review. An image is identified by the hash
// of its bytes, so re-cropping or replacing a file drops it out of the
// manifest and it has to be looked at again.
//
// The manifest was seeded with the images already live when it was written.
// Those were accepted as they stood rather than re-reviewed, which is the
// house habit: a guard goes in green and only ever fires on drift.
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

export const MANIFEST_PATH = path.join('content', 'image-review.json');

/** The first 16 hex of the file's SHA-256. Enough to identify, short to diff. */
export function imageHash(absolutePath) {
  return createHash('sha256').update(fs.readFileSync(absolutePath)).digest('hex').slice(0, 16);
}

export function readManifest(root = process.cwd()) {
  const file = path.join(root, MANIFEST_PATH);
  if (!fs.existsSync(file)) return {};
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

export function writeManifest(manifest, root = process.cwd()) {
  const file = path.join(root, MANIFEST_PATH);
  const ordered = Object.fromEntries(Object.keys(manifest).sort().map((k) => [k, manifest[k]]));
  fs.writeFileSync(file, `${JSON.stringify(ordered, null, 2)}\n`);
}

/**
 * Every image a project's record points at: the gallery and the five section
 * images. Paths come from the record rather than from a directory listing, so
 * an unused file sitting in the folder is not something anyone has to review.
 */
export function projectImagePaths(project) {
  const paths = [];
  for (const item of project.media?.items || []) if (item.src) paths.push(item.src);
  for (const key of ['hero', 'card', 'architecture', 'lifestyle', 'privateViewing']) {
    const src = project.images?.[key]?.src;
    if (src) paths.push(src);
  }
  return [...new Set(paths)];
}
