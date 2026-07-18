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

function compactPayload(payload) {
  return Object.fromEntries(Object.entries(payload).filter(([, value]) => {
    if (value === '' || value === undefined || value === null) return false;
    return !Array.isArray(value) || value.length > 0;
  }));
}

function crmPayload(lead) {
  return compactPayload({
    first_name: cleanString(lead.first_name),
    last_name: cleanString(lead.last_name),
    email: cleanString(lead.email),
    phone: cleanString(lead.phone),
    budget_min: optionalNumber(lead.budget_min),
    budget_max: optionalNumber(lead.budget_max),
    preferred_areas: allowedValues(lead.preferred_areas, ALLOWED_AREAS),
    property_types: allowedValues(lead.property_types, ALLOWED_PROPERTY_TYPES),
    bedrooms_min: optionalNumber(lead.bedrooms_min),
    bedrooms_max: optionalNumber(lead.bedrooms_max),
    nationality: cleanString(lead.nationality),
    message: cleanString(lead.message),
    consent: optionalBoolean(lead.consent),
    consent_text: cleanString(lead.consent_text),
    marketing_opt_in: optionalBoolean(lead.marketing_opt_in),
    source_page: cleanString(lead.source_page),
    utm_source: cleanString(lead.utm_source),
    utm_campaign: cleanString(lead.utm_campaign),
  });
}

exports.handler = async (event) => {
  const origin = event.headers.origin || event.headers.Origin || '';

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

  const lead = safeJson(event.body);
  if (!lead) {
    return response(400, { ok: false, error: 'Invalid JSON payload' }, origin);
  }

  const payload = crmPayload(lead);
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

    return response(200, {
      ok: true,
      success: true,
      lead_id: cleanString(crmResult.lead_id),
    }, origin);
  } catch (error) {
    console.error('CRM webhook request failed', { message: error.message || 'Unknown error' });
    return response(502, { ok: false, error: 'CRM webhook request failed' }, origin);
  }
};
