import path from 'node:path';
import { existsSync, mkdirSync, writeFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';

const require = createRequire('/Users/sasanraftari/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/package.json');
const { chromium } = require('playwright');

const htmlPath = path.resolve('Liora_Living_SOLENNE_POLISHED.html');
const outDir = path.resolve('artifacts/liora');
mkdirSync(outDir, { recursive: true });

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

async function collectState(page, label) {
  return page.evaluate((stateLabel) => {
    const text = (selector) => document.querySelector(selector)?.textContent.trim().replace(/\s+/g, ' ') || null;
    const value = (selector) => document.querySelector(selector)?.value || '';
    const rect = (selector) => {
      const element = document.querySelector(selector);
      if (!element) return null;
      const box = element.getBoundingClientRect();
      return {
        x: Math.round(box.x),
        y: Math.round(box.y),
        width: Math.round(box.width),
        height: Math.round(box.height),
      };
    };

    const vox = document.querySelector('#vox');
    const mode = document.querySelector('#vmode');
    const ctaRow = document.querySelector('#v7row');
    const textInner = document.querySelector('#vtxtinner');
    const contact = document.querySelector('#contact');
    const textOpacity = textInner ? Number(getComputedStyle(textInner).opacity) : 0;

    return {
      label: stateLabel,
      overlayOn: Boolean(vox?.classList.contains('on')),
      bodyLocked: document.body.style.overflow === 'hidden',
      sceneId: text('#vsid'),
      sceneTotal: text('#vtotal'),
      headline: text('#vthl'),
      subcopy: text('#vtsub'),
      modeLabel: text('#vmode .mode-label'),
      modeAria: mode?.getAttribute('aria-label') || null,
      activeDots: document.querySelectorAll('#vdts .vdt.act').length,
      dotCount: document.querySelectorAll('#vdts .vdt').length,
      layerCount: document.querySelectorAll('#vstage .vlayer').length,
      closingClass: Boolean(document.querySelector('#vtxtbox.closing')),
      ctaVisible: ctaRow ? getComputedStyle(ctaRow).display !== 'none' : false,
      ctaText: text('#v7row'),
      textOpacity,
      areaValue: value('#f-area'),
      purposeValue: value('#f-purpose'),
      messageValue: value('#f-msg'),
      contactTop: contact ? Math.round(contact.getBoundingClientRect().top) : null,
      viewportHeight: window.innerHeight,
      overlayRect: rect('#vox'),
      textRect: rect('#vtxtinner'),
    };
  }, label);
}

async function verifyMainFlow(page, events) {
  await page.goto(pathToFileURL(htmlPath).href, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.waitForSelector('.dev-viewing-btn', { timeout: 10000 });

  const privateButtonCount = await page.locator('.dev-viewing-btn').count();
  if (privateButtonCount !== 1) {
    throw new Error(`Expected one private viewing button, found ${privateButtonCount}.`);
  }

  await page.locator('.dev-viewing-btn').click();
  await page.waitForFunction(() => document.querySelector('#vox')?.classList.contains('on'), { timeout: 12000 });
  await page.waitForFunction(() => document.querySelectorAll('#vdts .vdt').length === 20, { timeout: 8000 });
  await page.waitForFunction(() => {
    const veilClear = !document.querySelector('#vveil')?.classList.contains('on');
    const text = document.querySelector('#vtxtinner');
    return veilClear && text && Number(getComputedStyle(text).opacity) > 0.4;
  }, { timeout: 12000 });
  await page.screenshot({ path: path.join(outDir, 'private-viewing-open.png'), fullPage: false });
  events.push(await collectState(page, 'open'));

  await page.mouse.wheel(0, 900);
  await page.waitForFunction(() => document.querySelector('#vmode')?.classList.contains('manual'), { timeout: 5000 });
  events.push(await collectState(page, 'manual'));

  const sceneBeforeArrow = await page.locator('#vsid').innerText();
  await page.keyboard.press('ArrowDown');
  await page.waitForFunction((previousScene) => {
    const moved = document.querySelector('#vsid')?.textContent.trim() !== previousScene.trim();
    const text = document.querySelector('#vtxtinner');
    return moved && text && Number(getComputedStyle(text).opacity) > 0.4;
  }, sceneBeforeArrow, { timeout: 7000 });
  events.push(await collectState(page, 'arrow-down'));

  await page.locator('#vdts .vdt').nth(19).click();
  await page.waitForFunction(() => document.querySelector('#vsid')?.textContent.trim() === '20', { timeout: 7000 });
  await page.waitForFunction(() => {
    const row = document.querySelector('#v7row');
    const text = document.querySelector('#vtxtinner');
    return document.querySelector('#vtxtbox.closing') && row && getComputedStyle(row).display !== 'none' && text && Number(getComputedStyle(text).opacity) > 0.4;
  }, { timeout: 7000 });
  await page.screenshot({ path: path.join(outDir, 'private-viewing-final.png'), fullPage: false });
  events.push(await collectState(page, 'final'));

  await page.locator('#v7row .v7cta').click();
  await page.waitForFunction(() => !document.querySelector('#vox')?.classList.contains('on'), { timeout: 7000 });
  await page.waitForFunction(() => {
    return document.querySelector('#f-msg')?.value.includes('Solenne material');
  }, { timeout: 7000 });
  await page.waitForFunction(() => {
    const contact = document.querySelector('#contact');
    if (!contact) return false;
    const box = contact.getBoundingClientRect();
    return box.top < window.innerHeight * 0.38 && box.bottom > window.innerHeight * 0.48;
  }, { timeout: 9000 });
  await page.screenshot({ path: path.join(outDir, 'private-viewing-contact-prefill.png'), fullPage: false });
  events.push(await collectState(page, 'request-material'));
}

async function verifyEscapeFlow(page, events) {
  await page.goto(pathToFileURL(htmlPath).href, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.waitForSelector('.dev-viewing-btn', { timeout: 10000 });
  await page.locator('.dev-viewing-btn').click();
  await page.waitForFunction(() => document.querySelector('#vox')?.classList.contains('on'), { timeout: 12000 });
  await page.keyboard.press('Escape');
  await page.waitForFunction(() => !document.querySelector('#vox')?.classList.contains('on'), { timeout: 7000 });
  events.push(await collectState(page, 'escape-close'));
}

async function verifyGuidedCompletion(browser, events) {
  const mobilePage = await browser.newPage({ viewport: { width: 390, height: 844 } });
  await mobilePage.goto(pathToFileURL(htmlPath).href, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await mobilePage.waitForSelector('.dev-viewing-btn', { timeout: 10000 });
  await mobilePage.evaluate(() => {
    if (window.gsap) window.gsap.globalTimeline.timeScale(80);
  });
  await mobilePage.locator('.dev-viewing-btn').click();
  await mobilePage.waitForFunction(() => document.querySelector('#vox')?.classList.contains('on'), { timeout: 12000 });
  await mobilePage.waitForFunction(() => {
    return document.querySelector('#vmode .mode-label')?.textContent.trim().toLowerCase() === 'replay';
  }, { timeout: 12000 });
  await mobilePage.waitForFunction(() => {
    const row = document.querySelector('#v7row');
    const text = document.querySelector('#vtxtinner');
    return document.querySelector('#vsid')?.textContent.trim() === '20'
      && document.querySelector('#vtxtbox.closing')
      && row
      && getComputedStyle(row).display !== 'none'
      && text
      && Number(getComputedStyle(text).opacity) > 0.4;
  }, { timeout: 7000 });
  await mobilePage.screenshot({ path: path.join(outDir, 'private-viewing-guided-mobile-end.png'), fullPage: false });
  events.push(await collectState(mobilePage, 'guided-mobile-end'));
  await mobilePage.close();
}

const browser = await launchBrowser();
const page = await browser.newPage({ viewport: { width: 1440, height: 950 } });
const logs = [];
const failedRequests = [];

page.on('console', (message) => {
  if (['error', 'warning', 'warn'].includes(message.type())) {
    logs.push({ type: message.type(), text: message.text() });
  }
});
page.on('pageerror', (error) => logs.push({ type: 'pageerror', text: error.message }));
page.on('requestfailed', (request) => {
  const error = request.failure()?.errorText || 'request failed';
  if (error === 'net::ERR_ABORTED') return;
  failedRequests.push({
    url: request.url(),
    error,
  });
});

const events = [];
try {
  await verifyMainFlow(page, events);
  await verifyEscapeFlow(page, events);
  await verifyGuidedCompletion(browser, events);
} finally {
  await browser.close();
}

const assertions = {
  opens: events.some((event) => event.label === 'open' && event.overlayOn),
  hasTwentyScenes: events.some((event) => event.label === 'open' && event.sceneTotal === '20' && event.dotCount === 20 && event.layerCount === 20),
  manualToggleWorks: events.some((event) => event.label === 'manual' && event.modeLabel?.toLowerCase() === 'manual' && event.modeAria === 'Resume guided viewing'),
  keyboardNavigationWorks: events.some((event) => event.label === 'arrow-down' && event.sceneId !== events.find((item) => item.label === 'manual')?.sceneId && event.modeLabel?.toLowerCase() === 'manual' && event.textOpacity > 0.4),
  finalCtaWorks: events.some((event) => event.label === 'final' && event.sceneId === '20' && event.closingClass && event.ctaVisible && event.textOpacity > 0.4),
  guidedEndsOnFinalCta: events.some((event) => event.label === 'guided-mobile-end' && event.sceneId === '20' && event.closingClass && event.ctaVisible && event.textOpacity > 0.4 && event.modeLabel?.toLowerCase() === 'replay'),
  requestMaterialPrefills: events.some((event) => event.label === 'request-material' && !event.overlayOn && event.areaValue === 'Benahavís' && event.messageValue.includes('Solenne material') && event.contactTop < event.viewportHeight * 0.38),
  escapeCloses: events.some((event) => event.label === 'escape-close' && !event.overlayOn && !event.bodyLocked),
  noConsoleIssues: logs.length === 0,
};

const report = {
  page: path.relative(process.cwd(), htmlPath),
  assertions,
  logs,
  failedRequests,
  events,
  screenshots: [
    'artifacts/liora/private-viewing-open.png',
    'artifacts/liora/private-viewing-final.png',
    'artifacts/liora/private-viewing-guided-mobile-end.png',
    'artifacts/liora/private-viewing-contact-prefill.png',
  ],
};

writeFileSync(path.join(outDir, 'private-viewing-flow-report.json'), JSON.stringify(report, null, 2));
console.log(JSON.stringify(report, null, 2));
