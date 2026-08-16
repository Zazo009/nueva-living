import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const root = process.cwd();
const dist = path.join(root, 'dist');
const failures = [];
const warnings = [];
const expectedNavTargets = [
  'guides.html',
  'why-nueva.html',
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
    const mobileNav = html.match(/<div class="mobile-menu"[^>]*>([\s\S]*?)<\/div>/i)?.[1] || '';
    for (const target of expectedNavTargets) {
      if (!desktopNav.includes(`href="${target}"`)) {
        fail(name, `desktop navigation is missing ${target}`);
      }
      if (!mobileNav.includes(`href="${target}"`)) {
        fail(name, `mobile navigation is missing ${target}`);
      }
    }
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

if (warnings.length) {
  console.warn(`Consistency warnings (${warnings.length}):`);
  warnings.forEach((message) => console.warn(`- ${message}`));
}

if (failures.length) {
  console.error(`Consistency audit failed (${failures.length}):`);
  failures.forEach((message) => console.error(`- ${message}`));
  process.exitCode = 1;
} else {
  console.log(`Consistency audit passed: ${htmlFiles.length} HTML pages checked.`);
}
