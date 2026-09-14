const crypto = require('crypto');

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
    // Forwarded rather than dropped here. The CRM treats a filled honeypot as
    // decisive on its own and logs the rejection with the full payload, so a
    // false positive -- a password manager filling a field named "honeypot",
    // say -- can be found and recovered. Dropping it at the edge would return
    // a fake success and lose the enquiry with no record that it existed.
    honeypot: cleanString(lead.honeypot),
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
    // Meta's own cookies, forwarded rather than used here and discarded. The
    // CRM reports stage changes back to Meta months later, and without one of
    // these there is no way to tie a closed sale to the ad that started it.
    meta_fbc: cleanString(lead.meta_fbc),
    meta_fbp: cleanString(lead.meta_fbp),
  });
}

// Locale prefix (es/fr/de/ru/ar) of the page the form was submitted from,
// so browser submissions land on that locale's thank-you page.
function refererLocalePrefix(event) {
  const referer = cleanString(event.headers.referer || event.headers.Referer);
  if (!referer) return '';
  try {
    const match = new URL(referer).pathname.match(/^\/(es|fr|de|ru|ar)\//);
    return match ? `${match[1]}/` : '';
  } catch {
    return '';
  }
}

function successResponse(crmResult, origin, browserFormSubmission, localePrefix = '') {
  if (browserFormSubmission) {
    return {
      statusCode: 303,
      headers: {
        Location: `/${localePrefix}thank-you.html`,
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

// Meta Conversions API: the server-side half of the pixel.
//
// It exists because the browser half is lossy -- an ad blocker, Safari's
// tracking prevention or a dropped request all cost an attributed lead, and at
// these price points there are few enough leads that losing some matters.
//
// Three rules hold it in place:
//
// 1. It never sends without consent. The browser records the visitor's choice
//    and passes it with the lead; anything other than a granted choice returns
//    before a request is built.
// 2. It never sends raw personal data. Email and phone are normalised the way
//    Meta specifies and then SHA-256 hashed, because an unnormalised hash
//    simply never matches. Name, message and nationality are not sent at all.
// 3. It never breaks a lead. The CRM has already accepted the enquiry by the
//    time this runs; it is time-boxed and every failure is swallowed and
//    logged. A visitor must never see an error because Meta was slow.
const META_API_VERSION = 'v21.0';
const META_TIMEOUT_MS = 2500;

const sha256 = (value) => crypto.createHash('sha256').update(String(value)).digest('hex');

// Meta's normalisation, not ours. Lowercase and trimmed for email; digits only
// for phone, which keeps the country code and drops the plus and the spaces.
const normalizedEmail = (value) => cleanString(value).trim().toLowerCase();
const normalizedPhone = (value) => cleanString(value).replace(/\D/g, '');

function metaUserData(lead, event) {
  const userData = {};
  const email = normalizedEmail(lead.email);
  if (email) userData.em = [sha256(email)];
  const phone = normalizedPhone(lead.phone);
  if (phone) userData.ph = [sha256(phone)];

  // The two strongest match signals that are not personal data at all: the
  // pixel's own first-party cookie and the click id Meta puts on the landing
  // URL. Sent verbatim, because Meta matches them unhashed.
  const fbp = cleanString(lead.meta_fbp);
  if (fbp) userData.fbp = fbp;
  const fbc = cleanString(lead.meta_fbc);
  if (fbc) userData.fbc = fbc;

  const ip = cleanString(event.headers['x-nf-client-connection-ip']
    || event.headers['x-forwarded-for']).split(',')[0].trim();
  if (ip) userData.client_ip_address = ip;
  const agent = cleanString(event.headers['user-agent']);
  if (agent) userData.client_user_agent = agent;
  return userData;
}

async function sendMetaConversion(lead, event) {
  const token = cleanEnvironmentValue(process.env.META_CAPI_TOKEN);
  const datasetId = cleanEnvironmentValue(process.env.META_DATASET_ID);
  if (!token || !datasetId) return;

  // Rule 1. Absent or denied both stop here.
  if (cleanString(lead.meta_consent) !== 'granted') return;

  // Rule: without the browser's own event id there is no deduplication, and
  // sending anyway would double-count every lead against the pixel. Better to
  // send nothing than to inflate the number the optimiser bids on.
  const eventId = cleanString(lead.meta_event_id);
  if (!eventId) {
    console.error('Meta CAPI skipped: lead carried no browser event id');
    return;
  }

  const body = {
    data: [{
      event_name: 'Lead',
      event_time: Math.floor(Date.now() / 1000),
      event_id: eventId,
      event_source_url: cleanString(lead.meta_source_url) || undefined,
      action_source: 'website',
      user_data: metaUserData(lead, event),
    }],
    // In the body rather than the query string, so it stays out of any
    // request log that records URLs.
    access_token: token,
  };

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), META_TIMEOUT_MS);
  try {
    const res = await fetch(
      `https://graph.facebook.com/${META_API_VERSION}/${datasetId}/events`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
        signal: controller.signal,
      }
    );
    if (!res.ok) {
      console.error('Meta CAPI rejected event', {
        status: res.status,
        response: cleanString(await res.text()).slice(0, 300),
      });
    }
  } catch (error) {
    console.error('Meta CAPI request failed', { message: error.message || 'Unknown error' });
  } finally {
    clearTimeout(timer);
  }
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

  // The newsletter's own honeypot predates the CRM's and is named `website`.
  // It is still dropped here rather than forwarded: it sits on a footer form
  // that exists on every page, so it attracts the bulk of drive-by submissions
  // and there is nothing in a newsletter signup worth recovering.
  if (cleanString(lead.website)) {
    return response(200, { ok: true, success: true }, origin);
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

    await sendMetaConversion(lead, event);

    return successResponse(crmResult, origin, browserFormSubmission, refererLocalePrefix(event));
  } catch (error) {
    console.error('CRM webhook request failed', { message: error.message || 'Unknown error' });
    return response(502, { ok: false, error: 'CRM webhook request failed' }, origin);
  }
};
