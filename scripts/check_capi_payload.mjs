// Fails if a CRM stage update would reach Meta in the wrong shape.
//
// Meta's Conversion Leads spec names three values exactly, and they are the
// difference between events Meta credits to the lead ads that produced them
// and events it merely accepts: action_source "system_generated",
// custom_data.event_source "crm", and custom_data.lead_event_source naming the
// tool. We sent action_source "other" and neither custom_data field for as
// long as the endpoint had existed. Nothing reported an error -- the API
// answers 200 either way -- so the only symptom was attribution that never
// arrived.
//
// lead_id is checked on the serialised bytes rather than on the object,
// because that is where it can go wrong: Meta types it as an integer, it runs
// to 17 digits, and about half of those do not survive a round trip through a
// JavaScript double. An off-by-one lead ID is not an error anywhere either.
//
// This drives the real handler with the network stubbed, so it checks what
// Meta would receive and not what the source says.
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);

// A 17-digit ID chosen because Number() rounds it: 16418614712855791 comes
// back as ...792. If the guard ever passes with that value corrupted, the
// serialiser has been replaced by a plain JSON.stringify.
const LEAD_ID = '16418614712855791';
const SECRET = 'guard-secret';

process.env.CRM_WEBHOOK_SECRET = SECRET;
process.env.META_CAPI_TOKEN = 'guard-token';
process.env.META_DATASET_ID = 'guard-dataset';

let body = null;
globalThis.fetch = async (_url, options) => {
  body = options.body;
  return { ok: true, status: 200, text: async () => '' };
};

const { handler } = require('../netlify/functions/nueva-crm-event.js');

const response = await handler({
  httpMethod: 'POST',
  headers: { 'x-webhook-secret': SECRET },
  body: JSON.stringify({
    stage: 'reserved',
    email: 'guard@example.com',
    phone: '+34600112233',
    meta_lead_id: LEAD_ID,
    fbc: 'fb.1.1.abc',
    fbp: 'fb.1.1.xyz',
    value: 676000,
    currency: 'EUR',
    occurred_at: Math.floor(Date.now() / 1000) - 3600,
  }),
});

const failures = [];
const expect = (ok, detail) => { if (!ok) failures.push(detail); };

expect(response.statusCode === 200, `handler answered ${response.statusCode}, not 200`);
expect(body !== null, 'the handler never called Meta');

if (body) {
  const event = JSON.parse(body).data[0];
  expect(
    event.action_source === 'system_generated',
    `action_source is "${event.action_source}", and Meta's spec names "system_generated" for every Conversion Leads event`,
  );
  const custom = event.custom_data ?? {};
  expect(
    custom.event_source === 'crm',
    `custom_data.event_source is "${custom.event_source}", and the spec names "crm"`,
  );
  expect(
    typeof custom.lead_event_source === 'string' && custom.lead_event_source.trim().length > 0,
    'custom_data.lead_event_source is missing, and the spec asks for the name of the tool the leads come from',
  );
  // On the bytes, not the parsed object: parsing is itself a round trip
  // through a double and would hide exactly the fault being looked for.
  expect(
    body.includes(`"lead_id":${LEAD_ID}`),
    `lead_id did not leave as the exact digits ${LEAD_ID}. It is either quoted as a string, which is not the type Meta asks for, or rounded by a double`,
  );
}

if (failures.length) {
  console.error(`\nCRM events would reach Meta in the wrong shape (${failures.length}):\n`);
  for (const failure of failures) console.error(`  ${failure}`);
  console.error('\nSee the Conversion Leads payload specification. Meta answers 200 to a');
  console.error('malformed event, so nothing else will tell you.\n');
  process.exit(1);
}

console.log('CRM events to Meta: system_generated, crm, lead_event_source and an exact 17-digit lead_id.');
