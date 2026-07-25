const { timingSafeEqual } = require('node:crypto');
const {
  DEFAULT_PROPERTY_WEBHOOK_URL,
  cleanEnvironmentValue,
  normalizePropertyPayload,
  sendPropertyToCrm,
  validatePropertyPayload,
} = require('../../lib/nueva-property-sync.cjs');

const DEFAULT_ALLOWED_ORIGINS = [
  'https://nuevaliving.com',
  'https://www.nuevaliving.com',
];

function cleanString(value) {
  return typeof value === 'string' ? value.replace(/\s+/g, ' ').trim() : '';
}

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
      'Access-Control-Allow-Headers': 'Content-Type, X-Property-Sync-Token',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Cache-Control': 'no-store',
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

function equalTokens(provided, expected) {
  const providedBuffer = Buffer.from(provided);
  const expectedBuffer = Buffer.from(expected);
  return providedBuffer.length === expectedBuffer.length
    && timingSafeEqual(providedBuffer, expectedBuffer);
}

function isAuthorized(event) {
  if (event.clientContext?.user) return true;

  const expectedToken = cleanEnvironmentValue(process.env.PROPERTY_SYNC_TOKEN);
  const providedToken = cleanString(
    event.headers['x-property-sync-token']
    || event.headers['X-Property-Sync-Token']
  );
  return Boolean(expectedToken && providedToken && equalTokens(providedToken, expectedToken));
}

exports.handler = async (event) => {
  const origin = event.headers.origin || event.headers.Origin || '';

  if (event.httpMethod === 'OPTIONS') {
    return response(204, {}, origin);
  }

  if (event.httpMethod !== 'POST') {
    return response(405, { ok: false, error: 'Method not allowed' }, origin);
  }

  if (!isAuthorized(event)) {
    return response(401, { ok: false, error: 'Unauthorized property sync request' }, origin);
  }

  const crmWebhookSecret = cleanEnvironmentValue(process.env.CRM_WEBHOOK_SECRET);
  const crmWebhookUrl = cleanEnvironmentValue(process.env.CRM_PROPERTY_WEBHOOK_URL)
    || DEFAULT_PROPERTY_WEBHOOK_URL;
  if (!crmWebhookSecret) {
    return response(500, { ok: false, error: 'Property webhook is not configured' }, origin);
  }

  const requestBody = safeJson(event.body);
  if (!requestBody || Array.isArray(requestBody)) {
    return response(400, { ok: false, error: 'Invalid JSON payload' }, origin);
  }

  const property = requestBody.property && typeof requestBody.property === 'object'
    ? requestBody.property
    : requestBody;
  const payload = normalizePropertyPayload(property);
  const errors = validatePropertyPayload(payload, property);
  if (errors.length) {
    return response(422, { ok: false, error: errors.join('; ') }, origin);
  }

  try {
    const result = await sendPropertyToCrm(payload, {
      secret: crmWebhookSecret,
      webhookUrl: crmWebhookUrl,
    });

    return response(200, {
      ok: true,
      success: true,
      property_id: result.property_id,
      action: result.action,
    }, origin);
  } catch (error) {
    console.error('CRM property webhook request failed', {
      name: payload.name,
      area: payload.area,
      message: error.message || 'Unknown error',
    });
    return response(502, { ok: false, error: 'CRM property webhook request failed' }, origin);
  }
};
