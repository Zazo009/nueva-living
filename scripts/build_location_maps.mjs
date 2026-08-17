// Derives the location-map data for every project from a single input: the plot
// coordinate in the project's own "location.site". Everything the map and the
// distance ledger show is computed here -- which reference points are worth
// showing for that particular plot, how far each one is by road, how long the
// drive takes, and which side of its dot each map label sits on.
//
// Why it is a separate script rather than part of build_property_pages.mjs:
// the figures come from real network calls (Nominatim to geocode the catalogue,
// OSRM to route from the plot), and a page build must never depend on a third
// party being up, nor hit those services 90 times for 15 projects x 6 locales.
// So this script runs on demand, writes content/geo/location-maps.json, and the
// page build reads that cache offline and deterministically.
//
//   node scripts/build_location_maps.mjs            # fill in anything missing
//   node scripts/build_location_maps.mjs --refresh  # re-route everything
//   node scripts/build_location_maps.mjs --project=cortijo-blanco-villa-collection
//
// The numbers this writes are published as road distances on a live sales site,
// so nothing here is allowed to guess. If a route cannot be measured the entry
// is left out and the build reports it, rather than falling back to a
// straight-line figure dressed up as a driving distance.

import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const LANDMARKS_FILE = path.join(ROOT, 'content/geo/landmarks.json');
const OUTPUT_FILE = path.join(ROOT, 'content/geo/location-maps.json');
const PROJECTS_DIR = path.join(ROOT, 'content/liora-projects');

// Nominatim's usage policy requires an identifying User-Agent and at most one
// request a second. OSRM's demo server has no published limit but the same
// courtesy applies. Both are only touched for values not already cached.
const USER_AGENT = 'nueva-living-site-build/1.0 (+https://nuevaliving.com)';
const GEOCODE_GAP_MS = 1200;
const ROUTE_GAP_MS = 350;

// A reference point past this road distance stops being a selling point and
// starts being noise. The beach and the airport are exempt: both are mandatory
// ledger rows, and cutting the beach at 6km simply deleted the row for a
// project whose nearest sand is 6.2km away, leaving a five-row ledger.
const MAX_RELEVANT_KM = { beach: Infinity, marina: 12, centre: 15, golf: 20, airport: Infinity };

// Golf is judged on the drive, not the map distance: a course 16km away at 21
// minutes up the coast road is a real amenity, while one 12km away through town
// may not be. A flat 15km cap left central Estepona with a single course and a
// five-row ledger even though its second is a 21-minute drive.
const MAX_RELEVANT_MIN = { golf: 22 };

// The ledger is six rows in this order. One beach, one marina, one town centre,
// the two nearest golf courses, one airport -- the spec's fixed shape, resolved
// per plot instead of hand-picked per project.
const LEDGER_SHAPE = [
  { category: 'beach', count: 1 },
  { category: 'marina', count: 1 },
  { category: 'centre', count: 1 },
  { category: 'golf', count: 2 },
  { category: 'airport', count: 1 }
];

// Only four plates fit on the map face before they start colliding. Prefer the
// points a buyer actually pictures themselves using -- the beach and the marina
// first, then the town, then the nearest course. The airport is a ledger fact,
// never a map label: it sits 45 minutes away and would blow the frame open.
const MAP_LABEL_PRIORITY = ['beach', 'marina', 'centre', 'golf'];
const MAX_MAP_LABELS = 4;
// Rendered height of a label plate (two lines plus padding), used to offset
// plates that would otherwise share a pixel row.
const PLATE_HEIGHT_PX = 46;

const args = process.argv.slice(2);
const REFRESH = args.includes('--refresh');
const ONLY = (args.find((a) => a.startsWith('--project=')) || '').split('=')[1] || null;

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

function readJson(file, fallback = null) {
  if (!fs.existsSync(file)) return fallback;
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function writeJson(file, data) {
  fs.writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`);
}

async function fetchJson(url, label) {
  const response = await fetch(url, { headers: { 'User-Agent': USER_AGENT } });
  if (!response.ok) throw new Error(`${label}: HTTP ${response.status}`);
  return response.json();
}

// -- geocoding -------------------------------------------------------------

async function geocodeCatalogue(catalogue) {
  let filled = 0;
  for (const entry of catalogue.landmarks) {
    if (Array.isArray(entry.ll) && !REFRESH) continue;
    const url = `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(entry.query)}&format=json&limit=1`;
    const results = await fetchJson(url, `geocode ${entry.key}`);
    if (!results.length) {
      console.warn(`  ! no geocode result for ${entry.key} ("${entry.query}") -- left without coordinates`);
      await sleep(GEOCODE_GAP_MS);
      continue;
    }
    entry.ll = [Number(Number(results[0].lat).toFixed(5)), Number(Number(results[0].lon).toFixed(5))];
    entry.geocodedFrom = results[0].display_name;
    filled += 1;
    console.log(`  geocoded ${entry.key.padEnd(22)} ${entry.ll.join(', ')}`);
    await sleep(GEOCODE_GAP_MS);
  }
  if (filled) writeJson(LANDMARKS_FILE, catalogue);
  return filled;
}

// -- geometry --------------------------------------------------------------

function crowKm([lat1, lon1], [lat2, lon2]) {
  const toRad = (deg) => (deg * Math.PI) / 180;
  const R = 6371;
  const dLat = toRad(lat2 - lat1);
  const dLon = toRad(lon2 - lon1);
  const a = Math.sin(dLat / 2) ** 2
    + Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLon / 2) ** 2;
  return 2 * R * Math.asin(Math.sqrt(a));
}

// OSRM takes lon,lat -- reversed from every other coordinate in this codebase,
// which is the single easiest thing to get wrong here.
async function routeByRoad(from, to, profile = 'driving') {
  const coords = `${from[1]},${from[0]};${to[1]},${to[0]}`;
  const url = profile === 'foot'
    ? `https://routing.openstreetmap.de/routed-foot/route/v1/foot/${coords}?overview=false`
    : `https://router.project-osrm.org/route/v1/driving/${coords}?overview=false`;
  const data = await fetchJson(url, `route (${profile})`);
  if (data.code !== 'Ok' || !data.routes?.length) return null;
  return { metres: data.routes[0].distance, seconds: data.routes[0].duration };
}

// A beach is a line, not a point. Routing to one named beach centroid measured
// Cortijo Blanco's beach at 2.1km when the sand is 900m down the street, because
// the catalogue's "Playa de San Pedro" node sits over a kilometre along the
// shore. So the beach row is not a catalogue entry at all: ask Overpass for the
// real beach geometry nearest this particular plot. The ledger labels the row
// generically ("Beach"/"Playa"/"Strand"), so no place name is needed -- which is
// just as well, since the nearest access is sometimes a named dog beach.
async function nearestBeach(site) {
  const query = `[out:json][timeout:25];
(
  way(around:4000,${site[0]},${site[1]})["natural"="beach"];
  node(around:4000,${site[0]},${site[1]})["natural"="beach"];
);
out center tags 40;`;
  // Overpass is a shared free service and answers 504 whenever it is busy. Two
  // mirrors, two attempts each, before giving up -- a transient upstream hiccup
  // must not fail a site build.
  const endpoints = ['https://overpass-api.de/api/interpreter', 'https://overpass.kumi.systems/api/interpreter'];
  let data = null;
  let lastError = null;
  for (const endpoint of endpoints) {
    for (let attempt = 1; attempt <= 2 && !data; attempt += 1) {
      try {
        const response = await fetch(endpoint, {
          method: 'POST',
          headers: { 'User-Agent': USER_AGENT, 'Content-Type': 'application/x-www-form-urlencoded' },
          body: new URLSearchParams({ data: query })
        });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        data = await response.json();
      } catch (error) {
        lastError = error;
        await sleep(2500 * attempt);
      }
    }
    if (data) break;
  }
  if (!data) throw new Error(`overpass unavailable (${lastError?.message || 'unknown'})`);
  const points = (data.elements || [])
    .map((element) => {
      const centre = element.center || { lat: element.lat, lon: element.lon };
      if (typeof centre.lat !== 'number' || typeof centre.lon !== 'number') return null;
      return { ll: [Number(centre.lat.toFixed(5)), Number(centre.lon.toFixed(5))], name: element.tags?.name || null };
    })
    .filter(Boolean)
    .sort((a, b) => crowKm(site, a.ll) - crowKm(site, b.ll));
  return points[0] || null;
}

// The sea label needs open water. Walk south from the plot until the point is
// clear of the coast, then keep it there: ~3km offshore puts the Mediterranean
// in the lower third of the frame on every project along this coast.
function seaPoint(site) {
  return [Number((site[0] - 0.027).toFixed(5)), site[1]];
}

// Anything a buyer could plausibly walk to gets measured on the walking network
// instead of the road network, because the two genuinely differ: the beach below
// Cortijo Blanco is 838m by car and 902m on foot, and the promenade routes a
// pedestrian takes do not exist for a car at all. Above this the figure is a
// drive -- claiming a walk to a beach across the A-7 is the kind of detail a
// buyer checks on arrival.
const WALKABLE_CATEGORIES = new Set(['beach', 'centre', 'marina']);
const WALK_CONSIDER_METRES = 1600;
const WALK_CLAIM_METRES = 1200;

// Which side of its dot a label sits on. Points west of the plot get their
// plate to the left, east to the right, so no plate ever crosses the pin. This
// stays geographic in RTL: a label belongs on the side its place is on.
function labelSide(site, ll) {
  return ll[1] < site[1] ? 'left' : 'right';
}

// -- selection -------------------------------------------------------------

// Measures one candidate on the road network, then re-measures it on foot when
// it is close enough that a walk is the honest way to describe it.
async function measureOne(site, candidate, cache) {
  const driveKey = `${site.join(',')}->${candidate.key}`;
  let drive = REFRESH ? null : cache[driveKey];
  if (!drive) {
    drive = await routeByRoad(site, candidate.ll, 'driving');
    await sleep(ROUTE_GAP_MS);
    if (!drive) return null;
    cache[driveKey] = drive;
  }

  let chosen = { ...drive, mode: 'drive' };
  // Whether to try the walking network is decided on straight-line distance,
  // not on the drive. Jardin del Mar's beach is 550m away but 3.4km by car,
  // because the N-340 forces a detour a pedestrian simply walks under -- gating
  // on the drive meant the foot profile was never consulted and a beach across
  // the road was published as a seven-minute drive.
  const crowMetres = crowKm(site, candidate.ll) * 1000;
  if (WALKABLE_CATEGORIES.has(candidate.category)
    && (drive.metres <= WALK_CONSIDER_METRES || crowMetres <= WALK_CONSIDER_METRES)) {
    const walkKey = `${site.join(',')}->${candidate.key}#foot`;
    let walk = REFRESH ? null : cache[walkKey];
    if (!walk) {
      walk = await routeByRoad(site, candidate.ll, 'foot');
      await sleep(ROUTE_GAP_MS);
      if (walk) cache[walkKey] = walk;
    }
    if (walk && walk.metres <= WALK_CLAIM_METRES) chosen = { ...walk, mode: 'walk' };
  }

  return {
    key: candidate.key,
    category: candidate.category,
    proper: candidate.proper,
    short: candidate.short || null,
    ll: candidate.ll,
    metres: Math.round(chosen.metres),
    km: Number((chosen.metres / 1000).toFixed(2)),
    min: Math.max(1, Math.round(chosen.seconds / 60)),
    mode: chosen.mode
  };
}

async function measureCandidates(site, catalogue, cache, beach) {
  const candidates = [];
  if (beach) candidates.push({ key: 'beach', category: 'beach', proper: null, ll: beach.ll });
  for (const entry of catalogue.landmarks) {
    if (entry.category === 'beach') continue; // resolved from real geometry, not the catalogue
    if (!Array.isArray(entry.ll)) continue;
    const limit = MAX_RELEVANT_KM[entry.category] ?? 12;
    // Crow distance is only ever used to decide whether a candidate is worth
    // routing -- never as a published figure. Road distance always exceeds it,
    // so a generous 1.6x screen cannot discard a genuinely close landmark.
    if (crowKm(site, entry.ll) > limit * 1.6) continue;
    candidates.push(entry);
  }

  const measured = [];
  for (const candidate of candidates) {
    const result = await measureOne(site, candidate, cache);
    if (!result) {
      console.warn(`  ! could not route to ${candidate.key} -- skipped`);
      continue;
    }
    const minuteLimit = MAX_RELEVANT_MIN[candidate.category];
    const limit = MAX_RELEVANT_KM[candidate.category] ?? 12;
    if (minuteLimit ? result.min > minuteLimit : result.km > limit) continue;
    // A plot that routes to nothing is sitting on the landmark: the geocode
    // resolved to the reference point itself, not to the project. Los Olivos
    // matched "Aloha Golf Club" and would have published "Aloha golf -- 0 m".
    // Drop it and let the next nearest fill the slot; the site coordinate is
    // the thing at fault and gets reported.
    if (result.metres < 120) {
      console.warn(`  ! ${candidate.key} routes to ${result.metres}m -- location.site appears to sit on this landmark; row dropped`);
      continue;
    }
    measured.push(result);
  }
  return measured;
}

function selectLedger(measured) {
  const byCategory = new Map();
  for (const item of measured) {
    if (!byCategory.has(item.category)) byCategory.set(item.category, []);
    byCategory.get(item.category).push(item);
  }
  // Airports rank by drive time, not distance. Gibraltar is a kilometre or two
  // nearer than Malaga from the western projects while being a slower drive and
  // far less use to a buyer, and sorting on metres alone put it on five ledgers.
  for (const [category, list] of byCategory) {
    list.sort((a, b) => (category === 'airport' ? a.min - b.min || a.metres - b.metres : a.metres - b.metres));
  }

  const rows = [];
  const missing = [];
  for (const { category, count } of LEDGER_SHAPE) {
    const available = byCategory.get(category) || [];
    if (available.length < count) missing.push(`${category} (found ${available.length}, wanted ${count})`);
    rows.push(...available.slice(0, count));
  }
  return { rows, missing };
}

// Four map labels, chosen by what a buyer pictures rather than by raw distance,
// and never two plates on the same side at nearly the same latitude.
function selectMapLabels(rows, site) {
  const chosen = [];
  for (const category of MAP_LABEL_PRIORITY) {
    for (const row of rows.filter((r) => r.category === category)) {
      if (chosen.length >= MAX_MAP_LABELS) break;
      chosen.push(row);
      break;
    }
  }
  // Fill any spare slot with the next nearest non-airport point.
  for (const row of rows) {
    if (chosen.length >= MAX_MAP_LABELS) break;
    if (row.category === 'airport' || chosen.includes(row)) continue;
    chosen.push(row);
  }

  const placed = chosen.map((row) => ({ ...row, side: labelSide(site, row.ll) }));
  // Plates are ~46px tall. Two on the same side within ~0.004 deg of latitude
  // (~450m, which is under a plate's height at these zooms) would overlap, so
  // the lower one is nudged up. The dot never moves -- only the plate.
  const bySide = { left: [], right: [] };
  for (const item of placed.sort((a, b) => b.ll[0] - a.ll[0])) {
    const stack = bySide[item.side];
    // A nudge has to clear a whole plate, not soften the overlap. Guadalmina
    // golf and San Pedro centre sit 19m apart in latitude, landed on the same
    // pixel row, and a -16px offset still left one printed over the other.
    const clashes = stack.filter((other) => Math.abs(other.ll[0] - item.ll[0]) < 0.006);
    item.dy = clashes.length ? -PLATE_HEIGHT_PX * clashes.length : 0;
    stack.push(item);
  }
  return placed;
}

// -- main ------------------------------------------------------------------

async function main() {
  const catalogue = readJson(LANDMARKS_FILE);
  if (!catalogue) throw new Error(`missing ${path.relative(ROOT, LANDMARKS_FILE)}`);

  console.log('Geocoding catalogue...');
  const filled = await geocodeCatalogue(catalogue);
  console.log(filled ? `  ${filled} coordinate(s) resolved` : '  all coordinates already cached');

  const existing = readJson(OUTPUT_FILE, { routeCache: {}, projects: {} });
  const cache = existing.routeCache || {};
  const projects = REFRESH ? {} : existing.projects || {};

  const slugs = fs.readdirSync(PROJECTS_DIR).filter((slug) => {
    if (ONLY && slug !== ONLY) return false;
    return fs.existsSync(path.join(PROJECTS_DIR, slug, 'project.json'));
  });

  const skipped = [];
  const report = [];
  for (const slug of slugs) {
    const project = readJson(path.join(PROJECTS_DIR, slug, 'project.json'));
    const site = project.location?.site;
    if (!Array.isArray(site) || site.length !== 2) {
      skipped.push(slug);
      continue;
    }
    if (projects[slug] && !REFRESH) {
      report.push(`${slug}: cached`);
      continue;
    }

    console.log(`\nRouting ${slug} from ${site.join(', ')}`);
    const beachKey = `beach@${site.join(',')}`;
    let beach = cache[beachKey];
    if (!beach) {
      beach = await nearestBeach(site);
      if (beach) cache[beachKey] = beach;
    }
    if (beach) {
      console.log(`  nearest beach geometry ${beach.ll.join(', ')}${beach.name ? ` (${beach.name})` : ''}`);
    } else {
      console.warn('  ! no beach found within 4km -- the beach row will be missing');
    }
    const measured = await measureCandidates(site, catalogue, cache, beach);
    const { rows, missing } = selectLedger(measured);
    const mapLabels = selectMapLabels(rows, site);

    projects[slug] = {
      site,
      sea: seaPoint(site),
      rows: rows.map(({ ll, ...row }) => ({ ...row, ll })),
      mapLabels: mapLabels.map((row) => ({ key: row.key, side: row.side, dy: row.dy })),
      measuredAt: new Date().toISOString().slice(0, 10),
      source: 'OSRM driving route from location.site; landmark coordinates from OpenStreetMap via Nominatim'
    };
    if (missing.length) projects[slug].incomplete = missing;
    report.push(`${slug}: ${rows.length} rows${missing.length ? ` (short: ${missing.join('; ')})` : ''}`);
  }

  writeJson(OUTPUT_FILE, { routeCache: cache, projects });

  console.log('\n--- summary ---');
  for (const line of report) console.log(`  ${line}`);
  if (skipped.length) {
    console.log(`\n  ${skipped.length} project(s) have no "location.site" and were skipped:`);
    for (const slug of skipped) console.log(`    ${slug}`);
    console.log('  Add the plot coordinate as location.site: [lat, lng] to generate a map for these.');
  }
  console.log(`\nWrote ${path.relative(ROOT, OUTPUT_FILE)}`);
}

main().catch((error) => {
  console.error(`\nbuild_location_maps failed: ${error.message}`);
  process.exit(1);
});
