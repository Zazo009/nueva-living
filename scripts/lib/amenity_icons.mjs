// The nineteen icons a project page can draw beside an amenity.
//
// Inline SVG rather than a sprite or an icon font: they are drawn once per
// card, there are at most twenty cards on a page, and the system stylesheet is
// already inlined -- a separate request for nineteen small paths would cost
// more than the markup does.
//
// All of them are 24x24, 1.25 stroke, round caps, no fill, so they sit on the
// same optical weight as the hairline box they are drawn in. currentColor
// means the card controls the colour and hover needs no second rule.
const P = (d) => `<path d="${d}"/>`;

const PATHS = {
  waves: P('M2 6c2 0 2 2 4 2s2-2 4-2 2 2 4 2 2-2 4-2 2 2 4 2') + P('M2 12c2 0 2 2 4 2s2-2 4-2 2 2 4 2 2-2 4-2 2 2 4 2') + P('M2 18c2 0 2 2 4 2s2-2 4-2 2 2 4 2 2-2 4-2 2 2 4 2'),
  flame: P('M12 2c1.5 3 4.5 4.5 4.5 8.5a4.5 4.5 0 0 1-9 0C7.5 8 9 6.5 9 4.5c1 .5 2.2 1.5 3 2.5 0-2 0-3.5 0-5Z') + P('M12 22a7 7 0 0 0 7-7'),
  dumbbell: P('M4 9v6') + P('M20 9v6') + P('M7 7v10') + P('M17 7v10') + P('M7 12h10'),
  tree: P('M12 21v-6') + P('M12 15c-3.3 0-6-2.2-6-5 0-1.8 1.1-3.4 2.7-4.2C9.1 3.7 10.4 3 12 3s2.9.7 3.3 2.8C16.9 6.6 18 8.2 18 10c0 2.8-2.7 5-6 5Z'),
  smile: P('M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18Z') + P('M8.5 14a4.5 4.5 0 0 0 7 0') + P('M9 9.5h.01') + P('M15 9.5h.01'),
  sun: P('M12 6a6 6 0 1 0 0 12 6 6 0 0 0 0-12Z') + P('M12 2v2') + P('M12 20v2') + P('M2 12h2') + P('M20 12h2') + P('M4.9 4.9l1.4 1.4') + P('M17.7 17.7l1.4 1.4') + P('M19.1 4.9l-1.4 1.4') + P('M6.3 17.7l-1.4 1.4'),
  mountain: P('M3 19h18L14 7l-3.5 6L8 10l-5 9Z'),
  laptop: P('M4 6h16v10H4z') + P('M2 19h20'),
  car: P('M5 15h14') + P('M6.5 15l1.2-4.6A2 2 0 0 1 9.6 9h4.8a2 2 0 0 1 1.9 1.4L17.5 15') + P('M4 15v3h3v-3') + P('M17 15v3h3v-3') + P('M4 15h16'),
  box: P('M4 8h16v11H4z') + P('M4 8l1.5-3h13L20 8') + P('M10 12h4'),
  arrows: P('M12 3v18') + P('M8 7l4-4 4 4') + P('M8 17l4 4 4-4'),
  utensils: P('M6 3v8a2 2 0 0 0 4 0V3') + P('M8 11v10') + P('M16 3c-1.5 1.5-2 3-2 5s.5 2.5 2 2.5V21'),
  thermometer: P('M14 14V5a2 2 0 1 0-4 0v9a4 4 0 1 0 4 0Z') + P('M12 17.5v.01'),
  cpu: P('M7 7h10v10H7z') + P('M10 4v3') + P('M14 4v3') + P('M10 17v3') + P('M14 17v3') + P('M4 10h3') + P('M4 14h3') + P('M17 10h3') + P('M17 14h3'),
  shield: P('M12 3l7 3v5c0 4.4-2.9 8.3-7 10-4.1-1.7-7-5.6-7-10V6l7-3Z') + P('M9.5 12l1.8 1.8L15 10'),
  sparkles: P('M12 3l1.8 4.7L18.5 9.5 13.8 11.3 12 16l-1.8-4.7L5.5 9.5l4.7-1.8L12 3Z') + P('M18 16l.7 1.8L20.5 18.5l-1.8.7L18 21l-.7-1.8L15.5 18.5l1.8-.7L18 16Z'),
  bellconcierge: P('M4 18h16') + P('M6 18a6 6 0 0 1 12 0') + P('M12 8V6') + P('M10.5 6h3'),
  droplet: P('M12 3s6 6.3 6 10a6 6 0 0 1-12 0c0-3.7 6-10 6-10Z'),
  wifi: P('M2.5 9a15 15 0 0 1 19 0') + P('M6 12.5a10 10 0 0 1 12 0') + P('M9.5 16a5 5 0 0 1 5 0') + P('M12 19.5h.01'),
  bike: P('M6.5 19a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7Z') + P('M17.5 19a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7Z') + P('M6.5 15.5L10 8h5') + P('M10 8l4 7.5') + P('M14 5h3'),
  accessibility: P('M12 6a2 2 0 1 0 0-4 2 2 0 0 0 0 4Z') + P('M12 8v5') + P('M8 10h8') + P('M10 13l-2 8') + P('M14 13l2 8'),
};

export const AMENITY_ICON_KEYS = Object.freeze(Object.keys(PATHS));

export function amenityIcon(key) {
  const paths = PATHS[key] || PATHS.sparkles;
  return `<svg class="amenity-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">${paths}</svg>`;
}
