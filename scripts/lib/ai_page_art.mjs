// Graphics and motion for ai.html (the assistant connector page), and only for that page.
//
// Everything here is drawn for this page: none of it reuses a photograph, render, icon or animation
// from elsewhere on the site (the owner asked for that on 2026-11-18). It carries no English words of
// its own, so the ten locales need nothing new: the three prompts the chat demo types are the same
// HTML strings as the "Try Asking" cards and are translated by the same group G entries, and the
// only words drawn in SVG are product names (Claude, ChatGPT) and the address, which every locale
// prints as is.
//
// Motion is decoration: every graphic is aria-hidden, the page reads the same without it, and
// prefers-reduced-motion freezes it in its finished state (SMIL is paused from script, CSS
// animations are switched off).

// ---------------------------------------------------------------------------------------------
// Hero: the coast at dusk. The lights along the shore stand for developments; two chat bubbles
// hang in the sky and dotted lines carry a spark from them down to the lights.
const shoreLights = [
  [120, 471], [205, 468], [262, 473], [340, 466], [418, 470], [497, 467], [566, 472], [640, 468],
  [722, 471], [801, 466], [866, 470], [948, 468], [1032, 472], [1110, 467], [1262, 470], [1336, 466],
  [1418, 471], [1490, 468],
];
const heroArcs = [
  ['M1272 252 C 1180 320, 1010 380, 948 468', '0s'],
  ['M1300 262 C 1290 340, 1300 420, 1336 466', '1.4s'],
  ['M1236 236 C 1000 250, 760 360, 640 468', '2.6s'],
  ['M1420 318 C 1460 380, 1480 430, 1490 468', '3.7s'],
];

export const AI_HERO_ART = `<div class="ai-hero-art" aria-hidden="true"><svg viewBox="0 0 1600 720" preserveAspectRatio="xMidYMid slice" focusable="false">
  <defs>
    <linearGradient id="aiSky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#16110b"/><stop offset=".45" stop-color="#2f2417"/><stop offset=".64" stop-color="#6a4f2b"/><stop offset=".66" stop-color="#8a6a3a"/>
    </linearGradient>
    <linearGradient id="aiSea" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#3b2c1a"/><stop offset="1" stop-color="#140f09"/>
    </linearGradient>
    <radialGradient id="aiSunGlow"><stop offset="0" stop-color="#f1cf8f" stop-opacity=".55"/><stop offset=".4" stop-color="#c9a35f" stop-opacity=".18"/><stop offset="1" stop-color="#c9a35f" stop-opacity="0"/></radialGradient>
    <radialGradient id="aiLight"><stop offset="0" stop-color="#fff2cf"/><stop offset=".35" stop-color="#f0c879" stop-opacity=".8"/><stop offset="1" stop-color="#c9a35f" stop-opacity="0"/></radialGradient>
  </defs>
  <rect width="1600" height="720" fill="url(#aiSky)"/>
  <g class="ai-stars" fill="#fff6e2">
    <circle cx="180" cy="90" r="1.4"/><circle cx="420" cy="60" r="1"/><circle cx="610" cy="130" r="1.3"/><circle cx="860" cy="70" r="1.1"/><circle cx="1010" cy="150" r=".9"/><circle cx="1150" cy="54" r="1.4"/><circle cx="1500" cy="120" r="1.2"/><circle cx="1380" cy="40" r=".9"/><circle cx="720" cy="210" r=".8"/><circle cx="300" cy="200" r=".9"/>
  </g>
  <circle cx="1180" cy="340" r="300" fill="url(#aiSunGlow)"><animate attributeName="r" values="280;320;280" dur="9s" repeatCount="indefinite"/></circle>
  <circle cx="1180" cy="346" r="50" fill="#f2cc86" opacity=".92"/>
  <path d="M0 470 L0 400 C 90 380 150 352 230 360 C 300 368 340 330 420 318 C 500 306 560 350 640 352 C 720 354 760 300 860 292 C 960 284 1010 340 1090 350 C 1170 360 1230 330 1320 336 C 1410 342 1480 376 1600 372 L1600 470 Z" fill="#2a1f13"/>
  <path d="M0 470 L0 430 C 120 420 200 398 300 404 C 400 410 470 384 560 388 C 660 392 720 416 820 410 C 920 404 1000 380 1100 392 C 1200 404 1300 424 1400 416 C 1480 410 1540 420 1600 418 L1600 470 Z" fill="#1d150c"/>
  <rect y="470" width="1600" height="250" fill="url(#aiSea)"/>
  <g class="ai-sunpath" stroke="#f2cc86" stroke-linecap="round">
    <line x1="1120" y1="490" x2="1240" y2="490" stroke-width="3" opacity=".7"/><line x1="1135" y1="510" x2="1225" y2="510" stroke-width="3" opacity=".55"/><line x1="1100" y1="532" x2="1260" y2="532" stroke-width="2" opacity=".42"/><line x1="1150" y1="556" x2="1210" y2="556" stroke-width="2" opacity=".34"/><line x1="1110" y1="584" x2="1250" y2="584" stroke-width="2" opacity=".24"/><line x1="1160" y1="618" x2="1200" y2="618" stroke-width="2" opacity=".18"/>
  </g>
  <g class="ai-swell" stroke="#c9a35f" stroke-width="1.2" fill="none" opacity=".26">
    <path d="M0 520 C 200 512 400 528 600 520 S 1000 512 1600 522" stroke-dasharray="60 34"><animate attributeName="stroke-dashoffset" from="0" to="-188" dur="7s" repeatCount="indefinite"/></path>
    <path d="M0 600 C 240 590 480 610 720 600 S 1200 590 1600 604" stroke-dasharray="90 50"><animate attributeName="stroke-dashoffset" from="0" to="280" dur="11s" repeatCount="indefinite"/></path>
    <path d="M0 668 C 300 660 600 676 900 668 S 1300 660 1600 670" stroke-dasharray="120 70"><animate attributeName="stroke-dashoffset" from="0" to="-380" dur="14s" repeatCount="indefinite"/></path>
  </g>
  <g class="ai-shore">
    ${shoreLights.map(([x, y], i) => `<g transform="translate(${x} ${y})"><circle r="11" fill="url(#aiLight)" opacity=".5"><animate attributeName="opacity" values=".25;.85;.25" dur="${(3.2 + (i % 5) * 0.7).toFixed(1)}s" begin="${((i * 0.37) % 3).toFixed(2)}s" repeatCount="indefinite"/></circle><circle r="2.2" fill="#fff0c8"/></g>`).join('')}
  </g>
  <g class="ai-arcs" fill="none" stroke="#e9c27f" stroke-width="1.3" stroke-linecap="round" stroke-dasharray="2 7" opacity=".55">
    ${heroArcs.map(([d]) => `<path d="${d}"/>`).join('')}
  </g>
  ${heroArcs.map(([d, begin]) => `<circle r="4" fill="#fff4d6"><animateMotion dur="4.8s" begin="${begin}" repeatCount="indefinite" path="${d}" keyPoints="0;1;1" keyTimes="0;.6;1" calcMode="linear"/><animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;.08;.55;.62;1" dur="4.8s" begin="${begin}" repeatCount="indefinite"/></circle>`).join('')}
  <g class="ai-bubbles">
    <g class="ai-float-a">
      <path d="M1210 170 h170 a22 22 0 0 1 22 22 v48 a22 22 0 0 1 -22 22 h-96 l-22 22 l-4 -22 h-48 a22 22 0 0 1 -22 -22 v-48 a22 22 0 0 1 22 -22 z" fill="rgba(255,250,243,.08)" stroke="#e9c27f" stroke-width="1.4"/>
      <g fill="#f2cc86"><circle cx="1266" cy="216" r="6"><animate attributeName="cy" values="216;206;216;216" keyTimes="0;.2;.4;1" dur="1.6s" repeatCount="indefinite"/></circle><circle cx="1296" cy="216" r="6"><animate attributeName="cy" values="216;216;206;216;216" keyTimes="0;.15;.35;.55;1" dur="1.6s" repeatCount="indefinite"/></circle><circle cx="1326" cy="216" r="6"><animate attributeName="cy" values="216;216;206;216" keyTimes="0;.3;.5;1" dur="1.6s" repeatCount="indefinite"/></circle></g>
    </g>
    <g class="ai-float-b">
      <path d="M1352 270 h150 a18 18 0 0 1 18 18 v34 a18 18 0 0 1 -18 18 h-40 l4 18 l-24 -18 h-90 a18 18 0 0 1 -18 -18 v-34 a18 18 0 0 1 18 -18 z" fill="#c9a35f" opacity=".9"/>
      <g stroke="#2f2417" stroke-width="5" stroke-linecap="round" opacity=".55"><line x1="1362" y1="296" x2="1470" y2="296"/><line x1="1362" y1="316" x2="1430" y2="316"/></g>
    </g>
  </g>
</svg></div>`;

// ---------------------------------------------------------------------------------------------
// Small line icons for the cards, drawn on when the card scrolls in. pathLength=1 lets one CSS
// rule draw any of them.
const icon = (paths) => `<svg class="ai-icon" viewBox="0 0 48 48" aria-hidden="true" focusable="false"><g fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">${paths.replace(/<(path|circle|rect|line|polyline)\b/g, '<$1 pathLength="1"')}</g></svg>`;
export const AI_ICONS = {
  // an open padlock
  free: icon('<rect x="11" y="22" width="26" height="19" rx="3"/><path d="M17 22v-6a8 8 0 0 1 15-4"/><circle cx="24" cy="31" r="2.4"/><line x1="24" y1="33.5" x2="24" y2="36"/>'),
  // two speech bubbles with different scripts' strokes
  languages: icon('<path d="M6 10h22a3 3 0 0 1 3 3v11a3 3 0 0 1-3 3H16l-6 5v-5H6a3 3 0 0 1-3-3V13a3 3 0 0 1 3-3z"/><path d="M34 19h8a3 3 0 0 1 3 3v10a3 3 0 0 1-3 3h-2v5l-6-5h-9a3 3 0 0 1-3-3v-2"/><path d="M10 16h14M14 16c0 5 4 8 8 8M20 16c0 5-4 8-8 8"/>'),
  // a page and its copy, ticked
  figures: icon('<path d="M8 6h16l6 6v24H8z"/><path d="M24 6v6h6"/><line x1="13" y1="19" x2="25" y2="19"/><line x1="13" y1="24" x2="25" y2="24"/><path d="M30 18h6l6 6v18H24v-6"/><polyline points="29 33 32 36 38 29"/>'),
  // a tower crane over a frame
  newBuild: icon('<line x1="14" y1="42" x2="14" y2="8"/><line x1="6" y1="12" x2="42" y2="12"/><line x1="14" y1="8" x2="30" y2="12"/><line x1="36" y1="12" x2="36" y2="20"/><rect x="32" y="20" width="8" height="5"/><path d="M22 42V28h20v14"/><line x1="22" y1="35" x2="42" y2="35"/><line x1="32" y1="28" x2="32" y2="42"/>'),
  // six tiles
  six: icon('<rect x="5" y="9" width="10" height="12" rx="1.5"/><rect x="19" y="9" width="10" height="12" rx="1.5"/><rect x="33" y="9" width="10" height="12" rx="1.5"/><rect x="5" y="27" width="10" height="12" rx="1.5"/><rect x="19" y="27" width="10" height="12" rx="1.5"/><rect x="33" y="27" width="10" height="12" rx="1.5"/>'),
  // a lens over a floor plan
  oneInFull: icon('<path d="M5 8h26v26H5z"/><path d="M5 20h10v14M15 8v6M22 20h9"/><circle cx="32" cy="32" r="8"/><line x1="38" y1="38" x2="44" y2="44"/>'),
};

// ---------------------------------------------------------------------------------------------
// The chat demo: a message types itself, the reply arrives as three illustrated result tiles and
// a small map of the coast whose pins fall where that prompt points (west, centre, east).
const tileArt = [
  // a villa with a pool
  `<svg viewBox="0 0 160 100" preserveAspectRatio="xMidYMid slice" focusable="false"><rect width="160" height="100" fill="var(--sky)"/><circle cx="124" cy="30" r="13" fill="var(--sun)"/><path d="M0 64 C40 54 80 60 160 52 V100 H0z" fill="var(--hill)"/><rect x="34" y="44" width="62" height="24" fill="#fbf4e6"/><rect x="58" y="34" width="44" height="12" fill="#f3e7d0"/><rect x="40" y="50" width="16" height="12" fill="var(--glass)"/><rect x="62" y="50" width="28" height="12" fill="var(--glass)"/><rect x="18" y="70" width="104" height="12" rx="2" fill="var(--pool)"/><path d="M26 76h18M56 76h22M90 76h16" stroke="#fff" stroke-opacity=".6" stroke-width="1.4"/><rect x="0" y="82" width="160" height="18" fill="var(--ground)"/><path d="M134 82v-26M134 58c-8-2-12 2-14 6M134 58c8-2 12 2 14 6M134 56c-2-6 2-10 6-10" stroke="var(--palm)" stroke-width="2" fill="none" stroke-linecap="round"/></svg>`,
  // terraced apartments over the sea
  `<svg viewBox="0 0 160 100" preserveAspectRatio="xMidYMid slice" focusable="false"><rect width="160" height="100" fill="var(--sky)"/><circle cx="34" cy="26" r="10" fill="var(--sun)"/><rect y="70" width="160" height="30" fill="var(--pool)"/><path d="M0 76h160" stroke="#fff" stroke-opacity=".35"/><path d="M60 72V40h76v32z" fill="#fbf4e6"/><path d="M70 40V28h60v12z" fill="#f3e7d0"/><g fill="var(--glass)"><rect x="66" y="46" width="14" height="8"/><rect x="86" y="46" width="14" height="8"/><rect x="106" y="46" width="14" height="8"/><rect x="66" y="58" width="14" height="8"/><rect x="86" y="58" width="14" height="8"/><rect x="106" y="58" width="14" height="8"/><rect x="78" y="31" width="14" height="6"/><rect x="100" y="31" width="14" height="6"/></g><path d="M60 55h76M60 67h76" stroke="var(--hill)" stroke-width="1.5"/><path d="M0 72 C20 64 40 66 56 72z" fill="var(--hill)"/></svg>`,
  // a frame going up, with a crane
  `<svg viewBox="0 0 160 100" preserveAspectRatio="xMidYMid slice" focusable="false"><rect width="160" height="100" fill="var(--sky)"/><circle cx="130" cy="24" r="9" fill="var(--sun)"/><path d="M0 70 C50 60 100 66 160 58V100H0z" fill="var(--hill)"/><rect y="84" width="160" height="16" fill="var(--ground)"/><g stroke="#fbf4e6" stroke-width="3" fill="none"><path d="M44 84V48h60v36M44 60h60M44 72h60M64 48v36M84 48v36"/></g><g stroke="var(--sun)" stroke-width="2" fill="none"><path d="M118 84V16M100 20h52M118 16l-18 4M140 20v14"/><rect x="136" y="34" width="8" height="6"/></g></svg>`,
];
const mapPins = [
  // x, y, cluster: w = west (Estepona), m = middle (Marbella, Nueva Andalucía), e = east (Mijas)
  [62, 66, 'w'], [88, 58, 'w'], [112, 63, 'w'], [168, 52, 'm'], [196, 46, 'm'], [222, 50, 'm'],
  [296, 38, 'e'], [322, 30, 'e'], [348, 34, 'e'],
];

export function aiChatDemo(prompts) {
  return `<div class="ai-demo ai-rise" aria-hidden="true">
      <ul class="ai-prompts" hidden>${prompts.map((p) => `<li>${p}</li>`).join('')}</ul>
      <div class="ai-chat" data-ai-chat data-focus="w">
        <div class="ai-chat-bar"><i></i><i></i><i></i></div>
        <div class="ai-chat-body">
          <div class="ai-msg ai-msg-user"><span class="ai-typed"></span><span class="ai-caret"></span></div>
          <div class="ai-msg ai-msg-bot">
            <div class="ai-dots"><i></i><i></i><i></i></div>
            <div class="ai-results">${tileArt.map((art, i) => `<div class="ai-tile" style="--i:${i}"><div class="ai-tile-art">${art}</div><b></b><b></b><b class="ai-tile-price"></b></div>`).join('')}</div>
            <div class="ai-map"><svg viewBox="0 0 400 110" focusable="false"><path class="ai-map-land" d="M0 0H400V22C370 24 340 28 300 36C260 44 240 40 200 44C160 48 120 58 80 62C50 66 24 70 0 74Z"/><path class="ai-map-coast" d="M0 74C24 70 50 66 80 62C120 58 160 48 200 44C240 40 260 44 300 36C340 28 370 24 400 22"/>${mapPins.map(([x, y, c], i) => `<g class="ai-pin" data-c="${c}" style="--i:${i}" transform="translate(${x} ${y})"><g class="ai-pin-drop"><path d="M0 0C-6-8-8-11-8-15A8 8 0 0 1 8-15C8-11 6-8 0 0Z"/><circle cy="-15" r="3"/></g></g>`).join('')}</svg></div>
          </div>
        </div>
        <div class="ai-composer"><span></span><svg viewBox="0 0 24 24" focusable="false"><path d="M4 12h14M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
      </div>
    </div>`;
}

// ---------------------------------------------------------------------------------------------
// The address, drawn: assistants on one side, the address in the middle, the project pages on the
// other. Gold sparks carry a question in, pale ones carry the answer back. Two layouts: across
// for wide screens, down for phones.
const pageGrid = (x0, y0, step, cols, rows) => {
  let out = '';
  let n = 0;
  for (let r = 0; r < rows; r += 1) for (let c = 0; c < cols; c += 1) {
    const x = x0 + c * step; const y = y0 + r * step;
    out += `<g class="ai-page-tile" style="--i:${n}" transform="translate(${x} ${y})"><rect width="40" height="40" rx="5"/><path d="M10 26l10-9 10 9M14 23v9h12v-9"/></g>`;
    n += 1;
  }
  return out;
};
const spark = (d, begin, cls) => `<circle class="${cls}" r="4.5"><animateMotion dur="3.6s" begin="${begin}" repeatCount="indefinite" path="${d}" keyPoints="0;1;1" keyTimes="0;.55;1" calcMode="linear"/><animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;.06;.5;.56;1" dur="3.6s" begin="${begin}" repeatCount="indefinite"/></circle>`;
const node = (x, y, w, label) => `<g class="ai-node" transform="translate(${x} ${y})"><rect x="${-w / 2}" y="-24" width="${w}" height="48" rx="24"/>${label}</g>`;
const plusLabel = '<path class="ai-node-plus" d="M-8 0h16M0-8v16"/>';

const wideIn = ['M190 70 C 260 70 270 150 340 150', 'M190 150 L 340 150', 'M190 230 C 260 230 270 150 340 150'];
const wideOut = 'M620 150 C 660 150 680 150 700 150';
const tallIn = ['M70 92 C 70 140 180 140 180 190', 'M180 92 L 180 190', 'M290 92 C 290 140 180 140 180 190'];
const tallOut = 'M180 250 L 180 318';

export const AI_FLOW_ART = `<div class="ai-flow ai-rise" aria-hidden="true" dir="ltr">
      <svg class="ai-flow-wide" viewBox="0 0 960 300" focusable="false">
        <g class="ai-flow-lines">${wideIn.map((d) => `<path d="${d}"/>`).join('')}<path d="${wideOut}"/></g>
        ${wideIn.map((d, i) => spark(d, `${i * 1.2}s`, 'ai-spark-in')).join('')}
        ${spark('M700 150 C 680 150 660 150 620 150', '0.6s', 'ai-spark-out')}
        ${node(115, 70, 150, '<text x="0" y="6">Claude</text>')}
        ${node(115, 150, 150, '<text x="0" y="6">ChatGPT</text>')}
        ${node(115, 230, 150, plusLabel)}
        <g class="ai-hub" transform="translate(480 150)"><circle class="ai-hub-ring" r="128"/><rect x="-140" y="-32" width="280" height="64" rx="32"/><text x="0" y="7">nuevaliving.com/mcp</text></g>
        <g class="ai-grid">${pageGrid(712, 64, 60, 4, 3)}</g>
      </svg>
      <svg class="ai-flow-tall" viewBox="0 0 360 520" focusable="false">
        <g class="ai-flow-lines">${tallIn.map((d) => `<path d="${d}"/>`).join('')}<path d="${tallOut}"/></g>
        ${tallIn.map((d, i) => spark(d, `${i * 1.2}s`, 'ai-spark-in')).join('')}
        ${spark('M180 318 L 180 250', '0.6s', 'ai-spark-out')}
        ${node(70, 68, 108, '<text x="0" y="6">Claude</text>')}
        ${node(180, 68, 108, '<text x="0" y="6">ChatGPT</text>')}
        ${node(290, 68, 108, plusLabel)}
        <g class="ai-hub" transform="translate(180 220)"><rect x="-140" y="-30" width="280" height="60" rx="30"/><text x="0" y="7">nuevaliving.com/mcp</text></g>
        <g class="ai-grid">${pageGrid(70, 330, 60, 4, 3)}</g>
      </svg>
    </div>`;

// ---------------------------------------------------------------------------------------------
// Your details: what a search carries through the gate (a place, a budget, a type of home) and
// what stays on your side of it (you, and the rest of the conversation).
export const AI_PRIVACY_ART = `<div class="ai-privacy ai-rise" aria-hidden="true">
      <svg viewBox="0 0 440 320" focusable="false">
        <g class="ai-priv-convo">
          <rect x="18" y="56" width="168" height="208" rx="18"/>
          <circle class="ai-priv-person" cx="58" cy="100" r="18"/><path class="ai-priv-person" d="M34 140c4-14 14-20 24-20s20 6 24 20"/>
          <g class="ai-priv-lines"><line x1="96" y1="94" x2="164" y2="94"/><line x1="96" y1="110" x2="150" y2="110"/><line x1="40" y1="170" x2="164" y2="170"/><line x1="40" y1="188" x2="142" y2="188"/><line x1="40" y1="206" x2="160" y2="206"/><line x1="40" y1="224" x2="120" y2="224"/></g>
        </g>
        <g class="ai-priv-gate"><line x1="236" y1="40" x2="236" y2="280"/><line x1="252" y1="40" x2="252" y2="280"/><g transform="translate(244 30)"><rect x="-13" y="-6" width="26" height="20" rx="4"/><path d="M-7-6v-6a7 7 0 0 1 14 0v6" fill="none"/></g></g>
        <g class="ai-priv-dest"><rect x="352" y="104" width="70" height="26" rx="6"/><rect x="352" y="138" width="70" height="26" rx="6"/><rect x="352" y="172" width="70" height="26" rx="6"/><circle cx="368" cy="117" r="3"/><circle cx="368" cy="151" r="3"/><circle cx="368" cy="185" r="3"/></g>
        <g class="ai-chip ai-chip-1"><circle r="17"/><path d="M0 7C-4 2-6-1-6-4A6 6 0 0 1 6-4C6-1 4 2 0 7Z"/><circle cy="-4" r="2"/></g>
        <g class="ai-chip ai-chip-2"><circle r="17"/><path d="M5-6a7 7 0 1 0 0 12M-8-2h9M-8 2h9"/></g>
        <g class="ai-chip ai-chip-3"><circle r="17"/><path d="M-7 1l7-7 7 7M-5-1v8h10v-8"/></g>
      </svg>
    </div>`;

// ---------------------------------------------------------------------------------------------
export const AI_PAGE_STYLE = `<style>
  .ai-page .page-hero { min-height: clamp(420px, 58svh, 600px); }
  .ai-page .page-hero .ai-hero-art { position: absolute; inset: 0; z-index: -2; }
  .ai-page .page-hero .ai-hero-art svg { width: 100%; height: 100%; display: block; }
  .ai-page .page-hero::after { background: linear-gradient(90deg, rgba(22,17,11,.86), rgba(22,17,11,.5) 46%, rgba(22,17,11,0) 74%), linear-gradient(0deg, rgba(22,17,11,.7), rgba(22,17,11,0) 46%); }
  html[lang^="ar"] .ai-page .page-hero .ai-hero-art svg { transform: scaleX(-1); }
  html[lang^="ar"] .ai-page .page-hero::after { background: linear-gradient(270deg, rgba(22,17,11,.86), rgba(22,17,11,.5) 46%, rgba(22,17,11,0) 74%), linear-gradient(0deg, rgba(22,17,11,.7), rgba(22,17,11,0) 46%); }
  .ai-float-a { animation: aiFloat 7s ease-in-out infinite; }
  .ai-float-b { animation: aiFloat 8s ease-in-out -3s infinite; }
  @keyframes aiFloat { 50% { transform: translateY(-12px); } }
  .ai-stars circle { animation: aiTwinkle 5s ease-in-out infinite; }
  .ai-stars circle:nth-child(3n) { animation-delay: -2s; } .ai-stars circle:nth-child(3n+1) { animation-delay: -3.6s; }
  @keyframes aiTwinkle { 50% { opacity: .25; } }
  .ai-sunpath line { animation: aiShimmer 3.4s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }
  .ai-sunpath line:nth-child(even) { animation-delay: -1.7s; }
  @keyframes aiShimmer { 50% { transform: scaleX(.6); opacity: .15; } }
  @media (max-width: 760px) { .ai-page .page-hero::after { background: linear-gradient(0deg, rgba(22,17,11,.9), rgba(22,17,11,.35) 70%, rgba(22,17,11,.1)); } }

  /* Scroll-in: script marks only what starts below the first screen (ai-wait), so the page reads
     fully without script and in a renderer that never scrolls. */
  .ai-rise { transition: opacity .9s ease, transform .9s cubic-bezier(.2,.7,.2,1); transition-delay: var(--d, 0s); }
  .ai-rise.ai-wait:not(.is-in) { opacity: 0; transform: translateY(26px); }

  .ai-icon { width: 46px; height: 46px; color: var(--bronze); margin-bottom: 18px; display: block; }
  .ai-icon [pathLength] { stroke-dasharray: 1; stroke-dashoffset: 0; }
  .ai-rise .ai-icon [pathLength] { transition: stroke-dashoffset 1.6s cubic-bezier(.6,0,.2,1) calc(var(--d, 0s) + .3s); }
  .ai-rise.ai-wait:not(.is-in) .ai-icon [pathLength] { stroke-dashoffset: 1; }
  .ai-page .card { transition: transform .4s ease, box-shadow .4s ease, opacity .9s ease; }
  .ai-page .card:hover { transform: translateY(-4px); box-shadow: 0 26px 70px rgba(41,36,27,.12); }
  .ai-page .card.ai-wait:not(.is-in) { transform: translateY(26px); }

  /* Steps: the number sits in a ring that closes as the card arrives. */
  @property --ai-ring { syntax: '<percentage>'; inherits: false; initial-value: 100%; }
  .ai-page #claude .card-number, .ai-page #chatgpt .card-number { --ai-ring: 100%; width: 58px; height: 58px; display: grid; place-items: center; border-radius: 50%; font-size: 24px; position: relative; }
  .ai-page #claude .card-number::before, .ai-page #chatgpt .card-number::before { content: ""; position: absolute; inset: 0; border-radius: 50%; padding: 1.5px; background: conic-gradient(var(--bronze-light) var(--ai-ring), var(--line) 0); -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0); -webkit-mask-composite: xor; mask-composite: exclude; transition: --ai-ring 1.4s cubic-bezier(.6,0,.2,1) calc(var(--d, 0s) + .25s); }
  .ai-wait:not(.is-in) .card-number::before { --ai-ring: 0%; }
  .ai-page #chatgpt .card-number { color: var(--bronze-light); }

  /* Chat demo */
  .ai-demo { margin: clamp(30px, 4vw, 52px) auto clamp(30px, 4vw, 48px); max-width: 780px; }
  .ai-chat { background: #fffdf8; border: 1px solid var(--line); border-radius: 22px; box-shadow: 0 40px 100px rgba(47,36,23,.16), 0 6px 18px rgba(47,36,23,.06); overflow: hidden; }
  .ai-chat-bar { display: flex; gap: 7px; padding: 14px 18px; border-bottom: 1px solid var(--line); background: var(--cream); }
  .ai-chat-bar i { width: 10px; height: 10px; border-radius: 50%; background: var(--sand); }
  .ai-chat-body { padding: clamp(18px, 3vw, 30px); display: grid; gap: 18px; min-height: 430px; align-content: start; }
  .ai-msg-user { justify-self: end; max-width: 86%; background: var(--deep); color: var(--ivory); padding: 14px 18px; border-radius: 18px 18px 4px 18px; font-size: 14px; line-height: 1.55; min-height: 50px; transition: opacity .5s ease; }
  html[lang^="ar"] .ai-msg-user { border-radius: 18px 18px 18px 4px; }
  .ai-caret { display: inline-block; width: 2px; height: 1.1em; background: var(--bronze-light); vertical-align: -0.18em; margin-inline-start: 2px; animation: aiCaret 1s steps(1) infinite; }
  @keyframes aiCaret { 50% { opacity: 0; } }
  .ai-chat:not(.is-typing) .ai-caret { display: none; }
  .ai-msg-bot { display: grid; gap: 14px; }
  .ai-dots { display: flex; gap: 6px; padding: 12px 16px; background: var(--cream); border-radius: 16px; width: max-content; opacity: 0; transition: opacity .3s; }
  .ai-dots i { width: 7px; height: 7px; border-radius: 50%; background: var(--bronze); animation: aiDot 1.2s ease-in-out infinite; }
  .ai-dots i:nth-child(2) { animation-delay: .15s; } .ai-dots i:nth-child(3) { animation-delay: .3s; }
  @keyframes aiDot { 30% { transform: translateY(-5px); opacity: .5; } }
  .ai-chat.is-thinking .ai-dots { opacity: 1; }
  .ai-chat.is-results .ai-dots { display: none; }
  .ai-results { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; }
  .ai-tile { background: #fff; border: 1px solid var(--line); border-radius: 12px; overflow: hidden; display: grid; gap: 7px; padding-bottom: 12px; opacity: 0; transform: translateY(16px) scale(.97); transition: opacity .6s ease, transform .6s cubic-bezier(.2,.7,.2,1); transition-delay: calc(var(--i) * .16s); }
  .ai-tile-art { aspect-ratio: 16 / 10; overflow: hidden; }
  .ai-tile-art svg { width: 100%; height: 100%; display: block; transform: scale(1.12); transition: transform 5s ease-out; }
  .ai-tile b { height: 7px; border-radius: 4px; background: var(--sand); margin-inline: 12px; width: 70%; }
  .ai-tile b + b { width: 46%; }
  .ai-tile .ai-tile-price { width: 34%; background: var(--bronze-light); height: 9px; }
  .ai-chat.is-results .ai-tile { opacity: 1; transform: none; }
  .ai-chat.is-results .ai-tile-art svg { transform: scale(1); }
  .ai-map { border-radius: 12px; overflow: hidden; background: #e7eef0; border: 1px solid var(--line); opacity: 0; transition: opacity .6s ease .5s; }
  .ai-map svg { display: block; width: 100%; height: auto; }
  .ai-map-land { fill: #efe6d3; } .ai-map-coast { fill: none; stroke: #c9b48b; stroke-width: 1.5; }
  .ai-chat.is-results .ai-map { opacity: 1; }
  .ai-pin path { fill: var(--sand); } .ai-pin circle { fill: #fff; }
  .ai-pin .ai-pin-drop { transform: translateY(-40px); opacity: 0; transition: transform .55s cubic-bezier(.3,1.6,.5,1), opacity .3s; transition-delay: calc(.8s + var(--i) * .07s); }
  .ai-chat.is-results .ai-pin-drop { transform: none; opacity: 1; }
  .ai-chat[data-focus="w"] .ai-pin[data-c="w"] path, .ai-chat[data-focus="m"] .ai-pin[data-c="m"] path, .ai-chat[data-focus="e"] .ai-pin[data-c="e"] path { fill: var(--bronze); }
  .ai-chat[data-focus="w"] .ai-tile, .ai-chat[data-focus="w"] .ai-tile-art { --sky: #f6dfb5; --sun: #f0b65e; --hill: #b9a37a; --glass: #8fb3bf; --pool: #5fa8bb; --ground: #d8c8a6; --palm: #6f7f4f; }
  .ai-chat[data-focus="e"] .ai-tile-art { --sky: #cfe2e9; --sun: #fbe3a8; --hill: #a9b38f; --glass: #7fa6b5; --pool: #4f9db5; --ground: #d5ccb2; --palm: #5f7350; }
  .ai-chat[data-focus="m"] .ai-tile-art { --sky: #e9c9b0; --sun: #e79a62; --hill: #9e8a68; --glass: #8aa1ab; --pool: #5a93a6; --ground: #cdbb98; --palm: #66704a; }
  .ai-chat.is-fading .ai-msg-user, .ai-chat.is-fading .ai-msg-bot { opacity: 0; transition: opacity .5s ease; }
  .ai-composer { display: flex; align-items: center; gap: 12px; margin: 0 clamp(18px, 3vw, 30px) clamp(18px, 3vw, 26px); padding: 10px 10px 10px 18px; border: 1px solid var(--line); border-radius: 999px; }
  .ai-composer span { flex: 1; height: 8px; border-radius: 4px; background: var(--cream); }
  .ai-composer svg { width: 34px; height: 34px; padding: 8px; border-radius: 50%; background: var(--deep); color: var(--bronze-light); }
  html[lang^="ar"] .ai-composer svg { transform: scaleX(-1); }
  .ai-chat.is-sent .ai-composer svg { animation: aiSend .5s ease; }
  @keyframes aiSend { 50% { transform: scale(.82); } }
  @media (max-width: 640px) { .ai-results { grid-template-columns: repeat(2, minmax(0, 1fr)); } .ai-results .ai-tile:nth-child(3) { display: none; } .ai-chat-body { min-height: 400px; } }

  /* Address flow */
  .ai-flow { margin: clamp(30px, 4vw, 48px) auto 0; max-width: 960px; }
  .ai-flow svg { width: 100%; height: auto; display: block; overflow: visible; }
  .ai-flow-tall { display: none !important; max-width: 400px; margin: 0 auto; }
  @media (max-width: 700px) { .ai-flow-wide { display: none !important; } .ai-flow-tall { display: block !important; } }
  .ai-flow-lines path { fill: none; stroke: rgba(201,163,95,.42); stroke-width: 1.4; stroke-dasharray: 3 7; animation: aiDash 1.6s linear infinite; }
  @keyframes aiDash { to { stroke-dashoffset: -20; } }
  .ai-node rect { fill: rgba(255,250,243,.05); stroke: rgba(201,163,95,.55); }
  .ai-node text, .ai-hub text { fill: var(--ivory); font: 500 17px "Montserrat", Arial, sans-serif; letter-spacing: .04em; text-anchor: middle; }
  .ai-node-plus { stroke: var(--bronze-light); stroke-width: 2; stroke-linecap: round; }
  .ai-hub rect { fill: var(--bronze-light); } .ai-hub text { fill: var(--deep); font-weight: 600; font-size: 18px; }
  .ai-hub-ring { fill: none; stroke: rgba(201,163,95,.25); stroke-dasharray: 2 10; animation: aiSpin 40s linear infinite; transform-origin: 0 0; }
  @keyframes aiSpin { to { transform: rotate(360deg); } }
  .ai-spark-in { fill: #f2cc86; } .ai-spark-out { fill: #fffaf3; }
  .ai-page-tile rect { fill: rgba(255,250,243,.04); stroke: rgba(201,163,95,.4); }
  .ai-page-tile path { fill: none; stroke: rgba(201,163,95,.7); stroke-width: 1.6; stroke-linejoin: round; }
  .ai-page-tile { animation: aiTile 4.8s ease-in-out infinite; animation-delay: calc(var(--i) * .4s); }
  @keyframes aiTile { 0%, 70%, 100% { opacity: .55; } 10% { opacity: 1; } }

  /* Privacy gate */
  .ai-privacy-split { display: grid; grid-template-columns: minmax(0, 1.15fr) minmax(0, .85fr); gap: clamp(28px, 5vw, 70px); align-items: center; }
  .ai-privacy-split > div { min-width: 0; }
  @media (max-width: 860px) { .ai-privacy-split { grid-template-columns: minmax(0, 1fr); } .ai-privacy { max-width: 420px; } }
  .ai-privacy svg { width: 100%; height: auto; display: block; }
  .ai-priv-convo rect { fill: #fffdf8; stroke: var(--line); }
  .ai-priv-person { fill: var(--sand); stroke: none; } path.ai-priv-person { fill: none; stroke: var(--sand); stroke-width: 10; stroke-linecap: round; }
  .ai-priv-lines line { stroke: var(--sand); stroke-width: 7; stroke-linecap: round; animation: aiLine 3.2s ease-in-out infinite; }
  .ai-priv-lines line:nth-child(2n) { animation-delay: -1.6s; }
  @keyframes aiLine { 50% { opacity: .45; } }
  .ai-priv-gate line { stroke: var(--bronze); stroke-width: 3; stroke-linecap: round; }
  .ai-priv-gate rect { fill: var(--bronze); } .ai-priv-gate path { stroke: var(--bronze); stroke-width: 3; }
  .ai-priv-dest rect { fill: var(--deep); } .ai-priv-dest circle { fill: var(--bronze-light); animation: aiBlink 2.4s ease-in-out infinite; }
  .ai-priv-dest circle:nth-of-type(2) { animation-delay: .8s; } .ai-priv-dest circle:nth-of-type(3) { animation-delay: 1.6s; }
  @keyframes aiBlink { 50% { opacity: .3; } }
  .ai-chip circle:first-child { fill: var(--bronze-light); }
  .ai-chip path { fill: none; stroke: var(--deep); stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }
  .ai-chip-1 path { fill: var(--deep); stroke: none; } .ai-chip-1 circle + path + circle { fill: var(--bronze-light); }
  .ai-chip { offset-path: path("M140 160 C 200 160 210 160 244 160 C 290 160 320 150 387 150"); offset-rotate: 0deg; animation: aiChip 6s cubic-bezier(.5,0,.3,1) infinite; opacity: 0; }
  .ai-chip-2 { animation-delay: 2s; } .ai-chip-3 { animation-delay: 4s; }
  @keyframes aiChip { 0% { offset-distance: 0%; opacity: 0; } 8% { opacity: 1; } 55% { offset-distance: 100%; opacity: 1; } 62%, 100% { offset-distance: 100%; opacity: 0; } }

  @media (prefers-reduced-motion: reduce) {
    .ai-page *, .ai-page *::before { animation: none !important; transition: none !important; }
    .ai-chip { opacity: 1; offset-distance: 0%; } .ai-chip-1 { offset-distance: 100%; } .ai-chip-2 { offset-distance: 55%; }
  }
</style>`;

export const AI_PAGE_SCRIPT = `<script>
  (() => {
    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduce) document.querySelectorAll('.ai-page svg').forEach((svg) => { if (svg.pauseAnimations) svg.pauseAnimations(); });
    document.querySelectorAll('.ai-page .cards').forEach((group) => Array.from(group.children).forEach((card, i) => card.style.setProperty('--d', (i * 0.12) + 's')));
    const rise = document.querySelectorAll('.ai-rise');
    if (reduce || !('IntersectionObserver' in window)) rise.forEach((el) => el.classList.add('is-in'));
    else {
      const seen = new IntersectionObserver((entries) => entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-in');
        seen.unobserve(entry.target);
      }), { threshold: 0.18, rootMargin: '0px 0px -6% 0px' });
      rise.forEach((el) => {
        if (el.getBoundingClientRect().top < window.innerHeight) return;
        el.classList.add('ai-wait');
        seen.observe(el);
      });
    }

    // The chat demo: type a prompt, think, answer, hold, fade, next. Runs only while on screen.
    const chat = document.querySelector('[data-ai-chat]');
    if (!chat) return;
    const prompts = Array.from(document.querySelectorAll('.ai-prompts li')).map((li) => li.textContent.trim());
    const focus = ['w', 'e', 'm'];
    const typed = chat.querySelector('.ai-typed');
    const wait = (ms) => new Promise((done) => setTimeout(done, ms));
    let visible = false;
    let running = false;
    const showDone = (i) => { typed.textContent = prompts[i]; chat.dataset.focus = focus[i]; chat.className = 'ai-chat is-results'; };
    if (reduce || !prompts.length) { if (prompts.length) showDone(0); return; }
    async function loop() {
      if (running) return;
      running = true;
      let i = 0;
      while (visible) {
        chat.className = 'ai-chat is-typing';
        chat.dataset.focus = focus[i % focus.length];
        typed.textContent = '';
        const text = prompts[i];
        for (let c = 1; c <= text.length && visible; c += 1) {
          typed.textContent = text.slice(0, c);
          await wait(text[c - 1] === ' ' ? 55 : 28 + Math.random() * 30);
        }
        await wait(380);
        chat.className = 'ai-chat is-sent is-thinking';
        await wait(1300);
        chat.className = 'ai-chat is-results';
        await wait(5200);
        chat.classList.add('is-fading');
        await wait(650);
        i = (i + 1) % prompts.length;
      }
      running = false;
    }
    showDone(0);
    new IntersectionObserver((entries) => {
      visible = entries[0].isIntersecting;
      if (visible) loop();
    }, { threshold: 0.35 }).observe(chat);
  })();
</script>`;
