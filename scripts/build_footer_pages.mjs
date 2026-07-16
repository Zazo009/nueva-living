import { writeFileSync } from 'node:fs';

const home = 'index.html';
const fontPreloadBlock = `  <link rel="preload" href="assets/fonts/google/co3bmX5slCNuHLi8bLeY9MK7whWMhyjYqXtKky2F7g.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="assets/fonts/google/8vIJ7ww63mVu7gt79mT7PkRXMw.woff2" as="font" type="font/woff2" crossorigin>`;

const navLinks = [
  ['Approach', 'approach.html'],
  ['Developments', 'developments.html'],
  ['Areas', 'areas.html'],
  ['Advisory', 'advisory.html'],
  ['Contact Us', 'contact.html'],
];

const footerLinks = {
  company: [
    ['Our Approach', 'approach.html'],
    ['About', 'about.html'],
    ['Advisory', 'advisory.html'],
    ['Request Access', 'contact.html'],
  ],
  projects: [
    ['All Developments', 'developments.html'],
    ['Areas Overview', 'areas.html'],
    ['Marbella', 'areas.html#marbella'],
    ['Estepona', 'areas.html#estepona'],
    ['Benahav&iacute;s', 'areas.html#benahavis'],
    ['Nueva Andaluc&iacute;a', 'areas.html#nueva-andalucia'],
  ],
  legal: [
    ['Privacy Policy', 'privacy-policy.html'],
    ['Legal Notice', 'legal-notice.html'],
    ['Cookie Policy', 'cookie-policy.html'],
  ],
};

function nav() {
  return `<nav class="site-nav">
    <div class="nav-links nav-links-left">
      ${navLinks.slice(0, 2).map(([label, href]) => `<a href="${href}">${label}</a>`).join('\n      ')}
    </div>
    <a class="nav-logo" href="${home}" aria-label="Nueva Living home">
      <img src="assets/liora/brand/nueva-living-hero-logo-transparent.png?v=7" alt="Nueva Living" width="420" height="100">
    </a>
    <div class="nav-links nav-links-right">
      ${navLinks.slice(2).map(([label, href]) => `<a href="${href}">${label}</a>`).join('\n      ')}
    </div>
    <button class="nav-burger" type="button" aria-label="Menu" aria-controls="mobileMenu" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
  </nav>
  <div class="mobile-menu" id="mobileMenu">
    ${navLinks.map(([label, href]) => `<a href="${href}">${label}</a>`).join('\n    ')}
  </div>`;
}

function breadcrumb(currentLabel) {
  return `<nav class="breadcrumb-bar" aria-label="Breadcrumb">
    <ol class="breadcrumb-list">
      <li><a href="${home}">Home</a></li>
      <li><span aria-current="page">${currentLabel}</span></li>
    </ol>
  </nav>`;
}

function footer() {
  const list = (items) => items.map(([label, href]) => `<li><a href="${href}">${label}</a></li>`).join('\n          ');
  return `<footer>
    <div class="footer-grid">
      <div>
        <img class="footer-logo" src="assets/liora/brand/nueva-living-lockup-espresso-transparent.png?v=7" alt="Nueva Living" width="700" height="340">
        <p class="footer-about">A specialist advisory firm focused exclusively on new-build and off-plan property across the Costa del Sol. Serving international buyers with clarity and confidence.</p>
      </div>
      <div class="footer-col">
        <div class="footer-col-title">Company</div>
        <ul>
          ${list(footerLinks.company)}
        </ul>
      </div>
      <div class="footer-col">
        <div class="footer-col-title">Projects</div>
        <ul>
          ${list(footerLinks.projects)}
        </ul>
      </div>
      <div class="footer-col">
        <div class="footer-col-title">Contact</div>
        <ul>
          <li><a href="mailto:contact@nuevaliving.com">contact@nuevaliving.com</a></li>
          <li><a href="https://wa.me/46707576709" target="_blank" rel="noopener" data-whatsapp-advisor data-context="Nueva Living" data-intent="speak with an advisor" aria-label="Contact Nueva Living on WhatsApp">+46 707 57 67 09 · WhatsApp</a></li>
          <li><a href="areas.html#marbella">Marbella, Spain</a></li>
        </ul>
        <div class="footer-col-title" style="margin-top:24px;">Legal</div>
        <ul>
          ${list(footerLinks.legal)}
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>Information presented on this website is for general marketing purposes only and does not constitute legal, financial or investment advice. Development details, prices and delivery dates are subject to change without notice.</p>
      <span>&copy; 2026 Nueva Living</span>
    </div>
  </footer>`;
}

function page({ title, breadcrumbTitle, description, heroImage, heroKicker, heroTitle, heroLead, body }) {
  return `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>${title} | Nueva Living</title>
  <meta name="description" content="${description}">
  <link rel="icon" href="assets/liora/liora-favicon-512.png?v=6" type="image/png" sizes="512x512">
  <link rel="icon" href="assets/liora/favicon-32.png?v=6" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="assets/liora/apple-touch-icon.png?v=6" sizes="180x180">
${fontPreloadBlock}
  <link rel="stylesheet" href="assets/fonts/google/liora-fonts.css">
  <link rel="stylesheet" href="assets/liora/liora-pages.css">
</head>
<body>
  ${nav()}
  ${breadcrumb(breadcrumbTitle || title)}
  <main>
    <section class="page-hero">
      <img src="${heroImage}" alt="">
      <div class="hero-inner">
        <span class="kicker">${heroKicker}</span>
        <h1 class="display-title">${heroTitle}</h1>
        <p class="lead">${heroLead}</p>
      </div>
    </section>
    ${body}
  </main>
  ${footer()}
  <script>
    const burger = document.querySelector('.nav-burger');
    const menu = document.getElementById('mobileMenu');
    if (burger && menu) {
      burger.addEventListener('pointerdown', (event) => event.stopPropagation());
      burger.addEventListener('click', (event) => {
        event.preventDefault();
        event.stopPropagation();
        const open = menu.classList.toggle('open');
        burger.setAttribute('aria-expanded', open ? 'true' : 'false');
        document.body.classList.toggle('menu-open', open);
      });
      menu.querySelectorAll('a').forEach((link) => {
        link.addEventListener('click', () => {
          menu.classList.remove('open');
          burger.setAttribute('aria-expanded', 'false');
          document.body.classList.remove('menu-open');
        });
      });
    }
  </script>
</body>
</html>`;
}

const pages = [
  {
    file: 'approach.html',
    title: 'Our Approach',
    description: 'A considered advisory approach to Costa del Sol new developments.',
    heroImage: 'assets/liora/viewing/scene-02.jpg',
    heroKicker: 'Our Approach',
    heroTitle: 'A clearer way into <em>new development</em>',
    heroLead: 'We reduce the market to the projects that deserve attention, then guide each buyer through comparison, reservation and completion with calm precision.',
    body: `<section class="section">
      <div class="section-inner split">
        <div>
          <span class="label">Buyer Led</span>
          <div class="rule"></div>
          <h2 class="section-title">Clarity before <em>choice</em></h2>
          <p class="body-copy">The Costa del Sol new-build market is active, fragmented and often noisy. Our role is to make the landscape legible: which developers are credible, which locations hold value, which payment structures make sense, and which opportunities align with the way you actually want to live or invest.</p>
        </div>
        <div class="image-panel"><img src="assets/liora/advisory-property.jpg" alt="Costa del Sol property advisory setting"></div>
      </div>
    </section>
    <section class="section quiet-band">
      <div class="section-inner">
        <div class="section-head">
          <span class="label">How We Work</span>
          <div class="rule"></div>
          <h2 class="section-title">A structured search with <em>human judgement</em></h2>
        </div>
        <div class="cards">
          <article class="card"><div class="card-number">01</div><h3>Curated Shortlist</h3><p>We filter projects by location, developer record, specification, delivery phase, pricing and long-term market relevance.</p></article>
          <article class="card"><div class="card-number">02</div><h3>Project Diligence</h3><p>We review the information buyers often receive too late: master plans, payment structures, reservation terms and comparable supply.</p></article>
          <article class="card"><div class="card-number">03</div><h3>Decision Support</h3><p>You receive a clear comparison of strengths, compromises and next steps before committing to a viewing or reservation.</p></article>
        </div>
      </div>
    </section>
    <section class="section">
      <div class="section-inner">
        <div class="section-head center">
          <span class="label">Process</span>
          <div class="rule"></div>
          <h2 class="section-title">From first enquiry to <em>reservation</em></h2>
          <p class="body-copy" style="margin-left:auto;margin-right:auto;">A quiet, sequenced process keeps decisions moving without pressure.</p>
        </div>
        <div class="cards">
          <article class="card"><div class="card-number">1</div><h3>Requirement Call</h3><p>We define budget, timing, area, lifestyle, rental expectations and non-negotiables.</p></article>
          <article class="card"><div class="card-number">2</div><h3>Private Selection</h3><p>You receive a focused shortlist with context, availability and current pricing.</p></article>
          <article class="card"><div class="card-number">3</div><h3>Viewing &amp; Next Step</h3><p>We coordinate viewings, project material, reservation terms and independent legal introduction.</p></article>
        </div>
      </div>
    </section>
    <section class="cta-band"><div class="cta-inner"><h2 class="cta-title">Start with a private brief, not a property feed.</h2><a class="btn" href="contact.html">Request Access</a></div></section>`,
  },
  {
    file: 'areas.html',
    title: 'Areas',
    description: 'Costa del Sol area guide for new development buyers.',
    heroImage: 'assets/liora/viewing/scene-01.jpg',
    heroKicker: 'Locations',
    heroTitle: 'The Costa del Sol, <em>area by area</em>',
    heroLead: 'Each area has a different rhythm, buyer profile and long-term value story. The right choice depends on lifestyle, access, view, rental plan and exit depth.',
    body: `<section class="section"><div class="section-inner"><div class="section-head"><span class="label">Area Guide</span><div class="rule"></div><h2 class="section-title">Where new development <em>makes sense</em></h2><p class="body-copy">We assess locations through demand, infrastructure, scarcity, price depth and the everyday experience of living there.</p></div><div class="area-stack">
      <article class="area-row" id="marbella"><img src="assets/liora/areas/marbella.jpg" alt="Marbella coastline at sunrise with La Concha mountain" width="1920" height="2880"><div class="area-copy"><span class="label">Marbella</span><h3>The established reference point</h3><p>Marbella remains the strongest luxury address on the coast, with enduring demand from the Golden Mile to Sierra Blanca and a deep international buyer pool.</p></div></article>
      <article class="area-row" id="estepona"><img src="assets/liora/areas/estepona.jpg" alt="Estepona old town street with white houses and flower pots" width="1920" height="1278"><div class="area-copy"><span class="label">Estepona</span><h3>Infrastructure-led momentum</h3><p>Estepona has become one of the most active new-build markets, supported by town improvements, coastal access and a strong development pipeline.</p></div></article>
      <article class="area-row" id="benahavis"><img src="assets/liora/areas/benahavis.jpg" alt="Benahavis mountain village and elevated hillside landscape" width="1920" height="1280"><div class="area-copy"><span class="label">Benahavis</span><h3>Privacy, elevation and views</h3><p>An elevated enclave above Marbella, Benahavis is known for gated communities, villas, panoramic views and a quieter form of luxury living.</p></div></article>
      <article class="area-row" id="nueva-andalucia"><img src="assets/liora/areas/nueva-andalucia.jpg" alt="Puerto Banus marina and La Concha near Nueva Andalucia" width="1920" height="1280"><div class="area-copy"><span class="label">Nueva Andalucia</span><h3>Golf Valley lifestyle</h3><p>Close to Puerto Banus and surrounded by golf, Nueva Andalucia suits buyers who want amenities, established demand and a more active year-round setting.</p></div></article>
      <article class="area-row" id="mijas-fuengirola"><img src="assets/liora/areas/fuengirola.jpg" alt="Fuengirola seafront sign with palms and Mediterranean water" width="1920" height="2560"><div class="area-copy"><span class="label">Mijas &amp; Fuengirola</span><h3>Connectivity and value</h3><p>A diverse coastal corridor offering newer developments, strong services and convenient access to Malaga, often with more accessible entry pricing.</p></div></article>
    </div></div></section>
    <section class="cta-band"><div class="cta-inner"><h2 class="cta-title">Not sure which area fits? Start with a private area brief.</h2><a class="btn" href="contact.html">Request Area Advice</a></div></section>`,
  },
  {
    file: 'advisory.html',
    title: 'Advisory',
    description: 'Buyer-focused advisory for Costa del Sol new development purchases.',
    heroImage: 'assets/liora/advisory-property.jpg',
    heroKicker: 'Advisory',
    heroTitle: 'Advice before <em>appetite</em>',
    heroLead: 'We help buyers understand the market before falling in love with a unit: location, developer credibility, specification, payment plan and resale depth.',
    body: `<section class="section"><div class="section-inner split"><div><span class="label">Independent View</span><div class="rule"></div><h2 class="section-title">A buyer-focused <em>filter</em></h2><p class="body-copy">Developer brochures are designed to sell. Our advisory work sits beside that material and helps buyers understand what is strong, what is ordinary, and what deserves further diligence.</p></div><div class="image-panel"><img src="assets/liora/viewing/scene-13.jpg" alt="Interior detail"></div></div></section>
    <section class="section quiet-band"><div class="section-inner"><div class="section-head"><span class="label">Advisory Scope</span><div class="rule"></div><h2 class="section-title">What we help you <em>evaluate</em></h2></div><div class="cards"><article class="card"><h3>Project Comparison</h3><p>Side-by-side assessment of pricing, orientation, amenities, delivery timing and surrounding supply.</p></article><article class="card"><h3>Purchase Strategy</h3><p>Guidance around primary use, holiday use, rental strategy, financing readiness and exit expectations.</p></article><article class="card"><h3>Reservation Path</h3><p>Coordination of project material, viewing sequence, independent legal counsel and reservation steps.</p></article></div></div></section>
    <section class="section"><div class="section-inner"><div class="section-head center"><span class="label">Principles</span><div class="rule"></div><h2 class="section-title">Quiet guidance, <em>clear judgement</em></h2></div><div class="cards two"><article class="card"><h3>No inflated shortlist</h3><p>We would rather show three suitable projects than thirty generic options.</p></article><article class="card"><h3>No pressure theatre</h3><p>Urgency only matters when it is real: availability, price movement or reservation deadlines.</p></article></div></div></section>
    <section class="cta-band"><div class="cta-inner"><h2 class="cta-title">Bring the decision into focus before you reserve.</h2><a class="btn" href="contact.html">Speak Privately</a></div></section>`,
  },
  {
    file: 'about.html',
    title: 'About',
    description: 'About Nueva Living, a Costa del Sol new development advisory firm.',
    heroImage: 'assets/liora/viewing/scene-19.jpg',
    heroKicker: 'About Nueva Living',
    heroTitle: 'Focused only on <em>new development</em>',
    heroLead: 'Nueva Living was created for buyers who want a calmer, more informed way into the Costa del Sol new-build market.',
    body: `<section class="section"><div class="section-inner split"><div class="image-panel logo-panel"><img src="assets/liora/brand/nueva-living-lockup-sand-transparent.png?v=7" alt="Nueva Living logo" width="700" height="340"></div><div><span class="label">The Firm</span><div class="rule"></div><h2 class="section-title">Specialist by <em>design</em></h2><p class="body-copy">By focusing exclusively on new developments and off-plan opportunities, we can provide sharper context, stronger developer relationships and a more precise advisory experience than a generalist agency.</p><p class="body-copy">Our work is built around clarity: what is available, what is credible, what fits, and what should be left alone.</p></div></div></section>
    <section class="section quiet-band"><div class="section-inner"><div class="cards"><article class="card"><div class="card-number">40+</div><h3>Developer Relationships</h3><p>Direct conversations and project access across key Costa del Sol micro-markets.</p></article><article class="card"><div class="card-number">7</div><h3>Key Areas Covered</h3><p>From Marbella and Benahavis to Estepona, Nueva Andalucia, Mijas and Fuengirola.</p></article><article class="card"><div class="card-number">100%</div><h3>New-Build Focus</h3><p>A clear specialism that keeps advice concentrated and relevant.</p></article></div></div></section>
    <section class="section"><div class="section-inner"><div class="section-head"><span class="label">What We Stand For</span><div class="rule"></div><h2 class="section-title">Access, discretion and <em>clarity</em></h2></div><div class="cards"><article class="card"><h3>Discretion</h3><p>Private requirements are handled carefully, with no broad sharing of buyer details.</p></article><article class="card"><h3>Selectivity</h3><p>We prioritise fewer, stronger opportunities over a noisy catalogue.</p></article><article class="card"><h3>Context</h3><p>Every recommendation is framed by area, developer, timing and long-term logic.</p></article></div></div></section>
    <section class="cta-band"><div class="cta-inner"><h2 class="cta-title">Tell us what you are looking for, and we will curate the next step.</h2><a class="btn" href="contact.html">Request Access</a></div></section>`,
  },
  {
    file: 'contact.html',
    title: 'Request Access',
    breadcrumbTitle: 'Contact Us',
    description: 'Request private access to curated Costa del Sol new development opportunities.',
    heroImage: 'assets/liora/viewing/scene-08.jpg',
    heroKicker: 'Private Access',
    heroTitle: 'Receive a curated <em>private shortlist</em>',
    heroLead: 'Share your requirements and we will respond with relevant new development opportunities, project material and a recommended next step.',
    body: `<section class="section"><div class="section-inner"><div class="section-head center"><span class="label">Your Brief</span><div class="rule"></div><h2 class="section-title">Start with the right <em>conversation</em></h2><p class="body-copy" style="margin-left:auto;margin-right:auto;">Share a short brief and we will respond with relevant project material, current availability and a recommended next step.</p></div><form class="form-panel" name="liora-access-request" method="POST" data-netlify="true" netlify-honeypot="bot-field" action="/thank-you.html"><input type="hidden" name="form-name" value="liora-access-request"><input type="hidden" name="subject" data-remove-prefix value="New Nueva Living contact enquiry"><p style="display:none"><label>Do not fill this out <input name="bot-field"></label></p><input type="hidden" id="request-context" name="request_context" value="General private access request"><div class="form-grid"><div class="field"><label for="name">Full Name</label><input id="name" name="name" autocomplete="name" placeholder="Your name" required></div><div class="field"><label for="email">Email Address</label><input id="email" name="email" type="email" autocomplete="email" placeholder="your@email.com" required></div><div class="field"><label for="phone">Phone Number</label><input id="phone" name="phone" type="tel" autocomplete="tel" placeholder="+34 or international"></div><div class="field"><label for="area">Preferred Area</label><select id="area" name="preferred_area"><option value="">Select area...</option><option>Marbella</option><option>Estepona</option><option>Benahavis</option><option>Nueva Andalucia</option><option>Open to all areas</option></select></div><div class="field"><label for="property-type">Property Type Interest</label><select id="property-type" name="property_type_interest"><option value="">Select type...</option><option>Apartments</option><option>Penthouses</option><option>Villas</option><option>Townhouses</option><option>Mixed / Open</option></select></div><div class="field"><label for="budget">Budget Range</label><select id="budget" name="budget_range"><option value="">Select budget...</option><option>&euro;300,000 - &euro;500,000</option><option>&euro;500,000 - &euro;900,000</option><option>&euro;900,000 - &euro;1,500,000</option><option>&euro;1,500,000+</option></select></div><div class="field"><label for="purpose">Purchase Purpose</label><select id="purpose" name="purchase_purpose"><option value="">Select purpose...</option><option>Primary Residence</option><option>Holiday Home</option><option>Investment / Rental</option><option>Combination</option></select></div><div class="field full"><label for="message">Message</label><textarea id="message" name="message" placeholder="Tell us about your requirements..."></textarea></div></div><div style="margin-top:34px;display:flex;gap:18px;align-items:center;flex-wrap:wrap;"><button class="btn" type="submit">Submit Request</button><span class="form-response" style="color:var(--muted);font-size:12px;"></span></div></form></div></section>`,
  },
  {
    file: 'privacy-policy.html',
    title: 'Privacy Policy',
    description: 'Privacy policy draft for Nueva Living.',
    heroImage: 'assets/liora/viewing/scene-11.jpg',
    heroKicker: 'Legal',
    heroTitle: 'Privacy <em>Policy</em>',
    heroLead: 'A clear draft privacy notice for the Nueva Living website. This content should be reviewed by legal counsel before publication.',
    body: legalBody('Privacy Policy', [
      ['Overview', 'This draft explains how Nueva Living may collect and use personal information submitted through enquiry forms, email or direct communication. It is provided as website copy and should be reviewed before public launch.'],
      ['Information We May Collect', 'Name, contact details, preferred area, budget range, purchase purpose and any details voluntarily included in a message. We may also receive basic technical information from website hosting or analytics tools if added later.'],
      ['How Information Is Used', 'Information is used to respond to enquiries, prepare relevant project suggestions, coordinate viewings and maintain appropriate records of client communication.'],
      ['Sharing', 'Buyer details should only be shared with developers, legal advisers or other third parties where necessary for a requested enquiry, viewing, reservation or service step.'],
      ['Retention &amp; Rights', 'Personal data should be retained only for as long as needed for the enquiry or client relationship. Visitors may request access, correction or deletion by contacting contact@nuevaliving.com.'],
    ]),
  },
  {
    file: 'legal-notice.html',
    title: 'Legal Notice',
    description: 'Legal notice draft for Nueva Living.',
    heroImage: 'assets/liora/viewing/scene-15.jpg',
    heroKicker: 'Legal',
    heroTitle: 'Legal <em>Notice</em>',
    heroLead: 'A polished legal notice framework for the site. Company registration and regulatory details should be confirmed before publication.',
    body: legalBody('Legal Notice', [
      ['Website Owner', 'This website is presented under the Nueva Living brand. Full legal entity name, registered address, company number and tax details should be inserted before publication.'],
      ['Purpose Of The Website', 'The site provides general marketing information about new-build and off-plan property opportunities across the Costa del Sol. Content is indicative and subject to change.'],
      ['No Legal Or Financial Advice', 'Information on this website does not constitute legal, financial, tax or investment advice. Buyers should seek independent professional advice before making any property decision.'],
      ['Property Information', 'Prices, availability, plans, delivery dates and specifications are provided for general orientation and may change without notice. Final details must be confirmed directly through official developer documentation.'],
      ['Intellectual Property', 'Branding, layout, written content and original materials on this website may not be copied or reused without permission. Third-party images remain subject to their respective rights.'],
    ]),
  },
  {
    file: 'cookie-policy.html',
    title: 'Cookie Policy',
    description: 'Cookie policy draft for Nueva Living.',
    heroImage: 'assets/liora/viewing/scene-10.jpg',
    heroKicker: 'Legal',
    heroTitle: 'Cookie <em>Policy</em>',
    heroLead: 'A calm, readable cookie notice for the preview site. Final wording should be matched to the tools used at launch.',
    body: legalBody('Cookie Policy', [
      ['Current Preview', 'This static preview is designed without a marketing cookie banner or tracking setup. If analytics, advertising pixels or CRM tracking are added later, this policy should be updated.'],
      ['Essential Cookies', 'Essential cookies may be used to support basic website function, security, form handling or preference storage where required.'],
      ['Analytics Cookies', 'If analytics tools are added, they may help understand page visits, device type and general website performance. Non-essential analytics should be disclosed and controlled appropriately.'],
      ['Third-Party Services', 'The site may load fonts, images, maps, video embeds or form tools from third-party providers. These providers may process technical data according to their own policies.'],
      ['Managing Preferences', 'Visitors can manage cookies through browser settings. A dedicated consent tool should be added if non-essential cookies are used at public launch.'],
    ]),
  },
];

function legalBody(title, sections) {
  return `<section class="section"><div class="section-inner legal-layout"><aside class="legal-nav">${sections.map(([heading]) => `<a href="#${slug(heading)}">${heading}</a>`).join('')}</aside><div class="legal-stack"><div class="section-head"><span class="label">Draft Notice</span><div class="rule"></div><h2 class="section-title">${title}</h2><p class="body-copy">This is polished website draft copy and should be reviewed by qualified legal counsel before publication.</p></div>${sections.map(([heading, text]) => `<article class="legal-card" id="${slug(heading)}"><h3>${heading}</h3><p>${text}</p></article>`).join('')}</div></div></section><section class="cta-band"><div class="cta-inner"><h2 class="cta-title">Need project-specific clarification?</h2><a class="btn" href="contact.html">Contact Nueva</a></div></section>`;
}

function slug(value) {
  return value.toLowerCase().replace(/&amp;/g, 'and').replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
}

for (const item of pages) {
  writeFileSync(item.file, page(item));
}

console.log(JSON.stringify({ pages: pages.map((item) => item.file) }, null, 2));
