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
import { copyFileSync, existsSync, mkdirSync, readdirSync } from 'node:fs';
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

for (const file of staged) copyFileSync(path.join(source, file), path.join(root, file));
console.log(`Staged ${staged.length} hand-authored pages from pages/: ${staged.join(', ')}`);
