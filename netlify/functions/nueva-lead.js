const DEFAULT_CRM_WEBHOOK_URL = 'https://marbella-crm.vercel.app/api/webhook/liora';
const DEFAULT_ALLOWED_ORIGINS = [
  'https://nuevaliving.com',
  'https://www.nuevaliving.com',
];
const ALLOWED_AREAS = new Set(['marbella', 'estepona', 'benahavis', 'other']);
const ALLOWED_PROPERTY_TYPES = new Set(['villa', 'apartment', 'penthouse', 'townhouse', 'duplex']);

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

function cleanString(value) {
  return typeof value === 'string' ? value.replace(/\s+/g, ' ').trim() : '';
}

function cleanEnvironmentValue(value) {
  const cleaned = cleanString(value);
  if (cleaned.length < 2) return cleaned;

  const first = cleaned[0];
  const last = cleaned[cleaned.length - 1];
  return (first === last && (first === '"' || first === "'"))
    ? cleaned.slice(1, -1).trim()
    : cleaned;
}

function optionalNumber(value) {
  if (value === '' || value === null || value === undefined) return undefined;
  const number = Number(value);
  return Number.isFinite(number) ? number : undefined;
}

function optionalBoolean(value) {
  if (value === '' || value === null || value === undefined) return undefined;
  if (typeof value === 'boolean') return value;
  if (typeof value === 'string') return ['true', '1', 'yes', 'on'].includes(value.toLowerCase());
  return Boolean(value);
}

function allowedValues(value, allowed) {
  if (!Array.isArray(value)) return [];
  return [...new Set(value.map(cleanString).filter((item) => allowed.has(item)))];
}

function normalizedText(value) {
  return cleanString(Array.isArray(value) ? value.join(' ') : value)
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase();
}

function normalizeAreas(value) {
  if (Array.isArray(value)) {
    const exact = allowedValues(value.map((item) => normalizedText(item)), ALLOWED_AREAS);
    if (exact.length === value.length) return exact;
  }

  const text = normalizedText(value);
  if (!text) return [];
  if (/open to all|all areas|mixed/.test(text)) return [...ALLOWED_AREAS];

  const areas = [];
  if (text.includes('marbella')) areas.push('marbella');
  if (text.includes('estepona') || text.includes('new golden mile')) areas.push('estepona');
  if (text.includes('benahavis')) areas.push('benahavis');
  if (!areas.length || /nueva andalucia|mijas|fuengirola|costa del sol|other/.test(text)) areas.push('other');
  return [...new Set(areas)];
}

function normalizePropertyTypes(value) {
  if (Array.isArray(value)) {
    const exact = allowedValues(value.map((item) => normalizedText(item)), ALLOWED_PROPERTY_TYPES);
    if (exact.length === value.length) return exact;
  }

  const text = normalizedText(value);
  if (!text) return [];
  if (/mixed|open/.test(text)) return [...ALLOWED_PROPERTY_TYPES];

  const types = [];
  if (text.includes('villa')) types.push('villa');
  if (/apartment|suite|garden residence/.test(text)) types.push('apartment');
  if (text.includes('penthouse')) types.push('penthouse');
  if (text.includes('townhouse')) types.push('townhouse');
  if (text.includes('duplex')) types.push('duplex');
  return [...new Set(types)];
}

function parseBudgetRange(value) {
  const text = cleanString(value);
  const numbers = [...text.matchAll(/[\d,.]+/g)]
    .map((match) => Number(match[0].replace(/[,.](?=\d{3}\b)/g, '').replace(',', '.')))
    .filter(Number.isFinite);
  if (!numbers.length) return {};
  if (/\+/.test(text) || numbers.length === 1) return { min: numbers[0] };
  return { min: numbers[0], max: numbers[1] };
}

function parseRequestBody(event) {
  const contentType = cleanString(event.headers['content-type'] || event.headers['Content-Type']).toLowerCase();
  if (contentType.includes('application/x-www-form-urlencoded')) {
    return Object.fromEntries(new URLSearchParams(event.body || ''));
  }
  return safeJson(event.body);
}

function sourcePath(lead, event) {
  if (cleanString(lead.source_page)) return cleanString(lead.source_page);
  const referer = cleanString(event.headers.referer || event.headers.Referer);
  if (!referer) return '';
  try {
    const url = new URL(referer);
    return `${url.pathname}${url.search}`;
  } catch {
    return '';
  }
}

function compactPayload(payload) {
  return Object.fromEntries(Object.entries(payload).filter(([, value]) => {
    if (value === '' || value === undefined || value === null) return false;
    return !Array.isArray(value) || value.length > 0;
  }));
}

function crmPayload(lead, event) {
  const budget = parseBudgetRange(lead.budget_range || lead.budget);
  const consent = optionalBoolean(lead.consent);
  const project = cleanString(lead.project);
  const originalMessage = cleanString(lead.message);
  const message = project && !originalMessage.toLowerCase().includes(project.toLowerCase())
    ? `${originalMessage ? `${originalMessage} ` : ''}Project: ${project}`
    : originalMessage;

  return compactPayload({
    first_name: cleanString(lead.first_name),
    last_name: cleanString(lead.last_name),
    email: cleanString(lead.email),
    phone: cleanString(lead.phone),
    budget_min: optionalNumber(lead.budget_min) ?? budget.min,
    budget_max: optionalNumber(lead.budget_max) ?? budget.max,
    preferred_areas: normalizeAreas(lead.preferred_areas || lead.preferred_area),
    property_types: normalizePropertyTypes(lead.property_types || lead.property_type_interest),
    bedrooms_min: optionalNumber(lead.bedrooms_min),
    bedrooms_max: optionalNumber(lead.bedrooms_max),
    nationality: cleanString(lead.nationality),
    message,
    consent,
    consent_text: cleanString(lead.consent_text) || (consent ? 'I agree to be contacted and for my data to be stored' : ''),
    marketing_opt_in: optionalBoolean(lead.marketing_opt_in),
    source_page: sourcePath(lead, event),
    utm_source: cleanString(lead.utm_source),
    utm_campaign: cleanString(lead.utm_campaign),
  });
}

function successResponse(crmResult, origin, browserFormSubmission) {
  if (browserFormSubmission) {
    return {
      statusCode: 303,
      headers: {
        Location: '/thank-you.html',
        'Cache-Control': 'no-store',
      },
      body: '',
    };
  }

  return response(200, {
    ok: true,
    success: true,
    lead_id: cleanString(crmResult.lead_id),
  }, origin);
}

exports.handler = async (event) => {
  const origin = event.headers.origin || event.headers.Origin || '';
  const contentType = cleanString(event.headers['content-type'] || event.headers['Content-Type']).toLowerCase();
  const browserFormSubmission = contentType.includes('application/x-www-form-urlencoded');

  if (event.httpMethod === 'OPTIONS') {
    return response(204, {}, origin);
  }

  if (event.httpMethod !== 'POST') {
    return response(405, { ok: false, error: 'Method not allowed' }, origin);
  }

  // Netlify values are normalized server-side so pasted whitespace or quotes
  // cannot silently invalidate the CRM authentication header.
  const webhookSecret = cleanEnvironmentValue(process.env.CRM_WEBHOOK_SECRET);
  const crmWebhookUrl = cleanEnvironmentValue(process.env.CRM_WEBHOOK_URL) || DEFAULT_CRM_WEBHOOK_URL;
  if (!webhookSecret) {
    return response(500, { ok: false, error: 'Lead webhook is not configured' }, origin);
  }

  const lead = parseRequestBody(event);
  if (!lead) {
    return response(400, { ok: false, error: 'Invalid JSON payload' }, origin);
  }

  const payload = crmPayload(lead, event);
  if (!payload.first_name || !payload.last_name || !payload.email) {
    return response(422, { ok: false, error: 'First name, last name and email are required' }, origin);
  }

  try {
    const crmResponse = await fetch(crmWebhookUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-webhook-secret': webhookSecret,
      },
      body: JSON.stringify(payload),
    });

    if (!crmResponse.ok) {
      const upstreamMessage = cleanString(await crmResponse.text()).slice(0, 300);
      console.error('CRM webhook rejected lead', {
        status: crmResponse.status,
        response: upstreamMessage || 'No response body',
      });
      return response(502, { ok: false, error: 'CRM webhook rejected the lead' }, origin);
    }

    let crmResult = {};
    try {
      crmResult = await crmResponse.json();
    } catch {
      // A successful CRM response may not include a JSON body.
    }

    return successResponse(crmResult, origin, browserFormSubmission);
  } catch (error) {
    console.error('CRM webhook request failed', { message: error.message || 'Unknown error' });
    return response(502, { ok: false, error: 'CRM webhook request failed' }, origin);
  }
};
