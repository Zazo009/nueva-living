import { CARD_CHROME_ENTRIES } from './card_chrome_translations.mjs';

// Translations for developments.html's own hand-authored page copy,
// applied by build_developments_locales.mjs as literal find/replace over
// the rendered English page (same proven pattern as the homepage's
// HOMEPAGE_CONTENT_ENTRIES). Entries missing a locale keep English.
//
// data-filter attribute VALUES are matching keys used by
// liora-discovery.js against each card's data-tags -- they must stay
// English. Only visible label text between > < is translated.

// Filter-pill labels and card tag chips share one vocabulary. Place-name
// style tags (Golden Mile, Rio Real, Estepona, ...) intentionally have no
// entry: the site-wide convention keeps proper-noun area labels as-is.
export const TAG_LABELS = {
  'Sea View': { es: 'Vistas al Mar', fr: 'Vue Mer', de: 'Meerblick', ru: 'Вид на Море', ar: 'إطلالة على البحر' },
  'Beachside': { es: 'Junto a la Playa', fr: 'Bord de Mer', de: 'Strandnähe', ru: 'У Пляжа', ar: 'بجوار الشاطئ' },
  'Golf Living': { es: 'Vida de Golf', fr: 'Vie Golf', de: 'Golf-Wohnen', ru: 'Гольф-Резиденции', ar: 'حياة الغولف' },
  'Wellness Living': { es: 'Bienestar', fr: 'Bien-Être', de: 'Wellness-Wohnen', ru: 'Wellness-Образ Жизни', ar: 'حياة العافية' },
  'Resort Lifestyle': { es: 'Estilo Resort', fr: 'Esprit Resort', de: 'Resort-Lebensstil', ru: 'Курортный Стиль Жизни', ar: 'نمط حياة المنتجعات' },
  'Family-Oriented': { es: 'Ideal para Familias', fr: 'Familial', de: 'Familienfreundlich', ru: 'Для Семьи', ar: 'مناسب للعائلات' },
  'Privacy &amp; Security': { es: 'Privacidad y Seguridad', fr: 'Intimité et Sécurité', de: 'Privatsphäre & Sicherheit', ru: 'Приватность и Безопасность', ar: 'الخصوصية والأمان' },
  'Walkable Lifestyle': { es: 'Todo a Pie', fr: 'Tout à Pied', de: 'Alles zu Fuß Erreichbar', ru: 'Всё в Шаговой Доступности', ar: 'كل شيء سيرًا على الأقدام' },
  'Lock-and-Leave': { es: 'Cierra y Vete', fr: 'Clé en Main', de: 'Abschließen & Verreisen', ru: 'Закрыл и Уехал', ar: 'أغلق وغادر' },
  'Smart Home': { es: 'Hogar Inteligente', fr: 'Maison Connectée', de: 'Smart Home', ru: 'Умный Дом', ar: 'منزل ذكي' },
  'Sustainable Living': { es: 'Vida Sostenible', fr: 'Habitat Durable', de: 'Nachhaltiges Wohnen', ru: 'Экологичная Жизнь', ar: 'حياة مستدامة' },
  'Design-Led': { es: 'Diseño de Autor', fr: 'Design Signature', de: 'Designorientiert', ru: 'Дизайнерский Подход', ar: 'تصميم متميز' },
  'Ultra Luxury': { es: 'Ultra Lujo', fr: 'Ultra Luxe', de: 'Ultra-Luxus', ru: 'Ультра-Люкс', ar: 'فخامة قصوى' },
  'Boutique Community': { es: 'Comunidad Boutique', fr: 'Communauté Boutique', de: 'Boutique-Wohnanlage', ru: 'Бутик-Комьюнити', ar: 'مجتمع بوتيكي' },
  'Contemporary Mediterranean': { es: 'Mediterráneo Contemporáneo', fr: 'Méditerranéen Contemporain', de: 'Zeitgenössisch Mediterran', ru: 'Современный Средиземноморский', ar: 'متوسطي معاصر' },
  'Minimalist Architecture': { es: 'Arquitectura Minimalista', fr: 'Architecture Minimaliste', de: 'Minimalistische Architektur', ru: 'Минималистичная Архитектура', ar: 'عمارة بسيطة' },
  'Organic Design': { es: 'Diseño Orgánico', fr: 'Design Organique', de: 'Organisches Design', ru: 'Органичный Дизайн', ar: 'تصميم عضوي' },
  'Panoramic Glass Design': { es: 'Diseño Acristalado Panorámico', fr: 'Design Vitré Panoramique', de: 'Panorama-Glasdesign', ru: 'Панорамное Остекление', ar: 'تصميم زجاجي بانورامي' },
  'Low-Density Development': { es: 'Promoción de Baja Densidad', fr: 'Programme à Faible Densité', de: 'Bebauung mit Geringer Dichte', ru: 'Малоэтажная Застройка', ar: 'مشروع منخفض الكثافة' },
  'Boutique Development': { es: 'Promoción Boutique', fr: 'Programme Boutique', de: 'Boutique-Projekt', ru: 'Бутик-Проект', ar: 'مشروع بوتيكي' },
  'Beachfront': { es: 'Primera Línea de Playa', fr: 'Front de Mer', de: 'Direkt am Strand', ru: 'Первая Линия', ar: 'واجهة بحرية' },
  'Hillside Views': { es: 'Vistas desde la Ladera', fr: 'Vues sur les Collines', de: 'Hanglage mit Aussicht', ru: 'Вид с Холма', ar: 'إطلالات التلال' },
  'Gated Community': { es: 'Urbanización Cerrada', fr: 'Résidence Fermée', de: 'Bewachte Wohnanlage', ru: 'Закрытая Резиденция', ar: 'مجمع مسور' },
  'Walkable to Amenities': { es: 'Servicios a Pie', fr: 'Commodités à Pied', de: 'Alles Fußläufig', ru: 'Инфраструктура Рядом', ar: 'خدمات قريبة سيرًا' },
  'Primary Residence': { es: 'Vivienda Habitual', fr: 'Résidence Principale', de: 'Hauptwohnsitz', ru: 'Основное Жильё', ar: 'سكن رئيسي' },
  'Holiday Home': { es: 'Casa de Vacaciones', fr: 'Résidence de Vacances', de: 'Ferienhaus', ru: 'Дом для Отдыха', ar: 'منزل عطلات' },
  'Investment Property': { es: 'Propiedad de Inversión', fr: 'Bien d’Investissement', de: 'Anlageimmobilie', ru: 'Инвестиционная Недвижимость', ar: 'عقار استثماري' },
  'Rental Yield Potential': { es: 'Potencial de Rentabilidad', fr: 'Potentiel Locatif', de: 'Mietrendite-Potenzial', ru: 'Потенциал Арендной Доходности', ar: 'إمكانات عائد الإيجار' },
  'Family Relocation': { es: 'Traslado en Familia', fr: 'Installation en Famille', de: 'Familienumzug', ru: 'Переезд с Семьёй', ar: 'انتقال عائلي' },
  'International Buyer': { es: 'Comprador Internacional', fr: 'Acheteur International', de: 'Internationaler Käufer', ru: 'Международный Покупатель', ar: 'مشترٍ دولي' },
  'Second Home': { es: 'Segunda Residencia', fr: 'Résidence Secondaire', de: 'Zweitwohnsitz', ru: 'Второй Дом', ar: 'منزل ثانٍ' },
  'Lifestyle Investment': { es: 'Inversión en Estilo de Vida', fr: 'Investissement Style de Vie', de: 'Lifestyle-Investment', ru: 'Инвестиция в Образ Жизни', ar: 'استثمار في نمط الحياة' },
  'Long-Term Value': { es: 'Valor a Largo Plazo', fr: 'Valeur à Long Terme', de: 'Langfristiger Wert', ru: 'Долгосрочная Ценность', ar: 'قيمة طويلة الأمد' },
  'Low-Maintenance Ownership': { es: 'Mantenimiento Mínimo', fr: 'Entretien Minimal', de: 'Pflegeleichtes Eigentum', ru: 'Минимум Обслуживания', ar: 'ملكية سهلة الصيانة' },
  // Card-chip-only vocabulary
  'Off-Plan': { es: 'Sobre Plano', fr: 'Sur Plan', de: 'Off-Plan', ru: 'На Этапе Строительства', ar: 'على المخطط' },
  'Completed': { es: 'Finalizado', fr: 'Terminé', de: 'Fertiggestellt', ru: 'Завершено', ar: 'مكتمل' },
  'Resort Amenities': { es: 'Servicios de Resort', fr: 'Prestations Resort', de: 'Resort-Ausstattung', ru: 'Курортная Инфраструктура', ar: 'مرافق المنتجع' },
  'Resort access': { es: 'Acceso a resort', fr: 'Accès resort', de: 'Resort-Zugang', ru: 'Доступ к курорту', ar: 'وصول إلى المنتجع' },
  'Large terraces': { es: 'Terrazas amplias', fr: 'Grandes terrasses', de: 'Große Terrassen', ru: 'Просторные террасы', ar: 'شرفات واسعة' },
  'Private Rooftop Pool': { es: 'Piscina Privada en Azotea', fr: 'Piscine Privée sur le Toit', de: 'Privater Dachpool', ru: 'Частный Бассейн на Крыше', ar: 'مسبح خاص على السطح' },
  'Rooftop Pool': { es: 'Piscina en Azotea', fr: 'Piscine sur le Toit', de: 'Dachpool', ru: 'Бассейн на Крыше', ar: 'مسبح على السطح' },
  'Walk to Beach': { es: 'Playa a Pie', fr: 'Plage à Pied', de: 'Strand zu Fuß', ru: 'Пляж Пешком', ar: 'الشاطئ سيرًا' },
  'Smart Living': { es: 'Vida Inteligente', fr: 'Habitat Connecté', de: 'Smartes Wohnen', ru: 'Умные Технологии', ar: 'حياة ذكية' },
  'Sky bar': { es: 'Sky bar', fr: 'Sky bar', de: 'Sky-Bar', ru: 'Скай-бар', ar: 'سكاي بار' },
  'Golf simulator': { es: 'Simulador de golf', fr: 'Simulateur de golf', de: 'Golfsimulator', ru: 'Гольф-симулятор', ar: 'محاكي غولف' },
  'Co-Working': { es: 'Coworking', fr: 'Coworking', de: 'Co-Working', ru: 'Коворкинг', ar: 'مساحة عمل مشتركة' },
  'Gym': { es: 'Gimnasio', fr: 'Salle de Sport', de: 'Fitnessstudio', ru: 'Тренажёрный Зал', ar: 'صالة رياضية' },
  'Indoor Spa': { es: 'Spa Interior', fr: 'Spa Intérieur', de: 'Indoor-Spa', ru: 'Крытый Спа', ar: 'سبا داخلي' },
  'Private Pool Penthouses': { es: 'Áticos con Piscina Privada', fr: 'Penthouses avec Piscine Privée', de: 'Penthäuser mit Privatpool', ru: 'Пентхаусы с Бассейном', ar: 'بنتهاوس بمسبح خاص' },
  'Private Spa': { es: 'Spa Privado', fr: 'Spa Privé', de: 'Privates Spa', ru: 'Частный Спа', ar: 'سبا خاص' },
  'Cinema &amp; Coworking': { es: 'Cine y Coworking', fr: 'Cinéma et Coworking', de: 'Kino & Co-Working', ru: 'Кинозал и Коворкинг', ar: 'سينما ومساحة عمل' },
  'Boutique Collection': { es: 'Colección Boutique', fr: 'Collection Boutique', de: 'Boutique-Kollektion', ru: 'Бутик-Коллекция', ar: 'مجموعة بوتيكية' },
  'Private Pool': { es: 'Piscina Privada', fr: 'Piscine Privée', de: 'Privater Pool', ru: 'Частный Бассейн', ar: 'مسبح خاص' },
  'Entertaining': { es: 'Para Recibir', fr: 'Recevoir', de: 'Gastfreundschaft', ru: 'Для Приёмов', ar: 'الاستضافة' },
  'Contemporary': { es: 'Contemporáneo', fr: 'Contemporain', de: 'Zeitgenössisch', ru: 'Современный Стиль', ar: 'معاصر' },
  'Double-Height Living': { es: 'Salón a Doble Altura', fr: 'Séjour Double Hauteur', de: 'Wohnen in Doppelhöhe', ru: 'Двусветная Гостиная', ar: 'معيشة مزدوجة الارتفاع' },
  'Rooftop Solarium': { es: 'Solárium en Azotea', fr: 'Solarium en Toiture', de: 'Dachsolarium', ru: 'Солярий на Крыше', ar: 'سطح شمسي' },
  'Walk to Puerto Banús': { es: 'A Pie a Puerto Banús', fr: 'À Pied de Puerto Banús', de: 'Zu Fuß nach Puerto Banús', ru: 'Пешком до Пуэрто-Бануса', ar: 'سيرًا إلى بويرتو بانوس' },
  'Insurance-Backed Payments': { es: 'Pagos Avalados por Seguro', fr: 'Paiements Assurés', de: 'Versicherte Zahlungen', ru: 'Платежи под Страховкой', ar: 'دفعات مضمونة بالتأمين' },
  'Staged Payment Plan': { es: 'Pago Escalonado', fr: 'Paiement Échelonné', de: 'Gestaffelter Zahlungsplan', ru: 'Поэтапная Оплата', ar: 'خطة دفع مرحلية' },
  'Lift': { es: 'Ascensor', fr: 'Ascenseur', de: 'Aufzug', ru: 'Лифт', ar: 'مصعد' },
  'EV Charging': { es: 'Carga para Vehículo Eléctrico', fr: 'Recharge Véhicule Électrique', de: 'E-Auto-Ladestation', ru: 'Зарядка Электромобиля', ar: 'شاحن سيارات كهربائية' },
  'Flex Living': { es: 'Flex Living', fr: 'Flex Living', de: 'Flex Living', ru: 'Гибкое Владение', ar: 'سكن مرن' }
};

const PAGE_ENTRIES_HEAD = [
  // Head
  { find: '<title>Costa del Sol New Developments | Nueva Living</title>', es: '<title>Obra Nueva en la Costa del Sol | Nueva Living</title>', fr: '<title>Programmes Neufs sur la Costa del Sol | Nueva Living</title>', de: '<title>Neubauprojekte an der Costa del Sol | Nueva Living</title>', ru: '<title>Новостройки на Коста-дель-Соль | Nueva Living</title>', ar: '<title>مشاريع جديدة في كوستا ديل سول | Nueva Living</title>' },
  { find: 'Explore new developments across the Costa del Sol, chosen for their design, location and everyday appeal.', es: 'Descubre promociones de obra nueva en toda la Costa del Sol, seleccionadas por su diseño, ubicación y atractivo para el día a día.', fr: 'Découvrez des programmes neufs sur toute la Costa del Sol, choisis pour leur design, leur emplacement et leur agrément au quotidien.', de: 'Entdecken Sie Neubauprojekte an der gesamten Costa del Sol, ausgewählt nach Design, Lage und Alltagstauglichkeit.', ru: 'Изучите новостройки по всему побережью Коста-дель-Соль, отобранные за дизайн, расположение и удобство для жизни.', ar: 'استكشف مشاريع جديدة في جميع أنحاء كوستا ديل سول، مختارة لتصميمها وموقعها وملاءمتها للحياة اليومية.' },
  { find: '<meta property="og:title" content="Costa del Sol New Developments | Nueva Living">', es: '<meta property="og:title" content="Obra Nueva en la Costa del Sol | Nueva Living">', fr: '<meta property="og:title" content="Programmes Neufs sur la Costa del Sol | Nueva Living">', de: '<meta property="og:title" content="Neubauprojekte an der Costa del Sol | Nueva Living">', ru: '<meta property="og:title" content="Новостройки на Коста-дель-Соль | Nueva Living">', ar: '<meta property="og:title" content="مشاريع جديدة في كوستا ديل سول | Nueva Living">' },
  { find: '<meta name="twitter:title" content="Costa del Sol New Developments | Nueva Living">', es: '<meta name="twitter:title" content="Obra Nueva en la Costa del Sol | Nueva Living">', fr: '<meta name="twitter:title" content="Programmes Neufs sur la Costa del Sol | Nueva Living">', de: '<meta name="twitter:title" content="Neubauprojekte an der Costa del Sol | Nueva Living">', ru: '<meta name="twitter:title" content="Новостройки на Коста-дель-Соль | Nueva Living">', ar: '<meta name="twitter:title" content="مشاريع جديدة في كوستا ديل سول | Nueva Living">' },

  // Breadcrumb
  { find: '<li><a href="index.html">Home</a></li>', es: '<li><a href="index.html">Inicio</a></li>', fr: '<li><a href="index.html">Accueil</a></li>', de: '<li><a href="index.html">Startseite</a></li>', ru: '<li><a href="index.html">Главная</a></li>', ar: '<li><a href="index.html">الرئيسية</a></li>' },
  { find: '<li><span aria-current="page">Developments</span></li>', es: '<li><span aria-current="page">Promociones</span></li>', fr: '<li><span aria-current="page">Programmes</span></li>', de: '<li><span aria-current="page">Neubauprojekte</span></li>', ru: '<li><span aria-current="page">Новостройки</span></li>', ar: '<li><span aria-current="page">المشاريع</span></li>' },

  // Hero
  { find: '<span class="kicker">Selected Developments</span>', es: '<span class="kicker">Promociones Seleccionadas</span>', fr: '<span class="kicker">Programmes Sélectionnés</span>', de: '<span class="kicker">Ausgewählte Neubauprojekte</span>', ru: '<span class="kicker">Избранные Новостройки</span>', ar: '<span class="kicker">مشاريع مختارة</span>' },
  { find: 'Luxury properties for sale on the <em>Costa del Sol</em>', es: 'Propiedades de lujo en venta en la <em>Costa del Sol</em>', fr: 'Propriétés de luxe à vendre sur la <em>Costa del Sol</em>', de: 'Luxusimmobilien zum Verkauf an der <em>Costa del Sol</em>', ru: 'Элитная недвижимость на продажу на <em>Коста-дель-Соль</em>', ar: 'عقارات فاخرة للبيع في <em>كوستا ديل سول</em>' },
  { find: 'Find your ideal home on the Costa del Sol with our advanced property search. Browse a carefully selected collection of new developments and luxury residences, and filter by location, price, property type and more to discover the home that perfectly matches your lifestyle.', es: 'Encuentra tu vivienda ideal en la Costa del Sol con nuestro buscador avanzado. Explora una colección cuidadosamente seleccionada de obra nueva y residencias de lujo, y filtra por ubicación, precio, tipo de propiedad y más para descubrir el hogar que encaja perfectamente con tu estilo de vida.', fr: 'Trouvez votre logement idéal sur la Costa del Sol grâce à notre recherche avancée. Parcourez une collection soigneusement sélectionnée de programmes neufs et de résidences de luxe, et filtrez par emplacement, prix, type de bien et plus encore pour découvrir la maison qui correspond parfaitement à votre style de vie.', de: 'Finden Sie Ihr ideales Zuhause an der Costa del Sol mit unserer erweiterten Immobiliensuche. Durchstöbern Sie eine sorgfältig ausgewählte Kollektion von Neubauprojekten und Luxusresidenzen und filtern Sie nach Lage, Preis, Immobilientyp und mehr, um das Zuhause zu entdecken, das perfekt zu Ihrem Lebensstil passt.', ru: 'Найдите идеальный дом на Коста-дель-Соль с помощью нашего расширенного поиска. Просмотрите тщательно отобранную коллекцию новостроек и элитных резиденций и отфильтруйте по расположению, цене, типу недвижимости и другим параметрам, чтобы найти дом, идеально соответствующий вашему образу жизни.', ar: 'اعثر على منزلك المثالي في كوستا ديل سول من خلال بحثنا المتقدم عن العقارات. تصفح مجموعة مختارة بعناية من المشاريع الجديدة والمساكن الفاخرة، وقم بالتصفية حسب الموقع والسعر ونوع العقار والمزيد لاكتشاف المنزل الذي يناسب نمط حياتك تمامًا.' },
  { find: 'aria-controls="devHeroLead">Read More</button>', es: 'aria-controls="devHeroLead">Leer Más</button>', fr: 'aria-controls="devHeroLead">Lire Plus</button>', de: 'aria-controls="devHeroLead">Mehr Lesen</button>', ru: 'aria-controls="devHeroLead">Читать Далее</button>', ar: 'aria-controls="devHeroLead">اقرأ المزيد</button>' },
  { find: '>Explore Developments</a>', es: '>Ver Promociones</a>', fr: '>Découvrir les Programmes</a>', de: '>Neubauprojekte Entdecken</a>', ru: '>Смотреть Новостройки</a>', ar: '>استكشاف المشاريع</a>' },
  // Inline hero-lead toggle script literals
  { find: "heroLeadToggle.textContent = expanded ? 'Read Less' : 'Read More';", es: "heroLeadToggle.textContent = expanded ? 'Leer Menos' : 'Leer Más';", fr: "heroLeadToggle.textContent = expanded ? 'Lire Moins' : 'Lire Plus';", de: "heroLeadToggle.textContent = expanded ? 'Weniger Lesen' : 'Mehr Lesen';", ru: "heroLeadToggle.textContent = expanded ? 'Свернуть' : 'Читать Далее';", ar: "heroLeadToggle.textContent = expanded ? 'اقرأ أقل' : 'اقرأ المزيد';" },

  // View tabs
  { find: 'aria-label="Developments view"', es: 'aria-label="Vista de promociones"', fr: 'aria-label="Vue des programmes"', de: 'aria-label="Projektansicht"', ru: 'aria-label="Вид списка новостроек"', ar: 'aria-label="عرض المشاريع"' },
  { find: 'data-view-tab="current" role="tab" aria-selected="true">Current Developments</button>', es: 'data-view-tab="current" role="tab" aria-selected="true">Promociones Actuales</button>', fr: 'data-view-tab="current" role="tab" aria-selected="true">Programmes Actuels</button>', de: 'data-view-tab="current" role="tab" aria-selected="true">Aktuelle Projekte</button>', ru: 'data-view-tab="current" role="tab" aria-selected="true">Текущие Новостройки</button>', ar: 'data-view-tab="current" role="tab" aria-selected="true">المشاريع الحالية</button>' },
  { find: 'data-view-tab="archived" role="tab" aria-selected="false">Earlier Sold Projects</button>', es: 'data-view-tab="archived" role="tab" aria-selected="false">Proyectos Ya Vendidos</button>', fr: 'data-view-tab="archived" role="tab" aria-selected="false">Projets Déjà Vendus</button>', de: 'data-view-tab="archived" role="tab" aria-selected="false">Bereits Verkaufte Projekte</button>', ru: 'data-view-tab="archived" role="tab" aria-selected="false">Ранее Проданные Проекты</button>', ar: 'data-view-tab="archived" role="tab" aria-selected="false">مشاريع بيعت سابقًا</button>' },
  { find: 'aria-label="Development discovery filters"', es: 'aria-label="Filtros de búsqueda de promociones"', fr: 'aria-label="Filtres de recherche de programmes"', de: 'aria-label="Filter für die Projektsuche"', ru: 'aria-label="Фильтры поиска новостроек"', ar: 'aria-label="عوامل تصفية البحث عن المشاريع"' },

  // AI search
  { find: ">Describe the home you're looking for</label>", es: '>Describe la vivienda que buscas</label>', fr: '>Décrivez le bien que vous recherchez</label>', de: '>Beschreiben Sie das Zuhause, das Sie suchen</label>', ru: '>Опишите дом, который вы ищете</label>', ar: '>صف المنزل الذي تبحث عنه</label>' },
  { find: 'placeholder="Use our AI assistant to find what you are looking for"', es: 'placeholder="Usa nuestro asistente de IA para encontrar lo que buscas"', fr: 'placeholder="Utilisez notre assistant IA pour trouver ce que vous cherchez"', de: 'placeholder="Nutzen Sie unseren KI-Assistenten, um zu finden, was Sie suchen"', ru: 'placeholder="Используйте нашего ИИ-ассистента, чтобы найти то, что вы ищете"', ar: 'placeholder="استخدم مساعد الذكاء الاصطناعي للعثور على ما تبحث عنه"' },
  { find: '<span data-ai-search-submit-label>Search</span>', es: '<span data-ai-search-submit-label>Buscar</span>', fr: '<span data-ai-search-submit-label>Rechercher</span>', de: '<span data-ai-search-submit-label>Suchen</span>', ru: '<span data-ai-search-submit-label>Найти</span>', ar: '<span data-ai-search-submit-label>بحث</span>' },
  { find: 'data-ai-search-example>Beachfront villa near Puerto Ban&uacute;s</button>', es: 'data-ai-search-example>Villa en primera línea cerca de Puerto Banús</button>', fr: 'data-ai-search-example>Villa en front de mer près de Puerto Banús</button>', de: 'data-ai-search-example>Strandvilla nahe Puerto Banús</button>', ru: 'data-ai-search-example>Вилла у моря рядом с Пуэрто-Банус</button>', ar: 'data-ai-search-example>فيلا على الشاطئ قرب بويرتو بانوس</button>' },
  { find: 'data-ai-search-example>Golf-front penthouse, 2 bedrooms</button>', es: 'data-ai-search-example>Ático frente al golf, 2 dormitorios</button>', fr: 'data-ai-search-example>Penthouse face au golf, 2 chambres</button>', de: 'data-ai-search-example>Penthouse am Golfplatz, 2 Schlafzimmer</button>', ru: 'data-ai-search-example>Пентхаус у гольф-поля, 2 спальни</button>', ar: 'data-ai-search-example>بنتهاوس مطل على الغولف، غرفتا نوم</button>' },
  { find: 'data-ai-search-example>Family home under &euro;1.5M, ready now</button>', es: 'data-ai-search-example>Vivienda familiar por menos de 1,5M€, lista para entrar</button>', fr: 'data-ai-search-example>Maison familiale sous 1,5M€, disponible maintenant</button>', de: 'data-ai-search-example>Familienhaus unter 1,5M€, sofort bezugsfertig</button>', ru: 'data-ai-search-example>Семейный дом до 1,5 млн €, готов к заселению</button>', ar: 'data-ai-search-example>منزل عائلي بأقل من 1.5 مليون يورو، جاهز الآن</button>' },
  { find: 'data-ai-search-category data-ai-search-example>&#127958;&#65039; Beach</button>', es: 'data-ai-search-category data-ai-search-example>&#127958;&#65039; Playa</button>', fr: 'data-ai-search-category data-ai-search-example>&#127958;&#65039; Plage</button>', de: 'data-ai-search-category data-ai-search-example>&#127958;&#65039; Strand</button>', ru: 'data-ai-search-category data-ai-search-example>&#127958;&#65039; Пляж</button>', ar: 'data-ai-search-category data-ai-search-example>&#127958;&#65039; شاطئ</button>' },
  { find: 'data-ai-search-category data-ai-search-example>&#9971;&#65039; Golf</button>', es: 'data-ai-search-category data-ai-search-example>&#9971;&#65039; Golf</button>', fr: 'data-ai-search-category data-ai-search-example>&#9971;&#65039; Golf</button>', de: 'data-ai-search-category data-ai-search-example>&#9971;&#65039; Golf</button>', ru: 'data-ai-search-category data-ai-search-example>&#9971;&#65039; Гольф</button>', ar: 'data-ai-search-category data-ai-search-example>&#9971;&#65039; غولف</button>' },
  { find: 'data-ai-search-category data-ai-search-example>&#127961;&#65039; Family</button>', es: 'data-ai-search-category data-ai-search-example>&#127961;&#65039; Familia</button>', fr: 'data-ai-search-category data-ai-search-example>&#127961;&#65039; Famille</button>', de: 'data-ai-search-category data-ai-search-example>&#127961;&#65039; Familie</button>', ru: 'data-ai-search-category data-ai-search-example>&#127961;&#65039; Семья</button>', ar: 'data-ai-search-category data-ai-search-example>&#127961;&#65039; عائلة</button>' },
  { find: 'data-ai-search-category data-ai-search-example>&#128176; Investment</button>', es: 'data-ai-search-category data-ai-search-example>&#128176; Inversión</button>', fr: 'data-ai-search-category data-ai-search-example>&#128176; Investissement</button>', de: 'data-ai-search-category data-ai-search-example>&#128176; Investment</button>', ru: 'data-ai-search-category data-ai-search-example>&#128176; Инвестиции</button>', ar: 'data-ai-search-category data-ai-search-example>&#128176; استثمار</button>' },

  // Primary filters
  { find: '<span>Location</span>', es: '<span>Ubicación</span>', fr: '<span>Emplacement</span>', de: '<span>Lage</span>', ru: '<span>Расположение</span>', ar: '<span>الموقع</span>' },
  { find: '<option value="">All Locations</option>', es: '<option value="">Todas las Ubicaciones</option>', fr: '<option value="">Tous les Emplacements</option>', de: '<option value="">Alle Lagen</option>', ru: '<option value="">Все Районы</option>', ar: '<option value="">جميع المواقع</option>' },
  { find: '<span>Property Type</span>', es: '<span>Tipo de Propiedad</span>', fr: '<span>Type de Bien</span>', de: '<span>Immobilientyp</span>', ru: '<span>Тип Недвижимости</span>', ar: '<span>نوع العقار</span>' },
  { find: '<option value="">All Types</option>', es: '<option value="">Todos los Tipos</option>', fr: '<option value="">Tous les Types</option>', de: '<option value="">Alle Typen</option>', ru: '<option value="">Все Типы</option>', ar: '<option value="">جميع الأنواع</option>' },
  { find: '<option value="apartment">Apartment</option>', es: '<option value="apartment">Apartamento</option>', fr: '<option value="apartment">Appartement</option>', de: '<option value="apartment">Wohnung</option>', ru: '<option value="apartment">Апартаменты</option>', ar: '<option value="apartment">شقة</option>' },
  { find: '<option value="penthouse">Penthouse</option>', es: '<option value="penthouse">Ático</option>', fr: '<option value="penthouse">Penthouse</option>', de: '<option value="penthouse">Penthouse</option>', ru: '<option value="penthouse">Пентхаус</option>', ar: '<option value="penthouse">بنتهاوس</option>' },
  { find: '<option value="villa">Villa</option>', es: '<option value="villa">Villa</option>', fr: '<option value="villa">Villa</option>', de: '<option value="villa">Villa</option>', ru: '<option value="villa">Вилла</option>', ar: '<option value="villa">فيلا</option>' },
  { find: '<option value="townhouse">Townhouse</option>', es: '<option value="townhouse">Adosado</option>', fr: '<option value="townhouse">Maison de Ville</option>', de: '<option value="townhouse">Reihenhaus</option>', ru: '<option value="townhouse">Таунхаус</option>', ar: '<option value="townhouse">تاون هاوس</option>' },
  { find: '<span>Status</span>', es: '<span>Estado</span>', fr: '<span>Statut</span>', de: '<span>Status</span>', ru: '<span>Статус</span>', ar: '<span>الحالة</span>' },
  { find: '<option value="">Any Status</option>', es: '<option value="">Cualquier Estado</option>', fr: '<option value="">Tout Statut</option>', de: '<option value="">Jeder Status</option>', ru: '<option value="">Любой Статус</option>', ar: '<option value="">أي حالة</option>' },
  { find: '<option value="off_plan">Off-Plan</option>', es: '<option value="off_plan">Sobre Plano</option>', fr: '<option value="off_plan">Sur Plan</option>', de: '<option value="off_plan">Off-Plan</option>', ru: '<option value="off_plan">На Этапе Строительства</option>', ar: '<option value="off_plan">على المخطط</option>' },
  { find: '<option value="under_construction">Under Construction</option>', es: '<option value="under_construction">En Construcción</option>', fr: '<option value="under_construction">En Construction</option>', de: '<option value="under_construction">Im Bau</option>', ru: '<option value="under_construction">Строится</option>', ar: '<option value="under_construction">قيد الإنشاء</option>' },
  { find: '<option value="completed">Completed</option>', es: '<option value="completed">Finalizado</option>', fr: '<option value="completed">Terminé</option>', de: '<option value="completed">Fertiggestellt</option>', ru: '<option value="completed">Завершено</option>', ar: '<option value="completed">مكتمل</option>' },
  { find: '<span>Move-in Timing</span>', es: '<span>Plazo de Entrada</span>', fr: '<span>Délai d’Emménagement</span>', de: '<span>Einzugstermin</span>', ru: '<span>Срок Заселения</span>', ar: '<span>موعد الانتقال</span>' },
  { find: '<option value="">Any Timing</option>', es: '<option value="">Cualquier Plazo</option>', fr: '<option value="">Tout Délai</option>', de: '<option value="">Jeder Zeitpunkt</option>', ru: '<option value="">Любой Срок</option>', ar: '<option value="">أي وقت</option>' },
  { find: '<option value="ready">Ready Now</option>', es: '<option value="ready">Listo para Entrar</option>', fr: '<option value="ready">Disponible Maintenant</option>', de: '<option value="ready">Sofort Bezugsfertig</option>', ru: '<option value="ready">Готово Сейчас</option>', ar: '<option value="ready">جاهز الآن</option>' },
  { find: '<option value="1y">Within 1 Year</option>', es: '<option value="1y">En 1 Año</option>', fr: '<option value="1y">Sous 1 An</option>', de: '<option value="1y">Innerhalb 1 Jahres</option>', ru: '<option value="1y">В Течение 1 Года</option>', ar: '<option value="1y">خلال سنة واحدة</option>' },
  { find: '<option value="2y">Within 2 Years</option>', es: '<option value="2y">En 2 Años</option>', fr: '<option value="2y">Sous 2 Ans</option>', de: '<option value="2y">Innerhalb von 2 Jahren</option>', ru: '<option value="2y">В Течение 2 Лет</option>', ar: '<option value="2y">خلال سنتين</option>' },
  { find: '<option value="2y+">2+ Years</option>', es: '<option value="2y+">Más de 2 Años</option>', fr: '<option value="2y+">Plus de 2 Ans</option>', de: '<option value="2y+">Über 2 Jahre</option>', ru: '<option value="2y+">Более 2 Лет</option>', ar: '<option value="2y+">أكثر من سنتين</option>' },
  { find: '<span>Price Range<em class="range-readout" data-range-readout>Any price</em></span>', es: '<span>Rango de Precio<em class="range-readout" data-range-readout>Cualquier precio</em></span>', fr: '<span>Fourchette de Prix<em class="range-readout" data-range-readout>Tout prix</em></span>', de: '<span>Preisspanne<em class="range-readout" data-range-readout>Jeder Preis</em></span>', ru: '<span>Диапазон Цен<em class="range-readout" data-range-readout>Любая цена</em></span>', ar: '<span>نطاق السعر<em class="range-readout" data-range-readout>أي سعر</em></span>' },
  { find: 'aria-label="Minimum price"', es: 'aria-label="Precio mínimo"', fr: 'aria-label="Prix minimum"', de: 'aria-label="Mindestpreis"', ru: 'aria-label="Минимальная цена"', ar: 'aria-label="الحد الأدنى للسعر"' },
  { find: 'aria-label="Maximum price"', es: 'aria-label="Precio máximo"', fr: 'aria-label="Prix maximum"', de: 'aria-label="Höchstpreis"', ru: 'aria-label="Максимальная цена"', ar: 'aria-label="الحد الأقصى للسعر"' },
  { find: '<span>Bedrooms<em class="range-readout" data-range-readout>Any</em></span>', es: '<span>Dormitorios<em class="range-readout" data-range-readout>Cualquiera</em></span>', fr: '<span>Chambres<em class="range-readout" data-range-readout>Toutes</em></span>', de: '<span>Schlafzimmer<em class="range-readout" data-range-readout>Beliebig</em></span>', ru: '<span>Спальни<em class="range-readout" data-range-readout>Любое число</em></span>', ar: '<span>غرف النوم<em class="range-readout" data-range-readout>أي عدد</em></span>' },
  { find: 'aria-label="Minimum bedrooms"', es: 'aria-label="Mínimo de dormitorios"', fr: 'aria-label="Nombre minimum de chambres"', de: 'aria-label="Minimale Schlafzimmeranzahl"', ru: 'aria-label="Минимум спален"', ar: 'aria-label="الحد الأدنى لغرف النوم"' },
  { find: 'aria-label="Maximum bedrooms"', es: 'aria-label="Máximo de dormitorios"', fr: 'aria-label="Nombre maximum de chambres"', de: 'aria-label="Maximale Schlafzimmeranzahl"', ru: 'aria-label="Максимум спален"', ar: 'aria-label="الحد الأقصى لغرف النوم"' },
  { find: '>Reset Filters</button>', es: '>Restablecer Filtros</button>', fr: '>Réinitialiser les Filtres</button>', de: '>Filter Zurücksetzen</button>', ru: '>Сбросить Фильтры</button>', ar: '>إعادة تعيين الفلاتر</button>' },

  // Lifestyle panel
  { find: '<span class="lifestyle-star" aria-hidden="true">&#10022;</span> Filter by Lifestyle</span>', es: '<span class="lifestyle-star" aria-hidden="true">&#10022;</span> Filtrar por Estilo de Vida</span>', fr: '<span class="lifestyle-star" aria-hidden="true">&#10022;</span> Filtrer par Style de Vie</span>', de: '<span class="lifestyle-star" aria-hidden="true">&#10022;</span> Nach Lebensstil Filtern</span>', ru: '<span class="lifestyle-star" aria-hidden="true">&#10022;</span> Фильтр по Образу Жизни</span>', ar: '<span class="lifestyle-star" aria-hidden="true">&#10022;</span> تصفية حسب نمط الحياة</span>' },
  { find: 'aria-label="Lifestyle filter mode"', es: 'aria-label="Modo de filtro de estilo de vida"', fr: 'aria-label="Mode de filtre style de vie"', de: 'aria-label="Lifestyle-Filtermodus"', ru: 'aria-label="Режим фильтра по образу жизни"', ar: 'aria-label="وضع تصفية نمط الحياة"' },
  { find: 'data-mode="lifestyle" aria-selected="true">Lifestyle</button>', es: 'data-mode="lifestyle" aria-selected="true">Estilo de Vida</button>', fr: 'data-mode="lifestyle" aria-selected="true">Style de Vie</button>', de: 'data-mode="lifestyle" aria-selected="true">Lebensstil</button>', ru: 'data-mode="lifestyle" aria-selected="true">Образ Жизни</button>', ar: 'data-mode="lifestyle" aria-selected="true">نمط الحياة</button>' },
  { find: 'data-mode="architecture" aria-selected="false">Architecture</button>', es: 'data-mode="architecture" aria-selected="false">Arquitectura</button>', fr: 'data-mode="architecture" aria-selected="false">Architecture</button>', de: 'data-mode="architecture" aria-selected="false">Architektur</button>', ru: 'data-mode="architecture" aria-selected="false">Архитектура</button>', ar: 'data-mode="architecture" aria-selected="false">العمارة</button>' },
  { find: 'data-mode="location" aria-selected="false">Setting</button>', es: 'data-mode="location" aria-selected="false">Entorno</button>', fr: 'data-mode="location" aria-selected="false">Cadre</button>', de: 'data-mode="location" aria-selected="false">Umgebung</button>', ru: 'data-mode="location" aria-selected="false">Окружение</button>', ar: 'data-mode="location" aria-selected="false">المحيط</button>' },
  { find: 'data-mode="investment" aria-selected="false">Investment</button>', es: 'data-mode="investment" aria-selected="false">Inversión</button>', fr: 'data-mode="investment" aria-selected="false">Investissement</button>', de: 'data-mode="investment" aria-selected="false">Investment</button>', ru: 'data-mode="investment" aria-selected="false">Инвестиции</button>', ar: 'data-mode="investment" aria-selected="false">الاستثمار</button>' },
  { find: '<span>No lifestyle filters selected</span>', es: '<span>Sin filtros de estilo de vida seleccionados</span>', fr: '<span>Aucun filtre de style de vie sélectionné</span>', de: '<span>Keine Lifestyle-Filter ausgewählt</span>', ru: '<span>Фильтры по образу жизни не выбраны</span>', ar: '<span>لم يتم اختيار فلاتر نمط الحياة</span>' },

  // Sort
  { find: '<span>Sort</span>', es: '<span>Ordenar</span>', fr: '<span>Trier</span>', de: '<span>Sortieren</span>', ru: '<span>Сортировка</span>', ar: '<span>ترتيب</span>' },
  { find: '<option value="curated">Recommended order</option>', es: '<option value="curated">Orden recomendado</option>', fr: '<option value="curated">Ordre recommandé</option>', de: '<option value="curated">Empfohlene Reihenfolge</option>', ru: '<option value="curated">Рекомендуемый порядок</option>', ar: '<option value="curated">الترتيب الموصى به</option>' },
  { find: '<option value="newest">Newest release</option>', es: '<option value="newest">Lanzamiento más reciente</option>', fr: '<option value="newest">Lancement le plus récent</option>', de: '<option value="newest">Neueste Veröffentlichung</option>', ru: '<option value="newest">Сначала новые</option>', ar: '<option value="newest">الأحدث إصدارًا</option>' },
  { find: '<option value="price-asc">Price: low to high</option>', es: '<option value="price-asc">Precio: de menor a mayor</option>', fr: '<option value="price-asc">Prix : croissant</option>', de: '<option value="price-asc">Preis: aufsteigend</option>', ru: '<option value="price-asc">Цена: по возрастанию</option>', ar: '<option value="price-asc">السعر: من الأقل إلى الأعلى</option>' },
  { find: '<option value="price-desc">Price: high to low</option>', es: '<option value="price-desc">Precio: de mayor a menor</option>', fr: '<option value="price-desc">Prix : décroissant</option>', de: '<option value="price-desc">Preis: absteigend</option>', ru: '<option value="price-desc">Цена: по убыванию</option>', ar: '<option value="price-desc">السعر: من الأعلى إلى الأقل</option>' },
  { find: '<option value="completion">Completion soonest</option>', es: '<option value="completion">Entrega más próxima</option>', fr: '<option value="completion">Livraison la plus proche</option>', de: '<option value="completion">Frühestes Fertigstellungsdatum</option>', ru: '<option value="completion">Ближайшая сдача</option>', ar: '<option value="completion">الأقرب إنجازًا</option>' },

  // Empty state
  { find: '<span>No exact match found.</span>', es: '<span>No se encontró ninguna coincidencia exacta.</span>', fr: '<span>Aucune correspondance exacte trouvée.</span>', de: '<span>Keine genaue Übereinstimmung gefunden.</span>', ru: '<span>Точных совпадений не найдено.</span>', ar: '<span>لم يتم العثور على تطابق دقيق.</span>' },
  { find: '<p>Try fewer filters, explore similar projects or tell us what you are looking for.</p>', es: '<p>Prueba con menos filtros, explora proyectos similares o cuéntanos qué buscas.</p>', fr: '<p>Essayez avec moins de filtres, explorez des projets similaires ou dites-nous ce que vous recherchez.</p>', de: '<p>Versuchen Sie es mit weniger Filtern, entdecken Sie ähnliche Projekte oder sagen Sie uns, wonach Sie suchen.</p>', ru: '<p>Попробуйте убрать часть фильтров, посмотрите похожие проекты или расскажите нам, что вы ищете.</p>', ar: '<p>جرّب عددًا أقل من الفلاتر، أو استكشف مشاريع مشابهة، أو أخبرنا بما تبحث عنه.</p>' },
  { find: '>Get a Personal Shortlist</a>', es: '>Solicita tu Lista Personalizada</a>', fr: '>Recevoir une Sélection Personnalisée</a>', de: '>Persönliche Auswahl Erhalten</a>', ru: '>Получить Персональную Подборку</a>', ar: '>احصل على قائمة مختارة شخصية</a>' },

  // Card meta labels + CTA (shared set lives in PROJECT_CARD_ENTRIES below;
  // merged into this page's entries at the bottom of this file)
];

// Project-card meta labels, meta values and CTA shared by every page that
// renders generated project cards (developments.html, segment pages).
export const PROJECT_CARD_ENTRIES = [
  ...CARD_CHROME_ENTRIES,
  { find: '<div><span>From</span><strong>', es: '<div><span>Desde</span><strong>', fr: '<div><span>À Partir de</span><strong>', de: '<div><span>Ab</span><strong>', ru: '<div><span>От</span><strong>', ar: '<div><span>ابتداءً من</span><strong>' },
  { find: '<div><span>Type</span><strong>', es: '<div><span>Tipo</span><strong>', fr: '<div><span>Type</span><strong>', de: '<div><span>Typ</span><strong>', ru: '<div><span>Тип</span><strong>', ar: '<div><span>النوع</span><strong>' },
  { find: '<div><span>Status</span><strong>', es: '<div><span>Estado</span><strong>', fr: '<div><span>Statut</span><strong>', de: '<div><span>Status</span><strong>', ru: '<div><span>Статус</span><strong>', ar: '<div><span>الحالة</span><strong>' },
  { find: '<div><span>Delivery</span><strong>', es: '<div><span>Entrega</span><strong>', fr: '<div><span>Livraison</span><strong>', de: '<div><span>Übergabe</span><strong>', ru: '<div><span>Сдача</span><strong>', ar: '<div><span>التسليم</span><strong>' },
  { find: '>Explore Project</a>', es: '>Explorar Proyecto</a>', fr: '>Découvrir le Projet</a>', de: '>Projekt Entdecken</a>', ru: '>Смотреть Проект</a>', ar: '>استكشاف المشروع</a>' },
  { find: 'aria-label="Previous image"', es: 'aria-label="Imagen anterior"', fr: 'aria-label="Image précédente"', de: 'aria-label="Vorheriges Bild"', ru: 'aria-label="Предыдущее изображение"', ar: 'aria-label="الصورة السابقة"' },
  { find: 'aria-label="Next image"', es: 'aria-label="Imagen siguiente"', fr: 'aria-label="Image suivante"', de: 'aria-label="Nächstes Bild"', ru: 'aria-label="Следующее изображение"', ar: 'aria-label="الصورة التالية"' },

  // Card meta type values (mirrors the homepage's dictionary)
  { find: '<strong>Apartments, Penthouses &amp; Villas</strong>', es: '<strong>Apartamentos, Áticos y Villas</strong>', fr: '<strong>Appartements, Penthouses et Villas</strong>', de: '<strong>Wohnungen, Penthäuser & Villen</strong>', ru: '<strong>Апартаменты, Пентхаусы и Виллы</strong>', ar: '<strong>شقق وبنتهاوس وفلل</strong>' },
  { find: '<strong>Semi-Detached Houses</strong>', es: '<strong>Casas Adosadas</strong>', fr: '<strong>Maisons Jumelées</strong>', de: '<strong>Doppelhaushälften</strong>', ru: '<strong>Дома на Две Семьи</strong>', ar: '<strong>منازل شبه منفصلة</strong>' },
  { find: '<strong>Penthouses &amp; Villas</strong>', es: '<strong>Áticos y Villas</strong>', fr: '<strong>Penthouses et Villas</strong>', de: '<strong>Penthäuser & Villen</strong>', ru: '<strong>Пентхаусы и Виллы</strong>', ar: '<strong>بنتهاوس وفلل</strong>' },
  { find: '<strong>Apartments &amp; Penthouses</strong>', es: '<strong>Apartamentos y Áticos</strong>', fr: '<strong>Appartements et Penthouses</strong>', de: '<strong>Wohnungen & Penthäuser</strong>', ru: '<strong>Апартаменты и Пентхаусы</strong>', ar: '<strong>شقق وبنتهاوس</strong>' },
  { find: '<strong>1-4 Bedroom Homes</strong>', es: '<strong>Viviendas de 1 a 4 Dormitorios</strong>', fr: '<strong>Logements de 1 à 4 Chambres</strong>', de: '<strong>Wohnungen mit 1–4 Schlafzimmern</strong>', ru: '<strong>Дома с 1–4 Спальнями</strong>', ar: '<strong>مساكن من غرفة إلى 4 غرف نوم</strong>' },
  { find: '<strong>Duplex Residences &amp; Penthouses</strong>', es: '<strong>Dúplex y Áticos</strong>', fr: '<strong>Duplex et Penthouses</strong>', de: '<strong>Duplex-Residenzen & Penthäuser</strong>', ru: '<strong>Дуплексы и Пентхаусы</strong>', ar: '<strong>دوبلكس وبنتهاوس</strong>' },
  { find: '<strong>Villas &amp; Apartments</strong>', es: '<strong>Villas y Apartamentos</strong>', fr: '<strong>Villas et Appartements</strong>', de: '<strong>Villen & Wohnungen</strong>', ru: '<strong>Виллы и Апартаменты</strong>', ar: '<strong>فلل وشقق</strong>' },
  { find: '<strong>Villas</strong>', es: '<strong>Villas</strong>', fr: '<strong>Villas</strong>', de: '<strong>Villen</strong>', ru: '<strong>Виллы</strong>', ar: '<strong>فلل</strong>' },
  // Card meta status values
  { find: '<strong>Off-Plan</strong>', es: '<strong>Sobre Plano</strong>', fr: '<strong>Sur Plan</strong>', de: '<strong>Off-Plan</strong>', ru: '<strong>На Этапе Строительства</strong>', ar: '<strong>على المخطط</strong>' },
  { find: '<strong>Off-plan</strong>', es: '<strong>Sobre plano</strong>', fr: '<strong>Sur plan</strong>', de: '<strong>Off-Plan</strong>', ru: '<strong>На этапе строительства</strong>', ar: '<strong>على المخطط</strong>' },
  { find: '<strong>Completed</strong>', es: '<strong>Finalizado</strong>', fr: '<strong>Terminé</strong>', de: '<strong>Fertiggestellt</strong>', ru: '<strong>Завершено</strong>', ar: '<strong>مكتمل</strong>' },
  { find: '<strong>Current release</strong>', es: '<strong>Fase actual</strong>', fr: '<strong>Phase actuelle</strong>', de: '<strong>Aktuelle Phase</strong>', ru: '<strong>Текущая очередь</strong>', ar: '<strong>المرحلة الحالية</strong>' },
  { find: '<strong>Under construction</strong>', es: '<strong>En construcción</strong>', fr: '<strong>En construction</strong>', de: '<strong>Im Bau</strong>', ru: '<strong>В стадии строительства</strong>', ar: '<strong>قيد الإنشاء</strong>' },
  { find: '<strong>Est. Q2 2029</strong>', es: '<strong>Est. T2 2029</strong>', fr: '<strong>Est. T2 2029</strong>', de: '<strong>Vsl. Q2 2029</strong>', ru: '<strong>Ориент. 2 кв. 2029</strong>', ar: '<strong>تقديريًا الربع الثاني 2029</strong>' },
];

const PAGE_ENTRIES_TAIL = [
  // Archived section
  { find: '<span class="label">Track Record</span>', es: '<span class="label">Trayectoria</span>', fr: '<span class="label">Historique</span>', de: '<span class="label">Erfolgsbilanz</span>', ru: '<span class="label">Наш Опыт</span>', ar: '<span class="label">سجل الإنجازات</span>' },
  { find: '<h2 class="section-title">Earlier <em>sold projects</em></h2>', es: '<h2 class="section-title">Proyectos <em>ya vendidos</em></h2>', fr: '<h2 class="section-title">Projets <em>déjà vendus</em></h2>', de: '<h2 class="section-title">Bereits <em>verkaufte Projekte</em></h2>', ru: '<h2 class="section-title">Ранее <em>проданные проекты</em></h2>', ar: '<h2 class="section-title">مشاريع <em>بيعت سابقًا</em></h2>' },
  { find: '<p class="body-copy">A look back at developments we have already sold out, kept here rather than removed so you can see our track record.</p>', es: '<p class="body-copy">Un repaso a las promociones que ya hemos vendido por completo, que mantenemos aquí en lugar de eliminarlas para que puedas ver nuestra trayectoria.</p>', fr: '<p class="body-copy">Un retour sur les programmes que nous avons déjà entièrement vendus, conservés ici plutôt que supprimés pour que vous puissiez voir notre historique.</p>', de: '<p class="body-copy">Ein Rückblick auf Projekte, die bereits vollständig verkauft sind — wir behalten sie hier, damit Sie unsere Erfolgsbilanz sehen können.</p>', ru: '<p class="body-copy">Обзор проектов, которые уже полностью распроданы, — мы сохраняем их здесь, чтобы вы могли оценить наш опыт.</p>', ar: '<p class="body-copy">نظرة على المشاريع التي بيعت بالكامل، نحتفظ بها هنا بدلًا من حذفها لتتمكن من الاطلاع على سجل إنجازاتنا.</p>' },
  { find: 'No earlier sold projects to show yet &mdash; check back soon.', es: 'Aún no hay proyectos vendidos que mostrar. Vuelve pronto.', fr: 'Aucun projet déjà vendu à afficher pour le moment — revenez bientôt.', de: 'Noch keine verkauften Projekte zu zeigen — schauen Sie bald wieder vorbei.', ru: 'Пока нет проданных проектов для показа — загляните позже.', ar: 'لا توجد مشاريع مباعة لعرضها بعد — عد قريبًا.' },

  // Before-you-view band
  { find: '<span class="label">Before You View</span>', es: '<span class="label">Antes de la Visita</span>', fr: '<span class="label">Avant Votre Visite</span>', de: '<span class="label">Vor der Besichtigung</span>', ru: '<span class="label">Перед Просмотром</span>', ar: '<span class="label">قبل المعاينة</span>' },
  { find: '<h2 class="section-title">What we check before <em>a viewing</em></h2>', es: '<h2 class="section-title">Qué comprobamos antes de <em>una visita</em></h2>', fr: '<h2 class="section-title">Ce que nous vérifions avant <em>une visite</em></h2>', de: '<h2 class="section-title">Was wir vor <em>einer Besichtigung</em> prüfen</h2>', ru: '<h2 class="section-title">Что мы проверяем перед <em>просмотром</em></h2>', ar: '<h2 class="section-title">ما نتحقق منه قبل <em>المعاينة</em></h2>' },
  { find: '<h3>Latest Prices &amp; Availability</h3>', es: '<h3>Precios y Disponibilidad Actualizados</h3>', fr: '<h3>Prix et Disponibilités à Jour</h3>', de: '<h3>Aktuelle Preise & Verfügbarkeit</h3>', ru: '<h3>Актуальные Цены и Наличие</h3>', ar: '<h3>أحدث الأسعار والتوافر</h3>' },
  { find: '<p>Which homes are available, their reservation status, current prices and expected delivery.</p>', es: '<p>Qué viviendas están disponibles, su estado de reserva, precios actuales y entrega prevista.</p>', fr: '<p>Quels logements sont disponibles, leur statut de réservation, les prix actuels et la livraison prévue.</p>', de: '<p>Welche Wohnungen verfügbar sind, ihr Reservierungsstatus, aktuelle Preise und die voraussichtliche Übergabe.</p>', ru: '<p>Какие объекты доступны, их статус резервирования, актуальные цены и ожидаемые сроки сдачи.</p>', ar: '<p>ما هي المساكن المتاحة، وحالة حجزها، والأسعار الحالية، وموعد التسليم المتوقع.</p>' },
  { find: '<h3>The Developer</h3>', es: '<h3>La Promotora</h3>', fr: '<h3>Le Promoteur</h3>', de: '<h3>Der Bauträger</h3>', ru: '<h3>Застройщик</h3>', ar: '<h3>المطور العقاري</h3>' },
  { find: '<p>Previous projects, warranties, specifications and comparable developments nearby.</p>', es: '<p>Proyectos anteriores, garantías, especificaciones y promociones comparables en la zona.</p>', fr: '<p>Projets antérieurs, garanties, spécifications et programmes comparables à proximité.</p>', de: '<p>Frühere Projekte, Garantien, Ausstattungsmerkmale und vergleichbare Projekte in der Nähe.</p>', ru: '<p>Предыдущие проекты, гарантии, спецификации и сопоставимые новостройки поблизости.</p>', ar: '<p>المشاريع السابقة والضمانات والمواصفات والمشاريع المماثلة القريبة.</p>' },
  { find: '<h3>The Location</h3>', es: '<h3>La Ubicación</h3>', fr: '<h3>L’Emplacement</h3>', de: '<h3>Die Lage</h3>', ru: '<h3>Расположение</h3>', ar: '<h3>الموقع</h3>' },
  { find: '<p>Access, nearby services, rental demand, resale appeal and how the area fits your plans.</p>', es: '<p>Accesos, servicios cercanos, demanda de alquiler, atractivo de reventa y cómo encaja la zona con tus planes.</p>', fr: '<p>Accès, services à proximité, demande locative, attrait à la revente et adéquation du secteur avec vos projets.</p>', de: '<p>Anbindung, nahegelegene Dienstleistungen, Mietnachfrage, Wiederverkaufsattraktivität und wie die Lage zu Ihren Plänen passt.</p>', ru: '<p>Транспортная доступность, инфраструктура рядом, спрос на аренду, привлекательность при перепродаже и соответствие района вашим планам.</p>', ar: '<p>سهولة الوصول والخدمات القريبة والطلب على الإيجار وجاذبية إعادة البيع ومدى ملاءمة المنطقة لخططك.</p>' },

  // CTA band
  { find: '<h2 class="cta-title">Ask for the latest project list and documents.</h2>', es: '<h2 class="cta-title">Solicita la lista de proyectos y documentación actualizada.</h2>', fr: '<h2 class="cta-title">Demandez la liste des projets et les documents à jour.</h2>', de: '<h2 class="cta-title">Fordern Sie die aktuelle Projektliste und Unterlagen an.</h2>', ru: '<h2 class="cta-title">Запросите актуальный список проектов и документы.</h2>', ar: '<h2 class="cta-title">اطلب أحدث قائمة للمشاريع والمستندات.</h2>' },
  { find: '>Get Project Information</a>', es: '>Solicitar Información</a>', fr: '>Obtenir des Informations</a>', de: '>Projektinformationen Anfordern</a>', ru: '>Получить Информацию</a>', ar: '>الحصول على معلومات المشروع</a>' },

];

// Nav, mobile menu and footer chrome shared by every hand-authored static
// page (developments.html, compare.html, thank-you.html, 404.html) whose
// locale variants are produced by clone-and-replace rather than a
// locale-aware render function.
export const CHROME_ENTRIES = [
  // Nav / mobile menu
  { find: '>Buying Guides</a>', es: '>Guías de Compra</a>', fr: '>Guides d’Achat</a>', de: '>Kaufratgeber</a>', ru: '>Покупателям</a>', ar: '>أدلة الشراء</a>' },
  { find: '>Why Nueva</a>', es: '>Por Qué Nueva</a>', fr: '>Pourquoi Nueva</a>', de: '>Warum Nueva</a>', ru: '>Почему Nueva</a>', ar: '>لماذا نويفا</a>' },
  { find: '>Developments</a>', es: '>Promociones</a>', fr: '>Programmes</a>', de: '>Neubauprojekte</a>', ru: '>Новостройки</a>', ar: '>المشاريع</a>' },
  { find: '>Areas</a>', es: '>Zonas</a>', fr: '>Secteurs</a>', de: '>Lagen</a>', ru: '>Районы</a>', ar: '>المناطق</a>' },
  { find: '>Advisory</a>', es: '>Asesoramiento</a>', fr: '>Conseil</a>', de: '>Beratung</a>', ru: '>Консультации</a>', ar: '>الاستشارات</a>' },
  { find: '>Contact Us</a>', es: '>Contacto</a>', fr: '>Contact</a>', de: '>Kontakt</a>', ru: '>Контакты</a>', ar: '>اتصل بنا</a>' },
  { find: 'aria-label="Nueva Living home"', es: 'aria-label="Inicio de Nueva Living"', fr: 'aria-label="Accueil Nueva Living"', de: 'aria-label="Nueva Living Startseite"', ru: 'aria-label="Главная Nueva Living"', ar: 'aria-label="الصفحة الرئيسية Nueva Living"' },
  { find: 'aria-label="Menu"', es: 'aria-label="Menú"', fr: 'aria-label="Menu"', de: 'aria-label="Menü"', ru: 'aria-label="Меню"', ar: 'aria-label="القائمة"' },

  // Footer
  { find: 'We help international buyers find and compare new-build and off-plan homes across the Costa del Sol.', es: 'Ayudamos a compradores internacionales a encontrar y comparar viviendas de obra nueva y sobre plano en toda la Costa del Sol.', fr: 'Nous aidons les acheteurs internationaux à trouver et comparer des logements neufs et sur plan sur toute la Costa del Sol.', de: 'Wir helfen internationalen Käufern, Neubau- und Off-Plan-Immobilien an der gesamten Costa del Sol zu finden und zu vergleichen.', ru: 'Мы помогаем международным покупателям находить и сравнивать новостройки и строящееся жильё по всему побережью Коста-дель-Соль.', ar: 'نساعد المشترين الدوليين في العثور على منازل جديدة وعلى المخطط ومقارنتها في جميع أنحاء كوستا ديل سول.' },
  { find: '<div class="footer-col-title">Company</div>', es: '<div class="footer-col-title">Empresa</div>', fr: '<div class="footer-col-title">Société</div>', de: '<div class="footer-col-title">Unternehmen</div>', ru: '<div class="footer-col-title">Компания</div>', ar: '<div class="footer-col-title">الشركة</div>' },
  { find: '>Why Nueva Living</a>', es: '>Por Qué Nueva Living</a>', fr: '>Pourquoi Nueva Living</a>', de: '>Warum Nueva Living</a>', ru: '>Почему Nueva Living</a>', ar: '>لماذا Nueva Living</a>' },
  { find: '>About</a>', es: '>Sobre Nosotros</a>', fr: '>À Propos</a>', de: '>Über Uns</a>', ru: '>О Нас</a>', ar: '>من نحن</a>' },
  { find: '<div class="footer-col-title">Projects</div>', es: '<div class="footer-col-title">Proyectos</div>', fr: '<div class="footer-col-title">Projets</div>', de: '<div class="footer-col-title">Projekte</div>', ru: '<div class="footer-col-title">Проекты</div>', ar: '<div class="footer-col-title">المشاريع</div>' },
  { find: '>All Developments</a>', es: '>Todas las Promociones</a>', fr: '>Tous les Programmes</a>', de: '>Alle Neubauprojekte</a>', ru: '>Все Новостройки</a>', ar: '>جميع المشاريع</a>' },
  { find: '>Areas Overview</a>', es: '>Resumen de Zonas</a>', fr: '>Aperçu des Secteurs</a>', de: '>Überblick der Lagen</a>', ru: '>Обзор Районов</a>', ar: '>نظرة عامة على المناطق</a>' },
  { find: '<div class="footer-col-title">Contact</div>', es: '<div class="footer-col-title">Contacto</div>', fr: '<div class="footer-col-title">Contact</div>', de: '<div class="footer-col-title">Kontakt</div>', ru: '<div class="footer-col-title">Контакты</div>', ar: '<div class="footer-col-title">التواصل</div>' },
  { find: '>Marbella, Spain</a>', es: '>Marbella, España</a>', fr: '>Marbella, Espagne</a>', de: '>Marbella, Spanien</a>', ru: '>Марбелья, Испания</a>', ar: '>ماربيا، إسبانيا</a>' },
  { find: '<div class="footer-col-title" style="margin-top:24px;">Legal</div>', es: '<div class="footer-col-title" style="margin-top:24px;">Legal</div>', fr: '<div class="footer-col-title" style="margin-top:24px;">Mentions Légales</div>', de: '<div class="footer-col-title" style="margin-top:24px;">Rechtliches</div>', ru: '<div class="footer-col-title" style="margin-top:24px;">Правовая Информация</div>', ar: '<div class="footer-col-title" style="margin-top:24px;">الشؤون القانونية</div>' },
  { find: '>Privacy Policy</a>', es: '>Política de Privacidad</a>', fr: '>Politique de Confidentialité</a>', de: '>Datenschutzerklärung</a>', ru: '>Политика Конфиденциальности</a>', ar: '>سياسة الخصوصية</a>' },
  { find: '>Legal Notice</a>', es: '>Aviso Legal</a>', fr: '>Mentions Légales</a>', de: '>Impressum</a>', ru: '>Юридическая Информация</a>', ar: '>إشعار قانوني</a>' },
  { find: '>Cookie Policy</a>', es: '>Política de Cookies</a>', fr: '>Politique de Cookies</a>', de: '>Cookie-Richtlinie</a>', ru: '>Политика Использования Cookie</a>', ar: '>سياسة ملفات تعريف الارتباط</a>' },
  { find: 'Information presented on this website is for general marketing purposes only and does not constitute legal, financial or investment advice. Development details, prices and delivery dates are subject to change without notice.', es: 'La información presentada en este sitio web tiene únicamente fines comerciales generales y no constituye asesoramiento legal, financiero ni de inversión. Los detalles de las promociones, precios y fechas de entrega pueden cambiar sin previo aviso.', fr: 'Les informations présentées sur ce site le sont à des fins commerciales générales uniquement et ne constituent pas un conseil juridique, financier ou en investissement. Les détails des programmes, les prix et les dates de livraison peuvent être modifiés sans préavis.', de: 'Die auf dieser Website dargestellten Informationen dienen ausschließlich allgemeinen Marketingzwecken und stellen keine Rechts-, Finanz- oder Anlageberatung dar. Projektdetails, Preise und Übergabetermine können sich ohne Vorankündigung ändern.', ru: 'Информация, представленная на этом сайте, носит исключительно общий маркетинговый характер и не является юридической, финансовой или инвестиционной консультацией. Характеристики проектов, цены и сроки сдачи могут изменяться без предварительного уведомления.', ar: 'المعلومات المعروضة على هذا الموقع هي لأغراض تسويقية عامة فقط ولا تشكل استشارة قانونية أو مالية أو استثمارية. تفاصيل المشاريع والأسعار ومواعيد التسليم قابلة للتغيير دون إشعار مسبق.' },
  { find: 'aria-label="Contact Nueva Living on WhatsApp"', es: 'aria-label="Contactar con Nueva Living por WhatsApp"', fr: 'aria-label="Contacter Nueva Living sur WhatsApp"', de: 'aria-label="Nueva Living über WhatsApp kontaktieren"', ru: 'aria-label="Связаться с Nueva Living в WhatsApp"', ar: 'aria-label="التواصل مع Nueva Living عبر واتساب"' }
];

export const DEVELOPMENTS_PAGE_ENTRIES = [
  ...PAGE_ENTRIES_HEAD,
  ...PROJECT_CARD_ENTRIES,
  ...PAGE_ENTRIES_TAIL,
  ...CHROME_ENTRIES
];

// "Show image N of M" gallery-dot aria-labels, translated as templates
// (regex-applied by the build script since N/M vary per card).
export const SHOW_IMAGE_TEMPLATES = {
  es: 'Mostrar imagen {n} de {m}',
  fr: 'Afficher l’image {n} sur {m}',
  de: 'Bild {n} von {m} anzeigen',
  ru: 'Показать изображение {n} из {m}',
  ar: 'عرض الصورة {n} من {m}'
};

// data-i18n-* runtime strings consumed by liora-discovery.js.
export const DISCOVERY_RUNTIME_STRINGS = {
  es: {
    countOne: '{count} promoción seleccionada',
    countMany: '{count} promociones seleccionadas',
    noFilters: 'Sin filtros de estilo de vida seleccionados',
    anyPrice: 'Cualquier precio',
    any: 'Cualquiera',
    searching: 'Buscando…',
    search: 'Buscar',
    aiMatching: 'Mostrando promociones que coinciden.',
    aiNoMatch: 'Ninguna promoción actual coincide con esa búsqueda.',
    aiError: 'La búsqueda con IA no está disponible ahora mismo. Prueba los filtros de abajo.'
  },
  fr: {
    countOne: '{count} programme sélectionné',
    countMany: '{count} programmes sélectionnés',
    noFilters: 'Aucun filtre de style de vie sélectionné',
    anyPrice: 'Tout prix',
    any: 'Toutes',
    searching: 'Recherche…',
    search: 'Rechercher',
    aiMatching: 'Affichage des programmes correspondants.',
    aiNoMatch: 'Aucun programme actuel ne correspond à cette recherche.',
    aiError: 'La recherche IA est indisponible pour le moment — essayez les filtres ci-dessous.'
  },
  de: {
    countOne: '{count} ausgewähltes Projekt',
    countMany: '{count} ausgewählte Projekte',
    noFilters: 'Keine Lifestyle-Filter ausgewählt',
    anyPrice: 'Jeder Preis',
    any: 'Beliebig',
    searching: 'Suche läuft…',
    search: 'Suchen',
    aiMatching: 'Passende Projekte werden angezeigt.',
    aiNoMatch: 'Kein aktuelles Projekt entspricht dieser Suche.',
    aiError: 'Die KI-Suche ist derzeit nicht verfügbar — nutzen Sie stattdessen die Filter unten.'
  },
  ru: {
    countOne: '{count} отобранный проект',
    countMany: 'Отобранных проектов: {count}',
    noFilters: 'Фильтры по образу жизни не выбраны',
    anyPrice: 'Любая цена',
    any: 'Любое число',
    searching: 'Идёт поиск…',
    search: 'Найти',
    aiMatching: 'Показаны подходящие новостройки.',
    aiNoMatch: 'Ни одна текущая новостройка не соответствует этому запросу.',
    aiError: 'ИИ-поиск сейчас недоступен — воспользуйтесь фильтрами ниже.'
  },
  ar: {
    countOne: 'مشروع مختار واحد',
    countMany: '{count} مشاريع مختارة',
    noFilters: 'لم يتم اختيار فلاتر نمط الحياة',
    anyPrice: 'أي سعر',
    any: 'أي عدد',
    searching: 'جارٍ البحث…',
    search: 'بحث',
    aiMatching: 'عرض المشاريع المطابقة.',
    aiNoMatch: 'لا يوجد مشروع حالي يطابق هذا البحث.',
    aiError: 'بحث الذكاء الاصطناعي غير متاح حاليًا — جرّب الفلاتر أدناه.'
  }
};
