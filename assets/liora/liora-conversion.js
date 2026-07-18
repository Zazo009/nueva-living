(() => {
  const site = {
    whatsappNumber: '46707576709',
    brand: 'Nueva Living',
    crmWebhookUrl: window.NUEVA_CRM_WEBHOOK_URL || '/.netlify/functions/nueva-lead'
  };

  const params = new URLSearchParams(window.location.search);
  const pageTitle = document.title.replace(/\s*\|\s*Nueva Living\s*$/i, '').trim();
  const pagePath = window.location.pathname || '/';
  const pageContext = document.body?.dataset?.projectName || params.get('project') || pageTitle || 'Nueva Living enquiry';
  const intentFromUrl = params.get('intent') || '';

  window.dataLayer = window.dataLayer || [];

  function clean(value) {
    return String(value || '').replace(/\s+/g, ' ').trim();
  }

  function readField(form, selectors) {
    const field = selectors
      .split(',')
      .map((selector) => form.querySelector(selector.trim()))
      .find(Boolean);
    return clean(field?.value);
  }

  function readChecked(form, selectors) {
    const field = selectors
      .split(',')
      .map((selector) => form.querySelector(selector.trim()))
      .find(Boolean);
    return Boolean(field?.checked);
  }

  function splitName(fullName) {
    const parts = clean(fullName).split(' ').filter(Boolean);
    if (!parts.length) return { firstName: '', lastName: '' };
    if (parts.length === 1) return { firstName: parts[0], lastName: '' };
    return {
      firstName: parts.slice(0, -1).join(' '),
      lastName: parts.slice(-1).join(' ')
    };
  }

  const validAreas = ['marbella', 'estepona', 'benahavis', 'other'];
  const validPropertyTypes = ['villa', 'apartment', 'penthouse', 'townhouse', 'duplex'];

  function normalizedText(value) {
    return clean(value)
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .toLowerCase();
  }

  function unique(values) {
    return [...new Set(values.filter(Boolean))];
  }

  function normalizeAreas(value) {
    const text = normalizedText(value);
    if (!text) return [];
    if (/open to all|all areas|mixed/.test(text)) return [...validAreas];

    const areas = [];
    if (text.includes('marbella')) areas.push('marbella');
    if (text.includes('estepona') || text.includes('new golden mile')) areas.push('estepona');
    if (text.includes('benahavis')) areas.push('benahavis');
    if (!areas.length || /nueva andalucia|mijas|fuengirola|costa del sol|other/.test(text)) areas.push('other');
    return unique(areas);
  }

  function normalizePropertyTypes(value) {
    const text = normalizedText(value);
    if (!text) return [];
    if (/mixed|open/.test(text)) return [...validPropertyTypes];

    const types = [];
    if (text.includes('villa')) types.push('villa');
    if (/apartment|suite|garden residence/.test(text)) types.push('apartment');
    if (text.includes('penthouse')) types.push('penthouse');
    if (text.includes('townhouse')) types.push('townhouse');
    if (text.includes('duplex')) types.push('duplex');
    return unique(types);
  }

  function parseNumberRange(value) {
    const numbers = clean(value).match(/\d+/g)?.map(Number).filter(Number.isFinite) || [];
    return {
      min: numbers[0] || '',
      max: numbers[1] || numbers[0] || ''
    };
  }

  function compactPayload(payload) {
    return Object.fromEntries(Object.entries(payload).filter(([, value]) => {
      if (value === '' || value === undefined || value === null) return false;
      return !Array.isArray(value) || value.length > 0;
    }));
  }

  function parseBudgetRange(value) {
    const text = clean(value);
    const numbers = [...text.matchAll(/[\d,.]+/g)]
      .map((match) => Number(match[0].replace(/[,.](?=\d{3}\b)/g, '').replace(',', '.')))
      .filter(Number.isFinite);

    if (!numbers.length) return { min: '', max: '' };
    if (/\+/.test(text) || numbers.length === 1) return { min: numbers[0], max: '' };
    return { min: numbers[0], max: numbers[1] || '' };
  }

  function track(eventName, payload = {}) {
    const detail = {
      event: eventName,
      page_path: pagePath,
      page_title: document.title,
      context: pageContext,
      ...payload
    };
    window.dataLayer.push(detail);
    window.dispatchEvent(new CustomEvent('nueva:track', { detail }));
  }

  function whatsappUrl(message) {
    return `https://wa.me/${site.whatsappNumber}?text=${encodeURIComponent(message)}`;
  }

  function advisorMessage(context = pageContext, intent = 'speak with an advisor') {
    const subject = clean(context) || site.brand;
    return `Hello Nueva Living, I would like to ${intent} about ${subject}.`;
  }

  function ensureHidden(form, name, value) {
    let field = form.querySelector(`[name="${CSS.escape(name)}"]`);
    if (!field) {
      field = document.createElement('input');
      field.type = 'hidden';
      field.name = name;
      form.appendChild(field);
    }
    field.value = value ?? '';
  }

  function buildLeadPayload(form, requestContext) {
    const fullName = readField(form, '[name="name"], [name="full_name"], [name="fullname"]');
    const split = splitName(fullName);
    const firstName = readField(form, '[name="first_name"]') || split.firstName;
    const lastName = readField(form, '[name="last_name"]') || split.lastName;
    const budgetRange = readField(form, '[name="budget_range"], [name="budget"], [name="price_range"]');
    const budget = parseBudgetRange(budgetRange);
    const project = readField(form, '[name="project"]') || (document.body?.dataset?.projectName || '');
    const preferredArea = readField(form, '[name="preferred_area"], [name="area"], [name="area_context"]') || clean(params.get('area'));
    const propertyType = readField(form, '[name="property_type_interest"], [name="property_type"], [name="type"]');
    const bedrooms = parseNumberRange(readField(form, '[name="bedrooms"], [name="bedroom_range"]'));
    const message = readField(form, 'textarea[name="message"], textarea, [name="message"]');
    const contextualMessage = project && !message.toLowerCase().includes(project.toLowerCase())
      ? `${message ? `${message}\n\n` : ''}Project: ${project}`
      : message;

    return compactPayload({
      first_name: firstName,
      last_name: lastName,
      email: readField(form, '[name="email"]'),
      phone: readField(form, '[name="phone"], [name="telephone"], [name="whatsapp"]'),
      budget_min: budget.min,
      budget_max: budget.max,
      preferred_areas: normalizeAreas(preferredArea),
      property_types: normalizePropertyTypes(propertyType),
      bedrooms_min: Number(readField(form, '[name="bedrooms_min"]')) || bedrooms.min,
      bedrooms_max: Number(readField(form, '[name="bedrooms_max"]')) || bedrooms.max,
      nationality: readField(form, '[name="nationality"]'),
      message: contextualMessage,
      consent: readChecked(form, '[name="consent"]'),
      consent_text: readChecked(form, '[name="consent"]')
        ? 'I agree to be contacted and for my data to be stored'
        : '',
      marketing_opt_in: readChecked(form, '[name="marketing_opt_in"]'),
      source_page: pagePath,
      utm_source: clean(params.get('utm_source')),
      utm_campaign: clean(params.get('utm_campaign'))
    });
  }

  function syncLeadToCrm(payload, trackingContext = {}) {
    if (!site.crmWebhookUrl) return Promise.reject(new Error('CRM endpoint is not configured'));

    const body = JSON.stringify(payload);
    track('crm_lead_webhook_queued', {
      ...trackingContext
    });

    return fetch(site.crmWebhookUrl, {
      method: 'POST',
      mode: 'cors',
      keepalive: true,
      headers: { 'Content-Type': 'application/json' },
      body
    })
      .then(async (response) => {
        let result = {};
        try {
          result = await response.json();
        } catch {
          // The status code remains authoritative if the proxy has no body.
        }

        const accepted = response.ok && (result.success === true || result.ok === true);
        track(accepted ? 'crm_lead_webhook_sent' : 'crm_lead_webhook_rejected', {
          status: response.status,
          ...trackingContext
        });

        if (!accepted) throw new Error(`CRM lead request failed with status ${response.status}`);
        return result;
      })
      .catch((error) => {
        track('crm_lead_webhook_error', {
          ...trackingContext,
          error: clean(error?.message)
        });
        throw error;
      });
  }

  function submitNetlifyCopy(form) {
    const netlifyFormName = form.querySelector('[name="form-name"]')?.value || form.getAttribute('name');
    if (!netlifyFormName) return Promise.resolve(false);
    const body = new URLSearchParams();
    new FormData(form).forEach((value, key) => {
      if (typeof value === 'string') body.append(key, value);
    });

    return fetch('/', {
      method: 'POST',
      keepalive: true,
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: body.toString()
    }).then((response) => response.ok);
  }

  function formStatusElement(form) {
    const existing = form.querySelector('.form-response, .form-note');
    if (existing) return existing;
    const status = document.createElement('span');
    status.className = 'form-response';
    form.appendChild(status);
    return status;
  }

  function setFormState(form, state, message) {
    const submit = form.querySelector('button[type="submit"], input[type="submit"]');
    const status = formStatusElement(form);
    status.setAttribute('role', 'status');
    status.setAttribute('aria-live', 'polite');
    status.textContent = message;
    status.classList.toggle('is-sent', state === 'success');
    status.classList.toggle('is-error', state === 'error');

    if (!submit) return;
    submit.dataset.originalLabel ||= submit.value || submit.textContent;
    submit.disabled = state === 'submitting' || state === 'success';
    const label = state === 'submitting'
      ? 'Sending...'
      : state === 'success'
        ? 'Request Sent'
        : submit.dataset.originalLabel;
    if (submit.tagName === 'INPUT') submit.value = label;
    else submit.textContent = label;
  }

  function enrichForm(form) {
    const formName = form.getAttribute('name') || form.querySelector('[name="form-name"]')?.value || 'liora-form';
    const projectField = form.querySelector('[name="project"]');
    const messageField = form.querySelector('textarea[name="message"], textarea');
    const requestContext =
      form.querySelector('[name="request_context"]')?.value ||
      projectField?.value ||
      intentFromUrl ||
      pageContext;

    ensureHidden(form, 'page_url', window.location.href);
    ensureHidden(form, 'page_path', pagePath);
    ensureHidden(form, 'source_page', pagePath);
    ensureHidden(form, 'lead_context', requestContext);
    ensureHidden(form, 'submitted_at', new Date().toISOString());
    if (intentFromUrl) ensureHidden(form, 'intent', intentFromUrl);
    if (params.get('area')) ensureHidden(form, 'area_context', params.get('area'));
    if (messageField && projectField && !messageField.value.trim()) {
      messageField.value = `I would like to receive the private project file for ${projectField.value}.`;
    }

    const payload = buildLeadPayload(form, requestContext);
    ensureHidden(form, 'first_name', payload.first_name);
    ensureHidden(form, 'last_name', payload.last_name);
    ensureHidden(form, 'budget_min', payload.budget_min);
    ensureHidden(form, 'budget_max', payload.budget_max);
    ensureHidden(form, 'crm_payload', JSON.stringify(payload));

    track('form_submit_intent', {
      form_name: formName,
      lead_context: requestContext
    });

    return {
      payload,
      trackingContext: {
        form_name: formName,
        lead_context: requestContext,
        project: projectField?.value || undefined
      }
    };
  }

  async function handleLeadSubmit(event) {
    const form = event.currentTarget;
    event.preventDefault();
    if (form.dataset.submitting === 'true') return;
    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }

    const { payload, trackingContext } = enrichForm(form);
    form.dataset.submitting = 'true';
    setFormState(form, 'submitting', 'Sending your private enquiry...');

    try {
      await syncLeadToCrm(payload, trackingContext);
      // Keep Netlify Forms as a secondary email/dashboard record without delaying confirmation.
      submitNetlifyCopy(form).catch(() => false);
      setFormState(form, 'success', 'Thank you. Your enquiry has been received and we will contact you shortly.');
      track('form_submit_success', trackingContext);
    } catch (error) {
      const fallbackCaptured = await submitNetlifyCopy(form).catch(() => false);
      if (fallbackCaptured) {
        setFormState(form, 'success', 'Thank you. Your enquiry has been received and we will contact you shortly.');
        track('form_submit_fallback_success', trackingContext);
      } else {
        setFormState(form, 'error', 'We could not send your request. Please email contact@nuevaliving.com.');
        track('form_submit_error', {
          ...trackingContext,
          error: clean(error?.message)
        });
      }
    } finally {
      delete form.dataset.submitting;
    }
  }

  window.lioraTrack = track;
  window.lioraWhatsappUrl = whatsappUrl;
  window.lioraBuildLeadPayload = buildLeadPayload;

  document.querySelectorAll('form').forEach((form) => {
    // Netlify removes data-netlify after registering a deployed form, but keeps form-name.
    const isLeadForm = form.matches('[data-crm-lead], [data-netlify="true"]') ||
      Boolean(form.querySelector('[name="form-name"]'));
    if (isLeadForm) form.addEventListener('submit', handleLeadSubmit);
  });

  document.querySelectorAll('a[data-whatsapp-advisor]').forEach((link) => {
    const context = link.dataset.project || link.dataset.context || pageContext;
    const intent = link.dataset.intent || 'speak with an advisor';
    link.href = whatsappUrl(advisorMessage(context, intent));
    link.target = '_blank';
    link.rel = 'noopener';
  });

  document.addEventListener('click', (event) => {
    const target = event.target.closest('a, button');
    if (!target) return;

    const label = clean(target.textContent || target.getAttribute('aria-label'));
    const href = target.getAttribute('href') || '';
    const projectCard = target.closest('[data-project-card], .dev-card, .project-card');
    const cardTitle = projectCard?.querySelector('.dev-name, h3, [data-project-name]')?.textContent;
    const context = clean(target.dataset.project || cardTitle || pageContext);

    if (href.includes('wa.me') || target.matches('[data-whatsapp-advisor]')) {
      track('whatsapp_click', { cta_label: label, lead_context: context, href });
      return;
    }

    if (href.includes('private-viewing') || target.classList.contains('dev-viewing-btn')) {
      track('private_viewing_request', { cta_label: label, lead_context: context, href });
      return;
    }

    if (href.includes('property-')) {
      track('project_click', { cta_label: label, lead_context: context, href });
      return;
    }

    if (
      target.matches('.btn, .project-btn, .dev-cta-link, .project-link, .nav-cta') ||
      /request|access|material|availability|advisor|viewing|enquire/i.test(label)
    ) {
      track('cta_click', { cta_label: label, lead_context: context, href });
    }
  }, { capture: true });
})();
