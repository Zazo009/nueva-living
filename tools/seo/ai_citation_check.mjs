// Asks Perplexity the buyer questions in ai_citation_questions.json and logs whether nuevaliving.com is
// cited, and which domains are cited instead. Run by hand, weekly:
//
//   PERPLEXITY_API_KEY=... node tools/seo/ai_citation_check.mjs          # ask every question
//   node tools/seo/ai_citation_check.mjs --dry                           # list the questions, ask nothing
//
// The key is read from the environment and never written anywhere. Results append to
// tools/seo/out/ai-citations.jsonl, one line per question per run, so a trend can be read later.
// This measures one assistant on one day: answers vary between runs, so read a month of weeks, not one row.
// ChatGPT, Gemini and Claude have no equivalent public "citations" field, so those are checked by hand
// from the same list (paste the question, note whether the site is named or linked).
import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..', '..');
const { questions } = JSON.parse(fs.readFileSync(path.join(root, 'tools/seo/ai_citation_questions.json'), 'utf8'));
const dry = process.argv.includes('--dry');
const key = process.env.PERPLEXITY_API_KEY;
const domainOf = (url) => { try { return new URL(url).hostname.replace(/^www\./, ''); } catch { return ''; } };

if (dry || !key) {
  if (!dry) console.error('PERPLEXITY_API_KEY is not set; listing the questions only.');
  questions.forEach((q, i) => console.log(`${String(i + 1).padStart(2)}. [${q.lang}] ${q.q}`));
  process.exit(dry ? 0 : 1);
}

const outDir = path.join(root, 'tools', 'seo', 'out');
fs.mkdirSync(outDir, { recursive: true });
const logFile = path.join(outDir, 'ai-citations.jsonl');
const date = new Date().toISOString().slice(0, 10);
let cited = 0;
const competitors = new Map();

for (const { lang, q } of questions) {
  const response = await fetch('https://api.perplexity.ai/chat/completions', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${key}` },
    body: JSON.stringify({ model: 'sonar', messages: [{ role: 'user', content: q }] }),
  });
  if (!response.ok) { console.error(`HTTP ${response.status} for: ${q}`); continue; }
  const data = await response.json();
  const urls = data.citations || (data.search_results || []).map((r) => r.url) || [];
  const domains = [...new Set(urls.map(domainOf).filter(Boolean))];
  const hit = domains.includes('nuevaliving.com');
  if (hit) cited += 1;
  domains.filter((d) => d !== 'nuevaliving.com').forEach((d) => competitors.set(d, (competitors.get(d) || 0) + 1));
  fs.appendFileSync(logFile, `${JSON.stringify({ date, engine: 'perplexity-sonar', lang, q, cited: hit, domains })}\n`);
  console.log(`${hit ? 'CITED ' : 'no    '} [${lang}] ${q}`);
}
console.log(`\nnuevaliving.com cited in ${cited} of ${questions.length} answers.`);
console.log('Domains cited most often instead:', [...competitors].sort((a, b) => b[1] - a[1]).slice(0, 10).map(([d, n]) => `${d} (${n})`).join(', '));
