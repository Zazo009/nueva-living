const DEFAULT_ALLOWED_ORIGINS = [
  'https://nuevaliving.com',
  'https://www.nuevaliving.com',
];

const AREAS = ['marbella', 'estepona', 'benahavis', 'nueva-andalucia', 'mijas-fuengirola'];
const PROPERTY_TYPES = ['apartment', 'penthouse', 'villa', 'townhouse'];
const STATUSES = ['off_plan', 'under_construction', 'completed'];
const TIMINGS = ['ready', '1y', '2y', '2y+'];
const TAGS = [
  'Sea View', 'Beachside', 'Golf Living', 'Wellness Living', 'Resort Lifestyle',
  'Family-Oriented', 'Privacy & Security', 'Walkable Lifestyle', 'Lock-and-Leave',
  'Smart Home', 'Sustainable Living', 'Design-Led', 'Ultra Luxury', 'Boutique Community',
  'Contemporary Mediterranean', 'Minimalist Architecture', 'Organic Design',
  'Panoramic Glass Design', 'Low-Density Development', 'Boutique Development',
  'Golden Mile', 'Golf Valley', 'New Golden Mile', 'Marbella East', 'Beachfront',
  'Hillside Views', 'Gated Community', 'Walkable to Amenities',
  'Primary Residence', 'Holiday Home', 'Investment Property', 'Rental Yield Potential',
  'Family Relocation', 'International Buyer', 'Second Home', 'Lifestyle Investment',
  'Long-Term Value', 'Low-Maintenance Ownership',
];

const SEARCH_TOOL = {
  name: 'apply_property_filters',
  description: 'Map a free-text property search into the site\'s existing filter values. Only include a field if the text clearly implies it -- omit anything uncertain.',
  input_schema: {
    type: 'object',
    properties: {
      area: { type: 'string', enum: AREAS, description: 'Location filter' },
      propertyType: { type: 'string', enum: PROPERTY_TYPES },
      status: { type: 'string', enum: STATUSES },
      timing: { type: 'string', enum: TIMINGS, description: 'Move-in timing bucket' },
      priceMin: { type: 'number', description: 'Minimum budget in EUR' },
      priceMax: { type: 'number', description: 'Maximum budget in EUR' },
      bedroomsMin: { type: 'number' },
      bedroomsMax: { type: 'number' },
      tags: {
        type: 'array',
        items: { type: 'string', enum: TAGS },
        description: 'Lifestyle, architecture, setting or investment tags implied by the text',
      },
      summary: { type: 'string', description: 'One short sentence confirming what was searched for, to show the visitor' },
    },
    required: [],
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
        max_tokens: 400,
        system: 'You map free-text Costa del Sol property search queries onto a fixed set of filter values by calling apply_property_filters exactly once. Never invent values outside the given enums. If nothing in the text maps to a field, omit it.',
        messages: [{ role: 'user', content: query }],
        tools: [SEARCH_TOOL],
        tool_choice: { type: 'tool', name: 'apply_property_filters' },
      }),
    });

    if (!aiResponse.ok) {
      const upstreamMessage = (await aiResponse.text()).slice(0, 300);
      console.error('Anthropic API rejected search request', { status: aiResponse.status, response: upstreamMessage });
      return response(502, { ok: false, error: 'AI search request failed' }, origin);
    }

    const result = await aiResponse.json();
    const toolUse = result?.content?.find((block) => block.type === 'tool_use');
    const filters = toolUse?.input || {};

    return response(200, { ok: true, filters }, origin);
  } catch (error) {
    console.error('AI search request failed', { message: error.message || 'Unknown error' });
    return response(502, { ok: false, error: 'AI search request failed' }, origin);
  }
};
