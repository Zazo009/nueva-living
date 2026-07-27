const DEFAULT_TRACKING_URL = 'https://marbella-crm.vercel.app/api/track';
const MAX_BODY_BYTES = 64 * 1024;

function json(statusCode, body) {
  return {
    statusCode,
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': 'no-store',
    },
    body: JSON.stringify(body),
  };
}

function cleanEnvironmentValue(value) {
  const cleaned = typeof value === 'string' ? value.trim() : '';
  if (cleaned.length < 2) return cleaned;
  const first = cleaned[0];
  const last = cleaned[cleaned.length - 1];
  return first === last && (first === '"' || first === "'")
    ? cleaned.slice(1, -1).trim()
    : cleaned;
}

function parsePayload(body) {
  try {
    const payload = JSON.parse(body || '{}');
    if (!payload || Array.isArray(payload) || typeof payload !== 'object') return null;
    return payload;
  } catch {
    return null;
  }
}

exports.handler = async (event) => {
  if (event.httpMethod === 'OPTIONS') {
    return json(204, {});
  }

  if (event.httpMethod !== 'POST') {
    return json(405, { ok: false, error: 'Method not allowed' });
  }

  if (Buffer.byteLength(event.body || '', 'utf8') > MAX_BODY_BYTES) {
    return json(413, { ok: false, error: 'Payload too large' });
  }

  const payload = parsePayload(event.body);
  if (!payload || typeof payload.type !== 'string' || typeof payload.session_id !== 'string') {
    return json(400, { ok: false, error: 'Invalid tracking payload' });
  }

  const trackingUrl = cleanEnvironmentValue(process.env.CRM_TRACKING_URL) || DEFAULT_TRACKING_URL;

  try {
    const upstream = await fetch(trackingUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
      signal: AbortSignal.timeout(5000),
    });

    if (!upstream.ok) {
      console.error('CRM tracking endpoint rejected event', {
        status: upstream.status,
        type: payload.type.slice(0, 80),
      });
      return json(502, { ok: false });
    }

    return json(200, { ok: true });
  } catch (error) {
    console.error('CRM tracking request failed', {
      message: error?.message || 'Unknown error',
      type: payload.type.slice(0, 80),
    });
    return json(502, { ok: false });
  }
};
