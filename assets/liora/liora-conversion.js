(() => {
  const site = {
    whatsappNumber: '34600000000',
    brand: 'Nueva Living',
    crmWebhookUrl: window.NUEVA_CRM_WEBHOOK_URL || '/.netlify/functions/liora-lead'
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

  function splitName(fullName) {
    const parts = clean(fullName).split(' ').filter(Boolean);
    if (!parts.length) return { firstName: '', lastName: '' };
    if (parts.length === 1) return { firstName: parts[0], lastName: '' };
    return {
      firstName: parts.slice(0, -1).join(' '),
      lastName: parts.slice(-1).join(' ')
    };
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

  function utmPayload() {
    return ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term']
      .reduce((acc, key) => {
        const value = clean(params.get(key));
        if (value) acc[key] = value;
        return acc;
      }, {});
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
    field.value = value;
  }

  function buildLeadPayload(form, requestContext) {
    const formName = form.getAttribute('name') || form.querySelector('[name="form-name"]')?.value || 'liora-form';
    const fullName = readField(form, '[name="name"], [name="full_name"], [name="fullname"]');
    const { firstName, lastName } = splitName(fullName);
    const budgetRange = readField(form, '[name="budget_range"], [name="budget"], [name="price_range"]');
    const budget = parseBudgetRange(budgetRange);
    const project = readField(form, '[name="project"]') || (document.body?.dataset?.projectName || '');
    const preferredArea = readField(form, '[name="preferred_area"], [name="area"], [name="area_context"]') || clean(params.get('area'));
    const propertyType = readField(form, '[name="property_type_interest"], [name="property_type"], [name="type"]');
    const message = readField(form, 'textarea[name="message"], textarea, [name="message"]');

    return {
      source: 'nueva-living',
      brand: site.brand,
      form_name: formName,
      lead_context: clean(requestContext),
      intent: clean(intentFromUrl || form.querySelector('[name="intent"]')?.value),
      project,
      first_name: firstName,
      last_name: lastName,
      full_name: fullName,
      email: readField(form, '[name="email"]'),
      phone: readField(form, '[name="phone"], [name="telephone"], [name="whatsapp"]'),
      budget_range: budgetRange,
      budget_min: budget.min,
      budget_max: budget.max,
      preferred_area: preferredArea,
      property_type_interest: propertyType,
      purchase_purpose: readField(form, '[name="purchase_purpose"], [name="purpose"], [name="motivation"]'),
      message,
      page_url: window.location.href,
      page_path: pagePath,
      source_page: document.title,
      submitted_at: new Date().toISOString(),
      metadata: {
        referrer: document.referrer || '',
        ...utmPayload()
      },
      ...utmPayload()
    };
  }

  function syncLeadToCrm(payload) {
    if (!site.crmWebhookUrl) return;

    const body = JSON.stringify(payload);
    track('crm_lead_webhook_queued', {
      form_name: payload.form_name,
      lead_context: payload.lead_context,
      project: payload.project || undefined
    });

    fetch(site.crmWebhookUrl, {
      method: 'POST',
      mode: 'cors',
      keepalive: true,
      headers: { 'Content-Type': 'application/json' },
      body
    })
      .then((response) => {
        track(response.ok ? 'crm_lead_webhook_sent' : 'crm_lead_webhook_rejected', {
          form_name: payload.form_name,
          status: response.status,
          lead_context: payload.lead_context
        });
      })
      .catch((error) => {
        track('crm_lead_webhook_error', {
          form_name: payload.form_name,
          lead_context: payload.lead_context,
          error: clean(error?.message)
        });
      });
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
    ensureHidden(form, 'source_page', document.title);
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
    ensureHidden(form, 'crm_source', payload.source);
    ensureHidden(form, 'crm_payload', JSON.stringify(payload));

    track('form_submit_intent', {
      form_name: formName,
      lead_context: requestContext
    });

    // CRM sync is intentionally non-blocking so the native form/Netlify fallback still captures every lead.
    syncLeadToCrm(payload);
  }

  window.lioraTrack = track;
  window.lioraWhatsappUrl = whatsappUrl;
  window.lioraBuildLeadPayload = buildLeadPayload;

  document.querySelectorAll('form').forEach((form) => {
    form.addEventListener('submit', () => enrichForm(form), { capture: true });
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
