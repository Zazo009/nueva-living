// The catalogue the assistant connector (netlify/functions/nueva-mcp.js) answers from.
//
// The connector lets a person search the projects from inside Claude or ChatGPT. Whatever it
// returns is published the moment an assistant reads it, so this file is built from the same
// public fields the project pages print, in the same ten languages, and from nothing else: no
// `crm` block, no internal notes, no developer. The one exception is a handful of numbers from
// `crm` (price floor and ceiling, bedroom range, unit count, construction stage) that the cards
// and the compare table already publish; they are copied as numbers, never as text.
//
// audit_site_consistency checks every entry against its own project's real name and developer,
// the same way it checks the project's pages.
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { LOCALES, localizeProject, pageUrl } from './i18n.mjs';
import { PRICE_FORMAT } from './prices.mjs';
import { localizeMonthDate } from './dates.mjs';
import { unitSize } from './unit_size.mjs';

const SITE = 'https://nuevaliving.com';
const MAX_IMAGES = 8;

// The features a person can require in a search. Each is read from the project's own tags and
// amenity list, which the page already prints; a project is only given a feature its page names.
const FEATURES = {
  sea_view: [/^sea views?$/i, /^panoramic views$/i],
  private_pool: [/^private (rooftop )?pool$/i],
  communal_pool: [/^communal (outdoor )?pools?/i, /^outdoor pool$/i],
  indoor_pool: [/indoor (heated )?pool|heated indoor pool/i],
  beach: [/^walk to beach$/i, /^beachfront$/i, /^beachside$/i, /^beach living$/i],
  golf: [/^golf( view| frontline| valley)?$/i],
  gated: [/^gated community$/i, /^24-hour security$/i, /^privacy & security$/i],
  gym: [/gym$/i],
  spa: [/^(indoor )?spa$/i, /^sauna$/i, /^hammam$/i],
  garden: [/^private garden$/i],
  rooftop: [/rooftop (solarium|pool)/i, /^solarium$/i],
  lift: [/^(private )?lift$/i],
  smart_home: [/^smart home$/i, /^home automation$/i],
  coworking: [/^coworking( space)?$/i],
  ev_charging: [/ev charging|electric vehicle charging/i],
  mountain_view: [/^mountain views$/i],
};

function featuresOf(project) {
  const discovery = project.discovery || {};
  const names = [
    ...(discovery.practicalTags || []), ...(discovery.lifestyleTags || []),
    ...(discovery.locationTags || []), ...(discovery.architectureTags || []),
    ...((project.crm?.amenities || []).filter((a) => typeof a === 'string')),
  ];
  return Object.entries(FEATURES)
    .filter(([, patterns]) => names.some((name) => patterns.some((re) => re.test(String(name).trim()))))
    .map(([key]) => key);
}

// Overlays that never translated a price leave it in English grouping ("€450,000") on a Swedish
// answer. The site's own pages fix that when they render; this does the same with the same table.
function localPrices(value, locale) {
  const format = PRICE_FORMAT[locale];
  if (!format || !value) return value;
  return value.replace(/(?:EUR\s*|€\s?)(\d{1,3}(?:,\d{3})+)/g, (whole, digits) => format(digits));
}

function eur(value) {
  const match = /(?:EUR|€)\s*([\d,.]+)/.exec(String(value || ''));
  if (!match) return null;
  const n = Number(match[1].replace(/[.,](?=\d{3}\b)/g, ''));
  return Number.isFinite(n) && n > 10000 ? n : null;
}

function bedroomsOf(value) {
  const match = /(\d+)/.exec(String(value || ''));
  return match ? Number(match[1]) : null;
}

function absolute(src) {
  if (!src) return null;
  return /^https?:\/\//.test(src) ? src : `${SITE}/${String(src).replace(/^\/+/, '')}`;
}

function text(value) {
  if (typeof value !== 'string') return '';
  // Headlines carry <em> for the italic half; an assistant wants plain text.
  return value.replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
}

function constructionStage(value) {
  const v = String(value || '').trim().toLowerCase();
  if (['off_plan', 'under_construction', 'completed'].includes(v)) return v;
  if (v.startsWith('under construction')) return 'under_construction';
  if (v.startsWith('off-plan') || v.startsWith('off plan')) return 'off_plan';
  if (v.includes('key ready') || v.includes('completed') || v.startsWith('resale')) return 'completed';
  return null;
}

function numberOrNull(value) {
  if (value === null || value === undefined || value === '') return null;
  const n = Number(value);
  return Number.isFinite(n) ? n : null;
}

function localeEntry(project, locale) {
  const p = localizeProject(project, locale);
  const availability = p.availability || {};
  return {
    name: p.name,
    url: pageUrl(project.output, locale),
    summary: text(p.card?.description || p.description),
    description: text(p.description),
    location: text(p.hero?.location || p.card?.locExtended),
    type: text(p.hero?.type || p.card?.typeTag),
    delivery: text(p.hero?.delivery),
    from: localPrices(text(p.hero?.startingPrice), locale),
    priceRange: localPrices(text(availability.priceRange), locale),
    availability: text(availability.copy),
    priceNote: text(availability.sourceNote),
    checked: localizeMonthDate(text(availability.checkedDate), locale),
    why: text(p.why?.copy),
    locationNote: text(p.location?.copy),
    distances: (p.location?.distances || [])
      .filter((row) => Array.isArray(row) && row.length >= 2)
      .map(([place, distance]) => [text(place), text(distance)]),
    units: (availability.units || []).map((unit) => ({
      ref: text(unit.reference),
      bedrooms: text(unit.bedrooms),
      size: text(unit.size),
      price: localPrices(text(unit.price), locale),
    })),
    images: (p.media?.items || [])
      .filter((item) => item?.src && !/\.(mp4|pdf)$/i.test(item.src))
      .slice(0, MAX_IMAGES)
      .map((item) => ({ url: absolute(item.src), alt: text(item.alt) })),
    mediaNote: text(p.media?.copy),
  };
}

function areaList() {
  const areas = JSON.parse(readFileSync(path.resolve('content/nueva-areas.json'), 'utf8'));
  return areas.map((area) => ({
    slug: area.slug,
    names: Object.fromEntries(LOCALES.map(({ code }) => [code, area.i18n?.[code]?.name || area.name])),
    url: area.output ? pageUrl(area.output, 'en') : null,
  }));
}

export function buildMcpCatalog(projects) {
  return { areas: areaList(), projects: buildProjects(projects) };
}

function buildProjects(projects) {
  return projects
    .filter((project) => !project.archived && project.output)
    .map((project) => {
      const crm = project.crm || {};
      const discovery = project.discovery || {};
      const site = project.location?.site;
      const tags = [
        ...(discovery.lifestyleTags || []),
        ...(discovery.architectureTags || []),
        ...(discovery.locationTags || []),
        ...(discovery.investmentTags || []),
        ...(discovery.practicalTags || []),
      ];
      return {
        slug: project.slug,
        area: discovery.area || crm.area || null,
        propertyTypes: crm.propertyTypes || discovery.propertyTypes || [],
        status: constructionStage(crm.constructionStatus),
        priceMin: numberOrNull(crm.priceMin ?? discovery.price),
        priceMax: numberOrNull(crm.priceMax),
        bedroomsMin: numberOrNull(crm.bedroomsMin),
        bedroomsMax: numberOrNull(crm.bedroomsMax),
        completion: discovery.completionSort || null,
        tags: [...new Set(tags)],
        features: featuresOf(project),
        // Numbers read from the English price list, one per home, for budget and bedroom search.
        // sqm is the developer's own figure, built where given, otherwise interior; sizeBasis says
        // which (scripts/lib/unit_size.mjs explains why there is no conversion between them).
        homes: (project.availability?.units || []).map((unit) => {
          const size = unitSize(unit.size);
          return {
            priceEur: eur(unit.price),
            bedrooms: bedroomsOf(unit.bedrooms),
            sqm: size ? size.sqm : null,
            sizeBasis: size ? size.basis : null,
          };
        }),
        image: absolute(project.images?.card?.src || project.images?.hero?.src),
        // Every pin on the site is the developer's own location or our reading of their map;
        // none is a cadastral point. The connector says so whatever the source.
        coordinates: Array.isArray(site) && site.length === 2 ? site : null,
        locales: Object.fromEntries(LOCALES.map(({ code }) => [code, localeEntry(project, code)])),
      };
    })
    .sort((a, b) => a.slug.localeCompare(b.slug));
}
