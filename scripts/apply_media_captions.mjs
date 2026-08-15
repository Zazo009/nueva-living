// One-shot maintenance script: merges the media caption/alt translations
// from lib/media_captions_{a,b}.mjs into each project.json as
// i18n.<locale>.media.items, preserving every existing i18n key.
//
// Structural fields (src, category, width, height, ...) are copied from the
// English item verbatim -- only alt/caption come from the translation table,
// so a translation file can never corrupt an image path or a layout size.
// Re-running is safe: it rewrites the same derived arrays.
import { readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { CAPTIONS_A } from './lib/media_captions_a.mjs';
import { CAPTIONS_B } from './lib/media_captions_b.mjs';

const LOCALES = ['es', 'fr', 'de', 'ru', 'ar'];
const ALL = { ...CAPTIONS_A, ...CAPTIONS_B };
const report = [];

for (const [slug, rows] of Object.entries(ALL)) {
  const file = path.resolve('content/liora-projects', slug, 'project.json');
  const project = JSON.parse(readFileSync(file, 'utf8'));
  const english = project.media?.items || [];

  if (rows.length !== english.length) {
    throw new Error(`${slug}: translation table has ${rows.length} rows, English has ${english.length} items`);
  }

  project.i18n = project.i18n || {};

  for (const locale of LOCALES) {
    project.i18n[locale] = project.i18n[locale] || {};
    project.i18n[locale].media = project.i18n[locale].media || {};

    project.i18n[locale].media.items = english.map((item, index) => {
      const row = rows[index][locale];
      if (!row) throw new Error(`${slug}[${index}]: missing ${locale} translation`);
      const [alt, caption] = row;
      const next = { ...item };
      if (item.alt !== undefined) next.alt = alt;
      // Only carry a caption when the English item has one -- never invent
      // a caption for an image that intentionally has none.
      if (item.caption !== undefined) next.caption = caption;
      return next;
    });
  }

  writeFileSync(file, JSON.stringify(project, null, 2));
  report.push(`${slug}: ${english.length} items x ${LOCALES.length} locales`);
}

console.log(report.join('\n'));

// --- images.{hero,architecture,lifestyle,privateViewing}.alt ---------------
// Same principle as above: only `alt` comes from the translation table; the
// image src/width/height and every other key are copied from English.
const { IMAGE_ALTS } = await import('./lib/image_alt_translations.mjs');

for (const [slug, byKey] of Object.entries(IMAGE_ALTS)) {
  const file = path.resolve('content/liora-projects', slug, 'project.json');
  const project = JSON.parse(readFileSync(file, 'utf8'));
  project.i18n = project.i18n || {};

  for (const locale of LOCALES) {
    project.i18n[locale] = project.i18n[locale] || {};
    const target = project.i18n[locale].images || {};
    for (const [imageKey, translations] of Object.entries(byKey)) {
      const english = project.images?.[imageKey];
      if (!english) throw new Error(`${slug}: no English images.${imageKey}`);
      if (!translations[locale]) throw new Error(`${slug}.${imageKey}: missing ${locale}`);
      target[imageKey] = { ...english, ...(target[imageKey] || {}), alt: translations[locale] };
    }
    project.i18n[locale].images = target;
  }

  writeFileSync(file, JSON.stringify(project, null, 2));
}

console.log(`image alts: ${Object.keys(IMAGE_ALTS).length} projects x 4 images x ${LOCALES.length} locales`);
