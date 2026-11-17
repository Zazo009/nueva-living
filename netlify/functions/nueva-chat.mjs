// Soléa, the chat on nuevaliving.com: the endpoint the browser talks to
// (assets/liora/nueva-solea.js). The prompt, the tools and the conversation loop are in
// lib/chat-core.js.
//
// A Netlify function in the streaming format, so the answer reaches the visitor while it is being
// written instead of after 5 to 15 seconds. The response is newline-delimited JSON:
//   {"type":"text","text":"..."}   a piece of the answer, as many as it takes
//   {"type":"done","cards":[...],"sent":false,"meta":{...}}   once, at the end
//   {"type":"error","code":"..."}   instead of done, when something failed
// meta is what the browser records with the question in the anonymous question log: the search
// criteria, the guide pages read, how many developments matched, and whether the site could not
// answer (gap). It never carries a name, an e-mail or a phone number.
import core from './lib/chat-core.js';

const { prepare, runChat, tooMany, cleanEnvironmentValue } = core;
const DEFAULT_ALLOWED_ORIGINS = ['https://nuevaliving.com', 'https://www.nuevaliving.com'];

function cors(origin) {
  const allowed = (process.env.ALLOWED_ORIGINS || DEFAULT_ALLOWED_ORIGINS.join(','))
    .split(',').map((item) => item.trim()).filter(Boolean);
  return {
    'Access-Control-Allow-Origin': allowed.includes(origin) ? origin : allowed[0],
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Cache-Control': 'no-store',
    Vary: 'Origin',
  };
}

function json(status, body, origin) {
  return new Response(JSON.stringify(body), { status, headers: { ...cors(origin), 'Content-Type': 'application/json' } });
}

export default async (req, context) => {
  const origin = req.headers.get('origin') || '';
  if (req.method === 'OPTIONS') return new Response(null, { status: 204, headers: cors(origin) });
  if (req.method !== 'POST') return json(405, { ok: false, error: 'Method not allowed' }, origin);

  const apiKey = cleanEnvironmentValue(process.env.ANTHROPIC_API_KEY);
  if (!apiKey) return json(500, { ok: false, error: 'Chat is not configured' }, origin);

  const ip = context?.ip || req.headers.get('x-nf-client-connection-ip') || 'unknown';
  if (tooMany(ip)) return json(429, { ok: false, error: 'busy' }, origin);

  let payload;
  try {
    payload = await req.json();
  } catch {
    return json(400, { ok: false, error: 'Invalid JSON' }, origin);
  }
  const prepared = prepare(payload);
  if (prepared.error) return json(prepared.error, { ok: false, error: prepared.error === 413 ? 'too_long' : 'invalid' }, origin);

  const encoder = new TextEncoder();
  const stream = new ReadableStream({
    async start(controller) {
      const send = (line) => controller.enqueue(encoder.encode(`${JSON.stringify(line)}\n`));
      try {
        const result = await runChat({
          apiKey,
          messages: prepared.messages,
          language: prepared.language,
          ip,
          userAgent: req.headers.get('user-agent') || '',
          onText: (text) => send({ type: 'text', text }),
        });
        send({ type: 'done', cards: result.cards, sent: result.sent, fallback: result.fallback || null, meta: result.meta });
      } catch (error) {
        console.error('chat failed', { message: error.message });
        send({ type: 'error', code: 'upstream' });
      }
      controller.close();
    },
  });
  return new Response(stream, {
    status: 200,
    headers: { ...cors(origin), 'Content-Type': 'application/x-ndjson; charset=utf-8', 'X-Accel-Buffering': 'no' },
  });
};
