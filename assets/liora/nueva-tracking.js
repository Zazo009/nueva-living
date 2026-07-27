(() => {
  'use strict';

  const endpoint = '/.netlify/functions/nueva-track';
  const sessionKey = '_nl_sid';
  const sessionTimestampKey = '_nl_ts';
  const sessionUtmKey = '_nl_utm';
  const sessionTimeout = 30 * 60 * 1000;
  const scrollMilestones = [25, 50, 75, 100];
  const trackedScrollMilestones = new Set();
  const startedAt = Date.now();
  let visibleSince = document.hidden ? 0 : startedAt;
  let visibleDuration = 0;
  let durationSent = false;
  let vitalsSent = false;
  let lastBusinessEventAt = 0;
  let largestContentfulPaint = 0;
  let cumulativeLayoutShift = 0;
  let interactionToNextPaint = 0;

  if (window.NUEVA_TRACKING_DISABLED === true) return;

  function storageGet(key) {
    try {
      return window.localStorage.getItem(key);
    } catch {
      return null;
    }
  }

  function storageSet(key, value) {
    try {
      window.localStorage.setItem(key, value);
    } catch {
      // Tracking remains functional when storage is blocked.
    }
  }

  function createId(prefix) {
    if (window.crypto?.randomUUID) return `${prefix}_${window.crypto.randomUUID()}`;
    const random = Math.random().toString(36).slice(2);
    return `${prefix}_${Date.now().toString(36)}_${random}`;
  }

  function getSessionId() {
    const now = Date.now();
    const storedId = storageGet(sessionKey);
    const storedTimestamp = Number(storageGet(sessionTimestampKey));
    const isActive = storedId && Number.isFinite(storedTimestamp) && now - storedTimestamp < sessionTimeout;
    const sessionId = isActive ? storedId : createId('nl');
    if (!isActive) storageSet(sessionUtmKey, '{}');
    storageSet(sessionKey, sessionId);
    storageSet(sessionTimestampKey, String(now));
    return sessionId;
  }

  const sessionId = getSessionId();
  const query = new URLSearchParams(window.location.search);
  const utmKeys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'];

  function sessionUtm() {
    let stored = {};
    try {
      stored = JSON.parse(storageGet(sessionUtmKey) || '{}');
    } catch {
      stored = {};
    }

    const current = {};
    utmKeys.forEach((key) => {
      const value = cleanText(query.get(key), 160);
      if (value) current[key] = value;
    });

    const acquisition = Object.keys(current).length ? current : stored;
    if (Object.keys(current).length) storageSet(sessionUtmKey, JSON.stringify(current));
    return acquisition;
  }

  const acquisition = sessionUtm();

  function browserName() {
    const userAgent = navigator.userAgent;
    if (/Edg\//.test(userAgent)) return 'Edge';
    if (/OPR\//.test(userAgent)) return 'Opera';
    if (/CriOS|Chrome\//.test(userAgent)) return 'Chrome';
    if (/FxiOS|Firefox\//.test(userAgent)) return 'Firefox';
    if (/Safari\//.test(userAgent)) return 'Safari';
    return 'Other';
  }

  function operatingSystem() {
    const userAgent = navigator.userAgent;
    if (/iPhone|iPad|iPod/.test(userAgent)) return 'iOS';
    if (/Android/.test(userAgent)) return 'Android';
    if (/Windows/.test(userAgent)) return 'Windows';
    if (/Mac OS X|Macintosh/.test(userAgent)) return 'macOS';
    if (/Linux/.test(userAgent)) return 'Linux';
    return 'Other';
  }

  function deviceType() {
    if (/Mobi|Android|iPhone|iPod/.test(navigator.userAgent)) return 'mobile';
    if (/iPad|Tablet/.test(navigator.userAgent) || (navigator.maxTouchPoints > 1 && innerWidth < 1100)) {
      return 'tablet';
    }
    return 'desktop';
  }

  function cleanText(value, maxLength = 180) {
    return String(value ?? '')
      .replace(/\s+/g, ' ')
      .trim()
      .slice(0, maxLength);
  }

  function safeValue(value) {
    if (typeof value === 'string') return cleanText(value, 300);
    if (typeof value === 'number' || typeof value === 'boolean') return value;
    if (Array.isArray(value)) return value.slice(0, 20).map((item) => safeValue(item));
    return undefined;
  }

  function safeDetails(details = {}) {
    const output = {};
    Object.entries(details).slice(0, 35).forEach(([key, value]) => {
      const safe = safeValue(value);
      if (safe !== undefined && safe !== '') output[key] = safe;
    });
    return output;
  }

  function basePayload(type, details = {}) {
    return {
      event_id: createId('evt'),
      type,
      session_id: sessionId,
      page: window.location.pathname || '/',
      page_title: document.title,
      referrer: document.referrer || '',
      timestamp: new Date().toISOString(),
      device: deviceType(),
      browser: browserName(),
      os: operatingSystem(),
      language: navigator.language || '',
      viewport_width: window.innerWidth,
      viewport_height: window.innerHeight,
      utm_source: acquisition.utm_source || '',
      utm_medium: acquisition.utm_medium || '',
      utm_campaign: acquisition.utm_campaign || '',
      utm_term: acquisition.utm_term || '',
      utm_content: acquisition.utm_content || '',
      ...safeDetails(details)
    };
  }

  function send(type, details = {}, options = {}) {
    storageSet(sessionTimestampKey, String(Date.now()));
    const payload = basePayload(type, details);
    const body = JSON.stringify(payload);

    if (options.beacon && navigator.sendBeacon) {
      const blob = new Blob([body], { type: 'application/json' });
      if (navigator.sendBeacon(endpoint, blob)) return Promise.resolve();
    }

    return fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body,
      keepalive: Boolean(options.keepalive)
    }).catch(() => {
      // Analytics must never interrupt the visitor experience.
    });
  }

  window.crmTrack = (type, details = {}) => send(cleanText(type, 80), details);

  function elementLabel(element) {
    return cleanText(
      element.dataset.track ||
      element.getAttribute('aria-label') ||
      element.getAttribute('title') ||
      element.textContent,
      120
    );
  }

  function projectName(element) {
    const card = element.closest('[data-project-card], .project-card, .dev-card');
    return cleanText(
      element.dataset.project ||
      card?.dataset.projectName ||
      card?.querySelector('[data-project-name], .dev-name, h2, h3')?.textContent,
      120
    );
  }

  function inferredTrackLabel(element) {
    const label = elementLabel(element) || 'Unlabelled control';
    const href = element.getAttribute('href') || '';
    if (element.matches('[data-whatsapp-advisor], a[href*="wa.me"]')) return `WhatsApp: ${label}`;
    if (element.matches('a[href^="mailto:"]')) return `Email: ${label}`;
    if (element.matches('a[href^="tel:"]')) return `Phone: ${label}`;
    if (element.closest('header, .topbar, .mobile-menu, .site-nav, #nav')) return `Navigation: ${label}`;
    if (element.closest('.hero, .hero-content, .hero-btns, .project-hero')) return `Hero: ${label}`;
    if (element.closest('footer')) return `Footer: ${label}`;
    if (element.closest('[data-project-card], .project-card, .dev-card') || /property-/.test(href)) {
      return `Project: ${projectName(element) || label}`;
    }
    if (element.matches('[data-shortlist-id], .nueva-shortlist-trigger, [data-shortlist-close]')) {
      return `Shortlist: ${label}`;
    }
    if (element.closest('#vox, #vveil, [data-private-viewing]')) return `Private Viewing: ${label}`;
    return label;
  }

  function annotateTracking(root = document) {
    const forms = [
      ...(root instanceof HTMLFormElement ? [root] : []),
      ...root.querySelectorAll('form')
    ];
    const controls = [
      ...(root instanceof Element && root.matches('a, button, [role="button"]') ? [root] : []),
      ...root.querySelectorAll('a, button, [role="button"]')
    ];

    forms.forEach((form) => {
      if (!form.dataset.trackForm) {
        form.dataset.trackForm = cleanText(form.getAttribute('name') || form.id || 'Website enquiry', 100);
      }
    });

    controls.forEach((element) => {
      if (!element.dataset.track) element.dataset.track = inferredTrackLabel(element);
    });
  }

  annotateTracking();
  new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      mutation.addedNodes.forEach((node) => {
        if (!(node instanceof Element)) return;
        annotateTracking(node);
      });
    });
  }).observe(document.documentElement, { childList: true, subtree: true });

  send('pageview', {
    url: window.location.href.split('#')[0],
    document_visibility: document.visibilityState
  });

  let scrollTicking = false;
  function currentScrollPercentage() {
    const scrollable = document.documentElement.scrollHeight - window.innerHeight;
    if (scrollable <= 0) return 100;
    return Math.min(100, Math.max(0, Math.round((window.scrollY / scrollable) * 100)));
  }

  function inspectScroll() {
    const percentage = currentScrollPercentage();
    scrollMilestones.forEach((milestone) => {
      if (percentage >= milestone && !trackedScrollMilestones.has(milestone)) {
        trackedScrollMilestones.add(milestone);
        send('scroll_depth', { percentage: milestone });
      }
    });
    scrollTicking = false;
  }

  window.addEventListener('scroll', () => {
    if (scrollTicking) return;
    scrollTicking = true;
    window.requestAnimationFrame(inspectScroll);
  }, { passive: true });

  function isOutbound(href) {
    try {
      const url = new URL(href, window.location.href);
      return /^https?:$/.test(url.protocol) && url.origin !== window.location.origin;
    } catch {
      return false;
    }
  }

  document.addEventListener('click', (event) => {
    const element = event.target.closest('a, button, [role="button"]');
    if (!element) return;

    const href = element.getAttribute('href') || '';
    const details = {
      label: inferredTrackLabel(element),
      href,
      project: projectName(element),
      element: element.tagName.toLowerCase()
    };

    if (isOutbound(href)) {
      send('outbound_click', details);
      return;
    }

    // Existing conversion events are richer than a second generic CTA click.
    if (performance.now() - lastBusinessEventAt < 80) return;
    send('element_click', details);
  });

  document.addEventListener('submit', (event) => {
    const form = event.target;
    if (!(form instanceof HTMLFormElement)) return;
    send('form_submit_attempt', {
      form: form.dataset.trackForm || form.name || form.id || 'Website enquiry',
      valid: form.checkValidity(),
      action: form.getAttribute('action') || ''
    });
  }, { capture: true });

  function mediaDetails(media) {
    return {
      media: cleanText(
        media.dataset.trackVideo ||
        media.dataset.title ||
        media.getAttribute('aria-label') ||
        media.currentSrc ||
        media.src ||
        media.tagName.toLowerCase(),
        160
      ),
      media_type: media.tagName.toLowerCase()
    };
  }

  // Capture-phase listeners include media inserted later by cinematic experiences.
  document.addEventListener('play', (event) => {
    const media = event.target;
    if (!(media instanceof HTMLMediaElement)) return;
    send('video_play', {
      ...mediaDetails(media),
      current_time: Math.round(media.currentTime)
    });
  }, true);

  document.addEventListener('pause', (event) => {
    const media = event.target;
    if (!(media instanceof HTMLMediaElement) || media.ended) return;
    send('video_pause', {
      ...mediaDetails(media),
      current_time: Math.round(media.currentTime)
    });
  }, true);

  document.addEventListener('ended', (event) => {
    const media = event.target;
    if (!(media instanceof HTMLMediaElement)) return;
    send('video_complete', {
      ...mediaDetails(media),
      duration: Math.round(media.duration || 0)
    });
  }, true);

  document.addEventListener('copy', (event) => {
    if (event.target?.closest?.('input, textarea, [contenteditable="true"]')) return;
    const selection = cleanText(window.getSelection()?.toString(), 100)
      .replace(/[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}/gi, '[email]')
      .replace(/\+?\d[\d\s()-]{7,}\d/g, '[number]');
    if (selection) send('content_copy', { text: selection });
  });

  window.addEventListener('beforeprint', () => send('print'));

  const rageClicks = [];
  document.addEventListener('pointerup', (event) => {
    const now = Date.now();
    rageClicks.push({ x: event.clientX, y: event.clientY, time: now });
    while (rageClicks.length && now - rageClicks[0].time > 1200) rageClicks.shift();
    const nearby = rageClicks.filter((point) => (
      Math.abs(point.x - event.clientX) < 45 &&
      Math.abs(point.y - event.clientY) < 45
    ));
    if (nearby.length === 4) {
      send('rage_click', {
        x: Math.round(event.clientX),
        y: Math.round(event.clientY),
        target: elementLabel(event.target.closest?.('a, button, input, select, textarea') || event.target)
      });
    }
  }, { passive: true });

  window.addEventListener('error', (event) => {
    send('javascript_error', {
      message: cleanText(event.message, 240),
      filename: cleanText(event.filename?.split('?')[0], 180),
      line: event.lineno || 0,
      column: event.colno || 0
    });
  });

  window.addEventListener('unhandledrejection', (event) => {
    send('unhandled_rejection', {
      message: cleanText(event.reason?.message || event.reason, 240)
    });
  });

  window.addEventListener('nueva:track', (event) => {
    const detail = safeDetails(event.detail || {});
    const type = cleanText(detail.event || 'business_event', 80);
    delete detail.event;
    lastBusinessEventAt = performance.now();
    send(type, detail);
  });

  function observePerformance() {
    if (!('PerformanceObserver' in window)) return;

    try {
      new PerformanceObserver((list) => {
        const entries = list.getEntries();
        largestContentfulPaint = entries.at(-1)?.startTime || largestContentfulPaint;
      }).observe({ type: 'largest-contentful-paint', buffered: true });
    } catch {
      // Metric is not supported in this browser.
    }

    try {
      new PerformanceObserver((list) => {
        list.getEntries().forEach((entry) => {
          if (!entry.hadRecentInput) cumulativeLayoutShift += entry.value;
        });
      }).observe({ type: 'layout-shift', buffered: true });
    } catch {
      // Metric is not supported in this browser.
    }

    try {
      new PerformanceObserver((list) => {
        list.getEntries().forEach((entry) => {
          interactionToNextPaint = Math.max(interactionToNextPaint, entry.duration || 0);
        });
      }).observe({ type: 'event', buffered: true, durationThreshold: 40 });
    } catch {
      // Metric is not supported in this browser.
    }
  }

  observePerformance();

  function sendVitals() {
    if (vitalsSent) return;
    vitalsSent = true;
    const navigation = performance.getEntriesByType('navigation')[0];
    send('web_vitals', {
      lcp_ms: Math.round(largestContentfulPaint),
      cls: Number(cumulativeLayoutShift.toFixed(4)),
      inp_ms: Math.round(interactionToNextPaint),
      dom_content_loaded_ms: Math.round(navigation?.domContentLoadedEventEnd || 0),
      load_ms: Math.round(navigation?.loadEventEnd || 0)
    }, { beacon: true, keepalive: true });
  }

  function accumulateVisibleDuration() {
    if (!visibleSince) return;
    visibleDuration += Date.now() - visibleSince;
    visibleSince = 0;
  }

  function sendDuration() {
    if (durationSent) return;
    durationSent = true;
    accumulateVisibleDuration();
    send('page_duration', {
      duration_seconds: Math.max(1, Math.round(visibleDuration / 1000)),
      max_scroll_percentage: currentScrollPercentage()
    }, { beacon: true, keepalive: true });
    sendVitals();
  }

  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      accumulateVisibleDuration();
      sendDuration();
    } else {
      durationSent = false;
      visibleSince = Date.now();
    }
  });
  window.addEventListener('pagehide', sendDuration);
})();
