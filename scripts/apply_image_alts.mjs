// Writes `images.{hero,architecture,lifestyle,privateViewing}.alt` into a
// project's nine locale overlays, from lib/image_alt_translations.mjs.
//
// These four are the large section images on a property page. They are a
// separate field group from the gallery (`media.items[].alt`), which
// tools/import/assemble.py covers, so a new project needs this step too --
// I had been doing it by hand, which is how the breakage below happened.
//
// It replaced apply_media_captions.mjs, which did two jobs. The other one was
// merging a five-locale snapshot of gallery captions from
// lib/media_captions_{a,b}.mjs. Those tables had been overtaken by the
// project records themselves: where they still lined up they agreed with
// project.json in every one of their strings, and the records carry the same
// text in nine locales rather than five. Three galleries had also grown since
// the tables were written -- golden-mile 6 rows against 16 items,
// nueva-andalucia-villa-collection 5 against 42, rio-real 8 against 19 -- and
// the length check threw on the first of them, which took the image-alt half
// down with it for every project. The tables are in the history if the wording
// is ever wanted back.
//
// It only fills an alt that is absent. The shipped wording wins over the
// table, because the shipped wording is what readers hear and what
// tools/import/tm.py has already harvested; overwriting it would churn 190
// strings across nl, pl, no and sv for two equally good renderings of the
// same sentence. That also makes re-running safe.
import { readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { IMAGE_ALTS } from './lib/image_alt_translations.mjs';

const LOCALES = ['es', 'fr', 'de', 'ru', 'ar', 'nl', 'pl', 'no', 'sv'];
const only = process.argv.find((arg) => arg.startsWith('--project='))?.slice('--project='.length);

let filled = 0;
let kept = 0;
const report = [];

for (const [slug, byKey] of Object.entries(IMAGE_ALTS)) {
  if (only && slug !== only) continue;
  const file = path.resolve('content/liora-projects', slug, 'project.json');
  const project = JSON.parse(readFileSync(file, 'utf8'));
  project.i18n = project.i18n || {};
  let wrote = 0;

  for (const locale of LOCALES) {
    project.i18n[locale] = project.i18n[locale] || {};
    const target = project.i18n[locale].images || {};
    for (const [imageKey, translations] of Object.entries(byKey)) {
      const english = project.images?.[imageKey];
      if (!english) throw new Error(`${slug}: no English images.${imageKey}`);
      if (!translations[locale]) throw new Error(`${slug}.${imageKey}: table has no ${locale}`);
      const existing = target[imageKey];
      if (existing?.alt) { kept += 1; continue; }
      // Structural fields come from English, so the table can never reach a
      // path or a layout size.
      target[imageKey] = { ...english, ...(existing || {}), alt: translations[locale] };
      wrote += 1;
      filled += 1;
    }
    project.i18n[locale].images = target;
  }

  if (wrote) {
    writeFileSync(file, JSON.stringify(project, null, 2));
    report.push(`${slug}: ${wrote} alt(s) filled`);
  }
}

if (only && !Object.keys(IMAGE_ALTS).includes(only)) {
  throw new Error(`${only} has no entry in lib/image_alt_translations.mjs`);
}

console.log(report.join('\n'));
console.log(`image alts: ${filled} filled, ${kept} already translated`);
