import path from 'node:path';
import { existsSync, mkdirSync, writeFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';

const require = createRequire('/Users/sasanraftari/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/package.json');
const { chromium } = require('playwright');

const htmlPath = path.resolve('Liora_Living_SOLENNE_POLISHED.html');
const outDir = path.resolve('artifacts/liora/transitions');
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

function matrixParts(transform) {
  if (!transform || transform === 'none') return { scaleX: 1, scaleY: 1, x: 0, y: 0 };
  const match = transform.match(/matrix\(([^)]+)\)/);
  if (!match) return { scaleX: null, scaleY: null, x: null, y: null };
  const values = match[1].split(',').map((value) => Number(value.trim()));
  return {
    scaleX: values[0],
    scaleY: values[3],
    x: values[4],
    y: values[5],
  };
}

const browser = await launchBrowser();
const page = await browser.newPage({ viewport: { width: 1440, height: 950 } });
const issues = [];
const samples = [];

try {
  await page.goto(pathToFileURL(htmlPath).href, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.locator('.dev-viewing-btn').click();
  await page.waitForFunction(() => document.querySelector('#vox')?.classList.contains('on'), { timeout: 12000 });
  await page.waitForFunction(() => document.querySelectorAll('#vdts .vdt').length === 20, { timeout: 8000 });
  await page.locator('#vmode').click();

  const checks = [
    { name: 'scene-04-golf-transition', scene: 3, progress: 0.84 },
    { name: 'scene-08-terrace-transition', scene: 7, progress: 0.84 },
    ...Array.from({ length: 10 }, (_, index) => {
      const scene = index + 9;
      return {
        name: `scene-${String(scene + 1).padStart(2, '0')}-late-transition`,
        scene,
        progress: 0.84,
      };
    }),
    { name: 'scene-20-closing-approach', scene: 18, progress: 0.88 },
  ];

  for (const check of checks) {
    await page.evaluate(({ scene, progress }) => {
      const film = document.getElementById('vfilm');
      const total = 20;
      const maxScroll = film.scrollHeight - film.clientHeight;
      film.scrollTop = ((scene + progress) / total) * maxScroll;
      window.ScrollTrigger?.update();
    }, check);

    await page.waitForTimeout(120);
    const file = path.join(outDir, `${check.name}.png`);
    await page.screenshot({ path: file, fullPage: false });

    const layerState = await page.evaluate(() => {
      return Array.from(document.querySelectorAll('.vlayer')).map((layer, index) => {
        const style = getComputedStyle(layer);
        return {
          index: index + 1,
          opacity: Number(style.opacity),
          transform: style.transform,
          backgroundImage: style.backgroundImage,
        };
      }).filter((layer) => layer.opacity > 0.01);
    });

    const parsedLayers = layerState.map((layer) => ({
      ...layer,
      matrix: matrixParts(layer.transform),
    }));

    for (const layer of parsedLayers) {
      if (!layer.backgroundImage || layer.backgroundImage === 'none') {
        issues.push(`${check.name}: visible layer ${layer.index} has no background image`);
      }
      if (Math.abs(layer.matrix.x || 0) > 1 || Math.abs(layer.matrix.y || 0) > 1) {
        issues.push(`${check.name}: layer ${layer.index} has lateral/vertical matrix translation ${JSON.stringify(layer.matrix)}`);
      }
      if ((layer.matrix.scaleX || 0) < 1.02 || (layer.matrix.scaleY || 0) < 1.02) {
        issues.push(`${check.name}: layer ${layer.index} scale is too low ${JSON.stringify(layer.matrix)}`);
      }
    }

    if (parsedLayers.length < 1 || parsedLayers.length > 2) {
      issues.push(`${check.name}: expected one or two visible layers, found ${parsedLayers.length}`);
    }

    samples.push({
      ...check,
      screenshot: path.relative(path.resolve('.'), file),
      layers: parsedLayers,
    });
  }
} finally {
  await browser.close();
}

const report = {
  page: path.basename(htmlPath),
  assertions: {
    noVisibleLayerTranslation: !issues.some((issue) => issue.includes('translation')),
    visibleLayersOverscaled: !issues.some((issue) => issue.includes('scale is too low')),
  },
  issues,
  samples,
};

writeFileSync(path.join(outDir, 'transition-edge-report.json'), JSON.stringify(report, null, 2));
console.log(JSON.stringify(report, null, 2));

if (issues.length) {
  process.exitCode = 1;
}
