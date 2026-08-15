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
// UI-chrome strings ("Guided", "Project Details", field labels), for every
// locale (see HOMEPAGE_CONTENT_ENTRIES / homepageContentReplacements below
// -- any entry missing a translation for a given locale keeps the
// documented English fallback for that string rather than crashing).
// Per-project card taglines on the "Selected
// Residences" grid ARE translated for every locale that has a
// `card.description` overlay (see projectCardTaglineReplacements). Every
// non-default-locale homepage is a real, complete page (not a
// placeholder): untranslated sections simply render their existing English
// content, which is honest fallback behaviour, not a broken or empty route.
import { existsSync, readFileSync, writeFileSync, mkdirSync, readdirSync } from 'node:fs';
import path from 'node:path';
import { LOCALES, DEFAULT_LOCALE, localeMeta, t, isRtl, localizeInternalLinks } from './lib/i18n.mjs';
import { loadProjects, renderViewingBlocks } from './lib/viewing.mjs';
import { BESPOKE_SCENE_ENTRIES } from './lib/bespoke_scene_translations.mjs';
import { EDITORIAL_ALT_ENTRIES } from './lib/editorial_alt_translations.mjs';

// Regenerates the cinematic-presentation viewer's VIEWING_PROJECTS /
// PROJECT_VIEWING_SCENE_SETS blocks for a given locale. Without this, the
// English-baked blocks written by build_property_pages.mjs (which only
// ever runs once, in English) would simply be cloned unchanged into every
// locale homepage below -- the viewer's per-project scene captions/labels
// silently staying English on every translated page.
function applyViewingBlocks(html, locale) {
  if (locale === DEFAULT_LOCALE) return html;
  const projects = loadProjects();
  const { projectsBlock, scenesBlock } = renderViewingBlocks(projects, locale);

  const replaceBlock = (source, startMarker, endMarker, block) => {
    const start = source.indexOf(startMarker);
    const end = source.indexOf(endMarker);
    if (start === -1 || end === -1 || end < start) {
      throw new Error(`nueva-living-home.html is missing the ${startMarker} / ${endMarker} markers.`);
    }
    return source.slice(0, start) + block + source.slice(end + endMarker.length);
  };

  let next = html;
  next = replaceBlock(next, '/* NUEVA GENERATED VIEWING PROJECTS START */', '/* NUEVA GENERATED VIEWING PROJECTS END */', projectsBlock);
  next = replaceBlock(next, '/* NUEVA GENERATED VIEWING SCENES START */', '/* NUEVA GENERATED VIEWING SCENES END */', scenesBlock);
  return next;
}

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
// rather than content/i18n/strings.json keys. Translations are defined once
// per source string, across all locales, in HOMEPAGE_CONTENT_ENTRIES below;
// homepageContentReplacements(locale) simply projects that table down to
// [find, replace] pairs for the requested locale. Any entry missing a
// translation for a given locale is filtered out, so that string keeps the
// existing, documented English fallback rather than crashing.
const HOMEPAGE_CONTENT_ENTRIES = [
  // Hero
  { find: 'Costa del Sol · New Development Specialist', es: 'Costa del Sol · Especialistas en Nueva Construcción', fr: 'Costa del Sol · Spécialiste des Programmes Neufs', de: 'Costa del Sol · Spezialist für Neubauprojekte', ru: 'Коста-дель-Соль · Специалист по Новостройкам', ar: 'كوستا ديل سول · متخصصون في المشاريع الجديدة' },
  { find: 'New Homes Worth Seeing on the <em>Costa del Sol</em>', es: 'Viviendas Nuevas que Merece la Pena Ver en la <em>Costa del Sol</em>', fr: 'Des Maisons Neuves qui Valent le Détour sur la <em>Costa del Sol</em>', de: 'Neubauten, die einen Besuch wert sind an der <em>Costa del Sol</em>', ru: 'Новые Дома, которые Стоит Увидеть на <em>Коста-дель-Соль</em>', ar: 'منازل جديدة تستحق المشاهدة في <em>كوستا ديل سول</em>' },
  { find: 'We help you find and compare the right new-build homes across Marbella, Estepona, Benahavís and the wider Costa del Sol.', es: 'Te ayudamos a encontrar y comparar las viviendas de nueva construcción adecuadas en Marbella, Estepona, Benahavís y el resto de la Costa del Sol.', fr: "Nous vous aidons à trouver et comparer les biens neufs qui vous conviennent à Marbella, Estepona, Benahavís et sur l'ensemble de la Costa del Sol.", de: 'Wir helfen Ihnen, die passenden Neubauimmobilien in Marbella, Estepona, Benahavís und der gesamten Costa del Sol zu finden und zu vergleichen.', ru: 'Мы помогаем вам находить и сравнивать подходящие новостройки в Марбелье, Эстепоне, Бенаависе и на всём побережье Коста-дель-Соль.', ar: 'نساعدك في إيجاد ومقارنة المنازل الجديدة المناسبة في ماربيا واستيبونا وبيناهافيس وسائر كوستا ديل سول.' },
  { find: '>Explore Developments<', es: '>Ver Promociones<', fr: '>Découvrir les Programmes<', de: '>Neubauprojekte Entdecken<', ru: '>Смотреть Новостройки<', ar: '>استكشاف المشاريع<' },
  { find: '>Get a Personal Shortlist<', es: '>Solicita tu Lista Personalizada<', fr: '>Recevoir une Sélection Personnalisée<', de: '>Persönliche Auswahl Erhalten<', ru: '>Получить Персональную Подборку<', ar: '>احصل على قائمة مختارة شخصية<' },
  { find: '>Call Us<', es: '>Llámanos<', fr: '>Appelez-Nous<', de: '>Rufen Sie Uns An<', ru: '>Позвоните Нам<', ar: '>اتصل بنا<' },
  { find: '<span>Scroll</span>', es: '<span>Desplázate</span>', fr: '<span>Défiler</span>', de: '<span>Scrollen</span>', ru: '<span>Прокрутите</span>', ar: '<span>مرر للأسفل</span>' },
  // Credibility strip
  { find: '>Developers We Work With<', es: '>Promotoras con las que Trabajamos<', fr: '>Promoteurs avec Qui Nous Collaborons<', de: '>Bauträger, mit denen wir Zusammenarbeiten<', ru: '>Застройщики, с Которыми Мы Работаем<', ar: '>المطورون الذين نتعامل معهم<' },
  { find: '>Costa del Sol Areas<', es: '>Zonas de la Costa del Sol<', fr: '>Secteurs de la Costa del Sol<', de: '>Lagen an der Costa del Sol<', ru: '>Районы Коста-дель-Соль<', ar: '>مناطق كوستا ديل سول<' },
  { find: '>New Builds Only<', es: '>Solo Obra Nueva<', fr: '>Uniquement des Biens Neufs<', de: '>Ausschließlich Neubauten<', ru: '>Только Новостройки<', ar: '>عقارات جديدة فقط<' },
  { find: '>One-to-One Buyer Support<', es: '>Acompañamiento Personalizado<', fr: '>Accompagnement Personnalisé<', de: '>Persönliche Käuferbetreuung<', ru: '>Персональное Сопровождение Покупателя<', ar: '>دعم شخصي للمشتري<' },
  // Developments section chrome
  { find: '<span class="label">Selected Residences</span>', es: '<span class="label">Viviendas Seleccionadas</span>', fr: '<span class="label">Résidences Sélectionnées</span>', de: '<span class="label">Ausgewählte Residenzen</span>', ru: '<span class="label">Избранные Резиденции</span>', ar: '<span class="label">مساكن مختارة</span>' },
  { find: '<h2 class="section-title">Selected New<br><em>Residences</em></h2>', es: '<h2 class="section-title">Nuevas Viviendas<br><em>Seleccionadas</em></h2>', fr: '<h2 class="section-title">Résidences Neuves<br><em>Sélectionnées</em></h2>', de: '<h2 class="section-title">Ausgewählte Neue<br><em>Residenzen</em></h2>', ru: '<h2 class="section-title">Избранные Новые<br><em>Резиденции</em></h2>', ar: '<h2 class="section-title">مساكن جديدة<br><em>مختارة</em></h2>' },
  { find: 'dev-badge">Completed, Ready To Move In', es: 'dev-badge">Finalizado, Listo para Entrar', fr: 'dev-badge">Terminé, Prêt à Emménager', de: 'dev-badge">Fertiggestellt, Bezugsfertig', ru: 'dev-badge">Завершено, Готово к Заселению', ar: 'dev-badge">مكتمل، جاهز للسكن' },
  { find: 'dev-badge">Current Release', es: 'dev-badge">Fase Actual', fr: 'dev-badge">Phase Actuelle', de: 'dev-badge">Aktuelle Phase', ru: 'dev-badge">Текущая Очередь', ar: 'dev-badge">المرحلة الحالية' },
  { find: 'dev-badge">Off-Plan', es: 'dev-badge">Sobre Plano', fr: 'dev-badge">Sur Plan', de: 'dev-badge">Off-Plan', ru: 'dev-badge">На Этапе Строительства', ar: 'dev-badge">على المخطط' },
  { find: 'dev-badge">Off-plan, Private Availability', es: 'dev-badge">Sobre Plano, Disponibilidad Privada', fr: 'dev-badge">Sur Plan, Disponibilité Privée', de: 'dev-badge">Off-Plan, Private Verfügbarkeit', ru: 'dev-badge">На Этапе Строительства, Закрытая Продажа', ar: 'dev-badge">على المخطط، إتاحة حصرية' },
  { find: 'dev-badge">Sea View Collection', es: 'dev-badge">Colección con Vistas al Mar', fr: 'dev-badge">Collection Vue Mer', de: 'dev-badge">Kollektion mit Meerblick', ru: 'dev-badge">Коллекция с Видом на Море', ar: 'dev-badge">مجموعة بإطلالة على البحر' },
  { find: 'dev-badge">Under Construction', es: 'dev-badge">En Construcción', fr: 'dev-badge">En Construction', de: 'dev-badge">Im Bau', ru: 'dev-badge">В Стадии Строительства', ar: 'dev-badge">قيد الإنشاء' },
  { find: '"lbl">Delivery<', es: '"lbl">Entrega<', fr: '"lbl">Livraison<', de: '"lbl">Übergabe<', ru: '"lbl">Сдача<', ar: '"lbl">التسليم<' },
  { find: '"lbl">From<', es: '"lbl">Desde<', fr: '"lbl">À Partir de<', de: '"lbl">Ab<', ru: '"lbl">От<', ar: '"lbl">ابتداءً من<' },
  { find: '"lbl">Status<', es: '"lbl">Estado<', fr: '"lbl">Statut<', de: '"lbl">Status<', ru: '"lbl">Статус<', ar: '"lbl">الحالة<' },
  { find: '"lbl">Type<', es: '"lbl">Tipo<', fr: '"lbl">Type<', de: '"lbl">Typ<', ru: '"lbl">Тип<', ar: '"lbl">النوع<' },
  { find: '"val">Completed<', es: '"val">Finalizado<', fr: '"val">Terminé<', de: '"val">Fertiggestellt<', ru: '"val">Завершено<', ar: '"val">مكتمل<' },
  { find: '"val">Current release<', es: '"val">Fase actual<', fr: '"val">Phase actuelle<', de: '"val">Aktuelle Phase<', ru: '"val">Текущая очередь<', ar: '"val">المرحلة الحالية<' },
  { find: '"val">Under construction<', es: '"val">En construcción<', fr: '"val">En construction<', de: '"val">Im Bau<', ru: '"val">В стадии строительства<', ar: '"val">قيد الإنشاء<' },
  { find: '>Apartments, Penthouses &amp; Villas<', es: '>Apartamentos, Áticos y Villas<', fr: '>Appartements, Penthouses et Villas<', de: '>Wohnungen, Penthäuser & Villen<', ru: '>Апартаменты, Пентхаусы и Виллы<', ar: '>شقق وبنتهاوس وفلل<' },
  { find: '>Semi-Detached Houses<', es: '>Casas Adosadas<', fr: '>Maisons Jumelées<', de: '>Doppelhaushälften<', ru: '>Дома на Две Семьи<', ar: '>منازل شبه منفصلة<' },
  { find: '>Penthouses &amp; Villas<', es: '>Áticos y Villas<', fr: '>Penthouses et Villas<', de: '>Penthäuser & Villen<', ru: '>Пентхаусы и Виллы<', ar: '>بنتهاوس وفلل<' },
  { find: '>Apartments &amp; Penthouses<', es: '>Apartamentos y Áticos<', fr: '>Appartements et Penthouses<', de: '>Wohnungen & Penthäuser<', ru: '>Апартаменты и Пентхаусы<', ar: '>شقق وبنتهاوس<' },
  { find: '>1-4 Bedroom Homes<', es: '>Viviendas de 1 a 4 Dormitorios<', fr: '>Logements de 1 à 4 Chambres<', de: '>Wohnungen mit 1–4 Schlafzimmern<', ru: '>Дома с 1–4 Спальнями<', ar: '>مساكن من غرفة إلى 4 غرف نوم<' },
  { find: '>Discover Project<', es: '>Descubrir Proyecto<', fr: '>Découvrir le Projet<', de: '>Projekt Entdecken<', ru: '>Узнать о Проекте<', ar: '>اكتشف المشروع<' },
  // Why section
  { find: 'Why New Development</span>', es: 'Por Qué Comprar Obra Nueva</span>', fr: 'Pourquoi un Bien Neuf</span>', de: 'Warum ein Neubau</span>', ru: 'Почему Новостройка</span>', ar: 'لماذا المشروع الجديد</span>' },
  { find: 'The Advantages of<br><em>Buying New</em>', es: 'Las Ventajas de<br><em>Comprar Nuevo</em>', fr: "Les Avantages d'<br><em>Acheter Neuf</em>", de: 'Die Vorteile des<br><em>Neubaukaufs</em>', ru: 'Преимущества<br><em>Покупки Новостройки</em>', ar: 'مزايا<br><em>شراء العقار الجديد</em>' },
  { find: '<h3>Modern Design &amp; Energy Efficiency</h3>', es: '<h3>Diseño Moderno y Eficiencia Energética</h3>', fr: '<h3>Design Moderne et Efficacité Énergétique</h3>', de: '<h3>Modernes Design & Energieeffizienz</h3>', ru: '<h3>Современный Дизайн и Энергоэффективность</h3>', ar: '<h3>تصميم عصري وكفاءة في استهلاك الطاقة</h3>' },
  { find: '<p>Modern layouts, better energy ratings, smart-home features and up-to-date materials come as standard in many new projects.</p>', es: '<p>Distribuciones modernas, mejores calificaciones energéticas, domótica y materiales actuales vienen de serie en muchas promociones nuevas.</p>', fr: '<p>Des agencements modernes, de meilleures performances énergétiques, la domotique et des matériaux actuels sont la norme dans de nombreux nouveaux programmes.</p>', de: '<p>Moderne Grundrisse, bessere Energiewerte, Smart-Home-Funktionen und aktuelle Materialien gehören bei vielen Neubauprojekten zum Standard.</p>', ru: '<p>Современные планировки, более высокие энергетические характеристики, технологии умного дома и актуальные материалы — стандарт для многих новых проектов.</p>', ar: '<p>تُعد التصميمات الحديثة وتصنيفات الطاقة الأفضل وميزات المنزل الذكي والمواد الحديثة معايير أساسية في العديد من المشاريع الجديدة.</p>' },
  { find: '<h3>Flexible Payment Structures</h3>', es: '<h3>Planes de Pago Flexibles</h3>', fr: '<h3>Modalités de Paiement Flexibles</h3>', de: '<h3>Flexible Zahlungspläne</h3>', ru: '<h3>Гибкие Схемы Оплаты</h3>', ar: '<h3>خطط سداد مرنة</h3>' },
  { find: '<p>Payments are usually split across the build, making it easier to plan your finances before completion.</p>', es: '<p>Los pagos suelen fraccionarse a lo largo de la construcción, lo que facilita planificar tus finanzas antes de la entrega.</p>', fr: "<p>Les paiements sont généralement échelonnés tout au long de la construction, ce qui facilite la planification financière avant la livraison.</p>", de: '<p>Die Zahlungen werden in der Regel über die Bauzeit verteilt, was die Finanzplanung vor der Fertigstellung erleichtert.</p>', ru: '<p>Платежи обычно распределяются на протяжении всего строительства, что упрощает финансовое планирование до завершения проекта.</p>', ar: '<p>عادةً ما تُقسَّم الدفعات على مراحل البناء، مما يسهّل التخطيط المالي قبل التسليم.</p>' },
  { find: '<h3>Developer Warranties</h3>', es: '<h3>Garantías de la Promotora</h3>', fr: '<h3>Garanties du Promoteur</h3>', de: '<h3>Bauträgergarantien</h3>', ru: '<h3>Гарантии Застройщика</h3>', ar: '<h3>ضمانات المطور</h3>' },
  { find: '<p>New homes come with building guarantees and warranties that you would not normally get with a resale property.</p>', es: '<p>Las viviendas nuevas incluyen garantías de construcción que normalmente no obtendrías con una propiedad de reventa.</p>', fr: "<p>Les logements neufs bénéficient de garanties de construction que vous n'obtiendriez normalement pas avec un bien de revente.</p>", de: '<p>Neubauten verfügen über Baugarantien, die Sie bei einer Bestandsimmobilie normalerweise nicht erhalten.</p>', ru: '<p>Новые дома предоставляются со строительными гарантиями, которых обычно нет при покупке вторичной недвижимости.</p>', ar: '<p>تأتي المنازل الجديدة بضمانات بناء لا تحصل عليها عادةً عند شراء عقار قديم.</p>' },
  { find: '<h3>Rental &amp; Resale Potential</h3>', es: '<h3>Potencial de Alquiler y Reventa</h3>', fr: '<h3>Potentiel Locatif et de Revente</h3>', de: '<h3>Vermietungs- und Wiederverkaufspotenzial</h3>', ru: '<h3>Потенциал Аренды и Перепродажи</h3>', ar: '<h3>إمكانات التأجير وإعادة البيع</h3>' },
  { find: '<p>The right new build can be attractive to future buyers and renters, especially when the location and unit choice are strong.</p>', es: '<p>La vivienda nueva adecuada puede resultar atractiva para futuros compradores e inquilinos, sobre todo cuando la ubicación y la elección de la vivienda son acertadas.</p>', fr: "<p>Le bien neuf idéal peut séduire de futurs acheteurs et locataires, en particulier lorsque l'emplacement et le choix du bien sont judicieux.</p>", de: '<p>Die richtige Neubauimmobilie kann für künftige Käufer und Mieter attraktiv sein, insbesondere bei einer starken Lage und Einheitenwahl.</p>', ru: '<p>Правильно выбранная новостройка может быть привлекательна для будущих покупателей и арендаторов, особенно при удачном расположении и выборе объекта.</p>', ar: '<p>يمكن أن يكون العقار الجديد المناسب جذابًا للمشترين والمستأجرين المستقبليين، خاصة عند اختيار موقع ووحدة مميزين.</p>' },
  { find: '<h3>Early-Phase Pricing</h3>', es: '<h3>Precios de Primera Fase</h3>', fr: '<h3>Tarifs de Première Phase</h3>', de: '<h3>Frühphasenpreise</h3>', ru: '<h3>Цены Ранней Фазы</h3>', ar: '<h3>أسعار المرحلة المبكرة</h3>' },
  { find: '<p>Buying earlier often gives you a better choice of views, layouts and payment plans. We help you weigh that against the build timeline and risk.</p>', es: '<p>Comprar en una fase temprana suele ofrecer mejor elección de vistas, distribuciones y planes de pago. Te ayudamos a valorarlo frente al plazo de construcción y el riesgo.</p>', fr: "<p>Acheter tôt vous offre souvent un meilleur choix de vues, d'agencements et de plans de paiement. Nous vous aidons à mettre cela en balance avec le calendrier de construction et le risque.</p>", de: '<p>Ein früherer Kauf bietet oft eine bessere Auswahl an Ausblicken, Grundrissen und Zahlungsplänen. Wir helfen Ihnen, dies gegen Bauzeit und Risiko abzuwägen.</p>', ru: '<p>Более ранняя покупка часто даёт лучший выбор видов, планировок и схем оплаты. Мы поможем соотнести это со сроками строительства и рисками.</p>', ar: '<p>غالبًا ما يمنحك الشراء المبكر خيارات أفضل من الإطلالات والتصاميم وخطط السداد. نساعدك على موازنة ذلك مع الجدول الزمني للبناء والمخاطر المرتبطة به.</p>' },
  // Areas section
  { find: '<span class="label reveal">Locations We Cover</span>', es: '<span class="label reveal">Zonas donde Trabajamos</span>', fr: '<span class="label reveal">Secteurs que Nous Couvrons</span>', de: '<span class="label reveal">Lagen, die wir Abdecken</span>', ru: '<span class="label reveal">Районы, с Которыми Мы Работаем</span>', ar: '<span class="label reveal">المناطق التي نغطيها</span>' },
  { find: 'The Costa del Sol<br><em>Area by Area</em>', es: 'La Costa del Sol<br><em>Zona a Zona</em>', fr: 'La Costa del Sol<br><em>Secteur par Secteur</em>', de: 'Die Costa del Sol<br><em>Lage für Lage</em>', ru: 'Коста-дель-Соль<br><em>Район за Районом</em>', ar: 'كوستا ديل سول<br><em>منطقة تلو الأخرى</em>' },
  { find: "Marbella brings together beaches, restaurants, international schools and some of the coast's most sought-after addresses.", es: 'Marbella reúne playas, restaurantes, colegios internacionales y algunas de las direcciones más solicitadas de la costa.', fr: 'Marbella réunit plages, restaurants, écoles internationales et certaines des adresses les plus prisées de la côte.', de: 'Marbella vereint Strände, Restaurants, internationale Schulen und einige der begehrtesten Adressen der Küste.', ru: 'Марбелья объединяет пляжи, рестораны, международные школы и одни из самых престижных адресов побережья.', ar: 'تجمع ماربيا بين الشواطئ والمطاعم والمدارس الدولية وبعض أكثر العناوين رواجًا على الساحل.' },
  { find: 'Estepona has grown quickly, with better public spaces, new projects and a more relaxed feel than central Marbella.', es: 'Estepona ha crecido rápidamente, con mejores espacios públicos, nuevas promociones y un ambiente más tranquilo que el centro de Marbella.', fr: "Estepona s'est développée rapidement, avec des espaces publics améliorés, de nouveaux programmes et une ambiance plus détendue que le centre de Marbella.", de: 'Estepona hat sich schnell entwickelt, mit besseren öffentlichen Räumen, neuen Projekten und einer entspannteren Atmosphäre als im Zentrum Marbellas.', ru: 'Эстепона быстро развивается: здесь появились более благоустроенные общественные пространства, новые проекты и более спокойная атмосфера, чем в центре Марбельи.', ar: 'شهدت استيبونا نموًا سريعًا، مع مساحات عامة أفضل ومشاريع جديدة وأجواء أكثر هدوءًا من وسط ماربيا.' },
  { find: 'Benahavís is known for privacy, hillside views, golf and gated communities close to Marbella.', es: 'Benahavís es conocido por su privacidad, vistas a la montaña, golf y urbanizaciones cerradas cerca de Marbella.', fr: 'Benahavís est réputée pour son intimité, ses vues sur les collines, le golf et ses résidences fermées à proximité de Marbella.', de: 'Benahavís ist bekannt für Privatsphäre, Ausblicke auf die Hügel, Golf und geschlossene Wohnanlagen nahe Marbella.', ru: 'Бенаависе известен уединённостью, видами на холмы, гольф-полями и закрытыми резиденциями недалеко от Марбельи.', ar: 'تشتهر بيناهافيس بالخصوصية وإطلالات التلال والغولف والمجمعات السكنية المسورة القريبة من ماربيا.' },
  { find: 'Nueva Andalucía puts golf, restaurants and Puerto Banús close by, making it a practical base for holidays or longer stays.', es: 'Nueva Andalucía tiene el golf, los restaurantes y Puerto Banús cerca, lo que la convierte en una base práctica para vacaciones o estancias largas.', fr: "Nueva Andalucía place le golf, les restaurants et Puerto Banús à proximité, ce qui en fait une base pratique pour des vacances ou des séjours plus longs.", de: 'Nueva Andalucía bietet Golf, Restaurants und Puerto Banús in unmittelbarer Nähe und ist damit eine praktische Basis für Urlaub oder längere Aufenthalte.', ru: 'Нуэва-Андалусия находится рядом с полями для гольфа, ресторанами и Пуэрто-Банус, что делает её удобной базой для отдыха или длительного пребывания.', ar: 'تجمع نويفا أندلوثيا بين ملاعب الغولف والمطاعم وبويرتو بانوس في مكان قريب، ما يجعلها قاعدة عملية للإجازات أو الإقامات الطويلة.' },
  { find: 'Mijas and Fuengirola offer good links to Málaga, established coastal life and a wide choice of newer homes.', es: 'Mijas y Fuengirola ofrecen buenas conexiones con Málaga, vida costera consolidada y una amplia oferta de viviendas más nuevas.', fr: 'Mijas et Fuengirola offrent de bonnes liaisons avec Málaga, une vie côtière bien établie et un large choix de logements plus récents.', de: 'Mijas und Fuengirola bieten gute Verbindungen nach Málaga, etabliertes Küstenleben und eine große Auswahl an neueren Wohnungen.', ru: 'Михас и Фуэнхирола предлагают удобное сообщение с Малагой, сложившуюся прибрежную жизнь и широкий выбор новых домов.', ar: 'توفر ميخاس وفوينخيرولا روابط جيدة مع مالقة، وحياة ساحلية راسخة، ومجموعة واسعة من المساكن الأحدث.' },
  { find: 'View area guide <span aria-hidden="true">&#8594;</span>', es: 'Ver guía de la zona <span aria-hidden="true">&#8594;</span>', fr: 'Voir le guide du secteur <span aria-hidden="true">&#8594;</span>', de: 'Lageführer Ansehen <span aria-hidden="true">&#8594;</span>', ru: 'Смотреть гид по району <span aria-hidden="true">&#8594;</span>', ar: 'عرض دليل المنطقة <span aria-hidden="true">&#8594;</span>' },
  // Journey section
  { find: '<span class="label reveal">Our Process</span>', es: '<span class="label reveal">Nuestro Proceso</span>', fr: '<span class="label reveal">Notre Processus</span>', de: '<span class="label reveal">Unser Ablauf</span>', ru: '<span class="label reveal">Наш Процесс</span>', ar: '<span class="label reveal">عمليتنا</span>' },
  { find: 'The Buyer<br><em>Journey</em>', es: 'El Recorrido<br><em>del Comprador</em>', fr: "Le Parcours<br><em>de l'Acheteur</em>", de: 'Die Reise des<br><em>Käufers</em>', ru: 'Путь<br><em>Покупателя</em>', ar: 'رحلة<br><em>المشتري</em>' },
  { find: 'One clear route from the first conversation to handover, with the right checks and decisions made at each stage.', es: 'Un camino claro desde la primera conversación hasta la entrega de llaves, con las comprobaciones y decisiones adecuadas en cada etapa.', fr: "Un parcours clair depuis le premier échange jusqu'à la livraison, avec les vérifications et décisions adaptées à chaque étape.", de: 'Ein klarer Weg vom ersten Gespräch bis zur Übergabe, mit den richtigen Prüfungen und Entscheidungen in jeder Phase.', ru: 'Понятный путь от первого разговора до передачи ключей, с необходимыми проверками и решениями на каждом этапе.', ar: 'مسار واضح من أول محادثة وحتى التسليم، مع الفحوصات والقرارات الصحيحة في كل مرحلة.' },
  { find: '<h3>Consultation</h3>', es: '<h3>Consulta Inicial</h3>', fr: '<h3>Consultation</h3>', de: '<h3>Beratungsgespräch</h3>', ru: '<h3>Консультация</h3>', ar: '<h3>الاستشارة</h3>' },
  { find: '<p>We start with a straightforward conversation about your plans, budget, timing and how you want to use the home.</p>', es: '<p>Empezamos con una conversación sencilla sobre tus planes, presupuesto, plazos y cómo quieres usar la vivienda.</p>', fr: "<p>Nous commençons par un échange simple sur vos projets, votre budget, votre calendrier et l'usage prévu du logement.</p>", de: '<p>Wir beginnen mit einem unkomplizierten Gespräch über Ihre Pläne, Ihr Budget, den Zeitrahmen und die geplante Nutzung der Immobilie.</p>', ru: '<p>Мы начинаем с простого разговора о ваших планах, бюджете, сроках и том, как вы планируете использовать жильё.</p>', ar: '<p>نبدأ بمحادثة مباشرة حول خططك وميزانيتك والجدول الزمني وكيفية استخدامك للمنزل.</p>' },
  { find: '>Start a conversation<', es: '>Iniciar una conversación<', fr: '>Démarrer une Conversation<', de: '>Gespräch Beginnen<', ru: '>Начать Разговор<', ar: '>ابدأ محادثة<' },
  { find: '<h3>Project Matching</h3>', es: '<h3>Selección de Proyectos</h3>', fr: '<h3>Sélection de Projets</h3>', de: '<h3>Projektauswahl</h3>', ru: '<h3>Подбор Проекта</h3>', ar: '<h3>مطابقة المشروع</h3>' },
  { find: '<p>You receive a focused shortlist that fits, without having to sort through the whole market.</p>', es: '<p>Recibes una lista personalizada y ajustada a tus necesidades, sin tener que revisar todo el mercado.</p>', fr: "<p>Vous recevez une sélection ciblée et adaptée, sans avoir à parcourir tout le marché.</p>", de: '<p>Sie erhalten eine gezielte, passende Auswahl, ohne den gesamten Markt selbst durchsuchen zu müssen.</p>', ru: '<p>Вы получаете точную подборку, соответствующую вашим требованиям, без необходимости изучать весь рынок самостоятельно.</p>', ar: '<p>تحصل على قائمة مختارة ومركزة تناسبك، دون الحاجة لتصفح السوق بالكامل.</p>' },
  { find: '<h3>Project Review</h3>', es: '<h3>Revisión del Proyecto</h3>', fr: '<h3>Analyse du Projet</h3>', de: '<h3>Projektprüfung</h3>', ru: '<h3>Анализ Проекта</h3>', ar: '<h3>مراجعة المشروع</h3>' },
  { find: '<p>We review the exact home, orientation, floorplan, materials, payment schedule and developer track record before you decide.</p>', es: '<p>Revisamos la vivienda exacta, orientación, plano, materiales, calendario de pagos y trayectoria de la promotora antes de que decidas.</p>', fr: "<p>Nous examinons le logement précis, son orientation, son plan, ses matériaux, l'échéancier de paiement et le parcours du promoteur avant votre décision.</p>", de: '<p>Wir prüfen die genaue Wohneinheit, Ausrichtung, den Grundriss, die Materialien, den Zahlungsplan und die Erfolgsbilanz des Bauträgers, bevor Sie sich entscheiden.</p>', ru: '<p>Мы анализируем конкретный объект, ориентацию, планировку, материалы, график платежей и репутацию застройщика до того, как вы примете решение.</p>', ar: '<p>نراجع المسكن بالتحديد والاتجاه والتصميم والمواد وجدول الدفع وسجل المطور قبل أن تقرر.</p>' },
  { find: '<h3>Reservation &amp; Legal</h3>', es: '<h3>Reserva y Aspectos Legales</h3>', fr: '<h3>Réservation et Aspects Juridiques</h3>', de: '<h3>Reservierung & Rechtliches</h3>', ru: '<h3>Резервирование и Юридическое Сопровождение</h3>', ar: '<h3>الحجز والإجراءات القانونية</h3>' },
  { find: '<p>When you are ready, we guide the reservation and work alongside your lawyer through the checks.</p>', es: '<p>Cuando estés listo, te acompañamos en la reserva y trabajamos junto a tu abogado durante las comprobaciones.</p>', fr: "<p>Lorsque vous êtes prêt, nous vous accompagnons dans la réservation et travaillons avec votre avocat tout au long des vérifications.</p>", de: '<p>Sobald Sie bereit sind, begleiten wir die Reservierung und arbeiten gemeinsam mit Ihrem Anwalt die Prüfungen durch.</p>', ru: '<p>Когда вы будете готовы, мы сопровождаем резервирование и работаем вместе с вашим юристом на всех этапах проверки.</p>', ar: '<p>عندما تكون جاهزًا، نرشدك خلال عملية الحجز ونعمل مع محاميك خلال إجراءات الفحص.</p>' },
  { find: '<h3>Completion &amp; After-Sale</h3>', es: '<h3>Entrega y Posventa</h3>', fr: '<h3>Livraison et Service Après-Vente</h3>', de: '<h3>Übergabe & Nachbetreuung</h3>', ru: '<h3>Завершение Сделки и Послепродажное Сопровождение</h3>', ar: '<h3>التسليم وخدمة ما بعد البيع</h3>' },
  { find: '<p>We stay involved through inspection and handover, and connect you with trusted local support after completion.</p>', es: '<p>Seguimos presentes durante la inspección y la entrega, y te ponemos en contacto con apoyo local de confianza tras la compra.</p>', fr: "<p>Nous restons impliqués lors de l'inspection et de la livraison, et vous mettons en relation avec des partenaires locaux de confiance après l'achat.</p>", de: '<p>Wir begleiten Sie bei Abnahme und Übergabe und verbinden Sie nach der Fertigstellung mit vertrauenswürdiger lokaler Unterstützung.</p>', ru: '<p>Мы остаёмся рядом на этапе осмотра и передачи ключей и знакомим вас с надёжными местными партнёрами после завершения сделки.</p>', ar: '<p>نبقى معك خلال المعاينة والتسليم، ونوصلك بدعم محلي موثوق بعد إتمام الشراء.</p>' },
  // About section
  { find: '<span class="label reveal">About the Firm</span>', es: '<span class="label reveal">Sobre la Firma</span>', fr: "<span class=\"label reveal\">À Propos de l'Agence</span>", de: '<span class="label reveal">Über das Unternehmen</span>', ru: '<span class="label reveal">О Компании</span>', ar: '<span class="label reveal">عن الشركة</span>' },
  { find: 'We Know<br><em>New Developments</em>', es: 'Conocemos<br><em>la Obra Nueva</em>', fr: 'Nous Connaissons<br><em>les Programmes Neufs</em>', de: 'Wir Kennen Uns Aus<br><em>mit Neubauprojekten</em>', ru: 'Мы Знаем<br><em>Новостройки</em>', ar: 'نحن نعرف<br><em>المشاريع الجديدة</em>' },
  { find: 'Nueva Living was created for people who want straightforward help when buying a new home on the Costa del Sol.', es: 'Nueva Living nació para quienes buscan ayuda clara y directa al comprar una vivienda nueva en la Costa del Sol.', fr: "Nueva Living a été créée pour les personnes qui souhaitent un accompagnement simple et direct lors de l'achat d'un bien neuf sur la Costa del Sol.", de: 'Nueva Living wurde für Menschen gegründet, die beim Kauf einer neuen Immobilie an der Costa del Sol unkomplizierte Unterstützung wünschen.', ru: 'Nueva Living создана для тех, кто хочет получить понятную и прямую помощь при покупке новой недвижимости на Коста-дель-Соль.', ar: 'تأسست Nueva Living لخدمة من يبحثون عن مساعدة واضحة ومباشرة عند شراء منزل جديد في كوستا ديل سول.' },
  { find: 'Because new developments are all we do, we know the projects, the developers and the questions worth asking.', es: 'Como solo nos dedicamos a la obra nueva, conocemos los proyectos, las promotoras y las preguntas que merece la pena hacer.', fr: "Comme nous ne travaillons que sur des programmes neufs, nous connaissons les projets, les promoteurs et les questions à poser.", de: 'Da wir uns ausschließlich auf Neubauprojekte konzentrieren, kennen wir die Projekte, die Bauträger und die Fragen, die es zu stellen gilt.', ru: 'Поскольку мы занимаемся исключительно новостройками, мы знаем проекты, застройщиков и вопросы, которые действительно важно задать.', ar: 'بما أننا نتخصص حصريًا في المشاريع الجديدة، فإننا نعرف المشاريع والمطورين والأسئلة الجديرة بالطرح.' },
  { find: '>About Nueva Living<', es: '>Sobre Nueva Living<', fr: '>À Propos de Nueva Living<', de: '>Über Nueva Living<', ru: '>О Nueva Living<', ar: '>عن Nueva Living<' },
  // Referral band
  { find: '<span class="label reveal">Know Someone Looking?</span>', es: '<span class="label reveal">¿Conoces a Alguien Interesado?</span>', fr: "<span class=\"label reveal\">Vous Connaissez Quelqu'un qui Cherche ?</span>", de: '<span class="label reveal">Kennen Sie Jemanden auf der Suche?</span>', ru: '<span class="label reveal">Знаете Кого-то в Поиске?</span>', ar: '<span class="label reveal">هل تعرف شخصًا يبحث عن عقار؟</span>' },
  { find: 'Introduce someone,<br><em>get rewarded</em>', es: 'Preséntanos a alguien,<br><em>recibe una recompensa</em>', fr: "Recommandez quelqu'un,<br><em>soyez récompensé</em>", de: 'Empfehlen Sie jemanden,<br><em>werden Sie belohnt</em>', ru: 'Порекомендуйте нас,<br><em>получите вознаграждение</em>', ar: 'قدّم شخصًا،<br><em>واحصل على مكافأة</em>' },
  { find: 'If someone in your life is thinking about a home on the Costa del Sol, our Referral &amp; Ambassador Program lets you introduce them and receive a share of our commission when their purchase completes.', es: 'Si alguien de tu entorno está pensando en comprar una vivienda en la Costa del Sol, nuestro Programa de Referidos y Embajadores te permite presentárnoslo y recibir una parte de nuestra comisión cuando complete la compra.', fr: "Si une personne de votre entourage envisage l'achat d'un bien sur la Costa del Sol, notre Programme de Parrainage et d'Ambassadeurs vous permet de la présenter et de recevoir une partie de notre commission lorsque son achat est finalisé.", de: 'Wenn jemand in Ihrem Umfeld über eine Immobilie an der Costa del Sol nachdenkt, können Sie ihn über unser Empfehlungs- und Botschafterprogramm vorstellen und einen Anteil unserer Provision erhalten, sobald der Kauf abgeschlossen ist.', ru: 'Если кто-то из ваших знакомых задумывается о покупке жилья на Коста-дель-Соль, наша Реферальная и Амбассадорская Программа позволяет вам представить его нам и получить часть нашей комиссии после завершения сделки.', ar: 'إذا كان أحد معارفك يفكر في شراء منزل في كوستا ديل سول، يتيح لك برنامج الإحالة والسفراء الخاص بنا تقديمه لنا والحصول على نسبة من عمولتنا عند إتمام عملية الشراء.' },
  { find: '>Introduce Someone<', es: '>Presentar a Alguien<', fr: '>Recommander une Personne<', de: '>Jemanden Empfehlen<', ru: '>Порекомендовать<', ar: '>قدّم شخصًا<' },
  // Contact / shortlist form
  { find: 'Tell Us What You Need</span>', es: 'Cuéntanos Qué Necesitas</span>', fr: 'Dites-Nous ce Dont Vous Avez Besoin</span>', de: 'Sagen Sie Uns, Was Sie Suchen</span>', ru: 'Расскажите, Что Вам Нужно</span>', ar: 'أخبرنا بما تحتاجه</span>' },
  { find: 'Get a Personal<br><em>Project Shortlist</em>', es: 'Solicita tu Lista<br><em>Personalizada de Proyectos</em>', fr: 'Recevez une Sélection<br><em>de Projets Personnalisée</em>', de: 'Erhalten Sie eine Persönliche<br><em>Projektauswahl</em>', ru: 'Получите Персональную<br><em>Подборку Проектов</em>', ar: 'احصل على قائمة<br><em>مشاريع مختارة شخصية</em>' },
  { find: 'Leave your contact details and tell us what you are looking for. Add more preferences if you already have a clear idea.', es: 'Déjanos tus datos de contacto y cuéntanos qué buscas. Añade más preferencias si ya tienes una idea clara.', fr: "Laissez-nous vos coordonnées et indiquez-nous ce que vous recherchez. Ajoutez davantage de préférences si vous avez déjà une idée précise.", de: 'Hinterlassen Sie Ihre Kontaktdaten und teilen Sie uns mit, wonach Sie suchen. Fügen Sie weitere Präferenzen hinzu, wenn Sie bereits eine klare Vorstellung haben.', ru: 'Оставьте свои контактные данные и расскажите, что вы ищете. Добавьте дополнительные предпочтения, если у вас уже есть чёткое представление.', ar: 'اترك بيانات التواصل الخاصة بك وأخبرنا بما تبحث عنه. أضف مزيدًا من التفضيلات إذا كانت لديك فكرة واضحة بالفعل.' },
  { find: '<label for="f-first-name">First Name</label>', es: '<label for="f-first-name">Nombre</label>', fr: '<label for="f-first-name">Prénom</label>', de: '<label for="f-first-name">Vorname</label>', ru: '<label for="f-first-name">Имя</label>', ar: '<label for="f-first-name">الاسم الأول</label>' },
  { find: '<label for="f-last-name">Last Name</label>', es: '<label for="f-last-name">Apellidos</label>', fr: '<label for="f-last-name">Nom</label>', de: '<label for="f-last-name">Nachname</label>', ru: '<label for="f-last-name">Фамилия</label>', ar: '<label for="f-last-name">اسم العائلة</label>' },
  { find: '<label for="f-email">Email Address</label>', es: '<label for="f-email">Correo Electrónico</label>', fr: '<label for="f-email">Adresse E-mail</label>', de: '<label for="f-email">E-Mail-Adresse</label>', ru: '<label for="f-email">Электронная Почта</label>', ar: '<label for="f-email">البريد الإلكتروني</label>' },
  { find: '<label for="f-phone">Phone Number</label>', es: '<label for="f-phone">Teléfono</label>', fr: '<label for="f-phone">Numéro de Téléphone</label>', de: '<label for="f-phone">Telefonnummer</label>', ru: '<label for="f-phone">Номер Телефона</label>', ar: '<label for="f-phone">رقم الهاتف</label>' },
  { find: '<span>Add More Details</span>', es: '<span>Añadir Más Detalles</span>', fr: '<span>Ajouter Plus de Détails</span>', de: '<span>Weitere Details Hinzufügen</span>', ru: '<span>Добавить Подробности</span>', ar: '<span>إضافة مزيد من التفاصيل</span>' },
  { find: '<small>Optional - helps us refine your shortlist</small>', es: '<small>Opcional - nos ayuda a afinar tu selección</small>', fr: '<small>Facultatif - nous aide à affiner votre sélection</small>', de: '<small>Optional - hilft uns, Ihre Auswahl zu verfeinern</small>', ru: '<small>Необязательно — поможет нам уточнить вашу подборку</small>', ar: '<small>اختياري - يساعدنا على تحسين قائمتك المختارة</small>' },
  { find: '<label for="f-area">Preferred Area</label>', es: '<label for="f-area">Zona Preferida</label>', fr: '<label for="f-area">Secteur Préféré</label>', de: '<label for="f-area">Bevorzugte Lage</label>', ru: '<label for="f-area">Предпочитаемый Район</label>', ar: '<label for="f-area">المنطقة المفضلة</label>' },
  { find: '<option value="">Select area…</option>', es: '<option value="">Selecciona una zona…</option>', fr: '<option value="">Sélectionnez un secteur…</option>', de: '<option value="">Lage auswählen…</option>', ru: '<option value="">Выберите район…</option>', ar: '<option value="">اختر منطقة…</option>' },
  { find: '<option>Open to all areas</option>', es: '<option>Abierto a cualquier zona</option>', fr: '<option>Ouvert à tous les secteurs</option>', de: '<option>Alle Lagen in Betracht ziehen</option>', ru: '<option>Рассмотрю любой район</option>', ar: '<option>مفتوح لجميع المناطق</option>' },
  { find: '<label for="f-property-type">Property Type Interest</label>', es: '<label for="f-property-type">Tipo de Vivienda de Interés</label>', fr: '<label for="f-property-type">Type de Bien Recherché</label>', de: '<label for="f-property-type">Gewünschter Immobilientyp</label>', ru: '<label for="f-property-type">Тип Недвижимости</label>', ar: '<label for="f-property-type">نوع العقار المطلوب</label>' },
  { find: '<option value="">Select type…</option>', es: '<option value="">Selecciona un tipo…</option>', fr: '<option value="">Sélectionnez un type…</option>', de: '<option value="">Typ auswählen…</option>', ru: '<option value="">Выберите тип…</option>', ar: '<option value="">اختر النوع…</option>' },
  { find: '<option>Apartments</option>', es: '<option>Apartamentos</option>', fr: '<option>Appartements</option>', de: '<option>Wohnungen</option>', ru: '<option>Апартаменты</option>', ar: '<option>شقق</option>' },
  { find: '<option>Penthouses</option>', es: '<option>Áticos</option>', fr: '<option>Penthouses</option>', de: '<option>Penthäuser</option>', ru: '<option>Пентхаусы</option>', ar: '<option>بنتهاوس</option>' },
  { find: '<option>Villas</option>', es: '<option>Villas</option>', fr: '<option>Villas</option>', de: '<option>Villen</option>', ru: '<option>Виллы</option>', ar: '<option>فلل</option>' },
  { find: '<option>Townhouses</option>', es: '<option>Casas Adosadas</option>', fr: '<option>Maisons de Ville</option>', de: '<option>Reihenhäuser</option>', ru: '<option>Таунхаусы</option>', ar: '<option>تاون هاوس</option>' },
  { find: '<option>Mixed / Open</option>', es: '<option>Mixto / Abierto</option>', fr: '<option>Mixte / Ouvert</option>', de: '<option>Gemischt / Offen</option>', ru: '<option>Смешанный / Не Определился</option>', ar: '<option>مختلط / مفتوح</option>' },
  { find: '<label for="f-budget">Budget Range</label>', es: '<label for="f-budget">Rango de Presupuesto</label>', fr: '<label for="f-budget">Fourchette Budgétaire</label>', de: '<label for="f-budget">Budgetrahmen</label>', ru: '<label for="f-budget">Диапазон Бюджета</label>', ar: '<label for="f-budget">النطاق السعري</label>' },
  { find: '<option value="">Select budget…</option>', es: '<option value="">Selecciona un presupuesto…</option>', fr: '<option value="">Sélectionnez un budget…</option>', de: '<option value="">Budget auswählen…</option>', ru: '<option value="">Выберите бюджет…</option>', ar: '<option value="">اختر الميزانية…</option>' },
  { find: '<label for="f-purpose">Purchase Purpose</label>', es: '<label for="f-purpose">Motivo de la Compra</label>', fr: "<label for=\"f-purpose\">Objectif de l'Achat</label>", de: '<label for="f-purpose">Zweck des Kaufs</label>', ru: '<label for="f-purpose">Цель Покупки</label>', ar: '<label for="f-purpose">الغرض من الشراء</label>' },
  { find: '<option value="">Select purpose…</option>', es: '<option value="">Selecciona un motivo…</option>', fr: '<option value="">Sélectionnez un objectif…</option>', de: '<option value="">Zweck auswählen…</option>', ru: '<option value="">Выберите цель…</option>', ar: '<option value="">اختر الغرض…</option>' },
  { find: '<option>Primary Residence</option>', es: '<option>Vivienda Habitual</option>', fr: '<option>Résidence Principale</option>', de: '<option>Hauptwohnsitz</option>', ru: '<option>Основное Жильё</option>', ar: '<option>مسكن رئيسي</option>' },
  { find: '<option>Holiday Home</option>', es: '<option>Vivienda Vacacional</option>', fr: '<option>Résidence Secondaire</option>', de: '<option>Ferienimmobilie</option>', ru: '<option>Дом для Отдыха</option>', ar: '<option>منزل عطلات</option>' },
  { find: '<option>Investment / Rental</option>', es: '<option>Inversión / Alquiler</option>', fr: '<option>Investissement / Location</option>', de: '<option>Kapitalanlage / Vermietung</option>', ru: '<option>Инвестиции / Аренда</option>', ar: '<option>استثمار / تأجير</option>' },
  { find: '<option>Combination</option>', es: '<option>Combinación</option>', fr: '<option>Combinaison</option>', de: '<option>Kombination</option>', ru: '<option>Комбинация</option>', ar: '<option>مزيج من الأغراض</option>' },
  { find: '<label for="f-msg">Message (optional)</label>', es: '<label for="f-msg">Mensaje (opcional)</label>', fr: '<label for="f-msg">Message (facultatif)</label>', de: '<label for="f-msg">Nachricht (optional)</label>', ru: '<label for="f-msg">Сообщение (необязательно)</label>', ar: '<label for="f-msg">رسالة (اختياري)</label>' },
  { find: 'placeholder="Tell us about your requirements…"', es: 'placeholder="Cuéntanos qué necesitas…"', fr: 'placeholder="Parlez-nous de vos critères…"', de: 'placeholder="Erzählen Sie uns von Ihren Anforderungen…"', ru: 'placeholder="Расскажите нам о ваших требованиях…"', ar: 'placeholder="أخبرنا عن متطلباتك…"' },
  { find: '<span>I agree to be contacted and for my data to be stored.</span>', es: '<span>Acepto ser contactado/a y que mis datos sean almacenados.</span>', fr: "<span>J'accepte d'être contacté(e) et que mes données soient conservées.</span>", de: '<span>Ich stimme zu, kontaktiert zu werden, und dass meine Daten gespeichert werden.</span>', ru: '<span>Я согласен(на) на обработку моих данных и на то, чтобы со мной связались.</span>', ar: '<span>أوافق على التواصل معي وعلى تخزين بياناتي.</span>' },
  { find: '<span>I would also like to receive occasional project updates from Nueva Living.</span>', es: '<span>También me gustaría recibir novedades ocasionales de proyectos por parte de Nueva Living.</span>', fr: '<span>Je souhaite également recevoir occasionnellement des actualités de projets de la part de Nueva Living.</span>', de: '<span>Ich möchte außerdem gelegentlich Projekt-Updates von Nueva Living erhalten.</span>', ru: '<span>Я также хотел(а) бы периодически получать новости о проектах от Nueva Living.</span>', ar: '<span>أرغب أيضًا في تلقي تحديثات دورية عن المشاريع من Nueva Living.</span>' },
  { find: '>Send My Request<', es: '>Enviar Mi Solicitud<', fr: '>Envoyer Ma Demande<', de: '>Meine Anfrage Senden<', ru: '>Отправить Запрос<', ar: '>إرسال طلبي<' },
  { find: '<span class="form-note">We review every enquiry personally.</span>', es: '<span class="form-note">Revisamos cada consulta de forma personal.</span>', fr: '<span class="form-note">Nous examinons chaque demande personnellement.</span>', de: '<span class="form-note">Wir prüfen jede Anfrage persönlich.</span>', ru: '<span class="form-note">Мы рассматриваем каждый запрос лично.</span>', ar: '<span class="form-note">نراجع كل استفسار شخصيًا.</span>' },
  { find: 'Prefer email? <a href="mailto:contact@nuevaliving.com">contact@nuevaliving.com</a>', es: '¿Prefieres el correo? <a href="mailto:contact@nuevaliving.com">contact@nuevaliving.com</a>', fr: "Vous préférez l'e-mail ? <a href=\"mailto:contact@nuevaliving.com\">contact@nuevaliving.com</a>", de: 'Lieber per E-Mail? <a href="mailto:contact@nuevaliving.com">contact@nuevaliving.com</a>', ru: 'Предпочитаете почту? <a href="mailto:contact@nuevaliving.com">contact@nuevaliving.com</a>', ar: 'تفضل البريد الإلكتروني؟ <a href="mailto:contact@nuevaliving.com">contact@nuevaliving.com</a>' },
  // "Show more" (why / areas / journey grids)
  { find: 'data-expand-grid>Show More</button>', es: 'data-expand-grid>Ver Más</button>', fr: 'data-expand-grid>Voir Plus</button>', de: 'data-expand-grid>Mehr Anzeigen</button>', ru: 'data-expand-grid>Показать Больше</button>', ar: 'data-expand-grid>عرض المزيد</button>' },
  // Cinematic-presentation viewer chrome
  { find: 'aria-label="Cinematic Presentation — Nueva Living"', es: 'aria-label="Presentación Cinemática — Nueva Living"', fr: 'aria-label="Présentation Cinématique — Nueva Living"', de: 'aria-label="Cinematische Präsentation — Nueva Living"', ru: 'aria-label="Кинематографичная Презентация — Nueva Living"', ar: 'aria-label="عرض سينمائي — Nueva Living"' },
  { find: '<div class="vbrand">Nueva Living · Cinematic Presentation</div>', es: '<div class="vbrand">Nueva Living · Presentación Cinemática</div>', fr: '<div class="vbrand">Nueva Living · Présentation Cinématique</div>', de: '<div class="vbrand">Nueva Living · Cinematische Präsentation</div>', ru: '<div class="vbrand">Nueva Living · Кинематографичная Презентация</div>', ar: '<div class="vbrand">Nueva Living · عرض سينمائي</div>' },
  { find: 'aria-label="Pause guided viewing"', es: 'aria-label="Pausar recorrido guiado"', fr: 'aria-label="Mettre en pause la visite guidée"', de: 'aria-label="Geführte Ansicht Pausieren"', ru: 'aria-label="Приостановить показ с гидом"', ar: 'aria-label="إيقاف الجولة الموجهة مؤقتًا"' },
  { find: '<span class="mode-label">Guided</span>', es: '<span class="mode-label">Guiado</span>', fr: '<span class="mode-label">Guidé</span>', de: '<span class="mode-label">Geführt</span>', ru: '<span class="mode-label">С Гидом</span>', ar: '<span class="mode-label">موجّه</span>' },
  { find: 'aria-label="Project details" aria-controls="vinfoPanel"', es: 'aria-label="Detalles del proyecto" aria-controls="vinfoPanel"', fr: 'aria-label="Détails du projet" aria-controls="vinfoPanel"', de: 'aria-label="Projektdetails" aria-controls="vinfoPanel"', ru: 'aria-label="Информация о проекте" aria-controls="vinfoPanel"', ar: 'aria-label="تفاصيل المشروع" aria-controls="vinfoPanel"' },
  { find: '<span class="info-label">Project Details</span>', es: '<span class="info-label">Detalles del Proyecto</span>', fr: '<span class="info-label">Détails du Projet</span>', de: '<span class="info-label">Projektdetails</span>', ru: '<span class="info-label">Информация о Проекте</span>', ar: '<span class="info-label">تفاصيل المشروع</span>' },
  { find: 'aria-label="Exit viewing">', es: 'aria-label="Salir de la presentación">', fr: 'aria-label="Quitter la visite">', de: 'aria-label="Ansicht Verlassen">', ru: 'aria-label="Выйти из просмотра">', ar: 'aria-label="الخروج من العرض">' },
  { find: '</svg>\n          Exit\n        </button>', es: '</svg>\n          Salir\n        </button>', fr: '</svg>\n          Quitter\n        </button>', de: '</svg>\n          Verlassen\n        </button>', ru: '</svg>\n          Выход\n        </button>', ar: '</svg>\n          خروج\n        </button>' },
  { find: '<span class="vclt">Scroll</span>', es: '<span class="vclt">Desplázate</span>', fr: '<span class="vclt">Défiler</span>', de: '<span class="vclt">Scrollen</span>', ru: '<span class="vclt">Прокрутите</span>', ar: '<span class="vclt">مرر للأسفل</span>' },
  { find: 'aria-label="Project details" aria-hidden="true">', es: 'aria-label="Detalles del proyecto" aria-hidden="true">', fr: 'aria-label="Détails du projet" aria-hidden="true">', de: 'aria-label="Projektdetails" aria-hidden="true">', ru: 'aria-label="Информация о проекте" aria-hidden="true">', ar: 'aria-label="تفاصيل المشروع" aria-hidden="true">' },
  { find: '<span class="vinfo-kicker" id="vinfoKicker">Project Details</span>', es: '<span class="vinfo-kicker" id="vinfoKicker">Detalles del Proyecto</span>', fr: '<span class="vinfo-kicker" id="vinfoKicker">Détails du Projet</span>', de: '<span class="vinfo-kicker" id="vinfoKicker">Projektdetails</span>', ru: '<span class="vinfo-kicker" id="vinfoKicker">Информация о Проекте</span>', ar: '<span class="vinfo-kicker" id="vinfoKicker">تفاصيل المشروع</span>' },
  { find: 'aria-label="Close project details"', es: 'aria-label="Cerrar detalles del proyecto"', fr: 'aria-label="Fermer les détails du projet"', de: 'aria-label="Projektdetails Schließen"', ru: 'aria-label="Закрыть информацию о проекте"', ar: 'aria-label="إغلاق تفاصيل المشروع"' },
  { find: '<span class="vt-label" id="vtlbl">01 — Private Preview</span>', es: '<span class="vt-label" id="vtlbl">01 — Vista Privada</span>', fr: '<span class="vt-label" id="vtlbl">01 — Aperçu Privé</span>', de: '<span class="vt-label" id="vtlbl">01 — Private Vorschau</span>', ru: '<span class="vt-label" id="vtlbl">01 — Закрытый Показ</span>', ar: '<span class="vt-label" id="vtlbl">01 — معاينة خاصة</span>' },
  { find: '<h2 class="vt-headline" id="vthl">Take a closer look,<br>one space at a time.</h2>', es: '<h2 class="vt-headline" id="vthl">Descúbrelo de cerca,<br>espacio a espacio.</h2>', fr: '<h2 class="vt-headline" id="vthl">Découvrez chaque espace,<br>un à la fois.</h2>', de: '<h2 class="vt-headline" id="vthl">Werfen Sie einen genaueren Blick,<br>Raum für Raum.</h2>', ru: '<h2 class="vt-headline" id="vthl">Загляните ближе,<br>пространство за пространством.</h2>', ar: '<h2 class="vt-headline" id="vthl">اكتشف كل تفصيل عن قرب،<br>مساحة تلو الأخرى.</h2>' },
  { find: '<span class="vt-sub" id="vtsub">See the setting, architecture and everyday spaces before asking for the full project pack.</span>', es: '<span class="vt-sub" id="vtsub">Conoce el entorno, la arquitectura y los espacios cotidianos antes de solicitar el dosier completo del proyecto.</span>', fr: "<span class=\"vt-sub\" id=\"vtsub\">Découvrez le cadre, l'architecture et les espaces du quotidien avant de demander le dossier complet du projet.</span>", de: '<span class="vt-sub" id="vtsub">Entdecken Sie die Umgebung, die Architektur und die Alltagsräume, bevor Sie die vollständigen Projektunterlagen anfordern.</span>', ru: '<span class="vt-sub" id="vtsub">Познакомьтесь с окружением, архитектурой и повседневными пространствами перед тем, как запросить полный пакет материалов по проекту.</span>', ar: '<span class="vt-sub" id="vtsub">تعرّف على الموقع والعمارة والمساحات اليومية قبل طلب الملف الكامل للمشروع.</span>' },
  { find: '<div class="v7proj">Nueva Living · New Development Preview</div>', es: '<div class="v7proj">Nueva Living · Vista Previa de Nueva Promoción</div>', fr: '<div class="v7proj">Nueva Living · Aperçu du Programme Neuf</div>', de: '<div class="v7proj">Nueva Living · Vorschau des Neubauprojekts</div>', ru: '<div class="v7proj">Nueva Living · Превью Новостройки</div>', ar: '<div class="v7proj">Nueva Living · معاينة المشروع الجديد</div>' },
  { find: '>Get Project Information<', es: '>Solicitar Información del Proyecto<', fr: '>Recevoir les Informations du Projet<', de: '>Projektinformationen Anfordern<', ru: '>Получить Информацию о Проекте<', ar: '>طلب معلومات المشروع<' },
  { find: '>Exit Viewing<', es: '>Salir de la Presentación<', fr: '>Quitter la Visite<', de: '>Ansicht Verlassen<', ru: '>Выйти из Просмотра<', ar: '>الخروج من العرض<' },
  { find: "vmodeBtn.setAttribute('aria-label', on ? 'Pause guided viewing' : 'Resume guided viewing');", es: "vmodeBtn.setAttribute('aria-label', on ? 'Pausar recorrido guiado' : 'Reanudar recorrido guiado');", fr: "vmodeBtn.setAttribute('aria-label', on ? 'Mettre en pause la visite guidée' : 'Reprendre la visite guidée');", de: "vmodeBtn.setAttribute('aria-label', on ? 'Geführte Ansicht pausieren' : 'Geführte Ansicht fortsetzen');", ru: "vmodeBtn.setAttribute('aria-label', on ? 'Приостановить показ с гидом' : 'Продолжить показ с гидом');", ar: "vmodeBtn.setAttribute('aria-label', on ? 'إيقاف الجولة الموجهة مؤقتًا' : 'استئناف الجولة الموجهة');" },
  { find: "vSetGuidedUI(true, 'Guided');", es: "vSetGuidedUI(true, 'Guiado');", fr: "vSetGuidedUI(true, 'Guidé');", de: "vSetGuidedUI(true, 'Geführt');", ru: "vSetGuidedUI(true, 'С гидом');", ar: "vSetGuidedUI(true, 'موجّه');" },
  { find: "vmodeLabel.textContent = label || (on ? 'Guided' : 'Manual');", es: "vmodeLabel.textContent = label || (on ? 'Guiado' : 'Manual');", fr: "vmodeLabel.textContent = label || (on ? 'Guidé' : 'Manuel');", de: "vmodeLabel.textContent = label || (on ? 'Geführt' : 'Manuell');", ru: "vmodeLabel.textContent = label || (on ? 'С гидом' : 'Вручную');", ar: "vmodeLabel.textContent = label || (on ? 'موجّه' : 'يدوي');" },
  { find: "function vStopGuided(label = 'Manual') {", es: "function vStopGuided(label = 'Manual') {", fr: "function vStopGuided(label = 'Manuel') {", de: "function vStopGuided(label = 'Manuell') {", ru: "function vStopGuided(label = 'Вручную') {", ar: "function vStopGuided(label = 'يدوي') {" },
  { find: "['Starting Price', project.price],", es: "['Precio desde', project.price],", fr: "['Prix de Départ', project.price],", de: "['Startpreis', project.price],", ru: "['Цена от', project.price],", ar: "['السعر ابتداءً من', project.price]," },
  { find: "['Bedrooms', project.bedrooms],", es: "['Dormitorios', project.bedrooms],", fr: "['Chambres', project.bedrooms],", de: "['Schlafzimmer', project.bedrooms],", ru: "['Спальни', project.bedrooms],", ar: "['غرف النوم', project.bedrooms]," },
  { find: "['Built Size', project.builtSize],", es: "['Superficie Construida', project.builtSize],", fr: "['Surface Habitable', project.builtSize],", de: "['Wohnfläche', project.builtSize],", ru: "['Площадь', project.builtSize],", ar: "['المساحة المبنية', project.builtSize]," },
  { find: "['Terrace Size', project.terraceSize],", es: "['Superficie de Terraza', project.terraceSize],", fr: "['Surface de la Terrasse', project.terraceSize],", de: "['Terrassenfläche', project.terraceSize],", ru: "['Площадь Террасы', project.terraceSize],", ar: "['مساحة الشرفة', project.terraceSize]," },
  { find: "['Completion', project.completion],", es: "['Entrega', project.completion],", fr: "['Livraison', project.completion],", de: "['Übergabe', project.completion],", ru: "['Сдача', project.completion],", ar: "['التسليم', project.completion]," },
  { find: "['Positioning', project.status]", es: "['Estado', project.status]", fr: "['Statut', project.status]", de: "['Status', project.status]", ru: "['Статус', project.status]", ar: "['الحالة', project.status]" },
  { find: '<span class="vinfo-pill">New Development</span>', es: '<span class="vinfo-pill">Nueva Promoción</span>', fr: '<span class="vinfo-pill">Programme Neuf</span>', de: '<span class="vinfo-pill">Neubauprojekt</span>', ru: '<span class="vinfo-pill">Новостройка</span>', ar: '<span class="vinfo-pill">مشروع جديد</span>' },
  { find: '<span class="vinfo-pill">Private Preview</span>', es: '<span class="vinfo-pill">Vista Privada</span>', fr: '<span class="vinfo-pill">Aperçu Privé</span>', de: '<span class="vinfo-pill">Private Vorschau</span>', ru: '<span class="vinfo-pill">Закрытый Показ</span>', ar: '<span class="vinfo-pill">معاينة خاصة</span>' },
  { find: "vInfoSection('Overview', project.overview)", es: "vInfoSection('Visión General', project.overview)", fr: "vInfoSection('Aperçu', project.overview)", de: "vInfoSection('Überblick', project.overview)", ru: "vInfoSection('Обзор', project.overview)", ar: "vInfoSection('نظرة عامة', project.overview)" },
  { find: "vInfoSection('Architecture', project.highlights)", es: "vInfoSection('Arquitectura', project.highlights)", fr: "vInfoSection('Architecture', project.highlights)", de: "vInfoSection('Architektur', project.highlights)", ru: "vInfoSection('Архитектура', project.highlights)", ar: "vInfoSection('العمارة', project.highlights)" },
  { find: "vInfoSection('Lifestyle', project.lifestyle)", es: "vInfoSection('Estilo de Vida', project.lifestyle)", fr: "vInfoSection('Art de Vivre', project.lifestyle)", de: "vInfoSection('Lifestyle', project.lifestyle)", ru: "vInfoSection('Образ Жизни', project.lifestyle)", ar: "vInfoSection('نمط الحياة', project.lifestyle)" },
  { find: "vInfoSection('Investment', project.investmentNotes)", es: "vInfoSection('Inversión', project.investmentNotes)", fr: "vInfoSection('Investissement', project.investmentNotes)", de: "vInfoSection('Investition', project.investmentNotes)", ru: "vInfoSection('Инвестиции', project.investmentNotes)", ar: "vInfoSection('الاستثمار', project.investmentNotes)" },
  { find: "vInfoSection('Availability', (project.availability || [])", es: "vInfoSection('Disponibilidad', (project.availability || [])", fr: "vInfoSection('Disponibilité', (project.availability || [])", de: "vInfoSection('Verfügbarkeit', (project.availability || [])", ru: "vInfoSection('Наличие', (project.availability || [])", ar: "vInfoSection('التوفر', (project.availability || [])" },
  { find: '<h3>Get Project Information</h3>', es: '<h3>Solicitar Información del Proyecto</h3>', fr: '<h3>Recevoir les Informations du Projet</h3>', de: '<h3>Projektinformationen Anfordern</h3>', ru: '<h3>Получить Информацию о Проекте</h3>', ar: '<h3>طلب معلومات المشروع</h3>' },
  { find: "project.ctaLabel || 'Get Project Information'", es: "project.ctaLabel || 'Solicitar Información del Proyecto'", fr: "project.ctaLabel || 'Recevoir les Informations du Projet'", de: "project.ctaLabel || 'Projektinformationen Anfordern'", ru: "project.ctaLabel || 'Получить Информацию о Проекте'", ar: "project.ctaLabel || 'طلب معلومات المشروع'" },
  { find: '<p>Get the latest brochure, master plan, floorplans, availability and prices.</p>', es: '<p>Recibe el último dosier, master plan, planos, disponibilidad y precios.</p>', fr: '<p>Recevez la brochure la plus récente, le plan de masse, les plans, la disponibilité et les prix.</p>', de: '<p>Erhalten Sie die aktuelle Broschüre, den Masterplan, Grundrisse, Verfügbarkeit und Preise.</p>', ru: '<p>Получите актуальную брошюру, генеральный план, планировки, информацию о наличии и цены.</p>', ar: '<p>احصل على أحدث كتيب، والمخطط الرئيسي، ومخططات الوحدات، والتوفر، والأسعار.</p>' },
  // Selected Residences card extras: price overlay prefix and the two
  // non-place-name type tags.
  { find: 'dev-price-overlay">From ', es: 'dev-price-overlay">Desde ', fr: 'dev-price-overlay">À partir de ', de: 'dev-price-overlay">Ab ', ru: 'dev-price-overlay">От ', ar: 'dev-price-overlay">ابتداءً من ' },
  { find: 'dev-type-tag">Sea View<', es: 'dev-type-tag">Vistas al Mar<', fr: 'dev-type-tag">Vue Mer<', de: 'dev-type-tag">Meerblick<', ru: 'dev-type-tag">Вид на Море<', ar: 'dev-type-tag">إطلالة على البحر<' },
  { find: 'dev-type-tag">Urban Resort<', es: 'dev-type-tag">Resort Urbano<', fr: 'dev-type-tag">Resort Urbain<', de: 'dev-type-tag">Urbanes Resort<', ru: 'dev-type-tag">Городской Курорт<', ar: 'dev-type-tag">منتجع حضري<' },
  { find: '>Explore All Residences<', es: '>Ver Todas las Viviendas<', fr: '>Voir Toutes les Résidences<', de: '>Alle Residenzen Ansehen<', ru: '>Смотреть Все Резиденции<', ar: '>عرض جميع المساكن<' },
  // Head: page title + meta description
  { find: '<title>Nueva Living | Costa del Sol New Developments</title>', es: '<title>Nueva Living | Obra Nueva en la Costa del Sol</title>', fr: '<title>Nueva Living | Programmes Neufs sur la Costa del Sol</title>', de: '<title>Nueva Living | Neubauprojekte an der Costa del Sol</title>', ru: '<title>Nueva Living | Новостройки на Коста-дель-Соль</title>', ar: '<title>Nueva Living | مشاريع جديدة في كوستا ديل سول</title>' },
  { find: 'Find and compare new-build homes across Marbella, Estepona, Benahavís and the wider Costa del Sol with personal buyer support.', es: 'Encuentra y compara viviendas de obra nueva en Marbella, Estepona, Benahavís y el resto de la Costa del Sol con acompañamiento personal al comprador.', fr: "Trouvez et comparez des logements neufs à Marbella, Estepona, Benahavís et sur l'ensemble de la Costa del Sol avec un accompagnement personnalisé.", de: 'Finden und vergleichen Sie Neubauimmobilien in Marbella, Estepona, Benahavís und an der gesamten Costa del Sol mit persönlicher Käuferbetreuung.', ru: 'Находите и сравнивайте новостройки в Марбелье, Эстепоне, Бенаависе и по всему побережью Коста-дель-Соль с персональным сопровождением покупателя.', ar: 'اعثر على منازل جديدة وقارن بينها في ماربيا واستيبونا وبيناهافيس وسائر كوستا ديل سول مع دعم شخصي للمشتري.' }
];

// Longest find first, so a short entry can never fire inside a longer
// string before that string's own entry has matched.
function homepageContentReplacements(locale) {
  return [...HOMEPAGE_CONTENT_ENTRIES, ...BESPOKE_SCENE_ENTRIES, ...EDITORIAL_ALT_ENTRIES]
    .filter((entry) => entry[locale])
    .sort((a, b) => b.find.length - a.find.length)
    .map((entry) => [entry.find, entry[locale]]);
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

// Homepage card gallery image alt text. Same root cause as the taglines:
// the cards are generated once in English by build_property_pages.mjs, so
// their alt attributes need mapping to each project's already-translated
// media items by index.
function projectCardAltReplacements(locale) {
  if (locale === DEFAULT_LOCALE) return [];
  const projectsDir = path.join(root, 'content/liora-projects');
  if (!existsSync(projectsDir)) return [];
  const replacements = [];
  for (const slug of readdirSync(projectsDir)) {
    const projectPath = path.join(projectsDir, slug, 'project.json');
    if (!existsSync(projectPath)) continue;
    const project = JSON.parse(readFileSync(projectPath, 'utf8'));
    const english = project.media?.items || [];
    const localized = project.i18n?.[locale]?.media?.items || [];
    if (localized.length !== english.length) continue;
    english.forEach((item, index) => {
      const en = item.alt;
      const translated = localized[index]?.alt;
      if (!en || !translated || en === translated) return;
      replacements.push([`alt="${en}"`, `alt="${translated}"`]);
    });
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
  const options = LOCALES.map((meta) => {
    // Absolute path -- see the matching comment in
    // scripts/lib/i18n.mjs's renderLanguageSwitcher() for why: a bare
    // relative "index.html" (English's case, no urlPrefix) gets silently
    // mis-rewritten by Netlify's link post-processing, which doesn't
    // understand this page's <base href="../"> tag.
    const href = `/${meta.urlPrefix ? `${meta.urlPrefix}/` : ''}index.html`;
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

  // Card image alts run before the text tables: some alts contain area
  // names that those tables rewrite, which would stop the full-alt match
  // from ever firing.
  for (const [find, replace] of projectCardAltReplacements(locale)) {
    html = html.split(find).join(replace);
  }

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

  // Cinematic-presentation viewer's per-project scene captions/labels
  html = applyViewingBlocks(html, locale);

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
  html = localizeInternalLinks(html, locale);
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
