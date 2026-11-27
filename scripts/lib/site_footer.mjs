// The site footer. One shape, one place.
//
// There were four. The homepage carried a three-column footer -- brand,
// Company, and Projects with Contact Us beneath it -- while every other page
// type carried a four-column one with a separate Legal column and the whole
// area list inside Projects. Nothing failed, because each footer was correct
// on its own page; it only showed when two page types were put side by side,
// and it made the footer 170px taller on 180 pages than on the homepage.
//
// The counts, before this file existed:
//   index.html            Company 7, Projects 2,  Contact Us 3
//   about.html            Company 5, Projects 10, Contact 3, Legal 3
//   property-*.html       Company 5, Projects 11, Contact 3, Legal 3
//   developments.html     Company 4, Projects 14, Contact 3, Legal 3
//
// The homepage's shape won, because it is the one the design specifies. The
// seven area links dropped out of Projects with it: every one of them is in
// the Areas menu on the same page, so nothing became unreachable, and
// audit_site_consistency checks that independently.
//
// The contact block did NOT follow the homepage. The homepage published
// +46 707 57 67 09 and "Marbella, Spain" while 180 pages published
// +34 645 44 66 24 and the street address -- the same business reachable two
// ways depending on which page you landed on. The Spanish line and the full
// address are what the site keeps, on every page: a complete address on every
// page is what a business with a physical office wants to be showing.
import { t, localizedPath } from './i18n.mjs';

// The one copy of the contact details. Changing a number here changes it on
// every page of the site, which is the point.
export const FOOTER_CONTACT = {
  email: 'contact@nuevaliving.com',
  phone: '+34 645 44 66 24',
  phoneHref: 'tel:+34645446624',
  address: 'Calle Las Torres, 3 (Aloha Gardens), 29660 Marbella',
  addressHref: 'https://maps.google.com/?q=Calle+Las+Torres,+3+(Aloha+Gardens),+29660+Marbella,+M%C3%A1laga,+Spain',
};

// Every link in the footer, in order, as [path, translation key]. Kept as data
// so the guard in audit_site_consistency can compare a built page against it
// rather than against another page that may have drifted the same way.
//
// November 2026 redesign: four links under Explore and four under Company, so
// the two columns end level, and the three legal pages on the bottom line next
// to the company details, where readers look for them. The footer came down
// from 494 to about 350px on a desktop and from 831 to about 510px on a phone.
export const FOOTER_EXPLORE_LINKS = [
  ['developments.html', 'nav.developments'],
  ['areas.html', 'nav.allAreas'],
  ['guides.html', 'nav.buyingGuides'],
  // The assistant connector page: a way of searching the developments.
  ['ai.html', 'footer.assistants'],
];

export const FOOTER_COMPANY_LINKS = [
  ['why-nueva.html', 'footer.whyNuevaLiving'],
  ['about.html', 'footer.about'],
  ['advisory.html', 'nav.advisory'],
  ['contact.html', 'footer.contactUs'],
];

// build_dist.mjs adds the "Cookie settings" control after the cookie policy
// link; it matches <li><a href="...cookie-policy.html">, so these stay list items.
export const FOOTER_LEGAL_LINKS = [
  ['privacy-policy.html', 'footer.privacyPolicy'],
  ['legal-notice.html', 'footer.legalNotice'],
  ['cookie-policy.html', 'footer.cookiePolicy'],
];

// "Ask about Nueva Living": each assistant opens with a question about the
// business in the page's language. The answer is the assistant's own.
export const FOOTER_ASSISTANTS = [
  ['ChatGPT', 'https://chatgpt.com/?q='],
  ['Claude', 'https://claude.ai/new?q='],
  ['Perplexity', 'https://www.perplexity.ai/search?q='],
  ['Google AI Mode', 'https://www.google.com/search?udm=50&q='],
  ['Copilot', 'https://copilot.microsoft.com/?q='],
  ['Grok', 'https://grok.com/?q='],
];

export const COSTA_BRIDGE = {
  href: 'https://costabridge.co.uk/directory/nueva-living-kr2i',
  badge: 'https://costabridge.co.uk/badge/listing/nueva-living-kr2i.svg?theme=dark',
};

const ICON = {
  mail: '<svg viewBox="0 0 24 24" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="1.7"><rect x="3" y="5" width="18" height="14" rx="1"/><path d="M3.5 6l8.5 7 8.5-7"/></g></svg>',
  phone: '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round" d="M6.6 3.5l2.8.3 1.2 4-2 1.4a12 12 0 0 0 6.2 6.2l1.4-2 4 1.2.3 2.8c-.2 1.6-1.6 2.8-3.2 2.6C10.4 19.3 4.7 13.6 4 6.7c-.2-1.6 1-3 2.6-3.2z"/></svg>',
  pin: '<svg viewBox="0 0 24 24" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="1.7"><path d="M12 21s-6.5-6.2-6.5-11a6.5 6.5 0 0 1 13 0c0 4.8-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.3"/></g></svg>',
  spark: '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" d="M10 3.5l1.6 4.9 4.9 1.6-4.9 1.6L10 16.5l-1.6-4.9L3.5 10l4.9-1.6zM17.5 14l.8 2.2 2.2.8-2.2.8-.8 2.2-.8-2.2-2.2-.8 2.2-.8z"/></svg>',
};

const escAttr = (value) => String(value).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;');

/**
 * @param {string} locale
 * @param {string} prefix  What a root-relative path has to be prefixed with to
 *                         resolve from this page (e.g. '' or '../').
 */
export function renderFooter(locale, prefix = '') {
  const link = ([target, key]) =>
    `<li><a href="${prefix}${localizedPath(target, locale)}">${t(key, locale)}</a></li>`;
  const badgeAlt = t('footer.costaBridge', locale);
  const badge = (cls) => `<a class="nf-badge ${cls}" href="${COSTA_BRIDGE.href}" target="_blank" rel="noopener" title="${badgeAlt}"><img src="${COSTA_BRIDGE.badge}" alt="${badgeAlt}" width="238" height="64" loading="lazy" decoding="async"></a>`;
  const question = encodeURIComponent(t('footer.aiPrompt', locale));

  return `<footer class="nf">
    <div class="nf-in">
      <div class="nf-top">
        <div class="nf-brand">
          <img class="nf-logo" src="${prefix}assets/liora/brand/nueva-living-lockup-espresso-transparent.png?v=7" alt="Nueva Living" width="700" height="340" loading="lazy" decoding="async">
          <p class="nf-about">${t('footer.about.text', locale)}</p>
          ${badge('nf-badge-phone')}
        </div>
        <nav class="nf-col" aria-label="${t('footer.exploreTitle', locale)}">
          <p class="nf-title">${t('footer.exploreTitle', locale)}</p>
          <ul>${FOOTER_EXPLORE_LINKS.map(link).join('')}</ul>
        </nav>
        <nav class="nf-col" aria-label="${t('footer.companyTitle', locale)}">
          <p class="nf-title">${t('footer.companyTitle', locale)}</p>
          <ul>${FOOTER_COMPANY_LINKS.map(link).join('')}</ul>
        </nav>
        <div class="nf-col nf-contact">
          <p class="nf-title">${t('footer.contactTitle', locale)}</p>
          <ul>
            <li><a href="mailto:${FOOTER_CONTACT.email}">${ICON.mail}<span class="nf-full">${FOOTER_CONTACT.email}</span><span class="nf-short">${t('footer.short.email', locale)}</span></a></li>
            <li><a href="${FOOTER_CONTACT.phoneHref}">${ICON.phone}<span class="nf-full" dir="ltr">${FOOTER_CONTACT.phone}</span><span class="nf-short">${t('footer.short.call', locale)}</span></a></li>
            <li><a href="${FOOTER_CONTACT.addressHref}" target="_blank" rel="noopener">${ICON.pin}<span class="nf-full">${FOOTER_CONTACT.address}</span><span class="nf-short">${t('footer.short.office', locale)}</span></a></li>
          </ul>
        </div>
      </div>
      <div class="nf-ai">
        <p class="nf-title">${t('footer.askAbout', locale)}</p>
        <ul class="nf-chips">${FOOTER_ASSISTANTS.map(([label, base]) => `<li><a href="${escAttr(base + question)}" target="_blank" rel="noopener nofollow" data-ask-ai="${label}">${ICON.spark}${label}</a></li>`).join('')}</ul>
        ${badge('nf-badge-wide')}
      </div>
      <div class="nf-bottom">
        <span class="nf-copy" dir="ltr">© 2026 Nueva Living · LIORA LIVING SL. · NIF B88827472</span>
        <ul class="nf-legal" aria-label="${t('footer.legalTitle', locale)}">
            ${FOOTER_LEGAL_LINKS.map(link).join('\n            ')}
        </ul>
        <p class="nf-disc-wide">${t('footer.disclaimer', locale)}</p>
        <details class="nf-disc"><summary>${t('footer.disclaimerTitle', locale)}</summary><p>${t('footer.disclaimer', locale)}</p></details>
      </div>
    </div>
  </footer>`;
}

/**
 * Swap a built English page's footer for the same footer in `locale`.
 *
 * The locale builders translate by running a table of English strings through
 * the page, longest first. That works for copy an editor wrote, and it failed
 * for the footer the moment the footer stopped being hand-written: the
 * disclaimer they knew how to translate was the hand-authored wording, and the
 * shared footer emits `footer.disclaimer`, which was not in the table -- so 45
 * locale pages printed an English sentence in the middle of a Spanish footer.
 * Rendering the footer for the locale removes the whole class of failure
 * rather than adding one more entry to the table.
 *
 * The LAST footer is the page's own: an earlier one may be a semantic
 * attribution element inside a testimonial.
 */
export function replaceFooter(html, locale) {
  const matches = [...html.matchAll(/<footer(?:\s[^>]*)?>[\s\S]*?<\/footer>/gi)];
  const siteFooter = matches.at(-1);
  if (!siteFooter) return html;
  return html.slice(0, siteFooter.index) + renderFooter(locale) + html.slice(siteFooter.index + siteFooter[0].length);
}
