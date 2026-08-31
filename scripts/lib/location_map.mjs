// Renders the project location card: a real, accurately projected map on one
// side and a distance ledger on the other. Every figure it prints comes from
// content/geo/location-maps.json, which build_location_maps.mjs produced by
// routing from the plot -- nothing here invents or rounds a distance into
// something friendlier than the road actually is.
//
// The card is a still graphic that happens to be built from live map data:
// no pan, no zoom, no popups. Interaction would invite a buyer to treat an
// indicative plot marker as a survey.

import fs from 'node:fs';
import path from 'node:path';
import { t, DEFAULT_LOCALE } from './i18n.mjs';

const CACHE_FILE = path.join(process.cwd(), 'content/geo/location-maps.json');

// Pinned to the exact Leaflet the spec was verified against, with SRI hashes so
// a compromised CDN cannot inject script into a property page.
export const LEAFLET_VERSION = '1.9.4';
const LEAFLET_CSS_SRI = 'sha384-sHL9NAb7lN7rfvG5lfHpm643Xkcjzp4jFvuavGOndn6pjVqS6ny56CAt3nsEVT4H';
const LEAFLET_JS_SRI = 'sha384-cxOPjt7s7Iz04uaHJceBmS+qpjv2JkIHNVcuOrM+YHwZOmJGBXI00mdUXEq65HTH';

let cache = null;

function loadCache() {
  if (cache) return cache;
  cache = fs.existsSync(CACHE_FILE)
    ? JSON.parse(fs.readFileSync(CACHE_FILE, 'utf8'))
    : { projects: {} };
  return cache;
}

// A project gets the live map only once its plot coordinate has been routed.
// Everything else keeps the existing stylised SVG map, so adding this feature
// cannot blank out the location section on 14 projects.
export function hasLiveLocationMap(slug) {
  const entry = loadCache().projects?.[slug];
  return Boolean(entry?.site && entry.rows?.length);
}

export function locationMapData(slug) {
  return loadCache().projects?.[slug] || null;
}

const esc = (value) => String(value ?? '')
  .replace(/&/g, '&amp;')
  .replace(/</g, '&lt;')
  .replace(/>/g, '&gt;')
  .replace(/"/g, '&quot;');

// Place names never translate -- Puerto Banús stays Puerto Banús in Russian.
// Only the category word around a name is localised, which is why every label
// is built from a template carrying {name} rather than from a translated string.
// A plate on the map face has roughly 120px before it collides with a
// neighbour or clips the frame, so the map uses the short form of a name where
// one exists ("San Pedro", not "San Pedro de Alcantara centre"). The ledger has
// a full 380px column and always prints the full name.
// Towns keep their own name in Russian and Arabic; venues do not.
//
// The rule above -- place names never translate -- is right for the venues on
// these maps. "Valderrama", "Finca Cortesin" and "Aloha" ARE the names of
// those golf courses, and a Russian golfer looking for Valderrama is looking
// for Valderrama. It reads wrong only for the towns, where the rest of the
// site says Марбелья and ماربيا everywhere else and only the map said
// "Marbella", leaving "Центр Marbella" beside "Гольф-клуб Río Real".
//
// Arabic is the sharper case: a Latin run inside right-to-left text breaks the
// line's direction, which no amount of familiarity fixes.
//
// Every form below is the one already dominant in the built corpus, so this
// introduces no new spelling. Atalaya and Cabopino are absent deliberately --
// they are urbanisations with no established Cyrillic or Arabic form.
const TOWN_NAMES = {
  'Marbella': { ru: 'Марбелья', ruGen: 'Марбельи', ar: 'ماربيا' },
  'Estepona': { ru: 'Эстепона', ruGen: 'Эстепоны', ar: 'إستيبونا' },
  'Málaga': { ru: 'Малага', ruGen: 'Малаги', ar: 'مالقة' },
  'Fuengirola': { ru: 'Фуэнхирола', ruGen: 'Фуэнхиролы', ar: 'فوينخيرولا' },
  'San Pedro de Alcántara': { ru: 'Сан-Педро-де-Алькантара', ar: 'سان بيدرو دي الكانتارا' },
  'San Pedro': { ru: 'Сан-Педро', ar: 'سان بيدرو' },
  'Puerto Banús': { ru: 'Пуэрто-Банус', ruGen: 'Пуэрто-Бануса', ar: 'بويرتو بانوس' },
  'Benahavís': { ru: 'Бенаавис', ruGen: 'Бенаависа', ar: 'بيناهافيس' },
  'Guadalmina': { ru: 'Гуадальмина', ruGen: 'Гуадальмины', ar: 'غوادالمينا' },
  'Mijas Pueblo': { ru: 'Михас-Пуэбло', ar: 'ميخاس بويبلو' },
  'Gibraltar': { ru: 'Гибралтар', ruGen: 'Гибралтара', ar: 'جبل طارق' },
  'La Cala': { ru: 'Ла-Кала', ruGen: 'Ла-Калы', ar: 'لا كالا' }
};

// A half-added town is worse than an absent one: it would render natively in
// Russian and stay Latin in Arabic on the same map, which is the exact split
// this table exists to close.
for (const [name, forms] of Object.entries(TOWN_NAMES)) {
  const missing = ['ru', 'ar'].filter((locale) => !forms[locale]);
  if (missing.length) {
    throw new Error(`TOWN_NAMES["${name}"] is missing ${missing.join(' and ')}. `
      + 'Add every locale at once, or leave the town out and let it stay Latin.');
  }
}

// "Центр" and "Аэропорт" govern the genitive; "Гольф-клуб X" is an
// apposition and stays nominative. San Pedro and Mijas Pueblo do not decline,
// so they carry no genitive form and fall back to the nominative.
const RU_GENITIVE_CATEGORIES = new Set(['centre', 'airport']);

function localTownName(name, locale, category) {
  const town = TOWN_NAMES[name];
  if (!town) return name;
  if (locale === 'ru' && RU_GENITIVE_CATEGORIES.has(category)) return town.ruGen || town.ru;
  return town[locale] || name;
}

function referenceLabel(row, locale, { short = false } = {}) {
  if (row.category === 'beach') return t('locmap.beach', locale);
  const name = localTownName((short && row.short) || row.proper || '', locale, row.category);
  const template = short && row.short && row.category === 'centre'
    ? name // a bare town name reads as the town on the map; "Centre of X" does not fit
    : t(`locmap.${row.category}`, locale, { name });
  return String(template).replace(/\s+/g, ' ').trim();
}

// Arabic distinguishes 3-10 minutes (plural "daqaiq") from 11+ (singular
// "daqiqa"). Getting this wrong is immediately visible to a Gulf buyer.
function minutesWord(min, mode, locale) {
  if (mode === 'walk') {
    const walk = t('locmap.walk', locale);
    if (locale !== 'ar') return walk;
    return `${min >= 3 && min <= 10 ? t('locmap.minutesFew', locale) : t('locmap.drive', locale)} ${walk}`;
  }
  if (locale === 'ar') return min >= 3 && min <= 10 ? t('locmap.minutesFew', locale) : t('locmap.drive', locale);
  return t('locmap.drive', locale);
}

// Arabic property marketing uses Latin digits and a Western decimal separator,
// so the numbering system is forced rather than left to the locale default.
function numberLocale(locale) {
  return locale === 'ar' ? 'ar-u-nu-latn' : locale;
}

// Under a kilometre the honest unit is metres, rounded to the nearest 10 -- a
// routed 902m printed as "902 m" claims a precision the plot boundary does not
// have. Above 10km whole kilometres; below it, one decimal.
function formatDistance(row, locale) {
  const nf = (options) => new Intl.NumberFormat(numberLocale(locale), options);
  if (row.metres < 1000) {
    const rounded = Math.round(row.metres / 10) * 10;
    return `${nf({ maximumFractionDigits: 0 }).format(rounded)} ${t('locmap.unitM', locale)}`;
  }
  const km = row.km;
  const value = km >= 10
    ? nf({ maximumFractionDigits: 0 }).format(Math.round(km))
    : nf({ minimumFractionDigits: 1, maximumFractionDigits: 1 }).format(km);
  return `${value} ${t('locmap.unitKm', locale)}`;
}

function formatMinutes(row, locale) {
  const value = new Intl.NumberFormat(numberLocale(locale), { maximumFractionDigits: 0 }).format(row.min);
  return `${value} ${minutesWord(row.min, row.mode, locale)}`;
}

function ledgerRows(data, locale) {
  return data.rows.map((row) => `
            <div class="locmap-row">
              <span class="locmap-row-label">${esc(referenceLabel(row, locale))}</span>
              <span class="locmap-row-figure"><bdi>${esc(formatDistance(row, locale))}</bdi> <em><bdi>${esc(formatMinutes(row, locale))}</bdi></em></span>
            </div>`).join('');
}

// The map labels are handed to the browser as data rather than pre-rendered
// HTML, because only Leaflet knows where a coordinate lands in pixels.
function mapPayload(data, locale) {
  const byKey = new Map(data.rows.map((row) => [row.key, row]));
  const labels = (data.mapLabels || []).map((label) => {
    const row = byKey.get(label.key);
    if (!row) return null;
    return {
      ll: row.ll,
      side: label.side,
      dy: label.dy || 0,
      golf: row.category === 'golf',
      name: referenceLabel(row, locale, { short: true }),
      sub: `${formatDistance(row, locale)} · ${formatMinutes(row, locale)}`
    };
  }).filter(Boolean);

  return {
    site: data.site,
    sea: data.sea,
    seaLabel: t('locmap.sea', locale),
    labels
  };
}

// Leaflet's stylesheet used to block the first paint of every property page,
// on a third-party origin, for a map that is the fifth section down. The
// container is a fixed 600px tall, so the late stylesheet cannot shift
// anything above it. Same media="print" swap the site already uses for its
// own below-the-fold CSS, with the noscript fallback that goes with it.
export function leafletHead() {
  const css = `https://unpkg.com/leaflet@${LEAFLET_VERSION}/dist/leaflet.css`;
  return `  <link rel="stylesheet" href="${css}" integrity="${LEAFLET_CSS_SRI}" crossorigin="anonymous" media="print" onload="this.media='all'" />
  <noscript><link rel="stylesheet" href="${css}" integrity="${LEAFLET_CSS_SRI}" crossorigin="anonymous" /></noscript>
  <script src="https://unpkg.com/leaflet@${LEAFLET_VERSION}/dist/leaflet.js" integrity="${LEAFLET_JS_SRI}" crossorigin="anonymous" defer></script>`;
}

export function renderLocationCard(project, locale = DEFAULT_LOCALE) {
  const data = locationMapData(project.slug);
  if (!data) return '';
  const rtl = locale === 'ar';
  const place = project.location?.mapLabelPlain
    || String(project.hero?.location || '').trim()
    || project.name;

  return `
        <div class="locmap${rtl ? ' locmap-rtl' : ''}" lang="${esc(locale)}"${rtl ? ' dir="rtl"' : ''}>
          <div class="locmap-map" id="locmap-${esc(project.slug)}" data-locmap='${esc(JSON.stringify(mapPayload(data, locale)))}' role="img" aria-label="${t('aria.indicativeLocationMap', locale, { name: esc(project.name) })}"></div>
          <aside class="locmap-panel">
            <span class="locmap-kicker">${t('locmap.kicker', locale)}</span>
            <h3 class="locmap-name">${esc(project.name)}</h3>
            <p class="locmap-place">${esc(place)}</p>
            <div class="locmap-ledger">${ledgerRows(data, locale)}
            </div>
            <p class="locmap-note">${t('locmap.disclaimer', locale)}</p>
          </aside>
        </div>`;
}
