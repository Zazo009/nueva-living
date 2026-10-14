// Tells IndexNow search engines (Bing and the engines and assistants built on its index)
// which URLs changed. Run by hand after a deploy has finished, not from the build:
//
//   node scripts/indexnow_ping.mjs            # every URL in dist/sitemap.xml
//   node scripts/indexnow_ping.mjs <url> ...  # just these
//
// The key is not a secret. It is proved by https://nuevaliving.com/<key>.txt, which the
// build writes. IndexNow takes up to 10,000 URLs per request.
import fs from 'node:fs';
import { INDEXNOW_KEY } from './lib/ai_discovery.mjs';

const host = 'nuevaliving.com';
const argUrls = process.argv.slice(2);
const urls = argUrls.length
  ? argUrls
  : [...fs.readFileSync('dist/sitemap.xml', 'utf8').matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]);

const proof = await fetch(`https://${host}/${INDEXNOW_KEY}.txt`).then((r) => r.text()).catch(() => '');
if (proof.trim() !== INDEXNOW_KEY) {
  console.error(`https://${host}/${INDEXNOW_KEY}.txt does not return the key yet: deploy first.`);
  process.exit(1);
}

for (let i = 0; i < urls.length; i += 10000) {
  const batch = urls.slice(i, i + 10000);
  const response = await fetch('https://api.indexnow.org/indexnow', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json; charset=utf-8' },
    body: JSON.stringify({ host, key: INDEXNOW_KEY, keyLocation: `https://${host}/${INDEXNOW_KEY}.txt`, urlList: batch })
  });
  console.log(`IndexNow: ${batch.length} URLs -> HTTP ${response.status}`);
}
