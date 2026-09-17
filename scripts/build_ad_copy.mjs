// Meta ad copy for every project, in every language.
//
// Nothing here is written by hand and nothing is translated at this step.
// Each field is composed from strings the project already ships -- the card
// description, the starting price, the type tag, the availability eyebrow --
// which are the same strings the page shows and the same ones the audit
// checks. So an ad can never claim a price the page does not, and a
// correction to a project reaches its ads by rebuilding rather than by
// someone remembering.
//
// Two headline variants per project per language, because the first real
// question is whether price or place pulls harder, and that differs by
// market. They are a pair to test, not a choice to agonise over.
import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const LOCALES = ['en', 'es', 'fr', 'de', 'ru', 'ar', 'nl', 'pl', 'no', 'sv'];

// What Meta shows before it truncates. The hard caps are far higher; these
// are the widths a visitor actually reads in a feed, so they are what the
// report measures against.
const VISIBLE = { primary: 125, headline: 40, description: 30 };

const projectsDir = path.join(root, 'content', 'liora-projects');
const slugs = fs.readdirSync(projectsDir)
  .filter((d) => fs.existsSync(path.join(projectsDir, d, 'project.json')))
  .sort();

// The overlay carries only what is translated; everything structural stays on
// the English base. Reading through one to the other is how the rest of the
// build does it too.
const pick = (base, overlay, section, key) => {
  const o = overlay?.[section];
  if (o && typeof o === 'object' && o[key] != null && o[key] !== '') return o[key];
  return base?.[section]?.[key] ?? '';
};

const rows = [];
for (const slug of slugs) {
  const project = JSON.parse(fs.readFileSync(path.join(projectsDir, slug, 'project.json'), 'utf8'));
  for (const locale of LOCALES) {
    const overlay = locale === 'en' ? null : project.i18n?.[locale];
    if (locale !== 'en' && !overlay) continue;

    const description = pick(project, overlay, 'card', 'description');
    const typeTag = pick(project, overlay, 'card', 'typeTag');
    const price = pick(project, overlay, 'hero', 'startingPrice');
    const location = pick(project, overlay, 'hero', 'location');
    const eyebrow = pick(project, overlay, 'hero', 'eyebrow');

    // The town, not the full "town, municipality" -- a headline has no room
    // to say Mijas twice. Arabic separates with an Arabic comma, so splitting
    // on the Latin one left the whole string and the fallback then dropped
    // the type tag to make it fit.
    // Projects separate the parts of a location with whichever mark reads well
    // in their own copy: a comma, an Arabic comma, a slash or a dash. Splitting
    // on the comma alone left eight locations whole, and at full length they
    // overflowed the description cap -- as did their eyebrow, so those rows
    // shipped with no description at all.
    const town = String(location).split(/[,\u060C\/\u2013\u2014]/)[0].trim();
    // And joined back with the separator that language actually uses.
    const comma = locale === 'ar' ? '\u060C ' : ', ';
    const prefix = locale === 'en' ? '' : `${locale}/`;
    const params = new URLSearchParams({
      utm_source: 'meta',
      utm_medium: 'paid_social',
      utm_campaign: `${locale}-${project.discovery?.area || 'costa-del-sol'}`,
      utm_content: slug
    });

    // Compose, measure, degrade. A field that does not fit is not shipped
    // truncated -- it falls back to a shorter true thing. The type tag is
    // sometimes a marketing phrase ("Urban Resort") and the eyebrow is
    // sometimes a whole sentence, and in Russian and Arabic both run long,
    // so a blind join overflowed on 366 of the 510.
    // Coerces first, so a non-string can never reach the sheet. It used to
    // measure String(c).length but return c itself, which let an array
    // through: ["From", "\u20ac690,000"] stringifies to 13 characters, sailed
    // under the 30-char cap, and shipped as an array in 384 of the 510 rows.
    const fit = (cap, ...candidates) =>
      candidates.map((c) => (c == null ? '' : String(c)))
        .find((c) => c && c.length <= cap) || '';

    // card.meta comes in two shapes: a flat list of strings on twelve
    // projects, and [label, value] pairs on the other thirty-nine. The value
    // is the part worth showing.
    const metaText = (m) => (Array.isArray(m) ? String(m[m.length - 1] ?? '') : String(m ?? ''));
    const enMeta = project.card?.meta || [];
    const localeMeta = (locale === 'en' ? enMeta : overlay?.card?.meta) || enMeta;
    // The bedroom count, located in English and then read by position from the
    // translated list -- "first entry containing a digit" picked whatever came
    // first, which across these projects is the price, the delivery quarter,
    // the unit count or the built area. The pair-form projects carry no
    // bedroom entry at all, so they fall through to the town, which is
    // translated.
    const bedsIndex = enMeta.findIndex((m) => /bedroom/i.test(metaText(m)));
    const beds = bedsIndex >= 0 ? metaText(localeMeta[bedsIndex] ?? enMeta[bedsIndex]) : '';

    rows.push({
      slug,
      locale,
      area: project.discovery?.area || '',
      price_from: project.discovery?.price ?? null,
      primary_text: description,
      headline_price: fit(VISIBLE.headline, price),
      headline_place: fit(VISIBLE.headline, `${typeTag}${comma}${town}`, town, typeTag),
      description: fit(VISIBLE.description, beds, town, eyebrow),
      cta: 'LEARN_MORE',
      link: `https://nuevaliving.com/${prefix}${project.output}?${params}`,
      image: project.images?.card?.src || project.images?.hero?.src || '',
      video: project.media?.video?.desktopSrc || ''
    });
  }
}

// Every text field ships as a string or the build stops. The length report
// below stringifies before measuring, so it cannot catch a wrong type -- it
// reported all 510 rows inside their caps while 384 carried arrays.
const TEXT_FIELDS = ['primary_text', 'headline_price', 'headline_place', 'description', 'cta', 'link'];
const malformed = rows.flatMap((r) => TEXT_FIELDS
  .filter((f) => typeof r[f] !== 'string')
  .map((f) => `${r.slug}/${r.locale}.${f} is ${Array.isArray(r[f]) ? 'an array' : typeof r[f]}`));
if (malformed.length) {
  console.error(`${malformed.length} field(s) are not strings:\n  ${malformed.slice(0, 6).join('\n  ')}`);
  process.exit(1);
}

fs.mkdirSync(path.join(root, 'content', 'ads'), { recursive: true });
fs.writeFileSync(path.join(root, 'content', 'ads', 'meta-ad-copy.json'),
  `${JSON.stringify(rows, null, 1)}\n`);

// A sheet, because the person reviewing this copy is not going to read JSON.
const csvCell = (v) => `"${String(v ?? '').replace(/"/g, '""')}"`;
const cols = ['slug', 'locale', 'primary_text', 'headline_price', 'headline_place',
  'description', 'cta', 'link'];
fs.writeFileSync(path.join(root, 'content', 'ads', 'meta-ad-copy.csv'),
  `${[cols.join(','), ...rows.map((r) => cols.map((c) => csvCell(r[c])).join(','))].join('\n')}\n`);

const over = (field, cap) => rows.filter((r) => String(r[field]).length > cap).length;
const withVideo = rows.filter((r) => r.video).length;
console.log(`${rows.length} ads: ${slugs.length} projects x ${LOCALES.length} languages`);
console.log(`  primary text over ${VISIBLE.primary} visible chars: ${over('primary_text', VISIBLE.primary)} (truncates to "... See more", hook is first)`);
console.log(`  price headline over ${VISIBLE.headline}: ${over('headline_price', VISIBLE.headline)}`);
console.log(`  place headline over ${VISIBLE.headline}: ${over('headline_place', VISIBLE.headline)}`);
console.log(`  description over ${VISIBLE.description}: ${over('description', VISIBLE.description)}`);
console.log(`  ads with a video master available: ${withVideo}`);
console.log('wrote content/ads/meta-ad-copy.json and .csv');
