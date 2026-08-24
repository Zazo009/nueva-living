# Hand-authored pages

These five files are the only pages on the site written by hand. Everything
else is generated from `content/` by the builders in `scripts/`.

**Edit the files in this directory.** The copies that appear in the repo root
during a build are output, not source: `scripts/stage_pages.mjs` overwrites
them from here at the start of every build, and they are gitignored.

## Why the split exists

Every builder in the chain reads these pages from the repo root, injects
navigation, hreflang, the language switcher and page scripts into them, and
writes them back to the same path. That made each file its own source *and* its
own build output, which caused two distinct failures:

- A hand edit to a page that is actually generated from a template looked like
  it worked and was silently reverted on the next build. The area guide index
  shipped its old heading for exactly this reason.
- An injection whose strip pattern stopped matching appended instead of
  replacing. Because the file was also the source, the extra copy was carried
  into the next build and the next. Twenty-five copies of the same 4.4KB script
  accumulated in four pages and went live: 105KB of the 125KB of
  `thank-you.html` was duplicated JavaScript.

Staging from a pristine source makes the second failure impossible rather than
merely detectable -- injections cannot accumulate across builds when every
build starts from the same file. `scripts/verify_build_idempotent.mjs` still
runs in the deploy to catch an injection that breaks within a single build.
