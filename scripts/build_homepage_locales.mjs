// Generates locale variants of the homepage (nueva-living-home.html -> a
// real, functioning es/index.html, fr/index.html, de/index.html,
// ru/index.html, ar/index.html) so the language switcher and the property
// pages' "Cinematic Presentation" links -- which already point at
// "<locale>/index.html" -- resolve to a real page instead of 404ing.
//
// Scope (documented, not silently partial): this script fully localizes
// the homepage's shared chrome -- nav, mobile menu, footer, language
// switcher, <html lang/dir>, hreflang, and (for Arabic) the RTL stylesheet
// and self-hosted Arabic font -- for every locale, plus the homepage's own
// hero copy, repeating content blocks (Why/Areas/Journey/About/Referral),
// the contact form, and the embedded cinematic-presentation viewer's
// UI-chrome strings ("Guided", "Project Details", field labels), currently
// only for Spanish (see homepageContentReplacements below -- other locales
// return an empty array there and keep the documented English fallback for
// this page's marketing copy). Per-project card taglines on the "Selected
// Residences" grid ARE translated for every locale that has a
// `card.description` overlay (see projectCardTaglineReplacements). Every
// non-default-locale homepage is a real, complete page (not a
// placeholder): untranslated sections simply render their existing English
// content, which is honest fallback behaviour, not a broken or empty route.
import { existsSync, readFileSync, writeFileSync, mkdirSync, readdirSync } from 'node:fs';
import path from 'node:path';
import { LOCALES, DEFAULT_LOCALE, localeMeta, t, isRtl, rootPrefix } from './lib/i18n.mjs';

const root = process.cwd();
const sourcePath = path.join(root, 'nueva-living-home.html');
if (!existsSync(sourcePath)) {
  console.log('nueva-living-home.html not found, skipping homepage locale build.');
  process.exit(0);
}

// Strip any switcher/hreflang/base-tag/RTL-link this script injected on a
// previous run, so re-running the build (e.g. a second local build, or a
// CI re-run) always starts from a clean English baseline instead of
// compounding duplicate injections into the source file it reads from.
function stripPriorInjections(html) {
  return html
    .replace(/<base href="\.\.\/">\n/g, '')
    .replace(/(<title>[^<]*<\/title>\n)(?:  <link rel="alternate"[^\n]*\n)*/, '$1')
    .replace(/<li><details class="lang-switcher" data-lang-switcher>[\s\S]*?<\/details><\/li>\n\s*/g, '')
    .replace(/\s*<details class="lang-switcher" data-lang-switcher>[\s\S]*?<\/details>\n(?=\s*<\/div>)/g, '\n')
    .replace(/\n\s*#nav \.lang-switcher, \.mobile-menu \.lang-switcher[\s\S]*?\.mobile-menu \.lang-switcher-option \{ color: inherit; \}\n/g, '\n')
    .replace(/\n\s*<link rel="stylesheet" href="\.\.\/assets\/liora\/liora-rtl\.css\?v=[^"]*">\n/g, '\n')
    .replace(/\s*<script>\n\s*document\.querySelectorAll\('\[data-lang-switcher\]'\)[\s\S]*?<\/script>\n/g, '\n');
}

const source = stripPriorInjections(readFileSync(sourcePath, 'utf8'));
const rtlCssVersion = existsSync(path.join(root, 'assets/liora/liora-rtl.css')) ? '1' : '1';

// Exact-string replacements for the homepage's own hand-authored nav/
// footer copy (verified against the current markup). Applied globally so
// both the desktop nav and the duplicated mobile-menu list pick up the
// same translation from one entry.
function navFooterReplacements(locale) {
  return [
    ['>Buying Guides<', `>${t('nav.buyingGuides', locale)}<`],
    ['>Why Nueva<', `>${t('nav.whyNueva', locale)}<`],
    ['>Developments<', `>${t('nav.developments', locale)}<`],
    ['>Areas<', `>${t('nav.areas', locale)}<`],
    ['>Advisory<', `>${t('nav.advisory', locale)}<`],
    ['>Contact Us<', `>${t('nav.contactUs', locale)}<`],
    ['aria-label="Nueva Living — Home"', `aria-label="${t('nav.home', locale)}"`],
    ['aria-label="Menu"', `aria-label="${t('nav.menu', locale)}"`],
    ['New Development Advice', t('footer.about.tagline', locale)],
    ['We help international buyers find and compare new-build and off-plan homes across the Costa del Sol.', t('footer.about.text', locale)],
    ['>Company<', `>${t('footer.companyTitle', locale)}<`],
    ['>Why Nueva Living<', `>${t('footer.whyNuevaLiving', locale)}<`],
    ['>About<', `>${t('footer.about', locale)}<`],
    ['>Privacy Policy<', `>${t('footer.privacyPolicy', locale)}<`],
    ['>Legal Notice<', `>${t('footer.legalNotice', locale)}<`],
    ['>Cookie Policy<', `>${t('footer.cookiePolicy', locale)}<`],
    ['>Projects<', `>${t('footer.projectsTitle', locale)}<`],
    ['>All Developments<', `>${t('footer.allDevelopments', locale)}<`],
    ['>Areas Overview<', `>${t('footer.areasOverview', locale)}<`],
    ['Information on this website is for general marketing purposes only and does not constitute legal, financial or investment advice. Details, prices and delivery dates are subject to change.', t('footer.disclaimer', locale)]
  ];
}

// Homepage-specific marketing copy and cinematic-viewer chrome. These are
// one-off, page-specific strings (not reused elsewhere), so -- like
// navFooterReplacements above -- they are literal [find, replace] pairs
// rather than content/i18n/strings.json keys. Only Spanish is populated for
// now (matching the "start with Spanish" instruction); other locales return
// an empty array here and keep the existing, documented English fallback
// for this page's hero/marketing/viewer copy.
function homepageContentReplacements(locale) {
  if (locale !== 'es') return [];
  return [
    // Hero
    ['Costa del Sol · New Development Specialist', 'Costa del Sol · Especialistas en Nueva Construcción'],
    ['New Homes Worth Seeing on the <em>Costa del Sol</em>', 'Viviendas Nuevas que Merece la Pena Ver en la <em>Costa del Sol</em>'],
    ['We help you find and compare the right new-build homes across Marbella, Estepona, Benahavís and the wider Costa del Sol.', 'Te ayudamos a encontrar y comparar las viviendas de nueva construcción adecuadas en Marbella, Estepona, Benahavís y el resto de la Costa del Sol.'],
    ['>Explore Developments<', '>Ver Promociones<'],
    ['>Get a Personal Shortlist<', '>Solicita tu Lista Personalizada<'],
    ['>Call Us<', '>Llámanos<'],
    ['<span>Scroll</span>', '<span>Desplázate</span>'],
    // Credibility strip
    ['>Developers We Work With<', '>Promotoras con las que Trabajamos<'],
    ['>Costa del Sol Areas<', '>Zonas de la Costa del Sol<'],
    ['>New Builds Only<', '>Solo Obra Nueva<'],
    ['>One-to-One Buyer Support<', '>Acompañamiento Personalizado<'],
    // Developments section chrome
    ['<span class="label">Selected Residences</span>', '<span class="label">Viviendas Seleccionadas</span>'],
    ['<h2 class="section-title">Selected New<br><em>Residences</em></h2>', '<h2 class="section-title">Nuevas Viviendas<br><em>Seleccionadas</em></h2>'],
    ['dev-badge">Completed, Ready To Move In', 'dev-badge">Finalizado, Listo para Entrar'],
    ['dev-badge">Current Release', 'dev-badge">Fase Actual'],
    ['dev-badge">Off-Plan', 'dev-badge">Sobre Plano'],
    ['dev-badge">Off-plan, Private Availability', 'dev-badge">Sobre Plano, Disponibilidad Privada'],
    ['dev-badge">Sea View Collection', 'dev-badge">Colección con Vistas al Mar'],
    ['dev-badge">Under Construction', 'dev-badge">En Construcción'],
    ['"lbl">Delivery<', '"lbl">Entrega<'],
    ['"lbl">From<', '"lbl">Desde<'],
    ['"lbl">Status<', '"lbl">Estado<'],
    ['"lbl">Type<', '"lbl">Tipo<'],
    ['"val">Completed<', '"val">Finalizado<'],
    ['"val">Current release<', '"val">Fase actual<'],
    ['"val">Under construction<', '"val">En construcción<'],
    ['>Apartments, Penthouses &amp; Villas<', '>Apartamentos, Áticos y Villas<'],
    ['>Semi-Detached Houses<', '>Casas Adosadas<'],
    ['>Penthouses &amp; Villas<', '>Áticos y Villas<'],
    ['>Apartments &amp; Penthouses<', '>Apartamentos y Áticos<'],
    ['>1-4 Bedroom Homes<', '>Viviendas de 1 a 4 Dormitorios<'],
    ['>Discover Project<', '>Descubrir Proyecto<'],
    // Why section
    ['Why New Development</span>', 'Por Qué Comprar Obra Nueva</span>'],
    ['The Advantages of<br><em>Buying New</em>', 'Las Ventajas de<br><em>Comprar Nuevo</em>'],
    ['<h3>Modern Design &amp; Energy Efficiency</h3>', '<h3>Diseño Moderno y Eficiencia Energética</h3>'],
    ['<p>Modern layouts, better energy ratings, smart-home features and up-to-date materials come as standard in many new projects.</p>', '<p>Distribuciones modernas, mejores calificaciones energéticas, domótica y materiales actuales vienen de serie en muchas promociones nuevas.</p>'],
    ['<h3>Flexible Payment Structures</h3>', '<h3>Planes de Pago Flexibles</h3>'],
    ['<p>Payments are usually split across the build, making it easier to plan your finances before completion.</p>', '<p>Los pagos suelen fraccionarse a lo largo de la construcción, lo que facilita planificar tus finanzas antes de la entrega.</p>'],
    ['<h3>Developer Warranties</h3>', '<h3>Garantías de la Promotora</h3>'],
    ['<p>New homes come with building guarantees and warranties that you would not normally get with a resale property.</p>', '<p>Las viviendas nuevas incluyen garantías de construcción que normalmente no obtendrías con una propiedad de reventa.</p>'],
    ['<h3>Rental &amp; Resale Potential</h3>', '<h3>Potencial de Alquiler y Reventa</h3>'],
    ['<p>The right new build can be attractive to future buyers and renters, especially when the location and unit choice are strong.</p>', '<p>La vivienda nueva adecuada puede resultar atractiva para futuros compradores e inquilinos, sobre todo cuando la ubicación y la elección de la vivienda son acertadas.</p>'],
    ['<h3>Early-Phase Pricing</h3>', '<h3>Precios de Primera Fase</h3>'],
    ['<p>Buying earlier often gives you a better choice of views, layouts and payment plans. We help you weigh that against the build timeline and risk.</p>', '<p>Comprar en una fase temprana suele ofrecer mejor elección de vistas, distribuciones y planes de pago. Te ayudamos a valorarlo frente al plazo de construcción y el riesgo.</p>'],
    // Areas section
    ['<span class="label reveal">Locations We Cover</span>', '<span class="label reveal">Zonas donde Trabajamos</span>'],
    ['The Costa del Sol<br><em>Area by Area</em>', 'La Costa del Sol<br><em>Zona a Zona</em>'],
    ["Marbella brings together beaches, restaurants, international schools and some of the coast's most sought-after addresses.", 'Marbella reúne playas, restaurantes, colegios internacionales y algunas de las direcciones más solicitadas de la costa.'],
    ['Estepona has grown quickly, with better public spaces, new projects and a more relaxed feel than central Marbella.', 'Estepona ha crecido rápidamente, con mejores espacios públicos, nuevas promociones y un ambiente más tranquilo que el centro de Marbella.'],
    ['Benahavís is known for privacy, hillside views, golf and gated communities close to Marbella.', 'Benahavís es conocido por su privacidad, vistas a la montaña, golf y urbanizaciones cerradas cerca de Marbella.'],
    ['Nueva Andalucía puts golf, restaurants and Puerto Banús close by, making it a practical base for holidays or longer stays.', 'Nueva Andalucía tiene el golf, los restaurantes y Puerto Banús cerca, lo que la convierte en una base práctica para vacaciones o estancias largas.'],
    ['Mijas and Fuengirola offer good links to Málaga, established coastal life and a wide choice of newer homes.', 'Mijas y Fuengirola ofrecen buenas conexiones con Málaga, vida costera consolidada y una amplia oferta de viviendas más nuevas.'],
    ['View area guide <span aria-hidden="true">&#8594;</span>', 'Ver guía de la zona <span aria-hidden="true">&#8594;</span>'],
    // Journey section
    ['<span class="label reveal">Our Process</span>', '<span class="label reveal">Nuestro Proceso</span>'],
    ['The Buyer<br><em>Journey</em>', 'El Recorrido<br><em>del Comprador</em>'],
    ['One clear route from the first conversation to handover, with the right checks and decisions made at each stage.', 'Un camino claro desde la primera conversación hasta la entrega de llaves, con las comprobaciones y decisiones adecuadas en cada etapa.'],
    ['<h3>Consultation</h3>', '<h3>Consulta Inicial</h3>'],
    ['<p>We start with a straightforward conversation about your plans, budget, timing and how you want to use the home.</p>', '<p>Empezamos con una conversación sencilla sobre tus planes, presupuesto, plazos y cómo quieres usar la vivienda.</p>'],
    ['>Start a conversation<', '>Iniciar una conversación<'],
    ['<h3>Project Matching</h3>', '<h3>Selección de Proyectos</h3>'],
    ['<p>You receive a focused shortlist that fits, without having to sort through the whole market.</p>', '<p>Recibes una lista personalizada y ajustada a tus necesidades, sin tener que revisar todo el mercado.</p>'],
    ['<h3>Project Review</h3>', '<h3>Revisión del Proyecto</h3>'],
    ['<p>We review the exact home, orientation, floorplan, materials, payment schedule and developer track record before you decide.</p>', '<p>Revisamos la vivienda exacta, orientación, plano, materiales, calendario de pagos y trayectoria de la promotora antes de que decidas.</p>'],
    ['<h3>Reservation &amp; Legal</h3>', '<h3>Reserva y Aspectos Legales</h3>'],
    ['<p>When you are ready, we guide the reservation and work alongside your lawyer through the checks.</p>', '<p>Cuando estés listo, te acompañamos en la reserva y trabajamos junto a tu abogado durante las comprobaciones.</p>'],
    ['<h3>Completion &amp; After-Sale</h3>', '<h3>Entrega y Posventa</h3>'],
    ['<p>We stay involved through inspection and handover, and connect you with trusted local support after completion.</p>', '<p>Seguimos presentes durante la inspección y la entrega, y te ponemos en contacto con apoyo local de confianza tras la compra.</p>'],
    // About section
    ['<span class="label reveal">About the Firm</span>', '<span class="label reveal">Sobre la Firma</span>'],
    ['We Know<br><em>New Developments</em>', 'Conocemos<br><em>la Obra Nueva</em>'],
    ['Nueva Living was created for people who want straightforward help when buying a new home on the Costa del Sol.', 'Nueva Living nació para quienes buscan ayuda clara y directa al comprar una vivienda nueva en la Costa del Sol.'],
    ['Because new developments are all we do, we know the projects, the developers and the questions worth asking.', 'Como solo nos dedicamos a la obra nueva, conocemos los proyectos, las promotoras y las preguntas que merece la pena hacer.'],
    ['>About Nueva Living<', '>Sobre Nueva Living<'],
    // Referral band
    ['<span class="label reveal">Know Someone Looking?</span>', '<span class="label reveal">¿Conoces a Alguien Interesado?</span>'],
    ['Introduce someone,<br><em>get rewarded</em>', 'Preséntanos a alguien,<br><em>recibe una recompensa</em>'],
    ['If someone in your life is thinking about a home on the Costa del Sol, our Referral &amp; Ambassador Program lets you introduce them and receive a share of our commission when their purchase completes.', 'Si alguien de tu entorno está pensando en comprar una vivienda en la Costa del Sol, nuestro Programa de Referidos y Embajadores te permite presentárnoslo y recibir una parte de nuestra comisión cuando complete la compra.'],
    ['>Introduce Someone<', '>Presentar a Alguien<'],
    // Contact / shortlist form
    ['Tell Us What You Need</span>', 'Cuéntanos Qué Necesitas</span>'],
    ['Get a Personal<br><em>Project Shortlist</em>', 'Solicita tu Lista<br><em>Personalizada de Proyectos</em>'],
    ['Leave your contact details and tell us what you are looking for. Add more preferences if you already have a clear idea.', 'Déjanos tus datos de contacto y cuéntanos qué buscas. Añade más preferencias si ya tienes una idea clara.'],
    ['<label for="f-first-name">First Name</label>', '<label for="f-first-name">Nombre</label>'],
    ['<label for="f-last-name">Last Name</label>', '<label for="f-last-name">Apellidos</label>'],
    ['<label for="f-email">Email Address</label>', '<label for="f-email">Correo Electrónico</label>'],
    ['<label for="f-phone">Phone Number</label>', '<label for="f-phone">Teléfono</label>'],
    ['<span>Add More Details</span>', '<span>Añadir Más Detalles</span>'],
    ['<small>Optional - helps us refine your shortlist</small>', '<small>Opcional - nos ayuda a afinar tu selección</small>'],
    ['<label for="f-area">Preferred Area</label>', '<label for="f-area">Zona Preferida</label>'],
    ['<option value="">Select area…</option>', '<option value="">Selecciona una zona…</option>'],
    ['<option>Open to all areas</option>', '<option>Abierto a cualquier zona</option>'],
    ['<label for="f-property-type">Property Type Interest</label>', '<label for="f-property-type">Tipo de Vivienda de Interés</label>'],
    ['<option value="">Select type…</option>', '<option value="">Selecciona un tipo…</option>'],
    ['<option>Apartments</option>', '<option>Apartamentos</option>'],
    ['<option>Penthouses</option>', '<option>Áticos</option>'],
    ['<option>Villas</option>', '<option>Villas</option>'],
    ['<option>Townhouses</option>', '<option>Casas Adosadas</option>'],
    ['<option>Mixed / Open</option>', '<option>Mixto / Abierto</option>'],
    ['<label for="f-budget">Budget Range</label>', '<label for="f-budget">Rango de Presupuesto</label>'],
    ['<option value="">Select budget…</option>', '<option value="">Selecciona un presupuesto…</option>'],
    ['<label for="f-purpose">Purchase Purpose</label>', '<label for="f-purpose">Motivo de la Compra</label>'],
    ['<option value="">Select purpose…</option>', '<option value="">Selecciona un motivo…</option>'],
    ['<option>Primary Residence</option>', '<option>Vivienda Habitual</option>'],
    ['<option>Holiday Home</option>', '<option>Vivienda Vacacional</option>'],
    ['<option>Investment / Rental</option>', '<option>Inversión / Alquiler</option>'],
    ['<option>Combination</option>', '<option>Combinación</option>'],
    ['<label for="f-msg">Message (optional)</label>', '<label for="f-msg">Mensaje (opcional)</label>'],
    ['placeholder="Tell us about your requirements…"', 'placeholder="Cuéntanos qué necesitas…"'],
    ['<span>I agree to be contacted and for my data to be stored.</span>', '<span>Acepto ser contactado/a y que mis datos sean almacenados.</span>'],
    ['<span>I would also like to receive occasional project updates from Nueva Living.</span>', '<span>También me gustaría recibir novedades ocasionales de proyectos por parte de Nueva Living.</span>'],
    ['>Send My Request<', '>Enviar Mi Solicitud<'],
    ['<span class="form-note">We review every enquiry personally.</span>', '<span class="form-note">Revisamos cada consulta de forma personal.</span>'],
    ['Prefer email? <a href="mailto:contact@nuevaliving.com">contact@nuevaliving.com</a>', '¿Prefieres el correo? <a href="mailto:contact@nuevaliving.com">contact@nuevaliving.com</a>'],
    // "Show more" (why / areas / journey grids)
    ['data-expand-grid>Show More</button>', 'data-expand-grid>Ver Más</button>'],
    // Cinematic-presentation viewer chrome
    ['aria-label="Cinematic Presentation — Nueva Living"', 'aria-label="Presentación Cinemática — Nueva Living"'],
    ['<div class="vbrand">Nueva Living · Cinematic Presentation</div>', '<div class="vbrand">Nueva Living · Presentación Cinemática</div>'],
    ['aria-label="Pause guided viewing"', 'aria-label="Pausar recorrido guiado"'],
    ['<span class="mode-label">Guided</span>', '<span class="mode-label">Guiado</span>'],
    ['aria-label="Project details" aria-controls="vinfoPanel"', 'aria-label="Detalles del proyecto" aria-controls="vinfoPanel"'],
    ['<span class="info-label">Project Details</span>', '<span class="info-label">Detalles del Proyecto</span>'],
    ['aria-label="Exit viewing">', 'aria-label="Salir de la presentación">'],
    ['</svg>\n          Exit\n        </button>', '</svg>\n          Salir\n        </button>'],
    ['<span class="vclt">Scroll</span>', '<span class="vclt">Desplázate</span>'],
    ['aria-label="Project details" aria-hidden="true">', 'aria-label="Detalles del proyecto" aria-hidden="true">'],
    ['<span class="vinfo-kicker" id="vinfoKicker">Project Details</span>', '<span class="vinfo-kicker" id="vinfoKicker">Detalles del Proyecto</span>'],
    ['aria-label="Close project details"', 'aria-label="Cerrar detalles del proyecto"'],
    ['<span class="vt-label" id="vtlbl">01 — Private Preview</span>', '<span class="vt-label" id="vtlbl">01 — Vista Privada</span>'],
    ['<h2 class="vt-headline" id="vthl">Take a closer look,<br>one space at a time.</h2>', '<h2 class="vt-headline" id="vthl">Descúbrelo de cerca,<br>espacio a espacio.</h2>'],
    ['<span class="vt-sub" id="vtsub">See the setting, architecture and everyday spaces before asking for the full project pack.</span>', '<span class="vt-sub" id="vtsub">Conoce el entorno, la arquitectura y los espacios cotidianos antes de solicitar el dosier completo del proyecto.</span>'],
    ['<div class="v7proj">Nueva Living · New Development Preview</div>', '<div class="v7proj">Nueva Living · Vista Previa de Nueva Promoción</div>'],
    ['>Get Project Information<', '>Solicitar Información del Proyecto<'],
    ['>Exit Viewing<', '>Salir de la Presentación<'],
    ["vmodeBtn.setAttribute('aria-label', on ? 'Pause guided viewing' : 'Resume guided viewing');", "vmodeBtn.setAttribute('aria-label', on ? 'Pausar recorrido guiado' : 'Reanudar recorrido guiado');"],
    ["vSetGuidedUI(true, 'Guided');", "vSetGuidedUI(true, 'Guiado');"],
    ["vmodeLabel.textContent = label || (on ? 'Guided' : 'Manual');", "vmodeLabel.textContent = label || (on ? 'Guiado' : 'Manual');"],
    ["function vStopGuided(label = 'Manual') {", "function vStopGuided(label = 'Manual') {"],
    ["['Starting Price', project.price],", "['Precio desde', project.price],"],
    ["['Bedrooms', project.bedrooms],", "['Dormitorios', project.bedrooms],"],
    ["['Built Size', project.builtSize],", "['Superficie Construida', project.builtSize],"],
    ["['Terrace Size', project.terraceSize],", "['Superficie de Terraza', project.terraceSize],"],
    ["['Completion', project.completion],", "['Entrega', project.completion],"],
    ["['Positioning', project.status]", "['Estado', project.status]"],
    ['<span class="vinfo-pill">New Development</span>', '<span class="vinfo-pill">Nueva Promoción</span>'],
    ['<span class="vinfo-pill">Private Preview</span>', '<span class="vinfo-pill">Vista Privada</span>'],
    ["vInfoSection('Overview', project.overview)", "vInfoSection('Visión General', project.overview)"],
    ["vInfoSection('Architecture', project.highlights)", "vInfoSection('Arquitectura', project.highlights)"],
    ["vInfoSection('Lifestyle', project.lifestyle)", "vInfoSection('Estilo de Vida', project.lifestyle)"],
    ["vInfoSection('Investment', project.investmentNotes)", "vInfoSection('Inversión', project.investmentNotes)"],
    ["vInfoSection('Availability', (project.availability || [])", "vInfoSection('Disponibilidad', (project.availability || [])"],
    ['<h3>Get Project Information</h3>', '<h3>Solicitar Información del Proyecto</h3>'],
    ["project.ctaLabel || 'Get Project Information'", "project.ctaLabel || 'Solicitar Información del Proyecto'"],
    ['<p>Get the latest brochure, master plan, floorplans, availability and prices.</p>', '<p>Recibe el último dosier, master plan, planos, disponibilidad y precios.</p>']
  ];
}

// Per-project homepage card taglines (the <p class="dev-tagline"> text on
// the "Selected Residences" grid). These come from each project's own
// project.json `card.description` (falling back to `description`), and are
// translated via each project's `i18n.<locale>.card.description` overlay --
// NOT via the literal find/replace pairs above, since this text is
// per-project data, not shared page copy. Projects/locales without a
// translated card.description simply keep the English tagline (documented
// fallback, same principle as everywhere else in this pipeline).
function projectCardTaglineReplacements(locale) {
  if (locale === DEFAULT_LOCALE) return [];
  const projectsDir = path.join(root, 'content/liora-projects');
  if (!existsSync(projectsDir)) return [];
  const replacements = [];
  for (const slug of readdirSync(projectsDir)) {
    const projectPath = path.join(projectsDir, slug, 'project.json');
    if (!existsSync(projectPath)) continue;
    const project = JSON.parse(readFileSync(projectPath, 'utf8'));
    const enTagline = project.card?.description || project.description;
    const translatedTagline = project.i18n?.[locale]?.card?.description;
    if (!enTagline || !translatedTagline || enTagline === translatedTagline) continue;
    replacements.push([`<p class="dev-tagline">${enTagline}</p>`, `<p class="dev-tagline">${translatedTagline}</p>`]);
  }
  return replacements;
}

const switcherCss = `
    #nav .lang-switcher, .mobile-menu .lang-switcher { position: relative; }
    #nav .lang-switcher-toggle, .mobile-menu .lang-switcher-toggle {
      display: inline-flex; align-items: center; gap: 6px; cursor: pointer; list-style: none;
      color: #f4ead9; font-family: 'Montserrat', Arial, sans-serif; font-size: clamp(13px, 0.95vw, 14px);
      font-weight: 600; letter-spacing: 0.10em; padding: 12px 0;
    }
    #nav .lang-switcher-toggle::-webkit-details-marker { display: none; }
    #nav .lang-switcher-caret { width: 10px; height: 7px; }
    #nav .lang-switcher-caret path, .mobile-menu .lang-switcher-caret path { stroke: currentColor; }
    #nav .lang-switcher-panel {
      position: absolute; top: 100%; right: 0; margin-top: 10px; min-width: 160px;
      background: #2f2417; border: 1px solid rgba(201,163,95,0.28); box-shadow: 0 18px 50px rgba(0,0,0,0.35);
      display: flex; flex-direction: column; padding: 8px; z-index: 40;
    }
    #nav .lang-switcher-option {
      display: block; padding: 9px 12px; color: #f4ead9; font-size: 13px; font-weight: 500;
      letter-spacing: 0.02em; text-decoration: none; white-space: nowrap;
    }
    #nav .lang-switcher-option:hover, #nav .lang-switcher-option.is-active { background: rgba(201,163,95,0.16); color: #c9a35f; }
    .mobile-menu .lang-switcher-panel { position: static; margin-top: 8px; border: none; background: transparent; box-shadow: none; padding-left: 12px; }
    .mobile-menu .lang-switcher-option { color: inherit; }
`;

function renderSwitcherHtml(locale, forMobile) {
  const current = localeMeta(locale);
  const p = rootPrefix(locale);
  const options = LOCALES.map((meta) => {
    const href = `${p}${meta.urlPrefix ? `${meta.urlPrefix}/` : ''}index.html`;
    const active = meta.code === locale;
    return `<a class="lang-switcher-option${active ? ' is-active' : ''}" href="${href}" lang="${meta.htmlLang}" ${active ? 'aria-current="true"' : ''}>${meta.nativeLabel}</a>`;
  }).join('\n              ');
  const inner = `<details class="lang-switcher" data-lang-switcher>
      <summary class="lang-switcher-toggle" aria-label="${t('lang.switcherLabel', locale)}">
        <span class="lang-switcher-code">${current.code.toUpperCase()}</span>
        <svg class="lang-switcher-caret" viewBox="0 0 12 8" aria-hidden="true"><path d="M1 1.5 6 6.5 11 1.5" stroke-width="1.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </summary>
      <div class="lang-switcher-panel" role="menu">
              ${options}
      </div>
    </details>`;
  return forMobile ? inner : `<li>${inner}</li>`;
}

const LANG_SWITCHER_SCRIPT = `<script>
  document.querySelectorAll('[data-lang-switcher]').forEach((el) => {
    document.addEventListener('click', (event) => {
      if (!el.open) return;
      if (el.contains(event.target)) return;
      el.open = false;
    });
  });
</script>`;

const siteUrl = 'https://nuevaliving.com';
function hreflangBlock() {
  const lines = LOCALES.map((m) => `  <link rel="alternate" hreflang="${m.hreflang}" href="${siteUrl}/${m.urlPrefix ? `${m.urlPrefix}/` : ''}index.html">`);
  lines.push(`  <link rel="alternate" hreflang="x-default" href="${siteUrl}/index.html">`);
  return lines.join('\n');
}

const written = [];

for (const meta of LOCALES) {
  if (meta.code === DEFAULT_LOCALE) continue;
  const locale = meta.code;
  let html = source;

  // <html lang/dir>
  html = html.replace('<html lang="en">', `<html lang="${meta.htmlLang}" dir="${meta.dir}">`);

  // <base> so every existing relative asset/page reference resolves
  // correctly from one directory deeper, exactly as on the property pages.
  html = html.replace(
    '<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />',
    '<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />\n  <base href="../">'
  );

  // Language switcher is inserted first, while the surrounding English
  // text is still literal and easy to anchor on; nav/footer text
  // translation runs after so it also picks up the switcher's own labels
  // (harmless no-op for those) in one consistent pass.
  html = html.replace(
    '</ul>\n    <button class="nav-burger"',
    `${renderSwitcherHtml(locale, false)}\n    </ul>\n    <button class="nav-burger"`
  );
  html = html.replace(
    '<a href="contact.html" onclick="closeMobile()">Contact Us</a>\n  </div>',
    `<a href="contact.html" onclick="closeMobile()">Contact Us</a>\n    ${renderSwitcherHtml(locale, true)}\n  </div>`
  );

  // Nav / footer chrome
  for (const [find, replace] of navFooterReplacements(locale)) {
    html = html.split(find).join(replace);
  }

  // Hero, marketing sections and cinematic-viewer chrome
  for (const [find, replace] of homepageContentReplacements(locale)) {
    html = html.split(find).join(replace);
  }

  // Per-project card taglines on the "Selected Residences" grid
  for (const [find, replace] of projectCardTaglineReplacements(locale)) {
    html = html.split(find).join(replace);
  }

  // Reciprocal hreflang, right after <title> (a stable, unique anchor).
  html = html.replace(
    /(<title>[^<]*<\/title>)/,
    `$1\n${hreflangBlock()}`
  );

  // Switcher styling + close-on-outside-click script + RTL/Arabic assets
  html = html.replace('</style>\n</head>', `${switcherCss}\n  </style>\n</head>`);
  if (isRtl(locale)) {
    html = html.replace(
      '</head>',
      `  <link rel="stylesheet" href="../assets/liora/liora-rtl.css?v=${rtlCssVersion}">\n</head>`
    );
  }
  html = html.replace('</body>', `  ${LANG_SWITCHER_SCRIPT}\n</body>`);

  const outPath = path.join(root, meta.urlPrefix, 'index.html');
  mkdirSync(path.dirname(outPath), { recursive: true });
  writeFileSync(outPath, html);
  written.push(`${meta.urlPrefix}/index.html`);
}

// The English homepage also gets the switcher (so users can navigate INTO
// a locale, not just back out of one) and the reciprocal hreflang set.
// Text stays English; no <base>, no RTL assets, no lang/dir change needed.
let englishHtml = source;
if (!englishHtml.includes('data-lang-switcher')) {
  englishHtml = englishHtml.replace(
    '</ul>\n    <button class="nav-burger"',
    `${renderSwitcherHtml(DEFAULT_LOCALE, false)}\n    </ul>\n    <button class="nav-burger"`
  );
  englishHtml = englishHtml.replace(
    '<a href="contact.html" onclick="closeMobile()">Contact Us</a>\n  </div>',
    `<a href="contact.html" onclick="closeMobile()">Contact Us</a>\n    ${renderSwitcherHtml(DEFAULT_LOCALE, true)}\n  </div>`
  );
  englishHtml = englishHtml.replace('</style>\n</head>', `${switcherCss}\n  </style>\n</head>`);
  englishHtml = englishHtml.replace(
    /(<title>[^<]*<\/title>)/,
    `$1\n${hreflangBlock()}`
  );
  englishHtml = englishHtml.replace('</body>', `  ${LANG_SWITCHER_SCRIPT}\n</body>`);
  writeFileSync(sourcePath, englishHtml);
  written.push('nueva-living-home.html (switcher + hreflang added)');
}

console.log(JSON.stringify({ written }, null, 2));
