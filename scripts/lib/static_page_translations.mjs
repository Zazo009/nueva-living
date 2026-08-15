// Body translations for the three hand-authored static pages that fall
// outside every render-based build pass: compare.html, thank-you.html and
// 404.html. Applied by build_static_page_locales.mjs as literal
// find/replace (longest-first), on top of the shared CHROME_ENTRIES from
// developments_page_translations.mjs.

export const THANK_YOU_ENTRIES = [
  { find: '<title>Enquiry Received | Nueva Living</title>', es: '<title>Consulta Recibida | Nueva Living</title>', fr: '<title>Demande Reçue | Nueva Living</title>', de: '<title>Anfrage Erhalten | Nueva Living</title>', ru: '<title>Запрос Получен | Nueva Living</title>', ar: '<title>تم استلام الطلب | Nueva Living</title>' },
  { find: 'Thank you for contacting Nueva Living. Your private new-development request has been received.', es: 'Gracias por contactar con Nueva Living. Hemos recibido tu solicitud privada sobre obra nueva.', fr: 'Merci d’avoir contacté Nueva Living. Votre demande privée concernant les programmes neufs a bien été reçue.', de: 'Vielen Dank für Ihre Kontaktaufnahme mit Nueva Living. Ihre private Neubau-Anfrage ist eingegangen.', ru: 'Благодарим за обращение в Nueva Living. Ваш запрос о новостройках получен.', ar: 'شكرًا لتواصلك مع Nueva Living. لقد استلمنا طلبك الخاص بالمشاريع الجديدة.' },
  { find: '<meta property="og:title" content="Enquiry Received | Nueva Living">', es: '<meta property="og:title" content="Consulta Recibida | Nueva Living">', fr: '<meta property="og:title" content="Demande Reçue | Nueva Living">', de: '<meta property="og:title" content="Anfrage Erhalten | Nueva Living">', ru: '<meta property="og:title" content="Запрос Получен | Nueva Living">', ar: '<meta property="og:title" content="تم استلام الطلب | Nueva Living">' },
  { find: 'Your private Nueva Living request has been received.', es: 'Hemos recibido tu solicitud privada de Nueva Living.', fr: 'Votre demande privée Nueva Living a bien été reçue.', de: 'Ihre private Nueva Living-Anfrage ist eingegangen.', ru: 'Ваш личный запрос в Nueva Living получен.', ar: 'تم استلام طلبك الخاص لدى Nueva Living.' },
  { find: '<li><span aria-current="page">Enquiry Received</span></li>', es: '<li><span aria-current="page">Consulta Recibida</span></li>', fr: '<li><span aria-current="page">Demande Reçue</span></li>', de: '<li><span aria-current="page">Anfrage Erhalten</span></li>', ru: '<li><span aria-current="page">Запрос Получен</span></li>', ar: '<li><span aria-current="page">تم استلام الطلب</span></li>' },
  { find: '<span class="kicker">Enquiry Received</span>', es: '<span class="kicker">Consulta Recibida</span>', fr: '<span class="kicker">Demande Reçue</span>', de: '<span class="kicker">Anfrage Erhalten</span>', ru: '<span class="kicker">Запрос Получен</span>', ar: '<span class="kicker">تم استلام الطلب</span>' },
  { find: 'Thanks, we have your <em>enquiry</em>', es: 'Gracias, hemos recibido tu <em>consulta</em>', fr: 'Merci, nous avons bien reçu votre <em>demande</em>', de: 'Danke, Ihre <em>Anfrage</em> ist bei uns', ru: 'Спасибо, ваш <em>запрос</em> у нас', ar: 'شكرًا، لقد استلمنا <em>طلبك</em>' },
  { find: 'We will review what you sent and get back to you with the right project information, current availability or a clear next step.', es: 'Revisaremos lo que nos has enviado y te responderemos con la información adecuada del proyecto, la disponibilidad actual o el siguiente paso a seguir.', fr: 'Nous examinerons votre demande et reviendrons vers vous avec les informations pertinentes sur le projet, la disponibilité actuelle ou une prochaine étape claire.', de: 'Wir prüfen Ihre Angaben und melden uns mit den passenden Projektinformationen, der aktuellen Verfügbarkeit oder einem klaren nächsten Schritt.', ru: 'Мы изучим ваш запрос и вернёмся к вам с нужной информацией о проекте, актуальным наличием или понятным следующим шагом.', ar: 'سنراجع ما أرسلته وسنعود إليك بمعلومات المشروع المناسبة أو التوافر الحالي أو خطوة تالية واضحة.' },
  { find: '<h3>What Happens Next</h3>', es: '<h3>Qué Pasa Ahora</h3>', fr: '<h3>Et Maintenant ?</h3>', de: '<h3>Wie es Weitergeht</h3>', ru: '<h3>Что Дальше</h3>', ar: '<h3>ماذا يحدث الآن</h3>' },
  { find: '<p>We check your enquiry against current availability, your preferred areas and the information you asked for.</p>', es: '<p>Contrastamos tu consulta con la disponibilidad actual, tus zonas preferidas y la información que solicitaste.</p>', fr: '<p>Nous comparons votre demande à la disponibilité actuelle, à vos secteurs préférés et aux informations demandées.</p>', de: '<p>Wir gleichen Ihre Anfrage mit der aktuellen Verfügbarkeit, Ihren bevorzugten Lagen und den gewünschten Informationen ab.</p>', ru: '<p>Мы сверяем ваш запрос с актуальным наличием, предпочитаемыми районами и запрошенной информацией.</p>', ar: '<p>نراجع طلبك مقارنةً بالتوافر الحالي والمناطق المفضلة لديك والمعلومات التي طلبتها.</p>' },
  { find: '<h3>A Personal Reply</h3>', es: '<h3>Una Respuesta Personal</h3>', fr: '<h3>Une Réponse Personnalisée</h3>', de: '<h3>Eine Persönliche Antwort</h3>', ru: '<h3>Персональный Ответ</h3>', ar: '<h3>رد شخصي</h3>' },
  { find: '<p>We will send the relevant project information or contact you to talk through the options.</p>', es: '<p>Te enviaremos la información relevante del proyecto o te contactaremos para comentar las opciones.</p>', fr: '<p>Nous vous enverrons les informations pertinentes sur le projet ou vous contacterons pour discuter des options.</p>', de: '<p>Wir senden Ihnen die relevanten Projektinformationen oder kontaktieren Sie, um die Optionen zu besprechen.</p>', ru: '<p>Мы отправим актуальную информацию о проекте или свяжемся с вами, чтобы обсудить варианты.</p>', ar: '<p>سنرسل لك معلومات المشروع ذات الصلة أو نتواصل معك لمناقشة الخيارات.</p>' },
  { find: '<h3>Need Faster Contact?</h3>', es: '<h3>¿Necesitas una Respuesta más Rápida?</h3>', fr: '<h3>Besoin d’un Contact plus Rapide ?</h3>', de: '<h3>Schnelleren Kontakt Gewünscht?</h3>', ru: '<h3>Нужен Быстрый Контакт?</h3>', ar: '<h3>هل تحتاج إلى تواصل أسرع؟</h3>' },
  { find: '>Message us on WhatsApp</a>', es: '>Escríbenos por WhatsApp</a>', fr: '>Écrivez-nous sur WhatsApp</a>', de: '>Schreiben Sie uns auf WhatsApp</a>', ru: '>Напишите нам в WhatsApp</a>', ar: '>راسلنا عبر واتساب</a>' },
  { find: '<h2 class="cta-title">Keep exploring new developments.</h2>', es: '<h2 class="cta-title">Sigue explorando la obra nueva.</h2>', fr: '<h2 class="cta-title">Continuez à explorer les programmes neufs.</h2>', de: '<h2 class="cta-title">Entdecken Sie weitere Neubauprojekte.</h2>', ru: '<h2 class="cta-title">Продолжайте знакомиться с новостройками.</h2>', ar: '<h2 class="cta-title">واصل استكشاف المشاريع الجديدة.</h2>' },
  { find: '>View Developments</a>', es: '>Ver Promociones</a>', fr: '>Voir les Programmes</a>', de: '>Neubauprojekte Ansehen</a>', ru: '>Смотреть Новостройки</a>', ar: '>عرض المشاريع</a>' }
];

export const COMPARE_ENTRIES = [
  { find: '<title>Compare Your Shortlist | Nueva Living</title>', es: '<title>Compara tu Lista | Nueva Living</title>', fr: '<title>Comparez Votre Sélection | Nueva Living</title>', de: '<title>Ihre Auswahl Vergleichen | Nueva Living</title>', ru: '<title>Сравните Вашу Подборку | Nueva Living</title>', ar: '<title>قارن قائمتك المختارة | Nueva Living</title>' },
  { find: 'Compare the Costa del Sol developments you have saved to your shortlist, side by side.', es: 'Compara lado a lado las promociones de la Costa del Sol que has guardado en tu lista.', fr: 'Comparez côte à côte les programmes de la Costa del Sol que vous avez enregistrés dans votre sélection.', de: 'Vergleichen Sie die von Ihnen gespeicherten Costa-del-Sol-Projekte direkt nebeneinander.', ru: 'Сравните сохранённые вами новостройки Коста-дель-Соль бок о бок.', ar: 'قارن مشاريع كوستا ديل سول التي حفظتها في قائمتك جنبًا إلى جنب.' },
  { find: '<li><a href="index.html">Home</a></li>', es: '<li><a href="index.html">Inicio</a></li>', fr: '<li><a href="index.html">Accueil</a></li>', de: '<li><a href="index.html">Startseite</a></li>', ru: '<li><a href="index.html">Главная</a></li>', ar: '<li><a href="index.html">الرئيسية</a></li>' },
  { find: '<li><a href="developments.html">Developments</a></li>', es: '<li><a href="developments.html">Promociones</a></li>', fr: '<li><a href="developments.html">Programmes</a></li>', de: '<li><a href="developments.html">Neubauprojekte</a></li>', ru: '<li><a href="developments.html">Новостройки</a></li>', ar: '<li><a href="developments.html">المشاريع</a></li>' },
  { find: '<li><span aria-current="page">Compare</span></li>', es: '<li><span aria-current="page">Comparar</span></li>', fr: '<li><span aria-current="page">Comparer</span></li>', de: '<li><span aria-current="page">Vergleichen</span></li>', ru: '<li><span aria-current="page">Сравнение</span></li>', ar: '<li><span aria-current="page">مقارنة</span></li>' },
  { find: '<span class="kicker">Your Shortlist</span>', es: '<span class="kicker">Tu Lista</span>', fr: '<span class="kicker">Votre Sélection</span>', de: '<span class="kicker">Ihre Auswahl</span>', ru: '<span class="kicker">Ваша Подборка</span>', ar: '<span class="kicker">قائمتك المختارة</span>' },
  { find: 'Compare your <em>saved developments</em>', es: 'Compara tus <em>promociones guardadas</em>', fr: 'Comparez vos <em>programmes enregistrés</em>', de: 'Vergleichen Sie Ihre <em>gespeicherten Projekte</em>', ru: 'Сравните <em>сохранённые новостройки</em>', ar: 'قارن <em>مشاريعك المحفوظة</em>' },
  { find: 'A side-by-side look at the projects you have saved, so you can weigh price, size and amenities without switching between pages.', es: 'Una vista comparativa de los proyectos que has guardado, para valorar precio, tamaño y servicios sin cambiar de página.', fr: 'Une vue côte à côte des projets que vous avez enregistrés, pour comparer prix, surfaces et prestations sans changer de page.', de: 'Ein direkter Vergleich der von Ihnen gespeicherten Projekte, damit Sie Preis, Größe und Ausstattung abwägen können, ohne zwischen Seiten zu wechseln.', ru: 'Сравнение сохранённых проектов бок о бок: цена, площадь и инфраструктура — без переключения между страницами.', ar: 'نظرة جنبًا إلى جنب على المشاريع التي حفظتها، لتوازن بين السعر والمساحة والمرافق دون التنقل بين الصفحات.' },
  { find: '<p class="body-copy">Loading your shortlist...</p>', es: '<p class="body-copy">Cargando tu lista...</p>', fr: '<p class="body-copy">Chargement de votre sélection...</p>', de: '<p class="body-copy">Ihre Auswahl wird geladen...</p>', ru: '<p class="body-copy">Загружаем вашу подборку...</p>', ar: '<p class="body-copy">جارٍ تحميل قائمتك...</p>' }
];

export const NOT_FOUND_ENTRIES = [
  { find: '<title>Page Not Found | Nueva Living</title>', es: '<title>Página No Encontrada | Nueva Living</title>', fr: '<title>Page Introuvable | Nueva Living</title>', de: '<title>Seite Nicht Gefunden | Nueva Living</title>', ru: '<title>Страница Не Найдена | Nueva Living</title>', ar: '<title>الصفحة غير موجودة | Nueva Living</title>' },
  { find: 'The requested Nueva Living page could not be found.', es: 'No se ha podido encontrar la página de Nueva Living solicitada.', fr: 'La page Nueva Living demandée est introuvable.', de: 'Die angeforderte Nueva Living-Seite wurde nicht gefunden.', ru: 'Запрошенная страница Nueva Living не найдена.', ar: 'تعذر العثور على صفحة Nueva Living المطلوبة.' },
  { find: '<meta property="og:title" content="Page Not Found | Nueva Living">', es: '<meta property="og:title" content="Página No Encontrada | Nueva Living">', fr: '<meta property="og:title" content="Page Introuvable | Nueva Living">', de: '<meta property="og:title" content="Seite Nicht Gefunden | Nueva Living">', ru: '<meta property="og:title" content="Страница Не Найдена | Nueva Living">', ar: '<meta property="og:title" content="الصفحة غير موجودة | Nueva Living">' },
  { find: 'This page is no longer <em>available</em>', es: 'Esta página ya no está <em>disponible</em>', fr: 'Cette page n’est plus <em>disponible</em>', de: 'Diese Seite ist nicht mehr <em>verfügbar</em>', ru: 'Эта страница больше <em>недоступна</em>', ar: 'هذه الصفحة لم تعد <em>متاحة</em>' },
  { find: 'The project or page you are looking for may have moved. Browse our current developments or contact us and we will help you find it.', es: 'El proyecto o la página que buscas puede haberse movido. Explora nuestras promociones actuales o contáctanos y te ayudaremos a encontrarlo.', fr: 'Le projet ou la page que vous recherchez a peut-être été déplacé. Parcourez nos programmes actuels ou contactez-nous et nous vous aiderons à le retrouver.', de: 'Das gesuchte Projekt oder die Seite wurde möglicherweise verschoben. Durchstöbern Sie unsere aktuellen Projekte oder kontaktieren Sie uns — wir helfen Ihnen weiter.', ru: 'Проект или страница, которую вы ищете, возможно, была перемещена. Посмотрите наши текущие новостройки или свяжитесь с нами — мы поможем её найти.', ar: 'ربما تم نقل المشروع أو الصفحة التي تبحث عنها. تصفح مشاريعنا الحالية أو تواصل معنا وسنساعدك في العثور عليها.' },
  { find: '<h2 class="cta-title">Return to the current Nueva Living collection.</h2>', es: '<h2 class="cta-title">Vuelve a la colección actual de Nueva Living.</h2>', fr: '<h2 class="cta-title">Revenez à la collection actuelle de Nueva Living.</h2>', de: '<h2 class="cta-title">Zurück zur aktuellen Nueva Living-Kollektion.</h2>', ru: '<h2 class="cta-title">Вернитесь к актуальной коллекции Nueva Living.</h2>', ar: '<h2 class="cta-title">عد إلى مجموعة Nueva Living الحالية.</h2>' },
  { find: '>View Developments</a>', es: '>Ver Promociones</a>', fr: '>Voir les Programmes</a>', de: '>Neubauprojekte Ansehen</a>', ru: '>Смотреть Новостройки</a>', ar: '>عرض المشاريع</a>' }
];

// data-i18n JSON blob for liora-compare.js's runtime strings.
export const COMPARE_RUNTIME_STRINGS = {
  es: {
    onRequest: 'A consultar', priceFrom: 'Desde {price}', bedroomsRange: '{min}-{max} dormitorios', bedroomsOne: '{n} dormitorios', toBeConfirmed: 'Por confirmar', dateLocale: 'es-ES',
    browse: 'Ver Promociones', rowPrice: 'Precio', rowBedrooms: 'Dormitorios', rowPropertyTypes: 'Tipos de propiedad', rowStatus: 'Estado', rowDelivery: 'Entrega', rowTotalUnits: 'Viviendas totales', rowAvailableUnits: 'Viviendas disponibles', rowArea: 'Zona', rowAmenities: 'Servicios',
    statusMap: { off_plan: 'Sobre plano', under_construction: 'En construcción', completed: 'Finalizado' },
    typeMap: { apartment: 'Apartamento', penthouse: 'Ático', villa: 'Villa', townhouse: 'Adosado', duplex: 'Dúplex' },
    note: 'Los precios, la disponibilidad y las fechas de entrega son orientativos y Nueva Living los reconfirma antes de cualquier reserva.',
    emptyNotSaved: 'Aún no has guardado ninguna promoción. Guarda un proyecto desde su página o tarjeta para compararlo aquí.',
    emptyNotFound: 'No hemos podido encontrar tus promociones guardadas. Puede que se hayan actualizado; prueba a navegar de nuevo.',
    emptyError: 'Los datos de comparación no están disponibles ahora mismo. Inténtalo de nuevo en breve.'
  },
  fr: {
    onRequest: 'Sur demande', priceFrom: 'À partir de {price}', bedroomsRange: '{min}-{max} chambres', bedroomsOne: '{n} chambres', toBeConfirmed: 'À confirmer', dateLocale: 'fr-FR',
    browse: 'Voir les Programmes', rowPrice: 'Prix', rowBedrooms: 'Chambres', rowPropertyTypes: 'Types de bien', rowStatus: 'Statut', rowDelivery: 'Livraison', rowTotalUnits: 'Logements au total', rowAvailableUnits: 'Logements disponibles', rowArea: 'Secteur', rowAmenities: 'Prestations',
    statusMap: { off_plan: 'Sur plan', under_construction: 'En construction', completed: 'Terminé' },
    typeMap: { apartment: 'Appartement', penthouse: 'Penthouse', villa: 'Villa', townhouse: 'Maison de ville', duplex: 'Duplex' },
    note: 'Les prix, la disponibilité et les dates de livraison sont indicatifs et reconfirmés par Nueva Living avant toute réservation.',
    emptyNotSaved: 'Vous n’avez encore enregistré aucun programme. Enregistrez un projet depuis sa page ou sa fiche pour le comparer ici.',
    emptyNotFound: 'Nous n’avons pas retrouvé vos programmes enregistrés. Ils ont peut-être été mis à jour — essayez de naviguer à nouveau.',
    emptyError: 'Les données de comparaison sont indisponibles pour le moment. Veuillez réessayer sous peu.'
  },
  de: {
    onRequest: 'Auf Anfrage', priceFrom: 'Ab {price}', bedroomsRange: '{min}-{max} Schlafzimmer', bedroomsOne: '{n} Schlafzimmer', toBeConfirmed: 'Wird bestätigt', dateLocale: 'de-DE',
    browse: 'Neubauprojekte Ansehen', rowPrice: 'Preis', rowBedrooms: 'Schlafzimmer', rowPropertyTypes: 'Immobilientypen', rowStatus: 'Status', rowDelivery: 'Übergabe', rowTotalUnits: 'Einheiten gesamt', rowAvailableUnits: 'Verfügbare Einheiten', rowArea: 'Lage', rowAmenities: 'Ausstattung',
    statusMap: { off_plan: 'Off-Plan', under_construction: 'Im Bau', completed: 'Fertiggestellt' },
    typeMap: { apartment: 'Wohnung', penthouse: 'Penthouse', villa: 'Villa', townhouse: 'Reihenhaus', duplex: 'Duplex' },
    note: 'Preise, Verfügbarkeit und Übergabetermine sind Richtwerte und werden von Nueva Living vor jeder Reservierung erneut bestätigt.',
    emptyNotSaved: 'Sie haben noch keine Projekte gespeichert. Speichern Sie ein Projekt über seine Seite oder Karte, um es hier zu vergleichen.',
    emptyNotFound: 'Wir konnten Ihre gespeicherten Projekte nicht finden. Sie wurden möglicherweise aktualisiert — versuchen Sie es erneut.',
    emptyError: 'Die Vergleichsdaten sind derzeit nicht verfügbar. Bitte versuchen Sie es in Kürze erneut.'
  },
  ru: {
    onRequest: 'По запросу', priceFrom: 'От {price}', bedroomsRange: '{min}-{max} спален', bedroomsOne: 'Спален: {n}', toBeConfirmed: 'Уточняется', dateLocale: 'ru-RU',
    browse: 'Смотреть Новостройки', rowPrice: 'Цена', rowBedrooms: 'Спальни', rowPropertyTypes: 'Типы недвижимости', rowStatus: 'Статус', rowDelivery: 'Сдача', rowTotalUnits: 'Всего резиденций', rowAvailableUnits: 'Доступно резиденций', rowArea: 'Район', rowAmenities: 'Инфраструктура',
    statusMap: { off_plan: 'На этапе строительства', under_construction: 'Строится', completed: 'Завершено' },
    typeMap: { apartment: 'Апартаменты', penthouse: 'Пентхаус', villa: 'Вилла', townhouse: 'Таунхаус', duplex: 'Дуплекс' },
    note: 'Цены, наличие и сроки сдачи являются ориентировочными и подтверждаются Nueva Living перед любым бронированием.',
    emptyNotSaved: 'Вы ещё не сохранили ни одной новостройки. Сохраните проект на его странице или карточке, чтобы сравнить его здесь.',
    emptyNotFound: 'Мы не нашли сохранённые вами проекты. Возможно, они были обновлены — попробуйте выбрать заново.',
    emptyError: 'Данные для сравнения сейчас недоступны. Пожалуйста, попробуйте чуть позже.'
  },
  ar: {
    onRequest: 'عند الطلب', priceFrom: 'ابتداءً من {price}', bedroomsRange: '{min}-{max} غرف نوم', bedroomsOne: '{n} غرف نوم', toBeConfirmed: 'قيد التأكيد', dateLocale: 'ar',
    browse: 'تصفح المشاريع', rowPrice: 'السعر', rowBedrooms: 'غرف النوم', rowPropertyTypes: 'أنواع العقارات', rowStatus: 'الحالة', rowDelivery: 'التسليم', rowTotalUnits: 'إجمالي الوحدات', rowAvailableUnits: 'الوحدات المتاحة', rowArea: 'المنطقة', rowAmenities: 'المرافق',
    statusMap: { off_plan: 'على المخطط', under_construction: 'قيد الإنشاء', completed: 'مكتمل' },
    typeMap: { apartment: 'شقة', penthouse: 'بنتهاوس', villa: 'فيلا', townhouse: 'تاون هاوس', duplex: 'دوبلكس' },
    note: 'الأسعار والتوافر ومواعيد التسليم إرشادية وتعيد Nueva Living تأكيدها قبل أي حجز.',
    emptyNotSaved: 'لم تحفظ أي مشاريع بعد. احفظ مشروعًا من صفحته أو بطاقته لمقارنته هنا.',
    emptyNotFound: 'لم نتمكن من العثور على مشاريعك المحفوظة. ربما تم تحديثها — جرّب التصفح من جديد.',
    emptyError: 'بيانات المقارنة غير متاحة حاليًا. يرجى المحاولة مرة أخرى قريبًا.'
  }
};
