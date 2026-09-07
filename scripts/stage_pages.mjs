// Restores the five hand-authored pages from pages/ before the build runs.
//
// These five are the only pages the site hand-authors. Every builder in the
// chain reads them from the repo root, injects into them and writes them back,
// so before this step existed they were simultaneously the source and the
// build output. Two things went wrong because of that:
//
//   - A hand edit to a fully generated page looked like it worked and was
//     silently overwritten on the next build.
//   - An injection whose strip stopped matching appended instead of replacing,
//     and because the file was also the source, the extra copy was carried
//     into the next build. Twenty-five copies of one script accumulated and
//     shipped.
//
// Starting every build from a pristine copy makes the second failure
// structurally impossible: injections can no longer accumulate across builds,
// because each build begins from the same source. The root copies are build
// artifacts and are gitignored; edit pages/ instead.
import { existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const source = path.join(root, 'pages');

if (!existsSync(source)) {
  console.error('pages/ is missing. It holds the hand-authored sources for the five root pages.');
  process.exit(1);
}

const staged = readdirSync(source).filter((f) => f.endsWith('.html'));
if (!staged.length) {
  console.error('pages/ contains no .html files.');
  process.exit(1);
}

// Overwriting the root copy is the whole point, but it also means an edit made
// to the root copy by hand vanishes with no message -- which is exactly how an
// hour of nav work on nueva-living-home.html was lost. A warning here would be
// pure noise, because later build steps inject into these same root copies by
// design and so every one of them differs on the next run. The banner goes in
// the file instead, where someone about to edit the wrong copy will see it.
const banner = (file) => `<!-- Generated from pages/${file} on every build. `
  + `Edit that file, not this one: changes here are overwritten. -->\n`;
for (const file of staged) {
  const html = readFileSync(path.join(source, file), 'utf8');
  writeFileSync(path.join(root, file), banner(file) + html);
}
