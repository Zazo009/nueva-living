// One place that talks to Meta's Conversions API.
//
// Two callers send events: nueva-lead when an enquiry arrives, and
// nueva-crm-event when that enquiry later becomes a viewing or a reservation.
// They share this because the parts that are easy to get wrong -- the
// normalisation before hashing, the timeout, never throwing -- should be got
// right once rather than twice.
const crypto = require('crypto');

const API_VERSION = 'v21.0';
const TIMEOUT_MS = 2500;

const clean = (value) => String(value ?? '').replace(/\s+/g, ' ').trim();
const sha256 = (value) => crypto.createHash('sha256').update(String(value)).digest('hex');

// Meta's normalisation, not ours. An unnormalised hash is a valid hash of the
// wrong string: it is accepted, it matches nobody, and nothing reports an
// error -- which is the worst way for this to fail.
const normalizedEmail = (value) => clean(value).trim().toLowerCase();
const normalizedPhone = (value) => clean(value).replace(/\D/g, '');

// Raw personal data never leaves here. Email and phone are hashed; the cookie
// values and the request metadata are not personal data and Meta matches them
// as they are.
function hashedUserData({ email, phone, fbp, fbc, ip, userAgent } = {}) {
  const userData = {};
  const em = normalizedEmail(email);
  if (em) userData.em = [sha256(em)];
  const ph = normalizedPhone(phone);
  if (ph) userData.ph = [sha256(ph)];
  const p = clean(fbp);
  if (p) userData.fbp = p;
  const c = clean(fbc);
  if (c) userData.fbc = c;
  const addr = clean(ip).split(',')[0].trim();
  if (addr) userData.client_ip_address = addr;
  const agent = clean(userAgent);
  if (agent) userData.client_user_agent = agent;
  return userData;
}

// Always resolves. A slow or unhappy Meta must never be able to fail the
// request that triggered it -- a lead is worth more than its measurement.
async function sendMetaEvent({
  token, datasetId, eventName, eventId, eventTime, sourceUrl,
  actionSource = 'website', userData = {}, customData, label = 'Meta CAPI',
}) {
  if (!token || !datasetId || !eventName) return { sent: false, reason: 'not configured' };
  if (!Object.keys(userData).length) return { sent: false, reason: 'no matchable user data' };

  const event = {
    event_name: eventName,
    event_time: eventTime || Math.floor(Date.now() / 1000),
    action_source: actionSource,
    user_data: userData,
  };
  if (eventId) event.event_id = eventId;
  if (sourceUrl) event.event_source_url = sourceUrl;
  if (customData && Object.keys(customData).length) event.custom_data = customData;

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);
  try {
    const res = await fetch(`https://graph.facebook.com/${API_VERSION}/${datasetId}/events`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      // In the body, not the query string, so it stays out of URL logs.
      body: JSON.stringify({ data: [event], access_token: token }),
      signal: controller.signal,
    });
    if (!res.ok) {
      console.error(`${label} rejected event`, {
        event: eventName,
        status: res.status,
        response: clean(await res.text()).slice(0, 300),
      });
      return { sent: false, reason: `http ${res.status}` };
    }
    return { sent: true };
  } catch (error) {
    console.error(`${label} request failed`, { event: eventName, message: error.message || 'Unknown error' });
    return { sent: false, reason: 'request failed' };
  } finally {
    clearTimeout(timer);
  }
}

module.exports = { clean, sha256, normalizedEmail, normalizedPhone, hashedUserData, sendMetaEvent };
