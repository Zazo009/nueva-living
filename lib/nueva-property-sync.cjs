const DEFAULT_PROPERTY_WEBHOOK_URL = 'https://marbella-crm.vercel.app/api/webhook/property';
const DEFAULT_SITE_URL = 'https://nuevaliving.com';
const ALLOWED_AREAS = new Set(['marbella', 'estepona', 'benahavis', 'other']);
const ALLOWED_CONSTRUCTION_STATUSES = new Set(['off_plan', 'under_construction', 'completed']);
const ALLOWED_PROPERTY_TYPES = new Set(['apartment', 'penthouse', 'villa', 'townhouse']);

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

function normalizedText(value) {
  return cleanString(value)
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase();
}

function optionalNumber(value) {
  if (value === '' || value === null || value === undefined) return undefined;
  if (typeof value === 'number') return Number.isFinite(value) ? value : undefined;

  const normalized = cleanString(value)
    .replace(/[^\d,.-]/g, '')
    .replace(/[,.](?=\d{3}(?:\D|$))/g, '')
    .replace(',', '.');
  const number = Number(normalized);
  return Number.isFinite(number) ? number : undefined;
}

function optionalInteger(value) {
  const number = optionalNumber(value);
  return number === undefined ? undefined : Math.max(0, Math.trunc(number));
}

function compactPayload(payload) {
  return Object.fromEntries(Object.entries(payload).filter(([, value]) => {
    if (value === '' || value === undefined || value === null) return false;
    return !Array.isArray(value) || value.length > 0;
  }));
}

function normalizeArea(value, { infer = false } = {}) {
  const text = normalizedText(value);
  if (ALLOWED_AREAS.has(text)) return text;
  if (!infer || !text) return '';
  if (text.includes('estepona') || text.includes('new golden mile')) return 'estepona';
  if (text.includes('benahavis')) return 'benahavis';
  if (text.includes('marbella') || text.includes('nueva andalucia') || text.includes('puerto banus')) {
    return 'marbella';
  }
  return 'other';
}

function normalizeConstructionStatus(value, { infer = false } = {}) {
  const text = normalizedText(value).replace(/[\s-]+/g, '_');
  if (ALLOWED_CONSTRUCTION_STATUSES.has(text)) return text;
  if (!infer || !text) return '';
  if (/under_construction|construction_started|building/.test(text)) return 'under_construction';
  if (/complete|completed|ready|key_ready/.test(text)) return 'completed';
  if (/off_plan|new_development|private_release|launch/.test(text)) return 'off_plan';
  return '';
}

function propertyType(value) {
  const text = normalizedText(value);
  if (!text) return '';
  if (/penthouse|sky villa/.test(text)) return 'penthouse';
  if (/townhouse|town house/.test(text)) return 'townhouse';
  if (/villa/.test(text)) return 'villa';
  if (/apartment|residence|suite|duplex/.test(text)) return 'apartment';
  return '';
}

function normalizePropertyTypes(value) {
  const values = Array.isArray(value) ? value : [value];
  return [...new Set(values.map(propertyType).filter((item) => ALLOWED_PROPERTY_TYPES.has(item)))];
}

function normalizeStringArray(value) {
  if (!Array.isArray(value)) return [];
  return [...new Set(value.map(cleanString).filter(Boolean))];
}

function normalizeDate(value) {
  const text = cleanString(value);
  if (!text) return '';
  if (!/^\d{4}-\d{2}-\d{2}$/.test(text)) return '';
  const date = new Date(`${text}T00:00:00Z`);
  return Number.isNaN(date.getTime()) ? '' : text;
}

function normalizeUrl(value) {
  const text = cleanString(value);
  if (!text) return '';
  try {
    const url = new URL(text);
    return ['http:', 'https:'].includes(url.protocol) ? url.href : '';
  } catch {
    return '';
  }
}

function absoluteAssetUrl(value, siteUrl = DEFAULT_SITE_URL) {
  const text = cleanString(value);
  if (!text) return '';
  const absolute = normalizeUrl(text);
  if (absolute) return absolute;
  return `${siteUrl.replace(/\/+$/, '')}/${text.replace(/^\/+/, '')}`;
}

function parseBedroomRange(value) {
  const numbers = cleanString(value).match(/\d+/g)?.map(Number) || [];
  if (!numbers.length) return {};
  return numbers.length === 1
    ? { min: numbers[0], max: numbers[0] }
    : { min: numbers[0], max: numbers[1] };
}

function quickFact(project, label) {
  const match = (project.quickFacts || []).find(([itemLabel]) => (
    normalizedText(itemLabel) === normalizedText(label)
  ));
  return match?.[1] || '';
}

function firstInteger(value) {
  const match = cleanString(value).match(/\d[\d,.]*/);
  return match ? optionalInteger(match[0]) : undefined;
}

function highestAvailabilityPrice(project) {
  const prices = (project.availability?.units || [])
    .map((unit) => optionalNumber(unit.price))
    .filter((value) => value !== undefined);
  return prices.length ? Math.max(...prices) : undefined;
}

function projectImages(project, siteUrl) {
  const imageSources = [
    project.images?.hero?.src,
    project.images?.architecture?.src,
    project.images?.privateViewing?.src,
    ...(project.media?.items || []).map((item) => item.src),
  ];
  return [...new Set(imageSources.map((src) => absoluteAssetUrl(src, siteUrl)).filter(Boolean))];
}

function normalizePropertyPayload(input, { infer = false } = {}) {
  const rawTypes = Array.isArray(input.property_types) ? input.property_types : [];
  const rawImages = Array.isArray(input.images) ? input.images : [];
  const rawAmenities = Array.isArray(input.amenities) ? input.amenities : [];
  const area = normalizeArea(input.area, { infer });
  const constructionStatus = normalizeConstructionStatus(input.construction_status, { infer });

  return compactPayload({
    name: cleanString(input.name),
    developer: cleanString(input.developer),
    area,
    address: cleanString(input.address),
    description: cleanString(input.description),
    price_min: optionalNumber(input.price_min),
    price_max: optionalNumber(input.price_max),
    currency: cleanString(input.currency || 'EUR').toUpperCase(),
    bedrooms_min: optionalInteger(input.bedrooms_min),
    bedrooms_max: optionalInteger(input.bedrooms_max),
    property_types: normalizePropertyTypes(rawTypes),
    total_units: optionalInteger(input.total_units),
    available_units: optionalInteger(input.available_units),
    delivery_date: normalizeDate(input.delivery_date),
    construction_status: constructionStatus,
    brochure_url: normalizeUrl(input.brochure_url),
    website_url: normalizeUrl(input.website_url),
    images: [...new Set(rawImages.map(normalizeUrl).filter(Boolean))],
    amenities: normalizeStringArray(rawAmenities),
  });
}

function projectToPropertyPayload(project, { siteUrl = DEFAULT_SITE_URL } = {}) {
  const crm = project.crm || {};
  const bedrooms = parseBedroomRange(
    crm.bedrooms
    || project.discovery?.bedrooms
    || project.hero?.type
    || quickFact(project, 'Bedrooms')
  );
  const lifestyleAmenities = (project.lifestyle?.panels || []).map(([title]) => title);
  const totalUnits = crm.totalUnits
    ?? firstInteger(quickFact(project, 'Collection'))
    ?? firstInteger(project.description);
  const availableUnits = crm.availableUnits
    ?? (project.availability?.units?.length || undefined)
    ?? firstInteger(project.discovery?.availability);

  return normalizePropertyPayload({
    name: project.name,
    developer: crm.developer,
    area: crm.area || project.hero?.location || project.card?.label || project.schema?.areaServed,
    address: crm.address,
    description: project.description || project.seoDescription,
    price_min: crm.priceMin ?? project.schema?.price ?? project.discovery?.price,
    price_max: crm.priceMax ?? highestAvailabilityPrice(project),
    currency: crm.currency || project.schema?.priceCurrency || 'EUR',
    bedrooms_min: crm.bedroomsMin ?? bedrooms.min,
    bedrooms_max: crm.bedroomsMax ?? bedrooms.max,
    property_types: crm.propertyTypes || project.discovery?.propertyTypes || [project.hero?.type],
    total_units: totalUnits,
    available_units: availableUnits,
    delivery_date: crm.deliveryDate,
    construction_status: crm.constructionStatus || project.discovery?.status || project.hero?.eyebrow,
    brochure_url: crm.brochureUrl,
    website_url: project.canonical || `${siteUrl.replace(/\/+$/, '')}/${project.output}`,
    images: crm.images || projectImages(project, siteUrl),
    amenities: crm.amenities || lifestyleAmenities,
  }, { infer: true });
}

function validatePropertyPayload(payload, rawInput = payload) {
  const errors = [];
  if (!payload.name) errors.push('name is required');
  if (!payload.area || !ALLOWED_AREAS.has(payload.area)) {
    errors.push(`area must be one of: ${[...ALLOWED_AREAS].join(', ')}`);
  }

  if (rawInput.construction_status && !payload.construction_status) {
    errors.push(`construction_status must be one of: ${[...ALLOWED_CONSTRUCTION_STATUSES].join(', ')}`);
  }

  if (Array.isArray(rawInput.property_types)) {
    const invalidTypes = rawInput.property_types.filter((item) => !propertyType(item));
    if (invalidTypes.length) {
      errors.push(`property_types contains unsupported values: ${invalidTypes.map(cleanString).join(', ')}`);
    }
  } else if (rawInput.property_types !== undefined) {
    errors.push('property_types must be an array');
  }

  if (payload.price_min !== undefined && payload.price_min < 0) errors.push('price_min must be positive');
  if (payload.price_max !== undefined && payload.price_max < 0) errors.push('price_max must be positive');
  if (
    payload.price_min !== undefined
    && payload.price_max !== undefined
    && payload.price_max < payload.price_min
  ) {
    errors.push('price_max must be greater than or equal to price_min');
  }

  if (rawInput.delivery_date && !payload.delivery_date) {
    errors.push('delivery_date must use YYYY-MM-DD');
  }

  if (rawInput.brochure_url && !payload.brochure_url) errors.push('brochure_url must be an HTTP(S) URL');
  if (rawInput.website_url && !payload.website_url) errors.push('website_url must be an HTTP(S) URL');
  if (!/^[A-Z]{3}$/.test(payload.currency || '')) errors.push('currency must be a three-letter code');

  return errors;
}

async function sendPropertyToCrm(
  payload,
  {
    secret,
    webhookUrl = DEFAULT_PROPERTY_WEBHOOK_URL,
    fetchImpl = globalThis.fetch,
  } = {}
) {
  const webhookSecret = cleanEnvironmentValue(secret);
  const normalizedWebhookUrl = normalizeUrl(webhookUrl);
  if (!webhookSecret) throw new Error('CRM_WEBHOOK_SECRET is not configured');
  if (!normalizedWebhookUrl) throw new Error('CRM property webhook URL is invalid');
  if (typeof fetchImpl !== 'function') throw new Error('fetch is not available');

  const crmResponse = await fetchImpl(normalizedWebhookUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-webhook-secret': webhookSecret,
    },
    body: JSON.stringify(payload),
  });

  const responseText = await crmResponse.text();
  let result = {};
  if (responseText) {
    try {
      result = JSON.parse(responseText);
    } catch {
      result = {};
    }
  }

  if (!crmResponse.ok || result.success === false) {
    const detail = cleanString(result.error || responseText).slice(0, 300);
    throw new Error(`CRM property webhook rejected the request (${crmResponse.status})${detail ? `: ${detail}` : ''}`);
  }

  return {
    success: true,
    property_id: cleanString(result.property_id),
    action: ['created', 'updated'].includes(result.action) ? result.action : '',
  };
}

module.exports = {
  ALLOWED_AREAS,
  ALLOWED_CONSTRUCTION_STATUSES,
  ALLOWED_PROPERTY_TYPES,
  DEFAULT_PROPERTY_WEBHOOK_URL,
  DEFAULT_SITE_URL,
  cleanEnvironmentValue,
  normalizePropertyPayload,
  projectToPropertyPayload,
  sendPropertyToCrm,
  validatePropertyPayload,
};
