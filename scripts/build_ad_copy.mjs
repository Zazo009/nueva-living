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
    const town = String(location).split(/[,\u060C]/)[0].trim();
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
    const fit = (cap, ...candidates) =>
      candidates.find((c) => c && String(c).length <= cap) || '';
    const meta = (locale === 'en' ? project.card?.meta : overlay?.card?.meta) || project.card?.meta || [];
    const beds = meta.find((m) => /\d/.test(m)) || '';

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
