const catalog = require('./data/projects-catalog.json');

const DEFAULT_ALLOWED_ORIGINS = [
  'https://nuevaliving.com',
  'https://www.nuevaliving.com',
];

const CATALOG_SLUGS = catalog.map((project) => project.slug);

const SEARCH_TOOL = {
  name: 'search_developments',
  description: 'Return which Costa del Sol developments (by slug) match the visitor\'s search, reasoning over each development\'s full profile below -- not just a keyword match on area or type. If no development is a strong match, return an empty matchedSlugs array and explain why in summary (e.g. no current development in that area), optionally suggesting the closest real alternative from the catalog by name in the summary text.',
  input_schema: {
    type: 'object',
    properties: {
      matchedSlugs: {
        type: 'array',
        items: { type: 'string', enum: CATALOG_SLUGS },
        description: 'Slugs of developments that genuinely match the search, best match first. Empty if nothing matches.',
      },
      summary: {
        type: 'string',
        description: 'One short, natural sentence for the visitor confirming what was found, or explaining why nothing matched and what the closest option is instead.',
      },
    },
    required: ['matchedSlugs', 'summary'],
  },
};

function response(statusCode, body, origin = '') {
  const allowedOrigins = (process.env.ALLOWED_ORIGINS || DEFAULT_ALLOWED_ORIGINS.join(','))
    .split(',')
    .map((item) => item.trim())
    .filter(Boolean);
  const allowOrigin = allowedOrigins.includes(origin) ? origin : allowedOrigins[0];

  return {
    statusCode,
    headers: {
      'Access-Control-Allow-Origin': allowOrigin,
      'Access-Control-Allow-Headers': 'Content-Type',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Content-Type': 'application/json',
      Vary: 'Origin',
    },
    body: JSON.stringify(body),
  };
}

function safeJson(value) {
  try {
    return JSON.parse(value || '{}');
  } catch {
    return null;
  }
}

function cleanEnvironmentValue(value) {
  const cleaned = typeof value === 'string' ? value.trim() : '';
  if (cleaned.length < 2) return cleaned;
  const first = cleaned[0];
  const last = cleaned[cleaned.length - 1];
  return (first === last && (first === '"' || first === "'"))
    ? cleaned.slice(1, -1).trim()
    : cleaned;
}

exports.handler = async (event) => {
  const origin = event.headers.origin || event.headers.Origin || '';

  if (event.httpMethod === 'OPTIONS') {
    return response(204, {}, origin);
  }
  if (event.httpMethod !== 'POST') {
    return response(405, { ok: false, error: 'Method not allowed' }, origin);
  }

  const apiKey = cleanEnvironmentValue(process.env.ANTHROPIC_API_KEY);
  if (!apiKey) {
    return response(500, { ok: false, error: 'AI search is not configured' }, origin);
  }

  const payload = safeJson(event.body);
  const query = typeof payload?.query === 'string' ? payload.query.trim().slice(0, 300) : '';
  if (!query) {
    return response(422, { ok: false, error: 'Missing search text' }, origin);
  }

  try {
    const aiResponse = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': apiKey,
        'anthropic-version': '2023-06-01',
      },
      body: JSON.stringify({
        model: 'claude-haiku-4-5-20251001',
        max_tokens: 600,
        system: `You help visitors search a small, real catalog of Costa del Sol property developments by calling search_developments exactly once. Judge matches using the full profile of each development (location, price, bedrooms, construction status, tags, and description/overview/location text) -- not just literal keyword overlap. A query can match on lifestyle or setting language even if it doesn't name the area directly. Never invent a development that isn't in the catalog, and never force a match that isn't genuinely relevant just to avoid an empty result.\n\nCatalog:\n${JSON.stringify(catalog)}`,
        messages: [{ role: 'user', content: query }],
        tools: [SEARCH_TOOL],
        tool_choice: { type: 'tool', name: 'search_developments' },
      }),
    });

    if (!aiResponse.ok) {
      const upstreamMessage = (await aiResponse.text()).slice(0, 300);
      console.error('Anthropic API rejected search request', { status: aiResponse.status, response: upstreamMessage });
      return response(502, { ok: false, error: 'AI search request failed' }, origin);
    }

    const result = await aiResponse.json();
    const toolUse = result?.content?.find((block) => block.type === 'tool_use');
    const matchedSlugs = Array.isArray(toolUse?.input?.matchedSlugs)
      ? toolUse.input.matchedSlugs.filter((slug) => CATALOG_SLUGS.includes(slug))
      : [];
    const summary = typeof toolUse?.input?.summary === 'string' ? toolUse.input.summary : '';

    return response(200, { ok: true, matchedSlugs, summary }, origin);
  } catch (error) {
    console.error('AI search request failed', { message: error.message || 'Unknown error' });
    return response(502, { ok: false, error: 'AI search request failed' }, origin);
  }
};
