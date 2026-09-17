// Unsubscribe.
//
// Gmail and Yahoo have required this of bulk senders since February 2024: a
// List-Unsubscribe header, a List-Unsubscribe-Post header, and an endpoint
// that honours a single POST without asking the person anything further. A
// sender without one is filtered on reputation regardless of how correct its
// DKIM and SPF are, so this is not a courtesy -- it is a delivery requirement.
//
// The CRM sends the mail; this endpoint receives the click. That split is
// deliberate. The unsubscribe link has to survive in a mailbox for months and
// be reachable by a mail provider's own servers, so it belongs on the public
// site rather than behind whatever the CRM is doing that week.
//
// GET does not unsubscribe. Mail scanners and link prefetchers follow every
// URL in a message, and a destructive GET means the diligent ones silently
// unsubscribe people who never clicked. GET renders a confirmation page whose
// button POSTs; the one-click header posts directly. Both land on the same
// POST branch, which is the only thing that changes any state.
const crypto = require('crypto');

const DEFAULT_CRM_UNSUBSCRIBE_URL = 'https://marbella-crm.vercel.app/api/webhook/unsubscribe';

// Long enough that guessing one is hopeless, short enough to keep the link
// from wrapping in a plain-text footer.
const TOKEN_LENGTH = 32;

function clean(value) {
  return typeof value === 'string' ? value.trim() : '';
}

// Matches the CRM's own normalisation so the same address always produces the
// same token, whatever casing the list carries it in.
function normalizedEmail(value) {
  return clean(value).toLowerCase();
}

function expectedToken(email, secret) {
  return crypto
    .createHmac('sha256', secret)
    .update(normalizedEmail(email))
    .digest('hex')
    .slice(0, TOKEN_LENGTH);
}

// Constant-time, and length-safe: timingSafeEqual throws on a length mismatch
// rather than returning false, which would turn a malformed token into a 500.
function tokenMatches(provided, expected) {
  const a = Buffer.from(provided);
  const b = Buffer.from(expected);
  if (a.length !== b.length) return false;
  return crypto.timingSafeEqual(a, b);
}

function decodeEmail(encoded) {
  try {
    return clean(Buffer.from(encoded, 'base64url').toString('utf8'));
  } catch {
    return '';
  }
}

function json(statusCode, body) {
  return {
    statusCode,
    headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' },
    body: JSON.stringify(body),
  };
}

function page(statusCode, { heading, body, form }) {
  const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>${heading} — Nueva Living</title>
<style>
  :root {
    --deep: #2f2417;
    --cream: #f4ead9;
    --ivory: #faf6ee;
    --gold: #a8834a;
    --gold-light: #c7a36b;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 24px;
    background: var(--deep);
    color: var(--cream);
    font-family: "Montserrat", Arial, sans-serif;
    line-height: 1.6;
  }
  main { max-width: 34rem; text-align: center; }
  .mark {
    font-family: "Cinzel", Georgia, serif;
    font-size: 0.75rem;
    letter-spacing: 0.34em;
    text-transform: uppercase;
    color: var(--gold-light);
    margin: 0 0 2.5rem;
  }
  h1 {
    font-family: "Cinzel", Georgia, serif;
    font-weight: 400;
    font-size: clamp(1.6rem, 5vw, 2.3rem);
    line-height: 1.25;
    margin: 0 0 1.1rem;
  }
  p { margin: 0 0 1.6rem; color: #d9cbb4; }
  .addr { color: var(--cream); overflow-wrap: anywhere; }
  button {
    font: inherit;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    font-size: 0.78rem;
    padding: 0.95rem 2.4rem;
    color: var(--deep);
    background: var(--gold-light);
    border: 1px solid var(--gold-light);
    cursor: pointer;
  }
  button:hover { background: var(--cream); border-color: var(--cream); }
  button:focus-visible { outline: 2px solid var(--cream); outline-offset: 3px; }
  a { color: var(--gold-light); }
  .foot { margin: 2.6rem 0 0; font-size: 0.8rem; color: #a8977d; }
</style>
</head>
<body>
<main>
  <p class="mark">Nueva Living</p>
  <h1>${heading}</h1>
  ${body}
  ${form || ''}
  <p class="foot"><a href="https://nuevaliving.com">nuevaliving.com</a></p>
</main>
</body>
</html>`;

  return {
    statusCode,
    headers: { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store' },
    body: html,
  };
}

function escapeHtml(value) {
  return value.replace(/[&<>"']/g, (ch) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
  })[ch]);
}

// The CRM owns the list, so it owns suppression. This endpoint's job is to
// deliver the fact reliably and to say so honestly if it could not: a person
// told they are unsubscribed who then receives the next send is a complaint,
// which costs far more than an error page.
async function notifyCrm(email, secret) {
  const url = clean(process.env.CRM_UNSUBSCRIBE_URL) || DEFAULT_CRM_UNSUBSCRIBE_URL;

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 5000);
  try {
    const res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'x-webhook-secret': secret },
      body: JSON.stringify({ email: normalizedEmail(email), unsubscribed_at: new Date().toISOString() }),
      signal: controller.signal,
    });
    if (!res.ok) {
      console.error('CRM rejected unsubscribe', { status: res.status });
      return false;
    }
    return true;
  } catch (error) {
    console.error('CRM unsubscribe request failed', { message: error.message });
    return false;
  } finally {
    clearTimeout(timeout);
  }
}

exports.handler = async (event) => {
  const method = event.httpMethod;
  if (method !== 'GET' && method !== 'POST') {
    return json(405, { ok: false, error: 'Method not allowed' });
  }

  const unsubscribeSecret = clean(process.env.UNSUBSCRIBE_SECRET);
  const webhookSecret = clean(process.env.CRM_WEBHOOK_SECRET);
  if (!unsubscribeSecret || !webhookSecret) {
    console.error('Unsubscribe is not configured', {
      hasUnsubscribeSecret: Boolean(unsubscribeSecret),
      hasWebhookSecret: Boolean(webhookSecret),
    });
    return method === 'GET'
      ? page(500, {
          heading: 'Something went wrong',
          body: '<p>We could not process this request. Please email <a href="mailto:contact@nuevaliving.com">contact@nuevaliving.com</a> and we will remove you by hand.</p>',
        })
      : json(500, { ok: false, error: 'Unsubscribe is not configured' });
  }

  const params = event.queryStringParameters || {};
  const email = decodeEmail(clean(params.e));
  const token = clean(params.t);

  // A bad token is indistinguishable from a tampered one, and both get the
  // same answer. Naming the address back would let anyone with the link
  // confirm it exists.
  if (!email || !token || !tokenMatches(token, expectedToken(email, unsubscribeSecret))) {
    return method === 'GET'
      ? page(400, {
          heading: 'This link is not valid',
          body: '<p>It may have been altered on its way here, or truncated by a mail client. Email <a href="mailto:contact@nuevaliving.com">contact@nuevaliving.com</a> and we will remove you by hand.</p>',
        })
      : json(400, { ok: false, error: 'Invalid unsubscribe link' });
  }

  if (method === 'GET') {
    const query = `e=${encodeURIComponent(clean(params.e))}&t=${encodeURIComponent(token)}`;
    return page(200, {
      heading: 'Unsubscribe from our emails?',
      body: `<p>We will stop sending property updates to <span class="addr">${escapeHtml(email)}</span>.</p>`,
      form: `<form method="POST" action="/unsubscribe?${escapeHtml(query)}"><button type="submit">Unsubscribe</button></form>`,
    });
  }

  const delivered = await notifyCrm(email, webhookSecret);

  // RFC 8058: the provider treats any 2xx as success and shows the person it
  // worked, so a failure here must not return 200 -- otherwise the only record
  // of the request is a log line nobody reads.
  if (!delivered) {
    return page(502, {
      heading: 'We could not complete that',
      body: '<p>Please try again in a moment, or email <a href="mailto:contact@nuevaliving.com">contact@nuevaliving.com</a> and we will remove you by hand.</p>',
    });
  }

  return page(200, {
    heading: 'You are unsubscribed',
    body: `<p>We have removed <span class="addr">${escapeHtml(email)}</span> from our mailing list. You will not receive further property updates from us.</p>`,
  });
};
