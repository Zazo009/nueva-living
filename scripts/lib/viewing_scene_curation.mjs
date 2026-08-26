// The cinematic player used to walk the whole media library in order.
//
// For the Cortijo Blanco villas that meant 55 scenes, of which the first
// fourteen were the outside -- the same garden façade at midday, at dusk and
// after dark, the same pool from five positions -- followed by fourteen of the
// living room. A viewer reached the end having seen one bedroom and one
// bathroom, and the natural reaction is "fine, but what about the rest of the
// house?". The gallery is the right place to browse every frame; a sequence
// that plays on its own has to move on.
//
// The rule is therefore: one frame per subject, and a cap per part of the
// property so no single part can dominate. Two frames that differ only by the
// light or the angle are two frames of the same subject.

// Subject keywords are ordered most-specific first, because a filename names
// more than one thing: "exterior-pool-day" is a photograph of the pool, and
// reading its first word instead would file it under the façade -- which is
// how an earlier version of this returned four pool shots and no façade.
const GROUPS = [
  { name: 'exterior', match: /^(exterior|facade|garden|outdoor|pool|entrance|terrace)/, cap: 4,
    subjects: ['pool', 'garden', 'outdoor', 'entrance', 'street', 'facade', 'exterior', 'terrace'] },
  { name: 'living', match: /^(living|open-plan|kitchen|dining|lounge)/, cap: 4,
    subjects: ['kitchen', 'dining', 'open', 'living', 'lounge'] },
  { name: 'private', match: /^(master|bedroom|bathroom|dressing|guest)/, cap: 4,
    subjects: ['dressing', 'bathroom', 'bedroom', 'guest'] },
  { name: 'solarium', match: /^solarium/, cap: 3,
    subjects: ['pool', 'dining', 'lounge', 'pergola', 'mountain', 'solarium'] },
  { name: 'basement', match: /^basement/, cap: 2,
    subjects: ['cinema', 'lounge', 'gym', 'basement'] },
  { name: 'construction', match: /^construction/, cap: 3,
    subjects: ['site', 'villas', 'shell', 'rooftop', 'street', 'construction'] }
];
const FALLBACK_GROUP = { name: 'other', cap: 3, subjects: [] };

// Floorplans are documents, not scenes. A slow pan across "Villa 01, basement"
// says nothing, and before this a floorplan could even land as the closing
// shot. They stay in the gallery, where someone can actually study them.
const NOT_A_SCENE = /^(villa-\d|floorplan|site-plan|masterplan)/;

// Words describing light or angle rather than subject.
const QUALIFIERS = new Set(['day', 'night', 'dusk', 'sunset', 'evening', 'morning',
  'wide', 'panorama', 'side', 'detail', 'overview', 'progress', 'level', 'view', 'room']);

const ATMOSPHERIC = /(night|dusk|sunset|evening)/;

// Below this a sequence stops feeling like a presentation, so a small project
// tops back up with whatever the caps left behind, in its own order.
const MINIMUM_SCENES = 8;

function stemOf(item) {
  return String(item?.src || '').split('/').pop().replace(/\.[^.]+$/, '');
}

function groupOf(stem) {
  return GROUPS.find((group) => group.match.test(stem)) || FALLBACK_GROUP;
}

function subjectOf(stem, group) {
  const tokens = stem.split('-').filter((token) => !QUALIFIERS.has(token));
  const found = group.subjects.find((subject) => tokens.some((token) => token.startsWith(subject)));
  return found || tokens.join('-') || stem;
}

export function curateViewingScenes(items) {
  const eligible = items
    .map((item, index) => index)
    .filter((index) => !NOT_A_SCENE.test(stemOf(items[index])));
  if (!eligible.length) return items.map((_, index) => index);

  // First frame of each subject wins: media order is already curated, so the
  // opening shot of a subject is the one chosen to lead it.
  const groups = new Map();
  for (const index of eligible) {
    const stem = stemOf(items[index]);
    const group = groupOf(stem);
    if (!groups.has(group.name)) groups.set(group.name, { cap: group.cap, firsts: new Map() });
    const { firsts } = groups.get(group.name);
    const subject = subjectOf(stem, group);
    if (!firsts.has(subject)) firsts.set(subject, index);
  }

  const kept = new Set();
  for (const { cap, firsts } of groups.values()) {
    for (const index of [...firsts.values()].slice(0, cap)) kept.add(index);
  }

  for (const index of eligible) {
    if (kept.size >= MINIMUM_SCENES) break;
    kept.add(index);
  }

  const order = [...kept].sort((a, b) => a - b);

  // The player treats the last scene as the close, so it should not be a
  // construction photo when the project has a shot taken at dusk or after dark
  // to end on.
  const closer = order.find((index) => {
    const stem = stemOf(items[index]);
    return ATMOSPHERIC.test(stem) && groupOf(stem).name === 'exterior';
  });
  if (closer !== undefined && order[order.length - 1] !== closer) {
    return [...order.filter((index) => index !== closer), closer];
  }
  return order;
}
