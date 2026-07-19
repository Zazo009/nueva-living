import { existsSync, readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const areas = JSON.parse(readFileSync('content/nueva-areas.json', 'utf8'));
const projects = readdirSync('content/liora-projects', { withFileTypes: true })
  .filter((entry) => entry.isDirectory())
  .map((entry) => join('content/liora-projects', entry.name, 'project.json'))
  .filter((file) => existsSync(file))
  .map((file) => JSON.parse(readFileSync(file, 'utf8')));

const home = 'index.html';
const fontPreloadBlock = `  <link rel="preload" href="assets/fonts/google/co3bmX5slCNuHLi8bLeY9MK7whWMhyjYqXtKky2F7g.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="assets/fonts/google/8vIJ7ww63mVu7gt79mT7PkRXMw.woff2" as="font" type="font/woff2" crossorigin>`;

const navLinks = [
  ['Approach', 'approach.html'],
  ['Why Nueva', 'why-nueva.html'],
  ['Developments', 'developments.html'],
  ['Areas', 'areas.html'],
  ['Advisory', 'advisory.html'],
  ['Contact Us', 'contact.html'],
];

const footerLinks = {
  company: [
    ['Our Approach', 'approach.html'],
    ['Why Nueva Living', 'why-nueva.html'],
    ['About', 'about.html'],
    ['Advisory', 'advisory.html'],
    ['Contact Us', 'contact.html'],
  ],
  projects: [
    ['All Developments', 'developments.html'],
    ['Areas Overview', 'areas.html'],
    ['Marbella', 'area-marbella.html'],
    ['Estepona', 'area-estepona.html'],
    ['Benahav&iacute;s', 'area-benahavis.html'],
    ['Nueva Andaluc&iacute;a', 'area-nueva-andalucia.html'],
    ['Mijas &amp; Fuengirola', 'area-mijas-fuengirola.html'],
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
      ${navLinks.slice(0, 3).map(([label, href]) => `<a href="${href}">${label}</a>`).join('\n      ')}
    </div>
    <a class="nav-logo" href="${home}" aria-label="Nueva Living home">
      <img src="assets/liora/brand/nueva-living-hero-logo-transparent.png?v=7" alt="Nueva Living" width="420" height="100">
    </a>
    <div class="nav-links nav-links-right">
      ${navLinks.slice(3).map(([label, href]) => `<a href="${href}">${label}</a>`).join('\n      ')}
    </div>
    <button class="nav-burger" type="button" aria-label="Menu" aria-controls="mobileMenu" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
  </nav>
  <div class="mobile-menu" id="mobileMenu">
    ${navLinks.map(([label, href]) => `<a href="${href}">${label}</a>`).join('\n    ')}
  </div>`;
}

function breadcrumb(currentLabel, parents = []) {
  const parentItems = parents.map(([label, href]) => `<li><a href="${esc(href)}">${esc(label)}</a></li>`).join('\n      ');
  return `<nav class="breadcrumb-bar" aria-label="Breadcrumb">
    <ol class="breadcrumb-list">
      <li><a href="${home}">Home</a></li>${parentItems ? `
      ${parentItems}` : ''}
      <li><span aria-current="page">${esc(currentLabel)}</span></li>
    </ol>
  </nav>`;
}

function footer() {
  const list = (items) => items.map(([label, href]) => `<li><a href="${href}">${label}</a></li>`).join('\n          ');
  return `<footer>
    <div class="footer-grid">
      <div>
        <img class="footer-logo" src="assets/liora/brand/nueva-living-lockup-espresso-transparent.png?v=7" alt="Nueva Living" width="700" height="340">
        <p class="footer-about">We help international buyers find and compare new-build and off-plan homes across the Costa del Sol.</p>
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
          <li><a href="area-marbella.html">Marbella, Spain</a></li>
        </ul>
        <div class="footer-col-title" style="margin-top:24px;">Legal</div>
        <ul>
          ${list(footerLinks.legal)}
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>Information presented on this website is for general marketing purposes only and does not constitute legal, financial or investment advice. Development details, prices and delivery dates are subject to change without notice.</p>
      <span>&copy; 2026 Nueva Living &middot; LIORA LIVING SL. &middot; NIF B88827472</span>
    </div>
  </footer>`;
}

function page({ title, breadcrumbTitle, breadcrumbs, description, heroImage, heroAlt = '', heroWidth, heroHeight, heroPosition, heroKicker, heroTitle, heroLead, body, bodyClass = '' }) {
  return `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>${esc(title)} | Nueva Living</title>
  <meta name="description" content="${esc(description)}">
  <link rel="icon" href="assets/liora/liora-favicon-512.png?v=6" type="image/png" sizes="512x512">
  <link rel="icon" href="assets/liora/favicon-32.png?v=6" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="assets/liora/apple-touch-icon.png?v=6" sizes="180x180">
${fontPreloadBlock}
  <link rel="stylesheet" href="assets/fonts/google/liora-fonts.css">
  <link rel="stylesheet" href="assets/liora/liora-pages.css">
</head>
<body${bodyClass ? ` class="${bodyClass}"` : ''}>
  ${nav()}
  ${breadcrumb(breadcrumbTitle || title, breadcrumbs)}
  <main>
    <section class="page-hero">
      <img src="${esc(heroImage)}" alt="${esc(heroAlt)}"${heroWidth ? ` width="${heroWidth}"` : ''}${heroHeight ? ` height="${heroHeight}"` : ''}${heroPosition ? ` style="object-position:${esc(heroPosition)}"` : ''} loading="eager" fetchpriority="high" decoding="async">
      <div class="hero-inner">
        <span class="kicker">${esc(heroKicker)}</span>
        <h1 class="display-title">${heroTitle}</h1>
        <p class="lead">${esc(heroLead)}</p>
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

function esc(value) {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function areaProjectCard(project) {
  const image = project.images?.hero || {};
  const meta = project.card?.meta || [];
  const projectType = project.hero?.type || project.quickFacts?.find(([label]) => label === 'Property type')?.[1] || 'New development';
  return `<article class="project-card area-project-card" data-project-card>
    <img src="${esc(image.src)}" alt="${esc(image.alt || project.name)}" width="${image.width || 1600}" height="${image.height || 900}" loading="lazy" decoding="async">
    <div class="project-body">
      <span class="label">${esc(project.card?.label || project.hero?.location || 'New Development')}</span>
      <h3>${esc(project.name)}</h3>
      <p>${esc(project.card?.description || project.description)}</p>
      <div class="meta">${meta.slice(0, 3).map(([label, value]) => `<div><span>${esc(label)}</span><strong>${esc(value)}</strong></div>`).join('')}</div>
      <div class="project-tags"><span>${esc(projectType)}</span><span>Current Availability</span></div>
      <a class="project-link" href="${esc(project.output)}">Explore Project</a>
    </div>
  </article>`;
}

function areaProjects(area) {
  const selected = area.featuredProjects
    .map((projectSlug) => projects.find((project) => project.slug === projectSlug))
    .filter(Boolean);

  if (selected.length) return selected.map(areaProjectCard).join('\n');

  return `<article class="area-project-empty">
    <span class="label">Private Selection</span>
    <h3>Current opportunities available by request</h3>
    <p>We do not publish a project here until its information is ready to compare. Tell us what you need and we will check the current Mijas and Fuengirola releases directly.</p>
    <a class="project-link" href="#area-enquiry">Request a Shortlist</a>
  </article>`;
}

function areaPriceSources(area) {
  const sources = area.priceSources || [{ label: 'View market reference', url: area.priceSource }];
  return sources
    .filter((source) => source.url)
    .map((source) => `<a href="${esc(source.url)}" target="_blank" rel="noopener noreferrer">${esc(source.label)}</a>`)
    .join('');
}

function areaForm(area) {
  const areaOptions = areas.map((option) => (
    `<option value="${esc(option.formArea)}"${option.slug === area.slug ? ' selected' : ''}>${esc(option.name)}</option>`
  )).join('');

  return `<form class="form-panel area-form" name="nueva-${esc(area.slug)}-enquiry" method="POST" data-crm-lead action="/.netlify/functions/nueva-lead">
    <input type="hidden" name="subject" data-remove-prefix value="New Nueva Living ${esc(area.name)} enquiry">
    <input type="hidden" name="request_context" value="${esc(area.name)} area enquiry">
    <div class="form-grid">
      <div class="field"><label for="${esc(area.slug)}-first-name">First Name</label><input id="${esc(area.slug)}-first-name" name="first_name" autocomplete="given-name" placeholder="First name" required></div>
      <div class="field"><label for="${esc(area.slug)}-last-name">Last Name</label><input id="${esc(area.slug)}-last-name" name="last_name" autocomplete="family-name" placeholder="Last name" required></div>
      <div class="field"><label for="${esc(area.slug)}-email">Email Address</label><input id="${esc(area.slug)}-email" name="email" type="email" autocomplete="email" placeholder="your@email.com" required></div>
      <div class="field"><label for="${esc(area.slug)}-phone">Phone Number</label><input id="${esc(area.slug)}-phone" name="phone" type="tel" autocomplete="tel" placeholder="+34 or international"></div>
      <div class="field"><label for="${esc(area.slug)}-area">Preferred Area</label><select id="${esc(area.slug)}-area" name="preferred_area">${areaOptions}<option value="Open to all areas">Open to all areas</option></select></div>
      <div class="field"><label for="${esc(area.slug)}-property-type">Property Type</label><select id="${esc(area.slug)}-property-type" name="property_type_interest"><option value="">Select type...</option><option>Apartments</option><option>Penthouses</option><option>Villas</option><option>Townhouses</option><option>Mixed / Open</option></select></div>
      <div class="field"><label for="${esc(area.slug)}-budget">Budget Range</label><select id="${esc(area.slug)}-budget" name="budget_range"><option value="">Select budget...</option><option>&euro;300,000 - &euro;500,000</option><option>&euro;500,000 - &euro;900,000</option><option>&euro;900,000 - &euro;1,500,000</option><option>&euro;1,500,000+</option></select></div>
      <div class="field"><label for="${esc(area.slug)}-bedrooms">Minimum Bedrooms</label><select id="${esc(area.slug)}-bedrooms" name="bedrooms_min"><option value="">Any</option><option value="1">1+</option><option value="2">2+</option><option value="3">3+</option><option value="4">4+</option></select></div>
      <div class="field full"><label for="${esc(area.slug)}-message">Message</label><textarea id="${esc(area.slug)}-message" name="message">${esc(area.formMessage)}</textarea></div>
      <label class="consent-row field full" for="${esc(area.slug)}-consent"><input id="${esc(area.slug)}-consent" name="consent" type="checkbox" required><span>I agree to be contacted and for my data to be stored.</span></label>
      <label class="consent-row field full" for="${esc(area.slug)}-marketing"><input id="${esc(area.slug)}-marketing" name="marketing_opt_in" type="checkbox"><span>I would also like to receive occasional project updates from Nueva Living.</span></label>
    </div>
    <div class="form-actions"><button class="btn" type="submit">Send Enquiry</button><span class="form-response"></span></div>
  </form>`;
}

function areaDetailPage(area) {
  const priceItems = area.prices.map((price) => `<div class="area-price-item"><span>${esc(price.label)}</span><strong>${esc(price.value)}</strong></div>`).join('');
  const highlights = area.highlights.map(([title, copy], index) => `<article class="area-highlight"><span>${String(index + 1).padStart(2, '0')}</span><h3>${esc(title)}</h3><p>${esc(copy)}</p></article>`).join('');
  const paragraphs = area.intro.paragraphs.map((paragraph) => `<p class="body-copy">${esc(paragraph)}</p>`).join('');

  return {
    file: area.output,
    title: `${area.name} Area Guide`,
    breadcrumbTitle: area.name,
    breadcrumbs: [['Areas', 'areas.html']],
    description: area.seo.description,
    heroImage: area.hero.image,
    heroAlt: area.hero.alt,
    heroWidth: area.hero.width,
    heroHeight: area.hero.height,
    heroPosition: area.hero.position,
    heroKicker: area.hero.kicker,
    heroTitle: area.hero.titleHtml,
    heroLead: area.hero.lead,
    bodyClass: 'area-detail-page',
    body: `<section class="section area-introduction"><div class="section-inner area-intro-layout"><div><span class="label">Living in ${esc(area.name)}</span><div class="rule"></div><h2 class="section-title">${area.intro.headlineHtml}</h2>${paragraphs}</div><div class="area-highlights">${highlights}</div></div></section>
    <section class="section quiet-band area-market"><div class="section-inner area-market-layout"><div><span class="label">Price Context</span><div class="rule"></div><h2 class="section-title">Current asking-price <em>reference</em></h2><p class="body-copy">Use the area average for orientation only. New-build pricing depends heavily on the exact location, specification and views.</p></div><div class="area-price-panel">${priceItems}<p>${esc(area.priceNote)}</p><div class="area-price-sources">${areaPriceSources(area)}</div></div></div></section>
    <section class="section area-developments"><div class="section-inner"><div class="section-head"><span class="label">Current Match</span><div class="rule"></div><h2 class="section-title">Projects in <em>${esc(area.name)}</em></h2><p class="body-copy">Only projects currently matching this area are shown. Price and availability are confirmed before a viewing.</p></div><div class="project-grid area-project-grid">${areaProjects(area)}</div></div></section>
    <section class="section area-enquiry-section" id="area-enquiry"><div class="section-inner"><div class="section-head center"><span class="label">Ask About ${esc(area.name)}</span><div class="rule"></div><h2 class="section-title">Request a relevant <em>shortlist</em></h2><p class="body-copy" style="margin-left:auto;margin-right:auto;">Tell us your budget and priorities. We will reply with matching projects and current availability.</p></div>${areaForm(area)}</div></section>`,
  };
}

const pages = [
  {
    file: 'approach.html',
    title: 'Our Approach',
    description: 'How Nueva Living helps buyers find and compare Costa del Sol new developments.',
    heroImage: 'assets/liora/viewing/scene-02.jpg',
    heroKicker: 'Our Approach',
    heroTitle: 'A simpler way to buy <em>a new home</em>',
    heroLead: 'We narrow down the market, compare the right projects and help you from the first shortlist through to completion.',
    body: `<section class="section">
      <div class="section-inner split">
        <div>
          <span class="label">Built Around You</span>
          <div class="rule"></div>
          <h2 class="section-title">Understand the options before <em>you choose</em></h2>
          <p class="body-copy">There are a lot of new projects on the Costa del Sol, and they are not all equally good. We help you understand the developer, location, payment plan and whether the home actually fits the way you want to live.</p>
        </div>
        <div class="image-panel"><img src="assets/liora/advisory-property.jpg" alt="Costa del Sol property advisory setting"></div>
      </div>
    </section>
    <section class="section quiet-band">
      <div class="section-inner">
        <div class="section-head">
          <span class="label">How We Work</span>
          <div class="rule"></div>
          <h2 class="section-title">A focused search with <em>real guidance</em></h2>
        </div>
        <div class="cards">
          <article class="card"><div class="card-number">01</div><h3>Your Shortlist</h3><p>We filter projects by location, developer, quality, completion date and price.</p></article>
          <article class="card"><div class="card-number">02</div><h3>The Important Details</h3><p>We check master plans, payment schedules, reservation terms and nearby alternatives before you decide.</p></article>
          <article class="card"><div class="card-number">03</div><h3>A Clear Comparison</h3><p>You see the strengths, trade-offs and next steps before booking a viewing or making a reservation.</p></article>
        </div>
      </div>
    </section>
    <section class="section">
      <div class="section-inner">
        <div class="section-head center">
          <span class="label">Process</span>
          <div class="rule"></div>
          <h2 class="section-title">From first enquiry to <em>reservation</em></h2>
          <p class="body-copy" style="margin-left:auto;margin-right:auto;">A simple step-by-step process, with no pressure.</p>
        </div>
        <div class="cards">
          <article class="card"><div class="card-number">1</div><h3>Tell Us What You Need</h3><p>We talk through your budget, timing, preferred areas and must-haves.</p></article>
          <article class="card"><div class="card-number">2</div><h3>Receive Your Shortlist</h3><p>You get a focused selection with current prices and availability.</p></article>
          <article class="card"><div class="card-number">3</div><h3>View and Decide</h3><p>We arrange viewings, share the project documents and explain the reservation process.</p></article>
        </div>
      </div>
    </section>
    <section class="cta-band"><div class="cta-inner"><h2 class="cta-title">Tell us what you are looking for and we will narrow it down.</h2><a class="btn" href="contact.html">Talk to Us</a></div></section>`,
  },
  {
    file: 'why-nueva.html',
    title: 'Why Choose Nueva Living',
    description: 'Why international buyers choose Nueva Living for clear, buyer-focused new-development advice on the Costa del Sol.',
    heroImage: 'assets/liora/advisory-property.jpg',
    heroAlt: 'Contemporary Costa del Sol home surrounded by Mediterranean planting',
    heroKicker: 'Why Nueva Living',
    heroTitle: 'A clearer way to find <em>the right new home</em>',
    heroLead: 'We combine local project knowledge with a focused, buyer-first process, from the first shortlist through to handover.',
    body: `<section class="section"><div class="section-inner split"><div><span class="label">What Sets Us Apart</span><div class="rule"></div><h2 class="section-title">Fewer options, better information and <em>no unnecessary pressure</em></h2><p class="body-copy">Buying from abroad can make every project look equally convincing. We help you compare the details that matter, explain the trade-offs and keep the search focused on homes that fit your plans.</p></div><div class="image-panel"><img src="assets/liora/viewing/scene-13.jpg" alt="Refined interior detail in a Costa del Sol residence" width="2048" height="1365" loading="lazy" decoding="async"></div></div></section>
    <section class="section quiet-band"><div class="section-inner"><div class="section-head"><span class="label">Why Buyers Choose Us</span><div class="rule"></div><h2 class="section-title">Practical support at <em>every stage</em></h2></div><div class="cards why-cards">
      <article class="card"><div class="card-number">01</div><h3>Local Expertise</h3><p>Years of hands-on experience with Costa del Sol areas, developers, new releases and the differences between nearby projects.</p></article>
      <article class="card"><div class="card-number">02</div><h3>Private Access</h3><p>Access to selected private releases and off-market availability when developers make it available.</p></article>
      <article class="card"><div class="card-number">03</div><h3>End-to-End Support</h3><p>Search, comparisons, viewings and negotiation, plus coordination with an independent lawyer for legal checks.</p></article>
      <article class="card"><div class="card-number">04</div><h3>Multilingual Guidance</h3><p>Clear communication in English, Spanish and Swedish throughout the buying process.</p></article>
      <article class="card"><div class="card-number">05</div><h3>Buyer-First Advice</h3><p>We explain strengths and trade-offs honestly, so the decision serves the buyer rather than simply completing a sale.</p></article>
      <article class="card"><div class="card-number">06</div><h3>Aftercare</h3><p>We stay available through handover and help connect you with relevant local services after completion.</p></article>
    </div></div></section>
    <section class="section"><div class="section-inner"><div class="section-head"><span class="label">Client Perspective</span><div class="rule"></div><h2 class="section-title">The experience we aim <em>to deliver</em></h2><p class="body-copy testimonial-disclaimer">Sample wording for layout only. These must be replaced with verified client feedback before being promoted as testimonials.</p></div><div class="cards testimonial-grid">
      <blockquote class="card testimonial-card"><p>“Nueva Living helped us reduce a long list to three options that genuinely matched how we wanted to live.”</p><footer>Sample testimonial · Marbella buyer</footer></blockquote>
      <blockquote class="card testimonial-card"><p>“The project comparison made the differences in location, payment terms and timing much easier to understand.”</p><footer>Sample testimonial · Estepona buyer</footer></blockquote>
      <blockquote class="card testimonial-card"><p>“Having one point of contact from the first viewing through to handover made buying from abroad feel manageable.”</p><footer>Sample testimonial · International buyer</footer></blockquote>
    </div></div></section>
    <section class="cta-band"><div class="cta-inner"><div><span class="label">Your Search</span><h2 class="cta-title">Tell us what matters to you. We will help narrow it down.</h2></div><a class="btn" href="contact.html#contact-form">Start Your Search</a></div></section>`,
  },
  {
    file: 'areas.html',
    title: 'Areas',
    description: 'Costa del Sol area guide for new development buyers.',
    heroImage: 'assets/liora/viewing/scene-01.jpg',
    heroKicker: 'Locations',
    heroTitle: 'The Costa del Sol, <em>area by area</em>',
    heroLead: 'Every area feels different. We help you compare daily life, travel times, views, prices and future resale demand.',
    body: `<section class="section"><div class="section-inner"><div class="section-head"><span class="label">Area Guide</span><div class="rule"></div><h2 class="section-title">Find the area that <em>fits you</em></h2><p class="body-copy">We look at what it is actually like to live there, how easy it is to get around and what supports long-term demand.</p></div><div class="area-stack">
      <a class="area-row" id="marbella" href="area-marbella.html" aria-label="Explore the Marbella area guide"><img src="assets/liora/areas/marbella.jpg" alt="Marbella coastline at sunrise with La Concha mountain" width="1920" height="2880" loading="lazy" decoding="async"><div class="area-copy"><span class="label">Marbella</span><h3>The coast's best-known address</h3><p>Marbella combines beaches, restaurants, international schools and established neighbourhoods, from the Golden Mile to Sierra Blanca.</p><span class="area-explore">Explore Marbella</span></div></a>
      <a class="area-row" id="estepona" href="area-estepona.html" aria-label="Explore the Estepona area guide"><img src="assets/liora/areas/estepona.jpg" alt="Estepona old town street with white houses and flower pots" width="1920" height="1278" loading="lazy" decoding="async"><div class="area-copy"><span class="label">Estepona</span><h3>A growing coastal town</h3><p>Estepona has seen major improvements in recent years, with a lively old town, good beach access and plenty of new projects.</p><span class="area-explore">Explore Estepona</span></div></a>
      <a class="area-row" id="benahavis" href="area-benahavis.html" aria-label="Explore the Benahavis area guide"><img src="assets/liora/areas/benahavis.jpg" alt="Benahavis mountain village and elevated hillside landscape" width="1920" height="1280" loading="lazy" decoding="async"><div class="area-copy"><span class="label">Benahavis</span><h3>Privacy, hills and open views</h3><p>Set above Marbella, Benahavis is known for gated communities, golf, villas and a quieter pace of life.</p><span class="area-explore">Explore Benahavis</span></div></a>
      <a class="area-row" id="nueva-andalucia" href="area-nueva-andalucia.html" aria-label="Explore the Nueva Andalucia area guide"><img src="assets/liora/areas/nueva-andalucia.jpg" alt="Puerto Banus marina and La Concha near Nueva Andalucia" width="1920" height="1280" loading="lazy" decoding="async"><div class="area-copy"><span class="label">Nueva Andalucia</span><h3>Golf Valley living</h3><p>Close to Puerto Banus and surrounded by golf courses, Nueva Andalucia works well for buyers who want restaurants, services and year-round activity nearby.</p><span class="area-explore">Explore Nueva Andalucia</span></div></a>
      <a class="area-row" id="mijas-fuengirola" href="area-mijas-fuengirola.html" aria-label="Explore the Mijas and Fuengirola area guide"><img src="assets/liora/areas/fuengirola.jpg" alt="Fuengirola seafront sign with palms and Mediterranean water" width="1920" height="2560" loading="lazy" decoding="async"><div class="area-copy"><span class="label">Mijas &amp; Fuengirola</span><h3>Easy access and more choice</h3><p>This part of the coast offers good services, easy links to Malaga and a wider range of prices.</p><span class="area-explore">Explore Mijas &amp; Fuengirola</span></div></a>
    </div></div></section>
    <section class="cta-band"><div class="cta-inner"><h2 class="cta-title">Not sure where to start? Tell us what matters to you.</h2><a class="btn" href="contact.html">Ask About Areas</a></div></section>`,
  },
  {
    file: 'advisory.html',
    title: 'Advisory',
    description: 'Buyer-focused advisory for Costa del Sol new development purchases.',
    heroImage: 'assets/liora/advisory-property.jpg',
    heroKicker: 'Advisory',
    heroTitle: 'Know what you are buying <em>before you decide</em>',
    heroLead: 'We help you check the location, developer, finishes, payment plan and future resale appeal before you choose a home.',
    body: `<section class="section"><div class="section-inner split"><div><span class="label">An Independent View</span><div class="rule"></div><h2 class="section-title">Clear advice for <em>the buyer</em></h2><p class="body-copy">A developer brochure shows the project at its best. We help you look beyond it and understand what is genuinely strong, what is fairly standard and what needs a closer check.</p></div><div class="image-panel"><img src="assets/liora/viewing/scene-13.jpg" alt="Interior detail"></div></div></section>
    <section class="section quiet-band"><div class="section-inner"><div class="section-head"><span class="label">How We Help</span><div class="rule"></div><h2 class="section-title">The details we help you <em>compare</em></h2></div><div class="cards"><article class="card"><h3>Compare Projects</h3><p>We compare prices, orientation, amenities, completion dates and nearby alternatives side by side.</p></article><article class="card"><h3>Plan the Purchase</h3><p>We talk through how you will use the home, rental plans, financing and what you may want later.</p></article><article class="card"><h3>Reserve with Clarity</h3><p>We organise project documents, viewings, reservation details and an introduction to an independent lawyer.</p></article></div></div></section>
    <section class="section"><div class="section-inner"><div class="section-head center"><span class="label">Our Promise</span><div class="rule"></div><h2 class="section-title">Straight answers, <em>no pressure</em></h2></div><div class="cards two"><article class="card"><h3>A Shorter, Better List</h3><p>We would rather show you three suitable projects than thirty generic options.</p></article><article class="card"><h3>Real Urgency Only</h3><p>We only flag urgency when availability, pricing or a reservation deadline genuinely changes.</p></article></div></div></section>
    <section class="cta-band"><div class="cta-inner"><h2 class="cta-title">Talk through the options before you reserve.</h2><a class="btn" href="contact.html">Talk to an Advisor</a></div></section>`,
  },
  {
    file: 'about.html',
    title: 'About',
    description: 'About Nueva Living, a Costa del Sol new development advisory firm.',
    heroImage: 'assets/liora/viewing/scene-19.jpg',
    heroKicker: 'About Nueva Living',
    heroTitle: 'We focus on <em>new developments</em>',
    heroLead: 'Nueva Living was created for buyers who want straightforward help in the Costa del Sol new-build market.',
    body: `<section class="section"><div class="section-inner split"><div class="image-panel logo-panel"><img src="assets/liora/brand/nueva-living-lockup-sand-transparent.png?v=7" alt="Nueva Living logo" width="700" height="340"></div><div><span class="label">About Nueva Living</span><div class="rule"></div><h2 class="section-title">New builds are <em>what we know</em></h2><p class="body-copy">Because we only work with new and off-plan homes, we know the developers, the projects and the questions buyers should ask.</p><p class="body-copy">Our job is simple: show you what is available, explain what is good and help you leave the wrong options behind.</p></div></div></section>
    <section class="section quiet-band"><div class="section-inner"><div class="cards"><article class="card"><div class="card-number">40+</div><h3>Developers We Work With</h3><p>Direct conversations and project access across the main Costa del Sol areas.</p></article><article class="card"><div class="card-number">7</div><h3>Areas We Cover</h3><p>From Marbella and Benahavis to Estepona, Nueva Andalucia, Mijas and Fuengirola.</p></article><article class="card"><div class="card-number">100%</div><h3>Focused on New Builds</h3><p>One clear focus keeps our advice useful and up to date.</p></article></div></div></section>
    <section class="section"><div class="section-inner"><div class="section-head"><span class="label">What Matters to Us</span><div class="rule"></div><h2 class="section-title">Access, privacy and <em>clear advice</em></h2></div><div class="cards"><article class="card"><h3>Privacy</h3><p>We handle your requirements carefully and only share details when needed for your request.</p></article><article class="card"><h3>Fewer, Better Options</h3><p>We focus on the projects worth considering rather than sending you a long catalogue.</p></article><article class="card"><h3>The Full Picture</h3><p>Every recommendation includes the area, developer, timing and what may support future value.</p></article></div></div></section>
    <section class="cta-band"><div class="cta-inner"><h2 class="cta-title">Tell us what you are looking for and we will help with the next step.</h2><a class="btn" href="contact.html">Contact Us</a></div></section>`,
  },
  {
    file: 'contact.html',
    title: 'Contact Us',
    breadcrumbTitle: 'Contact Us',
    description: 'Tell Nueva Living what kind of new home you are looking for on the Costa del Sol.',
    heroImage: 'assets/liora/viewing/scene-08.jpg',
    heroKicker: 'Contact Nueva Living',
    heroTitle: 'Tell us what you are <em>looking for</em>',
    heroLead: 'Share a few details and we will come back with relevant projects, current availability and a clear next step.',
    body: `<section class="section"><div class="section-inner"><div class="section-head center"><span class="label">Your Search</span><div class="rule"></div><h2 class="section-title">Let us help you <em>narrow it down</em></h2><p class="body-copy" style="margin-left:auto;margin-right:auto;">Tell us what matters to you. We will reply with the projects and information that best fit your search.</p></div><form class="form-panel" id="contact-form" name="liora-access-request" method="POST" data-crm-lead action="/.netlify/functions/nueva-lead"><input type="hidden" name="subject" data-remove-prefix value="New Nueva Living contact enquiry"><input type="hidden" id="request-context" name="request_context" value="General contact request"><div class="form-grid"><div class="field"><label for="first-name">First Name</label><input id="first-name" name="first_name" autocomplete="given-name" placeholder="First name" required></div><div class="field"><label for="last-name">Last Name</label><input id="last-name" name="last_name" autocomplete="family-name" placeholder="Last name" required></div><div class="field"><label for="email">Email Address</label><input id="email" name="email" type="email" autocomplete="email" placeholder="your@email.com" required></div><div class="field"><label for="phone">Phone Number</label><input id="phone" name="phone" type="tel" autocomplete="tel" placeholder="+34 or international"></div><div class="field"><label for="area">Preferred Area</label><select id="area" name="preferred_area"><option value="">Select area...</option><option>Marbella</option><option>Estepona</option><option>Benahavis</option><option>Nueva Andalucia</option><option>Open to all areas</option></select></div><div class="field"><label for="property-type">Property Type</label><select id="property-type" name="property_type_interest"><option value="">Select type...</option><option>Apartments</option><option>Penthouses</option><option>Villas</option><option>Townhouses</option><option>Mixed / Open</option></select></div><div class="field"><label for="budget">Budget Range</label><select id="budget" name="budget_range"><option value="">Select budget...</option><option>&euro;300,000 - &euro;500,000</option><option>&euro;500,000 - &euro;900,000</option><option>&euro;900,000 - &euro;1,500,000</option><option>&euro;1,500,000+</option></select></div><div class="field"><label for="purpose">How Will You Use It?</label><select id="purpose" name="purchase_purpose"><option value="">Select purpose...</option><option>Primary Residence</option><option>Holiday Home</option><option>Investment / Rental</option><option>Combination</option></select></div><div class="field full"><label for="message">Message</label><textarea id="message" name="message" placeholder="Tell us what you are looking for..."></textarea></div><label class="consent-row field full" for="consent"><input id="consent" name="consent" type="checkbox" required><span>I agree to be contacted and for my data to be stored.</span></label><label class="consent-row field full" for="marketing-opt-in"><input id="marketing-opt-in" name="marketing_opt_in" type="checkbox"><span>I would also like to receive occasional project updates from Nueva Living.</span></label></div><div class="form-actions"><button class="btn" type="submit">Send Enquiry</button><span class="form-response"></span></div></form></div></section>`,
  },
  {
    file: 'privacy-policy.html',
    title: 'Privacy Policy',
    description: 'Privacy policy draft for Nueva Living.',
    heroImage: 'assets/liora/viewing/scene-11.jpg',
    heroKicker: 'Legal',
    heroTitle: 'Privacy <em>Policy</em>',
    heroLead: 'How we collect, use and protect the information you share with us.',
    body: legalBody('Privacy Policy', [
      ['Overview', 'LIORA LIVING SL. (NIF B88827472), operating under the Nueva Living brand, is responsible for personal information submitted through enquiry forms, email or direct communication.'],
      ['Information We May Collect', 'Name, contact details, preferred area, budget range, purchase purpose and any details voluntarily included in a message. We may also receive basic technical information from website hosting or analytics tools if added later.'],
      ['How Information Is Used', 'Information is used to respond to enquiries, prepare relevant project suggestions, coordinate viewings and maintain appropriate records of client communication.'],
      ['Sharing', 'Enquiry details may be processed in Nueva Living\'s customer relationship management system and shared with developers, legal advisers or other service providers only where necessary for a requested enquiry, viewing, reservation or service step.'],
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
    heroLead: 'Who operates this website, what the information is for and the terms that apply.',
    body: legalBody('Legal Notice', [
      ['Website Owner', 'This website is presented under the Nueva Living brand and operated by LIORA LIVING SL., Tax ID (NIF) B88827472.'],
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
    heroLead: 'What cookies and third-party tools may be used on this website.',
    body: legalBody('Cookie Policy', [
      ['Current Setup', 'This website currently runs without advertising cookies. If analytics, advertising pixels or additional tracking are added later, this policy will need to be updated.'],
      ['Essential Cookies', 'Essential cookies may be used to support basic website function, security, form handling or preference storage where required.'],
      ['Analytics Cookies', 'If analytics tools are added, they may help understand page visits, device type and general website performance. Non-essential analytics should be disclosed and controlled appropriately.'],
      ['Third-Party Services', 'The site may load fonts, images, maps, video embeds or form tools from third-party providers. These providers may process technical data according to their own policies.'],
      ['Managing Preferences', 'Visitors can manage cookies through browser settings. A dedicated consent tool should be added if non-essential cookies are used at public launch.'],
    ]),
  },
];

pages.push(...areas.map(areaDetailPage));

function legalBody(title, sections) {
  return `<section class="section"><div class="section-inner legal-layout"><aside class="legal-nav">${sections.map(([heading]) => `<a href="#${slug(heading)}">${heading}</a>`).join('')}</aside><div class="legal-stack"><div class="section-head"><span class="label">Important Information</span><div class="rule"></div><h2 class="section-title">${title}</h2><p class="body-copy">This page explains the main terms in plain language. It should be reviewed by qualified legal counsel before any future material change.</p></div>${sections.map(([heading, text]) => `<article class="legal-card" id="${slug(heading)}"><h3>${heading}</h3><p>${text}</p></article>`).join('')}</div></div></section><section class="cta-band"><div class="cta-inner"><h2 class="cta-title">Have a question about a project?</h2><a class="btn" href="contact.html">Contact Us</a></div></section>`;
}

function slug(value) {
  return value.toLowerCase().replace(/&amp;/g, 'and').replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
}

for (const item of pages) {
  writeFileSync(item.file, page(item));
}

console.log(JSON.stringify({ pages: pages.map((item) => item.file) }, null, 2));
