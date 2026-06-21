import path from 'node:path';
import { existsSync, mkdirSync, writeFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';

const require = createRequire('/Users/sasanraftari/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/package.json');
const { chromium } = require('playwright');
const sharp = require('sharp');

const htmlPath = path.resolve('Liora_Living_SOLENNE_POLISHED.html');
const outDir = path.resolve('artifacts/liora');
mkdirSync(outDir, { recursive: true });

async function imageStats(file) {
  const image = sharp(file);
  const metadata = await image.metadata();
  const stats = await image.stats();
  return {
    file: path.relative(process.cwd(), file),
    width: metadata.width,
    height: metadata.height,
    stdev: Number(stats.channels.reduce((sum, channel) => sum + channel.stdev, 0).toFixed(2)),
  };
}

async function verifyViewport(browser, name, viewport) {
  const page = await browser.newPage({ viewport });
  const logs = [];
  const failedLioraRequests = [];

  page.on('console', (message) => {
    if (['error', 'warning', 'warn'].includes(message.type())) {
      logs.push({ type: message.type(), text: message.text() });
    }
  });
  page.on('pageerror', (error) => logs.push({ type: 'pageerror', text: error.message }));
  page.on('requestfailed', (request) => {
    const url = request.url();
    if (url.includes('/assets/liora/')) {
      failedLioraRequests.push({ url, error: request.failure()?.errorText || 'request failed' });
    }
  });

  await page.goto(pathToFileURL(htmlPath).href, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.waitForSelector('.hero-brand-logo', { timeout: 10000 });
  await page.waitForSelector('.brand-logo-word strong', { timeout: 10000 });

  const viewportShot = path.join(outDir, `${name}-viewport.png`);
  await page.screenshot({ path: viewportShot, fullPage: false });

  const heroLogoShot = path.join(outDir, `${name}-hero-logo.png`);
  await page.locator('.hero-brand-logo').screenshot({ path: heroLogoShot });

  await page.locator('#advisory').scrollIntoViewIfNeeded();
  await page.waitForFunction(() => {
    const image = document.querySelector('.advisory-img-wrap img');
    return image && image.complete && image.naturalWidth > 0;
  }, { timeout: 10000 });
  const advisoryShot = path.join(outDir, `${name}-advisory.png`);
  await page.screenshot({ path: advisoryShot, fullPage: false });

  const logoInfo = await page.evaluate(() => {
    function info(selector) {
      const element = document.querySelector(selector);
      if (!element) return null;
      const rect = element.getBoundingClientRect();
      return {
        src: element.getAttribute('src'),
        naturalWidth: element.naturalWidth,
        naturalHeight: element.naturalHeight,
        complete: element.complete,
        rect: {
          x: Math.round(rect.x),
          y: Math.round(rect.y),
          width: Math.round(rect.width),
          height: Math.round(rect.height),
        },
      };
    }

    const vbrand = document.querySelector('.vbrand');
    return {
      nav: info('.brand-logo-compact img'),
      hero: info('.hero-brand-logo'),
      footer: info('.footer-liora-logo'),
      navText: document.querySelector('.brand-logo-word')?.textContent.trim().replace(/\s+/g, ' ') || null,
      advisory: info('.advisory-img-wrap img'),
      vbrandBackground: vbrand ? getComputedStyle(vbrand, '::before').backgroundImage : null,
    };
  });

  await page.locator('.footer-liora-logo').scrollIntoViewIfNeeded();
  await page.waitForFunction(() => {
    const image = document.querySelector('.footer-liora-logo');
    return image && image.complete && image.naturalWidth > 0;
  }, { timeout: 10000 });
  const footerLogoShot = path.join(outDir, `${name}-footer-logo.png`);
  await page.locator('.footer-liora-logo').screenshot({ path: footerLogoShot });

  const footerShot = path.join(outDir, `${name}-footer.png`);
  await page.screenshot({ path: footerShot, fullPage: false });

  await page.close();

  return {
    name,
    viewport,
    logs,
    failedLioraRequests,
    logoInfo,
    screenshots: [
      await imageStats(viewportShot),
      await imageStats(heroLogoShot),
      await imageStats(advisoryShot),
      await imageStats(footerLogoShot),
      await imageStats(footerShot),
    ],
  };
}

async function launchBrowser() {
  try {
    return await chromium.launch({ headless: true });
  } catch (error) {
    const candidates = [
      '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
      '/Applications/Chromium.app/Contents/MacOS/Chromium',
      '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
    ];
    const executablePath = candidates.find((candidate) => existsSync(candidate));
    if (!executablePath) throw error;
    return chromium.launch({
      executablePath,
      headless: true,
      args: ['--no-sandbox'],
    });
  }
}

const browser = await launchBrowser();
const report = {
  page: path.relative(process.cwd(), htmlPath),
  desktop: await verifyViewport(browser, 'desktop', { width: 1440, height: 950 }),
  mobile: await verifyViewport(browser, 'mobile', { width: 390, height: 844 }),
};
await browser.close();

writeFileSync(path.join(outDir, 'verification-report.json'), JSON.stringify(report, null, 2));
console.log(JSON.stringify(report, null, 2));
