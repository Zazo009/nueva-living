// Pure, side-effect-free logic for the homepage's cinematic-presentation
// viewer data (VIEWING_PROJECTS / PROJECT_VIEWING_SCENE_SETS), shared by
// build_property_pages.mjs (which writes the initial English-baked blocks
// into nueva-living-home.html) and build_homepage_locales.mjs (which
// re-calls renderViewingBlocks() per non-English locale so the cinematic
// viewer's per-project scene captions/labels actually translate instead of
// being cloned as English on every locale homepage).
//
// This lives in its own module rather than being imported directly from
// build_property_pages.mjs because that script has unguarded top-level
// side effects (it writes all property page HTML files as soon as it's
// loaded) -- importing it from another script would silently re-run the
// entire property-page build a second time.
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import path from 'node:path';
import { DEFAULT_LOCALE, localizeProject, t, hasString } from './i18n.mjs';

const projectsDir = path.resolve('content/liora-projects');

function readJson(file) {
  return JSON.parse(readFileSync(file, 'utf8'));
}

function projectFiles() {
  if (!existsSync(projectsDir)) return [];
  return readdirSync(projectsDir, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => path.join(projectsDir, entry.name, 'project.json'))
    .filter((file) => existsSync(file));
}

export function loadProjects() {
  return projectFiles()
    .map((file) => ({ ...readJson(file), sourceFile: file }))
    .sort((a, b) => {
      const orderA = a.card?.order ?? 999;
      const orderB = b.card?.order ?? 999;
      return orderA === orderB ? a.name.localeCompare(b.name) : orderA - orderB;
    });
}

function localizedCategory(category, locale) {
  if (!category) return category;
  const key = `mediaCategory.${category}`;
  // Same guard as build_property_pages.mjs: on a localized build the
  // project's i18n overlay may already have translated the category, so
  // there is no key to look up and t() would return the key literal.
  return hasString(key) ? t(key, locale) : category;
}

const AREA_DISPLAY_NAMES = {
  marbella: 'Marbella',
  estepona: 'Estepona',
  benahavis: 'Benahavís',
  'nueva-andalucia': 'Nueva Andalucía',
  'mijas-fuengirola': 'Mijas & Fuengirola'
};

const VIEWING_SCENE_CATEGORY_TXT = {
  Exteriors: 'exterior',
  Location: 'exterior',
  Residences: 'interior',
  Resort: 'amenity'
};

const VIEWING_SCENE_OVERLAY = 'linear-gradient(to right, rgba(10,9,8,0.42), rgba(10,9,8,0.15), rgba(10,9,8,0.06))';

function renderViewingScenesJs(sourceProject, locale = DEFAULT_LOCALE) {
  const project = localizeProject(sourceProject, locale);
  const items = project.media?.items || [];
  if (!items.length) return null;

  const scenes = items.map((item, index) => {
    const num = String(index + 1).padStart(2, '0');
    const isLast = index === items.length - 1;
    const txt = isLast ? 'closing' : (VIEWING_SCENE_CATEGORY_TXT[item.category] || 'exterior');
    const motion = index % 2 === 0
      ? '(p) => ({ s: 1.06 - p * 0.02, x: p * -10, y: p * -2 })'
      : '(p) => ({ s: 1.055 - p * 0.018, x: p * 10, y: 0 })';
    const categoryLabel = item.category ? localizedCategory(item.category, locale) : t('mediaCategory.Residences', locale);
    return `    {
      img: ${JSON.stringify(item.src)},
      pos: "center 50%",
      label: ${JSON.stringify(`${num} — ${categoryLabel}`)},
      hl: ${JSON.stringify(item.caption || project.shortName || project.name)},
      sub: ${JSON.stringify(item.alt || '')},
      gold: ${isLast ? 'true' : 'false'},
      ov: ${JSON.stringify(VIEWING_SCENE_OVERLAY)},
      txt: ${JSON.stringify(txt)},
      motion: ${motion}
    }`;
  });

  return `  ${JSON.stringify(sourceProject.slug)}: [\n${scenes.join(',\n')}\n  ]`;
}

function renderViewingProjectEntryJs(sourceProject, locale = DEFAULT_LOCALE) {
  const project = localizeProject(sourceProject, locale);
  const discovery = project.discovery || {};
  const viewing = project.viewing || {};
  const areaDisplay = AREA_DISPLAY_NAMES[discovery.area] || project.card?.label || project.hero?.location || '';
  const highlights = project.architecture?.highlights || [];
  const investmentNotes = (project.investment?.cards || []).map(([, note]) => note).filter(Boolean);
  const localizedStatus = discovery.status ? t(`discoveryStatus.${discovery.status}`, locale) : '';
  // German capitalizes all nouns regardless of position; every other
  // locale here reads more naturally lowercased mid-phrase (e.g. "2-4
  // dormitorios", not "2-4 Dormitorios").
  const bedroomsWord = locale === 'de' ? t('cinematic.bedrooms', locale) : t('cinematic.bedrooms', locale).toLowerCase();
  const localizedBedrooms = discovery.bedrooms
    ? discovery.bedrooms.replace(/bedrooms?$/i, bedroomsWord)
    : '';
  const availability = viewing.availability || [
    { label: t('availability.status', locale), value: localizedStatus || project.hero?.delivery || t('common.onRequest', locale) },
    { label: t('viewing.material', locale), value: t('viewing.materialValue', locale) },
    { label: t('viewing.nextStep', locale), value: t('viewing.nextStepValue', locale, { project: project.shortName || project.name }) }
  ];

  const entry = {
    id: sourceProject.slug,
    name: project.name,
    location: project.hero?.location || '',
    area: areaDisplay,
    price: project.hero?.startingPrice || t('common.onRequest', locale),
    bedrooms: localizedBedrooms,
    builtSize: viewing.builtSize || '',
    terraceSize: viewing.terraceSize || '',
    completion: project.hero?.delivery || t('common.onRequest', locale),
    status: localizedStatus,
    lifestyle: project.description || '',
    overview: project.overview?.copy?.[0] || project.description || '',
    highlights,
    investmentNotes,
    availability,
    ctaLabel: viewing.ctaLabel || t('cta.requestProjectMaterial', locale),
    ctaMessage: project.enquiry?.message || `I would like to receive the latest information for ${project.name}.`
  };

  return `  ${JSON.stringify(sourceProject.slug)}: ${JSON.stringify(entry, null, 4).replace(/\n/g, '\n  ')}`;
}

export function renderViewingBlocks(projects, locale = DEFAULT_LOCALE) {
  const sorted = [...projects].sort((a, b) => (a.discovery?.priority ?? a.card?.order ?? 999) - (b.discovery?.priority ?? b.card?.order ?? 999));
  const defaultId = sorted[0]?.slug || '';

  const projectsBlock = `/* NUEVA GENERATED VIEWING PROJECTS START */
  const VIEWING_PROJECTS = {
${sorted.map((project) => renderViewingProjectEntryJs(project, locale)).join(',\n')}
  };
  const DEFAULT_VIEWING_PROJECT_ID = ${JSON.stringify(defaultId)};
  /* NUEVA GENERATED VIEWING PROJECTS END */`;

  const scenesBlock = `/* NUEVA GENERATED VIEWING SCENES START */
  const PROJECT_VIEWING_SCENE_SETS = {
${sorted.map((project) => renderViewingScenesJs(project, locale)).filter(Boolean).join(',\n')}
  };
  /* NUEVA GENERATED VIEWING SCENES END */`;

  return { projectsBlock, scenesBlock };
}
