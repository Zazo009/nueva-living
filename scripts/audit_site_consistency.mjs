import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const root = process.cwd();
const dist = path.join(root, 'dist');
const failures = [];
const warnings = [];
const expectedNavTargets = [
  'approach.html',
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
  const systemLinks = html.match(/assets\/liora\/nueva-system\.css\?v=[a-z0-9]+/gi) || [];
  const trackingScripts = html.match(/assets\/liora\/nueva-tracking\.js\?v=[a-z0-9]+/gi) || [];

  if (systemLinks.length !== 1) {
    fail(name, `expected one versioned Nueva system stylesheet, found ${systemLinks.length}`);
  }
  if (trackingScripts.length !== 1) {
    fail(name, `expected one versioned Nueva tracking script, found ${trackingScripts.length}`);
  }
  if (!/<head>[\s\S]*assets\/liora\/nueva-tracking\.js\?v=[a-z0-9]+[\s\S]*<\/head>/i.test(html)) {
    fail(name, 'Nueva tracking script is not loaded from the document head');
  }

  const stylesheetOrder = [...html.matchAll(/<link[^>]+rel="stylesheet"[^>]+href="([^"]+)"/gi)]
    .map((match) => match[1]);
  if (!stylesheetOrder.at(-1)?.includes('nueva-system.css')) {
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
