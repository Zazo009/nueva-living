(() => {
  'use strict';

  // Cookie consent, wired to Google Consent Mode v2.
  //
  // The defaults are written inline in the head, before the tag loader runs,
  // so nothing measurable happens until a choice exists. This file only reads
  // a stored choice, replays it, and runs the banner.
  //
  // Denied by default everywhere rather than only in the EEA. The visitors are
  // European buyers wherever they happen to be reading from, and a region list
  // is one more thing to keep correct.

  var STORAGE_KEY = 'nueva_consent_v1';
  var GRANTED = {
    ad_storage: 'granted',
    ad_user_data: 'granted',
    ad_personalization: 'granted',
    analytics_storage: 'granted'
  };
  var DENIED = {
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied',
    analytics_storage: 'denied'
  };

  function gtag() {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push(arguments);
  }

  function readChoice() {
    try {
      var raw = window.localStorage.getItem(STORAGE_KEY);
      if (!raw) return null;
      var value = JSON.parse(raw);
      return value && (value.state === 'granted' || value.state === 'denied') ? value : null;
    } catch (err) {
      return null;
    }
  }

  function writeChoice(state) {
    try {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify({
        state: state,
        at: new Date().toISOString()
      }));
    } catch (err) {
      // A visitor who blocks storage gets asked again next time, which is the
      // safe direction to fail in.
    }
  }

  function apply(state) {
    gtag('consent', 'update', state === 'granted' ? GRANTED : DENIED);
    window.dataLayer.push({
      event: 'nueva_consent',
      nueva_consent_state: state
    });
  }

  var banner = document.querySelector('[data-consent-banner]');

  function open() { if (banner) banner.setAttribute('data-open', ''); }
  function close() { if (banner) banner.removeAttribute('data-open'); }

  function choose(state) {
    writeChoice(state);
    apply(state);
    close();
  }

  var stored = readChoice();
  if (stored) apply(stored.state);
  else open();

  if (banner) {
    banner.addEventListener('click', function (event) {
      var button = event.target.closest('[data-consent-action]');
      if (!button) return;
      choose(button.getAttribute('data-consent-action') === 'accept' ? 'granted' : 'denied');
    });
  }

  // Any element can reopen the banner, which is how a visitor withdraws a
  // choice they already made.
  document.addEventListener('click', function (event) {
    var trigger = event.target.closest('[data-consent-reopen]');
    if (!trigger) return;
    event.preventDefault();
    open();
    var first = banner && banner.querySelector('[data-consent-action]');
    if (first) first.focus();
  });
})();
