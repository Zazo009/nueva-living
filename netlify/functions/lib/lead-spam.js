// Content rules for lead submissions that no real enquirer produces.
//
// The form already has two honeypots, and neither stopped this: two "leads"
// arrived with a Russian phishing message and a tracking link where the first
// and last name belong, from a throwaway e-mail domain. A bot that posts
// straight to the endpoint never sees a hidden field, so the check has to look
// at what was sent, not at what was left empty.
//
// The rules are deliberately narrow. A name is the one field where a link is
// never legitimate, so a link, an at-sign or a name far longer than any real
// one is spam. A message is allowed a link -- a buyer may paste a listing --
// but not a handful of them. Nothing here guesses from language or script:
// Cyrillic, Arabic and Chinese names are ordinary enquiries on this site.

const LINK = /(?:https?:\/\/|www\.|\b[a-z0-9-]+\.(?:com|net|org|biz|info|buzz|xyz|top|click|link|ru|cn|id)\b\/)/i;
const MAX_NAME_LENGTH = 60;
const MAX_LINKS_IN_MESSAGE = 2;

function clean(value) {
  return typeof value === 'string' ? value.replace(/\s+/g, ' ').trim() : '';
}

function linkCount(text) {
  return (text.match(new RegExp(LINK.source, 'gi')) || []).length;
}

function spamReason(lead = {}) {
  for (const field of ['first_name', 'last_name']) {
    const value = clean(lead[field]);
    if (!value) continue;
    if (LINK.test(value)) return `${field} contains a link`;
    if (value.includes('@')) return `${field} contains an at-sign`;
    if (value.length > MAX_NAME_LENGTH) return `${field} is ${value.length} characters long`;
  }

  const message = clean(lead.message);
  if (message && linkCount(message) > MAX_LINKS_IN_MESSAGE) {
    return `message contains ${linkCount(message)} links`;
  }

  return '';
}

module.exports = { spamReason };
