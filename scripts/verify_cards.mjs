// Guard rails for the listing card.
//
// The card is the single most reused component on the site -- 43 of them
// across the homepage, /developments, the area pages and the segment pages,
// times six languages. It has broken silently three times in one sitting:
//
//   1. Three copies of the gallery renderer drifted apart, so 19 galleries
//      never got the share/fullscreen buttons or the WebP markup.
//   2. A `.dev-img-wrap picture { display: block }` rule overrode the
//      slides' `display: contents`, collapsing six slides into one and
//      killing the swipe -- the markup was still perfect.
//   3. A full-card click overlay (`inset: 0`) sat on top of the gallery, so
//      a finger dragging over the photo hit an anchor instead of the
//      scroller. Again the markup was perfect; only the stacking was wrong.
//
// Every one of those shipped looking fine in a screenshot. This script
// asserts the invariants that were violated, so the build fails instead of
// the website.
//
// Run automatically at the end of build_dist.mjs. Also runnable alone:
//   node scripts/verify_cards.mjs

import fs from 'node:fs';
import path from 'node:path';

import { CARD_CHROME_ENTRIES } from './lib/card_chrome_translations.mjs';

// Every project's English card description and its per-locale translation,
// used to catch the case where a locale page renders the English one.
const PROJECT_DIR = path.join(process.cwd(), 'content', 'liora-projects');
const cardDescriptions = [];
if (fs.existsSync(PROJECT_DIR)) {
  for (const slug of fs.readdirSync(PROJECT_DIR)) {
    const file = path.join(PROJECT_DIR, slug, 'project.json');
    if (!fs.existsSync(file)) continue;
    const project = JSON.parse(fs.readFileSync(file, 'utf8'));
    const english = project.card?.description || project.description;
    if (english) cardDescriptions.push({ slug, english, i18n: project.i18n || {} });
  }
}

const dist = path.join(process.cwd(), 'dist');
const failures = [];

function fail(where, message) {
  failures.push(`${where}: ${message}`);
}

function htmlFiles(dir) {
  const out = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (entry.name === 'assets' || entry.name === 'content') continue;
      out.push(...htmlFiles(full));
    } else if (entry.name.endsWith('.html')) {
      out.push(full);
    }
  }
  return out;
}

// ---------------------------------------------------------------------------
// 1. CSS invariants
//
// These are presence checks on the rules whose absence caused a real,
// shipped breakage. They are deliberately narrow: each one names the bug it
// prevents, so if a future redesign genuinely removes the need for a rule,
// the person deleting it sees exactly what they are taking on.
// ---------------------------------------------------------------------------

const CSS_INVARIANTS = [
  {
    // Bug 3. If the overlay's containing block is .project-card again, it
    // covers the photo and the gallery stops receiving touches.
    pattern: /\.project-card\[data-project-card\]\s+\.dev-body\s*\{[^}]*position:\s*relative/,
    why: 'the full-card click overlay must be anchored to .dev-body, or it covers the '
       + 'gallery and swiping dies on every page except the homepage'
  },
  {
    // Bug 2. <picture> must stay display:contents so the <img> remains the
    // flex item of the scroll track.
    pattern: /\.dev-img-wrap\s+\.project-card-gallery-track\s+picture\s*\{[^}]*display:\s*contents/,
    why: 'gallery slides must keep display:contents, or all six slides collapse into '
       + 'one and the track stops scrolling'
  },
  {
    // The scroller itself. Native overflow scrolling is what makes the swipe
    // work; there is no JS gesture handling to fall back on.
    pattern: /\.project-card-gallery-track\s*\{[^}]*overflow-x:\s*auto/,
    why: 'the gallery track must stay a native horizontal scroller'
  },
  {
    // The track must also be a flex strip. These rules used to live only in
    // liora-pages.css and the homepage's inline copy -- and the homepage
    // does not load liora-pages.css, so losing them here stacks the slides
    // vertically on the one page that cannot fall back.
    pattern: /\.project-card-gallery-track\s*\{[^}]*display:\s*flex/,
    why: 'the gallery track must stay display:flex or the slides stop being a strip'
  },
  {
    pattern: /\.project-card-gallery-track\s+img\s*\{[^}]*flex:\s*0\s+0\s+100%/,
    why: 'each slide must be exactly one track width, or the carousel mistracks'
  },
  {
    // The scrim is the only thing making the overlay text legible; without
    // it a bright render leaves white-on-white.
    pattern: /\.dev-scrim\s*\{[^}]*linear-gradient/,
    why: 'the image scrim must stay, or the badges, location and price lose contrast'
  },
  {
    // A mandatory snap type plus scroll-snap-stop:always traps the gesture.
    pattern: /scroll-snap-type:\s*x\s+proximity/,
    why: 'snap must stay `proximity`; `mandatory` combined with scroll-snap-stop '
       + 'traps the gesture and a fast swipe sticks'
  }
];

const cssPath = path.join(dist, 'assets/liora/nueva-system.css');
if (!fs.existsSync(cssPath)) {
  fail('nueva-system.css', 'missing from dist');
} else {
  const css = fs.readFileSync(cssPath, 'utf8');
  for (const { pattern, why } of CSS_INVARIANTS) {
    if (!pattern.test(css)) fail('nueva-system.css', `${why} (no rule matching ${pattern})`);
  }
}

// ---------------------------------------------------------------------------
// 2. Markup invariants, on every card of every built page
// ---------------------------------------------------------------------------

const CARD_RE = /<article class="project-card dev-card[^"]*"[\s\S]*?<\/article>/g;
const OLD_CARD_MARKUP = /<article class="project-card(?! dev-card)/;

// Whether a string is "still English" is decided by the translation table
// itself, not by a list kept here -- German deliberately keeps "Off-Plan",
// and a hardcoded list would flag that forever. An entry counts as applied
// when the rendered text differs from the English `find`, or when the table
// says this locale uses the English wording on purpose.
const LOCALES = ['es', 'fr', 'de', 'ru', 'ar'];

// Every badge wording the table knows about, per locale. A badge outside
// this set is a new one nobody has translated -- exactly what happens when
// a project is added with an unfamiliar status.
const knownBadges = {};
for (const locale of LOCALES) {
  knownBadges[locale] = new Set(
    CARD_CHROME_ENTRIES
      .filter((entry) => entry.find.startsWith('dev-badge">'))
      .map((entry) => (entry[locale] || entry.find).replace('dev-badge">', ''))
  );
}

const pages = htmlFiles(dist);
let cardCount = 0;
const pagesWithCards = [];

for (const file of pages) {
  const name = path.relative(dist, file);
  const html = fs.readFileSync(file, 'utf8');

  if (OLD_CARD_MARKUP.test(html)) {
    fail(name, 'renders a project card that is not the shared unified card '
             + '(scripts/lib/project_card.mjs) -- card markup has forked again');
  }

  const cards = html.match(CARD_RE) || [];
  if (!cards.length) continue;
  pagesWithCards.push(name);
  cardCount += cards.length;

  const locale = name.includes('/') ? name.split('/')[0] : 'en';
  const isTranslated = ['es', 'fr', 'de', 'ru', 'ar'].includes(locale);

  cards.forEach((card, index) => {
    const where = `${name} card ${index + 1}`;

    // Structure. Each of these is something a redesign could quietly drop.
    const required = [
      ['dev-img-wrap', /class="dev-img-wrap"/],
      ['gallery track', /data-gallery-track/],
      ['share button', /data-card-share/],
      ['card body', /class="dev-body"/],
      ['project name', /class="dev-name"/],
      ['CTA link', /class="dev-cta-link"/]
    ];
    for (const [label, pattern] of required) {
      if (!pattern.test(card)) fail(where, `missing ${label}`);
    }

    // A multi-slide gallery needs one dot per slide and both arrows --
    // this is what caught the drifted renderer copies.
    const slides = (card.match(/<img[^>]+class=|<img /g) || []).length;
    const dots = (card.match(/data-gallery-dot="/g) || []).length;
    if (dots) {
      const trackSlides = (card.match(/data-gallery-track[\s\S]*?<\/div>/)?.[0].match(/<img /g) || []).length;
      if (trackSlides && dots !== trackSlides) {
        fail(where, `${trackSlides} slides but ${dots} dots`);
      }
      if (!/data-gallery-prev/.test(card) || !/data-gallery-next/.test(card)) {
        fail(where, 'multi-slide gallery is missing its arrows');
      }
      if (!/data-card-expand/.test(card)) {
        fail(where, 'multi-slide gallery is missing the fullscreen button');
      }
    }
    if (slides === 0) fail(where, 'has no image at all');

    // The card must not send the reader out of their language. data-card-url
    // is how the gallery navigates when the photo is clicked, so an
    // unlocalized one drops an Arabic reader onto the English project page
    // -- and only on that click, which is why it survived unnoticed while
    // the visible button was correct.
    const cardUrl = card.match(/data-card-url="([^"]+)"/)?.[1];
    if (cardUrl && !/^(?:[a-z][a-z0-9+.-]*:|\/\/|\/|#)/i.test(cardUrl)) {
      if (isTranslated && !cardUrl.startsWith(`${locale}/`)) {
        fail(where, `data-card-url "${cardUrl}" is not inside /${locale}/ -- clicking the `
                  + 'card image would switch the reader to English');
      }
      if (!isTranslated && /^(?:es|fr|de|ru|ar)\//.test(cardUrl)) {
        fail(where, `data-card-url "${cardUrl}" points into a locale directory on an English page`);
      }
    }

    // The description is translated by a find/replace keyed on the card's
    // markup, so a change to the tagline element silently stops it matching
    // and five languages quietly fall back to English with no error.
    if (isTranslated) {
      for (const { slug, english, i18n } of cardDescriptions) {
        const translated = i18n[locale]?.card?.description;
        if (translated && translated !== english && card.includes(`>${english}<`)) {
          fail(where, `${slug} renders its English description on a ${locale} page -- `
                    + 'the card description replacement stopped matching');
        }
      }
    }

    // Translation. The card chrome is localized by find/replace entries in
    // lib/card_chrome_translations.mjs; a new badge or a reworded CTA that
    // nobody adds an entry for shows up as English on five languages.
    if (isTranslated) {
      for (const entry of CARD_CHROME_ENTRIES) {
        // Only a real miss: the English wording is still on the page while
        // the table says this locale renders something else.
        if (entry[locale] !== entry.find && card.includes(entry.find)) {
          fail(where, `untranslated card chrome on a ${locale} page: `
                    + `"${entry.find.slice(0, 48)}" should be "${entry[locale].slice(0, 48)}"`);
        }
      }

      const badge = card.match(/class="dev-badge">([^<]*)</)?.[1];
      if (badge && !knownBadges[locale].has(badge)) {
        fail(where, `badge "${badge}" has no translation entry -- add one to `
                  + 'scripts/lib/card_chrome_translations.mjs so it is not English '
                  + 'on all five languages');
      }
    }
  });
}

// The card must be on every grid, in every language. If a locale build
// silently stops emitting cards, the count drops and this catches it.
const EXPECTED_GRID_PAGES = ['index.html', 'developments.html', 'area-marbella.html'];
for (const locale of ['', 'es/', 'fr/', 'de/', 'ru/', 'ar/']) {
  for (const page of EXPECTED_GRID_PAGES) {
    const target = `${locale}${page}`;
    if (fs.existsSync(path.join(dist, target)) && !pagesWithCards.includes(target)) {
      fail(target, 'renders no listing cards at all');
    }
  }
}

if (failures.length) {
  console.error(`\nCard verification FAILED (${failures.length}):`);
  failures.forEach((message) => console.error(`  - ${message}`));
  console.error('\nThe listing card is shared by every grid on the site. Fix the above '
              + 'before deploying -- see scripts/lib/project_card.mjs.\n');
  process.exit(1);
}

console.log(`Card verification passed: ${cardCount} cards across ${pagesWithCards.length} pages.`);
