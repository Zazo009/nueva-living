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
  address: 'Calle Las Torres (Aloha Gardens), 29660 Marbella',
  addressHref: 'https://maps.google.com/?q=Calle+Las+Torres+(Aloha+Gardens),+29660+Marbella,+M%C3%A1laga,+Spain',
};

// Every link in the footer, in order, as [path, translation key]. Kept as data
// so the guard in audit_site_consistency can compare a built page against it
// rather than against another page that may have drifted the same way.
export const FOOTER_COMPANY_LINKS = [
  ['why-nueva.html', 'footer.whyNuevaLiving'],
  ['about.html', 'footer.about'],
  ['advisory.html', 'nav.advisory'],
  ['contact.html', 'footer.contactUs'],
  ['privacy-policy.html', 'footer.privacyPolicy'],
  ['legal-notice.html', 'footer.legalNotice'],
  ['cookie-policy.html', 'footer.cookiePolicy'],
];

export const FOOTER_PROJECT_LINKS = [
  ['developments.html', 'nav.developments'],
  ['areas.html', 'nav.allAreas'],
];

/**
 * @param {string} locale
 * @param {string} prefix  What a root-relative path has to be prefixed with to
 *                         resolve from this page (e.g. '' or '../').
 */
export function renderFooter(locale, prefix = '') {
  const link = ([target, key]) =>
    `          <li><a href="${prefix}${localizedPath(target, locale)}">${t(key, locale)}</a></li>`;

  return `<footer>
    <div class="footer-grid">
      <div>
        <img class="footer-logo" src="${prefix}assets/liora/brand/nueva-living-lockup-espresso-transparent.png?v=7" alt="Nueva Living" width="700" height="340" loading="lazy" decoding="async">
        <p class="footer-about">${t('footer.about.text', locale)}</p>
      </div>
      <div class="footer-col">
        <div class="footer-col-title">${t('footer.companyTitle', locale)}</div>
        <ul>
${FOOTER_COMPANY_LINKS.map(link).join('\n')}
        </ul>
      </div>
      <div class="footer-col">
        <div class="footer-col-title">${t('footer.projectsTitle', locale)}</div>
        <ul>
${FOOTER_PROJECT_LINKS.map(link).join('\n')}
        </ul>
        <div class="footer-col-title" style="margin-top:22px;">${t('footer.contactUs', locale)}</div>
        <ul>
          <li><a href="mailto:${FOOTER_CONTACT.email}">${FOOTER_CONTACT.email}</a></li>
          <li><a href="${FOOTER_CONTACT.phoneHref}" dir="ltr">${FOOTER_CONTACT.phone}</a></li>
          <li><a href="${FOOTER_CONTACT.addressHref}" target="_blank" rel="noopener">${FOOTER_CONTACT.address}</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p class="footer-disclaimer">${t('footer.disclaimer', locale)}</p>
      <span class="footer-copy">© 2026 Nueva Living · LIORA LIVING SL. · NIF B88827472</span>
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
