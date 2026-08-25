import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const root = process.cwd();
const dist = path.join(root, 'dist');
const failures = [];
const warnings = [];
const expectedNavTargets = [
  'guides.html',
  'about.html',
  'developments.html',
  'areas.html',
  'advisory.html',
  'contact.html'
];

function fail(file, message) {
  failures.push(`${file}: ${message}`);
}

function warn(file, message) {
  warnings.push(`${file}: ${message}`);
}

// The mobile menu now contains a nested <div> (the Guides submenu panel),
// so a non-greedy match to the first </div> stops early and reports the
// links after it as missing. Walk the tag stack to the real closing tag
// instead.
function extractMobileMenu(html) {
  const open = html.match(/<div class="mobile-menu"[^>]*>/i);
  if (!open) return '';
  const start = open.index + open[0].length;
  const tag = /<(\/?)div\b[^>]*>/gi;
  tag.lastIndex = start;
  let depth = 1;
  let match;
  while ((match = tag.exec(html))) {
    depth += match[1] ? -1 : 1;
    if (depth === 0) return html.slice(start, match.index);
  }
  return html.slice(start);
}

function localTarget(file, rawTarget) {
  const target = rawTarget.split('#')[0].split('?')[0];
  if (!target || /^(?:https?:|mailto:|tel:|data:|blob:|javascript:|#|\/\.netlify\/)/i.test(rawTarget)) {
    return null;
  }
  if (target.startsWith('/')) {
    return path.join(dist, target === '/' ? 'index.html' : target.slice(1));
  }
  return path.resolve(path.dirname(file), target);
}

if (!fs.existsSync(dist)) {
  throw new Error('dist does not exist. Run node scripts/build_dist.mjs first.');
}

const htmlFiles = fs.readdirSync(dist)
  .filter((file) => file.endsWith('.html'))
  .sort();

for (const name of htmlFiles) {
  const file = path.join(dist, name);
  const html = fs.readFileSync(file, 'utf8');
  // The system stylesheet is inlined into a <style data-nueva-system> block
  // by build_dist rather than linked, so there is no versioned href to count.
  // The intent of this check is unchanged: exactly one copy of it, and it
  // must win the cascade against the linked stylesheets (asserted below).
  const systemStyles = html.match(/<style data-nueva-system>/g) || [];
  const trackingScripts = html.match(/assets\/liora\/nueva-tracking\.js\?v=[a-z0-9]+/gi) || [];

  if (systemStyles.length !== 1) {
    fail(name, `expected one inlined Nueva system stylesheet, found ${systemStyles.length}`);
  }
  if (trackingScripts.length !== 1) {
    fail(name, `expected one versioned Nueva tracking script, found ${trackingScripts.length}`);
  }
  if (!/<head>[\s\S]*assets\/liora\/nueva-tracking\.js\?v=[a-z0-9]+[\s\S]*<\/head>/i.test(html)) {
    fail(name, 'Nueva tracking script is not loaded from the document head');
  }

  // The inlined block must come after every linked stylesheet, or the linked
  // sheets override it on equal specificity -- which is exactly how the card
  // CTA silently lost its colour during the redesign.
  const lastLink = html.lastIndexOf('rel="stylesheet"');
  const systemStyleAt = html.indexOf('<style data-nueva-system>');
  if (systemStyleAt !== -1 && lastLink !== -1 && systemStyleAt < lastLink) {
    fail(name, 'Nueva system stylesheet is not the final stylesheet');
  }

  const ids = [...html.matchAll(/\sid="([^"]+)"/gi)].map((match) => match[1]);
  const duplicates = [...new Set(ids.filter((id, index) => ids.indexOf(id) !== index))];
  if (duplicates.length) {
    fail(name, `duplicate IDs: ${duplicates.join(', ')}`);
  }

  const title = html.match(/<title>([\s\S]*?)<\/title>/i)?.[1]?.trim();
  if (!title) fail(name, 'missing page title');

  for (const match of html.matchAll(/<button\b([^>]*)>/gi)) {
    if (!/\btype="(?:button|submit|reset)"/i.test(match[1])) {
      fail(name, 'button without an explicit type attribute');
    }
  }

  for (const match of html.matchAll(/<script([^>]*)>([\s\S]*?)<\/script>/gi)) {
    const attributes = match[1];
    const script = match[2].trim();
    if (!script || /\bsrc=/i.test(attributes) || /application\/ld\+json/i.test(attributes)) continue;
    try {
      new vm.Script(script, { filename: `${name}:inline-script` });
    } catch (error) {
      fail(name, `inline JavaScript syntax error: ${error.message}`);
    }
  }

  if (!html.includes('class="site-nav"') && name !== 'index.html') {
    warn(name, 'does not use the shared secondary-page navigation');
  } else if (name !== 'index.html') {
    const desktopNav = html.match(/<nav class="site-nav">([\s\S]*?)<\/nav>/i)?.[1] || '';
    const mobileNav = extractMobileMenu(html);
    for (const target of expectedNavTargets) {
      if (!desktopNav.includes(`href="${target}"`)) {
        fail(name, `desktop navigation is missing ${target}`);
      }
      if (!mobileNav.includes(`href="${target}"`)) {
        fail(name, `mobile navigation is missing ${target}`);
      }
    }
  }

  // Every page carries two language switchers: one in the desktop header,
  // one in the burger menu. Both are injected by find/replace against
  // anchors in hand-authored markup, so a nav edit can quietly stop an
  // anchor matching and drop a switcher with no build error -- which is
  // exactly how the desktop switcher disappeared from four pages and the
  // mobile one from every locale homepage. Assert the count instead.
  const switcherCount = (html.match(/class="lang-switcher"/g) || []).length;
  if (switcherCount !== 2) {
    fail(name, `expected 2 language switchers (desktop + mobile), found ${switcherCount}`);
  }

  // Likewise the Guides submenu, which shares the same injection risk.
  const dropdownCount = (html.match(/<details class="nav-dropdown"/g) || []).length;
  if (dropdownCount !== 2) {
    fail(name, `expected 2 Guides submenus (desktop + mobile), found ${dropdownCount}`);
  }

  const attributes = [...html.matchAll(/\s(?:href|src|poster)="([^"]+)"/gi)];
  for (const [, rawTarget] of attributes) {
    const target = localTarget(file, rawTarget);
    if (target && !fs.existsSync(target)) {
      fail(name, `missing local target ${rawTarget}`);
    }
  }
}

// Indexable pages and sitemap URLs must be the same set.
//
// These drifted once already: the five locale copies of each legal page
// carried no robots meta while their English original was noindex, so 15
// pages were indexable but deliberately absent from the sitemap -- Google
// told to ignore them by intent and to find them in practice. Comparing
// the two sets catches either half of that going wrong: a page excluded
// from the sitemap but left indexable, or a sitemap URL that turns out to
// be noindex.
{
  const sitemapPath = path.join(dist, 'sitemap.xml');
  if (fs.existsSync(sitemapPath)) {
    const xml = fs.readFileSync(sitemapPath, 'utf8');
    const listed = new Set(
      [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)]
        .map((match) => match[1].replace(/^https?:\/\/[^/]+\//, '').replace(/\/$/, '/index.html') || 'index.html')
    );

    const indexable = [];
    for (const file of everyHtmlFile(dist)) {
      const html = fs.readFileSync(file, 'utf8');
      if (/<meta name="robots" content="[^"]*noindex/i.test(html)) continue;
      indexable.push(path.relative(dist, file));
    }

    for (const page of indexable) {
      if (!listed.has(page)) {
        fail(page, 'is indexable but not listed in sitemap.xml -- either add it or mark it noindex');
      }
    }
    for (const url of listed) {
      const target = path.join(dist, url);
      if (fs.existsSync(target) && /<meta name="robots" content="[^"]*noindex/i.test(fs.readFileSync(target, 'utf8'))) {
        fail(url, 'is listed in sitemap.xml but is noindex');
      }
    }
  }
}

// Every in-page link must land on a section that exists, in every language.
// The property pages' sub-nav is the reason: its entries are conditional
// (media only when there are images, payment terms only when the project has
// a construction timeline), so a link and its section can drift apart and
// the tab then silently scrolls nowhere. This walks the locale directories
// too, which the checks above do not.
function everyHtmlFile(dir) {
  const out = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.isDirectory()) {
      if (entry.name === 'assets' || entry.name === 'content') continue;
      out.push(...everyHtmlFile(path.join(dir, entry.name)));
    } else if (entry.name.endsWith('.html')) {
      out.push(path.join(dir, entry.name));
    }
  }
  return out;
}

for (const file of everyHtmlFile(dist)) {
  const html = fs.readFileSync(file, 'utf8');
  const ids = new Set([...html.matchAll(/id="([^"]+)"/g)].map((match) => match[1]));
  const targets = new Set([...html.matchAll(/href="#([^"]+)"/g)].map((match) => match[1]));
  for (const target of targets) {
    if (target && !ids.has(target)) {
      fail(path.relative(dist, file), `in-page link #${target} has no matching element`);
    }
  }
}

const cssFile = path.join(dist, 'assets/liora/nueva-system.css');
if (!fs.existsSync(cssFile)) {
  fail('assets/liora/nueva-system.css', 'missing from dist');
} else {
  const css = fs.readFileSync(cssFile, 'utf8');
  const open = (css.match(/{/g) || []).length;
  const close = (css.match(/}/g) || []).length;
  if (open !== close) fail('assets/liora/nueva-system.css', `unbalanced braces (${open}/${close})`);
}

// The hero H1 is not allowed to break inside a word -- "Guadalobon" splitting
// into "Guadalobo / n" is what this exists to stop. The stylesheet caps the
// font size using --hero-title-run, the longest run of characters in the title
// that has no break opportunity in it. If that number is ever smaller than the
// title actually contains, the cap is too generous and the word breaks again.
// Recompute it from the rendered markup and compare, on every locale of every
// project page.
function heroTitleRunFromMarkup(nameHtml) {
  const text = nameHtml
    .replace(/<br\s*\/?>/gi, ' ')
    .replace(/<[^>]+>/g, '')
    .replace(/&nbsp;/gi, ' ')
    .replace(/&[a-z]+;|&#\d+;/gi, 'x');
  return text
    .split(/[\s\u00a0]+|(?<=-)|(?<=\u2013)|(?<=\u2014)/)
    .reduce((longest, run) => Math.max(longest, run.trim().length), 0);
}

// htmlFiles above is English-only and holds bare filenames; the hero title
// has to hold up in every locale, so enumerate dist and its locale folders.
const propertyPages = [dist, ...fs.readdirSync(dist, { withFileTypes: true })
  .filter((entry) => entry.isDirectory() && /^[a-z]{2}$/.test(entry.name))
  .map((entry) => path.join(dist, entry.name))]
  .flatMap((dir) => fs.readdirSync(dir)
    .filter((name) => name.startsWith('property-') && name.endsWith('.html'))
    .map((name) => path.join(dir, name)));

let heroTitlesChecked = 0;
for (const file of propertyPages) {
  const relative = path.relative(dist, file);
  const html = fs.readFileSync(file, 'utf8');
  const nameMatch = html.match(/<span class="hero-title-name">([\s\S]*?)<\/span>/);
  if (!nameMatch) continue;
  const runMatch = html.match(/<h1 class="hero-title"[^>]*--hero-title-run:\s*(\d+)/);
  if (!runMatch) {
    fail(relative, 'hero H1 has no --hero-title-run, so its font size is not capped '
      + 'and a long project name will break mid-word');
    continue;
  }
  heroTitlesChecked += 1;
  const declared = Number(runMatch[1]);
  const actual = heroTitleRunFromMarkup(nameMatch[1]);
  if (declared < actual) {
    fail(relative, `--hero-title-run is ${declared} but the title contains an unbreakable `
      + `run of ${actual} characters, so the font size cap is too generous and the word will split`);
  }
}

// {count} is a build-time placeholder resolved by resolveCount() for segment
// titles and H1s. It leaked into the JSON-LD and the og:/twitter: tags, so
// structured data advertised a literal "{count} New-Build Apartments..." on
// every segment page. The only legitimate survivor is a data-i18n-* attribute,
// which is a client-side template the discovery script fills in at runtime.
const countPlaceholderPages = [dist, ...fs.readdirSync(dist, { withFileTypes: true })
  .filter((entry) => entry.isDirectory() && /^[a-z]{2}$/.test(entry.name))
  .map((entry) => path.join(dist, entry.name))]
  .flatMap((dir) => fs.readdirSync(dir)
    .filter((name) => name.endsWith('.html'))
    .map((name) => path.join(dir, name)));

for (const file of countPlaceholderPages) {
  const html = fs.readFileSync(file, 'utf8');
  if (!html.includes('{count}')) continue;
  const stripped = html.replace(/\sdata-i18n-[a-z-]+="[^"]*"/g, '');
  if (stripped.includes('{count}')) {
    fail(path.relative(dist, file), 'an unresolved {count} placeholder reaches the page outside a '
      + 'data-i18n-* attribute -- it is being published to readers or to search engines');
  }
}

// Every form that posts a lead to the CRM carries a hidden honeypot. The CRM
// treats a filled one as decisive spam, so a form that ships without the field
// simply loses that protection -- silently, and only for that one form. Before
// this check the newsletter had a honeypot and all eleven actual lead forms
// did not, which is the shape of gap it exists to catch.
let leadFormsChecked = 0;
for (const file of countPlaceholderPages) {
  const html = fs.readFileSync(file, 'utf8');
  const relative = path.relative(dist, file);
  for (const match of html.matchAll(/<form[^>]*\bdata-crm-lead\b[^>]*>([\s\S]*?)<\/form>/g)) {
    leadFormsChecked += 1;
    const nameAttr = match[0].match(/name="([^"]+)"/);
    const formName = nameAttr ? nameAttr[1] : 'unnamed form';
    if (!/name="honeypot"/.test(match[1])) {
      fail(relative, `the CRM lead form "${formName}" has no hidden honeypot field, so bot `
        + 'submissions reach the CRM unflagged');
    }
  }
}

// Some lead forms are authored inside the JavaScript bundles and injected at
// runtime, so they never appear in the built HTML the check above walks. The
// shortlist form is one, and it shipped without a honeypot for exactly that
// reason. Scan the scripts for the same marker.
for (const name of fs.readdirSync(path.join(dist, 'assets', 'liora')).filter((f) => f.endsWith('.js'))) {
  const source = fs.readFileSync(path.join(dist, 'assets', 'liora', name), 'utf8');
  for (const match of source.matchAll(/<form[^>]*\bdata-crm-lead\b[^>]*>([\s\S]{0,4000}?)<\/form>/g)) {
    leadFormsChecked += 1;
    if (!/name=.honeypot./.test(match[1])) {
      fail(`assets/liora/${name}`, 'a CRM lead form written in JavaScript has no hidden honeypot '
        + 'field, so bot submissions from it reach the CRM unflagged');
    }
  }
  // And the client picks payload fields by name rather than serialising the
  // form, so the field has to be read explicitly or it never gets sent.
  if (/buildLeadPayload/.test(source) && !/\[name="honeypot"\]/.test(source)) {
    fail(`assets/liora/${name}`, 'buildLeadPayload does not read [name="honeypot"], so the hidden '
      + 'field is never included in the payload sent to the CRM');
  }
}

// Structured data now uses @id so the company and the two founders are one
// entity across the site rather than a fresh node minted per page. That only
// works if a reference resolves: the about page referenced the Organization by
// @id while the Organization node itself lived only on the homepage, leaving
// the one fact that page exists to assert -- who these people work for --
// hanging on a parser's willingness to go looking. Every {"@id": ...}
// reference must have a node defining that id on the same page.
let schemaRefsChecked = 0;
for (const file of countPlaceholderPages) {
  const html = fs.readFileSync(file, 'utf8');
  const relative = path.relative(dist, file);
  const defined = new Set();
  const referenced = new Map();

  const visit = (node, isRoot) => {
    if (Array.isArray(node)) return node.forEach((child) => visit(child, isRoot));
    if (!node || typeof node !== 'object') return;
    const id = node['@id'];
    // A node that carries @type as well as @id defines the entity; a bare
    // {"@id": ...} is a reference to one defined elsewhere.
    if (id && node['@type']) defined.add(id);
    else if (id && Object.keys(node).length === 1) referenced.set(id, true);
    for (const value of Object.values(node)) visit(value, false);
  };

  for (const block of html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)) {
    let parsed;
    try {
      parsed = JSON.parse(block[1]);
    } catch (error) {
      fail(relative, `JSON-LD does not parse: ${error.message}`);
      continue;
    }
    visit(parsed, true);
  }

  for (const id of referenced.keys()) {
    schemaRefsChecked += 1;
    if (!defined.has(id)) {
      fail(relative, `JSON-LD references the entity ${id} but no node on this page defines it, `
        + 'so the reference does not resolve');
    }
  }
}

// The buying guides state tax rates, statutory guarantee periods and warranty
// law. They shipped for weeks carrying only WebPage + BreadcrumbList -- the
// same assertions with no named author and no dates, which is the weakest
// possible posture for advice about a purchase this size. A guide that loses
// its byline or its Article block loses that silently, on one page.
let guidesChecked = 0;
for (const file of countPlaceholderPages) {
  const name = path.basename(file);
  if (!name.startsWith('guide-')) continue;
  const relative = path.relative(dist, file);
  const html = fs.readFileSync(file, 'utf8');
  guidesChecked += 1;

  if (!/class="guide-byline"/.test(html)) {
    fail(relative, 'a buying guide with no visible byline -- readers cannot see who stands '
      + 'behind advice on tax, guarantees or warranty law');
  }

  let article = null;
  for (const block of html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)) {
    let parsed;
    try {
      parsed = JSON.parse(block[1]);
    } catch {
      continue;
    }
    for (const node of Array.isArray(parsed) ? parsed : [parsed]) {
      if (node && node['@type'] === 'Article') article = node;
    }
  }

  if (!article) {
    fail(relative, 'a buying guide with no Article schema, so it names no author and no dates');
    continue;
  }
  for (const field of ['author', 'publisher', 'datePublished', 'dateModified']) {
    if (!article[field]) fail(relative, `the guide's Article schema has no ${field}`);
  }
  const bylineDate = html.match(/data-guide-updated datetime="(\d{4}-\d{2}-\d{2})"/)?.[1];
  if (bylineDate && article.dateModified && bylineDate !== article.dateModified) {
    fail(relative, `the visible byline says the guide was updated ${bylineDate} but its Article `
      + `schema says ${article.dateModified} -- readers and search engines are told different things`);
  }
}

// Accessibility fixes that are invisible by construction, and therefore the
// easiest kind to lose: nothing looks wrong when they regress.
let a11yPagesChecked = 0;
for (const file of countPlaceholderPages) {
  const relative = path.relative(dist, file);
  const html = fs.readFileSync(file, 'utf8');
  a11yPagesChecked += 1;

  // WCAG 2.4.1 -- injected by build_dist, so a change to that pipeline drops it
  // from every page at once rather than from one.
  if (!/data-skip-link/.test(html)) {
    fail(relative, 'no skip link, so a keyboard user must tab through the whole navigation '
      + 'on every page');
  } else if (!/<main[^>]*\sid="main-content"/.test(html)) {
    fail(relative, 'has a skip link but no #main-content for it to land on');
  }

  // WCAG 1.3.1 / 4.1.2 -- the visible label sits in a <div>, so the association
  // is explicit and silently droppable. A screen reader gets "slider" without it.
  for (const control of html.matchAll(/<input[^>]*\bdata-calc-(price-range|price|deposit|term)\b[^>]*>/g)) {
    if (!/aria-labelledby=|aria-label=/.test(control[0])) {
      fail(relative, `the calculator's ${control[1]} control has no accessible name`);
    }
  }
}

// Enquiry context and the cinematic-player link travel in the fragment, not a
// query string. Each distinct ?intent=<project> - <unit> was a separate
// crawlable URL serving the byte-identical contact page, and the site rendered
// 1,987 of them; ?private-viewing=1&project=<slug> added 600 more. Google
// consolidated them correctly via canonical, so nothing was mis-indexed -- it
// was simply a thousand duplicate URLs offered to the crawler for no gain.
//
// Readers still accept the query string, so links already in the wild keep
// working. What must not come back is the site *rendering* them.
let internalLinksScanned = 0;
for (const file of countPlaceholderPages) {
  const relative = path.relative(dist, file);
  const html = fs.readFileSync(file, 'utf8');
  for (const match of html.matchAll(/href="([^"]+)"/g)) {
    const href = match[1];
    if (/^(?:https?:)?\/\//.test(href) && !href.includes('nuevaliving.com')) continue;
    if (/^(?:mailto|tel):/.test(href)) continue;
    const query = href.split('#')[0].split('?')[1];
    if (!query) continue;
    internalLinksScanned += 1;
    // ?v= is the asset cache-buster on stylesheets and scripts, not a page URL.
    if (/^v=[A-Za-z0-9]+$/.test(query)) continue;
    fail(relative, `an internal link carries a query string ("?${query.slice(0, 48)}"), which gives `
      + 'Google a separate crawlable URL for the same document -- put the state in the fragment');
  }
}

// Titles were only ever checked in English, and three separate faults hid in
// the locale copies: an <em>-less half-translated H1 reading "84 New-Build
// Lägenheter och takvåningar for Sale in Marbella", a doubled brand suffix,
// and six titles running to 67 characters because seoTitle's shortening step
// split the property type on English conjunctions and silently no-opped for
// Polish, Dutch and Norwegian.
let localeTitlesChecked = 0;
const decodeEntities = (value) => value
  .replace(/&amp;/g, '&').replace(/&middot;/g, '·').replace(/&nbsp;/g, ' ')
  .replace(/&[a-z]+;/gi, 'x');

for (const file of countPlaceholderPages) {
  const relative = path.relative(dist, file);
  const html = fs.readFileSync(file, 'utf8');
  const locale = /^([a-z]{2})\//.exec(relative)?.[1] || 'en';
  const match = html.match(/<title>([\s\S]*?)<\/title>/);
  if (!match) {
    fail(relative, 'no <title>');
    continue;
  }
  localeTitlesChecked += 1;
  const title = decodeEntities(match[1]).trim();

  if (title.length > 62) {
    fail(relative, `<title> is ${title.length} characters, over the 62 that survive in a result: `
      + `"${title.slice(0, 60)}"`);
  }
  // "Nueva Living | Nueva Living" -- the builder appends the brand and some
  // overlays already carried it.
  if ((title.match(/Nueva Living/g) || []).length > 1 && !/why-nueva|om-oss|about/.test(relative)) {
    fail(relative, `<title> names the brand twice: "${title}"`);
  }
  // English fragments stranded in a translated title by a stale find string.
  if (locale !== 'en' && /\b(New-Build|for Sale)\b/.test(title)) {
    fail(relative, `<title> is part-translated -- an English fragment survives: "${title}"`);
  }
}

// Canonical form of every URL the site publishes about itself.
//
// Two live defects, both found in the Google Business Profile rather than in
// the build: the website field pointed at https://www.nuevaliving.com/ (which
// 301s to the apex, so the profile and the site never asserted the same URL),
// and the Facebook profile was claimed over plain http. Neither broke a page.
// Both weakened exactly the signal -- one company, one set of URLs -- that
// `sameAs`, `url` and <link rel="canonical"> exist to send.
//
// The site is the half we control at build time, so it is the half that gets
// checked: nothing we publish may point at the www host, and no URL we claim
// as our own may be unencrypted.
const CANONICAL_HOST = 'https://nuevaliving.com';
let selfUrlsChecked = 0;

for (const file of everyHtmlFile(dist)) {
  const relative = path.relative(dist, file);
  const html = fs.readFileSync(file, 'utf8');

  const wwwHits = html.match(/https?:\/\/www\.nuevaliving\.com[^"'\s<>]*/g) || [];
  for (const hit of wwwHits) {
    fail(relative, `publishes the www host, which 301s to the apex: "${hit}" `
      + `-- use ${CANONICAL_HOST} so the profile, the sitemap and the page all name one URL`);
  }

  // Only URLs the site claims as its own identity, not arbitrary outbound links.
  const schemaBlocks = html.match(/<script type="application\/ld\+json">[\s\S]*?<\/script>/g) || [];
  for (const block of schemaBlocks) {
    const insecure = block.match(/"http:\/\/[^"]+"/g) || [];
    for (const hit of insecure) {
      fail(relative, `claims an unencrypted URL in structured data: ${hit} -- `
        + 'a http:// sameAs is a different URL to Google than its https:// twin');
    }
  }

  const canonical = /<link rel="canonical" href="([^"]+)"/.exec(html);
  if (canonical) {
    selfUrlsChecked += 1;
    if (!canonical[1].startsWith(CANONICAL_HOST)) {
      fail(relative, `<link rel="canonical"> is not on ${CANONICAL_HOST}: "${canonical[1]}"`);
    }
  }
}

// One label per destination, per locale, in nav and footer.
//
// `developments.html` was reachable under four different Swedish names at
// once: "Nybyggnadsprojekt" from the nav, "Alla nybyggnadsprojekt" from the
// footer, and "Bostadsprojekt"/"Alla Bostadsprojekt" from the developments
// page, whose translations live in a second table that had drifted from
// strings.json. Every one of them rendered correctly, so nothing looked
// broken -- but a search engine reading the site sees one destination
// described four ways, and internal anchor text is part of how it decides
// what to call a page.
//
// Body CTAs are deliberately out of scope: "Explore Developments" is
// conversion copy and is allowed to read differently from a menu item. This
// checks navigation only, where one name is the whole point.
const NAV_DESTINATIONS = new Set([
  'developments.html', 'areas.html', 'guides.html', 'advisory.html',
  'contact.html', 'about.html', 'why-nueva.html', 'compare.html', 'referrals.html',
  'privacy-policy.html', 'legal-notice.html', 'cookie-policy.html'
]);
const navLabels = new Map(); // `${locale}|${target}` -> Map<label, firstFile>
let navLabelsChecked = 0;

for (const file of everyHtmlFile(dist)) {
  const relative = path.relative(dist, file);
  const locale = /^([a-z]{2})\//.exec(relative)?.[1] || 'en';
  const html = fs.readFileSync(file, 'utf8');

  // Match each region against its OWN closing tag. An alternation here lets
  // <nav> pair with the page's final </footer> and swallow the whole body,
  // which turned every prose link into a navigation link.
  const regions = [
    ...(html.match(/<nav\b[\s\S]*?<\/nav>/g) || []),
    ...(html.match(/<footer\b[\s\S]*?<\/footer>/g) || [])
  ];
  for (const region of regions) {
    for (const [, href, label] of region.matchAll(/<a[^>]*href="([^"]+)"[^>]*>([^<]+)<\/a>/g)) {
      // Local page targets only -- not anchors, assets or outbound links.
      if (!/^(?:\.\.\/)*[a-z0-9-]+\/?(?:[a-z0-9-]+)?\.html$/.test(href)) continue;
      // The site's own navigation set. Contextual cross-links are deliberately
      // excluded: a segment page linking to the Marbella guide under the label
      // "Elviria" is naming the sub-area it covers, not renaming the guide.
      if (!NAV_DESTINATIONS.has(href.replace(/^(?:\.\.\/)+/, '').replace(/^[a-z]{2}\//, ''))) continue;
      const target = href.replace(/^(?:\.\.\/)+/, '').replace(/^[a-z]{2}\//, '');
      // Compare the words, not the encoding: "Benahavís" and "Benahav&iacute;s"
      // are the same label written two ways and must not read as a conflict.
      const text = label.replace(/&amp;/g, '&').replace(/&iacute;/g, 'í')
        .replace(/&aacute;/g, 'á').replace(/&oacute;/g, 'ó').replace(/&uacute;/g, 'ú')
        .replace(/&eacute;/g, 'é').replace(/&ntilde;/g, 'ñ').replace(/&nbsp;/g, ' ')
        .replace(/\s+/g, ' ').trim();
      if (!text) continue;
      navLabelsChecked += 1;
      const key = `${locale}|${target}`;
      if (!navLabels.has(key)) navLabels.set(key, new Map());
      const seen = navLabels.get(key);
      if (!seen.has(text)) seen.set(text, relative);
    }
  }
}

for (const [key, seen] of navLabels) {
  if (seen.size < 2) continue;
  const [locale, target] = key.split('|');
  const shown = [...seen].map(([label, where]) => `"${label}" (${where})`).join(', ');
  fail(target, `is linked from nav or footer under ${seen.size} different names in `
    + `locale "${locale}": ${shown} -- pick one and translate it from a single key`);
}

// Every page in the sitemap must be reachable from the homepage.
//
// The seven segment pages -- the ones built specifically to catch search
// demand -- were linked from area pages and guides, but from no homepage, not
// from developments.html and not from areas.html. Search Console showed the
// result: three of them discovered but never crawled, and the Norwegian one
// reported as "URL is unknown to Google". Nothing was broken. The pages
// rendered, sat in the sitemap and simply were not found.
//
// A sitemap entry is a claim that a page matters. If nothing on the site
// links to it, the claim is not backed by the site's own structure.
const MAX_CLICK_DEPTH = 3;
let reachabilityChecked = 0;

function localLinkTargets(html, fromRelative) {
  // Locale pages carry <base href="../">, so a relative href resolves against
  // the site root, not the page's own folder. Resolving against the folder
  // turns "sv/about.html" into "sv/sv/about.html" -- a dead end that makes
  // every locale page look reachable when it is not, or unreachable when it
  // is. Read the base the page actually declares.
  const base = /<base[^>]+href="([^"]*)"/.exec(html)?.[1];
  const pageDir = path.posix.dirname(fromRelative) === '.' ? '' : `${path.posix.dirname(fromRelative)}/`;
  const dir = base ? path.posix.normalize(`${pageDir}${base}`).replace(/^\.\/?$/, '') : pageDir;
  const out = new Set();
  for (const [, href] of html.matchAll(/<a[^>]+href="([^"#?]+\.html)(?:[#?][^"]*)?"/g)) {
    const resolved = href.startsWith('/')
      ? href.slice(1)
      : path.posix.normalize(`${dir}${dir && !dir.endsWith('/') ? '/' : ''}${href}`);
    if (!resolved.startsWith('..')) out.add(resolved);
  }
  return out;
}

{
  const sitemapPath = path.join(dist, 'sitemap.xml');
  if (fs.existsSync(sitemapPath)) {
    const sitemap = fs.readFileSync(sitemapPath, 'utf8');
    const submitted = new Set(
      [...sitemap.matchAll(/<loc>https:\/\/nuevaliving\.com\/([^<]*)<\/loc>/g)]
        .map(([, p]) => (p === '' || p.endsWith('/') ? `${p}index.html` : p))
    );

    const depth = new Map([['index.html', 0]]);
    let frontier = ['index.html'];
    while (frontier.length) {
      const next = [];
      for (const page of frontier) {
        const file = path.join(dist, page);
        if (!fs.existsSync(file)) continue;
        for (const target of localLinkTargets(fs.readFileSync(file, 'utf8'), page)) {
          if (depth.has(target)) continue;
          depth.set(target, depth.get(page) + 1);
          next.push(target);
        }
      }
      frontier = next;
    }

    const unreachable = [];
    const tooDeep = [];
    for (const page of submitted) {
      reachabilityChecked += 1;
      const d = depth.get(page);
      if (d === undefined) unreachable.push(page);
      else if (d > MAX_CLICK_DEPTH) tooDeep.push(`${page} (${d} clicks)`);
    }
    if (unreachable.length) {
      fail('sitemap.xml', `${unreachable.length} submitted page(s) cannot be reached from the `
        + `homepage by following links at all: ${unreachable.slice(0, 6).join(', ')}`
        + `${unreachable.length > 6 ? ', …' : ''}`);
    }
    if (tooDeep.length) {
      fail('sitemap.xml', `${tooDeep.length} submitted page(s) sit more than ${MAX_CLICK_DEPTH} `
        + `clicks from the homepage: ${tooDeep.slice(0, 6).join(', ')}`
        + `${tooDeep.length > 6 ? ', …' : ''}`);
    }
  }
}

const projectNames = new Set();
{
  const projectsDir = path.join(root, 'content', 'liora-projects');
  if (fs.existsSync(projectsDir)) {
    for (const entry of fs.readdirSync(projectsDir, { withFileTypes: true })) {
      if (!entry.isDirectory()) continue;
      const projectFile = path.join(projectsDir, entry.name, 'project.json');
      if (!fs.existsSync(projectFile)) continue;
      const name = JSON.parse(fs.readFileSync(projectFile, 'utf8')).name;
      if (name) projectNames.add(name);
    }
  }
}

// User-visible text living in attributes, not between tags.
//
// Every earlier check here read text nodes, so placeholder, aria-label and
// title were invisible to all of them. The referrals form asked "Who are you
// introducing?" in English under a Swedish label, and 1,601 gallery buttons
// carried English aria-labels on nine locales -- none of it caught, because
// none of it is text on the page.
//
// A value that is byte-identical to the English page's is either untranslated
// or a proper noun. Proper nouns are the exception, so they are named.
const ATTR_LOCALES = ['es', 'fr', 'de', 'ru', 'ar', 'nl', 'pl', 'sv', 'no'];
// alt joined this list last: 2,258 image descriptions were still English on
// locale pages, spoken by screen readers and indexed by image search.
const TRANSLATABLE_ATTRS = ['placeholder', 'aria-label', 'title', 'alt'];
const ATTR_ALLOWED = /Nueva Living|Costa del Sol|you@email\.com|^\+34|WhatsApp|Instagram|Facebook|^https?:/;
let localeAttributesChecked = 0;

{
  const properNouns = new Set(['Sasan Raftari', 'Sami Altun']);
  for (const file of everyHtmlFile(dist)) {
    const relative = path.relative(dist, file);
    if (!/^[a-z]{2}\//.test(relative)) continue;
    const locale = relative.slice(0, 2);
    if (!ATTR_LOCALES.includes(locale)) continue;
    const twin = path.join(dist, relative.slice(3));
    if (!fs.existsSync(twin)) continue;
    const localeHtml = fs.readFileSync(file, 'utf8');
    const englishHtml = fs.readFileSync(twin, 'utf8');
    for (const attribute of TRANSLATABLE_ATTRS) {
      const pattern = new RegExp(`${attribute}="([^"]{6,90})"`, 'g');
      const english = new Set([...englishHtml.matchAll(pattern)].map(([, v]) => v));
      for (const [, value] of localeHtml.matchAll(pattern)) {
        if (!english.has(value)) continue;
        if (ATTR_ALLOWED.test(value) || properNouns.has(value)) continue;
        // Two or more words of Latin script is the signal for a sentence
        // rather than a name; single words and project names pass.
        if (!/[A-Za-z]{2,}\s+[A-Za-z]{2,}/.test(value)) continue;
        if (projectNames.has(value)) continue;
        localeAttributesChecked += 1;
        fail(relative, `${attribute}="${value}" is identical to the English page -- `
          + 'attribute text is never checked by the text-node passes above, so an '
          + 'untranslated one has no visible symptom');
      }
    }
  }
}

// The breadcrumb bar's offset must come from --nueva-header-h, never a number.
//
// It was written out three times -- 76px in the base rule, 66px under 640px,
// and var(--nueva-header-h) above 1121px -- while the fixed header is 59px
// tall below 1121px and 89px above it. Only the desktop pair matched, so the
// page background showed through between header and breadcrumb as a 17px
// strip on tablets and a 7px one on phones. Nothing was broken; two numbers
// that had to agree simply were not the same number.
let breadcrumbOffsetsChecked = 0;

for (const name of ['liora-pages.css', 'nueva-system.css']) {
  const file = path.join(root, 'assets', 'liora', name);
  if (!fs.existsSync(file)) continue;
  const css = fs.readFileSync(file, 'utf8');
  for (const [, body] of css.matchAll(/\.breadcrumb-bar\s*\{([^}]*)\}/g)) {
    const offset = /margin-top\s*:\s*([^;]+);/.exec(body);
    if (!offset) continue;
    breadcrumbOffsetsChecked += 1;
    if (!offset[1].includes('--nueva-header-h')) {
      fail(`assets/liora/${name}`, `.breadcrumb-bar sets margin-top: ${offset[1].trim()} -- `
        + 'it must read var(--nueva-header-h) so the offset cannot drift away from the '
        + 'height of the fixed header it is clearing');
    }
  }
}

// The Guides toggle is a <summary> and inherits nothing from `.mobile-menu a`,
// so its row height has to be stated with the links or it collapses to the
// line box: 22.8px on the homepage, 16px everywhere else. Both break WCAG
// 2.5.8's 24x24 target and both break the drawer's rhythm -- the row reads as
// a tighter gap rather than as a smaller button, which is how it was reported.
//
// The links' own 44px lived in the homepage's inline <style>, so every other
// page type had rows sized by line-height alone. It belongs in the shared
// sheet, and the two selectors belong in one rule so neither can drift.
let drawerRowHeights = 0;

{
  const file = path.join(root, 'assets', 'liora', 'nueva-system.css');
  if (fs.existsSync(file)) {
    // Strip comments first: the selector capture below reaches back to the
    // previous rule, so a comment above the rule lands inside it.
    const css = fs.readFileSync(file, 'utf8').replace(/\/\*[\s\S]*?\*\//g, '');
    const heights = new Map();
    for (const [, selectors, body] of css.matchAll(/([^{}]+)\{([^}]*)\}/g)) {
      const declared = /min-height\s*:\s*([^;]+);/.exec(body);
      if (!declared) continue;
      for (const selector of selectors.split(',').map((s2) => s2.trim())) {
        if (selector === '.mobile-menu a' || selector === '.mobile-menu .nav-dropdown-toggle') {
          heights.set(selector, declared[1].trim());
        }
      }
    }
    drawerRowHeights = heights.size;
    const link = heights.get('.mobile-menu a');
    const toggle = heights.get('.mobile-menu .nav-dropdown-toggle');
    if (!link || !toggle) {
      fail('assets/liora/nueva-system.css', 'the drawer row height is missing for '
        + `${!link ? '.mobile-menu a' : '.mobile-menu .nav-dropdown-toggle'} -- without it the `
        + 'row collapses to its line box, under the 24px WCAG 2.5.8 target');
    } else if (link !== toggle) {
      fail('assets/liora/nueva-system.css', `.mobile-menu a is ${link} tall but the Guides `
        + `toggle is ${toggle} -- the drawer's rhythm breaks at that row`);
    }
  }
}

if (warnings.length) {
  console.warn(`Consistency warnings (${warnings.length}):`);
  warnings.forEach((message) => console.warn(`- ${message}`));
}

if (failures.length) {
  console.error(`Consistency audit failed (${failures.length}):`);
  failures.forEach((message) => console.error(`- ${message}`));
  process.exitCode = 1;
} else {
  console.log(`Consistency audit passed: ${htmlFiles.length} HTML pages checked, `
    + `${heroTitlesChecked} hero titles measured against their font-size cap, `
    + `${leadFormsChecked} CRM lead forms checked for a honeypot, `
    + `${schemaRefsChecked} schema @id references resolved, `
    + `${guidesChecked} guides checked for a named author, `
    + `${a11yPagesChecked} pages checked for skip link and labelled controls, `
    + `${internalLinksScanned} internal query-string links scanned, `
    + `${localeTitlesChecked} titles measured in every locale, `
    + `${selfUrlsChecked} canonical URLs checked for host and scheme, `
    + `${navLabelsChecked} nav and footer labels checked for one name per destination, `
    + `${reachabilityChecked} submitted pages checked for reachability from the homepage, `
    + `locale attribute text checked for untranslated values, `
    + `${breadcrumbOffsetsChecked} breadcrumb offsets checked against the header height, `
    + `${drawerRowHeights} drawer row heights checked for one target size.`);
}
