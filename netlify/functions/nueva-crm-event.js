// What the CRM knows, sent back to Meta.
//
// Meta knows which leads it delivered. The CRM knows which of them became a
// viewing and which became a reservation. Until the second reaches the first,
// Meta optimises toward form-fills forever -- and form-fills are exactly what
// it is best at finding cheaply, which is how an account ends up with fifty
// enquiries a month and no viewings.
//
// This endpoint is how the loop closes. The CRM calls it when a lead changes
// stage; the person is matched to Meta by hashed email and phone, the same way
// the original Lead event was, so the conversion lands against the ad that
// produced it however many weeks earlier.
//
// Purchase carries the value. That is the point: given a number, Meta can bid
// toward revenue rather than toward volume, which for homes between EUR
// 269,000 and EUR 14,600,000 is a different business entirely.
const { clean, hashedUserData, sendMetaEvent } = require('./lib/meta-capi');

// Meta rejects an event older than seven days on this endpoint.
const MAX_AGE_SECONDS = 7 * 24 * 60 * 60;

// The CRM's vocabulary, mapped onto Meta's. Schedule and Purchase are standard
// events the optimiser understands; a qualified lead has no standard
// equivalent, so it goes as a custom event -- usable as an audience and as a
// signal, without pretending to be a sale.
const STAGES = {
  qualified: { event: 'LeadQualified' },
  viewing_booked: { event: 'Schedule' },
  viewing: { event: 'Schedule' },
  reserved: { event: 'Purchase', wantsValue: true },
  reservation: { event: 'Purchase', wantsValue: true },
};

function reply(statusCode, body) {
  return {
    statusCode,
    headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' },
    body: JSON.stringify(body),
  };
}

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') return reply(405, { ok: false, error: 'Method not allowed' });

  const secret = clean(process.env.CRM_WEBHOOK_SECRET);
  const provided = clean(event.headers['x-webhook-secret'] || event.headers['X-Webhook-Secret']);
  // Same shared secret the site already uses to authenticate to the CRM. The
  // direction is reversed here, but the trust boundary is the same two parties.
  if (!secret || provided !== secret) return reply(401, { ok: false, error: 'Unauthorized' });

  let body;
  try {
    body = JSON.parse(event.body || '{}');
  } catch {
    return reply(400, { ok: false, error: 'Invalid JSON payload' });
  }

  const stage = clean(body.stage).toLowerCase().replace(/[\s-]+/g, '_');
  const mapping = STAGES[stage];
  // A lead going cold is not an event. Meta has no use for it and sending one
  // would only teach the optimiser that something happened.
  if (!mapping) return reply(200, { ok: true, sent: false, reason: `stage "${stage}" is not reported` });

  const userData = hashedUserData({ email: body.email, phone: body.phone });
  if (!Object.keys(userData).length) {
    return reply(422, { ok: false, error: 'An email or phone number is required to match the person' });
  }

  const now = Math.floor(Date.now() / 1000);
  const occurred = Number(body.occurred_at);
  let eventTime = Number.isFinite(occurred) && occurred > 0 ? Math.floor(occurred) : now;
  if (now - eventTime > MAX_AGE_SECONDS) {
    console.error('CRM event older than Meta accepts, sending as now', { stage, eventTime });
    eventTime = now;
  }
  if (eventTime > now) eventTime = now;

  const customData = {};
  if (mapping.wantsValue) {
    const value = Number(body.value);
    if (Number.isFinite(value) && value > 0) {
      customData.value = value;
      customData.currency = clean(body.currency).toUpperCase() || 'EUR';
    }
  }
  const project = clean(body.project);
  if (project) customData.content_name = project.slice(0, 100);

  const result = await sendMetaEvent({
    token: clean(process.env.META_CAPI_TOKEN),
    datasetId: clean(process.env.META_DATASET_ID),
    eventName: mapping.event,
    // The CRM's own id for this stage change, so a retry cannot double-count.
    eventId: clean(body.event_id) || undefined,
    eventTime,
    // Not a browser: this happened in a CRM, days or weeks after the click.
    actionSource: 'other',
    userData,
    customData,
    label: 'Meta CRM event',
  });

  return reply(200, { ok: true, event: mapping.event, ...result });
};
