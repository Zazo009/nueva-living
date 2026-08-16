// Translations for the chrome on the listing card (lib/project_card.mjs).
//
// The homepage, developments and segment grids are rendered once in English
// and turned into the other five languages by find/replace entry tables.
// The area pages render per locale with t() directly and do not need these,
// but they are harmless there.
//
// Two kinds of entry live here:
//
//   Static   fixed wording -- the column labels, "From", the CTA, the status
//            badges. Written out once.
//
//   Derived  wording that contains numbers: "14 of 88 left", "2-4 bed", and
//            the delivery strings, which differ per project. These cannot be
//            hand-written because the numbers vary, so they are generated
//            from the project files and the same i18n strings the area pages
//            use. A new project needs no entry here.
//
// Every entry is keyed on the class name that immediately precedes the text
// so it can never match the same words elsewhere in the page.

import { readdirSync, readFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

import { t } from './i18n.mjs';

const LOCALES = ['es', 'fr', 'de', 'ru', 'ar'];
const PROJECT_DIR = join(dirname(fileURLToPath(import.meta.url)), '..', '..', 'content', 'liora-projects');

function escapeHtml(value) {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

// Build one entry from an i18n key: English is the `find`, each locale the
// replacement, both wrapped in the class prefix that anchors the match.
function entryFromKey(prefix, key, vars = {}) {
  const entry = { find: `${prefix}${escapeHtml(t(key, 'en', vars))}<` };
  for (const locale of LOCALES) {
    entry[locale] = `${prefix}${escapeHtml(t(key, locale, vars))}<`;
  }
  return entry;
}

export const CARD_CHROME_ENTRIES = [
  // Status badge over the image
  { find: 'dev-badge">Completed, Ready To Move In', es: 'dev-badge">Finalizado, Listo para Entrar', fr: 'dev-badge">Terminé, Prêt à Emménager', de: 'dev-badge">Fertiggestellt, Bezugsfertig', ru: 'dev-badge">Завершено, Готово к Заселению', ar: 'dev-badge">مكتمل، جاهز للسكن' },
  { find: 'dev-badge">Current Release', es: 'dev-badge">Fase Actual', fr: 'dev-badge">Phase Actuelle', de: 'dev-badge">Aktuelle Phase', ru: 'dev-badge">Текущая Очередь', ar: 'dev-badge">المرحلة الحالية' },
  { find: 'dev-badge">Off-plan, Private Availability', es: 'dev-badge">Sobre Plano, Disponibilidad Privada', fr: 'dev-badge">Sur Plan, Disponibilité Privée', de: 'dev-badge">Off-Plan, Private Verfügbarkeit', ru: 'dev-badge">На Этапе Строительства, Закрытая Продажа', ar: 'dev-badge">على المخطط، إتاحة حصرية' },
  { find: 'dev-badge">Off-Plan', es: 'dev-badge">Sobre Plano', fr: 'dev-badge">Sur Plan', de: 'dev-badge">Off-Plan', ru: 'dev-badge">На Этапе Строительства', ar: 'dev-badge">على المخطط' },
  { find: 'dev-badge">Sea View Collection', es: 'dev-badge">Colección con Vistas al Mar', fr: 'dev-badge">Collection Vue Mer', de: 'dev-badge">Kollektion mit Meerblick', ru: 'dev-badge">Коллекция с Видом на Море', ar: 'dev-badge">مجموعة بإطلالة على البحر' },
  { find: 'dev-badge">Under Construction', es: 'dev-badge">En Construcción', fr: 'dev-badge">En Construction', de: 'dev-badge">Im Bau', ru: 'dev-badge">В Стадии Строительства', ar: 'dev-badge">قيد الإنشاء' },

  // Fixed card chrome
  entryFromKey('dev-price-label">', 'card.from'),
  entryFromKey('dev-fact-label">', 'card.delivery'),
  entryFromKey('dev-fact-label">', 'card.homes'),
  entryFromKey('dev-fact-label">', 'card.available'),
  entryFromKey('dev-cta-label">', 'cta.exploreProject')
];

// --- derived entries -------------------------------------------------------

function projects() {
  const out = [];
  for (const slug of readdirSync(PROJECT_DIR)) {
    const file = join(PROJECT_DIR, slug, 'project.json');
    if (!existsSync(file)) continue;
    out.push(JSON.parse(readFileSync(file, 'utf8')));
  }
  return out;
}

const derived = [];
const seen = new Set();
const push = (entry) => {
  if (seen.has(entry.find)) return;
  seen.add(entry.find);
  derived.push(entry);
};

for (const project of projects()) {
  const crm = project.crm || {};

  // "14 of 88 left" on the badge
  const available = Number.isFinite(crm.availableUnits)
    ? crm.availableUnits
    : (project.availability?.units || []).length;
  const total = crm.totalUnits;
  if (available > 0 && Number.isFinite(total) && total > 0) {
    push(entryFromKey('dev-badge-units">', 'card.unitsLeft', { available, total }));
    push(entryFromKey('dev-fact-value">', 'card.unitsOf', { available, total }));
  }

  // "2-4 bed" in the Homes column
  const min = crm.bedroomsMin;
  const max = crm.bedroomsMax;
  if (Number.isFinite(min) || Number.isFinite(max)) {
    const lo = Number.isFinite(min) ? min : max;
    const hi = Number.isFinite(max) ? max : min;
    push(lo === hi
      ? entryFromKey('dev-fact-value">', 'card.bedSingle', { n: lo })
      : entryFromKey('dev-fact-value">', 'card.bedRange', { min: lo, max: hi }));
  }

  // The release phase, same shape as delivery: prose, per project,
  // translated through the i18n overlay. Empty on every project today, so
  // this generates nothing until the values are filled in.
  const phase = project.availability?.phase;
  if (phase) {
    const entry = { find: `dev-fact-sub">${escapeHtml(phase)}<` };
    let translated = false;
    for (const locale of LOCALES) {
      const value = project.i18n?.[locale]?.availability?.phase;
      entry[locale] = `dev-fact-sub">${escapeHtml(value || phase)}<`;
      if (value && value !== phase) translated = true;
    }
    if (translated) push(entry);
  }

  // Delivery is prose and already translated in each project's i18n
  // overlay, so the translation comes from the project rather than a string
  // key. Skipped when the locale has no overlay for it.
  const english = project.hero?.delivery;
  if (english) {
    const entry = { find: `dev-fact-value">${escapeHtml(english)}<` };
    let translated = false;
    for (const locale of LOCALES) {
      const value = project.i18n?.[locale]?.hero?.delivery;
      entry[locale] = `dev-fact-value">${escapeHtml(value || english)}<`;
      if (value && value !== english) translated = true;
    }
    if (translated) push(entry);
  }
}

// Longest first so a short string cannot eat the opening of a longer one.
derived.sort((a, b) => b.find.length - a.find.length);
CARD_CHROME_ENTRIES.push(...derived);
