const DEFAULT_ALLOWED_ORIGINS = [
  'https://liora-living.com',
  'https://www.liora-living.com',
];

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
      'Vary': 'Origin',
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

exports.handler = async (event) => {
  const origin = event.headers.origin || event.headers.Origin || '';

  if (event.httpMethod === 'OPTIONS') {
    return response(204, {}, origin);
  }

  if (event.httpMethod !== 'POST') {
    return response(405, { ok: false, error: 'Method not allowed' }, origin);
  }

  const crmWebhookUrl = process.env.CRM_WEBHOOK_URL;
  const webhookSecret = process.env.WEBHOOK_SECRET;

  if (!crmWebhookUrl || !webhookSecret) {
    return response(500, { ok: false, error: 'Lead webhook is not configured' }, origin);
  }

  const lead = safeJson(event.body);
  if (!lead) {
    return response(400, { ok: false, error: 'Invalid JSON payload' }, origin);
  }

  const hasContact = Boolean(lead.email || lead.phone);
  if (!hasContact) {
    return response(422, { ok: false, error: 'Lead requires email or phone' }, origin);
  }

  const enrichedLead = {
    ...lead,
    source: lead.source || 'liora-living',
    received_at: new Date().toISOString(),
    metadata: {
      ...(lead.metadata || {}),
      ip: event.headers['x-nf-client-connection-ip'] || event.headers['client-ip'] || '',
      user_agent: event.headers['user-agent'] || '',
      origin,
    },
  };

  try {
    const crmResponse = await fetch(crmWebhookUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${webhookSecret}`,
        'X-Liora-Webhook-Secret': webhookSecret,
      },
      body: JSON.stringify(enrichedLead),
    });

    if (!crmResponse.ok) {
      return response(
        502,
        { ok: false, error: 'CRM webhook rejected the lead', status: crmResponse.status },
        origin,
      );
    }

    return response(200, { ok: true }, origin);
  } catch (error) {
    return response(502, { ok: false, error: error.message || 'CRM webhook request failed' }, origin);
  }
};
