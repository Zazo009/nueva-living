import { readFileSync, writeFileSync } from 'node:fs';

const file = 'Liora_Living_SOLENNE_POLISHED.html';
const html = readFileSync(file, 'utf8');

const copy = [
  {
    label: '01 — Coastal Setting',
    hl: 'Above Benahavís,<br>the coast unfolds.',
    sub: 'The opening aerial places Solenne on the hillside, with the Mediterranean, evening sky and illuminated residences setting the tone.',
    txt: 'exterior',
  },
  {
    label: '02 — Hillside Residences',
    hl: 'Terraced homes<br>set into the slope.',
    sub: 'Layered architecture, landscaped edges and the pool terrace show how the development steps naturally into the Benahavís hillside.',
    txt: 'exterior',
  },
  {
    label: '03 — Villa Facade',
    hl: 'Clean lines,<br>warm timber detail.',
    sub: 'A close view of the residence facade highlights white volumes, vertical timber screens, integrated lighting and planted arrival.',
    txt: 'exterior',
  },
  {
    label: '04 — Golf Simulator',
    hl: 'A private golf room,<br>ready year-round.',
    sub: 'The simulator brings the Costa del Sol golf lifestyle indoors, with practice turf, launch data and a warm timber-framed setting.',
    txt: 'amenity',
  },
  {
    label: '05 — Arrival at Solenne',
    hl: 'An illuminated<br>hillside entrance.',
    sub: 'The approach is framed by palms, planted walls and subtle architectural lighting, with the Solenne marker set against the valley view.',
    txt: 'exterior',
  },
  {
    label: '06 — Rooftop Terraces',
    hl: 'Private roof decks<br>towards the sea.',
    sub: 'Rooftop pools, pergolas and lounge areas open across the valley, giving each home its own elevated outdoor room.',
    txt: 'terrace',
  },
  {
    label: '07 — Sunset Pool',
    hl: 'Water, sunset<br>and quiet horizon.',
    sub: 'The private pool terrace is staged for evening light, with loungers at the edge of the view and the coastline beyond.',
    txt: 'terrace',
  },
  {
    label: '08 — Sky Terrace Living',
    hl: 'Dining, lounging<br>and pool in one place.',
    sub: 'The roof terrace combines pool, sofa lounge and open-air dining, arranged around a clear Mediterranean outlook.',
    txt: 'terrace',
  },
  {
    label: '09 — Covered Outdoor Lounge',
    hl: 'Shade with<br>the sea beyond.',
    sub: 'A pergola roof, soft seating and dining area create an outdoor room protected from sun while keeping the view open.',
    txt: 'terrace',
  },
  {
    label: '10 — Garden Terrace',
    hl: 'A calmer level<br>beside the water.',
    sub: 'The terrace shifts to a private garden and pool edge, with sheltered seating and planting softening the architecture.',
    txt: 'terrace',
  },
  {
    label: '11 — Indoor–Outdoor Flow',
    hl: 'Living space<br>opens to the view.',
    sub: 'Sliding glass connects the lounge directly to the terrace and pool garden, making the outdoor space part of the everyday room.',
    txt: 'interior',
  },
  {
    label: '12 — View Lounge',
    hl: 'An open room<br>under the pergola.',
    sub: 'Seating and dining sit under patterned shade, facing the coastline with low glass balustrades kept visually quiet.',
    txt: 'terrace',
  },
  {
    label: '13 — Main Living Space',
    hl: 'Soft minimalism<br>through the living core.',
    sub: 'The kitchen, dining and lounge share a warm neutral palette, marble island and integrated joinery for calm daily living.',
    txt: 'interior',
  },
  {
    label: '14 — Principal Suite',
    hl: 'Bedroom calm<br>with a dressing area.',
    sub: 'The suite pairs soft textiles, warm lighting and a glass-fronted wardrobe, with daylight arriving from the private terrace.',
    txt: 'interior',
  },
  {
    label: '15 — Kitchen & Lounge',
    hl: 'A social core<br>with architectural warmth.',
    sub: 'Marble, timber, shelving and the linear fireplace give the open-plan interior both function and atmosphere.',
    txt: 'interior',
  },
  {
    label: '16 — Entertainment Level',
    hl: 'A second living world<br>below the home.',
    sub: 'The lower floor brings together lounge seating, billiards, wine display and a sculptural stair for relaxed entertaining.',
    txt: 'interior',
  },
  {
    label: '17 — Wellness Pool',
    hl: 'A private spa<br>within the residence.',
    sub: 'The indoor pool, loungers, treatment rooms and soft green palette create a dedicated wellness zone within the home.',
    txt: 'amenity',
  },
  {
    label: '18 — Bathroom Detail',
    hl: 'Green ceramic texture,<br>warm light.',
    sub: 'The bathroom combines herringbone green tile, pale timber and indirect lighting for a spa-like private detail.',
    txt: 'interior',
  },
  {
    label: '19 — Pool Horizon',
    hl: 'Water meets<br>the evening skyline.',
    sub: 'The pool stretches toward the coastal horizon, carrying the same quiet sunset mood from the architecture to the shared amenity.',
    txt: 'terrace',
  },
  {
    label: '20 — Fitness Studio',
    hl: 'Private fitness,<br>full material next.',
    sub: 'The preview closes in the training studio: a final look at the amenity layer before requesting brochure, plans, availability and pricing.',
    txt: 'closing',
  },
];

function jsString(value) {
  return `"${value
    .replace(/\\/g, '\\\\')
    .replace(/"/g, '\\"')
    .replace(/[^\x20-\x7e]/g, (char) => `\\u${char.charCodeAt(0).toString(16).padStart(4, '0')}`)}"`;
}

function replaceField(block, key, value) {
  const pattern = new RegExp(`\\b${key}:\\s*"((?:\\\\.|[^"\\\\])*)"`);
  if (!pattern.test(block)) throw new Error(`Missing field ${key}.`);
  return block.replace(pattern, `${key}: ${jsString(value)}`);
}

let index = 0;
const updated = html.replace(/\{\s*img:\s*"data:image\/jpeg;base64,[^"]+"[\s\S]*?motion:/g, (block) => {
  const item = copy[index];
  if (!item) return block;
  index += 1;
  let next = block;
  next = replaceField(next, 'label', item.label);
  next = replaceField(next, 'hl', item.hl);
  next = replaceField(next, 'sub', item.sub);
  next = replaceField(next, 'txt', item.txt);
  return next;
});

if (index !== copy.length) {
  throw new Error(`Updated ${index} scenes, expected ${copy.length}.`);
}

writeFileSync(file, updated);
console.log(`Updated ${index} private viewing scenes in ${file}`);
