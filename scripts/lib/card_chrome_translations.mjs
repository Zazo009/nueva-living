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

const LOCALES = ['es', 'fr', 'de', 'ru', 'ar', 'nl', 'pl', 'sv', 'no'];
const PROJECT_DIR = join(dirname(fileURLToPath(import.meta.url)), '..', '..', 'content', 'liora-projects');

// CRM numbers arrive as numbers on thirteen projects and as strings on one
// ("4", "15"). Number.isFinite rejects a string, so that project silently
// lost its Homes and Available columns and its unit badge -- no error, just
// a card with one fact instead of three. Coerce rather than trust the type.
function toNumber(value) {
  const n = typeof value === 'string' ? Number(value.trim()) : value;
  return Number.isFinite(n) ? n : undefined;
}

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
  { find: 'dev-badge">Completed, Ready To Move In', es: 'dev-badge">Finalizado, listo para entrar', fr: 'dev-badge">Terminé, prêt à emménager', de: 'dev-badge">Fertiggestellt, bezugsfertig', ru: 'dev-badge">Завершено, Готово к Заселению', ar: 'dev-badge">مكتمل، جاهز للسكن', nl: 'dev-badge">Voltooid, klaar om te betrekken', pl: 'dev-badge">Ukończone, gotowe do zamieszkania', sv: 'dev-badge">Färdigställd, inflyttningsklar', no: 'dev-badge">Ferdigstilt, klar for innflytting' },
  { find: 'dev-badge">Current Release', es: 'dev-badge">Fase actual', fr: 'dev-badge">Phase actuelle', de: 'dev-badge">Aktuelle Phase', ru: 'dev-badge">Текущая Очередь', ar: 'dev-badge">المرحلة الحالية', nl: 'dev-badge">Huidige fase', pl: 'dev-badge">Bieżąca pula', sv: 'dev-badge">Aktuell fas', no: 'dev-badge">Gjeldende fase' },
  { find: 'dev-badge">Off-plan, Private Availability', es: 'dev-badge">Sobre plano, disponibilidad privada', fr: 'dev-badge">Sur plan, disponibilité privée', de: 'dev-badge">Off-Plan, private Verfügbarkeit', ru: 'dev-badge">На Этапе Строительства, Закрытая Продажа', ar: 'dev-badge">على المخطط، إتاحة حصرية', nl: 'dev-badge">Op plan, privébeschikbaarheid', pl: 'dev-badge">Sprzedaż z planu, dostępność prywatna', sv: 'dev-badge">Under projektering, privat tillgänglighet', no: 'dev-badge">Under prosjektering, privat tilgjengelighet' },
  { find: 'dev-badge">Off-Plan', es: 'dev-badge">Sobre plano', fr: 'dev-badge">Sur plan', de: 'dev-badge">Off-Plan', ru: 'dev-badge">На Этапе Строительства', ar: 'dev-badge">على المخطط', nl: 'dev-badge">Op plan', pl: 'dev-badge">Sprzedaż z planu', sv: 'dev-badge">Under projektering', no: 'dev-badge">Under prosjektering' },
  { find: 'dev-badge">Key Ready', es: 'dev-badge">Listo para entrar', fr: 'dev-badge">Prêt à emménager', de: 'dev-badge">Bezugsfertig', ru: 'dev-badge">Готово к Заселению', ar: 'dev-badge">جاهز للسكن', nl: 'dev-badge">Sleutelklaar', pl: 'dev-badge">Gotowe do odbioru kluczy', sv: 'dev-badge">Nyckelklar', no: 'dev-badge">Nøkkelklar' },
  { find: 'dev-badge">Sea View Collection', es: 'dev-badge">Colección con vistas al mar', fr: 'dev-badge">Collection vue mer', de: 'dev-badge">Kollektion mit Meerblick', ru: 'dev-badge">Коллекция с Видом на Море', ar: 'dev-badge">مجموعة بإطلالة على البحر', nl: 'dev-badge">Collectie met zeezicht', pl: 'dev-badge">Kolekcja z widokiem na morze', sv: 'dev-badge">Kollektion med havsutsikt', no: 'dev-badge">Kolleksjon med sjøutsikt' },
  { find: 'dev-badge">Under Construction', es: 'dev-badge">En construcción', fr: 'dev-badge">En construction', de: 'dev-badge">Im Bau', ru: 'dev-badge">В Стадии Строительства', ar: 'dev-badge">قيد الإنشاء', nl: 'dev-badge">In aanbouw', pl: 'dev-badge">W budowie', sv: 'dev-badge">Under uppförande', no: 'dev-badge">Under bygging' },

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
  const available = toNumber(crm.availableUnits) ?? (project.availability?.units || []).length;
  const total = toNumber(crm.totalUnits);
  if (available > 0 && total !== undefined && total > 0) {
    push(entryFromKey('dev-badge-units">', 'card.unitsLeft', { available, total }));
    push(entryFromKey('dev-fact-value">', 'card.unitsOf', { available, total }));
  }

  // "2-4 bed" in the Homes column
  const min = toNumber(crm.bedroomsMin);
  const max = toNumber(crm.bedroomsMax);
  if (min !== undefined || max !== undefined) {
    const lo = min !== undefined ? min : max;
    const hi = max !== undefined ? max : min;
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
