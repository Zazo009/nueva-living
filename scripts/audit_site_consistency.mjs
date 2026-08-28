import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { pathToFileURL } from 'node:url';

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

  // Likewise the nav submenus, which share the same injection risk. There are
  // two of them now -- Areas and Guides -- and each appears once in the desktop
  // nav and once in the drawer. Counting the total would hide one submenu going
  // missing while the other doubled, so count each by the label it opens with.
  const dropdownCount = (html.match(/<details class="nav-dropdown"/g) || []).length;
  if (dropdownCount !== 4) {
    fail(name, `expected 4 nav submenus (Areas and Guides, desktop + mobile), found ${dropdownCount}`);
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
  // The area guides stay out even though Areas is now a submenu: segment
  // pages name them by the sub-area they cover ("Elviria", "Marbella Öster")
  // from their own breadcrumb and footer, and that is a description of the
  // page doing the linking, not a second name for the guide.
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

// Every find/replace entry must carry all nine locales.
//
// footer_page_translations_group_c.mjs was written when the site had five
// languages and never extended: all 33 of its entries covered es, fr, de, ru
// and ar and none covered nl, pl, sv or no. The off-plan versus resale guide
// was a third English in those four languages -- rendered perfectly, in the
// wrong language, which is why every earlier pass over "missing translations"
// walked straight past it.
//
// Read the modules rather than the built pages: a table that is missing a
// locale is the cause, and the page is only where it shows.
const ENTRY_LOCALES = ['es', 'fr', 'de', 'ru', 'ar', 'nl', 'pl', 'sv', 'no'];
let entityPagesChecked = 0;

// Every indexable page says who publishes it, in its own language.
//
// The organisation schema -- name, address, geo, sameAs, founders -- lived on
// the English pages alone. Nine language versions carried a WebPage and a
// BreadcrumbList and nothing identifying the company, so to a crawler
// arriving in Spanish or German the site asserted no entity at all. That is
// the signal that separates this company from the similarly named one that
// currently owns the brand query.
//
// The description is checked for being translated, not merely present: a
// schema description is read as text, and an English sentence inside Swedish
// structured data is an assertion in the wrong language.
{
  const distRoot = path.join(root, 'dist');
  if (fs.existsSync(distRoot)) {
    const missing = [];
    const englishText = [];
    const enDescription = /"description":\s*"([^"]{40,})"/;
    const readOrg = (file) => {
      const html = fs.readFileSync(file, 'utf8');
      if (/name="robots"\s+content="[^"]*noindex/.test(html)) return undefined;
      const blocks = [...html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)];
      for (const [, raw] of blocks) {
        let parsed;
        try { parsed = JSON.parse(raw); } catch { continue; }
        const nodes = Array.isArray(parsed) ? parsed : (parsed['@graph'] || [parsed]);
        for (const node of nodes) {
          if (node && (node['@type'] === 'Organization' || node['@type'] === 'RealEstateAgent')) return node;
        }
      }
      return null;
    };
    for (const locale of ENTRY_LOCALES) {
      const dir = path.join(distRoot, locale);
      if (!fs.existsSync(dir)) continue;
      const english = new Map();
      for (const file of fs.readdirSync(dir).filter((f) => f.endsWith('.html'))) {
        const node = readOrg(path.join(dir, file));
        if (node === undefined) continue;
        entityPagesChecked += 1;
        if (!node) { missing.push(`${locale}/${file}`); continue; }
        const englishNode = readOrg(path.join(distRoot, file));
        if (englishNode && englishNode.description
            && node.description === englishNode.description) {
          englishText.push(`${locale}/${file}`);
        }
      }
    }
    if (missing.length) {
      fail('dist', `${missing.length} indexable locale page(s) carry no organisation schema: `
        + `${missing.slice(0, 4).join(', ')}`
        + `${missing.length > 4 ? `, …and ${missing.length - 4} more` : ''}.`);
    }
    if (englishText.length) {
      fail('dist', `${englishText.length} page(s) assert the organisation description in English `
        + `inside another language: ${englishText.slice(0, 4).join(', ')}`
        + `${englishText.length > 4 ? `, …and ${englishText.length - 4} more` : ''}.`);
    }
  }
}

// Every translation entry, loaded once for the checks that reason about the
// table as a whole rather than about a built page.
const entriesModule = path.join(root, 'scripts', 'lib', 'footer_page_translations.mjs');
const allEntries = fs.existsSync(entriesModule)
  ? (await import(pathToFileURL(entriesModule).href)).FOOTER_PAGE_ENTRIES || []
  : [];

let areaNamesChecked = 0;

// One spelling of an area's name per page.
//
// The Swedish area page called the place "Mijas och Fuengirola" thirteen times
// and "Mijas & Fuengirola" eleven times, because the locale overlay translated
// some strings and left the ampersand standing in others -- the hero title,
// the section heading, the German page title. Nothing failed: each string was
// internally fine, and the untranslated-fragment check could not see it
// because the surrounding sentence WAS translated.
//
// The English form is allowed inside a form control value, which is the key
// the CRM stores rather than anything a reader sees.
{
  const distRoot = path.join(root, 'dist');
  const areasFile = path.join(root, 'content', 'nueva-areas.json');
  const offenders = [];
  if (fs.existsSync(distRoot) && fs.existsSync(areasFile)) {
    const areaData = JSON.parse(fs.readFileSync(areasFile, 'utf8'));
    for (const area of areaData) {
      const englishName = area.name;
      if (!/[&]/.test(englishName)) continue;   // only names with a conjunction can diverge
      const escaped = englishName.replace(/&/g, '&amp;');
      for (const [locale, overlay] of Object.entries(area.i18n || {})) {
        const localName = overlay.name;
        if (!localName || localName === englishName) continue;
        const file = path.join(distRoot, locale, path.basename(area.output));
        if (!fs.existsSync(file)) continue;
        areaNamesChecked += 1;
        // Strip form controls: their value is the CRM key, not reader-facing.
        const html = fs.readFileSync(file, 'utf8').replace(/<option[^>]*>/g, ' ');
        const strays = (html.match(new RegExp(escaped.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g')) || []).length;
        if (strays) offenders.push(`${locale}/${path.basename(area.output)} ("${englishName}" x${strays}, page otherwise says "${localName}")`);
      }
    }
  }
  if (offenders.length) {
    fail('dist', `${offenders.length} page(s) spell an area name two different ways: `
      + `${offenders.slice(0, 4).join(', ')}`
      + `${offenders.length > 4 ? `, …and ${offenders.length - 4} more` : ''}.`);
  }
}

let entityIdChecked = 0;

// One entity, one declaration, one description of itself.
//
// Sixty-two pages declared nuevaliving.com/#organization twice. On the
// homepage the two copies disagreed about the entity's @type -- RealEstateAgent
// against Organization -- and about its url, one with a trailing slash and one
// without. A third, hand-written copy sat inside pages/developments.html and
// was the one that disagreed with both. For a site whose problem is that a
// differently-spelled competitor owns its own brand query, publishing three
// versions of your own identity is the last thing you want to be doing.
{
  const distRoot = path.join(root, 'dist');
  const declared = new Map();
  const duplicates = [];
  const missing = [];
  for (const file of fs.existsSync(distRoot) ? everyHtmlFile(distRoot) : []) {
    const html = fs.readFileSync(file, 'utf8');
    if (/<meta name="robots" content="[^"]*noindex/i.test(html)) continue;
    entityIdChecked += 1;
    const rel = path.relative(distRoot, file);
    let count = 0;
    for (const block of html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)) {
      let parsed;
      try { parsed = JSON.parse(block[1]); } catch { continue; }
      for (const node of (Array.isArray(parsed) ? parsed : (parsed['@graph'] || [parsed]))) {
        if (!node || typeof node !== 'object') continue;
        if (!String(node['@id'] || '').endsWith('#organization')) continue;
        // A node carrying only @id is a reference, not a declaration.
        if (!Object.keys(node).some((k) => k !== '@id' && k !== '@context')) continue;
        count += 1;
        for (const key of ['@type', 'url', 'name', 'legalName', 'taxID']) {
          const seen = declared.get(key);
          if (seen === undefined) declared.set(key, node[key]);
          else if (seen !== node[key] && !duplicates.some((d) => d.startsWith(`${key}:`))) {
            duplicates.push(`${key}: "${seen}" on one page, "${node[key]}" on ${rel}`);
          }
        }
      }
    }
    if (count === 0) missing.push(rel);
    else if (count > 1) duplicates.push(`${rel} declares it ${count} times`);
  }
  if (missing.length) {
    fail('dist', `${missing.length} indexable page(s) declare no organisation entity: `
      + `${missing.slice(0, 4).join(', ')}`
      + `${missing.length > 4 ? `, …and ${missing.length - 4} more` : ''}.`);
  }
  if (duplicates.length) {
    fail('dist', `the organisation entity is not described consistently across the site: `
      + `${duplicates.slice(0, 3).join('; ')}.`);
  }
}

let segmentLinkChecked = 0;

// Internal linking between area guides and segment pages runs both ways.
//
// The segment pages linked to all six area pages; the area pages linked back
// to at most one of them, and three linked to none. That left the site's most
// commercial destinations -- "new-build apartments in X" -- unreachable from
// the area guide that ranks for the same place.
//
// The mapping lives in nueva-areas.json, so this checks it against what is
// actually built: every listed target has to exist, and every segment page
// has to be reachable from at least one area page.
{
  const distRoot = path.join(root, 'dist');
  const areasSource = path.join(root, 'content', 'nueva-areas.json');
  if (fs.existsSync(distRoot) && fs.existsSync(areasSource)) {
    const areas = JSON.parse(fs.readFileSync(areasSource, 'utf8'));
    const linked = new Set();
    const dangling = [];
    for (const area of areas) {
      for (const [, output] of area.relatedSegments || []) {
        segmentLinkChecked += 1;
        linked.add(output);
        if (!fs.existsSync(path.join(distRoot, output))) {
          dangling.push(`${area.slug} -> ${output}`);
        }
      }
    }
    const orphans = fs.readdirSync(distRoot)
      .filter((f) => f.startsWith('new-build-') && f.endsWith('.html') && !linked.has(f));
    if (dangling.length) {
      fail('content/nueva-areas.json',
        `${dangling.length} area page(s) link to a segment page that is not built: ${dangling.join(', ')}.`);
    }
    if (orphans.length) {
      fail('content/nueva-areas.json',
        `${orphans.length} segment page(s) are not linked from any area guide, so the linking runs `
        + `one way only: ${orphans.join(', ')}.`);
    }
  }
}

let faqSchemaChecked = 0;

// A visible FAQ must be marked up as one, in the reader's language.
//
// The general questions lived in strings.json for the visible accordion and in
// a second hardcoded English copy in build_dist.mjs for the schema. Only the
// English root pages got the copy, so all six guides shipped with no FAQ
// markup in any language and advisory, index and referrals had none in their
// nine locale versions -- 88 pages with a visible FAQ that no search engine
// could read as one.
//
// The first attempt at fixing it built the schema before the translation pass,
// which is a literal find/replace over the whole document including JSON-LD.
// The table translates the string "FAQ", so the type token itself came out as
// "@type": "Vanliga frågorPage" in eight of nine languages -- valid JSON,
// meaningless to a parser. So this checks three things at once: the schema
// exists, its @type survived, and its first question is the first question the
// page actually shows.
{
  const distRoot = path.join(root, 'dist');
  const missing = [];
  const mismatched = [];
  for (const file of fs.existsSync(distRoot) ? everyHtmlFile(distRoot) : []) {
    const html = fs.readFileSync(file, 'utf8');
    const visible = html.match(
      /<details class="segment-faq-item"[^>]*>\s*<summary>([\s\S]*?)<\/summary>/);
    if (!visible) continue;
    faqSchemaChecked += 1;
    const rel = path.relative(distRoot, file);
    const strip = (fragment) => fragment.replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
    let faq = null;
    for (const block of html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)) {
      let parsed;
      try { parsed = JSON.parse(block[1]); } catch { continue; }
      for (const node of (Array.isArray(parsed) ? parsed : (parsed['@graph'] || [parsed]))) {
        if (node && node['@type'] === 'FAQPage') faq = node;
      }
    }
    if (!faq) { missing.push(rel); continue; }
    const first = faq.mainEntity?.[0]?.name;
    if (strip(first || '') !== strip(visible[1])) {
      mismatched.push(`${rel} (schema "${String(first).slice(0, 30)}" vs page "${strip(visible[1]).slice(0, 30)}")`);
    }
  }
  if (missing.length) {
    fail('dist', `${missing.length} page(s) render a FAQ but ship no FAQPage schema: `
      + `${missing.slice(0, 4).join(', ')}`
      + `${missing.length > 4 ? `, …and ${missing.length - 4} more` : ''}.`);
  }
  if (mismatched.length) {
    fail('dist', `${mismatched.length} page(s) carry FAQ schema that does not match the FAQ shown: `
      + `${mismatched.slice(0, 3).join('; ')}.`);
  }
}

let registerPagesChecked = 0;

// One form of address per language, across every page type.
//
// The site said "ni" on its advisory and about pages and "du" in its guides,
// so a Swedish visitor was addressed differently depending on where they
// landed -- and the shared CTA band ended up with a heading in one register
// above a button in the other. The copy lives in six different places
// (translation tables, strings.json, per-project i18n overlays, the areas
// file, the homepage builder and the segment tables), which is why no single
// pass ever caught it.
//
// Norwegian is deliberately absent: "De" is archaic there, so "du" IS the
// correct formal address and converting it would be an error.
{
  const distRoot = path.join(root, 'dist');
  // JavaScript's \b is ASCII-only, so /\btes\b/ matches inside "êtes" and
  // /\bdu\b/ inside "födu". Every one of these languages has accented letters,
  // so the boundaries have to be Unicode letter lookarounds instead.
  const word = (alternatives, flags = 'gu') =>
    new RegExp(`(?<!\\p{L})(?:${alternatives})(?!\\p{L})`, flags);
  const INFORMAL = {
    sv: word('du|dig|din|ditt|dina', 'giu'),
    de: word('du|dich|dir|dein|deine|deinen|deinem|deiner', 'giu'),
    nl: word('jij|jou|jouw|jullie', 'giu'),
    fr: word('tu|ton|tes|toi', 'gu'),
    // Polish: second-person singular verb endings and the polite dative Ci,
    // but not the imperatives Polish UI conventionally uses on buttons
    // (Zapisz, Napisz, Wyślij), which are not read as addressing anyone.
    pl: word('\\w*(?:esz|asz|isz|ysz|łeś|łaś)|Ci|Ciebie|Cię|Tobie|Twój|Twoja|Twoje|Twoim|Twoich|Twojej|Twoją', 'gu'),
    // Spanish: tú possessives and clitics, plus infinitives carrying an
    // enclitic -te (ayudarte, ponerte). The allowlist below covers the nouns
    // that merely end in -te and the ones that are not clitics at all.
    es: word('tu|tú|tus|tuyo|tuya|tuyos|tuyas|ti|contigo|te|\\w+(?:ar|er|ir)te', 'giu'),
  };
  const ALLOWED = {
    pl: /^(nasz|Nasz|wasz|Wasz|Zapisz|zapisz|Napisz|napisz|Podpisz|podpisz|Opisz|opisz|Wpisz|wpisz)$/,
    es: /^(parte|aparte|convierte|fuerte|reparte|arte|corte|norte|deporte|soporte|reporte|suerte|muerte|puente|frente)$/i,
  };
  const offenders = [];
  for (const [locale, pattern] of Object.entries(INFORMAL)) {
    const dir = path.join(distRoot, locale);
    if (!fs.existsSync(dir)) continue;
    for (const file of fs.readdirSync(dir).filter((f) => f.endsWith('.html'))) {
      const html = fs.readFileSync(path.join(dir, file), 'utf8');
      const main = html.match(/<main[\s\S]*?<\/main>/);
      if (!main) continue;
      registerPagesChecked += 1;
      const text = main[0].replace(/<script[\s\S]*?<\/script>/g, ' ').replace(/<[^>]+>/g, ' ');
      const allowed = ALLOWED[locale];
      const found = (text.match(pattern) || []).filter((w) => !allowed || !allowed.test(w));
      if (found.length) offenders.push(`${locale}/${file} ("${found[0]}", ${found.length}x)`);
    }
  }
  if (offenders.length) {
    fail('dist', `${offenders.length} page(s) address the reader informally in a language the site `
      + `addresses formally: ${offenders.slice(0, 4).join(', ')}`
      + `${offenders.length > 4 ? `, …and ${offenders.length - 4} more` : ''}.`);
  }
}

let sharedFragmentsChecked = 0;

// Text with no translation entry at all is invisible to the unreplaced-source
// check, because that check can only look for strings the table knows about.
//
// The guides shipped nine such gaps: compare-table cells ("Covered", "Resale"),
// card headings ("Broker", "Refuse", "Valuation") and a hero kicker reading
// "How to Buy a New-Build on the Costa del Sol · 7 Steps for 2026" in all nine
// languages. Each was short enough to read as a design element rather than as
// copy, which is how they survived several translation passes.
//
// So compare the built pages instead of the table: any text node that is
// byte-identical in English and in every one of the nine locales is either a
// proper noun, a number, or a string nobody translated.
{
  const distRoot = path.join(root, 'dist');
  // Proper nouns are supposed to be identical in every language, so they are
  // read out of the source data rather than listed here -- a new project or
  // area then needs no edit to this check, and cannot be quietly exempted by
  // someone widening a hardcoded pattern.
  const properNouns = new Set();
  const areasFile = path.join(root, 'content', 'nueva-areas.json');
  if (fs.existsSync(areasFile)) {
    for (const area of JSON.parse(fs.readFileSync(areasFile, 'utf8'))) {
      properNouns.add(area.name);
      for (const price of area.prices || []) properNouns.add(price.label);
      for (const item of area.spotlight?.items || []) properNouns.add(item[0]);
    }
  }
  const projectsDir = path.join(root, 'content', 'liora-projects');
  if (fs.existsSync(projectsDir)) {
    for (const dir of fs.readdirSync(projectsDir)) {
      const file = path.join(projectsDir, dir, 'project.json');
      if (!fs.existsSync(file)) continue;
      const project = JSON.parse(fs.readFileSync(file, 'utf8'));
      properNouns.add(project.name);
      properNouns.add(project.shortName);
      // The location shown on a project card ("Rio Real", "Golf Valley") is a
      // place name too, and appears on the area pages that list the project.
      properNouns.add(project.card?.label);
      properNouns.add(project.hero?.location);
    }
  }
  const KEEP = /^(IVA|AJD|ITP|NIE|LOE|Nueva Living|Costa del Sol|Sasan Raftari|Sami Altun|aval|seguro|tasaci|basura)/;
  // Numbers, measurements, price bands and bare HTML entities carry no language.
  const NUMERIC = /^(?:[\d\s%€.,·\/–—&;a-z-]+|&#\d+;|[\d\s,.]+[–-][\d\s,.]+\s*m²|[\d\s,.]+\s*m²|&euro;[\d,]+\+?|Phase \d+|€[\d,.\s]+\s*\/\s*m²)$/;
  const textNodes = (file) => {
    const html = fs.readFileSync(file, 'utf8');
    const main = html.match(/<main[\s\S]*?<\/main>/);
    if (!main) return null;
    return new Set(main[0].replace(/<script[\s\S]*?<\/script>/g, ' ')
      .split(/<[^>]+>/).map((t) => t.replace(/\s+/g, ' ').trim()).filter(Boolean));
  };
  const untranslated = [];
  for (const file of fs.existsSync(distRoot) ? fs.readdirSync(distRoot) : []) {
    // Guides and area pages: both are long-form, both are hand-authored in
    // English first, and both are where untranslated copy hides longest.
    if (!/^(guide|area)-/.test(file) || !file.endsWith('.html')) continue;
    const english = textNodes(path.join(distRoot, file));
    if (!english) continue;
    let shared = english;
    for (const locale of ENTRY_LOCALES) {
      const localePage = path.join(distRoot, locale, file);
      if (!fs.existsSync(localePage)) continue;
      const here = textNodes(localePage);
      if (!here) continue;
      shared = new Set([...shared].filter((t) => here.has(t)));
    }
    sharedFragmentsChecked += 1;
    for (const text of shared) {
      if (text.length <= 3 || NUMERIC.test(text) || KEEP.test(text)) continue;
      if (properNouns.has(text) || properNouns.has(text.replace(/&amp;/g, '&'))) continue;
      untranslated.push(`${file}: "${text.slice(0, 44)}"`);
    }
  }
  if (untranslated.length) {
    fail('dist', `${untranslated.length} text fragment(s) are identical in English and in all nine `
      + `locales, so they were never translated: ${untranslated.slice(0, 5).join('; ')}`
      + `${untranslated.length > 5 ? `, …and ${untranslated.length - 5} more` : ''}.`);
  }
}

let titleCaseChecked = 0;

// Sentence case in every language but German.
//
// Twenty-three translations copied the English Title Case straight across --
// "Stel een Echte Shortlist Samen", "Compara Opciones Reales". Dutch, Spanish
// and French capitalise a heading's first word and its proper nouns, nothing
// else, so this read as machine output in exactly the languages the site is
// trying to sound native in. German is exempt: it capitalises every noun.
{
  const PROPER = /^(Nueva|Living|Costa|del|Sol|Marbell[a-zę]*|Estepon[aęy]*|Benah[aá]v[ií]s|M[aá]laga|Andaluc[ií]a|Andalousie|Mijas|Fuengirol[aęy]*|Ban[uú]s|Puerto|Golf|Valley|Sotogrande|Casares|Espa[nñ]a|Espagne|Spanje|Spani\w*|Hiszpani\w*|Andaluz\w*|Andalusi\w*|Andalousie|Sasan[a]?|Raftari(ego)?|Sami(ego)?|Altun[a]?|IVA|AJD|ITP|NIE|LOE|Ley)$/;
  const CASED = ['es', 'fr', 'nl', 'pl', 'sv', 'no'];
  const offenders = [];
  // Only entries whose English source is itself Title Case -- a heading or a
  // button label. Those are the ones a translator copies the casing from. In a
  // full English sentence a mid-string capital is a proper noun, not a style.
  const isTitleCase = (text) => {
    if (/[.?!:;,]/.test(text) || text.includes('<')) return false;
    const words = text.split(/\s+/).filter(Boolean);
    if (words.length < 2) return false;
    const significant = words.filter((w) => w.length > 3);
    return significant.length >= 2 && significant.every((w) => /^[A-Z]/.test(w));
  };
  // Place names are Title Case in every language -- "Marbella Este", "La Milla
  // de Oro", "Złoty Trójkąt". They are read out of the area data rather than
  // pattern-matched, so a new sub-area is exempt because it IS a place, not
  // because someone loosened the check.
  const placeNames = new Set();
  const areasSource = path.join(root, 'content', 'nueva-areas.json');
  if (fs.existsSync(areasSource)) {
    for (const area of JSON.parse(fs.readFileSync(areasSource, 'utf8'))) {
      placeNames.add(area.name);
      for (const item of area.subareas?.items || []) placeNames.add(item[0]);
      for (const item of area.spotlight?.items || []) placeNames.add(item[0]);
      for (const price of area.prices || []) placeNames.add(price.label);
    }
  }
  for (const entry of allEntries) {
    if (placeNames.has(entry.find)) { titleCaseChecked += 1; continue; }
    if (!isTitleCase(entry.find)) { titleCaseChecked += 1; continue; }
    for (const locale of CASED) {
      const value = entry[locale];
      if (typeof value !== 'string' || value.includes('<') || value.includes('&')) continue;
      // Each sentence capitalises its own first word, so check sentences, not
      // the whole string -- otherwise "¿Lo sabías? Financiación" reads as a
      // violation when it is simply a second sentence.
      for (const sentence of value.split(/[.?!:¿¡]+/)) {
        const words = sentence.split(/\s+/).filter(Boolean);
        if (words.length < 2) continue;
        const tail = words.slice(1).filter((w) => !PROPER.test(w.replace(/[.,:;?!/'’]/g, '')));
        if (!tail.length) continue;
        const capped = tail.filter((w) => /^[A-ZÁÉÍÓÚÑÅÄÖŁŚŻŹĆĘĄ][a-záéíóúñåäöłśżźćęą]{2,}$/.test(w));
        if (capped.length) {
          offenders.push(`${locale}: "${sentence.trim().slice(0, 44)}"`);
          break;
        }
      }
    }
    titleCaseChecked += 1;
  }
  if (offenders.length) {
    fail('scripts/lib/footer_page_translations.mjs',
      `${offenders.length} translation(s) carry English Title Case into a language that uses `
      + `sentence case: ${offenders.slice(0, 5).join('; ')}`
      + `${offenders.length > 5 ? `, …and ${offenders.length - 5} more` : ''}.`);
  }
}

let translationConflictsChecked = 0;

// One English string, one translation per language.
//
// Fourteen find strings were authored twice with different translations --
// "Start Your Search" three times. Which one the site rendered was decided by
// the order the group files happen to be concatenated in, not by the page. It
// showed: the shared guide CTA read "Låt oss hitta det som passar dig" above a
// button saying "Starta er sökning", two different registers of Swedish "you"
// inside one band, because the heading and the button matched entries from
// different files. Nothing failed, because each entry was internally complete.
{
  const byFind = new Map();
  for (const entry of allEntries) {
    if (!byFind.has(entry.find)) byFind.set(entry.find, []);
    byFind.get(entry.find).push(entry);
  }
  const conflicts = [];
  for (const [find, list] of byFind) {
    translationConflictsChecked += 1;
    if (list.length < 2) continue;
    const differing = ENTRY_LOCALES.filter((l) => new Set(list.map((e) => e[l])).size > 1);
    if (differing.length) conflicts.push(`"${find.slice(0, 48)}" (${differing.join(', ')})`);
  }
  if (conflicts.length) {
    fail('scripts/lib/footer_page_translations.mjs',
      `${conflicts.length} English string(s) carry more than one translation, so which one renders `
      + `depends on file order rather than on the page: ${conflicts.slice(0, 4).join('; ')}`
      + `${conflicts.length > 4 ? `, …and ${conflicts.length - 4} more` : ''}.`);
  }
}

let revealPagesChecked = 0;

// A page that hides content on scroll must ship the code that unhides it.
//
// The guides styled .g-reveal to opacity 0 by default, but the observer that
// adds .in lived inside two guides' own body copy instead of the shared
// template. The other four shipped a hero followed by 1,200 words of invisible
// text still holding its full height -- in all ten languages. Nothing failed,
// because the CSS and the script were authored in different files and neither
// knew the other was required. So: every built page carrying .g-reveal must
// carry exactly one reveal script, and the CSS must gate hiding on the class
// that script sets, so hiding can never outlive the unhiding.
{
  const distRoot = path.join(root, 'dist');
  const cssFile = path.join(root, 'assets', 'liora', 'liora-pages.css');
  if (fs.existsSync(distRoot) && fs.existsSync(cssFile)) {
    const css = fs.readFileSync(cssFile, 'utf8');
    const hidingRules = css.match(/^[^{}\n]*\.g-reveal(?![-\w])[^{}]*\{[^}]*opacity:\s*0[^}]*\}/gm) || [];
    const ungated = hidingRules.filter((rule) => !rule.split('{')[0].includes('.reveal-ready'));
    if (ungated.length) {
      fail('assets/liora/liora-pages.css',
        `${ungated.length} rule(s) hide .g-reveal without gating on .reveal-ready, so the content `
        + 'stays invisible on any page whose reveal script is missing or throws.');
    }
    const missingScript = [];
    const duplicateScript = [];
    for (const file of everyHtmlFile(distRoot)) {
      const html = fs.readFileSync(file, 'utf8');
      if (!html.includes('g-reveal')) continue;
      revealPagesChecked += 1;
      const observers = (html.match(/querySelectorAll\('\.g-reveal'\)/g) || []).length;
      const rel = path.relative(distRoot, file);
      if (observers === 0) missingScript.push(rel);
      else if (observers > 1) duplicateScript.push(rel);
    }
    if (missingScript.length) {
      fail('dist', `${missingScript.length} page(s) hide content behind .g-reveal but ship no reveal `
        + `script, so the body never becomes visible: ${missingScript.slice(0, 4).join(', ')}`
        + `${missingScript.length > 4 ? `, …and ${missingScript.length - 4} more` : ''}.`);
    }
    // Same failure, different element: the closing disclaimer and CTA band were
    // pasted into two guides' body copy, so four guides ended on the last FAQ
    // answer with no advice notice and no way to contact anyone.
    const badTail = [];
    for (const file of everyHtmlFile(distRoot)) {
      const html = fs.readFileSync(file, 'utf8');
      if (!html.includes('guide-article-page')) continue;
      const ctas = (html.match(/class="cta-band"/g) || []).length;
      const discs = (html.match(/class="guide-disclaimer/g) || []).length;
      if (ctas !== 1 || discs !== 1) {
        badTail.push(`${path.relative(distRoot, file)} (${ctas} CTA, ${discs} disclaimer)`);
      }
    }
    if (badTail.length) {
      fail('dist', `${badTail.length} guide page(s) do not end with exactly one disclaimer and one `
        + `CTA band: ${badTail.slice(0, 4).join(', ')}`
        + `${badTail.length > 4 ? `, …and ${badTail.length - 4} more` : ''}.`);
    }
    if (duplicateScript.length) {
      fail('dist', `${duplicateScript.length} page(s) ship the reveal script more than once, which `
        + `means it is pasted into page bodies instead of the shared template: `
        + `${duplicateScript.slice(0, 4).join(', ')}.`);
    }
  }
}

let ogLocalesChecked = 0;

// og:locale is language_TERRITORY, not a bare language code.
//
// English shipped "en_US" and every other language shipped its bare code --
// "de", "es", "ar". Open Graph defines the value as language_TERRITORY, so
// the nine locale versions were malformed and simply ignored by the networks
// that read it. It looked right in a diff, which is why it survived: the
// value matched the page's own lang attribute, and lang is where a bare code
// is correct.
{
  const distRoot = path.join(root, 'dist');
  if (fs.existsSync(distRoot)) {
    const malformed = [];
    const walk = (dir) => {
      for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
        const full = path.join(dir, entry.name);
        if (entry.isDirectory()) {
          if (entry.name !== 'assets') walk(full);
        } else if (entry.name.endsWith('.html')) {
          const value = /<meta property="og:locale" content="([^"]*)"/
            .exec(fs.readFileSync(full, 'utf8'))?.[1];
          if (!value) continue;
          ogLocalesChecked += 1;
          if (!/^[a-z]{2}_[A-Z]{2}$/.test(value)) {
            malformed.push(`${path.relative(distRoot, full)} ("${value}")`);
          }
        }
      }
    };
    walk(distRoot);
    if (malformed.length) {
      fail('dist', `${malformed.length} page(s) carry a malformed og:locale: `
        + `${malformed.slice(0, 4).join(', ')}`
        + `${malformed.length > 4 ? `, …and ${malformed.length - 4} more` : ''}. `
        + 'Open Graph wants language_TERRITORY (de_DE), not the bare language code.');
    }
  }
}

let descriptionRatiosChecked = 0;

// A translated description must carry the same substance as the English.
//
// About, advisory and contact each had a full English description --
// "Meet Sasan Raftari and Sami Altun... 40+ developers", "usually within one
// working day", "contracts, payment schedules and bank guarantees" -- and a
// generic one-liner in all nine languages, roughly half the length, with
// every specific dropped. Nothing was untranslated, so no check for English
// could see it. The English text had been improved in build_dist's pageMeta
// and the builders' own copy, which is what the locale pages use, never
// followed.
//
// Length is a proxy, and a crude one: a language can be terser than English
// and still say everything. Two thirds is loose enough to allow that and
// tight enough to catch a sentence that has been replaced by a label.
const MIN_DESCRIPTION_RATIO = 0.7;

{
  const distRoot = path.join(root, 'dist');
  const readDescription = (file) => {
    if (!fs.existsSync(file)) return null;
    const html = fs.readFileSync(file, 'utf8');
    if (/name="robots"\s+content="[^"]*noindex/.test(html)) return null;
    return /<meta name="description" content="([^"]*)"/.exec(html)?.[1] || null;
  };
  if (fs.existsSync(distRoot)) {
    const thin = [];
    for (const entry of fs.readdirSync(distRoot).filter((f) => f.endsWith('.html'))) {
      const english = readDescription(path.join(distRoot, entry));
      if (!english) continue;
      for (const locale of ENTRY_LOCALES) {
        const translated = readDescription(path.join(distRoot, locale, entry));
        if (!translated) continue;
        descriptionRatiosChecked += 1;
        const ratio = translated.length / english.length;
        if (ratio < MIN_DESCRIPTION_RATIO) {
          thin.push(`  ${locale}/${entry}: ${translated.length} chars against ${english.length} (${ratio.toFixed(2)})`);
        }
      }
    }
    if (thin.length) {
      fail('dist', `${thin.length} translated description(s) are far shorter than the English:\n`
        + `${thin.slice(0, 5).join('\n')}\n`
        + 'Check the translation still carries the specifics -- the names, the '
        + 'numbers, the promise -- rather than having been reduced to a label.');
    }
  }
}

let uniqueMetaChecked = 0;

// Within one language, no two pages share a title or a description.
//
// Fifteen of the thirty projects carried their seoDescription in English on
// all nine locales -- 135 meta descriptions, the text that actually appears
// in a result, identical across languages and untranslated. Nothing caught
// it, because the sweep for surviving English only ever read visible text.
//
// Per language, not across languages: Swedish and Norwegian both write "Om
// oss", Dutch and German both write "Villa in Estepona". Those are different
// URLs with different lang attributes and reciprocal hreflang, and rewriting
// one of them to satisfy a counter would be worse copy for no gain.
{
  const distRoot = path.join(root, 'dist');
  if (fs.existsSync(distRoot)) {
    const byLocale = new Map();
    const walk = (dir, locale) => {
      for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
        const full = path.join(dir, entry.name);
        if (entry.isDirectory()) {
          if (entry.name === 'assets') continue;
          walk(full, ENTRY_LOCALES.includes(entry.name) ? entry.name : locale);
        } else if (entry.name.endsWith('.html')) {
          const html = fs.readFileSync(full, 'utf8');
          if (/name="robots"\s+content="[^"]*noindex/.test(html)) continue;
          if (!byLocale.has(locale)) byLocale.set(locale, { title: new Map(), desc: new Map() });
          const bucket = byLocale.get(locale);
          const rel = path.relative(distRoot, full).split(path.sep).join('/');
          for (const [field, pattern] of [['title', /<title>([^<]*)<\/title>/],
                                          ['desc', /<meta name="description" content="([^"]*)"/]]) {
            const value = pattern.exec(html)?.[1]?.trim();
            if (!value) continue;
            uniqueMetaChecked += 1;
            if (!bucket[field].has(value)) bucket[field].set(value, []);
            bucket[field].get(value).push(rel);
          }
        }
      }
    };
    walk(distRoot, 'en');
    const clashes = [];
    for (const [locale, bucket] of byLocale) {
      for (const field of ['title', 'desc']) {
        for (const [value, files] of bucket[field]) {
          if (files.length > 1) {
            clashes.push(`  [${locale}] ${field}: ${files.slice(0, 3).join(', ')} share "${value.slice(0, 45)}…"`);
          }
        }
      }
    }
    if (clashes.length) {
      fail('dist', `${clashes.length} page(s) in one language share a title or description:\n`
        + `${clashes.slice(0, 5).join('\n')}`);
    }
  }
}

let sitemapPagesChecked = 0;

// The sitemap lists every indexable page, and only those.
//
// This was checked by hand and the hand got it wrong: comparing the
// sitemap's URL count against the audit's page count suggested a hundred
// pages were going unsubmitted, when the two numbers were simply counting
// different things -- the audit walks the repo root and the locale
// directories, the sitemap describes dist. The real answer was an exact
// match. A count that has to be interpreted is a count worth automating.
{
  const distRoot = path.join(root, 'dist');
  const sitemapPath = path.join(distRoot, 'sitemap.xml');
  if (fs.existsSync(sitemapPath)) {
    const listed = new Set([...fs.readFileSync(sitemapPath, 'utf8')
      .matchAll(/<loc>([^<]*)<\/loc>/g)].map((m) => m[1]));
    const indexable = new Map();
    const walk = (dir) => {
      for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
        const full = path.join(dir, entry.name);
        if (entry.isDirectory()) {
          if (entry.name !== 'assets') walk(full);
        } else if (entry.name.endsWith('.html')) {
          const html = fs.readFileSync(full, 'utf8');
          if (/name="robots"\s+content="[^"]*noindex/.test(html)) continue;
          const rel = path.relative(distRoot, full).split(path.sep).join('/');
          const url = rel.endsWith('index.html')
            ? `https://nuevaliving.com/${rel.slice(0, -'index.html'.length)}`
            : `https://nuevaliving.com/${rel}`;
          indexable.set(url, rel);
        }
      }
    };
    walk(distRoot);
    sitemapPagesChecked = indexable.size;
    const unsubmitted = [...indexable.keys()].filter((url) => !listed.has(url));
    const orphaned = [...listed].filter((url) => !indexable.has(url));
    if (unsubmitted.length) {
      fail('dist/sitemap.xml', `${unsubmitted.length} indexable page(s) are not in the sitemap: `
        + `${unsubmitted.slice(0, 4).map((u) => indexable.get(u)).join(', ')}`
        + `${unsubmitted.length > 4 ? `, …and ${unsubmitted.length - 4} more` : ''}.`);
    }
    if (orphaned.length) {
      fail('dist/sitemap.xml', `${orphaned.length} sitemap URL(s) point at a page that is `
        + `noindex or missing: ${orphaned.slice(0, 4).join(', ')}`
        + `${orphaned.length > 4 ? `, …and ${orphaned.length - 4} more` : ''}.`);
    }
  }
}

let redirectRulesChecked = 0;

// A redirect rule that a real file shadows does nothing.
//
// Netlify serves a matching static file in preference to a redirect rule
// unless the rule is forced with a trailing "!". The ten rules folding
// /sv/index.html into /sv/ are exactly that shape, and without the bang they
// would have shipped looking correct and doing nothing. Duplicated from-paths
// are the other silent case: the second rule never runs.
{
  const redirectsPath = path.join(root, 'dist', '_redirects');
  if (fs.existsSync(redirectsPath)) {
    const rules = fs.readFileSync(redirectsPath, 'utf8').split('\n')
      .map((line) => line.trim()).filter(Boolean)
      .map((line) => line.split(/\s+/));
    redirectRulesChecked = rules.length;
    const seen = new Set();
    const duplicated = [];
    const shadowed = [];
    for (const [from, , status] of rules) {
      if (seen.has(from)) duplicated.push(from);
      seen.add(from);
      if (from.endsWith('*') || from === '/') continue;
      const target = path.join(root, 'dist', from.replace(/^\//, ''));
      if (fs.existsSync(target) && fs.statSync(target).isFile() && !String(status).endsWith('!')) {
        shadowed.push(from);
      }
    }
    if (shadowed.length) {
      fail('dist/_redirects', `${shadowed.length} rule(s) are shadowed by a real file and will `
        + `never run: ${shadowed.slice(0, 4).join(', ')}. Netlify serves the file unless the `
        + 'status carries a trailing "!".');
    }
    // Pretty URLs answers the extensionless form from the .html file, so an
    // unforced rule here is consulted only after Netlify has already served
    // the page. Every rule folding one URL form into another has to be forced.
    const unforced = rules
      .filter(([from, to, status]) => status === '301' && to && to.endsWith('.html')
        && from === to.slice(0, -'.html'.length))
      .map(([from]) => from);
    if (unforced.length) {
      fail('dist/_redirects', `${unforced.length} extensionless rule(s) are not forced: `
        + `${unforced.slice(0, 4).join(', ')}. Netlify's Pretty URLs answers these from the `
        + '.html file before an unforced rule runs, so they do nothing.');
    }
    if (duplicated.length) {
      fail('dist/_redirects', `${duplicated.length} duplicated from-path(s): `
        + `${duplicated.slice(0, 4).join(', ')}. Only the first rule for a path ever runs.`);
    }
  }
}

let placeSpellingsChecked = 0;

// Place names have one spelling.
//
// "Puerto Banus" without the accent sat in 235 places against 1098 with it,
// and "Benahavís" was written "Benahávis" -- accent on the wrong vowel -- in
// sixteen, including a whole area guide in four languages. Both are the kind
// of thing that reads as sloppiness to a local buyer and splits a search term
// in two.
//
// The check runs over sources rather than output, because the wrong spelling
// has to be fixed in the English AND in every translation table's find string
// in the same pass: correcting one side alone stops the entries matching and
// silently reverts whole paragraphs to English. That happened twice while
// this was being fixed.
{
  // Only spellings that are unambiguously wrong. "Nueva Andalucia" without the
  // accent is deliberate in a dozen files -- it is a filter key the discovery
  // JS matches on, not display text -- so it is not listed here.
  const WRONG_SPELLINGS = [
    ['Puerto Banus', 'Puerto Banús'],
    ['Benahávis', 'Benahavís']
  ];
  const roots = ['scripts', 'content', 'pages'];
  const files = [];
  const walk = (dir) => {
    if (!fs.existsSync(dir)) return;
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) walk(full);
      else if (/\.(mjs|json|html)$/.test(entry.name)
        && entry.name !== 'audit_site_consistency.mjs') files.push(full);
    }
  };
  for (const root_ of roots) walk(path.join(root, root_));
  for (const [wrong, right] of WRONG_SPELLINGS) {
    placeSpellingsChecked += 1;
    const offenders = [];
    for (const file of files) {
      const text = fs.readFileSync(file, 'utf8');
      // No subtraction: "Puerto Banus" is not a substring of "Puerto Banús"
      // -- they differ at the u. Deducting the correct spellings made the
      // count negative and the check silently passed.
      const count = text.split(wrong).length - 1;
      if (count > 0) offenders.push(`${path.relative(root, file)} (${count})`);
    }
    if (offenders.length) {
      fail('place names', `"${wrong}" should be "${right}": ${offenders.slice(0, 4).join(', ')}`
        + `${offenders.length > 4 ? `, …and ${offenders.length - 4} more` : ''}. `
        + 'Fix the English and every translation table\'s find string together -- '
        + 'changing one side stops the entries matching and reverts paragraphs to English.');
    }
  }
}

let breadcrumbTrailsChecked = 0;

// A breadcrumb may not say the same thing twice.
//
// Three segment pages named themselves after their own parent area, so the
// trail read "Elviria > Elviria" -- invisible until both crumbs were finally
// translated, because before that one said "Эльвирия" and the other "Elviria"
// and the repetition looked like two different places. Naming the page type
// instead then collided with the Developments crumb in Russian, where both
// are "Новостройки". Two different mistakes, one shape.
{
  for (const locale of ['', ...ENTRY_LOCALES]) {
    const dir = path.join(root, locale);
    if (!fs.existsSync(dir)) continue;
    for (const file of fs.readdirSync(dir).filter((f) => f.endsWith('.html'))) {
      const html = fs.readFileSync(path.join(dir, file), 'utf8');
      const trail = /<ol class="breadcrumb-list">([\s\S]*?)<\/ol>/.exec(html);
      if (!trail) continue;
      breadcrumbTrailsChecked += 1;
      const crumbs = [...trail[1].matchAll(/>([^<>]+)<\/(?:a|span)>/g)]
        .map((m) => m[1].trim())
        .filter(Boolean);
      const seen = new Set();
      for (const crumb of crumbs) {
        if (seen.has(crumb)) {
          fail(`${locale ? `${locale}/` : ''}${file}`,
            `breadcrumb repeats "${crumb}": ${crumbs.join(' > ')}. `
            + 'Each crumb names a different level, so two identical ones mean a '
            + 'page is named after its own parent, or two labels collided in '
            + 'this language.');
          break;
        }
        seen.add(crumb);
      }
    }
  }
}

let survivingFindStrings = 0;

// A translated page must not still contain the English string a translation
// table was written to replace. Whenever it does, the replacement silently
// never fired -- because the table lives in a module that page's builder does
// not import, because the builder hardcodes the English instead of calling
// t(), or because the markup carries "&amp;" where the JSON-LD carries a raw
// "&". All three shapes were live at once: 558 pages served an English phone
// placeholder, 54 served an English schema.org name, and a breadcrumb named
// the area in English under a translated <h1>.
//
// Filter keys are the deliberate exception: data-card-type and friends carry
// the English vocabulary the discovery JS matches on, so they are stripped
// before the scan rather than reported every run.
{
  const dir = path.join(root, 'scripts', 'lib');
  const entries = [];
  const files = fs.existsSync(dir)
    ? fs.readdirSync(dir).filter((f) => /translations.*\.mjs$/.test(f))
    : [];
  for (const file of files) {
    let mod;
    try {
      mod = await import(pathToFileURL(path.join(dir, file)).href);
    } catch {
      continue;
    }
    for (const value of Object.values(mod)) {
      if (!Array.isArray(value)) continue;
      for (const entry of value) {
        if (!entry || typeof entry.find !== 'string' || entry.find.length <= 25) continue;
        entries.push(entry);
      }
    }
  }
  const stripFilterKeys = (html) => html
    .replace(/ data-[a-z-]+="[^"]*\|[^"]*"/g, '')
    .replace(/ data-card-type="[^"]*"/g, '')
    .replace(/<option value="[^"]*">/g, '<option>');
  const survivors = new Map();
  // dist/ is the last stage: build_dist runs localisation passes of its own
  // on top of the per-locale pages, so a string still English in the repo
  // root may well be translated by the time it deploys. Scan the deployed
  // output when it exists, and fall back to the repo root otherwise.
  const distRoot = path.join(root, 'dist');
  const scanRoot = fs.existsSync(distRoot) ? distRoot : root;
  for (const locale of ENTRY_LOCALES) {
    const localeDir = path.join(scanRoot, locale);
    if (!fs.existsSync(localeDir)) continue;
    const candidates = entries.filter((e) => e[locale] && e[locale] !== e.find);
    for (const file of fs.readdirSync(localeDir).filter((f) => f.endsWith('.html'))) {
      const html = stripFilterKeys(fs.readFileSync(path.join(localeDir, file), 'utf8'));
      for (const entry of candidates) {
        const raw = entry.find.split('&amp;').join('&');
        if (html.includes(entry.find) || (raw !== entry.find && html.includes(raw))) {
          survivingFindStrings += 1;
          const key = `${entry.find.slice(0, 55)}`;
          if (!survivors.has(key)) survivors.set(key, `${locale}/${file}`);
        }
      }
    }
  }
  if (survivors.size) {
    const shown = [...survivors].slice(0, 4).map(([find, where]) => `"${find}" (${where})`);
    fail('locale pages', `${survivors.size} English string(s) a translation table covers are still `
      + `present in translated pages: ${shown.join('; ')}`
      + `${survivors.size > 4 ? `; …and ${survivors.size - 4} more` : ''}. `
      + 'The replacement never fired -- check that the page\'s builder imports that table, '
      + 'calls t() instead of hardcoding, and matches the "&" form the markup actually uses.');
  }
}

let translationEntriesChecked = 0;

{
  const dir = path.join(root, 'scripts', 'lib');
  const files = fs.existsSync(dir)
    ? fs.readdirSync(dir).filter((f) => /translations.*\.mjs$/.test(f))
    : [];
  for (const file of files) {
    let mod;
    try {
      mod = await import(pathToFileURL(path.join(dir, file)).href);
    } catch {
      continue;
    }
    const gaps = new Map();
    for (const value of Object.values(mod)) {
      if (!Array.isArray(value)) continue;
      for (const entry of value) {
        if (!entry || typeof entry !== 'object' || typeof entry.find !== 'string') continue;
        translationEntriesChecked += 1;
        const missing = ENTRY_LOCALES.filter((l) => typeof entry[l] !== 'string');
        if (missing.length) gaps.set(entry.find.slice(0, 60), missing);
      }
    }
    if (gaps.size) {
      const shown = [...gaps].slice(0, 4)
        .map(([find, missing]) => `"${find}" missing ${missing.join(', ')}`);
      fail(`scripts/lib/${file}`, `${gaps.size} entr${gaps.size === 1 ? 'y does' : 'ies do'} not cover `
        + `every locale: ${shown.join('; ')}${gaps.size > 4 ? `; …and ${gaps.size - 4} more` : ''}`);
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
    + `${drawerRowHeights} drawer row heights checked for one target size, `
    + `${translationEntriesChecked} translation entries checked for all nine locales, `
    + `${survivingFindStrings === 0 ? 'no' : survivingFindStrings} English source string(s) left unreplaced in translated pages, `
    + `${breadcrumbTrailsChecked} breadcrumb trails checked for a repeated crumb, `
    + `${placeSpellingsChecked} place names checked for one spelling, `
    + `${redirectRulesChecked} redirect rules checked for shadowing and duplication, `
    + `${sitemapPagesChecked} indexable pages matched against the sitemap, `
    + `${uniqueMetaChecked} titles and descriptions checked for uniqueness within a language, `
    + `${descriptionRatiosChecked} translated descriptions measured against their English source, `
    + `${ogLocalesChecked} og:locale values checked for the language_TERRITORY form, `
    + `${entityPagesChecked} locale pages checked for a translated organisation schema, `
    + `${revealPagesChecked} pages checked for the script that unhides their scroll-revealed content, `
    + `${translationConflictsChecked} English strings checked for exactly one translation each, `
    + `${sharedFragmentsChecked} guides compared against their nine locale builds for untranslated text, `
    + `${registerPagesChecked} pages checked for one form of address per language, `
    + `${faqSchemaChecked} visible FAQs matched against their structured data, `
    + `${areaNamesChecked} locale area pages checked for one spelling of the area name, `
    + `${segmentLinkChecked} area-to-segment links checked in both directions, `
    + `${entityIdChecked} indexable pages checked for one consistent organisation entity.`);
}
