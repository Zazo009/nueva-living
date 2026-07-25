import assert from 'node:assert/strict';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const propertySync = require('../lib/nueva-property-sync.cjs');

const project = {
  name: 'Sunset Villas',
  output: 'property-sunset-villas.html',
  canonical: 'https://nuevaliving.com/property-sunset-villas.html',
  description: 'Luxury villas with sea views.',
  schema: {
    price: 850000,
    priceCurrency: 'EUR'
  },
  crm: {
    developer: 'Prime Invest',
    area: 'marbella',
    address: 'Calle del Mar 12',
    priceMax: 1500000,
    bedroomsMin: 3,
    bedroomsMax: 5,
    propertyTypes: ['villa'],
    totalUnits: 12,
    availableUnits: 8,
    deliveryDate: '2026-06-01',
    constructionStatus: 'off_plan',
    brochureUrl: 'https://nuevaliving.com/assets/sunset-villas-brochure.pdf',
    amenities: ['pool', 'gym', 'parking']
  },
  images: {
    hero: { src: 'assets/sunset-villas/hero.jpg' }
  }
};

const payload = propertySync.projectToPropertyPayload(project);
assert.deepEqual(payload, {
  name: 'Sunset Villas',
  developer: 'Prime Invest',
  area: 'marbella',
  address: 'Calle del Mar 12',
  description: 'Luxury villas with sea views.',
  price_min: 850000,
  price_max: 1500000,
  currency: 'EUR',
  bedrooms_min: 3,
  bedrooms_max: 5,
  property_types: ['villa'],
  total_units: 12,
  available_units: 8,
  delivery_date: '2026-06-01',
  construction_status: 'off_plan',
  brochure_url: 'https://nuevaliving.com/assets/sunset-villas-brochure.pdf',
  website_url: 'https://nuevaliving.com/property-sunset-villas.html',
  images: ['https://nuevaliving.com/assets/sunset-villas/hero.jpg'],
  amenities: ['pool', 'gym', 'parking']
});
assert.deepEqual(propertySync.validatePropertyPayload(payload, payload), []);

let forwardedRequest;
const crmResult = await propertySync.sendPropertyToCrm(payload, {
  secret: 'test-secret',
  fetchImpl: async (url, options) => {
    forwardedRequest = { url, options };
    return {
      ok: true,
      status: 200,
      text: async () => JSON.stringify({
        success: true,
        property_id: 'property-123',
        action: 'created'
      })
    };
  }
});

assert.equal(forwardedRequest.url, propertySync.DEFAULT_PROPERTY_WEBHOOK_URL);
assert.equal(forwardedRequest.options.headers['x-webhook-secret'], 'test-secret');
assert.deepEqual(JSON.parse(forwardedRequest.options.body), payload);
assert.deepEqual(crmResult, {
  success: true,
  property_id: 'property-123',
  action: 'created'
});

const invalidPayload = propertySync.normalizePropertyPayload({
  name: 'Invalid Area Project',
  area: 'malaga',
  property_types: ['castle'],
  construction_status: 'planning'
});
const invalidErrors = propertySync.validatePropertyPayload(invalidPayload, {
  name: 'Invalid Area Project',
  area: 'malaga',
  property_types: ['castle'],
  construction_status: 'planning'
});
assert.equal(invalidErrors.length, 3);

const originalFetch = globalThis.fetch;
const originalSecret = process.env.CRM_WEBHOOK_SECRET;
const originalSyncToken = process.env.PROPERTY_SYNC_TOKEN;
globalThis.fetch = async () => ({
  ok: true,
  status: 200,
  text: async () => JSON.stringify({
    success: true,
    property_id: 'property-456',
    action: 'updated'
  })
});
process.env.CRM_WEBHOOK_SECRET = 'test-secret';
process.env.PROPERTY_SYNC_TOKEN = 'admin-sync-token';

const { handler } = require('../netlify/functions/nueva-property.js');
const unauthorizedResponse = await handler({
  httpMethod: 'POST',
  headers: {},
  body: JSON.stringify(payload)
});
assert.equal(unauthorizedResponse.statusCode, 401);

const authorizedResponse = await handler({
  httpMethod: 'POST',
  headers: {
    'content-type': 'application/json',
    'x-property-sync-token': 'admin-sync-token'
  },
  body: JSON.stringify(payload)
});
assert.equal(authorizedResponse.statusCode, 200);
assert.deepEqual(JSON.parse(authorizedResponse.body), {
  ok: true,
  success: true,
  property_id: 'property-456',
  action: 'updated'
});

globalThis.fetch = originalFetch;
if (originalSecret === undefined) delete process.env.CRM_WEBHOOK_SECRET;
else process.env.CRM_WEBHOOK_SECRET = originalSecret;
if (originalSyncToken === undefined) delete process.env.PROPERTY_SYNC_TOKEN;
else process.env.PROPERTY_SYNC_TOKEN = originalSyncToken;

console.log('Property CRM sync tests passed.');
